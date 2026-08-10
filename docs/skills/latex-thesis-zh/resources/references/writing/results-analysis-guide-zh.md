# Experimental Results Analysis and Evidence-Grading Guide

Use this guide for model comparisons, component comparisons, sensitivity analyses, and the discussion
of generative or augmentation methods in Chinese engineering theses. It governs factual organization,
criterion binding, and explanatory strength in results chapters. For chapter-level experiment
completeness, read [`method-chapter-guide-zh.md`](method-chapter-guide-zh.md); for claim types about
method benefits, read [`method-description-guide-zh.md`](method-description-guide-zh.md); for wording
calibration, read [`over-claim-guard.md`](over-claim-guard.md).

After running the candidate check, review the original figures, tables, experimental protocol, and
method definitions against this guide:

```bash
uv run python scripts/analyze_experiment.py thesis.tex --results-analysis
```

`RA-*` supplies heuristic cues only and does not cover the guide's `R-*` checklist. A script hit does
not prove an error, and script silence does not prove completeness. Precision and recall on real theses
remain `UNVERIFIED`.

## 1. Fix the Objective and Factual Boundary First

Results analysis answers three questions in order: what difference was observed, which samples,
conditions, or metrics contain the difference, and which defined method structures are consistent with
it. State figure and table facts before explanations. Do not begin with a mechanism conclusion and then
select supporting numbers.

Fix the following objects before writing:

1. Data blocks, sample counts, evaluation order, and the information available to each method.
2. The evaluated object's pipeline stage, such as raw candidates, admitted candidates, the selected set,
   or downstream output.
3. Each metric's direction, best value, runner-up value, criterion, and risk-subset definition.
4. The source batch for figures, tables, and prose values, including whether they evaluate the same object.
5. The inputs, structures, losses, and training protocols already defined for each model.
6. The experiment type that can or cannot distinguish the complete setting from an individual component.

Local theses may guide paragraph organization only. They are not sources for the current thesis's
numbers, mechanisms, or academic claims. Limit conclusions to the actual data block, test protocol, and
evaluation object; do not rewrite offline validation as field deployment.

Basis: user specification §1, §3.2, and §5.1; external sources #1, #3, and #6.

## 2. Follow Two Eight-Step Argument Chains

Use the following order for a model-comparison subsection:

1. Comparison protocol and model grouping.
2. Overall metric ranking and the closest baseline.
3. Ranking changes across subsets, conditions, or risk tails.
4. Error localization with trajectories or scatter plots.
5. Typical-error and outlier-tail analysis with box plots or distributions.
6. Explanation through input information and representation mechanisms.
7. Review against component records or discriminating evidence.
8. Current conclusion and interface to the next experiment.

Use a second eight-step chain for statistical-fidelity subsections about generative or augmentation
methods:

1. Evaluation object and source batch.
2. Definitions of references and limits.
3. Marginal and specified-condition metrics.
4. Joint-distribution metrics.
5. Dynamic-structure metrics.
6. Support intervals and local differences in figures.
7. Consistency explanation for the complete generation-selection pipeline.
8. Interface to the downstream-utility experiment.

Establish the full empirical record in one to three natural paragraphs before relating it to problem
properties and method design. Do not alternate between one number and one guessed explanation.
Unexpected outcomes are valid analytical objects: report them accurately, identify which expectation
they alter, and state the follow-up test needed to distinguish explanations.

Basis: user specification §2 and §5.2; external sources #3 and #8.

## 3. Complete Numeric Comparisons Metric by Metric

- Compare every key metric with the true runner-up in the full table. Name different runners-up when
  metrics have different rankings.
- Use the following relative reduction for error metrics:

```text
(e_baseline - e_method) / e_baseline x 100%
```

Here, `e_baseline` is the baseline error and `e_method` is the current method's error.

- Report the absolute difference for `$R^2$` by default. Give a percentage only when the relative change
  has a meaningful interpretation.
- State the grouping basis, such as input access, model type, or training protocol. A group mean is not a
  controlled component experiment.
