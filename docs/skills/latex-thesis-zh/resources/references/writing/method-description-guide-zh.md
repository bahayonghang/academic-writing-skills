# Method Module Description and Interface Guide

Use this guide for method chapters in Chinese engineering theses, especially method chains with
serial, parallel, supervisory, or feedback relationships. It is the module-level narrative contract.
For the chapter skeleton, read
[`method-chapter-guide-zh.md`](method-chapter-guide-zh.md); for paragraph coherence, read
[`logic-coherence.md`](logic-coherence.md); for the thesis-wide mainline, read
[`thesis-writing-guide.md`](thesis-writing-guide.md).

Run the candidate check first, then use this guide for semantic review:

```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py document.tex --method-narrative --section 〈章名〉
```

`--section` selects exactly one chapter per run. Script results are candidates.
`Meaning-Check: NEEDS-LLM` means the thesis facts, equations, and experimental design still require
contextual review.

## 1. Completion Criteria and Rule Levels

A method description is closed when readers can answer five questions without reconstructing the
author's intent:

1. Which unresolved constraint makes the current module necessary?
2. Why does the selected structure or operator fit that constraint?
3. How do data, state, or supervision signals move from input to output?
4. Is each claimed benefit supported by definition, mechanism, or experimental evidence?
5. How does the output enter the next module, or which remaining constraint passes downstream?

| Rule level | Effect of omission | Review mapping |
| --- | --- | --- |
| Required | The method contract is open, irreproducible, or liable to relationship misreading | Major |
| Recommended | Facts may remain intact, but comprehension cost rises substantially | Minor (recommended repair) |
| Optional | Depends on method scale, disciplinary convention, or supervisor requirements | Info |

## 2. State the Overall Data Flow First

Before local equations, a multi-module method section states the shared input, each module's output,
execution order, training/inference differences, and the module that produces the final output. Prose,
the framework figure, equations, and pseudocode must express the same data flow.

```text
问题与数据契约
  -> 总体数据流和模块分工
  -> 模块 A：解决基础约束
  -> 模块 B：处理 A 的输出或剩余约束
  -> 模块 C：完成融合、校准、决策或监督
  -> 训练/推理流程与最终输出
  -> 实验验证对象
```

Completion criterion: the overview alone is sufficient to draw module nodes and directed interface
edges and to identify every training/inference difference.

## 3. Six-Role Contract for Each Module

Every core module covers six roles. Roles may be combined into natural paragraphs; fixed sentence
templates are unnecessary.

| Role | Required content | Review question |
| --- | --- | --- |
| Current constraint | What the upstream result still lacks, or which property the raw data has | Why can it not proceed directly? |
| Required capability | What capability removes the constraint | Does it require alignment, filtering, fusion, calibration, or feedback? |
| Design choice | How the chosen mechanism provides that capability | Why this structure or operator? |
| Processing | Which key transformations act on the input | What are the computation order, object changes, and state updates? |
| Output object | What the module produces exactly | What are its name, shape, semantics, and valid range? |
| Downstream interface | How the next module uses the output, or what remains unresolved | What relationship connects the modules? |

Use the following skeleton to check role coverage, then rewrite it as natural prose grounded in the
thesis context:

```text
由于〈当前输入/上游输出〉仍存在〈约束〉，后续〈任务〉不能直接进行。
为获得〈所需能力〉，本节采用〈设计〉；其中〈机制〉使其能够〈机制级作用〉。
给定〈输入〉，模型依次执行〈关键变换〉并得到〈输出〉。
该输出作为〈下一模块的输入/监督/约束〉；但〈剩余问题〉仍需由下一模块处理。
```

For a standard method, explain how it is applied to the current problem and what differs from the
standard version. A choice likely to be challenged needs the minimum necessary argument: purpose,
applicability, and verifiable support.

## 4. Fill Every Interface Edge

Every adjacent module pair must identify the upstream product, connecting transformation, and
downstream use. Fill the interface table before restructuring prose:

