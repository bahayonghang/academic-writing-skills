# 路由规则 — 完整详细信息

`latex-paper-en` 的扩展布线指南。 SKILL.md 仅保留核心规则；该文件保留完整的决策说明。

## 模块推理

- 在提出后续问题之前，从用户请求中推断出模块。仅当两个或多个模块在关键字路由后同样合理时才请求该模块。
- 如果用户要求一轮进行 2-3 次兼容检查，请按顺序运行它们，而不是强制进行单模块回复。
- 需要多个模块时的执行顺序：`compile` -> `bibliography` -> `format` -> `figures` / `tables` / `caption` / `pseudocode` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` / `abstract` -> `section-writing` -> `title` / `expression` / `translation` / `adapt`.
- 当对同一篇散文应用多次润色时，要从粗到细——论证/逻辑——>句子结构——>词汇/格式——并且不要颠倒过来；参见 `references/modules/workflow.md`。

## 在相邻模块之间进行选择

- 更喜欢`logic`对于横截面对齐请求（摘要、介绍、结论）、介绍漏斗问题或贡献漂移；更喜欢`literature`仅当问题具体涉及相关工作组织、比较或差距推导时。
- 当用户要求起草、重写、重组或审阅者润色特定部分，或要求段落角色、迷你大纲、反向大纲或声明证据图时，首选 `section-writing`。当用户要求检查是否出现问题时，优先选择诊断模块。
- 保留 `experiment` 用于结果、讨论、基线、消融、重要性、限制和结论完整性问题，即使用户将它们表述为“逻辑”问题。

## 特殊标志和加载规则

- 为了`section-writing`， 加载`references/modules/section-writing.md`，那么恰好有一个活动部分指南来自`references/writing/section-writing/`除非用户也要求流程或自我审查。
- 对于 `journal narrative`、`Nature-style`、`Results narrative`、`Discussion structure`、`full-paper argument` 或 `期刊式` 请求，加载 `references/writing/article-architecture.md`。普通语法润色或不包含期刊结构要求的会议摘要润色不应加载该文件。
- 对于整篇论文的动机/红线问题（“每个介绍承诺都得到测试和解决吗？”），运行`logic`和`--motivation-thread`;它附加一个只读的 Promise Map + Closure Map 启发式并保留默认值`logic`输出不变。
- 对于分级 de-AI / AIGC 维度分析，运行`deai`和`--tier light|medium|heavy`;它缩放阈值，添加 D1 句子长度检查，并按维度 (D1-D5) 标记结果。省略`--tier`保留默认输出。

## 故障处理

- 当脚本失败时，停止当前模块，报告确切的命令和退出代码，并推荐下一个最小的有用回退，而不是默默地切换模块。

## 输出合约详情

- 对于`literature`，默认先诊断+重写蓝图；仅当用户明确要求散文时才产生段落级重写。
- 对于 `section-writing`，返回部分目标、紧凑大纲、段落角色、重写蓝图或散文提案、主张证据图和自我审查清单。标记缺失的证据而不是填写它。

## 改写契约适用范围

判定标准只有一条：**该模块是否产出可直接替换原文的文本？** 若它只产出"该怎么改"的指令，则改写发生在 LLM 侧，只适用 `[LLM]` 层。三组逐项列出——不要因为某模块"看起来像润色"就给它加契约。

- **纳入契约（`[Script]` + `[LLM]` 两层）**：`expression`、`grammar`、`sentences`、`translation`。
- **仅 `[LLM]` 层**（无脚本，或脚本只出指令不出替换文本）：`section-writing`、`caption`、`adapt`、`deai`。`deai` 的 `-> Suggestion: vary sentence length` 这类输出是行为指令；LLM 依此产出的改写带 `[LLM]` 层字段。
- **排除——完全不加契约段**：`compile`、`format`、`bibliography`、`figures`、`tables`、`pseudocode`、`logic`、`literature`、`experiment`、`abstract`、`title`。这些是纯诊断模块，加字段只是噪音。

### 分层规则

- `[Script]` 只能置 `Meaning-Check: NEEDS-LLM`，且只能置 `none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`。规则脚本若声称 `PRESERVED`，等于制造虚假保证，比没有契约更糟。
- `[LLM]` 可置 `PRESERVED` 与 `Risk-Flags` 全闭集，但 `PRESERVED` 始终是待作者核对的提案。
- `Risk-Flags` 是闭集：`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`、`overstatement`、`ambiguity`、`terminology-drift`、`invented-claim`。不得发明新取值。
- 改写不得升高措辞强度。强度变化时置 `Risk-Flags: overstatement`，并引用 `references/evidence/over-claim-guard.md` 与 `references/writing/style-guide.md` 中的报告动词四级阶梯。
- 原文含义确实不清时，置 `ambiguity` 并给出保守读法——绝不静默选择更强的那一种。

### 编辑轴与追问边界

- `--goal grammar|clarity|concision|coherence` 是这次编辑要解决什么；`--strength minimal|moderate|restructure` 是允许改到多深。两轴正交：`--goal concision --strength minimal` 与 `--goal coherence --strength restructure` 都合法。`--goal` 不是严重度阶梯。
- 幅度语义（三方一致）：

| 取值          | 允许改动                                | 不得改动                     |
| ------------- | --------------------------------------- | ---------------------------- |
| `minimal`     | 词汇、标点、明显语法错                  | 句子结构、段落顺序           |
| `moderate`    | 上加：拆分/合并句子、语序调整            | 段落顺序、增删论断           |
| `restructure` | 上加：段落顺序、话题句位置               | 增删论断（永远禁止）         |

- 三档都受核心规则约束：绝不添加原文没有的论断、机制、引用、结果、局限、方法或作者意图。
- 默认值为 `--goal grammar` 与 `--strength minimal`——能解决问题的最小改动。
- 这不会变成固定问卷。既有规则不变：自动推断模块，不默认追问。编辑目标、幅度或作者原意只在答案会改变本次编辑时才追问——例如某句歧义到两种读法会产出不同改写时。
- `--tier` 语义不变：`deai` 的检测灵敏度（light 报得少、heavy 报得多）。它绝不被挪用为编辑幅度控制，两套词汇刻意不重叠。

## 安全原理（全文）

- 不要发明引文、指标、基线或实验结果——一旦用户信任，捏造的证据比明确标记的差距更难撤回。
- 离开`\cite{}`, `\ref{}`, `\label{}`、自定义宏和数学环境默认情况下保持不变——在 diff 中的杂散编辑比散文编辑更难发现，并且会默默地破坏编译。
- 将生成的散文视为提案，而不是提交 - 将源代码保留检查与重写分开，以便用户可以验证每个步骤。
- 除非用户明确要求外部验证或确认引文元数据可以发送到第三方 API，否则请勿启用在线参考书目检查。
- 这`deai`模块提高了可读性；它不是一个逃避检测器的工具，也不会消除披露义务。如果法学硕士在论文中扮演重要角色，请提醒用户根据目标地点的政策进行披露（`references/venues/ai-disclosure.md`具有每个期刊或会议的矩阵 - 有些期刊或会议要求在投稿信、专用部分或清单中进行披露）。
