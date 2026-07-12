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


def analyze(file_path: Path, section: str | None = None, per_chapter: bool = False) -> list[str]:
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
    if per_chapter:
        output.extend(_check_per_chapter(lines, doc.content, parser))
        if len(output) == warn_count:
            output.append("% EXPERIMENT: No per-chapter experiment issues detected.")
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
        "--generate",
        action="store_true",
        help="Generate analysis prompt instead of reviewing",
    )
    args = cli.parse_args()

    path = Path(args.input)
    if args.generate or not path.exists() or path.suffix != ".tex":
        print(generate_request(args.input))
        return 0

    print("\n".join(analyze(path, args.section, per_chapter=args.per_chapter)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
