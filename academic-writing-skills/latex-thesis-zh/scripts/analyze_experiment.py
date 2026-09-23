#!/usr/bin/env python3
"""
Experiment analysis helper for Chinese LaTeX thesis and journals.

Supports two modes:
- Prompt generation: format raw data into LLM prompt (original behavior)
- Review analysis: check discussion depth, literature echo, conclusion completeness
"""

import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

try:
    from parsers import SECTION_KEY_ALIASES, get_parser
    from tex_loader import AssembledDocument, assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import SECTION_KEY_ALIASES, get_parser
    from tex_loader import AssembledDocument, assemble


# 当前装配文档（由 analyze() 设置），供 _format_issue 输出 源文件:行号。
_DOC: AssembledDocument | None = None


# ── Prompt generation (original) ───────────────────────────────


def generate_request(input_data: str) -> str:
    path = Path(input_data)
    if path.exists() and path.is_file():
        content = path.read_text(encoding="utf-8", errors="ignore")
    else:
        content = input_data

    prompt = [
        "### 中文实验分析生成请求 (Experiment Analysis Request)",
        "请根据以下原始数据或草稿，生成符合中文顶刊与学位论文标准的完美实验分析段落。",
        "务必严格遵守 `references/modules/experiment.md` 中的所有约束条件。",
        "",
        "#### 规范要点提醒:",
        "- 强制使用 `\\paragraph{核心结论概括}` 引导段落。",
        "- 正文中**禁止**任何 `\\textbf{}` 等显式加粗。",
        "- **禁止**使用列表环境 (`\\begin{itemize}`) 罗列数据，需串联成连贯的论述段落。",
        "- 包含 SOTA 对比、消融结论，并确保具有深度的比较逻辑而不仅是报数字。",
        "- 极致客观、去口语化，严禁出现\u201c碾压、遥遥领先\u201d等夸张词汇及主观代词。",
        "",
        "#### 原始数据 / 打点草稿:",
        content,
        "",
        "#### 输出格式:",
        "% EXPERIMENT ANALYSIS DRAFT",
        "% [Insert LaTeX paragraph here]",
    ]
    return "\n".join(prompt)


# ── Review analysis (B3, B4, B5) ──────────────────────────────

SECTION_ALIASES = {
    "experiment": "experiment",
    "experiments": "experiment",
    "result": "result",
    "results": "result",
    "discussion": "discussion",
    "conclusion": "conclusion",
}

ATTRIBUTION_MARKERS_ZH = re.compile(
    r"(原因|机制|表明|解释为|归因于|导致|由于|之所以|这是因为|根本原因|"
    r"本质上|究其原因|可能是因为)",
)
DISCUSSION_CATEGORY_MARKERS_ZH = {
    "mechanism": re.compile(r"(原因|机制|解释|归因于|由于|之所以|本质上|究其原因)"),
    "comparison": re.compile(r"(相比|相较于|与.*相比|前人工作|已有研究|基线|文献)"),
    "limitation": re.compile(r"(局限|不足|边界|失效|代价|受限于|仍存在)"),
    "implication": re.compile(r"(启示|应用价值|实际意义|展望|未来工作|后续研究|推广)"),
}

CITE_KEY_RE = re.compile(r"\\(?:cite\w*)\*?(?:\[[^\]]*\]\s*)*\{([^}]*)\}")

CONCLUSION_FINDINGS_ZH = re.compile(
    r"(本文证明了|实验表明|结果表明|本文提出了|研究发现|关键发现|主要结果)",
)
CONCLUSION_IMPLICATIONS_ZH = re.compile(
    r"(启示|应用价值|实际意义|使.*成为可能|推动|促进|有助于|实践意义)",
)
CONCLUSION_LIMITATIONS_ZH = re.compile(
    r"(局限|不足|展望|未来工作|有待|进一步研究|改进方向|后续工作)",
)


# ── Per-method-chapter experiment checks (E-* family, R4b) ────────
#
# Industrial process theses use a "one method per chapter + in-chapter
# experiment" layout with no global discussion/related chapter, so the B3/B4
# checks above never fire. These heuristics walk each body chapter, locate its
# experiment and framework sections, and flag structural gaps. Every finding is
# tagged [Script]; line numbers point at the hit or the section head. Patterns
# are module-level constants so they can be tuned per discipline convention.

# Front/back-matter and survey chapters excluded from method-chapter checks.
NON_METHOD_CHAPTER_RE = re.compile(r"绪论|引言|结论|总结|展望|综述")
# Experiment-section locator (the in-chapter validation region).
EXP_SEC_RE = re.compile(r"实验|案例研究|仿真验证|结果(?:及|与)?分析|应用验证")
# Method/design-section locator.
METHOD_SEC_RE = re.compile(r"方法|模型|建模|框架|策略|算法|设计")
# E-FIG requires an overview figure only for framework/structure-named design
# sections; textbook theory sections (无框架/结构/策略/方案) stay exempt.
FRAMEWORK_SEC_RE = re.compile(r"框架|结构|策略|方案")

# E-DATA: data-description clues (source + train/test split).
DATA_SOURCE_RE = re.compile(r"数据|样本|工况")
DATA_SPLIT_RE = re.compile(r"训练|测试|验证集|划分|\d+\s*[:：/]\s*\d+")
# E-PARAM: parameter-setting clues.
PARAM_RE = re.compile(r"参数设置|超参|学习率|迭代次数|表[^。\n]{0,6}参数")
# E-ABL: ablation / mechanism-decomposition clues.
ABLATION_RE = re.compile(r"消融|拆解|变体|去除.{0,6}模块|单独(?:使用|验证)")
# E-METRIC: metric acronyms that should be defined by a formula on first use.
METRIC_TERM_RE = re.compile(
    r"(?<![A-Za-z])(?:RMSE|sMAPE|MAPE|MAE|MSE|R2|R²|ISE|IAE|ITAE|FAR|FDR|IGD|HV|GD)(?![A-Za-z])"
)

# Results-analysis (RA-*) uses its own vocabulary and thresholds so the existing
# E-METRIC behavior remains byte-for-byte independent from the opt-in family.
RA_METRIC_TERM_RE = re.compile(
    r"(?<![A-Za-z])(?:RMSE|sMAPE|MAPE|MAE|MSE|R2|R²|ISE|IAE|ITAE|FAR|FDR|IGD|HV|GD|"
    r"KS|W1|MMD|SWD|C2ST|ACF|PSD|AUC)(?![A-Za-z])"
)
RA_FIDELITY_TERM_RE = re.compile(r"(?<![A-Za-z])(?:KS|W1|MMD|SWD|C2ST|ACF|PSD)(?![A-Za-z])")
RA_EQUIV_ASSERT_RE = re.compile(r"统计(?:上)?等价|与[^，。！？]{0,8}等价")
RA_EQUIV_MATH_RE = re.compile(r"等价(?:类|变换|形式|转换|于下式)")
RA_EQUIV_EVIDENCE_RE = re.compile(r"等价检验|等效性检验|TOST|等价包络|等价界")
RA_CAUSAL_RE = re.compile(
    r"主要归因于|归功于|保证了|确保了|由[^，。！？]{1,12}(?:带来|贡献|驱动)|"
    r"(?:提升|改善|增益)(?:完全|全部|均)?来自"
)
RA_CAUSAL_NOUN_RE = re.compile(r"归因分析|误差归因")
RA_CONSISTENCY_RE = re.compile(r"与.{0,12}(?:一致|相符)|支持.{0,12}关联")
RA_COMPONENT_EVIDENCE_RE = re.compile(
    r"消融|拆解|变体|去除.{0,6}模块|单独(?:使用|验证)|组件记录|中间输出|"
    r"逐项(?:移除|添加)|受控对比"
)
RA_COMPARE_CONTEXT_RE = re.compile(r"基线|对比方法|各(?:模型|方法)")
RA_BEST_CLAIM_RE = re.compile(r"最优|最低|最高|优于")
RA_SECOND_BEST_RE = re.compile(r"次优|第二|仅次于|次佳|最接近的(?:基线|方法)")
RA_SHALLOW_RE = re.compile(
    r"更(?:加)?贴合|更(?:加)?吻合|基本一致|基本吻合|箱体更小|"
    r"曲线更(?:平滑|接近|贴近)|效果(?:更|较)好|明显(?:更|较)好"
)
RA_BOX_RE = re.compile(r"箱线|箱型|箱式")
RA_DISTRIBUTION_RE = re.compile(r"中位数|四分位|上须|下须|离群|尾部|最大(?:绝对)?误差")
RA_UNIVERSAL_RE = re.compile(
    r"(?:在)?(?:所有|全部|各项|全体)(?:指标|子集|工况)(?:上|中)?(?:均|都|皆)?"
    r"(?:优于|领先|最优)|全面(?:优于|领先)|一致优于"
)
RA_CONCESSION_RE = re.compile(r"除|但|然而|反转|并未")
RA_STAGE_SELECTED_RE = re.compile(r"选定集|筛选后")
RA_STAGE_GENERATED_RE = re.compile(r"生成样本|原始候选|合成样本")
RA_STAGE_NORMATIVE_RE = re.compile(r"不得|不能|避免|不应|应统一|简称|外推|区别于|不同于|注意")
RA_TRANSITION_RE = re.compile(
    r"下一(?:章|节|小节)|后续(?:实验|章节)|第[0-9一二三四五六七八九]+章|"
    r"[0-9]+\.[0-9]+\s*节|据此"
)
RA_SUMMARY_HEADING_RE = re.compile(r"\\(?:sub)*section\*?(?:\[[^]]*\])?\{[^}]*小结[^}]*\}")
RA_SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?；;])\s*|\n+")
RA_HEADING_LINE_RE = re.compile(
    r"^\\(?:chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^]]*\])?\{"
)
EQUATION_ENV_RE = re.compile(r"\\begin\{(?:equation|align|eqnarray|gather|multline)\*?\}")
METRIC_REUSE_RE = re.compile(r"[0-9]\.[0-9]\s*节")
# E-REF / E-FIG: cross-reference probes on raw text (extract_visible_text blanks refs).
REF_TAB_RE = re.compile(r"\\ref\{tab:")
REF_FIG_RE = re.compile(r"\\ref\{fig:")
# E-ECHO: chapter-2 framework echo (textual back-reference or cross-chapter \ref).
CH2_ECHO_RE = re.compile(r"第[2二]章")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
REF_TARGET_RE = re.compile(r"\\(?:ref|eqref|autoref)\{([^}]*)\}")

