# Compilation Recipes Guide

Complete guide to LaTeX compilation recipes in Academic Writing Skills.

## Overview

Academic Writing Skills provides multiple compilation recipes optimized for different use cases. Understanding when and how to use each recipe is crucial for efficient LaTeX workflow.

## Recipe Architecture

Each recipe is a sequence of compilation steps:

```
Recipe = [Step1, Step2, ..., StepN]
```

For example, `pdflatex-biber`:
```
[pdflatex, biber, pdflatex, pdflatex]
```

## Available Recipes

### Single-Pass Recipes

#### pdflatex

**Command**: `pdflatex document.tex`

**Use case**: Quick English-only drafts

**Pros**:
- Fastest compilation (1-2 seconds)
- Stable and mature
- Wide compatibility

**Cons**:
- Limited Unicode support
- No system fonts
- ASCII-centric

**When to use**:
- Rapid iteration on English papers
- No special characters needed
- Speed is priority

**Example**:
```bash
python compile.py paper.tex --recipe pdflatex
```

#### xelatex

**Command**: `xelatex document.tex`

**Use case**: Unicode/Chinese documents

**Pros**:
- Full Unicode support
- System font access
- Modern typography
- CJK support

**Cons**:
- Slower than pdfLaTeX (3-5 seconds)
- Larger output files

**When to use**:
- Chinese/Japanese/Korean text
- Custom fonts required
- Unicode characters needed

**Example**:
```bash
python compile.py thesis.tex --recipe xelatex
```

#### lualatex

**Command**: `lualatex document.tex`

**Use case**: Advanced scripting, Unicode

**Pros**:
- Full Unicode support
- Lua scripting capabilities
- Modern font handling

**Cons**:
- Slower than XeLaTeX
- Less mature ecosystem

**When to use**:
- Need Lua scripting
- Complex font requirements
- Alternative to XeLaTeX

### Bibliography Workflows

#### pdflatex-bibtex

**Commands**:
```
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

**Use case**: English papers with traditional BibTeX

**Pros**:
- Wide compatibility
- Stable and proven
- Works with legacy .bst styles

**Cons**:
- Limited Unicode support
- No advanced sorting
- ASCII-only author names

**When to use**:
- English-only bibliography
- Legacy .bst style files
- Maximum compatibility needed

**Example**:
```bash
python compile.py paper.tex --recipe pdflatex-bibtex
```

#### pdflatex-biber

**Commands**:
```
pdflatex document.tex
biber document
pdflatex document.tex
pdflatex document.tex
```

**Use case**: English papers with modern bibliography

**Pros**:
- Full Unicode support
- Advanced sorting
- Better localization
- Modern BibLaTeX features

**Cons**:
- Requires BibLaTeX package
- Slightly slower than BibTeX

**When to use**:
- Modern LaTeX projects
- Need Unicode in bibliography
- Want advanced features (e.g., multiple bibliographies)

**Example**:
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

**Recommended for**: Most new English papers

#### xelatex-bibtex

**Commands**:
```
xelatex document.tex
bibtex document
xelatex document.tex
xelatex document.tex
```

**Use case**: Chinese papers with traditional BibTeX

**Pros**:
- Unicode document support
- Works with legacy styles

**Cons**:
- BibTeX still ASCII-limited
- Inconsistent with document encoding

**When to use**:
- Chinese document
- Must use legacy .bst file
- No Biber available

#### xelatex-biber

**Commands**:
```
xelatex document.tex
biber document
xelatex document.tex
xelatex document.tex
```

**Use case**: Chinese papers with modern bibliography

**Pros**:
- Full Unicode everywhere
- GB/T 7714 support
- Consistent encoding
- Best for Chinese

**Cons**:
- Requires BibLaTeX + Biber

**When to use**:
- Chinese thesis/paper
- GB/T 7714 compliance needed
- Modern LaTeX setup

**Example**:
```bash
python compile.py thesis.tex --recipe xelatex-biber
```

**Recommended for**: All Chinese theses

### Automated Recipes

#### latexmk

**Command**: `latexmk -pdf document.tex`

**Use case**: Automatic dependency handling

**Pros**:
- Detects changes automatically
- Runs minimal necessary steps
- Handles complex dependencies
- Watch mode support

**Cons**:
- Slower initial setup
- Less predictable
- Harder to debug

**When to use**:
- Complex multi-file projects
- Continuous compilation needed
- Don't want to think about steps

**Example**:
```bash
python compile.py paper.tex --recipe latexmk
```

**Configuration**: Create `.latexmkrc`:
```perl
$pdf_mode = 1;  # pdflatex
$pdflatex = 'pdflatex -interaction=nonstopmode';
$bibtex_use = 2;  # Run bibtex when needed
```

For XeLaTeX:
```perl
$pdf_mode = 5;  # xelatex
$xelatex = 'xelatex -interaction=nonstopmode';
```

## Recipe Selection Decision Tree

```
Start
  │
  ├─ Chinese text?
  │   ├─ Yes → Use XeLaTeX
  │   │   ├─ Bibliography?
  │   │   │   ├─ Yes → xelatex-biber (recommended)
  │   │   │   └─ No → xelatex
  │   │   └─
  │   └─ No → Use pdfLaTeX
  │       ├─ Bibliography?
  │       │   ├─ Yes → pdflatex-biber (recommended)
  │       │   └─ No → pdflatex
  │       └─
  │
  ├─ Unicode characters?
  │   └─ Yes → Use XeLaTeX (see above)
  │
  ├─ Custom fonts?
  │   └─ Yes → Use XeLaTeX (see above)
  │
  ├─ Complex dependencies?
  │   └─ Yes → Use latexmk
  │
  └─ Default → pdflatex or pdflatex-biber
