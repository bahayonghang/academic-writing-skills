#!/usr/bin/env python3
"""Plan bounded Chinese thesis units and compare a revision without rewriting it.

Semantic fidelity remains NEEDS-LLM. See references/writing/unit-polish-zh.md.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, cast

try:
    import analyze_logic as logic
    from parsers import get_parser, resolve_section_keys
    from tex_loader import AssembledDocument, assemble, read_text_robust
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import analyze_logic as logic
    from parsers import get_parser, resolve_section_keys
    from tex_loader import AssembledDocument, assemble, read_text_robust


HAN_RE = re.compile(r"[\u4e00-\u9fff]")
# A percent after an even number of backslashes starts a comment (e.g. after \\\\).
COMMENT_RE = re.compile(r"(?<!\\)((?:\\\\)*)%[^\n]*")
# Match complete supported command names, never a prefix such as \cite in \citereset.
# BibLaTeX multicites have global (...) notes and repeated [prenote][postnote]{keys}.
CITE_RE = re.compile(
    r"\\(?P<command>[Cc]ite[pt]?|[Uu]pcite|[Cc]ites|"
    r"(?:[Pp]aren|[Aa]uto|[Tt]ext|[Ff]oot|[Ss]mart|[Ss]uper)cites?|"
    r"[Ff]ootcitetexts?)(?![A-Za-z@])\s*\*?"
)
REF_RE = re.compile(r"\\(?:[Rr]ef|[Ee]qref|[Aa]utoref|[Cc]ref|[Pp]ageref)\s*\*?\s*\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\s*\{([^}]*)\}")
HEADING_RE = re.compile(
    r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\s*"
    r"(?:\[[^\]]*\]\s*)?\{"
)
STRUCTURE_RE = re.compile(r"\\(?:input|include)\b|\\begin\s*\{document\}")
MATH_RE = re.compile(
    r"\\begin\s*\{(?P<env>equation\*?|align\*?|gather\*?)\}"
    r"(?P<body>.*?)\\end\s*\{(?P=env)\}"
    r"|(?<!\\)\$\$(?P<display>.*?)(?<!\\)\$\$"
    r"|(?<!\\)\$(?P<inline>.*?)(?<!\\)\$"
    r"|\\\((?P<paren>.*?)\\\)|\\\[(?P<bracket>.*?)\\\]",
    re.DOTALL,
)
NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])[-+−]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?"
    r"(?:\s*(?:\\%|[%％])|(?:\s|\\,)*[A-Za-zμµ℃°]+[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]*"
    r"(?:[/·][A-Za-zμµ]+[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]*)?)?"
)
TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Za-z][A-Za-z0-9_-]*\d[A-Za-z0-9_-]*"
    r"|[A-Z][A-Za-z0-9]*(?:-[A-Z][A-Za-z0-9]*)+|[A-Z]{2,})(?![A-Za-z0-9_])"
)
DEFAULT_HEDGES = (
    "可能",
    "或许",
    "也许",
    "在一定程度上",
    "一定程度",
    "某种程度",
    "大致",
    "基本上",
    "相对而言",
    "似乎",
    "有望",
)
STRENGTH_TERMS = (
    "证明",
    "表明",
    "揭示",
    "发现",
    "识别出",
    "提示",
    "支持",
    "可能表明",
    "或许提示",
    "似乎",
    "暗示",
    "倾向于",
    "因果",
    "相关",
    "显著",
    "不显著",
    "可能",
)
STRONG_TERMS = {"证明", "表明", "揭示", "发现", "识别出", "因果", "显著"}
NEGATIONS = ("不", "未", "无", "非", "没有", "并非", "不能", "无法")
DOCUMENT_BOUNDARY_RE = re.compile(r"\\(begin|end)\s*\{document\}")
DOCUMENT_CONTROL_RE = re.compile(
    r"\s*\\(?:documentclass|usepackage|bibliography|bibliographystyle)"
    r"(?:\[[^\]]*\])?\s*\{[^{}]*\}\s*"
    r"|\s*\\(?:maketitle|tableofcontents|listoffigures|listoftables|"
    r"frontmatter|mainmatter|backmatter|clearpage|cleardoublepage|newpage)\s*"
)


def _visible(text: str, parser: Any) -> str:
    text = COMMENT_RE.sub(r"\1", text)
    for start, end, _keys in reversed(_citations(text)):
        text = text[:start] + " " + text[end:]
    # The shared parser does not mask every supported cite/ref/math spelling.
    for pattern in (REF_RE, LABEL_RE, MATH_RE):
        text = pattern.sub(" ", text)
    return parser.extract_visible_text(text)


def _argument_end(text: str, start: int, closing: str) -> int | None:
    """Find a TeX argument end, respecting braces and escaped delimiters in notes."""
    depth = 0
    index = start + 1
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == closing and depth == 0:
            return index + 1
        if char == "{":
            depth += 1
        elif char == "}" and depth:
            depth -= 1
        index += 1
    return None


def _citations(text: str) -> list[tuple[int, int, list[str]]]:
    """Return supported citation spans and all keys, excluding note payloads."""
    citations = []
    previous_end = 0
    for match in CITE_RE.finditer(text):
        if match.start() < previous_end:
            continue
        multiple = match["command"].endswith("s")
        cursor = match.end()
        keys = []
        end = cursor
        # A multicite can have up to two parenthesized global notes.
        openings = "((" if multiple else ""
        while True:
            for opening in openings + "[[":
                while cursor < len(text) and text[cursor].isspace():
                    cursor += 1
                if cursor < len(text) and text[cursor] == opening:
                    note_end = _argument_end(text, cursor, ")" if opening == "(" else "]")
                    if note_end is None:
                        break
                    cursor = note_end
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if cursor >= len(text) or text[cursor] != "{":
                break
            key_end = _argument_end(text, cursor, "}")
            if key_end is None:
                break
            keys.extend(key.strip() for key in text[cursor + 1 : key_end - 1].split(","))
            cursor = end = key_end
            if not multiple:
                break
            openings = ""
        if end > match.end():
            citations.append((match.start(), end, [key for key in keys if key]))
            previous_end = end
    return citations


def _cite_keys(text: str) -> Counter[str]:
    return Counter(key for _start, _end, keys in _citations(text) for key in keys)


def _prose_content(content: str) -> str:
    """Mask document scaffolding without moving the reused splitter's line coordinates."""
    boundaries = list(DOCUMENT_BOUNDARY_RE.finditer(COMMENT_RE.sub(r"\1", content)))
    in_body = not any(match.group(1) == "begin" for match in boundaries)
    lines = []
    for raw in content.split("\n"):
        line = COMMENT_RE.sub(r"\1", raw)
        boundary = DOCUMENT_BOUNDARY_RE.search(line)
        if boundary:
            in_body = boundary.group(1) == "begin"
            # Retain prose on the same line as a begin/end marker.
            line = line[boundary.end() :] if in_body else line[: boundary.start()]
            lines.append(line)
        elif in_body and not DOCUMENT_CONTROL_RE.fullmatch(line):
            lines.append(raw)
        else:
            lines.append("")
    return "\n".join(lines)