- Report ranking reversals across overall results, subsets, conditions, or risk tails. Do not use “best
  overall” to conceal cross-over results.
- When a risk subset is small, report its sample count at the first interpretation and limit the claim to
  the current test block's point estimate.
- A large percentage does not imply a large practical effect. Also report the raw-scale difference and
  distinguish statistical evidence from practical importance.

Describe ties as “comparable under the current error scale” or “competitive with the baseline.” Then
distinguish among a genuinely small effect, an experiment unable to separate methods, and insufficient
sample size. Do not choose one explanation without the corresponding evidence.

Basis: user specification §3.1, §3.3, and §8; external sources #2, #3, and #9.

## 4. Bind References, Criteria, and Result Terms Individually

When one table mixes several comparison objects, distinguish three kinds of references or limits first;
handle statistics without criteria separately.

| Type | Purpose | Compliant comparison | Result term |
| --- | --- | --- | --- |
| Point reference | Describe how close an estimate is to a reference center | Estimate, interval, point reference, and absolute difference | close to reference |
| Distribution limit | For example, a resampling-distribution P95 that evaluates the same metric | Compare the corresponding confidence endpoint in the metric's direction | within upper bound or within interval |
| Specified target limit | Defined by a support domain, task objective, or preregistered rule | Name its source, then compare the corresponding endpoint | within upper bound or within interval |
| Statistic without a criterion | No predefined reference or threshold | Report only the estimate and interval | descriptive record |

“R2R point reference” and “R2R P95 limit” are naming examples for a specific project only. Public rules
use “point reference” and “distribution limit.” Do not collapse point references, distribution limits,
and specified target limits into one generic “reference.”

The endpoint direction must match the criterion:

| Criterion direction | Comparison object |
| --- | --- |
| Smaller is better with an upper limit | Confidence upper bound versus upper-limit threshold |
| Larger is better with a lower limit | Confidence lower bound versus lower-limit threshold |
| Two-sided interval or tolerance band | Check both endpoints |
| Point reference without a decision boundary | Report estimate, interval, and absolute difference |

Apply one sequence to every judgment: “estimate and interval -> corresponding reference or limit ->
absolute difference or endpoint comparison -> supported conclusion.” Do not skip the intermediate
comparison and turn a point estimate directly into a pass, equivalence, or overall-effectiveness claim.

Bind criteria metric by metric when one cell contains multiple metrics. If only KS has an upper limit and
W1 has no limit, write “KS within upper bound; W1 descriptive record,” not that the entire row is “within
the limit.” Interval overlap, numerical closeness, or falling inside an empirical range does not establish
statistical equivalence. Use “equivalent” only after a predefined equivalence test has actually been run.

Use the closed result vocabulary “close to reference,” “within upper bound,” “within interval,” and
“descriptive record.” When a criterion is not met, state “above the upper bound” or “outside the interval”
directly; do not invent ambiguous categories such as “essentially passed” or “approximately equivalent.”

The evaluation-object name must include its pipeline stage. When statistics come from a filtered selected
set, use “selected set” consistently in the subsection title, table title, figure title, and prose. Do not
abbreviate it as “generated samples” and extrapolate to the raw candidate pool or downstream utility.

Use the following reusable judgment skeleton. Replace project terms only for the object and criterion;
do not change the comparison order:

> Metric X has an estimate of a [l, u], with point reference/evaluation limit b; the absolute difference is
> d, or the comparison between its confidence endpoint and the limit yields c. Therefore, this metric is
> close to the reference/within the upper bound/within the interval. Metric Y has no criterion and is
> reported as a descriptive record only.

Basis: user specification §3.2, §5.3, and §5.4.

## 5. Give Figures, Tables, and Distribution Statistics Distinct Jobs

| Evidence | Primary question | Sufficient analysis |
| --- | --- | --- |
| Metric table | Which method is better, and by how much? | Best and runner-up, relative and absolute differences, ranking reversals |
| Prediction trajectory | Where does the difference occur? | Peaks, troughs, transitions, sustained offsets, or local underestimation |
| Scatter plot | How does error change with the target? | Diagonal departure, heteroscedasticity, boundary compression |
| Box plot | How are typical and tail errors composed? | Median, interquartile range, whiskers, and outliers |
| Component table | Which structural changes accompany metric changes? | Component-wise comparison on the same metrics and cross-over results |

