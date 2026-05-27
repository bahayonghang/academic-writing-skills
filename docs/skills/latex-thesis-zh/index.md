# `latex-thesis-zh`

Chinese LaTeX degree-thesis assistant for existing `.tex` projects. It is optimized for thesis structure, templates, GB/T 7714, Chinese academic style, logic, literature, and chapter-level consistency.

## Use It For

- Compile diagnosis for XeLaTeX, LuaLaTeX, latexmk, and common thesis templates.
- Chapter/section structure mapping and template detection.
- GB/T 7714 bibliography and thesis-format checks.
- Term, abbreviation, and naming consistency across chapters.
- Logic coherence, literature review quality, research-gap derivation, heading lead-ins, and cross-section closure.
- Chinese abstract, title, experiment, de-AI, and table review.

## Do Not Use It For

- English conference or journal papers; use `latex-paper-en`.
- Typst projects; use `typst-paper`.
- PDF-only reviewer-style audits; use `paper-audit`.
- Cover letters or rebuttals.

## Module Router

| Module | Use when | Primary command |
| --- | --- | --- |
| `structure` | You need a thesis chapter/section map | `uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex` |
| `template` | Template/class is unclear | `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py thesis.tex` |
| `compile` | Thesis build fails | `uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex` |
| `format` | Thesis layout or GB/T concerns | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_format.py thesis.tex` |
| `consistency` | Terminology or naming drifts | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py thesis.tex --terms` |
| `bibliography` | GB/T 7714 bibliography checks | `uv run python academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gb7714` |
| `title` | Thesis or chapter title optimization | `uv run python academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py thesis.tex --check` |
| `deai` | Chinese AI-trace and low-information rhetoric checks | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py thesis.tex --section introduction` |
| `logic` | Chapter mainline, intro funnel, lit review quality, or closure | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py thesis.tex --section related` |
| `literature` | Literature review synthesis and gap derivation | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py thesis.tex --section related` |
| `experiment` | Experiment chapter and conclusion completeness | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py thesis.tex --section experiments` |
| `abstract` | Chinese abstract structure diagnosis | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py thesis.tex --lang zh` |
| `tables` | Three-line table and GB/T table checks | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_tables.py thesis.tex` |

## Minimum Inputs

- Thesis entry file such as `thesis.tex`.
- Bibliography path when checking GB/T references.
- School/template context when known.
- Chapter or section name for targeted review.

## Output Artifacts

- Thesis-oriented diagnostics and review comments.
- Structure maps, template signals, consistency findings, and source-preserving suggestions.
- Chinese academic-writing feedback that does not silently rewrite citations, labels, or math.

## Common Requests

```text
Map thesis.tex and identify missing required parts.
```

```text
Detect the template and summarize the constraints before compiling.
```

```text
Check references.bib for GB/T 7714 issues.
```

```text
Turn this literature review into a thematic synthesis plan without adding citations.
```

## Notes

- Run the smallest module that can answer the request before escalating to broader review.
- Preserve citations, labels, math, and source structure unless the user explicitly asks for edits.
- Use `paper-audit` after source-level compile and bibliography checks are stable when the goal is submission readiness.
