# `latex-thesis-zh`

Chinese LaTeX degree-thesis assistant for existing `.tex` projects. It covers source-level
diagnosis, thesis argument and chapter structure, school-template constraints, and final-review
checks without silently changing citations, labels, mathematics, or template macros.

## Use It For

- Diagnose XeLaTeX, LuaLaTeX, latexmk, template, layout, formula, and GB/T 7714 issues.
- Map chapter structure and check terminology, abbreviations, references, tables, and headings.
- Review the introduction funnel, literature synthesis, method and process chapters, experiments,
  abstracts, conclusions, and cross-chapter closure.
- Reduce AI-writing traces while preserving academic claims and LaTeX syntax.
- Run school-specification and blind-review checks before submission.

## Do Not Use It For

- English conference or journal papers; use `latex-paper-en`.
- Typst projects; use `typst-paper`.
- PDF-only, multi-dimensional reviewer reports; use `paper-audit`.
- Pure literature discovery, DOCX-only work, or writing a thesis from scratch.

## Module Router

| Module | Use when | Primary command |
| --- | --- | --- |
| `compile` | The thesis build fails or the toolchain is unclear | `uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py main.tex` |
| `format` | Layout, formula wrapping, draft residue, or placeholder rows need checking | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_format.py main.tex` |
| `structure` | You need a chapter and section map | `uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py main.tex` |
| `consistency` | Terms, abbreviations, or names drift across chapters | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py main.tex --terms` |
| `template` | The thesis class or school template is unclear | `uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py main.tex` |
| `bibliography` | BibTeX data or GB/T 7714 compliance needs checking | `uv run python academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gb7714` |
| `title` | Thesis, chapter, or section titles need review | `uv run python academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py main.tex --check --headings` |
| `deai` | Visible Chinese prose contains AI-writing traces | `uv run python academic-writing-skills/latex-thesis-zh/scripts/deai_check.py main.tex --section introduction` |
| `logic` | The introduction funnel, chapter handoffs, mainline, or closure is weak | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py main.tex` |
| `literature` | The literature review lists papers without synthesis or a defensible gap | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py main.tex --section related` |
| `experiment` | Experiment language, evidence layers, or per-method-chapter completeness needs review | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py main.tex` |
| `references` | Cross-references, captions, labels, or numbering are inconsistent | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_references.py main.tex` |
| `tables` | Three-line tables, booktabs structure, or table generation needs checking | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_tables.py main.tex` |
| `abstract` | Abstract structure, length, or Chinese-English consistency needs diagnosis | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_abstract.py main.tex` |
| `conclusion` | The conclusion lacks summary, contributions, outlook, or numerical consistency | `uv run python academic-writing-skills/latex-thesis-zh/scripts/analyze_conclusion.py main.tex` |
| `spec-check` | A final thesis must be checked item by item against a school specification | `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_spec.py main.tex --template yanshan --degree doctor` |
| `blind-review` | Personal information must be detected or removed in a review copy | `uv run python academic-writing-skills/latex-thesis-zh/scripts/blind_review.py main.tex --check` |

## Minimum Inputs

- A thesis entry file such as `main.tex`; multi-file projects may use `\input` and `\include`.
- A bibliography path for bibliography checks.
- Optional chapter or section, school/template context, and degree type for targeted checks.
- For online bibliography verification, explicit permission to send citation metadata externally.

