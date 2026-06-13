#!/usr/bin/env python3
"""
Multi-file LaTeX document loader with source-location mapping.

Single authoritative include resolver for the latex-paper-en skill scripts
(ported from latex-thesis-zh/scripts/tex_loader.py). Real papers often keep
``main.tex`` as an ``\\input{sections/intro}`` skeleton; analyzers must see the
assembled document while still reporting diagnostics as ``source:line``.

Public API:
    read_text_robust(path)  -> (text, warning | None)   # utf-8 -> latin-1 -> replace
    iter_files(entry)       -> list[IncludeNode]         # document-order traversal
    assemble(entry)         -> AssembledDocument         # concatenated, line-mapped
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# \include{x} / \input{x} / \subfile{x} — the brace must follow immediately,
# so \includegraphics / \inputminted are not matched.
INCLUDE_RE = re.compile(r"\\(?:input|include|subfile)\{([^}]+)\}")
# Strip inline comments while keeping escaped \%
COMMENT_RE = re.compile(r"(?<!\\)%.*")


def read_text_robust(path: Path) -> tuple[str, str | None]:
    """Read a source file defensively: utf-8 strict, then latin-1, then utf-8
    with replacement (plus a loud warning). Never silently mangles a
    non-UTF-8 source into mojibake that "passes" every check."""
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


@dataclass
class IncludeNode:
    """One file in the include graph, in document order."""

    path: Path
    rel: str
    level: int
    exists: bool
    content: str | None = None
    warning: str | None = None


def _display_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _resolve_include_target(raw: str, current_dir: Path, root: Path) -> Path:
    name = raw.strip()
    if not name.endswith(".tex"):
        name += ".tex"
    candidate = (current_dir / name).resolve()
    if candidate.exists():
        return candidate
    fallback = (root / name).resolve()
    if fallback.exists():
        return fallback
    return candidate


def iter_files(entry: Path) -> list[IncludeNode]:
    """Traverse the include graph from ``entry`` in document order.

    Skips commented-out includes, guards against cycles, and records
    missing files as ``exists=False`` nodes instead of dropping them.
    """
    entry = Path(entry).resolve()
    root = entry.parent
    nodes: list[IncludeNode] = []
    visited: set[Path] = set()

    def _walk(path: Path, level: int) -> None:
        if path in visited:
            return
        visited.add(path)
        if not path.exists():
            nodes.append(
                IncludeNode(path=path, rel=_display_rel(path, root), level=level, exists=False)
            )
            return
        text, warning = read_text_robust(path)
        nodes.append(
            IncludeNode(
                path=path,
                rel=_display_rel(path, root),
                level=level,
                exists=True,
                content=text,
                warning=warning,
            )
        )
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("%"):
                continue
            for match in INCLUDE_RE.finditer(COMMENT_RE.sub("", line)):
                _walk(_resolve_include_target(match.group(1), path.parent, root), level + 1)

    _walk(entry, 0)
    return nodes


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
        """Location label.

        Single file: ``Line 15`` / ``Line 15-20`` (byte-compatible with the
        previous single-file output). Multi file: ``sections/intro.tex:15`` /
        ``sections/intro.tex:15-20`` (cross-file ranges keep the start file).
        """
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

    def warning_lines(self, comment_prefix: str = "%") -> list[str]:
        """Header warning lines for diagnostic output (encoding + missing includes)."""
        out = [f"{comment_prefix} WARN: {w}" for w in self.warnings]
        for raw, src, line_no in self.missing:
            out.append(f"{comment_prefix} WARN: include file not found: {raw} ({src}:{line_no})")
        return out


def assemble(entry: Path) -> AssembledDocument:
    """Assemble the full document from ``entry``, expanding includes inline.

    Keeps a per-line origin map so diagnostics computed against the
    assembled content can still point at ``source:line``. ``.typ`` entries
    are read as-is (use typ_loader for Typst multi-file assembly)."""
    entry = Path(entry).resolve()
    root = entry.parent
    doc = AssembledDocument(entry=entry)

    if entry.suffix.lower() == ".typ":
        text, warning = read_text_robust(entry)
        doc.content = text
        doc.lines = text.split("\n")
        rel = _display_rel(entry, root)
        doc.origins = [(rel, i) for i in range(1, len(doc.lines) + 1)]
        if warning:
            doc.warnings.append(warning)
        return doc

    out_lines: list[str] = []
    origins: list[tuple[str, int]] = []
    visited: set[Path] = set()

    def _emit(line: str, rel: str, line_no: int) -> None:
        out_lines.append(line)
        origins.append((rel, line_no))

    def _expand(path: Path) -> None:
        if path in visited:
            return
        visited.add(path)
        rel = _display_rel(path, root)
        text, warning = read_text_robust(path)
        if warning:
            doc.warnings.append(warning)
        for line_no, line in enumerate(text.split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith("%"):
                _emit(line, rel, line_no)
                continue
            scannable = COMMENT_RE.sub("", line)
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
                _expand(target)
            suffix = scannable[cursor:]
            if suffix.strip():
                _emit(suffix, rel, line_no)

    _expand(entry)
    doc.lines = out_lines
    doc.content = "\n".join(out_lines)
    doc.origins = origins
    return doc
