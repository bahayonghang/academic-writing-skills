# 代理名册

审阅代理人的完整列表`agents/`. `SKILL.md`保持一条线
概括;这个文件是权威名册。

## 委员会代理（默认深审）

- `committee_editor_agent.md`
- `committee_theory_agent.md`
- `committee_literature_agent.md`
- `committee_methodology_agent.md`
- `committee_logic_agent.md`

## 默认深度审查通道

- `section_reviewer_agent.md`
- `claims_evidence_reviewer_agent.md`
- `notation_consistency_reviewer_agent.md`
- `evaluation_fairness_reviewer_agent.md`
- `self_consistency_reviewer_agent.md`
- `zh_thesis_reviewer_agent.md` — 中文学位论文评阅通道
  （`zh_thesis_review`；仅 `lang == "zh"` 且 deep-review full/editor）
- `prior_art_reviewer_agent.md`
- `synthesis_agent.md`
- `editor_in_chief_agent.md`— EIC 直接拒稿筛选器（用于`gate`模式）
- `revision_coach_agent.md`— 将自由格式的审稿人信件解析为
结构化路线图（用于`re-audit`模式）
- `revision_suggestion_agent.md`— 将每个主要/中等问题转换为
原始/建议文本对以及其他操作；产生
  `artifacts/data/revision_suggestions.json`

## 参考审稿手册（不自动派发）

这些文件保留了供委员会和审查通道提示复用的详细标准；当前工作流不会自动派发它们。
其中的 A5-A7、B6-B10 和 C3-C5 标准仍由现行审查标准链接。
完整派发接线属于后续任务 `paper-audit-specialized-reviewer-wiring`。

- `critical_reviewer_agent.md`— 魔鬼代言人，带有 C3-C5 检查
- `domain_reviewer_agent.md`— A1-A7 评估的领域专业知识
- `methodology_reviewer_agent.md`— 通过 B3-B10 检查的严格方法
- `literature_reviewer_agent.md`——基于证据的文献验证
（选修的，`--literature-search`)
