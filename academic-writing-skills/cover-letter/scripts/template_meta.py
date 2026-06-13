"""Frontmatter parsing for cover-letter venue templates.

Templates carry a small YAML frontmatter block (string / int scalars and
``- item`` lists). PyYAML is not part of the Python standard library and is not
guaranteed to be installed when the skill runs from ``~/.claude/skills/``, so
this module parses the limited subset the templates actually use, with no third
party dependency. Shared by ``presubmission_check`` and ``journal_fit_check`` so
the parse rules stay in one place.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _scalar(token: str) -> Any:
    """Coerce a scalar token: quoted string, integer, or bare string."""
    token = token.strip()
    if len(token) >= 2 and token[0] in "\"'" and token[-1] == token[0]:
        return token[1:-1]
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    return token


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse a YAML-subset frontmatter body into a dict.

    Supports ``key: scalar`` and ``key:`` followed by indented ``- item`` lines.
    Unsupported constructs are ignored rather than raising.
    """
    meta: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        list_item = re.match(r"\s*-\s+(.*)$", raw)
        if list_item is not None and current_key is not None:
            bucket = meta.setdefault(current_key, [])
            if isinstance(bucket, list):
                bucket.append(_scalar(list_item.group(1)))
            continue
        kv = re.match(r"([A-Za-z0-9_]+)\s*:\s*(.*)$", raw)
        if kv is None:
            continue
        key, value = kv.group(1), kv.group(2).strip()
        if value == "":
            meta[key] = []
            current_key = key
        else:
            meta[key] = _scalar(value)
            current_key = None
    return meta


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return ``(frontmatter_dict, body_text)`` for a ``---``-delimited document.

    Falls back to ``({}, text)`` when no frontmatter block is present.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    return parse_frontmatter(text[3:end]), text[end + 4 :]


def load_template_meta(skill_dir: Path, venue: str | None) -> dict[str, Any] | None:
    """Load and parse a venue template's frontmatter, falling back to generic."""
    if not venue:
        return None
    candidate = skill_dir / "templates" / f"{venue}.md"
    if not candidate.exists():
        candidate = skill_dir / "templates" / "generic.md"
    if not candidate.exists():
        return None
    meta, _ = split_frontmatter(candidate.read_text(encoding="utf-8", errors="replace"))
    return meta or None
