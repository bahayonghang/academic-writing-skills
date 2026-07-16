# 输出布局

完整的工作空间布局`deep-review`. `SKILL.md`保留四个文件
概括;该文件是权威的工件图。

## 工作区根目录（面向读者，正好四个文件）

- `review_report.md`— 初步深度审查报告
- `revision_suggestions.md`— 针对每个问题的具体修复建议
主要/中度问题，包括建议的重写（如果适用）
- `review_report.html`— 主要报告的 HTML 孪生
- `revision_suggestions.html`— 建议的 HTML 孪生

## `artifacts/`（验证和工具）

- `artifacts/summary/` — `paper_summary.md`, `overall_assessment.txt`,
  `peer_review_report.md`
- `artifacts/data/` — `final_issues.json`, `all_comments.json`,
  `claim_map.json`, `section_index.json`, `revision_suggestions.json`,
  `revision_trajectory.md`
- `artifacts/meta/` — `metadata.json`, `checkpoint.json`,
  `phase0_context.md`, `full_text.md`
- `artifacts/sections/`, `artifacts/comments/`, `artifacts/committee/`,
  `artifacts/references/`

## 报告语言

报告语言由控制`--lang en|zh`（默认：自动检测
从`metadata.json`， 倒退`en`）。语言切换仅影响
报告标题、标签和表格标题 - 问题引用、源标签
(`[Script]`, `[LLM]`），并且结构化字段值保留其原始值
形式。
