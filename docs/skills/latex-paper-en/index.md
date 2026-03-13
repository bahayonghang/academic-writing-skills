# `latex-paper-en`

English LaTeX paper assistant for existing `.tex` projects.

## Use It For

- compile failures
- format or venue checks
- bibliography validation
- grammar and sentence cleanup
- logic and argument-flow review
- literature review quality checks (thematic organization, gap derivation)
- discussion depth and results-literature echo analysis
- conclusion completeness validation
- cross-section logic chain closure
- expression polishing
- Chinese-to-English academic translation
- title, figure, de-AI, and experiment-section review
- anti-citation-stacking checks (Introduction and Related Work)

## Do Not Use It For

- writing a paper from scratch
- Chinese thesis template work
- Typst-first projects
- literature research without a paper project

## Module Router

| Module | Best for | Script |
| --- | --- | --- |
| `compile` | build or diagnose `main.tex` | `uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex` |
| `format` | LaTeX or venue formatting issues | `uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex` |
| `bibliography` | BibTeX validation and missing citations | `uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex` |
| `grammar` | grammar cleanup | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_grammar.py main.tex --section introduction` |
| `sentences` | long or dense sentences | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_sentences.py main.tex --section introduction` |
| `logic` | coherence, methodological flow, lit review quality, cross-section closure | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods` |
| `expression` | academic tone polish | `uv run python academic-writing-skills/latex-paper-en/scripts/improve_expression.py main.tex --section related` |
| `translation` | Chinese to English academic translation | `uv run python academic-writing-skills/latex-paper-en/scripts/translate_academic.py input.txt --domain deep-learning` |
| `title` | title checking or generation | `uv run python academic-writing-skills/latex-paper-en/scripts/optimize_title.py main.tex --check` |
| `figures` | figure existence, DPI, captions | `uv run python academic-writing-skills/latex-paper-en/scripts/check_figures.py main.tex` |
| `deai` | reduce AI writing traces | `uv run python academic-writing-skills/latex-paper-en/scripts/deai_check.py main.tex --section introduction` |
| `experiment` | experiment-section review, discussion depth, conclusion completeness | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_experiment.py main.tex --section experiments` |

## Minimum Inputs

- entry file such as `main.tex`
- optional section name when the task is local
- optional bibliography path for bibliography work
- optional venue context like IEEE, ACM, Springer, NeurIPS, or ICML
- for `translation`, a pasted paragraph or standalone text file is also acceptable when no full-project scan is needed

## Good First Requests

```text
Compile main.tex with the latex-paper-en skill.
```

```text
Check the introduction for grammar and long sentences, but do not touch citations.
```

```text
Audit figures and bibliography before submission.
```

## Notes

- Preserve `\cite{}`, `\ref{}`, `\label{}`, and math unless you explicitly want source edits.
- Use one module at a time when you need clear diagnostics.
- Expected output is source-preserving review feedback, usually LaTeX-oriented comments, not silent rewrites.
- Eval coverage currently spans 6 prompt patterns: compile+bibliography, grammar+sentences+logic, figures+title, translation with LaTeX preservation, de-AI review, and experiment-section review.
- Anti-citation-stacking: max 2 clustered citations per sentence without individual discussion. Sentences with 3+ stacked references are flagged as AI writing traces in Introduction and Related Work.
- The `logic` module now checks literature review quality (A1: author enumeration, A3: gap derivation) and cross-section logic chain closure (C3: intro claims answered in conclusion). Use `--cross-section` for full-document closure checks.
- The `experiment` module now checks discussion depth (B3), results-literature echo (B4), and conclusion completeness (B5: findings + implications + limitations).
