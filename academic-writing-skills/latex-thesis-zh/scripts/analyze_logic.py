#!/usr/bin/env python3
"""
逻辑与方法论分析器 — 中文学位论文版本

检查：段落级逻辑衔接、标题后导语完整性、方法论论证、
文献综述质量（A1/A3）、跨章节逻辑链闭合（C3）。
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from parsers import extract_abstract, get_parser, resolve_section_keys
    from tex_loader import AssembledDocument, assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import extract_abstract, get_parser, resolve_section_keys
    from tex_loader import AssembledDocument, assemble


# 当前装配文档（由 analyze() 设置），让深层 helper 的行号输出能定位到源文件。
_DOC: AssembledDocument | None = None


def _zh_loc(start: int, end: int | None = None) -> str:
    """行号定位：单文件 ``第15行``/``第15-20行``，多文件 ``chapters/x.tex:15``。"""
    if _DOC is not None:
        return _DOC.lineref(start, end)
    if end is not None and end != start:
        return f"第{start}-{end}行"
    return f"第{start}行"


def _l_loc(line_no: int) -> str:
    """L## 风格定位（动机主线诊断用）。"""
    if _DOC is not None and _DOC.multi_file:
        src, src_line = _DOC.origin(line_no)
        return f"{src}:{src_line}"
    return f"L{line_no}"


TRANSITIONS_ZH = {
    "递进": {"此外", "进一步", "更重要的是", "不仅如此", "同时"},
    "转折": {"然而", "但是", "相反", "尽管如此", "不过"},
    "因果": {"因此", "由此可见", "故而", "所以", "从而"},
}


def _has_transition_zh(text: str) -> bool:
    return any(token in text for values in TRANSITIONS_ZH.values() for token in values)


def _needs_method_justification_zh(text: str) -> bool:
    if "本文采用" not in text and "本文使用" not in text and "我们采用" not in text:
        return False
    return not any(m in text for m in ["因为", "由于", "鉴于", "考虑到", "基于", "原因"])


# ── 文献综述质量检查 (A1, A3) ──────────────────────────────────

AUTHOR_ENUM_ZH = re.compile(
    r"^.*?[（(]\d{4}[)）].*?(?:提出|引入|设计|开发|采用|构建|建立)",
)

GAP_KEYWORDS_ZH = re.compile(
    r"(研究空白|不足|然而.*?尚未|仍然.*?(?:挑战|困难)|有待|缺乏|"
    r"尚未解决|亟待|亟需|鲜有研究|未能充分)",
)


def _check_lit_review_enumeration(lines: list[str], start: int, end: int, parser) -> list[str]:
    """A1: 检测3条及以上连续的作者/年份罗列模式。"""
    out: list[str] = []
    consecutive = 0
    streak_start = 0
    comment_prefix = parser.get_comment_prefix()
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            continue
        if AUTHOR_ENUM_ZH.search(visible):
            if consecutive == 0:
                streak_start = line_no
            consecutive += 1
        else:
            if consecutive >= 3:
                out.extend(
                    [
                        f"% 文献综述（{_zh_loc(streak_start, line_no - 1)}）"
                        "[Severity: Major] [Priority: P1]: "
                        f"检测到作者/年份罗列模式（连续{consecutive}条）",
                        "% 建议：按研究主题分组，组内进行批判性对比分析。",
                        "% 理由：按时间或作者罗列文献会削弱文献综述的综合深度。",
                        "",
                    ]
                )
            consecutive = 0
    if consecutive >= 3:
        out.extend(
            [
                f"% 文献综述（{_zh_loc(streak_start, min(end, len(lines)))}）"
                "[Severity: Major] [Priority: P1]: "
                f"检测到作者/年份罗列模式（连续{consecutive}条）",
                "% 建议：按研究主题分组，组内进行批判性对比分析。",
                "% 理由：按时间或作者罗列文献会削弱文献综述的综合深度。",
                "",
            ]
        )
    return out


