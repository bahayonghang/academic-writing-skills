# 快速开始

## 1. 选择技能

| 任务 | 技能 |
| --- | --- |
| 生成或核查投稿信 | `cover-letter` |
| 批评论文或给出投稿判断 | `paper-audit` |
| 处理英文 LaTeX 论文 | `latex-paper-en` |
| 处理中文 LaTeX 学位论文 | `latex-thesis-zh` |
| 处理 Typst 论文 | `typst-paper` |
| 检索本地 `.bib` 文献库 | `bib-search-citation` |

## 2. 运行一条真实命令

### 投稿信

```bash
uv run python -B academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
uv run python -B academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --letter cover_letter.md --manuscript main.tex --json
```

### 论文审查

```bash
uv run python -B academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python -B academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
```

### 英文 LaTeX 论文

```bash
uv run python -B academic-writing-skills/latex-paper-en/scripts/compile.py main.tex
uv run python -B academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods
```

### 中文 LaTeX 学位论文

```bash
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/map_structure.py main.tex
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_conclusion.py main.tex
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/blind_review.py main.tex --check
```

### Typst 论文

```bash
uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/check_references.py main.typ
```

### 文献库检索

```bash
uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba forecasting author:Cheng year>=2024 has:code cite:both limit:5"
```

## 3. 按技能路由继续

运行第一条命令后，打开对应的[技能概览](/zh/skills/)。选择与请求匹配的最小模块
或模式，并且只加载该步骤路由到的资源。

当任务职责发生变化时，例如从源码修复转为审稿式审查，或从论文证据转为投稿信对齐，
使用[使用指南](/zh/usage)重新路由。
