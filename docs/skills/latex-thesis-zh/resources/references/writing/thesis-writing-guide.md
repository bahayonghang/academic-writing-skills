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

## Body-Chapter Introduction (One-Paragraph / Two-Paragraph, Connecting Preceding and Following)

For each chapter from Chapter 2 to the conclusion, it is recommended to write a **Chapter Introduction** after the chapter title before entering subsections, echoing the "Chapter Summary" at the end of the chapter. In terms of positional form, both **numbered introduction sections** (`\chapter` followed directly by `\section{引言}`) and **post-chapter lead-ins** (unnumbered body prose after the chapter title) are compliant (see Section 3 of [method-chapter-guide-zh.md](method-chapter-guide-zh.md)). In terms of natural paragraphs, **both one-paragraph and two-paragraph forms are compliant**. In a paper-to-chapter workflow, **always writing a backward-connecting sentence is safer** (when inter-chapter dependencies exist) and more conducive to positioning the mainline during blind review; therefore, the backward sentence is the recommended move rather than fixing the number of paragraphs. However, this is **recommended rather than rigid**; see "Flexible rules" below for boundaries (method-chapter details appear in Section 3 of [method-chapter-guide-zh.md](method-chapter-guide-zh.md), and the templates below serve as the reference source).

**Length**: Generally 1~2 natural paragraphs, about 300~500 words (literature-intensive method chapters can be longer, undertaking a mini-review and including `\cite`). It is not an abstract, and should not repeat content already covered in the Chapter 1 literature review.

### Common Moves (Fixed Moves, Flexible Paragraphs)

Regardless of whether a one-paragraph or two-paragraph form is adopted, a qualified body-chapter introduction should cover the following four core semantic moves (fixed moves, flexible paragraphs):

| Move | Role | Typical phrasing | Necessity |
| --- | --- | --- | --- |
| ① Problem | Anchor process phenomena or data traits of this chapter's object, deriving technical problems and consequences | "＜Object＞ is obtained by ＜process＞ at ＜cycle＞... ＜Phenomenon＞ causes ＜problem＞, affecting ＜consequence＞." | Required |
| ② Backward interface | State connection with previous chapters, citing prior achievements via a role-reuse sentence | "The predictive model constructed in Chapters 3 and 4 serves as the fitness function for this chapter..." | By dependency (omissible for parallel chapters) |
| ③ Solution announcement | Announce the method, model, or system proposed in this chapter | "To address this problem, this chapter proposes ＜Method＞ (Full Name, ABBR), used for..." | Required |
| ④ Closure or roadmap | State this chapter's research roadmap or value closure toward the whole thesis / follow-ups | "This chapter first... then... finally validates..." or "providing ... support for Chapter Y" | Required (choose either or both; do not write section directories) |

### Two-Paragraph Form

The two-paragraph form is suitable when backward handoff requires explaining conclusions and limitations of the previous chapter (≥ 2 sentences), or when the problem and solution contain multiple hierarchical layers. The first paragraph may also be written as "phenomenon → problem" rather than purely backward-looking, and the backward-connecting sentence can be placed at the end of paragraph 1 or the beginning of paragraph 2 (covered by flexible rules).

**Two roles**:

1. **Backward handoff (Paragraph 1)**: State the value of the previous chapter to this chapter—what the previous chapter solved, what conclusions were reached, leading to why this chapter must continue. Refer to **chapter numbers** ("Chapter 2"), avoiding relative expressions like "previous chapter / above / earlier" (to facilitate reading and navigation).
2. **Forward setup (Paragraph 2)**: State what problem this chapter addresses, what the core idea is, and what advantages it holds over existing methods; at the end of the paragraph, according to disciplinary needs, use one or two sentences for a **method roadmap preview** ("First... then... finally, based on... experiments validate...") or section arrangements ("This chapter is organized as follows: ...", engineering disciplines often include a framework diagram). The signposting roadmap is not rigid and may follow discipline or supervisor conventions.

**Applicable template**:

```text
第 X 章……解决了……，并得出……，但在……方面仍存在……。
针对这一问题，本章提出……，其核心思想是……，相比……的优势在于……。
本章组织如下：N.1 节……，N.2 节……，N.3 节……。
```

### One-Paragraph Form

The one-paragraph form is common and concise in chapters addressing a single technical problem, where backward connection can be compressed into a single role-reuse sentence and the solution can be announced in a single sentence.

**Six-step progression order**:

