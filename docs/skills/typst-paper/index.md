# `typst-paper`

Typst academic paper assistant for existing `.typ` projects in English or Chinese.

## Use It For

- Typst compile or export issues
- format and venue checks
- bibliography validation for BibTeX or Hayagriva
- grammar, sentence, logic, and expression review
- literature review quality checks (thematic organization, gap derivation)
- discussion depth, results-literature echo, and conclusion completeness
- cross-section logic chain closure
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
| `logic` | coherence, introduction funnel, lit review quality, abstract/conclusion alignment, cross-section closure | `uv run python academic-writing-skills/typst-paper/scripts/analyze_logic.py main.typ --section methods` |
| `expression` | academic tone polish | `uv run python academic-writing-skills/typst-paper/scripts/improve_expression.py main.typ --section methods` |
| `translation` | Chinese and English academic translation | `uv run python academic-writing-skills/typst-paper/scripts/translate_academic.py input_zh.txt --domain deep-learning` |
| `title` | title checking or optimization | `uv run python academic-writing-skills/typst-paper/scripts/optimize_title.py main.typ --check` |
| `deai` | reduce English or Chinese AI writing traces, including low-information filler | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | experiment-section review, discussion depth/layering, conclusion completeness | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |

## Minimum Inputs

- entry file such as `main.typ`
- optional section name for targeted analysis
- optional bibliography path; BibTeX and Hayagriva sources are both supported
- for `translation`, a local section target or pasted passage both work as long as Typst labels and math should be preserved

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
- Expected output is Typst-ready, source-preserving review feedback rather than silent rewrites.
- Eval coverage currently spans 3 prompt patterns: compile+format review, bibliography validation with BibTeX/Hayagriva routing, and expression+translation while preserving Typst labels.
- The `logic` module checks literature review quality (A1: author enumeration, A3: gap derivation) and cross-section logic chain closure (C3). Use `--cross-section` for full-document closure checks.
- The `experiment` module checks discussion depth (B3), results-literature echo (B4), and conclusion completeness (B5: findings + implications + limitations).
- Anti-citation-stacking: max 2 clustered citations per sentence without individual discussion. Sentences with 3+ stacked references are flagged as AI writing traces in Introduction and Related Work.
