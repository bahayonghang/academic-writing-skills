# Format Checking Guide

Comprehensive guide to LaTeX format checking with Academic Writing Skills.

## Overview

Format checking ensures your LaTeX code follows best practices and venue-specific requirements. Academic Writing Skills integrates ChkTeX and custom checks for comprehensive validation.

## Check Levels

### Quick Check (--quick)

**Execution time**: 1-2 seconds

**Checks**:
- Citation spacing
- Basic punctuation errors
- Section structure
- Common LaTeX mistakes

**Use case**: Rapid iteration during writing

**Example**:
```bash
python check_format.py paper.tex --quick
```

**Output**:
```
Quick Format Check Results
=========================

✓ No citation spacing issues
✗ Line 42: Missing space before \cite
✗ Line 87: Punctuation outside math mode
✓ Section structure valid

2 issues found (2 fixable)
```

### Standard Check (default)

**Execution time**: 5-10 seconds

**Checks**:
- All quick checks
- ChkTeX integration
- Reference consistency
- Label conventions
- Figure/table captions
- Cross-reference validation

**Use case**: Regular validation during writing

**Example**:
```bash
python check_format.py paper.tex
```

**Output**:
```
Standard Format Check Results
============================

ChkTeX Analysis:
  ✗ Line 23: Command terminated with space
  ✗ Line 56: Use \dots instead of ...
  ✓ No undefined references

Label Conventions:
  ✗ Line 78: Label 'fig1' should be 'fig:description'
  ✓ All section labels follow convention

Citation Format:
  ✗ Line 92: Space missing before \cite{key}
  ✓ All citations properly formatted

5 issues found (4 fixable, 1 warning)
```

### Deep Check (--deep)

**Execution time**: 30-60 seconds

**Checks**:
- All standard checks
- Style guide compliance (IEEE/ACM/Springer)
- Advanced grammar patterns
- Consistency checks
- Terminology validation
- Cross-file analysis (for multi-file projects)

**Use case**: Pre-submission validation

**Example**:
```bash
python check_format.py paper.tex --deep
```

**Output**:
```
Deep Format Check Results
========================

Style Guide Compliance (IEEE):
  ✗ Section 3.2: Title should use Title Case
  ✗ Figure 2: Caption should start with "Fig." not "Figure"
  ✓ All tables follow IEEE format

Grammar Patterns:
  ⚠ Line 45: Passive voice detected (consider active)
  ⚠ Line 67: Weak verb "is" (consider stronger alternative)
  ✓ No obvious Chinglish patterns

Consistency:
  ✗ "machine learning" vs "Machine Learning" (inconsistent capitalization)
  ✓ All abbreviations defined on first use

12 issues found (6 fixable, 6 warnings)
```

## Common Issues

### 1. Citation Spacing

**Issue**: Missing space before citation

```latex
% Bad
word\cite{key}

% Good
word \cite{key}
```

**Detection**: Quick check

**Auto-fix**: Yes

### 2. Punctuation in Math Mode

**Issue**: Punctuation outside math mode

```latex
% Bad
The equation is $x = 1$ .

% Good
The equation is $x = 1$.
```

**Detection**: Quick check

**Auto-fix**: Yes

### 3. Label Conventions

**Issue**: Non-descriptive or inconsistent labels

```latex
% Bad
\label{1}
\label{my_figure}
\label{Table1}

% Good
\label{sec:introduction}
\label{fig:architecture}
\label{tab:results}
\label{eq:loss_function}
```

**Detection**: Standard check

**Auto-fix**: No (requires manual review)

**Convention**:
- Sections: `sec:description`
- Figures: `fig:description`
- Tables: `tab:description`
- Equations: `eq:description`

### 4. Section Capitalization

**Issue**: Inconsistent section title capitalization

```latex
% Bad (IEEE style)
\section{introduction and background}

% Good (IEEE style)
\section{Introduction and Background}

% Bad (ACM style)
\section{Introduction And Background}

% Good (ACM style)
\section{Introduction and background}
```

**Detection**: Deep check with `--venue` flag

**Auto-fix**: Yes (with confirmation)

