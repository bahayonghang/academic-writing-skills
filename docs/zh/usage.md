# 使用指南

## 跨技能共通约定

### 提供最小必要输入

- 入口文件路径，例如 `main.tex`、`thesis.tex`、`main.typ`、`paper.pdf`、`references.bib` 或 `cover_letter.md`
- 可选范围，例如章节、section、全文、venue、journal 或审查 focus
- 如果已经知道目标模块或模式，直接说明

### 把不同意图拆开

- 想要构建结果时用 compile
- 想要诊断时用 check
- 想要改写建议时用 rewrite / optimize 类模块
- 想要审稿报告和投稿判断时用 audit
- 想验证投稿信 claim 是否有论文证据时用 align-check

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

| 技能 | 输入 | 主用途 | 不要用于 |
| --- | --- | --- | --- |
| `cover-letter` | `.tex` + 可选 `.md`/`.tex` 投稿信 | 投稿信生成、优化、证据对齐、期刊适配 | 修改论文源码或写 rebuttal |
| `paper-audit` | `.tex`、`.typ`、`.pdf` | 投稿前检查、深审、门禁、复审 | 一上来做逐句源码润色 |
| `latex-paper-en` | `.tex` | 英文论文编译与定向审阅 | 中文学位论文或 Typst 项目 |
| `latex-thesis-zh` | `.tex` | 中文学位论文结构、国标、编译与定向审阅 | 英文会议/期刊论文 |
| `typst-paper` | `.typ` | Typst 论文编译与定向审阅 | LaTeX 项目 |
| `bib-search-citation` | `.bib` | 文献库检索、预览与引用提取 | 证明论文 claim 已被文献支撑 |

## 模块与模式总览

### `cover-letter`

模式：

- `generate`：从 LaTeX 论文生成投稿信草稿。
- `optimize`：审阅和优化已有投稿信，不覆盖原文件。
- `align-check`：检查投稿信 claim 是否被论文证据支撑。
- `journal-fit`：评估 scope fit、novelty framing、evidence density 和 format compliance。
- `presubmission`：检查声明、长度、套话、段落形态和 AI-tone 词汇。

默认建议：已有草稿时先 `align-check` 再 `journal-fit`；没有草稿时先 `generate`。

### `paper-audit`

模式：

- `quick-audit`
- `deep-review`
- `gate`
- `polish`
- `re-audit`

推荐选择：

- 想快速做脚本化筛查时用 `quick-audit`；
- 只看投稿 blocker 时用 `gate`；
- 需要审稿人式问题清单、review workspace、claim map、revision suggestions、revision trajectory 和 Markdown/HTML 报告时用 `deep-review`；
- 只看单一维度时，用 `--focus editor|theory|literature|methodology|logic`；
- 已有旧报告、想验证修订效果时用 `re-audit`。

### `latex-paper-en`

模块：`compile`、`format`、`bibliography`、`grammar`、`sentences`、`logic`、`literature`、`expression`、`translation`、`title`、`figures`、`pseudocode`、`deai`、`experiment`、`abstract`、`tables`、`caption`、`adapt`。

### `latex-thesis-zh`

模块：`compile`、`format`、`structure`、`consistency`、`template`、`bibliography`、`title`、`deai`、`logic`、`literature`、`experiment`、`abstract`、`tables`。

默认建议：做整篇检查时先跑 `structure`。

### `typst-paper`

模块：`compile`、`format`、`bibliography`、`grammar`、`sentences`、`logic`、`literature`、`expression`、`translation`、`title`、`pseudocode`、`deai`、`experiment`、`abstract`、`tables`、`caption`、`adapt`。

### `bib-search-citation`

入口形态：

- `--query`
- `--spec-json`
- `--spec-file`
- `preview_bib_search.py`

默认建议：先用紧凑 `--query`，只有真的需要引用格式、原始 BibTeX 或裁剪字段时，再追加 `cite:...`、`raw:true` 或 `--return-fields`。

## 常见命令

```bash
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --manuscript main.tex --letter cover_letter.md --json
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate
uv run python academic-writing-skills/paper-audit/scripts/render_html_report.py review_results/paper --lang zh
uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"
```

## 如何选流程

### 你需要投稿信

用 `cover-letter`，不要用泛用润色工具。关键边界是论文证据：`align-check` 会在投稿前标出不被论文支撑的 novelty、contribution 和数字 claim。

### 你快投稿了

在编译和文献都稳定后，再使用 `paper-audit`。投稿前机械检查由 `PRESUBMISSION` 层接入 audit 模式；PDF 输入只运行文本类检查。

### 你在修编译失败

根据源码格式，用 `latex-paper-en`、`latex-thesis-zh` 或 `typst-paper` 的 compile 模块。

### 你只想润某一节

优先用 `grammar`、`sentences`、`logic`、`literature`、`expression`、`deai`、`experiment` 这类局部模块，不必全篇跑一遍。

### 你要检索 `.bib` 文献库或直接返回引用片段

用 `bib-search-citation`，不要先用写作技能。`.bib` 命中只是文献来源线索，不等于已经证明论文中的具体论断。

## 输出预期

- `cover-letter` 返回草稿框架或按模式分类的 findings，并区分 claim-evidence、journal-fit 和投稿前机械问题。
- `paper-audit` 返回 severity 分级报告、`PRESUBMISSION` 发现、结构化问题清单、claim map、revision suggestions、revision trajectory、Markdown/HTML 报告和可选 score summary。
- 写作类技能通常返回保留 citation、label、math 和源码结构的脚本化诊断与问题建议。
- `bib-search-citation` 返回结构化检索结果、可选原始 BibTeX，以及可直接使用的引用片段。
