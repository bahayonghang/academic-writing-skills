---
name: typst-paper
description: Typst academic paper assistant for existing `.typ` paper projects in English or Chinese. Use this skill whenever the user wants to compile, audit, or improve a Typst paper, including format checks, bibliography validation for BibTeX or Hayagriva, grammar/sentence/logic review, expression polishing, translation, title optimization, de-AI editing, or experiment-section review. Trigger even when the user only mentions one Typst file, one bibliography issue, or one section rewrite.
metadata:
  category: academic-writing
  tags: [typst, paper, chinese, english, ieee, acm, springer, neurips, compilation, grammar, bibliography, hayagriva]
argument-hint: "[main.typ] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Bash(typst *)
---

# Typst Academic Paper Assistant

Use this skill for targeted work on an existing Typst paper project. Route requests to the smallest useful module and keep outputs compatible with Typst source review.

## Capability Summary

- Compile Typst projects and diagnose Typst CLI issues.
- Audit format, bibliography, grammar, sentence length, argument logic, expression quality, and AI traces.
- Support both BibTeX and Hayagriva bibliography files.
- Improve titles, translation, and experiment-section clarity for Typst papers.

## Triggering

Use this skill when the user has an existing `.typ` paper project and wants help with:

- Typst compilation or export issues
- format or venue compliance
- bibliography validation for BibTeX or Hayagriva
- grammar, sentence, logic, or expression review
- translation or bilingual polishing
- title optimization
- de-AI editing
- experiment-section review

## Do Not Use

Do not use this skill for:

- LaTeX-first conference or thesis projects
- DOCX/PDF-only editing without Typst source
- thesis template detection or GB/T 7714 thesis workflows
- from-scratch paper planning or literature research

## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `compile` | Typst build, export, font, or watch issues | `uv run python $SKILL_DIR/scripts/compile.py main.typ` | `references/modules/COMPILE.md` |
| `format` | Venue/layout review for a Typst paper | `uv run python $SKILL_DIR/scripts/check_format.py main.typ` | `references/modules/FORMAT.md` |
| `bibliography` | BibTeX or Hayagriva validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --typ main.typ` | `references/modules/BIBLIOGRAPHY.md` |
| `grammar` | Grammar cleanup on Typst prose | `uv run python $SKILL_DIR/scripts/analyze_grammar.py main.typ --section introduction` | `references/modules/GRAMMAR.md` |
| `sentences` | Long or dense sentence diagnostics | `uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --section introduction` | `references/modules/SENTENCES.md` |
| `logic` | Argument flow and coherence review | `uv run python $SKILL_DIR/scripts/analyze_logic.py main.typ --section methods` | `references/modules/LOGIC.md` |
| `expression` | Tone and expression polishing | `uv run python $SKILL_DIR/scripts/improve_expression.py main.typ --section methods` | `references/modules/EXPRESSION.md` |
| `translation` | Chinese/English academic translation in Typst context | `uv run python $SKILL_DIR/scripts/translate_academic.py input_zh.txt --domain deep-learning` | `references/modules/TRANSLATION.md` |
| `title` | Generate, compare, or optimize Typst paper titles | `uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --check` | `references/modules/TITLE.md` |
| `deai` | Reduce AI-writing traces while preserving Typst syntax | `uv run python $SKILL_DIR/scripts/deai_check.py main.typ --section introduction` | `references/modules/DEAI.md` |
| `experiment` | Inspect experiment-section clarity and reporting quality | `uv run python $SKILL_DIR/scripts/analyze_experiment.py main.typ --section experiment` | `references/modules/EXPERIMENT.md` |

## Required Inputs

- `main.typ` or the Typst entry file.
- Optional `--section SECTION` for targeted analysis.
- Optional bibliography path when the request targets references.
- Optional venue context when the user cares about IEEE, ACM, Springer, or similar expectations.

If arguments are missing, ask only for the Typst entry file and the target module.

## Output Contract

- Return findings in Typst diff-comment style whenever possible: `// MODULE (Line N) [Severity] [Priority]: Issue ...`
- Report the exact command used and the exit code when a script fails.
- Preserve `@cite`, `<label>`, math blocks, and Typst macros unless the user explicitly asks for source edits.

## Workflow

1. Parse `$ARGUMENTS` and select the active module.
2. Read only the reference file needed for that module.
3. Run the module script with `uv run python ...`.
4. Return Typst-ready comments and next actions.
5. For bibliography requests, decide BibTeX vs Hayagriva first, then run `bibliography`.

## Safety Boundaries

- Never invent citations, labels, or experimental claims.
- Never rewrite Typst references, labels, or math content by default.
- Keep compile diagnostics separate from prose rewrites so the user can validate each step.

## Reference Map

- `references/TYPST_SYNTAX.md`: Typst syntax reminders and pitfalls.
- `references/STYLE_GUIDE.md`: paper-writing style baseline.
- `references/CITATION_VERIFICATION.md`: citation verification workflow.
- `references/modules/`: module-specific Typst commands and choices.

Read only the file that matches the active module.

## Example Requests

- “Compile this Typst paper and tell me why the export works locally but fails in CI.”
- “Check bibliography, title, and abstract wording in my `main.typ` submission.”
- “Review the methods section for sentence length and logic, but keep Typst labels intact.”

See `examples/` for full request-to-command walkthroughs.
