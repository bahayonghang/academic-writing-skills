# 基于证据的学术去 AI 模式簇

> 模式谱系来自 Wikipedia 社区维护的 “Signs of AI writing” 指南及通用 humanizer 先例，
> 本文件按学术证据保全要求重新设计。这些模式是审阅提示，不是 AI 作者身份判定规则。

## 目的与自动化边界

完成核心 de-AI 指南检查后，若可见正文仍有低信息修辞，可渐进加载本文件。七类模式全部为
`[LLM]` / C 档 `llm-only`：单个词、词尾、标点或枚举数量都不能构成 finding。不得把这些
模式加入 `deai_check.py`、threshold YAML、tone-term 词表或 `--tier`。

判断前先抽取：

1. `source_span` 及其章节角色；
2. `rhetorical_move` 与它新增或改变的 claim；
3. 局部 `evidence_anchor`，如指标、比较、图表、实验或引用；
4. `scope_and_certainty`，包括 hedge 与 limitation；
5. `protected_units`：数字、单位、实体、术语、引用、标签、公式、宏和 source layout。

现有脚本的 trace/density 分数仍是启发式可读性指标，不是 AI probability，也不是本模式簇的
验收分数。

## H-ING：无依据的分析尾句

**应命中**：分词式或伴随式尾句新增了意义、原因、后果或范围，但前面的观察和可见证据不
支持该关系。

**不命中**：尾句只复述已报告指标，或有局部 figure、analysis、citation anchor。不得仅因
出现“突出、确保、反映、表明”等词就命中。

**修复**：删除证据尚未赚到的推断、绑定可见证据，或降为可检验假设；不得补造分析。

## H-PROMO：宣传性评价

**应命中**：“突破性、变革性、重要”等评价没有绑定可观察属性、比较对象、条件或引用。

**不命中**：评价紧邻使其成立的属性和证据，并清楚限定适用范围。

**修复**：写出可观察属性和证据锚点；两者均不存在时标记【待补证】，不得补数字、基线或来源。

## H-ATTR：模糊归因

**应命中**：读者无法确定谁提出 claim、哪一来源支持它或归因覆盖什么范围，如没有可解析
来源的“专家认为”。

**不命中**：作者/机构具名、引用可解析、被归因 claim 的边界清楚。诚实说明“证据有限”也
可以是合法 limitation。

**修复**：具名并引用来源，或改为作者自己的受限陈述；绝不虚构权威或引用。

## H-PRED：间接谓词堆叠

**应命中**：“作为、代表、标志着”等结构只延长简单谓词，没有提供技术关系。例如“表 2
作为结果的展示”可简化为“表 2 展示结果”。

**不命中**：谓词精确表达映射、代理、状态转换、数学表示或其他领域关系。

**修复**：只有关系类型和 certainty 均不变时才简化。

## H-TERM：同义词循环

**应命中**：同一 domain entity 在短距离内被无声明地反复换名，使读者无法确认是同一对象
还是不同范围。

**不命中**：上位/下位概念或别名已经显式定义，且切换是为了提高精确性。

**修复**：选用作者确认的 canonical term 并保持一致；保护术语表、缩写、模型名、数据集名、
基因名和化学名。

## H-SCOPE：虚假范围

**应命中**：“从 X 到 Y”、枚举数量或对称结构暗示的覆盖范围超过实际材料或证据。

**不命中**：范围精确，每个条目都真实、必要且有支持。三个真实贡献仍保留三项，不得为打破
rule of three 增删内容。

**修复**：将 scope 收窄到论文实际覆盖范围；不得虚构第四项或为了节奏删除已支持结果。

## H-OUTLOOK：空泛回弹结尾

**应命中**：challenge 或 limitation 后用没有结果、行动、条件或边界的积极口号回弹。

**不命中**：结尾回到已支持结果、提出具体 future test 或诚实说明 scope limitation。

**修复**：删除口号，或换成有证据的结论；保留不利结果、trade-off 与合法 hedge。

### 与防御性推测解释的分界

H-OUTLOOK 处理空泛积极回弹。防御性推测解释必须同时包含多个具体机制、逐项证据/区分检验
缺口，以及整体撤回这些机制的 terminal caveat。诚实说明“机制尚未确定”不是 H-OUTLOOK。

两种表面现象若来自同一 claim-evidence 缺口，只输出一条 finding。满足 defensive 组合判据
时，以 evidence calibration 为 primary，empty outlook 只记为 secondary style facet。只有
source span、根因和 repair 相互独立时才拆分；style-only H-OUTLOOK 不进入 `paper-audit` lane。

## 审阅、改写与保真复核

默认输出 finding、风险摘要或 rewrite blueprint。只有用户明确要求正文改写时才给 replacement
prose。

改写前逐项登记 claim、evidence anchor、数字、引用、标签、公式、实体、canonical term、
hedge、limitation 与 scope。可调整局部句法和修辞壳；未经另行授权，不重排段落或章节。改写
后核对每项是否丢失、新增、提高 certainty 或扩大 scope，并显式报告风险。

复用既有 `[LLM]` proposal 契约：

```text
Changed: <局部重组及删除的修辞壳>
Protected: <保留的主张、证据、锚点、术语、确定性与范围>
Meaning-Check: PRESERVED | NEEDS-LLM
Risk-Flags: none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim
```

`PRESERVED` 仍是供作者复核的提案，不是工具保证。

## 可选作者样本校准

作者确认的样本只能校准节奏、句法偏好和语气，不能覆盖用户本次要求、目标 venue/体裁、
术语、受保护语法、evidence、claim strength 或 scope。没有样本时沿用技能既有学术语气；
不得推测人格，也不得自动注入第一人称、观点、幽默或情绪。

## 证据状态

静态 reference、fixture 和 contract test 只能证明契约存在，不能证明 provider 稳定执行。
未做 provider-backed eval、作者盲评或真实论文查准率评估时，效果保持
`missing evidence / UNVERIFIED`。