Assign one primary conclusion to each figure or table. Prefer an opening sentence that states the
conclusion rather than merely saying “Figure X shows...”. Relate trajectory or scatter-plot observations
back to metrics. For example, concentrated underestimation in high-value windows should correspond to a
high-risk-tail error or maximum absolute error. In a box plot, separate the median and interquartile body
from whiskers, outliers, and maxima in the tail. “The curve fits better” and “the box is smaller” are
insufficient analyses.

For narrow columns, wrapping, and bilingual-caption rules, see [`tables.md`](../modules/tables.md). Use a
left-aligned fixed-width `p` column for result terms and allocate widths deliberately. Do not force long
sentences into a narrow cell with `\makecell`. After compilation, inspect character-by-character wraps,
abnormal spacing, and unreadable stacking instead of relying only on overfull warnings.

Basis: user specification §4, §5.4, and §5.5; external sources #1, #2, #3, and #5.

## 6. Analyze Generative or Augmentation Results Only When Applicable

This section applies only when outputs from a generative model undergo admission, reranking, or set
selection and are compared with real samples on marginal distributions, joint distributions, and dynamic
structure. Conventional predictive-model comparisons do not have to use these metric families.

The title states the source method, final pipeline stage, and evaluation question. The opening paragraph
also fixes the source batch, real samples, point references, evaluation limits, metric-computation space,
and whether all figures and tables use the same evaluation object.

| Metric family | Question answered | Required report | Supported conclusion |
| --- | --- | --- | --- |
| KS, W1 | Univariate marginals and specified-condition shifts | Estimate, interval, and metric-specific reference or limit | The corresponding marginal is close to its point reference, or its endpoint is within the limit |
| MMD, SWD | Multivariate joint-distribution difference | Kernel or projection setup, estimate, interval, and corresponding limit | The joint-distribution criterion is met under the current kernel or projection definition |
| C2ST | Whether a classifier separates real and selected sets | Classifier, grouping method, fold count, AUC interval, and criterion | Discriminability is near random under the current classifier and grouped-fold protocol |
| ACF, PSD | Temporal dependence and spectral-structure difference | Lag or frequency setup, error value, interval, and corresponding limit | The evaluated temporal or spectral statistic meets its dynamic limit |

Judge the marginal and specified-condition, joint-distribution, and dynamic-structure families metric by
metric before summarizing which statistical levels are close to references or meet limits. Do not use the
first KS result that meets its criterion to summarize the full metric set prematurely.

A density plot analysis covers both the main support interval and local differences in bins, shoulders,
peaks, or tails, and relates them to KS/W1 values. In conditional generation, state whether the generated
curve represents a specified condition, model output, or observable variable. Do not call a specified
condition the “synthetic sample's ground truth.” A plot localizes marginal differences; it cannot replace
joint-distribution or dynamic metrics.

When interpreting the complete setting, map “defined method constraint -> corresponding statistic ->
current observation.” Dynamic representations, temporal encodings, or dynamic-consistency constraints may
support a consistency explanation involving ACF and PSD results. Candidate-admission rules, feasibility
constraints, distribution-distance budgets, or set selection may support one involving the selected set's
KS, W1, MMD, SWD, and C2ST results. Separate the contributions of the generator, admission rule, and set
selection only when raw candidates, intermediate-stage outputs, or controlled component-removal records
exist. Otherwise, interpret only the complete generation-selection setting.

Close by answering positively which evaluated statistics place the selected set close to the corresponding
references or within the corresponding limits, then explain why the next subsection evaluates downstream
utility separately. Do not dilute the main conclusion with consecutive disclaimers or infer prediction,
classification, or optimization performance directly from statistical fidelity. Statistical fidelity and
downstream utility require separate subsections and cannot substitute for each other.

