---
key: CFQP69V6
title: "Data-Knowledge-Driven Multiobjective Adaptive Optimal Control for Wastewater Treatment Processes Under Multiple Operating Conditions"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2025.3531514"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. DATA-KNOWLEDGE-DRIVEN MULTIOBJECTIVE ADAPTIVE OPTIMAL CONTROL` → `IV. CONVERGENCE AND STABILITY ANALYSIS` → `V. EXPERIMENTAL STUDIES` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 multiobjective optimal control / DOC / IOC / transfer learning）。Introduction 末有节序路标，指向 Section II–VI。Method 在 III（AOF / DK-model / CGD）。Experiments 标题为 `EXPERIMENTAL STUDIES`（BSM1）。另有独立收敛与稳定性节 IV。

## Openers

- abstract: `Wastewater treatment processes` — "Wastewater treatment processes (WWTPs) are operated under multiple operating conditions." (p.1)
- introduction: `WASTEWATER treatment processes` — "WASTEWATER treatment processes (WWTPs), as important part of water resource recycling, have received widespread attention [1], [2], [3], [4]." (p.1；栏首掉字)
- method: `To satisfy the` — "To satisfy the operational requirements of different operating conditions of WWTPs, a DK-MAOC framework is introduced (as shown in Fig. 1)." (p.4, III)
- experiments: `To demonstrate the` — "To demonstrate the availability of DK-MAOC, experiments are tested on the platform BSM1." (p.9, V)
- conclusion: `In this article` — "In this article, a method called DK-MAOC, which integrated the different requirements of multiple operating conditions, was proposed." (p.13)

## Gap transitions

- however (introduction): "However, WWTPs usually operate under multiple operating conditions, which poses challenges for optimal control in meeting different operating demands." (p.1)
- however (introduction): "However, in WWTPs, the operating conditions are complex and variable." (p.1)
- however (introduction): "However, the above data-driven methods are based on the assumption of sufficient data." (p.2)
- therefore (introduction): "Therefore, a data-knowledge-driven adaptive optimal control (DK-MAOC) for WWTPs is developed." (p.2)
- although (experiments): "Although the objective functions of MIOC incorporate both operational objective functions and tracking error objective functions, the operational objective functions do not consider different operational requirements under varying operating conditions." (p.11)
- however (conclusion): "However, there are still some limitations." (p.13)
- therefore (conclusion): "Therefore, future research can focus on efficient optimization algorithms, such as hybrid methods that combine global search to identify optimal regions with local refinement for faster convergence [44], [45]." (p.13)

## Hedge verbs

- propose / causal / abstract, method: "a data-knowledge-driven multiobjective adaptive optimal control (DK-MAOC) strategy is proposed"; "a collaborative gradient descent algorithm is proposed"
- indicate / causal / abstract: "The experimental results indicate that DK-MAOC can effectively avoid the situation"
- demonstrate / causal / experiments, conclusion: "To demonstrate the availability of DK-MAOC"; "the experimental results demonstrate that"
- can / speculative / abstract, conclusion: "DK-MAOC can guarantee optimal operation of WWTPs"; "the proposed DK-MAOC strategy can provide a promising approach"

## Cross-section linkers

- introduction → problem: "In this article, the remainder parts are organized as follows. Section II describes the problem formulation. Section III gives the technical details of DK-MAOC, together with the design of AOF, the DK-model, and the CGD algorithm. In Section IV, the convergence of the DK-model and the stability of DK-MAOC are discussed. In Section V, the availability of DK-MAOC is demonstrated though analyzing experiment results. In Section VI, the conclusions of this article are summarized." (p.2)
- method → analysis: Remark 5 后接 `IV. CONVERGENCE AND STABILITY ANALYSIS` (p.8)
- experiments → conclusion: Discussion 段落后直接 `VI. CONCLUSION` (p.13)

## Candidate rules

- R001 abstract 贡献句用被动 `a ... strategy is proposed`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `In this article, the remainder parts are organized as follows` 指向 II–VI。
- R004 贡献用 `The main contributions of this work include two aspects.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `However, there are still some limitations` 承认局限，`Therefore, future research can focus on` 指向后续。

## Candidate phrases

- `a data-knowledge-driven multiobjective adaptive optimal control (DK-MAOC) strategy is proposed` (abstract)
- `The main contributions of this work include two aspects.` (introduction)
- `In this article, the remainder parts are organized as follows.` (introduction)
- `In this article, a method called DK-MAOC, which integrated` (conclusion)
- `Therefore, future research can focus on efficient optimization algorithms` (conclusion)

## House style

自称是 `this article` / `this work` / `the proposed DK-MAOC`。多见被动 `is proposed`。未见 `Here we`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Wastewater treatment processes (WWTPs) are operated under multiple operating conditions.
- p.1 abstract: To effectively deal with the problem of multiple operating conditions in WWTPs, a data-knowledge-driven multiobjective adaptive optimal control (DK-MAOC) strategy is proposed.
- p.1 abstract: The experimental results indicate that DK-MAOC can effectively avoid the situation of effluent nitrate nitrogen and total nitrogen exceeding the standards while reducing energy consumption of WWTPs.
- p.1 introduction: WASTEWATER treatment processes (WWTPs), as important part of water resource recycling, have received widespread attention [1], [2], [3], [4].
- p.1 introduction: However, WWTPs usually operate under multiple operating conditions, which poses challenges for optimal control in meeting different operating demands.
- p.1 introduction: However, in WWTPs, the operating conditions are complex and variable.
- p.2 introduction: However, the above data-driven methods are based on the assumption of sufficient data.
- p.2 introduction: Therefore, a data-knowledge-driven adaptive optimal control (DK-MAOC) for WWTPs is developed.
- p.2 introduction: The main contributions of this work include two aspects.
- p.2 introduction: In this article, the remainder parts are organized as follows. Section II describes the problem formulation. Section III gives the technical details of DK-MAOC, together with the design of AOF, the DK-model, and the CGD algorithm. In Section IV, the convergence of the DK-model and the stability of DK-MAOC are discussed. In Section V, the availability of DK-MAOC is demonstrated though analyzing experiment results. In Section VI, the conclusions of this article are summarized.
- p.4 method: To satisfy the operational requirements of different operating conditions of WWTPs, a DK-MAOC framework is introduced (as shown in Fig. 1).
- p.9 experiments: To demonstrate the availability of DK-MAOC, experiments are tested on the platform BSM1.
- p.11 experiments: Although the objective functions of MIOC incorporate both operational objective functions and tracking error objective functions, the operational objective functions do not consider different operational requirements under varying operating conditions.
- p.13 conclusion: In this article, a method called DK-MAOC, which integrated the different requirements of multiple operating conditions, was proposed.
- p.13 conclusion: Thus, we can conclude that the proposed DK-MAOC strategy was able to ensure compliance with the discharge standards of WWTPs while achieving superior operational performance under multiple operating conditions.
- p.13 conclusion: However, there are still some limitations.
- p.13 conclusion: Therefore, future research can focus on efficient optimization algorithms, such as hybrid methods that combine global search to identify optimal regions with local refinement for faster convergence [44], [45].