| Step | Move | Sentences | Required | Key writing points |
| --- | --- | --- | --- | --- |
| ① Object anchor | Problem | 1~2 | Required | Process phenomena or data traits of this chapter's object with concrete quantities; do not restate Chapter 1 industry background |
| ② Problem derivation | Problem | 1~3 | Required | Derive the technical problem and its consequences from phenomena ("causing... affecting...") |
| ③ Necessity sentence | — | 0~1 | Optional | Retain only when grounded in this chapter's object ("To this end, it is urgent to..."); delete empty platitudes like "has great significance" (point to deai) |
| ④ Backward interface | Backward | 0~1 | By dependency | Role-reuse sentence + chapter numbers, listable ("Chapters 3 and 4 model as fitness function"); omissible for parallel chapters; avoid "previous chapter" |
| ⑤ Solution announcement | Solution | 1~2 | Required | "Targeting this problem, this chapter constructs/proposes ＜Method＞ (English Full Name, ABBR), used for..." |
| ⑥ Closure or roadmap | Closure/Roadmap | 1~3 | Required | Value closure ("provides ... support for ...") or method roadmap ("first... then... finally..."), choose either or both; do not write section directories |

**One-paragraph template (synthetic text)**:

```text
<对象>由<数据/工序>以<周期/规模>获得，而<关键量>……。<现象>导致<技术问题>，影响<后果>。
[第 X 章的<产出>在<条件>下<局限>。]
针对该问题，本章基于<思想>，构建<方法名>（English Full Name, ABBR），用于<作用>。
本章首先……，随后……，最后基于<数据>验证……；[为第 Y 章的<任务>提供<接口>。]
```

**Length and openings**:
- Length: Single natural paragraph, about 300~600 Chinese characters, 6~12 sentences (600 is an uncalibrated / UNVERIFIED advisory threshold).
- Three opening strategies (cited from W1):
  1. Direct opening: Start directly from this chapter's research object and process/data phenomena;
  2. Question-driven opening: Open with the core technical contradiction or question to be solved;
  3. Transitional opening: First sentence directly states the backward role-reuse interface.

**One-paragraph positive and negative examples (synthetic text)**:
- **Compliant positive example**:
  > Online sensor sequences in continuous flow reaction processes are usually collected at second-level frequencies, with high data dimensions and non-stationary drift. Sampling fluctuations make transient features difficult to extract accurately, affecting the response speed of product purity soft measurement. To this end, it is urgent to improve the adaptive representation ability of feature extraction under non-stationary conditions. This chapter takes the dynamic calibration model established in Chapters 2 and 3 as the basic feature extractor, targets multi-condition non-stationary drift, and proposes an Adaptive Attention Gating Network (AAGN). This chapter first presents the dynamic gating topology and loss constraints of AAGN, then designs a noise-resistant updating mechanism, and finally validates representation performance on empirical datasets, providing high-fidelity state inputs for closed-loop optimization in Chapter 5.
  > (Analysis: Object anchor → problem derivation → necessity → backward enumeration → solution announcement → roadmap and closure, complete moves, about 270 characters (a compressed sample; real writing expands to 300~600 characters), tight progression.)
- **Non-compliant negative example**:
  > With the rapid development of modern industrialization and the widespread adoption of intelligent manufacturing technologies, industrial big data soft measurement holds extremely significant strategic value, practical utility, and broad application prospects in modern process industries, serving as a prominent frontier research hotspot attracting joint attention from academia and industry. For the research object of this chapter, because actual production processes are severely affected and jointly constrained by numerous complex, volatile onsite environments and various uncertain stochastic interference factors, dynamic data sequences collected by onsite sensors inevitably exhibit severe characteristics of high nonlinearity, multi-modality, large delays, and non-stationarity, creating enormous difficulties and severe challenges for high-precision soft measurement and safe, stable operational control. Targeting these major challenges, this chapter proposes an innovative soft-measurement algorithmic framework. This chapter is organized as follows: Section 4.1 presents the introduction; Section 4.2 describes related work; Section 4.3 proposes the algorithm; Section 4.4 conducts experiments; Section 4.5 concludes the chapter. This chapter first designs the algorithm model, secondly conducts parameter optimization, and finally performs experimental verification.
  > (Flaw analysis: ① Restating macro background and boilerplate significance sentences, pointing to `deai` empty phrases; ② Single sentence exceeding 120 words, pointing to `check_style_zh.py` E-LONGSENT over-long sentences; ③ Stacking "major challenges / enormous difficulties" rhetoric, pointing to `academic-style-zh.md`; ④ Writing both section directory and method roadmap, violating deduplication principles, pointing to [`paragraph-roles-zh.md`](paragraph-roles-zh.md).)

### Paragraph Style Selection