For general data, fairness, and ablation requirements, see
[`method-chapter-guide-zh.md`](method-chapter-guide-zh.md). For input and output
constraints in generated experiment prose, see [`experiment.md`](../modules/experiment.md).

Basis: user specification §5.1-§5.6.

## 7. Limit Explanatory Strength with the Five-Rung Evidence Ladder

When a method chapter selects evidence by claim type, use the four-level table in
[`method-description-guide-zh.md`](method-description-guide-zh.md). When a
results chapter selects wording from the evidence already available, use the five-rung ladder below. The
first answers “what evidence does this claim type require?”; the second answers “how far may the current
evidence go?” For wording choices, see [`over-claim-guard.md`](over-claim-guard.md); this guide does not
duplicate its vocabulary or replacement tables.

| Evidence rung | Permitted content | Recommended predicate |
| --- | --- | --- |
| Figure/table fact | Values and shapes observed directly in the current test block | “is,” “below,” “concentrates in” |
| Structural fact | Inputs and computations directly defined by an equation or algorithm | “uses,” “retains,” “adjusts,” “falls back” |
| Consistency explanation | A result shape corresponds to a structural mechanism | “is consistent with,” “corresponds to,” “supports an association with” |
| Component contribution | Controlled changes to a component within the same framework | “after removal, ... changes,” “this record supports ...” |
| Causal attribution | Strict control, equal budgets, and exclusion of alternative explanations | “is brought about by,” “is primarily attributable to” |

Map the method chapter's four claim levels to the results chapter's five evidence rungs as follows:

| Four-level method claim | Five-rung results destination | Use |
| --- | --- | --- |
| Definitional fact | Structural fact | Use equations or algorithm definitions to state actual inputs, processing, and outputs |
| Mechanism-level role | Structural fact -> consistency explanation | State the structural fact first; add consistency only when a corresponding result shape exists |
| Empirical performance | Figure/table fact + component contribution | Report figure/table facts first; controlled component records may support contribution |
| Causal attribution | Causal attribution | Use only when a discriminating design excludes alternative explanations |

Use the reverse mapping when reading from results evidence back to method claims:

| Five-rung results evidence | Method claim it can reconnect to | Prohibited extrapolation |
| --- | --- | --- |
| Figure/table fact | Observational part of empirical performance | Does not establish a mechanism-level role or causal attribution by itself |
| Structural fact | Definitional fact; definitional part of a mechanism-level role | Does not establish empirical performance by itself |
| Consistency explanation | A downgraded mechanism-level role | Cannot be rewritten as component contribution |
| Component contribution | Empirical performance with a controlled record | Does not automatically exclude every alternative mechanism |
| Causal attribution | Causal claim with discriminating evidence | Cannot extend to untested data blocks or protocols |

Rankings between complete models usually support only a consistency explanation. When a causal predicate
has no nearby component evidence, downgrade it or state that the mechanism remains undetermined.
`RA-CAUSAL` checks only a lexical combination of “single-sentence causal predicate and component-evidence
cue in the surrounding window.” A defensive speculative explanation that combines stacked mechanisms,
no per-mechanism evidence, and a terminal withdrawal remains a B3 composite judgment in
[`experiment.md`](../modules/experiment.md) under `[LLM]`. A word or hedge count cannot replace evidence
mapping.

Basis: user specification §5.6 and §6; external sources #1, #9, and #10.

## 8. Explain Heterogeneous Baselines Along Four Axes

Inspect four axes instead of inventing one story per baseline:

1. Input information: whether a method receives low-frequency conditions, masks, age, or other state variables.
2. Temporal and variable representation: whether it preserves temporal order, full history, local patterns,
   or inter-variable coupling.
3. Training objective: whether it constrains state overlap, risk tails, missing paths, or uncertainty.
4. Data support: whether sample size, tail sparsity, and target distribution match model capacity.

Concentrate on one or two axes per paragraph. A mechanism must come from a method definition, reliable
citation, or discriminating evidence. Do not infer that a model family is inherently unsuitable from one
test ranking, and do not equate publication date, parameter count, or complexity with performance.

Basis: user specification §7.

