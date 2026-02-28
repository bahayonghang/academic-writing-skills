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
- **Caption Generation & Optimization**: Generate concise, properly-cased, AI-flavor-free figure and table captions 🆕
- **Experiment Analysis**: Generate top-tier experiment analysis paragraphs from raw data/results, with SOTA comparison, ablation analysis, and statistical rigor 🆕
- **De-AI Editing**: Reduce AI writing traces while preserving technical accuracy
- **Venue Support**: IEEE, ACM, Springer, NeurIPS, ICML guidelines
- **Reference Integrity**: Undefined references, unreferenced labels, missing captions detection 🆕
- **Bibliography Verification**: BibTeX format validation with optional online CrossRef/Semantic Scholar verification 🆕

### latex-thesis-zh (Chinese Theses)
- **Structure Mapping**: Multi-file thesis structure analysis
- **GB/T 7714 Compliance**: Chinese national bibliography standard
- **Template Detection**: Support for thuthesis, pkuthss, ustcthesis, fduthesis
- **Chinese Academic Style**: Oral expression detection, terminology consistency
- **Logic & Methodology**: Paragraph coherence (AXES model), transition signals, methodological depth checking 🆕
- **Title Optimization**: Generate and optimize thesis titles following GB/T 7713.1-2006 standards
- **Caption Generation & Optimization**: Generate concise, properly-cased, AI-flavor-free English & bilingual captions 🆕
- **Experiment Analysis**: Generate experiment analysis paragraphs following Chinese core journal standards 🆕
- **De-AI Editing**: Reduce AI writing traces while preserving technical accuracy
- **Compilation**: XeLaTeX/LuaLaTeX with full Chinese support
- **Reference Integrity**: Undefined references, unreferenced labels, missing captions detection 🆕
- **Bibliography Verification**: BibTeX format validation with optional online CrossRef/Semantic Scholar verification 🆕

### typst-paper (Typst Academic Papers)
- **Fast Compilation**: Millisecond-level compilation speed
- **Bilingual Support**: Both English and Chinese papers
- **Format Checking**: Page settings, text formatting, citations
- **Grammar Analysis**: Same as LaTeX version with Typst syntax
- **Logic & Methodology**: Paragraph coherence (AXES model), transition signals, methodological depth checking 🆕
- **De-AI Editing**: Reduce AI writing traces
- **Title Optimization**: Bilingual title generation and optimization (English/Chinese)
- **Caption Generation & Optimization**: Generate concise, properly-cased, AI-flavor-free bilingual captions 🆕
- **Experiment Analysis**: Generate cohesive experiment analysis paragraphs for journal/conference papers 🆕
- **Venue Templates**: IEEE, ACM, Springer, NeurIPS templates
- **Modern Syntax**: Simple, intuitive markup language
- **Reference Integrity**: Undefined references, unreferenced labels, missing captions detection 🆕
- **Bibliography Verification**: BibTeX format validation with optional online CrossRef/Semantic Scholar verification 🆕

### paper-audit (Automated Paper Auditing) 🆕
- **Multi-format Support**: Accepts `.tex`, `.typ`, and `.pdf` files
- **Three Audit Modes**: self-check (comprehensive), review (focused), gate (submission-ready check)
- **PDF Visual Layout Check**: Margin overflow, text/image block overlaps, font inconsistency, low-resolution images, blank pages
- **Reference Integrity Check**: Undefined references, unreferenced labels, missing captions, numbering gaps
- **Caption Audit**: Ensure correct casing (Title/Sentence) and remove AI-like redundancy in captions 🆕
- **Experiment Narrative Audit**: Check whether experiment sections use cohesive paragraph narratives and include ablation/baseline comparisons 🆕
- **ScholarEval Assessment**: 8-dimension quality scoring (1–10) with publication readiness label
- **Online Bibliography Verification**: CrossRef + Semantic Scholar API validation (no API key required)
- **De-AI Editing**: Reduce AI writing traces
- **NeurIPS-aligned Scoring**: Quality/Clarity/Significance/Originality 1–6 scale with weighted report

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

There are two ways to install these skills: using `skilks` (recommended) or manual installation.

### Method 1: Using skilks (Recommended)

