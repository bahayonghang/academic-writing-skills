# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic writing assistant skills for Claude Code, supporting LaTeX and Typst for English papers and Chinese theses. The project provides three independent skills: `latex-paper-en` (English academic papers), `latex-thesis-zh` (Chinese theses), and `typst-paper` (Typst papers).

## Build & Test Commands

```bash
# Run all tests
python -m unittest

# Run a single test file
python -m unittest tests/test_parsers.py

# Documentation site (VitePress)
cd docs && npm install && npm run docs:dev     # Dev server at http://localhost:5173
cd docs && npm run docs:build                  # Build for production
cd docs && npm run docs:preview                # Preview production build

# Optional: use just shortcuts
cd docs && just build
cd docs && just check-links
```

## Skill Script Usage

Each skill has Python scripts in its `scripts/` directory. Run from the repository root:

```bash
# LaTeX compilation (auto-detects Chinese content for XeLaTeX)
python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex
python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex --recipe xelatex-biber

# Format checking
python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex --strict

# Bibliography verification
python academic-writing-skills/latex-paper-en/scripts/verify_bib.py references.bib --tex main.tex

# Typst compilation (millisecond-level speed)
typst compile main.typ
typst watch main.typ  # Real-time preview
```

## Architecture

```
academic-writing-skills/
├── latex-paper-en/          # English paper skill
│   ├── SKILL.md             # Skill definition (triggers, modules, output protocol)
│   ├── scripts/             # Python tools (compile.py, check_format.py, parsers.py)
│   └── references/          # Style guides, venue rules, forbidden terms
├── latex-thesis-zh/         # Chinese thesis skill (GB/T 7714, university templates)
│   ├── SKILL.md
│   ├── scripts/             # Includes map_structure.py, detect_template.py
│   └── references/          # GB standards, university-specific guides
├── typst-paper/             # Typst paper skill
│   ├── SKILL.md
│   ├── scripts/
│   └── references/          # Typst syntax, templates
├── tests/                   # Unit tests (unittest)
└── docs/                    # VitePress documentation (localized in docs/zh/)
```

### Skill Definition Pattern (SKILL.md)

Each skill follows a standardized structure:
1. **YAML frontmatter**: `name`, `description`, trigger keywords
2. **Critical Rules**: Protected elements (never modify `\cite{}`, `\ref{}`, `\label{}`, math environments)
3. **Modules**: Independent modules triggered by keywords (Compile, Format Check, Grammar, De-AI, etc.)
4. **Output Protocol**: All suggestions use diff-comment format with `Severity` and `Priority` fields
5. **References**: Links to detailed guides in `references/`

### Shared Parsers

`parsers.py` provides `LatexParser` and `TypstParser` classes for:
- Section splitting (`split_sections`)
- Visible text extraction (`extract_visible_text`)
- Text cleaning (`clean_text` - removes commands, math, comments)

## Content Safety Rules

- **NEVER** modify: `\cite{}`, `\ref{}`, `\label{}` in LaTeX; `@cite`, `@ref`, `@label` in Typst; math environments
- **NEVER** fabricate bibliography entries; only use existing `.bib` or `.yml` files
- **NEVER** change domain terminology without user confirmation
- Check `references/FORBIDDEN_TERMS.md` before modifying protected terms

## Commit Style

Follow the existing pattern: `emoji type(scope): message`
- `:sparkles: feat(scope):` - New feature
- `:memo: docs:` - Documentation
- `:bug: fix:` - Bug fix
- `:recycle: refactor:` - Refactoring
- `:white_check_mark: test:` - Tests

## Key Dependencies

- Python 3.9+ with Pillow
- LaTeX: TeX Live or MiKTeX (with latexmk, chktex, XeLaTeX for Chinese)
- Typst: `typst-cli` (via cargo or package manager)
- Docs: Node.js for VitePress