def _coordinates(doc: AssembledDocument, start: int, end: int) -> dict[str, Any]:
    source_file, source_start, source_end = logic._source_span(doc, start, end)
    return {"source_file": source_file, "source_start": source_start, "source_end": source_end}


def build_units(doc: AssembledDocument, first_chapter: int | None = None):
    """Reuse logic's cursor/splitter; keep raw text out of all returned units."""
    parser = get_parser(doc.entry)
    sections = parser.split_sections(doc.content)
    paragraphs = logic._split_arc_paragraphs(_prose_content(doc.content), parser, sections)
    subsections = logic._build_subsection_cursor(doc, parser, sections, first_chapter)
    paragraph_units: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for index, paragraph in enumerate(paragraphs):
        section = paragraph.section or "unclassified"
        counts[section] += 1
        context = {}
        for part, adjacent in (("prev.tail", index - 1), ("next.head", index + 1)):
            if 0 <= adjacent < len(paragraphs):
                neighbor = paragraphs[adjacent]
                if neighbor.section == paragraph.section:
                    context[part] = _coordinates(doc, neighbor.start, neighbor.end)
        paragraph_units.append(
            {
                "unit_id": f"{section}#{counts[section]}",
                "unit_type": "paragraph",
                "title": "",
                **_coordinates(doc, paragraph.start, paragraph.end),
                "assembled_start": paragraph.start,
                "assembled_end": paragraph.end,
                "han_count": len(HAN_RE.findall(paragraph.visible)),
                "context": context,
            }
        )
    units: list[dict[str, Any]] = []
    previous_doc = logic._DOC
    try:
        # These context helpers intentionally use the same document cursor as analyze().
        logic._DOC = doc
        for index, subsection in enumerate(subsections):
            window = logic._build_context_window(subsections, index, paragraphs)
            context = {
                part["part"]: {
                    key: part[key] for key in ("source_file", "source_start", "source_end")
                }
                for part in cast(list[dict[str, Any]], window["read_only"])
            }
            original = "\n".join(
                doc.lines[subsection.assembled_start - 1 : subsection.assembled_end]
            )
            unit = {
                "unit_id": subsection.subsection_id,
                "unit_type": "subsection",
                "title": subsection.title,
                **_coordinates(doc, subsection.assembled_start, subsection.assembled_end),
                "assembled_start": subsection.assembled_start,
                "assembled_end": subsection.assembled_end,
                "han_count": len(HAN_RE.findall(_visible(original, parser))),
                "context": context,
            }
            if unit["han_count"] > 1200:
                unit["paragraph_units"] = [
                    paragraph
                    for paragraph in paragraph_units
                    if unit["assembled_start"] <= paragraph["assembled_start"]
                    and paragraph["assembled_end"] <= unit["assembled_end"]
                ]
            units.append(unit)
    finally:
        logic._DOC = previous_doc
    return units or paragraph_units, paragraph_units, sections


