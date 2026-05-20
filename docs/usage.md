# Usage

## Cross-Skill Conventions

These conventions apply across the skill set.

### Provide the smallest useful input

- entry file path: `main.tex`, `thesis.tex`, `main.typ`, or `paper.pdf`
- optional scope: section, chapter, or full document
- target module or mode when you already know it

### Separate different intents

- compile when you want a build result
- check when you want diagnostics
- rewrite when you want proposed wording changes
- audit when you want a report with severity and scoring

### Repo-local command style

In this repository, run Python scripts with:

```bash
uv run python path/to/script.py ...
```

Run tests with:

```bash
uv run python -m pytest tests/
```

## Skill Matrix

| Skill | Input | Main use |
| --- | --- | --- |
| `latex-paper-en` | `.tex` | English paper compile and review |
| `latex-thesis-zh` | `.tex` | Chinese thesis compile and review |
| `typst-paper` | `.typ` | Typst paper compile and review |
| `bib-search-citation` | `.bib` | Search, filter, preview, and cite bibliography entries |
| `paper-audit` | `.tex`, `.typ`, `.pdf` | Readiness checks and structured review |

## Module Summary

### `latex-paper-en`

Modules:
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

Modules:
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

Recommended default for full-review work: run `structure` first.

### `typst-paper`

Modules:
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

Search surfaces:
- `--query`
- `--spec-json`
- `--spec-file`
- `preview_bib_search.py`

Recommended default: start with a compact `--query`, then add `cite:...`, `raw:true`,
or `--return-fields` only when the request needs them.

### `paper-audit`

Modes:
- `quick-audit`
- `deep-review`
- `gate`
- `polish`
- `re-audit`

Recommended routing:

- use `quick-audit` for fast script-backed screening
- use `quick-audit` for final-week pre-submission mechanical checks
- use `deep-review` when you need reviewer-style findings, issue bundles, and a roadmap
- deep-review defaults to committee-style pre-review (`Editor -> Theory -> Literature -> Methodology -> Logic`)
- use `--focus editor|theory|literature|methodology|logic` when you only want one dimension
- use `gate` for blockers only
- use `re-audit` when a previous report already exists

## Common Commands

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

## Choosing the Right Workflow

### You are fixing a broken build

Use the compile module of the matching writing skill.

### You are polishing one section

Use `grammar`, `sentences`, `logic`, `expression`, `deai`, or `experiment` on that section rather than on the full document.

### You are about to submit

Use `paper-audit` after your compile and bibliography steps are already stable.
For final-week mechanical checks, the `PRESUBMISSION` layer runs inside
`quick-audit` and `gate`; PDF inputs get text-only checks.

### You need to search a `.bib` library or return citation snippets

Use `bib-search-citation`, not the writing skills. It works on the bibliography file itself,
not on the paper source tree.

## Output Expectations

- Writing skills usually return issue-oriented suggestions and script-backed diagnostics.
- `bib-search-citation` returns structured search results, optional raw BibTeX, and citation-ready snippets.
- `paper-audit` returns severity-rated reports, `PRESUBMISSION` mechanical findings, structured issue bundles, revision roadmaps, reviewer-style `peer_review_report.md`, and optional score summaries.
