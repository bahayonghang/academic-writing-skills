#!/usr/bin/env python3
"""
Extract the thesis inventory for latex-defense-zh (read only).

The script reads a Chinese LaTeX thesis repository and writes inventory.json:
metadata, the chapter tree with role suggestions, figures, tables, labeled
equations, algorithms, publications with the chapter mapping, conclusion items,
preamble macros, and the logo candidate. The script never writes into the thesis.

Field details: references/plan-schema.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis DIR [--main FILE] \
        --out inventory.json [--json]

Exit codes: 0 success (warnings allowed); 2 main file missing or ambiguous.
"""

from __future__ import annotations

import argparse
import bisect
import contextlib
import json
import os
import posixpath
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tex_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import tex_loader

IMAGE_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".eps")
BLIND_RE = re.compile(r"(?i)blind|anon|review|盲审")
LOGO_RE = re.compile(r"(?i)logo|校徽|badge")
EQUATION_ENVS = ("equation", "align", "gather", "multline", "flalign", "eqnarray")
SINGLE_ROW_ENVS = ("equation", "multline")
TABULAR_ENVS = ("tabular", "tabular*", "tabularx", "xltabular", "longtable")
FLOAT_KINDS = {
    "figure": "fig",
    "figure*": "fig",
    "table": "tab",
    "table*": "tab",
    "algorithm": "alg",
}
META_FIELDS = ("title_zh", "author", "supervisor", "school", "subject", "date")
FORMAT_COMMANDS = (
    "textbf",
    "textit",
    "textsl",
    "emph",
    "underline",
    "uline",
    "textrm",
    "textsf",
    "texttt",
    "textsc",
    "textup",
    "textmd",
    "textnormal",
    "mbox",
    "text",
)
OUTLOOK_KEYWORDS = ("展望", "未来", "今后", "下一步")

ENV_TOKEN_RE = re.compile(r"\\(begin|end)\s*\{([^{}]+)\}")
LABEL_RE = re.compile(r"\\label\s*\{([^{}]*)\}")
CAPTION_RE = re.compile(r"\\(bicaption|caption)(?![A-Za-z@])\*?")
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?![A-Za-z@])\*?")
SUBCAPTIONBOX_RE = re.compile(r"\\subcaptionbox(?![A-Za-z@])(\*?)")
STRUCTURE_RE = re.compile(
    r"(?<!\\)\\(chapter|section|subsection|appendix|backmatter)(?![A-Za-z@])(\*?)"
)
MACRO_DEF_RE = re.compile(
    r"(?<!\\)\\(newcommand|renewcommand|providecommand|DeclareMathOperator|def)"
    r"(?![A-Za-z@])(\*?)"
)
TITLE_LINES_RE = re.compile(
    r"(?<!\\)\\(?:(?:newcommand|renewcommand|providecommand)\*?\s*\{?\s*|def\s*)"
    r"\\[A-Za-z@]*titlelines(?![A-Za-z@])\s*\}?"
)
NOTAG_RE = re.compile(r"\\(?:notag|nonumber)(?![A-Za-z@])")
TAG_RE = re.compile(r"\\tag\*?\s*\{([^{}]*)\}")
_MARK_CHAPTER = r"第[^章。；;）)]{1,30}?章"
CHAPTER_MARK_RE = re.compile(
    r"(?:[，,；;]\s*)?[（(]?\s*对应(?:论文|本文)?"
    rf"({_MARK_CHAPTER}(?:\s*[、，,和及与]\s*{_MARK_CHAPTER})*)\s*[）)]?"
)
NUMBERED_ITEM_RE = re.compile(r"^\s*(?:\(\s*\d+\s*\)|\d+\s*[.、)](?!\d))")
ITEM_NUMBER_PREFIX_RE = re.compile(r"^\s*(?:（\s*\d+\s*）|\(\s*\d+\s*\)|\d+\s*[.、)）])\s*")
LIST_BEGIN_RE = re.compile(r"\\begin\s*\{(?:enumerate|itemize)\}\s*(?:\[[^\]]*\])?")
LIST_END_RE = re.compile(r"\\end\s*\{(?:enumerate|itemize)\}")
HEADING_RE = re.compile(r"\\(?:sub)*section\*?\s*(?:\[[^\]]*\])?\s*\{(.*)\}")
CN_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


class ExtractError(Exception):
    """Main file selection failed (exit code 2)."""


# ---------------------------------------------------------------------------
# Low-level readers
# ---------------------------------------------------------------------------


def strip_comments(text: str) -> str:
    """Remove ``%`` comments line by line with the tex_loader rule (keeps ``\\%``)."""
    return "\n".join(tex_loader.COMMENT_RE.sub("", line) for line in text.split("\n"))


def skip_ws(text: str, pos: int) -> int:
    while pos < len(text) and text[pos] in " \t\r\n":
        pos += 1
    return pos


