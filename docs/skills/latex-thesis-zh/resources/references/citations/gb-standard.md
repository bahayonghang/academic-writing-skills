# GB/T 7714 Reference format specification


## Directory

- [1. Document type identification](#一文献类型标识)
- [2. Example of description format](#二著录格式示例)
  - [2.1 Journal Article](#21-期刊文章)
  - [2.2 Conference Paper](#22-会议论文)
  - [2.3 Dissertation](#23-学位论文)
- [3. BibLaTeX configuration](#三biblatex-配置)
  - [3.1 Use national standard style](#31-使用国标样式)
  - [3.2 BibTeX style](#32-bibtex-样式)
- [4. Frequently Asked Questions](#四常见问题)
  - [4.1 Author name format](#41-作者姓名格式)
  - [4.2 Multi-author processing](#42-多作者处理)
  - [4.3 DOI Requirements](#43-doi-要求)
  - [4.4 Page number format](#44-页码格式)
- [5. GB/T 7714-2025 key points and transition guidance](#五gbt-7714-2025-要点与过渡期建议)

> This document only covers the **National Standard** description rules (sections 1-4 are based on the 2015 version, and section 5 is the transition guide for the 2025 version).
> Chart numbers, chapter title fonts, etc. belong to the **school-level typesetting convention** (each school determines it, not the national standard content),
> Moved to [`../../templates/generic.md`](../../templates/generic.md); when template is known
> Read instead `templates/thuthesis.md` / `templates/pkuthss.md`.

---

## 1. Document type identification

| Type | Identity | Example |
|------|------|------|
| General books | M | [1] Author. Book title [M]. Place of publication: Publisher, year. |
| Journal article | J | [2] Author. Title[J]. Journal title, year, volume (issue): page number. |
| Dissertation | D | [3] Author. Title [D]. City: School, Year. |
| Conference Paper | C | [4] Author. Title [C]//Conference Name. City, Year: Page Number. |
| Patent | P | [5] Inventor. Patent name [P]. Country: Patent number, date. |
| Electronic literature | EB/OL | [6] Author. Title [EB/OL]. (Published date) [Citation date]. URL. |
| Standard | S | [7] Standard name [S]. Standard number, year. |
| Report | R | [8] Author. Report name[R]. Institution, year. |

## 2. Example of description format

### 2.1 Journal Articles
```bibtex
@article{example_journal,
  author = {张三 and 李四 and 王五},
  title = {深度学习在图像分类中的应用研究},
  journal = {计算机学报},
  year = {2023},
  volume = {46},
  number = {1},
  pages = {1--15},
  doi = {10.11897/SP.J.1016.2023.00001},
}
```

### 2.2 Conference Papers
```bibtex
@inproceedings{example_conf,
  author = {Smith, John and Johnson, Mary},
  title = {A Novel Approach to Object Detection},
  booktitle = {Proceedings of CVPR},
  year = {2023},
  pages = {1234--1243},
  address = {Vancouver, Canada},
}
```

### 2.3 Dissertation
```bibtex
@phdthesis{example_thesis,
  author = {张三},
  title = {基于深度学习的图像识别算法研究},
  school = {清华大学},
  year = {2023},
  address = {北京},
}
```

## 3. BibLaTeX configuration

### 3.1 Use national standard style
```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{refs.bib}

% 文档末尾
\printbibliography[title=参考文献]
```

### 3.2 BibTeX style
```latex
\bibliographystyle{gbt7714-numerical}  % 数字编号
% 或
\bibliographystyle{gbt7714-author-year}  % 作者-年份

\bibliography{refs}
```

## 4. Frequently Asked Questions

### 4.1 Author name format
- Chinese: Last name first, first name last, no punctuation
- English: surname, first name abbreviation. or surname, first name

### 4.2 Multi-author processing
- 3 persons and below: list all
- 4 people and above: first 3 people + "et al." or "et al."

### 4.3 DOI requirements
- It is recommended to add a DOI (it must be described if there is a DOI)
- Format: `doi = {10.xxxx/xxxxx}`

### 4.4 Page number format
- Use hyphens: 1--15 (double dash)
- Do not use wavy lines or single horizontal lines

## 5. GB/T 7714-2025 Key Points and Transition Period Suggestions

>Fact check date: 2026-06.

**Timeline**: GB/T 7714-2025 "Rules for Description of Information and Document References" was released on 2025-12-02.
**Implemented on 2026-07-01**, fully replacing GB/T 7714-2015.

**Main differences from the 2015 version**:

| Change Points | 2015 Edition | 2025 Edition |
|--------|---------|---------|
| Preprint | No special type | Added preprint description type |
| Dataset | No special type | Newly added data set (dataset) description type |
| Description symbols | Inconsistent usage of some symbols | Uniform rules for description symbols |
| Access date | Electronic resources are all cited with citation dates | **Non-online documents no longer require an access date** (online resources still require) |
| Personally responsible persons | The rules for recording names are stricter | The rules for recording personal responsible persons have been adjusted (subject to the original text of the standard) |

**Toolchain Status**: `biblatex-gb7714-2015` series of styles is still the de facto standard; the community has
gb7714-2025 style implementation (LaTeX Studio biblatex-gb7714-2025 beta), not yet fully stable.
Until school templates are upgraded, it is generally still accepted to use the 2015 style.

**Transition period suggestions**:

- Defense/submission before **2026-07-01**: Continue to follow the 2015 version (sections 1-4 of this document).
- Defense/submission for review after **2026-07-01**: First confirm whether the school’s graduate school/library has switched to the new national standard,
  Then decide the style; `verify_bib.py` of this skill supports `--standard gb7714-2025` checking according to the new national standard differences.
- Papers that cite arXiv preprints or public data sets should be described in the new type after switching to the 2025 version.
