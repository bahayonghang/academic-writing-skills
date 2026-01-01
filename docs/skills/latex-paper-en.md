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

## Installation

```bash
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-paper-en.skill.zip
```

## Quick Start

```bash
# Simple compilation
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex

# Compilation with bibliography
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-bibtex

# Format check
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex

# Bibliography verification
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib
```

## Scripts

### compile.py

Compile LaTeX documents with multiple recipe support.

**Usage**:
```bash
python compile.py <tex_file> [options]

Options:
  --recipe RECIPE      Compilation recipe (default: pdflatex)
  --output-dir DIR     Output directory (default: same as input)
  --clean              Clean auxiliary files after compilation
  --verbose            Show detailed compilation output
```

**Available recipes**:
- `pdflatex`: Single-pass pdfLaTeX compilation
- `xelatex`: Single-pass XeLaTeX compilation
- `latexmk`: Automated compilation with latexmk
- `pdflatex-bibtex`: pdfLaTeX + BibTeX workflow
- `xelatex-bibtex`: XeLaTeX + BibTeX workflow
- `pdflatex-biber`: pdfLaTeX + Biber workflow (recommended)
- `xelatex-biber`: XeLaTeX + Biber workflow (recommended)

**Examples**:
```bash
# Quick draft (fastest)
python compile.py paper.tex --recipe pdflatex

# Final version with bibliography
python compile.py paper.tex --recipe pdflatex-biber --clean

# Unicode/Chinese support
python compile.py paper.tex --recipe xelatex-biber

# Automated dependency handling
python compile.py paper.tex --recipe latexmk
```

### check_format.py

Check LaTeX format and style compliance.

**Usage**:
```bash
python check_format.py <tex_file> [options]

Options:
  --quick              Quick check (common issues only)
  --deep               Deep check (thorough analysis)
  --venue VENUE        Venue-specific rules (ieee, acm, springer)
  --sections SECTIONS  Check specific sections only
  --output FORMAT      Output format (text, json, html)
```

**Check levels**:

1. **Quick** (--quick): ~1-2 seconds
   - Citation spacing
   - Basic punctuation
   - Section structure

2. **Standard** (default): ~5-10 seconds
   - All quick checks
   - ChkTeX integration
   - Reference consistency
   - Label conventions

3. **Deep** (--deep): ~30-60 seconds
   - All standard checks
   - Style guide compliance
   - Advanced grammar patterns
   - Cross-reference validation

**Examples**:
```bash
# Quick check
python check_format.py paper.tex --quick

# Full check with IEEE style
python check_format.py paper.tex --venue ieee

# Deep check with JSON output
python check_format.py paper.tex --deep --output json

# Check specific sections
python check_format.py paper.tex --sections introduction,methods
```

### verify_bib.py

Verify BibTeX bibliography format.

**Usage**:
```bash
python verify_bib.py <bib_file> [options]

Options:
  --style STYLE        Citation style (ieee, acm, springer)
  --require-doi        Require DOI for all entries
  --require-url        Require URL for all entries
  --fix                Automatically fix common issues
  --output FORMAT      Output format (text, json)
```

**Checks**:
- Required fields (author, title, year, venue)
- Entry type consistency
- DOI format validation
- URL format validation
- Duplicate keys
- Formatting consistency

**Examples**:
```bash
# Basic verification
python verify_bib.py references.bib

# IEEE style with DOI requirement
python verify_bib.py references.bib --style ieee --require-doi

# Auto-fix common issues
python verify_bib.py references.bib --fix

# JSON output for CI/CD
python verify_bib.py references.bib --output json
```

### extract_prose.py

Extract prose text for external grammar checking.

**Usage**:
```bash
python extract_prose.py <tex_file> [options]

Options:
  --sections SECTIONS  Extract specific sections only
  --exclude EXCLUDE    Exclude sections (e.g., abstract,references)
  --output FILE        Output file (default: stdout)
  --format FORMAT      Output format (text, markdown)
```

**Examples**:
```bash
# Extract all prose
python extract_prose.py paper.tex > prose.txt

# Extract specific sections
python extract_prose.py paper.tex --sections introduction,methods

# Use with grammar tools
python extract_prose.py paper.tex | grammarly-cli
python extract_prose.py paper.tex | languagetool

# Markdown output
python extract_prose.py paper.tex --format markdown > prose.md
```

