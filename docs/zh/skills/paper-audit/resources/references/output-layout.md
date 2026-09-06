# 输出布局

完整的工作空间布局`deep-review`. `SKILL.md`保留四个文件
概括;该文件是权威的工件图。

下面所有内容只在交付级别允许写入时才产出。写入前先陈述解析出的目标目录——
`--output-dir ./review_results` 是相对于当前工作目录的，因此要念出它展开后的
实际路径。工作区本身是该路径下的一个 slug 子目录，以 `WORKSPACE:` 打印出来。
覆盖保护判定的是工作区，不是 `--output-dir` 父目录：工作区已存在时，按
`references/workflow-detail.md` 中的覆盖确认处理；不得静默覆盖。在交付级别
`T3` 下，以下文件一个都不产出；参见 `references/workflow-detail.md` 中的
不落盘路径。

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
