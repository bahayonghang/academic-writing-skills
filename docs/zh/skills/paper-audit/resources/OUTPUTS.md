# 输出产物

`paper-audit` 不同模式的输出不同。

## Quick-Audit / Gate 产物

对于 `quick-audit`、`gate` 和 `polish` precheck，主产物是可读报告：

- severity 分级问题
- checklist 结果
- score summary
- gate verdict（如果是 `gate`）

## Deep-Review 产物

### `final_issues.json`

deep-review 的主产物，也是结构化问题清单的事实来源。

常见字段：

- `title`
- `quote`
- `explanation`
- `comment_type`
- `severity`
- `confidence`
- `source_kind`
- `source_section`
- `related_sections`
- `root_cause_key`
- `review_lane`
- `gate_blocker`
- `quote_verified`

### `overall_assessment.txt`

简短总评。应说明：

- 这篇论文是否有价值
- 最大的 2 到 3 个风险点
- 这些问题是否可修

### `review_report.md`

人类可读的最终深审报告。

典型结构：

- overall assessment
- major / moderate / minor issues
- Phase 0 自动审查结果
- score summary
- revision roadmap

### `peer_review_report.md`

面向期刊 / SCI 审稿场景的 reviewer-facing 报告，由 deep-review artifacts 派生而来。

典型结构：

- Summary
- Major Issues
- Minor Issues
- Recommendation

当你需要更接近期刊审稿系统提交格式的结果时，优先查看这个文件；`review_report.md` 仍保留为证据更完整的深审报告。

### `revision_roadmap.md`

按优先级排列的修订动作清单。

### `committee/consensus.md`

deep-review 的委员会共识产物。

常见内容：

- 总分（`1-10`）
- editor verdict
- 评分公式拆解
- 最先改的 3 个问题

评分规则：

- 基础分 `9.0`
- 扣分：`1.5 * major + 0.7 * moderate + 0.2 * minor`
- 下限 `1.0`
- 若 editor verdict 是 `Desk Reject`，总分封顶 `4.0`

## Workspace 中间产物

这些文件支持 deep review，但不是最终交付物：

### `section_index.json`

记录 section 与行号范围映射。

### `claim_map.json`

记录 headline claims 和 closure targets，给 cross-cutting lanes 使用。

### `paper_summary.md`

给 reviewer lanes 共享上下文的结构化摘要。

### `all_comments.json`

合并前的全部 lane 输出集合。

### `committee/*.md`

委员会分角色记录（若产生）：

- `editor.md`
- `theory.md`
- `literature.md`
- `methodology.md`
- `logic.md`

## Script 与 Reviewer Provenance

`source_kind` 用于区分来源：

- `script`
- `llm`

分数可以综合，但 issue bundle 必须保留 provenance。
