#!/usr/bin/env python3
"""
Blind Review Anonymization - 盲审匿名化检查与盲审版副本生成

R1/R2 依据校方盲审通知原文（见 templates/yanshan.md「盲审」节与
references/modules/blind-review.md），R3 为常见惯例提示（以学校盲审通知为准）。

--check 定位泄露点：作者/导师字段、非空致谢、成果条目（作者列表/成果名称/期刊页码）、
可选 --author/--supervisor 全文姓名扫描、R3 扩展提示。
--generate 生成盲审副本：只写 `<stem>_blind.tex` 新文件（原文件字节不变）。
机械可安全项自动替换（字段值→□□□、致谢正文→占位文本）；R2 成果条目与正文姓名句
零改写、只插 `% TODO-BLIND` 注释，由 agent 给出 [LLM] 改写建议、用户确认后落入副本。

Usage:
    uv run python blind_review.py main.tex --check
    uv run python blind_review.py main.tex --check --author 张三 --supervisor 李四
    uv run python blind_review.py main.tex --generate --dry-run
    uv run python blind_review.py main.tex --generate [--suffix _blind] [--force]
"""

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from parsers import LatexParser, get_parser
    from tex_loader import (
        COMMENT_RE,
        INCLUDE_RE,
        _resolve_include_target,
        assemble,
        iter_files,
    )
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import LatexParser, get_parser
    from tex_loader import (
        COMMENT_RE,
        INCLUDE_RE,
        _resolve_include_target,
        assemble,
        iter_files,
    )

# ── Constants ────────────────────────────────────────────────

PLACEHOLDER = "□□□"
ACK_PLACEHOLDER = "（盲审版本，致谢内容略）"
AUTO_NOTE = "% BLIND-AUTO(R1): 原内容已隐去"
R2_TODO = (
    "% TODO-BLIND(R2): 改写为 [n] 署名次序，期刊名称，年份（如：[1]第一作者，机械工程学报，2024）"
)
R3_NOTE = "常见惯例，以学校盲审通知为准"

SEVERITY_PRIORITY = {"HIGH": "P0", "MEDIUM": "P1", "INFO": "P2"}

# documentclass ids whose cover-field macros are covered by the tables below.
# Anything else falls back to generic patterns only and gets a NEEDS-LLM note
# (prefer under-replacing + reporting over heuristic mass substitution).
KNOWN_TEMPLATES = {"thuthesis", "pkuthss", "ctexbook", "ctexrep", "book", "report"}

# R1 field patterns: (kind, label, pattern with ONE capture group = field value).
# Macro patterns run on all non-comment lines; key-value patterns only in the
# preamble (thuthesis \thusetup / pkuthss \pkuthssinfo / hyperref live there).
MACRO_FIELD_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("author", "作者字段", re.compile(r"\\[ce]?author\s*\{([^{}]*)\}")),
    (
        "supervisor",
        "导师字段",
        re.compile(r"\\[ce]?(?:supervisor|advisor|mentor)\s*\{([^{}]*)\}"),
    ),
]
KEYVAL_FIELD_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    # Field names per templates/*.md snapshots: thuthesis author=/supervisor=,
    # pkuthss cauthor=/eauthor=/cmentor=/ementor=; hyperref pdfauthor=.
    ("author", "作者字段", re.compile(r"(?<![\w-])[ce]?author\s*=\s*\{([^{}]*)\}")),
    (
        "supervisor",
        "导师字段",
        re.compile(r"(?<![\w-])(?:(?:[a-z]+-)?supervisor|[ce]mentor)\s*=\s*\{([^{}]*)\}"),
    ),
    ("author", "PDF元数据作者", re.compile(r"(?<![\w-])pdfauthor\s*=\s*\{([^{}]*)\}")),
]

