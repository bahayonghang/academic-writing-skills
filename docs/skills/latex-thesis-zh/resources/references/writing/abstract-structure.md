# Abstract Structure Guide

An effective academic abstract contains five structural elements that together tell a complete research story. This guide defines each element, how to detect it, and what makes it strong or weak.

## Five-Element Model

### 1. Background

**Purpose**: Establish the research context — the real-world problem, knowledge gap, or motivation.

**Detection markers (EN)**: "however", "remains unclear", "limited research", "growing interest", "challenge", "gap", "despite", "little is known", "increasingly important"

**Detection markers (ZH)**: "yet", "unclear", "understudied", "growing", "challenge", "blank", "despite", "little research"

**Quality criteria**: Moves from broad context to specific gap in 1-2 sentences. A vague background restates the field name without identifying a gap.

### 2. Objective

**Purpose**: State what this specific study aims to answer or accomplish.

**Detection markers (EN)**: "this study aims", "we investigate", "the purpose of", "this paper presents", "we propose", "our goal", "in this work", "we address", "this research examines"

**Detection markers (ZH)**: "This article aims to", "This research discusses", "This article proposes", "Research purpose", "For this reason we", "This work", "This article studies"

**Quality criteria**: Specific and falsifiable. A vague objective says "we study X" without specifying what aspect or what question about X.

### 3. Methods

**Purpose**: Describe the approach, data, tools, or analytical framework used.

**Detection markers (EN)**: "we propose", "using", "dataset", "participants", "method", "approach", "framework", "model", "algorithm", "collected", "trained", "evaluated", "sample", "experiment"

**Detection markers (ZH)**: "adopt", "method", "dataset", "sample", "model", "algorithm", "framework", "experiment", "training", "evaluation"

**Quality criteria**: Names the specific technique, data source, or experimental setup. Missing methods make the abstract feel like an opinion piece.

### 4. Results

**Purpose**: Report the key findings with concrete data.

**Detection markers (EN)**: "results show", "achieved", "outperforms", "accuracy", "improved", "reduced", "found that", "demonstrates", "significant", numbers, percentages, p-values

**Detection markers (ZH)**: "results show", "reach", "better than", "accuracy", "improve", "reduce", "find", "significant", numbers

**Quality criteria**: Must contain at least one quantitative finding (number, percentage, ratio, or comparative statement with magnitude). A results section without numbers is classified as VAGUE.

### 5. Conclusion / Significance

**Purpose**: State the contribution, implications, or practical value of the findings.

**Detection markers (EN)**: "our findings suggest", "contributes to", "implications", "demonstrates that", "can be used", "enables", "provides", "advances", "potential"

**Detection markers (ZH)**: "research findings indicate", "provide for", "contribute to", "have significance for", "can be used for", "promote", "contribute"

**Quality criteria**: Goes beyond restating results — connects findings to the broader field or practice. A hollow conclusion just repeats the results in different words.

## Common Defect Patterns

| Defect | Description | Typical fix |
|--------|-------------|-------------|
| Missing background | Jumps straight to "We propose..." | Add 1 sentence on the problem context |
| Vague objective | "We study deep learning for NLP" | Specify: "We investigate whether... improves..." |
| No methods | Describes results without explaining how | Add the core technique and data source |
| Data-free results | "Our method performs well" | Add a key metric: "achieves 94.2% F1" |
| Echo conclusion | Restates results verbatim | Add implication: "enabling real-time..." |

## Word Count Guidelines

| Context | Language | Range |
|---------|----------|-------|
| Default (no venue specified) | English | 150–250 words |
| Default (no venue specified) | Chinese | 200–300 characters |
| IEEE conference | English | 150–200 words |
| ACM conference | English | 150–250 words |
| NeurIPS/ICML | English | ≤ 200 words (strict) |
| Chinese thesis (GB/T) | Chinese | 300–500 characters |

Venue-specific limits override defaults. Check catalog.md for exact requirements.

## Diagnostic Output Format

The analyzer outputs a per-element diagnosis:

```
Background:  ✅ PRESENT  — "Despite growing interest in X, the impact of Y remains unclear."
Objective:   ⚠️ VAGUE    — "This paper studies X." → Suggestion: specify the research question
Methods:     ✅ PRESENT  — "We propose a framework based on Z, evaluated on dataset W."
Results:     ❌ MISSING  — No quantitative findings detected → Add key metrics
Conclusion:  ⚠️ VAGUE    — Restates results without implications → Add practical significance
```

## Dissertation abstract skeleton (thesis model)

The above five-factor model is of **conference/journal small paper** caliber. Abstracts for Chinese degree theses (especially engineering PhDs) follow a different set of
**Skeleton Structure**: Not the five sections of Background/Objective/Methods/Results/Conclusion, but "Object Positioning → Pain Points →
The starting sentence ends with a colon → the numbered working section → the optional closing section." `analyze_abstract.py` of **`--model thesis` is the default**,
Diagnose this skeleton; `--model five` Keep the above five-element model as a backup (this skill only serves dissertations, and the five-element model is suitable for
Ph.D. abstracts will systematically misreport, for example, Results will have no value and will be MISSING, while compliant Ph.D. abstracts will always be closed).

### Skeleton sequence (macro)

```text
① 对象定位首句："X 是……" / "X 产生于……"（研究对象为主语，非方法开头）
② 痛点/挑战段："然而，……难以/挑战/瓶颈……"
③ 总起句 + 冒号收束："本文主要研究工作/创新点如下："
④ 编号工作段 (1)(2)(3)…：每段"针对……问题，提出/建立……，实验/应用表明……"
⑤ 可选收尾段：综述成果/工程应用（"优化/工程应用"类论文常见，非必需）
```

