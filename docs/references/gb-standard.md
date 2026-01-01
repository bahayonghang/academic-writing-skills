# GB/T 7714-2015 Standard

Chinese national standard for bibliographic references (GB/T 7714-2015).

## Overview

GB/T 7714-2015 is the Chinese national standard for bibliographic references, replacing the previous GB/T 7714-2005 standard. It specifies formatting rules for references in Chinese academic publications.

## Key Requirements

### 1. Language Field

**Mandatory**: All entries must include `language` field

```bibtex
@article{zhang2024,
  ...,
  language = {zh}  % For Chinese
}

@article{smith2024,
  ...,
  language = {en}  % For English
}
```

### 2. Author Names

**Chinese authors**: Use Chinese characters or Pinyin

```bibtex
% Preferred: Chinese characters
author = {张三 and 李四}

% Acceptable: Pinyin with comma
author = {Zhang, San and Li, Si}

% Wrong: Western order
author = {San Zhang and Si Li}  % ✗
```

**English authors**: Use standard format

```bibtex
author = {Smith, John and Doe, Jane}
```

### 3. Title Format

**Use original language**:

```bibtex
% Chinese title
title = {深度学习在自然语言处理中的应用}

% English title
title = {Deep Learning for Natural Language Processing}
```

### 4. Punctuation

**Chinese entries**: Use Chinese punctuation (，。：)

**English entries**: Use English punctuation (,.:)

## Entry Types

### Journal Article (期刊文章)

**Chinese**:
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

**English**:
```bibtex
@article{smith2024machine,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning for Natural Language Processing},
  journal = {Journal of Machine Learning Research},
  year = {2024},
  volume = {25},
  number = {2},
  pages = {456--489},
  language = {en},
  doi = {10.1234/jmlr.2024.002}
}
```

**Required fields**:
- author
- title
- journal
- year
- language

**Optional fields**:
- volume
- number
- pages
- doi

### Conference Paper (会议论文)

**Chinese**:
```bibtex
@inproceedings{wang2024neural,
  author = {王五 and 赵六},
  title = {神经网络优化方法研究},
  booktitle = {中国计算机大会论文集},
  year = {2024},
  pages = {45--52},
  address = {北京},
  publisher = {电子工业出版社},
  language = {zh}
}
```

**English**:
```bibtex
@inproceedings{johnson2024optimization,
  author = {Johnson, Michael and Brown, Emily},
  title = {Optimization Techniques for Neural Networks},
  booktitle = {Proceedings of the International Conference on Machine Learning},
  year = {2024},
  pages = {234--245},
  address = {Vienna, Austria},
  publisher = {PMLR},
  language = {en}
}
```

**Required fields**:
- author
- title
- booktitle
- year
- language

### Book (图书)

**Chinese**:
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

**English**:
```bibtex
@book{mitchell1997machine,
  author = {Mitchell, Tom M.},
  title = {Machine Learning},
  publisher = {McGraw-Hill},
  year = {1997},
  address = {New York},
  language = {en},
  isbn = {978-0-070-42807-2}
}
```

**Required fields**:
- author
- title
- publisher
- year
- language

### PhD Thesis (博士论文)

**Chinese**:
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

**English**:
```bibtex
@phdthesis{anderson2023deep,
  author = {Anderson, David},
  title = {Deep Reinforcement Learning: Theory and Applications},
  school = {Stanford University},
  year = {2023},
  address = {Stanford, CA},
  language = {en}
}
```

**Required fields**:
- author
- title
- school
- year
- language

### Master's Thesis (硕士论文)

**Chinese**:
```bibtex
@mastersthesis{zhao2024study,
  author = {赵九},
  title = {卷积神经网络在图像分类中的应用研究},
  school = {北京大学},
  year = {2024},
  address = {北京},
  language = {zh}
}
```

### Technical Report (技术报告)

**Chinese**:
```bibtex
@techreport{sun2024report,
  author = {孙十},
  title = {人工智能技术发展报告},
  institution = {中国科学院},
  year = {2024},
  number = {TR-2024-01},
  address = {北京},
  language = {zh}
}
```

### Electronic Resource (电子资源)

**Chinese**:
```bibtex
@misc{li2024blog,
  author = {李十一},
  title = {深度学习入门教程},
  year = {2024},
  url = {https://example.com/tutorial},
  note = {[2024-03-15]},
  language = {zh}
}
```

## Formatting Rules

### Author Names

**Single author**:
```bibtex
author = {张三}  % Chinese
author = {Smith, John}  % English
```

**Multiple authors**:
```bibtex
author = {张三 and 李四 and 王五}  % Chinese
author = {Smith, John and Doe, Jane and Johnson, Michael}  % English
```

