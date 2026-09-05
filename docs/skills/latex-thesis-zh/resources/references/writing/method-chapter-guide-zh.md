# Main-Text Method + Experiment Chapter Guide

Writing and diagnosis of the **text methods chapter** for a Chinese doctoral thesis in an industrial/process background. This refers specifically to "one chapter, one method +
Experimental verification in the same chapter (hereinafter referred to as **Method Chapter**): From Chapter 3 to the conclusion, each chapter proposes a core method/model, and
Closed-loop verification in the experimental section within the chapter. Such chapters are mostly transcribed from published English essays through the paper-to-chapter workflow, and are reviewed blindly.
The first risk is "the feeling of splicing small papers/remaining in draft state". Diagnostic entry:

```bash
# 逐方法章实验完整性（E-DATA/E-ATTR/E-REF/E-FIG/E-METRIC/E-PARAM/E-ABL/E-ECHO）
uv run python $SKILL_DIR/scripts/analyze_experiment.py document.tex --per-chapter
# 拼接感 P-PAPER 默认扫全部正文章并报全部命中；单章文件承上/章序检查须声明真实章号
uv run python $SKILL_DIR/scripts/analyze_logic.py chapter3.tex --first-chapter 3
# 草稿态对冲 F-NOTE / 占位符表格行 F-PLACEHOLDER
uv run python $SKILL_DIR/scripts/check_format.py document.tex
```

> All thresholds for this article are 5 doctoral dissertations with industrial background (solid waste incineration, cement burning, cement clinker, cement grinding, zinc smelting and leaching)
> Read through the **discipline practices** caliber one by one (see each section for the source), **subject to the latest regulations of the instructor and the graduate school of our school**, command line
> can be covered. **Cross-chapter inspection (connection between previous chapters, main line between chapters, full-text coverage of P-PAPER) is recommended after assembly `document.tex`
> When running **, single file diagnosis must be equipped with `--first-chapter N` to declare the real chapter number.

## 1. Chapter judgment (judge first, then set rules)

For any body chapter, first classify it from the task performed by the body. The criteria and rules are different and
**cannot be mixed**. A chapter number helps locate content but cannot classify it by itself:

| Chapter type | Decisive criteria | Typical positions | Which set of rules to follow |
| --- | --- | --- | --- |
| Methods chapter (this guide) | One chapter, one method/model + closed loop of experimental section in the same chapter | Chapter 3 to the conclusion | This guide + `analyze_experiment.py --per-chapter` |
| Process Analysis Chapter | Process Flow Analysis + Full text method framework, does not contain independent methods | Usually Chapter 2 | [`process-chapter-guide-zh.md`](process-chapter-guide-zh.md) + `--process-chapter` |
| Engineering Application Chapter | Research artifact → operational constraint → system mechanism/operator task → graded validation | Independent chapter before the conclusion / integration chapter / final method-chapter experiment section | [`engineering-application-chapter-guide-zh.md`](engineering-application-chapter-guide-zh.md); do not run `--per-chapter` on an independent engineering chapter |

**Criterion description**: The process analysis chapter (Chapter 2) and the method chapter (from Chapter 3 onwards) usually coexist. The criteria are routing rules,
No full-text tags. The anchor point of the method chapter is "Chapter Title =〈Method Name/Abbreviation〉+〈Object〉+〈Task〉", and the abbreviation is in the chapter/section title,
Figure title appears repeatedly (5/5).

**Engineering application/system verification four-state distribution, the checker must not rigidly require a certain state** (5 actual tests): ①The independent engineering application chapter is placed
Before the conclusion (Zinc Chapter 6, 1/5); ② The last chapter is the integration/system verification chapter and end-to-end verification of the results of each assembly chapter (Chapter 8 of Solid Waste Incineration,
1/5); ③Industrial verification is absorbed into the experimental section of the final method chapter (grinding, firing, 2/5); ④Full offline backtesting, no on-site verification (clinker,
1/5). All four states are compliant.

Method validity and project implementation can be verified in layers: the simulation section of the method chapter only verifies the method itself (history/simulation controlled object), and is actually online
The data is centralized into application chapters. The control chapter "Use production data to fit NARX and then control it when the controlled object is controlled" is a common safety logic and is not a fraud.
(Red line 11).

