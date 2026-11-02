#!/usr/bin/env python3
"""
Typst Touying backend helpers for academic-defense-beamer.

plan_deck.py and build_deck.py import this module when a plan sets
deck.backend: touying. It writes plan text as Typst string literals, splits
**keyword** emphasis into hl() calls, converts caption and table-cell source
text, parses simple tabular bodies into cell grids, translates thesis macros
for mitex, checks the image formats that Typst reads, finds the Typst packages
on this machine without network access, and runs typst compile.

The module has no command line. Rules: references/touying-backend.md.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

try:
    import extract_thesis
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import extract_thesis

DEFAULT_THEME_PACKAGE = "@preview/simply-ysu-touying:0.2.0"
TOUYING_PACKAGE = "@preview/touying:0.8.0"
MITEX_PACKAGE = "@preview/mitex:0.2.6"
MIN_TYPST_VERSION = (0, 15, 1)
NAV_LABEL_MAX = 6
IMAGE_SUFFIXES = (".pdf", ".png", ".jpg", ".jpeg", ".svg")
IMAGE_DIR = "img"
LOG_NAME = "defense.log"
NOTES_PDF = "defense-notes.pdf"
REGION_BEGIN = "// defense-source-begin"
REGION_END = "// defense-source-end"

SPEC_RE = re.compile(r"^@([a-z0-9_-]+)/([A-Za-z0-9_-]+):(\d+)\.(\d+)\.(\d+)$")
VERSION_RE = re.compile(r"typst\s+(\d+)\.(\d+)\.(\d+)")
EMPHASIS_RE = re.compile(r"\*\*(.+?)\*\*")
COMMENT_RE = re.compile(r"(?<!\\)%.*")
COMMAND_RE = re.compile(r"\\([A-Za-z@]+)\*?|\\(.)", re.S)
TABULAR_BEGIN_RE = re.compile(r"\s*\\begin\s*\{(tabular\*?|tabularx|longtable|xltabular)\}")
COMPLEX_TABLE_RE = re.compile(r"\\(multirow|multicolumn|makecell)(?![A-Za-z@])|\\begin\s*\{")
RULE_RE = re.compile(
    r"\\(?:hline|toprule|midrule|bottomrule)(?![A-Za-z@])"
    r"|\\(?:cline|cmidrule)(?![A-Za-z@])(?:\s*\([^)]*\))?\s*\{[^{}]*\}"
    r"|\\addlinespace(?![A-Za-z@])(?:\s*\[[^\]]*\])?"
)
ROW_OPTION_RE = re.compile(r"^\s*\[[^\]]*\]")
DEF_RE = re.compile(r"\\def\s*\\([A-Za-z@]+)\s*\{")
MACRO_PREFIX_RE = re.compile(r"^\\(?:newcommand|renewcommand|providecommand)\*?")
CITE_COMMANDS = ("cite", "citep", "citet", "upcite", "parencite", "textcite")
FORMAT_COMMANDS = (
    "centering",
    "raggedright",
    "raggedleft",
    "small",
    "footnotesize",
    "scriptsize",
    "normalsize",
    "bfseries",
    "itshape",
    "mdseries",
    "upshape",
)
SPACE_COMMANDS = ("quad", "qquad")
SYMBOLS = {"%": "%", "&": "&", "#": "#", "_": "_", "$": "$", "{": "{", "}": "}"}
SPACE_SYMBOLS = (",", " ", ";", ":", "!", "\\")
NBSP = "\u00a0"
# ASCII whitespace only: Python's \s also matches NBSP and would undo the ``~`` conversion.
ASCII_SPACE = " \t\n\r\f\v"
ASCII_SPACE_RE = re.compile(r"[ \t\n\r\f\v]+")


class TypstBackendError(Exception):
    """Input that the Touying backend cannot render (exit code 2)."""


# ---------------------------------------------------------------------------
# Plan text
# ---------------------------------------------------------------------------


def ty_literal(text: str) -> str:
    """Typst string literal of ``text``; only the backslash and ``"`` are escaped."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def ty_str(value: object) -> str:
    """Typst string literal of a plan field; whitespace runs collapse to one space."""
    return ty_literal(re.sub(r"\s+", " ", "" if value is None else str(value)).strip())


