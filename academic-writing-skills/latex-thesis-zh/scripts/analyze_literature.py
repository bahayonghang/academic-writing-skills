#!/usr/bin/env python3
"""
文献综述分析器 — 中文学位论文版本

聚焦相关工作/文献综述段：
- A1: 作者年份罗列
- A2: 缺少比较分析
- A3: 缺少研究空白推导

绪论引用诊断（--intro-citations）：
- B1: 引用数量与阈值区间
- B2: 单点堆引（一个 \\cite 挤进 3 篇以上）
- B3: 同一作者/团队文献扎堆
- B4: 年份分布（需 --bib）
- B5: 缺少总结性对比表/研究演进图
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    from parsers import get_parser, resolve_section_keys
    from tex_loader import AssembledDocument, assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser, resolve_section_keys
    from tex_loader import AssembledDocument, assemble


# 当前装配文档（由 analyze() 设置），供行号输出定位到源文件。
_DOC: AssembledDocument | None = None


def _zh_loc(start: int, end: int | None = None) -> str:
    if _DOC is not None:
        return _DOC.lineref(start, end)
    if end is not None and end != start:
        return f"第{start}-{end}行"
    return f"第{start}行"


AUTHOR_ENUM_ZH = re.compile(
    r"^.*?[（(]\d{4}[)）].*?(?:提出|引入|设计|开发|采用|构建|建立)",
)

GAP_KEYWORDS_ZH = re.compile(
    r"(研究空白|不足|然而.*?尚未|仍然.*?(?:挑战|困难)|有待|缺乏|"
    r"尚未解决|亟待|亟需|鲜有研究|未能充分)",
)

COMPARISON_MARKERS_ZH = re.compile(
    r"(然而|但是|相比(?:之下)?|相较于|不同于|共同局限|共同不足|"
    r"对比|差异|优于|弱于|优劣|局限性|共同问题|trade-?off)",
    re.IGNORECASE,
)

SUMMARY_MARKERS_ZH = re.compile(
    r"(总体来看|整体上|综合来看|总体而言|归纳来看|这些工作表明|这类研究表明|共同趋势|总体趋势)",
    re.IGNORECASE,
)


def _visible_lines(lines: list[str], start: int, end: int, parser) -> list[tuple[int, str, str]]:
    visible: list[tuple[int, str, str]] = []
    comment_prefix = parser.get_comment_prefix()
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        text = parser.extract_visible_text(raw)
        if text:
            visible.append((line_no, raw, text))
    return visible


def _find_section_bounds(
    sections: dict[str, tuple[int, int]], section: str | None
) -> tuple[int, int] | None:
    if section:
        keys, _available = resolve_section_keys(section, sections)
        return sections[keys[0]] if keys else None
    for key in ("related", "literature", "related work"):
        if key in sections:
            return sections[key]
    return None


def _paragraphs(
    lines: list[str], start: int, end: int, parser
) -> list[tuple[int, int, list[str], list[str]]]:
    paragraphs: list[tuple[int, int, list[str], list[str]]] = []
    comment_prefix = parser.get_comment_prefix()
    current_texts: list[str] = []
    current_raws: list[str] = []
    para_start: int | None = None
    last_line = start

    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw:
            if current_texts and para_start is not None:
                paragraphs.append((para_start, last_line, current_raws[:], current_texts[:]))
                current_texts.clear()
                current_raws.clear()
                para_start = None
            continue
        if raw.startswith(comment_prefix):
            continue
        text = parser.extract_visible_text(raw)
        if not text:
            continue
        if para_start is None:
            para_start = line_no
        current_raws.append(raw)
        current_texts.append(text)
        last_line = line_no

    if current_texts and para_start is not None:
        paragraphs.append((para_start, last_line, current_raws, current_texts))
    return paragraphs


def _paragraph_a2_status(raws: list[str], texts: list[str]) -> tuple[str, int]:
    joined = "".join(texts)
    cite_hits = sum(
        1
        for raw, text in zip(raws, texts, strict=False)
        if "\\cite{" in raw or AUTHOR_ENUM_ZH.search(text)
    )
    has_comparison = bool(COMPARISON_MARKERS_ZH.search(joined))
    has_summary = bool(SUMMARY_MARKERS_ZH.search(joined))
    has_gap = bool(GAP_KEYWORDS_ZH.search(joined))

    if cite_hits < 2:
        return "pass", 99

    score = 0
    if cite_hits >= 2:
        score -= 2
    if cite_hits >= 3 and not (has_comparison or has_summary):
        score -= 1
    if has_comparison:
        score += 2
    if has_summary:
        score += 1
    if has_gap:
        score += 1

    if score <= -2:
        return "fail", score
    if score >= 1:
        return "pass", score
    return "uncertain", score


def analyze(file_path: Path, section: str | None = None) -> list[str]:
    global _DOC
    parser = get_parser(file_path)
    doc = assemble(file_path)
    _DOC = doc
    lines = doc.lines
    sections = parser.split_sections(doc.content)
    bounds = _find_section_bounds(sections, section)
    comment = parser.get_comment_prefix()

    if bounds is None:
        target = section or "related"
        avail = ", ".join(sections.keys()) if sections else "（未识别出任何已知章节）"
        return doc.warning_lines(comment) + [
            f"{comment} ERROR [Severity: Critical] [Priority: P0]: 未找到章节: {target}",
            f"{comment} 可用章节: {avail}",
            f"{comment} 提示：--section 同时接受英文键（related/...）与中文章节名（相关工作/文献综述/...）。",
        ]

    start, end = bounds
    visible = _visible_lines(lines, start, end, parser)
    out: list[str] = doc.warning_lines(comment)

    consecutive = 0
    streak_start = 0
    for line_no, _raw, text in visible:
        if AUTHOR_ENUM_ZH.search(text):
            if consecutive == 0:
                streak_start = line_no
            consecutive += 1
        else:
            if consecutive >= 3:
                out.extend(
                    [
                        f"{comment} 文献综述（{_zh_loc(streak_start, line_no - 1)}）[Severity: Major] [Priority: P1]: "
                        f"检测到作者/年份罗列模式（连续{consecutive}条）",
                        f"{comment} 建议：按研究主题重组文献，并在组内显式比较方法差异与共同局限。",
                        f"{comment} 理由：仅按作者和年份罗列，会削弱文献综述的综合深度。",
                        "",
                    ]
                )
            consecutive = 0
    if consecutive >= 3:
        out.extend(
            [
                f"{comment} 文献综述（{_zh_loc(streak_start, visible[-1][0])}）[Severity: Major] [Priority: P1]: "
                f"检测到作者/年份罗列模式（连续{consecutive}条）",
                f"{comment} 建议：按研究主题重组文献，并在组内显式比较方法差异与共同局限。",
                f"{comment} 理由：仅按作者和年份罗列，会削弱文献综述的综合深度。",
                "",
            ]
        )

    paragraphs = _paragraphs(lines, start, end, parser)
    paragraph_statuses = [
        (para_start, para_end, _paragraph_a2_status(raws, texts))
        for para_start, para_end, raws, texts in paragraphs
    ]
    fail_ranges = [
        (para_start, para_end)
        for para_start, para_end, (status, _score) in paragraph_statuses
        if status == "fail"
    ]
    uncertain_ranges = [
        (para_start, para_end)
        for para_start, para_end, (status, _score) in paragraph_statuses
        if status == "uncertain"
    ]

    if len(fail_ranges) >= 2:
        out.extend(
            [
                f"{comment} 文献综述（{_zh_loc(fail_ranges[0][0], fail_ranges[-1][1])}）[Severity: Major] [Priority: P1]: "
                "多个引文密集段落仍偏向文献罗列，缺少充分的比较分析句。",
                f"{comment} 建议：每个主题簇结尾补一两句，概括共同优势、关键差异或共享不足。",
                f"{comment} 理由：综述的价值不在于列举做过什么，而在于说明这些工作之间如何对话。",
                "",
            ]
        )
    elif len(fail_ranges) == 1 or uncertain_ranges:
        review_start = fail_ranges[0][0] if fail_ranges else uncertain_ranges[0][0]
        review_end = fail_ranges[0][1] if fail_ranges else uncertain_ranges[-1][1]
        out.extend(
            [
                f"{comment} 文献综述（{_zh_loc(review_start, review_end)}）[Severity: Needs Review] [Priority: P2]: "
                "至少有一个引文密集段落的比较分析可能偏弱，建议复核。",
                f"{comment} 建议：检查该段是否在段末明确总结共同局限、关键差异或 theme-level synthesis。",
                f"{comment} 理由：边界样例更适合模型或人工复核，不宜直接作为硬规则失败处理。",
                "",
            ]
        )

    scan_start = max(start, end - 10)
    tail = "".join(text for line_no, _, text in visible if line_no >= scan_start)
    if tail and not GAP_KEYWORDS_ZH.search(tail):
        out.extend(
            [
                f"{comment} 文献综述（{_zh_loc(scan_start, end)}）[Severity: Major] [Priority: P1]: "
                "相关工作末尾未发现明确的研究空白推导。",
                f"{comment} 建议：在结尾指出尚未解决的限制、边界条件或被忽略的情形，再引出本文切入点。",
                f"{comment} 理由：研究空白应从既有文献的共识与不足中自然推出，而不是直接跳到本文工作。",
                "",
            ]
        )

    out.extend(
        [
            f"{comment} 文献综述重写蓝图：共识 -> 分歧 -> 局限 -> 空白 -> 本文切入点",
            f"{comment} 建议改写链条：先概括多篇文献的共同结论，再指出方法分歧或 trade-off，随后提炼仍未解决的限制，最后再连接到本文贡献。",
        ]
    )

    return out


# ── 绪论引用诊断（B1~B5，--intro-citations）──────────────────────
#
# 阈值出处（默认值，均可用命令行覆盖，最终以本校规范为准）：
# - 博士论文参考文献总数一般 >=100（北工大/哈工大撰写规范），绪论承担其中
#   大部分引用，用户侧常用基准为 120~160 篇或更多；
# - 近三年文献 >=30%、近五年 >=50% 为较严的常见口径（近五年 >=1/3 为宽口径）。

CITE_COMMAND_RE = re.compile(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]*)\}")

DEFAULT_INTRO_MIN_CITES = 120
DEFAULT_INTRO_MAX_CITES = 160
RECENT3_SHARE_TARGET = 0.30
RECENT5_SHARE_TARGET = 0.50
STACKED_CITE_KEYS = 3  # 单个 \cite 中键数达到该值即视为堆引
CLUSTER_MIN_KEYS = 3  # 同前缀唯一键数达到该值即提示扎堆

_CAMEL_SEG_RE = re.compile(r"[A-Z][a-z]+|[A-Z]+(?![a-z])|[a-z]+|\d+")

_BIB_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s{}]+)\s*,")
_BIB_YEAR_RE = re.compile(
    r"""^\s*(?:year|date)\s*=\s*["{']*\s*(\d{4})""", re.IGNORECASE | re.MULTILINE
)
_BIB_SKIP_TYPES = {"string", "comment", "preamble"}