For the argument chain, service and interface writing, and replay/shadow/pilot/production evidence boundaries of an
independent engineering-application or system-implementation chapter, read
[`engineering-application-chapter-guide-zh.md`](engineering-application-chapter-guide-zh.md). This guide keeps only
the four valid placement states so that the detailed engineering-chapter rules have one owner.

## 2. Recommended skeleton and elastic caliber

The 5 reference papers have the following formula: 5/5. Highly isomorphic. Recommended skeleton:

```text
X.1 引言（或章标题后导语）
X.2 基础理论 / 框架 / 结构设计〔可选，框架节与建模节常分家〕
X.3 方法建模（逐模块数学推导）
X.4 理论分析〔控制方向章的收敛性/稳定性，预测/优化章无此要求〕
X.5 实验（设计）与结果分析
X.6 本章小结
```

- **Directly subordinate to the second level section 4~6**. The first section "Introduction" (4/5 is the introduction numbered X.1; Zin is the unnumbered introduction after the chapter), the experimental section contains
  The words "Experiment/Simulation Verification/Case Study/Result Analysis" and the last section "Summary of this Chapter" (5/5 are consistent word for word).
- **Framework/Structural Design Section and Modeling/Methodology Section are often separated** (Grind/Burn/Clinker X.2 Framework + X.3 Modeling): Framework Section gives overall
  Structure diagram + module overview, modeling section and module-by-module mathematical derivation; it can also be combined into one section.
- **Control Direction Chapter Interpolates Independent Theoretical Analysis Section between Methods and Experiments** (Convergence/Stability) - Rigid Conventions of Control Discipline; Prediction/
  If there is no optimization chapter, this section will not be reported (red lines will not be subject to hard inspection).
- **"Textbook-style basic theory section" is allowed in the methods chapter** (general network theory of solid waste incineration, introduction to zinc AE/LSTM) - 2/5 exists,
  Not considered redundant (redline 5).
- **Single chapter 10~30 pages** (mainstream 15~21), significantly longer than the English short paper with the same name (sampling inspection by the Chinese Academy of Sciences: large papers must be more detailed than small papers).

## 3. Chapter introduction specifications (connecting the previous to the following) - the most critical part of this guide

**The user has made a decision**: The two-stage linkage between the previous and the following is the **active recommendation form**——paper-to-chapter workflow always writes the following
More stable and more conducive to positioning the main line for blind review (see the two-section template [`thesis-writing-guide.md`](thesis-writing-guide.md)
"Introduction to the main article"). But it is **recommended rather than hard**, and the elastic boundary has been verified by 5 sample essays:

- **Parallel method chapters may not be inherited**: Strength of succession **∝ Real dependence between chapters**. Chapter 5/5 with data/model dependencies (burned
  Chapter 5 names Chapters 3 and 4); purely parallel method chapters do not need to refer back to each other (each chapter on clinker and solid waste incineration stands on its own). → Inspector
  For ** pure parallel chapters, only Info will be reported, and Major** will not be reported; the introduction will only be made when the output of the previous chapter has been reused in the chapter ("Chapter X" appears)
  The original level will be maintained only if there is no acceptance.
- **Use a "role-reuse sentence" rather than a narrative recap**: Do not repeat what the previous chapter did. State directly that "the prediction model from Chapter X serves as this chapter's fitness function" (cement grinding). Refer to the **chapter number** and avoid relative phrases such as "the previous chapter" or "the discussion above".
- **The next chapter is a "method route preview" rather than a "section number list"** (3/5): sentence pattern "first... secondly... finally, based on... experiment"
  Verified the validity of..."; there is no need to write "Section 3.2 will introduce...".
