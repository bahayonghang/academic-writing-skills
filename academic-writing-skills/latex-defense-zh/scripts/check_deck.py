#!/usr/bin/env python3
"""
Quality gate for the latex-defense-zh defense deck.

The script reads defense.tex, notes.md, and defense.log in the build output
directory, compares them with inventory.json and the thesis source, and prints
D-* findings. It does not write files.

Codes, criteria, thresholds, and fixes: references/quality-gate.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/check_deck.py --deck DIR/defense.tex \
        --inventory inventory.json [--plan slide_plan.yaml] [--log DIR/defense.log] \
        [--minutes 40] [--json]

Exit codes: 0 no Critical or Major finding; 1 at least one Critical or Major
finding; 2 input error.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

try:
    import defense_budget
    import extract_thesis
    import tex_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import defense_budget
    import extract_thesis
    import tex_loader

PRIORITY = {"Critical": "P0", "Major": "P1", "Minor": "P2", "Info": "P3"}
STAGES = ("predefense", "defense")
ROLES = (
    "cover",
    "toc",
    "background",
    "status",
    "challenges",
    "organization",
    "foundation",
    "intro",
    "problem",
    "method",
    "experiment",
    "summary",
    "architecture",
    "application",
    "innovation",
    "outlook",
    "achievements",
    "thanks",
    "backup",
)
LAYOUTS = (
    "cover",
    "toc",
    "bullets",
    "figure",
    "figure-bullets",
    "figure-grid",
    "equations-figure",
    "table",
    "cards",
    "paper-summary",
    "outlook",
    "thanks",
)
NON_CONTENT_ROLES = ("cover", "toc", "thanks", "backup")
# Page roles that each chapter role needs (references/defense-framework.md).
REQUIRED_ROLES = {
    "intro": ("background", "status", "challenges", "organization"),
    "foundation": ("foundation",),
    "research": ("intro", "problem", "method", "experiment", "summary"),
    "application": ("intro", "architecture", "application"),
    "conclusion": ("innovation", "outlook"),
}
# Chapter role inferred from the page roles when no plan gives it; the first match wins.
CHAPTER_ROLE_HINTS = (
    ("intro", {"background", "status", "challenges", "organization"}),
    ("conclusion", {"innovation", "outlook", "achievements"}),
    ("application", {"architecture", "application"}),
    ("research", {"problem", "method", "experiment", "summary"}),
    ("foundation", {"foundation"}),
)
# (layout, counted item, limit) from references/slide-layouts.md.
LAYOUT_LIMITS = (
    ("bullets", "item", 5),
    ("figure-bullets", "item", 4),
    ("equations-figure", "item", 3),
    ("paper-summary", "item", 4),
    ("cards", "card", 5),
    ("outlook", "box", 3),
    ("figure-grid", "figure", 6),
    ("equations-figure", "equation", 4),
)
ITEM_NAMES = {
    "item": "要点",
    "card": "卡片",
    "box": "展望条目",
    "figure": "子图",
    "equation": "公式",
}
# Initial thresholds, not calibrated (references/quality-gate.md).
DENSITY_MINOR = 180
DENSITY_MAJOR = 260
TAKEAWAY_MAX = 40
SAY_MIN = 150
SAY_MAX = 250
HBOX_MINOR = 5.0
HBOX_MAJOR = 20.0
TALL_RATIO = 1.6
WIDE_RATIO = 3.0
NOTES_TOLERANCE = 0.10
BITMAP_SUFFIXES = (".png", ".jpg", ".jpeg")
TALL_LAYOUTS = ("figure", "figure-grid", "equations-figure")
NOTES_NAME = "notes.md"
LOG_NAME = "defense.log"
LOG_WIDTH = 79  # TeX max_print_line: a longer message continues on the next log line

MARKER_RE = re.compile(
    r"^%\s*defense-frame:\s*id=(\S+)\s+role=(\S+)\s+chapter=(\S+)\s+layout=(\S+)\s*$"
)
FRAME_BEGIN_RE = re.compile(r"\\begin\s*\{frame\}")
FRAME_END_RE = re.compile(r"\\end\s*\{frame\}")
# Commands whose first brace arguments are not visible text. \DefenseFigure keeps its caption.
HIDDEN_ARGS = {
    "includegraphics": 1,
    "DefenseFigure": 1,
    "DefenseTocFrame": 1,
    "frametitle": 1,
    "column": 1,
    "hspace": 1,
    "vspace": 1,
    "label": 1,
}
HIDDEN_COMMAND_RE = re.compile(r"\\(" + "|".join(HIDDEN_ARGS) + r")(?![A-Za-z@])\*?")
# Brace arguments after \begin{env} that are not visible text; the frame title is excluded.
ENV_HIDDEN_ARGS = {"frame": 1, "minipage": 1, "column": 1}
SYMBOLS = (
    ("\\textbackslash{}", "\ue000"),
    ("\\textasciitilde{}", "\ue001"),
    ("\\textasciicircum{}", "\ue002"),
)
RESTORE = str.maketrans(
    {"\ue000": "\\", "\ue001": "~", "\ue002": "^", "\ue003": "{", "\ue004": "}"}
)
FIGURE_CALL_RE = re.compile(r"\\(includegraphics|DefenseFigure)(?![A-Za-z@])\*?")
CAPTION_CALL_RE = re.compile(r"\\DefenseCaption(?![A-Za-z@])")
CAPTION_NUMBER_RE = re.compile(r"^\s*图\s*(\d+(?:\s*[-－.．]\s*\d+)+)")
FIGURE_REF_RE = re.compile(r"([图表])\s*(\d+(?:\s*[-－.．]\s*\d+)+)")
TOC_ARG_RE = re.compile(r"\\DefenseTocFrame\s*\{\s*(\d+)\s*\}")
SUBSECTION_RE = re.compile(r"\\DefenseSubsection(?![A-Za-z@])")
RESEARCH_ITEM_RE = re.compile(r"研究内容\s*(\d+)")
COLUMNS_RE = re.compile(r"\\begin\s*\{columns\}")
TAKEAWAY_RE = re.compile(r"\\DefenseTakeaway(?![A-Za-z@])")
PAPER_BOX_RE = re.compile(r"\\DefensePaperBox(?![A-Za-z@])")
COUNT_RES = {
    "item": re.compile(r"\\item(?![A-Za-z@])"),
    "card": re.compile(r"\\DefenseCard(?![A-Za-z@])"),
    "box": re.compile(r"\\DefenseBoxTitle(?![A-Za-z@])"),
    "figure": re.compile(r"\\DefenseFigure(?![A-Za-z@])"),
}
EQUATION_NAMES = extract_thesis.EQUATION_ENVS
TABLE_NAMES = tuple(name.rstrip("*") for name in extract_thesis.TABULAR_ENVS)
OUTSIDE_MATH_RE = re.compile(
    r"\\begin\s*\{(?:equation|align|alignat|gather|multline|flalign|eqnarray|displaymath|math)"
    r"\*?\}|(?<!\\)\\\[|(?<!\\)\\\(|\$\$|(?<!\\)\$"
)
OUTSIDE_TABLE_RE = re.compile(
    r"\\begin\s*\{(?:" + "|".join(re.escape(name) for name in extract_thesis.TABULAR_ENVS) + r")\}"
)
PLACEHOLDER_RE = re.compile(r"〔待填写〕|(?<![A-Za-z])(?:TODO|TBD|XXX)(?![A-Za-z])")
STAGE_KEY_RE = re.compile(r"(?:^|,)\s*stage\s*=\s*\{?\s*([^,{}\s]*)")
LOGO_KEY_RE = re.compile(r"(?:^|,)\s*logo\s*=\s*(?:\{([^{}]*)\}|([^,{}]*))")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)*")
FULLWIDTH = str.maketrans("０１２３４５６７８９．", "0123456789.")
THOUSANDS_RE = re.compile(r"(?<=\d)(?:,|\{,\})(?=\d{3}(?!\d))")
# Structural numbers that D-NUM-SRC does not compare with the thesis.
NUMBER_EXCLUDED_RES = (
    re.compile(r"[图表式]\s*[（(]?\s*\d+(?:\s*[-－.．]\s*\d+)+"),
    re.compile(r"第\s*\d+\s*章"),
    re.compile(r"研究内容\s*\d+"),
    re.compile(r"\d+(?:\.\d+)*\s*节"),
)
SUBSECTION_NUMBER_RE = re.compile(r"(\\DefenseSubsection\s*\{\s*)(\d+(?:\.\d+)+)")
NOTES_HEADING_RE = re.compile(r"^## (\d+) (.*)（([^，（）]+)，([^，（）]+)，(-?\d+) 秒）\s*$")
NOTES_FIELD_RE = re.compile(r"^- (说什么|要点|时长|过渡|可能提问)：(.*)$")
NOTES_FIELDS = ("说什么", "要点", "时长", "过渡", "可能提问")
NOTES_TEXT_FIELDS = ("说什么", "要点", "过渡", "可能提问")
LOG_ERROR_RE = re.compile(r"^(?:! |(?:\./)?([^\s:]+\.(?:tex|sty|cls|def|cfg|fd|clo|ltx)):(\d+): )")
LOG_FATAL_RE = re.compile(r"Emergency stop|Fatal error")
LOG_SOURCE_LINE_RE = re.compile(r"^l\.(\d+)")
UNDEFINED_RE = re.compile(
    r"(Reference|Citation) `([^']*)' on page \S+ undefined on input line (\d+)"
)
VBOX_RE = re.compile(r"Overfull \\vbox \(([\d.]+)pt too high\)(?: detected at line (\d+))?")
HBOX_RE = re.compile(
    r"Overfull \\hbox \(([\d.]+)pt too wide\)"
    r"(?: in (?:paragraph|alignment) at lines (\d+)--\d+| detected at line (\d+))?"
)


class CheckError(Exception):
    """Input error (exit code 2)."""


@dataclass
class Finding:
    code: str
    severity: str
    frame: str
    file: str
    line: int | None
    message: str
    meaning_check: str = ""

    @property
    def priority(self) -> str:
        return PRIORITY[self.severity]

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "priority": self.priority,
            "source_kind": "script",
            "frame": self.frame,
            "line": self.line,
            "file": self.file,
            "message": self.message,
            "meaning_check": self.meaning_check,
        }


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def blank(text: str, spans: list[tuple[int, int]]) -> str:
    """Replace the characters of each span with spaces; newlines stay."""
    chars = list(text)
    for start, end in spans:
        for index in range(start, min(end, len(chars))):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def skip_arguments(text: str, pos: int, count: int) -> int:
    """Offset after the optional ``[...]`` arguments and up to ``count`` brace groups."""
    try:
        while True:
            option, after = extract_thesis.read_optional(text, pos)
            if option is None:
                break
            pos = after
        _, pos = extract_thesis.read_groups(text, pos, count)
    except ValueError:
        pass
    return pos


def group_after(text: str, pos: int) -> str | None:
    """The brace group after ``pos`` (after optional arguments), or None."""
    try:
        _, pos = extract_thesis.read_optional(text, pos)
        groups, _ = extract_thesis.read_groups(text, pos, 1)
    except ValueError:
        return None
    return groups[0] if groups else None


def source_spans(text: str) -> list[tuple[int, int]]:
    envs = extract_thesis.pair_environments(text)
    return [(env.start, env.end) for env in envs if env.name == "DefenseSource"]


def hidden_spans(text: str) -> list[tuple[int, int]]:
    """DefenseSource environments, file and layout arguments, and environment tokens."""
    spans = source_spans(text)
    for match in HIDDEN_COMMAND_RE.finditer(text):
        end = skip_arguments(text, match.end(), HIDDEN_ARGS[match.group(1)])
        spans.append((match.start(), end))
    for match in extract_thesis.ENV_TOKEN_RE.finditer(text):
        end = match.end()
        if match.group(1) == "begin":
            end = skip_arguments(text, end, ENV_HIDDEN_ARGS.get(match.group(2).strip(), 0))
        spans.append((match.start(), end))
    return spans


def visible(tex: str) -> str:
    """Plain text of an escaped deck fragment: commands and braces go, escapes are restored."""
    for command, mark in SYMBOLS:
        tex = tex.replace(command, mark)
    tex = re.sub(r"\\\\(?:\[[^\]]*\])?", " ", tex)
    tex = tex.replace("\\{", "\ue003").replace("\\}", "\ue004")
    tex = re.sub(r"\\([%&#_$])", r"\1", tex)
    tex = re.sub(r"\\(?:q?quad(?![A-Za-z@])|[,;:! ])", " ", tex)
    tex = re.sub(r"\\[A-Za-z@]+\*?", "", tex)
    tex = re.sub(r"\\.", "", tex)
    tex = tex.replace("{", "").replace("}", "").replace("~", " ")
    return tex.translate(RESTORE)


def normalize_digits(text: str) -> str:
    """Full-width digits become ASCII digits; thousands separators between digits go."""
    return THOUSANDS_RE.sub("", text.translate(FULLWIDTH))


def number_tokens(text: str) -> list[str]:
    """Numbers that D-NUM-SRC compares with the thesis, without structural numbers."""
    text = normalize_digits(text)
    for pattern in NUMBER_EXCLUDED_RES:
        text = pattern.sub(" ", text)
    tokens = []
    for token in NUMBER_RE.findall(text):
        if "." not in token and int(token) <= 10:
            continue
        tokens.append(token)
    return unique(tokens)


def label_number(text: str) -> str:
    """Thesis figure or table number with one separator form, for comparison."""
    return re.sub(r"[－.．]", "-", compact(text))


def normalize_equation(tex: str) -> str:
    tex = extract_thesis.LABEL_RE.sub("", tex)
    tex = extract_thesis.TAG_RE.sub("", tex)
    tex = extract_thesis.NOTAG_RE.sub("", tex)
    return compact(tex)


def normalize_path(value: str) -> str:
    value = value.strip().replace("\\", "/")
    return value[2:] if value.startswith("./") else value


# ---------------------------------------------------------------------------
# Deck, notes, and log parsing
# ---------------------------------------------------------------------------


@dataclass
class Frame:
    order: int
    id: str
    role: str | None
    chapter: int | None
    chapter_text: str | None
    layout: str | None
    marker: int | None  # 1-based line of the frame marker
    start: int  # 1-based line of \begin{frame}
    end: int  # 1-based line of \end{frame}
    text: str  # comment-free source of lines start..end
    outside: str = ""  # text with the DefenseSource environments blanked
    masked: str = ""  # text with every part that is not visible text blanked

    @property
    def content(self) -> bool:
        return self.role not in NON_CONTENT_ROLES

    def line_at(self, offset: int) -> int:
        return self.start + self.text.count("\n", 0, offset)

    def visible_lines(self, masked: str | None = None) -> list[tuple[int, str]]:
        source = self.masked if masked is None else masked
        return [(self.start + i, visible(line)) for i, line in enumerate(source.split("\n"))]


@dataclass
class Deck:
    path: Path
    lines: list[str]
    code: str
    starts: list[int]
    body: int  # offset of \begin{document}; the length of code when it is absent
    frames: list[Frame]

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def preamble(self) -> str:
        return self.code[: self.body]

    def line_of(self, offset: int) -> int:
        return bisect.bisect_right(self.starts, offset)

    def frame_at(self, line: int | None) -> Frame | None:
        if line is None:
            return None
        return next((frame for frame in self.frames if frame.start <= line <= frame.end), None)

    def commands(self, name: str, count: int) -> list[tuple[int, list[str]]]:
        """Line and brace arguments of each ``\\name`` in the preamble."""
        text = self.preamble
        found = []
        for match in re.finditer(r"(?<!\\)\\" + name + r"(?![A-Za-z@])", text):
            try:
                _, pos = extract_thesis.read_optional(text, match.end())
                groups, _ = extract_thesis.read_groups(text, pos, count)
            except ValueError:
                groups = []
            found.append((self.line_of(match.start()), groups))
        return found


def make_frame(lines: list[str], code: list[str], first: int, last: int, order: int) -> Frame:
    text = "\n".join(code[first : last + 1])
    frame = Frame(order, f"#{order}", None, None, None, None, None, first + 1, last + 1, text)
    index = first - 1
    while index >= 0 and not lines[index].strip():
        index -= 1
    match = MARKER_RE.match(lines[index].strip()) if index >= 0 else None
    if match:
        frame_id, role, chapter, layout = match.groups()
        frame.id, frame.role, frame.chapter_text, frame.layout = frame_id, role, chapter, layout
        frame.chapter = int(chapter) if chapter.isdecimal() else None
        frame.marker = index + 1
    frame.outside = blank(text, source_spans(text))
    frame.masked = blank(text, hidden_spans(text))
    return frame


def read_lines(path: Path) -> list[str]:
    return [line.rstrip("\r") for line in tex_loader.read_text_robust(path)[0].split("\n")]


def parse_deck(path: Path) -> Deck:
    try:
        lines = read_lines(path)
    except OSError as exc:
        raise CheckError(f"无法读取答辩稿 {path}：{exc}") from exc
    code_lines = [tex_loader.COMMENT_RE.sub("", line) for line in lines]
    code = "\n".join(code_lines)
    starts = [0]
    for line in code_lines[:-1]:
        starts.append(starts[-1] + len(line) + 1)
    frames: list[Frame] = []
    first: int | None = None
    for index, line in enumerate(code_lines):
        if first is None and FRAME_BEGIN_RE.search(line):
            first = index
        if first is not None and FRAME_END_RE.search(line):
            frames.append(make_frame(lines, code_lines, first, index, len(frames) + 1))
            first = None
    if first is not None:
        frames.append(make_frame(lines, code_lines, first, len(lines) - 1, len(frames) + 1))
    begin = re.search(r"\\begin\s*\{document\}", code)
    return Deck(path, lines, code, starts, begin.start() if begin else len(code), frames)


@dataclass
class NoteSection:
    order: int
    frame_id: str
    role: str
    seconds: int
    start: int  # 1-based line of the heading
    end: int
    fields: dict[str, tuple[int, str]] = field(default_factory=dict)

    @property
    def duration(self) -> int:
        """Seconds of the 时长 field; the heading value when the field is absent."""
        match = re.match(r"\s*(-?\d+)", self.fields.get("时长", (0, ""))[1])
        return int(match.group(1)) if match else self.seconds


def parse_notes(lines: list[str]) -> list[NoteSection]:
    sections: list[NoteSection] = []
    current: NoteSection | None = None
    for number, line in enumerate(lines, 1):
        if line.startswith("## "):
            if current is not None:
                current.end = number - 1
            match = NOTES_HEADING_RE.match(line)
            current = None
            if match:
                order, _, frame_id, role, seconds = match.groups()
                current = NoteSection(int(order), frame_id, role, int(seconds), number, len(lines))
                sections.append(current)
            continue
        found = NOTES_FIELD_RE.match(line)
        if current is not None and found and found.group(1) not in current.fields:
            current.fields[found.group(1)] = (number, found.group(2).strip())
    return sections


def log_entries(lines: list[str]) -> list[tuple[int, str]]:
    """Log messages with TeX's 79-character wrapping undone, with their first line number."""
    entries: list[tuple[int, str]] = []
    buffer = ""
    first = 0
    for number, line in enumerate(lines, 1):
        if not buffer:
            first = number
        buffer += line
        if len(line) != LOG_WIDTH:
            entries.append((first, buffer))
            buffer = ""
    if buffer:
        entries.append((first, buffer))
    return entries


