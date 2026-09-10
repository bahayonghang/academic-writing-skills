# Degree-Thesis Writing Philosophy

> “A thesis is not a pile of experiments; it is an academic story with a clear contribution.” - adapted from Neel Nanda

## Contents
- [Narrative Principle](#叙事原则)
- [Five-Sentence Abstract Formula](#摘要五句公式)
- [Seven Reader-Expectation Principles](#读者期望七原则)
- [Precise Wording](#用词精准)
- [Precision First](#精确优先)
- [Micro-Writing Techniques](#微观写作技巧)
- [Section-Specific Guide](#分章节指南)

## Narrative Principle
(Core idea)

A degree thesis tells a story around **one explicit research contribution**.

**Three pillars** (must be clear before the introduction ends):

| Pillar | Description | Example |
|------|------|------|
| **What was done** | 1-3 concrete innovations | “This thesis proposes method X and achieves Z under condition Y” |
| **Why it is credible** | Evidence matched to the claim | Theoretical proof, controlled comparison, or scoped engineering validation |
| **Why it matters** | Why readers should care | Connection to a recognized problem in the field |

**If you cannot state the contribution in one sentence, the thesis is not yet whole.**

## Five-Sentence Abstract Formula

(Adapted from Sebastian Farquhar, DeepMind)

The five-sentence formula is a planning aid for short abstracts, not a fixed sentence count or length
requirement for a degree thesis. Follow the user's current requirements and school template first, then
select an appropriate skeleton from the [abstract structure guide](abstract-structure.md). Do not force a doctoral abstract into five sentences.

1. Core result (“This thesis proposes...”, “This thesis demonstrates...”)
2. Why the problem is difficult and important
3. Method, including key terms for searchability
4. Existing validation evidence (proof, experiment, or engineering records, according to the work)
5. The most important supported result (which may be a qualitative conclusion with explicit conditions)

Do not invent numbers when quantitative results are unavailable, or add experiments to theoretical work merely to fill the formula.

**Delete** generic openings such as “With the rapid development of deep learning...”

## Seven Reader-Expectation Principles

(Adapted from Gopen & Swan)

| # | Principle | Rule | Example |
|---|------|------|------|
| 1 | **Subject-verb proximity** | Keep subject and predicate close | ❌ “The method proposed in this thesis based on..., achieved” -> ✅ “The proposed method achieved...” |
| 2 | **Stress at the end** | Put sentence focus last | ✅ “This section focuses on **input conditions**” |
| 3 | **Old information first** | Known information first, new information later | ✅ “Based on the analysis above, this thesis proposes...” |
| 4 | **One idea per paragraph** | One point in each paragraph | Split multi-point paragraphs |
| 5 | **Use verbs for actions** | Avoid nominalization | ❌ “performed an analysis” -> ✅ “analyzed” |
| 6 | **Context before display** | Explain before presenting a formula | State the meaning before the formula |
| 7 | **Clear connections** | Establish the actual relationship, then add signals if needed | No need to add “therefore” or “in addition” when objects and reasoning already provide the connection |

## Precise Wording

(Adapted from Zachary Lipton)

### Be Specific
- “Performance”: specify “accuracy” or “inference latency” only when the input identifies the metric; do not guess it.
- “Significant”: report actual statistics only when a test is supplied; otherwise remove the unsupported intensity word without adding a p-value.

### Remove Ambiguity
| Supplied input | Supported treatment |
| --- | --- |
| Only “The method may help improve predictive performance,” with no new data | “The method may improve predictive performance” retains uncertainty; do not add numbers or assert an observed improvement |
| Comparison records and an actual difference under the same protocol are supplied | State the metric, comparator, and scope from the records; do not add “statistically significant” without a test |

Specificity cannot create evidence. Use the evidence ladder in the
[results analysis guide](results-analysis-guide-zh.md) to decide what observations, comparisons, and mechanisms support.

### Avoid Empty Phrases
Delete: obviously, undoubtedly, as everyone knows, undeniably

## Precision First

(Adapted from Jacob Steinhardt, UC Berkeley)

- **Terminology consistency**: use one term for one concept throughout; co-occurrence or frequency does not establish that different technical names are synonyms
- **Explicit assumptions**: list every assumption before a theorem
- **Intuition + rigor**: pair intuitive explanation with formal proof
- **Define before use**: define every symbol and term before first use

## Micro-Writing Techniques

(Adapted from Ethan Perez, Anthropic)

- [ ] **Avoid vague reference**: ❌ “This shows...” -> ✅ “The experiment shows...”
- [ ] **Move verbs forward**: keep the predicate near the sentence opening
- [ ] **Delete fillers**: actually, to some extent, quite, relatively, basically
- [ ] **Active voice**: ❌ “The method was applied to” -> ✅ “This thesis applies the method to”
- [ ] **Quantify**: state the actual difference only when comparison records exist; “large improvement” without data calls for missing evidence, not an illustrative number

## Section-Specific Guide

These are writing suggestions. Length follows the supplied school requirements, template, and actual chapter goal.

| Section | Length Basis | Core Requirement |
|------|----------|----------|
| **Abstract** | School requirements and abstract type | Organize existing work and evidence; see [abstract structure](abstract-structure.md) |
| **Introduction** | Research problem and school requirements | Background -> problem -> contributions -> organization; see the [introduction guide](introduction-guide-zh.md) |
| **Literature review** | Evidence needed for thematic comparison | Combine synthesis with representative studies; see the [literature module](../modules/literature.md) |
| **Methods** | Actual method and proof needs | Explain existing assumptions, interfaces, and reproducibility conditions; see the [method description guide](method-description-guide-zh.md) |
| **Experiments/engineering validation** | Claim and validation type | See the [results guide](results-analysis-guide-zh.md) for analysis and the [engineering application guide](engineering-application-chapter-guide-zh.md) for engineering chapters |
| **Conclusion and outlook** | Research question and evidence scope | Answer the research question and identify actionable follow-up work; see the [conclusion guide](conclusion-guide-zh.md) |

### Introduction Must Include:
- Clear research-question statement
- Contributions corresponding to actual independent work; do not split or merge claims to meet a count
- Brief method overview
- Chapter organization
- Citation integration: a synthesis sentence may group multiple citations; expand representative studies selectively at key differences instead of introducing every reference separately

### Select Validation Details for the Actual Work:
- When experiments exist, state the claim each validates; distinguish standard deviation from standard error when repeated measurements exist
- Report actual hyperparameter search ranges when a search was performed, and relevant resources and duration for computational experiments
- A non-GPU engineering system does not need a GPU model; a theoretical chapter does not need invented training hyperparameters or experiments
- Engineering records support only their tested scope; offline replay does not establish field or operator acceptance

## Time Allocation

Spend approximately **equal time** on:
1. Abstract
2. Introduction
3. Figures and tables
4. All other content combined

**Reason**: most reviewers form a judgment before reading the method chapters.

**Reader order**: title -> abstract -> introduction -> figures/tables -> perhaps the rest.

## Revision Order (Logic -> Sentence -> Vocabulary; Irreversible)

When polishing takes several passes, follow this order and never reverse it:

1. **Argument / logic**: paragraph order, repeated/missing main ideas, chapter transitions.
2. **Sentence structure**: split very long sentences, passive to active, move information-dense components forward.
3. **Vocabulary / typesetting**: AI-frequency terms, number/unit format, terminology/abbreviation consistency.

Why fixed: if wording is polished first (Layer 3), a Layer 1 change may delete or merge that paragraph,
wasting the work. Coarse-to-fine revision is several times more efficient.

## Sources

| Source | Core Contribution |
|------|----------|
| Neel Nanda (Google DeepMind) | Narrative principle |
| Sebastian Farquhar (DeepMind) | Five-sentence abstract formula |
| Gopen & Swan | Seven reader-expectation principles |
| Zachary Lipton | Precise wording |
| Jacob Steinhardt (UC Berkeley) | Precision |
| Ethan Perez (Anthropic) | Micro-writing techniques |