def ty_text(value: object, emphasis: str = "hl") -> str:
    """Code expression of a plan text field: a string, or content with ``#<emphasis>(...)``.

    Plan text never enters markup mode, so ``#``, ``$``, ``]`` and ``//`` show as written.
    """
    text = re.sub(r"\s+", " ", "" if value is None else str(value)).strip()
    if not EMPHASIS_RE.search(text):
        return ty_str(text)
    parts: list[str] = []
    pos = 0
    for match in EMPHASIS_RE.finditer(text):
        if match.start() > pos:
            parts.append("#" + ty_literal(text[pos : match.start()]))
        parts.append(f"#{emphasis}({ty_literal(match.group(1))})")
        pos = match.end()
    if pos < len(text):
        parts.append("#" + ty_literal(text[pos:]))
    return "[" + "".join(parts) + "]"


def raw_block(text: str) -> str:
    """Raw block with the fence on its own lines; the fence outgrows any backtick run."""
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}\n{text}\n{fence}"


def default_nav_label(number: int, title: str) -> tuple[str, bool]:
    """Footer label of a chapter: the title when it has at most six characters, else 第k章.

    The flag is true when the title was too long, so that the caller can give a hint.
    """
    text = re.sub(r"\s+", " ", title).strip()
    if text and len(text) <= NAV_LABEL_MAX:
        return text, False
    return f"第{number}章", True


# ---------------------------------------------------------------------------
# Thesis source text: captions and table cells
# ---------------------------------------------------------------------------

Piece = tuple[str, str]  # (kind, text); kind is str, strong, emph, or math


def _skip_arguments(text: str, pos: int, count: int) -> tuple[list[str], int]:
    try:
        while True:
            option, after = extract_thesis.read_optional(text, pos)
            if option is None:
                break
            pos = after
        return extract_thesis.read_groups(text, pos, count)
    except ValueError:
        return [], pos


def _close_math(text: str, start: int) -> int:
    """Offset of the ``$`` that closes the math opened at ``start``; -1 when none."""
    index = start
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == "$":
            return index
        index += 1
    return -1


