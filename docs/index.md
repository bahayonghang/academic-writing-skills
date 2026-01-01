---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Professional LaTeX Tools for Claude Code"
  tagline: "Streamline your academic writing workflow with intelligent LaTeX compilation, format checking, and bibliography management"
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
    details: Comprehensive support for English academic papers with ChkTeX format checking, pdfLaTeX/XeLaTeX compilation, and IEEE/ACM/Springer style guides.

  - icon: 📚
    title: Chinese Thesis (latex-thesis-zh)
    details: Specialized tools for Chinese theses with GB/T 7714 compliance, XeLaTeX compilation, and support for major university templates (Tsinghua, PKU, USTC, Fudan).

  - icon: ⚡
    title: Multiple Compilation Recipes
    details: Flexible compilation workflows including xelatex, pdflatex, latexmk, and full bibliography workflows with BibTeX/Biber.

  - icon: 🔍
    title: Intelligent Format Checking
    details: Automated LaTeX format checking with ChkTeX, bibliography verification, and style guide compliance checking.

  - icon: 🎨
    title: Style Guide Integration
    details: Built-in references for academic writing styles, common Chinglish errors, and venue-specific formatting requirements.

  - icon: 🚀
    title: Easy Installation
    details: One-click installation via command line, seamless integration with Claude Code's skill system.
---

## Quick Start

Install the skills with a single command:

```bash
# Install both skills at once
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-paper-en.skill.zip
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-thesis-zh.skill.zip
```

## Why Academic Writing Skills?

Academic writing with LaTeX can be challenging, especially when managing compilation workflows, bibliography formatting, and style guide compliance. **Academic Writing Skills** brings intelligent automation to your LaTeX workflow:

- **No More Compilation Errors**: Intelligent recipe selection and error diagnosis
- **Style Guide Compliance**: Automated checking against IEEE, ACM, Springer, and GB/T 7714 standards
- **Time-Saving**: Focus on content, not formatting details
- **Best Practices**: Learn proper LaTeX usage through integrated references

## What's Included

### Skills

- **latex-paper-en**: Complete toolkit for English academic papers
- **latex-thesis-zh**: Specialized support for Chinese theses

### Compilation Recipes

Support for all major LaTeX compilation workflows:
- Single-pass compilation (xelatex, pdflatex)
- Automated dependency handling (latexmk)
- Full bibliography workflows (xelatex-biber, pdflatex-bibtex)

### Format Checking

- ChkTeX integration for LaTeX linting
- Bibliography verification (BibTeX format validation)
- Style guide compliance checking

### References

Built-in documentation for:
- Common Chinglish errors in academic writing
- IEEE, ACM, Springer, NeurIPS formatting guidelines
- GB/T 7714-2015 Chinese bibliography standard
- University thesis templates and requirements

## Learn More

- [Installation Guide](/installation) - Detailed installation instructions
- [Quick Start](/quick-start) - Get up and running in minutes
- [Usage Guide](/usage) - Comprehensive usage documentation
- [GitHub Repository](https://github.com/bahayonghang/academic-writing-skills) - Source code and issue tracker

## License

MIT License - Free for academic and commercial use.
