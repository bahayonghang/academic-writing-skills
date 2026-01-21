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
- **De-AI writing analysis** for reducing AI-generated text traces

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
| De-AI Polishing | deai, 去AI化, humanize | Reduce AI writing traces |

## Output Protocol

All suggestions must use a diff-comment style and include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 / P1 / P2

Minimal template:
```latex
% <MODULE> (Line <N>) [Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <Issue>
% Before: ...
% After:  ...
% Rationale: ...
% ⚠️ [PENDING VERIFICATION]: <if evidence/metric is required>
```

If a tool fails (missing script/tool or invalid path), respond with an error comment and a safe next step.

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

### Failure Handling

- Missing LaTeX tools: install TeX Live/MiKTeX and ensure PATH is set
- Missing file/script: verify working directory and `scripts/` path
- Compilation error: summarize the first error and request the relevant log snippet

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

## De-AI Polishing Module

Reduce AI-generated writing traces while preserving LaTeX syntax and technical accuracy.

### Features

- **AI trace detection** with pattern matching
- **Section-wise analysis** with density scores
- **Batch processing** for entire chapters
- **Syntax-preserving editing** (LaTeX commands, math, citations)

### Usage

**Interactive analysis** (single section):
```bash
python scripts/deai_check.py paper.tex --section introduction
```

**Full document analysis**:
```bash
python scripts/deai_check.py paper.tex --analyze
```

**Batch processing** (entire chapters):
```bash
python scripts/deai_batch.py paper.tex --all-sections
python scripts/deai_batch.py paper.tex --chapter chapter3/introduction.tex --output polished/
```

**Section-wise density scores**:
```bash
python scripts/deai_check.py paper.tex --score
```

### Output Example

```
================================================================================
DE-AI WRITING TRACE ANALYSIS REPORT
================================================================================
File: paper.tex
Total lines: 450

--------------------------------------------------------------------------------
SECTION-WISE AI TRACE DENSITY
--------------------------------------------------------------------------------

[HIGH] INTRODUCTION
  AI trace density: 8.5%
  Traces found: 12 / 141 lines

[MEDIUM] METHODS
  AI trace density: 3.2%
  Traces found: 5 / 156 lines
```

### Reference Documentation

See `references/DEAI_GUIDE.md` for:
- Common AI patterns to remove
- Section-specific guidelines
- Output format specifications
- Quick reference replacements



## Reference Files

- `references/TERMINOLOGY.md`: Domain terminology (Deep Learning, Time Series, Industrial Control)
- `references/TRANSLATION_GUIDE.md`: Translation principles, Chinglish corrections
- `references/STYLE_GUIDE.md`: Academic writing rules
- `references/COMMON_ERRORS.md`: Common mistakes
- `references/VENUES.md`: Conference/journal requirements
- `references/DEAI_GUIDE.md`: De-AI writing guide and AI pattern detection

## Next Steps

- [Compilation Recipes Guide](/guides/compilation)
- [Format Checking Guide](/guides/format-checking)
- [Bibliography Guide](/guides/bibliography)
