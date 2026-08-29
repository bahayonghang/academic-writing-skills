# In-depth guide to logical connection and methodology

## Paragraph-level logical connection (AXES model)

| Components | Description | Examples |
|----------|------|------|
| **A**ssertion (claim) | Clear topic sentence, stating the core point of view | "The attention mechanism can improve the effect of sequence modeling." |
| **X**ample (example) | Specific evidence or data to support the claim | "In experiments, the attention mechanism achieved 95% accuracy." |
| **E**xplanation (explanation) | Analyze why the evidence supports the claim | "This improvement stems from its ability to capture long-range dependencies." |
| **S**ignificance | Connection to a broader argument or next paragraph | "This finding informs the structure of this article." |

## Transition signal words

| Relationship Type | Chinese Signal Word | English Correspondence |
|----------|------------|----------|
| Progressive | In addition, further, more importantly | furthermore, moreover |
| Turning | However, however, contrary | however, nevertheless |
| cause and effect | therefore, hence, therefore | therefore, consequently |
| order | first, subsequently, finally | first, subsequently, finally |
| Example | for example, specifically, especially | for instance, specifically |

## Methodology in-depth checklist

- [ ] Each claim is supported by evidence (data, quotes, or logical reasoning)
- [ ] There is a good reason for the choice of method (why was this method chosen instead of another?)
- [ ] Explicit acknowledgment of study limitations
- [ ] Clearly state assumptions
- [ ] Reproducibility details are sufficient (parameters, data sets, evaluation metrics)

## FAQ

| Problem type | Manifestation | Fix method |
|----------|------|----------|
| Logical gaps | Lack of cohesion between paragraphs | Add transitional sentences to illustrate the relationship between paragraphs |
| Unsubstantiated claims | Assertions lacking supporting evidence | Supplementary quotes, data or reasoning |
| Shallow methodology | "This article uses X" but no reason | Explain why X is suitable for this problem |
| Implicit assumptions | Unstated preconditions | Explicitly stated assumptions |

## Chapter Guide

| Chapters | Key points of logical connection | Key points of methodological depth |
|------|--------------|----------------|
| Introduction | Background → bottleneck/blank → scientific problem → smooth connection of contribution | Demonstrate research significance and defensible questions |
| Related work | Grouped by topic, explicit comparison | Positioning the relationship with previous work |
| Methods | Progression between chapters and modules | Demonstrate the motivation, design and technical advantages of each module |
| Experiment | Setup→Results→Analysis→Discussion→Limitations process | Explain the selection of evaluation indicators and the result mechanism |
| Discussion | The connection between discovery → revelation → limitation | Acknowledging research boundaries |

When a chapter-level rewriting plan is needed, read [`thesis-writing-guide.md`](thesis-writing-guide.md) as a supplement, and take "research background -> technical bottlenecks/research gaps -> scientific issues -> methods of this article/chapter work -> experimental evidence -> contribution closure -> limitations and prospects" as the main line.

## Output format

```latex
% 逻辑衔接（第45行）[Severity: Major] [Priority: P1]: 段落间逻辑断层
% 问题：从问题描述直接跳转到解决方案，缺乏过渡
% 原文：数据存在噪声。本文提出一种滤波方法。
% 修改后：数据存在噪声，这对后续分析造成干扰。因此，本文提出一种滤波方法以解决该问题。
% 理由：添加因果过渡，连接问题与解决方案

% 方法论深度（第78行）[Severity: Major] [Priority: P1]: 方法选择缺乏论证
% 问题：方法选择未说明理由
% 原文：本文采用ResNet作为骨干网络。
% 修改后：本文采用ResNet作为骨干网络，其残差连接结构能有效缓解梯度消失问题，且在特征提取任务中表现优异。
% 理由：用技术原理论证架构选择
```

## Best Practices

