# 快速开始

## 1. 先选技能

| 你手里有什么 | 用哪个技能 |
| --- | --- |
| 英文 LaTeX 论文 | `latex-paper-en` |
| 中文 LaTeX 学位论文 | `latex-thesis-zh` |
| Typst 论文 | `typst-paper` |
| 想检索或提取引用的 `.bib` 文献库 | `bib-search-citation` |
| 想在投稿前做统一审查的论文 | `paper-audit` |

## 2. 先跑一条真实命令

仓库内示例统一遵循项目规则，使用 `uv run python ...`。

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
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex
```

### Typst 论文

```bash
uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ
```

### `.bib` 文献库检索

```bash
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "TimeMachine raw:true cite:both limit:1" | uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py
```

### 论文审查

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python academic-writing-skills/paper-audit/scripts/pre_submission_check.py paper.tex --json
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus methodology
```

## 3. 常见提示词

```text
用 latex-paper-en 编译 main.tex。
```

```text
先映射 thesis.tex 的结构，再检查国标问题。
```

```text
编译 main.typ，并检查摘要的语法和表达。
```

```text
在 references.bib 里找 2024 年后的 Cheng + Mamba 时序预测论文，并返回 LaTeX 和 Typst 引用。
```

```text
对 paper.pdf 做一次 gate 审查。
```

## 4. 推荐起步流程

### LaTeX 论文

1. 先编译。
2. 再做格式或文献检查。
3. 最后按章节做语法、长句或逻辑检查。

### 中文学位论文

1. 先做 `structure`。
2. 模板不明确时再做 `template`。
3. 然后编译、查国标和一致性。

### Typst 论文

1. 先编译。
2. 再做格式或文献检查。
3. 最后对当前编辑章节做语言质量检查。

### `.bib` 文献库检索

1. 先指明 `.bib` 文件。
2. 优先从紧凑 `--query` 开始。
3. 只有需要引用格式或原始 BibTeX 时，再加 `cite:...` 或 `raw:true`。
4. 想看紧凑摘要时，再把 JSON 结果管道给 `preview_bib_search.py`。

### 投稿前审查

1. 选模式：`quick-audit`、`deep-review`、`gate`、`polish`、`re-audit`。
2. 指明 `.tex`、`.typ` 或 `.pdf` 文件。
3. 只有真的需要 venue 约束时再加对应参数。
4. 想快速筛查用 `quick-audit`，想做审稿人风格深审用 `deep-review`。
5. `deep-review` 只看单一维度时，可加 `--focus ...`。