- **1~3 paragraphs, about 300~500 words**; the literature-intensive chapter can be expanded to 3 pages, undertake a small review and include `\cite` (solid waste incineration
  Chapter 4 (30+ quotes) - **The quote containing `\cite` is not an error**.
- **Both forms are compliant**: Numbered introduction section (X.1 Introduction, 4/5) / Unnumbered introduction after chapter (Zinc, 1/5); in numbered introduction section form
  `\chapter` and then directly `\section{引言}` will not report "missing introduction".
- **It is forbidden to repeat the introduction and summary** (Tsinghua §4.5: Contents already mentioned in the introduction and summary will not be repeated in the chapter introduction).
- **"Defect-driven transition" recommended paradigm**: The most elegant transition between chapters is at the **end of the experiment in the previous chapter** - forced out by the defects exposed by the experiment
  Next chapter (pulverizing Chapter 5 "Single-step decision-making causes system instability" to force out Chapter 6 rolling optimization).

| Writing | Judgment |
| --- | --- |
| "The prediction model in Chapter 5 still needs to be manually tuned. This chapter embeds it as a fitness function into the optimization framework... first... and finally the experiment verified the effectiveness." | Passed (continuation of role reuse sentences + method route preview) |
| Pure parallel chapter: The introduction only establishes the problems of this chapter, does not refer back to the previous chapter, but predicts the method route of this chapter | Info recommendation (the parallel chapter does not need to follow the previous chapter, red line 1) |
| Section 4.3 of the chapter says "Inherit the feature set of Chapter 3", but the introduction does not mention Chapter 3 at all | Maintain the original level (there are dependent clues but missing inheritance, the role reuse sentence should be supplemented) |
| The introduction is written as the second introduction, and the introduction and summary are repeated in large paragraphs | Violation of Tsinghua §4.5 (should be deleted to continue the problem, and the summary should not be repeated) |

## 4. Method Design Presentation Standards

- **Each chapter must be equipped with 1 overall method framework/structure diagram (5/5)**, placed at the beginning of the framework/method section, followed by (1)(2)(3) module by module
  Explain data flow. There is no `\ref{fig:...}` → **E-FIG(Major)** in Method/Framework section.
- **Formula 20~40 numbered formulas/chapter**, consecutive numbers (X-n); after each formula, "**X in the formula - interpretation**" is explained symbol by symbol (GB/T convention).
  The sampling inspection formula lacks the meaning of "in the formula" (LLM lane).
- **Mechanism modeling first lists the assumptions** (Zinc "make the following assumptions: 1)...4)") - Fixed actions in the mechanism chapter.
- **The algorithm presents three states, and can be switched within the same article according to the nature of the method** (red line 9, not forced to be unified throughout the article): ① Pseudocode box "Algorithm X-1
  "Input/Output/Step" (Yanda Department 3/3); ②Numbered step list; ③Flowchart (milled pseudocode + flowchart dual presentation).
  Deterministic algorithms mostly use pseudocode, and loop feedback control mostly uses flow charts.
- **Problem formalization in three states** (red line 8): ① Independent "Problem Description/Definition" section (Powder 4.2.1: Symbol + Mapping + Formula);
  ②Embedded method derivation; ③**Optimization model prefix Chapter 2, methods chapter cross-chapter reference number** - single data source, avoid repeated derivation,
  Legal and recommended.
- **Large papers must be more detailed than small papers** (sampled inspection by the Chinese Academy of Sciences): method principles, numerical/theoretical basis, and parameter fitting details should be more detailed than submitted small papers.
  More complete, not just a brief introduction.

## 5. Experimental Writing Standards (Industrial Edition)

- **Four elements of data description** (5/5, any one is missing → E-DATA Major): source (factory/device desensitization), sample size, training/testing
  Partitioning, preprocessing (filtering/3σ/normalization/time scale alignment). Four methods of desensitization: factory name anonymity, variable code, working condition limit,
  Numeric scaling statement.
- **Three comparison groups and four fairness controls**: classical baselines + comparable SOTA methods + ablation variants; the four controls are the same dataset, split, metrics, and hardware, so improvements are attributable to the method rather than more data or longer training. **Optimization and decision chapters may use only manual operation based on expert experience as the baseline and need not include an algorithmic baseline** (cement firing Chapter 5 and the solid-waste-incineration manual-operation case). This is a valid core comparison (red line 4).
- **Indicators must be given formulas, all for the first time, and will not be relisted for subsequent reuse**: RMSE/MAE/MAPE/R², ISE/IAE/ITAE, HV/GD, etc. + Business
  Indicators (standard compliance rate, energy saving rate). The index word appears but there is no formula in the chapter and the previous chapter is not reused (no "X.X Section" reuse reference) →
  **E-METRIC（Minor）**。
- **Parameter settings must have special tables + Sensitivity analysis** (5/5): Super parameters of comparison methods are also listed; super parameters "determined by trial and error method" can be written truthfully +
  Sensitivity sweep parameter chart replaces strict parameter adjustment (parameter sensitivity discussion has become an invisible requirement). No parameter clue → **E-PARAM(Minor)**.
- **Result Table Specifications**: Chinese and English dual questions; single-point values are mainly (4/5) legal; the best bold or last line is the winning and losing statistics line +/-/~; training/testing
  Double columns. Chapter report of stochastic optimization algorithm **Mean±Std** (pulverized 20 times) - but **no mean±variance, no significance test will not be reported**
  (Red line 3).
- **Three-stage routine for result analysis (5/5 strong paradigm)**: describing the phenomenon (calling chart numbers) → quantitative comparison (quoting numbers in the table + relative
  Percentage) → Mechanism attribution ('This is because/the main reason is'), the last sentence "Therefore/to sum up,... is effective" ends.
**Fourfold echoes of pictures-tables-text-percentages**, running accounts are prohibited. Experimental Section None `\ref{tab:/fig:}` → **E-REF(Major)**;
  Attribution sentence density is too low (default <15% or minimum 3 lines) → **E-ATTR (Major)**.
- **Necessary for ablation (5/5) + Top level closed-loop advanced standards**: Mechanism dismantling/single source vs fusion/just improve any form (nothing in the chapter)
  Ablation clue → **E-ABL (Info)**, various forms without hard blocking). Advanced standards: ① Each ablation forms a logical closed loop (mechanism required
  Evidence, not just a slight increase in numerical value); ② Verify the interaction between modules (A+B moves together ≠ their respective sums must be explained); ③ Consistent across data sets/cross working conditions.