def _heading_commands(text: str) -> list[str]:
    """Compare full heading payloads, including nested braces and starred commands."""
    commands = []
    for match in HEADING_RE.finditer(text):
        depth = 1
        end = match.end()
        while end < len(text) and depth:
            if text[end] in "{}" and text[end - 1] != "\\":
                depth += 1 if text[end] == "{" else -1
            end += 1
        commands.append(text[match.start() : end])
    return commands


def _keys(pattern: re.Pattern[str], text: str) -> Counter[str]:
    return Counter(
        key.strip() for keys in pattern.findall(text) for key in keys.split(",") if key.strip()
    )


def _math_tokens(text: str) -> Counter[str]:
    return Counter(
        re.sub(
            r"\s+",
            "",
            next(
                value
                for key, value in match.groupdict().items()
                if key != "env" and value is not None
            ),
        )
        for match in MATH_RE.finditer(text)
    )


def _load_hedges() -> tuple[str, ...]:
    path = Path(__file__).resolve().parent.parent / "references/writing/claim-forward-terms-zh.yaml"
    try:
        import yaml
    except ImportError:
        return DEFAULT_HEDGES
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return DEFAULT_HEDGES
    hedges = data.get("hedges") if isinstance(data, dict) else None
    if (
        not isinstance(hedges, list)
        or not hedges
        or not all(isinstance(term, str) and term for term in hedges)
    ):
        return DEFAULT_HEDGES
    return tuple(hedges)


