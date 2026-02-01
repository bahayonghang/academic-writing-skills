# Typst Academic Paper Assistant

A comprehensive toolkit for writing academic papers in Typst, supporting both English and Chinese papers for conferences and journals.

## Features

- 🚀 **Fast Compilation**: Millisecond-level compilation speed
- 📝 **Multiple Modules**: Grammar check, format validation, de-AI editing, etc.
- 🌍 **Bilingual Support**: English and Chinese academic writing
- 🎯 **Venue-Specific**: IEEE, ACM, Springer, NeurIPS, CVPR templates
- 🔧 **Automated Scripts**: Python scripts for common tasks

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
   python scripts/compile.py main.typ
   ```

2. **Watch mode** (auto-recompile on changes):
   ```bash
   python scripts/compile.py main.typ --watch
   ```

3. **Check formatting**:
   ```bash
   python scripts/check_format.py main.typ
   ```

4. **Verify bibliography**:
   ```bash
   python scripts/verify_bib.py references.bib --typ main.typ
   ```

## Modules

### 1. Compilation Module
**Triggers**: `compile`, `编译`, `typst compile`

Fast compilation with multiple output formats:
```bash
# Basic compilation
python scripts/compile.py main.typ

# Watch mode
python scripts/compile.py main.typ --watch

# Export as PNG
python scripts/compile.py main.typ --format png

# Custom output name
python scripts/compile.py main.typ --output paper.pdf

# Custom fonts
python scripts/compile.py main.typ --font-path ./fonts
```

### 2. Format Check Module
**Triggers**: `format`, `格式检查`, `lint`

Validate paper formatting:
```bash
# Basic check
python scripts/check_format.py main.typ

# Strict mode
python scripts/check_format.py main.typ --strict

# Venue-specific check
python scripts/check_format.py main.typ --venue ieee
```

### 3. Grammar Analysis Module
**Triggers**: `grammar`, `语法`, `proofread`

Check for common grammar errors:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency
- Chinglish patterns

See [COMMON_ERRORS.md](references/COMMON_ERRORS.md) for details.

### 4. Long Sentence Analysis Module
**Triggers**: `long sentence`, `长句`, `simplify`

Detect and simplify long sentences:
- English: >50 words or >3 clauses
- Chinese: >60 characters or >3 clauses

### 5. Academic Expression Module
**Triggers**: `academic tone`, `学术表达`, `improve writing`

Improve academic writing style:
- Replace weak verbs
- Enhance academic tone
- Fix informal expressions

See [STYLE_GUIDE.md](references/STYLE_GUIDE.md) for details.

### 6. Translation Module
**Triggers**: `translate`, `翻译`, `中译英`

Translate Chinese to English with domain-specific terminology:
- Deep Learning
- Time Series
- Industrial Control

### 7. Bibliography Module
**Triggers**: `bib`, `bibliography`, `参考文献`

Verify bibliography files:
```bash
# Check BibTeX file
python scripts/verify_bib.py references.bib

# Check Hayagriva file
python scripts/verify_bib.py references.yml

# Check citations
python scripts/verify_bib.py references.bib --typ main.typ

# Check style
python scripts/verify_bib.py references.bib --style ieee
```

### 8. De-AI Editing Module
**Triggers**: `deai`, `去AI化`, `humanize`

Reduce AI writing traces while preserving technical accuracy:
- Remove empty phrases
- Replace vague claims with specific statements
- Add appropriate hedging
- Improve natural flow

See [DEAI_GUIDE.md](references/DEAI_GUIDE.md) for details.

## Templates

See `references/TEMPLATES.md` for IEEE/ACM/Chinese templates and usage notes.

## Venue-Specific Requirements

| Venue | Columns | Font Size | Page Limit | Citation Style |
|-------|---------|-----------|------------|----------------|
| IEEE | 2 | 10pt | Varies | Numeric [1] |
| ACM | 2 | 9-10pt | Varies | Numeric or Author-Year |
| Springer | 1-2 | 10-12pt | Varies | Alphabetical |
| NeurIPS | 1 | 10pt | 8 pages | Numeric [1] |
| CVPR | 2 | 10pt | 8 pages | Numeric [1] |

See [VENUES.md](references/VENUES.md) for detailed requirements.

## Typst vs LaTeX

| Feature | Typst | LaTeX |
|---------|-------|-------|
| Compilation Speed | Milliseconds | Seconds |
| Syntax | Simple, intuitive | Complex, verbose |
| Error Messages | Clear, helpful | Cryptic, difficult |
| Learning Curve | Gentle | Steep |
| Live Preview | Native support | Requires tools |

## Reference Documents

- [STYLE_GUIDE.md](references/STYLE_GUIDE.md): Academic writing style guide
- [COMMON_ERRORS.md](references/COMMON_ERRORS.md): Common Chinglish errors
- [DEAI_GUIDE.md](references/DEAI_GUIDE.md): De-AI writing guide
- [VENUES.md](references/VENUES.md): Venue-specific requirements
- [TEMPLATES.md](references/TEMPLATES.md): Typst template examples
- [TYPST_SYNTAX.md](references/TYPST_SYNTAX.md): Typst syntax reference

## Resources

- [Typst Official Website](https://typst.app/)
- [Typst Documentation](https://typst.app/docs/)
- [Typst Universe](https://typst.app/universe/) - Templates and packages
- [Typst Tutorial](https://typst.app/docs/tutorial/)

## FAQ

**Q: Can Typst completely replace LaTeX?**
A: For most academic papers, yes. However, some specific journal templates or complex typesetting needs may still require LaTeX.

**Q: How to handle Chinese text?**
A: Use `#set text(lang: "zh", region: "cn")` and configure Chinese fonts (e.g., Source Han Serif or Noto Serif CJK).

**Q: Which citation style should I use?**
A: Choose based on your target venue. Typst supports IEEE, APA, MLA, GB7714, and more.

**Q: Is compilation really that fast?**
A: Yes! Typst typically compiles in milliseconds, making it ideal for live preview.

**Q: How to collaborate with others?**
A: Use Typst Web App for online collaboration, or Git for version control (Typst files are plain text).

## License

This toolkit is provided as-is for academic writing assistance.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
