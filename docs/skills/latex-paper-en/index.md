# `latex-paper-en`

English LaTeX paper assistant for existing `.tex` projects.

## Use It For

- compile failures
- format or venue checks
- bibliography validation
- grammar and sentence cleanup
- logic and argument-flow review
- literature review quality checks and rewrite blueprints (thematic organization, comparison, gap derivation)
- discussion depth and results-literature echo analysis
- conclusion completeness validation
- cross-section logic chain closure
- expression polishing
- Chinese-to-English academic translation
- title, figure, de-AI, and experiment-section review
- IEEE-safe pseudocode review for `algorithm2e`, `algorithmicx`, and `algpseudocodex`
- anti-citation-stacking checks (Introduction and Related Work)
- abstract structural analysis (five-element model)
- three-line table compliance checking and generation
- venue-to-venue format adaptation (journal/conference switching)

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
| `logic` | coherence, introduction funnel, lit review quality, abstract/conclusion alignment, cross-section closure | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods` |
| `literature` | related-work synthesis, comparative analysis, and research-gap derivation | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_literature.py main.tex --section related` |
| `expression` | academic tone polish | `uv run python academic-writing-skills/latex-paper-en/scripts/improve_expression.py main.tex --section related` |
| `translation` | Chinese to English academic translation | `uv run python academic-writing-skills/latex-paper-en/scripts/translate_academic.py input.txt --domain deep-learning` |
| `title` | title checking or generation | `uv run python academic-writing-skills/latex-paper-en/scripts/optimize_title.py main.tex --check` |
| `figures` | figure existence, DPI, captions | `uv run python academic-writing-skills/latex-paper-en/scripts/check_figures.py main.tex` |
| `pseudocode` | IEEE-safe pseudocode, float, caption, label, comment, and line-number review | `uv run python academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py main.tex --venue ieee` |
| `deai` | reduce AI writing traces and low-information boilerplate | `uv run python academic-writing-skills/latex-paper-en/scripts/deai_check.py main.tex --section introduction` |
| `experiment` | experiment-section review, discussion depth/layering, conclusion completeness | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_experiment.py main.tex --section experiments` |
| `abstract` | five-element abstract structural diagnosis | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex` |
| `tables` | three-line table compliance and generation | `uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex` |
| `caption` | figure and table caption quality review | LLM-driven (no standalone script) |
| `adapt` | venue-to-venue format adaptation | LLM-driven (see [Adaptation Workflow](./resources/references/JOURNAL_ADAPTATION_WORKFLOW)) |

## Minimum Inputs

- entry file such as `main.tex`
- optional section name when the task is local
- optional bibliography path for bibliography work
- optional venue context like IEEE, ACM, Springer, NeurIPS, or ICML
- for `pseudocode`, the target venue matters because IEEE-safe defaults are stricter than general LaTeX advice
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

```text
Analyze the abstract structure and check if all five elements are present.
```

```text
Check all tables for three-line rule compliance and decimal alignment.
```

```text
Check whether this IEEE pseudocode still uses algorithm2e floats and whether the caption is reviewer-safe.
```

```text
Rewrite the Related Work so it reads like a synthesis instead of a paper list, but keep all citation anchors intact.
```

## Notes

- Preserve `\cite{}`, `\ref{}`, `\label{}`, and math unless you explicitly want source edits.
- Use one module at a time when you need clear diagnostics.
- Expected output is source-preserving review feedback, usually LaTeX-oriented comments, not silent rewrites.
- Eval coverage now includes pseudocode prompts for IEEE float migration, caption/label hygiene, and advisory-vs-mandatory wording.
- Use `literature` when the request is specifically about rewriting or re-structuring Related Work. Keep `logic` for intro funnel and cross-section closure.
- Anti-citation-stacking: max 2 clustered citations per sentence without individual discussion. Sentences with 3+ stacked references are flagged as AI writing traces in Introduction and Related Work.
- The `logic` module now checks literature review quality (A1: author enumeration, A3: gap derivation) and cross-section logic chain closure (C3: intro claims answered in conclusion). Use `--cross-section` for full-document closure checks.
- The `experiment` module now checks discussion depth (B3), results-literature echo (B4), and conclusion completeness (B5: findings + implications + limitations).
