#!/usr/bin/env python3
"""
Build the Beamer defense deck for latex-defense-zh.

The script checks slide_plan.yaml against inventory.json, then writes defense.tex,
notes.md, thesis-macros.tex, build_manifest.json, and the three theme files into
the output directory. Figures stay in the thesis repository: the deck finds them
through a relative graphicspath. Equation and table bodies come from the
inventory source text. The script escapes all plain text fields.

Field and transformation rules: references/plan-schema.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/build_deck.py --plan slide_plan.yaml \
        --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile]

Exit codes: 0 success; 2 input error; 4 an output file exists and --force is
absent; 5 compile failure.
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
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import extract_thesis
    import tex_loader

SKILL_DIR = Path(__file__).resolve().parent.parent
JINJA_DIR = SKILL_DIR / "templates" / "jinja"
BEAMER_DIR = SKILL_DIR / "templates" / "beamer"
THEME_FILES = (
    "beamerthemeYanshanDefense.sty",
    "beamerthemeGenericDefense.sty",
    "defense-layouts.sty",
)
OWNED_FILES = ("defense.tex", "notes.md", "build_manifest.json", "thesis-macros.tex", *THEME_FILES)
THEMES = {"yanshan": "YanshanDefense", "generic": "GenericDefense"}
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
MACRO_NAME_RE = re.compile(r"\\([A-Za-z@]+)")
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


def tex_escape(value: object) -> str:
    """Escape a plan text field; ``**word**`` becomes ``\\DefenseHighlight{word}``."""
    if value is None:
        return ""
    text = re.sub(r"\s+", " ", str(value)).strip()
    parts: list[str] = []
    pos = 0
    for match in EMPHASIS_RE.finditer(text):
        parts.append(escape_plain(text[pos : match.start()]))
        parts.append("\\DefenseHighlight{" + escape_plain(match.group(1)) + "}")
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


def macro_names(text: str, known: set[str]) -> set[str]:
    return {name for name in MACRO_NAME_RE.findall(text) if name in known}


def select_macros(macros: list[dict], texts: list[str]) -> list[dict]:
    """Thesis macros that the texts use, directly or through other macros, in preamble order."""
    known = {macro["name"] for macro in macros}
    definitions: dict[str, str] = {}
    for macro in macros:
        definitions[macro["name"]] = definitions.get(macro["name"], "") + macro["definition"]
    needed: set[str] = set()
    for text in texts:
        needed |= macro_names(text, known)
    frontier = list(needed)
    while frontier:
        for name in macro_names(definitions[frontier.pop()], known) - needed:
            needed.add(name)
            frontier.append(name)
    return [macro for macro in macros if macro["name"] in needed]


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


def validate(plan: dict, lookup: Lookup) -> list[str]:
    errors = []
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


def frame_context(frame: dict, name: str, lookup: Lookup, warnings: list[str]) -> dict:
    layout = frame["layout"]
    chapter = frame.get("chapter")
    context: dict = {
        "id": frame["id"],
        "role": frame["role"],
        "layout": layout,
        "chapter": "-" if chapter is None else str(chapter),
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


def deck_labels(inventory: dict) -> list[dict]:
    """Every thesis label with its number, for \\DefenseDefineLabel."""
    pairs: list[tuple[str, str]] = []
    for figure in inventory.get("figures", []):
        pairs.append((figure["label"], figure["number"]))
        pairs += [(sub["label"], sub["number"]) for sub in figure["subfigures"] if sub.get("label")]
    for kind in ("tables", "algorithms"):
        pairs += [(item["label"], item["number"]) for item in inventory.get(kind, [])]
    for equation in inventory.get("equations", []):
        pairs += [(item["label"], item["number"]) for item in equation["labels"]]
    labels: dict[str, str] = {}
    for label, number in pairs:
        if label and number and not label.startswith("auto:"):
            labels.setdefault(label, number)
    return [{"label": label, "number": escape_plain(number)} for label, number in labels.items()]


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
        "% thesis-macros.tex: generated by latex-defense-zh scripts/build_deck.py.",
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
        "notes.md": render_notes(plan).encode("utf-8"),
        "thesis-macros.tex": render_macros(inventory, plan, lookup).encode("utf-8"),
    }
    for name in THEME_FILES:
        files[name] = (BEAMER_DIR / name).read_bytes()
    manifest = {
        "skill": "latex-defense-zh",
        "version": skill_version(),
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


def compile_deck(out_dir: Path) -> int:
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        print(
            "错误：未找到 latexmk；请安装 TeX Live（含 XeLaTeX 与 latexmk）后重试", file=sys.stderr
        )
        return 5
    command = [
        latexmk,
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "defense.tex",
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
    if failed or not (out_dir / "defense.pdf").is_file():
        log = out_dir / "defense.log"
        tail = (
            log.read_text(encoding="utf-8", errors="replace").splitlines()[-40:]
            if log.is_file()
            else []
        )
        print("错误：编译失败；defense.log 末 40 行：", file=sys.stderr)
        for line in tail:
            print(line, file=sys.stderr)
        return 5
    print(f"已编译 {out_dir / 'defense.pdf'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="校验答辩稿规划并渲染 Beamer 答辩稿（defense.tex）、讲稿与主题文件。"
    )
    parser.add_argument("--plan", required=True, help="已填写的 slide_plan.yaml")
    parser.add_argument(
        "--inventory", required=True, help="extract_thesis.py 输出的 inventory.json"
    )
    parser.add_argument("--out", required=True, help="输出目录（不存在时创建）")
    parser.add_argument("--logo", help="校徽图片路径；优先于规划与清单中的 logo")
    parser.add_argument("--force", action="store_true", help="覆盖输出目录中由本脚本生成的七个文件")
    parser.add_argument("--compile", action="store_true", help="生成后用 latexmk -xelatex 编译")
    args = parser.parse_args(argv)

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
        files = render(plan, inventory, lookup, out_dir, args.logo, digests, warnings)
    except BuildError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    existing = [name for name in OWNED_FILES if (out_dir / name).exists()]
    if existing and not args.force:
        print(
            f"错误：输出目录已有 {'、'.join(existing)}；确认覆盖时加 --force（只覆盖本脚本生成的七个文件）",
            file=sys.stderr,
        )
        return 4
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (out_dir / name).write_bytes(data)
    print(f"已写入 {out_dir}：帧数 {len(plan['frames'])}；warnings {len(warnings)} 条")
    for warning in warnings:
        print(f"  警告：{warning}")
    return compile_deck(out_dir) if args.compile else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