### 5. Figure/Table References

**Issue**: Inconsistent figure/table references

```latex
% Bad
See figure 1
As shown in Figure 1
Refer to fig. 1

% Good (IEEE style)
See Fig.~1
As shown in Fig.~1
Refer to Fig.~1
```

**Detection**: Deep check

**Auto-fix**: Yes

### 6. Undefined References

**Issue**: References to non-existent labels

```latex
See Section~\ref{sec:nonexistent}  % Label doesn't exist
```

**Detection**: Standard check

**Auto-fix**: No (requires adding label or fixing reference)

### 7. Command Spacing

**Issue**: Commands terminated with space

```latex
% Bad
\LaTeX is great

% Good
\LaTeX{} is great
% or
\LaTeX\ is great
```

**Detection**: ChkTeX (standard check)

**Auto-fix**: Yes

### 8. Ellipsis Usage

**Issue**: Using three dots instead of \dots

```latex
% Bad
We have x, y, z, ...

% Good
We have x, y, z, \dots
```

**Detection**: ChkTeX (standard check)

**Auto-fix**: Yes

## Venue-Specific Checks

### IEEE Style

**Enable**:
```bash
python check_format.py paper.tex --venue ieee
```

**Rules**:
1. **Section titles**: Title Case (Each Major Word Capitalized)
   ```latex
   \section{Introduction and Background}  % Correct
   ```

2. **Figure references**: "Fig." in text, "Figure" in captions
   ```latex
   See Fig.~1  % In text
   \caption{Figure 1: Architecture}  % In caption
   ```

3. **Table captions**: "TABLE" in uppercase
   ```latex
   \caption{TABLE I: Results}
   ```

4. **Citations**: Numerical [1], [2], [3]

### ACM Style

**Enable**:
```bash
python check_format.py paper.tex --venue acm
```

**Rules**:
1. **Section titles**: Sentence case (Only first word capitalized)
   ```latex
   \section{Introduction and background}  % Correct
   ```

2. **Figure references**: "Figure" everywhere
   ```latex
   See Figure~1  % In text
   \caption{Figure 1: Architecture}  % In caption
   ```

3. **Table captions**: "Table" (normal case)
   ```latex
   \caption{Table 1: Results}
   ```

4. **Citations**: Numerical [1] or author-year (Smith et al. 2024)

### Springer Style

**Enable**:
```bash
python check_format.py paper.tex --venue springer
```

**Rules**:
1. **Section titles**: Sentence case or Title Case (varies by venue)
   ```latex
   \section{Introduction and background}  % Common
   ```

2. **Figure references**: "Fig." everywhere
   ```latex
   See Fig.~1  % In text
   \caption{Fig. 1: Architecture}  % In caption
   ```

3. **Table captions**: "Table" (normal case)
   ```latex
   \caption{Table 1: Results}
   ```

4. **Citations**: Numerical [1] or author-year

## ChkTeX Integration

### Configuration

ChkTeX can be configured via `.chktexrc`:

```bash
# Create custom config
cat > ~/.chktexrc << 'EOF'
# Suppress warning about \dots
CmdLine { -n 11 }

# Suppress warning about spacing after commands
CmdLine { -n 1 }

# Enable all other warnings
VerbEnvir { verbatim listing }
EOF
```

### Common ChkTeX Warnings

| Code | Warning | Fix |
|------|---------|-----|
| 1 | Command terminated with space | Add `{}` or `\` |
| 8 | Wrong length of dash | Use `--` or `---` |
| 11 | Use `\dots` instead of `...` | Replace with `\dots` |
| 13 | Intersentence spacing | Use `\ ` after abbreviations |
| 17 | Number of `{` doesn't match `}` | Balance braces |
| 24 | Delete this space to maintain correct pagereferences | Remove space before `\ref` |

### Running ChkTeX Manually

```bash
# Basic check
chktex paper.tex

# With custom config
chktex -l ~/.chktexrc paper.tex

# Quiet mode (errors only)
chktex -q paper.tex