def read_group(text: str, pos: int) -> tuple[str, int]:
    """Read the balanced ``{...}`` group that starts at ``pos``.

    Returns the inner text and the index after the closing brace. Escaped
    braces ``\\{`` and ``\\}`` do not change the depth. Raises ValueError when
    no group starts at ``pos`` or the group is not closed.
    """
    if pos >= len(text) or text[pos] != "{":
        raise ValueError("group expected")
    depth = 0
    index = pos
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[pos + 1 : index], index + 1
        index += 1
    raise ValueError("unclosed group")


def read_optional(text: str, pos: int) -> tuple[str | None, int]:
    """Read an optional ``[...]`` argument after whitespace; brackets in braces do not count."""
    start = skip_ws(text, pos)
    if start >= len(text) or text[start] != "[":
        return None, pos
    depth = 0
    index = start + 1
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "]" and depth == 0:
            return text[start + 1 : index], index + 1
        index += 1
    raise ValueError("unclosed optional argument")


def read_groups(text: str, pos: int, count: int) -> tuple[list[str], int]:
    """Read up to ``count`` consecutive brace groups after whitespace."""
    groups: list[str] = []
    for _ in range(count):
        start = skip_ws(text, pos)
        if start >= len(text) or text[start] != "{":
            break
        group, pos = read_group(text, start)
        groups.append(group)
    return groups, pos


def command_args(text: str, name: str, count: int) -> list[str]:
    """Arguments of the first non-star ``\\name``; one optional argument is skipped."""
    match = re.search(r"(?<!\\)\\" + name + r"(?![A-Za-z@*])", text)
    if not match:
        return []
    try:
        _, pos = read_optional(text, match.end())
        groups, _ = read_groups(text, pos, count)
    except ValueError:
        return []
    return groups


def plain_text(tex: str) -> str:
    """Convert a short LaTeX fragment to plain text (titles, items, publications)."""
    text = re.sub(
        r"\\(?:label|cite[a-zA-Z]*|upcite|parencite|textcite|footnote)\*?"
        r"(?:\[[^\]]*\])*\{[^{}]*\}",
        "",
        tex,
    )
    text = text.replace("\\\\", " ")
    text = re.sub(r"\\([%&#_$])", r"\1", text)
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\\(?:" + "|".join(FORMAT_COMMANDS) + r")\*?\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:(?:q?quad)(?![A-Za-z])|[,;:! ])", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?", "", text)
    text = text.replace("~", " ").replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def clean_caption(tex: str) -> str:
    return LABEL_RE.sub("", tex).strip()


def cn_to_int(value: str) -> int | None:
    """Convert 1..99 in Arabic or Chinese numerals (一 to 九十九) to int."""
    value = value.strip()
    if value.isdigit():
        return int(value)
    if value == "十":
        return 10
    if len(value) == 1:
        return CN_DIGITS.get(value)
    if len(value) == 2 and value[0] == "十" and value[1] in CN_DIGITS:
        return 10 + CN_DIGITS[value[1]]
    if len(value) == 2 and value[1] == "十" and value[0] in CN_DIGITS:
        return CN_DIGITS[value[0]] * 10
    if len(value) == 3 and value[1] == "十" and value[0] in CN_DIGITS and value[2] in CN_DIGITS:
        return CN_DIGITS[value[0]] * 10 + CN_DIGITS[value[2]]
    return None


def parse_chapter_marks(text: str) -> list[int]:
    """Chapter numbers from marks such as 「对应论文第三、四章」 or 「对应第3-5章」."""
    numbers: list[int] = []
    for match in CHAPTER_MARK_RE.finditer(text):
        segment = unicodedata.normalize("NFKC", match.group(1))
        for inner in re.findall(r"第([^章]+?)章", segment):
            for part in re.split(r"[、,和及与]", inner):
                bounds = re.split(r"至|-|~|—|–", part)
                if len(bounds) == 2:
                    low, high = cn_to_int(bounds[0]), cn_to_int(bounds[1])
                    if low and high and low <= high:
                        numbers.extend(range(low, high + 1))
                    continue
                number = cn_to_int(part)
                if number:
                    numbers.append(number)
    return sorted(set(numbers))


def strip_chapter_marks(text: str) -> str:
    return re.sub(r"\s+", " ", CHAPTER_MARK_RE.sub("", text)).strip()


# ---------------------------------------------------------------------------
# Assembled source with offset -> file:line mapping
# ---------------------------------------------------------------------------


@dataclass
class Source:
    doc: tex_loader.AssembledDocument
    text: str
    line_starts: list[int]
    prefix: str

    @classmethod
    def load(cls, main: Path, root: Path) -> Source:
        doc = tex_loader.assemble(main)
        text = "\n".join(tex_loader.COMMENT_RE.sub("", line) for line in doc.lines)
        starts = [0] + [index + 1 for index, char in enumerate(text) if char == "\n"]
        prefix = main.parent.relative_to(root).as_posix()
        return cls(doc=doc, text=text, line_starts=starts, prefix=prefix)

    def origin(self, offset: int) -> str:
        """``<file relative to the thesis root>:<line>`` for an offset in ``text``."""
        rel, line = self.doc.origin(bisect.bisect_right(self.line_starts, offset))
        return f"{self.root_rel(rel)}:{line}"

    def root_rel(self, rel: str) -> str:
        return rel if self.prefix == "." else posixpath.normpath(f"{self.prefix}/{rel}")