def latex_inline(source: str, numbers: Mapping[str, str]) -> tuple[list[Piece], list[str]]:
    """Pieces of a caption or table cell, and the commands that have no Typst form.

    ``\\ref`` and ``\\eqref`` print the thesis number (``??`` for an unknown label),
    citation commands print nothing, ``\\textbf`` and ``\\emph`` keep their emphasis,
    ``$...$`` stays LaTeX for mitex, and ``~`` becomes a no-break space (U+00A0) that
    survives the whitespace collapse. An unsupported command stays as written.
    """
    text = COMMENT_RE.sub("", source)
    pieces: list[Piece] = []
    unsupported: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            pieces.append(("str", "".join(buffer)))
            buffer.clear()

    index = 0
    while index < len(text):
        char = text[index]
        if char == "$":
            end = _close_math(text, index + 1)
            if end < 0:
                buffer.append(text[index:])
                break
            flush()
            pieces.append(("math", text[index + 1 : end].strip()))
            index = end + 1
            continue
        if char == "\\":
            match = COMMAND_RE.match(text, index)
            assert match is not None
            name, symbol = match.group(1), match.group(2)
            index = match.end()
            if name is None:
                if symbol in SYMBOLS:
                    buffer.append(SYMBOLS[symbol])
                elif symbol in SPACE_SYMBOLS:
                    buffer.append(" ")
                else:
                    unsupported.append("\\" + (symbol or ""))
                    buffer.append(match.group(0))
                continue
            if name in CITE_COMMANDS:
                _, index = _skip_arguments(text, index, 1)
            elif name in ("ref", "eqref"):
                groups, index = _skip_arguments(text, index, 1)
                number = numbers.get(groups[0].strip(), "??") if groups else "??"
                buffer.append(f"({number})" if name == "eqref" else number)
            elif name in ("textbf", "textit", "emph"):
                groups, after = _skip_arguments(text, index, 1)
                inner, missing = latex_inline(groups[0], numbers) if groups else ([], [])
                if missing or any(kind != "str" for kind, _ in inner):
                    unsupported.append("\\" + name)
                    buffer.append(text[match.start() : after])
                else:
                    flush()
                    kind = "strong" if name == "textbf" else "emph"
                    pieces.append((kind, "".join(value for _, value in inner)))
                index = after
            elif name in SPACE_COMMANDS:
                buffer.append(" ")
            elif name in FORMAT_COMMANDS:
                pass
            else:
                unsupported.append("\\" + name)
                buffer.append(match.group(0))
            continue
        if char == "~":
            buffer.append(NBSP)
        elif text.startswith("---", index):
            buffer.append("\u2014")
            index += 2
        elif text.startswith("--", index):
            buffer.append("\u2013")
            index += 1
        elif char not in "{}":
            buffer.append(char)
        index += 1
    flush()
    merged: list[Piece] = []
    for kind, value in pieces:
        value = ASCII_SPACE_RE.sub(" ", value)
        if merged and kind == "str" and merged[-1][0] == "str":
            merged[-1] = ("str", merged[-1][1] + value)
        elif value or kind == "math":
            merged.append((kind, value))
    if merged and merged[0][0] == "str":
        merged[0] = ("str", merged[0][1].lstrip(ASCII_SPACE))
    if merged and merged[-1][0] == "str":
        merged[-1] = ("str", merged[-1][1].rstrip(ASCII_SPACE))
    return [piece for piece in merged if piece[1] or piece[0] == "math"], unsupported


def render_pieces(pieces: list[Piece], macros: bool) -> str:
    """Markup of the pieces; math uses mitex ``mi`` with the thesis macros when present."""
    parts = []
    for kind, value in pieces:
        if kind == "math":
            raw = raw_block(value)
            parts.append(f"#mi(thesis-macros + {raw}.text)" if macros else f"#mi({raw})")
        elif kind == "str":
            parts.append("#" + ty_literal(value))
        else:
            parts.append(f"#{kind}({ty_literal(value)})")
    return "".join(parts)


def pieces_plain(pieces: list[Piece]) -> str:
    """Text that check_deck.py reads back from the rendered cell: strings and math source."""
    return "".join(value for _, value in pieces)


def math_segments(source: str) -> list[str]:
    """``$...$`` bodies of a caption or cell, for the macro selection."""
    text = COMMENT_RE.sub("", source)
    found = []
    index = 0
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == "$":
            end = _close_math(text, index + 1)
            if end < 0:
                break
            found.append(text[index + 1 : end])
            index = end + 1
            continue
        index += 1
    return found


def _split_cells(row: str) -> list[str]:
    """Split a row at top-level ``&`` (outside braces and math)."""
    cells: list[str] = []
    depth = 0
    math = False
    start = 0
    index = 0
    while index < len(row):
        char = row[index]
        if char == "\\":
            index += 2
            continue
        if char == "$":
            math = not math
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "&" and depth == 0 and not math:
            cells.append(row[start:index])
            start = index + 1
        index += 1
    cells.append(row[start:])
    return cells