# E-ATTR reuses the B3 attribution word list (ATTRIBUTION_MARKERS_ZH). A per-chapter
# "结果分析" region can run to hundreds of lines dominated by figure/table/number
# description, so a flat 15% line-ratio is unreachable even for the well-attributed
# "描述→定量比较→机理归因" pattern (measured 2.5–3.6% on a high-quality thesis).
# The real failure mode is a laundry list with near-absent attribution, so the ratio
# guard is paired with an absolute floor: flag only when both the ratio is low AND
# fewer than ATTR_MIN_HITS attribution lines exist. Minimum-lines guard lowered to 3.
ATTR_MIN_LINES = 3
ATTR_RATIO = 0.15
ATTR_MIN_HITS = 3


def _format_issue(line_no: int, severity: str, priority: str, message: str) -> list[str]:
    loc = _DOC.lineref_en(line_no) if _DOC is not None else f"Line {line_no}"
    return [f"% EXPERIMENT ({loc}) [Severity: {severity}] [Priority: {priority}]: {message}"]


def _normalize_section(section: str | None) -> str | None:
    if not section:
        return None
    raw = section.strip()
    normalized = SECTION_ALIASES.get(raw.lower())
    if normalized:
        return normalized
    # 中文章节名（实验/讨论/结论 等）同样可用
    return SECTION_KEY_ALIASES.get(raw, SECTION_KEY_ALIASES.get(raw.lower(), raw.lower()))


def _check_discussion_depth(lines: list[str], start: int, end: int, parser) -> list[str]:
    """B3: Check ratio of explanatory lines in discussion."""
    out: list[str] = []
    total_visible = 0
    attribution_lines = 0

    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            continue
        total_visible += 1
        if ATTRIBUTION_MARKERS_ZH.search(visible):
            attribution_lines += 1

    if total_visible >= 5 and attribution_lines / total_visible < 0.15:
        out.extend(
            _format_issue(
                start,
                "Major",
                "P1",
                "Discussion may lack depth: low ratio of explanatory/attribution "
                f"language ({attribution_lines}/{total_visible} lines).",
            )
        )
        out.append("")
    return out


def _check_discussion_structure(lines: list[str], start: int, end: int, parser) -> list[str]:
    """Check whether discussion covers multiple argumentative categories."""
    out: list[str] = []
    visible_lines: list[str] = []
    category_hits = dict.fromkeys(DISCUSSION_CATEGORY_MARKERS_ZH, 0)

    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            continue
        visible_lines.append(visible)
        for name, pattern in DISCUSSION_CATEGORY_MARKERS_ZH.items():
            if pattern.search(visible):
                category_hits[name] += 1

    if len(visible_lines) < 6:
        return out

    covered_categories = [name for name, count in category_hits.items() if count > 0]
    if len(covered_categories) < 2:
        out.extend(
            _format_issue(
                start,
                "Major",
                "P1",
                "Discussion may lack layered structure: it should separately cover mechanism, prior-work comparison, limitations/boundaries, or implications/outlook.",
            )
        )
        out.append("")
    return out


def _extract_cite_keys_in_range(lines: list[str], start: int, end: int) -> set[str]:
    """Extract citation keys from lines in range."""
    keys: set[str] = set()
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1]
        for match in CITE_KEY_RE.finditer(raw):
            for key in match.group(1).split(","):
                k = key.strip()
                if k:
                    keys.add(k)
    return keys


def _check_results_literature_echo(
    lines: list[str],
    sections: dict[str, tuple[int, int]],
) -> list[str]:
    """B4: Check if Related Work citations reappear in Discussion."""
    out: list[str] = []
    if "related" not in sections or "discussion" not in sections:
        return out

    rel_start, rel_end = sections["related"]
    disc_start, disc_end = sections["discussion"]

    related_keys = _extract_cite_keys_in_range(lines, rel_start, rel_end)
    discussion_keys = _extract_cite_keys_in_range(lines, disc_start, disc_end)

    if related_keys and not related_keys & discussion_keys:
        out.extend(
            _format_issue(
                disc_start,
                "Major",
                "P1",
                "No citations from Related Work reappear in Discussion.",
            )
        )
        out.append("")
    return out


def _check_conclusion_completeness(lines: list[str], start: int, end: int, parser) -> list[str]:
    """B5: Conclusion must contain findings + implications + limitations."""
    out: list[str] = []
    section_text = ""
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if visible:
            section_text += " " + visible

    if not section_text.strip():
        return out

    if not CONCLUSION_LIMITATIONS_ZH.search(section_text):
        out.extend(
            _format_issue(start, "Major", "P1", "Conclusion lacks limitations or future work.")
        )
        out.append("")
    if not CONCLUSION_IMPLICATIONS_ZH.search(section_text):
        out.extend(_format_issue(start, "Minor", "P2", "Conclusion lacks implications statement."))
        out.append("")
    if not CONCLUSION_FINDINGS_ZH.search(section_text):
        out.extend(
            _format_issue(start, "Minor", "P2", "Conclusion lacks explicit core findings summary.")
        )
        out.append("")
    return out


def _range_raw(lines: list[str], start: int, end: int, parser) -> str:
    """Join the non-comment raw lines in [start, end] (1-based, inclusive)."""
    prefix = parser.get_comment_prefix()
    kept = [
        lines[ln - 1]
        for ln in range(start, min(end, len(lines)) + 1)
        if not lines[ln - 1].strip().startswith(prefix)
    ]
    return "\n".join(kept)