# ---------------------------------------------------------------------------
# Check context
# ---------------------------------------------------------------------------


@dataclass
class FigureUse:
    frame: Frame
    line: int
    file: str
    caption: str | None
    path: Path | None  # resolved file; None when the deck cannot find it
    owner: dict | None  # inventory figure that lists the file
    allowed: bool


@dataclass
class Context:
    deck: Deck
    inventory: dict
    plan: dict | None
    plan_meta: dict
    minutes: int
    notes_lines: list[str] | None
    log_name: str
    log: list[tuple[int, str]] | None
    notes: list[NoteSection] = field(default_factory=list)
    chapters: list[int] = field(default_factory=list)
    roles: dict[int, str | None] = field(default_factory=dict)
    stage: str = "predefense"
    stage_line: int | None = None
    thesis_numbers: set[str] | None = None
    uses: list[FigureUse] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def add(
        self,
        code: str,
        severity: str,
        frame: Frame | str | None,
        message: str,
        *,
        line: int | None = None,
        file: str | None = None,
        meaning: str = "",
    ) -> None:
        """Record a finding; a Frame gives its id and, for deck findings, its first line."""
        if isinstance(frame, Frame):
            frame_id = frame.id
            if line is None and file is None:
                line = frame.start
        else:
            frame_id = frame or "-"
        finding = Finding(code, severity, frame_id, file or self.deck.name, line, message, meaning)
        self.findings.append(finding)

    def skip(self, code: str) -> None:
        if code not in self.skipped:
            self.skipped.append(code)

    @property
    def plan_stage(self) -> str | None:
        return self.plan_meta.get("stage") if self.plan is not None else None

    def note_for(self, frame: Frame) -> NoteSection | None:
        """Notes section of a frame: by frame id, or by frame order without a marker."""
        if frame.marker is None:
            return next((s for s in self.notes if s.order == frame.order), None)
        return next((s for s in self.notes if s.frame_id == frame.id), None)

    def section_frame(self, section: NoteSection) -> str:
        """Deck frame id of a notes section."""
        frame = next((f for f in self.deck.frames if f.id == section.frame_id), None)
        if frame is None:
            frame = next(
                (f for f in self.deck.frames if f.marker is None and f.order == section.order),
                None,
            )
        return frame.id if frame else section.frame_id

    def notes_frame(self, line: int) -> str | None:
        section = next((s for s in self.notes if s.start <= line <= s.end), None)
        return self.section_frame(section) if section else None