@dataclass
class Env:
    name: str
    start: int
    body_start: int
    body_end: int
    end: int


def pair_environments(text: str) -> list[Env]:
    """All ``\\begin``/``\\end`` pairs, sorted by start offset."""
    stack: list[tuple[str, int, int]] = []
    pairs: list[Env] = []
    for match in ENV_TOKEN_RE.finditer(text):
        kind, name = match.group(1), match.group(2).strip()
        if kind == "begin":
            stack.append((name, match.start(), match.end()))
            continue
        for index in range(len(stack) - 1, -1, -1):
            if stack[index][0] == name:
                _, start, body_start = stack[index]
                del stack[index:]
                pairs.append(Env(name, start, body_start, match.start(), match.end()))
                break
    pairs.sort(key=lambda env: env.start)
    return pairs


@dataclass
class Warnings:
    items: list[dict[str, str | None]] = field(default_factory=list)

    def add(self, code: str, message: str, source: str | None = None) -> None:
        self.items.append({"code": code, "message": message, "source": source})


# ---------------------------------------------------------------------------
# Main file, metadata, macros
# ---------------------------------------------------------------------------


def select_main(root: Path, main: str | None, warnings: Warnings) -> Path:
    if main:
        path = root / main
        if not path.is_file():
            raise ExtractError(f"主文件不存在：{main}")
        return path.resolve()
    candidates = []
    for path in sorted(root.glob("*.tex")):
        text = strip_comments(tex_loader.read_text_robust(path)[0])
        if "\\documentclass" in text and re.search(r"\\begin\s*\{document\}", text):
            candidates.append(path)
    if not candidates:
        raise ExtractError(
            "论文根目录下没有同时含 \\documentclass 与 \\begin{document} 的 .tex 文件"
        )
    if len(candidates) == 1:
        return candidates[0]
    kept = [path for path in candidates if not BLIND_RE.search(path.stem)]
    names = "、".join(path.name for path in candidates)
    if len(kept) == 1:
        warnings.add(
            "W-MAIN", f"存在多个主文件候选（{names}），已选择 {kept[0].name}；可用 --main 指定"
        )
        return kept[0]
    raise ExtractError(f"存在多个主文件候选（{names}），请用 --main 指定")


def extract_meta(preamble: str, warnings: Warnings) -> tuple[dict[str, object], str]:
    meta: dict[str, object] = {}
    title = command_args(preamble, "title", 2)
    meta["title_zh"] = plain_text(title[0]) if title else ""
    meta["title_en"] = plain_text(title[1]) if len(title) > 1 else ""
    for name in ("author", "school", "subject", "date"):
        args = command_args(preamble, name, 2)
        meta[name] = plain_text(args[0]) if args else ""
    supervisor = command_args(preamble, "supervisor", 4)
    meta["supervisor"] = plain_text(supervisor[0]) if supervisor else ""
    meta["supervisor_title"] = plain_text(supervisor[1]) if len(supervisor) > 1 else ""

    lines: list[str] = []
    match = TITLE_LINES_RE.search(preamble)
    if match:
        try:
            pos = match.end()
            while True:
                optional, next_pos = read_optional(preamble, pos)
                if optional is None:
                    break
                pos = next_pos
            body, _ = read_group(preamble, skip_ws(preamble, pos))
            parts = re.split(r"\\\\(?:\s*\[[^\]]*\])?", body)
            lines = [line for line in (plain_text(part) for part in parts) if line]
        except ValueError:
            lines = []
    meta["title_lines"] = lines or ([meta["title_zh"]] if meta["title_zh"] else [])

    for name in META_FIELDS:
        if not meta[name]:
            warnings.add("W-META", f"缺少封面字段 {name}，请在规划 meta 中补全")

    documentclass = re.search(r"\\documentclass\s*(?:\[([^\]]*)\])?", preamble)
    options = (documentclass.group(1) or "") if documentclass else ""
    if re.search(r"(?i)doctor|phd", options):
        degree = "doctor"
    elif re.search(r"(?i)master", options):
        degree = "master"
    else:
        degree = "unknown"
    return meta, degree


def extract_macros(source: Source, preamble_end: int) -> list[dict[str, str]]:
    """Preamble macro definitions; build_deck.py copies the ones that the deck uses."""
    preamble = source.text[:preamble_end]
    macros: list[dict[str, str]] = []
    pos = 0
    while True:
        match = MACRO_DEF_RE.search(preamble, pos)
        if not match:
            break
        pos = match.end()
        try:
            cursor = skip_ws(preamble, match.end())
            if match.group(1) == "def":
                name_match = re.match(r"\\([A-Za-z@]+)", preamble[cursor:])
                if not name_match:
                    continue
                params_end = cursor + name_match.end()
                brace = preamble.find("{", params_end)
                if brace < 0 or not re.fullmatch(r"[#0-9\s]*", preamble[params_end:brace]):
                    continue
                _, end = read_group(preamble, brace)
            else:
                if preamble.startswith("{", cursor):
                    inner, cursor = read_group(preamble, cursor)
                    name_match = re.fullmatch(r"\s*\\([A-Za-z@]+)\s*", inner)
                else:
                    name_match = re.match(r"\\([A-Za-z@]+)", preamble[cursor:])
                    cursor += name_match.end() if name_match else 0
                if not name_match:
                    continue
                if match.group(1) != "DeclareMathOperator":
                    for _ in range(2):
                        _, cursor = read_optional(preamble, cursor)
                _, end = read_group(preamble, skip_ws(preamble, cursor))
        except ValueError:
            continue
        macros.append(
            {
                "name": name_match.group(1),
                "command": match.group(1) + match.group(2),
                "definition": preamble[match.start() : end],
                "source": source.origin(match.start()),
            }
        )
        pos = end
    return macros


