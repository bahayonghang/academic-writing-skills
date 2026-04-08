# `typst-paper`

面向现有 `.typ` 项目的 Typst 论文助手，支持中英文论文。

## 适用场景

- Typst 编译或导出问题
- 格式与 venue 检查
- BibTeX 或 Hayagriva 文献验证
- 语法、长句、逻辑、表达优化
- 文献综述质量检查与重写蓝图、讨论深度、结论完整性
- 跨章节逻辑链闭合
- 翻译与双语润色
- 标题优化
- `algorithmic`、`algorithm-figure`、`lovelace` 的 IEEE-like 伪代码审查
- 去 AI 修改
- 实验章节审阅
- 摘要结构分析（五元素模型）
- 三线表合规检查与生成
- 跨 venue 格式适配

## 模块路由

| 模块 | 用途 | 脚本 |
| --- | --- | --- |
| `compile` | 构建、导出、字体问题 | `uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ` |
| `format` | 版式和风格检查 | `uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ` |
| `bibliography` | BibTeX 或 Hayagriva 验证 | `uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ` |
| `grammar` | 语法检查 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_grammar.py main.typ --section introduction` |
| `sentences` | 长句分析 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_sentences.py main.typ --section introduction` |
| `logic` | 连贯性、绪论漏斗链、文献综述质量、摘要/结论一致性、跨章节逻辑链 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `literature` | related work 综合分析、比较分析与研究空白推导 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_literature.py main.typ --section related` |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | 中英学术翻译 | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py input_zh.txt --domain deep-learning` |
| `title` | 标题检查或优化 | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `pseudocode` | `algorithmic` / `algorithm-figure` / `lovelace` 的 IEEE-like 检查 | `uv run python academic-writing-skills/typst-paper/scripts/check_pseudocode.py main.typ --venue ieee` |
| `deai` | 中英文 Typst 降低 AI 痕迹与低信息密度套话 | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | 实验章节审阅、讨论深度/分层、结论完整性 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |
| `abstract` | 五元素摘要结构诊断 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_abstract.py main.typ` |
| `tables` | 三线表合规检查与生成 | `uv run python academic-writing-skills/typst-paper/scripts/check_tables.py main.typ` |
| `caption` | 图表 caption 质量审查 | LLM 驱动（无独立脚本） |
| `adapt` | 跨 venue 格式适配 | LLM 驱动（参见 [适配工作流](./resources/references/JOURNAL_ADAPTATION_WORKFLOW)） |

## 最小输入

- 入口文件，如 `main.typ`
- 若只处理局部内容，可补充 section 名称
- bibliography 路径可选，支持 BibTeX 和 Hayagriva
- 如果是 `pseudocode`，请尽量说明是否按 IEEE-like 输出要求审查
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

```text
审查这个 algorithm-figure 的 caption、style-algorithm 和行号设置。
```

- 默认输出是 Typst 友好的、保留源码结构的审阅意见，而不是静默改写。
- 当前 eval 已补充伪代码相关请求，包括 algorithm-figure 检查和 lovelace wrapper 指引。
- 如果用户明确要改写文献综述、补比较分析或推导研究空白，优先走 `literature`。
