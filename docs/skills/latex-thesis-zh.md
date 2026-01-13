# Chinese Thesis (latex-thesis-zh)

LaTeX assistant for Chinese doctoral/master theses.

## Overview

The `latex-thesis-zh` skill provides modular support for Chinese thesis writing, with each module independently callable.

### Trigger Words

| Module | Triggers |
|--------|----------|
| Compile | `compile`, `编译`, `xelatex` |
| Structure Mapping | `structure`, `结构`, `映射` |
| GB/T Format Check | `format`, `格式`, `国标`, `GB/T` |
| Academic Expression | `expression`, `表达`, `润色` |
| Long Sentence Analysis | `long sentence`, `长句`, `拆解` |
| Bibliography | `bib`, `bibliography`, `参考文献` |
| Template Detection | `template`, `模板`, `thuthesis` |

## Modules

### Compile Module

XeLaTeX-focused compilation for Chinese documents.

**Tools** (aligned with VS Code LaTeX Workshop):

| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| lualatex | `lualatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -xelatex` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

**Recipes**:

| Recipe | Steps | Use Case |
|--------|-------|----------|
| XeLaTeX | xelatex | Quick Chinese compile (recommended) |
| LuaLaTeX | lualatex | Complex font requirements |
| LaTeXmk | latexmk -xelatex | Auto dependency handling |
| xelatex-bibtex | xelatex → bibtex → xelatex×2 | Chinese + BibTeX |
| xelatex-biber | xelatex → biber → xelatex×2 | Chinese + Biber (recommended) |
| lualatex-bibtex | lualatex → bibtex → lualatex×2 | LuaLaTeX + BibTeX |
| lualatex-biber | lualatex → biber → lualatex×2 | LuaLaTeX + Biber |

**Usage**:

```bash
# Quick compile
python scripts/compile.py thesis.tex --recipe xelatex

# Full compile (recommended)
python scripts/compile.py thesis.tex --recipe xelatex-biber

# Clean auxiliary files
python scripts/compile.py thesis.tex --clean
```

### Structure Mapping Module

Analyze multi-file thesis structure. **Run this first**.

```bash
python scripts/map_structure.py thesis.tex
```

**Thesis Structure Requirements**:

| Section | Required Content |
|---------|------------------|
| Front Matter | Cover, Declaration, Abstract (CN+EN), TOC, Symbol List |
| Main Body | Introduction, Related Work, Core Chapters, Conclusion |
| Back Matter | References, Acknowledgments, Publication List |

### GB/T Format Check Module

Verify GB/T 7714-2015 compliance.

```bash
python scripts/check_format.py thesis.tex
python scripts/check_format.py thesis.tex --strict
```

**Checks**:
- Bibliography format (biblatex-gb7714-2015)
- Figure/table caption format
- Equation numbering
- Section heading styles

### Academic Expression Module

Detect colloquial expressions and suggest academic alternatives.

**Colloquial → Academic Examples**:

| ❌ Colloquial | ✅ Academic |
|--------------|-------------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |

### Long Sentence Analysis Module

Trigger: Sentences >60 characters OR >3 clauses

Output: Core extraction, modifier analysis, rewrite suggestions

### Bibliography Module

```bash
python scripts/verify_bib.py refs.bib
python scripts/verify_bib.py refs.bib --standard gb7714
```

### Template Detection Module

```bash
python scripts/detect_template.py thesis.tex
```

**Supported Templates**:

| Template | University |
|----------|------------|
| thuthesis | Tsinghua University |
| pkuthss | Peking University |
| ustcthesis | USTC |
| fduthesis | Fudan University |
| ctexbook | Generic |

## Workflow Suggestions

### Daily Writing

```bash
python scripts/compile.py thesis.tex --recipe xelatex
```

### Chapter Completion

```bash
python scripts/compile.py thesis.tex --recipe xelatex-biber
python scripts/verify_bib.py refs.bib --standard gb7714
```

### Final Submission

```bash
# 1. Structure mapping
python scripts/map_structure.py thesis.tex

# 2. Full compile
python scripts/compile.py thesis.tex --recipe xelatex-biber

# 3. GB/T check
python scripts/verify_bib.py refs.bib --standard gb7714

# 4. Consistency check
python scripts/check_consistency.py chapters/

# 5. Clean
python scripts/compile.py thesis.tex --clean
```

## Common Issues

### Chinese Font Missing

```latex
\setCJKmainfont{SimSun}  % Windows
\setCJKmainfont{STSong}  % macOS
```

### Bibliography Format Incorrect

```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
```

## Next Steps

- [Compilation Guide](/guides/compilation)
- [Bibliography Guide](/guides/bibliography)
- [GB/T 7714 Reference](/references/gb-standard)
