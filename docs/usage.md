# Usage

## Shared Input Contract

Provide:

- the primary file, such as `main.tex`, `main.typ`, `paper.pdf`, `references.bib`,
  or `cover_letter.md`;
- the intended scope: section, chapter, full paper, venue, journal, or audit focus;
- the desired module or mode when known.

Keep responsibilities separate. A bibliography match is not evidence that a claim is supported,
and a source-level writing check is not a reviewer-style submission decision.

## Skill Matrix

| Skill | Inputs | Responsibility | Hand off when |
| --- | --- | --- | --- |
| `cover-letter` | manuscript + optional letter | Submission-letter generation and evidence alignment | The manuscript itself needs editing or audit |
| `paper-audit` | `.tex`, `.typ`, `.pdf` | Critique, blockers, readiness, re-audit | Source changes or compile repair are required |
| `latex-paper-en` | English `.tex` | Source compile and targeted writing checks | A global reviewer report is required |
| `latex-thesis-zh` | Chinese thesis `.tex` | Thesis structure, GB/T, chapters, spec and blind review | The artifact is an English paper |
| `typst-paper` | `.typ` | Typst compile and targeted writing checks | The artifact is LaTeX |
| `bib-search-citation` | `.bib` | Retrieval, filtering, raw entries, citation snippets | Claim support must be verified in the paper |

## Current Routers

### `cover-letter`

`generate`, `optimize`, `align-check`, `journal-fit`, `presubmission`.

### `paper-audit`

`quick-audit`, `deep-review`, `gate`, `polish`, `re-audit`.

### `latex-paper-en`

`compile`, `format`, `bibliography`, `grammar`, `sentences`, `logic`,
`literature`, `section-writing`, `expression`, `translation`, `title`, `figures`,
`pseudocode`, `deai`, `experiment`, `tables`, `caption`, `abstract`, `adapt`.

### `latex-thesis-zh`

`compile`, `format`, `structure`, `consistency`, `template`, `bibliography`,
`title`, `deai`, `logic`, `literature`, `experiment`, `references`, `tables`,
`abstract`, `conclusion`, `spec-check`, `blind-review`.

For a whole thesis, start with `structure`. Use `spec-check` only with the correct school
template and degree, and run `blind-review --check` before generating a review copy.

### `typst-paper`

`compile`, `format`, `bibliography`, `grammar`, `sentences`, `logic`,
`literature`, `expression`, `translation`, `title`, `pseudocode`, `deai`,
`experiment`, `tables`, `references`, `abstract`, `adapt`.

### `bib-search-citation`

`query`, `spec-json`, `spec-file`, `preview`.

## Resource Loading

Each overview routes to a canonical resource group:

- `references/` for detailed rules;
- `templates/` for venue or format snapshots;
- `examples/` for end-to-end patterns;
- `agents/` for exposed reviewer/workflow contracts.

Load only the file required by the active module or mode. If the responsibility changes, return
to the skill matrix instead of silently combining incompatible workflows.

## Output Boundaries

- Writing skills preserve citations, labels, formulas, evidence, and source structure by default.
- `paper-audit` reports findings and decisions; it does not silently edit the manuscript.
- `cover-letter` must anchor novelty, contribution, and numeric claims to manuscript evidence.
- `bib-search-citation` reports bibliographic provenance, not semantic claim verification.
