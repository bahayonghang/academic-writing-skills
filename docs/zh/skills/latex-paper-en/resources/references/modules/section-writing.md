# 模块：章节写作

**触发**：章节写作、重写引言、摘要草案、方法叙述、相关工作重写、实验叙述、结论完善、段落角色、主张证据自我审查

**目的**：计划或重写一篇现有的英文论文部分，同时保留 LaTeX 语法并将散文提案与源诊断分开。

这是一个由 LLM 驱动的工作流程。不要运行脚本，除非用户还请求诊断模块，例如`logic`, `literature`, `experiment`， 或者`abstract`.

## 何时使用

当用户要求时使用此模块：

- 起草、重写或审稿润色摘要、引言、相关工作、方法、实验、讨论或结论；
- 设计段落角色或紧凑的章节大纲；
- 将诊断结果转化为重写蓝图；
- 检查主要主张是否有明显证据支持。

保留现有的诊断模块以进行源检查：

- `abstract`：五要素摘要诊断和字数统计。
- `logic`：连贯性、漏斗、动机线索和横截面闭合检查。
- `literature`：相关工作枚举、比较和差距诊断。
- `experiment`：结果、讨论、基线、消融、显着性和结论检查。

## 渐进式加载

只读当前部分指南以及可选的流程/自我审查支持：

|目标|读|
| --- | --- |
|摘要| `references/writing/section-writing/abstract.md` |
|介绍| `references/writing/section-writing/introduction.md` |
|相关工作| `references/writing/section-writing/related-work.md` |
|方法| `references/writing/section-writing/method.md` |
|实验或讨论| `references/writing/section-writing/experiments.md` |
|结论| `references/writing/section-writing/conclusion.md` |
|段落流问题| `references/writing/section-writing/flow.md` |
|面向审稿人的声明检查| `references/writing/section-writing/self-review.md` |

仅当在这些文件中进行选择时才使用 `references/writing/section-writing/index.md`。

## 工作流程

1. 确定目标部分和当前用户意图：诊断、重写蓝图、段落级散文或自我审查。
2. 仅加载相关部分指南。添加`flow.md`当用户询问清晰度/连贯性时，以及`self-review.md`当声明或审稿人风险很重要时。
3. 在提出散文之前先建立一个紧凑的大纲。
4. 在重写之前分配段落角色：开头、挑战、先前工作的限制、方法、技术优势、证据、限制、暗示或结束。
5. 默认情况下逐字保留 LaTeX 锚点：`\cite{}`, `\ref{}`, `\label{}`、数学、自定义宏、表格/图形锚点和期刊或会议命令。
6. 生成主要声明的声明-证据图。如果证据缺失，请将其标记为缺失，而不是发明引文、指标、基线或结果。

## 产出合约

对于章节编写任务，返回：

1. **部分目标**：一句话命名目标读者的效果。
2. **紧凑大纲**：3-7 个项目符号或段落角色表。
3. **重写蓝图或散文提案**：
   - 当用户要求计划或证据薄弱时，请使用蓝图。
   - 仅当用户明确要求措辞时才使用修改后的散文。
4. **声明-证据图**：
   - `Claim: ... | Evidence: ... | Status: supported/needs evidence/unsupported`
5. **自我审查清单**：
   - 清晰度、段落流程、术语一致性、不受支持的主张、缺失的实验/证据以及 LaTeX 保存。

## 硬性界限

- 请勿伪造引文、指标、基线、删减、p 值、数据集或结论。
- 除非明确要求，否则请勿更改引文键、标签、参考文献、数学、宏或模板命令。
- 不要让缺乏支持的主张听起来比可见的证据更有说服力。
- 不要用散文的热情覆盖剧本的发现。将诊断和建议的散文分开。
