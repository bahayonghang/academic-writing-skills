# `writing-anti-ai` -> academic de-AI 差异矩阵

来源锚点相对 `ref/claude-scholar/skills/writing-anti-ai/`；现有实现锚点相对
`academic-writing-skills/`。判定采用 `keep / adapt / reject`，`adapt` 项必须映射到设计中的
`H-*` 契约或 `F-*` fidelity 契约。

| ID | 来源能力 | 现有覆盖与风险 | 判定 | 落点 |
| --- | --- | --- | --- | --- |
| W1 | 过度强调意义 | 三方 guide 已有 Empty Phrases、Information Density、Academic Restraint | adapt：只补“评价必须绑定可观察属性”，不加词表 | H-PROMO |
| W2 | 过度强调知名度/媒体 | 学术论文中的作者/venue 信息可能合法，实质问题通常是来源与相关性 | reject 独立 de-AI 规则；无来源时归模糊归因 | H-ATTR boundary |
| W3 | `-ing` 尾句的肤浅分析 | 当前无显式段落级规则；`highlighting` 也可合法引出由数据支持的含义 | adapt：判断尾句是否新增未获证据的因果/意义 | H-ING |
| W4 | 宣传广告式语言 | 已有克制措辞和空话，但未把“价值判断 -> 可观察属性”写成闭环 | adapt，LLM-only | H-PROMO |
| W5 | 模糊归因 | 模糊量化已有，`experts argue` 等来源责任未显式覆盖 | adapt：定位 attribution、source、claim 三元组 | H-ATTR |
| W6 | 公式化挑战/未来展望 | 合法 limitation 不得删；空泛“尽管挑战仍前景光明”是增量；与 defensive-rhetoric 的 terminal caveat 区域相邻 | adapt：仅检查无具体问题、响应或边界的回弹结尾；同根因 finding 按下文规则合并 | H-OUTLOOK |
| W7 | 高频 AI 词汇 | 三方已有 term thresholds、filler 与 throat-clearing | reject 词表扩张；单词不构成 AI 证据 | existing |
| W8 | 系动词回避 | `represents`/`serves as` 在技术定义中可合法；当前无语义边界 | adapt：只在间接谓词不提供关系类型时简化 | H-PRED |
| W9 | 否定式排比 | 已有 binary contrast shell 及 baseline/criterion/evidence 反例 | reject 重复实现 | existing |
| W10 | 强行三段式 | 已有 Mechanical Structures，但来源建议“改成二或四项”会损坏真实枚举 | adapt 边界：数量不是信号，删的只能是语义冗余项 | H-SCOPE boundary |
| W11 | 刻意换词/同义词循环 | 当前未显式覆盖，且学术术语漂移会改变 domain entity | adapt：术语一致性优先于 elegant variation | H-TERM |
| W12 | 虚假范围 | 当前无显式覆盖 | adapt：范围框架必须与实际列举和证据集合一致 | H-SCOPE |
| W13 | 破折号过度使用 | 三份脚本已有 `punctuation:em_dash_overuse` 阈值和 tier 缩放 | reject 全禁；保持“过度使用”而非单次命中 | existing |
| W14 | 粗体过度使用 | 属格式/模板责任，不是学术 claim 质量 | reject de-AI 重复所有权 | out of scope |
| W15 | 内联标题垂直列表 | 列表可用于方法、贡献和审阅报告；格式检查另有 owner | reject | out of scope |
| W16 | 协作交流痕迹 | 现有 generic opening/throat-clearing 可处理正文残留；skill 自身输出不属于论文正文 | reject 新类别 | existing/router boundary |
| W17 | 知识截止免责声明 | “as of date”与“证据有限”可为合法范围边界 | reject blanket deletion；缺来源时走 H-ATTR，真实限制保留 | H-ATTR boundary |
| W18 | 填充短语 | 三方 filler/throat-clearing 已覆盖 | reject 重复词表 | existing |
| W19 | 过度限定 | 当前 overclaim 强调避免过度确定；机械删 hedge 会反向放大 claim | adapt 为 fidelity 约束：可合并重复 hedge，不得提高 certainty rung | F-CLAIM |
| W20 | 通用积极结论 | 当前未显式覆盖 | adapt：结尾必须回到已证结果、具体后续动作或诚实边界 | H-OUTLOOK |
| W21 | Personality and Soul | 自动加“我”、观点、幽默、情绪与学术体裁冲突且会制造新 claim | reject | prohibited |
| W22 | workflow / 50 分评分 / examples | audit-rewrite 顺序有用；评分无校准；示例多处捏造事实 | adapt 流程，reject 分数与示例内容 | F-LOOP |