def graphicspath_entries(text: str) -> list[str]:
    entries: list[str] = []
    for match in re.finditer(r"(?<!\\)\\graphicspath(?![A-Za-z@])", text):
        try:
            outer, _ = read_group(text, skip_ws(text, match.end()))
        except ValueError:
            continue
        pos = 0
        while True:
            start = skip_ws(outer, pos)
            if start >= len(outer) or outer[start] != "{":
                break
            entry, pos = read_group(outer, start)
            entry = entry.strip()
            if entry and entry not in entries:
                entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# Chapter tree
# ---------------------------------------------------------------------------


@dataclass
class Span:
    number: str
    start: int
    entry: dict[str, object]


@dataclass
class ChapterSpan:
    number: int
    start: int
    end: int
    entry: dict[str, object]
    sections: list[Span] = field(default_factory=list)
    subsections: list[Span] = field(default_factory=list)


def section_kind(title: str) -> str:
    if any(word in title for word in ("引言", "概述")):
        return "intro"
    if any(word in title for word in ("问题描述", "问题定义", "问题建模")):
        return "problem"
    if any(word in title for word in ("实验", "仿真", "案例", "结果")):
        return "experiment"
    if "小结" in title:
        return "summary"
    return "method"


def suggest_role(chapter: ChapterSpan, count: int) -> tuple[str, str]:
    """Role hints of references/defense-framework.md, applied in table row order."""
    title = str(chapter.entry["title"])
    if chapter.number == 1:
        return "intro", "第 1 章"
    for word in ("绪论", "引言"):
        if word in title:
            return "intro", f"章题含「{word}」"
    for word in ("结论", "总结与展望"):
        if word in title:
            return "conclusion", f"章题含「{word}」"
    for place in ("系统", "平台"):
        for action in ("设计", "应用", "实现"):
            if place in title and action in title:
                return "application", f"章题含「{place}」与「{action}」"
    headings = [str(span.entry["title"]) for span in chapter.sections + chapter.subsections]
    words = ("实验", "案例", "结果分析", "仿真")
    if chapter.number != count and not any(w in h for h in headings for w in words):
        return "foundation", "不是第 1 章或最后一章，节题不含「实验」「案例」「结果分析」「仿真」"
    return "research", "其余章"


def build_chapter_tree(source: Source, body_start: int, body_end: int) -> list[ChapterSpan]:
    text = source.text
    stop = body_end
    chapters: list[ChapterSpan] = []
    current: ChapterSpan | None = None
    for match in STRUCTURE_RE.finditer(text, body_start, body_end):
        kind, star = match.group(1), match.group(2)
        if kind in ("appendix", "backmatter"):
            stop = match.start()
            break
        if kind == "chapter" and current is not None:
            current.end = match.start()
            current = None
        if star:
            continue
        try:
            short, pos = read_optional(text, match.end())
            title, _ = read_group(text, skip_ws(text, pos))
        except ValueError:
            continue
        entry: dict[str, object] = {
            "title": plain_text(title),
            "short_title": plain_text(short) if short else None,
            "source": source.origin(match.start()),
        }
        if kind == "chapter":
            number = len(chapters) + 1
            current = ChapterSpan(number, match.start(), stop, {"number": number, **entry})
            chapters.append(current)
        elif current is None:
            continue
        elif kind == "section":
            number = f"{current.number}.{len(current.sections) + 1}"
            kind_hint = section_kind(str(entry["title"]))
            entry = {"number": number, **entry, "kind": kind_hint, "subsections": []}
            current.sections.append(Span(number, match.start(), entry))
        elif current.sections:
            parent = current.sections[-1]
            children = parent.entry["subsections"]
            assert isinstance(children, list)
            number = f"{parent.number}.{len(children) + 1}"
            entry = {"number": number, **entry}
            children.append(entry)
            current.subsections.append(Span(number, match.start(), entry))
    if current is not None:
        current.end = stop
    for chapter in chapters:
        role, evidence = suggest_role(chapter, len(chapters))
        chapter.entry["role_suggestion"] = role
        chapter.entry["role_evidence"] = evidence
        chapter.entry["sections"] = [span.entry for span in chapter.sections]
    return chapters


