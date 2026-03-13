# `typst-paper`

Typst academic paper assistant for existing `.typ` projects in English or Chinese.

## Use It For

- Typst compile or export issues
- format and venue checks
- bibliography validation for BibTeX or Hayagriva
- grammar, sentence, logic, and expression review
- translation and bilingual polishing
- title optimization
- de-AI cleanup
- experiment-section review
- anti-citation-stacking checks (Introduction and Related Work)

## Module Router

| Module | Best for | Script |
| --- | --- | --- |
| `compile` | build, export, or font issues | `uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ` |
| `format` | layout or style checks | `uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ` |
| `bibliography` | BibTeX or Hayagriva validation | `uv run python academic-writing-skills/typst-paper/scripts/verify_bib.py references.bib --typ main.typ` |
| `grammar` | grammar cleanup | `uv run python academic-writing-skills/typst-paper/scripts/analyze_grammar.py main.typ --section introduction` |
| `sentences` | long or dense sentence review | `uv run python academic-writing-skills/typst-paper/scripts/analyze_sentences.py main.typ --section introduction` |
| `logic` | coherence review | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `expression` | academic tone polish | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | Chinese and English academic translation | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py main.typ --section abstract` |
| `title` | title checking or optimization | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `deai` | reduce AI writing traces | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | experiment-section review | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |

## Good First Requests

```text
Compile main.typ and explain the first error.
```

```text
Check the abstract for grammar and academic tone.
```

```text
Verify references.bib against main.typ.
```

## Notes

- This skill is not for LaTeX-first projects.
- Keep `@cite`, labels, and math intact unless you explicitly want edits.
- Anti-citation-stacking: max 2 clustered citations per sentence without individual discussion. Sentences with 3+ stacked references are flagged as AI writing traces in Introduction and Related Work.
