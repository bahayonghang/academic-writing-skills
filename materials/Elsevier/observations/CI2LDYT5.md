---
key: CI2LDYT5
title: "Advances in sensitivity-based nonlinear model predictive control and dynamic real-time optimization"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2015.02.001"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. NLP strategies for NMPC` → `3` asNMPC 与稳定性 → `4` 多步扩展与蒸馏例 → `5` Economic NMPC / D-RTO → `6. Conclusions and future work`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 Newton-type / real-time iteration、两层 RTO、MHE/EKF）。Introduction 末有节序路标，指向 Section 2–6。Method 为 NLP 策略与问题改写。Experiments 并入第 4–5 节大规模蒸馏案例。

## Openers

- abstract: `Recent results in` — "Recent results in the development of efficient large-scale nonlinear programming (NLP) algorithms have led to fast, on-line realizations of optimization-based methods for nonlinear model predictive control (NMPC) and dynamic real-time optimization (D-RTO), with predictive nonlinear dynamic (e.g., first principle) models."
- introduction: `For over three` — "For over three decades, real-time optimization (RTO) and model predictive control (MPC) have emerged as essential technologies for optimal process operation in the chemical and refining industry."
- method: `We begin with` — "We begin with the following discrete-time nonlinear dynamic model of the plant with uncertainties:" (s.2)
- experiments: `This case study` — "This case study considers two cases: no disturbance, and 5% disturbance; in the second case disturbances are introduced as additive noise." (s.5)
- conclusion: `Advances in large-scale` — "Advances in large-scale nonlinear programming solvers and sensitivity lead to formulation of nonlinear model-based estimation (MHE) and control (NMPC) tasks that require only negligible on-line computation."

## Gap transitions

- however (introduction): "However, this two-layer approach assumes that model disturbances and transients are neglected in the RTO layer [13]."
- moreover (introduction): "Moreover, model inconsistency between layers and unresolved transient behavior may lead to unreachable setpoints [48]."
- on the other hand (introduction): "On the other hand, EKF may have poor performance for highly nonlinear systems [9,42], thus spawning related estimation methods"
- nevertheless (introduction): "Nevertheless, an important hurdle is the cost and reliability of on-line computation; lengthy and unreliable optimization calculations lead to unsuccessful controller performance."

## Hedge verbs

- lead / causal / abstract, conclusion: "have led to fast, on-line realizations"; "These advances also lead to a number of open questions"
- demonstrate / causal / abstract: "Two large scale distillation case studies, based on nonlinear first principle models, are presented that demonstrate the effectiveness of these approaches."
- review / associative / introduction, conclusion: "This study reviews recent results related to advanced step NMPC and D-RTO."
- assume / speculative / method: "We assume that N is sufficiently long such that zN ∈ Xf is always true"
- plan / speculative / conclusion: "In future, we plan to handle these through on-line state and parameter estimation"

## Cross-section linkers

- introduction → method: "In the next section we present the basic NMPC problem formulation and review an optimization framework based on interior-point NLP solvers and sensitivity concepts. Section 3 presents advanced step NMPC (asNMPC) strategies and related stability properties. ... Finally, Section 6 summarizes the paper along with directions for future work."
- method → experiments: 蒸馏案例并入第 4–5 节
- experiments → conclusion: 正则化结果后 `6. Conclusions and future work`

## Candidate rules

- R002 Related Work 并入 Introduction（综述体）。
- R003 节序路标：`In the next section we present` + 后续节号。
- R012 结论标题用 `Conclusions and future work`。
- R013 自称 `We also extend` / `This study reviews`。

## Candidate phrases

- `This leads to` (abstract)
- `We also extend these capabilities to` (abstract)
- `This study builds on the survey in` (introduction)
- `In the next section we present` (introduction)
- `This study reviews recent results related to` (conclusion)

## House style

自称 `We also extend` / `This study` / `This overview`。未见 `In this paper` 与 `Here we`。`This study` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Recent results in the development of efficient large-scale nonlinear programming (NLP) algorithms have led to fast, on-line realizations of optimization-based methods for nonlinear model predictive control (NMPC) and dynamic real-time optimization (D-RTO), with predictive nonlinear dynamic (e.g., first principle) models.
- abstract: This leads to advanced step NMPC (asNMPC), which essentially eliminates computational delay.
- abstract: Two large scale distillation case studies, based on nonlinear first principle models, are presented that demonstrate the effectiveness of these approaches.
- introduction: For over three decades, real-time optimization (RTO) and model predictive control (MPC) have emerged as essential technologies for optimal process operation in the chemical and refining industry.
- introduction: Nevertheless, an important hurdle is the cost and reliability of on-line computation; lengthy and unreliable optimization calculations lead to unsuccessful controller performance.
- introduction: Moreover, model inconsistency between layers and unresolved transient behavior may lead to unreachable setpoints [48].
- introduction: This study builds on the survey in [5] and also focuses on new results related to sensitivity-based NMPC and D-RTO.
- method: We begin with the following discrete-time nonlinear dynamic model of the plant with uncertainties:
- experiments: This case study considers two cases: no disturbance, and 5% disturbance; in the second case disturbances are introduced as additive noise.
- conclusion: Advances in large-scale nonlinear programming solvers and sensitivity lead to formulation of nonlinear model-based estimation (MHE) and control (NMPC) tasks that require only negligible on-line computation.
- conclusion: This study reviews recent results related to advanced step NMPC and D-RTO.
- conclusion: In future, we plan to handle these through on-line state and parameter estimation, where (z∗, v∗) are also updated for each NMPC problem.
