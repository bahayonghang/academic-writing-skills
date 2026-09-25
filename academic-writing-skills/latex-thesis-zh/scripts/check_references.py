#!/usr/bin/env python3
"""
Figure/Table/Equation Reference Integrity Checker for LaTeX (Chinese theses).

Extends the single-file checker with multi-file support via \\input{} and \\include{}.
Resolves included files relative to the main file's directory.

Usage:
    uv run python check_references.py main.tex
    uv run python check_references.py main.tex --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from tex_loader import AssembledDocument, assemble, iter_files
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from tex_loader import AssembledDocument, assemble, iter_files

# ---------------------------------------------------------------------------
# Regex patterns (LaTeX, multi-file)
# ---------------------------------------------------------------------------

LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
# Chinese theses may also use \hyperref[label]{text}
REF_RE = re.compile(
    r"\\(?:ref|eqref|autoref|cref|Cref|pageref)\{([^}]+)\}"
    r"|\\hyperref\[([^\]]+)\]\{[^}]*\}"
)
CAPTION_RE = re.compile(r"\\(?:bi)?caption\b\s*(?:\[[^\]]*\]\s*)?\{")
FIGURE_ENV_RE = re.compile(r"\\begin\{(figure|table)\*?\}")
FIGURE_ENV_END_RE = re.compile(r"\\end\{(figure|table)\*?\}")
COMMENT_PREFIX = "%"
SCHOOL_CHOICES = ("yanshan-ee-2025", "generic")
_COLLEGE_SCHOOL = "yanshan-ee-2025"
_FIGURE_FLOATS = {"figure", "figure*", "sidewaysfigure"}
_CJK_END_PUNCT = "。！？；，、："
_CAPTION_CMD_RE = re.compile(r"\\(caption|bicaption)\b")
_ENV_TOKEN_RE = re.compile(r"\\(begin|end)\{([A-Za-z*]+)\}")

# Prefixes tracked for "unreferenced label" warnings
TRACKED_PREFIXES = {"fig", "tab", "eq"}

# Prefixes checked for reference-before-definition ordering
ORDERING_PREFIXES = {"fig", "tab"}


@dataclass
class LabelInfo:
    """Label definition information."""

    name: str  # Full label name (e.g., "fig:arch")
    prefix: str  # Prefix (e.g., "fig", "tab", "eq")
    line: int  # Definition line number (1-indexed, within the source file)
    file: str  # Source file path


@dataclass
class RefInfo:
    """Reference information."""

    name: str  # Referenced label name
    line: int  # Reference line number (1-indexed, within the source file)
    file: str  # Source file path
    command: str  # Reference command (e.g., "ref", "eqref", "hyperref")


# ---------------------------------------------------------------------------
# Single-file checker (base)
# ---------------------------------------------------------------------------


class ReferenceChecker:
    """Single-file LaTeX reference integrity checker."""

    def __init__(self, content: str, file_path: str = "", school: str = "generic") -> None:
        self.content = content
        self.file_path = file_path
        self.lines = content.splitlines()
        self.issues: list[dict] = []
        self.school = school

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_comment_line(self, line: str) -> bool:
        """Return True if the line (after stripping) is a LaTeX comment."""
        return line.lstrip().startswith(COMMENT_PREFIX)

    def _strip_comment(self, line: str) -> str:
        """Remove LaTeX inline comment from a line (handles escaped %)."""
        return re.sub(r"(?<!\\)%.*", "", line)

    def _add_issue(
        self,
        line: int,
        severity: str,
        priority: str,
        message: str,
        file: str | None = None,
    ) -> None:
        """Append a structured issue dict."""
        self.issues.append(
            {
                "module": "REFERENCES",
                "file": file if file is not None else self.file_path,
                "line": line,
                "severity": severity,
                "priority": priority,
                "message": message,
            }
        )

    @staticmethod
    def _extract_prefix(label_name: str) -> str:
        """Extract the prefix of a label (part before first colon)."""
        if ":" in label_name:
            return label_name.split(":")[0]
        return ""

    # ------------------------------------------------------------------
    # Finders
    # ------------------------------------------------------------------

    def find_labels(self) -> list[LabelInfo]:
        """Find all \\label{} definitions in self.content, skipping comment lines."""
        labels: list[LabelInfo] = []
        for lineno, raw_line in enumerate(self.lines, start=1):
            if self._is_comment_line(raw_line):
                continue
            line = self._strip_comment(raw_line)
            for match in LABEL_RE.finditer(line):
                name = match.group(1).strip()
                prefix = self._extract_prefix(name)
                labels.append(LabelInfo(name=name, prefix=prefix, line=lineno, file=self.file_path))
        return labels

    def find_refs(self) -> list[RefInfo]:
        """Find all reference commands in self.content, skipping comment lines."""
        refs: list[RefInfo] = []
        for lineno, raw_line in enumerate(self.lines, start=1):
            if self._is_comment_line(raw_line):
                continue
            line = self._strip_comment(raw_line)
            for match in REF_RE.finditer(line):
                # Group 1: standard \ref{...} family; group 2: \hyperref[...]{...}
                name = (match.group(1) or match.group(2) or "").strip()
                if not name:
                    continue
                # Determine command
                full = match.group(0)
                if full.startswith(r"\hyperref"):
                    command = "hyperref"
                else:
                    cmd_match = re.match(r"\\(\w+)\{", full)
                    command = cmd_match.group(1) if cmd_match else "ref"
                refs.append(RefInfo(name=name, line=lineno, file=self.file_path, command=command))
        return refs

    # ------------------------------------------------------------------
    # Checks
    # ------------------------------------------------------------------

    def check_undefined_refs(self, labels: list[LabelInfo], refs: list[RefInfo]) -> None:
        """Check for \\ref{x} where no \\label{x} exists. Severity: Critical, P0."""
        defined = {lbl.name for lbl in labels}
        for ref in refs:
            if ref.name not in defined:
                self._add_issue(
                    line=ref.line,
                    file=ref.file,
                    severity="Critical",
                    priority="P0",
                    message=(
                        f"Undefined reference: \\{ref.command}{{{ref.name}}} "
                        f"— no matching \\label found"
                    ),
                )

    def check_unreferenced_labels(self, labels: list[LabelInfo], refs: list[RefInfo]) -> None:
        """Check \\label{x} never referenced (fig:, tab:, eq: only). Severity: Minor, P2."""
        referenced = {ref.name for ref in refs}
        for lbl in labels:
            if lbl.prefix in TRACKED_PREFIXES and lbl.name not in referenced:
                self._add_issue(
                    line=lbl.line,
                    file=lbl.file,
                    severity="Minor",
                    priority="P2",
                    message=f"Unreferenced label: \\label{{{lbl.name}}} is never cited in text",
                )

    def check_caption_presence(self, labels: list[LabelInfo]) -> None:
        """
        Check that figure/table environments containing \\label{fig:*} or \\label{tab:*}
        also contain a \\caption or \\bicaption. Severity: Major, P1.
        """
        # Build list of (start_line, end_line, env_type) from self.lines
        envs: list[tuple[int, int, str]] = []
        stack: list[tuple[int, str]] = []

        for lineno, raw_line in enumerate(self.lines, start=1):
            if self._is_comment_line(raw_line):
                continue
            line = self._strip_comment(raw_line)
            begin_match = FIGURE_ENV_RE.search(line)
            if begin_match:
                stack.append((lineno, begin_match.group(1)))
            end_match = FIGURE_ENV_END_RE.search(line)
            if end_match and stack:
                start_lineno, env_type = stack.pop()
                envs.append((start_lineno, lineno, env_type))

        for lbl in labels:
            if lbl.prefix not in ("fig", "tab"):
                continue
            enclosing = None
            for start, end, env_type in envs:
                if start <= lbl.line <= end:
                    enclosing = (start, end, env_type)
                    break
            if enclosing is None:
                continue
            start, end, env_type = enclosing
            env_text = "\n".join(self._strip_comment(line) for line in self.lines[start - 1 : end])
            if not CAPTION_RE.search(env_text):
                self._add_issue(
                    line=lbl.line,
                    file=lbl.file,
                    severity="Major",
                    priority="P1",
                    message=(
                        f"Missing caption in {env_type} environment: "
                        f"\\label{{{lbl.name}}} at line {lbl.line} has no \\caption"
                    ),
                )

    def check_ordering(self, labels: list[LabelInfo], refs: list[RefInfo]) -> None:
        """
        Check that first \\ref{x} does not appear before \\label{x} (same file only).
        Only for fig:/tab: prefixes. Severity: Minor, P2.
        """
        label_lines: dict[str, int] = {lbl.name: lbl.line for lbl in labels}
        first_ref_lines: dict[str, int] = {}
        for ref in refs:
            if ref.name not in first_ref_lines or ref.line < first_ref_lines[ref.name]:
                first_ref_lines[ref.name] = ref.line

        for name, ref_line in first_ref_lines.items():
            prefix = self._extract_prefix(name)
            if prefix not in ORDERING_PREFIXES:
                continue
            if name in label_lines and ref_line < label_lines[name]:
                self._add_issue(
                    line=ref_line,
                    file=next((ref.file for ref in refs if ref.name == name), self.file_path),
                    severity="Minor",
                    priority="P2",
                    message=(
                        f"Reference before definition: \\ref{{{name}}} at line {ref_line} "
                        f"appears before \\label{{{name}}} at line {label_lines[name]}"
                    ),
                )

    def check_numbering_gaps(self, labels: list[LabelInfo]) -> None:
        """
        Detect numbering gaps for labels with numeric suffixes.
        Severity: Minor, P2.
        """
        numeric_suffix_re = re.compile(r"^(.*?)(\d+)$")
        series: dict[str, list[tuple[int, int, str]]] = {}

        for lbl in labels:
            m = numeric_suffix_re.match(lbl.name)
            if not m:
                continue
            base = m.group(1)
            num = int(m.group(2))
            if base not in series:
                series[base] = []
            series[base].append((num, lbl.line, lbl.file))

        for series_key, entries in series.items():
            if len(entries) < 2:
                continue
            entries_sorted = sorted(entries, key=lambda x: x[0])
            numbers = [e[0] for e in entries_sorted]
            for i in range(len(numbers) - 1):
                if numbers[i + 1] - numbers[i] > 1:
                    missing_start = numbers[i] + 1
                    missing_end = numbers[i + 1] - 1
                    missing_range = (
                        str(missing_start)
                        if missing_start == missing_end
                        else f"{missing_start}–{missing_end}"
                    )
                    report_line = entries_sorted[i][1]
                    self._add_issue(
                        line=report_line,
                        file=entries_sorted[i][2],
                        severity="Minor",
                        priority="P2",
                        message=(
                            f"Numbering gap detected: {series_key}{missing_range} "
                            f"missing between {series_key}{numbers[i]} and "
                            f"{series_key}{numbers[i + 1]}"
                        ),
                    )

    # ------------------------------------------------------------------
    # Runner
    # ------------------------------------------------------------------

    def check_college_figure_captions(self) -> None:
        """Chinese terminal punctuation on non-table floats. Tables stay in check_tables."""
        text = _mask_comments(self.content)
        envs, unbalanced = _scan_envs(text)
        if unbalanced:
            self._college_issue(1, "CAP-COVERAGE", "浮动体环境未闭合，覆盖不足，不作为通过")
        for name, _begin, body_start, body_end, _end in envs:
            if name not in _FIGURE_FLOATS:
                continue
            body = text[body_start:body_end]
            for match in _CAPTION_CMD_RE.finditer(body):
                status, chinese = _chinese_caption_arg(body, match.start(), match.group(1))
                line = text.count("\n", 0, body_start + match.start()) + 1
                if status != "ok":
                    self._college_issue(
                        line, "CAP-COVERAGE", "无法确认中文题注主参数，留人工，不作为通过"
                    )
                    continue
                visible = _caption_visible(chinese or "")
                if visible and visible[-1] in _CJK_END_PUNCT:
                    self._college_issue(
                        line,
                        "CAP-PUNCT",
                        "中文题注可见正文以中文标点结束。英文句点、可选短题注和"
                        " \\bicaption 第二参数不计",
                    )

    def _college_issue(self, line: int, code: str, detail: str) -> None:
        self.issues.append(
            {
                "module": "REFERENCES",
                "file": self.file_path,
                "line": line,
                "severity": "Info",
                "priority": "P3",
                "message": f"[Script] Meaning-Check: NEEDS-LLM {code}: {detail}",
                "code": code,
                "meaning_check": "NEEDS-LLM",
                "layer": "[Script]",
            }
        )

    def run_all(self) -> list[dict]:
        """Run all checks and return the full issues list."""
        self.issues = []
        labels = self.find_labels()
        refs = self.find_refs()
        self.check_undefined_refs(labels, refs)
        self.check_unreferenced_labels(labels, refs)
        self.check_caption_presence(labels)
        self.check_ordering(labels, refs)
        self.check_numbering_gaps(labels)
        if self.school == _COLLEGE_SCHOOL:
            self.check_college_figure_captions()
        return self.issues


# ---------------------------------------------------------------------------
# Multi-file checker (ThesisReferenceChecker)
# ---------------------------------------------------------------------------


class ThesisReferenceChecker(ReferenceChecker):
    """
    Multi-file reference checker supporting \\input and \\include.

    Resolves included files relative to the main file's directory and
    adds .tex extension automatically if missing.  Labels and references
    are tracked per-file so ordering checks remain meaningful.
    """

    INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")

    def __init__(
        self,
        main_file: str,
        school: str = "generic",
        *,
        author_cite: bool = False,
        repeat_cite: bool = False,
    ) -> None:
        self.main_file = Path(main_file).resolve()
        self.base_dir = self.main_file.parent
        self.author_cite = author_cite
        self.repeat_cite = repeat_cite
        # Map from resolved file path -> file content (via the shared
        # tex_loader resolver: encoding-robust, cycle-safe, comment-aware)
        self.all_files: dict[str, str] = {}
        self.encoding_warnings: list[str] = []
        for node in iter_files(self.main_file):
            if node.exists and node.content is not None:
                self.all_files[node.rel] = node.content
                if node.warning:
                    self.encoding_warnings.append(node.warning)
        # Build combined content (used by base class for caption/env detection)
        combined = "\n".join(self.all_files.values())
        super().__init__(combined, str(self.main_file), school)
        self.multi_file = len(self.all_files) > 1
        # Per-file label/ref lists (populated by _scan_all_files)
        self._all_labels: list[LabelInfo] = []
        self._all_refs: list[RefInfo] = []
        self._scan_all_files()

    def _scan_all_files(self) -> None:
        """Scan every loaded file to collect per-file labels and refs."""
        for file_path_str, content in self.all_files.items():
            checker = ReferenceChecker(content, file_path_str)
            self._all_labels.extend(checker.find_labels())
            self._all_refs.extend(checker.find_refs())

    # Override run_all to use the cross-file label/ref sets
    def run_all(self) -> list[dict]:
        """Run all checks across all resolved files."""
        self.issues = []
        labels = self._all_labels
        refs = self._all_refs
        self.check_undefined_refs(labels, refs)
        self.check_unreferenced_labels(labels, refs)
        # Caption check: run per-file so line numbers are valid
        for file_path_str, content in self.all_files.items():
            per_file_checker = ReferenceChecker(content, file_path_str)
            per_file_labels = [lbl for lbl in labels if lbl.file == file_path_str]
            per_file_checker.check_caption_presence(per_file_labels)
            self.issues.extend(per_file_checker.issues)
        # Ordering: cross-file ordering is not meaningful, skip per-file
        for file_path_str in self.all_files:
            file_labels = [lbl for lbl in labels if lbl.file == file_path_str]
            file_refs = [ref for ref in refs if ref.file == file_path_str]
            if file_labels and file_refs:
                per = ReferenceChecker("", file_path_str)
                per.check_ordering(file_labels, file_refs)
                self.issues.extend(per.issues)
        self.check_numbering_gaps(labels)
        if self.school == _COLLEGE_SCHOOL:
            for file_path_str, content in self.all_files.items():
                per_file = ReferenceChecker(content, file_path_str, self.school)
                per_file.check_college_figure_captions()
                self.issues.extend(per_file.issues)
        if self.author_cite or self.repeat_cite:
            document = assemble(self.main_file)
            self.issues.extend(
                _citation_mode_issues(
                    document,
                    author_cite=self.author_cite,
                    repeat_cite=self.repeat_cite,
                )
            )
        return self.issues


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def _format_issues(issues: list[dict], comment_prefix: str = "%", multi_file: bool = False) -> str:
    """Format issues into the project's output protocol."""
    if not issues:
        return ""
    lines = []
    for issue in sorted(issues, key=lambda x: x.get("line") or 0):
        if multi_file and issue.get("file") and issue.get("line"):
            line_part = f"{issue['file']}:{issue['line']} "
        else:
            line_part = f"(Line {issue['line']}) " if issue.get("line") else ""
        lines.append(
            f"{comment_prefix} REFERENCES {line_part}"
            f"[Severity: {issue['severity']}] [Priority: {issue['priority']}]: "
            f"{issue['message']}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Reference Integrity Checker for LaTeX (Chinese theses, multi-file)"
    )
    parser.add_argument("file", help="Main .tex file to check")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument(
        "--school",
        choices=SCHOOL_CHOICES,
        default="generic",
        help="学院源码体例。仅 yanshan-ee-2025 启用非表浮动体中文题注候选；默认 generic",
    )
    parser.add_argument(
        "--author-cite",
        action="store_true",
        help="报告同句内明确作者短语之后的滞后引用。不传则不扫描",
    )
    parser.add_argument(
        "--repeat-cite",
        action="store_true",
        help="报告重复引用键缺少字面页码 postnote 的位置。不传则不扫描",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    checker = ThesisReferenceChecker(
        str(path),
        school=args.school,
        author_cite=args.author_cite,
        repeat_cite=args.repeat_cite,
    )
    issues = checker.run_all()

    for warning in checker.encoding_warnings:
        print(f"{COMMENT_PREFIX} REFERENCES [WARN]: {warning}", file=sys.stderr)

    if args.json:
        print(json.dumps(issues, indent=2, ensure_ascii=False))
    else:
        output = _format_issues(
            issues, comment_prefix=COMMENT_PREFIX, multi_file=checker.multi_file
        )
        if output:
            print(output)

    has_critical = any(i["severity"] == "Critical" for i in issues)
    return 1 if has_critical else 0


def _mask_comments(text: str) -> str:
    chars = list(text)
    index = 0
    while index < len(chars):
        if chars[index] == "%" and not _escaped(chars, index):
            while index < len(chars) and chars[index] != "\n":
                chars[index] = " "
                index += 1
            continue
        index += 1
    return "".join(chars)


def _escaped(chars: list[str], index: int) -> bool:
    slashes = 0
    cursor = index - 1
    while cursor >= 0 and chars[cursor] == "\\":
        slashes += 1
        cursor -= 1
    return slashes % 2 == 1


def _scan_envs(text: str) -> tuple[list[tuple[str, int, int, int, int]], bool]:
    stack: list[tuple[str, int, int]] = []
    found: list[tuple[str, int, int, int, int]] = []
    unbalanced = False
    for match in _ENV_TOKEN_RE.finditer(text):
        kind, name = match.group(1), match.group(2)
        if kind == "begin":
            stack.append((name, match.start(), match.end()))
            continue
        if stack and stack[-1][0] == name:
            bname, bstart, body_start = stack.pop()
            found.append((bname, bstart, body_start, match.start(), match.end()))
        else:
            unbalanced = True
    if stack:
        unbalanced = True
    return found, unbalanced


def _chinese_caption_arg(text: str, start: int, command: str) -> tuple[str, str | None]:
    index = _skip_ws(text, start + len(command) + 1)
    if index < len(text) and text[index] == "*":
        index = _skip_ws(text, index + 1)
    limit = 2 if command == "bicaption" else 1
    for _ in range(limit):
        if index < len(text) and text[index] == "[":
            group = _read_group(text, index, "[", "]")
            if group is None:
                return "manual", None
            _, index = group
            index = _skip_ws(text, index)
        else:
            break
    if index >= len(text) or text[index] != "{":
        return "manual", None
    group = _read_group(text, index, "{", "}")
    if group is None:
        return "manual", None
    return "ok", group[0]


def _skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t\r\n":
        index += 1
    return index


def _read_group(text: str, index: int, open_ch: str, close_ch: str) -> tuple[str, int] | None:
    if index >= len(text) or text[index] != open_ch:
        return None
    depth = 1
    cursor = index + 1
    while cursor < len(text):
        if text[cursor] == "\\" and cursor + 1 < len(text):
            cursor += 2
            continue
        if text[cursor] == open_ch:
            depth += 1
        elif text[cursor] == close_ch:
            depth -= 1
            if depth == 0:
                return text[index + 1 : cursor], cursor + 1
        cursor += 1
    return None


def _caption_visible(body: str) -> str:
    body = re.sub(r"(?<!\\)%.*", "", body)
    body = re.sub(r"(?<!\\)\$(?:\\.|[^$])*\$", " ", body)
    body = re.sub(
        r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|pageref|label)\*?\{[^{}]*\}",
        " ",
        body,
    )
    body = re.sub(r"\\[A-Za-z]+\*?", "", body)
    body = body.replace("{", "").replace("}", "")
    return body.strip()


