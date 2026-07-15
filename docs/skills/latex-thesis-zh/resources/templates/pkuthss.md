# Peking University thesis template (pkuthss)

>Fact check date: 2026-07-09. Template source of fact: pkuthss v1.9.4 (Codeberg repository cls/docs/examples);
> For the source of facts about school regulations, please see the head of the "Item-by-item Checklist".

## Template information
- **Template name**: pkuthss
- **Current warehouse**: https://codeberg.org/CasperVector/pkuthss（原 Gitea warehouse has been archived and moved out in 2024-08)
- **Document Class**: `\documentclass[doctor]{pkuthss}`
- **Maintenance Status**: The original author's repository was last substantially updated to 2024-04; the community has active branches
  (such as iofu728's Overleaf adapted version, which complies with the 2022 graduate student format review), before use
  **Subject to the school’s latest format review requirements**. If necessary, give priority to branches that have recently passed the review.

## Special format requirements

### Chart number
- Format: `图3.1` / `表3.1` (Chapter number. Serial number, use dots)
- Configuration: Template automatic processing

### References
- Style: `biblatex-gb7714-2015`
- Recommendation: use biblatex

### Special Chapter
- "Main Symbols Comparison Table" is a **conditional item**: Official Guidelines §1.6 - "If a large number of symbols, signs, and abbreviations are used in the paper... a 'Main Symbols Comparison Table' should be prepared" (after placing the table of contents and before the main text); "If the above symbols and abbreviations are not large in number, they do not need to be set up." Just explain it as soon as it appears in the text.
- Neither the pkuthss template nor the official examples have this chapter, you can add it if necessary.

## Compilation method

```bash
# 使用 latexmk
latexmk -xelatex thesis.tex

# 使用 make（如果有 Makefile）
make
```

## Common commands

```latex
% 文档类选项
\documentclass[
  doctor,           % 博士论文
  % master,         % 硕士论文
  openany,          % 章节可在任意页开始
  oneside,          % 单面打印
]{pkuthss}

% 封面信息
\pkuthssinfo{
  cthesisname = {博士研究生学位论文},
  ethesisname = {Doctor Thesis},
  ctitle = {论文标题},
  etitle = {English Title},
  cauthor = {作者姓名},
  eauthor = {Author Name},
  studentid = {学号},
  date = {\zhdigits{2024}年\zhnumber{6}月},
  school = {信息科学技术学院},
  cmajor = {计算机软件与理论},
  emajor = {Computer Software and Theory},
  direction = {研究方向},
  cmentor = {导师姓名},
  ementor = {Supervisor Name},
  ckeywords = {关键词1，关键词2，关键词3},
  ekeywords = {keyword1, keyword2, keyword3},
}
```

## Notes

1. Compile with XeLaTeX
2. "Main Symbols Comparison Table" is a conditional item (should be written only when the number of symbols/abbreviations is large, see official guide §1.6), and the template does not have this chapter built-in
3. Pay attention to check the header format
4. The reference format must be strictly followed.
5. Template maintenance has been slowed down (the original warehouse has been archived), please confirm with the college the format review requirements for that year before submission.

## Item-by-item checklist

> For `spec-check` module final inspection (`--template pkuthss`). Fact check date 2026-07-09. Source:
>
> - School regulations entry (§ number is its own chapter number): "Guidelines for Postgraduate Dissertation Writing", Peking University Degree Office
> May 2014 (the current download item "Writing Guide V2.0" on the official website of the Graduate School is still mounted on 2025-07):
> https://grs.pku.edu.cn/docs/2018-03/20180301082929918531.pdf (Master’s material page),
> https://grs.pku.edu.cn/docs/2019-05/20190524160158375113.pdf (Ph.D. material page, the two documents are consistent).
> - Template entry (based on column label "pkuthss documentation"): pkuthss v1.9.4 (2024-03-07) cls/docs/examples,
>   https://codeberg.org/CasperVector/pkuthss 。
>
> This guide **does not specify** main-text, introduction, or conclusion word counts; a minimum reference count; a five-year recency ratio; a ban on citations in the conclusion; or a mandatory "Chapter Summary" in every chapter. The checklist therefore contains no such entries, and values from other universities must not be imported.
> Checking method: `script:<checker>` = `check_spec.py` automatic judgment; `module:<模块>` = go SKILL.md
> Corresponding module command; `llm` = agent interprets item by item according to the text; `manual` = PDF needs to be compiled/printed for verification.

| ID | Inspection items | Specification basis | Inspection method | Applicable |
| --- | --- | --- | --- | --- |
| PKU-01 | The title should be concise and to the point, "generally should not exceed 20 Chinese characters (characters)"; if there is a subtitle, use a dash to separate the main and subtitles (the guide does not have a subtitle total clause, and the subtitles will be included in the 20-word determination) | §1.1 | script:title_len | General |
| PKU-02 | Ph.D. Chinese Abstract General 800-1000 Chinese characters (symbols) | §1.3 | script:abstract_len | Ph.D. |
| PKU-03 | Master's thesis abstract "generally about 600 Chinese characters" (the official original text has no judgment interval, and is manually judged based on the actual number of words) | §1.3 | llm | Master |
| PKU-04 | There should be 3~5 keywords, separated by commas between each keyword; put them at the bottom of the abstract page and write on a new line | §1.3 | script:kw_count | General |
| PKU-05 | The abstract of the paper cannot contain pictures, tables or other illustrative materials; fund support is marked in the footer of the first page of the abstract | §1.3 | llm | General |
| PKU-06 | The abstract must not be written as an outline of the full text (avoid the statement "Chapter 1...; Chapter 2...") | Chapter 2 | llm | General |
| PKU-07 | The English abstract includes from top to bottom: English title, author's name, professional name (after the name in brackets), instructor's name, "ABSTRACT", abstract content and keywords (KEY WORDS) | §1.4 | llm | General |
| PKU-08 | The content of the English abstract is consistent with the Chinese abstract; KEY WORDS corresponds to the Chinese keywords, with the first letter capitalized and separated by half-width commas | §1.4 | script:kw_zh_en_match | General |
| PKU-09 | The ten components are: cover, copyright statement, Chinese abstract, English abstract, table of contents, main text (including introduction and conclusion), references, appendices, acknowledgments/postscript or instructions, originality statement and authorized use instructions; each part is independent and each part starts from a new page | Chapter 1 opening | llm | General |
| PKU-10 | Chinese abstract first, English abstract (ABSTRACT) last | Beginning of Chapter 1 | script:abstract_order | General |
| PKU-11 | When using a large number of symbols, signs, and abbreviations, a "Main Symbols Comparison Table" should be prepared (after placing the table of contents and before the main text); if the number is not large, it can be omitted, and it will be explained when it appears in the text (conditional items, non-essential chapters) | §1.6 | llm | General |
| PKU-12 | The table of contents is generally listed to the third-level heading, that is, the second-level section heading (such as 2.2.5) | §1.5 | llm | General |
| PKU-13 | It is generally not recommended to use section headings of level three or above; levels with more than four numeric numbers should not appear | §1.7.1 | script:heading_depth | General |
| PKU-14 | Use Chinese numerals for chapter numbers (such as "Chapter 1 Introduction"), leave a Chinese character blank between the chapter number and the title, and center the bold number three; use Arabic numerals for section numbers, and use half-width decimal points to connect numbers | §1.7.1 | llm | General |
| PKU-15 | Figures, tables and expressions are numbered according to chapters, and the two numbers are connected with a half-width decimal point "." ("Figure 2.1", "Table 5.6", "Formula (1.2)"; the guide only gives the period format, no hyphen option) | §1.7.4 | llm | General |
| PKU-16 | The figure sequence and title should be placed below the figure (Chinese Song 11pt centered), and the table sequence and table title should be placed above the table; subfigures should be sequenced with (a), (b), (c) and must have subfigure names | §1.7.4 | llm | General |
| PKU-17 | For continuation tables, add the word "continuation" before the table sequence on each page | §1.7.4 | manual | General |
| PKU-18 | Footnotes are marked with ①②③ style superscripts, the serial numbers are arranged by page (footnote serial numbers on different pages do not need to be consecutive), and the content is in Song style Xiaowu | §1.7.3 | manual | General |
| PKU-19 | Documents cited in the paper must be described, and uncited documents must not appear; references are recorded after the main text and are not divided into chapters; foreign language documents are directly described in foreign languages | §1.8 | module:bibliography | General |
| PKU-20 | The annotation method adopts "sequential coding system" or "author-publishing year system"; in the sequential coding system, the document serial number is placed in "[ ]" and marked in the index position with superscript | §1.8 | module:bibliography | General |
| PKU-21 | pkuthss The format implemented by the default biblatex style caspervector is not consistent with the "Writing Guidelines"; you can consider using style=gb7714-2015 instead, or use the ugly option of biblatex-caspervector to be closer to the national standard format | pkuthss Documentation | llm | General |
| PKU-22 | Appendices are numbered in uppercase letters in order (Appendix A, Appendix B...). When there is only one appendix, "Appendix A" is also numbered; the diagrams in the appendix are such as "Figure A.1", "Table B.2" and "Formula (C-3)"; appendices are not necessary | §1.9 | script:appendix_letter | General |
| PKU-23 | The acknowledgment should be modest, sincere, and realistic, and the number of words should not exceed 1000 Chinese characters | §1.10 | llm | General |
| PKU-24 | Personal resume, academic papers and achievements published during school, etc. should be placed after the appendix and before acknowledgments; the list of published papers requires the same format as the reference list | §1.10 | llm | General |
| PKU-25 | The introduction roughly consists of five parts: posing the problem, background and significance of the topic, literature review, research methods, and paper structure arrangement | Chapter 2 | llm | General |
| PKU-26 | Evaluate your own research results realistically: unless there is sufficient evidence, avoid using "first time", "leading", "filling the gap" or similar words | Chapter 2 | llm | General |
| PKU-27 | Written in simplified Chinese characters officially announced and implemented by the state (excluding ancient characters, foreign language citations, foreign language and literature papers, etc.; approved English papers must use Chinese cover) | Chapter 1 Opening | llm | General |
| PKU-28 | Paper standard A4; page margins top/bottom/left/right/gutter are 3.0/2.5/2.6/2.6/0cm, gutter position left, left and right symmetrical margins; header margin 2.0cm, footer margin 1.75cm | §1.11 | manual | Universal |
| PKU-29 | Header No. 5 in Song font is centered, odd and even pages are different (odd pages = name of each chapter, even pages = "Ph.D. thesis of Peking University" or "Master's thesis of Peking University"), and a 0.75 pt horizontal line is underlined in the header text | §1.11 | manual | General |
| PKU-30 | Page numbers: use Roman numerals from "Abstract" to "Table of Contents"; use Arabic numerals from "Chapter 1 Introduction" | §1.11 | manual | General |
| PKU-31 | Each chapter starts from a new page (pkuthss defaults to double-sided mode, each chapter starts from the right page/odd page; you can add the openany option to avoid a blank page at the end of the chapter) | pkuthss documentation | script:new_page_chapter | General |
| PKU-32 | Double-sided printing (except cover and originality statement), left-side binding; the electronic version is a separate PDF and the content is exactly the same as the paper version (except signature) | Chapter 3 | manual | General |
| PKU-33 | When formatting the double-blind version of the paper, the cover must use \makeblind instead of \maketitle, remove the acknowledgments and other sections, and hide other parts that may reveal personal information (use the beabstract environment for Western abstracts; run the blind-review module before submitting for review) | pkuthss documentation §2.2 | manual | General |
| PKU-34 | When the format review prompts that the font size does not strictly meet the standards, you can add ugly to the document type option (the template intentionally deviates from the school's written regulations in a few numerical details by default) | pkuthss documentation | manual | General |
| PKU-35 | The template does not attempt to set the default font size of the table. You must set it yourself according to the school regulations | pkuthss documentation | manual | General |
