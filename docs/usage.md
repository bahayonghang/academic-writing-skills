# Usage Guide

Comprehensive guide to using Academic Writing Skills with Claude Code.

## Overview

Academic Writing Skills provides two complementary skills:

- **latex-paper-en**: For English academic papers (IEEE, ACM, Springer, etc.)
- **latex-thesis-zh**: For Chinese theses (GB/T 7714, university templates)

Each skill includes:
- Multiple compilation recipes
- Format checking tools
- Bibliography verification
- Style guide references

## Skill Invocation

### Method 1: Direct Script Execution

Run skill scripts directly:

```bash
# English paper compilation
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex

# Chinese thesis structure mapping
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
```

### Method 2: Claude Code Integration

Use skills through natural language with Claude:

```
You: Compile my LaTeX paper with pdflatex and check for format errors

Claude: [Invokes latex-paper-en skill]
I'll compile your paper and run format checks.

[Executes compilation and checking]

Claude: Compilation successful! Your paper compiled to paper.pdf.
Format check found 2 minor issues: ...
```

### Method 3: Skill Shortcuts

If configured, use skill shortcuts:

```bash
# If you've set up aliases
latex-en-compile paper.tex --recipe pdflatex-bibtex
latex-zh-structure thesis.tex
```

## Common Tasks

### Task 1: Compile a Paper

**English paper** (simple):
```bash
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex
```

**English paper** (with bibliography):
```bash
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-bibtex
```

**Chinese thesis**:
```bash
python ~/.claude/skills/latex-thesis-zh/scripts/compile.py thesis.tex --recipe xelatex-biber
```

### Task 2: Check Format

**Quick check** (fast, common issues):
```bash
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex --quick
```

**Full check** (thorough, all issues):
```bash
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex
```

**Check specific sections**:
```bash
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex --sections introduction,methods
```

### Task 3: Verify Bibliography

**Check BibTeX format**:
```bash
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib
```

**Check GB/T 7714 compliance** (Chinese):
```bash
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gbt7714
```

### Task 4: Extract Prose for Grammar Check

Extract text content for grammar checking:

```bash
# Extract all prose
python ~/.claude/skills/latex-paper-en/scripts/extract_prose.py paper.tex

# Extract specific sections
python ~/.claude/skills/latex-paper-en/scripts/extract_prose.py paper.tex --sections abstract,introduction
```

Use with external grammar tools:
```bash
# With Grammarly CLI
python extract_prose.py paper.tex | grammarly-cli

# With LanguageTool
python extract_prose.py paper.tex | languagetool
```

### Task 5: Map Thesis Structure

For Chinese theses, identify structure and template:

```bash
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
```

Output example:
```
Thesis Structure Analysis
========================

Template: Tsinghua University (thuthesis)
Main file: thesis.tex

Structure:
- 封面 (Cover): data/cover.tex
- 中文摘要 (Chinese Abstract): data/abstract_zh.tex
- English Abstract: data/abstract_en.tex
- 目录 (Contents): auto-generated
- 第1章 绪论: data/chap01.tex
- 第2章 相关工作: data/chap02.tex
- ...
- 参考文献 (References): ref/refs.bib
- 致谢 (Acknowledgements): data/ack.tex
```

### Task 6: Check Terminology Consistency

For Chinese theses, verify consistent terminology usage:

```bash
python ~/.claude/skills/latex-thesis-zh/scripts/check_consistency.py data/
```

Checks for:
- Inconsistent translations of technical terms
- Mixed use of English/Chinese terms
- Inconsistent punctuation usage

## Compilation Recipes

### Available Recipes

| Recipe | Compilers | Use Case |
|--------|-----------|----------|
| `pdflatex` | pdflatex ×1 | Quick English-only draft |
| `xelatex` | xelatex ×1 | Unicode/Chinese draft |
| `latexmk` | auto-detect | Auto dependency handling |
| `pdflatex-bibtex` | pdflatex → bibtex → pdflatex ×2 | English + BibTeX |
| `xelatex-bibtex` | xelatex → bibtex → xelatex ×2 | Chinese + BibTeX |
| `pdflatex-biber` | pdflatex → biber → pdflatex ×2 | English + modern refs |
| `xelatex-biber` | xelatex → biber → xelatex ×2 | Chinese + modern refs |

### Recipe Selection Guide

**Choose based on content**:

```
English-only, no refs          → pdflatex
English-only, with refs        → pdflatex-bibtex or pdflatex-biber
Unicode/Chinese, no refs       → xelatex
Unicode/Chinese, with refs     → xelatex-biber
Complex deps, auto handling    → latexmk
```

**Choose based on priority**:

```
Speed (fastest)                → pdflatex
Modern features                → xelatex or lualatex
Modern bibliography            → *-biber recipes
Compatibility (safest)         → *-bibtex recipes
Automation (easiest)           → latexmk
```

### Custom Recipes

Define custom recipes in skill configuration:

```yaml
# In ~/.claude/skills/latex-paper-en/config.yaml
recipes:
  my-custom:
    - xelatex
    - biber
    - xelatex
    - makeindex
    - xelatex
```

## Format Checking

### Check Levels

**Level 1: Quick Check** (--quick flag)
- Citation spacing
- Common punctuation errors
- Basic section structure
- Execution time: ~1-2 seconds

