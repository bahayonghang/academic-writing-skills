# Paragraph Roles and Structural Deduplication in Thesis Body

This guide provides baseline responsibility allocations and structural deduplication rules for each paragraph level in the thesis body. It focuses on resolving common structural repetition and writing redundancy issues frequently flagged in blind reviews and supervisor annotations, such as "this was already discussed earlier," "repeating the full-chapter problem at the start of each subsection," "translating algebraic operations word by word after equations," and "introducing new arguments in chapter summaries."

## Entry Points

```bash
uv run python scripts/analyze_logic.py main.tex --paragraph-roles
uv run python scripts/analyze_logic.py main.tex --paragraph-roles --section 3
```

- **Applicable scope**: Main-text body chapters from Chapter 2 up to the chapter before the conclusion (for the dedicated introduction chapter guide, see [`introduction-guide-zh.md`](introduction-guide-zh.md); for the dedicated conclusion chapter guide, see [`conclusion-guide-zh.md`](conclusion-guide-zh.md)).
- **Division of labor across guides**:
  - For two-paragraph chapter introduction handoffs and flexible rules, see [`thesis-writing-guide.md`](thesis-writing-guide.md) and Section 3 of [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md);
  - For section lead-in specifications, see [`structure-guide.md`](structure-guide.md);
  - For method subsection openings and equation closure, see Sections 3 and 5 of [`method-description-guide-zh.md`](method-description-guide-zh.md);
  - For experimental results analysis, see [`results-analysis-guide-zh.md`](results-analysis-guide-zh.md);
  - For chapter summary specifications, see [`thesis-writing-guide.md`](thesis-writing-guide.md) and Section 6 of [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md).
- **Execution profile**: `--paragraph-roles` is an optional additive flag, disabled by default; without this flag, `logic` output remains completely unchanged. All findings are `[Script]` observations defaulting to Info/P3 and including `Meaning-Check: NEEDS-LLM`.

## Six-Position Responsibility Matrix

| Position | Suitable responsibility | Do not repeat | Existing owner guide | Check code |
| --- | --- | --- | --- | --- |
| Chapter introduction | Chapter problem, interface with previous chapter, key proposed scheme | Reintroducing the broad industry background; detailing every subsection sequence | [`thesis-writing-guide.md`](thesis-writing-guide.md), [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md) | `_check_chapter_intro` (default), `PR-INTRO-BG`, `PR-INTRO-TOC` |
| Section lead-in with subsections | Define current section object or provide concise reading roadmap | Repeating the entire chapter problem and the complete method chain | [`structure-guide.md`](structure-guide.md) | S1 `_check_heading_leads` (default), `PR-LEAD-DUP` |
| Opening paragraph of method subsection | Directly state module inputs, function, or unresolved interface | Re-listing all research challenges from scratch | [`method-description-guide-zh.md`](method-description-guide-zh.md) | M-HEADING, M-SEQWORD, `PR-SUB-CHAL` |
| Post-equation paragraph | Explain symbols, key mechanism, boundary conditions | Translating every multiplication and addition step into text in order | [`method-description-guide-zh.md`](method-description-guide-zh.md) | M-EQUATION, `PR-EQ-NARR` |
| Experimental result paragraph | Numeric differences, visual patterns, moderate explanations | Reciting every table cell mechanically, speculating on failure causes without evidence | [`results-analysis-guide-zh.md`](results-analysis-guide-zh.md) | RA-*, B3, E-ATTR (pointer only, no new codes) |
| Chapter summary | New method highlights, most important results, necessary interface | Adding new arguments; re-listing the complete training/deployment pipeline | [`thesis-writing-guide.md`](thesis-writing-guide.md), [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md) | `PR-SUM-NEW`, `[LLM]` only |

## Position-by-Position Descriptions and Examples

### Chapter Introduction