def _word_counts(text: str, terms: tuple[str, ...]) -> Counter[str]:
    # Longest first prevents 不显著/显著 and 可能表明/可能/表明 double counting.
    pattern = "|".join(re.escape(term) for term in sorted(set(terms), key=lambda s: (-len(s), s)))
    return Counter(re.findall(pattern, text))


def verify(
    original: str,
    revised: str,
    *,
    terms: tuple[str, ...] = (),
    neighbors: tuple[str, ...] = (),
    max_growth: float = 0.20,
) -> list[dict[str, Any]]:
    """Return deterministic differences and semantic candidates, never replacement text."""
    parser = get_parser(Path("unit.tex"))
    orig, rev = COMMENT_RE.sub(r"\1", original), COMMENT_RE.sub(r"\1", revised)
    before, after = _visible(orig, parser), _visible(rev, parser)
    findings: list[dict[str, Any]] = []

    def add(code, title, left, right, *, tier="A", severity="Error", candidate="", basis=""):
        findings.append(
            {
                "code": code,
                "tier": tier,
                "severity": severity,
                "priority": "P1"
                if severity == "Error"
                else "P2"
                if severity == "Warning"
                else "P3",
                "title": title,
                "original": left,
                "revised": right,
                "candidate": candidate,
                "basis": basis,
            }
        )

    old_headings, new_headings = _heading_commands(orig), _heading_commands(rev)
    new_structure = Counter(STRUCTURE_RE.findall(rev)) - Counter(STRUCTURE_RE.findall(orig))
    leaked = []
    for neighbor in neighbors:
        # Remove the parent's heading before selecting its first visible prose sentence.
        for heading in _heading_commands(neighbor):
            neighbor = neighbor.replace(heading, "")
        sentence = re.split(r"[。！？!?]", _visible(neighbor, parser).strip(), maxsplit=1)[
            0
        ].strip()
        if len(HAN_RE.findall(sentence)) >= 12 and after.count(sentence) > before.count(sentence):
            leaked.append(sentence)
    if old_headings != new_headings or new_structure or leaked:
        add(
            "UP-SCOPE",
            "单元范围或标题发生变化",
            old_headings,
            new_headings + list(new_structure.elements()) + leaked,
            basis="unit-polish-zh.md：标题保留；只读邻域不得新增到润色稿",
        )
    for code, title, left, right in (
        ("UP-CITE", "引用键多重集发生变化", _cite_keys(orig), _cite_keys(rev)),
        ("UP-REF", "交叉引用目标多重集发生变化", _keys(REF_RE, orig), _keys(REF_RE, rev)),
        (
            "UP-LABEL",
            "标签集合发生变化",
            Counter(set(LABEL_RE.findall(orig))),
            Counter(set(LABEL_RE.findall(rev))),
        ),
        ("UP-MATH", "公式载荷发生变化", _math_tokens(orig), _math_tokens(rev)),
        (
            "UP-NUM",
            "可见数字或单位发生变化",
            Counter(re.sub(r"\s|\\,", "", m.group()) for m in NUMBER_RE.finditer(before)),
            Counter(re.sub(r"\s|\\,", "", m.group()) for m in NUMBER_RE.finditer(after)),
        ),
    ):
        if left != right:
            removed, added = left - right, right - left
            add(
                code,
                title,
                sorted(removed.elements()),
                sorted(added.elements()),
                basis="SKILL.md Safety Boundaries；unit-polish-zh.md 必须保留清单",
            )
    old_tokens, new_tokens = set(TOKEN_RE.findall(before)), set(TOKEN_RE.findall(after))
    if old_tokens != new_tokens:
        add(
            "UP-TOKEN",
            "受保护文本标识符集合变化",
            [],
            [],
            tier="B",
            severity="Warning",
            candidate=f"减少 {sorted(old_tokens - new_tokens)}；增加 {sorted(new_tokens - old_tokens)}",
        )
    changes = [
        f"「{term}」{before.count(term)}→{after.count(term)}"
        for term in terms
        if before.count(term) != after.count(term)
    ]
    if changes:
        add(
            "UP-TERM",
            "用户术语计数变化",
            [],
            [],
            tier="B",
            severity="Warning",
            candidate="，".join(changes),
        )
    hedges = _load_hedges()
    strength_texts = (before, after)
    if terms:
        # The explicit terminology contract is the only source of lexical exemptions.
        # Keep UP-TERM and all other checks on the original visible text.
        term_pattern = "|".join(re.escape(term) for term in sorted(terms, key=len, reverse=True))
        strength_texts = tuple(re.sub(term_pattern, " ", text) for text in strength_texts)
    left, right = (_word_counts(text, STRENGTH_TERMS + hedges) for text in strength_texts)
    # 与…一致 is a variable-content rung, counted once per bounded clause.
    for counts, text in zip((left, right), strength_texts):
        counts["与…一致"] = len(re.findall(r"与[^。！？!?；;\n]*?一致", text))
    if left != right:
        upward = any(right[t] > left[t] for t in STRONG_TERMS) or any(
            right[t] < left[t] for t in (*hedges, "可能表明", "或许提示", "倾向于", "暗示")
        )
        direction = "疑似抬升" if upward else "疑似削弱"
        changed = [
            f"「{term}」{left[term]}→{right[term]}"
            for term in sorted(left | right)
            if left[term] != right[term]
        ]
        add(
            "UP-STRENGTH",
            f"结论强度词计数变化（{direction}）",
            [],
            [],
            tier="B",
            severity="Warning",
            candidate=(
                "，".join(changed)
                + "；词面变化可能来自术语或普通用法，不代表语义强度已改变；"
                + f"原文语境：{_strength_context(strength_texts[0], left, right)}；"
                + f"润色稿语境：{_strength_context(strength_texts[1], left, right)}"
            ),
            basis="over-claim-guard.md 强度阶梯",
        )
    left, right = (_word_counts(text, NEGATIONS) for text in (before, after))
    if left != right:
        add(
            "UP-NEG",
            "否定标记计数变化（未标定）",
            [],
            [],
            tier="B",
            severity="Info",
            candidate=f"{dict(left)} → {dict(right)}；需核对否定对象",
        )
    old_length, new_length = len(HAN_RE.findall(before)), len(HAN_RE.findall(after))
    if new_length > old_length * (1 + max_growth) or new_length < old_length * (1 - max_growth):
        ratio = f"{(new_length - old_length) / old_length:+.1%}" if old_length else "原文为零"
        add(
            "UP-LENGTH",
            "可见汉字数变化超阈值（未标定）",
            [],
            [],
            tier="B",
            severity="Info",
            candidate=f"{old_length} → {new_length} 字；变化 {ratio}；阈值 {max_growth:.1%}",
        )
    return findings


