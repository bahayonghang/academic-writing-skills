# Installation

## Prerequisites

Before installing Academic Writing Skills, ensure you have:

1. **Claude Code CLI**: The official Claude Code command-line interface
2. **LaTeX Distribution**: A working LaTeX installation
   - **macOS**: [MacTeX](https://www.tug.org/mactex/)
   - **Windows**: [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)
   - **Linux**: TeX Live (via package manager)
3. **Python 3.6+**: Required for skill scripts

### Verifying Prerequisites

```bash
# Check Claude Code
claude --version

# Check LaTeX
pdflatex --version
xelatex --version

# Check Python
python --version  # or python3 --version
```

## Installation Methods

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bahayonghang/academic-writing-skills.git
   cd academic-writing-skills
   ```

2. **Copy skills to Claude Code's skills directory**:

### Linux / macOS

```bash
# Create skills directory (if not exists)
mkdir -p ~/.claude/skills

# Copy skill folders
cp -r .claude/skills/latex-paper-en ~/.claude/skills/
cp -r .claude/skills/latex-thesis-zh ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
# Create skills directory (if not exists)
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force

# Copy skill folders
Copy-Item -Recurse ".claude/skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse ".claude/skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
```

### Windows (CMD)

```cmd
:: Create skills directory (if not exists)
mkdir "%USERPROFILE%\.claude\skills"

:: Copy skill folders
xcopy /E /I ".claude\skills\latex-paper-en" "%USERPROFILE%\.claude\skills\latex-paper-en"
xcopy /E /I ".claude\skills\latex-thesis-zh" "%USERPROFILE%\.claude\skills\latex-thesis-zh"
```

## Verifying Installation

After installation, verify the skills are available by checking the directory:

```bash
# Linux / macOS
ls ~/.claude/skills/

# Windows (PowerShell)
Get-ChildItem "$env:USERPROFILE/.claude/skills"

# You should see:
# - latex-paper-en
# - latex-thesis-zh
```

## Installing Optional Dependencies

### ChkTeX (Recommended)

ChkTeX provides LaTeX format checking:

```bash
# macOS (via Homebrew)
brew install chktex

# Ubuntu/Debian
sudo apt-get install chktex

# Windows (via MiKTeX)
mpm --install=chktex
```

### latexmk (Recommended)

latexmk automates LaTeX compilation with dependency tracking:

```bash
# Usually included with TeX Live/MacTeX
# If not available:

# macOS (via Homebrew)
brew install latexmk

# Ubuntu/Debian
sudo apt-get install latexmk

# Windows
# Included with MiKTeX and TeX Live
```

### Biber (For Modern Bibliography)

Biber is the modern BibLaTeX backend:

```bash
# Usually included with TeX Live/MacTeX
# If not available:

# macOS (via Homebrew)
brew install biber

# Ubuntu/Debian
sudo apt-get install biber

# Windows
# Included with MiKTeX and TeX Live
```

## Configuration

### LaTeX Compiler Priority

The skills will automatically detect and use available compilers in this order:

**For English Papers (latex-paper-en)**:
1. pdfLaTeX (recommended for English-only papers)
2. XeLaTeX (for Unicode/international characters)
3. LuaLaTeX (alternative to XeLaTeX)

**For Chinese Thesis (latex-thesis-zh)**:
1. XeLaTeX (recommended for Chinese documents)
2. LuaLaTeX (alternative for Chinese)
3. pdfLaTeX (not recommended for Chinese)

### Custom Configuration

You can customize skill behavior by editing the skill files:

```bash
# Edit English paper skill configuration
nano ~/.claude/skills/latex-paper-en/SKILL.md

# Edit Chinese thesis skill configuration
nano ~/.claude/skills/latex-thesis-zh/SKILL.md
```

## Updating

To update to the latest version, re-clone the repository and copy the skill folders again:

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills

# Then copy skills using the commands above for your platform
```

## Uninstalling

To remove the skills:

### Linux / macOS

```bash
rm -rf ~/.claude/skills/latex-paper-en
rm -rf ~/.claude/skills/latex-thesis-zh
```

### Windows (PowerShell)

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE/.claude/skills/latex-paper-en"
Remove-Item -Recurse -Force "$env:USERPROFILE/.claude/skills/latex-thesis-zh"
```

## Troubleshooting

### "Skill not found" error

**Problem**: `claude skill install` fails with "skill not found"

**Solution**:
1. Verify your internet connection
2. Check that the GitHub URL is correct
3. Try downloading the `.skill.zip` file manually and installing locally

### "LaTeX not found" error

**Problem**: Compilation fails with "command not found: pdflatex"

**Solution**:
1. Verify LaTeX is installed: `which pdflatex`
2. Add LaTeX to your PATH:
   ```bash
   # macOS (MacTeX)
   export PATH="/usr/local/texlive/2024/bin/universal-darwin:$PATH"

   # Linux (TeX Live)
   export PATH="/usr/local/texlive/2024/bin/x86_64-linux:$PATH"
   ```

### "Python not found" error

**Problem**: Skill scripts fail with "python: command not found"

**Solution**:
1. Install Python 3.6+
2. Create a symlink: `ln -s /usr/bin/python3 /usr/local/bin/python`
3. Or use `python3` explicitly in skill scripts

### Permission denied errors

**Problem**: Installation fails with "permission denied"

**Solution**:
```bash
# Fix permissions
chmod -R 755 ~/.claude/skills/

# Or use sudo for system-wide installation
sudo claude skill install ...
```

## Next Steps

- [Quick Start Guide](/quick-start) - Get started in minutes
- [Usage Guide](/usage) - Learn how to use the skills
- [Compilation Recipes](/guides/compilation) - Understand compilation workflows

## Getting Help

- **Documentation**: Browse this site for guides and references
- **GitHub Issues**: [Report bugs or request features](https://github.com/bahayonghang/academic-writing-skills/issues)
- **Community**: Join discussions on GitHub