| Upstream module | Upstream product | Connection type | Intermediate transformation | Downstream use |
| --- | --- | --- | --- | --- |
| A | `z_A` | Serial data | Alignment/projection | Direct input to B |
| B | Candidate set | Calibration/selection | Threshold and budget filtering | Supervision samples for C |

| Connection type | Criterion | What to state |
| --- | --- | --- |
| Serial data | A's output directly becomes B's input | Whether name, shape, and semantics stay the same or change |
| Parallel representation | A and B share input and extract representations separately | Where and by which rule the representations fuse |
| Supervision/target | A produces labels, intervals, weights, losses, or constraints | How the signal enters B's objective |
| Calibration/selection | A produces candidates and B admits or ranks them | Boundaries among candidates, training samples, and final output |
| Feedback/control | A downstream evaluation updates an upstream object | Feedback quantity, update target, and stopping condition |
| Remaining constraint | A resolves part of the problem but exposes another limit | Use the limit to motivate B as a technical progression |

When no direct data dependency exists, apply M-NONDIRECT by ruling out the most likely mistaken
interpretation.

```text
B 不使用 A 的预测结果作为条件；二者共享同一输入语义，并通过 C 构造的监督关系相接。
```

Completion criterion: every table row has equivalent evidence in prose, a figure, or pseudocode, and
candidates, supervision objects, and final outputs remain distinct.

## 5. Embed Equations in the Argument

Each key equation forms a purpose -> equation -> explanation -> downstream-use loop:

```text
公式前：说明为什么需要该计算、输入对象是什么
公式：给出变换、目标或约束
公式后：解释新符号、输出语义及其下游用途
```

- Give external semantics when tensors, sets, time windows, masks, and labels first appear; explain internal transposes or projections separately.
- Keep equation order aligned with computation order; explicitly state any reordering made for derivation.
- “式中” completes only symbol glossing; also state the constraint addressed, object produced, and downstream consumer.
- Use the overview figure for global flow and module figures for local transformations; cite important edges instead of writing only “as shown in the figure.”
- Keep pseudocode inputs, updated/frozen objects, loop order, stopping conditions, and outputs consistent with the prose.

## 6. Match Benefit Claims to Evidence Strength

| Claim type | Required evidence | Compliant example |
| --- | --- | --- |
| Definitional fact | Equation or algorithm definition | “When the mask is zero, the conditional branch does not participate in fusion.” |
| Mechanism-level effect | Structural, complexity, or logical derivation | “The fallback path keeps data flow closed when the condition is absent.” |
| Empirical performance | Experiment, ablation, or reliable citation | “The module improves prediction accuracy.” |
| Causal attribution | Discriminating experiment or theoretical proof | “The performance gain mainly comes from this module.” |

Classify the claim first, then calibrate wording through
[`over-claim-guard.md`](over-claim-guard.md). Words such as “benefits,” “enhances,” “improves,” and
“effectively solves” do not replace evidence. With design support only, prefer “is used to,” “enables,”
“guarantees by definition,” or “provides ... for the next stage.” When evidence cannot distinguish
among mechanisms, preserve the observation and mark the mechanism as undetermined.

## 7. Let Headings Navigate

Independent technical units may retain `\subsection`, `\subsubsection`, or `\paragraph`. Headings
navigate. The prohibited pattern is using “this module is mainly used to ...” announcements in place
of causal and interface transitions, not inline headings themselves.

The following are valid boundary cases and do not trigger a problem merely because of heading form:

- inline headings that group method categories in English or Typst Related Work;
- emphasized headings that introduce a set of observations in a Typst experiment analysis;
- `\paragraph{核心结论概括}` used to summarize results in a Chinese experiment section.

Merge a “module” into an adjacent natural paragraph when it has only one or two defining sentences
and no independent input, output, or derivation.

## 8. Negative and Positive Examples

### Failing: Heading Announcements

```text
动态编码模块。本模块用于提取动态特征。
扩散模块。本模块用于生成样本。
筛选模块。本模块用于筛选高质量样本。
```

