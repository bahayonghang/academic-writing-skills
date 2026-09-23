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

The opening paragraph of a module should directly state its inputs, function, or unresolved interfaces, rather than re-listing all research challenges; for paragraph roles and deduplication rules across levels, see [`paragraph-roles-zh.md`](paragraph-roles-zh.md).

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
- Explain symbols, key mechanisms, and boundary conditions after equations, without translating every operator into words in sequence (see [`paragraph-roles-zh.md`](paragraph-roles-zh.md)).

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

Document-expression labels are in the final section. They are not rows in the table above, and the script does not emit them.

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

## 12. Method-narrative expression constraints (LLM only)

This section defines eight document-check labels. The judgment belongs only to the LLM. The labels are not script codes, and they do not extend the existing heading, sequence-word, equation-entry, or interface-table checks. This section keeps no branch that would later become a script.

### M-CODLANG

Scope: a method paragraph describes a tensor transform with programming terms, such as swapping axes, copying a dimension, or Concat.
Bad example: after swapping axes along the batch dimension, Concat the two feature paths.
Revision example: swap the time axis with the feature axis, then concatenate the two feature paths along the feature dimension.
Risk: the reader sees an implementation call and not the mathematical map.
Owner: LLM only. Severity Major, priority P1.

### M-FIGTEXT

Scope: inside one subsection, an operation name in the body does not match the architecture-figure label. The reading uses that figure's label.
Bad example: the figure says “time-step mapping” while the body says “step mapping”.
Revision example: the body uses “time-step mapping”.
Risk: one operation has two names. A mismatch on a model name or a protected term is reported and is not silently renamed.
Owner: LLM only. Severity Minor, priority P2.

### M-FORMDUPE

Scope: the body restates, in natural language, a computation the formula already states. That is semantic restatement.
Bad example: the formula writes the concatenation, and the body again says that marker g and marker E are concatenated to form H.
Revision example: keep the formula. The gloss sentence explains only a new bracket notation and does not narrate the concatenation again.
Risk: the same relation is read twice, and a symbol definition that exists only in the prose may be deleted.
Owner: LLM only. Severity Minor, priority P2.
PR-EQ-NARR only locates operator-by-operator narration. The two are not the same defect.

### M-SEMICOLON

Scope: a method paragraph joins two or more independent propositions with semicolons. A semicolon that separates same-level definitions inside a gloss block may stay.
Bad example: module A emits the state; module B reads that state and updates the weights.
Revision example: module A emits the state. Module B reads that state and updates the weights.
Risk: the semicolon hides the proposition boundary. A split must not add a cause the source does not state.
Owner: LLM only. Severity Minor, priority P2.
Do not edit the mathematics.

### N-ISOLATE

Scope: a method paragraph embeds a concrete hyperparameter assignment that belongs to the experiment configuration.
Bad example: training uses p = 0.5.
Revision example: training keeps an observation with probability p. The value of p is written in the experiment-setting paragraph.
Risk: the method paragraph mixes how a quantity is used with which number is used.
Owner: LLM only. Severity Minor, priority P2.
Together with M-REPRO: do not delete information required to reproduce a result. First check whether the value belongs in another paragraph. Change the method sentence to the symbol only after the experiment-setting paragraph carries the value.

### M-DETAILINV

Scope: an implementation enumeration that is not required to understand the mathematical role, such as a feature-engineering list, a probability-branch list, or a metadata-field list.
Bad example: the input is enumerated from first differences, second differences, and three pooled statistics.
Revision example: a feature map extracts the window statistics.
Risk: the method paragraph becomes a code comment.
Owner: LLM only. Severity Minor, priority P2.
If that enumeration is the only definition of the map, or if reproduction needs it, move it to an implementation note or the experiment paragraph. Do not delete it outright.

### M-TERMREG

Scope: colloquial or engineering wording in a method paragraph, such as “configure”, “piece together”, or “hard condition”, when the manuscript already has an academic wording.
Bad example: piece the two state paths together into the input.
Revision example: combine the two state paths into the input.
Risk: register drift, not a new technical fact.
Owner: LLM only. Severity Minor, priority P2.
Do not replace a protected term or a model name.

### M-REDUNDANT