ACK_TITLE_RE = re.compile(r"致\s*谢|谢\s*辞|acknowledg", re.IGNORECASE)
ACK_ENV_RE = re.compile(r"\\begin\{(acknowledgements?)\}")
ACHIEVEMENT_TITLE_RE = re.compile(r"攻读.*期间.*(?:成果|论文)")
DECLARATION_TITLE_RE = re.compile(r"原创性声明|独创性声明|授权说明|使用授权")
FUNDING_RE = re.compile(r"No\.\s*\d|基金.*(?:编号|资助)")
SELF_REF_RE = re.compile(r"(?:作者|本人|笔者)在.{0,15}?(?:课题组|实验室|团队)")
EN_TITLEPAGE_RE = re.compile(r"^\s*By\s*$|^\s*(?:Assistant\s+)?Supervisor\s*[:：]")
COVER_MACRO_RE = re.compile(r"\\make(?:cover|title)\b")
STUDENTID_RE = re.compile(r"(?<![\w-])(?:studentid|student-id)\s*=\s*\{([^{}]*)\}")

# R2 achievement-entry cues (scanned only inside the achievements chapter).
PAGE_RANGE_RE = re.compile(r"[:：]\s*\d+\s*[-–—]\s*\d+")
AUTHOR_LIST_RE = re.compile(r"(?:[一-鿿]{2,4}\s*[,，、]\s*){1,}[一-鿿]{2,4}\s*[.．。]")
QUOTED_TITLE_RE = re.compile(r"[《“][^《》“”]{4,}[》”]")

# Red line: never touch these in copies. Ack blocks containing them are
# downgraded from AUTO wipe to a TODO comment (content kept verbatim).
PROTECTED_RE = re.compile(
    r"\\(?:cite|ref|eqref|autoref|label|bibitem)\b"
    r"|(?<!\\)\$"
    r"|\\begin\{(?:equation|align|gather|math|displaymath|eqnarray)"
)
# Structural lines that must survive an ack-body wipe.
STRUCTURAL_RE = re.compile(
    r"^\s*\\(?:end\{document\}|appendix\b|backmatter\b|frontmatter\b|mainmatter\b"
    r"|bibliography\b|bibliographystyle\b|printbibliography\b|input\b|include\b"
    r"|begin\{acknowledgements?\}|end\{acknowledgements?\})"
)

VERBATIM_ENVS = ("filecontents", "verbatim", "lstlisting", "minted")


# ── Findings ─────────────────────────────────────────────────


@dataclass
class Finding:
    rule: str  # R1 | R2 | R3
    severity: str  # HIGH | MEDIUM | INFO
    kind: str
    line: int  # assembled line no (0 = document level)
    message: str
    action: str  # AUTO_FIELD | AUTO_ACK | TODO | INFO
    evidence: str = ""
    pattern: Optional[re.Pattern] = None  # AUTO_FIELD: value pattern to re-apply
    span: Optional[tuple[int, int]] = None  # AUTO_ACK: assembled body range
    todo: str = ""  # TODO: comment line to insert above


