# 学术 de-AI 模式簇与保真复核契约

> 适用于 `latex-paper-en`、`latex-thesis-zh` 与 `typst-paper` 的 de-AI runtime
> references、fixtures、evals 和跨 surface contract test。

## Contract: 七类模式只允许 claim-local LLM 判断

新增模式固定为 H-ING、H-PROMO、H-ATTR、H-PRED、H-TERM、H-SCOPE、H-OUTLOOK。
`[LLM]` 必须先提取 `source_span`、`rhetorical_move`、`claim`、`evidence_anchor`、
`scope_and_certainty` 与 `protected_units`，再判断修辞是否超出可见证据或改变实体/范围。

七类均为 C 档 `llm-only`。不得把 `-ing`、`serves as`、破折号、三个并列项、hedge 或
单个高频词当作 AI 作者身份信号；不得向 `deai_check.py`、threshold YAML、tone-term
reference、`DIMENSION_MAP` 或 `DEFAULT_THRESHOLDS` 添加对应类别。现有脚本 trace/density
分数是启发式可读性指标，不是 AI probability，也不作为本契约的验收分数。

**Tests Required**：`tests/contracts/test_deai_pattern_cluster_contract.py` 必须锁定三个
surface 的七类命中组合、反例、渐进加载路由和脚本零扩张边界。

## Contract: 每类必须同时有正例和证据充分反例

每个 surface 的本地 fixture 必须包含 A-H：

- A：H-ING/H-PROMO/H-ATTR/H-SCOPE/H-OUTLOOK 组合正例；
- B：H-PRED 正例；
- C：H-TERM 正例；
- D-H：分别保护有证据的分词/评价、具名归因、真实三项范围、精确技术谓词/定义换名、
  诚实 limitation 与具体 future test。

正例只证明应进行学术修辞审阅，不证明文本由 AI 生成。反例是契约组成部分，不得通过扩大
词表或删除合法结构来提高命中数量。

## Contract: H-OUTLOOK 与 defensive-rhetoric 去重

H-OUTLOOK 处理 challenge/limitation 后没有结果、行动、条件或边界的积极回弹；
defensive-rhetoric 处理“多个具体机制 + 逐项证据/区分检验缺口 + terminal caveat”。诚实的
`mechanism undetermined` 与 scope limitation 都不是 H-OUTLOOK。

同一段的两个表面现象若来自同一 claim-evidence 缺口，只输出一条 finding。满足 defensive
组合判据时以 evidence-calibration finding 为 primary，H-OUTLOOK 只作为 secondary style
facet。只有 source span、根因和 repair 可独立定位时才拆分；style-only finding 不进入
`paper-audit` lane。

## Contract: 正文改写必须经过 fidelity audit

默认停在 findings、risk summary 或 rewrite blueprint。只有用户明确要求正文改写时才提供
prose proposal，并执行 `audit -> rewrite -> fidelity audit`：

1. 改写前记录 claim、evidence、数字、引用、公式、标签、术语、实体、certainty、scope 与
   limitation；
2. 允许删除修辞壳、合并冗余或局部拆句，不默认重排段落/章节；
3. 改写后逐项核对：不得新增 claim/因果/主体/引用/数字，不得提高 certainty，不得扩大或
   删除 scope/limitation；
4. 缺少支持时写 `needs evidence` / `待补证`，不补造内容。

prose proposal 复用既有四字段和闭集：

```text
Changed: <what changed>
Protected: <anchors and academic payload kept>
Meaning-Check: PRESERVED | NEEDS-LLM
Risk-Flags: none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim
```

`PRESERVED` 是 `[LLM]` 提案，不是工具证明或作者批准。

## Convention: 作者样本是最低优先级可选约束

作者已确认样本只能校准节奏、句法偏好和语气，优先级低于用户本次要求、venue/体裁、术语表、
语法锚点和 claim-evidence/scope。没有样本时使用目标 skill 的既有 academic tone；不得推测
作者人格，也不得自动注入第一人称、观点、幽默或情绪。

## Convention: 证据声明与归属

模式谱系来自 Wikipedia 社区维护的 “Signs of AI writing” 及通用 humanizer 先例，已经按
学术证据保全要求重构。不得称为官方规范、AI 检测器或 detector-evasion 方法。静态 fixture
和 contract test 只证明契约存在；未执行 provider-backed eval、作者盲评或真实论文评估时，
效果必须标为 `missing evidence / UNVERIFIED`。

## Convention: 中文正文的冒号/分号建议归属表达指南

`latex-thesis-zh/references/writing/academic-style-zh.md` §5.4 是这项写作建议的唯一规则源；
expression 与 deai 只按需引用。它处理标签壳、分号堆叠与句间关系，不新增 H-*、E-*、D1
判据或数量阈值，不以标点判断 AI 作者身份。段落论证仍归 logic，论断强度仍归 over-claim-guard。
必要引出、复杂并列、模板规定及数学/引用/代码/URL 等受保护内容保持。

验证需同时观察过度用法的实际改写、仅并列事实不补因果、合理标点与源码保留三个分支；
`evals.json` 的字符串/正则断言只检查语料，不替代实际响应的保真审阅。
