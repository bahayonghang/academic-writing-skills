# `latex-paper-en`

面向现有 `.tex` 会议/期刊论文的英文 LaTeX 论文助手。它负责源码级编译、格式、文献、语言、逻辑、文献综述、伪代码、表格和实验章节诊断。

## 适用场景

- LaTeX 编译失败与构建诊断。
- IEEE、ACM、Springer、NeurIPS、ICML 等模板的格式检查。
- `.tex` 论文工程内的 bibliography 和 citation 验证。
- 语法、长句、表达、翻译、标题、摘要、图表和 caption 审阅。
- 逻辑、文献综述综合、研究空白推导、跨章节闭合与实验章节审阅。
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
