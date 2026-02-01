# LaTeX Academic Paper Assistant (English)

A comprehensive toolkit for writing academic papers in LaTeX, focused on English papers for conferences and journals.

## Features

- **Compilation workflows**: pdflatex / xelatex / latexmk with bibtex or biber
- **Multiple modules**: format check, grammar analysis, sentence decomposition, academic expression
- **Translation support**: Chinese to English with domain terminology
- **Bibliography verification**: citation consistency and BibTeX validation
- **De-AI editing**: reduce AI writing traces while preserving LaTeX syntax
- **Venue-specific guidance**: IEEE, ACM, Springer, NeurIPS, ICML rules
- **Automated scripts**: Python tools for common tasks

## Quick Start

### Prerequisites

1. **LaTeX distribution**: TeX Live or MiKTeX (ensure `pdflatex`, `xelatex`, `latexmk` are in PATH)
2. **Python 3**: Required to run the scripts

### Basic Usage

1. **Compile a paper**:
   ```bash
   python scripts/compile.py main.tex
   ```

2. **Format check**:
   ```bash
   python scripts/check_format.py main.tex --strict
   ```

3. **Verify bibliography**:
   ```bash
   python scripts/verify_bib.py references.bib --tex main.tex
   ```

4. **De-AI editing (interactive)**:
   ```bash
   python scripts/deai_check.py main.tex --section introduction
   ```

## Modules

### 1. Compilation Module
**Triggers**: `compile`, `编译`, `build latex`

```bash
# Auto-detect (xelatex for Chinese content)
python scripts/compile.py main.tex

# Explicit recipes
python scripts/compile.py main.tex --recipe xelatex
python scripts/compile.py main.tex --recipe pdflatex
python scripts/compile.py main.tex --recipe latexmk --outdir build

# With bibliography
python scripts/compile.py main.tex --recipe xelatex-bibtex
python scripts/compile.py main.tex --recipe xelatex-biber
```

### 2. Format Check Module
**Triggers**: `format check`, `chktex`, `格式检查`

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

### 3. Grammar Analysis Module
**Triggers**: `grammar`, `语法`, `proofread`, `润色`

Focus areas:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency
- Chinglish patterns

See [COMMON_ERRORS.md](references/COMMON_ERRORS.md) for details.

### 4. Sentence Decomposition Module
**Triggers**: `long sentence`, `长句`, `simplify`

Detect and simplify long sentences (>50 words or >3 clauses).

### 5. Academic Expression Module
**Triggers**: `academic tone`, `学术表达`, `improve writing`

Improve academic tone and replace weak verbs.
See [STYLE_GUIDE.md](references/STYLE_GUIDE.md) for details.

### 6. Translation Module
**Triggers**: `translate`, `翻译`, `中译英`, `Chinese to English`

Translate with domain-specific terminology (Deep Learning, Time Series, Industrial Control).
See [TERMINOLOGY.md](references/TERMINOLOGY.md) and [TRANSLATION_GUIDE.md](references/TRANSLATION_GUIDE.md).

### 7. Bibliography Module
**Triggers**: `bib`, `bibliography`, `参考文献`

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --standard gb7714
```

### 8. De-AI Polishing Module
**Triggers**: `deai`, `去AI化`, `humanize`, `reduce AI traces`

Reduce AI writing traces while preserving LaTeX syntax.
See [DEAI_GUIDE.md](references/DEAI_GUIDE.md) for details.

## Venue-Specific Requirements

See [VENUES.md](references/VENUES.md) for detailed requirements across IEEE/ACM/Springer/NeurIPS/ICML.

## Reference Documents

- [STYLE_GUIDE.md](references/STYLE_GUIDE.md): Academic writing rules
- [COMMON_ERRORS.md](references/COMMON_ERRORS.md): Common Chinglish errors
- [VENUES.md](references/VENUES.md): Conference/journal requirements
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): Protected terminology
- [TERMINOLOGY.md](references/TERMINOLOGY.md): Domain terminology
- [TRANSLATION_GUIDE.md](references/TRANSLATION_GUIDE.md): Translation guide
- [DEAI_GUIDE.md](references/DEAI_GUIDE.md): De-AI writing guide and patterns
- [COMPILATION.md](references/COMPILATION.md): Compilation recipes

## FAQ

**Q: Which compiler should I use?**
A: Use xelatex for multilingual or CJK content; pdflatex is fine for pure English papers. For full automation, latexmk is recommended.

**Q: Should I use BibTeX or Biber?**
A: Use the tool required by your template. If unsure, BibTeX is the most common.

**Q: How do I reduce AI traces safely?**
A: Use the De-AI module and keep all citations, labels, and math intact. See [DEAI_GUIDE.md](references/DEAI_GUIDE.md).

## License

This toolkit is provided as-is for academic writing assistance.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