Number of paragraphs = background paragraph (1~2) + working paragraph (number) + optional closing paragraph.

### Multi-Component Relationships Within a Numbered Work Item

When one numbered work item contains two or more components, verify their actual interfaces before
choosing the narrative order:

- **Serial dependency**: Use “current constraint -> earlier component's role/output -> remaining constraint -> later component's role -> evaluation object” only when the source states that the later component consumes the earlier output or continues from a specific constraint left by it. Serving the same evaluation object does not by itself prove a serial relationship.
- **Parallel collaboration**: When components share an input, handle different objects, or merge only at the end, preserve the parallel relation and state each component's object and merge point; do not claim that “the later component repairs the earlier component.”

Component names alone do not prove causality, gains, or ablation contributions. If the source does not
provide an interface, role, or evaluation evidence, mark the information as missing; do not invent module
functions, numbers, citations, or conclusions such as “produces an improvement.”

### Relationship with the five-factor model

| Dimensions | Five-element model (`--model five`) | Dissertation skeleton (`--model thesis`, default) |
| --- | --- | --- |
| Applicable | Conference/journal papers | Chinese doctoral/master's thesis |
| Main Body | Background/Objective/Methods/Results/Conclusion Five Sections | Numbered Work Sections (1)(2)(3)… |
| Numeric value | Results No value judgment VAGUE/MISSING | Numeric value is optional (4/5 qualitative closing compliance), only check the robust statement when it appears |
| Word Count | EN 150~250 words / ZH 200~300 words | Alignment check_spec Yanshan Constant: PhD 900~1200 words / Master 500~650 words |

The word count threshold is switched by `--degree {doctor,master}` (default doctor), and `--max-chars` can override the upper bound.

### T-* Grading rule table

The diagnostic item corresponds to the research `abstract-patterns.md` number; **★ mark (≥4/5) is the default alarm, and the 2~3/5 rule is only Info**:

| Check code | Content | Level | Traceability |
| --- | --- | --- | --- |
| T-OPEN | The first sentence starts with the research object as the subject and not the method | Warning | ★A1 5/5 |
| T-PAIN | There are pain points/challenge sentences (difficult/challenge/yet/bottleneck) | Warning | ★A2 5/5 |
| T-LEAD | There is a starting sentence before the numbered paragraph and it ends with ":" | Warning | ★A4 5/5 |
| T-ENUM | The main body is (1)(2)... numbered working section, and the number of sections is consistent with the number | Warning | ★A5 5/5, D4 |
| T-VERIFY | Verification method roll call (simulation/actual measurement/production data/field application), non-empty "verification valid" | Warning | ★C2 5/5 |
| T-ABBR | The full name in Chinese and English is defined when the abbreviation first appears | Warning | ★E3 5/5 |
| T-INNOV | The occurrence of innovative expressions (innovation/first time/new method or the numbered work section itself) | Warning | web A3 school regulations |
| T-TOC-STYLE | Non-table of contents abstract / background description is not too long | Warning | web A10 soft |
| T-PROB | Each work section begins with a question-oriented phrase (only if <50% of the entire article is reported) | Info | ★B1 |
| T-VERB | Method verb specification set (propose/establish/design/construct/research/adopt) | Info | ★B4 |
| T-NUM-HEDGE | Numeric indicators with "approximate/above/range" robust expression (check only if numerical values are available) | Info | C3 2/2 |
| T-KW-FIRST | First keyword ≈ research object/process name | Info | ★D2 |
| T-VOICE | Only search "I/We/Author"; "This article/This paper" is legal | Info | web A6 |

### Chinese-English abstract consistency (`--bilingual`)

When adding `--bilingual` to thesis mode, an additional comparison is made between English Abstract and Chinese abstract:

| Check code | Content | Level | Traceability |
| --- | --- | --- | --- |
| B-ORD | First/Second/Then/Finally ↔ First/Second/Then/Finally Number and order alignment | Warning | ★F3 5/5 |
| B-NUM | Chinese and English numerical token sets are consistent | Error (inconsistent values are a flaw) | ★F1; web A9 |
| B-ENUM | The number of numbered working segments is the same | Warning | ★F1 |
| B-LEN | English abstract is missing/too short | Warning | web A9 |
| B-SEM | Sentence-by-sentence/element-by-element semantic correspondence ([LLM] lane, reported to control prompt words) | — | ★F1 |
| B-NAT | Journal-style abstract rhetoric candidates: missing field context at the opening (check the abstract type before suggesting a change), no scope limit in the final sentence, or no number, comparison, or concrete test in the full abstract ([LLM], not a determination) | Info | nature-writing N3 (community-derived) |

B-NAT adapts community-derived, Nature-leaning rhetorical heuristics from
`ref/claude-scholar/skills/nature-writing`. The source provides no article or DOI list,
sample-selection method, or citation to official Nature author guidance. Some abstract
templates share a source lineage with `ref/Research-Paper-Writing-Skills` and are already
covered by this repository's section-writing resources. B-NAT is only a candidate prompt,
not an official Nature rule, venue-compliance determination, or hard script rule.

Tense/Voice (★F2 English summary method sentences are usually present tense passive) **Not implemented here**: The deai module already has English summary area gated
Tense detection ([tense-guide-zh.md](tense-guide-zh.md) + deai_check), `--bilingual` report endnote guide deai,
Avoid dual implementation drift (deai trace does not flow into this module).

## Constraints

- Never alter the author's core claims or fabricate data
- Never add results or conclusions not present in the original text
- Preserve all citations, labels, and math environments
- Mark all modifications with brackets: [ADDED: ...] or [REVISED: ...]