## Compilation Recipes

### Choosing the Right Recipe

**For English-only papers**:
```
No bibliography        → pdflatex (fastest)
With bibliography      → pdflatex-biber (recommended)
Legacy compatibility   → pdflatex-bibtex
```

**For Unicode/multilingual papers**:
```
No bibliography        → xelatex
With bibliography      → xelatex-biber (recommended)
Legacy compatibility   → xelatex-bibtex
```

**For complex dependencies**:
```
Auto handling          → latexmk
```

### Recipe Details

#### pdflatex
- **Compiler**: pdfLaTeX
- **Passes**: 1
- **Best for**: English-only, quick drafts
- **Speed**: ⚡⚡⚡ (fastest)
- **Limitations**: Limited Unicode support

#### pdflatex-bibtex
- **Compiler**: pdfLaTeX → BibTeX → pdfLaTeX × 2
- **Passes**: 4
- **Best for**: English papers with BibTeX
- **Speed**: ⚡⚡
- **Compatibility**: High (legacy)

#### pdflatex-biber
- **Compiler**: pdfLaTeX → Biber → pdfLaTeX × 2
- **Passes**: 4
- **Best for**: English papers with modern bibliography
- **Speed**: ⚡⚡
- **Features**: UTF-8, advanced sorting, localization

#### xelatex-biber
- **Compiler**: XeLaTeX → Biber → XeLaTeX × 2
- **Passes**: 4
- **Best for**: Unicode/multilingual papers
- **Speed**: ⚡
- **Features**: Full Unicode, system fonts, modern typography

#### latexmk
- **Compiler**: Auto-detect (pdfLaTeX/XeLaTeX/LuaLaTeX)
- **Passes**: Variable (handles dependencies automatically)
- **Best for**: Complex documents, automation
- **Speed**: ⚡ (adaptive)
- **Features**: Automatic recompilation, dependency tracking

## Format Checking

### ChkTeX Integration

The skill integrates ChkTeX for comprehensive LaTeX linting:

```bash
# Manual ChkTeX run
chktex paper.tex

# With custom config
chktex -l ~/.chktexrc paper.tex
```

### Common Issues

#### 1. Citation Spacing

**Issue**: Missing space before citation
```latex
% Bad
word\cite{key}

% Good
word \cite{key}
```

**Detection**: Automatically detected by `check_format.py --quick`

#### 2. Punctuation in Math Mode

**Issue**: Punctuation outside math mode
```latex
% Bad
The equation is $x = 1$ .

% Good
The equation is $x = 1$.
```

**Detection**: Detected by ChkTeX and standard check

#### 3. Inconsistent Capitalization

**Issue**: Section titles not following venue style
```latex
% Bad (IEEE style)
\section{introduction and background}

% Good (IEEE style)
\section{Introduction and Background}
```

**Detection**: Venue-specific check with `--venue ieee`

#### 4. Label Conventions

**Issue**: Non-descriptive or inconsistent labels
```latex
% Bad
\label{1}
\label{my_figure}

% Good
\label{sec:introduction}
\label{fig:architecture}
\label{tab:results}
\label{eq:loss_function}
```

**Detection**: Standard check

### Venue-Specific Rules

#### IEEE Style

- **Title**: Each Major Word Capitalized
- **Sections**: Each Major Word Capitalized
- **Figures**: "Fig." in text, "Figure" in captions
- **Tables**: "TABLE" in captions (uppercase)
- **Citations**: Numerical [1], [2], [3]

#### ACM Style

- **Title**: Each Major Word Capitalized
- **Sections**: Sentence case (Only first word capitalized)
- **Figures**: "Figure" everywhere
- **Tables**: "Table" everywhere
- **Citations**: Numerical [1] or author-year (Smith et al. 2024)

#### Springer Style

- **Title**: Sentence case or Title Case (varies by venue)
- **Sections**: Sentence case
- **Figures**: "Fig." in text and captions
- **Tables**: "Table" everywhere
- **Citations**: Numerical [1] or author-year

## Bibliography Management

### BibTeX Best Practices

1. **Consistent entry keys**:
   ```bibtex
   @article{Smith2024-deeplearning,
     author = {Smith, John and Doe, Jane},
     title = {Deep Learning for Natural Language Processing},
     journal = {Journal of Machine Learning Research},
     year = {2024},
     volume = {25},
     pages = {1--30},
     doi = {10.1234/jmlr.2024.001}
   }
   ```