## 9. Calibrate Ties, Reversals, and Unexpected Results with Examples

Insufficient numeric repetition:

> Method A has an RMSE of 0.17, Method B 0.19, and Method C 0.20; therefore, Method A is best.

Problem: it does not name the true runner-up, calculate a difference, localize the error, or state the
claim's scope.

Insufficient unsupported attribution:

> Method A's performance gain comes mainly from gating, attention, tail loss, and uncertainty modeling.

Problem: a complete-setting comparison cannot distinguish four components. Listing more mechanisms does
not strengthen explanatory evidence.

Sufficient progression from fact to explanation:

> Method A's overall RMSE is 10.2% lower than runner-up Method B, and its high-risk-tail RMSE is 24.5%
> lower, but B has the lowest error in the low-risk tail. The trajectories localize the difference near
> high-value peaks, while the box plots show that both A's main error body and upper tail are smaller. A
> explicitly receives condition availability and age and retains a single-source path when conditions are
> unavailable; this structural fact is consistent with the error changes in high-value and transition
> windows. Overall RMSE increases after removing the condition input, so the current record supports an
> association between condition information and the performance difference, but it does not attribute the
> entire gain to one gating component.

Sufficient wording for a tie:

> The error intervals for Methods A and B overlap, and the current test block does not show a stable ranking.
> This result supports describing the methods as comparable under this protocol. Whether the sample size can
> distinguish a smaller effect requires a power analysis or additional data.

Sufficient wording for an unexpected result:

> Method A has the lowest overall metric, but Method B leads in the low-risk subset, contrary to the
> expectation that the advantage would persist across subsets. The reversal is concentrated among low-risk
> samples. The current result cannot distinguish whether sample composition or model representation causes
> this pattern; stratified replications or controlled input comparisons are needed.

For generative or augmentation results, do not call a filtered selected set the raw generated samples,
do not apply a threshold defined only for KS to W1, and do not infer that one component “guaranteed”
fidelity from a complete-setting result.

Basis: user specification §3.3, §5.7, and §8; external sources #5, #8, and #9.

## 10. Separate the R-* Semantic Checklist from RA-* Script Cues

`R-*` is the manual and LLM semantic-review checklist; `RA-*` is a candidate locator. They cooperate as
shown below. A missed script cue cannot be interpreted as a passed `R-*` item.

| spec checklist item | Script cue | LLM judgment |
| --- | --- | --- |
| R-NUMERIC | RA-SECONDBEST | Recalculate percentages and name the runner-up for each metric |
| R-CRITERION | RA-EQUIV | Check the three criterion types and endpoint direction row by row |
| R-REVERSAL / R-COMPETING | RA-UNIVERSAL | Compare against the table for cross-over results |
| R-LOCALIZE / R-DISTRIBUTION | RA-SHALLOW / RA-DISTVOCAB | Judge error locations and body/tail content semantically |
| R-STAGE / R-BATCH | RA-STAGE | Check identical object naming across titles, tables, figures, and prose |
| R-CAUSALITY / R-MECHANISM | RA-CAUSAL | Grade every explanation on the evidence ladder |
| R-TRANSITION | RA-TRANSITION | Judge whether the interface sentence is substantive |
| R-PROTOCOL / R-TITLE / R-FIGSEM / R-TABLE-VISUAL / R-SCOPE / R-UTILITY | none | Pure LLM checks |

Every thesis still requires all 17 `R-*` checks, including those without script cues.

Basis: user specification §10; implementation design §3.3.

## 11. Thresholds, False-Positive Boundaries, and Sources

The following thresholds select candidates only. They are neither statistical criteria nor writing-quality
scores:

