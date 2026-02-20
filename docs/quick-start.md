# Quick Start

Get up and running with Academic Writing Skills in minutes.

## Installation

Copy skill folders to Claude Code's skills directory:

### Linux / macOS

```bash
mkdir -p ~/.claude/skills
cp -r academic-writing-skills/latex-paper-en ~/.claude/skills/
cp -r academic-writing-skills/latex-thesis-zh ~/.claude/skills/
cp -r academic-writing-skills/typst-paper ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force
Copy-Item -Recurse "academic-writing-skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/typst-paper" "$env:USERPROFILE/.claude/skills/"
```

## Your First Compilation

### English Paper (LaTeX)

1. **Open your LaTeX project** in Claude Code
2. **Ask Claude to compile**:
   ```
   Please compile main.tex using pdflatex with bibtex
   ```

3. **Check format**:
   ```
   Check the format of main.tex for IEEE submission
   ```

### Chinese Thesis (LaTeX)

1. **Open your LaTeX project** in Claude Code
2. **Map thesis structure**:
   ```
   Map the structure of thesis.tex to check completeness
   ```

3. **Compile with XeLaTeX**:
   ```
   Compile thesis.tex using xelatex with biber
   ```

4. **Check GB/T 7714 compliance**:
   ```
   Verify references.bib for GB7714 compliance
   ```

### Typst Paper 🆕

1. **Install Typst** (if not already installed):
   ```bash
   # Using Cargo
   cargo install typst-cli
   
   # Using Homebrew (macOS)
   brew install typst
   ```

2. **Ask Claude to compile**:
   ```
   Compile main.typ using Typst
   ```

3. **Use watch mode for live preview**:
   ```
   Start Typst watch mode for main.typ
   ```

4. **Check format**:
   ```
   Check the format of main.typ for IEEE conference submission
   ```

## Common Workflows

### Workflow 1: Quick Paper Draft (LaTeX)

Perfect for rapid iteration:

```
Compile paper.tex with pdflatex and check for common errors
```

### Workflow 2: Quick Paper Draft (Typst) 🆕

Lightning-fast compilation:

```
Compile paper.typ with Typst and check format
```

### Workflow 3: Final Submission (LaTeX)

For publication-ready output:

```
Compile paper.tex with pdflatex and biber, then check format and verify bibliography
```

### Workflow 4: Final Submission (Typst) 🆕

Modern workflow:

```
Compile paper.typ with Typst, check format for IEEE submission, and verify bibliography
```

### Workflow 5: Chinese Thesis

Complete thesis workflow:

```
Please perform a complete thesis review:
1. Map the structure of thesis.tex
2. Compile with xelatex and biber
3. Check refs.bib for GB7714 compliance
4. Check consistency across chapters
```

## Understanding Compilation Options

Academic Writing Skills supports multiple compilation options:

### LaTeX Recipes

| Recipe | Use Case | Speed |
|--------|----------|-------|
| `pdflatex` | English-only papers, fastest | ⚡⚡⚡ |
| `xelatex` | Unicode, Chinese, custom fonts | ⚡⚡ |
| `latexmk` | Auto dependency handling | ⚡ |
| `pdflatex-bibtex` | English + BibTeX refs | ⚡⚡ |
| `xelatex-biber` | Chinese + modern refs | ⚡ |

### Typst Compilation 🆕

| Command | Use Case | Speed |
|---------|----------|-------|
| `typst compile` | Single compilation | ⚡⚡⚡⚡ (milliseconds) |
| `typst watch` | Live preview | ⚡⚡⚡⚡ (auto-recompile) |
| `typst compile --format png` | Export as image | ⚡⚡⚡ |

Choose based on your needs:
- **Speed**: Typst > pdflatex > xelatex
- **Unicode/Chinese**: xelatex, lualatex, or Typst
- **Modern bibliography**: biber (LaTeX) or Hayagriva (Typst)
- **Live preview**: Typst watch mode

## Working with Claude Code

### Interactive Mode

Use skills interactively within Claude Code:

