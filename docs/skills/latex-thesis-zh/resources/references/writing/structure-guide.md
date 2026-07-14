# Dissertation Structure Guide


## Directory

- [1. Overall structure of the paper](#一论文整体结构)
  - [Prefix (required)](#前置部分必需)
  - [Text part](#正文部分)
  - [Postpart (required)](#后置部分必需)
- [2. Chapter numbering specifications](#二章节编号规范)
  - [Hierarchy](#层级结构)
  - [Number format](#编号格式)
- [3. Page settings](#三页面设置)
  - [Margin](#页边距)
  - [Header and Footer](#页眉页脚)
  - [Font size](#字体字号)
- [4. Common Checklist](#四常见检查清单)
  - [Prefix part](#前置部分)
  - [Text part](#正文部分)
  - [Post part](#后置部分)

---

## 1. Overall structure of the paper

### Prefix part (required)
1. **Cover** (cover)
   - Thesis title (Chinese and English)
   - Author name
   - Tutor name
   - Subject major
   - Submission date

2. **Declaration of originality and authorization** (declaration)
   - Statement of originality
   - Authorization for use
   - Signature page

3. **Abstract** (abstract)
   - Chinese abstract (500-1000 words)
   - Keywords (3-5)
   - English abstract (Abstract)
   - Keywords

4. **Table of Contents** (toc)
   - Automatically generated
   - Include chapter and page numbers

5. **Symbol comparison table** (recommended)
   - Explanation of symbols
   - List of abbreviations

### Text part

6. **Chapter 1: Introduction**
   - Research background
   - Research significance
   - Technical bottlenecks/research gaps
   - scientific questions
   - Research question/scientific question
   -Main contributions
   - Paper structure

7. **Chapter 2 (dual track, choose one according to paper type, no mixing)**
   - **Industrial/Process Background Paper → Process Analysis Chapter**: Process Flow Analysis + Modeling/Control Difficulties + Full Text Overall Method Framework
     (process analysis → variables/data → difficulties → overall framework → summary). When the research review is already covered in the introduction, **do not add a separate literature-review chapter**. See [`process-chapter-guide-zh.md`](process-chapter-guide-zh.md) for the detailed form.
   - **CS/Methodology Paper → Related Work/Literature Review Type**: Classified review of research status, comparative analysis of existing methods, and identification of research gaps.
   - Criterion: Whether the industrial/process object runs through the whole text (through → process analysis chapter; methodology is the main focus, and the object only appears later → related
     working style or method chapter style). If the summary is already in the introduction (accounting for about 45% of the introduction, see [`introduction-guide-zh.md`](introduction-guide-zh.md))
     Fully developed, Chapter 2 shall not repeat the review chapter.

8. **Chapter 3 to Chapter N-1: Core Content**
   - Method/Model/Algorithm
   - Experimental design
   - Result analysis

9. **Chapter N: Summary and Outlook**
   - Work summary
   - Contribution closure
   - Research limitations
   - future direction

### Postpart (required)

10. **References** (bibliography)
    - GB/T 7714 format
    - Numbered in order of reference

11. **ACKNOWLEDGMENT** (acknowledgment)
    - Thanks to the tutor
    - Thanks to the collaborators
    - Thanks to the funding agencies

12. **List of papers published during the degree study** (resume/publications)
    - Published papers
    - Accepted papers
    - Submitted papers (optional)

13. **Appendix** (if any)
    - Supplementary materials
    - code listing
    - Detailed derivation

## 2. Chapter numbering specifications

### Hierarchy
```
第1章 绪论
  1.1 研究背景
    1.1.1 问题描述
    1.1.2 挑战分析
  1.2 研究意义
第2章 相关工作
  2.1 ...
```

### Number of direct sections

- The direct subordinate `\section` of the main chapter is controlled within **5 sections** by default. This is not a mechanical word count requirement, but a clear argumentation loop for each chapter.
- **Exception to the second chapter of the process analysis chapter**: Common **4~7 direct sections** (including introduction and summary), the median number of 5 reference papers is 5~6, no mechanical alarm will occur if it exceeds 5 sections; when it exceeds 5 sections, priority will be given to checking variable/data sections that can be merged. For details on how to write, see [`process-chapter-guide-zh.md`](process-chapter-guide-zh.md).
- The recommended structure is: introduction, basic theory/problem description, model/algorithm/framework, experiment/case/application, and summary of this chapter.
- "Summary of this chapter" is written as one natural paragraph by default, and is concluded by "Problem/Objective -> Work/Methods of this Chapter -> Key Process/Evidence -> Value of Result -> Support for the Main Line of the Whole Chapter"; unless required by the school template or instructor, it will not be split into multiple short paragraphs or lists. See the "Summary at the end of the main article" section of [`thesis-writing-guide.md`](thesis-writing-guide.md) for details.
- When a chapter has more than 5 direct sections, adjacent functions will be merged first:
  - Merge "Data Preprocessing", "Variable Selection" and "Problem Definition" into "Basics of Problem Description and Modeling".
  - Organize "Model Framework", "Model Modeling" and "Algorithm Design" into a method main section, under `\subsection`.
  - Put "Experimental Settings", "Result Analysis" and "Robustness Analysis" into the main section of the experiment or case, under `\subsection`.
- If there is a school-level template or instructor requirement that requires more than 5 sections, the chapter introduction or introduction should explain how each section is organized around the same chapter title.

### Chapter title and section title snap together

- The chapter titles of the method chapter, model chapter, algorithm chapter and system application chapter of the text should try to reflect "research object + problem/task + method/path".
- The section title should inherit the object, problem or method in the chapter title, and should not just include "data collection", "result discussion", "model establishment" and other general titles that can be moved to any chapter.
- The general title can be retained, but the introduction must explain how it serves the object and issues of this chapter.

### Numbering format
- Chapter: Chapter X (Chinese numerals or Arabic numerals)
- Section: X.1
- Section: X.1.1
- Section: X.1.1.1 (try to avoid exceeding level four)

### Specifications for the blurb after the title
- After each chapter, each section, each subsection, and the four-level headings that need to be discussed, an introduction should be written first.
- The introduction should explain at least two to three of four things: the object of discussion at this level, the purpose of writing, the relationship with the previous level, and the organization of the following.
- Prohibit headings that go directly to lists, formulas, charts, algorithm contexts, or subheadings without any transition instructions.
- The introduction should be written as a complete paragraph rather than a short reminder; it is recommended to use explicit guidance expressions such as "This chapter/section will..." "The following will expand from...".
- The **Chapter Introduction** of each chapter of the main text (Chapter 2 to the conclusion) should be written in two paragraphs, about 300~500 words, connecting the previous chapter and the next: the first paragraph uses the chapter number ("Chapter See the "Introduction to the main article" section of [`thesis-writing-guide.md`](thesis-writing-guide.md) for details.
- The **Chapter Summary** of each chapter of the main text should be written as a single paragraph: it does not repeat the table of contents, does not add new results, and does not replace the final conclusion; it should summarize the issues, methods, evidence, value and support for the main line of the full text.
- Exceptions usually include: abstract, table of contents, references, acknowledgments, appendices and other non-main argument units.

## 3. Page settings

### Margins
| Location | Size |
|------|------|
| Top | 3.0 cm |
| Lower | 2.5 cm |
| Left | 2.5-3.0 cm |
| Right | 2.5 cm |

### Header and footer
- Header: Chapter title or "PhD thesis of XX University"
- Footer: page number (centered)
- Use Roman numerals on the summary page
- Use Arabic numerals in the text

### Font size
| Content | Font | Font size |
|------|------|------|
| Text | Song Dynasty | P4/5 |
| Chapter Title | Boldface | Number Three |
| Section Title | Boldface | Number Four |
| Table title/Figure title | Song Dynasty | Number 5 |

## 4. Common checklist

### Preface part
- [ ] Cover information is complete and accurate
- [ ] Declaration page signed
- [ ] The number of words in the abstract meets the requirements
- [ ] Appropriate number of keywords
- [ ] Contents page number is correct
- [ ] complete symbol table

### Text part
- [ ] Chapter 1 includes research background, significance and contribution
- [ ] The introduction forms the closing chain of "Background -> Technical bottlenecks/research gaps -> Scientific issues -> Contribution of this article -> Chapter arrangement"
- [ ] Literature review covers main related work
- [ ] There is an introductory paragraph after each chapter, section, subsection and fourth-level heading.
- [ ] At the end of the main article, "Summary of this Chapter" uses a natural paragraph to summarize the problem, methods, evidence, value and main line support.
- [ ] Methods chapters describing the motivation, design and technical advantages of each core module
- [ ] Method description is clear and complete
- [ ] The experimental design is reasonable
- [ ] Objective analysis of results
- [ ] The last chapter responds to the contribution of the introduction, with summary, limitations and prospects.

## 5. Main line of chapter writing

When doing chapter-level rewriting or writing plans, read [`thesis-writing-guide.md`](thesis-writing-guide.md) first. The structure check not only checks whether chapters exist, but also checks whether the text is progressively developed around the same scientific problem:

```text
研究背景 -> 技术瓶颈/研究空白 -> 科学问题 -> 本文方法/章节工作 -> 实验证据 -> 贡献闭合 -> 局限与展望
```

If a chapter only lists multiple works side by side, a bridging relationship such as "This chapter is based on the previous chapter..." or "Revolving around the same scientific issue, this chapter further..." should be added.

### Post part
- [ ] Uniform reference format
- [ ] Acknowledgments are appropriate
- [ ] Complete list of published papers
- [ ] Appendix number is correct
