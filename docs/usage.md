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
| `paper-writing-studio` | prose text + optional venue, journal, or domain | Venue-profile polish and translation with protected evidence tokens | The source file needs compile, format, or structure work |
| `latex-defense-zh` | Chinese thesis LaTeX repository | Beamer defense deck, speaker notes, fidelity quality gate, and preview | The user needs `.pptx`, a conference talk, or edits to the thesis text |

## Current Routers

### `cover-letter`

`generate`, `optimize`, `align-check`, `journal-fit`, `presubmission`.

### `paper-audit`

`quick-audit`, `deep-review`, `gate`, `polish`, `re-audit`.

### `latex-paper-en`

`compile`, `format`, `bibliography`, `grammar`, `sentences`, `logic`,
`literature`, `section-writing`, `expression`, `translation`, `title`, `figures`,
`pseudocode`, `deai`, `claim-forward`, `experiment`, `tables`, `caption`, `abstract`, `adapt`.

### `latex-thesis-zh`

`compile`, `format`, `structure`, `consistency`, `template`, `bibliography`,
`title`, `deai`, `claim-forward`, `polish`, `logic`, `literature`, `experiment`, `references`, `tables`,
`abstract`, `conclusion`, `spec-check`, `blind-review`.

For a whole thesis, start with `structure`. Use `spec-check` only with the correct school
template and degree, and run `blind-review --check` before generating a review copy.
Opt-in checks only report local candidates: `check_consistency.py --governance` requires `--custom-terms`, `--abbreviation-style` is independent, and `check_style_zh.py --degree-wording` is off by default; without these flags the previous output stays unchanged.
College number, equation, table-body, and Chinese-caption checks use `--school yanshan-ee-2025` on `check_style_zh.py`, `check_format.py`, `check_tables.py`, and `check_references.py`. The default and `--school generic` add no candidates, and there is no bare `yanshan` alias.
Citation placement, repeated-citation pages, college bibliography prompts, and review progression density run only behind explicit flags: `check_references.py --author-cite` and `--repeat-cite` are independent and may combine with `--school`; `verify_bib.py --college-details` is legal only with `--standard gb7714` or `gb7714-2025`; `analyze_literature.py --progression-density` may combine with `--section` and is mutually exclusive with `--intro-citations`. Without these flags the previous output stays unchanged.
Same-chapter table, body, and chapter-summary final values are compared only by `analyze_experiment.py --cross-surface`. `--section` may narrow the chapter. `--cross-surface-terms FILE` is valid only with that switch and replaces only the metric or evaluation-set list. Candidates are `[Script]`, Info/P3, and `Meaning-Check: NEEDS-LLM`, with a local position and no corrected number. Without `--cross-surface` the previous output stays unchanged, and the existing `--results-analysis` codes stay independent.
The graduate-school checklist is `--template yanshan`. The 2025 college checklist is `--template yanshan-ee-2025`. The two coexist. 111 statuses are not 111 compliant items. A partial checker does not PASS a compound item, and MODULE or NEEDS-LLM still needs human review.
Method-expression labels, a weakness written as an advantage, a pronoun left without an antecedent after a deleted preview, abstract quotation marks, and formula symbols in a title or chapter-arrangement line are LLM-only readings on the existing `logic`, `claim-forward`, `abstract`, and `structure` modules. They add no script code, no threshold, and no new module.

### `typst-paper`

`compile`, `format`, `bibliography`, `grammar`, `sentences`, `logic`,
`literature`, `expression`, `translation`, `title`, `pseudocode`, `deai`,
`experiment`, `tables`, `references`, `abstract`, `adapt`.

### `bib-search-citation`

`query`, `spec-json`, `spec-file`, `preview`.

### `paper-writing-studio`

`nature`, `ieee`, `elsevier`, `unspecified`.

The profile precedence is explicit venue > journal allowlist > unambiguous domain > `unspecified`.

### `latex-defense-zh`

`extract`, `plan`, `build`, `check`, `preview`.

The workflow has three user checkpoints: chapter roles after `extract`, the takeaway outline before `build`, and the delivery list after `preview`.

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
