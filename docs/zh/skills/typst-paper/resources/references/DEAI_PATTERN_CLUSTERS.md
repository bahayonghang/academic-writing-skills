# 基于证据的双语学术去 AI 模式簇

> 模式谱系来自 Wikipedia 社区维护的 “Signs of AI writing” 指南及通用 humanizer 先例，
> 本文件按学术证据保全要求重新设计。这些模式簇是审阅提示，不是 AI 作者身份判定规则。

## 目的与自动化边界

完成核心 de-AI 指南检查后，若中英文可见正文仍有低信息修辞，可加载本文件。七类模式全部
为 `[LLM]` / C 档 `llm-only`。不得把它们加入 `deai_check.py`、
`AI_TONE_THRESHOLDS.yaml`、`AI_TONE_TERMS.md` 或 `--tier`；单个词、词尾、标点或枚举数量
都不能构成 finding。

判断前先抽取 `source_span`、`rhetorical_move`、`claim`、局部 `evidence_anchor`、
`scope_and_certainty` 与 `protected_units`。受保护单元包括数字、单位、实体、术语、`@cite`、
`<label>`、公式、代码、宏、Typst 函数和 source layout。现有 trace/density 分数仍是启发式
可读性信号，不是 AI probability，也不是本模式簇的验收分数。

## H-ING：无依据的分析尾句

**应命中**：英文分词尾句或中文伴随式尾句新增意义、原因、后果或范围，但前面的观察和
可见证据不支持该关系。

**不命中**：尾句只复述已报告指标，或有局部图表、分析或引用锚点。不得仅根据
`highlighting`、`ensuring`、“突出”“确保”或表层语法命中。

**修复**：删除证据尚未支持的推断、绑定可见证据，或降为可检验假设；不得补造分析。

## H-PROMO：宣传性评价

**应命中**：“groundbreaking / transformative / 变革性 / 重要”等评价没有绑定可观察属性、
比较对象、条件或引用。

**不命中**：使评价成立的属性和证据位于局部上下文，并清楚限定适用范围。

**修复**：写出属性和证据锚点；否则标记 `[PENDING VERIFICATION]` / `待补证`，不得补数字、
基线或来源。

## H-ATTR：模糊归因

**应命中**：读者无法确定谁提出 claim、哪一来源支持它或归因覆盖什么范围，例如没有来源的
“experts argue / 专家认为”。

**不命中**：作者或机构具名、引用可解析、被归因 claim 的边界清楚。诚实说明证据有限也可以
是合法 limitation。

**修复**：具名并引用来源，或改为论文自身的受限陈述；绝不虚构权威或引用。

## H-PRED：间接谓词堆叠

**应命中**：`serves as / represents / marks / 作为 / 标志着` 只延长简单谓词，没有说明技术
关系。例如，“Table 2 serves as a presentation of the results”可改为“Table 2 presents the
results”。

**不命中**：谓词精确表达映射、代理、状态转换、数学表示或其他领域关系。

**修复**：只有关系类型和 certainty 均不变时才简化。

## H-TERM：同义词循环

**应命中**：同一领域实体在短距离内被无声明地反复使用不同中英文名称，使 identity 或 scope
产生歧义。

**不命中**：上位/下位概念或别名已经显式定义，且切换是为了提高精确性。

**修复**：选用作者确认的规范术语并保持一致；保护术语表、缩写、模型名、数据集名、基因名
和化学名。

## H-SCOPE：虚假范围

**应命中**：`from X to Y / 从 X 到 Y`、枚举数量或对称结构暗示的覆盖范围超过实际材料或
证据。

**不命中**：范围精确，每个条目都真实、必要且有支持。三个真实贡献仍保留三项，不得为打破
rule of three 增删内容。

**修复**：将 scope 收窄到论文实际覆盖范围；不得虚构第四项或为了节奏删除已支持结果。

## H-OUTLOOK：空泛回弹结尾

**应命中**：challenge 或 limitation 后用没有结果、行动、条件或边界的积极口号回弹。

**不命中**：结尾回到已支持结果、提出具体 future test 或诚实说明 scope limitation。

**修复**：删除口号，或换成有证据的结论；保留不利结果、trade-off 与合法 hedge。

### 与防御性推测解释的分界

H-OUTLOOK 处理空泛回弹。防御性推测解释必须同时包含多个具体机制、逐项证据或区分检验缺口，
以及 terminal caveat。诚实说明“mechanism remains undetermined / 机制尚未确定”不是
H-OUTLOOK。

两种表面现象若来自同一 claim-evidence 缺口，只输出一条 finding。满足 defensive 组合判据
时，以 evidence calibration 为 primary，empty outlook 只记为 secondary style facet。只有
source span、根因和 repair 相互独立时才拆分；style-only H-OUTLOOK 不进入 `paper-audit`
claims lane。

## 审阅、改写与保真复核

默认输出 finding、风险摘要或 rewrite blueprint。只有用户明确要求正文改写时才给 replacement
prose。改写前逐项登记 claim、evidence、数字、引用、标签、公式、实体、术语、hedge、limitation
与 scope。保护 `@cite`、`<label>`、公式、代码、`#set`、`#show`、`#let`、宏和 source layout。

可调整局部句法和修辞壳；跨段或章节重排需要另行授权。改写后核对受保护单元是否丢失或新增、
certainty 是否提高、scope 是否扩大。

复用既有 `[LLM]` proposal 契约：

```text
Changed: <local restructuring and rhetorical shells removed>
Protected: <claims, evidence, Typst anchors, terminology, certainty, and scope retained>
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
未做 provider-backed eval、作者盲评或真实论文精确率测量时，效果仍是
`missing evidence / UNVERIFIED`。