_SUPPORTED_CITES = {"cite", "citep", "citet", "parencite", "textcite", "autocite", "footcite"}
_AUTHOR_CITE_SKIP = {"citet", "textcite"}
_MULTI_CITES = {
    "cites",
    "citeps",
    "citets",
    "parencites",
    "textcites",
    "autocites",
    "footcites",
}
_NOCOUNT_CITES = {"nocite"}
_DEF_NEW = {
    "newcommand",
    "renewcommand",
    "providecommand",
    "DeclareRobustCommand",
    "newrobustcmd",
    "renewrobustcmd",
}
_DEF_ENV = {"newenvironment", "renewenvironment"}
_DEF_PRIM = {"def", "edef", "gdef", "xdef"}
_DEF_COMMANDS = _DEF_NEW | _DEF_ENV | _DEF_PRIM
_SKIP_ENVS = {
    "verbatim",
    "verbatim*",
    "Verbatim",
    "lstlisting",
    "minted",
    "alltt",
    "thebibliography",
}
_PARTICLE_WORDS = {"van", "von", "de", "da", "di", "del", "della", "der", "den", "bin", "al"}
_LATIN_STOP = {
    "the",
    "this",
    "that",
    "these",
    "those",
    "however",
    "therefore",
    "moreover",
    "furthermore",
    "using",
    "based",
    "after",
    "before",
    "when",
    "where",
    "while",
    "such",
    "other",
    "some",
    "many",
    "most",
    "both",
    "each",
    "any",
    "all",
    "here",
    "there",
    "also",
    "then",
    "thus",
    "hence",
    "via",
    "per",
    "from",
    "into",
    "over",
    "under",
    "their",
    "our",
    "and",
    "but",
    "not",
    "for",
    "with",
    "its",
    "his",
    "her",
    "fig",
    "figure",
    "table",
    "tab",
    "eq",
    "equation",
    "section",
    "chapter",
    "note",
    "see",
    "in",
    "on",
    "at",
    "by",
    "to",
    "of",
    "or",
    "an",
    "as",
    "if",
    "so",
    "yet",
    "are",
    "was",
    "were",
    "been",
    "have",
    "has",
    "had",
    "can",
    "may",
    "one",
    "two",
    "new",
    "first",
    "second",
    "third",
    "above",
    "below",
    "between",
    "among",
    "during",
    "within",
    "without",
    "about",
}
_CN_STOP = frozenset(
    {
        "文献",
        "研究",
        "本文",
        "作者",
        "工作",
        "方法",
        "结果",
        "实验",
        "论文",
        "已有",
        "已有研究",
        "相关",
        "上述",
        "这些",
        "那些",
        "其他",
        "其它",
        "部分",
        "我们",
        "他们",
        "内容",
        "问题",
        "系统",
        "模型",
        "数据",
        "分析",
        "讨论",
        "综述",
        "方案",
        "技术",
        "算法",
        "过程",
        "条件",
        "结构",
        "框架",
        "平台",
        "参数",
        "指标",
        "标准",
        "要求",
        "目的",
        "背景",
        "现状",
        "趋势",
        "方向",
        "策略",
        "机制",
        "原理",
        "理论",
        "公式",
        "图像",
        "信号",
        "误差",
        "精度",
        "效率",
        "样品",
        "材料",
        "设备",
        "阶段",
        "步骤",
        "流程",
        "现象",
        "特征",
        "性能",
        "效果",
        "影响",
        "因素",
        "方面",
        "路径",
        "范围",
        "对象",
        "目标",
        "任务",
        "场景",
        "环境",
        "网络",
        "函数",
        "变量",
        "样本",
        "训练",
        "测试",
        "验证",
        "比较",
    }
)
_ABBREV_WORDS = {
    "al",
    "etc",
    "fig",
    "eq",
    "eqs",
    "vs",
    "dr",
    "mr",
    "mrs",
    "ms",
    "prof",
    "cf",
    "ibid",
    "ed",
    "eds",
    "vol",
    "no",
    "nos",
    "pp",
    "p",
    "st",
    "jr",
    "sr",
}
_CAP_WORD = r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ'’\-]{2,}"
_PARTICLE = r"(?:van|von|de|da|di|del|della|der|den|bin|al)"
_LATIN_NAME = rf"(?:{_PARTICLE}\s+){{0,3}}{_CAP_WORD}(?:[-\s]+{_CAP_WORD}){{0,2}}"
_LATIN_AUTHOR = re.compile(
    rf"(?<![A-Za-zÀ-ÖØ-öø-ÿ])"
    rf"(?P<name>{_LATIN_NAME})"
    rf"(?P<tail>(?:\s+et\s+al\.?)|(?:\s*等人|\s*等))?"
)
_CN_ET = re.compile(r"(?<![\u4e00-\u9fff])(?P<name>[\u4e00-\u9fff]{1,4})(?P<etal>等人|等)(?!等)")
_PRED_RE = re.compile(
    r"提出|指出|表明|认为|发现|报道|报告|分析|设计|给出|建立|构建|引入|采用|证明|证实|"
    r"讨论|综述|比较|说明|论述|探讨|展示|描述|观察|定义|建议|声称|开发|实现|验证|公布|发表|研究|"
    r"\b(?:proposed|proposes|showed|shown|shows|reported|reports|found|finds|"
    r"demonstrated|demonstrates|argued|argues|noted|notes|observed|observes|"
    r"introduced|introduces|designed|designs|developed|develops|presented|presents|"
    r"suggested|suggests|claimed|claims|analyzed|analysed|discussed|discusses|"
    r"compared|compares|reviewed|reviews|established|establishes|proved|proves|"
    r"indicated|indicates|described|describes)\b",
    re.IGNORECASE,
)
_ROMAN_ATOM = r"M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})"
_PAGE_ATOM = rf"(?:[0-9]+|(?=[IVXLCDM])(?:{_ROMAN_ATOM}))"
_PAGE_RE = re.compile(rf"(?i)^\s*{_PAGE_ATOM}(?:\s*(?:--|–|—|-)\s*{_PAGE_ATOM})?\s*$")