You can easily install these skills using [skilks](https://github.com/bahayonghang/skilks), a community skill manager for Claude Code:

```bash
# Install specific skill
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skilks add github.com/bahayonghang/academic-writing-skills/typst-paper
npx skilks add github.com/bahayonghang/academic-writing-skills/paper-audit

# Or install all skills at once
npx skilks add github.com/bahayonghang/academic-writing-skills
```

### Method 2: Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
```

2. Copy the skill folders to your Claude Code skills directory:

#### Linux / macOS

```bash
# Create skills directory (if not exists)
mkdir -p ~/.claude/skills

# Copy skill folders
cp -r latex-paper-en ~/.claude/skills/
cp -r latex-thesis-zh ~/.claude/skills/
cp -r typst-paper ~/.claude/skills/
cp -r paper-audit ~/.claude/skills/
```

#### Windows (PowerShell)

```powershell
# Create skills directory (if not exists)
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force

# Copy skill folders
Copy-Item -Recurse "latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "typst-paper" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "paper-audit" "$env:USERPROFILE/.claude/skills/"
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

**Experiment Analysis** 🆕
- "analyze my experiment data and write results section"
- "generate ablation study analysis"
- "实验分析，生成符合IEEE标准的段落"
- Input: raw data tables/CSV/experiment descriptions
- Output: LaTeX/Typst paragraphs with cohesive narratives

**Caption Optimization** 🆕
- "generate top-tier table captions"
- "optimize this figure caption"
- "generate bilingual caption"
- Follows Title/Sentence case standards and removes redundant AI flavor.

**Paper Audit (Automated)** 🆕
- "run a full audit on my paper"
- "check paper quality before submission"
- "audit my PDF for layout issues"
- Supports .tex, .typ, .pdf files
- Three modes: self-check (full), review (focused), gate (submission gate)
- Add --online for bibliography verification via CrossRef/Semantic Scholar
- Add --scholar-eval for 8-dimension ScholarEval quality assessment

**Reference Integrity** 🆕
- "check figure references in my paper"
- "find undefined labels"
- "检查图表引用完整性"
- Detects: undefined \ref{}, unreferenced \label{}, missing captions, forward references

**📖 For detailed usage and examples, see the [documentation](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs).**

## Project Structure

```
academic-writing-skills/
├── latex-paper-en/                   # English paper skill
│   ├── SKILL.md                      # Skill definition
│   ├── README.md                     # Skill documentation
│   ├── scripts/                      # Python tools
│   │   ├── compile.py                # Unified compiler
│   │   ├── check_format.py           # ChkTeX wrapper
│   │   ├── verify_bib.py             # BibTeX checker
│   │   ├── optimize_title.py         # Title optimizer 🆕
│   │   ├── analyze_experiment.py     # Experiment analyzer 🆕
│   │   ├── check_references.py       # Reference integrity checker 🆕
│   │   ├── online_bib_verify.py      # Online bibliography verifier 🆕
│   │   └── extract_prose.py          # Text extractor
│   └── resources/                    # Skill resources
│       ├── modules/                  # Module instructions
│       │   ├── COMPILE.md
│       │   └── ...
│       └── references/               # Reference docs
│           ├── STYLE_GUIDE.md
│           ├── COMMON_ERRORS.md
│           ├── VENUES.md
│           └── ...
│
├── latex-thesis-zh/                  # Chinese thesis skill
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   │   ├── compile.py
│   │   ├── map_structure.py          # Thesis structure mapper
│   │   ├── check_format.py
│   │   ├── check_consistency.py
│   │   ├── verify_bib.py             # BibTeX checker
│   │   ├── optimize_title.py         # Title optimizer 🆕
│   │   ├── analyze_experiment.py     # Experiment analyzer 🆕
│   │   ├── check_references.py       # Reference integrity checker 🆕
│   │   ├── online_bib_verify.py      # Online bibliography verifier 🆕
│   │   └── detect_template.py        # Template detector
│   └── resources/                    # Skill resources
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
│   │   ├── optimize_title.py         # Title optimizer 🆕
│   │   ├── analyze_experiment.py     # Experiment analyzer 🆕
│   │   ├── check_references.py       # Reference integrity checker 🆕
│   │   └── online_bib_verify.py      # Online bibliography verifier 🆕
│   └── resources/                    # Skill resources
│       ├── modules/                  # Module instructions
│       └── references/               # Reference docs
│           ├── STYLE_GUIDE.md
│           ├── DEAI_GUIDE.md
│           ├── TEMPLATES.md
│           └── TYPST_SYNTAX.md
│
├── paper-audit/                      # Paper audit skill 🆕
│   ├── SKILL.md                      # Skill definition
│   ├── scripts/                      # Python tools
│   │   ├── audit.py                  # Main orchestrator
│   │   ├── pdf_parser.py             # PDF text extraction
│   │   ├── detect_language.py        # Language detection
│   │   ├── report_generator.py       # Report generation
│   │   ├── check_references.py       # Reference integrity checker 🆕
│   │   ├── visual_check.py           # PDF visual layout checker 🆕
│   │   ├── scholar_eval.py           # ScholarEval assessment 🆕
│   │   └── online_bib_verify.py      # Online bib verification (via audit.py)
│   └── resources/
│       └── references/
│           └── SCHOLAR_EVAL_GUIDE.md # ScholarEval scoring guide 🆕
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

Academic Use Only - Not for commercial use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