| Condition | One-paragraph form | Two-paragraph form |
| --- | --- | --- |
| Backward handoff | Can be compressed into a single role-reuse sentence, or parallel chapters omit it | Requires explaining conclusions and limitations of previous chapter (≥ 2 sentences) |
| Problem hierarchy | Single technical problem | Two or more problem layers, or needs framework before problem |
| Solution | Can be announced in one sentence | Solution contains multiple modules requiring itemized introduction |
| Length | About 300~600 words, 6~12 sentences | About 400~900 words; literature-intensive chapters needing mini-review `\cite` can be ≥ 3 paragraphs |
| Thesis consistency | Chapters may mix styles (2/5 in corpus), no forced uniformity | Same as left |
| Common prohibitions | Do not write both section directory and method roadmap in same intro; do not restate Chapter 1 background or review | Same as left |

**Flexible caliber** (verified by 5 industrial doctoral theses, the checker reduces false positives accordingly, consistent with section 3 of method-chapter-guide-zh.md):

- **Parallel method chapters need not refer backward**: the required handoff strength is **proportional to the real dependency between chapters**. A purely parallel method chapter may establish its own problem without referring to the previous chapter; the checker gives only an Info recommendation, not a defect. Only when the chapter reuses an earlier result (for example, it mentions "Chapter X") but its introduction omits the dependency should the checker request a role-reuse sentence.
- **Role reuse sentence inheritance and compliance**: Succession relies on "role reuse sentences" rather than "narrative review paragraphs" - instead of repeating what was done in the previous chapter, directly state "use the prediction model of Chapter X as the fitness function of this chapter", that is, compliance.
- **Method route preview format is compliant**: The method route preview written as "First...Second...Finally" is sufficient. There is no need to write the section number directory of "Section N.2 will introduce...", both states are compliant.
- **Do not repeat industry background or duplicate directory**: The chapter introduction must not restate the broad industry background or literature review already established in the introduction; choose either a section directory or a roadmap preview, never both in the same introduction; the section directory must not elaborate on the specific details of every section. For role matrix and deduplication rules across all paragraph levels, see [`paragraph-roles-zh.md`](paragraph-roles-zh.md).

**Positive and negative examples**:

| Writing | Judgment |
|------|------|
| "Chapter 2 established a baseline model, but its overhead is too high on long sequences. To address this bottleneck, this chapter proposes a sparse attention mechanism... This chapter is organized as follows: Section 3.1..." | Passed (two-paragraph: with chapter numbers, questions + ideas + road signs) |
| In a single paragraph, complete object anchor, problem derivation, Chapter 2 and 3 model reuse, new method proposal, and roadmap preview (about 400 words) | Passed (one-paragraph: complete six-step moves, lists chapter numbers for backward link, no dual directory and roadmap) |
| Purely parallel method chapter: The introduction only establishes the problems of this chapter and predicts the method route of this chapter, without referring back to the previous chapter | Passed (the parallel chapter does not need to be inherited, only Info is recommended to be explicitly inherited) |
| In a single intro paragraph, listing both "Section N.1... Section N.2..." and immediately "First... then... finally" | Flaw (duplicate directory and roadmap, violates deduplication principle, choose either one) |
| Section N.3 says "uses the feature set from Chapter X", but the introduction never mentions Chapter X | Missing backward link (there is an explicit dependency but no handoff; add a sentence explaining the reused role) |
| Directly after the chapter title: `\section` or formula | Missing chapter introduction (missing both a continuation and a continuation) |
| "The baseline method was discussed in the previous chapter." A single sentence is transferred to a subsection | Relative reference + oversimplification (should add the problem, solution, and closure/roadmap moves and use chapter numbers instead) |
| Write the entire chapter method details into the chapter introduction | Too long (details should be dropped to the corresponding subsections) |

> Boundary: The introduction (Chapter 1) is written in the funnel style of the "Introduction" section, and the two-paragraph format of this section is not applied; this section is only for the main chapters.

### Sources

