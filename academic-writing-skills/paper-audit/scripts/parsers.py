"""
Document Parsers for Paper Audit Skill.

Vendored copy aligned with latex-paper-en/scripts/parsers.py for the shared
core (DocumentParser ABC, LatexParser, TypstParser, helpers). Only the
``get_parser`` factory is extended to dispatch PDF inputs through
``pdf_parser.PdfParser`` so the audit pipeline can ingest .tex / .typ / .pdf
uniformly.

Alignment with the canonical (latex-paper-en) copy is enforced by
``tests/test_parsers_alignment.py``. When changing shared behavior, update the
canonical copy first and let the alignment test guide the rest.
"""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class DocumentParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    def split_sections(self, content: str) -> dict[str, tuple[int, int]]:
        """
        Split document into sections.
        Returns map of {section_name: (start_line, end_line)}.
        """
        pass

    @abstractmethod
    def extract_visible_text(self, line: str) -> str:
        """
        Extract text visible to reader, preserving structure markers.
        Used for line-by-line AI trace checking.
        """
        pass

    @abstractmethod
    def clean_text(self, content: str, keep_structure: bool = False) -> str:
        """
        Extract pure prose text, removing all markup.
        Used for prose extraction and word counting.
        """
        pass

    @abstractmethod
    def get_comment_prefix(self) -> str:
        """Get the comment prefix for the language."""
        pass

    def extract_headings(self, content: str) -> list[dict[str, Any]]:
        """Return heading nodes in document order.

        Parsers that support fine-grained heading inspection should override this.
        """
        return []

    def chapter_ranges(self, content: str) -> list[dict[str, Any]]:
        """Enumerate ALL top-level section ranges in document order.

        Unlike ``split_sections`` (which only keys sections matching the known
        SECTION patterns), this never drops a body section whose title carries
        no keyword — analyzers use it so such sections still get checked.
        Each item: ``{"title", "start", "end", "key" (matched key or None)}``.
        """
        lines_total = len(content.split("\n"))
        headings = self.extract_headings(content)
        if not headings:
            return []
        top_level = min(h["level"] for h in headings)
        top = [h for h in headings if h["level"] == top_level]
        sections = self.split_sections(content)
        ranges: list[dict[str, Any]] = []
        for idx, heading in enumerate(top):
            start = heading["line"]
            end = top[idx + 1]["line"] - 1 if idx + 1 < len(top) else lines_total
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
      unmatched body section is no longer swallowed by the previous section;
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


# ── --section alias map (English keys / loose synonyms) ───────────

SECTION_KEY_ALIASES = {
    "intro": "introduction",
    "contributions": "contribution",
    "related work": "related",
    "related works": "related",
    "literature": "related",
    "literature review": "related",
    "methods": "method",
    "methodology": "method",
    "approach": "method",
    "experiments": "experiment",
    "evaluation": "experiment",
    "implementation": "experiment",
    "results": "result",
    "performance": "result",
    "discussions": "discussion",
    "analysis": "discussion",
    "conclusions": "conclusion",
}


def resolve_section_keys(
    query: str, sections: dict[str, tuple[int, int]]
) -> tuple[list[str], list[str]]:
    """Resolve a user-supplied ``--section`` value to actual section keys.

    Accepts canonical keys (``introduction``) and loose synonyms
    (``methods`` -> ``method``); a base key also matches its ``_2``/``_3``
    duplicates. Returns ``(matched_keys, available_keys)`` — when nothing
    matches, the caller should list ``available_keys`` instead of a bare
    "not found".
    """
    available = list(sections.keys())
    base = query.strip().lower()
    base = SECTION_KEY_ALIASES.get(query.strip(), SECTION_KEY_ALIASES.get(base, base))
    matched = [k for k in sections if k == base or k.startswith(f"{base}_")]
    return matched, available


