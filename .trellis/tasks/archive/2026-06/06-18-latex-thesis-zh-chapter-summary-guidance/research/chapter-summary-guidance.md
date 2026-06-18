# Chapter Summary Guidance Research

## Question

How should `latex-thesis-zh` constrain "本章小结" outputs so they match Chinese
degree-thesis expectations and the user-provided Yanshan University example?

## User Sample

The screenshot shows a Yanshan University engineering doctoral thesis section
`4.5 本章小结`. Its body is a single long paragraph. The paragraph does not split
into bullet points or multiple micro-paragraphs; it moves through:

1. the chapter's evaluation problem and missing capabilities in existing methods;
2. the proposed method and named technical route;
3. the staged work inside the chapter;
4. the experimental object and scenarios;
5. the verified value of the method for dynamic non-stationary process
   operation-condition evaluation.

Inference: for this skill, the desired default is a compact, thesis-style
evidence summary, not a long essay and not a final-conclusion chapter.

## External Sources

- University of Electronic Science and Technology of China, `研究生学位论文撰写规范`
  (2022): states that each chapter should end with a "本章小结"; it should
  concisely and accurately summarize the chapter's research content, methods,
  and achievements, and it forms the basis for the final thesis conclusion.
  It also distinguishes the final conclusion from a repetition of chapter
  summaries.
  Source: https://gr.uestc.edu.cn/attached/papers/101/202203/%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6%E7%A0%94%E7%A9%B6%E7%94%9F%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E6%92%B0%E5%86%99%E8%A7%84%E8%8C%83_20220321.pdf

- Beijing University of Technology, `研究生学位论文撰写规范` (2023): states
  that thesis body chapters should have a "本章小结" section; the final
  conclusion is written separately as the last body chapter and summarizes the
  whole thesis' major achievements, innovation, value, and future work.
  Source: https://graduate.bjut.edu.cn/beijinggongyedaxueyanjiushengxueweilunwenzhuanxieguifan.pdf

- Beijing Institute of Technology, `博士、硕士学位论文撰写规范` (2017): says
  research-content chapters may have a "本章小结" section where needed. Its body
  chapter description lists research object, methods, experiments/observations,
  theory, data, analysis, viewpoints, and conclusions as the substance that
  chapter summaries can synthesize.
  Source: https://grd.bit.edu.cn/docs/2017-12/20171212070921798998.pdf

- China University of Petroleum (East China), master's thesis template/example:
  recommends adding "本章小结" from chapter 2 onward, with the purpose of
  summarizing the chapter's research content; it can be written from the
  chapter's work and main conclusions and prepares the transition to the next
  chapter.
  Source: https://io.upc.edu.cn/_upload/article/files/20/10/4098cf0a43369c9d927ca468610d/39fde058-4f5c-4a1b-b417-46b3442a288d.pdf

- OUC AI Lab, `硕士学位论文写作指导` (2025): practical guidance says "本章小结"
  summarizes the chapter's work in one paragraph. This is not an official
  university rule, but it aligns with the screenshot's one-paragraph style.
  Source: https://oucai.club/research/thesis_writing.html

## Local Evidence

- `academic-writing-skills/latex-thesis-zh/references/writing/thesis-writing-guide.md`
  has chapter-introduction guidance but no chapter-summary guidance.
- `academic-writing-skills/latex-thesis-zh/references/writing/structure-guide.md`
  recommends a body-chapter structure ending with "本章小结".
- `academic-writing-skills/latex-thesis-zh/SKILL.md` routes "章引言" requests
  but not "本章小结" requests.
- `academic-writing-skills/latex-thesis-zh/evals/evals.json` has no eval focused
  on chapter-summary output shape.

## Design Implications

- Add a subsection to `thesis-writing-guide.md` immediately after the chapter
  introduction section so the two form a pair: chapter opening and chapter
  closing.
- Default summary shape: one natural paragraph, about half a page in thesis
  prose terms. Avoid bullet lists unless the existing source or user requests
  enumerated conclusions.
- Rhetorical order:
  `问题/目标 -> 本章工作/方法 -> 关键过程/机制 -> 结果/证据 -> 对全篇主线的作用`.
- Use chapter-local wording such as "本章围绕...", "针对...", "首先...其次...
  然后...最后..." only when it remains one paragraph.
- Prohibit unsupported novelty and fabricated evidence; mark missing evidence
  instead of inventing data.
- Keep final-conclusion guidance separate: chapter summaries support the final
  conclusion but do not replace it.
