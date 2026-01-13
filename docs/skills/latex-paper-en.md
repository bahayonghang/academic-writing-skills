# English Papers (latex-paper-en)

Complete toolkit for English academic paper writing with LaTeX.

## Overview

The `latex-paper-en` skill provides comprehensive support for writing English academic papers in LaTeX, with a focus on major publication venues (IEEE, ACM, Springer, NeurIPS, etc.).

### Key Features

- **Multiple compilation recipes** (pdflatex, xelatex, latexmk, with bibliography workflows)
- **ChkTeX integration** for LaTeX linting
- **Format checking** with venue-specific rules (IEEE, ACM, Springer)
- **Bibliography verification** (BibTeX format validation)
- **Prose extraction** for grammar checking
- **Style guide references** (Common Chinglish errors, academic writing best practices)
- **Chinese-to-English academic translation** (Deep Learning, Time Series, Industrial Control domains)

## Environment Requirements

> **Note**: This skill assumes LaTeX environment is already configured on your system.

**Windows**: MiKTeX or TeX Live installed and added to PATH
**macOS/Linux**: TeX Live installed

Required tools: `pdflatex`, `xelatex`, `latexmk`, `biber`, `chktex`

## Modular Design

The skill uses a modular design where each module can be invoked independently:

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

### Tools (matching VS Code LaTeX Workshop)

| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=%OUTDIR%` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

### Recipes

| Recipe | Steps |
|--------|-------|
| XeLaTeX | xelatex |
| PDFLaTeX | pdflatex |
| LaTeXmk | latexmk |
| xelatex -> bibtex -> xelatex*2 | xelatex → bibtex → xelatex → xelatex |
| xelatex -> biber -> xelatex*2 | xelatex → biber → xelatex → xelatex |
| pdflatex -> bibtex -> pdflatex*2 | pdflatex → bibtex → pdflatex → pdflatex |
| pdflatex -> biber -> pdflatex*2 | pdflatex → biber → pdflatex → pdflatex |

### Usage

```bash
# Single compiler
python scripts/compile.py main.tex                          # Auto-detect
python scripts/compile.py main.tex --recipe xelatex         # XeLaTeX only
python scripts/compile.py main.tex --recipe pdflatex        # PDFLaTeX only

# With bibliography (recommended for papers)
python scripts/compile.py main.tex --recipe xelatex-bibtex  # BibTeX workflow
python scripts/compile.py main.tex --recipe xelatex-biber   # Biber workflow

# With output directory
python scripts/compile.py main.tex --recipe latexmk --outdir build

# Utilities
python scripts/compile.py main.tex --clean                  # Clean aux files
python scripts/compile.py main.tex --clean-all              # Clean all (incl. PDF)
```

## Format Check Module

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

## Grammar Analysis Module

LLM-based grammar checking focusing on:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency
- Chinglish detection

## Translation Module (Chinese → English)

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

### Usage Examples

**Basic Translation Request**:
```
Translate the following to academic English (Deep Learning domain):
本文提出了一种基于Transformer的时间序列预测方法...
```

**With Venue Specification**:
```
Translate the following for IEEE Transactions format:
实验结果表明，我们的方法在多个数据集上取得了最优性能...
```

## Bibliography Module

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
```

## Reference Files

- `references/TERMINOLOGY.md`: Domain terminology (Deep Learning, Time Series, Industrial Control)
- `references/TRANSLATION_GUIDE.md`: Translation principles, Chinglish corrections
- `references/STYLE_GUIDE.md`: Academic writing rules
- `references/COMMON_ERRORS.md`: Common mistakes
- `references/VENUES.md`: Conference/journal requirements

## Next Steps

- [Compilation Recipes Guide](/guides/compilation)
- [Format Checking Guide](/guides/format-checking)
- [Bibliography Guide](/guides/bibliography)
