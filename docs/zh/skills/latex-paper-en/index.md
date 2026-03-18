# `latex-paper-en`

面向现有 `.tex` 项目的英文 LaTeX 论文助手。

## 适用场景

- 编译失败
- 格式或 venue 检查
- 参考文献验证
- 语法与长句优化
- 逻辑与论证衔接检查
- 文献综述质量检查（主题组织、研究空白推导）
- 讨论深度与文献回溯分析
- 结论完整性验证
- 跨章节逻辑链闭合
- 学术表达润色
- 中译英学术翻译
- 标题、图表、去 AI、实验章节审阅
- `algorithm2e`、`algorithmicx`、`algpseudocodex` 的 IEEE-safe 伪代码审查

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
| `logic` | 连贯性、绪论漏斗链、文献综述质量、摘要/结论一致性、跨章节逻辑链 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods` |
| `expression` | 学术表达润色 | `uv run python academic-writing-skills/latex-paper-en/scripts/improve_expression.py main.tex --section related` |
| `translation` | 中译英学术翻译 | `uv run python academic-writing-skills/latex-paper-en/scripts/translate_academic.py input.txt --domain deep-learning` |
| `title` | 标题检查或生成 | `uv run python academic-writing-skills/latex-paper-en/scripts/optimize_title.py main.tex --check` |
| `figures` | 图表存在性、DPI、caption 检查 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_figures.py main.tex` |
| `pseudocode` | IEEE-safe 伪代码、浮动体、caption、label、注释和行号建议检查 | `uv run python academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py main.tex --venue ieee` |
| `deai` | 降低 AI 痕迹与低信息密度套话 | `uv run python academic-writing-skills/latex-paper-en/scripts/deai_check.py main.tex --section introduction` |
| `experiment` | 实验章节审阅、讨论深度/分层、结论完整性 | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_experiment.py main.tex --section experiments` |

## 最小输入

- 入口文件，如 `main.tex`
- 若只处理局部内容，可补充 section 名称
- 如果是文献问题，可补充 bibliography 路径
- 若关心投稿规范，可补充 IEEE、ACM、Springer、NeurIPS、ICML 等上下文
- 如果是 `pseudocode`，最好说明是否按 IEEE 规范审查，因为该模块会区分硬约束和建议默认值
- 如果是 `translation`，也可以只给一段待翻译文本或单独文本文件，而不必先扫描整个项目

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

```text
检查这个 IEEE 伪代码是否还在用 algorithm2e 浮动体，并判断 caption 是否安全。
```

- 默认输出是保留源码结构的审阅意见，通常采用 LaTeX 友好的 comment 形式，而不是直接静默改写。
- 当前 eval 已覆盖 IEEE 伪代码相关请求，包括浮动体迁移、caption/label 检查，以及“硬规则 vs 建议项”的区分。
