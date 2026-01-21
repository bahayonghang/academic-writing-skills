# Usage Guide

Comprehensive guide to using Academic Writing Skills.

## Overview

Academic Writing Skills provides two main skills:

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `latex-paper-en` | English academic papers | Compilation, format check, grammar, translation |
| `latex-thesis-zh` | Chinese theses | Compilation, GB/T 7714 check, template support |

## Modular Design

Each skill uses a modular design where you can use any module independently without following a sequence.
For Chinese theses, **structure mapping should run first** when doing a full review or handling multi-file projects.

## Output Protocol (All Modules)

All suggestions must use diff-comment style and include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 / P1 / P2

Minimal template:
```latex
% <MODULE> (Line <N>) [Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <Issue summary>
% Before: ...
% After:  ...
% Rationale: ...
% ⚠️ [PENDING VERIFICATION]: <if evidence/metric is required>
```

Short example:
```latex
% GRAMMAR (Line 23) [Severity: Major] [Priority: P1]: Article missing
% Before: We propose method for time series forecasting.
% After:  We propose a method for time series forecasting.
% Rationale: Missing indefinite article before singular count noun
```

### latex-paper-en Modules

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, build | LaTeX compilation |
| Format Check | format, chktex, lint | Format checking |
| Grammar Analysis | grammar, proofread | Grammar analysis |
| Sentence Decomposition | long sentence, simplify | Long sentence decomposition |
| Expression | academic tone, improve writing | Expression optimization |
| Translation | translate, 翻译, 中译英 | Chinese-English translation |
| Bibliography | bib, bibliography | Bibliography checking |

## Compile Module

### Available Tools

| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

### Compilation Recipes

| Recipe | Steps | Use Case |
|--------|-------|----------|
| XeLaTeX | xelatex | Unicode/Chinese support |
| PDFLaTeX | pdflatex | English-only, fastest |
| LaTeXmk | latexmk | Auto dependency handling |
| xelatex-bibtex | xelatex → bibtex → xelatex × 2 | Chinese + BibTeX |
| xelatex-biber | xelatex → biber → xelatex × 2 | Chinese + Biber |
| pdflatex-bibtex | pdflatex → bibtex → pdflatex × 2 | English + BibTeX |
| pdflatex-biber | pdflatex → biber → pdflatex × 2 | English + Biber |

### Usage Examples

```bash
# Auto-detect compiler
python scripts/compile.py main.tex

# Specify recipe
python scripts/compile.py main.tex --recipe xelatex-biber

# Specify output directory
python scripts/compile.py main.tex --recipe latexmk --outdir build

# Clean auxiliary files
python scripts/compile.py main.tex --clean
python scripts/compile.py main.tex --clean-all  # Including PDF
```

## Format Check Module

Uses ChkTeX for LaTeX code checking.

```bash
# Basic check
python scripts/check_format.py main.tex

# Strict mode
python scripts/check_format.py main.tex --strict
```

Output example:
```
============================================================
LaTeX Format Check Report
============================================================
File: main.tex
Status: WARNING
Message: Found 3 issues

[SPACING] (2 issues)
  Line 42: Interword spacing should perhaps be used.
  Line 87: Intersentence spacing should perhaps be used.

[PUNCTUATION] (1 issue)
  Line 120: Delete this space to maintain correct pagereferences.
============================================================
```

## Grammar Analysis Module

LLM-based grammar checking without external tools.

Focus areas:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency
- Chinglish detection

Output format:
```latex
% GRAMMAR (Line 23): Article missing
% Before: We propose method for time series forecasting.
% After: We propose a method for time series forecasting.
```

## Translation Module

Supports Chinese academic text to English translation.

### Supported Domains

| Domain | Keywords |
|--------|----------|
| Deep Learning | neural networks, attention, loss functions |
| Time Series | forecasting, ARIMA, sliding window |
| Industrial Control | PID control, fault detection, SCADA |

### Translation Workflow

1. **Terminology Confirmation** - Identify terms and confirm translations
2. **Structure Analysis** - Analyze paragraph structure, determine tense
3. **Sentence Translation** - Translation with annotations
4. **Chinglish Check** - Detect and fix common errors
5. **Academic Polish** - Final review

### Usage Example

```
User: Translate to academic English (Deep Learning):
本文提出了一种基于 Transformer 的时间序列预测方法。

Assistant:
## Terminology Confirmation
| 中文 | English |
|------|---------|
| 时间序列预测 | time series forecasting |
| 基于...的 | ...-based |

## Translation
We propose a Transformer-based approach for time series forecasting.
```

## Bibliography Module

Verifies BibTeX file integrity and format.

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --standard gb7714
```

## Best Practices

### 1. Choose the Right Recipe

```
English papers (no Chinese) → pdflatex or pdflatex-biber
Contains Chinese/Unicode → xelatex or xelatex-biber
Complex dependencies → latexmk
```

### 2. Check Format Frequently

```bash
python scripts/check_format.py paper.tex
python scripts/check_format.py paper.tex --strict  # Before submission
```

### 3. Confirm Terminology Before Translation

When translating specialized content, confirm key terms first.

### 4. Keep Bibliography Clean

Run bibliography verification regularly.

## Troubleshooting

### Compilation Fails

**Problem**: `! LaTeX Error: File 'xxx.sty' not found`

**Solution**:
```bash
tlmgr install <package>  # TeX Live
mpm --install=<package>  # MiKTeX
```

### Chinese Not Displaying

**Problem**: Chinese shows as boxes

**Solution**: Use XeLaTeX:
```bash
python scripts/compile.py main.tex --recipe xelatex
```

### Bibliography Empty

**Problem**: Bibliography section is empty

**Solution**: Use full recipe:
```bash
python scripts/compile.py main.tex --recipe xelatex-biber
```

## Next Steps

- [Compilation Recipes](/guides/compilation)
- [Format Checking](/guides/format-checking)
- [Bibliography Management](/guides/bibliography)
