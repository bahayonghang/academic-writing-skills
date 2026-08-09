# `latex-thesis-zh`

面向现有 `.tex` 学位论文工程的中文 LaTeX 助手，覆盖源码级诊断、论文主线与章节结构、
学校模板约束和定稿检查，不静默改动引用、标签、数学环境或模板宏命令。

## 适用场景

- 诊断 XeLaTeX、LuaLaTeX、latexmk、模板、版式、公式和 GB/T 7714 问题。
- 映射章节结构，检查术语、缩略语、交叉引用、表格和标题架构。
- 审阅绪论漏斗、文献综合、方法章、过程章、实验、摘要、结论和跨章节闭合。
- 在保留学术主张与 LaTeX 语法的前提下降低 AI 写作痕迹。
- 送审前执行学校规范逐项终检和盲审隐匿检查。

## 不适用场景

- 英文会议或期刊论文；请用 `latex-paper-en`。
- Typst 工程；请用 `typst-paper`。
- 只有 PDF 的多维度审稿报告；请用 `paper-audit`。
- 纯文献发现、只有 DOCX 的工作，或从零代写学位论文。

## 模块路由

| 模块 | 适用场景 | 主命令 |
| --- | --- | --- |
| `compile` | 论文构建失败或工具链不明确 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py main.tex` |
| `format` | 需要检查版式、公式断行、草稿残留或占位表格行 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_format.py main.tex` |
| `structure` | 需要论文章节与小节地图 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py main.tex` |
| `consistency` | 跨章节术语、缩略语或命名漂移 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py main.tex --terms` |
| `template` | 论文 class 或学校模板不明确 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py main.tex` |
| `bibliography` | 需要检查 BibTeX 数据或 GB/T 7714 合规性；2026-07-01 起实施的新国标使用 `--standard gb7714-2025` | `uv run python academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gb7714` |
| `title` | 需要审阅论文、章或节标题 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py main.tex --check --headings` |
| `deai` | 中文可见正文存在 AI 写作痕迹 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py main.tex --section introduction` |
| `logic` | 绪论漏斗、章节承接、主线、方法模块接口或闭合不足 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py main.tex [--method-narrative --section <章名>]` |
| `literature` | 文献综述逐篇罗列，缺少综合比较或可答辩的研究空白 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py main.tex --section related` |
| `experiment` | 需要审阅实验表达、证据层次或逐方法章实验完整性 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py main.tex` |
| `references` | 交叉引用、图表题、标签或编号不一致 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_references.py main.tex` |
| `tables` | 需要检查三线表、booktabs 结构或生成表格 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_tables.py main.tex` |
| `abstract` | 需要诊断摘要结构、字数或中英一致性 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py main.tex` |
| `conclusion` | 结论缺少总结、创新、展望或数值一致性 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_conclusion.py main.tex` |
| `spec-check` | 定稿需要对照学校规范逐项检查 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_spec.py main.tex --template yanshan --degree doctor` |
| `blind-review` | 需要检测个人信息或生成隐匿后的送审副本 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/blind_review.py main.tex --check` |

## 最小输入

- 学位论文入口文件，如 `main.tex`；多文件工程可以使用 `\input` 和 `\include`。
- 执行 bibliography 检查时提供文献库路径。
- 局部检查可提供章节、小节、学校/模板上下文和学位类型。
- 在线核验文献前，明确允许将引文元数据发送到外部服务。

