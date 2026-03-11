# `latex-paper-en`

面向现有 `.tex` 项目的英文 LaTeX 论文助手。

## 适用场景

- 编译失败
- 格式或 venue 检查
- 参考文献验证
- 语法与长句优化
- 逻辑与论证衔接检查
- 学术表达润色
- 中译英学术翻译
- 标题、图表、去 AI、实验章节审阅

## 不适用场景

- 从零写论文
- 中文学位论文模板工作
- Typst 项目
- 纯调研、没有论文工程

## 模块路由

| 模块 | 用途 | 脚本 |
| --- | --- | --- |
| `compile` | 构建或定位 `main.tex` 错误 | `uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex` |
| `format` | LaTeX 或 venue 格式问题 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex` |
| `bibliography` | BibTeX 验证与缺失引用 | `uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex` |
| `grammar` | 语法检查 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_grammar.py main.tex --section introduction` |
| `sentences` | 长句或密集句分析 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_sentences.py main.tex --section introduction` |
| `logic` | 连贯性与方法论流畅度 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods` |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/latex-paper-en/scripts/improve_expression.py main.tex --section related` |
| `translation` | 中译英学术翻译 | `uv run python academic-writing-skills/latex-paper-en/scripts/translate_academic.py input.txt --domain deep-learning` |
| `title` | 标题检查或生成 | `uv run python academic-writing-skills/latex-paper-en/scripts/optimize_title.py main.tex --check` |
| `figures` | 图表存在性、DPI、caption 检查 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_figures.py main.tex` |
| `deai` | 降低 AI 痕迹 | `uv run python academic-writing-skills/latex-paper-en/scripts/deai_check.py main.tex --section introduction` |
| `experiment` | 实验章节审阅 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_experiment.py main.tex --section experiments` |

## 最小输入

- 入口文件，如 `main.tex`
- 若只处理局部内容，可补充 section 名称
- 如果是文献问题，可补充 bibliography 路径
- 若关心投稿规范，可补充 IEEE、ACM、Springer、NeurIPS、ICML 等上下文

## 推荐提示词

```text
用 latex-paper-en 编译 main.tex。
```

```text
检查 introduction 的语法和长句，但不要改 citations。
```

```text
投稿前帮我检查 figures 和 bibliography。
```