@dataclass
class _RawCite:
    command: str
    keys: list[str]
    postnote: str
    start: int
    end: int
    file: str = ""
    line: int = 1
    shared: bool = False
    literal_page: bool = False

    @property
    def empty(self) -> bool:
        return not self.postnote.strip()

    @property
    def proven(self) -> bool:
        return self.literal_page and not self.empty and not self.shared


def _citation_mode_issues(
    document: AssembledDocument,
    *,
    author_cite: bool,
    repeat_cite: bool,
) -> list[dict]:
    """Opt-in author placement and repeat-page candidates. Not called when both flags are off."""
    source = document.content
    masked = _mask_comments(source)
    chars = list(masked)
    cites = _scan_cites(masked, chars)
    _place_cites(document, source, cites)
    issues: list[dict] = []
    if author_cite:
        rel, line = document.origin(1)
        issues.append(
            _cite_issue(
                rel,
                line,
                "RC-AUTHOR-COVERAGE",
                "未把每个2–4字中文词当作姓名。作者主语不确定时只作候选或覆盖说明，"
                "不宣称识别出作者。不跨不完整句或段落绑定。",
            )
        )
        issues.extend(_author_cite_issues(document, source, chars, cites))
    if repeat_cite:
        issues.extend(_repeat_cite_issues(document, cites))
    return issues


