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
- `pseudocode`
- `deai`
- `experiment`
- `abstract`
- `tables`
- `caption`
- `adapt`

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
- `logic`
- `experiment`
- `abstract`
- `tables`

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
- `pseudocode`
- `deai`
- `experiment`
- `abstract`
- `tables`
- `caption`
- `adapt`

### `paper-audit`

模式：
- `quick-audit`
- `deep-review`
- `gate`
- `polish`
- `re-audit`

推荐选择：

- 想快速做脚本化筛查时用 `quick-audit`
- 想拿到审稿人风格问题清单和路线图时用 `deep-review`
- `deep-review` 默认走委员会预审（`Editor -> Theory -> Literature -> Methodology -> Logic`）
- 只看单一维度时，用 `--focus editor|theory|literature|methodology|logic`
- 只看 blocker 时用 `gate`
- 已有旧报告、想验证修订效果时用 `re-audit`

### `industrial-ai-research`

交付模式：
- `research-brief`
- `literature-map`
- `venue-ranked survey`
- `research-gap memo`
- `survey-draft`

这个技能会先做 intake，再开始综合。

## 常见命令

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex
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

## 输出预期

- 写作类技能通常返回面向问题的建议和脚本化诊断。
- `paper-audit` 返回 severity 分级报告、结构化问题清单、修订路线图，以及可选 score summary。
- 调研类输出应明确区分已验证证据与推断。