## 七个新增 LLM-only 模式簇

| Contract | 命中组合 | 证据充分反例 | 修复边界 |
| --- | --- | --- | --- |
| H-ING unsupported analytical tail | 分词/伴随尾句引入新的意义、原因或结果，但前文数据与引用不支持该关系 | 尾句只复述已报告指标，或有明确 figure/citation/analysis anchor | 删除未赚到的推断，或降为待验证假设；不按 `-ing` 词面命中 |
| H-PROMO promotional evaluation | 价值形容与“重要/突破/丰富”评价没有可观察属性、比较或证据 | 评价紧邻指标、baseline、条件和引用 | 写属性与证据；缺失时 `needs evidence`，不虚构数字 |
| H-ATTR vague attribution | 归因主体泛化，读者不能定位 source、scope 或具体 claim | 具名作者/机构 + 可解析引用 + 清晰归因边界 | 补 source 或改为作者自己的受限陈述；不伪造引用 |
| H-PRED indirect predication | `serves as / represents / marks` 等仅延长句子且不声明技术关系 | 该谓词精确表达映射、代理、状态转换或数学语义 | 在关系不变时简化；技术含义存在则保留 |
| H-TERM synonym cycling | 同一 domain entity 在短距离内无声明地换名，造成实体或范围歧义 | 明确定义的上位/下位概念切换，或为避免歧义的命名 | 选 canonical term 并统一；保护作者术语表和缩写 |
| H-SCOPE manufactured breadth | `from X to Y`、枚举数量或对称结构暗示超出实际材料的覆盖范围 | 列举集合完整、范围声明精确，三项均为真实且必要的内容 | 收窄 scope；不为“打破三项”增删真实贡献 |
| H-OUTLOOK empty recovery ending | challenge/limitation 后用空泛积极承诺收尾，没有结果、行动、条件或边界 | 结尾回到可见结果、具体后续实验或明确 scope limitation | 删除口号或改为证据支持的结论；保留实质不利结果 |

## 与 defensive-rhetoric 契约的分界

`H-OUTLOOK` 判断 limitation/challenge 后是否用无内容的积极承诺回弹；
`defensive-ai-rhetoric-contract.md` 判断的是“多个具体机制 + 逐项证据/区分检验缺口 +
terminal unverifiability caveat”。诚实说明“机制未定”不是 H-OUTLOOK，合法范围局限也不能因
段尾出现 limitation 而命中。

同一段同时满足两者时：

1. 若两种表面现象来自同一 claim-evidence 缺口，只输出一条 finding；满足 defensive 组合判据
   时以 evidence-calibration finding 为 primary，并把 empty outlook 记为 secondary style facet。
2. 只有 source span、根因和 repair 都可独立定位时才拆成两条 finding；不得对同一位置给重复
   修复，也不得让 style-only H-OUTLOOK 占用 `paper-audit` claim-evidence lane。

## Fidelity 契约

### F-LOOP：`audit -> rewrite -> fidelity audit`

只有用户明确要求正文改写时才进入 rewrite。改写前记录 claim、evidence、数字、引用、术语、
限定条件与语法锚点；改写后逐项核对，不接受“整体意思差不多”。

### F-CLAIM：信息保留清单

- 每个原 claim 仍存在，或被明确标记为因缺证而删除/降级；
- 不新增 claim、因果关系、实验、数字、引用、主体或范围；
- certainty rung 不提高，合法 hedge 与 limitation 不因“自然化”被删除；
- canonical term、`\cite{}`、`\ref{}`、`\label{}`、公式、Typst `@cite`/`<label>` 保持；
- 局部句法和修辞壳可变，章节结构与 source layout 默认不变，除非用户另行授权。

### F-OUTPUT：现有四字段

prose proposal 复用现有字段，不创建“human score”或 AI probability：

```text
Changed: <局部重组及删去的修辞壳>
Protected: <引用、数字、术语、公式与边界>
Meaning-Check: PRESERVED | NEEDS-LLM
Risk-Flags: <既有闭集>
```

`PRESERVED` 只是 `[LLM]` 提案，作者仍需复核；没有 provider 或人工评估时不得把它解释为
已验证的语义等价。