class BlindReviewChecker:
    """Locate personal-information leaks against blind-review rules R1/R2/R3."""

    def __init__(
        self,
        tex_file: Path,
        author: Optional[str] = None,
        supervisor: Optional[str] = None,
    ):
        self.tex_file = Path(tex_file).resolve()
        self.author = (author or "").strip() or None
        self.supervisor = (supervisor or "").strip() or None
        self.doc = assemble(self.tex_file)
        self.parser = get_parser(self.tex_file)
        self.lines = self.doc.lines
        self.template_id = self._detect_template()
        self.chapters = self.parser.chapter_ranges(self.doc.content)
        self.findings: list[Finding] = []
        self._scan_cache = self._scan_lines()

    # -- shared line access ----------------------------------------

    def _detect_template(self) -> str:
        m = re.search(r"\\documentclass(?:\[[^\]]*\])?\{(\w+)\}", self.doc.content)
        return m.group(1) if m else "unknown"

    def _verbatim_mask(self) -> list[bool]:
        begin_re = re.compile(r"\\begin\{(?:" + "|".join(VERBATIM_ENVS) + r")\*?\}")
        end_re = re.compile(r"\\end\{(?:" + "|".join(VERBATIM_ENVS) + r")\*?\}")
        mask = [False] * len(self.lines)
        depth = 0
        for i, line in enumerate(self.lines):
            if begin_re.search(line):
                depth += 1
            mask[i] = depth > 0
            if end_re.search(line) and depth > 0:
                depth -= 1
        return mask

    def _scan_lines(self) -> list[tuple[int, str]]:
        """(assembled line no, comment-stripped line); skips comment lines and
        verbatim/filecontents bodies (bib data embedded there is not a field)."""
        mask = self._verbatim_mask()
        out = []
        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith("%") or mask[i - 1]:
                continue
            out.append((i, COMMENT_RE.sub("", line)))
        return out

    def _range(self, start: int, end: int) -> list[tuple[int, str]]:
        return [(no, text) for no, text in self._scan_cache if start <= no <= end]

    def _begin_document_line(self) -> int:
        for no, text in self._scan_cache:
            if "\\begin{document}" in text:
                return no
        return len(self.lines) + 1

    def loc(self, line_no: int) -> str:
        if line_no <= 0:
            return "(全文)"
        src, src_line = self.doc.origin(line_no)
        return f"({src}:L{src_line})"

    # -- section lookup ----------------------------------------------

    def _ack_blocks(self) -> list[tuple[int, int, int]]:
        """(heading/begin line, body start, body end) of acknowledgement blocks."""
        blocks = []
        for ch in self.chapters:
            title = LatexParser.normalize_heading_title(ch["title"])
            if ACK_TITLE_RE.search(title):
                blocks.append((ch["start"], ch["start"] + 1, ch["end"]))
        open_line, env = None, None
        for no, text in self._scan_cache:
            m = ACK_ENV_RE.search(text)
            if m and open_line is None:
                open_line, env = no, m.group(1)
                continue
            if open_line is not None and env and re.search(r"\\end\{" + env + r"\}", text):
                blocks.append((open_line, open_line + 1, no - 1))
                open_line, env = None, None
        return blocks

    def _achievement_chapters(self) -> list[dict]:
        return [
            ch
            for ch in self.chapters
            if ACHIEVEMENT_TITLE_RE.search(LatexParser.normalize_heading_title(ch["title"]))
        ]

    # -- rule checks ---------------------------------------------------

    def _check_fields(self) -> None:
        begin_doc = self._begin_document_line()
        seen: set[str] = set()
        for no, text in self._scan_cache:
            tables = [MACRO_FIELD_PATTERNS]
            if no < begin_doc:
                tables.append(KEYVAL_FIELD_PATTERNS)
            for table in tables:
                for kind, label, pat in table:
                    for m in pat.finditer(text):
                        if not m.group(1).strip():
                            continue
                        seen.add(kind)
                        self.findings.append(
                            Finding(
                                rule="R1",
                                severity="HIGH",
                                kind=f"{kind}_field",
                                line=no,
                                message=f"{label}未隐去（生成模式将替换为 {PLACEHOLDER}）",
                                action="AUTO_FIELD",
                                evidence=m.group(0),
                                pattern=pat,
                            )
                        )
        for kind, zh in (("author", "作者"), ("supervisor", "导师")):
            if kind not in seen:
                self.findings.append(
                    Finding(
                        rule="R1",
                        severity="INFO",
                        kind="needs_llm",
                        line=0,
                        message=f"未检出{zh}字段（可能在独立封面文件或未识别模板宏中），"
                        "请人工复查（NEEDS-LLM）",
                        action="INFO",
                    )
                )
        if self.template_id not in KNOWN_TEMPLATES:
            self.findings.append(
                Finding(
                    rule="R1",
                    severity="INFO",
                    kind="needs_llm",
                    line=0,
                    message=f"模板 {self.template_id} 未识别，仅应用通用字段表；"
                    "封面/题名页个人字段请人工复查（NEEDS-LLM）",
                    action="INFO",
                )
            )

    def _check_ack(self) -> None:
        for head, body_start, body_end in self._ack_blocks():
            visible = []
            for i in range(body_start, min(body_end, len(self.lines)) + 1):
                line = self.lines[i - 1]
                if line.strip().startswith("%"):
                    continue
                visible.append(self.parser.extract_visible_text(line))
            n = len(re.sub(r"\s+", "", "".join(visible)))
            if n <= 10:
                continue
            self.findings.append(
                Finding(
                    rule="R1",
                    severity="HIGH",
                    kind="ack",
                    line=head,
                    message=f"致谢内容未隐去（约 {n} 字），生成模式将整块替换为“{ACK_PLACEHOLDER}”",
                    action="AUTO_ACK",
                    span=(body_start, body_end),
                )
            )

    def _check_achievements(self) -> None:
        for ch in self._achievement_chapters():
            for no, text in self._range(ch["start"] + 1, ch["end"]):
                visible = self.parser.extract_visible_text(text)
                cues = []
                if AUTHOR_LIST_RE.search(visible):
                    cues.append("作者列表")
                if QUOTED_TITLE_RE.search(visible):
                    cues.append("成果名称")
                if PAGE_RANGE_RE.search(visible):
                    cues.append("期刊页码")
                if not cues:
                    continue
                self.findings.append(
                    Finding(
                        rule="R2",
                        severity="HIGH",
                        kind="achievement",
                        line=no,
                        message="成果条目含 "
                        + "/".join(cues)
                        + "，须改写为 [n] 署名次序，期刊名称，年份"
                        "（脚本零改写，生成模式只插 TODO 注释）",
                        action="TODO",
                        evidence=visible.strip()[:60],
                        todo=R2_TODO,
                    )
                )

    def _check_names(self) -> None:
        targets = [
            (label, name)
            for label, name in (("作者姓名", self.author), ("导师姓名", self.supervisor))
            if name
        ]
        if not targets:
            return
        hot: set[int] = set()
        for head, _b, e in self._ack_blocks():
            hot.update(range(head, e + 1))
        for ch in self._achievement_chapters():
            hot.update(range(ch["start"], ch["end"] + 1))
        field_lines = {f.line for f in self.findings if f.action == "AUTO_FIELD"}
        for no, text in self._scan_cache:
            if no in field_lines:
                continue
            visible = self.parser.extract_visible_text(text)
            squashed = re.sub(r"\s+", "", visible)
            for label, name in targets:
                packed = re.sub(r"\s+", "", name)
                if name not in visible and (not packed or packed not in squashed):
                    continue
                severity = "HIGH" if no in hot else "MEDIUM"
                self.findings.append(
                    Finding(
                        rule="R1",
                        severity=severity,
                        kind="name",
                        line=no,
                        message=f"正文出现{label}“{name}”，请隐去或改为泛称（作者/导师）",
                        action="TODO",
                        evidence=visible.strip()[:60],
                        todo=f"% TODO-BLIND(R1): 隐去{label}“{name}”（改为“作者/导师”等泛称）",
                    )
                )

    def _check_r3(self) -> None:
        for h in self.parser.extract_headings(self.doc.content):
            title = LatexParser.normalize_heading_title(h["title"])
            if DECLARATION_TITLE_RE.search(title):
                self.findings.append(
                    Finding(
                        rule="R3",
                        severity="INFO",
                        kind="declaration",
                        line=h["line"],
                        message=f"原创性声明/授权说明含签名信息，盲审版常需移除或隐名（{R3_NOTE}）",
                        action="INFO",
                    )
                )
        begin_doc = self._begin_document_line()
        cover_reported = False
        for no, text in self._scan_cache:
            visible = self.parser.extract_visible_text(text)
            if FUNDING_RE.search(visible):
                self.findings.append(
                    Finding(
                        rule="R3",
                        severity="INFO",
                        kind="funding",
                        line=no,
                        message=f"疑似基金项目编号/资助信息，可能间接暴露身份（{R3_NOTE}）",
                        action="INFO",
                        evidence=visible.strip()[:60],
                    )
                )
            if SELF_REF_RE.search(visible):
                self.findings.append(
                    Finding(
                        rule="R3",
                        severity="INFO",
                        kind="self_ref",
                        line=no,
                        message=f"正文自指身份表述（如“作者在××课题组”）（{R3_NOTE}）",
                        action="INFO",
                        evidence=visible.strip()[:60],
                    )
                )
            if EN_TITLEPAGE_RE.match(visible):
                self.findings.append(
                    Finding(
                        rule="R3",
                        severity="INFO",
                        kind="titlepage_en",
                        line=no,
                        message=f"英文题名页 By/Supervisor 行含个人信息（{R3_NOTE}）",
                        action="INFO",
                        evidence=visible.strip()[:60],
                    )
                )
            if no < begin_doc and STUDENTID_RE.search(text):
                self.findings.append(
                    Finding(
                        rule="R3",
                        severity="INFO",
                        kind="cover",
                        line=no,
                        message=f"封面学号字段含个人信息（{R3_NOTE}）",
                        action="INFO",
                    )
                )
            if not cover_reported and COVER_MACRO_RE.search(text):
                cover_reported = True
                self.findings.append(
                    Finding(
                        rule="R3",
                        severity="INFO",
                        kind="cover",
                        line=no,
                        message="封面/题名页由模板宏生成，作者/导师/学号等个人字段"
                        f"请按学校通知隐去（{R3_NOTE}）",
                        action="INFO",
                    )
                )

    def run_check(self) -> list[Finding]:
        self.findings = []
        self._check_fields()
        self._check_ack()
        self._check_achievements()
        self._check_names()
        self._check_r3()
        self.findings.sort(key=lambda f: (f.line, f.rule, f.kind))
        return self.findings


