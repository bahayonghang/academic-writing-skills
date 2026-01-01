# Academic Writing Skills for Claude Code

[中文版](README_CN.md) | [📚 Documentation](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs)

> LaTeX academic writing assistant skills for Claude Code, supporting both English papers and Chinese theses.

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

## Installation

### Quick Install (Recommended)

Install both skills with a single command:

```bash
# Install English paper skill
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-paper-en.skill.zip

# Install Chinese thesis skill
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-thesis-zh.skill.zip
```

### Manual Installation

#### Option 1: Copy to Claude Code Skills Directory
```bash
# Copy skill folders to your Claude Code skills directory
cp -r .claude/skills/latex-paper-en ~/.claude/skills/
cp -r .claude/skills/latex-thesis-zh ~/.claude/skills/
```

#### Option 2: Use .skill Packages
```bash
# The packaged skills are in the dist/ directory
# Import them using Claude Code's skill import feature
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
├── .claude/skills/
│   ├── latex-paper-en/           # English paper skill
│   │   ├── SKILL.md              # Skill definition
│   │   ├── scripts/              # Python tools
│   │   │   ├── compile.py        # Unified compiler
│   │   │   ├── check_format.py   # ChkTeX wrapper
│   │   │   ├── verify_bib.py     # BibTeX checker
│   │   │   └── extract_prose.py  # Text extractor
│   │   └── references/           # Reference docs
│   │       ├── STYLE_GUIDE.md
│   │       ├── COMMON_ERRORS.md
│   │       ├── VENUES.md
│   │       └── ...
│   │
│   └── latex-thesis-zh/          # Chinese thesis skill
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── compile.py
│       │   ├── map_structure.py  # Thesis structure mapper
│       │   ├── check_format.py
│       │   └── check_consistency.py
│       └── references/
│           ├── GB_STANDARD.md
│           ├── ACADEMIC_STYLE_ZH.md
│           ├── STRUCTURE_GUIDE.md
│           └── UNIVERSITIES/
│               ├── tsinghua.md
│               ├── pku.md
│               └── generic.md
│
└── dist/                         # Packaged skills
    ├── latex-paper-en.skill
    └── latex-thesis-zh.skill
```

## Requirements

- Python 3.8+
- TeX Live or MiKTeX (with latexmk, chktex)
- For Chinese documents: XeLaTeX with CJK fonts

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