def _cite_issue(file: str, line: int, code: str, detail: str) -> dict:
    return {
        "module": "REFERENCES",
        "file": file,
        "line": line,
        "severity": "Info",
        "priority": "P3",
        "message": f"[Script] Meaning-Check: NEEDS-LLM {code}: {detail}",
        "code": code,
        "meaning_check": "NEEDS-LLM",
        "layer": "[Script]",
    }


def _place_cites(document: AssembledDocument, source: str, cites: list[_RawCite]) -> None:
    for cite in cites:
        assembled = source.count("\n", 0, cite.start) + 1
        cite.file, cite.line = document.origin(assembled)
        stripped = cite.postnote.strip()
        cite.literal_page = bool(stripped) and _PAGE_RE.match(stripped) is not None
        cite.shared = len(cite.keys) > 1 and bool(stripped)


def _scan_cites(masked: str, chars: list[str]) -> list[_RawCite]:
    found: list[_RawCite] = []
    index = 0
    length = len(masked)
    while index < length:
        if masked[index] != "\\" or _escaped_at(masked, index):
            index += 1
            continue
        name, name_end = _command_name(masked, index)
        if not name:
            index += 1
            continue
        if name == "begin":
            env_name, env_end = _env_name(masked, name_end)
            if env_name in _SKIP_ENVS:
                token = "\\end{" + env_name + "}"
                end_at = masked.find(token, env_end)
                if end_at >= 0:
                    end_at += len(token)
                    _blank_chars(chars, index, end_at)
                    index = end_at
                    continue
            index = name_end
            continue
        if name == "verb":
            end_at = _verb_end(masked, name_end)
            if end_at is not None:
                _blank_chars(chars, index, end_at)
                index = end_at
                continue
            index = name_end
            continue
        if name in _DEF_COMMANDS:
            end_at = _skip_definition(masked, name, name_end)
            if end_at is not None:
                _blank_chars(chars, index, end_at)
                index = end_at
                continue
            index = name_end
            continue
        if name in _MULTI_CITES or name in _NOCOUNT_CITES:
            end_at = _consume_cite_groups(masked, name_end)
            index = end_at if end_at > index else name_end
            continue
        if name in _SUPPORTED_CITES:
            parsed = _parse_supported_cite(masked, name, name_end, index)
            if parsed is None:
                index = name_end
                continue
            found.append(parsed)
            index = parsed.end
            continue
        index = name_end
    return found


