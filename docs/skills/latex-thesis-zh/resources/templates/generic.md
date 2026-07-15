# General Chinese paper template

## Directory

- [Applicable scenarios](#适用场景)
- [Basic configuration](#基础配置)
- [Chapter Settings](#章节设置)
- [Chart number](#图表编号)
- [Common school-level formatting conventions](#常见校级排版约定)
- [Font configuration](#字体配置)
- [Compilation method](#编译方式)
- [Notes](#注意事项)
- [Itemized Checklist](#逐项检查清单)

---

## Applicable scenarios

- Used when there is no school-specific template
- Compiled based on the national standard GB/T 7713.1-2006 "Rules for Writing Dissertations" (this version has been abolished, starting from 2026-02-01
  GB/T 7713.1-2025 is implemented instead; the full text of the 2025 version has not been publicly released as an electronic text, and the entry materials in this article are still based on the 2006 version
  The published text is based on and the version relationship is indicated, and the latest regulations of the school shall prevail)

## Basic configuration

```latex
\documentclass[12pt, a4paper]{ctexbook}

% 页面设置
\usepackage[
  top=3cm,
  bottom=2.5cm,
  left=3cm,
  right=2.5cm,
]{geometry}

% 参考文献
\usepackage[backend=biber, style=gb7714-2015]{biblatex}

% 图表标题
\usepackage{caption}
\captionsetup{
  font=small,
  labelsep=space,
  format=hang,
}

% 页眉页脚
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\leftmark}
\fancyfoot[C]{\thepage}
```

## Chapter settings

```latex
% 章节标题格式
\ctexset{
  chapter = {
    format = \centering\heiti\zihao{3},
    nameformat = {},
    titleformat = {},
    number = \chinese{chapter},
    name = {第,章},
    aftername = \quad,
    beforeskip = 20pt,
    afterskip = 20pt,
  },
  section = {
    format = \heiti\zihao{4},
    aftername = \quad,
    beforeskip = 10pt,
    afterskip = 10pt,
  },
  subsection = {
    format = \heiti\zihao{-4},
    aftername = \quad,
    beforeskip = 8pt,
    afterskip = 8pt,
  },
}
```

## chart number

```latex
% 按章编号
\usepackage{amsmath}
\numberwithin{equation}{chapter}
\numberwithin{figure}{chapter}
\numberwithin{table}{chapter}

% 编号格式：3.1
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}
\renewcommand{\theequation}{\thechapter.\arabic{equation}}
```

## Common school-level formatting conventions

> The following are the **common** formatting conventions for dissertations in domestic universities (school-level regulations derived from GB/T 7713.1,
> **Non-GB/T 7714 national standard mandatory content**), the details of each school are different, **the latest format specifications of the school shall prevail**.
> Read `thuthesis.md` / `pkuthss.md` instead when the template is known, the template will automatically handle these formats.

### Chart and formula numbers

- **Figure title**: Below the figure, "Figure 3-1 Figure title content" (hyphen) or "Figure 3.1 Figure title content" (dot), common Song style number 5
- **Table title**: Above the table, the format is the same as the figure title ("Table 3-1" / "Table 3.1"), commonly used in Song style number 5
- **Formula number**: The right side of the formula is right-aligned, usually (3.1) or (3-1) (the first formula in Chapter 3); if a long formula squeezes the number into the next line, it should usually be split into controlled multiple lines instead of being forced into one line
- The hyphen or period depends on the school template: thuthesis uses "Figure 3-1", pkuthss uses "Figure 3.1"

### Chapter title font (common settings)

| Level | Font | Font Size | Alignment |
|------|------|------|------|
| Chapter Title | Bold | Number Three | Centered |
| Section title | Boldface | Size 4 | Left justified |
| Section title | Boldface | Small four | Left-aligned |
| Paragraph title | Boldface | Size 5 | Left aligned |

## Font configuration

```latex
% 确保系统有这些字体
\setCJKmainfont{SimSun}[
  BoldFont=SimHei,
  ItalicFont=KaiTi,
]
\setCJKsansfont{SimHei}
\setCJKmonofont{FangSong}

% 英文字体
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Courier New}
```

## Compilation method

```bash
xelatex main
biber main
xelatex main
xelatex main
```

## Notes

1. Must use XeLaTeX
2. Make sure the required fonts are installed
3. Use biblatex + biber for references
4. Adjust the format according to specific school requirements

## Item-by-item checklist

> For `spec-check` module final inspection (`--template generic`). Fact check date 2026-07-09.
> Every section number in the normative-basis column refers to **GB/T 7713.1-2006, Presentation of Theses and Dissertations**. That edition has been withdrawn and was replaced by GB/T 7713.1-2025 on 2026-02-01; the full 2025 text was not publicly available when this snapshot was checked, so its differences are not asserted here.
> Sources: the National Standard Information Public Service Platform record and a text-layer copy hosted on a university website
> (https://www.xxmu.edu.cn/qks/GB_T7713.1-2006.pdf). Items marked "school-level practice" are **not national-standard clauses**; they are common university requirements, and the student's current school rules take precedence.
> Checking method: `script:<checker>` = `check_spec.py` automatic judgment; `module:<模块>` = go SKILL.md
> Corresponding module command; `llm` = agent interprets item by item according to the text; `manual` = PDF needs to be compiled/printed for verification.

| ID | Inspection items | Specification basis | Inspection method | Applicable |
| --- | --- | --- | --- | --- |
| GEN-01 | The title concisely reflects the most important specific content, no more than 20 words (national standard value, each school may relax, subject to the school's standards); avoid uncommon abbreviations, acronyms, characters, codes and formulas | §5.1.1.2 | script:title_len | General |
| GEN-02 | The title appears exactly the same everywhere in the paper; for funded projects, the fund will be noted at the footer of the page where the title appears | §5.1.1.2 | llm | General |
| GEN-03 | There should be a Chinese abstract, and for international communication there should also be a foreign language (mostly in English) abstract; Chinese first and English last is the school-level practice | §5.1.5.2 + school-level practice | script:abstract_order | General |
| GEN-04 | The abstract is self-contained: describe the research purpose, experimental methods, results and final conclusions, focusing on the results and conclusions | §5.1.5.3 | llm | General |
| GEN-05 | The national standard value for the number of words in an abstract: Chinese should generally not exceed 200 to 300 words, and foreign languages should not exceed 250 content words (a little more may be used for special needs); each school's dissertation generally has higher word count requirements, which shall be subject to the school's specifications (the script only reports the actual number of words, no threshold is set) | §5.1.5.4 | script:abstract_len | General |
| GEN-06 | Do not use figures, tables, chemical structural formulas, non-public symbols and terminology in the abstract (unless there is no alternative); it is university-level practice not to indicate cited document numbers | §5.1.5.5 + university-level practice | script:abstract_no_cite | General |
| GEN-07 | 3 to 8 keywords, start a new line with prominent characters and place them in the lower left corner of the abstract. Try to use standard words such as "Chinese Thesaurus" (each school may tighten the number; the national standard does not specify separators) | §5.1.6 | script:kw_count | General |
| GEN-08 | Abstracts, keywords, classification numbers and table of contents pages should all have English translations corresponding to Chinese | §5.1.10 | script:kw_zh_en_match | General |
| GEN-09 | There should be a table of contents page, which should be placed on a separate page after the sequence and preface; if there are many figures, lists can be listed separately and placed after the table of contents page | §5.1.7 §5.1.8 | llm | General |
| GEN-10 | If notes such as symbols and abbreviations need to be collected, they should be placed after the chart list (conditional item) | §5.1.9 | llm | General |
| GEN-11 | Adopt simplified Chinese characters and legal measurement units officially announced and implemented by the country | §4.2 | llm | General |
| GEN-12 | Terms, symbols, and codes are unified throughout the text; new professional terms/abbreviations/idioms are annotated, and new foreign terms are translated with parentheses to indicate the original text | §4.3 | module:consistency | General |
| GEN-13 | The introduction briefly describes the research purpose, scope, previous work and knowledge gaps, theoretical basis, research methods, etc.; it is concise and concise, not similar to the abstract, and does not become a note of the abstract; the textbook knowledge is not repeated (the review and theoretical analysis can be separated into separate chapters) | §5.2.1 | llm | General |
| GEN-14 | The national standard for figure numbering is continuous throughout the entire text ("Figure 1" and "Figure 2", continuous until the appendix, and has nothing to do with the chapter number. Only one figure is also marked as "Figure 1"); each school generally changes the numbering according to the chapter ("Figure 2.1"/"Figure 3-1"), which is subject to the school's standards and unified throughout the text | §5.2.3 §5.2.4 + school level convention | llm | General |
| GEN-15 | Figures should have numbers and titles, centered at the bottom of the graph; table numbers and titles should be centered above the table; curve graph coordinates must be marked with quantities, standard symbols, and units | §5.2.3 §5.2.4 | llm | General |
| GEN-16 | Table to page: number followed by table title (can be omitted) and "(continued)" (such as "Table 1 (continued)"), the continued table repeats the header and unit statement | §5.2.4 | manual | General |
| GEN-17 | The conclusion should be accurate, complete, clear and concise, and should be the final overall conclusion, not a simple repetition of each paragraph's summary; when it is impossible to derive a conclusion, only necessary discussions can be made; suggestions, research ideas, unresolved problems, etc. can be put forward | §5.2.5 | llm | General |
| GEN-18 | References shall be carried out in accordance with GB 7714 "Rules for describing references after the text" (citations without date shall be carried out according to the latest version) | §5.2.6 | module:bibliography | General |
| GEN-19 | The reference list starts on a new page; entries are sorted with two empty words, top boxes when returning, and no punctuation marks are added after the document | §6.6 | manual | General |
| GEN-20 | Notes may be scattered as footnotes at the bottom of the page, but must not be included in the text | §5.2.7 | llm | General |
| GEN-21 | Appendices are numbered in uppercase letters in order (Appendix A, Appendix B...). The number and title each occupy one line and are placed in the center above the article. Each appendix is on a separate page; the article numbers in the appendix are such as B.1, B.1.1 | §6.5 Appendix B | script:appendix_letter | General |
| GEN-22 | Chapter and section numbers are arranged in the top grid, with one word left between the number and the title or text. The chapter title occupies two lines; the numbering level is up to four levels (x.x.x.x, Appendix B normative example) | §6.3 Appendix B | script:heading_depth | General |
| GEN-23 | Formulas should be placed on a new line in the middle. Long formulas should be wrapped at the equal sign or after symbols such as + and - as much as possible; numbers should be aligned to the right; "in the formula:" should be placed on a separate line starting with two empty words | §6.4 | module:format | General |
| GEN-24 | Page numbers: Starting from the introduction (including main text, references, appendices, acknowledgments, etc.), Arabic numerals are used to code consecutively; the leading part (abstract page, table of contents page, list, symbol description) is coded consecutively with Arabic numerals according to the national standard. All schools generally use Roman numerals, and the school's standards shall prevail | §4.7 + school-level practices | manual | General |
| GEN-25 | Page: 25mm or more for the head/slotting edge, 20mm or more for the footing/cutout (each school often gives the exact cm value, subject to the school's specifications); A4 format (210mm×297mm) | §4.5 §6.7 | manual | General |
| GEN-26 | Each chapter starts on a new page (or on the right page): The national standard does not have this clause, it is a school-level practice, and the school's standards shall prevail | School-level practice | llm | General |
| GEN-27 | There is a "Summary of this Chapter" at the end of each chapter: the national standard does not have this clause, and some schools require it, and the school's standards shall prevail | School-level practices | llm | General |

> Number of words in main text/introduction/conclusion, minimum number of references and proportion in the past five years: GB/T 7713.1-2006 **There is no corresponding clause**,
> Therefore, this list does not include such items; when the school has explicit requirements, the school's specifications will be organized into `--spec-file` custom list
> (The format is the same as the table above) When running the final inspection, do not apply values from other schools.
