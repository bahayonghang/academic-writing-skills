# Bibliography Management Guide

Complete guide to managing bibliographies with Academic Writing Skills.

## Overview

Academic Writing Skills provides comprehensive bibliography management for both English papers (BibTeX/Biber) and Chinese theses (GB/T 7714-2015 compliance).

## BibTeX Basics

### Entry Structure

```bibtex
@entrytype{key,
  field1 = {value1},
  field2 = {value2},
  ...
}
```

### Common Entry Types

#### @article (Journal Article)

```bibtex
@article{Smith2024-ml,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning for Natural Language Processing},
  journal = {Journal of Machine Learning Research},
  year = {2024},
  volume = {25},
  number = {3},
  pages = {123--145},
  doi = {10.1234/jmlr.2024.001}
}
```

**Required fields**: author, title, journal, year
**Optional fields**: volume, number, pages, doi, url

#### @inproceedings (Conference Paper)

```bibtex
@inproceedings{Wang2024-neural,
  author = {Wang, Alice and Zhang, Bob},
  title = {Neural Network Optimization Techniques},
  booktitle = {Proceedings of the International Conference on Machine Learning},
  year = {2024},
  pages = {456--467},
  address = {Vienna, Austria},
  publisher = {PMLR}
}
```

**Required fields**: author, title, booktitle, year
**Optional fields**: pages, address, publisher, doi

#### @book

```bibtex
@book{Johnson2023-deep,
  author = {Johnson, Michael},
  title = {Deep Learning Fundamentals},
  publisher = {MIT Press},
  year = {2023},
  address = {Cambridge, MA},
  isbn = {978-0-262-12345-6}
}
```

**Required fields**: author, title, publisher, year
**Optional fields**: address, edition, isbn

#### @phdthesis

```bibtex
@phdthesis{Chen2023-research,
  author = {Chen, David},
  title = {Advanced Techniques in Deep Reinforcement Learning},
  school = {Stanford University},
  year = {2023},
  address = {Stanford, CA}
}
```

**Required fields**: author, title, school, year
**Optional fields**: address, type

#### @misc (Preprints, Software, etc.)

```bibtex
@misc{Brown2024-arxiv,
  author = {Brown, Emily and others},
  title = {Large Language Models: A Survey},
  year = {2024},
  eprint = {2401.12345},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL}
}
```

## Bibliography Verification

### Basic Verification

```bash
python verify_bib.py references.bib
```

**Checks**:
- Required fields present
- Entry format valid
- No duplicate keys
- DOI format valid
- URL format valid

**Output**:
```
Bibliography Verification Results
=================================

✓ All entries have required fields
✗ Entry 'Smith2024': Missing DOI
✗ Entry 'Wang2024': Duplicate key
✓ All URLs valid

2 issues found
```

### Style-Specific Verification

#### IEEE Style

```bash
python verify_bib.py references.bib --style ieee
```

**Additional checks**:
- Journal abbreviations (IEEE standard)
- Conference name format
- Page number format (123--145)

#### ACM Style

```bash
python verify_bib.py references.bib --style acm
```

**Additional checks**:
- DOI required for all entries
- URL format (ACM Digital Library)

#### Springer Style

```bash
python verify_bib.py references.bib --style springer
```

**Additional checks**:
- Series information for LNCS
- Volume/issue format

### GB/T 7714-2015 (Chinese)

```bash
python verify_bib.py references.bib --standard gbt7714
```

**Checks**:
- Language field required
- Author name format (Chinese vs. English)
- Title format (Chinese vs. English)
- Journal/conference name format
- Year, volume, issue, page format

**Example**:
```bibtex
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习在自然语言处理中的应用},
  journal = {计算机学报},
  year = {2024},
  volume = {47},
  number = {3},
  pages = {123--145},
  language = {zh},  % Required!
  doi = {10.11897/SP.J.1016.2024.00123}
}
```

## Common Issues

### 1. Missing Required Fields

**Issue**: Entry missing required fields

```bibtex
% Bad
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning}
  % Missing: journal, year
}

% Good
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning},
  journal = {Journal of ML},
  year = {2024}
}
```

**Detection**: Basic verification

**Fix**: Add missing fields from original source

### 2. Malformed Entries

**Issue**: Syntax errors in BibTeX

```bibtex
% Bad
@article{Smith2024
  author = {Smith, John}  % Missing comma
  title = Machine Learning  % Missing braces
}

% Good
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning}
}
```

**Detection**: BibTeX parser errors

**Fix**: Check braces, commas, quotes

### 3. Duplicate Keys

**Issue**: Multiple entries with same key

```bibtex
@article{Smith2024, ...}
@inproceedings{Smith2024, ...}  % Duplicate!
```