def _attribution_ratio(lines: list[str], start: int, end: int, parser) -> tuple[int, int]:
    """Return (attribution_lines, visible_lines) for [start, end], mirroring B3."""
    total = 0
    attr = 0
    for ln in range(start, min(end, len(lines)) + 1):
        raw = lines[ln - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            continue
        total += 1
        if ATTRIBUTION_MARKERS_ZH.search(visible):
            attr += 1
    return attr, total


def _section_intervals(headings: list, ch_start: int, ch_end: int) -> list[dict]:
    """Level-2 (\\section) ranges within a chapter [ch_start, ch_end]."""
    secs = [h for h in headings if h["level"] == 2 and ch_start <= h["line"] <= ch_end]
    intervals: list[dict] = []
    for i, h in enumerate(secs):
        end = secs[i + 1]["line"] - 1 if i + 1 < len(secs) else ch_end
        intervals.append({"title": h["title"], "start": h["line"], "end": end})
    return intervals


# ── Opt-in results-analysis checks (RA-* family) ──────────────


def _visible_range(lines: list[str], start: int, end: int, parser) -> str:
    prefix = parser.get_comment_prefix()
    visible: list[str] = []
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(prefix) or RA_HEADING_LINE_RE.match(raw):
            continue
        text = parser.extract_visible_text(raw)
        if text:
            visible.append(text)
    return "\n".join(visible)


def _visible_line_count(lines: list[str], start: int, end: int, parser) -> int:
    return len(_visible_range(lines, start, end, parser).splitlines())


def _make_ra_interval(
    lines: list[str],
    parser,
    *,
    start: int,
    end: int,
    chapter_start: int,
    chapter_end: int,
    source: str,
    key: str | None = None,
    chapter_has_summary: bool = False,
) -> dict:
    return {
        "start": start,
        "end": end,
        "chapter_start": chapter_start,
        "chapter_end": chapter_end,
        "source": source,
        "key": key,
        "chapter_has_summary": chapter_has_summary,
        "visible_lines": _visible_line_count(lines, start, end, parser),
    }


def _collect_results_intervals(
    lines: list[str], content: str, parser, section: str | None = None
) -> list[dict]:
    """Collect results/discussion intervals with chapter-context ownership."""
    sections = parser.split_sections(content)
    normalized = _normalize_section(section)
    chapter_ranges = parser.chapter_ranges(content)

    def owning_chapter_has_summary(start: int) -> bool:
        for chapter in chapter_ranges:
            if chapter["start"] <= start <= chapter["end"]:
                chapter_raw = _range_raw(lines, chapter["start"], chapter["end"], parser)
                return bool(RA_SUMMARY_HEADING_RE.search(chapter_raw))
        return False

    if normalized:
        family = re.compile(rf"^{re.escape(normalized)}(?:_\d+)?$")
        return [
            _make_ra_interval(
                lines,
                parser,
                start=start,
                end=end,
                chapter_start=start,
                chapter_end=end,
                source="global",
                key=key,
                chapter_has_summary=owning_chapter_has_summary(start),
            )
            for key, (start, end) in sections.items()
            if family.fullmatch(key)
        ]

    headings = parser.extract_headings(content)
    normalize_title = getattr(parser, "normalize_heading_title", None)
    chapter_intervals: list[dict] = []
    for chapter in chapter_ranges:
        title = chapter["title"]
        if callable(normalize_title):
            title = normalize_title(title)
        if NON_METHOD_CHAPTER_RE.search(str(title)):
            continue
        chapter_start = chapter["start"]
        chapter_end = chapter["end"]
        for candidate in _section_intervals(headings, chapter_start, chapter_end):
            if not EXP_SEC_RE.search(candidate["title"]):
                continue
            chapter_intervals.append(
                _make_ra_interval(
                    lines,
                    parser,
                    start=candidate["start"],
                    end=candidate["end"],
                    chapter_start=chapter_start,
                    chapter_end=chapter_end,
                    source="chapter",
                    chapter_has_summary=owning_chapter_has_summary(candidate["start"]),
                )
            )

    global_family = re.compile(r"^(?:discussion|result)(?:_\d+)?$")
    global_intervals = [
        _make_ra_interval(
            lines,
            parser,
            start=start,
            end=end,
            chapter_start=start,
            chapter_end=end,
            source="global",
            key=key,
            chapter_has_summary=owning_chapter_has_summary(start),
        )
        for key, (start, end) in sections.items()
        if global_family.fullmatch(key)
    ]

    kept = list(chapter_intervals)
    for candidate in global_intervals:
        overlaps_chapter = any(
            candidate["start"] <= item["end"] and item["start"] <= candidate["end"]
            for item in chapter_intervals
        )
        if not overlaps_chapter:
            kept.append(candidate)
    return sorted(kept, key=lambda item: (item["start"], item["end"]))


def _split_ra_paragraphs(lines: list[str], start: int, end: int, parser) -> list[dict]:
    """Split prose into raw/visible paragraph triples without losing LaTeX refs."""
    paragraphs: list[dict] = []
    block: list[tuple[int, str]] = []
    prefix = parser.get_comment_prefix()

    def flush() -> None:
        if not block:
            return
        visible = [parser.extract_visible_text(raw) for _line_no, raw in block]
        visible_text = " ".join(part for part in visible if part).strip()
        if visible_text:
            paragraphs.append(
                {
                    "start_line": block[0][0],
                    "raw_text": "\n".join(raw for _line_no, raw in block),
                    "visible_text": visible_text,
                }
            )
        block.clear()

    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1]
        stripped = raw.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith(prefix):
            continue
        if RA_HEADING_LINE_RE.match(stripped):
            flush()
            continue
        block.append((line_no, raw))
    flush()
    return paragraphs


def _ra_sentences(text: str) -> list[str]:
    return [part.strip() for part in RA_SENTENCE_SPLIT_RE.split(text) if part.strip()]


def _ra_finding(line_no: int, severity: str, priority: str, code: str, detail: str) -> list[str]:
    message = f"[Script] {code}（启发式线索，须 LLM 按证据阶梯复核）：{detail}"
    return [*_format_issue(line_no, severity, priority, message), ""]