def _read(path: Path, warnings: list[str]) -> str:
    text, warning = read_text_robust(path)
    if warning:
        warnings.append(warning)
    return text


def _read_terms(path: Path, warnings: list[str]) -> tuple[str, ...]:
    data = json.loads(_read(path, warnings))
    if not isinstance(data, dict):
        raise ValueError("--terms 需要包含 zh/en 分组的 JSON 对象")
    terms = set()
    for language in ("zh", "en"):
        groups = data.get(language, [])
        if not isinstance(groups, list) or any(
            not isinstance(group, list) or any(not isinstance(t, str) or not t for t in group)
            for group in groups
        ):
            raise ValueError("--terms 的 zh/en 必须是字符串数组的数组")
        terms.update(term for group in groups for term in group)
    return tuple(sorted(terms))


def _location(unit: dict[str, Any]) -> str:
    return f"{unit['source_file']}:L{unit['source_start']}-L{unit['source_end']}"


def _strength_context(text: str, left: Counter[str], right: Counter[str]) -> str:
    excerpts = []
    for term in sorted(left | right):
        if left[term] == right[term]:
            continue
        pattern = r"与[^。！？!?；;\n]*?一致" if term == "与…一致" else re.escape(term)
        match = re.search(pattern, text)
        if match:
            excerpt = text[max(0, match.start() - 12) : match.end() + 12].strip()
            excerpt = re.sub(r"\s+", " ", excerpt)
            if excerpt not in excerpts:
                excerpts.append(excerpt)
    return " / ".join(excerpts) if excerpts else "无对应词面"