- **Dimensional caliber of significance test** (no one size fits all): The direction that requires statistical inference (empirical evidence, partial control comparison) is a hard requirement;
  **The convention for comparison of purely deterministic algorithms is the mean ± variance of multiple runs + consistency across multiple operating conditions, not the p-value**. Industrial Process Paper 5/5 None
  p-value/t-test is conventional (red line 3).
- **Enhancement items** (if any, the stronger, no exceptions): public benchmark + two-stage verification of this issue (solid waste incineration ZDT is first certified and universally verified)
  Applicable); multiple working conditions/multiple varieties (three varieties of grinding); disturbance robustness; real-time reasoning (delay + memory); ** Process mechanism translation
  Algorithm output** (Powder translates the optimization solution into process operation logic and then calculates the energy saving rate, instead of just reporting numbers).
- **Honest wording for simulation versus on-site application** (red line 12, positive check): even when the data are real, offline validation must be described as a "simulation experiment" or "offline validation" and **must not be presented as an "on-site application"**.

## 6. Summary template of this chapter

- **Template (5/5)**: Single paragraph "**Problem → Method → (Key) Number → Meaning**" (can string method points 'first...last',
  with core numbers). Length **1 paragraph, 150~350 words** Mainstream (numbered and bulleted retelling contributions belong to the minority, not the default form).
- **Whether to end with a forward link such as "lays the foundation for Chapter X" is context-dependent**: the zinc thesis uses one in all sampled cases and names the target chapter, while the cement-firing, clinker, and solid-waste-incineration theses generally do not.
  → **Treat the forward-link sentence only as an Info recommendation; its absence must not trigger a hard finding** (red line 2). An engineering-application chapter summary should close with evidenced mechanisms, the current evidence boundary, and its contribution to the thesis. Quantified benefits and broader applicability may be stated only when the supplied evidence supports them.
- **Conclusion ≠ Simple repetition of the summary of each chapter** (Tsinghua §4.6): "Conclusion/Summary and Outlook" of the full text comprehensively summarizes the contribution, limitations and future of the full text
  Direction; the summary of this chapter only summarizes the evidence in the chapter, and does not mechanically repeat the "Chapter X..." sentence pattern of each chapter.

## 7. Echoing the framework of Chapter 2

The method chapter must correspond to the overall framework in Chapter 2 (5/5), but **either forward or reverse correspondence is compliant**:

- **Fixed Anaphora**: "According to Chapter 2... Process/Variable Analysis";
- **Cross-chapter reference to Chapter 2's model number/table number/variable system** (CV/MV/EV code), with objects of the same name throughout the book;
- **The method chapter does not redraw the overall structure, but only draws the local framework of this chapter** (does not duplicate the framework diagram of Chapter 2).