# ── Report ───────────────────────────────────────────────────


def format_finding(checker: BlindReviewChecker, f: Finding) -> str:
    priority = SEVERITY_PRIORITY[f.severity]
    line = (
        f"% BLIND-REVIEW {checker.loc(f.line)} [{f.severity}] [{priority}] "
        f"[Script]: {f.rule} {f.message}"
    )
    if f.evidence:
        line += f" — {f.evidence}"
    return line


def check_report(checker: BlindReviewChecker) -> str:
    findings = checker.findings
    counts = {s: sum(1 for f in findings if f.severity == s) for s in ("HIGH", "MEDIUM", "INFO")}
    lines = []
    lines.append("=" * 60)
    lines.append("盲审匿名化检查报告 (Blind Review Anonymization)")
    lines.append("=" * 60)
    lines.append(f"入口文件: {checker.tex_file}")
    lines.append(f"模板: {checker.template_id} · R1/R2 依据校方盲审通知原文；R3 为{R3_NOTE}")
    lines.append(f"统计: HIGH {counts['HIGH']} · MEDIUM {counts['MEDIUM']} · INFO {counts['INFO']}")
    lines.extend(checker.doc.warning_lines())

    main_findings = [f for f in findings if f.rule in ("R1", "R2") and f.severity != "INFO"]
    lines.append("")
    lines.append("-" * 60)
    if main_findings:
        lines.append("[R1/R2] 需隐匿项（[Script] 自动定位）:")
        lines.extend(format_finding(checker, f) for f in main_findings)
    else:
        lines.append("[R1/R2] 未检出需隐匿项")

    r3 = [f for f in findings if f.rule == "R3"]
    if r3:
        lines.append("")
        lines.append(f"[R3] 扩展提示（{R3_NOTE}）:")
        lines.extend(format_finding(checker, f) for f in r3)

    needs_llm = [f for f in findings if f.kind == "needs_llm"]
    if needs_llm:
        lines.append("")
        lines.append("[NEEDS-LLM] 待人工/agent 复查:")
        lines.extend(f"- {f.message}" for f in needs_llm)

    if not checker.author and not checker.supervisor:
        lines.append("")
        lines.append(
            "提示: 未提供 --author/--supervisor，已跳过全文姓名扫描"
            "（可加 --author 姓名 --supervisor 姓名 复查正文姓名残留）。"
        )

    lines.append("")
    lines.append(
        "后续: --generate 生成盲审副本（只写 *_blind 新文件，原文件字节不变）；"
        "TODO 项由 agent 按 references/modules/blind-review.md 给出 [LLM] 改写建议，"
        "用户确认后落入副本。"
    )
    lines.append("=" * 60)
    return "\n".join(lines)


