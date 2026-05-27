# Quick Start

## 1. Pick the Skill

| If you have... | Use |
| --- | --- |
| A LaTeX manuscript and need a submission cover letter | `cover-letter` |
| A paper you want to audit before submission | `paper-audit` |
| An English LaTeX paper | `latex-paper-en` |
| A Chinese LaTeX thesis | `latex-thesis-zh` |
| A Typst paper | `typst-paper` |
| A `.bib` library you want to search or cite from | `bib-search-citation` |

## 2. Try One Real Command

All repository-local Python examples below follow the repo rule: `uv run python ...`.

### Cover letter

```bash
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --manuscript main.tex --letter cover_letter.md --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode journal-fit --letter cover_letter.md --journal nature --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode presubmission --letter cover_letter.md --journal nature --json
```

### Paper audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
uv run python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py paper.tex
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus full --review-dir review_results/paper
```

### English LaTeX paper

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex
```

### Chinese LaTeX thesis

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex
```

### Typst paper

```bash
uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ
```

### Bib library search

```bash
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "TimeMachine raw:true cite:both limit:1" | uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py
```

## 3. Typical Prompt Patterns

```text
Generate a Nature cover letter from main.tex, then check whether every strong claim is supported by the manuscript.
```

```text
Run a gate audit on paper.pdf before submission and separate blockers from advisory issues.
```

```text
Compile main.tex with the latex-paper-en skill, then check the abstract structure.
```

```text
Map the structure of thesis.tex and check GB/T bibliography issues.
```

```text
Compile main.typ and review the algorithm-figure pseudocode for IEEE-like formatting.
```

```text
Search references.bib for Cheng papers after 2024 on Mamba forecasting and return both LaTeX and Typst citations.
```

## 4. Recommended First Workflow

### For cover letters

1. Use `generate` when you only have the manuscript.
2. Use `optimize` when a draft already exists.
3. Run `align-check` before trusting any novelty or contribution claim.
4. Run `journal-fit` for a target venue and `presubmission` for declaration, length, cliché, and tone checks.

### For audits

1. Choose `quick-audit`, `deep-review`, `gate`, `polish`, or `re-audit`.
2. Point to the `.tex`, `.typ`, or `.pdf` file.
3. Use `quick-audit` for fast screening and `gate` for blockers.
4. Use `deep-review` when you need the review workspace, issue bundle, revision trajectory, and Markdown/HTML reports.

### For LaTeX papers

1. Compile.
2. Run format or bibliography checks.
3. Run grammar, sentence, logic, literature, experiment, or table checks on a target section.

### For Chinese theses

1. Run `structure` first.
2. Detect the template if it is unclear.
3. Compile and verify bibliography, consistency, logic, or tables.

### For Typst papers

1. Compile/export first.
2. Run format or bibliography checks.
3. Run language-quality, logic, literature, pseudocode, or table modules on the section you are editing.

### For bibliography search

1. Point to the `.bib` file first.
2. Start with a compact `--query`.
3. Add `cite:...` or `raw:true` only when you need citation forms or raw BibTeX.
4. Pipe into `preview_bib_search.py` when you want a compact summary instead of raw JSON.