def locate(chapters: list[ChapterSpan], offset: int) -> tuple[int, str | None, str | None] | None:
    for chapter in chapters:
        if not chapter.start <= offset < chapter.end:
            continue
        section = next((s for s in reversed(chapter.sections) if s.start <= offset), None)
        subsection = None
        if section is not None:
            subsection = next(
                (
                    s
                    for s in reversed(chapter.subsections)
                    if section.start <= s.start <= offset
                    and s.number.startswith(f"{section.number}.")
                ),
                None,
            )
        return (
            chapter.number,
            section.number if section else None,
            subsection.number if subsection else None,
        )
    return None


# ---------------------------------------------------------------------------
# Floats and equations
# ---------------------------------------------------------------------------


def load_aux_numbers(root: Path) -> dict[str, str]:
    """``\\newlabel`` numbers from every ``*.aux`` under the thesis root.

    Hidden directories (``.git`` and similar) are skipped. Shallower files win
    when two files define the same label.
    """
    files = [
        path
        for path in root.rglob("*.aux")
        if not any(part.startswith(".") for part in path.relative_to(root).parts[:-1])
    ]
    files.sort(key=lambda path: (len(path.relative_to(root).parts), path.as_posix()))
    numbers: dict[str, str] = {}
    for path in files:
        text = tex_loader.read_text_robust(path)[0]
        for match in re.finditer(r"\\newlabel\s*(?=\{)", text):
            try:
                label, pos = read_group(text, match.end())
                data, _ = read_group(text, skip_ws(text, pos))
                number, _ = read_group(data, skip_ws(data, 0))
            except ValueError:
                continue
            number = number.replace("\\relax", "").strip()
            if label.startswith("sub@") or not number:
                continue
            numbers.setdefault(label, number)
    return numbers


def number_separator(aux: dict[str, str]) -> str:
    for number in aux.values():
        match = re.fullmatch(r"\d+([-.])\d+", number)
        if match:
            return match.group(1)
    return "-"


def inside(offset: int, regions: list[tuple[int, int]]) -> bool:
    return any(start <= offset < end for start, end in regions)


def first_caption(text: str, start: int, end: int, excluded: list[tuple[int, int]]) -> str | None:
    for match in CAPTION_RE.finditer(text, start, end):
        if inside(match.start(), excluded):
            continue
        try:
            _, pos = read_optional(text, match.end())
            caption, _ = read_group(text, skip_ws(text, pos))
        except ValueError:
            return None
        return clean_caption(caption)
    return None


def first_label(text: str, start: int, end: int, excluded: list[tuple[int, int]]) -> str | None:
    for match in LABEL_RE.finditer(text, start, end):
        if not inside(match.start(), excluded):
            return match.group(1).strip()
    return None


def graphics_paths(text: str, start: int, end: int) -> list[tuple[str, int]]:
    paths: list[tuple[str, int]] = []
    for match in INCLUDEGRAPHICS_RE.finditer(text, start, end):
        try:
            _, pos = read_optional(text, match.end())
            path, _ = read_group(text, skip_ws(text, pos))
        except ValueError:
            continue
        paths.append((path.strip(), match.start()))
    return paths


def resolve_image(root: Path, base: Path, graphicspath: list[str], raw: str) -> tuple[str, bool]:
    """Resolve an ``\\includegraphics`` path the way graphicx searches it.

    ``base`` is the main file directory. The result is relative to the thesis root.
    """
    has_extension = Path(raw).suffix.lower() in IMAGE_EXTENSIONS
    directories = [*graphicspath, ""]

    def rel(path: str) -> str:
        return os.path.relpath(os.path.normpath(path), root).replace("\\", "/")

    for directory in directories:
        candidate_base = os.path.join(base, directory, raw)
        candidates = (
            [candidate_base]
            if has_extension
            else [candidate_base + ext for ext in IMAGE_EXTENSIONS]
        )
        for candidate in candidates:
            if os.path.isfile(candidate):
                return rel(candidate), True
    return rel(os.path.join(base, directories[0], raw)), False


def subfigure_regions(text: str, env: Env, envs: list[Env]) -> list[dict[str, object]]:
    regions: list[dict[str, object]] = []
    for match in SUBCAPTIONBOX_RE.finditer(text, env.body_start, env.body_end):
        try:
            _, pos = read_optional(text, match.end())
            caption, pos = read_group(text, skip_ws(text, pos))
            for _ in range(2):
                _, pos = read_optional(text, pos)
            _, end = read_group(text, skip_ws(text, pos))
        except ValueError:
            continue
        regions.append(
            {
                "start": match.start(),
                "end": end,
                "star": bool(match.group(1)),
                "caption": clean_caption(caption),
            }
        )
    for inner in envs:
        if inner.name == "subfigure" and env.body_start <= inner.start < env.body_end:
            caption = first_caption(text, inner.body_start, inner.body_end, [])
            regions.append(
                {"start": inner.start, "end": inner.end, "star": False, "caption": caption or ""}
            )
    regions.sort(key=lambda region: int(str(region["start"])))
    return regions