**Detection**: `verify_bib.py --check-duplicates`

**Fix**: Rename keys uniquely
```bibtex
@article{Smith2024-journal, ...}
@inproceedings{Smith2024-conference, ...}
```

### 4. Inconsistent Formatting

**Issue**: Mixed formatting styles

```bibtex
% Bad
@article{key1,
  author = {Smith, John},  % Last, First
  ...
}

@article{key2,
  author = {Jane Doe},  % First Last
  ...
}

% Good
@article{key1,
  author = {Smith, John},
  ...
}

@article{key2,
  author = {Doe, Jane},
  ...
}
```

**Detection**: Style-specific checks

**Fix**: Use consistent format (prefer "Last, First")

### 5. Missing DOI

**Issue**: No DOI provided

```bibtex
% Incomplete
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning},
  journal = {Journal of ML},
  year = {2024}
  % Missing DOI
}

% Complete
@article{Smith2024,
  author = {Smith, John},
  title = {Machine Learning},
  journal = {Journal of ML},
  year = {2024},
  doi = {10.1234/jml.2024.001}
}
```

**Detection**: `verify_bib.py --require-doi`

**Fix**: Look up DOI on journal website or CrossRef

### 6. Incorrect Author Format

**Issue**: Author names not properly formatted

```bibtex
% Bad
author = {John Smith and Jane Doe}  % First Last

% Good
author = {Smith, John and Doe, Jane}  % Last, First

% Also acceptable
author = {Smith, J. and Doe, J.}  % Last, Initial
```

**Detection**: Style-specific checks

**Fix**: Use "Last, First" or "Last, Initial" format

### 7. Page Number Format

**Issue**: Incorrect page range format

```bibtex
% Bad
pages = {123-145}  % Single dash

% Good
pages = {123--145}  % Double dash (en-dash)
```

**Detection**: Style-specific checks

**Fix**: Use double dash `--` for ranges

### 8. Missing Language Field (Chinese)

**Issue**: Chinese entries without language field

```bibtex
% Bad
@article{zhang2024,
  author = {张三},
  title = {深度学习研究},
  journal = {计算机学报},
  year = {2024}
  % Missing language field!
}

% Good
@article{zhang2024,
  author = {张三},
  title = {深度学习研究},
  journal = {计算机学报},
  year = {2024},
  language = {zh}  % Required for GB/T 7714
}
```

**Detection**: GB/T 7714 verification

**Fix**: Add `language = {zh}` for Chinese entries

## Auto-Fix

### Safe Auto-Fix

```bash
python verify_bib.py references.bib --fix
```

**Auto-fixable issues**:
- Page number format (single dash → double dash)
- Trailing commas
- Whitespace normalization
- Field ordering

**Example**:
```bash
$ python verify_bib.py references.bib --fix

Auto-fixing 3 issues...
  ✓ Fixed page format in 2 entries
  ✓ Normalized whitespace in 1 entry

3 issues fixed. Backup saved to references.bib.bak
```

### Manual Review Required

Some issues require manual review:
- Missing required fields
- Duplicate keys
- Author name format
- Language field (Chinese)

## BibTeX vs. Biber

### BibTeX (Traditional)

**Pros**:
- Wide compatibility
- Stable and mature
- Works with legacy .bst styles

**Cons**:
- ASCII-only
- Limited sorting
- No Unicode support

**Use case**: English-only papers, legacy templates

**Example**:
```latex
\bibliographystyle{ieeetr}
\bibliography{references}
```

### Biber (Modern)

**Pros**:
- Full Unicode support
- Advanced sorting
- Better localization
- Modern features

**Cons**:
- Requires BibLaTeX
- Less compatible with old templates

**Use case**: Modern papers, Chinese theses, Unicode

**Example**:
```latex
\usepackage[backend=biber,style=ieee]{biblatex}
\addbibresource{references.bib}
...
\printbibliography
```

## GB/T 7714-2015 (Chinese Standard)

### Overview

GB/T 7714-2015 is the Chinese national standard for bibliographic references.

### Key Requirements

1. **Language field**: Required for all entries
2. **Author names**: Original language (Chinese or English)
3. **Title**: Original language
4. **Specific punctuation**: Chinese vs. English
5. **Ordering**: Specific rules for Chinese/English mixed

### Entry Examples

#### Chinese Journal Article

```bibtex
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习在自然语言处理中的应用},
  journal = {计算机学报},
  year = {2024},
  volume = {47},
  number = {3},
  pages = {123--145},
  language = {zh},
  doi = {10.11897/SP.J.1016.2024.00123}
}
```

#### Chinese Conference Paper

```bibtex
@inproceedings{wang2024neural,
  author = {王五 and 赵六},
  title = {神经网络优化方法研究},
  booktitle = {中国计算机大会论文集},
  year = {2024},
  pages = {45--52},
  address = {北京},
  language = {zh}
}
```

