#!/usr/bin/env python3
"""
Experiment analysis helper for Chinese LaTeX thesis and journals.

Supports two modes:
- Prompt generation: format raw data into LLM prompt (original behavior)
- Review analysis: check discussion depth, literature echo, conclusion completeness
"""

import argparse
import re
import sys
from pathlib import Path

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


def analyze(
    file_path: Path,
    section: str | None = None,
    per_chapter: bool = False,
    results_analysis: bool = False,
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
    if per_chapter and not results_analysis:
        output.extend(_check_per_chapter(lines, doc.content, parser))
        if len(output) == warn_count:
            output.append("% EXPERIMENT: No per-chapter experiment issues detected.")
        return output

    if results_analysis:
        if per_chapter:
            output.extend(_check_per_chapter(lines, doc.content, parser))
        output.extend(_check_results_analysis(lines, doc.content, parser, section))
        if len(output) == warn_count:
            output.append("% EXPERIMENT: No results-analysis issues detected.")
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
        "--generate",
        action="store_true",
        help="Generate analysis prompt instead of reviewing",
    )
    args = cli.parse_args()

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
            )
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