Scope: the opening repeats the previous transition, a long sentence after a formula restates the design intent, or a paraphrase restates the formula.
Bad example: the previous section already said the drift must be suppressed. This section likewise builds the update in order to suppress the drift.
Revision example: this section states the state update and passes the updated state to the next module.
Risk: the reader reads the same motive again.
Owner: LLM only. Severity Minor, priority P2.
Do not delete the only interface or the only number. Replacing a word and repeating the claim is not deduplication.

### Suggestion blocks

```latex
% 方法叙述（合成）[Severity: Major] [Priority: P1]: [LLM] M-CODLANG 张量操作写成了编程术语
% 问题：方法段用编程术语描述张量变换
% 原文：沿批量维交换轴后 Concat 两路特征。
% 修改后：交换时间轴与特征轴，再按特征维拼接两路特征。
% 理由：读者需要数学映射。本标签只由 LLM 判断。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] M-FIGTEXT 正文与架构图标注不一致
% 问题：图标注写“时间步映射”，正文写“时步映射”
% 原文：时步映射把窗口映射到隐变量。
% 修改后：时间步映射把窗口映射到隐变量。
% 理由：同一操作只保留图上的名字。模型名与受保护术语只报告，不改名。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] M-FORMDUPE 正文重述了公式已有的计算
% 问题：公式已经给出拼接，正文又写了一遍
% 原文：将标记 g 与标记 E 拼接得到 H。
% 修改后：其中 $[\cdot;\cdot]$ 表示沿标记维拼接。
% 理由：这是语义复述。PR-EQ-NARR 只定位逐算子翻译，二者不是同一缺陷。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] M-SEMICOLON 分号连接了独立命题
% 问题：两个主谓结构被分号串在一起
% 原文：模块 A 输出状态；模块 B 读取该状态并更新权重。
% 修改后：模块 A 输出状态。模块 B 读取该状态并更新权重。
% 理由：分号判断指向 expression 已有的 LLM 层。不改数学。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] N-ISOLATE 方法段写入了实验赋值
% 问题：方法段给出了具体概率值
% 原文：训练时取 $p=0.5$。
% 修改后：训练时以概率 $p$ 保留观测。$p$ 的取值写在实验设置段。
% 理由：不得删除复现所需信息。先核该数值是否属于另一段。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] M-DETAILINV 方法段写入了实现枚举
% 问题：输入被写成特征工程清单
% 原文：从一阶差分、二阶差分和三组池化统计中枚举输入。
% 修改后：由特征映射 $\mathcal{R}$ 提取窗口统计量。
% 理由：若该枚举是唯一定义或复现所需，先挪走，不直接删除。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] M-TERMREG 方法段使用了口语动词
% 问题：“拼装”不是本段已有的学术说法
% 原文：把两路状态拼装成输入。
% 修改后：将两路状态组合为输入。
% 理由：只改语域。不替换受保护术语或模型名。

% 方法叙述（合成）[Severity: Minor] [Priority: P2]: [LLM] M-REDUNDANT 首段重复了上一段动机
% 问题：两段都在讲抑制漂移，后段没有新接口
% 原文：上一节已经说明需要抑制漂移。本节同样为了抑制漂移而建立更新式。
% 修改后：本节给出状态更新式，并把更新结果交给下一模块。
% 理由：换词以后再重复主张，不是去重。唯一接口或数值不得删除。
```

### Division from existing checks

M-FORMDUPE owns semantic restatement. PR-EQ-NARR only locates operator-by-operator narration. Deduplicate at the same place, then let the LLM decide. Do not report the two as the same defect.

N-ISOLATE and M-REPRO must not delete information required to reproduce a result. First check whether that information belongs in another paragraph.

M-SEMICOLON points at the existing LLM layer in expression. See [academic-style-zh.md](academic-style-zh.md#punctuation-prose). Do not create a check code.

All eight labels are judged only by the LLM. There is no script branch.

### A sentence split promises math-token invariance only

Bad example: stop the update when $a_{t}=a_{\max}$; otherwise step forward by $a_{t+1}=a_{t}+\delta$.
Revision example: stop the update when $a_{t}=a_{\max}$. Otherwise step forward by $a_{t+1}=a_{t}+\delta$.

The two math fragments stay as they are. Do not split one math fragment into two, and do not turn a Chinese phrase into a new equation. After the edit, run `polish_unit_zh.py --verify` on the touched unit. `UP-MATH` checks the math-token multiset only. This section promises token invariance only. It does not claim that the prose meaning is unchanged. Do not edit the mathematics.
