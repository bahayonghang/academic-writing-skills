# `latex-thesis-zh`

面向现有 `.tex` 学位论文项目的中文 LaTeX 论文助手。

## 适用场景

- 结构映射
- 国标相关格式检查
- 模板检测
- 论文编译
- 术语或命名一致性检查
- 标题优化
- 去 AI 修改
- 实验章节审阅

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
| `deai` | 降低 AI 痕迹 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py thesis.tex --section introduction` |
| `experiment` | 实验章节审阅 | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py thesis.tex --section experiments` |

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