def _escaped_at(text: str, index: int) -> bool:
    slashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slashes += 1
        cursor -= 1
    return slashes % 2 == 1


def _command_name(text: str, index: int) -> tuple[str, int]:
    cursor = index + 1
    while cursor < len(text) and text[cursor].isalpha():
        cursor += 1
    if cursor == index + 1:
        return "", index + 1
    return text[index + 1 : cursor], cursor


def _env_name(text: str, name_end: int) -> tuple[str, int]:
    cursor = _skip_ws(text, name_end)
    group = _read_group(text, cursor, "{", "}")
    if group is None:
        return "", name_end
    return group[0], group[1]


def _verb_end(text: str, name_end: int) -> int | None:
    cursor = name_end
    if cursor < len(text) and text[cursor] == "*":
        cursor += 1
    if cursor >= len(text):
        return None
    delim = text[cursor]
    if delim.isalnum() or delim.isspace():
        return None
    end = text.find(delim, cursor + 1)
    if end < 0:
        return None
    return end + 1


def _skip_definition(text: str, name: str, name_end: int) -> int | None:
    cursor = name_end
    if cursor < len(text) and text[cursor] == "*":
        cursor += 1
    cursor = _skip_ws(text, cursor)
    if name in _DEF_PRIM:
        if cursor >= len(text) or text[cursor] != "\\":
            return None
        cursor += 1
        while cursor < len(text) and text[cursor].isalpha():
            cursor += 1
        while cursor < len(text) and text[cursor] != "{":
            if text[cursor] == "\\" and cursor + 1 < len(text):
                cursor += 2
                continue
            cursor += 1
        return None if cursor >= len(text) else _group_end(text, cursor, "{", "}")
    if cursor < len(text) and text[cursor] == "{":
        end = _group_end(text, cursor, "{", "}")
        if end is None:
            return None
        cursor = end
    elif cursor < len(text) and text[cursor] == "\\":
        cursor += 1
        while cursor < len(text) and text[cursor].isalpha():
            cursor += 1
    else:
        return None
    for _ in range(3):
        cursor = _skip_ws(text, cursor)
        if cursor < len(text) and text[cursor] == "[":
            end = _group_end(text, cursor, "[", "]")
            if end is None:
                return None
            cursor = end
        else:
            break
    for _ in range(2 if name in _DEF_ENV else 1):
        cursor = _skip_ws(text, cursor)
        end = _group_end(text, cursor, "{", "}")
        if end is None:
            return None
        cursor = end
    return cursor