class LatexParser(DocumentParser):
    """Parser for LaTeX documents."""

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

    # Deprecated: kept for backward compatibility only. ``split_sections`` now
    # classifies normalized heading titles via SECTION_TITLE_RULES below, which
    # tolerates \section*{}, plural / compound titles, ALL-CAPS variants and
    # commented-out headings.
    SECTION_PATTERNS = {
        "abstract": r"\\begin{abstract}|\\section*?{abstract}?",
        "introduction": r"\\section*?{Introduction}|\\section*?{INTRODUCTION}",
        "related": r"\\section*?{Related\s+Work}|\\section*?{RELATED\s+WORK}",
        "method": r"\\section*?{.*(?:Method|Methodology|Approach)}",
        "experiment": r"\\section*?{.*(?:Experiment|Evaluation|Implementation)}",
        "result": r"\\section*?{.*(?:Result|Performance)}",
        "discussion": r"\\section*?{.*(?:Discussion|Analysis)}",
        "conclusion": r"\\section*?{.*(?:Conclusion|Conclusions)}",
    }

    # (key, max heading level allowed, regex on the normalized lowercase title).
    # Order matters: first match wins. Titles are lowercased with internal
    # spacing kept, so "Methods", "Experimental Results", "RELATED WORKS" and
    # "Results and Discussion" all classify correctly.
    SECTION_TITLE_RULES: list[tuple[str, int, str]] = [
        ("abstract", 2, r"^abstract$"),
        ("introduction", 2, r"^introduction$"),
        ("related", 2, r"^related work|^related$|literature review|^prior work"),
        ("contribution", 2, r"^contributions?$"),
        ("conclusion", 2, r"conclu"),
        ("method", 2, r"method|methodolog|approach|proposed|framework"),
        ("experiment", 2, r"experiment|evaluation|implementation"),
        ("result", 2, r"result|performance|findings"),
        ("discussion", 2, r"discussion|analysis"),
    ]

    # Preservation patterns for visible text extraction
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

    # Environments to skip entirely for clean text
    SKIP_ENVIRONMENTS = [
        "equation",
        "equation*",
        "align",
        "align*",
        "gather",
        "gather*",
        "multline",
        "multline*",
        "eqnarray",
        "eqnarray*",
        "displaymath",
        "figure",
        "figure*",
        "table",
        "table*",
        "tabular",
        "tabular*",
        "lstlisting",
        "verbatim",
        "minted",
        "algorithm",
        "algorithmic",
    ]

    def get_comment_prefix(self) -> str:
        return "%"

    @staticmethod
    def normalize_heading_title(title: str) -> str:
        """Normalize a heading title for classification.

        Unwraps simple formatting commands (``\\textsc{X}`` -> ``X``), drops
        stray commands and braces, collapses whitespace and lowercases. Internal
        spacing is kept (English titles are space-delimited), so ``Related Work``
        and ``RELATED  WORK`` both classify as ``related work``.
        """
        title = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", title)
        title = re.sub(r"\\[a-zA-Z]+\*?", " ", title)
        title = re.sub(r"[{}~]", " ", title)
        title = re.sub(r"\s+", " ", title).strip().lower()
        return title.strip(" :.")

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
        # Preserve structure markers logic
        preserved = []
        temp_line = line

        for pattern in self.PRESERVE_PATTERNS:
            matches = list(re.finditer(pattern, temp_line, re.DOTALL))
            for match in reversed(matches):
                preserved.append(
                    {"start": match.start(), "end": match.end(), "text": match.group()}
                )
                # Replace with placeholder of same length to keep indices valid
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
            # "% \section{...}" remark is never parsed as a real heading.
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

    def clean_text(self, content: str, keep_structure: bool = False) -> str:
        # Remove comments
        content = re.sub(r"(?<!\\)%.*", "", content)

        # Remove skip environments
        for env in self.SKIP_ENVIRONMENTS:
            pattern = rf"\\begin{{{env}}}.*?\\end{{{env}}}"
            content = re.sub(pattern, "", content, flags=re.DOTALL)

        # Remove inline / display math
        content = re.sub(r"\$[^$]+\$", "", content)
        content = re.sub(r"\\\[.*?\\\]", "", content, flags=re.DOTALL)
        content = re.sub(r"\\\(.*?\\\)", "", content, flags=re.DOTALL)

        # Formatting
        if keep_structure:
            content = re.sub(r"\\section\*?{([^}]+)}", r"\n\n## \1\n\n", content)
            content = re.sub(r"\\subsection\*?{([^}]+)}", r"\n\n### \1\n\n", content)
        else:
            content = re.sub(r"\\(?:sub)*section\*?{[^}]+}", "", content)

        # Remove commands
        content = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?{([^}]*)}", r"\1", content)
        content = re.sub(r"\\[a-zA-Z]+\*?", "", content)
        content = re.sub(r"[{}]", "", content)

        # Cleanup whitespace
        content = re.sub(r"\n+", "\n", content)
        content = re.sub(r" +", " ", content)
        content = re.sub(r"\.(\s*\.)+", ".", content)  # Fix multiple periods

        return content.strip()


