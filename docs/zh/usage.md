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
| `bib-search-citation` | `.bib` | 文献库检索、预览与引用提取 |
| `paper-audit` | `.tex`、`.typ`、`.pdf` | 投稿前检查与结构化审查 |

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

### `bib-search-citation`

入口形态：
- `--query`
- `--spec-json`
- `--spec-file`
- `preview_bib_search.py`

默认建议：先用紧凑 `--query`，只有真的需要引用格式、原始 BibTeX 或裁剪字段时，
再追加 `cite:...`、`raw:true` 或 `--return-fields`。

### `paper-audit`

模式：
- `quick-audit`
- `deep-review`
- `gate`
- `polish`
- `re-audit`

推荐选择：

- 想快速做脚本化筛查时用 `quick-audit`
- 投稿前最后几天的机械检查也用 `quick-audit`
- 想拿到审稿人风格问题清单和路线图时用 `deep-review`
- `deep-review` 默认走委员会预审（`Editor -> Theory -> Literature -> Methodology -> Logic`）
- 只看单一维度时，用 `--focus editor|theory|literature|methodology|logic`
- 只看 blocker 时用 `gate`
- 已有旧报告、想验证修订效果时用 `re-audit`

## 常见命令

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate
uv run python academic-writing-skills/paper-audit/scripts/pre_submission_check.py paper.tex --json
```

## 如何选流程

### 你在修编译失败

用对应写作技能的 `compile` 模块。

### 你只想润某一节

优先用 `grammar`、`sentences`、`logic`、`expression`、`deai`、`experiment` 这类局部模块，不必全篇跑一遍。

### 你快投稿了

在编译和文献都稳定后，再使用 `paper-audit`。投稿前机械检查由
`PRESUBMISSION` 层接入 `quick-audit` 和 `gate`；PDF 输入只运行文本类检查。

### 你要检索 `.bib` 文献库或直接返回引用片段

用 `bib-search-citation`，不要先用写作技能。它处理的是文献库文件本身，
不是论文源文件树。

## 输出预期

- 写作类技能通常返回面向问题的建议和脚本化诊断。
- `bib-search-citation` 返回结构化检索结果、可选原始 BibTeX，以及可直接使用的引用片段。
- `paper-audit` 返回 severity 分级报告、`PRESUBMISSION` 机械发现、结构化问题清单、修订路线图，以及可选 score summary。