This is a responsibility list without problem origin, design rationale, input/output, or module
connections.

### Baseline: Data Flow without a Reason for Progression

```text
A 输出动态特征，B 以该特征为条件生成候选，C 对候选进行筛选。
```

The sentence gives the order but does not explain why B is needed, why candidates cannot be used
directly, or what admission criterion C applies.

### Recommended: Constraint-Driven Continuous Narrative

```text
A 得到的基础表征仍受原始样本覆盖范围限制，不能补充稀疏区域。为扩展该区域的候选支撑，
B 复用相同输入语义，并以 A 之外的指定条件生成候选。生成条件不等同于可信监督，因此候选
不能直接进入学生训练。C 随后利用独立校准对象将候选转换为带区间和权重的监督样本，最终
由学生模型输出任务结果。
```

Remaining constraints and supervision interfaces connect adjacent modules while ruling out a false
data-dependency interpretation.

## 9. Review and Rewrite Procedure

1. Lock factual boundaries: protect symbols, equations, citations, numbers, data splits, and established experimental conclusions.
2. Draw the module graph: record each node's input, process, output, training state, and failure/fallback path.
3. Fill the adjacent-interface table: determine connection type, transformation, and downstream use edge by edge.
4. Rewrite the overall data flow and module transitions first, module-internal sentences second, and headings last.
5. Check every equation for a closed purpose -> equation -> explanation -> downstream-use loop.
6. Classify benefits as definitional facts, mechanism effects, empirical performance, or causal attribution, then remove unsupported escalation.
7. Read only the opening and closing paragraph of each module; stop when the whole method chain and every interface edge can be restated.

## 10. Check Mapping

| ID | Lane | Script trigger or artifact | Severity | Guide section |
| --- | --- | --- | --- | --- |
| M-HEADING | Script candidate + LLM review | Inline-heading groups use responsibility announcements instead of transitions | Minor/P2 | 7 |
| M-SEQWORD | Script candidate + LLM review | A subsection opening gives layout order without a cause or constraint | Info/P3 | 4, 7 |
| M-EQUATION | Script candidate + LLM review | Visible prose after a numbered equation lacks a gloss entry point | Minor/P2 | 5 |
| M-EDGETABLE | Script skeleton + LLM completion | Emits a subsection list and blank edge-interface table; not a finding | Unscored | 4, 9 |

The script only filters candidates. Review M-MOTIVE, M-RATIONALE, M-IO, M-EDGE, M-NONDIRECT, the
complete M-EQUATION contract, M-EVIDENCE, M-REPRO, and M-CLOSURE module by module and edge by edge.

## 11. Reproducibility Information and Sources

At minimum, state input provenance and time semantics, preprocessing and data splits, how key
parameters are chosen, training order, updated/frozen objects, random procedures, stopping conditions,
failure/fallback paths, and output type, range, unit, and consumer. Standard methods may cite their
original source; additions and variants require an explicit description.

- Gopen and Swan, [The Science of Scientific Writing](https://www.americanscientist.org/blog/the-long-view/the-science-of-scientific-writing): use the topic position for old information and the stress position for new information.
- MIT EECS Communication Lab, [Paper: Methods (EE)](https://mitcommlab.mit.edu/eecs/commkit/journal-article-methods-ee/): provide the minimum necessary rationale for method choices; headings support logical flow but do not replace transitions.
- MIT MechE Communication Lab, [Journal Article: Methods](https://mitcommlab.mit.edu/meche/commkit/journal-article-methods/): emphasize how and why the method is applied to the current problem.
- IEEE Author Center, [Structure Your Article](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/): method detail should support reproduction, trust, and extension.
- Nature, [Formatting Guide](https://www.nature.com/nature/for-authors/formatting-guide): keep methods concise while retaining what readers need to explain and reproduce results.
- PLOS ONE, [Submission Guidelines](https://journals.plos.org/plosone/s/submission-guidelines): give technical details for statistical and analytical methods, including software, preprocessing, and missing-data handling.
