# Chapter 2 (Process Analysis Chapter) Writing Guide

**Chapter 2** writing and diagnosis of a Chinese doctoral thesis in an industrial/process context. This refers specifically to "process flow analysis +
Full text method structure "chapter format (hereinafter referred to as **Process Analysis Chapter**): Chapter 2 first analyzes the process/process and introduces modeling/control difficulties.
Then it falls to the overall methodological framework that governs subsequent chapters. Diagnostic entry:

```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex --process-chapter
uv run python $SKILL_DIR/scripts/check_format.py main.tex
```

> All thresholds for this article (length, number of sections, number of words in the introduction, word list of process characteristics) are 5 doctoral theses in the process industry and public catalogs
> The **discipline practice** caliber of the survey (see each section for the source), **subject to the latest regulations of the instructor and the graduate school of the school**; command line
>Thresholds can be overridden. The reference papers are referred to by process areas (solid waste incineration, cement burning, cement clinker calcination, cement grinding,
> Zinc smelting and leaching), page numbers are decrypted PDF physics pages.

## 1. Chapter judgment (judge first, then set rules)

Chapter 2 has three mainstream forms with different criteria and rules; **they must not be mixed**. Identify the form first, then apply its own rules:

| Features | Process Analysis Chapter Format (this guide) | Methods Chapter Format | Split Two Chapter Variations |
| --- | --- | --- | --- |
| Decisive criteria | Industrial/process objects **throughout the entire text** | Methodology is the main focus, objects only appear later | Processes and solutions are divided into two chapters |
| Chapter 2 Contents | Process Analysis + Difficulties + Full Text Method Framework | Directly write methods/models/experiments | Chapter 2 Pure Technology, Chapter 3 Overall Plan |
| The review is in place | The review is in the introduction and there is no longer a review chapter | Same as Zuo | Same as Zuo |
| Which set of rules to follow | This guide + `--process-chapter` | [method-chapter-guide-zh.md](method-chapter-guide-zh.md) + experiment `--per-chapter` | The process chapter follows this guide, the plan chapter follows the framework specification |

**Criterion explanation**: Whether the industrial object is "throughout the whole text" is the decisive criterion - every chapter after the second chapter focuses on the same industrial process
(Multi-chapter modeling/prediction/control/optimization) is a process analysis chapter; the application object only appears in the last one or two chapters for verification, then it is
Methods chapter format shall be handled according to the special chapter guidelines for methods chapters. This guideline does not apply. Script `--process-chapter` will do ** chapter format first
Prejudgment (dual signals)**: The chapter/section title must hit both the process signal (process/process/process analysis/variable analysis) and the frame signal
(overall framework/technical framework/research plan), apply P-\* check, otherwise only an Info prompt "If it is method + experiment" is output
Please follow the "method chapter rules" for chapter format (the common "problem description/overall framework" section names in method chapters will not be triggered separately).

## 2. Recommended skeleton and order invariants

The format of the 5 reference papers is 5/5 consistent, and the recommended skeleton is:

```text
2.1 引言（或章标题后导语）
2.2 工艺/过程分析（常并入变量选取）
2.3 变量/数据〔可选，3/5 论文在此建立统一数据契约〕
2.4 难点/关键问题
2.5 总体框架/方案
2.6 本章小结
```

**Order Invariant** (P-ORDER base): `工艺分析 →（变量/数据）→ 难点/问题 → 总体框架 → 小结`.
**The difficulties section must precede the framework section** because the framework is a structured response to those difficulties. Reversing the order (framework before difficulties) triggers
P-ORDER（Minor）。

Reference paper skeleton comparison (section titles have been grouped according to process areas):