def _group_end(text: str, index: int, open_ch: str, close_ch: str) -> int | None:
    group = _read_group(text, index, open_ch, close_ch)
    if group is None:
        return None
    return group[1]


def _consume_cite_groups(text: str, name_end: int) -> int:
    cursor = name_end
    if cursor < len(text) and text[cursor] == "*":
        cursor += 1
    for _ in range(12):
        cursor = _skip_ws(text, cursor)
        if cursor >= len(text) or text[cursor] not in "{[":
            break
        closer = "}" if text[cursor] == "{" else "]"
        end = _group_end(text, cursor, text[cursor], closer)
        if end is None:
            break
        cursor = end
    return cursor


def _parse_supported_cite(text: str, name: str, name_end: int, start: int) -> _RawCite | None:
    cursor = name_end
    if cursor < len(text) and text[cursor] == "*":
        cursor += 1
    cursor = _skip_ws(text, cursor)
    brackets: list[str] = []
    for _ in range(2):
        if cursor >= len(text) or text[cursor] != "[":
            break
        group = _read_group(text, cursor, "[", "]")
        if group is None:
            return None
        brackets.append(group[0])
        cursor = _skip_ws(text, group[1])
    if cursor < len(text) and text[cursor] == "[":
        return None
    if cursor >= len(text) or text[cursor] != "{":
        return None
    group = _read_group(text, cursor, "{", "}")
    if group is None:
        return None
    keys = _split_cite_keys(group[0])
    if not keys:
        return None
    if len(brackets) >= 2:
        postnote = brackets[1]
    elif len(brackets) == 1:
        postnote = brackets[0]
    else:
        postnote = ""
    return _RawCite(name, keys, postnote, start, group[1])