# ── Generation ───────────────────────────────────────────────


@dataclass
class CopyPlan:
    src: Path
    dst: Path
    rel: str
    text: str
    notes: list[str]


def _suffixed_name(raw: str, suffix: str) -> str:
    raw = raw.strip()
    if raw.endswith(".tex"):
        return raw[:-4] + suffix + ".tex"
    return raw + suffix


def _replace_field_values(line: str, patterns: list[re.Pattern[str]]) -> str:
    """Replace field VALUES with the placeholder, keeping macro + braces.

    Only the pre-comment part of the line is touched.
    """
    m = COMMENT_RE.search(line)
    boundary = m.start() if m else len(line)
    head, tail = line[:boundary], line[boundary:]

    def _sub(mm: re.Match[str]) -> str:
        s, e = mm.span(1)
        base = mm.start(0)
        text = mm.group(0)
        return text[: s - base] + PLACEHOLDER + text[e - base :]

    for pat in patterns:
        head = pat.sub(_sub, head)
    return head + tail


def _rewrite_includes(
    line: str,
    current_dir: Path,
    root: Path,
    affected_paths: set[Path],
    suffix: str,
) -> tuple[str, int]:
    """Point \\input/\\include at the _blind copy when the target is affected."""
    if line.strip().startswith("%"):
        return line, 0
    m = COMMENT_RE.search(line)
    boundary = m.start() if m else len(line)
    head, tail = line[:boundary], line[boundary:]
    count = 0

    def _sub(mm: re.Match[str]) -> str:
        nonlocal count
        raw = mm.group(1)
        target = _resolve_include_target(raw, current_dir, root)
        if target in affected_paths:
            count += 1
            return mm.group(0).replace(raw, _suffixed_name(raw, suffix))
        return mm.group(0)

    head = INCLUDE_RE.sub(_sub, head)
    return head + tail, count