# Verbose mode
chktex -v paper.tex
```

## Auto-Fix

### Safe Auto-Fix

Some issues can be automatically fixed:

```bash
python check_format.py paper.tex --fix
```

**Auto-fixable issues**:
- Citation spacing
- Punctuation in math mode
- Command spacing
- Ellipsis usage
- Figure/table reference format (with venue flag)

**Example**:
```bash
$ python check_format.py paper.tex --fix

Auto-fixing 5 issues...
  ✓ Fixed citation spacing (3 instances)
  ✓ Fixed punctuation in math mode (1 instance)
  ✓ Fixed command spacing (1 instance)

5 issues fixed. Please review changes.
```

### Manual Review Required

Some issues require manual review:

- Label naming
- Section title content
- Undefined references
- Terminology consistency

## Batch Checking

### Check Multiple Files

```bash
# Check all .tex files
for file in *.tex; do
  python check_format.py "$file"
done

# Check specific files
python check_format.py intro.tex methods.tex results.tex
```

### Check Multi-File Project

```bash
# Check main file (includes all chapters)
python check_format.py thesis.tex --deep
```

## CI/CD Integration

### GitHub Actions

```yaml
name: LaTeX Format Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          sudo apt-get install texlive-full chktex
          pip install -r requirements.txt

      - name: Format check
        run: |
          python check_format.py paper.tex --output json > results.json

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: format-check-results
          path: results.json
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running LaTeX format check..."
python check_format.py paper.tex --quick

if [ $? -ne 0 ]; then
  echo "Format check failed. Please fix issues before committing."
  exit 1
fi
```

## Output Formats

### Text Output (default)

```bash
python check_format.py paper.tex
```

Human-readable output with colors and formatting.

### JSON Output

```bash
python check_format.py paper.tex --output json
```

Machine-readable output for CI/CD:

```json
{
  "file": "paper.tex",
  "issues": [
    {
      "line": 42,
      "type": "citation_spacing",
      "severity": "error",
      "message": "Missing space before \\cite",
      "fixable": true
    }
  ],
  "summary": {
    "total": 5,
    "errors": 3,
    "warnings": 2,
    "fixable": 4
  }
}
```

### HTML Output

```bash
python check_format.py paper.tex --output html > report.html
```

Formatted HTML report with syntax highlighting.

## Best Practices

### 1. Check Early, Check Often

Run quick checks frequently during writing:

```bash
# After each writing session
python check_format.py paper.tex --quick
```

### 2. Use Appropriate Check Level

- **Draft stage**: Quick check
- **Review stage**: Standard check
- **Pre-submission**: Deep check with venue flag

### 3. Fix Issues Incrementally

Don't accumulate issues:

```bash
# Fix issues as they appear
python check_format.py paper.tex --fix
```

### 4. Use Venue-Specific Checks

Always specify venue for final check:

```bash
python check_format.py paper.tex --deep --venue ieee
```

### 5. Integrate with Editor

Configure your editor to run checks on save:

**VS Code** (`.vscode/tasks.json`):
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "LaTeX Format Check",
      "type": "shell",
      "command": "python check_format.py ${file} --quick",
      "problemMatcher": []
    }
  ]
}
```

## Troubleshooting

### ChkTeX Not Found

**Error**: `chktex: command not found`

**Solution**: Install ChkTeX
```bash
# macOS
brew install chktex

# Ubuntu/Debian
sudo apt-get install chktex

# Windows (MiKTeX)
mpm --install=chktex
```

### False Positives

**Problem**: ChkTeX reports false positives

**Solution**: Suppress specific warnings
```bash
# Suppress warning 11 (dots)
python check_format.py paper.tex --chktex-ignore 11

# Or configure .chktexrc
echo "CmdLine { -n 11 }" >> ~/.chktexrc
```

### Slow Deep Check

**Problem**: Deep check takes too long

**Solution**: Use standard check for regular validation
```bash
# Regular check
python check_format.py paper.tex

# Deep check only before submission
python check_format.py paper.tex --deep --venue ieee
```

## Next Steps

- [Compilation Guide](/guides/compilation) - Compile your documents
- [Bibliography Guide](/guides/bibliography) - Manage references
- [Usage Guide](/usage) - General usage documentation
