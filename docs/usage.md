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
| `paper-audit` | `.tex`, `.typ`, `.pdf` | Readiness checks and structured review |
| `industrial-ai-research` | topic | Literature research and synthesis |

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

### `paper-audit`

Modes:
- `quick-audit`
- `deep-review`
- `gate`
- `polish`
- `re-audit`

Recommended routing:

- use `quick-audit` for fast script-backed screening
- use `deep-review` when you need reviewer-style findings, issue bundles, and a roadmap
- deep-review defaults to committee-style pre-review (`Editor -> Theory -> Literature -> Methodology -> Logic`)
- use `--focus editor|theory|literature|methodology|logic` when you only want one dimension
- use `gate` for blockers only
- use `re-audit` when a previous report already exists

### `industrial-ai-research`

Deliverable modes:
- `research-brief`
- `literature-map`
- `venue-ranked survey`
- `research-gap memo`
- `survey-draft`

This skill starts with intake questions before synthesis.

## Common Commands

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate
```

## Choosing the Right Workflow

### You are fixing a broken build

Use the compile module of the matching writing skill.

### You are polishing one section

Use `grammar`, `sentences`, `logic`, `expression`, `deai`, or `experiment` on that section rather than on the full document.

### You are about to submit

Use `paper-audit` after your compile and bibliography steps are already stable.

### You are not editing a paper yet, only researching

Use `industrial-ai-research`, not the writing skills.

### You want to draft a full survey paper

Use `industrial-ai-research` with the `survey-draft` deliverable mode. It builds an outline, assembles evidence packs, writes section-by-section, and optionally hands off to `latex-paper-en` for LaTeX formatting.

## Output Expectations

- Writing skills usually return issue-oriented suggestions and script-backed diagnostics.
- `paper-audit` returns severity-rated reports, structured issue bundles, revision roadmaps, reviewer-style `peer_review_report.md`, and optional score summaries.
- Research output should separate verified evidence from inference.