def plan_copies(checker: BlindReviewChecker, suffix: str) -> tuple[list[CopyPlan], list[str], list]:
    """Build the copy plan from findings. Returns (plans, todo summary, nodes)."""
    doc = checker.doc
    root = checker.tex_file.parent
    nodes = [n for n in iter_files(checker.tex_file) if n.exists]
    by_rel = {n.rel: n for n in nodes}
    src_lines_of = {n.rel: (n.content or "").split("\n") for n in nodes}

    field_edits: dict[str, dict[int, list[re.Pattern[str]]]] = {}
    todo_edits: dict[str, dict[int, list[str]]] = {}
    ack_edits: dict[str, dict[int, set[int]]] = {}
    todo_summary: list[str] = []

    for f in checker.findings:
        if f.action == "AUTO_FIELD":
            rel, src_line = doc.origin(f.line)
            raw_lines = src_lines_of.get(rel)
            if raw_lines is None or src_line > len(raw_lines) or f.pattern is None:
                continue
            raw = COMMENT_RE.sub("", raw_lines[src_line - 1])
            if f.pattern.search(raw):
                field_edits.setdefault(rel, {}).setdefault(src_line, []).append(f.pattern)
            else:
                # Assembled/source drift (e.g. field shares a line with an
                # include): under-replace + report instead of guessing.
                note = "% TODO-BLIND(R1): 此行字段值需人工隐去（自动替换定位失败）"
                todo_edits.setdefault(rel, {}).setdefault(src_line, []).append(note)
                todo_summary.append(f"{checker.loc(f.line)} R1 字段自动替换定位失败，转人工")
        elif f.action == "AUTO_ACK":
            if f.span is None:
                continue
            head_rel, head_line = doc.origin(f.line)
            raw_lines = src_lines_of.get(head_rel)
            if raw_lines is None:
                continue
            body_start, body_end = f.span
            wipe: set[int] = set()
            protected = False
            for i in range(body_start, min(body_end, len(doc.lines)) + 1):
                rel, src_line = doc.origin(i)
                if rel != head_rel or src_line > len(raw_lines):
                    continue
                raw = raw_lines[src_line - 1]
                if STRUCTURAL_RE.match(raw):
                    continue
                if PROTECTED_RE.search(COMMENT_RE.sub("", raw)):
                    protected = True
                    break
                wipe.add(src_line)
            if protected:
                note = (
                    "% TODO-BLIND(R1): 致谢含 \\cite/\\ref/\\label/数学环境，"
                    f"请人工改写为“{ACK_PLACEHOLDER}”"
                )
                todo_edits.setdefault(head_rel, {}).setdefault(head_line, []).append(note)
                todo_summary.append(
                    f"{checker.loc(f.line)} R1 致谢含受保护标记，降级为 TODO（未自动替换）"
                )
            else:
                ack_edits.setdefault(head_rel, {})[head_line] = wipe
        elif f.action == "TODO":
            rel, src_line = doc.origin(f.line)
            todo_edits.setdefault(rel, {}).setdefault(src_line, []).append(f.todo)
            todo_summary.append(f"{checker.loc(f.line)} {f.rule} {f.message}")

    # Drop TODO comments that would annotate lines wiped by an ack replacement.
    for rel, heads in ack_edits.items():
        wiped = set().union(*heads.values()) if heads else set()
        per_file = todo_edits.get(rel)
        if not per_file:
            continue
        for line_no in list(per_file):
            if line_no in wiped:
                del per_file[line_no]
        if not per_file:
            del todo_edits[rel]

    entry_rel = next((n.rel for n in nodes if n.path == checker.tex_file), "main.tex")
    affected_rels = set(field_edits) | set(todo_edits) | set(ack_edits) | {entry_rel}
    affected_rels &= set(by_rel)
    affected_paths = {by_rel[rel].path for rel in affected_rels}

    plans: list[CopyPlan] = []
    for rel in sorted(affected_rels):
        node = by_rel[rel]
        raw_lines = src_lines_of[rel]
        heads = ack_edits.get(rel, {})
        wiped = set().union(*heads.values()) if heads else set()
        fields = field_edits.get(rel, {})
        todos = todo_edits.get(rel, {})
        out: list[str] = []
        auto_count = todo_count = include_count = 0
        for i, line in enumerate(raw_lines, 1):
            if i in wiped:
                continue
            for todo in todos.get(i, ()):
                out.append(todo)
                todo_count += 1
            if i in fields:
                out.append(AUTO_NOTE)
                line = _replace_field_values(line, fields[i])
                auto_count += 1
            new_line, n_inc = _rewrite_includes(
                line, node.path.parent, root, affected_paths, suffix
            )
            include_count += n_inc
            out.append(new_line)
            if i in heads:
                out.append(AUTO_NOTE)
                out.append(ACK_PLACEHOLDER)
                auto_count += 1
        if (node.content or "").endswith("\n") and (not out or out[-1] != ""):
            out.append("")
        notes = []
        if auto_count:
            notes.append(f"AUTO 替换 {auto_count} 处")
        if todo_count:
            notes.append(f"TODO-BLIND {todo_count} 处")
        if include_count:
            notes.append(f"include 引用改写 {include_count} 处")
        if not notes:
            notes.append("无内容改动（仅作为副本入口）")
        dst = node.path.with_name(node.path.stem + suffix + node.path.suffix)
        plans.append(CopyPlan(src=node.path, dst=dst, rel=rel, text="\n".join(out), notes=notes))
    return plans, todo_summary, nodes


