# 使用指南

## 跨技能共通约定

### 提供最小必要输入

- 入口文件路径，例如 `main.tex`、`thesis.tex`、`main.typ`、`paper.pdf`
- 可选范围，例如章节、section、全文
- 如果你已经知道目标模块或模式，直接说明

### 把不同意图拆开

- 想要构建结果时用 compile
- 想要诊断时用 check
- 想要改写建议时用 rewrite 类模块
- 想要结构化报告时用 audit

### 仓库命令风格

本仓库中的 Python 脚本统一使用：

```bash
uv run python path/to/script.py ...
```

测试统一使用：

```bash
uv run python -m pytest tests/
```

## 技能矩阵

| 技能 | 输入 | 主用途 |
| --- | --- | --- |
| `latex-paper-en` | `.tex` | 英文论文编译与审阅 |
| `latex-thesis-zh` | `.tex` | 中文学位论文编译与审阅 |
| `typst-paper` | `.typ` | Typst 论文编译与审阅 |
| `paper-audit` | `.tex`、`.typ`、`.pdf` | 投稿前检查与结构化审查 |
| `industrial-ai-research` | topic | 文献调研与综合 |

## 模块总览

### `latex-paper-en`

模块：
- `compile`
- `format`
- `bibliography`
- `grammar`
- `sentences`
- `logic`
- `expression`
- `translation`
- `title`
- `figures`
- `deai`
- `experiment`

### `latex-thesis-zh`

模块：
- `compile`
- `format`
- `structure`
- `consistency`
- `template`
- `bibliography`
- `title`
- `deai`
- `experiment`

默认建议：做整篇检查时先跑 `structure`。

### `typst-paper`

模块：
- `compile`
- `format`
- `bibliography`
- `grammar`
- `sentences`
- `logic`
- `expression`
- `translation`
- `title`
- `deai`
- `experiment`

### `paper-audit`

模式：
- `self-check`
- `review`
- `gate`
- `polish`
- `re-audit`

### `industrial-ai-research`

交付模式：
- `research-brief`
- `literature-map`
- `venue-ranked survey`
- `research-gap memo`

这个技能会先做 intake，再开始综合。

## 常见命令

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate
```

## 如何选流程

### 你在修编译失败

用对应写作技能的 `compile` 模块。

### 你只想润某一节

优先用 `grammar`、`sentences`、`logic`、`expression`、`deai`、`experiment` 这类局部模块，不必全篇跑一遍。

### 你快投稿了

在编译和文献都稳定后，再使用 `paper-audit`。

### 你还没开始写，只是在做调研

用 `industrial-ai-research`，不要先用写作技能。