def tabular_rows(source: str) -> list[list[str]]:
    """Cell source texts of a simple tabular body; raises TypstBackendError for other tables.

    Simple means one tabular, tabular*, or tabularx environment with rule commands,
    ``&``, ``\\\\``, and cell text; multirow, multicolumn, makecell, and nested
    environments make the table complex.
    """
    text = COMMENT_RE.sub("", source or "")
    match = TABULAR_BEGIN_RE.match(text)
    if not match:
        raise TypstBackendError("表体不是 tabular 环境")
    env = match.group(1)
    if env in ("longtable", "xltabular"):
        raise TypstBackendError(f"表体为 {env}，Touying 后端只支持简单 tabular")
    count = 1 if env == "tabular" else 2
    groups, pos = _skip_arguments(text, match.end(), count)
    end = text.rfind("\\end{" + env + "}")
    if len(groups) != count or end < pos:
        raise TypstBackendError(f"{env} 的参数或结尾不完整")
    body = text[pos:end]
    found = COMPLEX_TABLE_RE.search(body)
    if found:
        what = "\\" + found.group(1) if found.group(1) else "嵌套环境"
        raise TypstBackendError(f"表体含 {what}，属于复杂表")
    body = RULE_RE.sub(" ", body)
    rows: list[list[str]] = []
    for row in extract_thesis.split_rows(body):
        cells = [cell.strip() for cell in _split_cells(ROW_OPTION_RE.sub("", row))]
        if any(cells):
            rows.append(cells)
    if not rows:
        raise TypstBackendError("表体没有单元格")
    width = max(len(row) for row in rows)
    return [row + [""] * (width - len(row)) for row in rows]


def table_grid(source: str, numbers: Mapping[str, str]) -> list[list[list[Piece]]]:
    """Pieces of every cell of a simple table; raises TypstBackendError when not simple."""
    grid = []
    unsupported: list[str] = []
    for row in tabular_rows(source):
        cells = []
        for cell in row:
            pieces, missing = latex_inline(cell, numbers)
            unsupported += missing
            cells.append(pieces)
        grid.append(cells)
    if unsupported:
        names = "、".join(dict.fromkeys(unsupported))
        raise TypstBackendError(f"表格单元格含 Touying 后端不能转换的命令 {names}，属于复杂表")
    return grid


def table_plain(source: str, numbers: Mapping[str, str]) -> list[str] | None:
    """Plain text of each cell, row by row; None for a table that is not simple."""
    try:
        grid = table_grid(source, numbers)
    except TypstBackendError:
        return None
    return [pieces_plain(cell) for row in grid for cell in row]


# ---------------------------------------------------------------------------
# Equations and macros
# ---------------------------------------------------------------------------


MACRO_NAME_RE = re.compile(r"\\([A-Za-z@]+)")
STAGE_EN = {"predefense": "Pre-defense", "defense": "Defense"}
DEGREE_NAMES = {"doctor": "博士", "master": "硕士"}


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


def label_numbers(inventory: dict) -> dict[str, str]:
    """Every thesis label with its thesis number (figures, subfigures, tables, equations)."""
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
    return labels


def stage_labels(stage: str, degree: str | None) -> tuple[str, str]:
    """``config-info`` stage and stage-en: 博士学位论文预答辩 and Pre-defense, for example."""
    name = "预答辩" if stage == "predefense" else "答辩"
    return f"{DEGREE_NAMES.get(degree or '', '')}学位论文{name}", STAGE_EN.get(stage, stage)


def equation_body(equation: dict) -> str:
    """Equation source for mitex: the inventory text without ``\\label``; nothing else changes."""
    return extract_thesis.LABEL_RE.sub("", equation["tex"]).strip("\n")


