# Quick Start

Get up and running with Academic Writing Skills in minutes.

## Installation

Copy skill folders to your Claude Code skills directory:

### Linux / macOS

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/latex-paper-en ~/.claude/skills/
cp -r .claude/skills/latex-thesis-zh ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force
Copy-Item -Recurse ".claude/skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse ".claude/skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
```

## Your First Compilation

### English Paper

1. **Open your LaTeX project** in Claude Code
2. **Compile your paper**:
   ```bash
   # Simple compilation with pdfLaTeX
   python ~/.claude/skills/latex-paper-en/scripts/compile.py main.tex

   # Or with XeLaTeX
   python ~/.claude/skills/latex-paper-en/scripts/compile.py main.tex --recipe xelatex

   # Full workflow with bibliography
   python ~/.claude/skills/latex-paper-en/scripts/compile.py main.tex --recipe pdflatex-bibtex
   ```

3. **Check format**:
   ```bash
   python ~/.claude/skills/latex-paper-en/scripts/check_format.py main.tex
   ```

### Chinese Thesis

1. **Open your LaTeX project** in Claude Code
2. **Map thesis structure**:
   ```bash
   python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py main.tex
   ```

3. **Compile with XeLaTeX**:
   ```bash
   python ~/.claude/skills/latex-thesis-zh/scripts/compile.py main.tex --recipe xelatex-biber
   ```

4. **Check GB/T 7714 compliance**:
   ```bash
   python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py references.bib
   ```

## Common Workflows

### Workflow 1: Quick Paper Draft

Perfect for rapid iteration:

```bash
# Compile with pdfLaTeX (fastest)
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex

# Check for common errors
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex
```

### Workflow 2: Final Submission

For publication-ready output:

```bash
# Full compilation with bibliography
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-biber

# Format check
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex

# Bibliography verification
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib
```

### Workflow 3: Chinese Thesis

Complete thesis workflow:

```bash
# 1. Map structure (identifies template and chapters)
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex

# 2. Compile with XeLaTeX and Biber
python ~/.claude/skills/latex-thesis-zh/scripts/compile.py thesis.tex --recipe xelatex-biber

# 3. Check GB/T 7714 compliance
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py refs.bib

# 4. Check terminology consistency
python ~/.claude/skills/latex-thesis-zh/scripts/check_consistency.py data/
```

## Understanding Compilation Recipes

Academic Writing Skills supports multiple compilation recipes:

| Recipe | Use Case | Speed |
|--------|----------|-------|
| `pdflatex` | English-only papers, fastest | ⚡⚡⚡ |
| `xelatex` | Unicode, Chinese, custom fonts | ⚡⚡ |
| `latexmk` | Auto dependency handling | ⚡ |
| `pdflatex-bibtex` | English + BibTeX refs | ⚡⚡ |
| `xelatex-biber` | Chinese + modern refs | ⚡ |

Choose based on your needs:
- **Speed**: pdflatex
- **Unicode/Chinese**: xelatex or lualatex
- **Modern bibliography**: biber
- **Auto dependencies**: latexmk

## Working with Claude Code

### Interactive Mode

Use skills interactively within Claude Code:

```
You: Compile my paper with XeLaTeX and check for format errors

Claude: I'll compile your paper using the xelatex recipe and run format checks.

[Runs compilation and format checking]

Claude: Compilation successful! Found 3 minor format issues:
1. Line 42: \cite command spacing
2. Line 87: Inconsistent capitalization in section title
3. Line 120: Missing space after period
```

### Automated Workflows

Create automated workflows for common tasks:

```bash
# Create a compilation script
cat > compile_all.sh << 'EOF'
#!/bin/bash
echo "Compiling paper..."
python ~/.claude/skills/latex-paper-en/scripts/compile.py paper.tex --recipe pdflatex-biber

echo "Checking format..."
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex

echo "Verifying bibliography..."
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib

echo "Done!"
EOF

chmod +x compile_all.sh
./compile_all.sh
```

## Tips for Success

### 1. Use the Right Recipe

**English papers**:
- Start with `pdflatex` for speed
- Switch to `xelatex` if you need Unicode characters

**Chinese thesis**:
- Always use `xelatex` or `lualatex`
- Use `biber` for modern bibliography (GB/T 7714)

### 2. Check Early, Check Often

Run format checks frequently to catch issues early:

```bash
# Quick format check (fast)
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex --quick

# Full format check (thorough)
python ~/.claude/skills/latex-paper-en/scripts/check_format.py paper.tex
```

### 3. Understand Your Template

For Chinese theses, map the structure first:

```bash
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
```

This helps identify:
- University template (Tsinghua, PKU, USTC, Fudan, generic)
- Main file and chapter structure
- Required vs. optional components

### 4. Keep Bibliography Clean

Verify bibliography format before final submission:

```bash
# Check BibTeX format
python ~/.claude/skills/latex-paper-en/scripts/verify_bib.py references.bib

# Check GB/T 7714 compliance (Chinese)
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gbt7714
```

## Common Issues

### Compilation Fails

**Error**: `! LaTeX Error: File 'xxx.sty' not found`

**Solution**: Install missing package:
```bash
# TeX Live
tlmgr install <package-name>

# MiKTeX
mpm --install=<package-name>
```

### Bibliography Not Showing

**Error**: Bibliography section is empty

**Solution**: Use the correct full recipe:
```bash
# For BibTeX
python compile.py paper.tex --recipe pdflatex-bibtex

# For Biber
python compile.py paper.tex --recipe xelatex-biber
```

### Chinese Characters Not Displaying

**Error**: Chinese text shows as boxes or errors

**Solution**: Use XeLaTeX or LuaLaTeX:
```bash
python compile.py thesis.tex --recipe xelatex
```

## Next Steps

- [Full Usage Guide](/usage) - Detailed feature documentation
- [Compilation Recipes](/guides/compilation) - Deep dive into recipes
- [Format Checking](/guides/format-checking) - Understanding format checks
- [Bibliography Management](/guides/bibliography) - Managing references

## Need Help?

- **Documentation**: Browse skill-specific guides
- **Examples**: Check `.claude/skills/*/references/` for examples
- **Issues**: [GitHub Issues](https://github.com/bahayonghang/academic-writing-skills/issues)