2. **Required fields by entry type**:
   ```bibtex
   @article:    author, title, journal, year, volume, pages
   @inproceedings: author, title, booktitle, year, pages
   @book:       author, title, publisher, year
   @phdthesis:  author, title, school, year
   ```

3. **Include DOI when available**:
   ```bibtex
   doi = {10.1234/journal.2024.001}
   ```

### Common Bibliography Issues

1. **Missing required fields**
   - **Detection**: `verify_bib.py` catches all missing fields
   - **Fix**: Add missing fields from original source

2. **Malformed entries**
   - **Detection**: BibTeX parser errors
   - **Fix**: Check braces, quotes, commas

3. **Duplicate keys**
   - **Detection**: `verify_bib.py --check-duplicates`
   - **Fix**: Rename duplicate keys uniquely

4. **Inconsistent formatting**
   - **Detection**: Style-specific checks
   - **Fix**: Use `--fix` flag for automatic corrections

## Style Guide References

The skill includes comprehensive style guide references:

### Common Errors

See: `~/.claude/skills/latex-paper-en/references/COMMON_ERRORS.md`

Topics:
- Chinglish errors in academic writing
- Article usage (a, an, the)
- Preposition usage
- Verb tense in academic writing
- Common grammar mistakes

### Venues

See: `~/.claude/skills/latex-paper-en/references/VENUES.md`

Covered venues:
- IEEE (Transactions, Conferences)
- ACM (SIGCHI, SIGMOD, etc.)
- Springer (LNCS, journals)
- NeurIPS, ICML, ICLR
- AAAI, IJCAI

Each venue includes:
- Formatting guidelines
- Citation styles
- Figure/table conventions
- Page limits
- Submission requirements

### Academic Writing Style

See: `~/.claude/skills/latex-paper-en/references/STYLE_GUIDE.md`

Topics:
- Conciseness and clarity
- Active vs. passive voice
- Hedging language
- Transitions
- Abstract writing
- Introduction structure

## Integration with Claude Code

### Natural Language Commands

Use the skill through conversational interfaces:

```
You: Compile my IEEE paper with bibliography and check for format errors

Claude: I'll compile your paper using the pdflatex-biber recipe (recommended for
modern bibliography) and run IEEE-specific format checks.

[Executes compilation and checking]

Claude: Compilation successful! Format check found 2 issues:
1. Section 3.2 title should use IEEE capitalization: "Machine Learning Models"
2. Citation [5] needs space before it on line 87
```

### Workflow Automation

Create automated workflows:

```yaml
# .claude/workflows/paper-check.yaml
name: Paper Check
triggers:
  - file_save: "*.tex"
steps:
  - skill: latex-paper-en
    script: check_format.py
    args: "${file} --quick"
  - notify:
      level: warning
      message: "${check_results}"
```

## Advanced Usage

### Custom Compilation Recipes

Define custom recipes in `config.yaml`:

```yaml
custom_recipes:
  my_workflow:
    - xelatex
    - biber
    - makeindex
    - xelatex
    - xelatex
```

### Continuous Integration

Use in CI pipelines:

```yaml
# .github/workflows/latex-ci.yml
- name: Check LaTeX format
  run: |
    python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex --output json > results.json

- name: Compile paper
  run: |
    python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-biber

- name: Upload PDF
  uses: actions/upload-artifact@v3
  with:
    name: paper.pdf
    path: paper.pdf
```

## Troubleshooting

### Compilation Fails

**Error**: `! LaTeX Error: File 'xxx.sty' not found`

**Solution**: Install missing package
```bash
tlmgr install <package>  # TeX Live
mpm --install <package>  # MiKTeX
```

### ChkTeX Not Found

**Error**: `chktex: command not found`

**Solution**: Install ChkTeX
```bash
brew install chktex        # macOS
apt-get install chktex     # Ubuntu
```

### Bibliography Not Appearing

**Error**: Empty bibliography section

**Solution**: Use full workflow recipe
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

## Next Steps

- [Compilation Recipes Guide](/guides/compilation)
- [Format Checking Guide](/guides/format-checking)
- [Bibliography Guide](/guides/bibliography)
- [Usage Guide](/usage)
