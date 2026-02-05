# Academic Writing Skills for Claude Code

[中文版](README_CN.md) | [📚 Documentation](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs)

> Academic writing assistant skills for Claude Code, supporting LaTeX and Typst for both English papers and Chinese theses.

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
- **Logic & Methodology**: Paragraph coherence (AXES model), transition signals, methodological depth checking 🆕
- **Title Optimization**: Generate and optimize paper titles following IEEE/ACM/Springer best practices
- **De-AI Editing**: Reduce AI writing traces while preserving technical accuracy
- **Venue Support**: IEEE, ACM, Springer, NeurIPS, ICML guidelines

### latex-thesis-zh (Chinese Theses)
- **Structure Mapping**: Multi-file thesis structure analysis
- **GB/T 7714 Compliance**: Chinese national bibliography standard
- **Template Detection**: Support for thuthesis, pkuthss, ustcthesis, fduthesis
- **Chinese Academic Style**: Oral expression detection, terminology consistency
- **Logic & Methodology**: Paragraph coherence (AXES model), transition signals, methodological depth checking 🆕
- **Title Optimization**: Generate and optimize thesis titles following GB/T 7713.1-2006 standards
- **De-AI Editing**: Reduce AI writing traces while preserving technical accuracy
- **Compilation**: XeLaTeX/LuaLaTeX with full Chinese support

### typst-paper (Typst Academic Papers)
- **Fast Compilation**: Millisecond-level compilation speed
- **Bilingual Support**: Both English and Chinese papers
- **Format Checking**: Page settings, text formatting, citations
- **Grammar Analysis**: Same as LaTeX version with Typst syntax
- **Logic & Methodology**: Paragraph coherence (AXES model), transition signals, methodological depth checking 🆕
- **De-AI Editing**: Reduce AI writing traces
- **Title Optimization**: Bilingual title generation and optimization (English/Chinese)
- **Venue Templates**: IEEE, ACM, Springer, NeurIPS templates
- **Modern Syntax**: Simple, intuitive markup language

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
cp -r academic-writing-skills/latex-paper-en ~/.claude/skills/
cp -r academic-writing-skills/latex-thesis-zh ~/.claude/skills/
cp -r academic-writing-skills/typst-paper ~/.claude/skills/
```

### Windows (PowerShell)

```powershell
# Create skills directory (if not exists)
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force

# Copy skill folders
Copy-Item -Recurse "academic-writing-skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/typst-paper" "$env:USERPROFILE/.claude/skills/"
```

### Windows (CMD)

```cmd
:: Create skills directory (if not exists)
mkdir "%USERPROFILE%\.claude\skills"

:: Copy skill folders
xcopy /E /I "academic-writing-skills\latex-paper-en" "%USERPROFILE%\.claude\skills\latex-paper-en"
xcopy /E /I "academic-writing-skills\latex-thesis-zh" "%USERPROFILE%\.claude\skills\latex-thesis-zh"
xcopy /E /I "academic-writing-skills\typst-paper" "%USERPROFILE%\.claude\skills\typst-paper"
```

## Quick Start

Simply chat with Claude Code and mention your needs. The skills will be automatically triggered based on keywords.

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

### Common Use Cases

**Compilation**
- "compile my paper with xelatex-biber"
- "build the LaTeX document"
- "编译我的论文"

**Translation (Chinese → English)**
- "translate this section to English"
- "中译英这段文字"
- Automatically detects domain terminology (Deep Learning, Time Series, Industrial Control)
- Checks for Chinglish patterns and suggests improvements

**De-AI Editing (Reduce AI Writing Traces)**
- "deai check my introduction"
- "去AI化这段文字"
- "humanize this paragraph"
- Removes empty phrases, over-confident expressions, and mechanical structures
- Preserves all LaTeX/Typst syntax and citations

**Grammar & Style**
- "check grammar in abstract"
- "improve academic tone"
- "检查语法错误"
- Detects subject-verb agreement, article usage, tense consistency
- Suggests academic expression improvements

**Format Checking**
- "check format compliance"
- "verify GB/T 7714 standard" (Chinese thesis)
- "格式检查"

**Bibliography**
- "verify my bibliography"
- "check citation consistency"
- "检查参考文献"

**Long Sentence Analysis**
- "simplify this complex sentence"
- "拆解长难句"
- Automatically triggers for sentences >50 words (English) or >60 characters (Chinese)

**Logic & Methodology** 🆕
- "check logical coherence in my introduction"
- "analyze methodological depth"
- "检查逻辑衔接"
- "分析方法论深度"
- Uses AXES model (Assertion, eXample, Explanation, Significance) for paragraph coherence
- Checks transition signals and methodological rigor

**Title Optimization**
- "optimize my paper title"
- "generate title candidates"
- "优化论文标题"
- "生成标题方案"
- Follows IEEE/ACM/Springer/NeurIPS best practices
- Removes ineffective words ("Novel", "A Study of", "Research on")
- Ensures key terms (Method + Problem) appear in first 65 characters (English) or 20 characters (Chinese)
- Provides multiple candidates with quality scores (0-100)

**📖 For detailed usage and examples, see the [documentation](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs).**

## Project Structure

```
academic-writing-skills/
├── latex-paper-en/                   # English paper skill
│   ├── SKILL.md                      # Skill definition
│   ├── scripts/                      # Python tools
│   │   ├── compile.py                # Unified compiler
│   │   ├── check_format.py           # ChkTeX wrapper
│   │   ├── verify_bib.py             # BibTeX checker
│   │   ├── optimize_title.py         # Title optimizer 🆕
│   │   └── extract_prose.py          # Text extractor
│   └── references/                   # Reference docs
│       ├── STYLE_GUIDE.md
│       ├── COMMON_ERRORS.md
│       ├── VENUES.md
│       └── ...
│
├── latex-thesis-zh/                  # Chinese thesis skill
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── compile.py
│   │   ├── map_structure.py          # Thesis structure mapper
│   │   ├── check_format.py
│   │   ├── check_consistency.py
│   │   ├── verify_bib.py             # BibTeX checker
│   │   ├── optimize_title.py         # Title optimizer 🆕
│   │   └── detect_template.py        # Template detector
│   └── references/
│       ├── GB_STANDARD.md
│       ├── ACADEMIC_STYLE_ZH.md
│       ├── STRUCTURE_GUIDE.md
│       └── UNIVERSITIES/
│           ├── tsinghua.md
│           ├── pku.md
│           ├── yanshan.md
│           └── generic.md
│
├── typst-paper/                      # Typst paper skill 🆕
│   ├── SKILL.md                      # Skill definition
│   ├── README.md                     # Usage guide
│   ├── scripts/                      # Python tools
│   │   ├── compile.py                # Typst compiler
│   │   ├── check_format.py           # Format checker
│   │   ├── verify_bib.py             # Bibliography checker
│   │   └── optimize_title.py         # Title optimizer 🆕
│   └── references/                   # Reference docs
│       ├── STYLE_GUIDE.md
│       ├── COMMON_ERRORS.md
│       ├── DEAI_GUIDE.md
│       ├── VENUES.md
│       ├── TEMPLATES.md
│       └── TYPST_SYNTAX.md
│
└── docs/                             # Documentation site
```

## Requirements

### For LaTeX
- Python 3.8+
- TeX Live or MiKTeX (with latexmk, chktex)
- For Chinese documents: XeLaTeX with CJK fonts

### For Typst 🆕
- Python 3.8+
- Typst CLI (install via `cargo install typst-cli` or package manager)
- For Chinese documents: Chinese fonts (Source Han Serif, Noto Serif CJK SC)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
