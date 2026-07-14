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
| **Why it is credible** | Rigorous experimental evidence | Sufficient baseline comparisons and ablation studies |
| **Why it matters** | Why readers should care | Connection to a recognized problem in the field |

**If you cannot state the contribution in one sentence, the thesis is not yet whole.**

## Five-Sentence Abstract Formula

(Adapted from Sebastian Farquhar, DeepMind)

1. Core result (“This thesis proposes...”, “This thesis demonstrates...”)
2. Why the problem is difficult and important
3. Method, including key terms for searchability
4. Experimental evidence
5. Most important quantitative result

**Delete** generic openings such as “With the rapid development of deep learning...”

## Seven Reader-Expectation Principles

(Adapted from Gopen & Swan)

| # | Principle | Rule | Example |
|---|------|------|------|
| 1 | **Subject-verb proximity** | Keep subject and predicate close | ❌ “The method proposed in this thesis based on..., achieved” -> ✅ “The proposed method achieved...” |
| 2 | **Stress at the end** | Put sentence focus last | ✅ “Through attention, accuracy increased by **15%**” |
| 3 | **Old information first** | Known information first, new information later | ✅ “Based on the analysis above, this thesis proposes...” |
| 4 | **One idea per paragraph** | One point in each paragraph | Split multi-point paragraphs |
| 5 | **Use verbs for actions** | Avoid nominalization | ❌ “performed an analysis” -> ✅ “analyzed” |
| 6 | **Context before display** | Explain before presenting a formula | State the meaning before the formula |
| 7 | **Explicit transitions** | Use signals between paragraphs | “therefore,” “however,” “in addition” |

## Precise Wording

(Adapted from Zachary Lipton)

### Be Specific
- ❌ “performance” -> ✅ “accuracy,” “inference latency”
- ❌ “significant” -> ✅ “statistically significant (p < 0.05)” or delete it

### Remove Ambiguity
- ❌ “may help improve” -> ✅ “accuracy increased by 3.2%”

### Avoid Empty Phrases
Delete: obviously, undoubtedly, as everyone knows, undeniably

## Precision First

(Adapted from Jacob Steinhardt, UC Berkeley)

- **Terminology consistency**: use one term for one concept throughout
- **Explicit assumptions**: list every assumption before a theorem
- **Intuition + rigor**: pair intuitive explanation with formal proof
- **Define before use**: define every symbol and term before first use

## Micro-Writing Techniques

(Adapted from Ethan Perez, Anthropic)

- [ ] **Avoid vague reference**: ❌ “This shows...” -> ✅ “The experiment shows...”
- [ ] **Move verbs forward**: keep the predicate near the sentence opening
- [ ] **Delete fillers**: actually, to some extent, quite, relatively, basically
- [ ] **Active voice**: ❌ “The method was applied to” -> ✅ “This thesis applies the method to”
- [ ] **Quantify**: ❌ “large improvement” -> ✅ “improved by 12.3%”

## Section-Specific Guide

| Section | Suggested Length | Core Requirement |
|------|----------|----------|
| **Abstract** | 300-500 Chinese characters | Five-sentence formula; remove generic opening |
| **Introduction** | 3-5 pages | Background -> problem -> contribution list -> organization |
| **Literature review** | 5-10 pages | Group by theme; discuss each work's contribution and limitation; no more than 2 parallel citations in one sentence |
| **Methods** | As needed | Ensure reproducibility; list every hyperparameter |
| **Experiments** | Main body | State which claim each experiment validates; include error analysis |
| **Conclusion and outlook** | 1-2 pages | Answer research question; actionable future work |

### Introduction Must Include:
- Clear research-question statement
- 2-4 contributions, each no more than 1-2 lines
- Brief method overview
- Chapter organization
- Citation integration: every cited work must include a brief description of its contribution, method, or limitation; never stack 3 or more citations in one sentence without analysis (see guide.md category 6)

### Experiments Must Include:
- Specific claim validated by each experiment
- Error analysis (standard deviation vs standard error)
- Hyperparameter search range
- Computing resources (GPU model, total duration)

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
