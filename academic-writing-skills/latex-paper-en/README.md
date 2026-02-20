# LaTeX Academic Paper Assistant (English)

A comprehensive toolkit for writing academic papers in LaTeX, focused on English papers for conferences and journals.

## Features

- **Compilation workflows**: pdflatex / xelatex / latexmk with bibtex or biber
- **Multiple modules**: format check, grammar analysis, sentence decomposition, academic expression
- **Translation support**: Chinese to English with domain terminology
- **Bibliography verification**: citation consistency and BibTeX validation
- **De-AI editing**: reduce AI writing traces while preserving LaTeX syntax
- **Logic analysis**: paragraph coherence and methodology justification checks
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

4. **Grammar analysis**:
   ```bash
   python scripts/analyze_grammar.py main.tex --section introduction
   ```

5. **De-AI editing (analysis)**:
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
python scripts/compile.py main.tex --biber
```

### 2. Format Check Module
**Triggers**: `format check`, `chktex`, `格式检查`

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

### 3. Grammar Analysis Module
**Triggers**: `grammar`, `语法`, `proofread`, `润色`

```bash
python scripts/analyze_grammar.py main.tex
python scripts/analyze_grammar.py main.tex --section introduction
```

### 4. Sentence Decomposition Module
**Triggers**: `long sentence`, `长句`, `simplify`

```bash
python scripts/analyze_sentences.py main.tex
python scripts/analyze_sentences.py main.tex --section methods --max-words 45
```

### 5. Academic Expression Module
**Triggers**: `academic tone`, `学术表达`, `improve writing`

```bash
python scripts/improve_expression.py main.tex
python scripts/improve_expression.py main.tex --section related
```

Improve academic tone and replace weak verbs.  
See [STYLE_GUIDE.md](references/STYLE_GUIDE.md) for details.

### 6. Translation Module
**Triggers**: `translate`, `翻译`, `中译英`, `Chinese to English`

```bash
python scripts/translate_academic.py "本文提出了一种基于Transformer的方法" --domain deep-learning
python scripts/translate_academic.py input_zh.txt --domain industrial-control --output translation_report.md
```

Translate with domain-specific terminology (Deep Learning, Time Series, Industrial Control).  
See [TERMINOLOGY.md](references/TERMINOLOGY.md) and [TRANSLATION_GUIDE.md](references/TRANSLATION_GUIDE.md).

### 7. Bibliography Module
**Triggers**: `bib`, `bibliography`, `参考文献`

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --standard gb7714
python scripts/verify_bib.py references.bib --tex main.tex --json
```

Key result fields: `missing_in_bib`, `unused_in_tex`.

### 8. De-AI Polishing Module
**Triggers**: `deai`, `去AI化`, `humanize`, `reduce AI traces`

Reduce AI writing traces while preserving LaTeX syntax.
See [DEAI_GUIDE.md](references/DEAI_GUIDE.md) for details.

### 9. Logic & Methodology Module
**Triggers**: `logic`, `coherence`, `methodology`

```bash
python scripts/analyze_logic.py main.tex
python scripts/analyze_logic.py main.tex --section methods
```

### 10. Title Optimization Module
**Triggers**: `title`, `标题`, `title optimization`

```bash
python scripts/optimize_title.py main.tex --check
python scripts/optimize_title.py main.tex --generate
python scripts/optimize_title.py main.tex --optimize
python scripts/optimize_title.py main.tex --compare "Title A" "Title B" "Title C"
python scripts/optimize_title.py "papers/*.tex" --batch --output title_report.json
python scripts/optimize_title.py main.tex --interactive
```

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
