#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decision logic for path-scoped spec injection (ticket-refresh model).

Pure logic only: the per-spec decision engine, block rendering and budgeted
payload assembly. Importing this module has no side effects; every piece of IO
orchestration (stdin, config, identity, state files, locking, GC) lives in the
platform hook that calls it. Unit tests import this module directly.

Clock
    The periodic refresh window uses epoch seconds. Context resets are
    explicit lifecycle events: the hook records an opaque reset identifier,
    and a mismatch with the last emission re-teaches the spec in full.

Budget
    All caps are in characters, because the platform's ``additionalContext``
    ceiling is 10,000 *characters* (counting bytes made CJK specs pay 3x).
    Truncation slices code points, which can never split a multi-byte
    sequence. The per-event cap is enforced on the assembled payload string —
    wrappers, ``\\n\\n`` separators, index block and tickets all counted — so
    nothing is ever appended unchecked.
"""

from __future__ import annotations

import hashlib
import sys
from typing import Any, Sequence

from .spec_match import SpecMatch

# Bound on the size of a spec file we are willing to read and hash. A spec
# larger than this degrades to an index line (warned) — an inlined body that
# big could never fit the budget anyway, and the read+hash would be unbounded.
MAX_SPEC_SOURCE_BYTES = 10 * 1024 * 1024

# Upper bound on the room reserved for named index lines while FULL blocks are
# still being packed. Beyond it the reserve falls back to the summary line
# alone: a big fan-out must not starve the specs that can still be taught.
INDEX_RESERVE_MAX_CHARS = 900

# State record schema version. Records with any other version are ignored
# (safe direction: an ignored record re-injects rather than stays silent).
STATE_VERSION = 2

def _warn(message: str) -> None:
    print(f"[WARN] spec_inject: {message}", file=sys.stderr)


# =============================================================================
# Clock
# =============================================================================


def within_window(
    clock: dict[str, Any],
    last: dict[str, Any],
    win_seconds: int,
) -> bool:
    """True when the last emission is still inside the refresh window (→ stay
    silent).

    A window of ``0`` means never refresh (infinite window → always True).
    Missing timestamps or a negative delta are past-window (False → refresh),
    the safe side of the misfire asymmetry.
    """
    cur_ts = clock.get("ts")
    last_ts = last.get("ts")
    if isinstance(cur_ts, (int, float)) and isinstance(last_ts, (int, float)):
        if win_seconds == 0:
            return True
        delta = cur_ts - last_ts
        return 0 <= delta < win_seconds

    return False


def decide(
    stateless: bool,
    last: dict[str, Any] | None,
    sha256_hex: str,
    clock: dict[str, Any],
    win_seconds: int,
) -> str:
    """Return one of ``"full"`` | ``"ticket"`` | ``"silent"`` for a spec.

    Order is contractual: statelessness first (bounded cost, no state to
    consult), then first sight, content change, context reset, the refresh
    window, and finally completeness. A ticket says "you were shown this spec",
    which is a lie when the recorded FULL was truncated, so an incomplete
    record is re-taught in full instead.
    """
    if stateless:
        return "ticket"
    if last is None:
        return "full"
    if last.get("sha256") != sha256_hex:
        return "full"
    if clock.get("reset") != last.get("reset"):
        return "full"

    if within_window(clock, last, win_seconds):
        return "silent"

    # "complete" is optional and absent means a whole body was shown.
    if last.get("complete") is False:
        return "full"
    return "ticket"


# =============================================================================
# Rendering
# =============================================================================


def truncate_chars(text: str, cap: int) -> str:
    """Slice ``text`` to at most ``cap`` code points. ``cap <= 0`` = no limit."""
    if cap <= 0 or len(text) <= cap:
        return text
    return text[:cap]


def truncation_notice(rel_path: str, cap: int) -> str:
    return (
        f"\n[Trellis: truncated at {cap} characters — "
        f"read {rel_path} for the full content]"
    )


def render_full(edited_rel: str, spec_rel: str, sha12: str, body: str) -> str:
    return (
        f'<spec-context file="{edited_rel}" spec="{spec_rel}" sha256="{sha12}">\n'
        f"{body}\n"
        f"</spec-context>"
    )


def render_ticket(
    edited_rel: str,
    spec_rel: str,
    sha12: str,
    stateless: bool,
) -> str:
    """Render a ticket block.

    ``stateless=True`` covers both the no-identity and circuit-breaker paths:
    there is no record of a prior emission, so the wording must not claim one.
    """
    if stateless:
        body = (
            "This spec governs the file you just touched. If you have not read it in\n"
            f"this session, Read {spec_rel} before continuing."
        )
    else:
        body = (
            "You were shown this spec earlier in this session and its content is unchanged.\n"
            "It still governs edits to matching files. If you no longer remember it, Read\n"
            f"{spec_rel} before continuing."
        )
    return (
        f'<spec-ticket file="{edited_rel}" spec="{spec_rel}" sha256="{sha12}">\n'
        f"{body}\n"
        f"</spec-ticket>"
    )


def _index_block(lines: Sequence[str]) -> str:
    return "<spec-index>\n" + "\n".join(lines) + "\n</spec-index>"


# =============================================================================
# State records
# =============================================================================


def make_record(
    rel_path: str,
    sha256_hex: str,
    mode: str,
    clock: dict[str, Any],
    complete: bool = True,
) -> dict[str, Any]:
    """Build a state record. ``complete=False`` marks a FULL whose body was
    truncated below the whole spec — an absent flag means whole."""
    record: dict[str, Any] = {
        "v": STATE_VERSION,
        "spec": rel_path,
        "sha256": sha256_hex,
        "mode": mode,
        "ts": clock.get("ts"),
    }
    if isinstance(clock.get("reset"), str):
        record["reset"] = clock["reset"]
    if not complete:
        record["complete"] = False
    return record


# =============================================================================
# Payload assembly
# =============================================================================


def _derive_fitting_full(
    edited_rel: str,
    spec_rel: str,
    sha12: str,
    text: str,
    max_spec_chars: int,
    fits,
) -> tuple[str, bool] | None:
    """Largest truncated FULL block that fits the remaining total budget.

    Binary search over the body cap: the rendered block's length is monotone
    non-decreasing in the cap, so the largest cap whose block still ``fits``
    is found in ~log2(len(text)) renders (this also absorbs the digit-length
    wobble of the notice text, which a closed-form estimate cannot).

    The search ceiling is ``max_spec_chars`` when set and the whole body when
    it is ``0`` (unlimited) — with a ceiling of 1, as an unguarded
    ``max(1, 0)`` would give, nothing but a one-character spec could ever be
    derived. Returns ``(block, complete)`` — ``complete`` is True only when
    the winning cap covered the whole body — or None when no non-empty prefix
    fits (the caller degrades to an index line).
    """
    def candidate_for(cap: int) -> str:
        body = truncate_chars(text, cap)
        if len(body) < len(text):
            body += truncation_notice(spec_rel, cap)
        return render_full(edited_rel, spec_rel, sha12, body)

    ceiling = len(text) if max_spec_chars <= 0 else min(max_spec_chars, len(text))
    lo, hi = 1, max(1, ceiling)
    best: tuple[str, bool] | None = None
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = candidate_for(mid)
        if fits(candidate):
            best = (candidate, mid >= len(text))
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def _index_line(match: SpecMatch) -> str:
    return f"- {match.rel_path} — {match.description or 'no description'}"


def assemble_payload(
    edited_rel: str,
    matches: Sequence[SpecMatch],
    stateless: bool,
    state_records: dict[str, dict[str, Any]],
    clock: dict[str, Any],
    max_spec_chars: int,
    max_total_chars: int,
    win_seconds: int,
    match_files: dict[str, str] | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """Assemble the additionalContext payload from the matched specs.

    Returns ``(payload, records)`` where ``records`` are the state lines to
    append for the emissions that actually made it into the payload (silent
    hits and budget-dropped emissions record nothing — they stay eligible).

    Every candidate block is measured against the *assembled* payload string
    (``"\\n\\n".join(...)``), so the per-event character ceiling holds for the
    exact string that is emitted.

    ``match_files`` maps a governing spec to the first matching file in a
    multi-file tool call. Single-file callers omit it and retain the original
    ``edited_rel`` behavior.
    """
    blocks: list[str] = []

    def file_for(match: SpecMatch) -> str:
        return (match_files or {}).get(match.rel_path, edited_rel)

    def fits(candidate: str, reserve: int = 0) -> bool:
        """Does ``candidate`` fit the per-event ceiling, keeping ``reserve``
        characters free for what still has to be appended after it?"""
        if max_total_chars <= 0:
            return True
        return len("\n\n".join([*blocks, candidate])) + reserve <= max_total_chars

    # Reserve while candidates are still pending: the index lines those
    # candidates would actually need (true strings, not estimates) plus the
    # summary line — so a derived-cap FULL cannot eat the budget and starve
    # the specs behind it (measured: 10-spec fan-out at max_total_chars 3000
    # emitted one 3000-char FULL and dropped the other nine silently). The
    # named part is only guaranteed within INDEX_RESERVE_MAX_CHARS; beyond
    # that the reserve falls back to the summary line alone.
    _all_index_lines = [_index_line(m) for m in matches]
    _summary_upper = (
        f"- (+{len(matches)} more governing specs over budget — run "
        f"python ./.trellis/scripts/get_context.py --mode spec "
        f"--file {edited_rel} to list them)"
    )
    _summary_reserve = len("\n\n" + _index_block([_summary_upper]))

    def reserve_for(pending: Sequence[str]) -> int:
        if not pending:
            return 0  # Nothing can follow this block — nothing to reserve.
        named = len("\n\n" + _index_block([*pending, _summary_upper]))
        if named > INDEX_RESERVE_MAX_CHARS:
            return _summary_reserve
        return named

    index_lines: list[str] = []
    ticket_pending: list[tuple[str, str, str]] = []  # (file, spec, sha256)
    records: list[dict[str, Any]] = []

    for match_idx, match in enumerate(matches):
        try:
            size = match.spec_path.stat().st_size
        except OSError:
            size = 0
        if size > MAX_SPEC_SOURCE_BYTES:
            # Too big to read+hash, let alone inline: name it and move on.
            _warn(
                f"{match.rel_path} is {size} bytes (over "
                f"{MAX_SPEC_SOURCE_BYTES}) — degraded to an index line"
            )
            index_lines.append(_index_line(match))
            continue

        try:
            data = match.spec_path.read_bytes()
        except OSError:
            _warn(f"cannot read {match.rel_path} — skipped")
            continue

        sha256_hex = hashlib.sha256(data).hexdigest()
        sha12 = sha256_hex[:12]
        last = None if stateless else state_records.get(match.rel_path)
        decision = decide(stateless, last, sha256_hex, clock, win_seconds)

        if decision == "silent":
            continue

        if decision == "ticket":
            # Deferred: tickets are counted against the budget last.
            ticket_pending.append((file_for(match), match.rel_path, sha256_hex))
            continue

        pending = [*index_lines, *_all_index_lines[match_idx + 1 :]]
        reserve = reserve_for(pending)
        _fits = (lambda c: fits(c, reserve))

        text = data.decode("utf-8", errors="replace")
        body = truncate_chars(text, max_spec_chars)
        complete = len(body) >= len(text)
        if not complete:
            body += truncation_notice(match.rel_path, max_spec_chars)
        matching_file = file_for(match)
        block = render_full(matching_file, match.rel_path, sha12, body)
        if not _fits(block):
            # Contract amendment 1: before degrading, truncate FURTHER to the
            # largest body prefix that fits the remaining total budget
            # (wrapper + notice counted). Without this, the frozen defaults
            # made the truncation path unreachable (body cap + notice +
            # wrapper > total cap) and long specs fell straight to an index
            # line — the rejected index-only mode by another route.
            derived = _derive_fitting_full(
                matching_file,
                match.rel_path,
                sha12,
                text,
                max_spec_chars,
                _fits,
            )
            if derived is not None:
                derived_block, derived_complete = derived
                blocks.append(derived_block)
                records.append(
                    make_record(
                        match.rel_path, sha256_hex, "full", clock, derived_complete
                    )
                )
                continue
            # No usable prefix fits — degrade to an index line, never drop
            # silently. Not recorded: stays eligible for a later event.
            index_lines.append(_index_line(match))
            continue
        blocks.append(block)
        records.append(
            make_record(match.rel_path, sha256_hex, "full", clock, complete)
        )

    if index_lines:
        # The index block is budget-bounded too: lines that do not fit collapse
        # into one summary line (count + how to list them via pull mode) so the
        # ceiling is honored without silently dropping a governing spec.
        chosen: list[str] = []
        dropped = 0
        for line in index_lines:
            if fits(_index_block([*chosen, line])):
                chosen.append(line)
            else:
                dropped += 1
        if dropped:
            # Contract amendment 3: the summary must actually be reachable.
            # Greedy packing rarely leaves a summary-sized gap, so pop chosen
            # lines (re-counting them as dropped) until the summary fits —
            # only an absurdly small total budget can drop it entirely.
            while True:
                noun = "spec" if dropped == 1 else "specs"
                summary = (
                    f"- (+{dropped} more governing {noun} over budget — run "
                    f"python ./.trellis/scripts/get_context.py --mode spec "
                    f"--file {edited_rel} to list them)"
                )
                if fits(_index_block([*chosen, summary])):
                    chosen.append(summary)
                    break
                if not chosen:
                    _warn(
                        f"spec index summary for {edited_rel} dropped — "
                        f"per-event budget exhausted"
                    )
                    break
                chosen.pop()
                dropped += 1
        if chosen:
            blocks.append(_index_block(chosen))

    for matching_file, spec_rel, sha256_hex in ticket_pending:
        ticket = render_ticket(
            matching_file, spec_rel, sha256_hex[:12], stateless
        )
        if not fits(ticket):
            _warn(f"ticket for {spec_rel} dropped — per-event budget exhausted")
            continue
        blocks.append(ticket)
        records.append(make_record(spec_rel, sha256_hex, "ticket", clock))

    return "\n\n".join(blocks), records
