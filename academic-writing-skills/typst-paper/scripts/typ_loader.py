#!/usr/bin/env python3
"""
Multi-file Typst document loader with source-location mapping.

Typst counterpart of ``tex_loader.py``: a paper's ``main.typ`` often pulls body
text in via ``#include "sections/intro.typ"``. Analyzers must see the assembled
document while still reporting diagnostics as ``source:line``.

Public API:
    read_text_robust(path)  -> (text, warning | None)
    assemble(entry)         -> AssembledDocument        # concatenated, line-mapped

Only ``#include`` (which inlines body content) is expanded. ``#import`` brings
symbols into scope rather than prose and is intentionally left in place.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# #include "file.typ" — string-literal path form used for body inlining.
INCLUDE_RE = re.compile(r'#include\s+"([^"]+)"')
LINE_COMMENT_RE = re.compile(r"//.*")
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
MAX_DEPTH = 32


def read_text_robust(path: Path) -> tuple[str, str | None]:
    """Read a source file defensively: utf-8 strict, then latin-1, then utf-8
    with replacement (plus a loud warning)."""
    data = path.read_bytes()
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        pass
    try:
        text = data.decode("latin-1")
        return text, f"{path.name}: not UTF-8, decoded as latin-1 (please convert to UTF-8)"
    except UnicodeDecodeError:
        text = data.decode("utf-8", errors="replace")
        return (
            text,
            f"{path.name}: encoding error, some characters undecodable (result may be incomplete)",
        )


def _display_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _resolve_include_target(raw: str, current_dir: Path, root: Path) -> Path:
    name = raw.strip()
    if not name.endswith(".typ"):
        name += ".typ"
    candidate = (current_dir / name).resolve()
    if candidate.exists():
        return candidate
    fallback = (root / name).resolve()
    if fallback.exists():
        return fallback
    return candidate


def _blank_block_comments(text: str) -> str:
    """Blank out ``/* */`` blocks while keeping newlines, so an ``#include``
    hidden inside a block comment is not expanded and line numbers stay intact."""
    return BLOCK_COMMENT_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), text)


@dataclass
class AssembledDocument:
    """Concatenated document content plus an assembled-line -> source map."""

    entry: Path
    content: str = ""
    lines: list[str] = field(default_factory=list)
    origins: list[tuple[str, int]] = field(default_factory=list)
    missing: list[tuple[str, str, int]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    multi_file: bool = False

    def origin(self, line_no: int) -> tuple[str, int]:
        """Map an assembled 1-based line number to (source rel path, source line)."""
        if 1 <= line_no <= len(self.origins):
            return self.origins[line_no - 1]
        return (_display_rel(self.entry, self.entry.parent), max(line_no, 1))

    def lineref(self, start: int, end: int | None = None) -> str:
        """Location label. Single file: ``Line 15`` / ``Line 15-20``.
        Multi file: ``sections/intro.typ:15`` / ``sections/intro.typ:15-20``."""
        if not self.multi_file:
            if end is not None and end != start:
                return f"Line {start}-{end}"
            return f"Line {start}"
        src, src_line = self.origin(start)
        if end is not None and end != start:
            end_src, end_line = self.origin(end)
            if end_src == src:
                return f"{src}:{src_line}-{end_line}"
        return f"{src}:{src_line}"

    def warning_lines(self, comment_prefix: str = "//") -> list[str]:
        """Header warning lines for diagnostic output (encoding + missing includes)."""
        out = [f"{comment_prefix} WARN: {w}" for w in self.warnings]
        for raw, src, line_no in self.missing:
            out.append(f"{comment_prefix} WARN: include file not found: {raw} ({src}:{line_no})")
        return out


def assemble(entry: Path) -> AssembledDocument:
    """Assemble the full Typst document from ``entry``, expanding ``#include``
    directives inline with a per-line origin map. Guards against cycles and
    bounds recursion at ``MAX_DEPTH``."""
    entry = Path(entry).resolve()
    root = entry.parent
    doc = AssembledDocument(entry=entry)

    out_lines: list[str] = []
    origins: list[tuple[str, int]] = []
    visited: set[Path] = set()

    def _emit(line: str, rel: str, line_no: int) -> None:
        out_lines.append(line)
        origins.append((rel, line_no))

    def _expand(path: Path, depth: int) -> None:
        if path in visited or depth > MAX_DEPTH:
            return
        visited.add(path)
        rel = _display_rel(path, root)
        text, warning = read_text_robust(path)
        if warning:
            doc.warnings.append(warning)
        scannable_lines = _blank_block_comments(text).split("\n")
        for line_no, line in enumerate(text.split("\n"), 1):
            scannable = LINE_COMMENT_RE.sub("", scannable_lines[line_no - 1])
            matches = list(INCLUDE_RE.finditer(scannable))
            if not matches:
                _emit(line, rel, line_no)
                continue
            cursor = 0
            for match in matches:
                prefix = scannable[cursor : match.start()]
                if prefix.strip():
                    _emit(prefix, rel, line_no)
                cursor = match.end()
                target = _resolve_include_target(match.group(1), path.parent, root)
                if not target.exists():
                    doc.missing.append((match.group(1).strip(), rel, line_no))
                    continue
                if target in visited:
                    continue
                doc.multi_file = True
                _expand(target, depth + 1)
            suffix = scannable[cursor:]
            if suffix.strip():
                _emit(suffix, rel, line_no)

    _expand(entry, 0)
    doc.lines = out_lines
    doc.content = "\n".join(out_lines)
    doc.origins = origins
    return doc
