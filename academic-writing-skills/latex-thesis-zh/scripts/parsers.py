"""
Document Parsers for Chinese Academic Thesis
Support for LaTeX and Typst document parsing.
"""

import re
from abc import ABC, abstractmethod
from typing import Any


class DocumentParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    def split_sections(self, content: str) -> dict[str, tuple[int, int]]:
        pass

    @abstractmethod
    def extract_visible_text(self, line: str) -> str:
        pass

    @abstractmethod
    def get_comment_prefix(self) -> str:
        pass

    def extract_headings(self, content: str) -> list[dict[str, Any]]:
        """Return heading nodes in document order.

        Parsers that support fine-grained heading inspection should override this.
        """
        return []

    def chapter_ranges(self, content: str) -> list[dict[str, Any]]:
        """Enumerate ALL level-1 chapter ranges in document order.

        Unlike ``split_sections`` (which only keys chapters matching the known
        SECTION patterns), this never drops a body chapter whose title carries
        no keyword — analyzers use it so such chapters still get checked.
        Each item: ``{"title", "start", "end", "key" (matched key or None)}``.
        """
        lines_total = len(content.split("\n"))
        headings = [h for h in self.extract_headings(content) if h["level"] == 1]
        sections = self.split_sections(content)
        ranges: list[dict[str, Any]] = []
        for idx, heading in enumerate(headings):
            start = heading["line"]
            end = headings[idx + 1]["line"] - 1 if idx + 1 < len(headings) else lines_total
            key = next(
                (k for k, (s, _e) in sections.items() if s == start),
                None,
            )
            ranges.append({"title": heading["title"], "start": start, "end": end, "key": key})
        return ranges


def _split_sections_from_headings(
    headings: list[dict[str, Any]],
    classify,
    total_lines: int,
) -> dict[str, tuple[int, int]]:
    """Shared interval builder for ``split_sections`` implementations.

    Rules fixing the historical silent-skip defects:
    - a matched heading opens a new range;
    - ANY heading at the same or higher level closes the open range, so an
      unmatched body chapter is no longer swallowed by the previous section;
    - duplicate keys get ``_2``/``_3`` suffixes instead of overwriting.
    """
    sections: dict[str, tuple[int, int]] = {}
    key_counts: dict[str, int] = {}
    open_key: str | None = None
    open_start = 0
    open_level = 0

    def _close(end_line: int) -> None:
        nonlocal open_key
        if open_key is not None:
            sections[open_key] = (open_start, max(end_line, open_start))
            open_key = None

    for heading in headings:
        key = classify(heading)
        if open_key is not None and (key is not None or heading["level"] <= open_level):
            _close(heading["line"] - 1)
        if key is not None:
            key_counts[key] = key_counts.get(key, 0) + 1
            open_key = key if key_counts[key] == 1 else f"{key}_{key_counts[key]}"
            open_start = heading["line"]
            open_level = heading["level"]
    _close(total_lines)
    return sections


# ── --section 同义映射（中英文均可指定章节，R3/F11） ─────────────

SECTION_KEY_ALIASES = {
    "摘要": "abstract",
    "绪论": "introduction",
    "引言": "introduction",
    "intro": "introduction",
    "创新点": "contribution",
    "主要贡献": "contribution",
    "贡献": "contribution",
    "相关工作": "related",
    "文献综述": "related",
    "literature": "related",
    "方法": "method",
    "原理": "method",
    "设计": "method",
    "实验": "experiment",
    "实现": "experiment",
    "测试": "experiment",
    "experiments": "experiment",
    "结果": "result",
    "性能": "result",
    "results": "result",
    "讨论": "discussion",
    "分析": "discussion",
    "结论": "conclusion",
    "总结": "conclusion",
    "总结与展望": "conclusion",
}


def resolve_section_keys(
    query: str, sections: dict[str, tuple[int, int]]
) -> tuple[list[str], list[str]]:
    """Resolve a user-supplied ``--section`` value to actual section keys.

    Accepts English keys (``introduction``) and Chinese names (``绪论``)
    interchangeably; a base key also matches its ``_2``/``_3`` duplicates.
    Returns ``(matched_keys, available_keys)`` — when nothing matches, the
    caller should list ``available_keys`` instead of a bare "not found".
    """
    available = list(sections.keys())
    base = query.strip().lower()
    base = SECTION_KEY_ALIASES.get(query.strip(), SECTION_KEY_ALIASES.get(base, base))
    matched = [k for k in sections if k == base or k.startswith(f"{base}_")]
    return matched, available