- W1: Wanwei Shukan, *Degree Thesis Writing Guide and Template—Introduction and Transition Paragraphs*, https://www.eshukan.com/academic/show.aspx?id=170089 ("Introductions to other chapters are usually also a single natural paragraph, introducing the theme of this chapter and briefly explaining its content, serving a guide reading function"; three opening strategies: direct/question/transition)
- W2: Shanghai International Studies University, *Graduate Degree Thesis Formatting Specification Guidelines*, https://graduate.shisu.edu.cn/_upload/article/34/80/bd4949214d11ab764fb3259a644c/26c942f8-0ab8-44aa-97cf-f4e41291ea81.pdf (Backward link and overview as two moves; numbered intro section and lead-in forms both compliant)
- W3: Pat Thomson, *connecting chapters/chapter introductions*, https://patthomson.net/2014/01/16/connecting-chapterschapter-introductions/ (LINK / FOCUS / OVERVIEW three steps; fixed moves, flexible paragraphs)
- W4: Thesis Hub, *Structuring Thesis Chapters: The Introductory/Concluding Paragraphs*, https://thesishub.org/structuring-thesis-chapters-the-introductory-concluding-paragraphs/ (Single introduction paragraph accomplishes backward link, introduces chapter object, previews chapter, and links to thesis argument)
- W7: Leshem & Bitzer (2021), *'Signposting' research stories in doctoral theses*, https://doi.org/10.5785/37-1-965 (Excessive signposting makes text repetitious; one-paragraph form avoids duplicate directory and roadmap, avoids repeating background)
## Summary at the end of the main article (single paragraph closing style)

For each chapter from Chapter 2 to the conclusion, the "Chapter Summary" at the end of the chapter should echo the beginning and end of the chapter introduction: the chapter introduction is responsible for explaining "why this chapter was written", and the chapter summary is responsible for explaining "what this chapter solved, how to prove it, and what support it has for the whole article." It is not an abbreviation for the final "summary and outlook", nor is it a restatement of the section titles.

**Length**: The default is **1 natural paragraph**. Follow a university template, supervisor, or explicit
user request that requires multiple paragraphs or a list; do not turn one paragraph, a fixed length, or a
fixed number of values into universal rules. Use sequence words only for a process with a real temporal or
execution order. Do not force parallel modules, method interfaces, or independent evaluation tasks into a
“first-second-finally” sequence.

**Argument boundary**: The summary must not introduce new citations, formulas, figures/tables, or derivations (extending the existing rule of "do not add citations not in the original text", see [`paragraph-roles-zh.md`](paragraph-roles-zh.md)); summarizing method highlights at sentence-level granularity is compliant, whereas step-by-step recitation of training or deployment pipelines is non-compliant; back-referencing existing figures or tables in the chapter body (`\ref`) is compliant.

**Single segment character sequence**:

1. **Problem/Objective**: At the beginning, point out the core issues, evaluation objects or technical bottlenecks around this chapter.
2. **Work/Method**: Summarize what is proposed, constructed, designed or analyzed in this chapter, without going into details of formula derivation.
3. **Process/Evidence**: Condensed description of key steps, experimental objects, cases, indicators or verification paths.
4. **Results/Value**: Only write conclusions that can be supported by the evidence in the original text; when there is lack of data, it is marked as insufficient evidence, and the results will not be reconstructed.
5. **Main Line Support**: Concluding with this chapter’s supporting role in subsequent chapters, overall contribution, or full-text scientific issues.

**Apply the five roles by chapter type**:

| Chapter type | Work/method focus | Process/evidence focus | Legitimate boundary |
| --- | --- | --- | --- |
| Framework/process chapter | Relate the object, constraints, problem derivation, and overall framework | Process analysis, framework coverage, or mapping to later chapters; quantitative metrics are optional | Do not invent RMSE, significance, or application effects merely to fill a “result” slot |
| Method chapter | Use modules or functions as subjects and state inputs, outputs, and interfaces; serial or parallel relations follow source facts | Cover every independent evaluation objective; do not omit a secondary task in a joint-task chapter | Do not replace real interfaces with sequence words or infer one component's contribution from the complete setting |
| System/engineering chapter | Organize around operating constraints, system mechanisms, or operator tasks instead of repeating components and screens | Distinguish offline, observational, pilot, or operational evidence while retaining environment and scope limits | Use process words only for a real deployment sequence; do not upgrade observations to closed-loop benefits |

List every independent task in the chapter and its evidence status before compressing the summary. A task
with only a method description may be summarized as “constructed/designed...,” but cannot become
“evaluation shows....” Mark missing evidence as `missing evidence`; do not omit that task or borrow another
task's conclusion merely because another task has results.

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
| A framework chapter contains only process analysis and mapping to later chapters, with no metrics | It may legitimately close on framework coverage and mainline support; do not require invented values |
| A method chapter has independent prediction and diagnosis tasks, but the summary reports only prediction | Incomplete task coverage (add the diagnosis work and its actual evidence status) |
| A system chapter follows a real “connect-observe-fallback” order, but the material proves only short-term observation | Preserve the sequence; stop the claim at short-term observation and do not assert production closed-loop benefits |

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
