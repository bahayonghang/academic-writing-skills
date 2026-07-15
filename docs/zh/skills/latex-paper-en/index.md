# `latex-paper-en`

面向现有 `.tex` 会议/期刊论文的英文 LaTeX 论文助手。它负责源码级编译、格式、文献、语言、逻辑、文献综述、图像、caption、分节写作、伪代码、表格和实验章节诊断。

## 适用场景

- LaTeX 编译失败与构建诊断。
- IEEE、ACM、Springer、NeurIPS、ICML 等模板的格式检查。
- `.tex` 论文工程内的 bibliography 和 citation 验证。
- 语法、长句、表达、翻译、标题、摘要、图表和 caption 审阅。
- 逻辑、文献综述综合、研究空白推导、跨章节闭合与实验章节审阅。
- 面向 Abstract、Introduction、Related Work、Method、Experiments 和 Conclusion 的分节改写方案、段落角色和 claim-evidence map。
- `algorithm2e`、`algorithmicx`、`algpseudocodex` 的 IEEE-safe 伪代码审查。
- 保留 LaTeX 语法、citation、label 和 math 的去 AI 检查。

## 不适用场景

- 从零写论文。
- 中文学位论文模板工作。
- Typst 项目。
- 审稿式打分或投稿门禁；请用 `paper-audit`。
- 投稿信生成；请用 `cover-letter`。

## 模块路由