def _check_ra_equiv(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del interval, chapter_window_raw
    if RA_EQUIV_EVIDENCE_RE.search(chapter_window_visible):
        return []
    out: list[str] = []
    for paragraph in paragraphs:
        unsupported = any(
            RA_EQUIV_ASSERT_RE.search(sentence) and not RA_EQUIV_MATH_RE.search(sentence)
            for sentence in _ra_sentences(paragraph["visible_text"])
        )
        if unsupported:
            out.extend(
                _ra_finding(
                    paragraph["start_line"],
                    "Major",
                    "P1",
                    "RA-EQUIV",
                    "出现等价断言，但章级窗口未见等价检验、TOST 或等价界线索。",
                )
            )
    return out


def _check_ra_causal(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del interval, chapter_window_raw
    out: list[str] = []
    chapter_has_evidence = bool(RA_COMPONENT_EVIDENCE_RE.search(chapter_window_visible))
    for index, paragraph in enumerate(paragraphs):
        unsupported = any(
            RA_CAUSAL_RE.search(sentence)
            and not RA_CAUSAL_NOUN_RE.search(sentence)
            and not RA_CONSISTENCY_RE.search(sentence)
            for sentence in _ra_sentences(paragraph["visible_text"])
        )
        if not unsupported:
            continue
        local = " ".join(
            item["visible_text"]
            for item in paragraphs[max(0, index - 1) : min(len(paragraphs), index + 2)]
        )
        # Parent design §3.1: local evidence suppresses; chapter-only evidence downgrades.
        if RA_COMPONENT_EVIDENCE_RE.search(local):
            continue
        # defensive-ai-rhetoric boundary: multi-mechanism + terminal caveat remains llm-only.
        if chapter_has_evidence:
            severity, priority = "Minor", "P2"
            detail = "章内存在组件证据但未绑定到该论断对象，需核对证据与归因对象是否同指。"
        else:
            severity, priority = "Major", "P1"
            detail = "因果谓词附近及章级窗口均未见消融、受控对比或组件记录线索。"
        out.extend(_ra_finding(paragraph["start_line"], severity, priority, "RA-CAUSAL", detail))
    return out


def _check_ra_secondbest(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del chapter_window_raw, chapter_window_visible
    if interval["visible_lines"] < 8 or not REF_TAB_RE.search(interval["raw_text"]):
        return []
    interval_visible = " ".join(paragraph["visible_text"] for paragraph in paragraphs)
    if (
        RA_COMPARE_CONTEXT_RE.search(interval_visible)
        and RA_BEST_CLAIM_RE.search(interval_visible)
        and not RA_SECOND_BEST_RE.search(interval_visible)
    ):
        return _ra_finding(
            interval["start"],
            "Minor",
            "P2",
            "RA-SECONDBEST",
            "表格比较中出现最优断言，但未点名真实次优方法或最接近基线。",
        )
    return []


def _check_ra_shallow(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del interval, chapter_window_raw, chapter_window_visible
    out: list[str] = []
    for paragraph in paragraphs:
        raw = paragraph["raw_text"]
        visible = paragraph["visible_text"]
        if (
            REF_FIG_RE.search(raw)
            and RA_SHALLOW_RE.search(visible)
            and not re.search(r"\d", visible)
            and not RA_METRIC_TERM_RE.search(visible)
        ):
            out.extend(
                _ra_finding(
                    paragraph["start_line"],
                    "Minor",
                    "P2",
                    "RA-SHALLOW",
                    "图引用附近仅见贴合或效果描述，未见数字或指标定位。",
                )
            )
    return out


def _check_ra_distvocab(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del interval, chapter_window_raw, chapter_window_visible
    out: list[str] = []
    for index, paragraph in enumerate(paragraphs):
        if not RA_BOX_RE.search(paragraph["visible_text"]):
            continue
        current_and_next = " ".join(
            item["visible_text"] for item in paragraphs[index : min(index + 2, len(paragraphs))]
        )
        if not RA_DISTRIBUTION_RE.search(current_and_next):
            out.extend(
                _ra_finding(
                    paragraph["start_line"],
                    "Minor",
                    "P2",
                    "RA-DISTVOCAB",
                    "箱线分析当前段及后一段未区分误差主体与尾部统计。",
                )
            )
    return out


def _check_ra_universal(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del interval, chapter_window_raw, chapter_window_visible
    out: list[str] = []
    for paragraph in paragraphs:
        for sentence in _ra_sentences(paragraph["visible_text"]):
            if RA_UNIVERSAL_RE.search(sentence) and not RA_CONCESSION_RE.search(sentence):
                out.extend(
                    _ra_finding(
                        paragraph["start_line"],
                        "Info",
                        "P3",
                        "RA-UNIVERSAL",
                        "出现全称优势断言，需对照各指标和子集核对排序反转。",
                    )
                )
                break
    return out


def _check_ra_stage(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del chapter_window_raw
    if len(set(RA_FIDELITY_TERM_RE.findall(chapter_window_visible))) < 2:
        return []
    statements: list[tuple[int, int, str]] = []
    for paragraph in paragraphs:
        for sentence in _ra_sentences(paragraph["visible_text"]):
            # Parent design §3.1: normative statements are compliance evidence, not mixed naming.
            if not RA_STAGE_NORMATIVE_RE.search(sentence):
                statements.append((len(statements), paragraph["start_line"], sentence))
    selected = [
        (statement_id, line_no, text)
        for statement_id, line_no, text in statements
        if RA_STAGE_SELECTED_RE.search(text)
    ]
    generated = [
        (statement_id, line_no, text)
        for statement_id, line_no, text in statements
        if RA_STAGE_GENERATED_RE.search(text)
    ]
    if (
        selected
        and generated
        and any(
            selected_id != generated_id
            for selected_id, _selected_line, _selected_text in selected
            for generated_id, _generated_line, _generated_text in generated
        )
    ):
        return _ra_finding(
            min(selected[0][1], generated[0][1]),
            "Info",
            "P3",
            "RA-STAGE",
            "同一区间在不同陈述句中混用选定集与生成样本命名。",
        )
    return []


def _check_ra_transition(
    paragraphs: list[dict], interval: dict, chapter_window_raw: str, chapter_window_visible: str
) -> list[str]:
    del chapter_window_raw, chapter_window_visible
    # Parent design §3.2 red line 9: summary presence is ownership metadata only;
    # it must not widen a global/--section evidence window beyond the interval.
    if not paragraphs or interval["chapter_has_summary"]:
        return []
    last = paragraphs[-1]
    if not RA_TRANSITION_RE.search(last["visible_text"]):
        return _ra_finding(
            last["start_line"],
            "Info",
            "P3",
            "RA-TRANSITION",
            "结果分析末段未见本实验结论到下一章、下一节或后续实验的接口线索。",
        )
    return []


RA_CHECKERS = (
    _check_ra_equiv,
    _check_ra_causal,
    _check_ra_secondbest,
    _check_ra_shallow,
    _check_ra_distvocab,
    _check_ra_universal,
    _check_ra_stage,
    _check_ra_transition,
)


def _check_results_analysis(
    lines: list[str], content: str, parser, section: str | None = None
) -> list[str]:
    intervals = _collect_results_intervals(lines, content, parser, section)
    if not intervals:
        return _ra_finding(
            1,
            "Info",
            "P3",
            "RA-STRUCT",
            "未检出结果分析区间；可用 --section 指定实际章节键后重试。",
        )

    out: list[str] = []
    for interval in intervals:
        interval["raw_text"] = _range_raw(lines, interval["start"], interval["end"], parser)
        paragraphs = _split_ra_paragraphs(lines, interval["start"], interval["end"], parser)
        chapter_raw = _range_raw(lines, interval["chapter_start"], interval["chapter_end"], parser)
        chapter_visible = _visible_range(
            lines, interval["chapter_start"], interval["chapter_end"], parser
        )
        for checker in RA_CHECKERS:
            out.extend(checker(paragraphs, interval, chapter_raw, chapter_visible))
    return out


def _check_experiment_chapter(
    lines: list[str], parser, ch_start: int, ch_end: int, secs: list, exp_secs: list
) -> list[str]:
    """Run the E-* heuristics for one method chapter with in-chapter experiments."""
    out: list[str] = []
    chapter_raw = _range_raw(lines, ch_start, ch_end, parser)
    exp_raw = "\n".join(_range_raw(lines, s["start"], s["end"], parser) for s in exp_secs)
    exp_start = exp_secs[0]["start"]

    # E-DATA (Major): missing data-source or train/test split clue.
    if not DATA_SOURCE_RE.search(exp_raw) or not DATA_SPLIT_RE.search(exp_raw):
        out.extend(
            _format_issue(
                exp_start,
                "Major",
                "P1",
                "[Script] E-DATA 实验节缺数据描述要素（数据来源/样本量/训练-测试划分线索不足）。",
            )
        )
        out.append("")

    # E-ATTR (Major): result analysis reports numbers without mechanism attribution.
    attr = total = 0
    for s in exp_secs:
        a, t = _attribution_ratio(lines, s["start"], s["end"], parser)
        attr += a
        total += t
    if total >= ATTR_MIN_LINES and attr < ATTR_MIN_HITS and attr / total < ATTR_RATIO:
        out.extend(
            _format_issue(
                exp_start,
                "Major",
                "P1",
                f"[Script] E-ATTR 实验节归因语言偏少（{attr}/{total} 行含机理归因词），"
                "结果分析或停留在报数字。",
            )
        )
        out.append("")

    # E-REF (Major): analysis text detached from any table/figure.
    if not REF_TAB_RE.search(exp_raw) and not REF_FIG_RE.search(exp_raw):
        out.extend(
            _format_issue(
                exp_start,
                "Major",
                "P1",
                "[Script] E-REF 实验节未引用任何图表（缺 \\ref{tab:...} 与 \\ref{fig:...}），"
                "分析文字与图表脱钩。",
            )
        )
        out.append("")

    # E-FIG (Major): framework/structure design section without an overview figure.
    for s in secs:
        if not (METHOD_SEC_RE.search(s["title"]) and FRAMEWORK_SEC_RE.search(s["title"])):
            continue
        if not REF_FIG_RE.search(_range_raw(lines, s["start"], s["end"], parser)):
            out.extend(
                _format_issue(
                    s["start"],
                    "Major",
                    "P1",
                    "[Script] E-FIG 框架/结构设计节未见总体框架图引用（缺 \\ref{fig:...}）。",
                )
            )
            out.append("")

    # E-METRIC (Minor): metric acronym used but no formula and no cross-section reuse.
    metric = METRIC_TERM_RE.search(exp_raw)
    if (
        metric
        and not EQUATION_ENV_RE.search(chapter_raw)
        and not METRIC_REUSE_RE.search(chapter_raw)
    ):
        out.extend(
            _format_issue(
                exp_start,
                "Minor",
                "P2",
                f"[Script] E-METRIC 出现评价指标（{metric.group(0)}）但本章未给出计算公式，"
                "也无“X.Y 节”复用指涉。",
            )
        )
        out.append("")

    # E-PARAM (Minor): experiment section without parameter-setting clues.
    if not PARAM_RE.search(exp_raw):
        out.extend(
            _format_issue(
                exp_start,
                "Minor",
                "P2",
                "[Script] E-PARAM 实验节缺参数设置线索（参数表/超参交代）。",
            )
        )
        out.append("")

    # E-ABL (Info): no ablation / mechanism-decomposition experiment in the chapter.
    if not ABLATION_RE.search(chapter_raw):
        out.extend(
            _format_issue(
                ch_start,
                "Info",
                "P3",
                "[Script] E-ABL 本章未见消融/机制拆解实验线索。",
            )
        )
        out.append("")

    # E-ECHO (Info): chapter echoes neither the chapter-2 framework nor any
    # cross-chapter label (a \ref whose target is not defined within this chapter).
    labels = set(LABEL_RE.findall(chapter_raw))
    refs = {r for r in REF_TARGET_RE.findall(chapter_raw) if r}
    cross_ref = any(r not in labels for r in refs)
    if not CH2_ECHO_RE.search(chapter_raw) and not cross_ref:
        out.extend(
            _format_issue(
                ch_start,
                "Info",
                "P3",
                "[Script] E-ECHO 全章未回指第2章框架（无“第2章/第二章”表述且无跨章引用）。",
            )
        )
        out.append("")
    return out


def _check_per_chapter(lines: list[str], content: str, parser) -> list[str]:
    """R4b: walk each body method chapter and run the E-* experiment checks."""
    out: list[str] = []
    headings = parser.extract_headings(content)
    total_lines = len(lines)
    chapters = [h for h in headings if h["level"] == 1]
    normalize = getattr(parser, "normalize_heading_title", None)
    for idx, ch in enumerate(chapters):
        ch_start = ch["line"]
        ch_end = chapters[idx + 1]["line"] - 1 if idx + 1 < len(chapters) else total_lines
        title = normalize(ch["title"]) if callable(normalize) else ch["title"]
        if NON_METHOD_CHAPTER_RE.search(str(title)):
            continue
        secs = _section_intervals(headings, ch_start, ch_end)
        exp_secs = [s for s in secs if EXP_SEC_RE.search(s["title"])]
        if not exp_secs:
            continue
        out.extend(_check_experiment_chapter(lines, parser, ch_start, ch_end, secs, exp_secs))
    return out


# Opt-in cross-surface cues. Raw \\ref{tab:} is required; extract_visible_text drops refs.
DEFAULT_XS_METRICS = ("准确率", "精确率", "召回率", "F1", "误差")
DEFAULT_XS_EVAL_SETS = ("测试集", "验证集", "训练集")
_XS_NEGATION_RE = re.compile(r"(?:不使用|没有使用|未使用|不用|而非|不是|并非)$")
_XS_NUMBER_RE = re.compile(
    r"(?:\d{1,3}(?:(?:\\,|[ \u00a0])\d{3})+|\d+)(?:\.\d+)?"
    r"(?:[eE][+-]?\d+|×\s*10\^(?:\{[+-]?\d+\}|[+-]?\d+))?"
)
_XS_INTERVAL_GAP_RE = re.compile(r"^(?:\s*%?\s*)?(?:--|---|\u2013|\u2014|∼|至)(?:\s*%?\s*)?$")
_XS_ENV_BEGIN_RE = re.compile(r"\\begin\{(table\*|table|longtable)\}")


def _load_xs_terms(path: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Load ``{"metrics": [...], "eval_sets": [...]}``. Absent fields keep defaults."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read cross-surface terms: {path.name}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("cross-surface terms must be a JSON object") from exc
    if not isinstance(data, dict):
        raise ValueError("cross-surface terms must be a JSON object")
    if set(data) - {"metrics", "eval_sets"}:
        raise ValueError("cross-surface terms only allows metrics and eval_sets")
    metrics = DEFAULT_XS_METRICS
    eval_sets = DEFAULT_XS_EVAL_SETS
    if "metrics" in data:
        metrics = _xs_string_list(data["metrics"], "metrics")
    if "eval_sets" in data:
        eval_sets = _xs_string_list(data["eval_sets"], "eval_sets")
    return metrics, eval_sets


def _xs_string_list(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{name} must be an array of non-empty strings")
    return tuple(value)


def _xs_finding(line_no: int, code: str, detail: str) -> list[str]:
    message = f"[Script] {code} Meaning-Check: NEEDS-LLM：{detail}"
    return [*_format_issue(max(line_no, 1), "Info", "P3", message), ""]


def _xs_bits(label: str, metric: str, row: str, eval_set: str, unit: str) -> str:
    return f"{label}，指标 {metric}，对象 {row}，评价集 {eval_set}，单位 {unit}"


def _xs_ascii_boundary(text: str, start: int, end: int) -> bool:
    before = text[start - 1] if start else ""
    after = text[end] if end < len(text) else ""
    if before.isascii() and before.isalnum():
        return False
    return not (after.isascii() and after.isalnum())


def _xs_match_terms(text: str, terms: tuple[str, ...], *, positive_only: bool) -> list[str]:
    found: list[str] = []
    occupied = [False] * len(text)
    for term in sorted(set(terms), key=len, reverse=True):
        start = 0
        while True:
            idx = text.find(term, start)
            if idx < 0:
                break
            end = idx + len(term)
            if term.isascii() and not _xs_ascii_boundary(text, idx, end):
                start = idx + 1
                continue
            if any(occupied[idx:end]):
                start = idx + 1
                continue
            for pos in range(idx, end):
                occupied[pos] = True
            window = text[max(0, idx - 8) : idx]
            if not positive_only or not _XS_NEGATION_RE.search(window):
                found.append(term)
            start = end
    return found


_XS_APPROX_BEFORE_RE = re.compile(r"(?:约|约为|大约|近)\s*$")


def _strip_grid_comments(grid: str) -> str:
    """Drop unescaped ``%`` comments per line before the grid is split on ``\\\\`` / ``&``."""
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in grid.splitlines())


def _prepare_measure_text(raw: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", raw)
    text = text.replace("$-$", "-").replace("\\minus", "-").replace("−", "-")
    text = text.replace("\\%", "%").replace("％", "%")
    text = text.replace("\\times", "×").replace("\\sim", "∼")
    text = text.replace("$", "").replace("~", " ")
    text = re.sub(r"\\ref\{tab:[^}]+\}", " ", text)
    text = re.sub(r"\\(?:textbf|mathrm|text|mbox)\{([^{}]*)\}", r"\1", text)
    return text


def _to_decimal(token: str) -> Decimal:
    cleaned = token.replace("\\,", "").replace(" ", "").replace("\u00a0", "")
    cleaned = re.sub(r"×10\^\{([+-]?\d+)\}", r"E\1", cleaned)
    cleaned = re.sub(r"×10\^([+-]?\d+)", r"E\1", cleaned)
    return Decimal(cleaned)


def _xs_blank(kind: str) -> dict[str, Any]:
    return {"kind": kind, "unit": None, "scalar": None, "low": None, "high": None}


def _unit_after(text: str, end: int) -> tuple[str | None, str]:
    rest = text[end:]
    if re.match(r"\s*%", rest):
        return "%", "ok"
    match = re.match(r"\s*([A-Za-z]{1,8})(?![A-Za-z])", rest)
    if not match:
        return None, "ok"
    after = rest[match.end() :]
    if re.match(r"\s*[/·^]", after):
        return match.group(1), "compound"
    return match.group(1), "ok"


def _is_measurement(token: str, unit: str | None, compound: bool) -> bool:
    if unit == "%" or compound or re.search(r"[eE×]", token):
        return True
    if "\\," in token or re.search(r"\d[ \u00a0]\d", token):
        return True
    core = re.split(r"[eE×]", token)[0]
    return "." in core


def _signed_token(text: str, match: re.Match[str]) -> tuple[str, int]:
    """Attach a real sign. ``--`` / ``---`` stay interval connectors, not signs."""
    start = match.start()
    if start >= 3 and text[start - 3 : start] == "---":
        return match.group(0), start
    if start >= 2 and text[start - 2 : start] == "--":
        return match.group(0), start
    if start >= 1 and text[start - 1] in "+-" and not (start >= 2 and text[start - 2] == "-"):
        return text[start - 1] + match.group(0), start - 1
    return match.group(0), start


def _extract_quantities(text: str, *, allow_bare: bool = False) -> list[dict[str, Any]]:
    try:
        matches = list(_XS_NUMBER_RE.finditer(text))
    except (InvalidOperation, ValueError):
        return [_xs_blank("unclear")]
    kept: list[tuple[re.Match[str], str, int, str | None, str]] = []
    bare: list[tuple[re.Match[str], str, int]] = []
    for match in matches:
        token, token_start = _signed_token(text, match)
        unit, flag = _unit_after(text, match.end())
        if not _is_measurement(token, unit, flag == "compound"):
            if flag != "compound" and re.fullmatch(r"[+-]?\d+", token):
                bare.append((match, token, token_start))
            continue
        kept.append((match, token, token_start, unit, flag))
    # A bare integer is a value only when the header or the sentence states % / 无量纲.
    # Other integers stay out so chapter numbers are not measurements.
    if not kept and (allow_bare or "无量纲" in text):
        kept.extend((match, token, token_start, None, "ok") for match, token, token_start in bare)
    if not kept:
        return []
    quantities: list[dict[str, Any]] = []
    index = 0
    try:
        while index < len(kept):
            match, token, token_start, unit, flag = kept[index]
            if flag == "compound":
                return [_xs_blank("compound")]
            if _XS_APPROX_BEFORE_RE.search(text[:token_start]):
                return [_xs_blank("unclear")]
            if index + 1 < len(kept):
                _nxt, token2, token_start2, unit2, flag2 = kept[index + 1]
                gap = text[match.end() : token_start2]
                if _XS_INTERVAL_GAP_RE.fullmatch(gap):
                    if flag2 == "compound" or (unit and unit2 and unit != unit2):
                        return [_xs_blank("unclear")]
                    chosen = unit or unit2 or ("%" if "%" in gap else None)
                    low = _to_decimal(token)
                    high = _to_decimal(token2)
                    if low > high:
                        low, high = high, low
                    quantities.append(
                        {
                            "kind": "interval",
                            "unit": chosen,
                            "scalar": None,
                            "low": low,
                            "high": high,
                        }
                    )
                    index += 2
                    continue
            quantities.append(
                {
                    "kind": "scalar",
                    "unit": unit,
                    "scalar": _to_decimal(token),
                    "low": None,
                    "high": None,
                }
            )
            index += 1
    except (InvalidOperation, ValueError):
        return [_xs_blank("unclear")]
    return quantities


def _same_quantity(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["kind"] != right["kind"] or left["kind"] not in {"scalar", "interval"}:
        return False
    if not left["unit"] or left["unit"] != right["unit"]:
        return False
    if left["kind"] == "scalar":
        return left["scalar"] == right["scalar"]
    return left["low"] == right["low"] and left["high"] == right["high"]


def _apply_unit(quantity: dict[str, Any], inherit: str | None, text: str) -> dict[str, Any]:
    if quantity["unit"]:
        return quantity
    if inherit and inherit != "COMPOUND":
        return {**quantity, "unit": inherit}
    if "无量纲" in text:
        return {**quantity, "unit": "无量纲"}
    return quantity


def _header_unit(header: str, metric: str) -> str | None:
    rest = header.replace(metric, " ")
    if re.search(r"[/·^]", rest):
        return "COMPOUND"
    if "无量纲" in header:
        return "无量纲"
    if "%" in header or "％" in header:
        return "%"
    units = re.findall(r"(?<![A-Za-z])([A-Za-z]{1,8})(?![A-Za-z])", rest)
    if len(units) == 1:
        return units[0]
    if len(units) > 1:
        return "COMPOUND"
    return None


def _column_eval(caption: str, header: str, eval_sets: tuple[str, ...]) -> str | None:
    caption_hits = list(dict.fromkeys(_xs_match_terms(caption, eval_sets, positive_only=True)))
    header_hits = list(dict.fromkeys(_xs_match_terms(header, eval_sets, positive_only=True)))
    if len(header_hits) == 1 and len(caption_hits) == 1 and header_hits[0] != caption_hits[0]:
        return None
    if len(header_hits) == 1:
        return header_hits[0]
    if len(header_hits) == 0 and len(caption_hits) == 1:
        return caption_hits[0]
    return None


def _clean_cell(raw: str) -> str:
    text = _prepare_measure_text(raw)
    text = re.sub(
        r"\\(?:toprule|midrule|bottomrule|hline|endhead|endfoot|endlastfoot)\b\*?",
        " ",
        text,
    )
    text = re.sub(r"\\(?:cline|cmidrule)\*?\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return " ".join(text.split())


def _consume_braced(text: str, open_idx: int) -> tuple[str, int]:
    depth = 0
    for index in range(open_idx, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[open_idx + 1 : index], index + 1
    return text[open_idx + 1 :], len(text)


def _take_command(text: str, command: str) -> tuple[str, list[str]]:
    token = "\\" + command
    out: list[str] = []
    captured: list[str] = []
    cursor = 0
    while True:
        found = text.find(token, cursor)
        if found < 0:
            out.append(text[cursor:])
            break
        out.append(text[cursor:found])
        pos = found + len(token)
        if pos < len(text) and text[pos] == "*":
            pos += 1
        if pos < len(text) and text[pos] == "[":
            depth = 0
            while pos < len(text):
                if text[pos] == "[":
                    depth += 1
                elif text[pos] == "]":
                    depth -= 1
                    if depth == 0:
                        pos += 1
                        break
                pos += 1
        parts: list[str] = []
        while pos < len(text) and text[pos] == "{":
            inner, pos = _consume_braced(text, pos)
            parts.append(inner)
        captured.append("".join(parts))
        cursor = pos
    return "".join(out), captured


def _split_top(text: str, mode: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    index = 0
    while index < len(text):
        if text.startswith("\\,", index) or text.startswith("\\&", index):
            buf.append(text[index : index + 2])
            index += 2
            continue
        if mode == "row" and text.startswith("\\\\", index) and depth == 0:
            parts.append("".join(buf))
            buf = []
            index += 2
            if index < len(text) and text[index] == "*":
                index += 1
            if index < len(text) and text[index] == "[":
                bracket = 0
                while index < len(text):
                    if text[index] == "[":
                        bracket += 1
                    elif text[index] == "]":
                        bracket -= 1
                        if bracket == 0:
                            index += 1
                            break
                    index += 1
            continue
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}" and depth:
            depth -= 1
        if mode == "cell" and char == "&" and depth == 0:
            parts.append("".join(buf))
            buf = []
            index += 1
            continue
        buf.append(char)
        index += 1
    tail = "".join(buf)
    if tail.strip() or not parts:
        parts.append(tail)
    return parts


def _inner_env(raw: str, env: str) -> str:
    match = re.search(rf"\\begin\{{{re.escape(env)}\}}", raw)
    if not match:
        return ""
    pos = match.end()
    if pos < len(raw) and raw[pos] == "[":
        close = raw.find("]", pos)
        pos = close + 1 if close >= 0 else pos
    if pos < len(raw) and raw[pos] == "{":
        _inner, pos = _consume_braced(raw, pos)
    end_match = re.search(rf"\\end\{{{re.escape(env)}\}}", raw[pos:])
    if not end_match:
        return raw[pos:]
    return raw[pos : pos + end_match.start()]


def _matching_env_end(lines: list[str], start: int, name: str) -> int | None:
    depth = 0
    begin = re.compile(rf"\\begin\{{{re.escape(name)}\}}")
    end = re.compile(rf"\\end\{{{re.escape(name)}\}}")
    for index in range(start, len(lines)):
        depth += len(begin.findall(lines[index]))
        depth -= len(end.findall(lines[index]))
        if depth == 0:
            return index
    return None


def _records_from_grid(
    grid: str,
    raw: str,
    start_line: int,
    chapter_start: int,
    metrics: tuple[str, ...],
    eval_sets: tuple[str, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    _bare, captions = _take_command(raw, "caption")
    _bare, bicaps = _take_command(raw, "bicaption")
    _bare, labels = _take_command(raw, "label")
    tab_labels = [item.strip() for item in labels if item.strip().startswith("tab:")]
    if len(tab_labels) != 1:
        return [], []
    caption = " ".join([*captions, *bicaps])
    body = _strip_grid_comments(grid)
    for command in ("caption", "bicaption", "label"):
        body, _captured = _take_command(body, command)
    parsed_rows: list[tuple[list[str], list[str]]] = []
    for row in _split_top(body, "row"):
        raw_cells = _split_top(row, "cell")
        cleaned = [_clean_cell(cell) for cell in raw_cells]
        if any(cleaned):
            parsed_rows.append((raw_cells, cleaned))
    if len(parsed_rows) < 2:
        return [], []
    header = parsed_rows[0][1]
    source = ""
    if _DOC is not None:
        source, _origin_line = _DOC.origin(start_line)
    records: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []

    def skip(row_label: str, metric: str, eval_set: str | None) -> None:
        skips.append(
            {
                "chapter_start": chapter_start,
                "table_label": tab_labels[0],
                "row_label": row_label,
                "metric": metric,
                "eval_set": eval_set,
            }
        )

    for raw_cells, cleaned in parsed_rows[1:]:
        if not cleaned or not cleaned[0]:
            continue
        row_label = cleaned[0]
        for col, header_cell in enumerate(header):
            if col == 0 or col >= len(raw_cells):
                continue
            metric_hits = _xs_match_terms(header_cell, metrics, positive_only=False)
            if len(metric_hits) != 1:
                continue
            metric = metric_hits[0]
            eval_set = _column_eval(caption, header_cell, eval_sets)
            if not eval_set:
                skip(row_label, metric, None)
                continue
            inherit = _header_unit(header_cell, metric)
            if inherit == "COMPOUND":
                skip(row_label, metric, eval_set)
                continue
            prepared = _prepare_measure_text(raw_cells[col])
            quantities = _extract_quantities(prepared, allow_bare=inherit in {"%", "无量纲"})
            if len(quantities) != 1 or quantities[0]["kind"] not in {"scalar", "interval"}:
                skip(row_label, metric, eval_set)
                continue
            quantity = _apply_unit(quantities[0], inherit, header_cell + prepared)
            if quantity["kind"] not in {"scalar", "interval"} or not quantity["unit"]:
                skip(row_label, metric, eval_set)
                continue
            records.append(
                {
                    "source_file": source,
                    "line": start_line,
                    "table_label": tab_labels[0],
                    "row_label": row_label,
                    "column_header": header_cell,
                    "numeric_text": " ".join(raw_cells[col].split()),
                    "metric": metric,
                    "eval_set": eval_set,
                    "unit": quantity["unit"],
                    "quantity": quantity,
                    "chapter_start": chapter_start,
                }
            )
    return records, skips


def _inspect_table(
    raw: str,
    start_line: int,
    env_name: str,
    chapter_start: int,
    metrics: tuple[str, ...],
    eval_sets: tuple[str, ...],
) -> dict[str, Any]:
    label_match = re.search(r"\\label\{(tab:[^}]+)\}", raw)
    label = label_match.group(1) if label_match else ""
    unsupported = bool(re.search(r"\\(?:multicolumn|multirow)\b", raw))
    if env_name in {"table", "table*"}:
        unsupported = unsupported or bool(
            re.search(r"\\begin\{(?:tabular\*|tabularx|tabu|longtable)\}", raw)
        )
        unsupported = unsupported or len(re.findall(r"\\begin\{tabular\}", raw)) != 1
        grid = "" if unsupported else _inner_env(raw, "tabular")
    else:
        unsupported = unsupported or bool(re.search(r"\\begin\{tabular", raw))
        grid = "" if unsupported else _inner_env(raw, "longtable")
    if unsupported:
        return {"start": start_line, "uncovered": True, "label": label, "records": [], "skips": []}
    try:
        records, skips = _records_from_grid(
            grid, raw, start_line, chapter_start, metrics, eval_sets
        )
    except (InvalidOperation, ValueError):
        return {"start": start_line, "uncovered": True, "label": label, "records": [], "skips": []}
    if not label and records:
        label = str(records[0]["table_label"])
    return {
        "start": start_line,
        "uncovered": False,
        "label": label,
        "records": records,
        "skips": skips,
    }


def _chapter_tables(
    lines: list[str],
    start: int,
    end: int,
    chapter_start: int,
    metrics: tuple[str, ...],
    eval_sets: tuple[str, ...],
) -> list[dict[str, Any]]:
    tables: list[dict[str, Any]] = []
    index = start - 1
    last = min(end, len(lines)) - 1
    while index <= last:
        line = lines[index]
        if line.lstrip().startswith("%"):
            index += 1
            continue
        match = _XS_ENV_BEGIN_RE.search(line)
        if not match:
            index += 1
            continue
        name = match.group(1)
        end_index = _matching_env_end(lines, index, name)
        if end_index is None:
            tables.append(
                {"start": index + 1, "uncovered": True, "label": "", "records": [], "skips": []}
            )
            break
        raw = "\n".join(lines[index : end_index + 1])
        tables.append(_inspect_table(raw, index + 1, name, chapter_start, metrics, eval_sets))
        tables[-1]["end"] = end_index + 1
        index = end_index + 1
    return tables


def _summary_ranges(
    headings: list[dict[str, Any]], chapter: dict[str, Any], parser
) -> list[tuple[int, int]]:
    selected = [item for item in headings if chapter["start"] <= item["line"] <= chapter["end"]]
    normalize = getattr(parser, "normalize_heading_title", None)
    ranges: list[tuple[int, int]] = []
    for index, heading in enumerate(selected):
        title = heading["title"]
        if callable(normalize):
            title = normalize(title)
        if "小结" not in str(title):
            continue
        stop = chapter["end"]
        for nxt in selected[index + 1 :]:
            if nxt["level"] <= heading["level"]:
                stop = nxt["line"] - 1
                break
        ranges.append((heading["line"], stop))
    return ranges


def _select_xs_chapters(parser, content: str, section: str | None) -> list[dict[str, Any]]:
    ranges = parser.chapter_ranges(content)
    normalized = _normalize_section(section)
    if not normalized:
        return ranges
    family = re.compile(rf"^{re.escape(normalized)}(?:_\d+)?$")
    spans = [pair for key, pair in parser.split_sections(content).items() if family.fullmatch(key)]
    kept: list[dict[str, Any]] = []
    for chapter in ranges:
        key = chapter.get("key")
        if isinstance(key, str) and family.fullmatch(key):
            kept.append(chapter)
            continue
        if any(
            chapter["start"] <= span_end and span_start <= chapter["end"]
            for span_start, span_end in spans
        ):
            kept.append(chapter)
    return kept


_ROW_NEXT_OK = frozenset("的在为")


def _row_hit_closed(text: str, start: int, end: int) -> bool:
    """A following name character means the label is only a prefix, not the object."""
    if end >= len(text):
        return True
    nxt = text[end]
    if nxt.isascii() and nxt.isalnum():
        return False
    return not ("\u4e00" <= nxt <= "\u9fff" and nxt not in _ROW_NEXT_OK)


def _longest_hits(text: str, candidates: list[str]) -> list[str]:
    hits: list[str] = []
    for item in candidates:
        if not item:
            continue
        start = 0
        while True:
            idx = text.find(item, start)
            if idx < 0:
                break
            end = idx + len(item)
            if _row_hit_closed(text, idx, end):
                hits.append(item)
                break
            start = idx + 1
    kept: list[str] = []
    for item in hits:
        if any(item != other and item in other for other in hits):
            continue
        if item not in kept:
            kept.append(item)
    return kept


def _explicit_row(text: str, metrics: tuple[str, ...], eval_sets: tuple[str, ...]) -> str | None:
    match = re.search(r"中(.+?)在", text)
    if not match:
        return None
    label = " ".join(match.group(1).split())
    if not label or len(label) > 20:
        return None
    if _xs_match_terms(label, metrics, positive_only=False):
        return None
    if _xs_match_terms(label, eval_sets, positive_only=True):
        return None
    return label


def _xs_surface_paragraphs(
    lines: list[str],
    chapter: dict[str, Any],
    parser,
    summary_ranges: list[tuple[int, int]],
    table_spans: list[tuple[int, int]],
) -> list[dict[str, Any]]:
    paragraphs: list[dict[str, Any]] = []
    block: list[tuple[int, str]] = []
    surface: str | None = None
    prefix = parser.get_comment_prefix()

    def flush() -> None:
        nonlocal block, surface
        if block and surface:
            paragraphs.append(
                {
                    "surface": surface,
                    "line": block[0][0],
                    "raw": "\n".join(text for _line_no, text in block),
                    "rows": list(block),
                }
            )
        block = []
        surface = None

    for line_no in range(chapter["start"], chapter["end"] + 1):
        raw = lines[line_no - 1]
        stripped = raw.strip()
        in_table = any(start <= line_no <= stop for start, stop in table_spans)
        if (
            not stripped
            or stripped.startswith(prefix)
            or in_table
            or RA_HEADING_LINE_RE.match(stripped)
        ):
            flush()
            continue
        current = (
            "summary" if any(start <= line_no <= stop for start, stop in summary_ranges) else "body"
        )
        if surface not in (None, current):
            flush()
        surface = current
        block.append((line_no, raw))
    flush()
    return paragraphs


def _unique_surface(items: list[dict[str, Any]]) -> dict[str, Any] | str | None:
    if not items:
        return None
    if any(not _same_quantity(items[0]["quantity"], item["quantity"]) for item in items[1:]):
        return "conflict"
    return items[0]


def _check_cross_surface(
    lines: list[str],
    content: str,
    parser,
    section: str | None,
    terms_path: Path | None,
) -> list[str]:
    metrics, eval_sets = (
        _load_xs_terms(terms_path) if terms_path else (DEFAULT_XS_METRICS, DEFAULT_XS_EVAL_SETS)
    )
    chapters = _select_xs_chapters(parser, content, section)
    out: list[str] = []
    count = {"compared": 0, "uncovered": 0, "differences": 0}
    mentions: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    metric_notes: list[tuple[int, str, str]] = []
    eval_groups: dict[tuple[int, str, str, str], set[str]] = {}
    eval_lines: dict[tuple[int, str, str, str], int] = {}

    def cover(line_no: int, detail: str) -> None:
        count["uncovered"] += 1
        out.extend(_xs_finding(line_no, "RA-XS-COVERAGE", detail))

    def differ(line_no: int, code: str, detail: str) -> None:
        count["differences"] += 1
        out.extend(_xs_finding(line_no, code, detail))

    if section and not chapters:
        cover(1, "未命中指定章节")
    elif not chapters:
        cover(1, "未检出章节，不能视为三表面一致")
    headings = parser.extract_headings(content)
    for chapter in chapters:
        tables = _chapter_tables(
            lines, chapter["start"], chapter["end"], chapter["start"], metrics, eval_sets
        )
        for table in tables:
            if table["uncovered"]:
                cover(table["start"], "表格语法未覆盖")
        summary_ranges = _summary_ranges(headings, chapter, parser)
        if tables and not summary_ranges:
            cover(chapter["start"], "无小结，不能视为三表面一致")
        if summary_ranges and not tables:
            cover(chapter["start"], "无结果表，不能视为三表面一致")
        labels = {str(table["label"]) for table in tables if table.get("label")}
        uncovered_labels = {
            str(table["label"]) for table in tables if table["uncovered"] and table.get("label")
        }
        records = [record for table in tables for record in table["records"]]
        skips = [skip for table in tables for skip in table["skips"]]
        spans = [(int(table["start"]), int(table.get("end", table["start"]))) for table in tables]
        for paragraph in _xs_surface_paragraphs(lines, chapter, parser, summary_ranges, spans):
            for line_no, raw_line in paragraph["rows"]:
                for sentence in _ra_sentences(raw_line):
                    _handle_xs_sentence(
                        sentence,
                        int(line_no),
                        str(paragraph["surface"]),
                        int(chapter["start"]),
                        metrics,
                        eval_sets,
                        labels,
                        uncovered_labels,
                        records,
                        skips,
                        cover,
                        mentions,
                        missing,
                        eval_groups,
                        eval_lines,
                        metric_notes,
                    )
    for line_no, left, right in metric_notes:
        out.extend(
            _xs_finding(line_no, "RA-XS-METRIC", f"不同指标被写成换算或互推（{left}，{right}）")
        )
    for key, names in eval_groups.items():
        if len(names) < 2:
            continue
        _chapter_start, label, row, metric = key
        out.extend(
            _xs_finding(
                eval_lines[key],
                "RA-XS-EVALSET",
                f"同一表、对象和指标使用了不同评价集（{label}，指标 {metric}，对象 {row}）",
            )
        )
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for item in mentions:
        grouped.setdefault(item["key"], []).append(item)
    for items in grouped.values():
        body = _unique_surface([item for item in items if item["surface"] == "body"])
        summary = _unique_surface([item for item in items if item["surface"] == "summary"])
        if body == "conflict" or summary == "conflict":
            cover(int(items[0]["line"]), "多个候选值，不能判断终值")
            continue
        count["compared"] += 1
        record_quantity = items[0]["quantity_table"]
        bits = str(items[0]["bits"])
        body_line = int(body["line"]) if isinstance(body, dict) else int(items[0]["line"])
        summary_line = int(summary["line"]) if isinstance(summary, dict) else int(items[0]["line"])
        if not isinstance(body, dict):
            out.extend(_xs_finding(summary_line, "RA-XS-MISSING", f"缺少正文表面（{bits}）"))
        elif not _same_quantity(body["quantity"], record_quantity):
            differ(body_line, "RA-XS-BODY", f"正文终值与表记录不一致（{bits}）")
        if not isinstance(summary, dict):
            out.extend(_xs_finding(body_line, "RA-XS-MISSING", f"缺少小结表面（{bits}）"))
        elif not _same_quantity(summary["quantity"], record_quantity):
            differ(summary_line, "RA-XS-SUMMARY", f"小结终值与表记录不一致（{bits}）")
    missing_grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for item in missing:
        missing_grouped.setdefault(item["key"], []).append(item)
    for items in missing_grouped.values():
        surfaces = {str(item["surface"]) for item in items}
        line_no = min(int(item["line"]) for item in items)
        bits = str(items[0]["bits"])
        differ(line_no, "RA-XS-SUMMARY", f"已绑定的表中无此记录（{bits}）")
        if "body" not in surfaces:
            out.extend(_xs_finding(line_no, "RA-XS-MISSING", f"缺少正文表面（{bits}）"))
        if "summary" not in surfaces:
            out.extend(_xs_finding(line_no, "RA-XS-MISSING", f"缺少小结表面（{bits}）"))
    out.append(
        "% EXPERIMENT CROSS-SURFACE: "
        f"compared_keys={count['compared']} uncovered={count['uncovered']} "
        f"differences={count['differences']}。本检查不是全文合规证明。"
    )
    out.append("")
    return out


def _handle_xs_sentence(
    sentence: str,
    line_no: int,
    surface: str,
    chapter_start: int,
    metrics: tuple[str, ...],
    eval_sets: tuple[str, ...],
    labels: set[str],
    uncovered_labels: set[str],
    records: list[dict[str, Any]],
    skips: list[dict[str, Any]],
    cover,
    mentions: list[dict[str, Any]],
    missing: list[dict[str, Any]],
    eval_groups: dict[tuple[int, str, str, str], set[str]],
    eval_lines: dict[tuple[int, str, str, str], int],
    metric_notes: list[tuple[int, str, str]],
) -> None:
    prepared = _prepare_measure_text(sentence)
    pair = _xs_metric_pair(prepared, metrics)
    if pair:
        metric_notes.append((line_no, pair[0], pair[1]))
        return
    refs = re.findall(r"\\ref\{(tab:[^}]+)\}", sentence)
    metric_hits = list(dict.fromkeys(_xs_match_terms(prepared, metrics, positive_only=False)))
    quantities = _extract_quantities(prepared)
    has_measure = any(item["kind"] in {"scalar", "interval"} for item in quantities)
    if len(refs) >= 2:
        cover(line_no, "多个表引用，不能唯一绑定")
        return
    if len(refs) == 0:
        if metric_hits and has_measure:
            cover(line_no, "无表引用，同值也不能绑定")
        return
    ref = refs[0]
    if ref in uncovered_labels:
        cover(line_no, "表格语法未覆盖")
        return
    if ref not in labels:
        cover(line_no, "表引用不在本章")
        return
    known_rows = list(
        dict.fromkeys(
            str(record["row_label"])
            for record in [*records, *skips]
            if record["table_label"] == ref and record["chapter_start"] == chapter_start
        )
    )
    explicit = _explicit_row(prepared, metrics, eval_sets)
    rows = _longest_hits(prepared, known_rows)
    if explicit and (not rows or any(row != explicit and row in explicit for row in rows)):
        rows = [explicit]
    if len(rows) != 1:
        if has_measure or metric_hits:
            cover(line_no, "对象不能唯一绑定")
        return
    if len(metric_hits) != 1:
        if has_measure:
            cover(line_no, "指标不能唯一绑定")
        return
    positive_eval = list(dict.fromkeys(_xs_match_terms(prepared, eval_sets, positive_only=True)))
    if positive_eval:
        group_key = (chapter_start, ref, rows[0], metric_hits[0])
        eval_groups.setdefault(group_key, set()).update(positive_eval)
        eval_lines.setdefault(group_key, line_no)
    if len(positive_eval) != 1:
        if not positive_eval:
            cover(line_no, "评价集不能唯一绑定")
        return
    if len(quantities) != 1 or quantities[0]["kind"] not in {"scalar", "interval"}:
        cover(line_no, "终值或区间口径不能比较")
        return
    quantity = _apply_unit(quantities[0], None, prepared)
    if not quantity["unit"]:
        cover(line_no, "单位缺失或不能识别")
        return
    row = rows[0]
    metric = metric_hits[0]
    eval_set = positive_eval[0]
    unit = str(quantity["unit"])
    table_records = [
        record
        for record in records
        if record["chapter_start"] == chapter_start and record["table_label"] == ref
    ]
    scoped = [
        record
        for record in table_records
        if record["metric"] == metric
        and record["row_label"] == row
        and record["eval_set"] == eval_set
    ]
    same_unit = [record for record in scoped if record["unit"] == unit]
    bits = _xs_bits(ref, metric, row, eval_set, unit)
    key = (chapter_start, ref, metric, row, eval_set, unit)
    if len(same_unit) == 1:
        mentions.append(
            {
                "key": key,
                "surface": surface,
                "line": line_no,
                "quantity": quantity,
                "quantity_table": same_unit[0]["quantity"],
                "bits": bits,
            }
        )
        return
    if len(same_unit) > 1:
        cover(line_no, "多个候选值，不能判断终值")
        return
    if scoped:
        cover(line_no, "单位不一致，不能比较")
        return
    if _xs_cell_blocked(skips, chapter_start, ref, row, metric, eval_set):
        cover(line_no, "表单元格终值或单位不能比较")
        return
    if not table_records:
        cover(line_no, "表中无可用记录")
        return
    missing.append({"key": key, "surface": surface, "line": line_no, "bits": bits})


def _xs_cell_blocked(
    skips: list[dict[str, Any]],
    chapter_start: int,
    label: str,
    row: str,
    metric: str,
    eval_set: str,
) -> bool:
    return any(
        skip["chapter_start"] == chapter_start
        and skip["table_label"] == label
        and skip["row_label"] == row
        and skip["metric"] == metric
        and skip["eval_set"] in {None, eval_set}
        for skip in skips
    )


def _xs_metric_pair(text: str, metrics: tuple[str, ...]) -> tuple[str, str] | None:
    ordered = sorted(set(metrics), key=len, reverse=True)
    if len(ordered) < 2:
        return None
    alt = "|".join(re.escape(item) for item in ordered)
    for match in re.finditer(rf"由({alt})可得({alt})", text):
        prefix = text[max(0, match.start() - 4) : match.start()]
        if re.search(r"(?:不能|不可|无法|并未)$", prefix):
            continue
        if match.group(1) != match.group(2):
            return match.group(1), match.group(2)
    for match in re.finditer(rf"({alt})换算为({alt})", text):
        prefix = text[max(0, match.start() - 6) : match.start()]
        if re.search(r"(?:不能|不可|无法|并未)", prefix):
            continue
        if match.group(1) != match.group(2):
            return match.group(1), match.group(2)
    return None


def analyze(
    file_path: Path,
    section: str | None = None,
    per_chapter: bool = False,
    results_analysis: bool = False,
    cross_surface: bool = False,
    cross_surface_terms: Path | None = None,
) -> list[str]:
    """Review-mode analysis for experiment/discussion/conclusion sections."""
    global _DOC
    parser = get_parser(file_path)
    doc = assemble(file_path)
    _DOC = doc
    lines = doc.lines
    sections = parser.split_sections(doc.content)

    output: list[str] = doc.warning_lines(parser.get_comment_prefix())
    warn_count = len(output)

    # R4b: per-method-chapter experiment checks (E-* family), gated behind the flag.
    if per_chapter and not results_analysis and not cross_surface:
        output.extend(_check_per_chapter(lines, doc.content, parser))
        if len(output) == warn_count:
            output.append("% EXPERIMENT: No per-chapter experiment issues detected.")
        return output

    if results_analysis or cross_surface:
        if per_chapter:
            output.extend(_check_per_chapter(lines, doc.content, parser))
        if results_analysis:
            output.extend(_check_results_analysis(lines, doc.content, parser, section))
            if len(output) == warn_count:
                output.append("% EXPERIMENT: No results-analysis issues detected.")
            if not cross_surface:
                return output
        if cross_surface:
            output.extend(
                _check_cross_surface(lines, doc.content, parser, section, cross_surface_terms)
            )
        return output

    normalized = _normalize_section(section)

    if sections:
        if (not normalized or normalized == "discussion") and "discussion" in sections:
            d_start, d_end = sections["discussion"]
            output.extend(_check_discussion_depth(lines, d_start, d_end, parser))
            output.extend(_check_discussion_structure(lines, d_start, d_end, parser))

        if not normalized:
            output.extend(_check_results_literature_echo(lines, sections))

        if (not normalized or normalized == "conclusion") and "conclusion" in sections:
            c_start, c_end = sections["conclusion"]
            output.extend(_check_conclusion_completeness(lines, c_start, c_end, parser))

    # R4a: a scattered "one method per chapter + in-chapter experiment" thesis has
    # no independent discussion/review chapter (综述 lives in 绪论, 讨论 is embedded in
    # each experiment section), so B3 has no substantive region and B4 can never run.
    # Emit a structure hint instead of a silent false green. Note that split_sections
    # can spuriously key a chapter title containing 分析/讨论 as `discussion`, so the
    # absence of `related` (B4's hard dependency) is the reliable scattered-structure
    # signal — fire when either anchor section is missing.
    if not normalized and ("discussion" not in sections or "related" not in sections):
        output.extend(
            _format_issue(
                1,
                "Info",
                "P3",
                "[Script] 结构提示：未检出独立的讨论章或综述章，B3（讨论深度）/B4（文献回溯）"
                "在此结构下难以生效；若为“一章一方法 + 同章实验”章式，请改用 --per-chapter "
                "逐方法章检查。",
            )
        )
        output.append("")

    if len(output) == warn_count:
        output.append("% EXPERIMENT: No discussion/conclusion issues detected.")
    return output


def main() -> int:
    cli = argparse.ArgumentParser(
        description="Experiment analysis for Chinese LaTeX thesis (review + prompt generation)"
    )
    cli.add_argument("input", help="File path or raw experiment data")
    cli.add_argument("--section", help="Section name to analyze")
    cli.add_argument(
        "--per-chapter",
        action="store_true",
        help="Run per-method-chapter experiment checks (E-* family) for theses that "
        "keep experiments inside each method chapter rather than a global discussion",
    )
    cli.add_argument(
        "--results-analysis",
        action="store_true",
        help="Run opt-in RA-* heuristic cues over results-analysis intervals",
    )
    cli.add_argument(
        "--cross-surface",
        action="store_true",
        help="Opt-in same-chapter table/body/summary number cues (RA-XS-*)",
    )
    cli.add_argument(
        "--cross-surface-terms",
        help="JSON metric and eval-set lists; valid only with --cross-surface",
    )
    cli.add_argument(
        "--generate",
        action="store_true",
        help="Generate analysis prompt instead of reviewing",
    )
    args = cli.parse_args()
    if args.cross_surface_terms and not args.cross_surface:
        print("error: --cross-surface-terms requires --cross-surface", file=sys.stderr)
        return 2
    terms_path = Path(args.cross_surface_terms) if args.cross_surface_terms else None
    if args.cross_surface and terms_path is not None:
        try:
            _load_xs_terms(terms_path)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    path = Path(args.input)
    if args.generate or not path.exists() or path.suffix != ".tex":
        print(generate_request(args.input))
        return 0

    print(
        "\n".join(
            analyze(
                path,
                args.section,
                per_chapter=args.per_chapter,
                results_analysis=args.results_analysis,
                cross_surface=args.cross_surface,
                cross_surface_terms=terms_path,
            )
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
