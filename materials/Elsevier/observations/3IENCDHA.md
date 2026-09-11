---
key: 3IENCDHA
title: "Robust closed-loop dynamic real-time optimization"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2023.04.003"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,8-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Formulation` → `3. Case studies` → `4. Conclusion`。前置 `abstract` 与 `article info` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段稳态 RTO、DRTO、CL-DRTO、鲁棒 MPC 与不确定性处理）。Introduction 末有节序路标。Method 为 Formulation。Experiments 标题为 `Case studies`。

## Openers

- abstract: `Real-time optimization` — "Real-time optimization (RTO) is a valuable tool for economic optimization of chemical process systems."
- introduction: `Economic optimization is` — "Economic optimization is an important consideration in chemical engineering applications, particularly in an environment of increasing market competition and rising costs."
- method: `The objective of` — "The objective of the robust DRTO formulation is to extend the CL-DRTO strategy previously developed in Jamaludin and Swartz [6] to effectively handle plant uncertainty at the DRTO level."
- experiments: `The first case` — "The first case study in which the robust DRTO is applied is a single-input–single-output (SISO) system, where the performance of the robust DRTO is compared against that of a nominal DRTO."
- conclusion: `In this work` — "In this work, a multi-scenario closed-loop dynamic real-time optimization (CL-DRTO) formulation with input clipping approximation was presented as a means of handling uncertainty at the economic optimization layer while modeling the dynamic behavior of both the plant being optimized and the MPC controlling the plant."

## Gap transitions

- however (introduction): "However, not considering the transient phase of a plant and instead leaving the transition to a lower level controller, can lead to economically suboptimal operation."
- therefore (introduction): "Therefore, it can be advantageous to include dynamic modeling of the plant behavior directly in the economic optimization problem [3]."
- while (introduction): "While uncertainty handling has been widely investigated for regulatory control in the form of robust MPC, it is less common for it to be handled at the economic optimization level."
- in contrast (introduction): "In contrast to steady-state RTO, explicit consideration of uncertainty in DRTO has received relatively little attention."

## Hedge verbs

- extend / causal / abstract, introduction: "This paper extends the formulation for direct inclusion of uncertainty handling."; "The paper extends the MPC-aware CL-DRTO paradigm"
- present / causal / introduction, conclusion: "we present a detailed formulation"; "a multi-scenario ... formulation ... was presented"
- show / associative / conclusion: "The method shows improvement over a single-scenario CL-DRTO in terms of economics and constraint violation in two simulated case studies."

## Cross-section linkers

- introduction → method: "The remainder of the paper is organized as follows. The mathematical formulation of the robust DRTO algorithm is presented in Section 2, where the primary economic optimization problem is laid out, followed by the setup of the embedded MPC subproblems. The solution strategy for this multi-level optimization problem is then explained, followed by a description of its modification by inclusion of the input clipping approximation method. Section 3 presents two case studies"
- method → experiments: input clipping 段落后 `3. Case studies`
- experiments → conclusion: 多不确定性来源后 `4. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remainder of the paper is organized as follows`
- R009 自称：`This paper extends` / `In this work` / `we present`

## Candidate phrases

- `This paper extends the formulation` (abstract)
- `The paper extends the ... paradigm` (introduction)
- `The remainder of the paper is organized as follows` (introduction)
- `In the present work, we present a detailed formulation` (introduction)
- `In this work, a ... formulation ... was presented` (conclusion)

## House style

自称 `This paper extends` / `In this work` / `we present` / `The method shows`。第一人称复数与论文主语并存。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Real-time optimization (RTO) is a valuable tool for economic optimization of chemical process systems.
- abstract: This paper extends the formulation for direct inclusion of uncertainty handling.
- abstract: A robust multi-scenario CL-DRTO scheme which models the dynamic behavior of the plant and its MPC system under uncertainty is introduced.
- introduction: Economic optimization is an important consideration in chemical engineering applications, particularly in an environment of increasing market competition and rising costs.
- introduction: However, not considering the transient phase of a plant and instead leaving the transition to a lower level controller, can lead to economically suboptimal operation.
- introduction: The paper extends the MPC-aware CL-DRTO paradigm of Jamaludin and Swartz [6] to directly account for uncertainty within the DRTO optimization formulation.
- introduction: The remainder of the paper is organized as follows. The mathematical formulation of the robust DRTO algorithm is presented in Section 2, where the primary economic optimization problem is laid out, followed by the setup of the embedded MPC subproblems.
- method: The objective of the robust DRTO formulation is to extend the CL-DRTO strategy previously developed in Jamaludin and Swartz [6] to effectively handle plant uncertainty at the DRTO level.
- experiments: The first case study in which the robust DRTO is applied is a single-input–single-output (SISO) system, where the performance of the robust DRTO is compared against that of a nominal DRTO.
- experiments: The system is a single reaction CSTR with one inlet stream, one outlet, and one reaction.
- conclusion: In this work, a multi-scenario closed-loop dynamic real-time optimization (CL-DRTO) formulation with input clipping approximation was presented as a means of handling uncertainty at the economic optimization layer while modeling the dynamic behavior of both the plant being optimized and the MPC controlling the plant.
- conclusion: The method shows improvement over a single-scenario CL-DRTO in terms of economics and constraint violation in two simulated case studies.