def split_rows(body: str) -> list[str]:
    """Split an equation body at top-level ``\\\\`` (outside braces and inner environments)."""
    rows: list[str] = []
    depth = 0
    env_depth = 0
    start = 0
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\":
            word = re.match(r"\\(begin|end)(?![A-Za-z@])", body[index : index + 7])
            if word:
                env_depth += 1 if word.group(1) == "begin" else -1
                index += word.end()
                continue
            if body.startswith("\\\\", index) and depth == 0 and env_depth == 0:
                rows.append(body[start:index])
                index += 2
                start = index
                continue
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        index += 1
    rows.append(body[start:])
    return rows


@dataclass
class Numbering:
    aux: dict[str, str]
    separator: str
    counters: dict[tuple[int, str], int] = field(default_factory=dict)

    def next(self, chapter: int, kind: str) -> str:
        key = (chapter, kind)
        self.counters[key] = self.counters.get(key, 0) + 1
        return f"{chapter}{self.separator}{self.counters[key]}"

    def resolve(self, label: str | None, computed: str) -> tuple[str, str]:
        if label and label in self.aux:
            return self.aux[label], "aux"
        return computed, "computed"


@dataclass
class Context:
    source: Source
    envs: list[Env]
    chapters: list[ChapterSpan]
    numbering: Numbering
    root: Path
    base: Path
    graphicspath: list[str]
    warnings: Warnings


def figure_fields(ctx: Context, env: Env, regions: list[dict[str, object]], number: str) -> dict:
    text = ctx.source.text
    files = []
    for raw, offset in graphics_paths(text, env.body_start, env.body_end):
        resolved, exists = resolve_image(ctx.root, ctx.base, ctx.graphicspath, raw)
        files.append({"path": raw, "resolved": resolved, "exists": exists})
        if not exists:
            ctx.warnings.add("W-FIG-FILE", f"图片文件不存在：{raw}", ctx.source.origin(offset))
    subfigures = []
    letter_index = 0
    for region in regions:
        start, end = int(str(region["start"])), int(str(region["end"]))
        letter = None
        if not region["star"]:
            letter = chr(ord("a") + letter_index)
            letter_index += 1
        sub_label = first_label(text, start, end, [])
        sub_number = None
        if letter:
            sub_number, _ = ctx.numbering.resolve(sub_label, f"{number}({letter})")
        paths = graphics_paths(text, start, end)
        subfigures.append(
            {
                "letter": letter,
                "caption": region["caption"],
                "file": paths[0][0] if paths else None,
                "label": sub_label,
                "number": sub_number,
            }
        )
    return {"files": files, "subfigures": subfigures}


def extract_floats(ctx: Context) -> dict[str, list[dict[str, object]]]:
    text = ctx.source.text
    found: dict[str, list[dict[str, object]]] = {"fig": [], "tab": [], "alg": []}
    for env in ctx.envs:
        kind = FLOAT_KINDS.get(env.name)
        place = locate(ctx.chapters, env.start) if kind else None
        if kind is None or place is None:
            continue
        chapter, section, subsection = place
        regions = subfigure_regions(text, env, ctx.envs) if kind == "fig" else []
        excluded = [(int(str(r["start"])), int(str(r["end"]))) for r in regions]
        caption = first_caption(text, env.body_start, env.body_end, excluded)
        if caption is None:
            continue
        computed = ctx.numbering.next(chapter, kind)
        label = first_label(text, env.body_start, env.body_end, excluded)
        number, number_source = ctx.numbering.resolve(label, computed)
        index = computed.rsplit(ctx.numbering.separator, 1)[-1]
        entry: dict[str, object] = {
            "label": label or f"auto:{kind}:{chapter}-{index}",
            "number": number,
            "number_source": number_source,
            "caption": caption,
            "chapter": chapter,
            "section": section,
            "subsection": subsection,
        }
        if kind == "fig":
            entry.update(figure_fields(ctx, env, regions, number))
        elif kind == "tab":
            body = next(
                (
                    text[inner.start : inner.end]
                    for inner in ctx.envs
                    if inner.name in TABULAR_ENVS and env.body_start <= inner.start < env.body_end
                ),
                None,
            )
            if body is None:
                ctx.warnings.add(
                    "W-TABLE-BODY",
                    f"表 {number} 中未找到 tabular 类环境",
                    ctx.source.origin(env.start),
                )
            entry["tabular_source"] = body
        entry["source"] = ctx.source.origin(env.start)
        found[kind].append(entry)
    return found


def extract_equations(ctx: Context) -> list[dict[str, object]]:
    text = ctx.source.text
    equations: list[dict[str, object]] = []
    for env in ctx.envs:
        place = locate(ctx.chapters, env.start) if env.name in EQUATION_ENVS else None
        if place is None:
            continue
        chapter, section, subsection = place
        body = text[env.body_start : env.body_end]
        rows = [body] if env.name in SINGLE_ROW_ENVS else split_rows(body)
        labels: list[dict[str, str]] = []
        for row in rows:
            row_labels = [match.group(1).strip() for match in LABEL_RE.finditer(row)]
            if not row.strip():
                continue
            tag = TAG_RE.search(row)
            if NOTAG_RE.search(row):
                computed = None
            elif tag:
                computed = tag.group(1).strip()
            else:
                computed = ctx.numbering.next(chapter, "eq")
            for label in row_labels:
                if computed is None and label not in ctx.numbering.aux:
                    continue
                number, number_source = ctx.numbering.resolve(label, computed or "")
                labels.append({"label": label, "number": number, "number_source": number_source})
        if not labels:
            continue
        equations.append(
            {
                "label": labels[0]["label"],
                "number": labels[0]["number"],
                "number_source": labels[0]["number_source"],
                "labels": labels,
                "env": env.name,
                "tex": body,
                "chapter": chapter,
                "section": section,
                "subsection": subsection,
                "source": ctx.source.origin(env.start),
            }
        )
    return equations