def translate_macro(macro: dict) -> str:
    """A thesis macro definition in the form that mitex reads (``\\newcommand``).

    ``\\def\\X{...}`` and ``\\DeclareMathOperator(*)`` become ``\\newcommand``; the
    definition body does not change. A parameterised ``\\def`` raises TypstBackendError.
    """
    command = str(macro.get("command") or "")
    definition = str(macro.get("definition") or "")
    name = macro.get("name", "")
    base = command.rstrip("*")
    if base in ("newcommand", "renewcommand", "providecommand"):
        return MACRO_PREFIX_RE.sub(lambda _: "\\newcommand", definition, count=1)
    if base == "def":
        match = DEF_RE.match(definition)
        if not match:
            raise TypstBackendError(f"宏 \\{name} 的 \\def 带参数或分隔符，mitex 不支持")
        try:
            body, _ = extract_thesis.read_group(definition, match.end() - 1)
        except ValueError as exc:
            raise TypstBackendError(f"宏 \\{name} 的 \\def 定义不完整") from exc
        return "\\newcommand{\\" + match.group(1) + "}{" + body + "}"
    if base == "DeclareMathOperator":
        start = re.match(r"\\DeclareMathOperator\*?", definition)
        groups, _ = _skip_arguments(definition, start.end() if start else 0, 2)
        if len(groups) != 2:
            raise TypstBackendError(f"宏 \\{name} 的 \\DeclareMathOperator 定义不完整")
        operator = "\\operatorname*" if command.endswith("*") else "\\operatorname"
        return "\\newcommand{" + groups[0].strip() + "}{" + operator + "{" + groups[1] + "}}"
    raise TypstBackendError(f"宏 \\{name} 的定义命令 \\{command} 没有 mitex 对应写法")


def unsupported_macros(macros: list[dict]) -> list[str]:
    """Messages for the macros that translate_macro rejects."""
    errors = []
    for macro in macros:
        try:
            translate_macro(macro)
        except TypstBackendError as exc:
            errors.append(str(exc))
    return errors


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------


def image_problem(resolved: str) -> str | None:
    """Why an inventory image cannot be copied for Typst; None when it can."""
    path = Path(resolved)
    if path.is_absolute() or ".." in path.parts:
        return f"图片路径 {resolved} 不在论文目录内"
    suffix = path.suffix.lower()
    if suffix == ".eps":
        return f"图片 {resolved} 为 EPS，Typst 不能读取；请在论文中改用 PDF、PNG、JPG 或 SVG"
    if suffix not in IMAGE_SUFFIXES:
        return f"图片 {resolved} 的格式 {suffix or '（无扩展名）'} 不受 Touying 后端支持"
    return None


def image_target(resolved: str) -> str:
    """Path of the copied image relative to the output directory."""
    return f"{IMAGE_DIR}/{Path(resolved).as_posix()}"


# ---------------------------------------------------------------------------
# Packages and the typst executable (no network access)
# ---------------------------------------------------------------------------


def parse_spec(spec: str) -> tuple[str, str, str] | None:
    """(namespace, name, version) of ``@namespace/name:x.y.z``; None for another form."""
    match = SPEC_RE.match(spec.strip())
    if not match:
        return None
    namespace, name, *version = match.groups()
    return namespace, name, ".".join(version)


def _data_dir(env: Mapping[str, str]) -> Path | None:
    home = Path(env.get("HOME") or env.get("USERPROFILE") or Path.home())
    if sys.platform == "win32":
        return Path(env["APPDATA"]) if env.get("APPDATA") else None
    if sys.platform == "darwin":
        return home / "Library" / "Application Support"
    return Path(env.get("XDG_DATA_HOME") or home / ".local" / "share")


def _cache_dir(env: Mapping[str, str]) -> Path | None:
    home = Path(env.get("HOME") or env.get("USERPROFILE") or Path.home())
    if sys.platform == "win32":
        return Path(env["LOCALAPPDATA"]) if env.get("LOCALAPPDATA") else None
    if sys.platform == "darwin":
        return home / "Library" / "Caches"
    return Path(env.get("XDG_CACHE_HOME") or home / ".cache")


def package_roots(
    namespace: str, package_path: str | None = None, env: Mapping[str, str] | None = None
) -> list[Path]:
    """Directories that typst reads ``<namespace>/<name>/<version>`` from, in order.

    The local package directory is --package-path, else TYPST_PACKAGE_PATH, else the
    Typst data directory. ``@preview`` packages also come from the cache directory
    (TYPST_PACKAGE_CACHE_PATH, else the Typst cache directory).
    """
    env = os.environ if env is None else env
    roots: list[Path] = []
    local = package_path or env.get("TYPST_PACKAGE_PATH")
    if local:
        roots.append(Path(local))
    else:
        data = _data_dir(env)
        if data is not None:
            roots.append(data / "typst" / "packages")
    if namespace == "preview":
        cache = env.get("TYPST_PACKAGE_CACHE_PATH")
        if cache:
            roots.append(Path(cache))
        else:
            directory = _cache_dir(env)
            if directory is not None:
                roots.append(directory / "typst" / "packages")
    return roots


