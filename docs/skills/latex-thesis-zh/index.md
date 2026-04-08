# `latex-thesis-zh`

Chinese LaTeX thesis assistant for existing `.tex` thesis projects.

## Use It For

- structure mapping
- GB/T 7714-related format checks
- template detection
- thesis compilation
- term or naming consistency checks
- logic and coherence review (literature review quality, cross-section closure)
- literature review rewrite blueprints for thesis-style synthesis and gap derivation
- discussion depth and conclusion completeness checks
- title optimization
- de-AI cleanup (including filler connector and parallel sentence detection)
- experiment-chapter review
- citation stacking detection (Introduction and Related Work chapters)
- abstract structural analysis (five-element model)
- three-line table compliance checking and generation

## Recommended Default

For large or multi-file theses, run `structure` first.

## Module Router

| Module | Best for | Script |
| --- | --- | --- |
| `compile` | thesis build issues | `uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex` |
| `format` | thesis formatting or GB/T concerns | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_format.py thesis.tex` |
| `structure` | chapter and section map | `uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex` |
| `consistency` | term drift across chapters | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py thesis.tex --terms` |
| `template` | detect or validate thesis template | `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex` |
| `bibliography` | GB/T 7714 bibliography checks | `uv run python academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gb7714` |
| `title` | title or chapter-title optimization | `uv run python academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py thesis.tex --check` |
| `deai` | reduce AI writing traces and low-information rhetoric | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py thesis.tex --section introduction` |
| `logic` | coherence, introduction funnel, chapter mainline, lit review quality, cross-section closure | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py thesis.tex --section related` |
| `literature` | thesis literature review synthesis, comparison, and gap derivation | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py thesis.tex --section related` |
| `experiment` | experiment-section review, discussion depth/layering, conclusion completeness | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py thesis.tex --section experiments` |
| `abstract` | five-element abstract structural diagnosis | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py thesis.tex` |
| `tables` | three-line table compliance and generation (GB/T) | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_tables.py thesis.tex` |

## Good First Requests

```text
Map the structure of thesis.tex and identify missing required parts.
```

```text
Detect the template and summarize the key thesis constraints.
```

```text
Check references.bib for GB/T 7714 issues.
```

```text
Rewrite this literature review section into a thematic synthesis, but do not add any new citations.
```

## Notes

- This skill is thesis-specific and not the right tool for English conference papers.
- Preserve citations, labels, and math by default.
- Minimum useful input is the thesis entry file such as `thesis.tex`; add a bibliography path only when the request targets references.
- Expected output is source-preserving thesis review feedback, typically `% Module (L##) [Severity] [Priority]: ...`, rather than broad rewrites.
- Eval coverage currently spans 3 prompt patterns: template+compile diagnosis, structure+consistency review, and bibliography+de-AI checks.
- Use `literature` when the request is explicitly about rewriting the literature review or deriving the gap. Keep `logic` for intro funnel, chapter mainline, and cross-section closure.
- The `logic` module checks literature review quality (A1: author enumeration, A3: gap derivation) and cross-section logic chain closure (C3). Use `--cross-section` for full-document closure checks.
- The `experiment` module checks discussion depth (B3), results-literature echo (B4), and conclusion completeness (B5).
- The `deai` module now detects AI filler connectors (C1) and parallel sentence structures (C2) in addition to existing AI trace patterns.
- Citation stacking detection (Category 6 in de-AI): flags sentences with 3+ clustered citations without per-work discussion in Introduction and Related Work chapters. Max 2 clustered citations per sentence unless stating well-established background facts.