- **Suitable responsibility**: Clarify the specific technical problem to be solved in this chapter, the output/conclusion interface from the preceding chapter, and the core technical solution proposed in this chapter.
- **Do not repeat**: Reintroducing the macro application background of the entire industry at length; providing both a section directory and a roadmap preview in the same introduction, or elaborating on the detailed contents of every subsection.
- **Negative example** (repeats the industry background and macro demand already established in Chapter 1 introduction):
  > In recent years, with the rapid development of intelligent manufacturing and industrial internet, process industries have occupied an increasingly vital position in the national economy. However, due to complex operating conditions, harsh environments, and sensor noise interference, achieving high-precision state estimation has become a hot research topic in academia and industry. This chapter is organized as follows: Section 3.1 introduces preprocessing, Section 3.2 introduces model construction, Section 3.3 introduces parameter optimization, Section 3.4 introduces experimental evaluation, and Section 3.5 summarizes the chapter.
- **Positive example**:
  > The offline surrogate model established in Chapter 2 verified the feasibility of state estimation, but its generalization error increases significantly under severe operating condition fluctuations. To address this dynamic generalization bottleneck, this chapter proposes an adaptive dynamic reweighting mechanism that adjusts estimator weights using online sequential residuals. This chapter first presents the mathematical formulation of the mechanism, second designs the online reweighting criteria, and finally evaluates generalization performance on industrial operational data.

### Section Lead-in with Subsections

- **Suitable responsibility**: Define the specific object analyzed in this section, clarify its role in the overall chapter, or provide a brief and clear reading roadmap for direct subsections.
- **Do not repeat**: Reciting the full chapter's scientific problems, complete method chain, and multi-module architecture that were already introduced in the chapter introduction.
- **Negative example** (repeats the chapter-level challenges and complete method chain already established in the chapter introduction):
  > To address the core challenges of large estimation errors and weak generalization under non-stationary conditions, this chapter overall proposes a complete state estimation system comprising dynamic feature extraction, adaptive reweighting, and multi-task output. As a core component of this system, this section will conduct in-depth research surrounding all generalization bottlenecks and feature extraction challenges mentioned above.
- **Positive example**:
  > This section focuses on designing the adaptive reweighting module. The module receives sequential representations from the preceding section, estimates a weight matrix from dynamic deviations, and outputs weighted representations. Below, Section 3.2.1 establishes the mathematical formulation of the reweighting model, and Section 3.2.2 derives the online update rule.

### Opening Paragraph of Method Subsection

- **Suitable responsibility**: Directly state the input objects, core function, or directly inherit unresolved interfaces from upstream modules.
- **Do not repeat**: Enumerating all domain research challenges from the very beginning once again (e.g., "challenge one... challenge two... challenge three...").
- **Negative example** (repeats global research challenges already summarized in the section lead-in or chapter introduction):
  > When constructing feature projection operators, existing studies generally face multiple challenges: first, the feature redundancy issue caused by high-dimensional observations; second, the distribution shift problem resulting from asynchronous multi-modal sampling; and finally, the overfitting hazard induced by scarce labeled samples. To overcome all the aforementioned challenges, this subsection conducts in-depth derivations.
- **Positive example**:
  > Addressing the asynchronous feature representations output by the preceding section, this subsection constructs a time-continuous projection operator. This operator maps discrete time indices into a continuous latent manifold, eliminating multi-channel alignment discrepancies while preserving sampling topology.

### Post-Equation Paragraph

- **Suitable responsibility**: Use "式中" (where) to define newly introduced symbols; explain the key physical or algorithmic mechanism embodied in the equation, as well as valid assumptions and boundary conditions.
- **Do not repeat**: Translating algebraic operations such as matrix multiplication, summations, and inversions word by word into natural language sentences following the symbol sequence.
- **Negative example** (repeats algebraic computation procedures already clear from mathematical notation):
  > In the above equation, first calculate the matrix product of matrix $\mathbf{A}$ and input vector $\mathbf{x}$, then add the bias vector $\mathbf{b}$ to the multiplication product, then transpose the summed vector and multiply it by weight matrix $\mathbf{W}$, and finally apply the Softmax activation function to compute final output probabilities.
- **Positive example**:
  > 式中: $\mathbf{W}$ is the dynamic scaling matrix, and $\mathbf{b}$ is the condition bias term. This transformation projects inputs onto the orthogonal complement of principal components, filtering out steady-state drift disturbances while preserving dynamic transitions. When the signal-to-noise ratio falls below a preset threshold, the bias term falls back to the empirical mean prior.

### Experimental Result Paragraph

