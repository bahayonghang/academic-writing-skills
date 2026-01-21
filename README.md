# Academic Writing Skills for Claude Code

[中文版](README_CN.md) | [📚 Documentation](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs)

> LaTeX academic writing assistant skills for Claude Code, supporting both English papers and Chinese theses.

> **⚠️ Disclaimer**: This is a personal project for my own use. No guarantees are made regarding functionality or stability. If you encounter any issues, please submit them via [Issues](https://github.com/bahayonghang/academic-writing-skills/issues).

## Documentation

**📖 Full documentation is available in the [docs](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs) directory.**

To view the documentation locally:

```bash
cd docs
npm install
npm run docs:dev
```

Then open http://localhost:5173 in your browser.

## Features

### latex-paper-en (English Academic Papers)
- **Format Checking**: ChkTeX integration for LaTeX linting
- **Compilation**: Support for pdfLaTeX/XeLaTeX/LuaLaTeX via latexmk
- **Grammar Analysis**: Chinglish detection, weak verb replacement
- **Sentence Analysis**: Complex sentence decomposition
- **Expression Restructuring**: Academic tone improvements
- **Venue Support**: IEEE, ACM, Springer, NeurIPS, ICML guidelines

### latex-thesis-zh (Chinese Theses)
- **Structure Mapping**: Multi-file thesis structure analysis
- **GB/T 7714 Compliance**: Chinese national bibliography standard
- **Template Detection**: Support for thuthesis, pkuthss, ustcthesis, fduthesis
- **Chinese Academic Style**: Oral expression detection, terminology consistency
- **Compilation**: XeLaTeX/LuaLaTeX with full Chinese support

## Output Protocol

All suggestions use diff-comment style and must include fixed fields:
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

## Failure Handling

- Missing LaTeX tools: install TeX Live/MiKTeX and ensure PATH is set
- Missing file/script: verify working directory and `scripts/` path
- Compilation error: summarize the first error and request the relevant log snippet

## Installation

Copy the skill folders to your Claude Code skills directory:

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

## Quick Start

### Compile Documents

```bash
# Auto-detect compiler
python scripts/compile.py main.tex

# Use specific recipe (VS Code LaTeX Workshop style)
python scripts/compile.py main.tex --recipe xelatex-biber    # Chinese thesis
python scripts/compile.py main.tex --recipe pdflatex-biber   # English paper

# Watch mode (continuous compilation)
python scripts/compile.py main.tex --watch
```

### Available Recipes

| Recipe | Steps | Use Case |
|--------|-------|----------|
| `xelatex` | XeLaTeX only | Quick Chinese compile |
| `pdflatex` | PDFLaTeX only | Quick English compile |
| `latexmk` | LaTeXmk auto | Auto dependency handling |
| `xelatex-bibtex` | xelatex → bibtex → xelatex×2 | Chinese + BibTeX |
| `xelatex-biber` | xelatex → biber → xelatex×2 | Chinese + Biber (Recommended) |
| `pdflatex-bibtex` | pdflatex → bibtex → pdflatex×2 | English + BibTeX |
| `pdflatex-biber` | pdflatex → biber → pdflatex×2 | English + Biber |

### Other Tools

```bash
# Format check
python scripts/check_format.py main.tex

# BibTeX verification
python scripts/verify_bib.py references.bib

# Thesis structure mapping (Chinese thesis only)
python scripts/map_structure.py main.tex

# Terminology consistency check (Chinese thesis only)
python scripts/check_consistency.py main.tex
```

## Project Structure

```
academic-writing-skills/
├── .claude/
│   └── skills/
│       ├── latex-paper-en/           # English paper skill
│       │   ├── SKILL.md              # Skill definition
│       │   ├── scripts/              # Python tools
│       │   │   ├── compile.py        # Unified compiler
│       │   │   ├── check_format.py   # ChkTeX wrapper
│       │   │   ├── verify_bib.py     # BibTeX checker
│       │   │   └── extract_prose.py  # Text extractor
│       │   └── references/           # Reference docs
│       │       ├── STYLE_GUIDE.md
│       │       ├── COMMON_ERRORS.md
│       │       ├── VENUES.md
│       │       └── ...
│       │
│       └── latex-thesis-zh/          # Chinese thesis skill
│           ├── SKILL.md
│           ├── scripts/
│           │   ├── compile.py
│           │   ├── map_structure.py  # Thesis structure mapper
│           │   ├── check_format.py
│           │   └── check_consistency.py
│           └── references/
│               ├── GB_STANDARD.md
│               ├── ACADEMIC_STYLE_ZH.md
│               ├── STRUCTURE_GUIDE.md
│               └── UNIVERSITIES/
│                   ├── tsinghua.md
│                   ├── pku.md
│                   └── generic.md
│
├── docs/                             # Documentation site
│
└── dist/                             # Packaged skills
    ├── latex-paper-en.skill.zip
    └── latex-thesis-zh.skill.zip
```

## Requirements

- Python 3.8+
- TeX Live or MiKTeX (with latexmk, chktex)
- For Chinese documents: XeLaTeX with CJK fonts

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