class TypstParser(DocumentParser):
    """Parser for Typst documents."""

    HEADING_PATTERN = re.compile(r"^(?P<marks>={1,5})\s+(?P<title>.+?)\s*$")

    # Deprecated: kept for backward compatibility; split_sections now goes
    # through SECTION_TITLE_RULES (heading-based, same semantics).
    SECTION_PATTERNS = {
        "introduction": r"^=\s+(?:Introduction|INTRODUCTION|绪论|引言)",
        "related": r"^=\s+(?:Related\s+Work|RELATED\s+WORK|相关工作|文献综述)",
        "method": r"^=\s+.*(?:Method|Methodology|Approach|方法|原理|设计)",
        "experiment": r"^=\s+.*(?:Experiment|Evaluation|Implementation|实验|实现|测试)",
        "result": r"^=\s+.*(?:Result|Performance|结果|性能)",
        "discussion": r"^=\s+.*(?:Discussion|Analysis|讨论|分析)",
        "conclusion": r"^=\s+.*(?:Conclusion|Conclusions|结论|总结与展望)",
        "abstract": r"#abstract\[",
    }

    # (key, max heading level, regex on the lowercased title). Bilingual so the
    # same parser serves English papers and the occasional Chinese Typst draft.
    SECTION_TITLE_RULES: list[tuple[str, int, str]] = [
        ("abstract", 1, r"^abstract$|^摘要$"),
        ("introduction", 1, r"^introduction$|^(?:绪论|引言)$"),
        ("related", 1, r"^related work|^related$|literature review|相关工作|文献综述"),
        ("contribution", 1, r"^contributions?$|^(?:创新点|主要贡献)$"),
        ("conclusion", 1, r"conclu|结论|总结"),
        ("method", 1, r"method|methodolog|approach|proposed|framework|方法|原理|设计"),
        ("experiment", 1, r"experiment|evaluation|implementation|实验|实现|测试"),
        ("result", 1, r"result|performance|结果|性能"),
        ("discussion", 1, r"discussion|analysis|讨论|分析"),
    ]

    PRESERVE_PATTERNS = [
        r"@[a-zA-Z0-9_-]+",  # Citations @key
        r"#cite\([^)]+\)",  # Function calls #cite()
        r"#figure\([^)]+\)",  # Figures
        r"#table\([^)]+\)",  # Tables
        r"\$[^$]+\$",  # Math $...$
        r"//.*",  # Line comments
        r"/\*.*?\*/",  # Block comments
        r"<[a-zA-Z0-9_-]+>",  # Labels <label>
        r"#link\([^)]+\)",  # Links
    ]

    def get_comment_prefix(self) -> str:
        return "//"

    def _classify_heading(self, heading: dict[str, Any]) -> str | None:
        title = re.sub(r"\s+", " ", heading["title"]).strip().lower()
        for key, max_level, pattern in self.SECTION_TITLE_RULES:
            if heading["level"] <= max_level and re.search(pattern, title):
                return key
        return None

    def split_sections(self, content: str) -> dict[str, tuple[int, int]]:
        lines_total = len(content.split("\n"))
        headings = self.extract_headings(content)
        return _split_sections_from_headings(headings, self._classify_heading, lines_total)

    def extract_visible_text(self, line: str) -> str:
        # Same logic as LatexParser but with Typst patterns
        temp_line = line

        # Remove comments first for Typst
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
        # Blank out block comments (which may wrap a heading line) while keeping
        # line numbers intact, so "/* = Old Heading */" is never parsed.
        content = re.sub(
            r"/\*.*?\*/",
            lambda m: re.sub(r"[^\n]", " ", m.group()),
            content,
            flags=re.DOTALL,
        )
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

    def clean_text(self, content: str, keep_structure: bool = False) -> str:
        # Remove comments
        content = re.sub(r"//.*", "", content)
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

        # Remove math
        content = re.sub(r"\$[^$]+\$", "", content)

        # Handle headers
        if keep_structure:
            content = re.sub(r"^=+\s+(.+)$", r"\n\n## \1\n\n", content, flags=re.MULTILINE)
        else:
            content = re.sub(r"^=+\s+.+$", "", content, flags=re.MULTILINE)

        # Remove function calls #func(...) - basic support
        content = re.sub(r"#[a-zA-Z0-9_]+\([^)]*\)", "", content)
        content = re.sub(r"@[a-zA-Z0-9_-]+", "", content)
        content = re.sub(r"<[a-zA-Z0-9_-]+>", "", content)

        # Cleanup
        content = re.sub(r"\n+", "\n", content)
        content = re.sub(r" +", " ", content)
        content = re.sub(r"\.(\s*\.)+", ".", content)  # Fix multiple periods
        return content.strip()