- **Suitable responsibility**: Report statistically significant numeric differences between major baselines, extract distribution and convergence trends from plots, and provide reasonable mechanism-level explanations.
- **Do not repeat**: Reading every cell value in a table mechanically; speculating on baseline failure mechanisms without ablation or targeted experimental evidence.
- **Negative example** (repeats every numeric cell already presented in experimental tables):
  > As shown in Table 4-2, Algorithm A achieves an RMSE of 0.321 on Dataset 1, Algorithm B achieves an RMSE of 0.345, Algorithm C achieves 0.389, and our method achieves 0.287; on Dataset 2, Algorithm A achieves 0.412, Algorithm B achieves 0.430, Algorithm C achieves 0.478, and our method achieves 0.356. We speculate this is because Algorithm C lacks an attention mechanism, causing deep layers to fail to converge.
- **Positive example**:
  > Table 4-2 compares estimation errors across four algorithms under two operating regimes. Under non-stationary conditions (Dataset 2), our method reduces root mean square error by 13.6% compared to the closest runner-up Algorithm A, demonstrating that the dynamic reweighting mechanism stably tracks state shifts under heightened disturbance.

### Chapter Summary

- **Suitable responsibility**: Synthesize the new method highlights proposed in the chapter, the most critical empirical results or core findings, and necessary interfaces provided for subsequent chapters or the thesis mainline.
- **Do not repeat**: Introducing new mathematical derivations, figures, tables, or uncited references into the summary; reciting execution steps from data cleaning, preprocessing, model training to parameter settings in a chronological pipeline log.
- **Negative example** (repeats detailed formulas and citations derived in body subsections, introducing new arguments not previously demonstrated):
  > This chapter investigated time-series state estimation problems. First, we conducted data preprocessing; second, we formulated the total loss $\mathcal{L}_{\text{total}} = \alpha \mathcal{L}_{\text{rec}} + \beta \mathcal{L}_{\text{reg}}$ as shown in Eq. (3-28), and trained the model using convergence criteria from literature \cite{smith2024}. Finally, we obtained optimal weights $\mathbf{W}^*$.
- **Positive example**:
  > Addressing estimation drift under non-stationary operating conditions, this chapter proposed an adaptive dynamic reweighting method. We first established residual-based weight update rules and second eliminated sampling asynchrony via continuous projection. Industrial empirical validations demonstrate that this method significantly improves tracking precision and disturbance rejection under severe fluctuations, providing reliable state feedback for the global closed-loop optimization in Chapter 4.

## Cross-Level Deduplication Criteria

Academic theses encompass multi-tiered hierarchical structures: introduction, body chapters, sections, subsections, and paragraphs. To prevent each level from repeating previous assertions independently, follow these criteria:

1. **Complete in one place, referenced elsewhere**:
   - The authoritative complete definition of core concepts, background demands, overall frameworks, or evaluation criteria belongs only to the earliest introducing layer (introduction defines background and status quo, chapter intro defines chapter scheme, section lead-in defines section object, body subsections detail operators and mechanisms);
   - Subsequent levels must use referential phrasing (e.g., "using the weighting matrix defined in Section 3.2", "for the experimental platform setup, see Section 4.1"), strictly avoiding redefining terms in every subsection.
2. **Two questions of information increment**:
   - When reviewing any transition paragraph or linking sentence, authors and reviewers should ask:
     1. Does this paragraph provide new information (a new object, constraint, derivation, or empirical trend) not yet stated above?
     2. If this paragraph or sentence is removed directly, does the logical chain of the chapter or section break?
   - If it provides no new information and its deletion does not interrupt the argument, it constitutes writing redundancy and should be compressed or deleted.
3. **Four types of repetition and remediation**:
   - **Synonymous restatement**: Rewriting earlier arguments with near-synonyms without new evidence -> Remove redundant sentences and preserve the initial clear formulation.
   - **Premature conclusion restatement**: Claiming full-chapter or whole-thesis conclusions at the start or end of a subsection before evidence is presented -> Narrow the claim to local outputs of the current subsection.
   - **Material duplication**: Repeating identical dataset sources, hardware configurations, or baseline parameters across multiple method subsections -> Consolidate into a dedicated subsection and use forward/backward references elsewhere.
   - **Concept redefinition**: Redefining the same generic mathematical symbols across multiple subsections with formulas -> Standardize in a notation table or define upon first appearance only.