```

## Performance Comparison

| Recipe | Time (small doc) | Time (large doc) | Output Size |
|--------|------------------|------------------|-------------|
| pdflatex | 1-2s | 5-10s | Small |
| xelatex | 3-5s | 15-30s | Medium |
| lualatex | 4-6s | 20-40s | Medium |
| pdflatex-bibtex | 5-8s | 20-40s | Small |
| pdflatex-biber | 6-10s | 25-50s | Small |
| xelatex-biber | 12-20s | 60-120s | Medium |
| latexmk | Variable | Variable | Variable |

*Times are approximate and depend on document complexity and system performance.*

## Troubleshooting

### Bibliography Not Appearing

**Problem**: Bibliography section is empty after compilation

**Cause**: Single-pass compilation doesn't process bibliography

**Solution**: Use full workflow recipe
```bash
# Wrong
python compile.py paper.tex --recipe pdflatex

# Correct
python compile.py paper.tex --recipe pdflatex-biber
```

### Citations Show as [?]

**Problem**: Citations display as `[?]` in output

**Cause**: Incomplete compilation cycle

**Solution**: Run full recipe (multiple passes needed)
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

### Chinese Characters Not Displaying

**Problem**: Chinese text shows as boxes or errors

**Cause**: Using pdfLaTeX for Chinese

**Solution**: Switch to XeLaTeX
```bash
python compile.py thesis.tex --recipe xelatex-biber
```

### Compilation Too Slow

**Problem**: Compilation takes too long

**Solutions**:
1. Use faster recipe for drafts:
   ```bash
   python compile.py paper.tex --recipe pdflatex  # Skip bibliography
   ```

2. Use draft mode in LaTeX:
   ```latex
   \documentclass[draft]{article}
   ```

3. Compile only changed chapters (for thesis)

### Font Not Found

**Problem**: `! Font \xxx not found`

**Cause**: System font not available to XeLaTeX

**Solution**: Install font or use different font
```bash
# macOS: Install font via Font Book
# Linux: Copy to ~/.fonts/
# Windows: Install via Fonts control panel
```

## Best Practices

### 1. Use Appropriate Recipe for Stage

**Draft stage**: Fast single-pass
```bash
python compile.py paper.tex --recipe pdflatex
```

**Review stage**: Full workflow
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

**Final submission**: Full workflow + clean
```bash
python compile.py paper.tex --recipe pdflatex-biber --clean
```

### 2. Consistent Recipe Usage

Stick to one recipe per project to avoid inconsistencies:

```bash
# Good: Always use same recipe
python compile.py paper.tex --recipe pdflatex-biber

# Bad: Switching recipes randomly
python compile.py paper.tex --recipe pdflatex
python compile.py paper.tex --recipe xelatex-biber  # May cause issues
```

### 3. Clean Auxiliary Files Regularly

```bash
# Clean after major changes
python compile.py paper.tex --recipe pdflatex-biber --clean

# Or manually
rm *.aux *.bbl *.blg *.log *.out
```

### 4. Use latexmk for Complex Projects

For multi-file projects with many dependencies:

```bash
python compile.py thesis.tex --recipe latexmk
```

### 5. Version Control Auxiliary Files

**Don't commit**:
- `*.aux`, `*.log`, `*.out`
- `*.bbl`, `*.blg`
- `*.pdf` (usually)

**Do commit**:
- `.latexmkrc` (if customized)
- Source `.tex` files
- `.bib` files

## Advanced Usage

### Custom Recipes

Define custom recipes in skill configuration:

```yaml
# ~/.claude/skills/latex-paper-en/config.yaml
custom_recipes:
  my_workflow:
    - xelatex
    - biber
    - makeindex
    - xelatex
    - xelatex
```

### Parallel Compilation

For multi-file projects, compile chapters in parallel:

```bash
# Compile chapters in parallel
for chapter in chap*.tex; do
  python compile.py "$chapter" --recipe pdflatex &
done
wait
```

### Continuous Compilation

Use watch mode for continuous compilation:

```bash
python compile.py paper.tex --recipe latexmk --watch
```

Or use `latexmk` directly:
```bash
latexmk -pdf -pvc paper.tex
```

## Next Steps

- [Format Checking Guide](/guides/format-checking) - Ensure code quality
- [Bibliography Guide](/guides/bibliography) - Manage references
- [Usage Guide](/usage) - General usage documentation