| Thesis | Direct section | Skeleton points | Length |
| --- | --- | --- | --- |
| Solid waste incineration | 5 | Introduction / Process Analysis / Intelligent Prediction and Optimization Control Architecture / Importance and Difficulties / Summary | PDF p30–41 |
| Cement Firing | 6 | Introduction / System Introduction / Variable Selection and Characteristics / Problem Description / Framework Design / Summary | PDF p27–44 |
| Cement clinker calcination | 5 | Introduction / Process description / Key issues / Forecast options / Summary | PDF p28–37 |
| Cement grinding | 7 | Introduction / Process analysis and variable selection / Data preprocessing / Optimization problem / Optimization framework / Optimization model / Summary | PDF p35–52 |
| Zinc smelting and leaching | 4 | Process analysis / Difficulty analysis / Overall framework / Summary (**Introduction after chapter, unnumbered introduction section**) | PDF p30–40 |

Chapter title pattern: `〈对象过程〉+〈工艺分析/过程描述/问题描述〉(+〈框架/方案〉)`, common doublet
(Such as "Process Analysis and Operation Optimization Framework of Cement Grinding Process").

## 3. Process description specification (funnel type)

Organization = **Four-layer funnel type** (most typical of solid waste incineration and zinc smelting):

1. **Full process positioning**: First, give the whole process diagram to explain the panoramic view of the process (Zinc Smelting Figure 2-1 The whole process of hydrometallurgical zinc smelting);
2. **Core process focus**: Zoom in to the process where the research object is located (Zinc smelting Figure 2-2 Neutral leaching 5-tank cascade);
3. **Equipment/Mechanism**: Equipment number + chemical reaction equation/mechanism (Solid waste incineration Figure 2-1 contains equipment number 33, Arrhenius
   formula and thermochemical equation; zinc smelting gives the leaching reaction equation);