Reference [Elsevier](https://elsevier.blog/logical-academic-writing/), [Proof-Reading-Service](https://www.proof-reading-service.com/blogs/academic-publishing/a-guide-to-creating-clear-and-well-structured-scholarly-arguments):

1. **One paragraph, one topic**: Each paragraph focuses on a single core idea
2. **Topic sentence first**: The beginning of the paragraph states the proposition of this paragraph.
3. **Complete evidence chain**: Each claim needs support (data, references or logic)
4. **Explicit Transition**: Use signal words to indicate paragraph relationships
5. **Argument rather than description**: Explain "why" rather than just state "what"

## Completeness of the blurb after the title (S1)

**Rule**: Except for special sections such as the abstract, table of contents, references, acknowledgments, and appendices, each chapter, each section, each subsection, and the four-level headings responsible for the function of developing arguments should first give an introduction after the title, and then enter the list, chart, formula, or next-level heading.

**Minimum functions of the introduction**:
- Indicate what will be discussed at this level;
- Explain why it is discussed here;
- Explain the relationship with the above;
- Preview the unfolding sequence within this level.

**Detection Heuristics** (Script Automation):
- Scan `\chapter`, `\section`, `\subsection`, `\subsubsection`, `\paragraph` and other header commands;
- If the first thing that appears after the title is a list, chart, formula environment, next-level title, or there is no visible text, it is determined that the introduction is missing;
- If only a very short sentence appears after the title and there are no introductory signals such as "this chapter/this section/below/first", then marking it as an introduction may be too weak.

**Revision suggestions**: Add a complete introduction after the title to define the research object, writing purpose and writing route at this level, instead of directly piling up the content.

---

## Literature review quality verification (A1-A4)

Make sure relevant work sections are comprehensive analyzes rather than simple lists.

### A1: Topic clustering (author/year listing is prohibited)

**Rule**: Related work should be organized by research topic rather than by author or year of publication. Three or more consecutive sentences that follow the pattern "The author (year) proposed/introduced..." are regarded as lists.

**Detection Heuristics** (Script Automation):
- Regular: `^.*?[（(]\d{4}[)）].*?(?:提出|引入|设计|开发|采用|构建|建立)`
- Threshold: 3 or more consecutive matches → Major/P1

| Mode | Judgment |
|------|------|
| "Zhang San (2019) proposed X. Li Si (2020) introduced Y. Wang Wu (2021) designed Z." | Listing mode (mark) |
| "Attention-based methods have experienced continuous evolution... Zhang San (2019) and Li Si (2020) explored it from different angles... However, Wang Wu (2021) pointed out..." | Topic Synthesis (Passed) |

**Correction**: Reorganized into thematic groups and conducted critical comparative analysis within the groups.

### A2: Theme groups are followed by critical analysis (LLM judgment)

**Rule**: Each topic group should be followed by a comprehensive review that compares or evaluates the cited literature - not just lists. Look for evaluative language: "however," "despite," "common shortcomings," "in comparison."

*This rule requires LLM judgment, and regularity cannot be reliably detected. *

### A3: Derivation of research gaps at the end of related work

**Rule**: The last paragraph of related work must contain a clear description of the research gap that provides motivation for this study.

**Detection Heuristics** (Script Automation):
- Scan the last 10 lines of chapter `related`
- Keywords: `研究空白|不足|然而.*?尚未|仍然.*?(?:挑战|困难)|有待|缺乏|尚未解决|亟待|亟需|鲜有研究|未能充分`
- No match → Major/P1

### A4: Funnel type citation density (LLM judgment)

**Rule**: The citation density should be in a funnel shape of wide→narrow→fine: first introduce the general field, gradually narrow down to specific sub-problems, and finally focus on the most relevant previous work. A flat or inverted funnel suggests poor narrative structure.

*This rule requires LLM judgment to evaluate narrative arcs. *

---

## Cross-chapter logic chain closure check (C3)

**Rule**: Statements of contribution in the introduction must be clearly echoed in the conclusion. For example, if it is stated in the introduction that "this article proposes

**Detection heuristic** (script automation, full document mode is enabled by default; `--cross-section` is the compatibility switch):
- Extract contribution keywords from `introduction` chapter
- Extract response keywords from `conclusion` chapter
- If the introduction has a contribution statement but the conclusion has no responsive language → Major/P1 (observation marked `[Script]`)

| Introductory Statement | Desired Concluding Response |
|----------|--------------|
| "This article proposes a novel attention mechanism." | "Experiments show that the proposed attention mechanism achieves..." |
| "The main contributions of this article are: (1)..." | "The experiment verified the contribution (1)..." |

**NOTE**: This check is heuristic in nature and the results are presented as observations, not deterministic judgments.

---

## Motor red line closure diagnosis (optional switch: `--motivation-thread`)

**Rule**: A strong dissertation follows a single "problem → solution" thread. Every promise made in the introduction ("This thesis proposes X to solve Y") should be **validated** in the experiments or results and **answered** in the discussion or conclusion. This diagnostic exposes breaks in that thread.

**How to run** (Additional type - without this switch, the logic module output is exactly the same as the original):

```bash
uv run python scripts/analyze_logic.py main.tex --motivation-thread
```

**Output** (read only, all marked `[Script]`):

- **Commitment Mapping**: Each promise in the introduction (hit `CONTRIBUTION_KEYWORDS_ZH`) → the line with the highest word overlap in the experiment/results; `[未找到证据]` means that the promise has never been verified.
- **Closed mapping**: Each claim in the introduction → the line with the highest word overlap in the discussion/conclusion; `[未闭合]` means that the claim has never been answered.
- **Wandering evidence**: A result line that carries a numerical conclusion but cannot be traced back to any of the introductory promises (possibly scope creep).

**Mechanism**: keyword + content token overlap (English word ≥4 characters + Chinese character tuple). It is a navigational aid rather than a conclusive statement—reports explicitly indicate possible false positives and require human review. If a promise is shown as unmatched simply because the results section has been worded differently, it should be regarded as a prompt to "make up for an explicit response" rather than a hard error.

| Mode | Judgment |
|------|------|
| Introduction "This article proposes sparse attention to reduce latency" → Result "Latency reduced by 42%" | Matched (passed) |
| Introduction promises interpretability, but no results section mentions | `[未找到证据]` (tag) |
| Introduction claims never echoed in discussion/conclusion | `[未闭合]` (tag) |

---

## Chapter writing main line reinforcement

When a user requests to "rewrite the introduction/method chapter/experimental discussion/summary and outlook", first determine whether this is a main writing problem or a script diagnosis problem. If you need to write a plan, keep the script diagnosis results and output as follows:

1. Chapter objective: The scientific question or technical question to be answered in this chapter.
2. Paragraph roles: background, bottlenecks, gaps, methods, strengths, evidence, limitations, prospects.
3. Evidence mapping: Each contribution or innovation point corresponds to the methods chapter, experimental results or conclusion response.
4. Rewrite blueprint: Rewrite at the paragraph level only when the user explicitly requests it, and no new references, data or experimental conclusions will be added.

---

## Paragraph-Arc Observations (Optional Flag: `--paragraph-arc`)

When the issue concerns a first-sentence lead, last-sentence close, adjacent-paragraph interface, or
a one-sentence/enumeration paragraph, run:

```bash
uv run python scripts/analyze_logic.py main.tex --paragraph-arc
```

| Code | Observation surface | Boundary |
| --- | --- | --- |
| `P-ARC-LEAD` | First-sentence lead shape | Does not judge whether the point is valid |
| `P-ARC-CLOSE` | Retrospective or prospective last-sentence shape | A missing marker does not imply an incomplete paragraph |
| `P-ARC-LINK` | Explicit linkage or endpoint lexical overlap | Never crosses a heading, equation, figure, table, algorithm, or list |
| `P-ARC-FLAT` | One sentence or pure author enumeration | A1 remains the owner of author enumeration in related work |

This branch is off by default. Findings are `[Script]` observations and always carry
`Meaning-Check: NEEDS-LLM`. See
[`paragraph-arc-zh.md`](paragraph-arc-zh.md) for the complete criteria, paragraph patterns, original
examples, and AXES boundary.