**Level 2: Standard Check** (default)
- All Level 1 checks
- ChkTeX integration
- Reference consistency
- Label conventions
- Execution time: ~5-10 seconds

**Level 3: Deep Check** (--deep flag)
- All Level 2 checks
- Style guide compliance (IEEE/ACM/Springer)
- Advanced grammar patterns
- Cross-reference validation
- Execution time: ~30-60 seconds

### Common Issues Detected

1. **Citation spacing**:
   ```latex
   % Bad
   word\cite{key}

   % Good
   word \cite{key}
   ```

2. **Punctuation in math mode**:
   ```latex
   % Bad
   $x = 1$ .

   % Good
   $x = 1$.
   ```

3. **Section capitalization**:
   ```latex
   % Bad (IEEE style)
   \section{introduction and background}

   % Good (IEEE style)
   \section{Introduction and Background}
   ```

4. **Label conventions**:
   ```latex
   % Bad
   \label{1}

   % Good
   \label{sec:introduction}
   \label{fig:architecture}
   \label{tab:results}
   ```

## Bibliography Management

### Verification Features

**Format validation**:
- Required fields (author, title, year, venue)
- DOI format
- URL format
- Page number format

**Standard compliance**:
- IEEE citation style
- ACM citation style
- GB/T 7714-2015 (Chinese)

**Common issues detected**:
- Missing required fields
- Malformed entries
- Duplicate keys
- Inconsistent formatting

### BibTeX Best Practices

1. **Use consistent keys**:
   ```bibtex
   % Good pattern
   @article{AuthorYear-keyword,
     ...
   }
   ```

2. **Include DOI when available**:
   ```bibtex
   @article{Smith2024-ml,
     ...
     doi = {10.1234/journal.2024.001},
   }
   ```

3. **Use proper entry types**:
   ```bibtex
   @inproceedings{...}  % For conference papers
   @article{...}         % For journal articles
   @book{...}            % For books
   @phdthesis{...}       % For PhD theses
   ```

## Working with University Templates

### Supported Templates

**Chinese universities**:
- Tsinghua University (thuthesis)
- Peking University (pkuthss)
- USTC (ustcthesis)
- Fudan University (fduthesis)
- Generic Chinese thesis template

### Template Detection

The `map_structure.py` script automatically detects:

```bash
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
```

Detection based on:
- Document class (`\documentclass{thuthesis}`)
- Package imports
- File naming conventions
- Directory structure

### Template-Specific Features

Each template has specific requirements checked by the skill:

**Tsinghua (thuthesis)**:
- Cover page format
- Abstract bilingual requirement
- Chapter naming conventions
- Bibliography style (GB/T 7714)

**PKU (pkuthss)**:
- Specific cover fields
- Declaration page
- Abstract keywords
- Bibliography format

## Advanced Usage

### Batch Processing

Process multiple files:

```bash
# Compile all .tex files
for file in *.tex; do
  python ~/.claude/skills/latex-paper-en/scripts/compile.py "$file" --recipe pdflatex
done

# Check all .tex files
for file in *.tex; do
  python ~/.claude/skills/latex-paper-en/scripts/check_format.py "$file"
done
```

### Continuous Integration

Use in CI/CD pipelines:

```yaml
# .github/workflows/latex-check.yml
name: LaTeX Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install LaTeX
        run: sudo apt-get install texlive-full

      - name: Check format
        run: python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex

      - name: Compile
        run: python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-biber
```

### Custom Workflows

Create project-specific workflows:

```bash
#!/bin/bash
# my-thesis-workflow.sh

echo "Step 1: Structure analysis"
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex

echo "Step 2: Format check"
python ~/.claude/skills/latex-thesis-zh/scripts/check_format.py thesis.tex

echo "Step 3: Bibliography verification"
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py refs.bib --standard gbt7714

echo "Step 4: Compilation"
python ~/.claude/skills/latex-thesis-zh/scripts/compile.py thesis.tex --recipe xelatex-biber

echo "Step 5: Consistency check"
python ~/.claude/skills/latex-thesis-zh/scripts/check_consistency.py data/

echo "Workflow complete!"
```

## Configuration

### Skill Configuration Files

Each skill has a configuration file:

```
~/.claude/skills/latex-paper-en/config.yaml
~/.claude/skills/latex-thesis-zh/config.yaml
```

### Customizable Settings

**Compilation**:
```yaml
compilation:
  default_recipe: pdflatex-bibtex
  timeout: 300  # seconds
  max_retries: 3
  clean_auxiliary: true
```

**Format checking**:
```yaml
format_check:
  chktex_config: ~/.chktexrc
  max_warnings: 10
  strict_mode: false
```

**Bibliography**:
```yaml
bibliography:
  style: ieee  # ieee, acm, springer, gbt7714
  require_doi: true
  validate_urls: true
```

## Troubleshooting

See [Common Errors Reference](/references/common-errors) for detailed troubleshooting.

## Next Steps

- [Compilation Recipes Guide](/guides/compilation) - Deep dive into recipes
- [Format Checking Guide](/guides/format-checking) - Understanding checks
- [Bibliography Guide](/guides/bibliography) - Managing references
- [English Papers Skill](/skills/latex-paper-en) - Detailed skill docs
- [Chinese Thesis Skill](/skills/latex-thesis-zh) - Detailed skill docs
