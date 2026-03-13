# `latex-thesis-zh`

Chinese LaTeX thesis assistant for existing `.tex` thesis projects.

## Use It For

- structure mapping
- GB/T 7714-related format checks
- template detection
- thesis compilation
- term or naming consistency checks
- title optimization
- de-AI cleanup
- experiment-chapter review
- citation stacking detection (Introduction and Related Work chapters)

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
| `deai` | reduce AI writing traces | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py thesis.tex --section introduction` |
| `experiment` | experiment-section review | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py thesis.tex --section experiments` |

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

## Notes

- This skill is thesis-specific and not the right tool for English conference papers.
- Preserve citations, labels, and math by default.
- Citation stacking detection (Category 6 in de-AI): flags sentences with 3+ clustered citations without per-work discussion in Introduction and Related Work chapters. Max 2 clustered citations per sentence unless stating well-established background facts.