def read_mapping(path: Path, kind: str) -> dict:
    label = "清单" if kind == "json" else "规划"
    try:
        text = tex_loader.read_text_robust(path)[0]
        value = json.loads(text) if kind == "json" else yaml.safe_load(text)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise CheckError(f"无法读取{label} {path}：{exc}") from exc
    if not isinstance(value, dict):
        raise CheckError(f"{label} {path} 的顶层不是映射")
    return value


def thesis_root(inventory: dict, inventory_path: Path) -> Path:
    root = Path(str(inventory.get("thesis_root") or ""))
    return root if root.is_absolute() else inventory_path.parent / root


def load_thesis_numbers(inventory: dict, root: Path) -> set[str] | None:
    """Numbers of the assembled thesis source; None when the thesis cannot be read."""
    main = root / str(inventory.get("main_tex") or "")
    if not main.is_file():
        return None
    try:
        document = tex_loader.assemble(main)
    except (OSError, ValueError):
        return None
    text = "\n".join(tex_loader.COMMENT_RE.sub("", line) for line in document.lines)
    return set(NUMBER_RE.findall(normalize_digits(text)))


def resolve_image(base: Path, graphicspath: list[str], name: str) -> Path | None:
    """Find a graphics file the way graphicx does: the deck directory, then \\graphicspath."""
    if not name:
        return None
    has_extension = Path(name).suffix.lower() in extract_thesis.IMAGE_EXTENSIONS
    for directory in ["", *graphicspath]:
        stem = base / directory / name
        candidates = (
            [stem]
            if has_extension
            else [stem.with_name(stem.name + ext) for ext in extract_thesis.IMAGE_EXTENSIONS]
        )
        for candidate in candidates:
            if candidate.is_file():
                return candidate.resolve()
    return None


