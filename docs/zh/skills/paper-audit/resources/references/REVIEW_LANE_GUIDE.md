# 查看审查通道指南

默认`deep-review`审查通道：

## 分段审查通道

- `section_intro_related`
  - 检查研究框架、新颖性定位以及论文前部作出的承诺；观察同一组四项段落弧线信号：
    `P-ARC-LEAD`（段首主题引导）、`P-ARC-CLOSE`（段末收束）、
    `P-ARC-LINK`（相邻段接口）和 `P-ARC-FLAT`（段内展开）；仅缺少显式过渡词
    不等于逻辑断裂
- `section_methods`
  - 检查定义、假设、推导和方法细节；审查方法论接口与论证完整性时，加载 `section_methods` 焦点块（位于 `SUBAGENT_TEMPLATES.md`）
- `section_results`
  - 检查度量计算、证据充分性和比较公平性
- `section_discussion_conclusion`
  - 检查解释、限制处理和声明结束
- `section_appendix`
  - 检查附录材料是否支持或矛盾标题主张

## 横切审查通道

- `claims_vs_evidence`— 最多 8 个问题
- `notation_and_numeric_consistency`— 最多 10 个问题
- `evaluation_fairness_and_reproducibility`— 最多 8 个问题
- `self_standard_consistency`— 最多 6 个问题
- `prior_art_and_novelty_grounding`— 最多 6 个问题
- `pre_submission_readiness`— 最多 12 期（仅限全部/编辑焦点；
由高信号填充`PRESUBMISSION`脚本发现）

每审查通道焦点指令、DO/DON'T 规则和分组约定均存在
`SUBAGENT_TEMPLATES.md`。输出限制阻止LLM填充；反复出现的问题
折叠为具有多个示例位置的一个条目。

## 输出规则

每个通道必须输出 JSON 结果匹配`ISSUE_SCHEMA.md`.

`pre_submission_readiness`是故意狭窄的。它可以包含关键或
主要的机械问题，例如破折号、重复的AI 语气词汇、
抽象的结果差距，或根源卫生问题，但它不能吸收
方法论、理论、文献或主张有效性审核员的工作。什么时候
`--focus methodology|theory|literature|logic`被选中，保留这些发现
仅在阶段 0 自动化环境中。
