---
name: latex-paper-en
description: |
  LaTeX academic paper assistant for English conference/journal papers.
  Provides: format checking (chktex), compilation (pdflatex/xelatex/lualatex via latexmk),
  grammar analysis, complex sentence decomposition, and expression restructuring.

  Use when:
  - Working with .tex files for English academic papers
  - User mentions "paper review", "grammar check", "improve writing", "proofread"
  - User asks to compile LaTeX documents
  - User mentions venues like IEEE, ACM, Springer, NeurIPS, ICML
  - User needs help with academic English writing style
  - User wants to check BibTeX/bibliography formatting
---

# LaTeX Academic Paper Assistant (English)

## Critical Rules

**NEVER violate these rules:**
1. NEVER modify content inside `\cite{}`, `\ref{}`, `\label{}`, `\equation`, `\align`, or math environments
2. NEVER fabricate bibliography entries - only read from existing .bib files
3. NEVER change domain-specific terminology without permission (see [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md))
4. NEVER apply changes directly - always output in diff-comment format first
5. ALWAYS run format check before analyzing text content

## Quick Start

### Compile Document
```bash
# Auto-detect and compile (recommended)
python scripts/compile.py main.tex

# Explicit compiler selection
python scripts/compile.py main.tex --compiler pdflatex
python scripts/compile.py main.tex --compiler xelatex
python scripts/compile.py main.tex --compiler lualatex

# Using recipes (VS Code LaTeX Workshop style)
python scripts/compile.py main.tex --recipe pdflatex          # PDFLaTeX only
python scripts/compile.py main.tex --recipe xelatex           # XeLaTeX only
python scripts/compile.py main.tex --recipe latexmk           # LaTeXmk auto
python scripts/compile.py main.tex --recipe pdflatex-bibtex   # pdflatex -> bibtex -> pdflatex*2
python scripts/compile.py main.tex --recipe pdflatex-biber    # pdflatex -> biber -> pdflatex*2
python scripts/compile.py main.tex --recipe xelatex-bibtex    # xelatex -> bibtex -> xelatex*2
python scripts/compile.py main.tex --recipe xelatex-biber     # xelatex -> biber -> xelatex*2

# Continuous compilation (watch mode)
python scripts/compile.py main.tex --watch

# Clean auxiliary files
python scripts/compile.py main.tex --clean
```

### Format Check
```bash
# Run chktex linting
python scripts/check_format.py main.tex

# Check with specific rules
python scripts/check_format.py main.tex --strict
```

## Workflow (4-Layer Approach)

### Layer 0: Pre-flight Check (MANDATORY)
1. Run `python scripts/check_format.py main.tex` for LaTeX linting
2. Run `python scripts/verify_bib.py references.bib` for BibTeX integrity
3. Map file structure if multi-file project

**Output**: Format health report (PASS/WARN/FAIL)

### Layer 1: Grammar & Style Analysis (Read-Only)
Focus areas:
- Subject-verb agreement, article usage (a/an/the)
- Tense consistency (past for methods, present for results)
- Chinglish detection (see [COMMON_ERRORS.md](references/COMMON_ERRORS.md))
- Weak verb replacement: make→construct, do→perform, get→obtain

### Layer 2: Complex Sentence Decomposition
**Trigger**: Sentences >50 words or >3 subordinate clauses

Output analysis format:
```latex
% LONG SENTENCE DETECTED (Line 45, 67 words)
% Core Clause: [main subject + verb + object]
% Subordinate Structure:
% - [Relative] which...
% - [Purpose] to...
% Suggested Rewrite: [simplified version]
```

### Layer 3: Expression Restructuring
Output as LaTeX-safe diff:
```latex
% SUGGESTION (Line 23): Improve academic tone
% Before: We use machine learning to get better results.
% After: We employ machine learning techniques to achieve superior performance.
% Changes: "use"→"employ", "get"→"achieve", "better results"→"superior performance"
```

## Output Report Structure

```markdown
# LaTeX Paper Review Report

## Executive Summary
- Status: READY / NEEDS REVISION / MAJOR ISSUES
- Compilation: [status]
- Grammar Issues: X found
- Long Sentences: Y found

## Critical Issues (Must Fix)
[Format/compilation errors]

## Grammar & Style Improvements
[Categorized by severity]

## Long Sentence Analysis
[Each with decomposition]

## Expression Refinements
[With rationale]
```

## Venue-Specific Rules

Load venue rules from [VENUES.md](references/VENUES.md):
- **IEEE**: Active voice for contributions, past tense for methods
- **ACM**: Present tense for general truths, structured abstract
- **Springer**: Figure captions below, table captions above
- **NeurIPS/ICML**: Concise (8 pages), specific formatting

## References

- [STYLE_GUIDE.md](references/STYLE_GUIDE.md): Academic writing style rules
- [COMMON_ERRORS.md](references/COMMON_ERRORS.md): Chinglish and common mistakes
- [VENUES.md](references/VENUES.md): Conference/journal requirements
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): Protected terminology
- [COMPILATION.md](references/COMPILATION.md): Detailed compilation guide
