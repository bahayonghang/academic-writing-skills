# Module: Logical connection and methodological depth
**Trigger words**: logic, coherence, logic, connection, methodology, methodology, argument, argument

**Script Usage**:
```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py main.typ
uv run python $SKILL_DIR/scripts/analyze_logic.py main.typ --section method
```

> `--section`Accepts canonical keys and synonyms (`methods`/`methodology`/`approach` → `method`）。

**Goal**: Ensure logical flow between paragraphs and strengthen methodological rigor.

**Key inspection areas**:

**1. Paragraph-level logical connection (AXES model)**:
|components|illustrate|Example|
|----------|------|------|
|**A**ssertion (assertion)|A clear topic sentence that states the core idea|"The attention mechanism can improve the effect of sequence modeling."|
|**X**ample (example)|Specific evidence or data to support the claim|"In experiments, the attention mechanism achieved 95% accuracy."|
|**E**xplanation (explanation)|Analyze why the evidence supports the claim|"This improvement comes from its ability to capture long-range dependencies."|
|**S**ignificance (meaning)|Connection to wider argument or next paragraph|"This discovery provides a basis for the architectural design of this article."|

**2. Transition signal words**:
|Relationship type|Chinese signal words|English correspondence|
|----------|------------|----------|
|progressively|In addition, further and more importantly|furthermore, moreover|
|turning point|However, but, on the contrary|however, nevertheless|
|cause and effect|Therefore, it can be seen that therefore|therefore, consequently|
|order|first, subsequently, finally|first, subsequently, finally|
|Example|For example, specifically, especially|for instance, specifically|

**3. Methodological in-depth checklist**:
- [ ] Each claim is supported by evidence (data, quotes, or logical reasoning)
- [ ] There are good reasons for the method chosen (why this method rather than another?)
- [ ] Explicit acknowledgment of research limitations
- [ ] Clearly state assumptions
- [ ] Reproducibility details are sufficient (parameters, data sets, evaluation metrics)

**4. Frequently Asked Questions**:
|Question type|Performance|Correction method|
|----------|------|----------|
|logical gap|Lack of cohesion between paragraphs|Add transitional sentences to illustrate paragraph relationships|
|Unfounded claim|Assertion lacks supporting evidence|Supplementary quotes, data or reasoning|
|Shallow methodology|"This article adopts X" but there is no reason|Explain why X is suitable for this problem|
|implicit assumptions|Prerequisites not stated|Explicitly state assumptions|

**Output format**:
```typst
// 逻辑衔接（第45行）[Severity: Major] [Priority: P1]: 段落间逻辑断层
// 问题：从问题描述直接跳转到解决方案，缺乏过渡
// 原文：数据存在噪声。本文提出一种滤波方法。
// 修改后：数据存在噪声，这对后续分析造成干扰。因此，本文提出一种滤波方法以解决该问题。
// 理由：添加因果过渡，连接问题与解决方案

// 方法论深度（第78行）[Severity: Major] [Priority: P1]: 方法选择缺乏论证
// 问题：方法选择未说明理由
// 原文：本文采用ResNet作为骨干网络。
// 修改后：本文采用ResNet作为骨干网络，其残差连接结构能有效缓解梯度消失问题，且在特征提取任务中表现优异。
// 理由：用技术原理论证架构选择
```

**Chapter Guide**:
|chapter|Key points of logical connection|Methodological depth focus|
|------|--------------|----------------|
|Abstract|The smooth connection of purpose→method→result→conclusion|Highlight core contributions|
|Introduction|Smooth transition from question → blank → contribution|Demonstrate research significance|
|Related Work|Group by topic, explicit comparison|The relationship between positioning and previous work|
|Methods|Logical progression between steps|Justify every design choice|
|Experiments|Settings→Results→Analysis Process|Explain evaluation metric selection|
|Discussion|The connection of discovery → enlightenment → limitation|Recognize research boundaries|

**Best Practice**:
1. **One paragraph, one topic**: Each paragraph focuses on a single core idea
2. **Topic sentence first**: The first paragraph states the proposition of this paragraph
3. **Complete evidence chain**: Each claim needs support (data, references or logic)
4. **Explicit Transition**: Use signal words to indicate paragraph relationships
5. **Argument rather than description**: explain "why" rather than just state "what"

Reference: [WRITING_PHILOSOPHY.md](../WRITING_PHILOSOPHY.md)

---

## Literature Review Quality Validation (A1-A4)

> Authoritative rules are defined in `latex-paper-en/references/modules/LOGIC.md`. This section mirrors them for Typst usage.

### A1: Thematic Clustering (Not Author/Year Enumeration)

Related Work must organize references by research theme. Detecting 3+ consecutive sentences following "Author (Year) proposed..." signals enumeration → Major/P1.

**Script detection**:`analyze_logic.py`checks for consecutive author/year enumeration patterns in the`related`section.

### A2: Critical Analysis After Each Theme Cluster (LLM-judgment)

Each thematic group must end with a synthesis sentence that compares or evaluates. *Requires LLM judgment.*

### A3: Research Gap Derivation

The final paragraph of Related Work must contain explicit research gap language. The script scans the last 10 lines for gap keywords (`gap|limitation|remains|lack|overlooked|under-explored`). No match → Major/P1.

### A4: Funnel-Shaped Citation Density (LLM-judgment)

Citation density should follow broad→focused→specific. *Requires LLM judgment.*

---

## Cross-Section Logic Chain Closure (C3)

Introduction contribution claims must be answered in the Conclusion. The script extracts contribution keywords from`introduction`and answer keywords from`conclusion`. If intro has claims but conclusion has zero answer language → Major/P1 (`[Script]`observation).

Activate with`--cross-section`flag or full-document analysis (no`--section`).

---

## Motivation Red-Thread Closure (opt-in: `--motivation-thread`)

A strong paper is one problem→solution arc: every Introduction promise should be *tested* in Results/Experiments and *resolved* in Discussion/Conclusion. This opt-in diagnostic is additive — without the flag the normal logic output is unchanged.

```bash
uv run python scripts/analyze_logic.py main.typ --motivation-thread
```

Produces (read-only, all`[Script]`, comment prefix`//`):

- **Promise Map** — each Introduction promise → best-overlapping Results/Experiment line; `[NO EVIDENCE FOUND]` = promise never tested.
- **Closure Map** — each Introduction claim → best-overlapping Discussion/Conclusion line; `[UNCLOSED]` = claim never resolved.
- **Evidence-without-promise** — numeric Results lines that trace to no Introduction promise.

Mechanism: keyword + content-token overlap (English words ≥4 chars plus CJK bigrams), so it works on English and Chinese Typst papers alike. It is a heuristic navigation aid, not a verdict — the report says so and asks for manual verification.