def deck_logo(deck: Deck) -> str | None:
    for _, groups in reversed(deck.commands("DefenseSetup", 1)):
        match = LOGO_KEY_RE.search(groups[0]) if groups else None
        if match:
            value = (match.group(1) if match.group(1) is not None else match.group(2)).strip()
            return normalize_path(value) if value else None
    return None


def figure_uses(deck: Deck, inventory: dict, root: Path) -> list[FigureUse]:
    """Graphics files that the frames show outside DefenseSource, with their inventory figure."""
    by_name: dict[str, dict] = {}
    by_file: dict[Path, dict] = {}
    for figure in inventory.get("figures") or []:
        for item in figure.get("files") or []:
            for key in (item.get("path"), item.get("resolved")):
                if key:
                    by_name.setdefault(normalize_path(key), figure)
            resolved = root / str(item.get("resolved") or "")
            if item.get("resolved") and resolved.is_file():
                by_file.setdefault(resolved.resolve(), figure)
        for sub in figure.get("subfigures") or []:
            if sub.get("file"):
                by_name.setdefault(normalize_path(sub["file"]), figure)
    logo = deck_logo(deck)
    graphicspath = extract_thesis.graphicspath_entries(deck.preamble)
    uses = []
    for frame in deck.frames:
        for match in FIGURE_CALL_RE.finditer(frame.outside):
            count = 2 if match.group(1) == "DefenseFigure" else 1
            try:
                _, pos = extract_thesis.read_optional(frame.text, match.end())
                groups, _ = extract_thesis.read_groups(frame.text, pos, count)
            except ValueError:
                continue
            if not groups:
                continue
            name = groups[0].strip()
            path = resolve_image(deck.path.parent, graphicspath, name)
            owner = by_name.get(normalize_path(name)) or (by_file.get(path) if path else None)
            allowed = owner is not None or (logo is not None and normalize_path(name) == logo)
            caption = groups[1] if len(groups) == 2 else None
            line = frame.line_at(match.start())
            uses.append(FigureUse(frame, line, name, caption, path, owner, allowed))
    return uses


def deck_chapters(deck: Deck, plan_meta: dict, inventory: dict) -> list[int]:
    """Chapter numbers of \\DefenseAddChapter; else of the plan meta or the inventory."""
    numbers = [
        int(groups[0].strip())
        for _, groups in deck.commands("DefenseAddChapter", 2)
        if groups and groups[0].strip().isdecimal()
    ]
    if numbers:
        return numbers
    source = plan_meta.get("chapters")
    if not isinstance(source, list):
        source = inventory.get("chapters") or []
    return [c["number"] for c in source if isinstance(c, dict) and isinstance(c.get("number"), int)]


def chapter_roles(
    chapters: list[int], frames: list[Frame], plan_meta: dict
) -> dict[int, str | None]:
    """Chapter role from the plan; else inferred from the page roles of the frame markers."""
    planned = plan_meta.get("chapters")
    planned_roles = {
        c.get("number"): c.get("role")
        for c in (planned if isinstance(planned, list) else [])
        if isinstance(c, dict)
    }
    roles: dict[int, str | None] = {}
    for number in chapters:
        role = planned_roles.get(number)
        if role not in defense_budget.CHAPTER_ROLES:
            pages = {frame.role for frame in frames if frame.chapter == number}
            role = next((name for name, hints in CHAPTER_ROLE_HINTS if pages & hints), None)
        roles[number] = role
    return roles


def deck_stage(deck: Deck) -> tuple[str, int | None]:
    """Last stage setting of the preamble; predefense (the theme default) without one."""
    settings: list[tuple[int, str]] = []
    for line, groups in deck.commands("DefenseSetup", 1):
        match = STAGE_KEY_RE.search(groups[0]) if groups else None
        if match:
            settings.append((line, match.group(1)))
    for line, groups in deck.commands("DefenseStage", 1):
        if groups:
            settings.append((line, groups[0].strip()))
    if not settings:
        return "predefense", None
    line, stage = max(settings)
    return stage, line


# ---------------------------------------------------------------------------
# Structure checks
# ---------------------------------------------------------------------------


def check_marker(ctx: Context) -> None:
    seen: dict[str, int] = {}
    for frame in ctx.deck.frames:
        if frame.marker is None:
            ctx.add("D-MARKER", "Minor", frame, "缺少帧标记 % defense-frame；按帧序号定位")
            continue
        invalid = []
        if frame.role not in ROLES:
            invalid.append(f"role={frame.role}")
        if frame.layout not in LAYOUTS:
            invalid.append(f"layout={frame.layout}")
        if frame.chapter is None and frame.chapter_text != "-":
            invalid.append(f"chapter={frame.chapter_text}")
        if invalid:
            message = f"帧标记取值无效：{'，'.join(invalid)}"
            ctx.add("D-MARKER", "Major", frame, message, line=frame.marker)
        if frame.id in seen:
            message = f"帧 id {frame.id} 与第 {seen[frame.id]} 帧重复"
            ctx.add("D-MARKER", "Major", frame, message, line=frame.marker)
        else:
            seen[frame.id] = frame.order