## 首条命令

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py main.tex
```

优先运行能回答问题的最小模块。多目标请求按[路由规则](./resources/references/modules/routing-rules.md)
规定的顺序执行。编译必须经过 `compile.py`，不要直接调用 TeX 工具。

## 输出产物

- 使用 `% MODULE (L##) [Severity] [Priority]: ...` 格式的源码定位诊断。
- 脚本失败时给出精确命令、退出码和关键 stderr。
- 结构地图、模板信号、文献检查结果和保留源码的改写提案。
- 分开陈述检查结果和建议改写；不虚构引用、数据、论断、基金或致谢。
- 盲审结果只写入 `*_blind` 副本，原始源码保持不变。

## 公开资源

### 模块参考

- [路由规则](./resources/references/modules/routing-rules.md)
- [编译](./resources/references/modules/compile.md)
- [格式](./resources/references/modules/format.md)
- [结构与逻辑](./resources/references/modules/logic.md)
- [一致性](./resources/references/modules/consistency.md)
- [模板检测](./resources/references/modules/template.md)
- [参考文献](./resources/references/modules/bibliography.md)
- [标题](./resources/references/modules/title.md)
- [去 AI 审阅](./resources/references/modules/deai.md)
- [文献综述](./resources/references/modules/literature.md)
- [实验审阅](./resources/references/modules/experiment.md)
- [交叉引用](./resources/references/modules/references.md)
- [表格](./resources/references/modules/tables.md)
- [摘要](./resources/references/modules/abstract.md)
- [结论](./resources/references/modules/conclusion.md)
- [规范终检](./resources/references/modules/spec-check.md)
- [盲审](./resources/references/modules/blind-review.md)

### 写作参考

- [写作哲学](./resources/references/writing/writing-philosophy-zh.md)
- [学位论文写作指南](./resources/references/writing/thesis-writing-guide.md)
- [绪论专章指南](./resources/references/writing/introduction-guide-zh.md)
- [过程分析章指南](./resources/references/writing/process-chapter-guide-zh.md)
- [方法章指南](./resources/references/writing/method-chapter-guide-zh.md)
- [方法模块描述与接口](./resources/references/writing/method-description-guide-zh.md)
- [结论章指南](./resources/references/writing/conclusion-guide-zh.md)
- [摘要结构](./resources/references/writing/abstract-structure.md)
- [结构指南](./resources/references/writing/structure-guide.md)
- [逻辑与连贯性](./resources/references/writing/logic-coherence.md)
- [中文学术风格](./resources/references/writing/academic-style-zh.md)
- [标题优化](./resources/references/writing/title-optimization.md)
- [英文摘要时态指南](./resources/references/writing/tense-guide-zh.md)
- [过度声称防护](./resources/references/writing/over-claim-guard.md)

### 格式、引用与去 AI 参考

- [GB/T 7714](./resources/references/citations/gb-standard.md)
- [编译策略](./resources/references/latex/compilation.md)
- [图表题指南](./resources/references/formatting/caption-guide.md)
- [公式指南](./resources/references/formatting/formula-guide.md)
- [表格指南](./resources/references/formatting/table-guide.md)
- [去 AI 指南](./resources/references/deai/guide.md)
- [禁用词](./resources/references/deai/forbidden-terms.md)
- [中文语气词](./resources/references/deai/tone-terms-zh.md)
- [语气阈值](./resources/references/deai/tone-thresholds.yaml)

### 模板

- [通用中文学位论文](./resources/templates/generic.md)
- [清华大学 thuthesis](./resources/templates/thuthesis.md)
- [北京大学 pkuthss](./resources/templates/pkuthss.md)
- [燕山大学 2024 版规范](./resources/templates/yanshan.md)

### 示例

- [编译与模板](./resources/examples/compile-and-template.md)
- [结构与一致性](./resources/examples/structure-and-consistency.md)
- [逻辑与实验](./resources/examples/logic-and-experiment.md)
- [文献综述改写](./resources/examples/literature-review-rewrite.md)
- [参考文献与去 AI](./resources/examples/bibliography-and-deai.md)

## 常见请求与交接

本技能负责源码级学位论文工作：模板检测、受控编译、章节诊断、写作审阅、规范终检和
盲审副本。英文论文交给 `latex-paper-en`，Typst 源码交给 `typst-paper`，本地文献库发现
交给 `bib-search-citation`，最终多维度审稿报告交给 `paper-audit`。
