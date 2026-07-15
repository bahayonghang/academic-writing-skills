# Main line guide for writing Chinese degree thesis chapters

This guide is used to optimize chapter-level writing in existing Chinese LaTeX dissertations. It is not a direct translation of English conference paper section-writing; it is subject to the chapter structure, template specification, title post-title lead, GB/T 7714 citation and defense interpretability requirements of thesis.

## Use boundaries

- Used for: introduction, literature review, methods chapter, experimental chapter, summary and outlook, abstract/innovation/conclusion alignment.
- Not used for: writing dissertations from scratch, fabricating documents, fabricating experiments, and bypassing school template requirements.
- `\cite{}`, `\ref{}`, `\label{}`, math environment, reference keys, and template macro commands are retained by default.

## Overall main line

A dissertation should form a defensible main line:

```text
研究背景 -> 技术瓶颈/研究空白 -> 科学问题 -> 本文方法/章节工作 -> 实验证据 -> 贡献闭合 -> 局限与展望
```

When revising chapters, write out this main line first, and then judge whether each chapter is advancing it, rather than stacking multiple tasks side by side.

## Introduction

Recommended structure:

1. Research background: Explain the domain context and application value of the problem.
2. Technical bottlenecks/research gaps: Unsolved problems derived from existing methods or practical limitations.
3. Scientific questions: Gather the blanks into the core questions to be answered in this article.
4. What this paper does: Describe how the method or system responds to the problem.
5. Main contribution: Each contribution should be mapped to subsequent methods or experiments.
6. Chapter arrangement: Explain how each chapter progresses, rather than mechanically listing titles.

Checkpoint:

-Whether I jump directly from the background to the work of this article due to lack of previous work or technical reasons.
-Whether "research significance" is written as a slogan without corresponding technical bottlenecks.
- Whether each contribution is supported by experimental, analytical or chapter evidence.

> Detailed rules for the introduction chapter (citation quota, year distribution, visualization of research status, three elements of scientific issues, four-way closure)
> See [introduction-guide-zh.md](introduction-guide-zh.md); the corresponding script check is
> `analyze_literature.py --intro-citations` and `analyze_logic.py --intro-mainline`.

## Introduction to the main article (two paragraphs connecting the previous and the following, recommended form)

For each chapter from Chapter 2 to the conclusion, it is **recommended** to write a **Chapter Introduction** after the chapter title and then enter the subsections, echoing the "Chapter Summary" at the end of the chapter. It is different from the three-layer funnel introduction of Chapter 1. It is shorter and more focused on "connecting the previous and the following". The paper-to-chapter workflow is always more stable and more conducive to blind review and positioning of the main line, so this section is listed as an active recommendation form; however, it is recommended rather than rigid. See the "flexible caliber" below for the elastic boundary (see the third section of [method-chapter-guide-zh.md](method-chapter-guide-zh.md) for details on the method chapter, and the two paragraph templates in this section are the sources of citations).

**Length**: Generally 1~2 natural paragraphs, about 300~500 words (the methods chapter can be extended, bear a small review and include `\cite`). It is not an abstract, and it should not repeat what was already covered in the introduction to the literature review.

**Two roles**:

1. **Continuation (paragraph 1)**: Point out the value of the previous chapter to this chapter - what was solved in the previous chapter and what conclusions were drawn, which leads to why this chapter should continue. Use **chapter number** ("Chapter 2") to refer to it, and avoid relative expressions such as "previous chapter/above/previous chapter" (to facilitate skipping and positioning).
2. **Forward setup (paragraph 2)**: State the problem addressed in this chapter, its core idea, and its advantage over existing methods. Depending on disciplinary needs, end with one or two sentences that **preview the method sequence** ("First... next... finally... experiments based on ... validate ...") or list the section arrangement ("This chapter is organized as follows: ..."; engineering chapters often include a chapter framework diagram). This roadmap is optional and should follow disciplinary and supervisor conventions.

**Applicable templates**:

```text
第 X 章……解决了……，并得出……，但在……方面仍存在……。
针对这一问题，本章提出……，其核心思想是……，相比……的优势在于……。
本章组织如下：N.1 节……，N.2 节……，N.3 节……。
```

**Flexible caliber** (verified by 5 industrial doctoral theses, the checker reduces false positives accordingly, consistent with section 3 of method-chapter-guide-zh.md):