def check_coverage(ctx: Context) -> None:
    frames = [frame for frame in ctx.deck.frames if frame.role != "backup"]
    if frames and frames[0].role != "cover":
        ctx.add("D-COVERAGE", "Major", frames[0], "首帧应为封面（cover）")
    if frames and frames[-1].role != "thanks":
        ctx.add("D-COVERAGE", "Major", frames[-1], "末帧（备用页除外）应为致谢页（thanks）")
    for number, role in ctx.roles.items():
        chapter_frames = [frame for frame in ctx.deck.frames if frame.chapter == number]
        present = {frame.role for frame in chapter_frames}
        missing = [page for page in REQUIRED_ROLES.get(role or "", ()) if page not in present]
        if missing:
            target = chapter_frames[0] if chapter_frames else None
            message = f"第 {number} 章（{role}）缺少页角色：{'、'.join(missing)}"
            ctx.add("D-COVERAGE", "Major", target, message)


def toc_argument(frame: Frame) -> int | None:
    match = TOC_ARG_RE.search(frame.text)
    return int(match.group(1)) if match else None


def check_toc(ctx: Context) -> None:
    frames = ctx.deck.frames
    if len(frames) < 2 or toc_argument(frames[1]) != 0:
        target = frames[1] if len(frames) > 1 else None
        ctx.add("D-TOC", "Major", target, "第二帧应为总目录 \\DefenseTocFrame{0}")
    for number in ctx.chapters[1:]:
        tocs = [f for f in frames if f.role == "toc" and f.chapter == number]
        if not tocs:
            tocs = [f for f in frames if f.marker is None and toc_argument(f) == number]
        body = [f for f in frames if f.chapter == number and f.role != "toc"]
        if not tocs:
            target = body[0] if body else None
            ctx.add("D-TOC", "Major", target, f"缺少第 {number} 章的章前目录")
            continue
        toc = tocs[0]
        argument = toc_argument(toc)
        if argument != number:
            found = "未调用 \\DefenseTocFrame" if argument is None else f"参数为 {argument}"
            message = f"第 {number} 章的章前目录{found}，应为 \\DefenseTocFrame{{{number}}}"
            ctx.add("D-TOC", "Major", toc, message)
        if body and body[0].order != toc.order + 1:
            message = f"第 {number} 章的章前目录应紧接在该章首帧 {body[0].id} 之前"
            ctx.add("D-TOC", "Major", toc, message)


def subsection_text(frame: Frame) -> str:
    match = SUBSECTION_RE.search(frame.outside)
    group = group_after(frame.text, match.end()) if match else None
    return visible(group) if group is not None else ""


def check_chain(ctx: Context) -> None:
    research = [number for number, role in ctx.roles.items() if role == "research"]
    intros = [f for f in ctx.deck.frames if f.role == "intro" and f.chapter in research]
    for role, label in (("challenges", "问题卡片"), ("innovation", "创新点卡片")):
        frames = [frame for frame in ctx.deck.frames if frame.role == role]
        if not frames:
            continue
        cards = sum(len(COUNT_RES["card"].findall(frame.outside)) for frame in frames)
        if cards != len(intros):
            message = f"{label} {cards} 张，研究章引言页 {len(intros)} 个；两者应相等"
            ctx.add("D-CHAIN", "Major", frames[0], message)
    for frame in intros:
        expected = research.index(frame.chapter) + 1 if frame.chapter in research else 0
        match = RESEARCH_ITEM_RE.search(subsection_text(frame))
        found = int(match.group(1)) if match else None
        if found != expected:
            current = f"当前为「研究内容 {found}」" if found else "当前缺少「研究内容 i」"
            message = f"小节条应为「研究内容 {expected}：章题」，{current}"
            ctx.add("D-CHAIN", "Major", frame, message)


def check_placeholder(ctx: Context) -> None:
    for number, line in enumerate(ctx.deck.lines, 1):
        tokens = unique(PLACEHOLDER_RE.findall(line))
        if tokens:
            frame = ctx.deck.frame_at(number)
            ctx.add("D-PLACEHOLDER", "Major", frame, f"含占位符 {'、'.join(tokens)}", line=number)
    for number, line in enumerate(ctx.notes_lines or [], 1):
        tokens = unique(PLACEHOLDER_RE.findall(line))
        if tokens:
            message = f"含占位符 {'、'.join(tokens)}"
            frame_id = ctx.notes_frame(number)
            ctx.add("D-PLACEHOLDER", "Major", frame_id, message, line=number, file=NOTES_NAME)


# ---------------------------------------------------------------------------
# Figure checks
# ---------------------------------------------------------------------------


def check_fig_allow(ctx: Context) -> None:
    for use in ctx.uses:
        if not use.allowed:
            message = f"图片 {use.file} 不在清单 figures 的图片文件中；只用论文已有的图"
            ctx.add("D-FIG-ALLOW", "Critical", use.frame, message, line=use.line)


def check_fig_missing(ctx: Context) -> None:
    for use in ctx.uses:
        if use.allowed and use.path is None:
            message = f"图片 {use.file} 按 \\graphicspath 与扩展名回退找不到文件"
            ctx.add("D-FIG-MISSING", "Major", use.frame, message, line=use.line)


def check_fig_number(ctx: Context) -> None:
    known = {
        "图": {
            label_number(str(f.get("number") or "")) for f in ctx.inventory.get("figures") or []
        },
        "表": {label_number(str(t.get("number") or "")) for t in ctx.inventory.get("tables") or []},
    }

    def unknown(text: str) -> list[str]:
        refs = FIGURE_REF_RE.findall(text)
        return unique(
            [f"{kind}{compact(n)}" for kind, n in refs if label_number(n) not in known[kind]]
        )

    for frame in ctx.deck.frames:
        for line, text in frame.visible_lines():
            if unknown(text):
                message = f"{'、'.join(unknown(text))} 不在清单编号中"
                ctx.add("D-FIG-NUMBER", "Major", frame, message, line=line)
    for section in ctx.notes:
        for name in NOTES_TEXT_FIELDS:
            line, value = section.fields.get(name, (0, ""))
            if unknown(value):
                message = f"讲稿「{name}」中的 {'、'.join(unknown(value))} 不在清单编号中"
                frame_id = ctx.section_frame(section)
                ctx.add("D-FIG-NUMBER", "Major", frame_id, message, line=line, file=NOTES_NAME)

    captions: list[tuple[Frame, int, str, set[str]]] = []
    for use in ctx.uses:
        if use.caption is not None and use.owner is not None:
            owner = {label_number(str(use.owner.get("number") or ""))}
            captions.append((use.frame, use.line, use.caption, owner))
    for frame in ctx.deck.frames:
        owners = {
            label_number(str(use.owner.get("number") or ""))
            for use in ctx.uses
            if use.frame is frame and use.owner is not None
        }
        for match in CAPTION_CALL_RE.finditer(frame.outside):
            group = group_after(frame.text, match.end())
            if group is not None and owners:
                captions.append((frame, frame.line_at(match.start()), group, owners))
    for frame, line, caption, owners in captions:
        match = CAPTION_NUMBER_RE.match(visible(caption))
        number = label_number(match.group(1)) if match else None
        if number and number in known["图"] and number not in owners:
            shown = "、".join(sorted(owners))
            message = f"题注编号 图{number} 与所示图片所属的图 {shown} 不同"
            ctx.add("D-FIG-NUMBER", "Major", frame, message, line=line)


