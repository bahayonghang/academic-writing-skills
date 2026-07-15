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
| `pseudocode` | `algorithmic`, `algorithm-figure`, or `lovelace` review, including caption and wrapper checks | `uv run python academic-writing-skills/typst-paper/scripts/check_pseudocode.py main.typ --venue ieee` |
| `deai` | English or Chinese AI-trace checks | `uv run python academic-writing-skills/typst-paper/scripts/deai_check.py main.typ --section introduction` |
| `experiment` | Experiment write-up and discussion layering | `uv run python academic-writing-skills/typst-paper/scripts/analyze_experiment.py main.typ --section experiment` |
| `abstract` | Five-element abstract diagnosis | `uv run python academic-writing-skills/typst-paper/scripts/analyze_abstract.py main.typ` |
| `tables` | Table structure and three-line checks | `uv run python academic-writing-skills/typst-paper/scripts/check_tables.py main.typ` |
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

## Public Resources

### References

- [Abstract Structure Guide](./resources/references/ABSTRACT_STRUCTURE.md)
- [AI Tone Terms (Bilingual, Typst) — Reference](./resources/references/AI_TONE_TERMS.md)
- [AI Tone Threshold Configuration (Typst, bilingual)](./resources/references/AI_TONE_THRESHOLDS.yaml)
- [Best Practices](./resources/references/BEST_PRACTICES.md)
- [Citation Style Guide](./resources/references/CITATION_STYLES.md)
- [Citation Verification Guide](./resources/references/CITATION_VERIFICATION.md)
- [Common Chinglish Errors in Academic Writing](./resources/references/COMMON_ERRORS.md)
- [De-AI Writing Guide for Typst Academic Papers](./resources/references/DEAI_GUIDE.md)
- [Journal Name Abbreviations](./resources/references/JOURNAL_ABBREVIATIONS.md)
- [Journal Adaptation Workflow](./resources/references/JOURNAL_ADAPTATION_WORKFLOW.md)
- [Module: Abstract](./resources/references/modules/ABSTRACT.md)
- [Module: Adapt](./resources/references/modules/ADAPT.md)
- [Module: Bibliography](./resources/references/modules/BIBLIOGRAPHY.md)
- [Figure and Table Caption Generation Guide (Typst)](./resources/references/modules/CAPTION.md)
- [module:compile](./resources/references/modules/COMPILE.md)
- [Module: De-AI editing](./resources/references/modules/DEAI.md)
- [Role](./resources/references/modules/EXPERIMENT.md)
- [Module: Academic Expression](./resources/references/modules/EXPRESSION.md)
- [Module: Format Check](./resources/references/modules/FORMAT.md)
- [Module: Syntax Analysis (English)](./resources/references/modules/GRAMMAR.md)
- [Module: Literature Review Synthesis](./resources/references/modules/LITERATURE.md)
- [Module: Logical connection and methodological depth](./resources/references/modules/LOGIC.md)
- [Module: Pseudocode Review](./resources/references/modules/PSEUDOCODE.md)
- [Module: References](./resources/references/modules/REFERENCES.md)
- [Module: Analysis of long and difficult sentences](./resources/references/modules/SENTENCES.md)
- [Module: Tables](./resources/references/modules/TABLES.md)
- [Module: Title Optimization](./resources/references/modules/TITLE.md)
- [Module: Translation (Chinese to English)](./resources/references/modules/TRANSLATION.md)
- [Workflow & Best Practices](./resources/references/modules/WORKFLOW.md)
- [Number and Unit Formatting Guide](./resources/references/NUMBER_UNIT_GUIDE.md)
- [Over-Claim Guard](./resources/references/OVER_CLAIM_GUARD.md)
- [Reviewer Perspective Guide](./resources/references/REVIEWER_PERSPECTIVE.md)
- [Routing, Workflow, and Safety Notes (typst-paper)](./resources/references/skill-routing-notes.md)
- [Academic Writing Style Guide (Typst)](./resources/references/STYLE_GUIDE.md)
- [Three-Line Table Guide (Typst)](./resources/references/TABLE_GUIDE.md)
- [Typst Academic Template Example](./resources/references/TEMPLATES.md)
- [Tense Guide](./resources/references/TENSE_GUIDE.md)
- [Academic Terminology Reference](./resources/references/TERMINOLOGY.md)
- [Academic Translation Guide](./resources/references/TRANSLATION_GUIDE.md)
- [Typst Syntax Reference for Academic Writing](./resources/references/TYPST_SYNTAX.md)
- [Venue-Specific Requirements for Typst Papers](./resources/references/VENUES.md)
- [Writing Philosophy for Academic Papers](./resources/references/WRITING_PHILOSOPHY.md)

### Templates

- [ACM Conferences and Journals (Typst)](./resources/templates/acm.md)
- [IEEE Conferences and Journals (Typst)](./resources/templates/ieee.md)
- [NeurIPS / ICML / ICLR (Typst)](./resources/templates/neurips.md)

### Examples

- [Example: Bibliography And Pseudocode](./resources/examples/bibliography-and-pseudocode.md)
- [Example: Bibliography And Title](./resources/examples/bibliography-and-title.md)
- [Example: Compile And Format](./resources/examples/compile-and-format.md)
- [Example: Expression And Translation](./resources/examples/expression-and-translation.md)
- [Literature Review Rewrite](./resources/examples/literature-review-rewrite.md)

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