## First Commands

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/detect_template.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py main.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py main.tex
```

Run the smallest matching module. For multi-part requests, follow the order documented in
[routing rules](./resources/references/modules/routing-rules.md). Compilation must go through
`compile.py`; do not invoke TeX tools directly.

## Output Artifacts

- Source-located diagnostics in `% MODULE (L##) [Severity] [Priority]: ...` form.
- Exact commands, exit codes, and key stderr when a script fails.
- Structure maps, template signals, bibliography findings, and source-preserving rewrite proposals.
- Separate findings and proposed edits; no fabricated citations, data, claims, funds, or acknowledgments.
- Blind-review output only in `*_blind` copies, with the original source unchanged.

## Public Resources

### Module References

- [Routing rules](./resources/references/modules/routing-rules.md)
- [Compile](./resources/references/modules/compile.md)
- [Format](./resources/references/modules/format.md)
- [Structure and logic](./resources/references/modules/logic.md)
- [Consistency](./resources/references/modules/consistency.md)
- [Template detection](./resources/references/modules/template.md)
- [Bibliography](./resources/references/modules/bibliography.md)
- [Title](./resources/references/modules/title.md)
- [De-AI review](./resources/references/modules/deai.md)
- [Literature review](./resources/references/modules/literature.md)
- [Experiment review](./resources/references/modules/experiment.md)
- [Cross-references](./resources/references/modules/references.md)
- [Tables](./resources/references/modules/tables.md)
- [Abstract](./resources/references/modules/abstract.md)
- [Conclusion](./resources/references/modules/conclusion.md)
- [Specification check](./resources/references/modules/spec-check.md)
- [Blind review](./resources/references/modules/blind-review.md)

### Writing References

- [Writing philosophy](./resources/references/writing/writing-philosophy-zh.md)
- [Thesis writing guide](./resources/references/writing/thesis-writing-guide.md)
- [Introduction chapter guide](./resources/references/writing/introduction-guide-zh.md)
- [Process chapter guide](./resources/references/writing/process-chapter-guide-zh.md)
- [Method chapter guide](./resources/references/writing/method-chapter-guide-zh.md)
- [Conclusion chapter guide](./resources/references/writing/conclusion-guide-zh.md)
- [Abstract structure](./resources/references/writing/abstract-structure.md)
- [Structure guide](./resources/references/writing/structure-guide.md)
- [Logic and coherence](./resources/references/writing/logic-coherence.md)
- [Chinese academic style](./resources/references/writing/academic-style-zh.md)
- [Title optimization](./resources/references/writing/title-optimization.md)
- [English abstract tense guide](./resources/references/writing/tense-guide-zh.md)
- [Over-claim guard](./resources/references/writing/over-claim-guard.md)

### Formatting, Citations, And De-AI References

- [GB/T 7714](./resources/references/citations/gb-standard.md)
- [Compilation strategy](./resources/references/latex/compilation.md)
- [Caption guide](./resources/references/formatting/caption-guide.md)
- [Formula guide](./resources/references/formatting/formula-guide.md)
- [Table guide](./resources/references/formatting/table-guide.md)
- [De-AI guide](./resources/references/deai/guide.md)
- [Forbidden terms](./resources/references/deai/forbidden-terms.md)
- [Chinese tone terms](./resources/references/deai/tone-terms-zh.md)
- [Tone thresholds](./resources/references/deai/tone-thresholds.yaml)

### Templates

- [Generic Chinese thesis](./resources/templates/generic.md)
- [Tsinghua thuthesis](./resources/templates/thuthesis.md)
- [Peking University pkuthss](./resources/templates/pkuthss.md)
- [Yanshan University 2024 specification](./resources/templates/yanshan.md)

### Examples

- [Compile and template](./resources/examples/compile-and-template.md)
- [Structure and consistency](./resources/examples/structure-and-consistency.md)
- [Logic and experiment](./resources/examples/logic-and-experiment.md)
- [Literature-review rewrite](./resources/examples/literature-review-rewrite.md)
- [Bibliography and de-AI](./resources/examples/bibliography-and-deai.md)

## Common Requests And Handoffs

Use this skill for source-level thesis work: template detection, controlled compilation, chapter
diagnosis, writing review, specification checks, and blind-review copies. Hand off English papers to
`latex-paper-en`, Typst sources to `typst-paper`, local bibliography discovery to
`bib-search-citation`, and final multi-dimensional reviewer reports to `paper-audit`.
