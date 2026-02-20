---
name: latex-paper-en
version: 1.2.0
category: academic-writing
tags:
  - latex
  - paper
  - english
  - ieee
  - acm
  - springer
  - neurips
  - icml
  - deep-learning
  - compilation
  - grammar
  - bibliography
description: |
  LaTeX academic paper assistant for English papers (IEEE, ACM, Springer, NeurIPS, ICML).
  Use when writing, reviewing, compiling, or improving English LaTeX academic papers.
  Use when user mentions compile, grammar, bibliography, deai, translate, title, logic,
  reviewer perspective, or any LaTeX paper quality improvement task.
  Domains: Deep Learning, Time Series, Industrial Control.
argument-hint: "[main.tex] [--section <section>] [--module <module>]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(pdflatex *), Bash(xelatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *), Bash(chktex *)
references:
  - resources/references/STYLE_GUIDE.md
  - resources/references/COMMON_ERRORS.md
  - resources/references/VENUES.md
  - resources/references/FORBIDDEN_TERMS.md
  - resources/references/TERMINOLOGY.md
  - resources/references/TRANSLATION_GUIDE.md
  - resources/references/DEAI_GUIDE.md
  - resources/references/WRITING_PHILOSOPHY.md
  - resources/references/REVIEWER_PERSPECTIVE.md
  - resources/references/CITATION_VERIFICATION.md
  - resources/references/COMPILATION.md
  - resources/references/BEST_PRACTICES.md
scripts:
  - scripts/compile.py
  - scripts/check_format.py
  - scripts/check_figures.py
  - scripts/verify_bib.py
  - scripts/analyze_grammar.py
  - scripts/analyze_sentences.py
  - scripts/analyze_logic.py
  - scripts/improve_expression.py
  - scripts/translate_academic.py
  - scripts/optimize_title.py
  - scripts/deai_check.py
  - scripts/deai_batch.py
  - scripts/extract_prose.py
  - scripts/parsers.py
---

# LaTeX Academic Paper Assistant (English)

## Critical Rules

1. NEVER modify `\cite{}`, `\ref{}`, `\label{}`, math environments
2. NEVER fabricate bibliography entries
3. NEVER change domain terminology without confirmation
4. ALWAYS output suggestions in diff-comment format first

## Argument Conventions ($ARGUMENTS)

- Use `$ARGUMENTS` to capture user-provided inputs (main `.tex` path, target section, module choice).
- If `$ARGUMENTS` is missing or ambiguous, ask for: main `.tex` path, target scope, and desired module.
- Treat file paths as literal; do not guess missing paths.

## Execution Guardrails

- Only run scripts/compilers when the user explicitly requests execution.
- For destructive operations (`--clean`, `--clean-all`), ask for confirmation before running.

## Unified Output Protocol (All Modules)

Each suggestion MUST include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 (blocking) / P1 (important) / P2 (nice-to-have)

**Default comment template** (diff-comment style):
```latex
% <MODULE> (Line <N>) [Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <Issue summary>
% Original: ...
% Revised:  ...
% Rationale: ...
% ⚠️ [PENDING VERIFICATION]: <if evidence/metric is required>
```

## Failure Handling (Global)

If a tool/script cannot run, respond with a comment block including the reason and a safe next step:
```latex
% ERROR [Severity: Critical] [Priority: P0]: <short error>
% Cause: <missing file/tool or invalid path>
% Action: <install tool / verify file path / re-run command>
```
Common cases:
- **Script not found**: confirm `scripts/` path and working directory
- **LaTeX tool missing**: suggest installing TeX Live/MiKTeX or adding to PATH
- **File not found**: ask user to provide the correct `.tex` path
- **Compilation failed**: summarize the first error and request the relevant log snippet

## Modules (Independent, Pick Any)

| Module | Trigger Keywords | Script | Details |
|--------|-----------------|--------|---------|
| Compile | compile, 编译, build | `python scripts/compile.py main.tex` | [COMPILE.md](resources/modules/COMPILE.md) |
| Format Check | format, chktex, lint | `python scripts/check_format.py main.tex` | [FORMAT.md](resources/modules/FORMAT.md) |
| Grammar | grammar, 语法, proofread | `python scripts/analyze_grammar.py main.tex` | [GRAMMAR.md](resources/modules/GRAMMAR.md) |
| Sentences | long sentence, 长句 | `python scripts/analyze_sentences.py main.tex` | [SENTENCES.md](resources/modules/SENTENCES.md) |
| Expression | academic tone, 学术表达 | `python scripts/improve_expression.py main.tex` | [EXPRESSION.md](resources/modules/EXPRESSION.md) |
| Logic | logic, coherence, methodology | `python scripts/analyze_logic.py main.tex` | [LOGIC.md](resources/modules/LOGIC.md) |
| Translation | translate, 翻译, 中译英 | `python scripts/translate_academic.py "text"` | [TRANSLATION.md](resources/modules/TRANSLATION.md) |
| Bibliography | bib, bibliography | `python scripts/verify_bib.py refs.bib` | [BIBLIOGRAPHY.md](resources/modules/BIBLIOGRAPHY.md) |
| De-AI | deai, 去AI化, humanize | `python scripts/deai_check.py main.tex` | [DEAI.md](resources/modules/DEAI.md) |
| Title | title, 标题 | `python scripts/optimize_title.py main.tex` | [TITLE.md](resources/modules/TITLE.md) |
| Reviewer | reviewer, 审稿, checklist | — | [REVIEWER_PERSPECTIVE.md](resources/references/REVIEWER_PERSPECTIVE.md) |
| Workflow | workflow, full review | — | [WORKFLOW.md](resources/modules/WORKFLOW.md) |

## Best Practices & Venue Rules
Load additional context from:
- [VENUES.md](resources/references/VENUES.md): Specific rules for IEEE, ACM, Springer, NeurIPS, ICML
- [BEST_PRACTICES.md](resources/references/BEST_PRACTICES.md): General workflow recommendations

## References

- [STYLE_GUIDE.md](resources/references/STYLE_GUIDE.md): Academic writing rules
- [COMMON_ERRORS.md](resources/references/COMMON_ERRORS.md): Chinglish patterns
- [VENUES.md](resources/references/VENUES.md): Conference/journal requirements
- [FORBIDDEN_TERMS.md](resources/references/FORBIDDEN_TERMS.md): Protected terminology
- [TERMINOLOGY.md](resources/references/TERMINOLOGY.md): Domain terminology (DL/TS/IC)
- [TRANSLATION_GUIDE.md](resources/references/TRANSLATION_GUIDE.md): Translation guide
- [DEAI_GUIDE.md](resources/references/DEAI_GUIDE.md): De-AI writing guide and patterns
- [WRITING_PHILOSOPHY.md](resources/references/WRITING_PHILOSOPHY.md): Writing philosophy
- [REVIEWER_PERSPECTIVE.md](resources/references/REVIEWER_PERSPECTIVE.md): Reviewer checklist
- [CITATION_VERIFICATION.md](resources/references/CITATION_VERIFICATION.md): Citation verification
- [COMPILATION.md](resources/references/COMPILATION.md): Compilation recipes