def _render_difference(code: str, values: list[str]) -> str:
    if not values:
        return "无差异项"
    if code in ("UP-CITE", "UP-REF", "UP-LABEL"):
        command = code.removeprefix("UP-").lower()
        return f"{command}{{{', '.join(values)}}}"
    normalized = (re.sub(r"\s+", " ", value).strip() for value in values)
    return "；".join(f"「{value}」" for value in normalized)


def _render_unit(unit: dict[str, Any]) -> list[str]:
    split = " [需拆分]" if unit.get("paragraph_units") else ""
    lines = [
        f"% 单元 {unit['unit_id']}《{unit['title']}》 {unit['unit_type']} "
        f"{_location(unit)} 约 {unit['han_count']} 字 [可改]{split}"
    ]
    for part, coordinates in unit["context"].items():
        lines.append(f"%   {part}: {_location(coordinates)} [只读]")
    for paragraph in unit.get("paragraph_units", []):
        lines.extend(_render_unit(paragraph))
    return lines


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("tex_file", type=Path, help="LaTeX 工程入口（--original 核对时不读取）")
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true", help="列出润色单元与只读邻域坐标")
    mode.add_argument("--verify", action="store_true", help="核对单个单元的润色稿")
    cli.add_argument("--section", help="按章节键或标题筛选单元清单或 --unit 来源")
    source = cli.add_mutually_exclusive_group()
    source.add_argument("--unit", help="单元 id：小节编号或章节键#段序；与 --original 互斥")
    source.add_argument("--original", type=Path, help="独立原文文件；与 --unit 互斥")
    cli.add_argument("--first-chapter", type=int, help="覆盖首个编号章的起始编号")
    cli.add_argument("--revised", type=Path, help="待核对的单元润色稿文件（--verify 必填）")
    cli.add_argument("--terms", type=Path, help="consistency 格式的 zh/en 术语 JSON 文件")
    cli.add_argument(
        "--max-growth", type=float, default=0.20, help="字数变化阈值（默认 0.20，未标定）"
    )
    cli.add_argument("--json", action="store_true", help="输出结构化 JSON 清单或核对结果")
    args = cli.parse_args(argv)
    if args.verify and (args.revised is None or (args.unit is None and args.original is None)):
        cli.error("--verify 需要 --revised 以及 --unit 或 --original")
    if not math.isfinite(args.max_growth) or args.max_growth < 0:
        cli.error("--max-growth 必须是非负有限数")
    warnings: list[str] = []
    result: dict[str, Any] = {
        "mode": "plan" if args.plan else "verify",
        "entry": str(args.tex_file),
        "unit": args.unit,
        "original": str(args.original) if args.original else None,
        "revised": str(args.revised) if args.revised else None,
        "findings": [],
        "verdict": "PLAN" if args.plan else "PASS-SCRIPT",
        "meaning_check": "NEEDS-LLM",
        "warnings": warnings,
    }
    exit_code = 0
    try:
        # Explicit-file comparisons need no project assembly or unrelated source reads.
        if args.plan or args.unit:
            doc = assemble(args.tex_file)
            warnings.extend(line.removeprefix("% WARN: ") for line in doc.warning_lines())
            if args.verify and doc.missing:
                raise ValueError("原文含缺失的 include 文件，无法核对完整单元")
            units, paragraph_units, sections = build_units(doc, args.first_chapter)
            if not logic._has_numbered_depth3(doc, get_parser(doc.entry)):
                result["notice"] = logic.SUBSECTION_CONTEXT_NO_DEPTH3
            if args.section:
                keys, available = resolve_section_keys(args.section, sections)
                if not keys:
                    raise ValueError(f"未找到章节 {args.section}；可用章节：{', '.join(available)}")
                units = [
                    unit
                    for unit in units
                    if any(
                        sections[key][0] <= unit["assembled_start"] <= sections[key][1]
                        for key in keys
                    )
                ]
                paragraph_units = [
                    unit
                    for unit in paragraph_units
                    if any(
                        sections[key][0] <= unit["assembled_start"] <= sections[key][1]
                        for key in keys
                    )
                ]
            if args.unit:
                selected = next(
                    (u for u in units + paragraph_units if u["unit_id"] == args.unit), None
                )
                if selected is None:
                    raise ValueError(f"未找到单元 {args.unit}")
                units = [selected]
            result["units"] = units
            if args.verify:
                unit = units[0]
                original = "\n".join(doc.lines[unit["assembled_start"] - 1 : unit["assembled_end"]])
                result["original"] = _location(unit)
                neighbors = tuple(
                    "\n".join(
                        _read(doc.entry.parent / part["source_file"], warnings).splitlines()[
                            part["source_start"] - 1 : part["source_end"]
                        ]
                    )
                    for part in unit["context"].values()
                )
        if args.verify:
            if args.original:
                original = _read(args.original, warnings)
                neighbors = ()
            revised = _read(args.revised, warnings)
            terms = _read_terms(args.terms, warnings) if args.terms else ()
            findings = verify(
                original, revised, terms=terms, neighbors=neighbors, max_growth=args.max_growth
            )
            result["findings"] = findings
            exit_code = int(any(f["severity"] == "Error" for f in findings))
            result["verdict"] = "BLOCK" if exit_code else "PASS-SCRIPT"
    except (OSError, ValueError) as error:
        result["error"] = str(error)
        result["verdict"] = "ERROR"
        exit_code = 0 if args.plan else 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        title = "润色单元清单（polish）" if args.plan else "润色单元核对（polish）"
        print("\n".join(("=" * 60, title, "=" * 60)))
        print(
            f"% CONTRACT [Script]: mode={result['mode']} entry={args.tex_file} "
            f"unit={args.unit or 'none'} original={result['original']} revised={result['revised']} "
            f"section={args.section or 'all'} terms={args.terms or 'none'}"
        )
        for warning in warnings:
            print(f"% WARN: {warning}")
        if "error" in result:
            print(f"% ERROR: {result['error']}")
        elif args.plan:
            if "notice" in result:
                print(result["notice"])
            for unit in result["units"]:
                print("\n".join(_render_unit(unit)))
            print(
                f"% POLISH: 共 {len(result['units'])} 个单元。每次只处理一个单元；"
                "处理后运行 --verify；超过 1200 字的单元按内部段落单元逐段处理。"
            )
        else:
            for finding in result["findings"]:
                print(
                    f"% POLISH ({result['original']}) [Severity: {finding['severity']}] "
                    f"[Priority: {finding['priority']}] [Script]: {finding['code']} {finding['title']}"
                )
                if finding["tier"] == "A":
                    original_diff = _render_difference(finding["code"], finding["original"])
                    revised_diff = _render_difference(finding["code"], finding["revised"])
                    print(f"% 原文: {original_diff}\n% 润色稿: {revised_diff}")
                else:
                    print(f"% 候选: {finding['candidate']}")
                if finding["basis"]:
                    print(f"% 依据: {finding['basis']}")
                print("% Meaning-Check: NEEDS-LLM")
        if args.verify:
            print(
                f"% POLISH: 核对结论 = {result['verdict']}（仍需 [LLM] 语义复核：因果、范围、术语替换）"
            )
            print("% Meaning-Check: NEEDS-LLM")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
