# `latex-paper-en`

English LaTeX paper assistant for existing `.tex` conference and journal manuscripts. It is the source-level workflow for compile, format, bibliography, language, logic, literature, figures, captions, section-writing, pseudocode, tables, and experiment-section diagnostics.

## Use It For

- Compile failures and LaTeX build diagnosis.
- Venue formatting for IEEE, ACM, Springer, NeurIPS, ICML, and similar paper templates.
- Bibliography and citation validation inside a `.tex` paper project.
- Grammar, sentence, expression, translation, title, abstract, figure, table, and caption review.
- Logic, literature synthesis, research-gap derivation, cross-section closure, and experiment-section review.
- Section-specific rewrite planning for Abstract, Introduction, Related Work, Method, Experiments, and Conclusion with paragraph roles and claim-evidence maps.
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
| `section-writing` | Section-specific outline, paragraph roles, rewrite plan, and claim-evidence self-review | LLM-driven workflow |
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

## Public Resources

### References

- [Journal Name Abbreviations](./resources/references/citations/journal-abbreviations.md)
- [Citation Style Guide](./resources/references/citations/styles.md)
- [Citation Verification Guide](./resources/references/citations/verification.md)
- [Protected Terms - DO NOT Modify](./resources/references/deai/forbidden-terms.md)
- [De-AI Writing Guide for English Academic Papers](./resources/references/deai/guide.md)
- [AI Tone Terms (English) — Reference](./resources/references/deai/tone-terms-en.md)
- [AI Tone Threshold Configuration (English papers)](./resources/references/deai/tone-thresholds.yaml)
- [Claim-Evidence Contract](./resources/references/evidence/claim-evidence-contract.md)
- [Over-Claim Guard](./resources/references/evidence/over-claim-guard.md)
- [Number and Unit Formatting Guide](./resources/references/formatting/number-unit-guide.md)
- [Three-Line Table Guide](./resources/references/formatting/table-guide.md)
- [LaTeX Compilation Guide](./resources/references/latex/compilation.md)
- [Module: Abstract](./resources/references/modules/abstract.md)
- [Module: Adapt](./resources/references/modules/adapt.md)
- [Module: Bibliography](./resources/references/modules/bibliography.md)
- [Figure and Table Caption Generation Guide](./resources/references/modules/caption.md)
- [Module: Compile](./resources/references/modules/compile.md)
- [Module: De-AI Editing](./resources/references/modules/deai.md)
- [Module: Experiment Review](./resources/references/modules/experiment.md)
- [Module: Expression Restructuring](./resources/references/modules/expression.md)
- [Module: Format Check](./resources/references/modules/format.md)
- [Module: Grammar Analysis](./resources/references/modules/grammar.md)
- [Module: Literature Review Synthesis](./resources/references/modules/literature.md)
- [Module: Logical Coherence & Methodological Depth](./resources/references/modules/logic.md)
- [Module: Pseudocode Review](./resources/references/modules/pseudocode.md)
- [Routing Rules — Full Detail](./resources/references/modules/routing-rules.md)
- [Module: Section Writing](./resources/references/modules/section-writing.md)
- [Module: Long Sentence Analysis](./resources/references/modules/sentences.md)
- [Module: Tables](./resources/references/modules/tables.md)
- [Tense Guide](./resources/references/modules/tense-guide.md)
- [Module: Title Optimization](./resources/references/modules/title.md)
- [Module: Translation (Chinese -> English)](./resources/references/modules/translation.md)
- [Workflow & Best Practices](./resources/references/modules/workflow.md)
- [Reviewer Perspective Guide](./resources/references/review/reviewer-perspective.md)
- [LLM / AI-Assistance Disclosure Policies (2026-06)](./resources/references/venues/ai-disclosure.md)
- [Venue-Specific Requirements](./resources/references/venues/catalog.md)
- [Journal Adaptation Workflow](./resources/references/venues/journal-adaptation-workflow.md)
- [Abstract Structure Guide](./resources/references/writing/abstract-structure.md)
- [Best Practices](./resources/references/writing/best-practices.md)
- [Common Chinglish Errors in Academic Writing](./resources/references/writing/common-errors.md)
- [Abstract Section Writing](./resources/references/writing/section-writing/abstract.md)
- [Conclusion Section Writing](./resources/references/writing/section-writing/conclusion.md)
- [Experiments And Discussion Section Writing](./resources/references/writing/section-writing/experiments.md)
- [Paragraph Flow And Reverse Outline](./resources/references/writing/section-writing/flow.md)
- [Section-Writing Reference Index](./resources/references/writing/section-writing/index.md)
- [Introduction Section Writing](./resources/references/writing/section-writing/introduction.md)
- [Method Section Writing](./resources/references/writing/section-writing/method.md)
- [Related Work Section Writing](./resources/references/writing/section-writing/related-work.md)
- [Reviewer-Facing Self-Review](./resources/references/writing/section-writing/self-review.md)
- [Academic Writing Style Guide](./resources/references/writing/style-guide.md)
- [Academic Terminology Reference](./resources/references/writing/terminology.md)
- [Academic Translation Guide](./resources/references/writing/translation-guide.md)
- [Writing Philosophy for Academic Papers](./resources/references/writing/writing-philosophy.md)

### Templates

- [ACM Conferences (LaTeX)](./resources/templates/acm.md)
- [ICML (LaTeX)](./resources/templates/icml.md)
- [IEEE Conferences/Journals (LaTeX)](./resources/templates/ieee.md)
- [NeurIPS (LaTeX)](./resources/templates/neurips.md)
- [Springer (LNCS) (LaTeX)](./resources/templates/springer-lncs.md)

### Examples

- [Example: Compile And Bibliography](./resources/examples/compile-and-bibliography.md)
- [Example: Experiment Review](./resources/examples/experiment-review.md)
- [Example: Figures And Title](./resources/examples/figures-and-title.md)
- [Example: Grammar And Logic Review](./resources/examples/grammar-and-logic.md)
- [Literature Review Rewrite](./resources/examples/literature-review-rewrite.md)
- [Example: Multi-Module Sequence](./resources/examples/multi-module-sequence.md)
- [Example: Translation And De-AI](./resources/examples/translation-and-deai.md)

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

```text
Give me a reviewer-facing Introduction rewrite plan with paragraph roles and a claim-evidence map.
```

## Notes

- Run the smallest module that can answer the request before escalating to broader review.
- Preserve citations, labels, math, and source structure unless the user explicitly asks for edits.
- Use `paper-audit` after source-level compile and bibliography checks are stable when the goal is submission readiness.