# ---------------------------------------------------------------------------
# Publications and conclusion
# ---------------------------------------------------------------------------


def achievement_block(text: str, envs: list[Env], body_start: int) -> str | None:
    match = re.search(r"(?<!\\)\\achievement(?![A-Za-z@])\s*(?=\{)", text)
    if match:
        try:
            return read_group(text, match.end())[0]
        except ValueError:
            pass
    for env in envs:
        if env.name == "achievements":
            return text[env.body_start : env.body_end]
    for match in re.finditer(r"(?<!\\)\\chapter(?![A-Za-z@])\*?", text[body_start:]):
        start = body_start + match.end()
        try:
            _, pos = read_optional(text, start)
            title, pos = read_group(text, skip_ws(text, pos))
        except ValueError:
            continue
        if "成果" in title or "发表的学术论文" in title:
            following = re.search(r"(?<!\\)\\chapter(?![A-Za-z@])|\\end\s*\{document\}", text[pos:])
            return text[pos : pos + following.start()] if following else text[pos:]
    return None


def extract_publications(text: str, envs: list[Env], body_start: int) -> list[dict[str, object]]:
    block = achievement_block(text, envs, body_start)
    if block is None:
        return []
    token_re = re.compile(
        r"\\(achievementcategory|section|item)(?![A-Za-z@])\*?"
        r"|\\end\s*\{(?:enumerate|itemize|description)\}"
    )
    publications: list[dict[str, object]] = []
    category = ""
    item_start: int | None = None

    def close(end: int) -> None:
        if item_start is None:
            return
        raw = plain_text(block[item_start:end])
        content = strip_chapter_marks(raw)
        if content:
            publications.append(
                {
                    "id": f"P{len(publications) + 1}",
                    "category": category,
                    "text": content,
                    "chapters": parse_chapter_marks(raw),
                }
            )

    for match in token_re.finditer(block):
        close(match.start())
        item_start = None
        name = match.group(1)
        if name in ("achievementcategory", "section"):
            with contextlib.suppress(ValueError):
                category = plain_text(read_group(block, skip_ws(block, match.end()))[0])
        elif name == "item":
            try:
                item_start = read_optional(block, match.end())[1]
            except ValueError:
                item_start = match.end()
    close(len(block))
    return publications


def conclusion_units(body: str) -> list[tuple[str, str]]:
    """Split a chapter body into (kind, text) units: heading, item, or paragraph."""
    units: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    list_depth = 0
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            if list_depth == 0:
                current = None
            continue
        heading = HEADING_RE.match(stripped)
        if heading:
            units.append(("heading", [heading.group(1)]))
            current = None
            continue
        for pattern, step in ((LIST_BEGIN_RE, 1), (LIST_END_RE, -1)):
            marker = pattern.match(stripped)
            if marker:
                list_depth += step
                if list_depth <= 0:
                    current = None
                stripped = stripped[marker.end() :].strip()
        if not stripped:
            continue
        item = re.match(r"\\item(?![A-Za-z@])\s*(?:\[[^\]]*\])?", stripped)
        numbered = NUMBERED_ITEM_RE.match(unicodedata.normalize("NFKC", stripped))
        if item and list_depth <= 1:
            current = [stripped[item.end() :]]
            units.append(("item", current))
        elif numbered and list_depth == 0:
            current = [stripped]
            units.append(("item", current))
        elif current is None:
            current = [stripped]
            units.append(("para", current))
        else:
            current.append(stripped)
    return [(kind, plain_text(" ".join(parts))) for kind, parts in units]


def extract_conclusion(text: str, chapter: ChapterSpan | None) -> dict[str, object]:
    result: dict[str, object] = {
        "chapter": chapter.number if chapter else None,
        "contributions": [],
        "outlook": [],
    }
    if chapter is None:
        return result
    body = text[chapter.start : chapter.end]
    try:
        _, pos = read_optional(body, len("\\chapter"))
        body = body[read_group(body, skip_ws(body, pos))[1] :]
    except ValueError:
        pass
    in_outlook = False
    contributions: list[str] = []
    outlook: list[str] = []
    for kind, content in conclusion_units(body):
        if kind != "item":
            if any(word in content for word in OUTLOOK_KEYWORDS):
                in_outlook = True
            continue
        content = ITEM_NUMBER_PREFIX_RE.sub("", content).strip()
        if content:
            (outlook if in_outlook else contributions).append(content)
    result["contributions"] = contributions
    result["outlook"] = outlook
    return result


