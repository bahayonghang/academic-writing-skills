#!/usr/bin/env python3
"""
Path-scoped spec matching for on-demand spec injection.

Spec files under `.trellis/spec/**/*.md` MAY start with a YAML-like
frontmatter block declaring which repo paths they govern:

    ---
    name: commands-workflow
    description: workflow command conventions
    paths:
      - packages/cli/src/commands/workflow.ts
      - packages/cli/src/utils/workflow-resolver.ts
    ---

The parser is hand-rolled (house pattern, modeled on
``trellis_config.parse_simple_yaml`` — no YAML dependency) and reads only a
bounded head of each file (16 KiB / 200 lines, whichever ends first). Only
files whose first line is exactly ``---`` are considered. ``name:`` /
``description:`` single-line strings are recognized (description is reused in
index lines). ``paths:`` accepts both a block list (``- <glob>`` items) and a
flow sequence (``paths: [a, b]``).

The parser is deliberately tolerant — a spec is prose that happens to carry a
routing hint, not a config file. Unknown keys, unrecognized line shapes and
stray ``- item`` lines are ignored; block scalars (``key: >`` / ``key: |``)
consume their more-indented continuation lines, so a SKILL.md-style
``description: >`` paragraph does not disqualify the file. An opening ``---``
with no recognized key before the closing marker is not frontmatter at all
(a Markdown horizontal rule opening the prose) and is ignored silently. Two
things are errors, and both warn + skip the whole file rather than route on a
half-read block: a malformed ``paths:`` (a scalar where a list belongs — that
key is the one thing the rest of the pipeline depends on), and a frontmatter
block that is still open when the head bound is reached.

Glob grammar (repo-relative, POSIX separators):

- ``*``  matches within a single path segment (never crosses ``/``)
- ``?``  matches exactly one character within a segment
- ``**`` as a whole segment matches zero or more segments
- a trailing ``/`` is sugar for ``/**``
- ``**`` embedded in a segment with other characters degrades to ``*``

Validation rejects only what is unsafe or meaningless: empty globs, a leading
``/`` (globs are repo-relative), ``..`` segments, backslashes (POSIX
separators only) and control characters. Everything else is legal — real
repositories carry ``@scope`` packages, ``[slug]`` routes, ``(marketing)``
groups and non-ASCII directories, and the translation escapes literals
character by character. An invalid glob is skipped with a stderr warning; the
rest of the file's globs still apply.

Translation examples (glob → matches / non-matches):

    packages/cli/src/commands/update.ts
        matches only that exact file
    packages/cli/src/commands/*.ts
        matches packages/cli/src/commands/update.ts
        not     packages/cli/src/commands/channel/spawn.ts
    packages/cli/src/templates/**
        matches packages/cli/src/templates/trellis/index.ts (any depth)
        not     packages/cli/src/templates (the directory itself)
    packages/**/index.ts
        matches packages/index.ts and packages/cli/src/index.ts
    src/util?.py
        matches src/utils.py, not src/util.py or src/utilXY.py
    packages/cli/
        same as packages/cli/**

Provides:
    SpecMatch               - frozen match record (spec_path, rel_path, description)
    match_specs_for_file    - map an edited file to the specs that govern it
    normalize_repo_relative - the canonical repo-relative path normalization
    parse_spec_frontmatter  - parse the optional frontmatter head block
    glob_to_regex           - deterministic glob → compiled regex translation
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from .paths import DIR_SPEC, DIR_WORKFLOW
from .trellis_config import _strip_inline_comment, _unquote

# Bounded head-read limits for frontmatter scanning (design contract).
HEAD_MAX_BYTES = 16384
HEAD_MAX_LINES = 200

# Recognized frontmatter keys. An opening `---` block that declares none of
# them is prose under a horizontal rule, not frontmatter.
_KNOWN_KEYS = ("paths", "name", "description")

_GLOB_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")
_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")
# YAML block-scalar introducers; the value lives in the indented lines below.
_BLOCK_SCALARS = ("|", ">", "|-", ">-", "|+", ">+")

# macOS and Windows filesystems are case-insensitive: the very same file can
# be handed to us in a case the glob author never wrote. Match case-insensitively
# there — over-injecting a spec is the safe side of the asymmetry.
_CASE_INSENSITIVE_FS = sys.platform == "darwin" or sys.platform.startswith("win")
_GLOB_FLAGS = re.IGNORECASE if _CASE_INSENSITIVE_FS else 0


@dataclass(frozen=True)
class SpecFrontmatter:
    """Parsed frontmatter head. ``paths`` is None when the key is absent."""

    paths: tuple[str, ...] | None
    name: str | None
    description: str | None


@dataclass(frozen=True)
class SpecMatch:
    spec_path: Path
    """Absolute path to the spec file."""
    rel_path: str
    """Repo-relative POSIX path, for display."""
    description: str | None
    """Frontmatter ``description:`` value, if declared."""


def _warn(message: str) -> None:
    print(f"[WARN] spec_match: {message}", file=sys.stderr)


def _parse_flow_sequence(value: str) -> list[str]:
    """Split a YAML flow sequence body (``[a, b]``) into unquoted items.

    Commas separate; each item is trimmed and unquoted. Empty items (a
    trailing comma, ``[]``) collapse away.
    """
    inner = value[1:-1]
    items = (_unquote(part.strip()).strip() for part in inner.split(","))
    return [item for item in items if item]


def _read_head(path: Path) -> str:
    """Read at most HEAD_MAX_BYTES from the file, decoded as UTF-8."""
    with open(path, "rb") as f:
        data = f.read(HEAD_MAX_BYTES)
    return data.decode("utf-8", errors="replace")


def parse_spec_frontmatter(head_text: str) -> SpecFrontmatter | None:
    """Parse the optional frontmatter block from a spec file's head.

    Returns None when the file has no frontmatter: either the first line is not
    ``---``, or the block declares no recognized key before its closing marker
    (a horizontal rule opening a prose file — silent, not an error).

    Raises ValueError on a malformed ``paths:`` key (a scalar where a list
    belongs) and on a block that is still open when the head bound
    (HEAD_MAX_LINES / HEAD_MAX_BYTES) is reached — routing on a half-read
    frontmatter would be worse than skipping the file loudly. Every other line
    shape is tolerated and ignored.
    """
    lines = head_text.splitlines()[:HEAD_MAX_LINES]
    if not lines:
        return None
    first = lines[0].lstrip("\ufeff")  # tolerate a UTF-8 BOM
    if first != "---":
        return None

    paths: list[str] | None = None
    name: str | None = None
    description: str | None = None
    pending_key: str | None = None
    block_indent: int | None = None
    saw_known_key = False
    closed = False

    for line in lines[1:]:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        if block_indent is not None:
            # Inside a block scalar: everything more indented (and blank lines)
            # is its value. A dedent ends the block; that line still counts.
            if not stripped or indent > block_indent:
                continue
            block_indent = None

        if stripped == "---":
            closed = True
            break
        if not stripped or stripped.startswith("#"):
            continue

        if stripped == "-" or stripped.startswith("- "):
            if pending_key == "paths" and paths is not None:
                item = _unquote(_strip_inline_comment(stripped[1:].strip()).strip())
                paths.append(item)
            # List items outside `paths:` are tolerated and ignored.
            continue

        key_match = _KEY_RE.match(stripped)
        if key_match is None:
            continue  # Unrecognized line shape — tolerated and ignored.

        key = key_match.group(1)
        saw_known_key = saw_known_key or key in _KNOWN_KEYS
        raw_value = key_match.group(2).strip()
        if raw_value in _BLOCK_SCALARS:
            if key == "paths":
                raise ValueError("'paths' must be a list of globs")
            pending_key = None
            block_indent = indent
            continue

        value = _unquote(_strip_inline_comment(raw_value).strip())
        if value:
            pending_key = None
            if key == "paths":
                if not (value.startswith("[") and value.endswith("]")):
                    raise ValueError("'paths' must be a list of globs")
                paths = _parse_flow_sequence(value)
            elif key == "name":
                name = value
            elif key == "description":
                description = value
            # Unknown scalar keys are tolerated and ignored.
        else:
            pending_key = key
            if key == "paths":
                paths = []

    if not saw_known_key:
        # An opening `---` with no recognized key is a horizontal rule, not a
        # frontmatter block. Silent by design: prose files are not malformed.
        return None
    if not closed:
        raise ValueError(
            f"frontmatter block never closed within the head bound "
            f"({HEAD_MAX_BYTES} bytes / {HEAD_MAX_LINES} lines)"
        )

    return SpecFrontmatter(
        paths=tuple(paths) if paths is not None else None,
        name=name,
        description=description,
    )


def validate_glob(glob: str) -> str | None:
    """Return an error message for an invalid glob, or None when valid.

    Deny-list, not allow-list: only what is unsafe or meaningless is rejected
    (see module docstring). Everything else — ``@scope``, ``[slug]``,
    ``(marketing)``, non-ASCII directory names — is a legal path in a real
    repository and translates fine.
    """
    if not glob:
        return "empty glob"
    if glob.startswith("/"):
        return "absolute paths are not allowed (globs are repo-relative)"
    if ".." in glob.split("/"):
        return "'..' segments are not allowed"
    if "\\" in glob:
        return "backslashes are not allowed (globs use POSIX '/' separators)"
    if _GLOB_CONTROL_RE.search(glob):
        return "contains control characters"
    return None


def glob_to_regex(glob: str) -> re.Pattern[str]:
    """Translate a validated glob to a compiled full-match regex.

    Deterministic, segment-based translation (see module docstring for the
    grammar and examples): ``**`` as a whole segment spans zero or more
    segments; ``*`` becomes ``[^/]*``; ``?`` becomes ``[^/]``; everything
    else is escaped literally. A trailing ``/`` is expanded to ``/**`` first.
    On case-insensitive filesystems (macOS, Windows) the pattern compiles with
    ``re.IGNORECASE`` — see ``_CASE_INSENSITIVE_FS``.
    """
    if glob.endswith("/"):
        glob += "**"
    segments = glob.split("/")
    parts: list[str] = []
    for i, seg in enumerate(segments):
        is_last = i == len(segments) - 1
        if seg == "**":
            # Last: consume the rest of the path (at least the separator
            # boundary is already emitted by the previous segment). Not last:
            # zero or more whole segments including their separators.
            parts.append(".*" if is_last else r"(?:[^/]+/)*")
            continue
        piece = "".join(
            "[^/]*" if ch == "*" else "[^/]" if ch == "?" else re.escape(ch)
            for ch in seg
        )
        parts.append(piece if is_last else piece + "/")
    return re.compile("^" + "".join(parts) + "$", _GLOB_FLAGS)


def normalize_repo_relative(repo_root: Path, file_path: str | Path) -> str | None:
    """Canonical repo-relative POSIX path — the one normalization in the
    pipeline, used both for matching and for display.

    Root and file are fully resolved (``strict=False``, so a file that no
    longer exists still normalizes): symlinked repo roots, macOS's
    ``/tmp`` → ``/private/tmp`` and ``..`` segments cannot make one file look
    like two different paths. The result is NFC-normalized (macOS hands out
    NFD filenames). Relative inputs are taken as repo-relative. Returns None
    when the file resolves outside the repo.
    """
    try:
        root = Path(repo_root).resolve(strict=False)
        candidate = Path(file_path)
        if not candidate.is_absolute():
            text = str(file_path).replace("\\", "/")
            while text.startswith("./"):
                text = text[2:]
            if not text:
                return None
            candidate = root / text
        rel = candidate.resolve(strict=False).relative_to(root).as_posix()
    except (OSError, ValueError):
        return None
    return unicodedata.normalize("NFC", rel)


def match_specs_for_file(repo_root: Path, file_path: str | Path) -> list[SpecMatch]:
    """Return specs whose frontmatter ``paths:`` globs match file_path.

    ``file_path`` may be absolute or repo-relative. More specific matching
    globs are returned first; ``rel_path`` is the deterministic tie-break.
    Scans ``.trellis/spec/**/*.md`` with bounded head-reads only. Never raises;
    unreadable or malformed spec files are skipped with a stderr warning.
    """
    try:
        repo_root = Path(repo_root).resolve()
        spec_dir = repo_root / DIR_WORKFLOW / DIR_SPEC
        if not spec_dir.is_dir():
            return []
        rel = normalize_repo_relative(repo_root, file_path)
        if rel is None:
            return []

        matches: list[SpecMatch] = []
        specificity: dict[str, tuple[int, int, int, int]] = {}
        for spec_file in spec_dir.rglob("*.md"):
            spec_rel = spec_file.relative_to(repo_root).as_posix()
            try:
                head = _read_head(spec_file)
            except OSError as exc:
                _warn(f"cannot read {spec_rel}: {exc}")
                continue
            try:
                frontmatter = parse_spec_frontmatter(head)
            except ValueError as exc:
                _warn(f"malformed frontmatter in {spec_rel}: {exc}")
                continue
            if frontmatter is None or not frontmatter.paths:
                continue
            for glob in frontmatter.paths:
                error = validate_glob(glob)
                if error is not None:
                    _warn(f"invalid glob {glob!r} in {spec_rel}: {error}")
                    continue
                if glob_to_regex(glob).match(rel):
                    scored_glob = glob + "**" if glob.endswith("/") else glob
                    wildcard_count = scored_glob.count("*") + scored_glob.count("?")
                    segments = scored_glob.split("/")
                    literal_segments = sum(
                        "*" not in segment and "?" not in segment
                        for segment in segments
                    )
                    specificity[spec_rel] = (
                        0 if wildcard_count == 0 else 1,
                        -literal_segments,
                        wildcard_count,
                        -(len(scored_glob) - wildcard_count),
                    )
                    matches.append(
                        SpecMatch(
                            spec_path=spec_file,
                            rel_path=spec_rel,
                            description=frontmatter.description,
                        )
                    )
                    break

        # Payload assembly spends its budget in this order. Exact and narrowly
        # scoped matches must therefore outrank broad tree globs; alphabetic
        # order is only a deterministic tie-break.
        matches.sort(key=lambda m: (*specificity[m.rel_path], m.rel_path))
        return matches
    except Exception as exc:  # Never raise — callers are hooks/context tools.
        _warn(f"spec scan failed: {exc}")
        return []