**Reverse correspondence is also compliant**: when the Chapter 2 framework already maps method modules to later chapters, a later method chapter need not explicitly refer back to Chapter 2. Therefore, a chapter with neither an explicit "Chapter 2" reference nor a cross-chapter `\ref` triggers only E-ECHO (Info) and **must not be escalated**.

## 8. Special section on "Sense of splicing of short papers" and draft status

Industrial doctoral theses are often assembled from several published papers, but **the thesis text must not expose stitching or draft residue**. Four recurring blind-review concerns are
(Cross-confirmed by official random inspection and blind review experience): **The innovation point is not outstanding / the main line of logic is broken / the workload is thin / it feels patchwork**. control
Avoid:

| Exposed writing (should be changed) | Suggested expression | Check the driveway |
| --- | --- | --- |
| "Core issues corresponding to source papers/small papers/N papers" | "N core questions/N research contents" | P-PAPER (Script, default is to report all hits in all chapters) |
| "This article proposes PG-MOEA/D..." (The chapter says "this article" but refers to the method in this chapter) | Change "This article proposes" | Info / LLM Lane |
| Draft state hedging: "To be verified/temporarily used as a placeholder/still in progress/completed after re-running/recalculated/does not represent the performance after enhancement" | Finalized statement or deletion | F-NOTE (Script, Info) |
| Result table placeholder row `& --- & --- & ---` | Fill in data or delete rows | F-PLACEHOLDER (Script, Major) |
| "We proposed/we found" is rampant (the Chinese Academy of Sciences named 318 "we" in a paper) | "This chapter/this article" distinguishes the contributions of authors and collaborators | LLM Lane |
| Direct translation of published English papers, obvious translation accent | Rewriting rather than translating, filling in theoretical details | LLM Lane |
| Methods and figures are screenshots from published papers, unlabeled/uncited | Self-drawn or cited; figures not mentioned in the text are deleted | LLM Lane |
| **Contradictory method name** (the screenshot example uses NSGA-II, which conflicts with the full text PG-MOEA/D) | Unified terminology and symbol table | **LLM lane** (semantic level, scripts are not judged) |

**Duplicate Check List** (LLM judgment, scripts are not hard-checked):

- [ ] There are no meta-expressions such as "source paper/small paper/N papers" and "to avoid a sense of splicing" in the entire chapter;
- [ ] Method names/model abbreviations should be consistent in chapter titles, figure titles, text, and pseudocode (no self-contradiction);
- [ ] The result table has no placeholder rows and no draft hedging words;
- [ ] Each chapter progresses around the only theme of the whole text (Tsinghua §4: It cannot be pieced together from several pieces of work), and there is a main thread running through it.

## 9. List of red lines to prevent false alarms (12 items, the checker must not report errors)

The following situations are **valid and must not produce a Major finding** (negative cases locked against five reference theses):

1. **The introduction to the chapter on parallel methods does not follow the above** → Cannot be reported as Major (depends on driven judgment, pure parallel is at most Info).
2. **The chapter summary has no forward-link sentence such as "lays the foundation for Chapter X"** → Do not report it (at most recommend it as Info).
3. **No statistical significance test / no mean ± variance** → Do not report (industry practice).
4. **Optimization/Decision-making chapter has no algorithm baseline, only manual experience comparison** → Legal.
5. **The method chapter contains a textbook-style basic theory section** → Legal.
6. **Introduction to preview method route instead of section number directory** → Legal (both states are acceptable).
7. **The introduction contains a lot of `\cite`** → Legal (can afford a small summary).
8. **The optimization problem model is not included in this chapter but is quoted from Chapter 2** → Legal and recommended.
9. **Algorithm presentation method is not consistent between chapters** (pseudocode vs flowchart) → legal.
10. **Four states of engineering application** (independent chapter/integrated final chapter/embedded experimental section/no on-site verification) → are all legal.
11. **The control chapter uses simulated controlled objects (NARX fitting) to conduct control experiments** → It is a legal and common practice.
12. **Simulation vs field wording boundary**: If the data is real but offline verification must be written as "simulation experiment/offline verification", "field application" must not be written
    ——Wording honesty checkpoint (positive check, non-false positive exemption).

## 10. Threshold and Source

