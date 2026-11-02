# Defense Deck Framework

This file specifies the page order, the chapter roles, and the page sequence of each chapter role in a doctoral thesis defense deck. For the page count of each page role, see [Time Budget](time-budget.md). For the layouts, see [Layout Catalog](slide-layouts.md).

The framework comes from a 94-page doctoral predefense pptx (16:9). This file records only the structure and the page types of that pptx. The author, the thesis title, and the body content of that pptx do not go into any file of this skill.

## Deck Page Order

1. Cover (`cover`).
2. Overall TOC (`toc`): lists all chapters, makes no chapter bold, and calls `\DefenseTocFrame{0}`.
3. The pages of chapter 1.
4. Chapter k (k = 2..n): first a chapter TOC page (`toc`) that makes chapter k bold and calls `\DefenseTocFrame{k}`, then the pages of chapter k.
5. Thanks page (`thanks`).

In the defense stage, an achievements page (`achievements`) follows the outlook page of the conclusion chapter.

Backup pages (`backup`) come after the thanks page. The page order check, the content page count, and the time budget do not count backup pages.

The overall TOC of the reference framework makes chapter 1 bold. The overall TOC of this skill makes no chapter bold, and this skill adds no chapter TOC page before chapter 1.

## Chapter Roles

| Role          | Meaning                                                                                                                                                            | Recognition hint                                                                                                                   |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `intro`       | Introduction chapter                                                                                                                                               | Chapter 1, or the chapter title contains “绪论” or “引言”                                                                          |
| `conclusion`  | Conclusion chapter                                                                                                                                                 | The chapter title contains “结论” or “总结与展望”                                                                                  |
| `application` | System or platform design and application chapter                                                                                                                  | The chapter title contains “系统” or “平台”, and also one of “设计”, “应用”, or “实现”                                             |
| `foundation`  | Theoretical foundation and problem framework chapter: gives the mechanism, the problem formulation, and the overall framework, with no separate method experiments | Not chapter 1 or the last chapter, and no section title at any level in the chapter contains “实验”, “案例”, “结果分析”, or “仿真” |
| `research`    | Research chapter: proposes a method and validates the method with experiments                                                                                      | All other chapters                                                                                                                 |

The recognition hints apply in the row order of the table. The first row that matches takes effect. The extraction script writes the result as a role suggestion. The chapter role in the plan file is the final value, and the user can change the role.

## Page Sequence of Each Chapter Role

| Chapter role  | Page role sequence                                                | Default page count at 40 minutes                             |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------------------------ |
| `intro`       | `background` → `status` → `challenges` → `organization`           | 2, 2, 1, 1                                                   |
| `foundation`  | `foundation` × n                                                  | 3                                                            |
| `research`    | `intro` → `problem` → `method` × m → `experiment` × e → `summary` | 1, 1, m, e, 1; with three research chapters, m = 3 and e = 4 |
| `application` | `intro` → `architecture` → `application` × n                      | 1, 1, 2                                                      |
| `conclusion`  | `innovation` → `outlook`; the defense stage adds `achievements`   | 1, 1; the defense stage adds 1                               |

For other durations and chapter structures, calculate the page counts with the formula in [Time Budget](time-budget.md).

## Page Role Content

| Page role                     | Content                                                                                                                                                                                                         | Default layout                         |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `background`                  | Research background and significance: bullets or a figure, plus one takeaway sentence                                                                                                                           | `bullets` or `figure-bullets`          |
| `status`                      | Research status: a literature statistics figure or a review figure, plus a summary paragraph; the last page leads to the research chapters of the thesis                                                        | `figure` or `bullets`                  |
| `challenges`                  | Open problems and challenges: one problem card for each research chapter, in chapter order, with emphasized keywords                                                                                            | `cards`                                |
| `organization`                | Research content and chapter arrangement: the thesis organization figure, plus a description of the three layers theory, method, and application                                                                | `figure`                               |
| `foundation`                  | Foundation chapter: mechanism figure, problem formulation, and overall framework                                                                                                                                | `equations-figure` or `figure-bullets` |
| `intro` (research chapter)    | Introduction: the subsection bar “研究内容 i：章题” (research content i: chapter title), the technical route figure, and one paragraph of the form “本章首先…其次…最后…” (this chapter first…, then…, finally…) | `figure-bullets`                       |
| `problem`                     | Problem description: a data figure or a problem diagram, plus the problem statement                                                                                                                             | `figure-bullets` or `bullets`          |
| `method`                      | Method: equations and a diagram in two columns, or a flowchart and bullets; equation numbers follow the thesis                                                                                                  | `equations-figure` or `figure-bullets` |
| `experiment`                  | Experiment: comparison subfigures (2×2 or 2×3) or a metrics table; subfigure captions and figure numbers follow the thesis                                                                                      | `figure-grid`, `figure`, or `table`    |
| `summary`                     | Chapter summary: conclusion bullets, plus the “论文” (paper) box for the paper that matches this chapter                                                                                                        | `paper-summary`                        |
| `intro` (application chapter) | Application background and goals                                                                                                                                                                                | `figure-bullets`                       |
| `architecture`                | System architecture figure                                                                                                                                                                                      | `figure`                               |
| `application`                 | Platform interface or application results                                                                                                                                                                       | `figure` or `table`                    |
| `innovation`                  | Main innovations: innovation cards; the card count equals the research chapter count                                                                                                                            | `cards`                                |
| `outlook`                     | Future research outlook: items such as “其一” (first) and “其二” (second)                                                                                                                                       | `outlook`                              |
| `achievements`                | Results obtained during the degree study (defense stage)                                                                                                                                                        | `bullets`                              |
| `backup`                      | Backup page for answers to expected questions                                                                                                                                                                   | Any content layout                     |

## Mapping of Problems, Research Content, and Innovations

- The problem card count on the `challenges` page, the research chapter count, and the innovation card count on the `innovation` page are equal.
- Number the research chapters i = 1..R in chapter order. Problem card i, the subsection bar “研究内容 i：章题” on the `intro` page of research chapter i, and innovation card i refer to the same chapter.
- The text of an innovation card comes from the matching contribution item in the conclusion chapter of the thesis. The card gives the chapter number.

## “论文” (Paper) Box

- Entry source: an item in the thesis publication list that has a mark for the matching chapter, for example “对应论文第三章” (matches chapter 3 of the thesis).
- Position: the `summary` page of the matching chapter. The citation text is a word-for-word copy from the publication list.
- When one chapter matches more than one publication, the `summary` page shows one entry, by default the first entry. The speaker notes can mention the other entries.
- A chapter with no matching entry gets no “论文” box. Do not invent publications.

## Stage Differences

| Item                             | `predefense`             | `defense`                                     |
| -------------------------------- | ------------------------ | --------------------------------------------- |
| Stage text on the cover          | 博士学位论文预答辩       | 博士学位论文答辩                              |
| Main sentence on the thanks page | 敬请各位老师批评和指正！ | 敬请各位老师批评和指正！                      |
| Achievements page                | None                     | An `achievements` page after the outlook page |

A formal defense often needs a description of the revisions made for the predefense comments and the blind review comments. This version does not generate a revision description page.
