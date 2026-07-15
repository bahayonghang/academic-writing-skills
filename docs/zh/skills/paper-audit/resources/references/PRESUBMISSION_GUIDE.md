# 预提交模式集成

脚本如何支持`PRESUBMISSION`层插入每个`paper-audit`模式。
用于确定性规则列表、严重性校准和AI-tone术语禁令
列表，参见`references/PRE_SUBMISSION_RULES.md`.

接下来阅读：
- `references/PRE_SUBMISSION_RULES.md`用于规则分类和术语列表。
- `references/MODE_GUIDE.md`用于完整模式工作流程。

## 目的

`PRESUBMISSION`是确定性的最后一周机械层（em破折号，
AI-tone 术语频率、摘要完整性、LaTeX 引文/标签/方程
卫生、段落形状的弱信号、具体的标题）。它**不是一个
公共模式**；它在现有模式内运行。

## 模式行为矩阵

|模式|提交前角色|晋升|门效应|
|---|---|---|---|
| `quick-audit` |内联机械就绪信号|不适用|不适用|
| `gate` |咨询+关键阻碍|不适用|只有“严重”无法通过大门|
| `re-audit` |机械结果的回归比较|不适用|不适用|
| `deep-review`阶段0|审阅者通道的脚本上下文|完整/编辑重点可能会将高信号项目提升为`pre_submission_readiness`审查通道|不适用|

对于重点理论、文献、方法论和逻辑评论，
`PRESUBMISSION`研究结果仅停留在第 0 阶段的背景下。他们永远不会成为
集中束通道问题。

## 严重性映射

|预提交来源分类|快速/门严重性|深入审查捆绑严重性|
|---|---|---|
|批判的|严重/P0|主要+`gate_blocker=true` |
|主要的|专业 / P1|缓和|
|次要的|未成年人/P2|仅次要或阶段 0|

`gate`仅在关键脚本结果或失败的清单项目上失败。主要的
和未成年人`PRESUBMISSION`调查结果仅供参考。

## PDF 与源行为

|检查组|LaTeX/Typst 源|PDF模式|
|---|---|---|
|长划线扫描|跑步|跑步|
|禁用AI音调|跑步|跑步|
|抽象五要素检查|跑步|跑步|
|长段落/主题句弱信号|跑步|跑步|
|LaTeX 引文领带卫生|跑步|跳过|
|标签空间/连字符规则|跑步|跳过|
|编号方程参考规则|跑步|跳过|
|源标题规则|跑步|跳过|

跳过必须在脚本输出中作为忽略的注释或元数据可见，决不
作为问题。

## 出处规则

- 全部`PRESUBMISSION`调查结果保留`[Script]`出处。
- 结果必须锚定到源文本、行号或部分。
- 面向审稿人的散文绝不能默默地吸收机械的发现，就好像
它们是审稿人的判断。
- 仅进行技能审核；它不会重写论文来源。路由重写
要求特定格式的写作技巧。

## 与集成`gate`

1. `gate`读`PRESUBMISSION`调查结果及其自己的清单。
2. 关键发现转化为阻碍因素。
3. 主要和次要调查结果出现在咨询建议中
判决和 EIC 筛选。
4. IEEE 伪代码规则：区分强制规则和 IEEE 安全推荐规则。

## 与集成`deep-review`

1. `audit.py --mode deep-review`运行`PRESUBMISSION`作为阶段 0 的一部分。
2. 焦点路由决定这些发现会发生什么：
   - `--focus full`或者`--focus editor`：可以促销高信号项目
进入`pre_submission_readiness`审查通道和并排合并
审稿人的调查结果。
   - `--focus theory|literature|methodology|logic`： 保持`PRESUBMISSION`在
仅阶段 0 上下文；不要将它们视为重点审查通道问题。
3. 促销不会绕过整合。促销商品仍在流通
   `consolidate_review_findings.py`和`verify_quotes.py`.

## 与集成`re-audit`

`re-audit`比较新的`PRESUBMISSION`上次运行的结果。
状态标签遵循标准`re-audit`架构：`FULLY_ADDRESSED`,
`PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`.

机械回归与审稿人发现的回归一起报告，但是
保留他们的`[Script]`出处，以便用户可以区分风格漂移
实质性审稿人的担忧。
