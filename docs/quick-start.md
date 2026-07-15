# Quick Start

## 1. Choose The Skill

| Task | Skill |
| --- | --- |
| Generate or verify a submission letter | `cover-letter` |
| Critique a paper or make a readiness decision | `paper-audit` |
| Work on an English LaTeX paper | `latex-paper-en` |
| Work on a Chinese LaTeX thesis | `latex-thesis-zh` |
| Work on a Typst paper | `typst-paper` |
| Search a local `.bib` library | `bib-search-citation` |

## 2. Run One Real Command

### Submission cover letter

```bash
uv run python -B academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
uv run python -B academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --letter cover_letter.md --manuscript main.tex --json
```

### Paper audit

```bash
uv run python -B academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python -B academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
```

### English LaTeX paper

```bash
uv run python -B academic-writing-skills/latex-paper-en/scripts/compile.py main.tex
uv run python -B academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods
```

### Chinese LaTeX thesis

```bash
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/map_structure.py main.tex
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_conclusion.py main.tex
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/blind_review.py main.tex --check
```

### Typst paper

```bash
uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/check_references.py main.typ
```

### Bibliography search

```bash
uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba forecasting author:Cheng year>=2024 has:code cite:both limit:5"
```

## 3. Follow The Skill Router

After the first command, open the matching [skill overview](/skills/). Select the smallest
module or mode that matches the request and load only its routed resource.

Use [the usage guide](/usage) when the task changes responsibility, for example from source
repair to reviewer-style audit or from manuscript evidence to submission-letter alignment.
