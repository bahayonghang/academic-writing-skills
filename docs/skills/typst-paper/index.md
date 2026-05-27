# `typst-paper`

Typst academic paper assistant for existing `.typ` manuscripts in English or Chinese. It mirrors the paper-writing workflow while respecting Typst syntax, labels, bibliography formats, and pseudocode conventions.

## Use It For

- Typst compile/export, font, and watch issues.
- Venue formatting and layout checks.
- BibTeX or Hayagriva bibliography validation.
- Grammar, sentence, expression, translation, title, abstract, table, and de-AI review.
- Logic, literature synthesis, research-gap derivation, cross-section closure, and experiment-section review.
- IEEE-like pseudocode review for `algorithmic`, `algorithm-figure`, and `lovelace`.

## Do Not Use It For

- LaTeX-first papers; use `latex-paper-en` or `latex-thesis-zh`.
- DOCX/PDF-only edits without Typst source.
- Reviewer-style scoring or gate decisions; use `paper-audit`.
- Cover-letter tasks.

## Module Router

| Module | Use when | Primary command |
| --- | --- | --- |
| `compile` | Build, export, or font issues | `uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ` |
| `format` | Layout or venue style checks | `uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ` |
| `bibliography` | BibTeX or Hayagriva validation | `uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ` |
| `grammar` | Grammar cleanup | `uv run python academic-writing-skills/typst-paper/scripts/analyze_grammar.py main.typ --section introduction` |
| `sentences` | Long or dense sentence review | `uv run python academic-writing-skills/typst-paper/scripts/analyze_sentences.py main.typ --section introduction` |
| `logic` | Coherence, intro funnel, abstract/conclusion alignment, or closure | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `literature` | Related-work synthesis and gap derivation | `uv run python academic-writing-skills/typst-paper/scripts/analyze_literature.py main.typ --section related` |
| `expression` | Academic tone polish | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | Chinese/English academic translation | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py input_zh.txt --domain deep-learning` |
| `title` | Title checking or optimization | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `pseudocode` | `algorithmic`, `algorithm-figure`, or `lovelace` review | `uv run python academic-writing-skills/typst-paper/scripts/check_pseudocode.py main.typ --venue ieee` |
| `deai` | English or Chinese AI-trace checks | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | Experiment write-up and discussion layering | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |
| `abstract` | Five-element abstract diagnosis | `uv run python academic-writing-skills/typst-paper/scripts/analyze_abstract.py main.typ` |
| `tables` | Table structure and three-line checks | `uv run python academic-writing-skills/typst-paper/scripts/check_tables.py main.typ` |
| `caption` | Figure/table caption quality review | LLM-driven module |
| `adapt` | Venue-to-venue adaptation | LLM-driven workflow |

## Minimum Inputs

- Entry file such as `main.typ`.
- Optional section name for local analysis.
- Bibliography path; BibTeX and Hayagriva are both supported.
- Venue or IEEE-like context for pseudocode and formatting.

## Output Artifacts

- Typst-ready diagnostics and review comments.
- Source-preserving suggestions that keep `@cite`, labels, math, and Typst structure intact by default.
- Module-level findings that can feed later audit or submission workflows.

## Common Requests

```text
Compile main.typ and explain the first error.
```

```text
Verify references.bib against main.typ.
```

```text
Review this algorithm-figure block for caption and line-number issues.
```

```text
Rewrite-plan the Related Work so it becomes synthesis rather than citation listing.
```

## Notes

- Run the smallest module that can answer the request before escalating to broader review.
- Preserve citations, labels, math, and source structure unless the user explicitly asks for edits.
- Use `paper-audit` after source-level compile and bibliography checks are stable when the goal is submission readiness.