def _split_cite_keys(body: str) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    buffer: list[str] = []
    depth = 0
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body):
            buffer.append(char)
            buffer.append(body[index + 1])
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}" and depth:
            depth -= 1
        if char == "," and depth == 0:
            _append_cite_key(keys, seen, "".join(buffer))
            buffer = []
        else:
            buffer.append(char)
        index += 1
    _append_cite_key(keys, seen, "".join(buffer))
    return keys


def _append_cite_key(keys: list[str], seen: set[str], raw: str) -> None:
    key = raw.strip()
    if key and key not in seen:
        seen.add(key)
        keys.append(key)


def _blank_chars(chars: list[str], start: int, end: int) -> None:
    for index in range(start, min(end, len(chars))):
        if chars[index] != "\n":
            chars[index] = " "


def _author_visible(chars: list[str], cites: list[_RawCite]) -> str:
    view = chars[:]
    for cite in cites:
        _blank_chars(view, cite.start, cite.end)
    text = "".join(view)
    for pattern in (
        r"\$\$[\s\S]*?\$\$",
        r"(?<!\$)\$(?!\$)[^$\n]*\$",
        r"\\\[[\s\S]*?\\\]",
        r"\\\([\s\S]*?\\\)",
    ):
        text = re.sub(pattern, lambda match: _space_keep_newlines(match.group(0)), text)
    return text


def _space_keep_newlines(fragment: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in fragment)


def _author_cite_issues(
    document: AssembledDocument,
    source: str,
    chars: list[str],
    cites: list[_RawCite],
) -> list[dict]:
    visible = _author_visible(chars, cites)
    issues: list[dict] = []
    seen: set[tuple[str, str, int]] = set()
    for para_start, para_end in _paragraph_spans(visible):
        for sent_start, sent_end in _complete_sentences(visible, para_start, para_end):
            window = [cite for cite in cites if sent_start <= cite.start < sent_end]
            for match in _LATIN_AUTHOR.finditer(visible, sent_start, sent_end):
                if not _latin_clear(match.group("name")):
                    continue
                if not match.group("tail") and not _immediate_author_verb(
                    visible, match.end(), sent_end
                ):
                    continue
                _add_author_hit(
                    issues,
                    seen,
                    source,
                    visible,
                    window,
                    match.start(),
                    match.end(),
                    sent_end,
                    "RC-AUTHOR",
                    uncertain=False,
                )
            for match in _CN_ET.finditer(visible, sent_start, sent_end):
                if match.group("name") in _CN_STOP:
                    continue
                _add_author_hit(
                    issues,
                    seen,
                    source,
                    visible,
                    window,
                    match.start(),
                    match.end(),
                    sent_end,
                    "RC-AUTHOR-UNCERTAIN",
                    uncertain=True,
                )
            for name_start, name_end, pred_end in _bare_chinese(visible, sent_start, sent_end):
                _add_author_hit(
                    issues,
                    seen,
                    source,
                    visible,
                    window,
                    name_start,
                    name_end,
                    sent_end,
                    "RC-AUTHOR-UNCERTAIN",
                    uncertain=True,
                    predicate_end=pred_end,
                )
    _ = document
    return issues


def _latin_clear(name: str) -> bool:
    parts = [part for part in re.split(r"[\s-]+", name) if part]
    content = [part for part in parts if part.lower() not in _PARTICLE_WORDS]
    if not content or not any(char.islower() for char in "".join(content)):
        return False
    return not (len(content) == 1 and content[0].lower() in _LATIN_STOP)


_AUTHOR_VERB_RE = re.compile(
    r"提出|指出|认为|报道|发现|证明|构建|"
    r"(?:proposed|proposes|showed|shows|reported|reports|found|finds|"
    r"demonstrated|demonstrates|argued|argues|noted|notes|observed|observes|"
    r"introduced|introduces|designed|designs|developed|develops|presented|presents|"
    r"suggested|suggests|claimed|claims|analyzed|analysed|discussed|discusses|"
    r"compared|compares|reviewed|reviews|established|establishes|proved|proves|"
    r"indicated|indicates|described|describes)\b",
    re.IGNORECASE,
)


def _immediate_author_verb(visible: str, name_end: int, limit: int) -> bool:
    """A bare Latin name counts only when an authorship verb follows it directly."""
    index = name_end
    while index < limit and visible[index] in " \t　":
        index += 1
    return _AUTHOR_VERB_RE.match(visible, index, limit) is not None


def _is_cjk(char: str) -> bool:
    return "\u4e00" <= char <= "\u9fff"