#### Chinese Book

```bibtex
@book{liu2023machine,
  author = {刘七},
  title = {机器学习基础},
  publisher = {清华大学出版社},
  year = {2023},
  address = {北京},
  language = {zh},
  isbn = {978-7-302-12345-6}
}
```

#### Chinese Thesis

```bibtex
@phdthesis{chen2023research,
  author = {陈八},
  title = {深度强化学习理论与应用研究},
  school = {清华大学},
  year = {2023},
  address = {北京},
  language = {zh}
}
```

#### Mixed Bibliography

```bibtex
% Chinese entry
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习研究},
  journal = {计算机学报},
  year = {2024},
  language = {zh}
}

% English entry
@article{smith2024machine,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning Advances},
  journal = {Journal of Machine Learning Research},
  year = {2024},
  language = {en}
}
```

### Common GB/T 7714 Issues

#### 1. Mixed Language in Single Entry

**Issue**: Chinese and English authors in same entry

```bibtex
% Bad
@article{key,
  author = {张三 and Smith, John},  % Mixed!
  ...
}

% Good (separate entries or use one language)
@article{key,
  author = {张三 and 李四},  % All Chinese
  ...
}
```

#### 2. Missing Language Field

**Issue**: No language field specified

```bibtex
% Bad
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  ...
  % Missing language!
}

% Good
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  ...,
  language = {zh}
}
```

#### 3. Incorrect Name Format

**Issue**: Chinese names in Western order

```bibtex
% Bad
author = {San Zhang}  % Western order

% Good
author = {张三}  % Chinese characters
% or
author = {Zhang, San}  % Pinyin with comma
```

## Best Practices

### 1. Consistent Key Naming

Use consistent pattern for keys:

```bibtex
% Pattern: AuthorYear-keyword
@article{Smith2024-ml,
  ...
}

@inproceedings{Wang2024-neural,
  ...
}
```

### 2. Always Include DOI

```bibtex
@article{Smith2024,
  ...,
  doi = {10.1234/journal.2024.001}
}
```

### 3. Use Proper Entry Types

```bibtex
% Correct entry types
@article{...}         % Journal articles
@inproceedings{...}   % Conference papers
@book{...}            % Books
@phdthesis{...}       % PhD theses
@mastersthesis{...}   % Master's theses
@techreport{...}      % Technical reports
@misc{...}            % Preprints, software, etc.
```

### 4. Maintain Separate .bib Files

```
references/
├── papers.bib        % Journal/conference papers
├── books.bib         % Books and chapters
├── theses.bib        % Theses and dissertations
└── misc.bib          % Preprints, software, etc.
```

### 5. Regular Verification

```bash
# Verify after adding entries
python verify_bib.py references.bib

# Full check before submission
python verify_bib.py references.bib --style ieee --require-doi
```

### 6. Version Control

```bash
# Commit .bib files
git add references.bib
git commit -m "Add new references"

# Don't commit generated files
echo "*.bbl" >> .gitignore
echo "*.blg" >> .gitignore
```

## Tools and Resources

### Bibliography Management Tools

- **JabRef**: Cross-platform BibTeX editor
- **Zotero**: Reference manager with BibTeX export
- **Mendeley**: Reference manager with BibTeX export
- **BibDesk**: macOS BibTeX manager

### Online Resources

- **CrossRef**: Look up DOIs
- **Google Scholar**: Export BibTeX citations
- **DBLP**: Computer science bibliography
- **arXiv**: Preprint citations

### Validation Tools

```bash
# Academic Writing Skills
python verify_bib.py references.bib

# biber validation
biber --validate-datamodel references.bcf

# BibTeX validation
bibtex references
```

## Troubleshooting

### Bibliography Not Appearing

**Problem**: Bibliography section empty

**Solution**: Use full compilation recipe
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

### Citations Show as [?]

**Problem**: Citations display as `[?]`

**Solution**: Complete compilation cycle
```bash
python compile.py paper.tex --recipe pdflatex-biber
```

### Biber Error

**Problem**: `biber: command not found`

**Solution**: Install Biber
```bash
# macOS
brew install biber

# Ubuntu/Debian
sudo apt-get install biber
```

### Encoding Issues

**Problem**: Chinese characters not displaying

**Solution**: Ensure UTF-8 encoding
```bash
# Check encoding
file -i references.bib

# Convert if needed
iconv -f GBK -t UTF-8 references.bib > references_utf8.bib
```

## Next Steps

- [Compilation Guide](/guides/compilation) - Compile with bibliography
- [Format Checking Guide](/guides/format-checking) - Check LaTeX format
- [Usage Guide](/usage) - General usage documentation