| Check | Candidate threshold or gate | Severity | Criterion source |
| --- | --- | --- | --- |
| RA-EQUIV | An equivalence claim occurs while the chapter window has no equivalence test, TOST, equivalence envelope, or equivalence-bound cue | Major/P1 | User specification §3.2 and §5.3 |
| RA-CAUSAL | A causal predicate has no component evidence within one paragraph on either side; downgrade when chapter-level evidence exists | Major/P1 or Minor/P2 | User specification §5.6 and §6; source #10 |
| RA-SECONDBEST | At least 8 visible lines contain a table reference, comparison context, and best-result claim but no runner-up cue | Minor/P2 | User specification §3.1; source #2 |
| RA-SHALLOW | A figure reference and shallow shape wording occur in one paragraph without a number or metric term | Minor/P2 | User specification §4; source #5 |
| RA-DISTVOCAB | Neither the box-plot paragraph nor its next paragraph contains body or tail statistic terms | Minor/P2 | User specification §4 |
| RA-UNIVERSAL | A universal superiority claim has no concession or reversal marker in the same sentence | Info/P3 | User specification §3.3; source #3 |
| RA-STAGE | After at least two fidelity metrics appear in the chapter window, selected-set/post-filtering and generated-sample/synthetic-sample/raw-candidate names occur in separate declarative sentences | Info/P3 | User specification §5.1 and §5.4 |
| RA-TRANSITION | The final paragraph lacks a next-chapter, next-section, follow-up-experiment, or “therefore” interface cue | Info/P3 | User specification §2 and §5.6; sources #3 and #6 |

False-positive boundaries: mathematical equivalence classes or transformations do not trigger RA-EQUIV;
consistency predicates do not trigger RA-CAUSAL; a causal claim with nearby component evidence is not
reported, while chapter-level but unbound evidence produces Minor only; normative or negative sentences
do not participate in RA-STAGE object-mixing counts; RA-STAGE stays silent without at least two fidelity
metrics; RA-SECONDBEST stays silent without comparison context or a table reference; RA-TRANSITION stays
silent when the chapter already has a summary subsection. Existing industrial-thesis boundaries remain:
missing significance tests, missing mean-plus-variance reports, and an expert-experience baseline in an
optimization chapter cannot trigger an issue by themselves.

On 2026-08-10, five local PDF-extracted theses were calibrated read-only by second-level experiment
section. A candidate for high-frequency alternation between numeric and attribution sentences fired four
times; every hit was affected by pagination, table rows, or lost paragraph boundaries and did not provide
a reviewable single-paragraph alternation. The candidate was therefore excluded from the runtime family.
RA-STAGE produced no hit in the same corpus and remains an Info/P3 cue; this observation does not
establish recall. Synthetic examples prove only the contract and regression behavior. Precision and recall
remain UNVERIFIED / missing evidence.

External sources:

1. University of Toronto Engineering Communication Program, [Results and Discussions](https://ecp.engineering.utoronto.ca/resources/online-handbook/components-of-documents/results-and-discussions/).
2. UC San Diego MAE, [Lab Report Writing: Results and Data Commentary](http://maecourses.ucsd.edu/callafon/labcourse/handouts/Results.pdf).
3. MIT EECS Communication Lab, [Paper: Results](https://mitcommlab.mit.edu/eecs/commkit/journal-article-results/).
4. City University of Hong Kong OSAWEC, [Results](https://osawec.elc.cityu.edu.hk/repo/front-page/thesis/results/).
5. Flinders University, [Discussing Results](https://students.flinders.edu.au/content/dam/student/slss/academic-writing/discussing-results.pdf).
6. University of Melbourne, [Analysing Data and Reporting Results](https://students.unimelb.edu.au/academic-skills/graduate-research-services/writing-thesis-sections-part-2/analysing-data-and-reporting-results).
7. Sheffield MEE, [What Goes In? What Goes Out?](https://mee.group.shef.ac.uk/Report_writing_website/4.3.html).
8. Peacock (2002), [Communicative Moves in the Discussion Section of Research Articles](https://jolantasinkuniene.wordpress.com/wp-content/uploads/2014/03/peacock-communication-moves-in-discussion-section-of-ra.pdf).
9. CASRAI, [Writing a Discussion Section](https://casrai.org/guides/writing-the-discussion-section-of-a-research-paper).
10. CASRAI, [Causal Analysis](https://casrai.org/guides/causal-analysis).

Basis: user specification §9 and §10; external sources #1-#10.