4. **Structural recapitulation retention principle**:
   - Chapter summaries and thesis conclusions serve structural recapitulation roles to close the argument chain;
   - Structural recapitulation is allowed to review key points, but must be **densely synthesized and compressed** (chapter summaries compressed into a single paragraph stringing highlights), never degrading into chronological step-by-step pipeline recitations.
5. **Transition sentences carrying level-specific nouns**:
   - Transitions between paragraphs and subsections should use specific academic domain nouns belonging to that level (e.g., "addressing asynchronous latencies following feature alignment");
   - Avoid generic navigation phrases like "the following introduces...", "next we discuss...", or "this section is divided into three parts", which lack academic information increment.

## Coordination with Existing Rules

To maintain strict alignment with existing repository specifications and calibrated industrial doctoral thesis practices, this guide establishes the following coordination rules:

- **D2 Chapter introductions: either directory or roadmap, not both**:
  - The established rules in Section 3 of [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md) ("both numbered introduction sections and unnumbered lead-ins are compliant" and "both roadmap previews and section directories are compliant") remain fully valid;
  - This guide only adds a deduplication constraint: **choose either a roadmap preview or a section directory, never both in the same introduction**; section directories must not detail the contents of every section. The checker only triggers findings when both co-occur or when a section directory contains $\ge 5$ detailed items.
- **D3 Chapter summaries: boundary between highlights and step-by-step logs**:
  - The established rule that "stringing method highlights with 'first... finally' is compliant" remains valid;
  - This guide clarifies the boundary: summarizing each method highlight in a single clause (macro chapter-level granularity, e.g., "first proposed... second derived... finally verified...") is fully compliant; however, elaborating into step-by-step execution pipelines (e.g., data cleaning -> feature engineering -> initialization -> forward iteration -> checkpoint deployment) constitutes redundant pipeline logging. This determination is semantic and handled by the `[LLM]` review checklist.
- **D4 Chapter summaries: no new arguments**:
  - The established rule of "do not add results or citations not present in the body" is extended: **do not add new citations, formulas, figures/tables, or derivations**;
  - Back-referencing existing figures or tables in the chapter body within the summary (e.g., using `\ref{fig:...}` or `\ref{tab:...}`) is compliant argument review and will not trigger findings.
- **D5 Chapter introductions: boundary of industry background and literature review**:
  - The existing rule "do not repeat the introduction literature review (Tsinghua §4.5)" is aligned alongside "do not restate industry background";
  - Chapter 2 is exempt at the script layer as an overview-style introduction bridging the background; the guide still recommends that body chapters keep background strictly focused on immediate technical dependencies.

## [LLM] Review Checklist

When running `--paragraph-roles` to obtain heuristic candidates, LLMs or human reviewers should evaluate semantic compliance using the following checklist:

1. **Chapter introduction**:
   - [ ] Does the introduction spend extensive paragraphs restating macro industry importance or national policies rather than focusing on direct chapter interfaces?
   - [ ] Does the ending append a full section-by-section list after already providing a "first... finally..." roadmap preview?
2. **Section lead-in with subsections**:
   - [ ] Does the lead-in repeat the overall chapter goal and all method modules rather than establishing the context for this specific section?
   - [ ] Is the lead-in merely a generic announcement ("this section is divided into three subsections") without explaining the progression logic?
3. **Opening paragraph of method subsection**:
   - [ ] Does the subsection opening directly state input data and eliminated constraints, or does it re-list all three thesis-level challenges once again?
   - [ ] Does the opening connect with data interfaces from the section lead-in or previous subsection?
4. **Post-equation paragraph**:
   - [ ] Does the text following the formula merely translate mathematical operators (addition, convolution, transpose) in sequence without explaining variable semantics or mechanisms?
   - [ ] Does the text clarify downstream uses and valid boundary conditions for the calculated object?
5. **Experimental result paragraph**:
   - [ ] (Detailed criteria refer to [`results-analysis-guide-zh.md`](results-analysis-guide-zh.md) and RA-*/B3 rules; this checklist does not duplicate them)
   - [ ] Does the paragraph degenerate into reading table cells line by line without synthesizing key margins or trends?
   - [ ] Does it assert baseline internal defect mechanisms without comparative ablation evidence?
