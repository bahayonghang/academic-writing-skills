"""Internationalization dictionary for paper-audit report renderers.

Centralizes every user-facing string that ``report_generator.py`` (and the
HTML templates) emit. Rendering functions look up strings via :func:`t` so
the report language can switch between ``en`` (default) and ``zh`` without
duplicating render logic.

What IS translated:
    - Markdown section titles (e.g. ``## Overall Assessment``)
    - Field labels (e.g. ``**Type**``)
    - Table headers (e.g. ``| Line | Severity | Issue |``)
    - Status sentences and default placeholders

What is NOT translated:
    - Issue ``quote`` field — paper source text
    - ``[Script]`` / ``[LLM]`` source tags
    - Structured field values (``severity`` lowercase keys, ``confidence``
      labels, ``review_lane`` names, ``comment_type`` enum values)
    - File paths, dates, numeric scores, identifiers
"""

from __future__ import annotations

from typing import Any

EN: dict[str, str] = {
    # ---- Common metadata bar labels --------------------------------------
    "common.paper": "**Paper**",
    "common.file": "**File**",
    "common.language": "**Language**",
    "common.mode": "**Mode**",
    "common.generated": "**Generated**",
    "common.venue": "**Venue**",
    "common.focus": "**Focus**",
    "common.artifacts": "**Artifacts**",
    "common.compatibility_note": "**Compatibility Note**",
    "common.review_round": "**Review Round**",
    "common.primary_view": "**Primary View**",
    "common.style": "**Style**",
    "common.journal": "**Journal**",
    "common.previous_report": "**Previous Report**",
    "common.compat_note_template": "legacy mode alias `{alias}` mapped to `{mode}`.",
    # ---- Report titles ---------------------------------------------------
    "title.deep_review": "# Deep Review Report",
    "title.deep_review_summary": "# Deep Review Summary",
    "title.peer_review": "# Peer Review Report",
    "title.audit": "# Paper Audit Report",
    "title.gate": "# Quality Gate Report",
    "title.polish_precheck": "# Polish Precheck Report",
    "title.reaudit": "# Re-Audit Report",
    "title.revision_suggestions": "# Revision Suggestions",
    # ---- Section headings (## ...) --------------------------------------
    "section.summary": "## Summary",
    "section.overall_assessment": "## Overall Assessment",
    "section.decision_signals": "## Decision Signals",
    "section.major_issues": "## Major Issues",
    "section.moderate_issues": "## Moderate Issues",
    "section.minor_issues": "## Minor Issues",
    "section.recommendation": "## Recommendation",
    "section.executive_summary": "## Executive Summary",
    "section.submission_blockers": "## Submission Blockers",
    "section.quality_improvements": "## Quality Improvements",
    "section.pre_submission_checklist": "## Pre-Submission Checklist",
    "section.scores": "## Scores",
    "section.committee": "## Academic Pre-Review Committee",
    "section.paper_summary": "## Paper Summary",
    "section.phase0_findings": "## Phase 0 Automated Findings",
    "section.revision_roadmap": "## Revision Roadmap",
    "section.revision_suggestions": "## Revision Suggestions",
    "section.strengths": "## Strengths",
    "section.weaknesses": "## Weaknesses",
    "section.questions_for_authors": "## Questions for Authors",
    "section.detailed_automated_findings": "## Detailed Automated Findings",
    "section.blocking_issues": "## Blocking Issues (must fix)",
    "section.checklist": "## Checklist",
    "section.advisory_recommendations": "## Advisory Recommendations (non-blocking)",
    "section.detected_sections": "## Detected Sections",
    "section.blockers_polish": "## Blockers (must fix before polish)",
    "section.ready_for_critic": "## Status: Ready for Critic Phase",
    "section.revision_summary": "## Revision Summary",
    "section.prior_issue_verification": "## Prior Issue Verification",
    "section.new_issues": "## New Issues (not in previous report)",
    "section.current_scores": "## Current Scores",
    "section.suggestions_breakdown": "## Detailed Suggestions",
    "section.estimated_effort": "## Estimated Total Effort",
    "section.reaudit_instructions": "## Re-Audit Instructions",
    "section.verdict_template": "## Verdict: {verdict}",
    # ---- Sub-headings (### ...) ------------------------------------------
    "subsection.high_signal_quality_issues": "### High-Signal Quality Issues",
    "subsection.additional_quality_improvements": "### Additional Quality Improvements",
    "subsection.priority_1": "### Priority 1 --- Must Address (Blocking)",
    "subsection.priority_2": "### Priority 2 --- Strongly Recommended",
    "subsection.priority_3": "### Priority 3 --- Optional Improvements",
    "subsection.committee.editor": "### Editor (Desk Reject Screen)",
    "subsection.committee.theory": "### Reviewer 1 (Theory Contribution)",
    "subsection.committee.literature": "### Reviewer 3 (Literature Dialogue)",
    "subsection.committee.methodology": "### Reviewer 2 (Methodology & Transparency)",
    "subsection.committee.logic": "### Reviewer 4 (Logic Chain)",
    "subsection.committee.consensus": "### Committee Consensus",
    "subsection.script_module_template": "### [Script] {module}",
    # ---- Field labels ----------------------------------------------------
    "label.major": "**Major**",
    "label.moderate": "**Moderate**",
    "label.minor": "**Minor**",
    "label.type": "**Type**",
    "label.source": "**Source**",
    "label.confidence": "**Confidence**",
    "label.section": "**Section**",
    "label.related_sections": "**Related Sections**",
    "label.root_cause_key": "**Root Cause Key**",
    "label.quote_verified": "**Quote Verified**",
    "label.quote": "**Quote**",
    "label.explanation": "**Explanation**",
    "label.original": "**Original**",
    "label.suggested": "**Suggested**",
    "label.rationale": "**Rationale**",
    "label.additional_actions": "**Additional Actions**",
    "label.problem": "**Problem**",
    "label.why_it_matters": "**Why it matters**",
    "label.suggestion": "**Suggestion**",
    "label.severity": "**Severity**",
    "label.committee_score": "**Committee Score**",
    "label.editor_verdict": "**Editor Verdict**",
    "label.reviewer_recommendation": "**Reviewer Recommendation**",
    "label.issue_bundle": "**Issue Bundle**",
    "label.primary": "**Primary**",
    "label.companion": "**Companion**",
    "label.structured_issues": "**Structured Issues**",
    "label.revision_roadmap": "**Revision Roadmap**",
    "label.revision_suggestions": "**Revision Suggestions**",
    "label.resolution_rate": "**Resolution rate**",
    "label.recommendation_bold": "**Recommendation**",
    "label.precheck_findings": "**Pre-check findings**",
    # ---- Cell / row helpers ---------------------------------------------
    "label.yes": "yes",
    "label.no": "no",
    "label.unknown_section": "unknown",
    # ---- Table headers ---------------------------------------------------
    "table.findings_header": "| Line | Severity | Issue |",
    "table.findings_sep": "|------|----------|-------|",
    "table.dimension_header": "| Dimension | Score | Label |",
    "table.dimension_sep": "|-----------|-------|-------|",
    "table.dimension_simple_header": "| Dimension | Score |",
    "table.dimension_simple_sep": "|-----------|-------|",
    "table.scores_audit_header": "| Dimension | Score | Issues (C/M/m) | Key Finding |",
    "table.scores_audit_sep": "|-----------|-------|-----------------|-------------|",
    "table.metric_header": "| Metric | Count |",
    "table.metric_sep": "|--------|-------|",
    "table.sections_header": "| Section | Lines | Words |",
    "table.sections_sep": "|---------|-------|-------|",
    "table.new_issues_header": "| # | Module | Line | Severity | Issue |",
    "table.new_issues_sep": "|---|--------|------|----------|-------|",
    "table.prior_header": (
        "| # | root_cause_key | Module | Prior Severity | Status | Current | Message |"
    ),
    "table.prior_sep": "|---|----------------|--------|---------------|--------|---------|---------|",
    "table.effort_header": "| Priority | Items | Est. Time |",
    "table.effort_sep": "|----------|-------|-----------|",
    # ---- Severity / dimension display strings ---------------------------
    "severity.major": "Major",
    "severity.moderate": "Moderate",
    "severity.minor": "Minor",
    "severity.critical": "Critical",
    "dimension.quality": "Quality",
    "dimension.clarity": "Clarity",
    "dimension.significance": "Significance",
    "dimension.originality": "Originality",
    "dimension.overall": "Overall",
    # ---- Score labels ----------------------------------------------------
    "score.strong_accept": "Strong Accept",
    "score.accept": "Accept",
    "score.borderline_accept": "Borderline Accept",
    "score.borderline_reject": "Borderline Reject",
    "score.reject": "Reject",
    "score.strong_reject": "Strong Reject",
    # ---- Journal recommendation values (display) ------------------------
    "rec.accept": "Accept",
    "rec.minor_revision": "Minor Revision",
    "rec.major_revision": "Major Revision",
    "rec.reject": "Reject",
    "rec.accept.rationale": (
        "The central contribution appears supportable and only non-substantive edits remain."
    ),
    "rec.minor_revision.rationale": (
        "The paper is potentially publishable, but several clarifications or "
        "limited corrections are still needed."
    ),
    "rec.major_revision.rationale": (
        "The paper may become publishable, but key issues still affect the "
        "credibility, completeness, or transparency of the claims."
    ),
    "rec.reject.rationale": (
        "The current version has unresolved issues that materially weaken the "
        "core conclusions or submission readiness."
    ),
    # ---- Status sentences / defaults ------------------------------------
    "status.no_submission_blockers": "- No submission blockers detected.",
    "status.no_quality_improvements": "- No quality improvements identified.",
    "status.no_major_issue": (
        "No major validity-threatening issue was identified in the current deep-review bundle."
    ),
    "status.no_minor_issue": "No minor issue requiring additional comment was identified.",
    "status.deep_review_default_assessment": (
        "Deep review completed. Inspect the primary artifact and issue bundle before revising."
    ),
    "status.deep_review_default_assessment_long": (
        "Deep review completed. Inspect the structured issue list below for "
        "the highest-impact claim, methodology, and consistency risks before "
        "revising."
    ),
    "status.resolve_critical_and_rerun": (
        "Resolve these Critical issues and re-run before proceeding."
    ),
    "status.non_imrad_note": "**Note**: Non-standard section structure detected.",
    "status.executive_template": (
        "Found **{total} issues** ({critical} critical). Overall score: "
        "**{overall:.1f}/6.0** ({label})."
    ),
    "status.precheck_findings_template": "{logic} logic, {expression} expression issues",
    "status.all_prior_resolved": (
        "*All prior issues resolved and no new issues found. Ready for next step.*"
    ),
    "status.all_prior_resolved_new_only": (
        "*All prior issues resolved, but {new_count} new issue(s) detected. "
        "Review new issues before proceeding.*"
    ),
    "status.remaining_unresolved": (
        "*{remaining} prior issue(s) still unresolved. Continue revision and re-run audit.*"
    ),
    "status.resolution_rate_template": "{pct}% ({fixed}/{total} fully resolved)",
    "status.issue_bundle_template": ("{major} major / {moderate} moderate / {minor} minor"),
    "status.advisory_intro": ("These are advisory recommendations, not submission blockers."),
    "status.no_revision_suggestions": (
        "No actionable revision suggestion was generated. Inspect "
        "`final_issues.json` for the raw issue bundle."
    ),
    # ---- Re-audit metric row labels -------------------------------------
    "metric.prior_issues": "Prior issues",
    "metric.fully_addressed": "Fully addressed",
    "metric.partially_addressed": "Partially addressed",
    "metric.not_addressed": "Not addressed",
    "metric.new_issues": "New issues",
    "metric.root_cause_unavailable": "root cause unavailable",
    # ---- Verdict words --------------------------------------------------
    "verdict.pass": "PASS",
    "verdict.fail": "FAIL",
    "verdict.pass_mark": "[PASS]",
    "verdict.fail_mark": "[FAIL]",
    "verdict.blocking_mark": "[BLOCKING]",
    "verdict.info_mark": "[INFO]",
    # ---- Revision-suggestions specific ----------------------------------
    "suggestions.opening": (
        "The list below pairs each high-priority issue with a concrete "
        "edit. Suggestions are derived from the deep-review issue bundle "
        "and require author judgment before application."
    ),
    "suggestions.entry_title": "### {label}: {title}",
    "suggestions.no_suggestion_text": (
        "_No direct text rewrite was generated. Apply the additional actions below instead._"
    ),
    "suggestions.original_block": "Original text",
    "suggestions.suggested_block": "Suggested rewrite",
    "suggestions.rationale_block": "Rationale",
    "suggestions.actions_block": "Additional actions",
    # ---- Misc -----------------------------------------------------------
    "misc.dash": "—",
    "misc.section_unknown": "unknown",
    "misc.review_default_lane": "review",
}