def author_prefix(key: str) -> str:
    """引用键 -> 作者前缀（启发式，用于同作者/团队扎堆提示）。

    - ``zhaoOnlineCementClinker2021`` -> ``zhao``（小写开头取首个小写连串）
    - ``Zhang2021CementTransition`` -> ``zhang``（姓+年份取首驼峰段）
    - ``ChaiTianYouFuZaGongYe...`` -> ``chaitian``（拼音全名驼峰取前两段）
    """
    segs = _CAMEL_SEG_RE.findall(key)
    if not segs:
        return key.lower()
    first = segs[0]
    if first.islower():
        return first
    if (
        len(segs) >= 3
        and segs[1].isalpha()
        and len(segs[1]) <= 4
        and segs[2].isalpha()
        and len(segs[2]) <= 4
    ):
        return (first + segs[1]).lower()
    return first.lower()


def parse_bib_years(bib_text: str) -> dict[str, int | None]:
    """从 BibTeX/BibLaTeX 文本提取 键 -> 年份（无 year/date 字段则为 None）。"""
    years: dict[str, int | None] = {}
    matches = list(_BIB_ENTRY_RE.finditer(bib_text))
    for idx, match in enumerate(matches):
        if match.group(1).lower() in _BIB_SKIP_TYPES:
            continue
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(bib_text)
        body = bib_text[match.end() : body_end]
        year_match = _BIB_YEAR_RE.search(body)
        years[match.group(2)] = int(year_match.group(1)) if year_match else None
    return years


