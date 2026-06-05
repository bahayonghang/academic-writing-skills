# `latex-thesis-zh`

面向现有 `.tex` 学位论文项目的中文 LaTeX 助手。它聚焦学位论文结构、模板、GB/T 7714、中文学术表达、逻辑、文献综述和章节一致性。

## 适用场景

- XeLaTeX、LuaLaTeX、latexmk 和常见学位论文模板的编译诊断。
- 章节/小节结构映射和模板检测。
- GB/T 7714 文献与学位论文格式检查。
- 跨章节术语、缩略语和命名一致性检查。
- 逻辑连贯、文献综述质量、研究空白推导、标题后导语、章节写作主线和跨章节闭合检查。
- 中文摘要、标题、实验、去 AI 和表格审阅。

## 不适用场景

- 英文会议或期刊论文；请用 `latex-paper-en`。
- Typst 项目；请用 `typst-paper`。
- PDF-only 审稿式审查；请用 `paper-audit`。
- 投稿信或 rebuttal。

## 模块路由

| 模块 | 适用场景 | 主命令 |
| --- | --- | --- |
| `structure` | 需要论文章节/小节地图 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex` |
| `template` | 模板或 class 不明确 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex` |
| `compile` | 学位论文构建失败 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex` |
| `format` | 论文版式或国标格式问题 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_format.py thesis.tex` |
| `consistency` | 术语或命名漂移 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py thesis.tex --terms` |
| `bibliography` | GB/T 7714 文献检查 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gb7714` |
| `title` | 论文或章节标题优化 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py thesis.tex --check` |
| `deai` | 中文 AI 痕迹和低信息套话检查 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py thesis.tex --section introduction` |
| `logic` | 章节主线、绪论漏斗、文献综述质量或闭合 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py thesis.tex --section related` |
| `literature` | 文献综述综合和 gap 推导 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py thesis.tex --section related` |
| `experiment` | 实验章节和结论完整性 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py thesis.tex --section experiments` |
| `abstract` | 中文摘要结构诊断 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py thesis.tex --lang zh` |
| `tables` | 三线表与 GB/T 表格检查 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_tables.py thesis.tex` |

## 最小输入

- 学位论文入口文件，如 `thesis.tex`。
- 检查国标文献时提供 bibliography 路径。
- 已知学校或模板时提供上下文。
- 局部审阅时提供章节或 section 名称。

## 输出产物

- 面向学位论文的诊断和审阅意见。
- 结构地图、模板信号、一致性 findings 和保留源码的建议。
- 不静默改动 citation、label 或 math 的中文学术写作反馈。

## 常见请求

```text
先映射 thesis.tex 的结构，并指出缺失的必要部分。
```

```text
先检测模板并总结约束，再编译。
```

```text
检查 references.bib 的 GB/T 7714 问题。
```

```text
把这一节文献综述改成主题综合式方案，但不要新增引用。
```

```text
把绪论改成背景、技术瓶颈、科学问题和贡献闭合逐步收束的写作方案。
```