- **Parallel method chapters need not refer backward**: the required handoff strength is **proportional to the real dependency between chapters**. A purely parallel method chapter may establish its own problem without referring to the previous chapter; the checker gives only an Info recommendation, not a defect. Only when the chapter reuses an earlier result (for example, it mentions "Chapter X") but its introduction omits the dependency should the checker request a role-reuse sentence.
- **Role reuse sentence inheritance and compliance**: Succession relies on "role reuse sentences" rather than "narrative review paragraphs" - instead of repeating what was done in the previous chapter, directly state "use the prediction model of Chapter X as the fitness function of this chapter", that is, compliance.
- **Method route preview format is compliant**: The method route preview written as "First...Second...Finally" is sufficient. There is no need to write the section number directory of "Section N.2 will introduce...", both states are compliant.

**Positive and negative examples**:

| Writing | Judgment |
|------|------|
| "Chapter 2 established a baseline model, but its overhead is too high on long sequences. To address this bottleneck, this chapter proposes a sparse attention mechanism... This chapter is organized as follows: Section 3.1..." | Passed (with chapter numbers, questions + ideas + road signs) |
| Purely parallel method chapter: The introduction only establishes the problems of this chapter and predicts the method route of this chapter, without referring back to the previous chapter | Passed (the parallel chapter does not need to be inherited, only Info is recommended to be explicitly inherited) |
| Section N.3 says "uses the feature set from Chapter X", but the introduction never mentions Chapter X | Missing backward link (there is an explicit dependency but no handoff; add a sentence explaining the reused role) |
| Directly after the chapter title: `\section` or formula | Missing chapter introduction (missing both a continuation and a continuation) |
| "The baseline method was discussed in the previous chapter." A single sentence is transferred to a subsection | Relative reference + oversimplification (should be expanded into two paragraphs, use chapter numbers instead) |
| Write the entire chapter method details into the chapter introduction | Too long (details should be dropped to the corresponding subsections) |

> Boundary: The introduction (Chapter 1) is written in the funnel style of the "Introduction" section, and the two-paragraph format of this section is not applied; this section is only for the main chapters.

## Summary at the end of the main article (single paragraph closing style)

For each chapter from Chapter 2 to the conclusion, the "Chapter Summary" at the end of the chapter should echo the beginning and end of the chapter introduction: the chapter introduction is responsible for explaining "why this chapter was written", and the chapter summary is responsible for explaining "what this chapter solved, how to prove it, and what support it has for the whole article." It is not an abbreviation for the final "summary and outlook", nor is it a restatement of the section titles.

**Length**: The default is written as **1 natural paragraph**. Unless the school template, the instructor requires it, or the user explicitly requires the points to be listed, it will not be broken into multiple short paragraphs or lists. In an engineering degree thesis, "first, second, then, and last" can be used to connect stages of work, but these connectives should serve the same continuous paragraph.

**Single segment character sequence**:

1. **Problem/Objective**: At the beginning, point out the core issues, evaluation objects or technical bottlenecks around this chapter.
2. **Work/Method**: Summarize what is proposed, constructed, designed or analyzed in this chapter, without going into details of formula derivation.
3. **Process/Evidence**: Condensed description of key steps, experimental objects, cases, indicators or verification paths.
4. **Results/Value**: Only write conclusions that can be supported by the evidence in the original text; when there is lack of data, it is marked as insufficient evidence, and the results will not be reconstructed.
5. **Main Line Support**: Concluding with this chapter’s supporting role in subsequent chapters, overall contribution, or full-text scientific issues.

**Applicable templates**:

```text
本章围绕……问题，针对……不足，提出/构建了……。首先，……；其次，……；然后，……；最后，……。以……为实验/案例对象的验证表明，……，从而为后续……/全文……提供了支撑。
```

**Positive and negative examples**:

| Writing | Judgment |
|------|------|
| "This chapter focuses on the abnormal characterization and insufficient dynamic response in the evaluation of non-stationary industrial process operating conditions, and proposes... first... secondly... then... finally... verification shows... to provide support for subsequent optimization and control." | Passed (single paragraph, problem-method-evidence-value closure) |
| Write three paragraphs in a row: "This chapter will introduce... first. This chapter will introduce... next. This chapter will introduce... at the end." | Overly scattered (should be compressed into a natural paragraph to avoid catalog-style retelling) |
| List with items "1. Completed... 2. Completed... 3. Completed..." | Non-default form (change to continuous paragraphs unless required by template/instructor) |
| "The method proposed in this chapter reaches the international leading level and fills the domestic gap." However, there is no corresponding evidence in the text | The evidence is out of bounds (should be deleted or changed to a verifiable statement) |

