# Tsinghua University thesis template (thuthesis)

>Fact check date: 2026-07-09. Template fact source: thuthesis v7.7.1 manual (thuthesis.dtx) vs.
> CHANGELOG (GitHub tuna/thuthesis); the source of school regulations facts can be found at the head of the "Itemized Checklist".

## Template information
- **Template name**: thuthesis
- **GitHub**: https://github.com/tuna/thuthesis
- **CTAN**: https://ctan.org/pkg/thuthesis
- **Document Class**: `\documentclass{thuthesis}`
- **Version Baseline**: v7.7.1 (2026-05-26, synchronized with the May 2026 edition of the "Writing Guide": unified wording for PhD and master's authorization pages).
  Get the latest version from CTAN or GitHub releases before writing. The old version may not be consistent with the school's review requirements.

## Special format requirements

### Chart number
- Format: Numbered by chapter, the template is connected by periods by default: `图 2.1` / `表 2.1`; graduate students require "." or "-" (such as `图 2-1`), unified throughout the article
- Configuration: Automatic template processing; use `\thusetup{number-separator = -}` when a hyphen is required (or set figure/table/equation-number-separator separately)

### References
- BibTeX style: `thuthesis-numeric.bst` (numeric number) or `thuthesis-author-year.bst` (author-year),
  Distributed with the template, derived based on gbt7714 v2.1.6+, needs to cooperate with natbib:
  `\usepackage[sort]{natbib}` + `\bibliographystyle{thuthesis-numeric}` + `\bibliography{refs}`
- Also use `biblatex-gb7714-2015` (backend=biber)
- Note: The old dedicated bst style in the v4 era has been abandoned, and the current version only provides the above two bst

### Formula number
- Format: numbered by chapter, the template default period is `(2.1)`; used with the chart, the number-separator can be changed to `(2-1)`, unified throughout the article

### Page settings
- Automatically handled by templates
- Do not manually modify page margins

## Compilation method

```bash
# 推荐使用 latexmk
latexmk -xelatex main.tex

# 或手动编译
xelatex main
bibtex main
xelatex main
xelatex main
```

## Common commands

```latex
% 封面信息
\thusetup{
  title = {论文标题},
  title* = {English Title},
  author = {作者姓名},
  supervisor = {导师姓名},
  degree-category = {工学博士},
}

% 摘要
\begin{abstract}
  摘要内容...
\end{abstract}

\begin{abstract*}
  English abstract...
\end{abstract*}

% 关键词
\thusetup{
  keywords = {关键词1, 关键词2, 关键词3},
  keywords* = {keyword1, keyword2, keyword3},
}
```

## Notes

1. Must be compiled using XeLaTeX
2. Make sure the system has Chinese fonts (SimSun, SimHei, KaiTi) installed
3. Use the template matching style for references (thuthesis-numeric.bst / thuthesis-author-year.bst or biblatex-gb7714)
4. Check whether the template version is the latest before submitting (CTAN/GitHub releases)

## Item-by-item checklist

> For `spec-check` module final inspection (`--template thuthesis`). Fact check date 2026-07-09. Source:
>
> - School regulations entry (§ number is its own chapter number): "Guidelines for Postgraduate Dissertation Writing", Tsinghua University Graduate School 2025
> Public copy of March version (official domain name hosting)
>   https://www.dhs.tsinghua.edu.cn/wp-content/uploads/2023/12/2025032107444819.pdf ；
> The official release channel of the Graduate School is limited to on-campus network access. The original text of the May 2026 edition is not publicly available, according to thuthesis
> CHANGELOG The difference is only "unifying the wording of the doctoral and master's authorization pages".
> - Template entry (based on column label "thuthesis manual"): thuthesis v7.7.1 manual (thuthesis.dtx,
>   GitHub tuna/thuthesis）。
>
> This guide **does not specify** main-text, introduction, or conclusion word counts; a minimum reference count; a five-year recency ratio; a ban on citations in the conclusion; or a mandatory "Chapter Summary" in every chapter. The checklist therefore contains no such entries, and values from other universities must not be imported.
> Checking method: `script:<checker>` = `check_spec.py` automatic judgment; `module:<模块>` = go SKILL.md
> Corresponding module command; `llm` = agent interprets item by item according to the text; `manual` = PDF needs to be compiled/printed for verification.

| ID | Inspection items | Specification basis | Inspection method | Applicable |
| --- | --- | --- | --- | --- |
| THU-01 | Thesis title "Strictly controlled within 25 Chinese characters (characters)" (the guidelines do not have a subtitle total clause, and the subtitle will be included in the 25-character determination) | §2.3.1 | script:title_len | General |
| THU-02 | Chinese abstract is limited to 800~1000 Chinese characters (characters) | §2.3.5 | script:abstract_len | General |
| THU-03 | Abstract length is limited to one page | §2.3.5 | manual | General |
| THU-04 | Keywords "no more than 5, each keyword is separated by a semicolon" (officially there is no lower limit for the number, manual judgment; keywords in the thuthesis source file are separated by Western commas, and are automatically output as full-width semicolons by the template) | §2.3.5 | llm | General |
| THU-05 | English Keywords correspond to keywords in the Chinese abstract part | §2.3.5 | script:kw_zh_en_match | General |
| THU-06 | The Chinese abstract comes first and the Abstract comes last (§2.1 composition order). The text content of the Chinese version of the abstract corresponds to the English version | §2.1 §2.3.5 | script:abstract_order | General |
| THU-07 | No pictures, charts, tables, or other illustrative materials appear in the abstract | §2.3.5 | llm | General |
| THU-08 | The abstract should not be written as an outline of the full text (avoid the "Chapter 1...; Chapter 2..." statement), focus on the results and conclusions | §4.3 | llm | General |
| THU-09 | List the table of contents to the second-level section heading (for example, 2.2.5) | §2.3.6 | llm | General |
| THU-10 | It is generally not recommended to use three-level section headings; the numbering is up to four paragraphs (x.x.x.x, \subsubsection), and no deeper levels appear | §2.3.9.2 | script:heading_depth | General |
| THU-11 | The components and order comply with the regulations (Chinese and English cover, list, authorization statement, abstract, Abstract, table of contents, list and symbol description, main text, references, appendices, acknowledgments, statement, resume and academic achievements, instructor's comments, defense committee resolution), each component is independent, and each part starts from a new page | §2.1 | llm | General |
| THU-12 | The main text starts on the right page of another page, and each chapter should start on a new page | §2.3.9.1 | script:new_page_chapter | General |
| THU-13 | Chapter title such as "Chapter 1 Introduction": Use Arabic numerals for the chapter number, and leave a Chinese character between the chapter number and the title name (template name={Chapter, Chapter} automatically processed) | §2.3.9.2 | llm | General |
| THU-14 | "List of Dissertation Steering Group, Public Reviewers and Defense Committee" shall be limited to one page in principle | §2.3.3 | manual | General |
| THU-15 | Figures, tables and expressions are numbered according to chapters. The two numbers are connected with a half-width horizontal line "-" or a decimal point "." (such as "Figure 2-1" or "Figure 2.1"), and the whole article is unified; thuthesis defaults to a period, and the number-separator option can be used to change the hyphen | §2.3.19 | llm | General |
| THU-16 | The figure sequence and title are placed below the figure (centered at 11pt), and the table sequence and title are placed above the table; the table uses a three-line table (1.5 points for the upper and lower edges, 1 point for the third line, and auxiliary lines can be added if necessary) | §2.3.19 | module:tables | General |
| THU-17 | Each sub-figure should be sequenced with (a), (b), (c) and must have a sub-figure title | §2.3.19 | llm | General |
| THU-18 | Figures should be placed immediately after the text that first cites the figure (figure cross-references are complete and without breaks) | §2.3.19 | module:references | General |
| THU-19 | For cross-page figures, mark the word "continuation" on the next page; for continued tables, add the word "continuation" before the table sequence on each page and repeat the table header; for charts that are too wide, rotate them counterclockwise 90° for placement | §2.3.19 | manual | General |
| THU-20 | The expression serial number plus parentheses are placed at the end of the line on the right side of the expression; longer expressions are wrapped after the operator or parentheses, and the upper and lower lines are aligned at "=" as much as possible | §2.3.19 | module:format | General |
| THU-21 | Reference description and annotation shall be uniformly implemented in accordance with GB/T 7714-2015 (without distinction between science and engineering and humanities and social sciences); only one of "sequential coding system" or "author-publishing year system" shall be selected and unified throughout the text | §3 §3.4 | module:bibliography | General |
| THU-22 | The reference list corresponds one-to-one with the citations in the text; the cited reference list is placed on a separate page after the text; reading references can be included in the appendix (titled "Bibliography") | §3.5 §3.1 | module:bibliography | General |
| THU-23 | Use the template to match the literature style: thuthesis-numeric / thuthesis-author-year (bst with natbib, or biblatex's style=thuthesis-author-year), the style is slightly adapted from gbt7714 / biblatex-gb7714-2015 | thuthesis manual | llm | General |
| THU-24 | Appendices are numbered in uppercase letters in order (Appendix A, Appendix B...). If there is only one appendix, it is also numbered as "Appendix A". Each appendix should have a title | §2.3.11 | script:appendix_letter | General |
| THU-25 | Figures and formulas in the appendix are numbered separately, such as "Figure A.1", "Table B.2" and "Formula (C-3)" | §2.3.11 | llm | General |
| THU-26 | The introduction generally includes: the posing of the problem, the background and significance of the topic, literature review, research methods, and the structure of the paper; the literature review should be "described" with "comments" | §4.4 | llm | General |
| THU-27 | The conclusion is the final and overall conclusion, not a simple repetition of the summaries of each chapter in the text; it explains the limitations of the research work and puts forward opinions or suggestions for future work | §4.6 | llm | General |
| THU-28 | Evaluate your own research results realistically: avoid using "first", "leading", "filling the gap" or similar words unless there is sufficient evidence | §4.6 | llm | General |
| THU-29 | Except for international students, all written in simplified Chinese; non-universal new nouns, new terms, and new concepts will be explained clearly | §4.1 §2.3.18 | llm | General |
| THU-30 | Quantities and units strictly comply with GB 3100-1993, GB/T 3101-1993, GB/T 3102-1993. The whole text is unified and the two types are not allowed to be mixed | §2.3.18 | llm | General |
| THU-31 | Acknowledgments are limited to one page, and the title and header content are both "Acknowledgments" | §2.3.12 | manual | General |
| THU-32 | The statement is on a separate page, and the title and header content are both "Statement" | §2.3.13 | manual | General |
| THU-33 | Academic achievements during schooling are divided by type and numbered consecutively (academic papers, monographs/translations, patents, research reports, works, etc.); if no results have been obtained, write "none"; for accepted and unpublished papers, add parentheses to indicate that they were accepted by ×××× journals | §2.3.14 | llm | General |
| THU-34 | Margins 3.0 cm top, bottom, left, and right, gutter 0 cm, header/footer 2.2 cm from border; A4 standard paper | §2.4.1 §2.2 | manual | Universal |
| THU-35 | The header starts from "Abstract", the content is the same as the chapter title of the part, the odd and even pages are the same, the home page of each part also has the header, and the 5-point font is centered | §2.4.2 | manual | General |
| THU-36 | Page numbers: From the Chinese abstract to symbols and abbreviations, use uppercase Roman numerals consecutively from Ⅰ; starting from Chapter 1 of the main text, use Arabic numerals consecutively from 1; page numbers should be placed in the center of the footer without modification lines on both sides | §2.4.2 | manual | General |
| THU-37 | Double-sided printing starting from the Chinese abstract (four parts including the cover are single-sided, without header pages) | §2.4.1 | manual | General |
