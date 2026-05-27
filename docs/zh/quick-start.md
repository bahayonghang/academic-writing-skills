# 快速开始

## 1. 先选技能

| 你手里有什么 | 用哪个技能 |
| --- | --- |
| LaTeX 论文，并需要投稿信 | `cover-letter` |
| 想在投稿前做统一审查的论文 | `paper-audit` |
| 英文 LaTeX 论文 | `latex-paper-en` |
| 中文 LaTeX 学位论文 | `latex-thesis-zh` |
| Typst 论文 | `typst-paper` |
| 想检索或提取引用的 `.bib` 文献库 | `bib-search-citation` |

## 2. 先跑一条真实命令

仓库内示例统一遵循项目规则，使用 `uv run python ...`。

### 投稿信

```bash
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --manuscript main.tex --letter cover_letter.md --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode journal-fit --letter cover_letter.md --journal nature --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode presubmission --letter cover_letter.md --journal nature --json
```

### 论文审查

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
uv run python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py paper.tex
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus full --review-dir review_results/paper
```

### 英文 LaTeX 论文

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex
```

### 中文 LaTeX 学位论文

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex
```

### Typst 论文

```bash
uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ
```

### `.bib` 文献库检索

```bash
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "TimeMachine raw:true cite:both limit:1" | uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py
```

## 3. 常见提示词

```text
根据 main.tex 生成 Nature 投稿信，并检查每个强 claim 是否有论文证据支撑。
```

```text
对 paper.pdf 做 gate 审查，并把投稿 blocker 和 advisory issues 分开。
```

```text
用 latex-paper-en 编译 main.tex，然后检查摘要结构。
```

```text
先映射 thesis.tex 的结构，再检查国标文献问题。
```

```text
编译 main.typ，并按 IEEE-like 要求审查 algorithm-figure 伪代码。
```

```text
在 references.bib 里找 2024 年后的 Cheng + Mamba 时序预测论文，并返回 LaTeX 和 Typst 引用。
```

## 4. 推荐起步流程

### 投稿信

1. 只有论文时先跑 `generate`。
2. 已有草稿时先跑 `optimize`。
3. 相信任何 novelty 或 contribution claim 前，先跑 `align-check`。
4. 投稿前再跑 `journal-fit` 和 `presubmission`。

### 投稿前审查

1. 选 `quick-audit`、`deep-review`、`gate`、`polish` 或 `re-audit`。
2. 指明 `.tex`、`.typ` 或 `.pdf` 文件。
3. 快速筛查用 `quick-audit`，只看阻塞项用 `gate`。
4. 需要 review workspace、问题清单、revision trajectory 和 Markdown/HTML 报告时用 `deep-review`。

### LaTeX 论文

1. 先编译。
2. 再做格式或文献检查。
3. 最后按章节做语法、长句、逻辑、文献综述、实验或表格检查。

### 中文学位论文

1. 先跑 `structure`。
2. 模板不明确时再跑 `template`。
3. 然后编译、查国标、一致性、逻辑或表格。

### Typst 论文

1. 先编译或导出。
2. 再做格式或文献检查。
3. 最后对当前编辑章节做语言、逻辑、文献综述、伪代码或表格检查。

### `.bib` 文献库检索

1. 先指明 `.bib` 文件。
2. 优先从紧凑 `--query` 开始。
3. 只有需要引用格式或原始 BibTeX 时，再加 `cite:...` 或 `raw:true`。
4. 想看紧凑摘要时，再把 JSON 结果管道给 `preview_bib_search.py`。