> Boundary: The final "Conclusion/Summary and Outlook" should integrate the contributions, limitations and future directions of the full text; the summary of this chapter only summarizes the evidence in the chapter, and does not mechanically repeat the "Chapter X..." sentence structure of each chapter.

## Literature Review

Recommended chain:

```text
共识 -> 分歧 -> 局限 -> 空白 -> 本文切入点
```

Each topic group should first explain what the literature in this group solves, then compare the method assumptions, mechanisms, scope of applicability or failure modes, and finally point out the limitations related to the problem of this article. Do not name items by author and year.

Boundary:

- Do not add citations that do not appear in the original text.
- Do not write "few relevant studies" as "no one has studied yet" unless there is already evidence.
- If a research gap lacks citation support, mark it as "insufficient evidence" and do not force a firm conclusion.

## Method Chapter

> If Chapter 2 is a **Process Analysis Chapter** with an industrial/process background (process flow analysis + full-text method framework, rather than directly writing methods),
> Read [process-chapter-guide-zh.md](process-chapter-guide-zh.md) first, and the corresponding script check is
> `analyze_logic.py --process-chapter`; Only when it is judged to be of the "Chapter 2 Method + Experiment" genre, the following Method Chapter Three Questions will be applied.
>
> For details about the text methods + experimental chapters ("one chapter, one method + experiments in the same chapter") starting from Chapter 3
> [method-chapter-guide-zh.md](method-chapter-guide-zh.md)——Five-segment skeleton, chapter introduction and grading,
> Experimental industrial version specifications, splicing sense/draft state list; the corresponding script is `analyze_experiment.py --per-chapter`
> Splice representation scan with P-PAPER running by default.

Each core chapter or module should answer three things:

1. **Motivation**: Why this chapter/module must exist, which bottleneck it responds to.
2. **Design**: What are the input, processing flow, key structures, and output.
3. **Advantages**: What are the technical benefits compared to comparable solutions, and how to verify them later.

Explicit progression between chapters is required:

```text
基于上一章提出的 ...，本章进一步解决 ...
```

If multiple tasks are just placed side by side, "common scientific issues" and "progressive relationships" need to be supplemented.

## Experiment and discussion

The lab chapter should not look like a project report. Recommended level:

1. Experimental settings: data, indicators, baseline, protocol fairness.
2. Validity: The main results are compared with strong baselines.
3. Ablation/Sensitivity: Validate key modules, parameters or design choices.
4. Mechanistic explanation: explain the reason for the result instead of reciting the table.
5. Literature review: Compare with representative work in the literature review.
6. Limitations and Enlightenments: Explain the scope of application and subsequent improvements.

It is prohibited to draw conclusions from unreported data. If baseline, ablation, or significance information is missing, gaps should be clearly marked.

## Abstract, innovation points and summary

The abstract, innovation points and conclusion should be like a "tripartite closure":

| Position | Should Answer |
| --- | --- |
| Abstract | Research questions, methods, results, significance |
| Innovation points/main contributions | This article is an incremental improvement over existing work |
| Summary and Outlook | Proven contributions, limitations, future directions |

Check whether each innovative point is echoed in the conclusion and whether it is supported by experimental or chapter evidence.

> Abstract skeleton details (object positioning first sentence, pain point paragraph, general sentence ending with colon, numbered work paragraphs, consistency between Chinese and English, word count rules)
> See the "Thesis Abstract Skeleton (thesis Model)" section of [abstract-structure.md](abstract-structure.md),
> Corresponding script `analyze_abstract.py` (default thesis mode, `--bilingual` checks Chinese and English consistency).
> For the details of the conclusion chapter (flat three-section format, contribution bar skeleton, outlook blacklist, conclusion ≠ abstract, numerical consistency), see
> [conclusion-guide-zh.md](conclusion-guide-zh.md), corresponding to script `analyze_conclusion.py`.

## Output suggested format

```latex
% THESIS-WRITING（第 N 行）[Severity: Major] [Priority: P1]: 章节主线断裂
% 问题：绪论提出了“提高鲁棒性”，但实验章节没有对应验证。
% 建议：补充鲁棒性实验，或将绪论贡献改为当前结果能支持的范围。
% 证据状态：needs evidence
```

---

## Further reading

- [writing-philosophy-zh.md](writing-philosophy-zh.md): Philosophy of dissertation writing - narrative principles, five-sentence formula for abstracts, seven principles of reader expectations and micro-writing skills, suitable for reading through before rewriting the introduction/abstract.
