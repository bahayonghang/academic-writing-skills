# Speaker Notes Format

This file specifies the five-field format of the defense speaker notes and the output format of `notes.md`. The seconds for each page come from the plan file. For the calculation method, see [Time Budget](time-budget.md). For the question categories, see [Defense Question Preparation](qa-prep.md).

## Five Fields

| Field | Content | Length |
| --- | --- | --- |
| 说什么 (what to say) | The spoken script of the page: first the conclusion, then the evidence; cite figure, table, and equation numbers | 150–250 Chinese characters for a content page |
| 要点 (key point) | The most important sentence of the page, the same as the takeaway sentence or shorter | One sentence |
| 时长 (duration) | The seconds for the page, from `notes.seconds` in the plan file | Integer seconds |
| 过渡 (transition) | One sentence that leads to the next page | One sentence |
| 可能提问 (possible questions) | Questions that the committee can ask about the page | 1–2 items |

The range of 150–250 characters is an initial range and is not calibrated. The “说什么” field of the cover, the TOC pages, and the thanks page has no such limit.

## Writing Rules

- Use the first person in spoken style, for example “本文” (this thesis) and “我们” (we). Do not read the page text word for word.
- For a figure, first say the figure number, then the order in which to read the figure, for example “如图3-2所示，左侧为……右侧为……” (as Figure 3-2 shows, the left side is …, the right side is …).
- Mention only numbers that are in the thesis. Give each number with its unit and its comparison baseline.
- On the last page of a chapter, the transition leads to the next chapter, for example “为解决问题二，下面汇报第 4 章” (to solve problem 2, I now present chapter 4).
- The notes of the overall TOC page describe the presentation structure, for example “我将按照论文的 7 章内容进行汇报” (I will present the 7 chapters of the thesis in order).
- The notes of the thanks page are “汇报完毕，请各位老师批评指正” (this ends my presentation; please give your comments).

## notes.md Format

The build script writes one section for each frame, in frame order. The section heading has the form “## \<index\> \<frame title\>（\<frame id\>，\<page role\>，\<seconds\> 秒）”, with full-width Chinese parentheses and commas. The five lines below the heading are the five fields in order. At the end of the file, the build script writes the total seconds of all pages and the target seconds (60 × minutes).

```markdown
## 8 3.1 引言（c3-intro，intro，51 秒）

- 说什么：本章针对问题一展开研究。如图3-1所示，技术路线分为三步……
- 要点：本章针对问题一提出示例方法一。
- 时长：51 秒
- 过渡：下面先说明本章研究的问题。
- 可能提问：为什么选择该技术路线？；与第 2 章的框架是什么关系？
```

- When “可能提问” has two items, a full-width semicolon “；” separates the items.
- A field that the plan file does not fill yet keeps the placeholder “〔待填写〕” (to be filled). The quality gate reports the remaining placeholders.
