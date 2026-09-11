---
key: 7XFVXJNV
title: "Feedback control for optimal process operation"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2006.10.011"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-17"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节（survey）：`1. Introduction` → `2. Optimization by regulation (self-optimizing control)` → `3. Real-time optimization (RTO)` → `4. Reducing the gap between regulation and RTO` → `5. Direct finite horizon optimizing control` → `6. Open issues` → `7. Conclusions`。前置 Abstract / Keywords 与 Contents。无独立 Related Work。`related_work=inlined`（各节评 self-optimizing control、RTO、MPC 集成与 SMB 控制文献）。Introduction 末有节序路标。Method/Experiments 由第 5 节 Hashimoto reactive SMB 案例承担。结论前有 `Open issues`。

## Openers

- abstract: `In chemical process` — "In chemical process operation, the purpose of control is to achieve optimal process operation despite the presence of significant uncertainty about the plant behavior and disturbances."
- introduction: `From a process` — "From a process engineering point of view, the purpose of automatic feedback control (and that of manual control as well) is not primarily to keep the controlled variables at their set-points as well as possible or to nicely track dynamic set-point changes, but to operate the plant such that the net return is maximized in the presence of disturbances and uncertainties, exploiting the available measurements."
- method: `For demanding applications` — "For demanding applications, the replacement of linear MPC controllers by nonlinear model-predictive control is a promising option and industrial applications have been reported in particular in polymerization processes [46–49]." (s.5)
- experiments: `The example application` — "The example application that will briefly be described in the sequel is the racemization of Tröger's Base (TB) in combination with a chromatographic separation in order to produce of the enantiomer TB – that is used for the treatment of cardiovascular diseases." (s.5.2.5)
- conclusion: `This survey paper` — "This survey paper points out that process control should be seen as a means to optimize plant operations rather than to just track pre-computed set-points."

## Gap transitions

- but (abstract): "Tracking of set-points is often required for lower-level control loops, but on the process level in most cases this is not the primary concern and may even be counterproductive."
- but nonetheless (introduction): "This has been pointed out in a number of papers (see e.g. [1–5]) but nonetheless almost all of the literature on automatic control and controller design for chemical processes is concerned with the task to make certain controlled variables track given set-points"
- however (introduction): "In chemical process control, however, good tracking of set-points is mostly of interest for lower-level control tasks."
- however (open issues): "A practically very important limiting issue however is that of reliability and transparency."

## Hedge verbs

- review / associative / abstract, introduction: "different approaches ... are reviewed"; "we give a review of the state of the art"
- demonstrate / causal / abstract, section 5: "The potential of this approach is demonstrated by its application to a complex process"; "it will be demonstrated that direct online optimizing control can successfully be applied"
- should / speculative / introduction, conclusion: "process control should be seen as a means to optimize plant operations"
- may / speculative / abstract, introduction: "may even be counterproductive"; "may even be infeasible"
- point out / associative / conclusion: "This survey paper points out that"

## Cross-section linkers

- introduction → method: "First the idea to implement the optimal plant operation by conventional feedback control, termed “self-optimizing control” [5], is discussed in Section 2. ... Finally, open issues and possible lines of future research are discussed."
- method → experiments: `5.2 Case study` 后 `5.2.5. Optimizing controller application`
- experiments → conclusion: Open issues 后 `7. Conclusions`

## Candidate rules

- R002 Related Work 并入各技术节（综述体）。
- R003 节序路标：`First the idea ... is discussed in Section 2`
- R014 综述自称 `In this paper, different approaches ... are reviewed` / `This survey paper points out`
- R016 结论前独立 `Open issues` 节。

## Candidate phrases

- `In this paper, different approaches how to realize ... are reviewed` (abstract)
- `In this contribution, we give a review of the state of the art` (introduction)
- `The potential of this approach is demonstrated by` (abstract)
- `This survey paper points out that` (conclusion)
- `Issues for further research are outlined in the final section` (abstract)

## House style

自称 `In this paper` / `In this contribution, we` / `This survey paper`。未见 `Here we`。`In this paper` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: In chemical process operation, the purpose of control is to achieve optimal process operation despite the presence of significant uncertainty about the plant behavior and disturbances.
- abstract: In this paper, different approaches how to realize optimal process operation by feedback control are reviewed.
- abstract: The potential of this approach is demonstrated by its application to a complex process which combines reaction with chromatographic separation.
- introduction: From a process engineering point of view, the purpose of automatic feedback control (and that of manual control as well) is not primarily to keep the controlled variables at their set-points as well as possible or to nicely track dynamic set-point changes, but to operate the plant such that the net return is maximized in the presence of disturbances and uncertainties, exploiting the available measurements.
- introduction: In this contribution, we give a review of the state of the art in integrated process optimization and control of continuous processes and highlight the option of direct or online optimizing control (also called one-layer approach [7] or full optimizing control [8]).
- method: For demanding applications, the replacement of linear MPC controllers by nonlinear model-predictive control is a promising option and industrial applications have been reported in particular in polymerization processes [46–49].
- method: In the next section, it will be demonstrated that direct online optimizing control can successfully be applied to control problems that are hard to tackle by conventional control techniques.
- experiments: The objective of the optimizing controller is to minimize the solvent consumption QDe for a constant feed flow and a given purity requirement in the presence of a plant/model mismatch.
- conclusion: This survey paper points out that process control should be seen as a means to optimize plant operations rather than to just track pre-computed set-points.
- conclusion: Using an economic cost function in the MPC computations instead of a function that penalizes the distance to the desired set-points or trajectories which are assumed as given and fixed offers new exiting possibilities.