**LaTeX Example**:
```
You: Compile my paper with XeLaTeX and check for format errors

Claude: I'll compile your paper using xelatex and run format checks.

[Runs compilation and format checking]

Claude: Compilation successful! Found 3 minor format issues:
1. Line 42: \cite command spacing
2. Line 87: Inconsistent capitalization in section title
3. Line 120: Missing space after period
```

**Typst Example** 🆕:
```
You: Compile my Typst paper and start watch mode

Claude: I'll compile your paper with Typst and start watch mode for live preview.

[Runs compilation]

Claude: Compilation successful in 15ms! Watch mode started - your paper will auto-recompile on changes.
```

### Automated Workflows

Simply ask Claude to perform multi-step workflows:

**LaTeX workflow**:
```
Please compile paper.tex with pdflatex and biber, check format, and verify bibliography
```

**Typst workflow** 🆕:
```
Please compile paper.typ with Typst, check format for ACM submission, and verify citations
```

## Tips for Success

### 1. Choose the Right Tool

**LaTeX**:
- Mature ecosystem with extensive packages
- Required by some journals/conferences
- Slower compilation (seconds)

**Typst** 🆕:
- Modern syntax, easier to learn
- Lightning-fast compilation (milliseconds)
- Great for rapid iteration
- Growing ecosystem

### 2. Use the Right Compilation Method

**English papers (LaTeX)**:
- Start with `pdflatex` for speed
- Switch to `xelatex` if you need Unicode characters

**Chinese thesis (LaTeX)**:
- Always use `xelatex` or `lualatex`
- Use `biber` for modern bibliography (GB/T 7714)

**Any paper (Typst)** 🆕:
- Use `typst compile` for single compilation
- Use `typst watch` for live preview during writing

### 3. Check Early, Check Often

Ask Claude to check your work frequently:

```
Check the format of my paper
```

```
Proofread my introduction section for grammar errors
```

### 4. Understand Your Template

For Chinese theses, map the structure first:

```
Map the structure of thesis.tex
```

This helps identify:
- University template (Tsinghua, PKU, USTC, Fudan, generic)
- Main file and chapter structure
- Required vs. optional components

### 5. Keep Bibliography Clean

Verify bibliography format before final submission:

```
Verify references.bib for format errors
```

```
Check refs.bib for GB7714 compliance
```

## Common Issues

### LaTeX Compilation Fails

**Error**: `! LaTeX Error: File 'xxx.sty' not found`

**Solution**: Install missing package:
```bash
# TeX Live
tlmgr install <package-name>

# MiKTeX
mpm --install=<package-name>
```

### Typst Not Found 🆕

**Error**: `typst: command not found`

**Solution**: Install Typst:
```bash
# Using Cargo
cargo install typst-cli

# Using Homebrew (macOS)
brew install typst

# Using package manager (Linux)
sudo pacman -S typst  # Arch Linux
```

### Bibliography Not Showing (LaTeX)

**Error**: Bibliography section is empty

**Solution**: Ask Claude to compile with the full workflow:
```
Compile paper.tex with pdflatex and bibtex workflow
```

### Chinese Characters Not Displaying (LaTeX)

**Error**: Chinese text shows as boxes or errors

**Solution**: Use XeLaTeX:
```
Compile thesis.tex using xelatex
```

### Typst Font Issues 🆕

**Error**: Font not found

**Solution**: Check available fonts:
```bash
typst fonts
```

Then configure your document to use available fonts.

## Next Steps

- [Full Usage Guide](/usage) - Detailed feature documentation
- [English Paper Modules](/skills/latex-paper-en/) - LaTeX English paper workflow and core modules
- [Chinese Thesis Resources](/skills/latex-thesis-zh/) - Chinese thesis structure and format check
- [Typst Paper Modules](/skills/typst-paper/) - Typst paper workflow and core modules

## Need Help?

- **Documentation**: Browse skill-specific guides
- **Examples**: Check `.claude/skills/*/references/` for examples
- **Issues**: [GitHub Issues](https://github.com/bahayonghang/academic-writing-skills/issues)
