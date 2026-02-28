---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Professional LaTeX & Typst Tools for Claude Code"
  tagline: "Streamline your academic writing workflow with intelligent compilation, format checking, and bibliography management"
  actions:
    - theme: brand
      text: Get Started
      link: /installation
    - theme: alt
      text: View on GitHub
      link: https://github.com/bahayonghang/academic-writing-skills

features:
  - icon: 📝
    title: English Papers (latex-paper-en)
    details: Comprehensive support for English academic papers with ChkTeX format checking, pdfLaTeX/XeLaTeX compilation, logic & methodology analysis, top-tier caption generation, and IEEE/ACM/Springer style guides.

  - icon: 📚
    title: Chinese Thesis (latex-thesis-zh)
    details: Specialized tools for Chinese theses with GB/T 7714 compliance, XeLaTeX compilation, logic & methodology analysis, bilingual caption generation, and support for major university templates (Tsinghua, PKU, USTC, Fudan).

  - icon: ⚡
    title: Typst Papers (typst-paper)
    details: Modern markup language with millisecond compilation, bilingual support, logic & methodology analysis, caption generation, and venue-specific templates (IEEE, ACM, Springer, NeurIPS).

  - icon: 🚀
    title: Fast Compilation
    details: Flexible compilation workflows including xelatex, pdflatex, latexmk for LaTeX, and lightning-fast Typst compilation with watch mode.

  - icon: 🔍
    title: Intelligent Format Checking
    details: Automated format checking with ChkTeX for LaTeX, Typst syntax validation, bibliography verification, and style guide compliance.

  - icon: 🎨
    title: De-AI Editing
    details: Reduce AI writing traces while preserving technical accuracy. Built-in references for academic writing styles and common errors.

  - icon: 🔬
    title: Paper Audit (paper-audit)
    details: Automated multi-mode paper auditing for .tex/.typ/.pdf files. PDF visual layout checking, figure/table reference integrity, caption audit, ScholarEval 8-dimension quality scoring, and online bibliography verification via CrossRef/Semantic Scholar.
---

## Quick Start

Install the skills with a single command:

```bash
# Install specific skill
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skilks add github.com/bahayonghang/academic-writing-skills/typst-paper

# Or install all skills at once
npx skilks add github.com/bahayonghang/academic-writing-skills
```

## Why Academic Writing Skills?

Academic writing can be challenging, especially when managing compilation workflows, bibliography formatting, and style guide compliance. **Academic Writing Skills** brings intelligent automation to your workflow:

- **No More Compilation Errors**: Intelligent recipe selection and error diagnosis
- **Fast Compilation**: Typst compiles in milliseconds vs LaTeX's seconds
- **Style Guide Compliance**: Automated checking against IEEE, ACM, Springer, and GB/T 7714 standards
- **Time-Saving**: Focus on content, not formatting details
- **Best Practices**: Learn proper usage through integrated references

## What's Included

### Skills

- **latex-paper-en**: Complete toolkit for English academic papers (LaTeX)
- **latex-thesis-zh**: Specialized support for Chinese theses (LaTeX)
- **typst-paper**: Modern markup language for fast academic writing 🆕
- **paper-audit**: Automated paper auditing with PDF support, visual checks, and ScholarEval 🆕

### Compilation Support

**LaTeX**:
- Single-pass compilation (xelatex, pdflatex)
- Automated dependency handling (latexmk)
- Full bibliography workflows (xelatex-biber, pdflatex-bibtex)

**Typst** 🆕:
- Millisecond-level compilation
- Watch mode for live preview
- Multiple output formats (PDF, PNG, SVG)

### Format Checking

- ChkTeX integration for LaTeX linting
- Typst syntax validation
- Bibliography verification (BibTeX/Hayagriva)
- Style guide compliance checking
- Reference integrity checking (undefined refs, missing/poor captions)
- PDF visual layout analysis (margins, overlaps, image DPI)

### References

Built-in documentation for:
- Common Chinglish errors in academic writing
- IEEE, ACM, Springer, NeurIPS formatting guidelines
- GB/T 7714-2015 Chinese bibliography standard
- University thesis templates and requirements
- Typst syntax reference and best practices

### Paper Quality Assessment 🆕

- **ScholarEval**: 8-dimension academic quality scoring (1-10 scale)
- **Publication Readiness Labels**: Strong Accept → Not ready
- **Online Bibliography Verification**: CrossRef + Semantic Scholar API
- **PDF Visual Analysis**: Layout issues for camera-ready submissions

## Learn More

- [Installation Guide](/installation) - Detailed installation instructions
- [Quick Start](/quick-start) - Get up and running in minutes
- [Usage Guide](/usage) - Comprehensive usage documentation
- [GitHub Repository](https://github.com/bahayonghang/academic-writing-skills) - Source code and issue tracker

## License

Academic Use Only - Not for commercial use.
