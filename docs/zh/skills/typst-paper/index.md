# `typst-paper`

面向现有 `.typ` 中英文论文的 Typst 学术论文助手。它在保留 Typst 语法、label、文献格式和伪代码约定的前提下，覆盖论文写作常见检查。

## 适用场景

- Typst 编译、导出、字体和 watch 问题。
- venue 格式和版式检查。
- BibTeX 或 Hayagriva 文献验证。
- 语法、长句、表达、翻译、标题、摘要、表格和去 AI 审阅。
- 逻辑、文献综述综合、研究空白推导、跨章节闭合和实验章节审阅。
- `algorithmic`、`algorithm-figure`、`lovelace` 的 IEEE-like 伪代码审查。

## 不适用场景

- LaTeX 项目；请用 `latex-paper-en` 或 `latex-thesis-zh`。
- 没有 Typst 源码的 DOCX/PDF-only 编辑。
- 审稿式打分或投稿门禁；请用 `paper-audit`。
- 投稿信任务。

## 模块路由

| 模块 | 适用场景 | 主命令 |
| --- | --- | --- |
| `compile` | 构建、导出或字体问题 | `uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ` |
| `format` | 版式或 venue 风格检查 | `uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ` |
| `bibliography` | BibTeX 或 Hayagriva 验证 | `uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ` |
| `grammar` | 语法检查 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_grammar.py main.typ --section introduction` |
| `sentences` | 长句或密集句审阅 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_sentences.py main.typ --section introduction` |
| `logic` | 连贯性、绪论漏斗、摘要/结论一致性或闭合 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `literature` | Related Work 综合和 gap 推导 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_literature.py main.typ --section related` |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | 中英学术翻译 | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py input_zh.txt --domain deep-learning` |
| `title` | 标题检查或优化 | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `pseudocode` | `algorithmic`、`algorithm-figure` 或 `lovelace` 审查，包含 caption 和 wrapper 检查 | `uv run python academic-writing-skills/typst-paper/scripts/check_pseudocode.py main.typ --venue ieee` |
| `deai` | 中英文 AI 痕迹检查 | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | 实验写法和讨论分层 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |
| `abstract` | 五元素摘要诊断 | `uv run python academic-writing-skills/typst-paper/scripts/analyze_abstract.py main.typ` |
| `tables` | 表格结构和三线表检查 | `uv run python academic-writing-skills/typst-paper/scripts/check_tables.py main.typ` |
| `adapt` | 跨 venue 适配 | LLM 驱动工作流 |

## 最小输入

- 入口文件，如 `main.typ`。
- 局部分析可提供 section 名称。
- 文献路径可选，支持 BibTeX 和 Hayagriva。
- 伪代码和格式任务可提供 venue 或 IEEE-like 上下文。

## 输出产物

- Typst 友好的诊断和审阅意见。
- 默认保留 `@cite`、label、math 和 Typst 结构的源码友好建议。
- 可进入后续 audit 或投稿流程的模块级 findings。

## 公开资源

### 参考资料

- [抽象结构指南](./resources/references/ABSTRACT_STRUCTURE.md)
- [AI Tone Terms (Bilingual, Typst) — Reference](./resources/references/AI_TONE_TERMS.md)
- [AI Tone Threshold Configuration (Typst, bilingual)](./resources/references/AI_TONE_THRESHOLDS.yaml)
- [最佳实践](./resources/references/BEST_PRACTICES.md)
- [引文风格指南](./resources/references/CITATION_STYLES.md)
- [引文验证指南](./resources/references/CITATION_VERIFICATION.md)
- [学术写作中常见的中式英语错误](./resources/references/COMMON_ERRORS.md)
- [Typst学术论文去AI写作指南](./resources/references/DEAI_GUIDE.md)
- [期刊名称缩写](./resources/references/JOURNAL_ABBREVIATIONS.md)
- [期刊改编工作流程](./resources/references/JOURNAL_ADAPTATION_WORKFLOW.md)
- [模块：摘要](./resources/references/modules/ABSTRACT.md)
- [模块：适应](./resources/references/modules/ADAPT.md)
- [模块：参考书目](./resources/references/modules/BIBLIOGRAPHY.md)
- [图形和表格标题生成指南 (Typst)](./resources/references/modules/CAPTION.md)
- [模块：编译](./resources/references/modules/COMPILE.md)
- [模块：去AI化编辑](./resources/references/modules/DEAI.md)
- [角色](./resources/references/modules/EXPERIMENT.md)
- [模块：学术表达](./resources/references/modules/EXPRESSION.md)
- [模块：格式检查](./resources/references/modules/FORMAT.md)
- [模块：语法分析（英文）](./resources/references/modules/GRAMMAR.md)
- [模块：文献综述综合](./resources/references/modules/LITERATURE.md)
- [模块：逻辑衔接与方法论深度](./resources/references/modules/LOGIC.md)
- [模块：伪代码审查](./resources/references/modules/PSEUDOCODE.md)
- [模块：参考文献](./resources/references/modules/REFERENCES.md)
- [模块：长难句分析](./resources/references/modules/SENTENCES.md)
- [模块：表格](./resources/references/modules/TABLES.md)
- [模块：标题优化](./resources/references/modules/TITLE.md)
- [模块：翻译（中译英）](./resources/references/modules/TRANSLATION.md)
- [工作流程和最佳实践](./resources/references/modules/WORKFLOW.md)
- [数字和单位格式指南](./resources/references/NUMBER_UNIT_GUIDE.md)
- [超额声明保护](./resources/references/OVER_CLAIM_GUARD.md)
- [审稿人观点指南](./resources/references/REVIEWER_PERSPECTIVE.md)
- [路线、工作流程和安全注意事项（打字纸）](./resources/references/skill-routing-notes.md)
- [学术写作风格指南（Typst）](./resources/references/STYLE_GUIDE.md)
- [三行表格指南（打字员）](./resources/references/TABLE_GUIDE.md)
- [Typst 学术模板示例](./resources/references/TEMPLATES.md)
- [时态指南](./resources/references/TENSE_GUIDE.md)
- [Academic Terminology Reference](./resources/references/TERMINOLOGY.md)
- [Academic Translation Guide](./resources/references/TRANSLATION_GUIDE.md)
- [学术写作的 Typst 语法参考](./resources/references/TYPST_SYNTAX.md)
- [Typst 试卷的期刊或会议特定要求](./resources/references/VENUES.md)
- [学术论文写作哲学](./resources/references/WRITING_PHILOSOPHY.md)

### 模板

- [ACM 会议和期刊 (Typst)](./resources/templates/acm.md)
- [IEEE 会议和期刊 (Typst)](./resources/templates/ieee.md)
- [NeurIPS / ICML / ICLR (Typst)](./resources/templates/neurips.md)

### 示例

- [示例：参考书目和伪代码](./resources/examples/bibliography-and-pseudocode.md)
- [示例：参考书目和标题](./resources/examples/bibliography-and-title.md)
- [示例：编译和格式化](./resources/examples/compile-and-format.md)
- [示例：表达和翻译](./resources/examples/expression-and-translation.md)
- [文献综述重写](./resources/examples/literature-review-rewrite.md)

## 常见请求

```text
编译 main.typ，并解释第一个报错。
```

```text
核对 references.bib 和 main.typ 的引用关系。
```

```text
审查这个 algorithm-figure 的 caption 和行号设置。
```

```text
把 Related Work 从 citation list 改成综合式重写方案。
```
