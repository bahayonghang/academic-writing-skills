# `latex-paper-en`

English LaTeX paper assistant for existing `.tex` conference and journal manuscripts. It is the source-level workflow for compile, format, bibliography, language, logic, literature, pseudocode, tables, and experiment-section diagnostics.

## Use It For

- Compile failures and LaTeX build diagnosis.
- Venue formatting for IEEE, ACM, Springer, NeurIPS, ICML, and similar paper templates.
- Bibliography and citation validation inside a `.tex` paper project.
- Grammar, sentence, expression, translation, title, abstract, figure, table, and caption review.
- Logic, literature synthesis, research-gap derivation, cross-section closure, and experiment-section review.
- IEEE-safe pseudocode review for `algorithm2e`, `algorithmicx`, and `algpseudocodex`.
- De-AI review that preserves LaTeX syntax, citations, labels, and math.

## Do Not Use It For

- Writing a paper from scratch.
- Chinese thesis template work.
- Typst-first projects.
- Reviewer-style scoring or gate decisions; use `paper-audit`.
- Cover-letter generation; use `cover-letter`.

## Module Router

| Module | Use when | Primary command |
| --- | --- | --- |
| `compile` | Build fails or you need a fresh compile | `uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex` |
| `format` | Venue or LaTeX formatting is in question | `uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex` |
| `bibliography` | Citations or BibTeX need validation | `uv run python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex` |
| `grammar` | Surface-level grammar review | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_grammar.py main.tex --section introduction` |
| `sentences` | Long or dense sentence diagnostics | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_sentences.py main.tex --section introduction` |
| `logic` | Coherence, intro funnel, abstract/conclusion alignment, or closure | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_logic.py main.tex --section methods` |
| `literature` | Related Work synthesis, comparison, and gap derivation | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_literature.py main.tex --section related` |
| `expression` | Academic tone polish | `uv run python academic-writing-skills/latex-paper-en/scripts/improve_expression.py main.tex --section related` |
| `translation` | Chinese-to-English academic translation | `uv run python academic-writing-skills/latex-paper-en/scripts/translate_academic.py input.txt --domain deep-learning` |
| `title` | Title checking or generation | `uv run python academic-writing-skills/latex-paper-en/scripts/optimize_title.py main.tex --check` |
| `figures` | Figure existence, extension, DPI, or caption review | `uv run python academic-writing-skills/latex-paper-en/scripts/check_figures.py main.tex` |
| `pseudocode` | Algorithm block, caption, label, comment, and line-number review | `uv run python academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py main.tex --venue ieee` |
| `deai` | AI-trace and low-information boilerplate checks | `uv run python academic-writing-skills/latex-paper-en/scripts/deai_check.py main.tex --section introduction` |
| `experiment` | Experiment write-up, discussion depth, and conclusion completeness | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_experiment.py main.tex --section experiments` |
| `abstract` | Five-element abstract diagnosis | `uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex` |
| `tables` | Table structure, booktabs, and three-line compliance | `uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex` |
| `caption` | Figure/table caption quality review | LLM-driven module |
| `adapt` | Venue-to-venue adaptation | LLM-driven workflow |

## Minimum Inputs

- Entry file such as `main.tex`.
- Optional `--section` or section name for local checks.
- Bibliography path for bibliography work.
- Venue context when formatting, pseudocode, or adaptation matters.

## Output Artifacts

- Script-backed diagnostics and issue-oriented review comments.
- Source-preserving suggestions that keep citations, labels, math, and LaTeX structure intact by default.
- Module-specific findings suitable for staged fixing before `paper-audit` or `cover-letter` workflows.

## Common Requests

```text
Compile main.tex and explain the first blocking error.
```

```text
Check the introduction for grammar and long sentences, but do not touch citations.
```

```text
Review this IEEE pseudocode for algorithm2e usage, caption safety, and label hygiene.
```

```text
Analyze the Related Work and derive a synthesis-first rewrite plan.
```

## Notes

- Run the smallest module that can answer the request before escalating to broader review.
- Preserve citations, labels, math, and source structure unless the user explicitly asks for edits.
- Use `paper-audit` after source-level compile and bibliography checks are stable when the goal is submission readiness.