def get_parser(
    file_path: Any,
    pdf_mode: str = "basic",
    heading_pt: float = 14.0,
    body_pt: float = 12.0,
) -> "DocumentParser":
    """
    Factory method extended for paper-audit to dispatch .tex / .typ / .pdf.

    Args:
        file_path: Path to the document file.
        pdf_mode: PDF extraction mode - "basic" (pymupdf) or "enhanced" (pymupdf4llm).
        heading_pt: Font size threshold (pt) for H2-level headings in PDF basic mode.
        body_pt: Font size threshold (pt) for H3-level headings in PDF basic mode.

    Returns:
        Appropriate DocumentParser instance.

    Raises:
        ValueError: If the file format is not supported.
    """
    path_str = str(file_path).lower()

    if path_str.endswith(".typ"):
        return TypstParser()
    elif path_str.endswith(".tex"):
        return LatexParser()
    elif path_str.endswith(".pdf"):
        from pdf_parser import PdfParser

        return PdfParser(mode=pdf_mode, heading_pt=heading_pt, body_pt=body_pt)
    else:
        raise ValueError(
            f"Unsupported format: {Path(file_path).suffix}. Supported formats: .tex, .typ, .pdf"
        )


def _normalize_whitespace(text: str) -> str:
    """Collapse whitespace to single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def _extract_balanced_block(content: str, start_idx: int, opener: str, closer: str) -> str:
    """Extract a balanced block body from content starting at opener index."""
    if start_idx < 0 or start_idx >= len(content) or content[start_idx] != opener:
        return ""

    depth = 0
    block_start = -1

    for i in range(start_idx, len(content)):
        char = content[i]
        if char == opener:
            depth += 1
            if depth == 1:
                block_start = i + 1
        elif char == closer:
            depth -= 1
            if depth == 0 and block_start >= 0:
                return content[block_start:i]
            if depth < 0:
                return ""
    return ""


def _extract_template_arg(content: str, arg: str) -> str:
    """Extract a named argument from a Typst template invocation.

    Universe templates are configured as ``#show: ieee.with(title: [..],
    abstract: [..])``; the title / abstract live in the ``.with(..)`` call
    rather than ``#set document(..)``. Supports both content ``[..]`` and
    string ``"..."`` argument values.
    """
    show = re.search(r"#show\s*:\s*[\w.-]+\.with\s*\(", content)
    if not show:
        return ""
    region = content[show.end() - 1 :]  # start at the opening '('
    arg_match = re.search(rf"(?:\(|,)\s*{re.escape(arg)}\s*:\s*", region)
    if not arg_match:
        return ""
    idx = arg_match.end()
    if idx < len(region) and region[idx] == "[":
        block = _extract_balanced_block(region, idx, "[", "]")
        return _strip_typst_markup(block)
    str_match = re.match(r'"([^"]*)"', region[idx:])
    if str_match:
        return _normalize_whitespace(str_match.group(1))
    return ""


def _strip_typst_markup(text: str) -> str:
    """Strip lightweight Typst markup for title/abstract extraction."""
    cleaned = text
    cleaned = re.sub(r"#\w+\([^)]*\)", " ", cleaned)

    # Collapse simple bracket macros repeatedly (e.g., #emph[Paper], nested forms).
    while True:
        collapsed = re.sub(r"#\w+\[([^\[\]]*)\]", r"\1", cleaned)
        if collapsed == cleaned:
            break
        cleaned = collapsed

    cleaned = re.sub(r"[\[\]]", " ", cleaned)
    return _normalize_whitespace(cleaned)


def _strip_latex_markup(text: str) -> str:
    """Strip lightweight LaTeX markup for title/abstract extraction."""
    cleaned = text
    cleaned = re.sub(r"(?<!\\)%.*", "", cleaned)
    cleaned = re.sub(r"\$[^$]*\$", " ", cleaned)
    cleaned = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?{([^{}]*)}", r"\1", cleaned)
    cleaned = re.sub(r"\\[a-zA-Z]+\*?", " ", cleaned)
    cleaned = re.sub(r"[{}]", " ", cleaned)
    return _normalize_whitespace(cleaned)


def extract_title(content: str) -> str:
    """Extract document title from LaTeX/Typst source content."""
    # LaTeX: \title{...}
    latex_match = re.search(r"\\title(?:\[[^\]]*\])?\{(.+?)\}", content, re.DOTALL)
    if latex_match:
        return _strip_latex_markup(latex_match.group(1))

    # Typst template form: #show: ieee.with(title: [ ... ])
    template_title = _extract_template_arg(content, "title")
    if template_title:
        return template_title

    # Typst common: #set document(title: "...")
    typst_str = re.search(
        r"#set\s+document\s*\(\s*title\s*:\s*\"([^\"]+)\"",
        content,
        re.DOTALL,
    )
    if typst_str:
        return _normalize_whitespace(typst_str.group(1))

    # Typst bracket style: #set document(title: [ ... ])
    typst_block = re.search(r"#set\s+document\s*\(\s*title\s*:\s*\[", content, re.DOTALL)
    if typst_block:
        bracket_idx = typst_block.end() - 1
        text = _extract_balanced_block(content, bracket_idx, "[", "]")
        if text:
            return _strip_typst_markup(text)

    return ""


def extract_abstract(content: str) -> str:
    """Extract abstract text from LaTeX/Typst source content."""
    # LaTeX abstract environment
    latex_abs = re.search(r"\\begin{abstract}(.*?)\\end{abstract}", content, re.DOTALL)
    if latex_abs:
        return _strip_latex_markup(latex_abs.group(1))

    # LaTeX section-based abstract
    sec_abs = re.search(
        r"\\section\*?\{Abstract\}(.*?)(?=\\section\*?\{|\\end\{document\}|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if sec_abs:
        return _strip_latex_markup(sec_abs.group(1))

    # Typst template form: #show: ieee.with(abstract: [ ... ])
    template_abs = _extract_template_arg(content, "abstract")
    if template_abs:
        return template_abs

    # Typst: #abstract[...]
    typst_abs = re.search(r"#abstract\[", content, re.DOTALL)
    if typst_abs:
        bracket_idx = typst_abs.end() - 1
        text = _extract_balanced_block(content, bracket_idx, "[", "]")
        if text:
            return _strip_typst_markup(text)

    # Typst heading-based abstract: "= Abstract" / "= 摘要"
    typst_heading_abs = re.search(
        r"^=\s+(?:摘要|[Aa]bstract)\s*\n(.*?)(?=^=\s+|\Z)",
        content,
        re.DOTALL | re.MULTILINE,
    )
    if typst_heading_abs:
        return _strip_typst_markup(typst_heading_abs.group(1))

    return ""


def extract_latex_citation_keys(content: str) -> set[str]:
    """
    Extract citation keys from LaTeX source.
    Supports \\cite, \\citep, \\citet, \\nocite and variants with optional arguments.
    """
    keys: set[str] = set()
    pattern = re.compile(r"\\(?:cite\w*|nocite)\*?(?:\[[^\]]*\]\s*)*\{([^}]*)\}")
    for match in pattern.finditer(content):
        raw = match.group(1)
        for key in raw.split(","):
            normalized = key.strip()
            if normalized:
                keys.add(normalized)
    return keys