def _bare_chinese(text: str, start: int, end: int) -> list[tuple[int, int, int]]:
    found: list[tuple[int, int, int]] = []
    index = start
    while index < end:
        if not _is_cjk(text[index]) or (index > start and _is_cjk(text[index - 1])):
            index += 1
            continue
        cursor = index
        while cursor < end and _is_cjk(text[cursor]):
            cursor += 1
        run = text[index:cursor]
        upper = min(4, len(run) - 1)
        for length in range(upper, 1, -1):
            name = run[:length]
            if "等" in name or name in _CN_STOP:
                continue
            pred = _PRED_RE.match(run[length:])
            if pred is None:
                continue
            found.append((index, index + length, index + length + pred.end()))
            break
        index = cursor
    return found


def _add_author_hit(
    issues: list[dict],
    seen: set[tuple[str, str, int]],
    source: str,
    visible: str,
    window: list[_RawCite],
    phrase_start: int,
    phrase_end: int,
    sent_end: int,
    code: str,
    *,
    uncertain: bool,
    predicate_end: int | None = None,
) -> None:
    if _has_immediate_cite(source, phrase_end, window, sent_end):
        return
    lagged = [
        cite for cite in window if cite.start > phrase_end and cite.command not in _AUTHOR_CITE_SKIP
    ]
    if predicate_end is not None:
        lagged = [cite for cite in lagged if cite.start >= predicate_end]
    elif lagged and _PRED_RE.search(visible, phrase_end, lagged[0].start) is None:
        return
    if not lagged:
        return
    cite = lagged[0]
    key = ", ".join(cite.keys)
    marker = (code, key, cite.start)
    if marker in seen:
        return
    seen.add(marker)
    snippet = " ".join(source[phrase_start : cite.end].split())
    if len(snippet) > 80:
        snippet = snippet[:80]
    detail = f"键 {key}。片段 {snippet}。"
    if uncertain:
        detail = "不确定是否作者主语，请核读。" + detail
    issues.append(_cite_issue(cite.file, cite.line, code, detail))


def _has_immediate_cite(source: str, phrase_end: int, cites: list[_RawCite], limit: int) -> bool:
    index = phrase_end
    while index < limit and index < len(source) and source[index] in " \t\r\n~\u3000":
        index += 1
    return any(cite.start == index for cite in cites)


def _paragraph_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    index = 0
    while index < len(text):
        if text[index] != "\n":
            index += 1
            continue
        cursor = index + 1
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1
        if cursor < len(text) and text[cursor] == "\n":
            if text[start:index].strip():
                spans.append((start, index))
            index = cursor + 1
            while index < len(text) and text[index] in " \t\n":
                if text[index] != "\n":
                    break
                nxt = index + 1
                while nxt < len(text) and text[nxt] in " \t":
                    nxt += 1
                if nxt < len(text) and text[nxt] == "\n":
                    index = nxt
                    continue
                break
            start = index
            continue
        index += 1
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def _complete_sentences(text: str, start: int, end: int) -> list[tuple[int, int]]:
    sentences: list[tuple[int, int]] = []
    sent_start = start
    index = start
    while index < end:
        if _is_sentence_boundary(text, index):
            sentences.append((sent_start, index + 1))
            sent_start = index + 1
        index += 1
    return sentences


def _is_sentence_boundary(text: str, index: int) -> bool:
    char = text[index]
    if char in "。！？!?":
        return True
    if char != ".":
        return False
    if (
        index > 0
        and index + 1 < len(text)
        and text[index - 1].isdigit()
        and text[index + 1].isdigit()
    ):
        return False
    if _is_abbrev_dot(text, index):
        return False
    if index + 1 >= len(text):
        return True
    nxt = text[index + 1]
    return nxt.isspace() or nxt in "。！？\"'”’）)]}"


def _is_abbrev_dot(text: str, index: int) -> bool:
    if index <= 0 or not (text[index - 1].isascii() and text[index - 1].isalpha()):
        return False
    if index == 1 or not (text[index - 2].isascii() and text[index - 2].isalpha()):
        return True
    cursor = index - 1
    while cursor >= 0 and text[cursor].isascii() and text[cursor].isalpha():
        cursor -= 1
    return text[cursor + 1 : index].lower() in _ABBREV_WORDS


def _repeat_cite_issues(document: AssembledDocument, cites: list[_RawCite]) -> list[dict]:
    issues: list[dict] = []
    rel, line = document.origin(1)
    issues.append(
        _cite_issue(
            rel,
            line,
            "RC-COVERAGE",
            "覆盖不足。\\cites 等多重命令、自定义宏传键与未展开参数未计入。"
            "本检查不证明页码支持当前句，也不发明页码。",
        )
    )
    by_key: dict[str, list[_RawCite]] = {}
    for cite in cites:
        if cite.shared:
            issues.append(
                _cite_issue(
                    cite.file,
                    cite.line,
                    "RC-SHARED",
                    "键 "
                    + ", ".join(cite.keys)
                    + " 共享同一 postnote，不能证明每个键的页码。不发明页码。",
                )
            )
        for key in cite.keys:
            by_key.setdefault(key, []).append(cite)
    for key, occs in by_key.items():
        if len(occs) < 2:
            continue
        places = "; ".join(f"{occ.file}:{occ.line}" for occ in occs)
        if any(occ.empty for occ in occs):
            issues.append(
                _cite_issue(
                    occs[0].file,
                    occs[0].line,
                    "RC-REPEATPAGE",
                    f"键 {key} 至少出现两次，且至少一处 postnote 为空。"
                    f"位置 {places}。请人工核验页码。不发明页码，也不证明页码支持当前句。",
                )
            )
        elif not all(occ.proven for occ in occs):
            issues.append(
                _cite_issue(
                    occs[0].file,
                    occs[0].line,
                    "RC-POSTNOTE",
                    f"键 {key} 的 postnote 不是逐键字面页码，不能据此通过学院规则。不发明页码。",
                )
            )
    return issues


if __name__ == "__main__":
    sys.exit(main())