**More than 3 authors** (optional):
```bibtex
author = {张三 and 李四 and 王五 and others}
author = {Smith, John and Doe, Jane and Johnson, Michael and others}
```

### Title Capitalization

**Chinese**: No special capitalization

```bibtex
title = {深度学习在自然语言处理中的应用}
```

**English**: Sentence case or title case (depends on venue)

```bibtex
title = {Deep learning for natural language processing}  % Sentence case
title = {Deep Learning for Natural Language Processing}  % Title case
```

### Journal Names

**Chinese**: Full name

```bibtex
journal = {计算机学报}
journal = {软件学报}
journal = {自动化学报}
```

**English**: Full name or standard abbreviation

```bibtex
journal = {Journal of Machine Learning Research}
journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence}
% or abbreviated
journal = {IEEE Trans. Pattern Anal. Mach. Intell.}
```

### Page Numbers

**Use double dash** for ranges:

```bibtex
pages = {123--145}  % Correct
pages = {123-145}   % Wrong
```

### DOI Format

```bibtex
doi = {10.1234/journal.2024.001}
```

## Mixed Bibliography

**Chinese and English entries together**:

```bibtex
% Chinese entry
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习研究},
  journal = {计算机学报},
  year = {2024},
  volume = {47},
  number = {3},
  pages = {123--145},
  language = {zh}
}

% English entry
@article{smith2024machine,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning Advances},
  journal = {Journal of Machine Learning Research},
  year = {2024},
  volume = {25},
  number = {2},
  pages = {456--489},
  language = {en}
}
```

**Sorting**: Chinese entries typically appear before English entries

## LaTeX Integration

### Using biblatex with gb7714-2015

```latex
\documentclass{article}
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{references.bib}

\begin{document}

\section{Introduction}
Recent work~\cite{zhang2024deep,smith2024machine} has shown...

\printbibliography

\end{document}
```

### Compilation

```bash
xelatex document.tex
biber document
xelatex document.tex
xelatex document.tex
```

## Common Mistakes

### 1. Missing Language Field

**Wrong**:
```bibtex
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  journal = {计算机学报},
  year = {2024}
  % Missing language field!
}
```

**Correct**:
```bibtex
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  journal = {计算机学报},
  year = {2024},
  language = {zh}  % Required!
}
```

### 2. Mixed Language in Single Entry

**Wrong**:
```bibtex
@article{key,
  author = {张三 and Smith, John},  % Mixed!
  ...
}
```

**Correct**: Use separate entries or one language

```bibtex
@article{key1,
  author = {张三 and 李四},  % All Chinese
  ...,
  language = {zh}
}

@article{key2,
  author = {Smith, John and Doe, Jane},  % All English
  ...,
  language = {en}
}
```

### 3. Incorrect Author Format

**Wrong**:
```bibtex
author = {San Zhang}  % Western order for Chinese name
```

**Correct**:
```bibtex
author = {张三}  % Chinese characters
% or
author = {Zhang, San}  % Pinyin with comma
```

### 4. Single Dash in Page Range

**Wrong**:
```bibtex
pages = {123-145}  % Single dash
```

**Correct**:
```bibtex
pages = {123--145}  % Double dash
```

### 5. Missing Required Fields

**Wrong**:
```bibtex
@article{zhang2024,
  author = {张三},
  title = {深度学习}
  % Missing: journal, year, language
}
```

**Correct**:
```bibtex
@article{zhang2024,
  author = {张三},
  title = {深度学习},
  journal = {计算机学报},
  year = {2024},
  language = {zh}
}
```

## Verification

### Using Academic Writing Skills

```bash
# Check GB/T 7714 compliance
python verify_bib.py references.bib --standard gbt7714

# Strict mode (fail on warnings)
python verify_bib.py references.bib --standard gbt7714 --strict

# Auto-fix common issues
python verify_bib.py references.bib --standard gbt7714 --fix
```

### Manual Verification

**Checklist**:
- [ ] All entries have `language` field
- [ ] Author names in correct format
- [ ] Titles in original language
- [ ] Required fields present
- [ ] Page ranges use double dash
- [ ] No mixed language in single entry

## Resources

- **GB/T 7714-2015 Standard**: Official document (Chinese)
- **biblatex-gb7714-2015**: LaTeX package for GB/T 7714
- **JabRef**: BibTeX editor with GB/T 7714 support
- **Zotero**: Reference manager with GB/T 7714 export

## Next Steps

- [Bibliography Guide](/guides/bibliography) - General bibliography management
- [Chinese Thesis Skill](/skills/latex-thesis-zh) - Chinese thesis tools
- [Usage Guide](/usage) - Tool usage