def run_generate(checker: BlindReviewChecker, suffix: str, dry_run: bool, force: bool) -> int:
    plans, todo_summary, nodes = plan_copies(checker, suffix)
    lines = []
    lines.append("")
    lines.append("-" * 60)
    lines.append("盲审副本生成计划 (DRY-RUN):" if dry_run else "盲审副本生成结果:")
    for plan in plans:
        rel_dst = plan.rel.replace(plan.src.name, plan.dst.name)
        lines.append(f"- {plan.rel} → {rel_dst}（{'；'.join(plan.notes)}）")
    if todo_summary:
        lines.append("TODO-BLIND 汇总（由 agent 给出 [LLM] 改写建议，用户确认后落入副本）:")
        lines.extend(f"- {item}" for item in todo_summary)

    if dry_run:
        lines.append("DRY-RUN: 未写入任何文件")
        print("\n".join(lines))
        return 0

    existing = [p.dst for p in plans if p.dst.exists()]
    if existing and not force:
        lines.append("[ERROR] 目标副本已存在（加 --force 覆盖）:")
        lines.extend(f"- {p}" for p in existing)
        print("\n".join(lines))
        return 3

    before = {n.path: hashlib.sha256(n.path.read_bytes()).hexdigest() for n in nodes}
    for plan in plans:
        plan.dst.write_text(plan.text, encoding="utf-8")
    changed = [
        str(p)
        for p, digest in before.items()
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest
    ]
    if changed:
        lines.append("[ERROR] 原文件被意外改动（请回退并报告）: " + ", ".join(changed))
        print("\n".join(lines))
        return 4
    lines.append(f"原文件未改动: {len(before)} 个源文件内容哈希校验一致")
    entry_plan = next((p for p in plans if p.src == checker.tex_file), None)
    if entry_plan is not None:
        lines.append(f"盲审版入口: {entry_plan.dst}")
    print("\n".join(lines))
    return 0