4. **Key variables**: Convergence to the controlled quantity/key variable (solid waste incineration → flue gas oxygen content + 6 influencing factors; zinc smelting →
   The pH of the 3# tank outlet converges to "Adjust 1#/2# waste acid flow to stabilize 3# pH"; cement grinding → specific surface area/unit power consumption + MV/CV division).

Three hard norms:

- **Process Flow Diagram Essential** (P-FLOW Basics): 5/5 The process sections of the reference papers all have process flow diagrams (including equipment numbers or process boxes).
  There is no `\ref{fig:...}` flowchart reference in the process analysis section that triggers **P-FLOW (Major)**.
- **Depth is measured by "ability to support difficult derivation"**: It can be written to the mechanism/reaction equation level, but it must serve the following "Why is it difficult to model/
"Difficult to control" is not a textbook list of craftsmanship.
- **Must fall into variables/controlled quantities**: The end point of process analysis is to lock the research object and give variable selection, which will be established for subsequent chapters.
  **Unified Data Contract** (3/5 The paper sets up a variable table/role division in Chapter 2. For example, the specific surface area of the five cement varieties used in cement grinding is listed in the table.
  Scope, division MV/CV).

## 4. Difficulties in deriving chain templates

Derivation chain = **Process characteristic words → (cause/make/difficult/cause/cause/increase...difficulty)→modeling/control difficulties**.
5/5 The papers are all explicit cause and effect sentences, not lists of characteristic nouns. P-DERIVE check: Difficult section lacks characteristic words → **Major**;
There are attribute words but no causal connectives → **Minor**.

**Process Characteristics Vocabulary** (configurable, script `PROCESS_TRAIT_RE_ZH`): strong nonlinearity, large hysteresis/large inertia/time delay,
Strong coupling, time-varying, multi-working conditions, multi-rate, multi-source heterogeneity, fluctuation, uncertainty/disturbance, long tail, and imbalance.

Derivation mode (**indicative, not quoted verbatim**, taken from the summary of difficult sections of the reference paper):

| Paper | Illustration of derivation model | Appearing characteristic words |
| --- | --- | --- |
| Solid waste incineration | Complex composition, calorific value fluctuations, changing working conditions → Strong nonlinearity → Difficulty in accurate modeling | Strong nonlinearity, large inertia, strong coupling, uncertainty |
| Zinc smelting and leaching | Liquid-solid multiphase + multi-tank cascade coupling + strong nonlinearity → difficult to estimate pH; time delay characteristics → inconsistent time lag → difficult to coordinate operating parameters | Cascade coupling, strong nonlinearity, time delay/large lag, multiple working conditions |
| Cement firing | High data dimension, different collection frequencies → redundant variables; inconsistent coal and power consumption time scales | High dimensionality, multiple sampling frequencies, time-varying delays |
| Cement grinding | Multi-source heterogeneity + multi-time scale imbalance → difficult modeling; residence delay + graded reflow → time-varying time delay and high nonlinearity | Multi-source heterogeneity, multi-time scale imbalance, time-varying delay, strong coupling |

**Number of difficult points ≈ Number of subsequent method chapters**: The difficulty is the "problem", and each subsequent method chapter will respond to it one by one (3 difficulties in solid waste incineration, zinc smelting
3 difficulties, 3 sub-problems of cement burning, and multiple difficulties of cement grinding, respectively corresponding to multiple method chapters starting from Chapter 3). **But the difficulty↔The chapter number is
Difficulty sections usually do not name names** - Difficulty sections only summarize "problems-features", and chapter number mapping is left to Introduction 1.3 and the Framework section.

**Positive and negative examples** (P-DERIVE criterion):

| Writing | Judgment |
| --- | --- |
| "The process composition is complex, the heating value fluctuates, and operating conditions switch frequently, **causing** strong nonlinearity and high inertia in the controlled process and **making** accurate first-principles modeling difficult." | Passed (process traits + causal link + modeling difficulty form a complete derivation chain) |
| "This process has the characteristics of strong nonlinearity, large lag, and multi-variable coupling. "(Only list characteristic words) | P-DERIVE Minor (There are words but no cause and effect, the sentence "causing... to be difficult to..." should be supplemented) |
| "This process is difficult to model and requires advanced methods. "(No characteristic words, no derivation) | P-DERIVE Major (No characteristic words, the difficulty is not derived from the process) |

## 5. Formal specification of mathematical problems

After the difficulties are qualitatively summarized, a mathematical expression is given in the problem formalization section (or at the end of the difficulty section) to establish a unified symbol for the subsequent method chapter:

- **Symbol definition**: The controlled quantity/state/input/disturbance symbol is defined once (such as pH, oxygen content, f-CaO symbol), and will be used in subsequent chapters;
- **Mapping/optimization formula**: Write the research object as mapping `y = f(x)` or optimization formula `min J s.t. 约束` (cement grinding
  Multi-objective optimization model (i.e. independent formal section);
- **Subproblem-Chapter Correspondence**: Multiple subproblems include three subproblems (such as quality prediction/energy consumption prediction/decision optimization three subproblems →
  Chapter 3 / 4 / 5).

Space flexibility: The problem formalization can be incorporated into the difficult section, or it can be an independent section - independent sections will increase the number of direct sections to 6~7 (normal,
See Section 8).

## 6. Overall frame diagram specification (P-FRAME core)

The frame section is the closing point of "difficulty → frame" and must **explicitly refer back to the difficulty**. Model sentence (PhD thesis on a certain cement firing system
Beginning of Section 2.5, PDF p43): "According to the analysis of process characteristics and existing problems and difficulties in the previous section, adopt corresponding solutions. "

Three norms:

1. **Framework diagram required** (Basic of P-FRAME): 5/5 The paper has an overall framework diagram. There is no `\ref{fig:...}` in the frame section
   Frame diagram reference triggers **P-FRAME(Major)**.
2. **Hierarchical organization + data flow arrows + overlay method modules**: The framework diagram is layered according to "data/input → method module → output",
   The modules are connected with data flow arrows (Zinc Smelting Figure 2-4 Four layers: Input → Estimation → Identification → Control; overall framework diagram of cement firing:
   Data platform → two prediction models → two-loop coupled decision-making). The framework section must cover **≥2 method module names or subsequent chapter points**,
   Otherwise "frame empty" triggers **P-FRAME (Major)**.
3. **Chapter-number mapping (recommended enhancement)**: **Prefer** an explicit mapping from each framework module to "Chapter X" in the framework diagram or an interface table (for example, mapping research items to Chapters 3, 4, 5, and 6). This improves blind-review and defense navigation. **A missing mapping triggers Info only and is not a hard failure**. All five reference theses organize framework data flow by method-module names without chapter numbers. They place chapter-number mappings in the introduction's "Research Content and Organization" section (for example, a Figure 1-1 or Figure 1-3 chapter tree), and later chapter introductions refer back with wording such as "According to Chapter 2...". Both approaches are compliant; this guide recommends explicit chapter-number mapping as an enhancement.

Figure title specifications: The title of the framework diagram should contain positioning words such as "overall framework/technical route/data flow", which are consistent with the layers in the diagram; the diagram title should be in the figure
below (see [`../modules/format.md`](../modules/format.md) for details).

**Role of an engineering or system-implementation chapter**: when a thesis has a separate engineering-application chapter, the framework diagram **may include or omit it**. The zinc-smelting thesis omits it from the framework diagram and includes it only in the Introduction 1.3 chapter tree, while other theses include it through an interface table. A missing mapping for an engineering chapter produces Info only, not Major.

**Positive and negative examples** (P-FRAME criterion):

| Writing | Judgment |
| --- | --- |
| The frame section contains `\ref{fig:framework}` hierarchical data flow diagram, the text covers "Soft Measurement/Working Condition Identification/Optimization Control" ≥2 modules, and the beginning refers to the difficult points | Passed (with diagram + ≥2 modules + difficult points closed) |
| The framework section only has one paragraph of text "This article proposes a complete solution", no diagrams and no module decomposition | P-FRAME Major (missing framework diagram + empty framework) |
| The framework diagram and modules are complete, but the corresponding "Chapter X" is not marked for each module | P-FRAME Info (adding the chapter-number mapping is recommended; omitting it is still compliant) |

## 7. Introduction—Chapter 2 Division of Work List and Duplication Checklist

The introduction "Research Content and Organizational Structure" (1.3/1.4/1.5) and the overall framework of Chapter 2 have clear division of labor and **no duplication of content**
(Zinc smelting is the clearest):

| Dimensions | Introduction 1.3/1.4/1.5 | Chapter 2 Overall Framework Section |
| --- | --- | --- |
| Oriented | Full text navigation | Problem solving |
| Content | What to do chapter by chapter + progressive relationship | Technical connection and data flow between method modules |
| Coverage | All chapters (including background/project/summary) | Only core method chapters covered |
| Pictures | Chapter structure tree diagram (such as seven-chapter structure tree) | Data flow/module framework diagram |
| Foothold | Research motivation | 2.1/2.2 Technology and difficulties |

**Duplicate Check List** (To prevent repetition in the introduction—Chapter 2, LLM judgment, no hard check of the script):

- [ ] Chapter 2 Framework Section **Do not repeat chapter by chapter** the "Chapter Arrangement/What Each Chapter Does" already written in the introduction;
- [ ] The introduction chapter is based on "structural arrangement" (what Chapter N does), and the framework section is based on "technical data flow" (how modules form a closed loop);
- [ ] The only overlap between the two is the method module name - the nature of the block diagram (chapter tree vs. data flow diagram), granularity, and footing are different, and they are ** compliant
  Division of labor, non-duplication**.

## 8. Flexible caliber of length and number of sections

| caliber | default value | source |
| --- | --- | --- |
| Chapter 2 length | 10~18 pages (about 8%~13% of the full text), significantly shorter than the methods chapter | 5 reference papers measured |
| Number of direct sections | 4~7 sections (including introduction and summary), median 5~6 | Same as above |
| Introduction length | Default numbered introduction section is ≤1600 words; post-chapter introduction is about 190~600 words | Same as above |

Flexibility in the number of sections: Process analysis chapter often has 4~7 directly subordinate sections, **no mechanical alarm if more than 5 sections** (cement grinding 7 sections, due to the formalization of the problem
Independent segments are normal). When there are more than 5 sections, priority is given to checking variables/data sections that can be merged - such as "data preprocessing" and "variable selection"
"Problem Definition" is merged into "Problem Description and Modeling Fundamentals". See [`structure-guide.md`](structure-guide.md) for details
The "Number of Direct Subsections" section.

## 9. Standard expression of "sense of splicing of small essays"

A large industrial doctoral thesis is often assembled from several published papers, but **the thesis text must not reveal paper-stitching traces**
(Risk of blind review). In the P-PAPER check chapter, it can be seen that the text hits the expression "source paper/small paper/N papers" → **Minor**.

| Exposed writing style (should be changed) | Suggested expressions |
| --- | --- |
| "Three core issues corresponding to the three source papers" | "Three core issues/three research contents" |
| "The interface relationship between the three source papers in the larger paper" | "The technical connection relationship between the three research contents" |
| "This article is composed of N academic papers" | Delete, or rephrase as a progressive relationship of research content |

Note: Even **meta-statements** such as "to avoid the sense of splicing into small papers" should not appear in the main text (it also exposes the splicing intention).
`\cite{}` and text within comments are not included in P-PAPER.

## 10. Description of two introduction forms

**Both Chapter 2 introduction forms are compliant** (4:1 in the reference theses). The R2 checker supports both and does not force either form:

| Form | Paper | Length | Characteristics |
| --- | --- | --- | --- |
| Section No. "2.1 Introduction" | Solid waste incineration/cement burning/cement clinker calcination/cement grinding (4/5) | About 600~1500 words | `\chapter` directly followed by `\section{引言}`, No. 2.1 |
| No numbered introduction after the chapter title | Zinc smelting and leaching (1/5) | About 190~600 words | Go directly to the introduction after the chapter title, and then proceed to 2.1 Process Analysis |

**Key point: The introduction to Chapter 2 is an "overview of this chapter", not a "connection between the previous and the following". ** It previews each section of this chapter (introductory paragraph 2 of solid waste incineration
Preview "Process Description → Structure → Important and Difficult Points"; Zinc smelting uses "first/then/then/last" in four sections), and the undertaking object is
**The introduction establishes the research background** rather than the conclusion of the previous chapter. Therefore, the introduction to Chapter 2:

- **Only required**: Preview each section of this chapter + moderate length;
- **Not required**: Explicitly write "Chapter 1" to continue the conclusion of the previous chapter - this is the link between Chapter 3 and the method chapter.
  (See the "Introduction to the main article" section of [`thesis-writing-guide.md`](thesis-writing-guide.md)).

Based on this, the R2 checker only checks "the preview sections + length" for Chapter 2, and does not report "missing connection"; the two-part link from Chapter 3
Applicable from now on. The two forms of this chapter summary are summarized in the order of sections and are almost mirror images of the introduction/introduction (both list of points and single paragraph are available, see
[`thesis-writing-guide.md`](thesis-writing-guide.md)'s "Summary at the end of the article" section).

## Output suggested format

```latex
% 过程分析章（chapters/chapter2.tex:120）[Severity: Major] [Priority: P1]: [Script] P-FLOW 工艺分析节内未见 \ref{fig:...} 流程图引用
% 建议：补工艺流程图（含设备编号或工序框）并在正文引用；工艺章无流程图是盲审高频质疑点。
```

---

## Further reading

- [structure-guide.md](structure-guide.md): Chapter 2 Dual-track Positioning, Directly Subordinate Section Budget Flexibility.
- [introduction-guide-zh.md](introduction-guide-zh.md): The six-section skeleton of the introduction (the introduction side divided with Chapter 2).
- [thesis-writing-guide.md](thesis-writing-guide.md): Chapter 3 begins with the main body of the method chapter, the introduction, the summary of this chapter, and the three questions of the method chapter.
- [../modules/logic.md](../modules/logic.md): Detailed explanation of P-FLOW/P-DERIVE/P-FRAME/P-ORDER/P-PAPER check items.
- [../modules/format.md](../modules/format.md): F-MD/F-NOTE source code hygiene check.
