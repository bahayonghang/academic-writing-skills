# `latex-thesis-zh`

面向现有 `.tex` 学位论文项目的中文 LaTeX 论文助手。

## 适用场景

- 结构映射
- 国标相关格式检查
- 模板检测
- 论文编译
- 术语或命名一致性检查
- 逻辑与连贯性检查（文献综述质量、跨章节逻辑链闭合）
- 文献综述重写蓝图（主题综合、比较分析、研究空白推导）
- 讨论深度与结论完整性检查
- 标题优化
- 去 AI 修改（含填充连接词与排比句检测）
- 实验章节审阅
- 摘要结构分析（五元素模型）
- 三线表合规检查与生成（GB/T）

## 默认建议

对于多文件或整篇论文审阅，先跑 `structure`。

## 模块路由

| 模块 | 用途 | 脚本 |
| --- | --- | --- |
| `compile` | 论文构建问题 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex` |
| `format` | 论文格式或 GB/T 问题 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_format.py thesis.tex` |
| `structure` | 章节结构总览 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex` |
| `consistency` | 跨章节术语漂移 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py thesis.tex --terms` |
| `template` | 检测或验证模板 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex` |
| `bibliography` | GB/T 7714 文献检查 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gb7714` |
| `title` | 标题或章节标题优化 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py thesis.tex --check` |
| `deai` | 降低 AI 痕迹与低信息密度套话 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py thesis.tex --section introduction` |
| `logic` | 逻辑连贯性、绪论漏斗链、章节主线、文献综述质量、跨章节逻辑链 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py thesis.tex --section related` |
| `literature` | 文献综述综合分析、比较分析与研究空白推导 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py thesis.tex --section related` |
| `experiment` | 实验章节审阅、讨论深度/分层、结论完整性 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py thesis.tex --section experiments` |
| `abstract` | 五元素摘要结构诊断 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py thesis.tex` |
| `tables` | 三线表合规检查与生成（GB/T） | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_tables.py thesis.tex` |

## 推荐提示词

```text
先映射 thesis.tex 的结构，并指出缺失的必要部分。
```

```text
检测一下这个学位论文模板，并总结关键约束。
```

```text
检查 references.bib 的 GB/T 7714 问题。
```

```text
把这一节文献综述从作者年份罗列改成按主题对话式写法，但不要新增引用。
```

- 最小输入通常是学位论文入口文件，如 `thesis.tex`；只有涉及参考文献时才需要额外给 bibliography 路径。
- 默认输出是保留源码结构的 thesis 审阅意见，通常采用 `% Module (L##) [Severity] [Priority]: ...` 这类格式，而不是整段重写。
- 当前 eval 覆盖 3 类请求：template+compile 排障、structure+consistency 审阅，以及 bibliography+deai 检查。
- 当用户明确要处理文献综述重写、比较分析或 gap 推导时，优先走 `literature`。