def find_logo(root: Path, base: Path, graphicspath: list[str], warnings: Warnings) -> str | None:
    matches: list[str] = []
    for directory in graphicspath or [""]:
        folder = base / directory
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if (
                path.is_file()
                and path.suffix.lower() in IMAGE_EXTENSIONS
                and LOGO_RE.search(path.stem)
            ):
                matches.append(os.path.relpath(path, root).replace("\\", "/"))
    if len(matches) == 1:
        return matches[0]
    if matches:
        warnings.add(
            "W-LOGO", f"找到多个校徽候选（{'、'.join(matches)}），请在规划 meta.logo 中指定"
        )
    else:
        warnings.add(
            "W-LOGO", "未在 graphicspath 目录中找到校徽文件，可用 build_deck.py --logo 指定"
        )
    return None


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------


def extract_inventory(thesis: Path, main: str | None = None) -> dict[str, object]:
    """Build the inventory dict. Raises ExtractError when the main file is missing or ambiguous."""
    root = Path(thesis).resolve()
    if not root.is_dir():
        raise ExtractError(f"论文目录不存在：{thesis}")
    warnings = Warnings()
    main_path = select_main(root, main, warnings)
    source = Source.load(main_path, root)
    for message in source.doc.warnings:
        warnings.add("W-ENCODING", message)
    for raw, rel, line in source.doc.missing:
        warnings.add("W-INCLUDE", f"未找到 include 文件：{raw}", f"{source.root_rel(rel)}:{line}")

    text = source.text
    begin = re.search(r"\\begin\s*\{document\}", text)
    if begin is None:
        raise ExtractError(f"主文件缺少 \\begin{{document}}：{main_path.name}")
    end = re.search(r"\\end\s*\{document\}", text[begin.end() :])
    body_start = begin.end()
    body_end = body_start + end.start() if end else len(text)

    meta, degree = extract_meta(text[: begin.start()], warnings)
    graphicspath = graphicspath_entries(text)
    envs = pair_environments(text)
    chapters = build_chapter_tree(source, body_start, body_end)
    aux = load_aux_numbers(root)
    ctx = Context(
        source=source,
        envs=envs,
        chapters=chapters,
        numbering=Numbering(aux=aux, separator=number_separator(aux)),
        root=root,
        base=main_path.parent,
        graphicspath=graphicspath,
        warnings=warnings,
    )
    floats = extract_floats(ctx)
    equations = extract_equations(ctx)
    publications = extract_publications(text, envs, body_start)
    if not publications:
        warnings.add("W-PUB", "未找到成果列表或其中没有条目；「论文」框将为空")
    conclusion_chapters = [c for c in chapters if c.entry["role_suggestion"] == "conclusion"]
    conclusion = extract_conclusion(text, conclusion_chapters[-1] if conclusion_chapters else None)
    if not conclusion_chapters:
        warnings.add("W-CONCLUSION", "未识别出结论章；创新点与展望条目为空")

    return {
        "thesis_root": root.as_posix(),
        "main_tex": main_path.relative_to(root).as_posix(),
        "degree": degree,
        "meta": meta,
        "logo": find_logo(root, main_path.parent, graphicspath, warnings),
        "graphicspath": graphicspath,
        "chapters": [chapter.entry for chapter in chapters],
        "figures": floats["fig"],
        "tables": floats["tab"],
        "equations": equations,
        "algorithms": floats["alg"],
        "publications": publications,
        "conclusion": conclusion,
        "macros": extract_macros(source, begin.start()),
        "warnings": warnings.items,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="只读提取中文学位论文 LaTeX 仓库的答辩稿清单（inventory.json）。"
    )
    parser.add_argument("--thesis", required=True, help="论文仓库根目录")
    parser.add_argument("--main", help="主文件（相对 --thesis）；有多个候选时必须指定")
    parser.add_argument("--out", required=True, help="输出的 inventory.json 路径")
    parser.add_argument("--json", action="store_true", help="在标准输出打印计数与 warnings 摘要")
    args = parser.parse_args(argv)

    try:
        inventory = extract_inventory(Path(args.thesis), args.main)
    except ExtractError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    conclusion = inventory["conclusion"]
    warnings = inventory["warnings"]
    assert isinstance(conclusion, dict) and isinstance(warnings, list)
    counts: dict[str, int] = {}
    for name in ("chapters", "figures", "tables", "equations", "algorithms", "publications"):
        items = inventory[name]
        assert isinstance(items, list)
        counts[name] = len(items)
    counts["contributions"] = len(conclusion["contributions"])
    counts["outlook"] = len(conclusion["outlook"])
    if args.json:
        summary = {"inventory": str(out), "counts": counts, "warnings": warnings}
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        described = "，".join(f"{name} {value}" for name, value in counts.items())
        print(f"已写入 {out}：{described}；warnings {len(warnings)} 条")
        for warning in warnings:
            location = f"（{warning['source']}）" if warning.get("source") else ""
            print(f"  {warning['code']}: {warning['message']}{location}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