| 模块 | 适用场景 | 主命令 |
| --- | --- | --- |
| `compile` | 构建失败或需要重新编译 | `uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex` |
| `format` | venue 或 LaTeX 格式存疑 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex` |
| `bibliography` | citation 或 BibTeX 需要验证 | `uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex` |
| `grammar` | 语法审阅 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_grammar.py main.tex --section introduction` |
| `sentences` | 长句或密集句诊断 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_sentences.py main.tex --section introduction` |
| `logic` | 连贯性、绪论漏斗、摘要/结论一致性或闭合 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods` |
| `literature` | Related Work 综合、比较和 gap 推导 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_literature.py main.tex --section related` |
| `section-writing` | 分节大纲、段落角色、改写方案和 claim-evidence 自查 | LLM 驱动工作流 |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/latex-paper-en/scripts/improve_expression.py main.tex --section related` |
| `translation` | 中译英学术翻译 | `uv run python academic-writing-skills/latex-paper-en/scripts/translate_academic.py input.txt --domain deep-learning` |
| `title` | 标题检查或生成 | `uv run python academic-writing-skills/latex-paper-en/scripts/optimize_title.py main.tex --check` |
| `figures` | 图片存在性、扩展名、DPI 或 caption 审阅 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_figures.py main.tex` |
| `pseudocode` | 算法块、caption、label、注释和行号审查 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py main.tex --venue ieee` |
| `deai` | AI 痕迹和低信息密度套话检查 | `uv run python academic-writing-skills/latex-paper-en/scripts/deai_check.py main.tex --section introduction` |
| `experiment` | 实验写法、讨论深度和结论完整性 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_experiment.py main.tex --section experiments` |
| `abstract` | 五元素摘要诊断 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex` |
| `tables` | 表格结构、booktabs 和三线表检查 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex` |
| `caption` | 图表 caption 质量审查 | LLM 驱动模块 |
| `adapt` | 跨 venue 适配 | LLM 驱动工作流 |

## 最小输入

- 入口文件，如 `main.tex`。
- 局部检查可提供 section 名称。
- 文献问题提供 bibliography 路径。
- 格式、伪代码或适配任务提供 venue 上下文。

## 输出产物

- 脚本化诊断和面向问题的审阅意见。
- 默认保留 citation、label、math 和 LaTeX 结构的源码友好建议。
- 可在 `paper-audit` 或 `cover-letter` 前使用的模块级 findings。

## 公开资源

### 参考资料

- [期刊名称缩写](./resources/references/citations/journal-abbreviations.md)
- [引文风格指南](./resources/references/citations/styles.md)
- [引文验证指南](./resources/references/citations/verification.md)
- [受保护条款 - 请勿修改](./resources/references/deai/forbidden-terms.md)
- [De-AI英语学术论文写作指南](./resources/references/deai/guide.md)
- [AI Tone 术语（英文） — 参考](./resources/references/deai/tone-terms-en.md)
- [AI Tone Threshold Configuration (English papers)](./resources/references/deai/tone-thresholds.yaml)
- [声明-证据合同](./resources/references/evidence/claim-evidence-contract.md)
- [超额声明保护](./resources/references/evidence/over-claim-guard.md)
- [数字和单位格式指南](./resources/references/formatting/number-unit-guide.md)
- [三行表格指南](./resources/references/formatting/table-guide.md)
- [LaTeX 编译指南](./resources/references/latex/compilation.md)
- [模块：摘要](./resources/references/modules/abstract.md)
- [模块：适应](./resources/references/modules/adapt.md)
- [模块：参考书目](./resources/references/modules/bibliography.md)
- [图形和表格标题生成指南](./resources/references/modules/caption.md)
- [模块：编译](./resources/references/modules/compile.md)
- [模块：去AI编辑](./resources/references/modules/deai.md)
- [模块：实验回顾](./resources/references/modules/experiment.md)
- [模块：表达重组](./resources/references/modules/expression.md)
- [模块：格式检查](./resources/references/modules/format.md)
- [模块：语法分析](./resources/references/modules/grammar.md)
- [模块：文献综述综合](./resources/references/modules/literature.md)
- [模块：逻辑连贯性和方法论深度](./resources/references/modules/logic.md)
- [模块：伪代码审查](./resources/references/modules/pseudocode.md)
- [路由规则 — 完整详细信息](./resources/references/modules/routing-rules.md)
- [模块：章节写作](./resources/references/modules/section-writing.md)
- [模块：长句分析](./resources/references/modules/sentences.md)
- [模块：表格](./resources/references/modules/tables.md)
- [时态指南](./resources/references/modules/tense-guide.md)
- [模块：标题优化](./resources/references/modules/title.md)
- [模块：翻译（中文 -> 英文）](./resources/references/modules/translation.md)
- [工作流程和最佳实践](./resources/references/modules/workflow.md)
- [审稿人观点指南](./resources/references/review/reviewer-perspective.md)
- [法学硕士/人工智能援助披露政策 (2026-06)](./resources/references/venues/ai-disclosure.md)
- [期刊或会议特定要求](./resources/references/venues/catalog.md)
- [期刊改编工作流程](./resources/references/venues/journal-adaptation-workflow.md)
- [抽象结构指南](./resources/references/writing/abstract-structure.md)
- [最佳实践](./resources/references/writing/best-practices.md)
- [学术写作中常见的中式英语错误](./resources/references/writing/common-errors.md)
- [摘要部分写作](./resources/references/writing/section-writing/abstract.md)
- [结论部分写作](./resources/references/writing/section-writing/conclusion.md)
- [实验和讨论部分写作](./resources/references/writing/section-writing/experiments.md)
- [段落流程和反向大纲](./resources/references/writing/section-writing/flow.md)
- [章节写作参考索引](./resources/references/writing/section-writing/index.md)
- [引言部分写作](./resources/references/writing/section-writing/introduction.md)
- [方法部分写作](./resources/references/writing/section-writing/method.md)
- [相关工作部分写作](./resources/references/writing/section-writing/related-work.md)
- [面向审稿人的自我评审](./resources/references/writing/section-writing/self-review.md)
- [学术写作风格指南](./resources/references/writing/style-guide.md)
- [Academic Terminology Reference](./resources/references/writing/terminology.md)
- [Academic Translation Guide](./resources/references/writing/translation-guide.md)
- [学术论文写作哲学](./resources/references/writing/writing-philosophy.md)

### 模板

- [ACM 会议 (LaTeX)](./resources/templates/acm.md)
- [ICML（乳胶）](./resources/templates/icml.md)
- [IEEE 会议/期刊 (LaTeX)](./resources/templates/ieee.md)
- [NeurIPS（乳胶）](./resources/templates/neurips.md)
- [施普林格 (LNCS) (乳胶)](./resources/templates/springer-lncs.md)

### 示例

- [示例：编译和参考书目](./resources/examples/compile-and-bibliography.md)
- [示例：实验回顾](./resources/examples/experiment-review.md)
- [示例：数字和标题](./resources/examples/figures-and-title.md)
- [示例：语法和逻辑复习](./resources/examples/grammar-and-logic.md)
- [文献综述重写](./resources/examples/literature-review-rewrite.md)
- [示例：多模块序列](./resources/examples/multi-module-sequence.md)
- [示例：翻译与去AI](./resources/examples/translation-and-deai.md)

## 常见请求

```text
编译 main.tex，并解释第一个阻塞错误。
```

```text
检查 introduction 的语法和长句，但不要改 citations。
```

```text
审查这个 IEEE 伪代码的 algorithm2e 用法、caption 安全性和 label hygiene。
```

```text
分析 Related Work，并给出综合式重写方案。
```

```text
给 Introduction 一个面向 reviewer 的改写方案，包含段落角色和 claim-evidence map。
```
