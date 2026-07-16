"""Balanced BibTeX scanner vendored from bib-search-citation/search_bib.py.

Keep these parsing helpers synchronized with the source scanner. Search-only
features such as crossref inheritance, duplicate-key ranking, and scoring are
intentionally excluded from this skill-local copy.
"""

from __future__ import annotations

import re
from typing import Any


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    brace_depth = 0
    paren_depth = 0
    in_quotes = False
    escaped = False

    for char in text:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            current.append(char)
            escaped = True
            continue
        if in_quotes:
            if char == '"':
                in_quotes = False
            current.append(char)
            continue
        if char == '"' and brace_depth == 0:
            in_quotes = True
            current.append(char)
            continue
        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth = max(0, brace_depth - 1)
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth = max(0, paren_depth - 1)
        elif char == delimiter and brace_depth == 0 and paren_depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def resolve_field_value(value: str, macros: dict[str, str]) -> str:
    """Expand @string macros and ``#`` concatenation."""
    value = value.strip().rstrip(",").strip()
    if "#" not in value:
        return _resolve_value_atom(value, macros)
    return "".join(_resolve_value_atom(part, macros) for part in split_top_level(value, "#"))


def _resolve_value_atom(atom: str, macros: dict[str, str]) -> str:
    atom = atom.strip()
    if not atom:
        return ""
    if len(atom) >= 2 and (
        (atom[0] == '"' and atom[-1] == '"') or (atom[0] == "{" and atom[-1] == "}")
    ):
        return atom[1:-1]
    if atom.isdigit():
        return atom
    return macros.get(atom.lower(), atom)


def parse_fields(body: str, macros: dict[str, str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for chunk in split_top_level(body):
        if not chunk or "=" not in chunk:
            continue
        name, value = chunk.split("=", 1)
        fields[name.strip().lower()] = resolve_field_value(value, macros)
    return fields


def _scan_entry_span(content: str, start: int, opener: str, closer: str) -> tuple[int, bool]:
    """Return ``(end_pos, closed)`` for a balanced entry body."""
    pos = start
    depth = 1
    in_quotes = False
    escaped = False
    while pos < len(content) and depth > 0:
        char = content[pos]
        if escaped:
            escaped = False
            pos += 1
            continue
        if char == "\\":
            escaped = True
            pos += 1
            continue
        if in_quotes:
            if char == '"':
                in_quotes = False
            pos += 1
            continue
        if char == '"' and depth == 1:
            in_quotes = True
            pos += 1
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
        pos += 1
    return pos, depth == 0


def _line_of(content: str, index: int) -> int:
    return content.count("\n", 0, index) + 1


def _find_key_separator(inner: str) -> int | None:
    brace_depth = 0
    paren_depth = 0
    in_quotes = False
    escaped = False
    for offset, char in enumerate(inner):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if in_quotes:
            if char == '"':
                in_quotes = False
            continue
        if char == '"' and brace_depth == 0:
            in_quotes = True
            continue
        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth = max(0, brace_depth - 1)
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth = max(0, paren_depth - 1)
        elif char == "," and brace_depth == 0 and paren_depth == 0:
            return offset
    return None


def parse_bib_entries(
    content: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    """Parse entries, warnings, and ``@string`` macros from BibTeX text."""
    entries: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    macros: dict[str, str] = {}
    idx = 0

    while idx < len(content):
        at = content.find("@", idx)
        if at == -1:
            break
        type_match = re.match(r"@\s*([A-Za-z]+)\s*([\{\(])", content[at:])
        if not type_match:
            idx = at + 1
            continue
        entry_type = type_match.group(1).lower()
        opener = type_match.group(2)
        closer = "}" if opener == "{" else ")"
        body_start = at + type_match.end()
        pos, closed = _scan_entry_span(content, body_start, opener, closer)

        if not closed:
            line = _line_of(content, at)
            warnings.append(
                {
                    "type": "unbalanced_entry",
                    "start_line": line,
                    "message": (
                        f"entry starting at line {line} is missing a closing '{closer}'; "
                        "skipped to the next entry"
                    ),
                }
            )
            resync = re.search(r"(?m)^\s*@", content[at + 1 :])
            idx = at + 1 + resync.start() if resync else len(content)
            continue

        raw_entry = content[at:pos].strip()
        inner = raw_entry[raw_entry.find(opener) + 1 : -1].strip()
        if entry_type in {"comment", "preamble"}:
            idx = pos
            continue
        if entry_type == "string":
            for name, value in parse_fields(inner, macros).items():
                macros[name.lower()] = value
            idx = pos
            continue

        comma = _find_key_separator(inner)
        if comma is None:
            idx = pos
            continue
        key = inner[:comma].strip()
        fields = parse_fields(inner[comma + 1 :].strip().rstrip(","), macros)
        line_start = content.rfind("\n", 0, at) + 1
        if content[line_start:at].lstrip().startswith("%"):
            line = _line_of(content, at)
            warnings.append(
                {
                    "type": "commented_entry_included",
                    "key": key,
                    "start_line": line,
                    "message": (
                        f"entry '{key}' at line {line} sits behind a '%' marker; real BibTeX "
                        "still parses it - delete the entry or wrap it in @comment{...} to "
                        "disable it"
                    ),
                }
            )
        entries.append(
            {"entry_type": entry_type, "key": key, "fields": fields, "raw_bib": raw_entry}
        )
        idx = pos

    return entries, warnings, macros