| Dimensions | Default | Source |
| --- | --- | --- |
| Number of pages in a single chapter | 10~30 pages (mainstream 15~21) | 5 actual tests |
| Directly under the second level section | 4~6 | 5 actual tests |
| Figure/Chapter (Figure > Table 3:1~7:1) | 5~17 | 5 actual measurements |
| Table/Chapter | 1~9 | 5 actual tests |
| Numbering formula/chapter | 20~40 | 5 actual measurements |
| Chapter introduction | 1~3 paragraphs, 300~500 words (except for chapters with dense literature) | 5 actual tests |
| Summary of this chapter | 1 paragraph, 150~350 words | 5 practical tests |
| E-ATTR attribution sentence density | ≥15% or at least 3 lines (chapter-by-chapter) | Reuse B3 vocabulary list |

All thresholds reflect **disciplinary conventions**. **The supervisor's and graduate school's latest requirements take precedence**, and command-line options may override the defaults.

### Script checks mapping table

Each specification ↔ corresponds to the check code (the lane column is the script module it belongs to, both are `[Script]`; `[LLM]` is semantic-level manual), the last column
Point to the specification section:

| Checkcode | Lane | Trigger | Severity | Section |
| --- | --- | --- | --- | --- |
| P-PAPER | logic (default is full chapter, all hits are reported) | Source paper/small paper/N papers | Minor | Eight |
| F-NOTE | format | draft hedging word (see the eight-section word list) | Info | eight |
| F-PLACEHOLDER | format | Table body row ≥2 empty placeholder cells (`& --- & ---`) | Major | Five |
| E-DATA | experiment `--per-chapter` | The experiment section lacks data sources or division clues | Major | Five |
| E-ATTR | experiment | Experiment section attribution sentence density < 15% (or < 3 lines) | Major | Five |
| E-REF | experiment | Experiment section has no `\ref{tab:` and no `\ref{fig:` | Major | Five |
| E-FIG | experiment | Methods/Framework Section None `\ref{fig:` | Major | Four |
| E-METRIC | experiment | The indicator word appears but there is no formula and no cross-section reuse references | Minor | Five |
| E-PARAM | experiment | Experiment section has no parameter setting clue | Minor | Five |
| E-ABL | experiment | No ablation clues in chapter | Info | Five |
| E-ECHO | experiment | There is no "Chapter 2" anaphora in the whole chapter and no cross-chapter `\ref` | Info | Seven |
| `--first-chapter N` | logic (parameter) | Declare the first `\chapter` real chapter number in a single chapter file, enable continuity/chapter sequence check | — | Three |
| The method name is contradictory | **LLM** | The method name/abbreviation in the text conflicts with the full text | Manual | Eight |
| Authenticity of the succession / "This article vs this chapter" | **LLM** | Whether the following sentence corresponds to real dependence and whether the reference is misplaced | Artificial | Three/Eight |
| The formula lacks the interpretation of "in the formula" | **LLM** | The numbered formula is missing the symbol-by-symbol interpretation (sampling) | Manual | Four |

## Output suggested format

```latex
% 方法章实验节（chapters/chapter4.tex:412）[Severity: Major] [Priority: P1]: [Script] E-REF 实验节未见 \ref{tab:...}/\ref{fig:...} 引用
% 建议：结果分析须"点名图表号 → 引表内数字与相对百分比 → 机理归因（这是因为…）"，图-表-文字须四重呼应。
```

---

## Further reading

- [process-chapter-guide-zh.md](process-chapter-guide-zh.md): Chapter 2 process analysis chapter format, point after identification.
- [introduction-guide-zh.md](introduction-guide-zh.md): The six-section skeleton of the introduction (it is forbidden to repeat the summary of the chapter introduction).
- [thesis-writing-guide.md](thesis-writing-guide.md): Main line of the full text, two-paragraph template for chapter introduction and single-paragraph template for chapter summary.
- [engineering-application-chapter-guide-zh.md](engineering-application-chapter-guide-zh.md): Argument and evidence boundaries for an independent engineering-application or system-implementation chapter.
- [structure-guide.md](structure-guide.md): The number of directly subordinate sections is flexible, and the chapter title is linked to the section title.
- [../modules/logic.md](../modules/logic.md): P-PAPER generalization with `--first-chapter` description.
- [../modules/experiment.md](../modules/experiment.md): `--per-chapter` Chapter-by-Chapter E-\* Checklist.
- [../modules/format.md](../modules/format.md): F-NOTE extended table and F-PLACEHOLDER placeholder row check.