def _cite_occurrences(
    lines: list[str], start: int, end: int, comment_prefix: str
) -> list[tuple[int, list[str]]]:
    """收集 (行号, 该行每条 \\cite 命令的键列表)，跳过注释行。"""
    occurrences: list[tuple[int, list[str]]] = []
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        for match in CITE_COMMAND_RE.finditer(raw):
            keys = [k.strip() for k in match.group(1).split(",") if k.strip()]
            if keys:
                occurrences.append((line_no, keys))
    return occurrences


def _has_visual_summary(lines: list[str], start: int, end: int) -> bool:
    markers = ("\\begin{table", "\\begin{tabular", "\\begin{figure", "\\includegraphics")
    return any(
        marker in lines[line_no - 1]
        for line_no in range(start, min(end, len(lines)) + 1)
        for marker in markers
    )


def analyze_intro_citations(
    file_path: Path,
    bib_path: Path | None = None,
    min_cites: int = DEFAULT_INTRO_MIN_CITES,
    max_cites: int = DEFAULT_INTRO_MAX_CITES,
    current_year: int | None = None,
) -> list[str]:
    """B1~B5：绪论引用数量、堆引、扎堆、年份分布与可视化收束诊断。"""
    global _DOC
    parser = get_parser(file_path)
    doc = assemble(file_path)
    _DOC = doc
    lines = doc.lines
    sections = parser.split_sections(doc.content)
    comment = parser.get_comment_prefix()
    out: list[str] = doc.warning_lines(comment)

    if "introduction" in sections:
        start, end = sections["introduction"]
    else:
        start, end = 1, len(lines)
        out.append(
            f"{comment} 绪论引用 [Severity: Info] [Priority: P3]: [Script] "
            "未识别出绪论章节，按整份文件统计。"
        )

    occurrences = _cite_occurrences(lines, start, end, comment)
    unique_keys: list[str] = []
    seen: set[str] = set()
    for _line_no, keys in occurrences:
        for key in keys:
            if key not in seen:
                seen.add(key)
                unique_keys.append(key)
    total = len(unique_keys)

    # B1：引用数量区间。
    if total < min_cites:
        out.extend(
            [
                f"{comment} 绪论引用（{_zh_loc(start, end)}）[Severity: Major] [Priority: P1]: "
                f"[Script] B1 引用数量不足：唯一引用 {total} 篇，低于基准下限 {min_cites} 篇。",
                f"{comment} 建议：从本地 .bib 或文献库补检相关主题文献（不可编造条目），"
                f"博士绪论常见基准为 {min_cites}~{max_cites} 篇或更多。",
                f"{comment} 理由：绪论承担全文大部分文献综述职能，引用量过低难以覆盖研究脉络。",
                "",
            ]
        )
    elif total > max_cites:
        out.append(
            f"{comment} 绪论引用（{_zh_loc(start, end)}）[Severity: Info] [Priority: P3]: "
            f"[Script] B1 唯一引用 {total} 篇，高于常见上限 {max_cites} 篇——数量本身不扣分，"
            "建议复核是否存在凑数引用。"
        )
    else:
        out.append(
            f"{comment} 绪论引用（{_zh_loc(start, end)}）[Severity: Info] [Priority: P3]: "
            f"[Script] B1 唯一引用 {total} 篇，处于基准区间 {min_cites}~{max_cites}。"
        )

    # B2：单点堆引。
    stacked = [(ln, keys) for ln, keys in occurrences if len(keys) >= STACKED_CITE_KEYS]
    if stacked:
        head = ", ".join(f"{_zh_loc(ln)}({len(keys)}篇)" for ln, keys in stacked[:10])
        more = f" 等共 {len(stacked)} 处" if len(stacked) > 10 else ""
        out.extend(
            [
                f"{comment} 绪论引用 [Severity: Minor] [Priority: P2]: [Script] "
                f"B2 检测到 {len(stacked)} 处单点堆引（一个 \\cite 含 {STACKED_CITE_KEYS} 篇以上）：{head}{more}。",
                f"{comment} 建议：把整簇引用拆到各自的观点句中，逐篇说明差异或递进，而不是一括号带过。",
                f"{comment} 理由：堆引读起来像凑数，也无法体现对每篇文献的消化。",
                "",
            ]
        )

    # B3：同作者/团队扎堆。
    groups: dict[str, list[str]] = {}
    for key in unique_keys:
        groups.setdefault(author_prefix(key), []).append(key)
    clustered = {p: ks for p, ks in groups.items() if len(ks) >= CLUSTER_MIN_KEYS}
    if clustered:
        for prefix, keys in sorted(clustered.items(), key=lambda kv: -len(kv[1])):
            co_cited = [
                ln
                for ln, occ_keys in occurrences
                if sum(1 for k in occ_keys if author_prefix(k) == prefix) >= 2
            ]
            co_note = (
                f"，且在 {', '.join(_zh_loc(ln) for ln in co_cited[:5])} 整簇共引"
                if co_cited
                else ""
            )
            out.append(
                f"{comment} 绪论引用 [Severity: Minor] [Priority: P2]: [Script] "
                f"B3 前缀“{prefix}”文献 {len(keys)} 篇{co_note}：{', '.join(keys[:6])}"
                f"{'...' if len(keys) > 6 else ''}。"
            )
        out.extend(
            [
                f"{comment} 建议：若为同一作者/团队，拆开分述并比较其方法演进与局限；"
                "若为不同作者（常见于中文姓氏拼音），请人工复核后忽略。",
                f"{comment} 理由：不宜只引用一组学者的文献；同团队多篇整簇共引会削弱综述的独立性。",
                "",
            ]
        )

    # B4：年份分布（需 --bib）。
    if bib_path is not None:
        bib_years = parse_bib_years(bib_path.read_text(encoding="utf-8", errors="replace"))
        year_now = current_year if current_year is not None else date.today().year
        known = [bib_years[k] for k in unique_keys if bib_years.get(k) is not None]
        unknown = total - len(known)
        if known:
            recent3 = sum(1 for y in known if y is not None and y >= year_now - 2)
            recent5 = sum(1 for y in known if y is not None and y >= year_now - 4)
            share3 = recent3 / len(known)
            share5 = recent5 / len(known)
            unknown_note = f"（另有 {unknown} 篇未在 bib 中找到年份）" if unknown else ""
            out.append(
                f"{comment} 绪论引用 [Severity: Info] [Priority: P3]: [Script] "
                f"B4 年份分布：近三年 {recent3}/{len(known)}（{share3:.0%}），"
                f"近五年 {recent5}/{len(known)}（{share5:.0%}）{unknown_note}。"
            )
            if share3 < RECENT3_SHARE_TARGET or share5 < RECENT5_SHARE_TARGET:
                out.extend(
                    [
                        f"{comment} 绪论引用 [Severity: Major] [Priority: P1]: [Script] "
                        f"B4 近期文献占比不足（目标：近三年 >={RECENT3_SHARE_TARGET:.0%}、"
                        f"近五年 >={RECENT5_SHARE_TARGET:.0%}）。",
                        f"{comment} 建议：每个主题簇按“奠基文献 1~2 篇 + 近三年文献 2~3 篇”补位，"
                        "从本地 .bib 检索候选，不可编造。",
                        f"{comment} 理由：多校规范要求近五年文献不少于 1/3 且必须包含近两年文献；"
                        "缺近期文献会被质疑综述未跟进前沿。",
                        "",
                    ]
                )
        else:
            out.append(
                f"{comment} 绪论引用 [Severity: Info] [Priority: P3]: [Script] "
                "B4 绪论引用键均未在 bib 中匹配到年份，无法统计分布——请确认 --bib 指向正确文件。"
            )
    else:
        out.append(
            f"{comment} 绪论引用 [Severity: Info] [Priority: P3]: [Script] "
            "B4 未提供 --bib，跳过年份分布统计（提供后可输出近三年/近五年占比）。"
        )

    # B5：可视化收束。
    if occurrences and not _has_visual_summary(lines, start, end):
        out.extend(
            [
                f"{comment} 绪论引用（{_zh_loc(start, end)}）[Severity: Minor] [Priority: P2]: "
                "[Script] B5 研究现状范围内未发现总结性表格或图示。",
                f"{comment} 建议：补一张研究演进时间线图（年代轴+阶段分期）或文献对比矩阵表"
                "（方法/假设/适用范围/局限），并在小节末尾用一段收束。",
                f"{comment} 理由：纯段落推进的综述难以呈现研究路线，图表化归纳是评审的普遍期望。",
                "",
            ]
        )

    out.append(
        f"{comment} 选文配比提示：每个主题簇 = 奠基文献 1~2 篇 + 近三年文献 2~3 篇，"
        "中外来源均衡；同一团队多篇拆开比较着写。阈值以本校规范为准。"
    )
    return out