def find_package(
    spec: str, package_path: str | None = None, env: Mapping[str, str] | None = None
) -> Path | None:
    """Directory of an installed package (it holds typst.toml); None when absent."""
    parsed = parse_spec(spec)
    if parsed is None:
        return None
    namespace, name, version = parsed
    for root in package_roots(namespace, package_path, env):
        directory = root / namespace / name / version
        if (directory / "typst.toml").is_file():
            return directory
    return None


def missing_packages(
    specs: list[str], package_path: str | None = None, env: Mapping[str, str] | None = None
) -> list[str]:
    return [spec for spec in specs if find_package(spec, package_path, env) is None]


def typst_version(executable: str) -> tuple[int, int, int] | None:
    """Version of the typst executable; None when it does not answer --version."""
    try:
        result = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = VERSION_RE.search(result.stdout or "")
    if not match:
        return None
    major, minor, patch = (int(part) for part in match.groups())
    return major, minor, patch


def version_text(version: tuple[int, int, int] | None) -> str | None:
    return ".".join(str(part) for part in version) if version else None


def install_hint(spec: str) -> str:
    return (
        f"  - {spec}：在有网络的环境运行一次 typst compile 让 typst 缓存它，或按 "
        "references/touying-backend.md 以 @local 方式安装；本脚本不下载包"
    )


def compile_deck(
    out_dir: Path,
    *,
    theme_package: str,
    notes_pdf: bool = True,
    package_path: str | None = None,
    font_path: str | None = None,
) -> int:
    """Check typst and the packages, then compile defense.pdf and defense-notes.pdf.

    Returns 0, 5 (typst missing, too old, or a compile failure), or 6 (a package is
    not installed; typst compile does not run, so nothing is downloaded).
    """
    executable = shutil.which("typst")
    if executable is None:
        print("错误：未找到 typst；请安装 Typst 0.15.1 或更高版本后重试", file=sys.stderr)
        return 5
    version = typst_version(executable)
    if version is None or version < MIN_TYPST_VERSION:
        found = version_text(version) or "未知"
        minimum = version_text(MIN_TYPST_VERSION)
        print(f"错误：typst 版本 {found} 低于 {minimum}；请升级 Typst", file=sys.stderr)
        return 5
    missing = missing_packages(
        [theme_package, TOUYING_PACKAGE, MITEX_PACKAGE], package_path=package_path
    )
    if missing:
        print("错误：以下 Typst 包未安装在本机：", file=sys.stderr)
        for spec in missing:
            print(install_hint(spec), file=sys.stderr)
        return 6
    log = out_dir / LOG_NAME
    log.write_text("", encoding="utf-8")
    targets = [("defense.pdf", False)] + ([(NOTES_PDF, True)] if notes_pdf else [])
    for name, notes in targets:
        command = [executable, "compile", "--root", str(out_dir)]
        if package_path:
            command += ["--package-path", package_path]
        if font_path:
            command += ["--font-path", font_path]
        if notes:
            command += ["--input", "notes=on"]
        command += [str(out_dir / "defense.typ"), str(out_dir / name)]
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
            failed, stderr = result.returncode != 0, result.stderr or ""
        except subprocess.TimeoutExpired:
            failed, stderr = True, "typst compile timed out\n"
        with log.open("a", encoding="utf-8") as stream:
            stream.write(f"== typst compile {name} ==\n{stderr}")
        if failed or not (out_dir / name).is_file():
            print(f"错误：{name} 编译失败；{LOG_NAME} 末 40 行：", file=sys.stderr)
            for line in stderr.splitlines()[-40:]:
                print(line, file=sys.stderr)
            return 5
        print(f"已编译 {out_dir / name}")
    return 0
