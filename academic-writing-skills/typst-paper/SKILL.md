---
name: typst-paper
version: 1.2.0
category: academic-writing
tags:
  - typst
  - paper
  - chinese
  - english
  - ieee
  - acm
  - springer
  - neurips
  - deep-learning
  - compilation
  - grammar
  - bibliography
description: |
  Typst academic paper assistant (Chinese & English papers, conference/journal submissions).
  Use when writing, reviewing, compiling, or improving Typst academic papers.
  Use when user mentions typst compile, grammar, bibliography, deai, translate, title, logic,
  reviewer perspective, or any Typst paper quality improvement task.
  Domains: Deep Learning, Time Series, Industrial Control, Computer Science.
argument-hint: "[main.typ] [--section <section>] [--module <module>]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(typst *)
references:
  - resources/references/STYLE_GUIDE.md
  - resources/references/COMMON_ERRORS.md
  - resources/references/VENUES.md
  - resources/references/TERMINOLOGY.md
  - resources/references/TRANSLATION_GUIDE.md
  - resources/references/DEAI_GUIDE.md
  - resources/references/WRITING_PHILOSOPHY.md
  - resources/references/REVIEWER_PERSPECTIVE.md
  - resources/references/CITATION_VERIFICATION.md
  - resources/references/TYPST_SYNTAX.md
  - resources/references/BEST_PRACTICES.md
scripts:
  - scripts/compile.py
  - scripts/check_format.py
  - scripts/verify_bib.py
  - scripts/analyze_grammar.py
  - scripts/analyze_sentences.py
  - scripts/analyze_logic.py
  - scripts/improve_expression.py
  - scripts/translate_academic.py
  - scripts/optimize_title.py
  - scripts/deai_check.py
  - scripts/deai_batch.py
  - scripts/parsers.py
---

# Typst Academic Paper Assistant

## Critical Rules

1. NEVER modify `@cite`, `@ref`, `@label`, math environments (`$...$`)
2. NEVER fabricate bibliography entries
3. NEVER change domain terminology without confirmation
4. ALWAYS output suggestions in diff-comment format first

## Argument Conventions ($ARGUMENTS)

- Use `$ARGUMENTS` to capture user-provided inputs (main `.typ` path, target section, module choice).
- If `$ARGUMENTS` is missing or ambiguous, ask for: main `.typ` path, target scope, and desired module.
- Treat file paths as literal; do not guess missing paths.

## Execution Guardrails

- Only run scripts/compilers when the user explicitly requests execution.
- For destructive operations, ask for confirmation before running.

## Unified Output Protocol (All Modules)

Each suggestion MUST include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 (blocking) / P1 (important) / P2 (nice-to-have)

**Default comment template** (diff-comment style):
```typst
// <MODULE> (Line <N>) [Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <Issue summary>
// Original: ...
// Revised:  ...
// Rationale: ...
// ⚠️ [PENDING VERIFICATION]: <if evidence/metric is required>
```

## Failure Handling (Global)

If a tool/script cannot run, respond with a comment block including the reason and a safe next step:
```typst
// ERROR [Severity: Critical] [Priority: P0]: <short error>
// Cause: <missing file/tool or invalid path>
// Action: <install tool / verify file path / re-run command>
```
Common cases:
- **Script not found**: confirm `scripts/` path and working directory
- **Typst not installed**: suggest installing via `cargo install typst-cli` or package manager
- **File not found**: ask user to provide the correct `.typ` path
- **Compilation failed**: summarize the first error from Typst output

## Modules (Independent, Pick Any)

| Module | Trigger Keywords | Script | Details |
|--------|-----------------|--------|---------|
| Compile | compile, 编译, build, typst compile | `typst compile main.typ` | [COMPILE.md](resources/modules/COMPILE.md) |
| Format Check | format, lint, 格式检查 | `python scripts/check_format.py main.typ` | [FORMAT.md](resources/modules/FORMAT.md) |
| Grammar | grammar, 语法, proofread | `python scripts/analyze_grammar.py main.typ` | [GRAMMAR.md](resources/modules/GRAMMAR.md) |
| Sentences | long sentence, 长句 | `python scripts/analyze_sentences.py main.typ` | [SENTENCES.md](resources/modules/SENTENCES.md) |
| Expression | academic tone, 学术表达 | `python scripts/improve_expression.py main.typ` | [EXPRESSION.md](resources/modules/EXPRESSION.md) |
| Logic | logic, coherence, methodology | `python scripts/analyze_logic.py main.typ` | [LOGIC.md](resources/modules/LOGIC.md) |
| Translation | translate, 翻译, 中译英 | `python scripts/translate_academic.py "text"` | [TRANSLATION.md](resources/modules/TRANSLATION.md) |
| Bibliography | bib, bibliography, 参考文献 | `python scripts/verify_bib.py refs.bib` | [BIBLIOGRAPHY.md](resources/modules/BIBLIOGRAPHY.md) |
| De-AI | deai, 去AI化, humanize | `python scripts/deai_check.py main.typ` | [DEAI.md](resources/modules/DEAI.md) |
| Title | title, 标题 | `python scripts/optimize_title.py main.typ` | [TITLE.md](resources/modules/TITLE.md) |
| Reviewer | reviewer, 审稿, checklist | — | [REVIEWER_PERSPECTIVE.md](resources/references/REVIEWER_PERSPECTIVE.md) |
| Workflow | workflow, full review | — | [WORKFLOW.md](resources/modules/WORKFLOW.md) |

## Best Practices & Typst Specifics
Load additional context from:
- [VENUES.md](resources/references/VENUES.md): Specific rules for IEEE, ACM, Springer, NeurIPS, ICML
- [TYPST_SYNTAX.md](resources/references/TYPST_SYNTAX.md): Typst syntax advantages and specific rules vs LaTeX
- [BEST_PRACTICES.md](resources/references/BEST_PRACTICES.md): General workflow recommendations

## References

- [STYLE_GUIDE.md](resources/references/STYLE_GUIDE.md): Academic writing rules
- [COMMON_ERRORS.md](resources/references/COMMON_ERRORS.md): Chinglish patterns
- [VENUES.md](resources/references/VENUES.md): Conference/journal requirements
- [TERMINOLOGY.md](resources/references/TERMINOLOGY.md): Domain terminology (DL/TS/IC)
- [TRANSLATION_GUIDE.md](resources/references/TRANSLATION_GUIDE.md): Translation guide
- [DEAI_GUIDE.md](resources/references/DEAI_GUIDE.md): De-AI writing guide and patterns
- [WRITING_PHILOSOPHY.md](resources/references/WRITING_PHILOSOPHY.md): Writing philosophy
- [REVIEWER_PERSPECTIVE.md](resources/references/REVIEWER_PERSPECTIVE.md): Reviewer checklist
- [CITATION_VERIFICATION.md](resources/references/CITATION_VERIFICATION.md): Citation verification
- [TYPST_SYNTAX.md](resources/references/TYPST_SYNTAX.md): Typst notes and syntax advantages
