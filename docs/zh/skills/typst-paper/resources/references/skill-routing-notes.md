# 路由、工作流与安全说明（typst-paper）

本扩展指南从 `SKILL.md` 原样迁出。路由不明确、需要组合模块或出现边界问题时阅读。

## 路由规则（完整）

- 首先从用户请求推断模块。仅当请求仍然同样良好地映射到多个不兼容的模块时才请求该模块。
- 如果用户请求 2-3 项兼容检查，请按顺序运行它们，而不是将所有内容合并为一项通用检查。
- 当需要多个模块时使用此执行顺序：`compile` -> `bibliography` -> `format` -> `pseudocode` / `tables` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` -> `title` / `expression` / `translation` / `adapt`.
- 对同一段正文执行多轮润色时，应从粗到细：论证/逻辑 -> 句子结构 -> 词汇/格式，不要反向执行；参见 `references/modules/WORKFLOW.md`。
- 对于参考书目请求，请在运行脚本之前决定 BibTeX 与 Hayagriva；不要事后猜测格式。
- 摘要-引言-结论对齐、引言漏斗断裂或贡献漂移优先使用 `logic`；只有用户明确要求相关工作综合、比较或研究空白推导时才使用 `literature`。
- 对于整篇论文的动机/红线问题（“每个介绍承诺都得到测试和解决吗？”），运行`logic`和`--motivation-thread`;它附加一个只读的 Promise Map + Closure Map 启发式并保留默认值`logic`输出不变。
- 对于分级 de-AI / AIGC 维度分析，运行`deai`和`--tier light|medium|heavy`;它缩放阈值，添加双语 D1 句子长度检查，并按维度 (D1-D5) 标记结果。省略`--tier`保留默认输出。
- 保持`pseudocode`为了`algorithm-figure`, `algorithmic`, `lovelace`、标题、包装器和类似 IEEE 的样式挂钩问题，即使用户将其表述为格式问题。
- 如果命令失败，请报告确切的命令和退出代码，然后再建议下一个回退；不要默默地用通用的散文评论替换失败的脚本运行。

## 改写契约适用范围

判定标准只有一条：**该模块是否产出可直接替换原文的文本？** 若它只产出关于如何修改的指令，则改写发生在 LLM 侧，只适用 `[LLM]` 层。三组逐项列出——不要因为某个模块"看起来像润色"就给它加契约。

- **纳入契约（`[Script]` + `[LLM]` 两层）**：`expression`、`grammar`、`sentences`、`translation`。
- **仅 `[LLM]` 层**（无脚本，或脚本只出指令不出替换文本）：`adapt`、`deai`。`deai` 的 `-> Suggestion: vary sentence length` 这类输出是行为指令；LLM 依此产出的改写带 `[LLM]` 层字段。
- **排除——完全不加契约段**：`compile`、`format`、`bibliography`、`tables`、`references`、`pseudocode`、`logic`、`literature`、`experiment`、`abstract`、`title`。这些是纯诊断模块，加字段只是噪音。

### 分层规则

- `[Script]` 只能置 `Meaning-Check: NEEDS-LLM`，且只能置 `none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`。规则脚本若声称 `PRESERVED`，等于制造虚假保证，比没有契约更糟。
- `[LLM]` 可置 `PRESERVED` 与 `Risk-Flags` 全闭集，但 `PRESERVED` 始终是待作者核对的提案。
- `Risk-Flags` 是闭集：`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`、`overstatement`、`ambiguity`、`terminology-drift`、`invented-claim`。不得发明新取值。
- 改写不得升高措辞强度。强度变化时置 `Risk-Flags: overstatement`，并引用 `references/OVER_CLAIM_GUARD.md` 与 `references/STYLE_GUIDE.md` 中的报告动词阶梯。
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

## 触发场​​景（完整列表）

当用户已有 `.typ` 论文项目并需要以下帮助时，请使用此技能：

- Typst 编译或导出问题
- 格式或期刊或会议合规性
- BibTeX 或 Hayagriva 的参考书目验证
- 语法、句子、逻辑或表达复习
- 文献综述重组、相关工作综合或研究差距推导
- 翻译或双语润色
- 标题优化
- 伪代码和算法块审查
- 去AI编辑
- 实验部分回顾

## 安全原理（完整）

- 不要发明引文、标签或实验主张——一旦用户信任，捏造的证据比明确标记的差距更难撤回。
- 默认保持 `@cite`、`<label>`、数学块和 Typst 宏不变；这类意外编辑在 diff 中比正文修改更难发现，而且 Typst 通常只在编译时暴露错误。
- 将编译诊断与散文重写分开——将它们捆绑在一起会鼓励用户同时应用两者，并且不知道哪个更改破坏了什么。
- 除非用户明确要求外部验证或确认引文元数据可以发送到第三方 API，否则请勿启用在线参考书目检查。

## 所需输入（详细信息）

- `main.typ` 或 Typst 条目文件。
- 可选 `--section SECTION` 用于目标分析。
- 当请求目标引用时可选的参考书目路径。
- 当用户关心 IEEE、ACM、Springer 或类似期望时，可选期刊或会议上下文。

如果参数缺失，保留已推断的模块，只询问缺少的 Typst 入口文件、章节、参考书目路径或投稿场所上下文。

## 辅助脚本

- `scripts/deai_batch.py`: 批处理`deai`许多部分/文件的模块。
- `scripts/online_bib_verify.py`: 背后的在线后端`verify_bib.py --online`.
