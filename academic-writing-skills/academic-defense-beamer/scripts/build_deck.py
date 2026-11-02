#!/usr/bin/env python3
"""
Build the defense deck for academic-defense-beamer (Beamer or Typst Touying).

The script checks slide_plan.yaml against inventory.json, then writes defense.tex,
defense-notes.tex, notes.md, thesis-macros.tex, build_manifest.json, and the three
theme files into the output directory. Figures stay in the thesis repository: the
deck finds them through a relative graphicspath. Equation and table bodies come
from the inventory source text. The script escapes all plain text fields. Each
frame carries its speaker note (\\DefenseNote); defense-notes.tex compiles the
presenter build defense-notes.pdf with the notes on the right half of each page.

When the plan sets deck.backend: touying, the script writes defense.typ for the
simply-ysu-touying theme instead, copies the planned thesis images into img/,
and compiles with typst (defense-notes.pdf adds a notes:N page after each slide).

Field and transformation rules: references/plan-schema.md; presenting:
references/presenting.md; Touying: references/touying-backend.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/build_deck.py --plan slide_plan.yaml \
        --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile] \
        [--no-notes-pdf] [--typst-package SPEC] [--typst-package-path DIR] \
        [--font-path DIR]

Exit codes: 0 success; 2 input error; 4 an output file exists and --force is
absent; 5 compile failure; 6 a Typst package is not installed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import jinja2
import yaml

try:
    import extract_thesis
    import tex_loader
    import typst_backend
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import extract_thesis
    import tex_loader
    import typst_backend

SKILL_DIR = Path(__file__).resolve().parent.parent
JINJA_DIR = SKILL_DIR / "templates" / "jinja"
TYPST_DIR = SKILL_DIR / "templates" / "typst"
BEAMER_DIR = SKILL_DIR / "templates" / "beamer"
THEME_FILES = (
    "beamerthemeYanshanDefense.sty",
    "beamerthemeGenericDefense.sty",
    "defense-layouts.sty",
)
NOTES_TEX = "defense-notes.tex"
NOTES_PDF = "defense-notes.pdf"
OWNED_FILES = (
    "defense.tex",
    NOTES_TEX,
    "notes.md",
    "build_manifest.json",
    "thesis-macros.tex",
    *THEME_FILES,
)
TYPST_OWNED_FILES = ("defense.typ", "notes.md", "build_manifest.json")
THEMES = {"yanshan": "YanshanDefense", "generic": "GenericDefense"}
BACKENDS = ("beamer", "touying")
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
FRAME_ONLY_LAYOUTS = ("cover", "toc", "thanks")
SINGLE_FIGURE_LAYOUTS = ("figure", "figure-bullets", "figure-grid")
SHOWN_BY = {
    "bullets": (
        "bullets",
        "figure-bullets",
        "equations-figure",
        "cards",
        "paper-summary",
        "outlook",
    ),
    "figures": ("figure", "figure-bullets", "figure-grid", "equations-figure"),
    "equations": ("equations-figure",),
    "table": ("table",),
    "paper": ("paper-summary",),
}
FIXED_PACKAGES = (
    "amsmath",
    "amssymb",
    "mathtools",
    "bm",
    "booktabs",
    "multirow",
    "makecell",
    "tabularx",
    "array",
    "threeparttable",
    "siunitx",
    "adjustbox",
)
# Subfigure count -> (per row, minipage width, gap, height); references/slide-layouts.md.
GRID = {
    2: (2, "0.32", "0.08", "0.45"),
    3: (3, "0.3", "0.03", "0.45"),
    4: (2, "0.32", "0.08", "0.21"),
    5: (3, "0.3", "0.03", "0.21"),
    6: (3, "0.3", "0.03", "0.21"),
}
# longtable and xltabular do not compile inside \adjustbox (plan_deck.py skips them too).
LONG_TABLE_RE = re.compile(r"\\begin\s*\{(?:longtable|xltabular)\}")
PACKAGE_RE = re.compile(r"^[A-Za-z0-9-]+$")
FRAME_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
EMPHASIS_RE = re.compile(r"\*\*(.+?)\*\*")
ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
CN_NUMERALS = "一二三四五六七八九十"
EMPTY_NOTE = "无"


class BuildError(Exception):
    """Input error (exit code 2)."""


# ---------------------------------------------------------------------------
# Escaping and source transformations
# ---------------------------------------------------------------------------


def escape_plain(text: str) -> str:
    return "".join(ESCAPES.get(char, char) for char in text)


def tex_escape(value: object, emphasis: str = "DefenseHighlight") -> str:
    """Escape a plan text field; ``**word**`` becomes ``\\<emphasis>{word}``."""
    if value is None:
        return ""
    text = re.sub(r"\s+", " ", str(value)).strip()
    parts: list[str] = []
    pos = 0
    for match in EMPHASIS_RE.finditer(text):
        parts.append(escape_plain(text[pos : match.start()]))
        parts.append(f"\\{emphasis}{{" + escape_plain(match.group(1)) + "}")
        pos = match.end()
    parts.append(escape_plain(text[pos:]))
    return "".join(parts)


def item_text(value: object) -> str:
    """Escaped list item text; ``{}`` keeps a leading ``[`` or ``<`` out of ``\\item`` options."""
    text = tex_escape(value)
    return "{}" + text if text.startswith(("[", "<")) else text


def source_caption(prefix: str, caption: str) -> str:
    """Caption from thesis source; ``\\ref`` and citations resolve inside DefenseSource."""
    return prefix + "\\begin{DefenseSource}" + caption + "\\end{DefenseSource}"


def transform_equation(equation: dict) -> str:
    """Replace each ``\\label{x}`` with ``\\tag*{(<number of x>)}``; other characters stay.

    A row that already has ``\\tag``, a second label in a row, a label without a
    thesis number, and every label of ``eqnarray`` are removed without a tag.
    """
    numbers = {item["label"]: item["number"] for item in equation["labels"]}
    env = equation["env"]
    body = equation["tex"]
    rows = [body] if env in extract_thesis.SINGLE_ROW_ENVS else extract_thesis.split_rows(body)
    result = []
    for row in rows:
        tagged = env == "eqnarray" or bool(extract_thesis.TAG_RE.search(row))

        def replace(match: re.Match[str]) -> str:
            nonlocal tagged
            number = numbers.get(match.group(1).strip())
            if tagged or not number:
                return ""
            tagged = True
            return "\\tag*{(" + number + ")}"

        result.append(extract_thesis.LABEL_RE.sub(replace, row))
    return "\\\\".join(result)


select_macros = typst_backend.select_macros


def macro_line(macro: dict) -> str:
    definition = macro["definition"]
    if macro["command"].rstrip("*") in ("newcommand", "renewcommand", "providecommand"):
        return re.sub(
            r"^\\(?:newcommand|renewcommand|providecommand)", r"\\providecommand", definition
        )
    return f"\\ifdefined\\{macro['name']}\\else {definition}\\fi"


# ---------------------------------------------------------------------------
# Input and validation
# ---------------------------------------------------------------------------


def read_input(path: Path, kind: str) -> tuple[dict, bytes]:
    try:
        data = path.read_bytes()
        text = tex_loader.read_text_robust(path)[0]
        value = json.loads(text) if kind == "json" else yaml.safe_load(text)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise BuildError(f"无法读取 {path}：{exc}") from exc
    if not isinstance(value, dict):
        raise BuildError(f"{path} 的顶层不是映射")
    return value, data


class Lookup:
    """Inventory items by label or id."""

    def __init__(self, inventory: dict) -> None:
        self.figures = {item["label"]: item for item in inventory.get("figures", [])}
        self.tables = {item["label"]: item for item in inventory.get("tables", [])}
        self.equations = {
            item["label"]: equation
            for equation in inventory.get("equations", [])
            for item in equation["labels"]
        }
        self.papers = {item["id"]: item for item in inventory.get("publications", [])}


def validate_frame(frame: dict, name: str, lookup: Lookup) -> list[str]:
    errors = []
    role, layout = frame.get("role"), frame.get("layout")
    if role not in ROLES:
        errors.append(f"{name}：未知 role {role!r}")
    notes = frame.get("notes")
    if notes is not None and not isinstance(notes, dict):
        errors.append(f"{name}：notes 应为映射")
    elif notes:
        if notes.get("seconds") is not None and not isinstance(notes["seconds"], int):
            errors.append(f"{name}：notes.seconds 应为整数")
        if not isinstance(notes.get("questions") or [], list):
            errors.append(f"{name}：notes.questions 应为列表")
    if layout not in LAYOUTS:
        return errors + [f"{name}：未知 layout {layout!r}"]
    if layout == "toc" and not (isinstance(frame.get("chapter"), int) and frame["chapter"] >= 0):
        errors.append(f"{name}：目录帧的 chapter 应为 0 或章号")
    if layout in FRAME_ONLY_LAYOUTS:
        return errors
    if not isinstance(frame.get("bullets") or [], list):
        errors.append(f"{name}：bullets 应为列表")

    refs = frame.get("figures") or []
    if not isinstance(refs, list) or not all(isinstance(ref, dict) for ref in refs):
        errors.append(f"{name}：figures 应为映射列表，每项含 label")
        refs = []
    for ref in refs:
        label = ref.get("label")
        figure = lookup.figures.get(label) if isinstance(label, str) else None
        if figure is None:
            errors.append(f"{name}：图 {label!r} 不在清单中")
            continue
        letters = {sub["letter"]: sub for sub in figure["subfigures"] if sub.get("letter")}
        subfigures = ref.get("subfigures") or []
        if not isinstance(subfigures, list):
            errors.append(f"{name}：图 {label} 的 subfigures 应为字母列表")
            subfigures = []
        for letter in subfigures:
            if not isinstance(letter, str) or letter not in letters:
                errors.append(f"{name}：图 {label} 没有子图 {letter!r}")
            elif not letters[letter].get("file"):
                errors.append(f"{name}：图 {label} 的子图 {letter} 没有图片文件")
        width = ref.get("width")
        if width is not None and not (
            isinstance(width, (int, float)) and not isinstance(width, bool) and 0 < width <= 1
        ):
            errors.append(f"{name}：图 {label} 的 width 应为 0 到 1 之间的数")
        if layout != "figure-grid" and not figure["files"]:
            errors.append(f"{name}：图 {label} 没有图片文件")
    equations = frame.get("equations") or []
    if not isinstance(equations, list):
        errors.append(f"{name}：equations 应为列表")
        equations = []
    for ref in equations:
        label = ref.get("label") if isinstance(ref, dict) else ref
        if not isinstance(label, str) or label not in lookup.equations:
            errors.append(f"{name}：公式 {label!r} 不在清单中")
    table = frame.get("table")
    if table is not None:
        item = lookup.tables.get(table) if isinstance(table, str) else None
        if item is None:
            errors.append(f"{name}：表 {table!r} 不在清单中")
        elif layout == "table" and not item.get("tabular_source"):
            errors.append(f"{name}：表 {table} 没有表体源文本")
        elif layout == "table" and LONG_TABLE_RE.match(item["tabular_source"]):
            errors.append(f"{name}：表 {table} 的表体为 longtable 或 xltabular，不能放入缩放框")
    paper = frame.get("paper")
    if paper is not None and (not isinstance(paper, str) or paper not in lookup.papers):
        errors.append(f"{name}：成果 {paper!r} 不在清单中")

    if layout in SINGLE_FIGURE_LAYOUTS and len(refs) != 1:
        errors.append(f"{name}：版式 {layout} 需要 1 幅图")
    if layout == "figure-grid" and len(refs) == 1:
        subfigures = refs[0].get("subfigures") or []
        count = len(subfigures) if isinstance(subfigures, list) else 0
        if count not in GRID:
            errors.append(f"{name}：版式 figure-grid 需要 2–6 个子图字母，当前 {count} 个")
    if layout == "equations-figure":
        if not 1 <= len(equations) <= 4:
            errors.append(f"{name}：版式 equations-figure 需要 1–4 个公式")
        if len(refs) > 1:
            errors.append(f"{name}：版式 equations-figure 至多 1 幅图")
    if layout == "table" and table is None:
        errors.append(f"{name}：版式 table 需要 table 字段")
    return errors


def plan_backend(plan: dict) -> object:
    """deck.backend of the plan; a plan without it builds the Beamer deck."""
    deck = plan.get("deck")
    if isinstance(deck, dict):
        return deck.get("backend") or "beamer"
    return "beamer" if deck is None else f"deck={deck!r}（deck 应为含 backend 的映射）"


def validate(plan: dict, lookup: Lookup) -> list[str]:
    errors = []
    backend = plan_backend(plan)
    if backend not in BACKENDS:
        errors.append(f"deck.backend 应为 beamer 或 touying，当前 {backend!r}")
    meta = plan.get("meta")
    if not isinstance(meta, dict):
        errors.append("规划缺少 meta 映射")
        meta = {}
    if meta.get("stage") not in STAGES:
        errors.append(f"meta.stage 应为 predefense 或 defense，当前 {meta.get('stage')!r}")
    if meta.get("theme") not in THEMES:
        errors.append(f"meta.theme 应为 yanshan 或 generic，当前 {meta.get('theme')!r}")
    minutes = meta.get("minutes")
    if minutes is not None and not (isinstance(minutes, int) and minutes > 0):
        errors.append(f"meta.minutes 应为正整数，当前 {minutes!r}")
    if not isinstance(meta.get("title_lines") or [], list):
        errors.append("meta.title_lines 应为列表")
    chapters = meta.get("chapters")
    if chapters is not None and not (
        isinstance(chapters, list)
        and all(isinstance(c, dict) and "number" in c and "title" in c for c in chapters)
    ):
        errors.append("meta.chapters 应为映射列表，每项含 number 与 title")
    elif chapters and any(not isinstance(c.get("nav_label"), (str, type(None))) for c in chapters):
        errors.append("meta.chapters[].nav_label 应为字符串")
    if backend == "touying" and meta.get("theme") not in (None, "yanshan"):
        errors.append("Touying 后端只支持 meta.theme: yanshan")
    packages = meta.get("extra_packages") or []
    if not isinstance(packages, list):
        errors.append("meta.extra_packages 应为列表")
        packages = []
    for package in packages:
        if not isinstance(package, str) or not PACKAGE_RE.match(package):
            errors.append(f"meta.extra_packages 含非法宏包名 {package!r}")
    frames = plan.get("frames")
    if not isinstance(frames, list) or not frames:
        return errors + ["规划缺少 frames 列表"]
    seen: set[str] = set()
    for index, frame in enumerate(frames, 1):
        if not isinstance(frame, dict):
            errors.append(f"第 {index} 帧不是映射")
            continue
        frame_id = frame.get("id")
        if not isinstance(frame_id, str) or not FRAME_ID_RE.match(frame_id):
            errors.append(f"第 {index} 帧的 id 无效：{frame_id!r}")
        elif frame_id in seen:
            errors.append(f"帧 id 重复：{frame_id}")
        seen.add(str(frame_id))
        errors += validate_frame(frame, f"第 {index} 帧（{frame_id}）", lookup)
    return errors


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def relative_path(target: Path, out_dir: Path, warnings: list[str]) -> str:
    try:
        return os.path.relpath(target, out_dir).replace("\\", "/")
    except ValueError:
        warnings.append(f"{target.as_posix()} 与输出目录不在同一盘符，已写绝对路径")
        return target.as_posix()


def deck_graphicspath(inventory: dict, out_dir: Path, warnings: list[str]) -> list[str]:
    base = Path(inventory["thesis_root"]) / Path(inventory["main_tex"]).parent
    paths: list[str] = []
    for target in [base / entry for entry in inventory.get("graphicspath", [])] + [base]:
        path = relative_path(target, out_dir, warnings).rstrip("/") + "/"
        if path not in paths:
            paths.append(path)
    return paths


def figure_file(figure: dict, name: str, warnings: list[str]) -> str:
    if len(figure["files"]) > 1:
        warnings.append(f"{name}：图 {figure['label']} 含多个图片文件，只显示第一个")
    return figure["files"][0]["path"]


def frame_note(frame: dict) -> dict:
    """Arguments of \\DefenseNote: key point, script, transition, seconds (no questions).

    Empty fields stay empty; ``**word**`` becomes bold without the highlight color.
    """
    notes = frame.get("notes") or {}
    return {
        "key": tex_escape(notes.get("key"), "textbf"),
        "say": tex_escape(notes.get("say"), "textbf"),
        "transition": tex_escape(notes.get("transition"), "textbf"),
        "seconds": notes.get("seconds") or 0,
    }


def frame_context(frame: dict, name: str, lookup: Lookup, warnings: list[str]) -> dict:
    layout = frame["layout"]
    chapter = frame.get("chapter")
    context: dict = {
        "id": frame["id"],
        "role": frame["role"],
        "layout": layout,
        "chapter": "-" if chapter is None else str(chapter),
        "note": frame_note(frame),
    }
    if layout == "toc":
        context["toc"] = chapter
    if layout in FRAME_ONLY_LAYOUTS:
        return context
    for field_name, layouts in SHOWN_BY.items():
        if frame.get(field_name) and layout not in layouts:
            warnings.append(f"{name}：版式 {layout} 不显示 {field_name} 字段")

    bullets = list(frame.get("bullets") or [])
    context.update(
        {
            "title": tex_escape(frame.get("section")),
            "subsection": tex_escape(frame.get("subsection")),
            "takeaway": tex_escape(frame.get("takeaway")),
            "bullets": [item_text(bullet) for bullet in bullets],
            "position": "top" if frame.get("position") == "top" else "left",
            "figure": None,
            "grid": None,
            "equations": [],
            "table": None,
            "paper": None,
            "cards": [],
            "outlook": [],
        }
    )
    refs = frame.get("figures") or []
    if refs and layout in SHOWN_BY["figures"]:
        ref = refs[0]
        figure = lookup.figures[ref["label"]]
        caption = source_caption(f"图{escape_plain(figure['number'])}\\quad ", figure["caption"])
        context["figure"] = {"caption": caption, "width": ref.get("width"), "file": None}
        if layout == "figure-grid":
            letters = {sub["letter"]: sub for sub in figure["subfigures"] if sub.get("letter")}
            selected = [letters[letter] for letter in ref["subfigures"]]
            per_row, width, gap, height = GRID[len(selected)]
            cells = [
                {
                    "file": sub["file"],
                    "caption": source_caption(f"({sub['letter']}) ", sub["caption"]),
                }
                for sub in selected
            ]
            context["grid"] = {
                "cells": cells,
                "per_row": per_row,
                "width": width,
                "gap": gap,
                "height": height,
            }
        else:
            context["figure"]["file"] = figure_file(figure, name, warnings)
    if layout == "equations-figure":
        for ref in frame.get("equations") or []:
            equation = lookup.equations[ref["label"] if isinstance(ref, dict) else ref]
            numbers = ""
            if equation["env"] == "eqnarray":
                numbers = "\\quad ".join(f"({item['number']})" for item in equation["labels"])
            context["equations"].append(
                {
                    "env": equation["env"] + "*",
                    "body": transform_equation(equation),
                    "numbers": numbers,
                }
            )
    if layout == "table":
        table = lookup.tables[frame["table"]]
        context["table"] = {
            "caption": source_caption(
                f"表{escape_plain(table['number'])}\\quad ", table["caption"]
            ),
            "source": table["tabular_source"],
        }
    if layout == "paper-summary" and frame.get("paper"):
        context["paper"] = tex_escape(lookup.papers[frame["paper"]]["text"])
    if layout == "cards":
        for index, bullet in enumerate(bullets, 1):
            if frame["role"] == "challenges":
                label = "问题" + CN_NUMERALS[index - 1] if index <= 10 else f"问题 {index}"
            else:
                label = f"创新点 {index}"
            context["cards"].append({"label": label, "text": tex_escape(bullet)})
    if layout == "outlook":
        context["outlook"] = [
            {
                "label": "其" + CN_NUMERALS[index] if index < 10 else f"其 {index + 1}",
                "text": tex_escape(item),
            }
            for index, item in enumerate(bullets)
        ]
    return context


label_numbers = typst_backend.label_numbers


def deck_labels(inventory: dict) -> list[dict]:
    """Every thesis label with its number, for \\DefenseDefineLabel."""
    return [
        {"label": label, "number": escape_plain(number)}
        for label, number in label_numbers(inventory).items()
    ]


def frame_heading(frame: dict) -> str:
    if frame["layout"] == "cover":
        return "封面"
    if frame["layout"] == "thanks":
        return "致谢"
    if frame["layout"] == "toc":
        return f"第 {frame['chapter']} 章目录" if frame.get("chapter") else "目录"
    return re.sub(r"\s+", " ", str(frame.get("section") or "")).strip()


def note_value(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip() if value is not None else ""
    return text or EMPTY_NOTE


def render_notes(plan: dict) -> str:
    lines = ["# 答辩讲稿", ""]
    total = 0
    for index, frame in enumerate(plan["frames"], 1):
        notes = frame.get("notes") or {}
        seconds = notes.get("seconds") or 0
        total += seconds
        questions = "；".join(note_value(q) for q in notes.get("questions") or []) or EMPTY_NOTE
        lines += [
            f"## {index} {frame_heading(frame)}（{frame['id']}，{frame['role']}，{seconds} 秒）",
            "",
            f"- 说什么：{note_value(notes.get('say'))}",
            f"- 要点：{note_value(notes.get('key'))}",
            f"- 时长：{seconds} 秒",
            f"- 过渡：{note_value(notes.get('transition'))}",
            f"- 可能提问：{questions}",
            "",
        ]
    minutes = plan["meta"].get("minutes") or 40
    lines += [
        "## 合计",
        "",
        f"- 全部页秒数合计：{total} 秒",
        f"- 目标秒数：{60 * minutes} 秒（{minutes} 分钟）",
        "",
    ]
    return "\n".join(lines)


def render_macros(inventory: dict, plan: dict, lookup: Lookup) -> str:
    texts: list[str] = []
    for frame in plan["frames"]:
        if frame["layout"] in FRAME_ONLY_LAYOUTS:
            continue
        for ref in frame.get("figures") or []:
            figure = lookup.figures[ref["label"]]
            texts += [figure["caption"]] + [sub["caption"] or "" for sub in figure["subfigures"]]
        for ref in frame.get("equations") or []:
            texts.append(lookup.equations[ref["label"] if isinstance(ref, dict) else ref]["tex"])
        if frame.get("table"):
            table = lookup.tables[frame["table"]]
            texts += [table["caption"], table.get("tabular_source") or ""]
    lines = [
        "% thesis-macros.tex: generated by academic-defense-beamer scripts/build_deck.py.",
        "% Thesis preamble macros that the selected equations, tables, and captions use.",
        "% newcommand, renewcommand, and providecommand become providecommand. The other",
        "% definitions apply only when the name is not defined yet.",
    ]
    for macro in select_macros(inventory.get("macros", []), texts):
        lines += [f"% {macro.get('source', '')}", macro_line(macro)]
    return "\n".join(lines) + "\n"


def skill_version() -> str:
    skill_md = SKILL_DIR / "SKILL.md"
    if skill_md.is_file():
        match = re.search(
            r"^\s*version:\s*\"?([^\"\s]+)", skill_md.read_text(encoding="utf-8"), re.M
        )
        if match:
            return match.group(1)
    return "unknown"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def render(
    plan: dict,
    inventory: dict,
    lookup: Lookup,
    out_dir: Path,
    logo: str | None,
    digests: tuple[str, str],
    warnings: list[str],
    notes_pdf: bool = True,
) -> dict[str, bytes]:
    meta = plan["meta"]
    if meta.get("inventory_sha256") not in (None, digests[1]):
        warnings.append("规划的 inventory_sha256 与当前清单不一致；清单在规划后已更新")
    theme = THEMES[meta["theme"]]
    base = Path(inventory["thesis_root"])
    logo_path = ""
    if logo:
        logo_path = relative_path(Path(logo).resolve(), out_dir, warnings)
    elif meta.get("logo") or inventory.get("logo"):
        target = base / (meta.get("logo") or inventory["logo"])
        if not target.is_file():
            warnings.append(f"校徽文件不存在：{target.as_posix()}；封面显示文字标识")
        logo_path = relative_path(target, out_dir, warnings)
    lines = [str(line) for line in meta.get("title_lines") or [] if str(line).strip()]
    title = "\\\\".join(
        ("{}" + text if text.startswith(("[", "*")) else text)
        for text in (tex_escape(line) for line in lines)
    )
    supervisor = tex_escape(meta.get("supervisor"))
    if meta.get("supervisor_title"):
        supervisor += "\\quad " + tex_escape(meta["supervisor_title"])
    chapters = meta.get("chapters") or inventory.get("chapters", [])
    frames = []
    for index, frame in enumerate(plan["frames"], 1):
        frames.append(frame_context(frame, f"第 {index} 帧（{frame['id']}）", lookup, warnings))

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(JINJA_DIR), encoding="utf-8"),
        block_start_string="((*",
        block_end_string="*))",
        variable_start_string="(((",
        variable_end_string=")))",
        comment_start_string="((=",
        comment_end_string="=))",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        keep_trailing_newline=True,
        undefined=jinja2.StrictUndefined,
    )
    deck = env.get_template("deck.tex.j2").render(
        theme=theme,
        packages=list(FIXED_PACKAGES) + list(meta.get("extra_packages") or []),
        graphicspath=deck_graphicspath(inventory, out_dir, warnings),
        logo=logo_path,
        stage=meta["stage"],
        title=title,
        author=tex_escape(meta.get("author")),
        supervisor=supervisor,
        subject=tex_escape(meta.get("subject")),
        school=tex_escape(meta.get("school")),
        date=tex_escape(meta.get("date")),
        chapters=[
            {"number": chapter["number"], "title": tex_escape(chapter["title"])}
            for chapter in chapters
        ],
        labels=deck_labels(inventory),
        frames=frames,
    )
    files = {
        "defense.tex": deck.encode("utf-8"),
        NOTES_TEX: env.get_template("defense-notes.tex.j2").render().encode("utf-8"),
        "notes.md": render_notes(plan).encode("utf-8"),
        "thesis-macros.tex": render_macros(inventory, plan, lookup).encode("utf-8"),
    }
    for name in THEME_FILES:
        files[name] = (BEAMER_DIR / name).read_bytes()
    manifest = {
        "skill": "academic-defense-beamer",
        "version": skill_version(),
        "backend": "beamer",
        "notes_pdf": NOTES_PDF if notes_pdf else None,
        "theme": theme,
        "stage": meta["stage"],
        "frames": len(plan["frames"]),
        "plan_sha256": digests[0],
        "inventory_sha256": digests[1],
        "files": {name: sha256(data) for name, data in files.items()},
        "warnings": warnings,
    }
    files["build_manifest.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    return files


# ---------------------------------------------------------------------------
# Touying rendering (deck.backend: touying)
# ---------------------------------------------------------------------------

# Image height per layout when the plan gives no width; the slide body is 6.45 cm high.
TYPST_HEIGHTS = {
    "figure": "4.2cm",
    "figure-bullets-top": "2.3cm",
    "figure-bullets": "3.2cm",
    "equations-figure": "2.9cm",
}
TYPST_GRID_HEIGHTS = {"0.45": "2.9cm", "0.21": "1.35cm"}
RECAP_MAX = 3


def plain_text(value: object) -> str:
    return re.sub(r"\s+", " ", "" if value is None else str(value)).strip()


def optional_text(value: object, emphasis: str = "hl") -> str:
    """Typst expression of a text field; an empty string when the field is empty."""
    return typst_backend.ty_text(value, emphasis) if plain_text(value) else ""


def typst_note(frame: dict) -> str:
    """Markup of the speaker note: key point (bold), script, transition, and seconds.

    The questions stay in notes.md; ``**word**`` becomes bold without the highlight color.
    """
    notes = frame.get("notes") or {}
    parts = []
    if plain_text(notes.get("key")):
        parts.append(f"#strong({typst_backend.ty_text(notes['key'], 'strong')})")
    if plain_text(notes.get("say")):
        parts.append("#" + typst_backend.ty_text(notes["say"], "strong"))
    tail = ""
    if plain_text(notes.get("transition")):
        tail = "#" + typst_backend.ty_text(notes["transition"], "strong")
    seconds = int(notes.get("seconds") or 0)
    parts.append(tail + f'#h(1fr)#text(size: 12pt, "{seconds} 秒")')
    return "#parbreak()".join(parts)


def typst_math_texts(plan: dict, lookup: Lookup) -> list[str]:
    """LaTeX math that the Touying deck passes to mitex, for the macro selection."""
    texts: list[str] = []
    for frame in plan["frames"]:
        layout = frame["layout"]
        if layout in FRAME_ONLY_LAYOUTS:
            continue
        refs = frame.get("figures") or []
        if refs and layout in SHOWN_BY["figures"]:
            figure = lookup.figures[refs[0]["label"]]
            for caption in [figure["caption"]] + [s["caption"] for s in figure["subfigures"]]:
                texts += typst_backend.math_segments(caption or "")
        if layout == "equations-figure":
            for ref in frame.get("equations") or []:
                label = ref["label"] if isinstance(ref, dict) else ref
                texts.append(lookup.equations[label]["tex"])
        if layout == "table" and frame.get("table"):
            table = lookup.tables[frame["table"]]
            for text in (table["caption"], table.get("tabular_source")):
                texts += typst_backend.math_segments(text or "")
    return texts


class TypstRender:
    """State of one Touying render: thesis numbers, macro use, copied images, and errors."""

    def __init__(self, inventory: dict, lookup: Lookup, macros: bool, warnings: list[str]):
        self.inventory = inventory
        self.lookup = lookup
        self.macros = macros
        self.warnings = warnings
        self.numbers = label_numbers(inventory)
        self.images: dict[str, Path] = {}
        self.errors: list[str] = []
        meta_chapters = inventory.get("chapters", [])
        self.chapters = [
            {"number": c["number"], "title": c.get("short_title") or c["title"]}
            for c in meta_chapters
        ]

    def image(self, figure: dict, path: str, name: str) -> str:
        """String literal of the copied image path; records the copy and any problem."""
        item = next((f for f in figure["files"] if f.get("path") == path), None)
        resolved = str(item.get("resolved") or "") if item else ""
        if not resolved:
            self.errors.append(f"{name}：图 {figure['label']} 的图片 {path} 没有对应的论文文件")
            return typst_backend.ty_literal("")
        problem = typst_backend.image_problem(resolved)
        source = Path(self.inventory["thesis_root"]) / resolved
        if problem:
            self.errors.append(f"{name}：{problem}")
        elif not source.is_file():
            self.errors.append(f"{name}：图片文件不存在：{source.as_posix()}")
        target = typst_backend.image_target(resolved)
        self.images[target] = source
        return typst_backend.ty_literal(target)

    def caption(self, prefix: str, source: str | None, name: str, what: str) -> dict:
        """Number prefix (plain text) and caption source markup of a figure or table."""
        pieces, missing = typst_backend.latex_inline(source or "", self.numbers)
        if missing:
            self.warnings.append(
                f"{name}：{what}的题注含 Touying 后端不能转换的命令 "
                f"{'、'.join(dict.fromkeys(missing))}，按原文显示"
            )
        gap = "0.5em" if prefix.startswith("(") else "1em"
        return {
            "prefix": "#" + typst_backend.ty_literal(prefix) + f"#h({gap})",
            "caption": typst_backend.render_pieces(pieces, self.macros),
        }

    def cell(self, pieces: list) -> str:
        return "[" + typst_backend.render_pieces(pieces, self.macros) + "]"


def typst_size(ref: dict, height: str) -> str:
    width = ref.get("width")
    return f"width: {round(width * 100)}%" if width else f"height: {height}"


def typst_frame_context(
    frame: dict, name: str, render: TypstRender, chapters: list[dict], plan: dict
) -> dict:
    layout = frame["layout"]
    chapter = frame.get("chapter")
    context: dict = {
        "id": frame["id"],
        "role": frame["role"],
        "layout": layout,
        "chapter": "-" if chapter is None else str(chapter),
        "note": typst_note(frame),
        "skip_headings": [],
    }
    if layout == "toc":
        context["toc"] = chapter
        if chapter == 0:
            context["groups"] = outline_groups(chapters)
        else:
            title = next((c["title"] for c in chapters if c["number"] == chapter), None)
            context["heading"] = typst_backend.ty_text(title or f"第{chapter}章")
            args = []
            if plain_text(frame.get("takeaway")):
                args.append("question: " + typst_backend.ty_text(frame["takeaway"]))
            keywords = [b for b in frame.get("bullets") or [] if plain_text(b)][:3]
            if keywords:
                items = "".join(typst_backend.ty_text(k) + ", " for k in keywords)
                args.append(f"keywords: ({items})")
            context["opener"] = ", ".join(args)
    if layout == "thanks":
        innovation = next((f for f in plan["frames"] if f.get("role") == "innovation"), None)
        bullets = [b for b in (innovation or {}).get("bullets") or [] if plain_text(b)]
        context["recap"] = []
        if 1 <= len(bullets) <= RECAP_MAX:
            context["recap"] = [
                {"title": typst_backend.ty_str(f"创新点 {i}"), "body": typst_backend.ty_text(b)}
                for i, b in enumerate(bullets, 1)
            ]
    if layout in FRAME_ONLY_LAYOUTS:
        return context
    for field_name, layouts in SHOWN_BY.items():
        if frame.get(field_name) and layout not in layouts:
            render.warnings.append(f"{name}：版式 {layout} 不显示 {field_name} 字段")

    lookup = render.lookup
    bullets = list(frame.get("bullets") or [])
    position = "top" if frame.get("position") == "top" else "left"
    context.update(
        {
            "title": typst_backend.ty_text(frame.get("section")),
            "subsection": optional_text(frame.get("subsection")),
            "takeaway": optional_text(frame.get("takeaway")),
            "bullets": [typst_backend.ty_text(bullet) for bullet in bullets],
            "position": position,
            "figure": None,
            "grid": None,
            "equations": [],
            "table": None,
            "paper": None,
            "cards": [],
            "outlook": [],
        }
    )
    refs = frame.get("figures") or []
    if refs and layout in SHOWN_BY["figures"]:
        ref = refs[0]
        figure = lookup.figures[ref["label"]]
        context["figure"] = render.caption(f"图{figure['number']}", figure["caption"], name, "图")
        if layout == "figure-grid":
            letters = {sub["letter"]: sub for sub in figure["subfigures"] if sub.get("letter")}
            selected = [letters[letter] for letter in ref["subfigures"]]
            per_row, _, _, height = GRID[len(selected)]
            cells = []
            for sub in selected:
                cell = render.caption(f"({sub['letter']})", sub["caption"], name, "子图")
                cell["path"] = render.image(figure, sub["file"], name)
                cell["size"] = f"height: {TYPST_GRID_HEIGHTS[height]}"
                cells.append(cell)
            context["grid"] = {"cells": cells, "columns": per_row}
        else:
            path = figure_file(figure, name, render.warnings)
            key = f"{layout}-top" if layout == "figure-bullets" and position == "top" else layout
            context["figure"]["path"] = render.image(figure, path, name)
            context["figure"]["size"] = typst_size(ref, TYPST_HEIGHTS[key])
    if layout == "equations-figure":
        for ref in frame.get("equations") or []:
            equation = lookup.equations[ref["label"] if isinstance(ref, dict) else ref]
            numbers = " ".join(
                f"({item['number']})" for item in equation["labels"] if item["number"]
            )
            raw = typst_backend.raw_block(typst_backend.equation_body(equation))
            context["equations"].append(
                {
                    "number": typst_backend.ty_literal(numbers) if numbers else "none",
                    "source": f"thesis-macros + {raw}.text" if render.macros else raw,
                }
            )
    if layout == "table":
        table = lookup.tables[frame["table"]]
        try:
            grid = typst_backend.table_grid(table["tabular_source"], render.numbers)
        except typst_backend.TypstBackendError as exc:
            render.errors.append(f"{name}：表 {table['label']} {exc}；可换版式或改用 Beamer 后端")
            grid = [[[]]]
        context["table"] = render.caption(f"表{table['number']}", table["caption"], name, "表")
        context["table"]["header"] = [render.cell(cell) for cell in grid[0]]
        context["table"]["rows"] = [[render.cell(cell) for cell in row] for row in grid[1:]]
    if layout == "paper-summary" and frame.get("paper"):
        context["paper"] = typst_backend.ty_str(lookup.papers[frame["paper"]]["text"])
    if layout == "cards":
        for index, bullet in enumerate(bullets, 1):
            if frame["role"] == "challenges":
                label = "问题" + CN_NUMERALS[index - 1] if index <= 10 else f"问题 {index}"
            else:
                label = f"创新点 {index}"
            context["cards"].append(
                {"label": typst_backend.ty_str(label), "text": typst_backend.ty_text(bullet)}
            )
    if layout == "outlook":
        context["outlook"] = [
            {
                "label": typst_backend.ty_str(
                    "其" + CN_NUMERALS[index] if index < 10 else f"其 {index + 1}"
                ),
                "text": typst_backend.ty_text(item),
            }
            for index, item in enumerate(bullets)
        ]
    return context


def outline_groups(chapters: list[dict]) -> str:
    """``outline-slide(groups:)``: each run of consecutive research chapters, by heading index."""
    runs: list[list[int]] = []
    for index, chapter in enumerate(chapters, 1):
        if chapter.get("role") != "research":
            continue
        if runs and runs[-1][1] == index - 1:
            runs[-1][1] = index
        else:
            runs.append([index, index])
    if not runs:
        return ""
    return "(" + "".join(f"(from: {first}, to: {last}), " for first, last in runs) + ")"


def typst_headings(frames: list[dict], chapters: list[dict]) -> list[list[str]]:
    """Level-1 headings without a chapter opener (``<touying:skip>``) to write before each frame.

    Every chapter gets one level-1 heading so that the outline, the footer, and the
    opener numbers follow the thesis. A chapter-contents frame writes its own heading.
    """
    titles = {c["number"]: typst_backend.ty_text(c["title"]) for c in chapters}
    done: set[int] = set()
    result = []
    for frame in frames:
        pending: list[str] = []
        chapter = frame.get("chapter")
        if frame["layout"] == "thanks":
            pending = [titles[n] for n in titles if n not in done]
            done |= set(titles)
        elif isinstance(chapter, int) and chapter in titles and chapter not in done:
            for number in titles:
                if number < chapter and number not in done:
                    pending.append(titles[number])
                    done.add(number)
            if frame["layout"] != "toc":
                pending.append(titles[chapter])
            done.add(chapter)
        result.append(pending)
    return result


def render_typst(
    plan: dict,
    inventory: dict,
    lookup: Lookup,
    digests: tuple[str, str],
    warnings: list[str],
    notes_pdf: bool,
    package: str,
    version: str | None,
) -> tuple[dict[str, bytes], dict[str, Path]]:
    """defense.typ, notes.md, build_manifest.json, and the images to copy into img/."""
    meta = plan["meta"]
    if meta.get("inventory_sha256") not in (None, digests[1]):
        warnings.append("规划的 inventory_sha256 与当前清单不一致；清单在规划后已更新")
    if typst_backend.parse_spec(package) is None:
        raise BuildError(f"--typst-package 应为 @namespace/name:x.y.z，当前 {package!r}")
    selected = select_macros(inventory.get("macros", []), typst_math_texts(plan, lookup))
    errors: list[str] = []
    translated = []
    for macro in selected:
        try:
            translated.append(typst_backend.translate_macro(macro))
        except typst_backend.TypstBackendError as exc:
            errors.append(f"{exc}；可改用 Beamer 后端")
    render = TypstRender(inventory, lookup, bool(translated), warnings)
    render.errors += errors
    chapters = []
    for chapter in meta.get("chapters") or render.chapters:
        entry = {"number": chapter["number"], "title": str(chapter["title"])}
        entry["role"] = chapter.get("role")
        label = chapter.get("nav_label")
        if not (isinstance(label, str) and label.strip()):
            label = typst_backend.default_nav_label(entry["number"], entry["title"])[0]
        entry["nav_label"] = label
        chapters.append(entry)
    frames = [
        typst_frame_context(frame, f"第 {index} 帧（{frame['id']}）", render, chapters, plan)
        for index, frame in enumerate(plan["frames"], 1)
    ]
    for context, headings in zip(frames, typst_headings(plan["frames"], chapters)):
        context["skip_headings"] = headings
    if render.errors:
        raise BuildError(
            "Touying 后端无法渲染：\n" + "\n".join(f"  - {error}" for error in render.errors)
        )

    lines = [str(line) for line in meta.get("title_lines") or [] if str(line).strip()]
    title = "[" + "#linebreak()".join("#" + typst_backend.ty_text(line) for line in lines) + "]"
    supervisor = typst_backend.ty_text(meta.get("supervisor"))
    if plain_text(meta.get("supervisor_title")):
        supervisor = f"[#{supervisor}#h(1em)#{typst_backend.ty_text(meta['supervisor_title'])}]"
    stage, stage_en = typst_backend.stage_labels(meta["stage"], inventory.get("degree"))
    nav = "".join(typst_backend.ty_str(c["nav_label"]) + ", " for c in chapters)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TYPST_DIR), encoding="utf-8"),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        keep_trailing_newline=True,
        undefined=jinja2.StrictUndefined,
    )
    deck = env.get_template("deck.typ.j2").render(
        package=package,
        macros=typst_backend.raw_block("\n".join(translated)) if translated else "",
        nav_labels=f"({nav})" if nav else "auto",
        title=title if lines else '""',
        author=typst_backend.ty_text(meta.get("author")),
        supervisor=supervisor,
        subject=typst_backend.ty_text(meta.get("subject")),
        school=typst_backend.ty_text(meta.get("school")),
        date=typst_backend.ty_text(meta.get("date")),
        stage=typst_backend.ty_str(stage),
        stage_en=typst_backend.ty_str(stage_en),
        region_begin=typst_backend.REGION_BEGIN,
        region_end=typst_backend.REGION_END,
        frames=frames,
    )
    files = {
        "defense.typ": deck.encode("utf-8"),
        "notes.md": render_notes(plan).encode("utf-8"),
    }
    manifest = {
        "skill": "academic-defense-beamer",
        "version": skill_version(),
        "backend": "touying",
        "notes_pdf": NOTES_PDF if notes_pdf else None,
        "theme": "yanshan",
        "stage": meta["stage"],
        "frames": len(plan["frames"]),
        "typst_package": package,
        "typst_version": version,
        "plan_sha256": digests[0],
        "inventory_sha256": digests[1],
        "files": {name: sha256(data) for name, data in files.items()},
        "copied_images": sorted(render.images),
        "warnings": warnings,
    }
    files["build_manifest.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    return files, render.images


def previous_images(out_dir: Path) -> set[str]:
    """copied_images of the build_manifest.json that an earlier build wrote."""
    try:
        manifest = json.loads((out_dir / "build_manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    images = manifest.get("copied_images") if isinstance(manifest, dict) else None
    return {str(item) for item in images or [] if isinstance(item, str)}


def write_images(out_dir: Path, images: dict[str, Path], previous: set[str]) -> None:
    """Copy the planned images (bytes unchanged); delete earlier copies that left the plan.

    Only files that build_manifest.json lists as copied are deleted; unchanged
    copies keep their mtimes.
    """
    for target, source in images.items():
        path = out_dir / target
        data = source.read_bytes()
        if path.is_file() and path.read_bytes() == data:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    root = (out_dir / typst_backend.IMAGE_DIR).resolve()
    for target in sorted(previous - set(images)):
        path = (out_dir / target).resolve()
        if root not in path.parents or not path.is_file():
            continue
        path.unlink()
        parent = path.parent
        while parent != root and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent


def compile_deck(out_dir: Path, notes_pdf: bool = True) -> int:
    """Compile defense.tex, then defense-notes.tex unless ``notes_pdf`` is false."""
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        print(
            "错误：未找到 latexmk；请安装 TeX Live（含 XeLaTeX 与 latexmk）后重试", file=sys.stderr
        )
        return 5
    code = compile_file(latexmk, out_dir, "defense.tex")
    if code == 0 and notes_pdf:
        code = compile_file(latexmk, out_dir, NOTES_TEX)
    return code


def compile_file(latexmk: str, out_dir: Path, name: str) -> int:
    stem = Path(name).stem
    command = [
        latexmk,
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        name,
    ]
    try:
        result = subprocess.run(
            command,
            cwd=out_dir,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
            check=False,
        )
        failed = result.returncode != 0
    except subprocess.TimeoutExpired:
        failed = True
    if failed or not (out_dir / f"{stem}.pdf").is_file():
        log = out_dir / f"{stem}.log"
        tail = (
            log.read_text(encoding="utf-8", errors="replace").splitlines()[-40:]
            if log.is_file()
            else []
        )
        print(f"错误：{name} 编译失败；{stem}.log 末 40 行：", file=sys.stderr)
        for line in tail:
            print(line, file=sys.stderr)
        return 5
    print(f"已编译 {out_dir / f'{stem}.pdf'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "校验答辩稿规划并渲染答辩稿（Beamer 的 defense.tex 或 Touying 的 defense.typ）、"
            "讲稿与主题文件。"
        )
    )
    parser.add_argument("--plan", required=True, help="已填写的 slide_plan.yaml")
    parser.add_argument(
        "--inventory", required=True, help="extract_thesis.py 输出的 inventory.json"
    )
    parser.add_argument("--out", required=True, help="输出目录（不存在时创建）")
    parser.add_argument("--logo", help="校徽图片路径；优先于规划与清单中的 logo")
    parser.add_argument("--force", action="store_true", help="覆盖输出目录中由本脚本生成的八个文件")
    parser.add_argument(
        "--compile",
        action="store_true",
        help="生成后用 latexmk -xelatex 编译投屏版 defense.pdf 与备注版 defense-notes.pdf",
    )
    parser.add_argument(
        "--no-notes-pdf",
        action="store_true",
        help="不编译备注版 defense-notes.pdf；build_manifest.json 的 notes_pdf 记为 null",
    )
    parser.add_argument(
        "--typst-package",
        default=typst_backend.DEFAULT_THEME_PACKAGE,
        help=f"Touying 主题包（默认 {typst_backend.DEFAULT_THEME_PACKAGE}；仅 Touying 后端）",
    )
    parser.add_argument(
        "--typst-package-path", help="传给 typst --package-path 的本地包目录（仅 Touying 后端）"
    )
    parser.add_argument("--font-path", help="传给 typst --font-path 的字体目录（仅 Touying 后端）")
    args = parser.parse_args(argv)
    notes_pdf = not args.no_notes_pdf
    notices: list[str] = []
    touying = False

    warnings: list[str] = []
    try:
        plan, plan_bytes = read_input(Path(args.plan), "yaml")
        inventory, inventory_bytes = read_input(Path(args.inventory), "json")
        lookup = Lookup(inventory)
        errors = validate(plan, lookup)
        if args.logo and not Path(args.logo).is_file():
            errors.append(f"--logo 文件不存在：{args.logo}")
        out_dir = Path(args.out).resolve()
        if out_dir.exists() and not out_dir.is_dir():
            errors.append(f"--out 不是目录：{args.out}")
        if errors:
            raise BuildError("规划校验未通过：\n" + "\n".join(f"  - {error}" for error in errors))
        digests = (sha256(plan_bytes), sha256(inventory_bytes))
        touying = plan_backend(plan) == "touying"
        images: dict[str, Path] = {}
        if touying:
            if args.logo:
                notices.append("Touying 后端不使用 --logo；主题包自带校标")
            executable = shutil.which("typst")
            version = typst_backend.typst_version(executable) if executable else None
            files, images = render_typst(
                plan,
                inventory,
                lookup,
                digests,
                warnings,
                notes_pdf,
                args.typst_package,
                typst_backend.version_text(version),
            )
        else:
            if (
                args.typst_package != typst_backend.DEFAULT_THEME_PACKAGE
                or args.typst_package_path
                or args.font_path
            ):
                notices.append(
                    "--typst-package、--typst-package-path 与 --font-path 只对 Touying 后端生效"
                )
            files = render(
                plan, inventory, lookup, out_dir, args.logo, digests, warnings, notes_pdf
            )
    except BuildError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    owned = TYPST_OWNED_FILES if touying else OWNED_FILES
    existing = [name for name in owned if (out_dir / name).exists()]
    image_dir = out_dir / typst_backend.IMAGE_DIR
    if touying and image_dir.is_dir() and any(image_dir.iterdir()):
        existing.append(f"{typst_backend.IMAGE_DIR}/")
    if existing and not args.force:
        scope = "defense.typ、notes.md、build_manifest.json 与复制的图" if touying else "八个文件"
        print(
            f"错误：输出目录已有 {'、'.join(existing)}；确认覆盖时加 --force（只覆盖本脚本生成的{scope}）",
            file=sys.stderr,
        )
        return 4
    previous = previous_images(out_dir) if touying else set()
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        target = out_dir / name
        # Keep unchanged files and their mtimes: latexmk skips a rebuild when the
        # content hashes match, and a fresh defense.tex mtime would then postdate the PDF.
        if target.is_file() and target.read_bytes() == data:
            continue
        target.write_bytes(data)
    if touying:
        write_images(out_dir, images, previous)
    print(f"已写入 {out_dir}：帧数 {len(plan['frames'])}；warnings {len(warnings)} 条")
    for warning in warnings + notices:
        print(f"  警告：{warning}")
    if not args.compile:
        return 0
    if touying:
        return typst_backend.compile_deck(
            out_dir,
            theme_package=args.typst_package,
            notes_pdf=notes_pdf,
            package_path=args.typst_package_path,
            font_path=args.font_path,
        )
    return compile_deck(out_dir, notes_pdf)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
