# `typst-paper`

面向现有 `.typ` 项目的 Typst 论文助手，支持中英文论文。

## 适用场景

- Typst 编译或导出问题
- 格式与 venue 检查
- BibTeX 或 Hayagriva 文献验证
- 语法、长句、逻辑、表达优化
- 文献综述质量检查、讨论深度、结论完整性
- 跨章节逻辑链闭合
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
| `logic` | 连贯性、文献综述质量、跨章节逻辑链 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | 中英学术翻译 | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py input_zh.txt --domain deep-learning` |
| `title` | 标题检查或优化 | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `deai` | 降低 AI 痕迹 | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | 实验章节审阅、讨论深度、结论完整性 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |

## 最小输入

- 入口文件，如 `main.typ`
- 若只处理局部内容，可补充 section 名称
- bibliography 路径可选，支持 BibTeX 和 Hayagriva
- 如果是 `translation`，可直接给局部段落，但会默认保留 Typst labels、引用和公式

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

- 默认输出是 Typst 友好的、保留源码结构的审阅意见，而不是静默改写。
- 当前 eval 覆盖 3 类请求：compile+format、BibTeX/Hayagriva bibliography 路由检查，以及在保留 Typst labels 前提下的 expression+translation。
