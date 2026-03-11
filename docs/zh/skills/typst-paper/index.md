# `typst-paper`

面向现有 `.typ` 项目的 Typst 论文助手，支持中英文论文。

## 适用场景

- Typst 编译或导出问题
- 格式与 venue 检查
- BibTeX 或 Hayagriva 文献验证
- 语法、长句、逻辑、表达优化
- 翻译与双语润色
- 标题优化
- 去 AI 修改
- 实验章节审阅

## 模块路由

| 模块 | 用途 | 脚本 |
| --- | --- | --- |
| `compile` | 构建、导出、字体问题 | `uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ` |
| `format` | 版式和风格检查 | `uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ` |
| `bibliography` | BibTeX 或 Hayagriva 验证 | `uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ` |
| `grammar` | 语法检查 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_grammar.py main.typ --section introduction` |
| `sentences` | 长句分析 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_sentences.py main.typ --section introduction` |
| `logic` | 连贯性检查 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | 中英学术翻译 | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py main.typ --section abstract` |
| `title` | 标题检查或优化 | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `deai` | 降低 AI 痕迹 | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | 实验章节审阅 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |

## 推荐提示词

```text
编译 main.typ，并解释第一个报错。
```

```text
检查摘要的语法和学术表达。
```

```text
核对 references.bib 和 main.typ 的引用关系。
```