6. **Chapter summary**:
   - [ ] Does the summary introduce new citations, formulas, or figures not previously discussed in the body?
   - [ ] Does the summary recite every experimental setup and training step as a chronological pipeline log?

## Check Mapping

| Position | Existing check code | New check code (`--paragraph-roles`) | Manual / LLM dedicated responsibility |
| --- | --- | --- | --- |
| Chapter introduction | `_check_chapter_intro` (bridging) | `PR-INTRO-BG`, `PR-INTRO-TOC` | Evaluate whether background text is strictly required for immediate derivation |
| Section lead-in with subsections | S1 `_check_heading_leads` (lead presence) | `PR-LEAD-DUP` | Assess whether vocabulary overlap between lead-in and intro is legitimate term sharing |
| Opening paragraph of method subsection | M-HEADING, M-SEQWORD | `PR-SUB-CHAL` | Evaluate whether enumerated challenges represent module-specific motivations |
| Post-equation paragraph | M-EQUATION (missing gloss entry) | `PR-EQ-NARR` | Determine whether operator descriptions provide necessary computational steps |
| Experimental result paragraph | RA-*, B3, E-ATTR | None (pointer only, no new codes) | Evidence hierarchy and causal attribution review (read results-analysis) |
| Chapter summary | None (routes to logic guide) | `PR-SUM-NEW` | Distinguish method highlight synthesis from step-by-step pipeline recitation |

### Heuristic Threshold Constants Table

The following constants are defined in `scripts/analyze_logic.py` and are explicitly designated as **未标定 / UNVERIFIED**. They serve as heuristic screening prompts without claims on cross-corpus false-positive rates, and can be overridden via term tables:

| Constant | Default value | Semantic meaning | Calibration status |
| --- | --- | --- | --- |
| `PR_INTRO_BG_MIN_HITS` | 3 | Deduplicated background marker hit threshold in chapter intro | 未标定 / UNVERIFIED |
| `PR_INTRO_TOC_MIN_ITEMS` | 5 | Section directory detailed item count threshold in chapter intro | 未标定 / UNVERIFIED |
| `PR_LEAD_DUP_JACCARD` | 0.3500 | Upper bigram Jaccard overlap threshold between lead-in and intro | 未标定 / UNVERIFIED |
| `PR_LEAD_MIN_HAN` | 40 | Minimum Han character count for lead-in overlap comparison | 未标定 / UNVERIFIED |
| `PR_SUB_CHAL_MIN_HITS` | 2 | Challenge marker hit threshold in subsection opening (with sequence words) | 未标定 / UNVERIFIED |
| `PR_EQ_NARR_MIN_HITS` | 3 | Operator translation marker hit threshold in post-equation paragraph | 未标定 / UNVERIFIED |

## Sources

Methodological principles regarding cross-chapter deduplication, functional division, and mathematical writing in this guide are adapted from the following public URL sources:

- 知学术, [论文跨章节重复表述？去冗余的 4 步清单](https://www.openxueshu.com/archives/fourstep-checklist-for-eliminating-redundant-expressions-across-chapters-in-a-thesis) (four-step deduplication, two questions of information increment, complete in one place referenced elsewhere, corresponding to W1)
- C. Perry, [A Structured Approach to Presenting PhD Theses](https://www.ece.nus.edu.sg/stfpage/eleamk/phd/phdth1.html) (concluding summary outlines major themes without introducing new material, corresponding to W5)
- ICMJE Recommendations, [Manuscript Preparation: Preparing for Submission](https://icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) (do not repeat all data in tables or figures, emphasize key observations, corresponding to W6)
- K. Houston, [How to Write Mathematics](https://www.maths.ox.ac.uk/system/files/attachments/How%20to%20write%20mathematics.pdf) (formulas are shorthand notation, explain relationships rather than detailing every step, corresponding to W10)

Tsinghua Graduate School's Thesis Writing Guide §4.5 (chapter intro does not repeat introduction review) and §4.6 (conclusion does not simply repeat chapter summaries) are documented in Sections 3 and 6 of [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md), and their standards are directly maintained here.