# ── CLI ──────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="盲审匿名化检查与盲审版副本生成（原文件永不修改）")
    parser.add_argument("tex_file", help="论文入口 .tex 文件")
    parser.add_argument("--check", action="store_true", help="定位个人信息泄露点（默认动作）")
    parser.add_argument(
        "--generate", action="store_true", help="生成盲审 *_blind 副本（原文件字节不变）"
    )
    parser.add_argument("--author", help="作者姓名（提供后全文扫描该姓名）")
    parser.add_argument("--supervisor", help="导师姓名（提供后全文扫描该姓名）")
    parser.add_argument("--suffix", default="_blind", help="副本文件名后缀（默认 _blind）")
    parser.add_argument("--dry-run", action="store_true", help="只打印生成计划，不写任何文件")
    parser.add_argument("--force", action="store_true", help="目标副本已存在时允许覆盖")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
        sys.exit(1)
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.suffix):
        print(f"[ERROR] 非法后缀: {args.suffix}（仅允许字母/数字/下划线/连字符）", file=sys.stderr)
        sys.exit(2)

    checker = BlindReviewChecker(tex_path, author=args.author, supervisor=args.supervisor)
    checker.run_check()
    print(check_report(checker))

    if args.generate:
        sys.exit(run_generate(checker, args.suffix, args.dry_run, args.force))

    has_high = any(f.severity == "HIGH" for f in checker.findings)
    sys.exit(1 if has_high else 0)


if __name__ == "__main__":
    main()
