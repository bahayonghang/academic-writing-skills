# Typst Academic Paper Assistant

A comprehensive toolkit for writing academic papers in Typst, supporting both English and Chinese papers for conferences and journals.

## Features

- 🚀 **Fast Compilation**: Millisecond-level compilation speed
- 📝 **Multiple Modules**: Grammar check, format validation, de-AI editing, etc.
- 🌍 **Bilingual Support**: English and Chinese academic writing
- 🎯 **Venue-Specific**: IEEE, ACM, Springer, NeurIPS, CVPR templates
- 🔧 **Automated Scripts**: Python scripts for common tasks
- 🧠 **Comprehensive Analysis**: Logic, methodology, workflow, and reviewer perspective

## Quick Start

### Installation

1. **Install Typst**:
   ```bash
   # Using Cargo (Rust package manager)
   cargo install typst-cli

   # Using Homebrew (macOS)
   brew install typst

   # Using package manager (Linux)
   # Arch Linux
   sudo pacman -S typst
   ```

2. **Install Python dependencies** (for scripts):
   ```bash
   pip install pyyaml  # For Hayagriva bibliography support
   ```

### Basic Usage

1. **Compile a paper**:
   ```bash
   typst compile main.typ
   ```

2. **Check formatting**:
   ```bash
   python scripts/check_format.py main.typ
   ```

3. **Verify bibliography**:
   ```bash
   python scripts/verify_bib.py refs.bib
   ```

## Modules

### 1. Compilation Module
**Triggers**: `compile`, `编译`, `build`, `typst compile`

Fast compilation with Typst CLI:
```bash
typst compile main.typ
```
See [COMPILE.md](resources/modules/COMPILE.md).

### 2. Format Check Module
**Triggers**: `format`, `lint`, `格式检查`

Validate paper formatting:
```bash
python scripts/check_format.py main.typ
```
See [FORMAT.md](resources/modules/FORMAT.md).

### 3. Grammar Analysis Module
**Triggers**: `grammar`, `语法`, `proofread`

Check for common grammar errors:
```bash
python scripts/analyze_grammar.py main.typ
```
See [GRAMMAR.md](resources/modules/GRAMMAR.md).

### 4. Long Sentence Analysis Module
**Triggers**: `long sentence`, `长句`

Detect and simplify long sentences:
```bash
python scripts/analyze_sentences.py main.typ
```
See [SENTENCES.md](resources/modules/SENTENCES.md).

### 5. Academic Expression Module
**Triggers**: `academic tone`, `学术表达`

Improve academic writing style:
```bash
python scripts/improve_expression.py main.typ
```
See [EXPRESSION.md](resources/modules/EXPRESSION.md).

### 6. Logic Analysis Module
**Triggers**: `logic`, `coherence`, `methodology`

Analyze logic coherence and methodology depth:
```bash
python scripts/analyze_logic.py main.typ
```
See [LOGIC.md](resources/modules/LOGIC.md).

### 7. Translation Module
**Triggers**: `translate`, `翻译`, `中译英`

Translate Chinese to English with domain-specific terminology:
```bash
python scripts/translate_academic.py "text"
```
See [TRANSLATION.md](resources/modules/TRANSLATION.md).

### 8. Bibliography Module
**Triggers**: `bib`, `bibliography`, `参考文献`

Verify bibliography files:
```bash
python scripts/verify_bib.py refs.bib
```
See [BIBLIOGRAPHY.md](resources/modules/BIBLIOGRAPHY.md).

### 9. De-AI Editing Module
**Triggers**: `deai`, `去AI化`, `humanize`

Reduce AI writing traces while preserving technical accuracy:
```bash
python scripts/deai_check.py main.typ
```
See [DEAI.md](resources/modules/DEAI.md).

### 10. Title Optimization Module
**Triggers**: `title`, `标题`

Optimize or generate paper titles based on best practices:
```bash
python scripts/optimize_title.py main.typ
```
See [TITLE.md](resources/modules/TITLE.md).

### 11. Reviewer Perspective Module
**Triggers**: `reviewer`, `审稿`, `checklist`

Review paper from an academic peer reviewer's perspective.
See [REVIEWER_PERSPECTIVE.md](resources/references/REVIEWER_PERSPECTIVE.md).

### 12. Workflow Module
**Triggers**: `workflow`, `full review`

Execute the full review pipeline.
See [WORKFLOW.md](resources/modules/WORKFLOW.md).

## Templates & Venues

See [VENUES.md](resources/references/VENUES.md) for detailed requirements on venues.

| Venue | Columns | Font Size | Page Limit | Citation Style |
|-------|---------|-----------|------------|----------------|
| IEEE | 2 | 10pt | Varies | Numeric [1] |
| ACM | 2 | 9-10pt | Varies | Numeric or Author-Year |
| Springer | 1-2 | 10-12pt | Varies | Alphabetical |
| NeurIPS | 1 | 10pt | 8 pages | Numeric [1] |
| CVPR | 2 | 10pt | 8 pages | Numeric [1] |

## Typst vs LaTeX

| Feature | Typst | LaTeX |
|---------|-------|-------|
| Compilation Speed | Milliseconds | Seconds |
| Syntax | Simple, intuitive | Complex, verbose |
| Error Messages | Clear, helpful | Cryptic, difficult |
| Learning Curve | Gentle | Steep |

See [TYPST_SYNTAX.md](resources/references/TYPST_SYNTAX.md) for details.

## Reference Documents

- [STYLE_GUIDE.md](resources/references/STYLE_GUIDE.md): Academic writing rules
- [COMMON_ERRORS.md](resources/references/COMMON_ERRORS.md): Chinglish patterns
- [VENUES.md](resources/references/VENUES.md): Conference/journal requirements
- [TERMINOLOGY.md](resources/references/TERMINOLOGY.md): Domain terminology (DL/TS/IC)
- [TRANSLATION_GUIDE.md](resources/references/TRANSLATION_GUIDE.md): Translation guide
- [DEAI_GUIDE.md](resources/references/DEAI_GUIDE.md): De-AI writing guide and patterns
- [WRITING_PHILOSOPHY.md](resources/references/WRITING_PHILOSOPHY.md): Writing philosophy
- [REVIEWER_PERSPECTIVE.md](resources/references/REVIEWER_PERSPECTIVE.md): Reviewer checklist
- [CITATION_VERIFICATION.md](resources/references/CITATION_VERIFICATION.md): Citation verification
- [TYPST_SYNTAX.md](resources/references/TYPST_SYNTAX.md): Typst notes and syntax advantages
- [BEST_PRACTICES.md](resources/references/BEST_PRACTICES.md): General workflow recommendations

## Resources

- [Typst Official Website](https://typst.app/)
- [Typst Documentation](https://typst.app/docs/)

## FAQ

**Q: Can Typst completely replace LaTeX?**
A: For most academic papers, yes. However, some specific journal templates or complex typesetting needs may still require LaTeX.

**Q: How to handle Chinese text?**
A: Use `#set text(lang: "zh", region: "cn")` and configure Chinese fonts (e.g., Source Han Serif or Noto Serif CJK).

**Q: Which citation style should I use?**
A: Choose based on your target venue. Typst supports IEEE, APA, MLA, GB7714, and more.

## License

This toolkit is provided as-is for academic writing assistance.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