class LatexParser(DocumentParser):
    """Parser for Chinese LaTeX Thesis."""

    HEADING_PATTERN = re.compile(
        r"\\(?P<command>chapter|section|subsection|subsubsection|paragraph)\*?"
        r"(?:\[[^\]]*\])?\{(?P<title>[^}]*)\}"
    )

    HEADING_LEVELS = {
        "chapter": 1,
        "section": 2,
        "subsection": 3,
        "subsubsection": 4,
        "paragraph": 5,
    }

    # Chinese Section patterns
    # Deprecated: kept for backward compatibility only. ``split_sections`` now
    # classifies normalized heading titles via SECTION_TITLE_RULES below, which
    # tolerates \chapter*{}, optional args and intra-title spacing (绪\quad 论).
    SECTION_PATTERNS = {
        "abstract": r"\\chapter{摘要}|\\section{摘要}",
        "introduction": r"\\chapter{绪论}|\\chapter{引言}|\\section{绪论}|\\section{引言}",
        "contribution": r"\\chapter{(?:创新点|主要贡献)}|\\section{(?:创新点|主要贡献)}",
        "related": r"\\chapter{相关工作}|\\section{相关工作}|\\section{文献综述}",
        "method": r"\\chapter{.*?(?:方法|原理|设计)}",
        "experiment": r"\\chapter{.*?(?:实验|实现|测试)}|\\section{.*?(?:实验|实现)}",
        "result": r"\\chapter{.*?(?:结果|性能)}|\\section{.*?(?:结果|性能)}",
        "discussion": r"\\chapter{.*?(?:讨论|分析)}|\\section{.*?(?:讨论|分析)}",
        "conclusion": r"\\chapter{结论}|\\chapter{总结与展望}|\\section{结论}",
    }

    # (key, max heading level allowed, regex on the normalized title).
    # Order matters: first match wins. Semantics mirror SECTION_PATTERNS
    # (exact titles for abstract/intro/..., "contains" for method/experiment/...;
    # method stays chapter-level only, as before).
    SECTION_TITLE_RULES: list[tuple[str, int, str]] = [
        ("abstract", 2, r"^摘要$"),
        ("introduction", 2, r"^(?:绪论|引言)$"),
        ("contribution", 2, r"^(?:创新点|主要贡献)$"),
        ("related", 2, r"^(?:相关工作|文献综述)$"),
        ("conclusion", 2, r"^(?:结论|总结与展望)$"),
        ("method", 1, r"(?:方法|原理|设计)"),
        ("experiment", 2, r"(?:实验|实现|测试)"),
        ("result", 2, r"(?:结果|性能)"),
        ("discussion", 2, r"(?:讨论|分析)"),
    ]

    PRESERVE_PATTERNS = [
        r"\\cite{[^}]+}",  # Citations
        r"\\ref{[^}]+}",  # References
        r"\\label{[^}]+}",  # Labels
        r"\\eqref{[^}]+}",  # Equation references
        r"\\autoref{[^}]+}",  # Auto references
        r"\$\$[^$]*\$\$",  # Display math
        r"\$[^$]*\$",  # Inline math
        r"\\begin{equation}.*?\\end{equation}",  # Equations
        r"\\begin{align}.*?\\end{align}",  # Align environments
        r"\\begin{.*?}.*?\\end{.*?}",  # Generic environments
        r"\\includegraphics(?:\[[^]]*\])?\{[^}]+\}",  # Images
        r"\\caption{[^}]+}",  # Captions
    ]

    def get_comment_prefix(self) -> str:
        return "%"

    @staticmethod
    def normalize_heading_title(title: str) -> str:
        """Normalize a heading title for classification.

        Drops spacing commands (``\\quad``/``\\hspace{..}``/``~``) and all
        whitespace so ``绪\\quad 论`` and ``绪 论`` classify as ``绪论``.
        """
        title = re.sub(r"\\(?:quad|qquad|hspace\*?\{[^}]*\}|[,;! ])", "", title)
        return re.sub(r"[~\s]+", "", title)

    def _classify_heading(self, heading: dict[str, Any]) -> str | None:
        title = self.normalize_heading_title(heading["title"])
        for key, max_level, pattern in self.SECTION_TITLE_RULES:
            if heading["level"] <= max_level and re.search(pattern, title):
                return key
        return None

    def split_sections(self, content: str) -> dict[str, tuple[int, int]]:
        lines_total = len(content.split("\n"))
        headings = self.extract_headings(content)
        return _split_sections_from_headings(headings, self._classify_heading, lines_total)

    def extract_visible_text(self, line: str) -> str:
        temp_line = line
        preserved = []

        for pattern in self.PRESERVE_PATTERNS:
            matches = list(re.finditer(pattern, temp_line, re.DOTALL))
            for match in reversed(matches):
                preserved.append(
                    {"start": match.start(), "end": match.end(), "text": match.group()}
                )
                placeholder = " " * (match.end() - match.start())
                temp_line = temp_line[: match.start()] + placeholder + temp_line[match.end() :]

        preserved.sort(key=lambda x: x["start"])

        visible_parts = []
        last_end = 0

        for item in preserved:
            if item["start"] > last_end:
                visible_parts.append(temp_line[last_end : item["start"]])
            last_end = item["end"]

        if last_end < len(temp_line):
            visible_parts.append(temp_line[last_end:])

        return " ".join(visible_parts).strip()

    def extract_headings(self, content: str) -> list[dict[str, Any]]:
        headings: list[dict[str, Any]] = []
        for line_no, line in enumerate(content.split("\n"), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(self.get_comment_prefix()):
                continue
            # Strip inline comments (respecting \%) so a trailing
            # "% \chapter{...}" remark is never parsed as a real heading.
            stripped = re.sub(r"(?<!\\)%.*", "", stripped)
            match = self.HEADING_PATTERN.search(stripped)
            if not match:
                continue
            command = match.group("command")
            headings.append(
                {
                    "line": line_no,
                    "level": self.HEADING_LEVELS[command],
                    "command": command,
                    "title": match.group("title").strip(),
                }
            )
        return headings


class TypstParser(DocumentParser):
    """Parser for Chinese Typst Thesis."""

    HEADING_PATTERN = re.compile(r"^(?P<marks>={1,5})\s+(?P<title>.+?)\s*$")

    # Chinese Section patterns for Typst
    # e.g. = 摘要, = 绪论
    # Deprecated: kept for backward compatibility; split_sections now goes
    # through SECTION_TITLE_RULES (level-1 headings only, same semantics).
    SECTION_PATTERNS = {
        "abstract": r"^=\s+摘要",
        "introduction": r"^=\s+(?:绪论|引言)",
        "contribution": r"^=\s+(?:创新点|主要贡献)",
        "related": r"^=\s+(?:相关工作|文献综述)",
        "method": r"^=\s+.*(?:方法|原理|设计)",
        "experiment": r"^=\s+.*(?:实验|实现|测试)",
        "result": r"^=\s+.*(?:结果|性能)",
        "discussion": r"^=\s+.*(?:讨论|分析)",
        "conclusion": r"^=\s+.*(?:结论|总结与展望)",
    }

    SECTION_TITLE_RULES: list[tuple[str, int, str]] = [
        ("abstract", 1, r"^摘要$"),
        ("introduction", 1, r"^(?:绪论|引言)$"),
        ("contribution", 1, r"^(?:创新点|主要贡献)$"),
        ("related", 1, r"^(?:相关工作|文献综述)$"),
        ("conclusion", 1, r"(?:结论|总结与展望)"),
        ("method", 1, r"(?:方法|原理|设计)"),
        ("experiment", 1, r"(?:实验|实现|测试)"),
        ("result", 1, r"(?:结果|性能)"),
        ("discussion", 1, r"(?:讨论|分析)"),
    ]

    PRESERVE_PATTERNS = [
        r"@[a-zA-Z0-9_-]+",  # Citations
        r"#cite\([^)]+\)",
        r"#figure\([^)]+\)",
        r"#table\([^)]+\)",
        r"\$[^$]+\$",
        r"//.*",
        r"/\*.*?\*/",
        r"<[a-zA-Z0-9_-]+>",
        r"#link\([^)]+\)",
    ]

    def get_comment_prefix(self) -> str:
        return "//"

    def _classify_heading(self, heading: dict[str, Any]) -> str | None:
        title = re.sub(r"\s+", "", heading["title"])
        for key, max_level, pattern in self.SECTION_TITLE_RULES:
            if heading["level"] <= max_level and re.search(pattern, title):
                return key
        return None

    def split_sections(self, content: str) -> dict[str, tuple[int, int]]:
        lines_total = len(content.split("\n"))
        headings = self.extract_headings(content)
        return _split_sections_from_headings(headings, self._classify_heading, lines_total)

    def extract_visible_text(self, line: str) -> str:
        temp_line = line
        if "//" in temp_line:
            temp_line = temp_line.split("//")[0]

        preserved = []
        for pattern in self.PRESERVE_PATTERNS:
            matches = list(re.finditer(pattern, temp_line, re.DOTALL))
            for match in reversed(matches):
                preserved.append(
                    {"start": match.start(), "end": match.end(), "text": match.group()}
                )
                placeholder = " " * (match.end() - match.start())
                temp_line = temp_line[: match.start()] + placeholder + temp_line[match.end() :]

        preserved.sort(key=lambda x: x["start"])

        visible_parts = []
        last_end = 0
        for item in preserved:
            if item["start"] > last_end:
                visible_parts.append(temp_line[last_end : item["start"]])
            last_end = item["end"]
        if last_end < len(temp_line):
            visible_parts.append(temp_line[last_end:])

        return " ".join(visible_parts).strip()

    def extract_headings(self, content: str) -> list[dict[str, Any]]:
        headings: list[dict[str, Any]] = []
        for line_no, line in enumerate(content.split("\n"), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(self.get_comment_prefix()):
                continue
            match = self.HEADING_PATTERN.match(stripped)
            if not match:
                continue
            headings.append(
                {
                    "line": line_no,
                    "level": len(match.group("marks")),
                    "command": "heading",
                    "title": match.group("title").strip(),
                }
            )
        return headings


def get_parser(file_path: Any) -> DocumentParser:
    """Factory method to get appropriate parser."""
    path_str = str(file_path).lower()
    if path_str.endswith(".typ"):
        return TypstParser()
    return LatexParser()


def _normalize_whitespace(text: str) -> str:
    """Collapse whitespace to single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def _strip_latex_markup(text: str) -> str:
    """Remove LaTeX commands from text, keeping content."""
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])*\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    text = re.sub(r"[{}]", "", text)
    return _normalize_whitespace(text)


def extract_title(content: str) -> str:
    """Extract document title from Chinese LaTeX thesis source.

    Supports \\ctitle, \\title commands commonly used in Chinese thesis templates.
    """
    # Chinese title: \ctitle{...}
    ctitle = re.search(r"\\ctitle\{(.+?)\}", content, re.DOTALL)
    if ctitle:
        return _strip_latex_markup(ctitle.group(1))

    # Standard: \title{...}
    title = re.search(r"\\title(?:\[[^\]]*\])?\{(.+?)\}", content, re.DOTALL)
    if title:
        return _strip_latex_markup(title.group(1))

    return ""


def extract_abstract(content: str) -> str:
    """Extract abstract text from Chinese LaTeX thesis source.

    Supports \\cabstract, \\begin{cabstract}, \\begin{abstract} environments.
    """
    # Chinese abstract environment: \begin{cabstract}...\end{cabstract}
    cab = re.search(r"\\begin{cabstract}(.*?)\\end{cabstract}", content, re.DOTALL)
    if cab:
        return _strip_latex_markup(cab.group(1))

    # Standard abstract environment
    ab = re.search(r"\\begin{abstract}(.*?)\\end{abstract}", content, re.DOTALL)
    if ab:
        return _strip_latex_markup(ab.group(1))

    # Section-based: \chapter{摘要} or \section{摘要}
    sec = re.search(
        r"\\(?:chapter|section)\{摘要\}(.*?)(?=\\(?:chapter|section)\{|\\end\{document\}|\Z)",
        content,
        re.DOTALL,
    )
    if sec:
        return _strip_latex_markup(sec.group(1))

    return ""
