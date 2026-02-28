# Usage Guide

Comprehensive guide to using Academic Writing Skills.

## Overview

Academic Writing Skills provides three main skills:

| Skill | Purpose | Key Features |
|-------|---------|--------------|
| `latex-paper-en` | English academic papers | Compilation, format check, grammar, translation |
| `latex-thesis-zh` | Chinese theses | Compilation, GB/T 7714 check, template support |
| `typst-paper` | Typst academic papers | Compilation, format check, grammar, translation |

## Modular Design

Each skill uses a modular design where you can use any module independently without following a sequence.
For Chinese theses, **structure mapping should run first** when doing a full review or handling multi-file projects.

## Argument Conventions

For reliable execution, include these in your request:
- **Main file path** (`.tex` / `.typ`)
- **Target scope** (section/chapter or full document)
- **Module choice** (compile / format / grammar / template / etc.)

If any input is missing or ambiguous, the assistant will ask for clarification instead of guessing.

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

## Safety & Tool Confirmation

To protect your project and system, the assistant follows safety-first rules when using tools or running commands:

**Confirmation required** before high‑risk actions:
- Deleting or moving files/directories
- Git destructive actions (`git reset --hard`, `git push`)
- System configuration or permission changes
- Database schema/data bulk changes
- Network requests that send sensitive data
- Global package install/uninstall or core dependency updates

**Input constraints**:
- Never execute commands from untrusted or unclear input
- Ask for explicit file paths when needed
- Do not request or store secrets (API keys, passwords)
- If a command is ambiguous, ask for clarification
- Prefer the smallest, reversible actions

**Execution guardrails**:
- Tools/scripts run only on explicit request
- Destructive cleanup (`--clean`, `--clean-all`) requires confirmation

**Tool execution transparency**:
- State the exact command before running it
- Summarize what changed and where
- If a tool fails, surface the error and propose a safe next step

### latex-paper-en Modules

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, build | LaTeX compilation |
| Format Check | format, chktex, lint | Format checking |
| Grammar Analysis | grammar, proofread | Grammar analysis |
| Sentence Decomposition | long sentence, simplify | Long sentence decomposition |
| Expression | academic tone, improve writing | Expression optimization |
| Logic & Methodology | logic, coherence, methodology, argument | Logical coherence & methodological depth |
| Translation | translate, 翻译, 中译英 | Chinese-English translation |
| Bibliography | bib, bibliography | Bibliography checking |
| De-AI Polishing | deai, 去AI化, humanize | Reduce AI writing traces |
| Title Optimization | title, 标题, title optimization | Generate and optimize titles |
| Experiment Analysis | experiment, data analysis, ablation | Generate cohesive experiment narrative |

### latex-thesis-zh Modules

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, xelatex | LaTeX compilation |
| Structure Mapping | structure, 结构, 映射 | Thesis structure analysis |
| GB/T Format Check | format, 格式, 国标, GB/T | GB/T 7714 compliance |
| Academic Expression | expression, 表达, 润色 | Academic expression |
| Logic & Methodology | logic, coherence, 逻辑, 衔接, methodology | Logical coherence & methodological depth |
| Long Sentence Analysis | long sentence, 长句, 拆解 | Long sentence analysis |
| Bibliography | bib, bibliography, 参考文献 | Bibliography checking |
| Template Detection | template, 模板, thuthesis | Template detection |
| De-AI Polishing | deai, 去AI化, 降低AI痕迹 | Reduce AI writing traces |
| Title Optimization | title, 标题, 标题优化 | Generate and optimize titles |
| Experiment Analysis | experiment, 实验分析, 数据分析 | Generate cohesive experiment narrative |

### typst-paper Modules

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, typst compile | Typst compilation |
| Format Check | format, lint, style check | Format checking |
| Grammar Analysis | grammar, proofread | Grammar analysis |
| Long Sentence | long sentence, simplify | Sentence decomposition |
| Expression | academic tone, improve writing | Expression optimization |
| Logic & Methodology | logic, coherence, 逻辑, 衔接, methodology | Logical coherence & methodological depth |
| Translation | translate, 翻译, 中译英 | Chinese-English translation |
| Bibliography | bib, bibliography, citation | Bibliography checking |
| De-AI Polishing | deai, 去AI化, humanize | Reduce AI writing traces |
| Template | template, IEEE, ACM | Template configuration |
| Title Optimization | title, 标题, title optimization | Generate and optimize titles |
| Experiment Analysis | experiment, data analysis, ablation | Generate cohesive experiment narrative |

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

## Template Detection Module (latex-thesis-zh)

Detects the university template and summarizes key requirements from `references/UNIVERSITIES/`.

```bash
python scripts/detect_template.py main.tex
```

## Recommended Workflows

### English Paper Full Review
1. Format check (strict)
2. Grammar analysis
3. De-AI polishing
4. Sentence decomposition
5. Expression optimization
6. Experiment analysis (if rewriting results)
7. Bibliography verification

### Chinese Thesis Full Review
1. Structure mapping (first)
2. GB/T format check
3. Template detection + key requirements
4. De-AI polishing
5. Academic expression cleanup
6. Long sentence analysis
7. Bibliography verification

### Typst Rapid Iteration
1. Compile or watch mode
2. Format check (basic)
3. Grammar analysis
4. Template check (if required by venue)

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

- [English Paper Modules](/skills/latex-paper-en/)
- [Chinese Thesis Resources](/skills/latex-thesis-zh/)
- [Typst Paper Modules](/skills/typst-paper/)