ZH: dict[str, str] = {
    # ---- Common metadata bar labels --------------------------------------
    "common.paper": "**论文**",
    "common.file": "**文件**",
    "common.language": "**语言**",
    "common.mode": "**模式**",
    "common.generated": "**生成时间**",
    "common.venue": "**目标期刊**",
    "common.focus": "**审稿焦点**",
    "common.artifacts": "**工件目录**",
    "common.compatibility_note": "**兼容性提示**",
    "common.review_round": "**审稿轮次**",
    "common.primary_view": "**主视图**",
    "common.style": "**样式**",
    "common.journal": "**期刊**",
    "common.previous_report": "**先前报告**",
    "common.compat_note_template": "旧别名 `{alias}` 已映射为 `{mode}`。",
    # ---- Report titles ---------------------------------------------------
    "title.deep_review": "# 深度审稿报告",
    "title.deep_review_summary": "# 深度审稿摘要",
    "title.peer_review": "# 同行评议报告",
    "title.audit": "# 论文审核报告",
    "title.gate": "# 投稿门控报告",
    "title.polish_precheck": "# 润色前置检查报告",
    "title.reaudit": "# 复审报告",
    "title.revision_suggestions": "# 修订建议",
    # ---- Section headings ------------------------------------------------
    "section.summary": "## 摘要",
    "section.overall_assessment": "## 总体评估",
    "section.decision_signals": "## 决策信号",
    "section.major_issues": "## 主要问题",
    "section.moderate_issues": "## 中等问题",
    "section.minor_issues": "## 次要问题",
    "section.recommendation": "## 审稿推荐",
    "section.executive_summary": "## 执行摘要",
    "section.submission_blockers": "## 投稿阻断",
    "section.quality_improvements": "## 质量改进",
    "section.pre_submission_checklist": "## 投稿前检查清单",
    "section.scores": "## 评分",
    "section.committee": "## 学术预审委员会",
    "section.paper_summary": "## 论文摘要",
    "section.phase0_findings": "## Phase 0 自动审查发现",
    "section.revision_roadmap": "## 修订路线图",
    "section.revision_suggestions": "## 修订建议",
    "section.strengths": "## 优点",
    "section.weaknesses": "## 缺点",
    "section.questions_for_authors": "## 给作者的问题",
    "section.detailed_automated_findings": "## 自动审查详细结果",
    "section.blocking_issues": "## 阻断问题（必须修复）",
    "section.checklist": "## 检查清单",
    "section.advisory_recommendations": "## 建议性推荐（非阻断）",
    "section.detected_sections": "## 检测到的章节",
    "section.blockers_polish": "## 阻断（润色前必须修复）",
    "section.ready_for_critic": "## 状态：可进入批判阶段",
    "section.revision_summary": "## 修订摘要",
    "section.prior_issue_verification": "## 旧问题验证",
    "section.new_issues": "## 新增问题（旧报告中未提及）",
    "section.current_scores": "## 当前评分",
    "section.suggestions_breakdown": "## 具体建议",
    "section.estimated_effort": "## 预估总工作量",
    "section.reaudit_instructions": "## 复审指引",
    "section.verdict_template": "## 裁定：{verdict}",
    # ---- Sub-headings ----------------------------------------------------
    "subsection.high_signal_quality_issues": "### 高信号质量问题",
    "subsection.additional_quality_improvements": "### 其他质量改进",
    "subsection.priority_1": "### 优先级 1 --- 必须处理（阻断）",
    "subsection.priority_2": "### 优先级 2 --- 强烈建议",
    "subsection.priority_3": "### 优先级 3 --- 可选改进",
    "subsection.committee.editor": "### 主编（直接拒稿筛查）",
    "subsection.committee.theory": "### 评审 1（理论贡献）",
    "subsection.committee.literature": "### 评审 3（文献对话）",
    "subsection.committee.methodology": "### 评审 2（方法与透明度）",
    "subsection.committee.logic": "### 评审 4（逻辑链）",
    "subsection.committee.consensus": "### 委员会共识",
    "subsection.script_module_template": "### [Script] {module}",
    # ---- Field labels ----------------------------------------------------
    "label.major": "**主要**",
    "label.moderate": "**中等**",
    "label.minor": "**次要**",
    "label.type": "**类型**",
    "label.source": "**来源**",
    "label.confidence": "**置信度**",
    "label.section": "**章节**",
    "label.related_sections": "**关联章节**",
    "label.root_cause_key": "**根因键**",
    "label.quote_verified": "**原文已核对**",
    "label.quote": "**原文**",
    "label.explanation": "**说明**",
    "label.original": "**原文**",
    "label.suggested": "**建议**",
    "label.rationale": "**理由**",
    "label.additional_actions": "**额外操作**",
    "label.problem": "**问题**",
    "label.why_it_matters": "**影响**",
    "label.suggestion": "**建议**",
    "label.severity": "**严重度**",
    "label.committee_score": "**委员会评分**",
    "label.editor_verdict": "**主编裁定**",
    "label.reviewer_recommendation": "**审稿推荐**",
    "label.issue_bundle": "**问题包**",
    "label.primary": "**主报告**",
    "label.companion": "**辅助报告**",
    "label.structured_issues": "**结构化问题**",
    "label.revision_roadmap": "**修订路线图**",
    "label.revision_suggestions": "**修订建议**",
    "label.resolution_rate": "**解决率**",
    "label.recommendation_bold": "**推荐**",
    "label.precheck_findings": "**前置检查发现**",
    # ---- Cell / row helpers ---------------------------------------------
    "label.yes": "是",
    "label.no": "否",
    "label.unknown_section": "未知",
    # ---- Table headers ---------------------------------------------------
    "table.findings_header": "| 行号 | 严重度 | 问题 |",
    "table.findings_sep": "|------|--------|------|",
    "table.dimension_header": "| 维度 | 得分 | 标签 |",
    "table.dimension_sep": "|------|------|------|",
    "table.dimension_simple_header": "| 维度 | 得分 |",
    "table.dimension_simple_sep": "|------|------|",
    "table.scores_audit_header": "| 维度 | 得分 | 问题数 (严/主/次) | 关键发现 |",
    "table.scores_audit_sep": "|------|------|-------------------|----------|",
    "table.metric_header": "| 指标 | 数量 |",
    "table.metric_sep": "|------|------|",
    "table.sections_header": "| 章节 | 行号 | 字数 |",
    "table.sections_sep": "|------|------|------|",
    "table.new_issues_header": "| # | 模块 | 行号 | 严重度 | 问题 |",
    "table.new_issues_sep": "|---|------|------|--------|------|",
    "table.prior_header": "| # | 根因键 | 模块 | 旧严重度 | 状态 | 当前 | 消息 |",
    "table.prior_sep": "|---|--------|------|----------|------|------|------|",
    "table.effort_header": "| 优先级 | 数量 | 预计时间 |",
    "table.effort_sep": "|--------|------|----------|",
    # ---- Severity / dimension display strings ---------------------------
    "severity.major": "主要",
    "severity.moderate": "中等",
    "severity.minor": "次要",
    "severity.critical": "严重",
    "dimension.quality": "质量",
    "dimension.clarity": "清晰度",
    "dimension.significance": "重要性",
    "dimension.originality": "原创性",
    "dimension.overall": "总体",
    # ---- Score labels ----------------------------------------------------
    "score.strong_accept": "强烈录用",
    "score.accept": "录用",
    "score.borderline_accept": "勉强录用",
    "score.borderline_reject": "勉强拒稿",
    "score.reject": "拒稿",
    "score.strong_reject": "强烈拒稿",
    # ---- Journal recommendation values (display) ------------------------
    "rec.accept": "录用",
    "rec.minor_revision": "小修",
    "rec.major_revision": "大修",
    "rec.reject": "拒稿",
    "rec.accept.rationale": "核心贡献基本可支撑，剩余的多为非实质性编辑修订。",
    "rec.minor_revision.rationale": "论文具备发表潜力，但仍需若干澄清或有限纠正。",
    "rec.major_revision.rationale": (
        "论文有发表潜力，但关键问题仍影响论断的可信度、完整性或透明度。"
    ),
    "rec.reject.rationale": "当前版本仍存在未解决的问题，明显削弱核心结论或投稿成熟度。",
    # ---- Status sentences / defaults ------------------------------------
    "status.no_submission_blockers": "- 未发现投稿阻断问题。",
    "status.no_quality_improvements": "- 未发现质量改进项。",
    "status.no_major_issue": "本次深度审稿未发现威胁有效性的主要问题。",
    "status.no_minor_issue": "未发现需额外评论的次要问题。",
    "status.deep_review_default_assessment": "深度审稿完成。修订前请查看主报告及问题包。",
    "status.deep_review_default_assessment_long": (
        "深度审稿完成。修订前请重点关注下方结构化问题列表中影响最大的论断、方法与一致性风险。"
    ),
    "status.resolve_critical_and_rerun": "请先解决以上严重问题再重新运行。",
    "status.non_imrad_note": "**提示**：检测到非标准章节结构。",
    "status.executive_template": (
        "共发现 **{total} 个问题**（其中严重 {critical} 个）。总分：**{overall:.1f}/6.0**（{label}）。"
    ),
    "status.precheck_findings_template": "逻辑 {logic} 个，表达 {expression} 个",
    "status.all_prior_resolved": "*所有旧问题已解决，且无新增问题。可进入下一步。*",
    "status.all_prior_resolved_new_only": (
        "*所有旧问题已解决，但检测到 {new_count} 个新问题。请先复核新问题再继续。*"
    ),
    "status.remaining_unresolved": "*仍有 {remaining} 个旧问题未解决，请继续修订后重跑审稿。*",
    "status.resolution_rate_template": "{pct}%（{fixed}/{total} 完全解决）",
    "status.issue_bundle_template": "主要 {major} / 中等 {moderate} / 次要 {minor}",
    "status.advisory_intro": "以下为建议性推荐，非投稿阻断项。",
    "status.no_revision_suggestions": (
        "未生成可执行的修订建议。请查阅 `final_issues.json` 获取原始问题包。"
    ),
    # ---- Re-audit metric row labels -------------------------------------
    "metric.prior_issues": "旧问题数",
    "metric.fully_addressed": "完全解决",
    "metric.partially_addressed": "部分解决",
    "metric.not_addressed": "未解决",
    "metric.new_issues": "新增问题",
    "metric.root_cause_unavailable": "无根因信息",
    # ---- Verdict words --------------------------------------------------
    "verdict.pass": "通过",
    "verdict.fail": "未通过",
    "verdict.pass_mark": "[通过]",
    "verdict.fail_mark": "[未通过]",
    "verdict.blocking_mark": "[阻断]",
    "verdict.info_mark": "[信息]",
    # ---- Revision-suggestions specific ----------------------------------
    "suggestions.opening": (
        "下文将每个高优先级问题与一项具体修订配对。所有建议均源自深度审稿问题包，"
        "应用前请由作者自行判断是否合适。"
    ),
    "suggestions.entry_title": "### {label}：{title}",
    "suggestions.no_suggestion_text": "_未生成直接文本改写，请按下列额外操作执行。_",
    "suggestions.original_block": "原文",
    "suggestions.suggested_block": "建议改写",
    "suggestions.rationale_block": "理由",
    "suggestions.actions_block": "额外操作",
    # ---- Misc -----------------------------------------------------------
    "misc.dash": "—",
    "misc.section_unknown": "未知",
    "misc.review_default_lane": "review",
}

STRINGS: dict[str, dict[str, str]] = {"en": EN, "zh": ZH}

DEFAULT_LANG = "en"


def normalize_lang(lang: str | None) -> str:
    """Coerce a free-form language code to ``en`` or ``zh``."""
    if not lang:
        return DEFAULT_LANG
    lowered = lang.strip().lower()
    if lowered in STRINGS:
        return lowered
    if lowered.startswith("zh") or lowered.startswith("cn"):
        return "zh"
    return DEFAULT_LANG


def t(key: str, lang: str = DEFAULT_LANG, **kwargs: Any) -> str:
    """Look up ``key`` in the given language with optional ``str.format`` args.

    Falls back to English when the key is missing in the requested language,
    then to the key itself if the English entry is also missing.
    """
    target = STRINGS.get(normalize_lang(lang), EN)
    text = target.get(key)
    if text is None:
        text = EN.get(key, key)
    return text.format(**kwargs) if kwargs else text


def available_languages() -> tuple[str, ...]:
    return tuple(STRINGS.keys())