def image_size(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image

        with Image.open(path) as image:
            width, height = image.size
    except Exception:  # unreadable files skip D-FIG-ASPECT (references/quality-gate.md)
        return None
    return (width, height) if width > 0 and height > 0 else None


def check_fig_aspect(ctx: Context) -> None:
    for use in ctx.uses:
        if use.path is None or use.path.suffix.lower() not in BITMAP_SUFFIXES:
            continue
        layout = use.frame.layout
        left = layout == "figure-bullets" and bool(COLUMNS_RE.search(use.frame.outside))
        if layout not in TALL_LAYOUTS and not left:
            continue
        size = image_size(use.path)
        if size is None:
            continue
        width, height = size
        if layout in TALL_LAYOUTS and height / width > TALL_RATIO:
            message = (
                f"位图 {use.file} 高宽比 {height / width:.2f}，大于 {TALL_RATIO}（版式 {layout}）"
            )
            ctx.add("D-FIG-ASPECT", "Minor", use.frame, message, line=use.line)
        elif left and width / height > WIDE_RATIO:
            message = f"位图 {use.file} 宽高比 {width / height:.2f}，大于 {WIDE_RATIO:g}（figure-bullets 左栏）"
            ctx.add("D-FIG-ASPECT", "Minor", use.frame, message, line=use.line)


# ---------------------------------------------------------------------------
# Source checks
# ---------------------------------------------------------------------------


def source_blocks(text: str, names: tuple[str, ...]) -> list[extract_thesis.Env]:
    """Outermost environments of the given names inside DefenseSource environments."""
    envs = extract_thesis.pair_environments(text)
    regions = [(env.start, env.end) for env in envs if env.name == "DefenseSource"]
    inside = [
        env
        for env in envs
        if env.name.rstrip("*") in names
        and any(start <= env.start and env.end <= end for start, end in regions)
    ]
    return [
        env
        for env in inside
        if not any(o is not env and o.start <= env.start and env.end <= o.end for o in inside)
    ]


def report_outside(
    ctx: Context, code: str, frame: Frame, pattern: re.Pattern[str], kind: str
) -> None:
    """One Major finding per line where the pattern occurs outside DefenseSource."""
    found: dict[int, list[str]] = {}
    for match in pattern.finditer(frame.outside):
        found.setdefault(frame.line_at(match.start()), []).append(match.group(0))
    for line, tokens in found.items():
        message = f"DefenseSource 外出现{kind} {' '.join(unique(tokens))}；放入 DefenseSource 并逐字复制论文"
        ctx.add(code, "Major", frame, message, line=line)


def check_eq_src(ctx: Context) -> None:
    known = {
        normalize_equation(str(eq.get("tex") or "")) for eq in ctx.inventory.get("equations") or []
    }
    for frame in ctx.deck.frames:
        for env in source_blocks(frame.text, EQUATION_NAMES):
            if normalize_equation(frame.text[env.body_start : env.body_end]) not in known:
                message = f"DefenseSource 中的 {env.name} 公式与清单中任一公式不同；按论文逐字复制"
                ctx.add("D-EQ-SRC", "Critical", frame, message, line=frame.line_at(env.start))
        report_outside(ctx, "D-EQ-SRC", frame, OUTSIDE_MATH_RE, "数学公式")


def check_tab_src(ctx: Context) -> None:
    known = {compact(str(t.get("tabular_source") or "")) for t in ctx.inventory.get("tables") or []}
    for frame in ctx.deck.frames:
        for env in source_blocks(frame.text, TABLE_NAMES):
            if compact(frame.text[env.start : env.end]) not in known:
                message = (
                    f"DefenseSource 中的 {env.name} 表体与清单中任一表体不同；表体逐字复制论文"
                )
                ctx.add("D-TAB-SRC", "Critical", frame, message, line=frame.line_at(env.start))
        report_outside(ctx, "D-TAB-SRC", frame, OUTSIDE_TABLE_RE, "表格环境")


def check_num_src(ctx: Context) -> None:
    thesis = ctx.thesis_numbers
    if thesis is None:
        ctx.skip("D-NUM-SRC")
        return

    def report(frame: Frame | str | None, line: int, text: str, file: str | None) -> None:
        missing = [token for token in number_tokens(text) if token not in thesis]
        if missing:
            message = f"数字 {'、'.join(missing)} 在论文全文中没有同形数字；回到论文原句核对"
            ctx.add("D-NUM-SRC", "Major", frame, message, line=line, file=file, meaning="NEEDS-LLM")

    for frame in ctx.deck.frames:
        masked = SUBSECTION_NUMBER_RE.sub(
            lambda m: m.group(1) + " " * len(m.group(2)), frame.masked
        )
        for line, text in frame.visible_lines(masked):
            report(frame, line, text, None)
    for section in ctx.notes:
        for name in NOTES_TEXT_FIELDS:
            if name in section.fields:
                line, value = section.fields[name]
                report(ctx.section_frame(section), line, value, NOTES_NAME)


def check_paper(ctx: Context) -> None:
    publications = ctx.inventory.get("publications") or []
    by_text = {compact(str(p.get("text") or "")): p for p in publications}
    for frame in ctx.deck.frames:
        for match in PAPER_BOX_RE.finditer(frame.outside):
            group = group_after(frame.text, match.end())
            if group is None:
                continue
            line = frame.line_at(match.start())
            publication = by_text.get(compact(visible(group)))
            if publication is None:
                message = "「论文」框文本与清单成果列表中任一条目不同；著录文本逐字取自成果列表"
                ctx.add("D-PAPER", "Critical", frame, message, line=line)
                continue
            chapters = publication.get("chapters") or []
            if frame.chapter is not None and frame.chapter not in chapters:
                marked = "、".join(str(c) for c in chapters) or "（未标注）"
                message = (
                    f"成果 {publication.get('id')} 在成果列表中对应第 {marked} 章，"
                    f"不含本帧所在的第 {frame.chapter} 章"
                )
                ctx.add("D-PAPER", "Major", frame, message, line=line)
    for number, role in ctx.roles.items():
        if role != "research" or not any(number in (p.get("chapters") or []) for p in publications):
            continue
        summaries = [f for f in ctx.deck.frames if f.role == "summary" and f.chapter == number]
        if summaries and not any(PAPER_BOX_RE.search(f.outside) for f in summaries):
            message = f"第 {number} 章在成果列表中有对应成果，小结页没有「论文」框"
            ctx.add("D-PAPER", "Minor", summaries[0], message)


COVER_FIELDS = (
    ("title", "题目"),
    ("author", "作者"),
    ("DefenseSupervisor", "导师"),
    ("DefenseSchool", "学院"),
    ("DefenseSubject", "学科"),
    ("date", "日期"),
)


def check_meta(ctx: Context) -> None:
    values: dict[str, tuple[int | None, str]] = {}
    for command, label in COVER_FIELDS:
        found = ctx.deck.commands(command, 1)
        line, groups = found[-1] if found else (None, [])
        text = compact(visible(groups[0])) if groups else ""
        values[command] = (line, text)
        if not text:
            ctx.add("D-META", "Major", None, f"封面字段「{label}」为空（\\{command}）", line=line)
    meta = ctx.inventory.get("meta") or {}
    for command, key, label in (("title", "title_zh", "题目"), ("author", "author", "作者")):
        line, text = values[command]
        expected = compact(str(meta.get(key) or ""))
        if not expected:
            message = f"清单 meta.{key} 为空，不能核对封面{label}"
            ctx.add("D-META", "Info", None, message, line=line)
        elif text and text != expected:
            ctx.add("D-META", "Major", None, f"封面{label}与清单 meta.{key} 不同", line=line)


def check_stage(ctx: Context) -> None:
    achievements = [frame for frame in ctx.deck.frames if frame.role == "achievements"]
    line = ctx.stage_line
    if ctx.stage not in STAGES:
        message = f"阶段 {ctx.stage} 无效；应为 predefense 或 defense"
        ctx.add("D-STAGE", "Major", None, message, line=line)
    planned = ctx.plan_stage
    if planned is not None and planned != ctx.stage:
        message = f"答辩稿阶段 {ctx.stage} 与规划 meta.stage（{planned}）不同"
        ctx.add("D-STAGE", "Major", None, message, line=line)
    if ctx.stage == "defense" and not achievements:
        ctx.add("D-STAGE", "Major", None, "defense 阶段缺少成果页（achievements）", line=line)
    if ctx.stage == "predefense":
        for frame in achievements:
            ctx.add("D-STAGE", "Minor", frame, "predefense 阶段不设成果页（achievements）")


# ---------------------------------------------------------------------------
# Density, time, and notes checks
# ---------------------------------------------------------------------------


def check_density(ctx: Context) -> None:
    for frame in ctx.deck.frames:
        if not frame.content:
            continue
        count = sum(len(compact(text)) for _, text in frame.visible_lines())
        if count > DENSITY_MAJOR:
            ctx.add("D-DENSITY", "Major", frame, f"可见字符 {count} 个，超过 {DENSITY_MAJOR} 个")
        elif count > DENSITY_MINOR:
            ctx.add("D-DENSITY", "Minor", frame, f"可见字符 {count} 个，超过 {DENSITY_MINOR} 个")
        for layout, item, limit in LAYOUT_LIMITS:
            if frame.layout != layout:
                continue
            if item == "equation":
                found = len(source_blocks(frame.text, EQUATION_NAMES))
            else:
                found = len(COUNT_RES[item].findall(frame.outside))
            if found > limit:
                message = f"版式 {layout} 的{ITEM_NAMES[item]} {found} 个，上限 {limit} 个"
                ctx.add("D-DENSITY", "Minor", frame, message)
        for match in TAKEAWAY_RE.finditer(frame.outside):
            group = group_after(frame.text, match.end())
            length = len(compact(visible(group or "")))
            if length > TAKEAWAY_MAX:
                message = f"结论句 {length} 字，超过 {TAKEAWAY_MAX} 字"
                ctx.add("D-DENSITY", "Minor", frame, message, line=frame.line_at(match.start()))


def check_budget(ctx: Context) -> None:
    roles = [ctx.roles.get(number) for number in ctx.chapters]
    known = [role for role in roles if role]
    stage = ctx.plan_stage or ctx.stage
    budget = None
    if known and len(known) == len(roles):
        try:
            budget = defense_budget.compute_budget(known, ctx.minutes, stage)
        except ValueError:
            budget = None
    if budget is None:
        ctx.skip("D-BUDGET")
    else:
        content = sum(frame.content for frame in ctx.deck.frames)
        low, high = budget.page_range
        if not low <= content <= high:
            message = (
                f"内容帧 {content} 个，不在 {ctx.minutes} 分钟的预算区间 [{low}, {high}] 内"
                f"（预算内容页数 {budget.content_pages}）"
            )
            ctx.add("D-BUDGET", "Major", None, message)
    if ctx.notes_lines is None:
        return
    # The time budget does not count backup pages (references/defense-framework.md).
    total = sum(section.duration for section in ctx.notes if section.role != "backup")
    target = 60 * ctx.minutes
    if abs(total - target) > NOTES_TOLERANCE * target:
        message = f"讲稿秒数合计 {total} 秒，与目标 {target} 秒相差超过 {NOTES_TOLERANCE:.0%}"
        ctx.add("D-BUDGET", "Minor", None, message, file=NOTES_NAME)


def check_notes(ctx: Context) -> None:
    if ctx.notes_lines is None:
        ctx.add("D-NOTES", "Major", None, "缺少 notes.md；重新运行 build_deck.py", file=NOTES_NAME)
        return
    for frame in ctx.deck.frames:
        section = ctx.note_for(frame)
        if section is None:
            ctx.add("D-NOTES", "Minor", frame, "notes.md 缺少本帧的讲稿节", file=NOTES_NAME)
            continue
        missing = [name for name in NOTES_FIELDS if name not in section.fields]
        if missing:
            message = f"讲稿节缺少栏目：{'、'.join(missing)}"
            ctx.add("D-NOTES", "Minor", frame, message, line=section.start, file=NOTES_NAME)
        if frame.content and "说什么" in section.fields:
            line, value = section.fields["说什么"]
            length = len(compact(value))
            if not SAY_MIN <= length <= SAY_MAX:
                message = f"「说什么」{length} 字，内容页应为 {SAY_MIN}–{SAY_MAX} 字"
                ctx.add("D-NOTES", "Minor", frame, message, line=line, file=NOTES_NAME)


# ---------------------------------------------------------------------------
# Log checks
# ---------------------------------------------------------------------------


def place(
    ctx: Context, code: str, severity: str, source: int | None, log_line: int, message: str
) -> None:
    """Report at the deck line when it is inside a frame; else at the log line."""
    frame = ctx.deck.frame_at(source)
    if frame is not None:
        ctx.add(code, severity, frame, f"{message}（{ctx.log_name}:{log_line}）", line=source)
    else:
        ctx.add(code, severity, None, message, line=log_line, file=ctx.log_name)


def check_compile(ctx: Context) -> None:
    if ctx.log is None:
        ctx.skip("D-COMPILE")
        return
    for index, (number, text) in enumerate(ctx.log):
        error = LOG_ERROR_RE.match(text)
        if error:
            source = None
            if error.group(2) is None:
                for _, following in ctx.log[index + 1 : index + 20]:
                    found = LOG_SOURCE_LINE_RE.match(following)
                    if found:
                        source = int(found.group(1))
                        break
            elif Path(error.group(1)).name == ctx.deck.name:
                source = int(error.group(2))
            place(ctx, "D-COMPILE", "Critical", source, number, f"编译错误：{text.strip()}")
        elif LOG_FATAL_RE.search(text):
            place(ctx, "D-COMPILE", "Critical", None, number, f"编译错误：{text.strip()}")
        undefined = UNDEFINED_RE.search(text)
        if undefined:
            kind = "交叉引用" if undefined.group(1) == "Reference" else "文献引用"
            message = f"{kind} {undefined.group(2)} 未定义"
            place(ctx, "D-COMPILE", "Major", int(undefined.group(3)), number, message)
    pdf = ctx.deck.path.with_suffix(".pdf")
    if not pdf.is_file():
        ctx.add("D-COMPILE", "Critical", None, f"缺少 {pdf.name}；编译没有生成 PDF", file=pdf.name)
    elif pdf.stat().st_mtime < ctx.deck.path.stat().st_mtime:
        message = f"{pdf.name} 早于 {ctx.deck.name}；重新编译"
        ctx.add("D-COMPILE", "Critical", None, message, file=pdf.name)


def check_overflow_v(ctx: Context) -> None:
    if ctx.log is None:
        ctx.skip("D-OVERFLOW-V")
        return
    for number, text in ctx.log:
        match = VBOX_RE.search(text)
        if match:
            source = int(match.group(2)) if match.group(2) else None
            message = f"Overfull \\vbox，超出 {match.group(1)}pt"
            place(ctx, "D-OVERFLOW-V", "Major", source, number, message)


def check_overflow_h(ctx: Context) -> None:
    if ctx.log is None:
        ctx.skip("D-OVERFLOW-H")
        return
    for number, text in ctx.log:
        match = HBOX_RE.search(text)
        if not match or float(match.group(1)) <= HBOX_MINOR:
            continue
        severity = "Major" if float(match.group(1)) > HBOX_MAJOR else "Minor"
        found = match.group(2) or match.group(3)
        message = f"Overfull \\hbox，超出 {match.group(1)}pt"
        place(ctx, "D-OVERFLOW-H", severity, int(found) if found else None, number, message)


# The order of this mapping is the order in which the checks run.
CHECKS = {
    "D-MARKER": check_marker,
    "D-COVERAGE": check_coverage,
    "D-TOC": check_toc,
    "D-CHAIN": check_chain,
    "D-PLACEHOLDER": check_placeholder,
    "D-FIG-ALLOW": check_fig_allow,
    "D-FIG-MISSING": check_fig_missing,
    "D-FIG-NUMBER": check_fig_number,
    "D-FIG-ASPECT": check_fig_aspect,
    "D-EQ-SRC": check_eq_src,
    "D-TAB-SRC": check_tab_src,
    "D-NUM-SRC": check_num_src,
    "D-PAPER": check_paper,
    "D-META": check_meta,
    "D-STAGE": check_stage,
    "D-DENSITY": check_density,
    "D-BUDGET": check_budget,
    "D-NOTES": check_notes,
    "D-COMPILE": check_compile,
    "D-OVERFLOW-V": check_overflow_v,
    "D-OVERFLOW-H": check_overflow_h,
}
CODES = tuple(CHECKS)


# ---------------------------------------------------------------------------
# Input, output, and main
# ---------------------------------------------------------------------------


def load_context(args: argparse.Namespace) -> Context:
    deck_path = Path(args.deck)
    if not deck_path.is_file():
        raise CheckError(f"答辩稿不存在：{args.deck}")
    inventory_path = Path(args.inventory)
    inventory = read_mapping(inventory_path, "json")
    plan = read_mapping(Path(args.plan), "yaml") if args.plan else None
    plan_meta = plan.get("meta") if plan is not None else None
    if not isinstance(plan_meta, dict):
        plan_meta = {}
    if args.minutes is not None:
        if not defense_budget.MIN_MINUTES <= args.minutes <= defense_budget.MAX_MINUTES:
            raise CheckError(
                f"--minutes 应在 {defense_budget.MIN_MINUTES}–{defense_budget.MAX_MINUTES} 之间"
            )
        minutes = args.minutes
    else:
        planned = plan_meta.get("minutes")
        minutes = planned if isinstance(planned, int) and not isinstance(planned, bool) else 40
    if args.log and not Path(args.log).is_file():
        raise CheckError(f"日志不存在：{args.log}")
    log_path = Path(args.log) if args.log else deck_path.parent / LOG_NAME
    notes_path = deck_path.parent / NOTES_NAME

    deck = parse_deck(deck_path)
    notes_lines = read_lines(notes_path) if notes_path.is_file() else None
    log = log_entries(read_lines(log_path)) if log_path.is_file() else None
    ctx = Context(deck, inventory, plan, plan_meta, minutes, notes_lines, log_path.name, log)
    ctx.notes = parse_notes(notes_lines) if notes_lines is not None else []
    ctx.chapters = deck_chapters(deck, plan_meta, inventory)
    ctx.roles = chapter_roles(ctx.chapters, deck.frames, plan_meta)
    ctx.stage, ctx.stage_line = deck_stage(deck)
    root = thesis_root(inventory, inventory_path)
    ctx.thesis_numbers = load_thesis_numbers(inventory, root)
    ctx.uses = figure_uses(deck, inventory, root)
    return ctx


def run_checks(ctx: Context) -> list[Finding]:
    """Run every check; findings sort by frame order, then code, file, and line."""
    for check in CHECKS.values():
        check(ctx)
    order = {frame.id: frame.order for frame in ctx.deck.frames}
    last = len(ctx.deck.frames) + 1

    def key(finding: Finding) -> tuple[int, str, str, int]:
        position = 0 if finding.frame == "-" else order.get(finding.frame, last)
        return (position, finding.code, finding.file, finding.line or 0)

    return sorted(ctx.findings, key=key)


def render_text(findings: list[Finding], summary: dict[str, int], skipped: list[str]) -> list[str]:
    lines = []
    for finding in findings:
        location = f"{finding.file}:{finding.line if finding.line is not None else '-'}"
        prefix = f"Meaning-Check: {finding.meaning_check}：" if finding.meaning_check else ""
        lines.append(
            f"% {finding.code} (frame={finding.frame}, {location}) "
            f"[Severity: {finding.severity}] [Priority: {finding.priority}]: "
            f"[Script] {prefix}{finding.message}"
        )
    counts = "，".join(f"{severity} {summary[severity]}" for severity in PRIORITY)
    lines.append(f"% 汇总：{counts}；skipped：{'、'.join(skipped) or '无'}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="答辩稿质量门：按 D-* 码检查 defense.tex、notes.md 与编译日志，不写文件。"
    )
    parser.add_argument("--deck", required=True, help="build_deck.py 输出目录中的 defense.tex")
    parser.add_argument(
        "--inventory", required=True, help="extract_thesis.py 输出的 inventory.json"
    )
    parser.add_argument("--plan", help="slide_plan.yaml；提供时按规划取章角色、阶段与分钟数")
    parser.add_argument("--log", help="编译日志；缺省时使用答辩稿目录中的 defense.log（存在时）")
    parser.add_argument(
        "--minutes", type=int, help="汇报时长（分钟）；缺省取规划 meta.minutes，再缺省 40"
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args(argv)

    try:
        ctx = load_context(args)
    except CheckError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    findings = run_checks(ctx)
    summary = {severity: sum(f.severity == severity for f in findings) for severity in PRIORITY}
    if args.json:
        payload = {
            "deck": ctx.deck.name,
            "findings": [finding.as_dict() for finding in findings],
            "summary": summary,
            "skipped": ctx.skipped,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for line in render_text(findings, summary, ctx.skipped):
            print(line)
    return 1 if summary["Critical"] or summary["Major"] else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