def main() -> int:
    cli = argparse.ArgumentParser(description="中文学位论文文献综述分析")
    cli.add_argument("file", type=Path, help="目标 .tex/.typ 文件")
    cli.add_argument(
        "--section",
        default="related",
        help="指定分析章节，默认 related",
    )
    cli.add_argument(
        "--intro-citations",
        action="store_true",
        help="运行绪论引用诊断（B1~B5：数量/堆引/扎堆/年份分布/可视化收束），忽略 --section",
    )
    cli.add_argument("--bib", type=Path, help="参考文献 .bib 路径（B4 年份分布需要）")
    cli.add_argument(
        "--min-cites",
        type=int,
        default=DEFAULT_INTRO_MIN_CITES,
        help=f"绪论唯一引用数下限（默认 {DEFAULT_INTRO_MIN_CITES}，博士档）",
    )
    cli.add_argument(
        "--max-cites",
        type=int,
        default=DEFAULT_INTRO_MAX_CITES,
        help=f"绪论唯一引用数常见上限（默认 {DEFAULT_INTRO_MAX_CITES}，超出仅提示）",
    )
    cli.add_argument(
        "--current-year",
        type=int,
        default=None,
        help="年份分布的基准年（默认取系统当前年份；测试或补写旧稿时可覆盖）",
    )
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[错误] 文件未找到: {args.file}", file=sys.stderr)
        return 1

    if args.intro_citations:
        if args.bib is not None and not args.bib.exists():
            print(f"[错误] bib 文件未找到: {args.bib}", file=sys.stderr)
            return 1
        print(
            "\n".join(
                analyze_intro_citations(
                    args.file,
                    bib_path=args.bib,
                    min_cites=args.min_cites,
                    max_cites=args.max_cites,
                    current_year=args.current_year,
                )
            )
        )
        return 0

    print("\n".join(analyze(args.file, args.section)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