def _check_gap_derivation(lines: list[str], start: int, end: int, parser) -> list[str]:
    """A3: 检查相关工作末尾是否包含研究空白描述。"""
    out: list[str] = []
    scan_start = max(start, end - 10)
    comment_prefix = parser.get_comment_prefix()
    found_gap = False
    for line_no in range(scan_start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and GAP_KEYWORDS_ZH.search(visible):
            found_gap = True
            break
    if not found_gap:
        out.extend(
            [
                f"% 文献综述（{_zh_loc(scan_start, end)}）"
                "[Severity: Major] [Priority: P1]: "
                "相关工作末尾未发现研究空白推导",
                "% 建议：添加明确的研究空白陈述，连接文献综述与本文贡献。",
                "% 理由：相关工作应以识别研究空白作为结尾，为本研究提供动机。",
                "",
            ]
        )
    return out


# ── 跨章节逻辑链闭合 (C3) ──────────────────────────────────────

CONTRIBUTION_KEYWORDS_ZH = re.compile(
    r"(本文提出|本文的贡献|本文设计|本文开发|主要贡献|本研究提出|本文构建)",
)
ANSWER_KEYWORDS_ZH = re.compile(
    r"(本文证明了|实验表明|结果表明|本文提出了|验证了|证实了|研究发现)",
)

LEAD_EXEMPT_TITLES_ZH = (
    "摘要",
    "abstract",
    "参考文献",
    "bibliography",
    "致谢",
    "附录",
    "目录",
    "contents",
)
LEAD_STRUCTURAL_COMMANDS = (
    r"\chapter",
    r"\section",
    r"\subsection",
    r"\subsubsection",
    r"\paragraph",
    r"\begin{figure",
    r"\begin{table",
    r"\begin{equation",
    r"\begin{align",
    r"\begin{itemize",
    r"\begin{enumerate",
    r"\item",
)
LEAD_GUIDE_KEYWORDS_ZH = (
    "本章",
    "本节",
    "本部分",
    "本小节",
    "本小章",
    "本段",
    "下面",
    "首先",
    "然后",
    "最后",
    "具体",
    "围绕",
    "从而",
)
INTRO_BACKGROUND_RE_ZH = re.compile(r"(背景|需求|近年来|应用|场景|行业|领域|现实)")
INTRO_PROBLEM_RE_ZH = re.compile(r"(问题|挑战|瓶颈|局限|不足|困难|代价高|尚未解决)")
INTRO_PRIOR_RE_ZH = re.compile(r"(现有|已有|既有|前人|相关工作|文献|已有研究|然而|但是)")
TRIAD_PROBLEM_RE_ZH = re.compile(r"(问题|挑战|任务|目标|瓶颈|局限|研究问题)")
TRIAD_METHOD_RE_ZH = re.compile(r"(提出|设计|构建|方法|框架|模型|机制|策略)")
TRIAD_RESULT_RE_ZH = re.compile(r"(结果表明|实验表明|研究发现|提升|优于|准确率|召回率|性能|基准)")
TRIAD_CONTRIBUTION_RE_ZH = re.compile(r"(贡献|创新点|本文提出|主要贡献|本研究提出|独特之处)")
CHAPTER_BRIDGE_KEYWORDS_ZH = (
    "基于上一章",
    "承接上一章",
    "在上一章基础上",
    "在前文基础上",
    "进一步",
    "针对尚未解决",
    "围绕上述问题",
    "为解决上述问题",
    "延续前文",
)

# ── 正文章引言（承上启下两段式）专项检查 ─────────────────────
#
# 与 S1 通用导语检查互补：S1 管“标题后有没有导语”，本检查管正文章引言
# 是否符合“承上启下、约两段”的学位论文约定。绪论第 1 章不在此范围，由
# _check_introduction_funnel 负责，故按标题显式排除，避免重复诊断。

# 启下：本章要做什么（与“本章/本节”同现时视为已交代本章任务）。
CHAPTER_PREVIEW_KEYWORDS_ZH = (
    "提出",
    "设计",
    "研究",
    "介绍",
    "给出",
    "描述",
    "构建",
    "分析",
    "讨论",
    "综述",
    "围绕",
    "组织",
    "安排",
    "结构",
    "展开",
    "分为",
)
# 启下：路标式预告（无需与“本章”同现即成立）。
CHAPTER_ROADMAP_KEYWORDS_ZH = (
    "组织如下",
    "安排如下",
    "结构如下",
    "本章组织",
    "本章安排",
    "本章结构",
    "首先",
    "其次",
    "随后",
    "接着",
    "最后",
    "余下",
    "本章其余",
)
# 相对指代：规范建议改用章节号。
RELATIVE_REF_PATTERNS_ZH = (
    "上一章",
    "下一章",
    "前一章",
    "后一章",
    "上一节",
    "下一节",
    "上文",
    "下文",
)
CHAPTER_NUM_REF_RE = re.compile(r"第\s*\d+\s*章")
SECTION_NUM_PREVIEW_RE = re.compile(r"\d+\.\d+\s*节")
# 章引言豁免标题（在 LEAD_EXEMPT_TITLES_ZH 之外，额外排除绪论与收尾章）。
CHAPTER_INTRO_EXEMPT_TITLES_ZH = (
    "绪论",
    "引言",
    "结论",
    "总结",
    "展望",
)
CHAPTER_INTRO_MIN_CHARS = 40
CHAPTER_INTRO_MAX_CHARS = 900


def _section_visible_lines(
    lines: list[str], bounds: tuple[int, int], parser
) -> list[tuple[int, str]]:
    visible_lines: list[tuple[int, str]] = []
    comment_prefix = parser.get_comment_prefix()
    start, end = bounds
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible:
            visible_lines.append((line_no, visible))
    return visible_lines


def _coverage_map_zh(text: str) -> dict[str, bool]:
    return {
        "problem": bool(TRIAD_PROBLEM_RE_ZH.search(text)),
        "method": bool(TRIAD_METHOD_RE_ZH.search(text)),
        "result": bool(TRIAD_RESULT_RE_ZH.search(text) or re.search(r"\d+(?:\.\d+)?%?", text)),
        "contribution": bool(TRIAD_CONTRIBUTION_RE_ZH.search(text)),
    }


def _check_introduction_funnel(
    lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    out: list[str] = []
    if "introduction" not in sections:
        return out

    visible_lines = _section_visible_lines(lines, sections["introduction"], parser)
    if len(visible_lines) < 3:
        return out

    first_problem = first_prior = first_contribution = None
    for line_no, visible in visible_lines:
        if first_problem is None and INTRO_PROBLEM_RE_ZH.search(visible):
            first_problem = line_no
        if first_prior is None and (
            INTRO_PRIOR_RE_ZH.search(visible) or "\\cite{" in lines[line_no - 1]
        ):
            first_prior = line_no
        if first_contribution is None and CONTRIBUTION_KEYWORDS_ZH.search(visible):
            first_contribution = line_no

    if first_contribution is None:
        return out

    if first_problem is None or first_contribution < first_problem:
        out.extend(
            [
                f"% 绪论结构（{_zh_loc(first_contribution)}）[Severity: Major] [Priority: P1]: "
                "绪论可能从背景直接跳到本文方案，缺少技术瓶颈铺垫",
                "% 建议：先明确主流方法解决不了什么，再提出本文研究问题或方法。",
                "% 理由：绪论应按背景→瓶颈→前人不足→本文工作的漏斗链展开。",
                "",
            ]
        )

    if first_problem is not None and first_prior is None:
        out.extend(
            [
                f"% 绪论结构（{_zh_loc(first_problem)}）[Severity: Major] [Priority: P1]: "
                "绪论提出了问题，但没有从前人工作不足推导该问题",
                "% 建议：补充已有工作的尝试与局限，再落到本文研究动机。",
                "% 理由：只有问题没有前人不足，会让研究动机显得突兀。",
                "",
            ]
        )
    elif (
        first_problem is not None
        and first_prior is not None
        and first_contribution is not None
        and first_prior > first_contribution
    ):
        out.extend(
            [
                f"% 绪论结构（{_zh_loc(first_contribution)}）[Severity: Major] [Priority: P1]: "
                "本文工作出现在前人不足之前，绪论漏斗链顺序可能错误",
                "% 建议：先交代已有方法的不足，再引出本文方法。",
                "% 理由：研究问题和方法应建立在明确的文献缺口之上。",
                "",
            ]
        )
    return out


def _check_tri_section_alignment(
    content: str, lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    out: list[str] = []
    if "conclusion" not in sections:
        return out

    abstract_text = extract_abstract(content)
    if not abstract_text:
        return out

    contribution_key = "contribution" if "contribution" in sections else "introduction"
    if contribution_key not in sections:
        return out

    contribution_text = " ".join(
        text for _, text in _section_visible_lines(lines, sections[contribution_key], parser)
    )
    conclusion_text = " ".join(
        text for _, text in _section_visible_lines(lines, sections["conclusion"], parser)
    )
    if not contribution_text or not conclusion_text:
        return out

    coverage = {
        "abstract": _coverage_map_zh(abstract_text),
        "contribution_source": _coverage_map_zh(contribution_text),
        "conclusion": _coverage_map_zh(conclusion_text),
    }
    required_facets = {
        facet
        for facet in ("problem", "method", "result", "contribution")
        if sum(1 for sec in coverage.values() if sec[facet]) >= 2
    }
    mismatches: list[str] = []
    for section_name, section_coverage in coverage.items():
        missing = sorted(facet for facet in required_facets if not section_coverage[facet])
        if len(missing) >= 2 or (
            section_name in {"abstract", "conclusion"}
            and ("result" in missing or "contribution" in missing)
        ):
            mismatches.append(f"{section_name} 缺少 {', '.join(missing)}")

    if coverage["contribution_source"]["contribution"]:
        if not coverage["abstract"]["contribution"]:
            mismatches.append("abstract 缺少贡献表述")
        if not coverage["conclusion"]["contribution"]:
            mismatches.append("conclusion 缺少贡献回应")
    if coverage["abstract"]["method"] and not coverage["conclusion"]["result"]:
        mismatches.append("conclusion 缺少结果支撑")

    if mismatches:
        out.extend(
            [
                "% 跨章节一致性 [Severity: Major] [Priority: P1]: 摘要、创新点/贡献来源、结论之间可能存在错位",
                f"% 观察：{'；'.join(mismatches)}。",
                "% 建议：三处都要围绕研究问题、方法、核心结果、增量贡献形成对应关系。",
                "% 理由：摘要、创新点与结论应长得像但不应各说各话。",
                "",
            ]
        )
    return out


def _check_chapter_mainline(content: str, lines: list[str], parser) -> list[str]:
    """Check whether major chapters are bridged into one thesis storyline."""
    out: list[str] = []
    headings = [h for h in parser.extract_headings(content) if h["level"] == 1]
    if len(headings) < 3:
        return out

    substantive = [
        h
        for h in headings
        if not _is_exempt_heading(h["title"])
        and "结论" not in h["title"]
        and "总结" not in h["title"]
    ]
    if len(substantive) < 3:
        return out

    missing_bridges: list[str] = []
    for heading in substantive[1:]:
        start_line = heading["line"] + 1
        lead_text = ""
        for line_no in range(start_line, min(start_line + 8, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            kind = _classify_lead_gap(raw)
            if kind in {"empty", "comment", "structural"}:
                continue
            visible = parser.extract_visible_text(raw)
            if visible:
                lead_text = visible
                break
        if not lead_text:
            continue
        has_bridge = any(keyword in lead_text for keyword in CHAPTER_BRIDGE_KEYWORDS_ZH)
        generic_chapter_open = lead_text.startswith("本章") or lead_text.startswith("本文")
        if not has_bridge and generic_chapter_open:
            missing_bridges.append(f"{heading['title']}（{_zh_loc(heading['line'])}）")

    if len(missing_bridges) >= 2:
        out.extend(
            [
                "% 章节主线 [Severity: Major] [Priority: P1]: 多个核心章节缺少与前章结论的桥接，整体主线可能偏向工作罗列",
                f"% 观察：{', '.join(missing_bridges)} 的开头未明确承接上一章或说明递进关系。",
                "% 建议：在章节引言或本章小结中显式写出“基于上一章……本章进一步……”。",
                "% 理由：学位论文需要体现递进或并列互补的系统性，而不是可任意换序的工作堆砌。",
                "",
            ]
        )
    return out


def _is_chapter_intro_exempt(title: str) -> bool:
    """章引言检查的豁免标题：在通用导语豁免之外，再排除绪论与收尾章。"""
    if _is_exempt_heading(title):
        return True
    normalized = title.strip()
    return any(token in normalized for token in CHAPTER_INTRO_EXEMPT_TITLES_ZH)


def _chapter_intro_gap(line: int, title: str, observe: str, suggest: str) -> list[str]:
    """承上/启下缺失的统一输出（Major/P1，[Script]）。"""
    return [
        f"% 章引言（{_zh_loc(line)}）[Severity: Major] [Priority: P1]: [Script] 第“{title}”章{observe}",
        f"% 建议：{suggest}",
        "% 理由：正文章引言应承上启下——承接前章、引出本章问题与各节安排，是论文主线的关节。",
        "",
    ]


def _check_chapter_intro(content: str, lines: list[str], parser) -> list[str]:
    """正文章引言（承上启下两段式）专项检查。

    仅作用于正文章（level-1 标题，排除绪论/引言/结论/总结/展望及摘要等），
    且该章须含至少一个下级小节——否则“预告各节安排”无从谈起，交给 S1 与
    _check_chapter_mainline。与 S1 互补：S1 管“有没有导语”，本检查管承上、
    启下、相对指代与篇幅是否符合章引言约定。绪论由 _check_introduction_funnel 负责。
    """
    out: list[str] = []
    headings = parser.extract_headings(content)
    chapters = [h for h in headings if h["level"] == 1]
    if not chapters:
        return out

    body_chapters = [c for c in chapters if not _is_chapter_intro_exempt(c["title"])]
    if not body_chapters:
        return out

    for order, chapter in enumerate(body_chapters):
        title = chapter["title"]
        is_first_body = order == 0

        # 本章范围：章标题行 -> 下一个 level-1 标题（或文末）。
        next_chapter_line = next(
            (h["line"] for h in headings if h["level"] == 1 and h["line"] > chapter["line"]),
            None,
        )
        chapter_end = (next_chapter_line - 1) if next_chapter_line else len(lines)

        # 本章首个下级小节（level >= 2）。无小节则跳过本章。
        first_section_line = next(
            (
                h["line"]
                for h in headings
                if chapter["line"] < h["line"] <= chapter_end and h["level"] >= 2
            ),
            None,
        )
        if first_section_line is None:
            continue

        # 章引言块 = 章标题行+1 .. 首个小节行-1 的可见正文。
        intro_parts: list[str] = []
        for line_no in range(chapter["line"] + 1, min(first_section_line - 1, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if _classify_lead_gap(raw) in {"empty", "comment", "structural"}:
                continue
            visible = parser.extract_visible_text(raw)
            if visible:
                intro_parts.append(visible)
        intro_text = " ".join(intro_parts)
        intro_len = len(intro_text.replace(" ", ""))

        bridge_suggest = (
            "在章引言第一段用章节号回顾前一章解决了什么、得出什么结论，引出本章为何继续。"
        )
        preview_suggest = "在章引言第二段说明本章针对什么问题、核心思想，必要时预告本章各节安排。"

        # 空章引言：承上（非首个正文章）+ 启下均缺失。
        if not intro_text:
            if not is_first_body:
                out.extend(
                    _chapter_intro_gap(
                        chapter["line"],
                        title,
                        "章引言缺少承上衔接：未承接前一章结论或说明递进关系",
                        bridge_suggest,
                    )
                )
            out.extend(
                _chapter_intro_gap(
                    chapter["line"],
                    title,
                    "章引言缺少启下：未说明本章要解决的问题、思路或各节安排",
                    preview_suggest,
                )
            )
            continue

        # 承上：桥接词 / 第X章 / 相对指代 任一即视为有承上尝试（相对指代另行提示措辞）。
        has_relative_ref = any(p in intro_text for p in RELATIVE_REF_PATTERNS_ZH)
        has_bridge = (
            any(k in intro_text for k in CHAPTER_BRIDGE_KEYWORDS_ZH)
            or CHAPTER_NUM_REF_RE.search(intro_text) is not None
            or has_relative_ref
        )
        if not has_bridge and not is_first_body:
            out.extend(
                _chapter_intro_gap(
                    chapter["line"],
                    title,
                    "章引言缺少承上衔接：未承接前一章结论或说明递进关系",
                    bridge_suggest,
                )
            )

        # 启下：路标预告，或“本章 + 任务动词”说明本章要做什么。
        has_roadmap = (
            any(k in intro_text for k in CHAPTER_ROADMAP_KEYWORDS_ZH)
            or SECTION_NUM_PREVIEW_RE.search(intro_text) is not None
        )
        has_chapter_action = "本章" in intro_text and any(
            k in intro_text for k in CHAPTER_PREVIEW_KEYWORDS_ZH
        )
        if not has_roadmap and not has_chapter_action:
            out.extend(
                _chapter_intro_gap(
                    chapter["line"],
                    title,
                    "章引言缺少启下：未说明本章要解决的问题、思路或各节安排",
                    preview_suggest,
                )
            )

        # 相对指代（规范：用章节号）。
        if has_relative_ref:
            hit = next(p for p in RELATIVE_REF_PATTERNS_ZH if p in intro_text)
            out.extend(
                [
                    f"% 章引言（{_zh_loc(chapter['line'])}）[Severity: Minor] [Priority: P2]: "
                    f"[Script] 第“{title}”章章引言使用相对指代“{hit}”",
                    "% 建议：改用章节号（如“第2章”）指代，避免“上一章/上文”这类相对表述。",
                    "% 理由：学位论文规范建议用章节编号指代，便于非线性阅读与精确定位。",
                    "",
                ]
            )

        # 篇幅：过简 / 过长（约定 1~2 段、约 300~500 字）。
        if intro_len < CHAPTER_INTRO_MIN_CHARS:
            out.extend(
                [
                    f"% 章引言（{_zh_loc(chapter['line'])}）[Severity: Minor] [Priority: P2]: "
                    f"[Script] 第“{title}”章章引言过简（约{intro_len}字）",
                    "% 建议：扩展为承上启下两段——先承接前章，再交代本章问题、思路与各节安排。",
                    "% 理由：章引言一般为 1~2 个自然段、约 300~500 字，过简难以承担承上启下。",
                    "",
                ]
            )
        elif intro_len > CHAPTER_INTRO_MAX_CHARS:
            out.extend(
                [
                    f"% 章引言（{_zh_loc(chapter['line'])}）[Severity: Minor] [Priority: P2]: "
                    f"[Script] 第“{title}”章章引言过长（约{intro_len}字）",
                    "% 建议：将具体方法/实验细节下沉到对应小节，章引言保留承上启下两段。",
                    "% 理由：章引言应是简短导览，过长会与正文小节重复并稀释主线。",
                    "",
                ]
            )

    return out


def _check_cross_section_closure(
    lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    """C3: 验证绪论中的贡献声明在结论中得到回应。"""
    out: list[str] = []
    if "introduction" not in sections or "conclusion" not in sections:
        return out

    intro_start, intro_end = sections["introduction"]
    concl_start, concl_end = sections["conclusion"]
    comment_prefix = parser.get_comment_prefix()

    intro_claims = 0
    for line_no in range(intro_start, min(intro_end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and CONTRIBUTION_KEYWORDS_ZH.search(visible):
            intro_claims += 1

    if intro_claims == 0:
        return out

    concl_answers = 0
    for line_no in range(concl_start, min(concl_end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and ANSWER_KEYWORDS_ZH.search(visible):
            concl_answers += 1

    if concl_answers == 0:
        out.extend(
            [
                f"% 逻辑衔接（{_zh_loc(concl_start, concl_end)}）"
                "[Severity: Major] [Priority: P1]: "
                "[Script] 跨章节逻辑链可能不完整",
                f"% 观察：绪论中有{intro_claims}处贡献声明，但结论中未发现明确回应。",
                "% 建议：在结论中添加明确回应每项贡献的陈述。",
                "% 理由：结论应当闭合绪论中开启的逻辑链。",
                "",
            ]
        )
    return out


def _is_exempt_heading(title: str) -> bool:
    normalized = title.strip().lower()
    return any(token in normalized for token in LEAD_EXEMPT_TITLES_ZH)


def _classify_lead_gap(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return "empty"
    if stripped.startswith("%") or stripped.startswith("//"):
        return "comment"
    if any(stripped.startswith(token) for token in LEAD_STRUCTURAL_COMMANDS):
        return "structural"
    return "text"


def _check_heading_leads(content: str, lines: list[str], parser) -> list[str]:
    """检查标题后是否先给出导语段落，而不是直接跳入结构元素。"""
    out: list[str] = []
    headings = parser.extract_headings(content)
    if not headings:
        return out

    for index, heading in enumerate(headings):
        title = heading["title"]
        if _is_exempt_heading(title):
            continue

        start_line = heading["line"] + 1
        end_line = headings[index + 1]["line"] - 1 if index + 1 < len(headings) else len(lines)
        if start_line > end_line:
            out.extend(
                [
                    f"% 结构衔接（{_zh_loc(heading['line'])}）[Severity: Major] [Priority: P1]: "
                    f"标题“{title}”后未发现导语段落",
                    "% 建议：在标题后先用一段导语交代本层级的研究对象、写作目的和行文安排。",
                    "% 理由：标题后直接结束或切到下一级标题，会导致结构展开过于突兀。",
                    "",
                ]
            )
            continue

        first_text_line = None
        first_structural_line = None
        first_text = ""
        for line_no in range(start_line, min(end_line, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            kind = _classify_lead_gap(raw)
            if kind in {"empty", "comment"}:
                continue
            if kind == "structural":
                first_structural_line = line_no
                break

            visible = parser.extract_visible_text(raw)
            if visible:
                first_text_line = line_no
                first_text = visible
                break

        if first_text_line is None:
            reason = (
                f"标题后直接进入结构元素（{_zh_loc(first_structural_line)}）"
                if first_structural_line
                else "标题后未发现可见正文"
            )
            out.extend(
                [
                    f"% 结构衔接（{_zh_loc(heading['line'])}）[Severity: Major] [Priority: P1]: "
                    f"标题“{title}”后缺少导语段落",
                    f"% 观察：{reason}。",
                    "% 建议：先补一段完整导语，再进入列表、图表、公式或下一级标题。",
                    "% 理由：章节、小节和四级标题展开时应先说明本段写什么、为何写、如何组织。",
                    "",
                ]
            )
            continue

        is_short = len(first_text) < 18
        has_guide_signal = any(keyword in first_text for keyword in LEAD_GUIDE_KEYWORDS_ZH)
        if heading["level"] <= 4 and is_short and not has_guide_signal:
            out.extend(
                [
                    f"% 结构衔接（{_zh_loc(first_text_line)}）[Severity: Minor] [Priority: P2]: "
                    f"标题“{title}”后的导语可能过短",
                    f"% 原文: {first_text}",
                    "% 建议：扩展为一段完整导语，交代本层级内容范围、与上文关系及展开顺序。",
                    "% 理由：过短句子难以承担章节导入和逻辑承接功能。",
                    "",
                ]
            )
    return out


# ── 动机主线闭合诊断（可选开关：--motivation-thread）──
#
# 只读诊断：把绪论的每条承诺/主张映射到后文的呼应位置。它是启发式的
# （关键词 + 词面重叠），每条结论都标 [Script] 并提示人工复核，与上面的
# 跨章节（C3）检查口吻一致，绝不改写源文件。

_THREAD_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "for",
    "with",
    "via",
    "that",
    "this",
    "these",
    "those",
    "from",
    "into",
    "onto",
    "our",
    "ours",
    "their",
    "such",
    "more",
    "most",
    "than",
    "then",
    "thus",
    "also",
    "which",
    "while",
    "where",
    "when",
    "paper",
    "work",
    "study",
    "propose",
    "proposed",
    "present",
    "presents",
    "presented",
    "introduce",
    "introduces",
    "method",
    "methods",
    "approach",
    "approaches",
    "model",
    "models",
    "framework",
    "results",
    "result",
    "show",
    "shows",
    "shown",
    "using",
    "used",
    "based",
    "novel",
    "new",
    "main",
    "contribution",
    "contributions",
    "achieve",
    "achieves",
    "improve",
    "improves",
    "improvement",
    "demonstrate",
    "demonstrates",
}


def _thread_tokens(text: str) -> set[str]:
    """用于重叠匹配的内容 token：英文词（>=4 字符、非停用词）+ 中文字符二元组，
    使启发式在中英混排文本上也能工作。"""
    lowered = text.lower()
    tokens: set[str] = set()
    for word in re.findall(r"[a-z][a-z'-]{3,}", lowered):
        if word not in _THREAD_STOPWORDS:
            tokens.add(word)
    for run in re.findall(r"[一-鿿]{2,}", lowered):
        for i in range(len(run) - 1):
            tokens.add(run[i : i + 2])
    return tokens


def _thread_best_match(
    promise_tokens: set[str], candidates: list[tuple[int, str]], min_overlap: int = 2
) -> tuple[int, int] | None:
    """返回重叠度最高的候选行 (行号, 重叠数)，没有达到阈值则返回 None。"""
    best_line = None
    best_score = 0
    for line_no, text in candidates:
        overlap = len(promise_tokens & _thread_tokens(text))
        if overlap > best_score:
            best_score = overlap
            best_line = line_no
    if best_line is not None and best_score >= min_overlap:
        return best_line, best_score
    return None


_THREAD_INTRO_KW = ("introduction", "绪论", "引言")
_THREAD_RELATED_KW = ("related", "literature review", "文献综述", "相关工作")
_THREAD_CLOSURE_KW = (
    "discussion",
    "analysis",
    "conclusion",
    "讨论",
    "分析",
    "结论",
    "总结",
    "展望",
)
_LATEX_HEADING_RE = re.compile(r"\\(?:chapter|(?:sub)*section|paragraph)\*?\s*\{([^}]*)\}")
_TYPST_HEADING_RE = re.compile(r"^=+\s+(.*)$")


def _thread_headings(lines: list[str], parser) -> list[tuple[int, str]]:
    """通用标题扫描，返回 (行号, 小写标题)。

    与 parser 的已知章节关键词表不同，这里把任意标题都视为边界，因此常见的
    复数/复合标题（'Experiments'、'Experimental Results'、'Results and
    Discussion'）仍能正确切出证据正文区。仅由可选的动机主线诊断使用，其它逻辑
    不依赖它。
    """
    is_typst = parser.get_comment_prefix() == "//"
    heads: list[tuple[int, str]] = []
    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        match = _TYPST_HEADING_RE.match(stripped) if is_typst else _LATEX_HEADING_RE.match(stripped)
        if match:
            heads.append((i, match.group(1).strip().lower()))
    return heads


def _check_motivation_thread(
    lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    """全篇红线诊断：承诺映射 + 闭合映射。

    承诺映射：绪论的每条承诺（"本文提出 X"）-> 实验/结果中可能验证它的一行。
    闭合映射：绪论的每条主张 -> 讨论/结论中可能回应它的一行。
    """
    p = parser.get_comment_prefix()
    out: list[str] = []
    heads = _thread_headings(lines, parser)
    intro_pos = next(
        (idx for idx, (_, title) in enumerate(heads) if any(k in title for k in _THREAD_INTRO_KW)),
        None,
    )
    if intro_pos is None and "introduction" not in sections:
        return [f"{p} 动机主线 [Script]：未找到绪论，跳过红线诊断。"]

    if intro_pos is not None:
        intro_line = heads[intro_pos][0]
        intro_end = heads[intro_pos + 1][0] - 1 if intro_pos + 1 < len(heads) else len(lines)
    else:
        intro_line, intro_end = sections["introduction"]

    closure_line = next(
        (
            ln
            for ln, title in heads
            if ln > intro_end and any(k in title for k in _THREAD_CLOSURE_KW)
        ),
        None,
    )
    related_ranges: list[tuple[int, int]] = []
    for j, (ln, title) in enumerate(heads):
        if any(k in title for k in _THREAD_RELATED_KW):
            end = heads[j + 1][0] - 1 if j + 1 < len(heads) else len(lines)
            related_ranges.append((ln, end))

    promises = [
        (ln, txt)
        for ln, txt in _section_visible_lines(lines, (intro_line, intro_end), parser)
        if CONTRIBUTION_KEYWORDS_ZH.search(txt)
    ]
    evidence_end = closure_line - 1 if closure_line else len(lines)
    evidence_lines = [
        (ln, txt)
        for ln, txt in _section_visible_lines(lines, (intro_end + 1, evidence_end), parser)
        if not any(lo <= ln <= hi for lo, hi in related_ranges)
    ]
    closure_lines = (
        _section_visible_lines(lines, (closure_line, len(lines)), parser) if closure_line else []
    )

    out.append(f"{p} 动机主线 [Script]（启发式）：全篇红线闭合诊断。")
    out.append(f"{p} 说明：基于关键词 + 词面重叠的启发式，可能误报，请人工复核。")
    out.append("")

    # ── 承诺映射 ──
    out.append(f"{p} 动机主线：承诺映射（绪论承诺 -> 实验/结果证据）")
    if not promises:
        out.append(
            f"{p} - 绪论中未检测到明确的“本文提出/贡献”承诺 [Severity: Moderate] [Priority: P2]。"
        )
    else:
        for idx, (ln, txt) in enumerate(promises[:10], 1):
            if not evidence_lines:
                out.append(
                    f"{p} - P{idx}（绪论 {_l_loc(ln)}）-> [未找到正文证据] "
                    "[Severity: Major] [Priority: P1]：绪论与结论之间没有正文"
                )
                continue
            match = _thread_best_match(_thread_tokens(txt), evidence_lines)
            if match:
                out.append(
                    f"{p} - P{idx}（绪论 {_l_loc(ln)}）-> 证据 {_l_loc(match[0])} "
                    f"[已匹配, overlap={match[1]}]"
                )
            else:
                out.append(
                    f"{p} - P{idx}（绪论 {_l_loc(ln)}）-> [未找到证据] [Severity: Major] [Priority: P1]："
                    "承诺未在实验/结果中验证"
                )
                out.append(f"{p}   承诺: {txt[:100]}")
    out.append("")

    # ── 闭合映射 ──
    out.append(f"{p} 动机主线：闭合映射（绪论主张 -> 讨论/结论收口）")
    if not promises:
        out.append(f"{p} - 没有可闭合的明确主张。")
    elif not closure_lines:
        out.append(f"{p} - [缺少讨论/结论章节] [Severity: Major] [Priority: P1]：主张无法闭合。")
    else:
        for idx, (ln, txt) in enumerate(promises[:10], 1):
            match = _thread_best_match(_thread_tokens(txt), closure_lines)
            if match:
                out.append(
                    f"{p} - C{idx}（绪论 {_l_loc(ln)}）-> 收口 {_l_loc(match[0])} "
                    f"[已闭合, overlap={match[1]}]"
                )
            else:
                out.append(
                    f"{p} - C{idx}（绪论 {_l_loc(ln)}）-> [未闭合] [Severity: Major] [Priority: P1]："
                    "主张未在讨论/结论中回应"
                )
    out.append("")

    # ── 游离证据（轻量、限量）──
    if promises and evidence_lines:
        promise_union: set[str] = set()
        for _, txt in promises:
            promise_union |= _thread_tokens(txt)
        orphans = [
            (ln, txt)
            for ln, txt in evidence_lines
            if TRIAD_RESULT_RE_ZH.search(txt)
            and re.search(r"\d", txt)
            and not (_thread_tokens(txt) & promise_union)
        ]
        if orphans:
            out.append(f"{p} 动机主线：游离证据（结果无法追溯到任一绪论承诺）")
            for ln, txt in orphans[:5]:
                out.append(
                    f"{p} - 证据 {_l_loc(ln)} [Severity: Moderate] [Priority: P2]: {txt[:90]}"
                )
            out.append("")
    return out


def analyze(
    file_path: Path,
    section: str | None = None,
    cross_section: bool = False,
    motivation_thread: bool = False,
) -> list[str]:
    global _DOC
    parser = get_parser(file_path)
    doc = assemble(file_path)
    _DOC = doc
    content = doc.content
    lines = doc.lines
    sections = parser.split_sections(content)
    comment_prefix = parser.get_comment_prefix()
    warn = doc.warning_lines(comment_prefix)

    matched_keys: list[str] = []
    if section:
        matched_keys, available = resolve_section_keys(section, sections)
        if not matched_keys:
            avail = ", ".join(available) if available else "（本文档未识别出任何已知章节）"
            return warn + [
                f"% ERROR [Severity: Critical] [Priority: P0]: 未找到章节: {section}",
                f"% 可用章节: {avail}",
                "% 提示：--section 同时接受英文键（introduction/related/...）与中文章节名（绪论/相关工作/...）。",
            ]
        ranges = [sections[k] for k in matched_keys]
    else:
        ranges = list(sections.values()) if sections else [(1, len(lines))]

    out: list[str] = list(warn)
    previous_visible = ""
    for start, end in ranges:
        for line_no in range(start, min(end, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if not raw or raw.startswith(comment_prefix):
                continue

            visible = parser.extract_visible_text(raw)
            if not visible:
                continue

            if _needs_method_justification_zh(visible):
                out.extend(
                    [
                        f"% 方法论深度（{_zh_loc(line_no)}）[Severity: Major] [Priority: P1]: "
                        "方法选择缺乏论证",
                        f"% 原文: {visible}",
                        "% 建议：添加选择理由（如效率/准确率/可复现性）。",
                        "% 理由：方法选择应说明为何采用该方案。",
                        "",
                    ]
                )

            if (
                previous_visible
                and not _has_transition_zh(visible)
                and any(k in previous_visible for k in ["问题", "挑战", "困难", "噪声"])
                and any(k in visible for k in ["本文提出", "本文设计", "我们的方法"])
            ):
                out.extend(
                    [
                        f"% 逻辑衔接（{_zh_loc(line_no)}）[Severity: Major] [Priority: P1]: "
                        "问题与解决方案间可能存在逻辑跳跃",
                        f"% 原文: {visible}",
                        '% 建议：添加显式过渡（如"因此"、"为解决上述问题"）。',
                        "% 理由：增强段落间的逻辑连贯性。",
                        "",
                    ]
                )

            previous_visible = visible

    # ── 章节级检查 ─────────────────────────────────────────────
    if not section:
        out.extend(_check_heading_leads(content, lines, parser))
        out.extend(_check_chapter_mainline(content, lines, parser))
        out.extend(_check_chapter_intro(content, lines, parser))

    if sections:
        # 漏斗检查：全文档模式或显式 --section introduction/绪论 时执行
        if "introduction" in sections and (not section or "introduction" in matched_keys):
            out.extend(_check_introduction_funnel(lines, sections, parser))

        related_keys = [k for k in sections if k == "related" or k.startswith("related_")]
        for related_key in related_keys:
            if not section or related_key in matched_keys:
                r_start, r_end = sections[related_key]
                out.extend(_check_lit_review_enumeration(lines, r_start, r_end, parser))
                out.extend(_check_gap_derivation(lines, r_start, r_end, parser))

        # C3 闭合已并入默认全文档模式（--cross-section 保留为兼容开关）。
        if not section:
            out.extend(_check_cross_section_closure(lines, sections, parser))
            out.extend(_check_tri_section_alignment(content, lines, sections, parser))
        if motivation_thread and not section:
            out.extend(_check_motivation_thread(lines, sections, parser))

    if len(out) == len(warn):
        out.append("% 逻辑/方法论：未检测到规则级逻辑问题。")
    return out


def main() -> int:
    cli = argparse.ArgumentParser(description="中文学位论文逻辑与方法论分析")
    cli.add_argument("file", type=Path, help="目标 .tex/.typ 文件")
    cli.add_argument(
        "--section", help="指定分析章节（接受英文键或中文章节名，如 introduction/绪论）"
    )
    cli.add_argument(
        "--cross-section",
        action="store_true",
        help="（兼容开关）C3 跨章节闭合检查已并入默认全文档模式，此选项保留以兼容旧命令",
    )
    cli.add_argument(
        "--motivation-thread",
        action="store_true",
        help="运行全篇动机红线诊断（承诺映射 + 闭合映射）",
    )
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[错误] 文件未找到: {args.file}", file=sys.stderr)
        return 1

    print("\n".join(analyze(args.file, args.section, args.cross_section, args.motivation_thread)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
