# Usage

## Cross-Skill Conventions

### Provide the smallest useful input

- entry file path: `main.tex`, `thesis.tex`, `main.typ`, `paper.pdf`, `references.bib`, or `cover_letter.md`
- optional scope: section, chapter, full document, venue, journal, or review focus
- target module or mode when you already know it

### Separate different intents

- compile when you want a build result
- check when you want diagnostics
- rewrite or optimize when you want proposed wording changes
- audit when you want severity-rated reviewer findings and a readiness judgment
- align-check when you want claims verified against visible manuscript evidence

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

| Skill | Input | Main use | Do not use for |
| --- | --- | --- | --- |
| `cover-letter` | `.tex` + optional `.md`/`.tex` letter | Submission letter generation, optimization, claim alignment, journal fit | Manuscript source editing or rebuttals |
| `paper-audit` | `.tex`, `.typ`, `.pdf` | Readiness checks, deep review, gate decisions, re-audit | Sentence-level source editing as the first step |
| `latex-paper-en` | `.tex` | English paper compile and targeted review | Chinese thesis or Typst projects |
| `latex-thesis-zh` | `.tex` | Chinese thesis compile, structure, GB/T, and targeted review | English conference/journal papers |
| `typst-paper` | `.typ` | Typst paper compile and targeted review | LaTeX-first projects |
| `bib-search-citation` | `.bib` | Search, filter, preview, and cite bibliography entries | Proving a manuscript claim is supported |

## Module and Mode Summary

### `cover-letter`

Modes:

- `generate` — draft from a LaTeX manuscript.
- `optimize` — review and improve an existing letter without overwriting it.
- `align-check` — verify letter claims against manuscript evidence.
- `journal-fit` — score scope fit, novelty framing, evidence density, and format compliance.
- `presubmission` — check declarations, length, clichés, paragraph shape, and AI-tone phrases.

Recommended default: if a draft exists, run `align-check` before `journal-fit`; if no draft exists, run `generate` first.

### `paper-audit`

Modes:

- `quick-audit`
- `deep-review`
- `gate`
- `polish`
- `re-audit`

Recommended routing:

- use `quick-audit` for fast script-backed screening;
- use `gate` for blocker-only submission decisions;
- use `deep-review` when you need reviewer-style findings, review workspace artifacts, claim maps, revision suggestions, revision trajectory, and Markdown/HTML reports;
- use `--focus editor|theory|literature|methodology|logic` when you only want one committee dimension;
- use `re-audit` when a previous report exists.

### `latex-paper-en`

Modules: `compile`, `format`, `bibliography`, `grammar`, `sentences`, `logic`, `literature`, `expression`, `translation`, `title`, `figures`, `pseudocode`, `deai`, `experiment`, `abstract`, `tables`, `caption`, `adapt`.

### `latex-thesis-zh`

Modules: `compile`, `format`, `structure`, `consistency`, `template`, `bibliography`, `title`, `deai`, `logic`, `literature`, `experiment`, `abstract`, `tables`.

Recommended default for full-review work: run `structure` first.

### `typst-paper`

Modules: `compile`, `format`, `bibliography`, `grammar`, `sentences`, `logic`, `literature`, `expression`, `translation`, `title`, `pseudocode`, `deai`, `experiment`, `abstract`, `tables`, `caption`, `adapt`.

### `bib-search-citation`

Search surfaces:

- `--query`
- `--spec-json`
- `--spec-file`
- `preview_bib_search.py`

Recommended default: start with a compact `--query`, then add `cite:...`, `raw:true`, or `--return-fields` only when the request needs them.

## Common Commands

```bash
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --manuscript main.tex --letter cover_letter.md --json
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate
uv run python academic-writing-skills/paper-audit/scripts/render_html_report.py review_results/paper --lang en
uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex
uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check
uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"
```

## Choosing the Right Workflow

### You need a submission cover letter

Use `cover-letter`, not a generic prose editor. The important boundary is manuscript evidence: `align-check` flags unsupported novelty, contribution, and numeric claims before submission.

### You are about to submit

Use `paper-audit` after compile and bibliography steps are stable. For final-week mechanical checks, the `PRESUBMISSION` layer runs inside audit modes; PDF inputs get text-only checks.

### You are fixing a broken build

Use the compile module of `latex-paper-en`, `latex-thesis-zh`, or `typst-paper`, depending on the source format.

### You are polishing one section

Use `grammar`, `sentences`, `logic`, `literature`, `expression`, `deai`, or `experiment` on that section rather than on the full document.

### You need to search a `.bib` library or return citation snippets

Use `bib-search-citation`, not the writing skills. A `.bib` match is bibliographic provenance, not evidence that a paper supports a manuscript claim.

## Output Expectations

- `cover-letter` returns a draft scaffold or findings tagged by mode, with claim-evidence issues separated from journal-fit and pre-submission issues.
- `paper-audit` returns severity-rated reports, `PRESUBMISSION` findings, structured issue bundles, claim maps, revision suggestions, revision trajectories, Markdown/HTML reports, and optional score summaries.
- Writing skills return issue-oriented suggestions and script-backed diagnostics while preserving citations, labels, math, and source structure by default.
- `bib-search-citation` returns structured search results, optional raw BibTeX, and citation-ready snippets.
