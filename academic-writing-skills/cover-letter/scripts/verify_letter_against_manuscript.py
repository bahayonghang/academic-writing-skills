"""Verify cover-letter claim quotes can be located in the manuscript source.

Adapted from ``paper-audit/scripts/verify_quotes.py``. The cover-letter
specialization is in the matching strategy:

* exact substring match against the manuscript's visible prose (post-LaTeX-strip)
* numeric + metric-keyword fallback (e.g. "47% reduction in latency" matches
  manuscript text containing "47%" and "latency" within the same paragraph)
* paraphrase tolerance: a 4-gram from the letter claim matching the manuscript
  is treated as ``quote_verified=true`` with confidence demoted to "medium"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from build_letter_claim_map import NUMBER_UNIT_PATTERN
from parsers import LatexParser

UNVERIFIED_CONFIDENCE = "unverified"

# A claim number and its metric keyword must co-occur within this many characters
# of manuscript prose (≈ a sentence / short paragraph). The previous check
# accepted the number appearing anywhere and the keyword appearing anywhere in
# the whole document, which silently "verified" fabricated combinations such as
# "73% reduction in memory" when the manuscript only had an unrelated "73%" and
# a separate "reduction".
_NUMERIC_WINDOW = 160

# Metric words that carry the *identity* of what a number measures. When one of
# these sits next to a number in the letter claim, the manuscript window around
# that same number must contain it too — "3% throughput improvement" must not
# verify against a manuscript that only reports "3% accuracy improvement"
# (CL-1). Direction-only words (reduction / improvement) name no metric, so
# they use the tighter `_DIRECTION_RE` / `_DIRECTION_WINDOW` gate below instead
# (A-CL-4); a claim with neither a specific metric nor a direction word keeps
# the loosest any-keyword gate further down.
_SPECIFIC_METRIC_RE = re.compile(
    r"\b(?:accuracy|f1|auc|precision|recall|rmse|mae|latency|throughput|"
    r"speedup|error|memory|footprint|cost|savings|modalit(?:y|ies))\b",
    re.IGNORECASE,
)
# How far (in characters) from the number, inside the letter claim, a specific
# metric word may sit and still count as naming that number.
_CLAIM_METRIC_WINDOW = 40

# Direction-only words name no metric identity, so they cannot use
# `_SPECIFIC_METRIC_RE`'s all-must-match gate above. The original code left
# them on the *loosest* gate (`_NUMERIC_WINDOW` = 160, any-keyword — see
# `metric_keywords` in `_has_numeric_match`), which let a direction word
# anywhere in that wide neighborhood "verify" a number it does not actually
# describe (A-CL-4). Mirror `local_specific`'s mechanism with a tighter,
# direction-specific window instead.
_DIRECTION_RE = re.compile(r"\b(?:reduction|improvement)\b", re.IGNORECASE)
# A direction noun usually sits in the same clause as the number it modifies;
# 60 characters is roughly one clause (vs. the 160-char loose fallback).
_DIRECTION_WINDOW = 60


def _strip_manuscript(content: str) -> str:
    """Return manuscript text after stripping LaTeX markup for matching."""
    parser = LatexParser()
    return parser.clean_text(content)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _has_4gram_match(claim: str, manuscript: str) -> bool:
    """Return True if any 4-gram from the claim appears in the manuscript."""
    claim_tokens = re.findall(r"\b[\w'-]+\b", claim.lower())
    if len(claim_tokens) < 4:
        return False
    manuscript_normalized = " ".join(re.findall(r"\b[\w'-]+\b", manuscript.lower()))
    for i in range(len(claim_tokens) - 3):
        fragment = " ".join(claim_tokens[i : i + 4])
        if fragment in manuscript_normalized:
            return True
    return False


def _has_numeric_match(claim: str, manuscript: str) -> bool:
    """Return True when a number in the claim appears in the manuscript with a
    matching metric keyword nearby (within ``_NUMERIC_WINDOW`` characters).

    Every specific metric word adjacent to the number in the claim (within
    ``_CLAIM_METRIC_WINDOW`` characters) must also appear in the manuscript
    window — the letter cannot re-attach a manuscript number to a different
    metric (CL-1). A direction-only claim (reduction/improvement, no specific
    metric word) instead requires the direction word within
    ``_DIRECTION_WINDOW`` of the number in the manuscript (A-CL-4). Claims with
    neither keep the original any-keyword co-occurrence gate."""
    number_patterns = (
        NUMBER_UNIT_PATTERN,
        r"(?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?\b",
        r"\b\d+(?:\.\d+)?\s+(?:sensor\s+)?modalit(?:y|ies)\b",
        r"\b\d+(?:\.\d+)?\s+(?:datasets?|benchmarks?|studies|facilit(?:y|ies))\b",
    )
    numbers: list[str] = []
    for pattern in number_patterns:
        numbers.extend(re.findall(pattern, claim, flags=re.IGNORECASE))
    # This keyword set is `_SPECIFIC_METRIC_RE ∪ _DIRECTION_RE` — every word it
    # matches is handled by one of the two tighter co-occurrence branches below;
    # a metric word that belonged to neither would silently fall through to the
    # loosest any-keyword gate.
    metric_keywords = re.findall(
        r"\b(?:accuracy|f1|auc|precision|recall|rmse|mae|latency|throughput|"
        r"speedup|error|reduction|improvement|memory|footprint|cost|savings|modalit(?:y|ies))\b",
        claim,
        flags=re.IGNORECASE,
    )
    if not numbers:
        return False
    # Collapse whitespace (do NOT delete it) so character offsets stay meaningful
    # for the proximity window while "12 sensor modalities" still matches.
    manuscript_norm = re.sub(r"\s+", " ", manuscript.lower().replace("\\", ""))
    claim_norm = re.sub(r"\s+", " ", claim.lower().replace("\\", ""))
    keywords = [kw.lower() for kw in metric_keywords]
    for number in numbers:
        needle = re.sub(r"\s+", " ", number.lower().replace("\\", "")).strip()
        if not needle:
            continue
        # Specific metric words that sit next to this number in the claim name
        # what the number measures; verification must find all of them again.
        local_specific: set[str] = set()
        local_direction: set[str] = set()
        claim_idx = claim_norm.find(needle)
        if claim_idx != -1:
            local_lo = max(0, claim_idx - _CLAIM_METRIC_WINDOW)
            local_hi = claim_idx + len(needle) + _CLAIM_METRIC_WINDOW
            local_window = claim_norm[local_lo:local_hi]
            local_specific = {
                match.group(0).lower() for match in _SPECIFIC_METRIC_RE.finditer(local_window)
            }
            local_direction = {
                match.group(0).lower() for match in _DIRECTION_RE.finditer(local_window)
            }
        start = 0
        while True:
            idx = manuscript_norm.find(needle, start)
            if idx == -1:
                break
            lo = max(0, idx - _NUMERIC_WINDOW)
            hi = idx + len(needle) + _NUMERIC_WINDOW
            window = manuscript_norm[lo:hi]
            if local_specific:
                if all(kw in window for kw in local_specific):
                    return True
            elif local_direction:
                direction_lo = max(0, idx - _DIRECTION_WINDOW)
                direction_hi = idx + len(needle) + _DIRECTION_WINDOW
                direction_window = manuscript_norm[direction_lo:direction_hi]
                if all(kw in direction_window for kw in local_direction):
                    return True
            elif keywords:
                if any(kw in window for kw in keywords):
                    return True
            else:
                # A bare number with no metric keyword in the claim can only be
                # checked for presence (e.g. "2.1x faster" has no listed keyword).
                return True
            start = idx + len(needle)
    return False


def verify_claim(claim: str, manuscript_text: str) -> tuple[bool, str]:
    """Verify a single claim against the manuscript.

    Returns ``(verified, confidence)``. Confidence ladder:
    * ``high`` — exact substring match (normalized).
    * ``medium`` — 4-gram or numeric+metric match.
    * ``unverified`` — no anchor found.
    """
    claim_norm = _normalize(claim)
    manuscript_norm = _normalize(manuscript_text)

    # Trim very short claims; they false-positive.
    if len(claim_norm) < 12:
        return False, UNVERIFIED_CONFIDENCE

    if claim_norm in manuscript_norm:
        return True, "high"
    if _has_numeric_match(claim, manuscript_text):
        return True, "medium"
    if _has_4gram_match(claim, manuscript_text):
        return True, "medium"
    return False, UNVERIFIED_CONFIDENCE


def verify_claim_candidates(
    candidates: list[dict],
    manuscript_text: str,
) -> list[dict]:
    """Annotate claim candidates with quote_verified + confidence."""
    manuscript_clean = _strip_manuscript(manuscript_text)
    updated: list[dict] = []
    for candidate in candidates:
        verified, confidence = verify_claim(candidate.get("claim", ""), manuscript_clean)
        patched = dict(candidate)
        patched["quote_verified"] = verified
        patched["confidence"] = confidence
        # Downgrade claim_strength to "unsupported" when the manuscript truly
        # cannot anchor the claim.
        if not verified and patched.get("claim_strength") in {"supported", "strong"}:
            patched["claim_strength"] = "observed"
        # A bare headline-number anchor (context-free "3%" match) is strictly
        # weaker evidence than the targeted verification that just failed above
        # — metric identity was checked against the full manuscript. Do not let
        # it veto the align-check finding (CL-1). Contribution-overlap support
        # implies a shared 4-gram, which would have verified the quote, so only
        # the weak numeric anchor can reach this state.
        if not verified and patched.get("manuscript_supported"):
            patched["manuscript_supported"] = False
        updated.append(patched)
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify cover-letter claim quotes against the manuscript source"
    )
    parser.add_argument(
        "claim_map",
        help="Path to claim_map.json emitted by build_letter_claim_map.py",
    )
    parser.add_argument(
        "manuscript",
        help="Path to the manuscript .tex source",
    )
    parser.add_argument("--output", "-o", help="Optional output path for verified map")
    parser.add_argument(
        "--write-back",
        action="store_true",
        help="Overwrite the claim_map file with verified annotations",
    )
    args = parser.parse_args(argv)

    claim_map_path = Path(args.claim_map).resolve()
    manuscript_path = Path(args.manuscript).resolve()
    if not claim_map_path.exists():
        print(f"File not found: {args.claim_map}", file=sys.stderr)
        return 2
    if not manuscript_path.exists():
        print(f"File not found: {args.manuscript}", file=sys.stderr)
        return 2

    claim_map = json.loads(claim_map_path.read_text(encoding="utf-8"))
    manuscript_text = manuscript_path.read_text(encoding="utf-8", errors="replace")

    candidates = claim_map.get("claim_candidates", [])
    verified = verify_claim_candidates(candidates, manuscript_text)
    claim_map["claim_candidates"] = verified
    claim_map["verified_count"] = sum(1 for c in verified if c.get("quote_verified"))
    claim_map["unverified_count"] = sum(1 for c in verified if not c.get("quote_verified"))
    # verify_claim_candidates may clear manuscript_supported (CL-1); refresh the
    # aggregate emitted by build_letter_claim_map so the map stays consistent.
    claim_map["manuscript_supported_count"] = sum(
        1 for c in verified if c.get("manuscript_supported")
    )

    payload = json.dumps(claim_map, indent=2, ensure_ascii=False)

    if args.write_back:
        claim_map_path.write_text(payload, encoding="utf-8")
    elif args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    return 0 if claim_map["unverified_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
