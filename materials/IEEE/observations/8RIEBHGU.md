---
key: 8RIEBHGU
title: "Physics-Informed Neural Networks-Based Adaptive Optimized Control and Its Application to Automated Surface Vessels"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3619904"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PINNS-ENABLED ADAPTIVE OPTIMIZED CONTROL DESIGN` → `III. PINNS-BASED ADAPTIVE OPTIMIZED CONTROL DESIGN FOR SECOND-ORDER AFFINE SYSTEM` → `IV. SIMULATION VERIFICATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 physics-based / data-driven、PINNs、RL/ADP、BLF-based safe RL）。Introduction 末为编号贡献，无 `The rest of this article is organized` 路标。Method 拆成一般设计（II）与二阶仿射/船舶应用（III）。Experiments 标题为 `SIMULATION VERIFICATION`（仿真 + HiL）。附录给 Theorem 证明。

## Openers

- abstract: `The abundant knowledge` — "The abundant knowledge of data and physics models can be simultaneously utilized in learning-based modeling, prediction, and control methods, which makes the balance between model efficiency, accuracy, and complexity." (p.1)
- introduction: `DISCUSSIONS on the` — "DISCUSSIONS on the crucial importance of abundant data toward learning-based modeling, prediction, and control methods for many practical control problems have highlighted its efficiency in compensating for the inaccuracies of physics-based models and achieving a balance between model accuracy and complexity [1]." (p.1)
- method: `Controlling dynamical systems` — "Controlling dynamical systems with state-variables x(t) ∈ Rn subject to control inputs u(t) ∈ Rm" (p.3, II)
- experiments: `This section demonstrates` — "This section demonstrates the proposed PINNs-based adaptive optimized control method for the automated surface vessel control problem with an appropriate comparison." (p.7, IV)
- conclusion: `This article proposes` — "This article proposes a PINNs-based adaptive optimized control method for control-affine systems, applied to second-order automated vessel control." (p.9)

## Gap transitions

- however (introduction): "However, these models risk losing generalization under untrained sets because neural networks (NNs) are not easily interpretable [5]." (p.1)
- therefore (introduction): "Therefore, with essential and significant requirements to fully utilize information from physics and data for an efficient learning mechanism for optimal learning-based control, our research focuses on developing a PINNs-based adaptive optimized control method with essential learning designs for the whole learning framework, which is shown in Fig. 1." (p.2)
- meanwhile (experiments): "Meanwhile, from the comparison, a suitable deeper NN structure (T2) has promoted the performance of the PINNs method compared with the NN structure T1." (p.9)

## Hedge verbs

- investigate / causal / abstract: "this work investigates the physics-informed neural networks (PINNs)-based adaptive optimized control method"
- propose / causal / abstract, conclusion: "the proposed method"; "This article proposes a PINNs-based adaptive optimized control method"
- demonstrate / causal / abstract, experiments: "its effectiveness and practical applicability are demonstrated through comparative simulations and hardware-in-the-loop tests"; "The simulation results demonstrate that the PINNs-based method can promote control performance"
- show / causal / experiments: "the PINNs' performance outperforms the pure NN model with fewer errors"

## Cross-section linkers

- introduction → method: 编号贡献后直接 `II. PINNS-ENABLED ADAPTIVE OPTIMIZED CONTROL DESIGN`，无独立路标句 (p.3)
- method → application: "This section introduces the theoretical part of the PINNs-enabled adaptive optimized control algorithm design, which involves the control law decomposition design, PINNs model training, RL-based learning design, and learning convergence analysis, which will be utilized in the next section with application to the actual physical system." (p.4)
- application → experiments: Algorithm 1 与 Theorem 2 后接 `IV. SIMULATION VERIFICATION` (p.7)
- experiments → conclusion: 参数对比段落后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `this work investigates` / `the proposed method`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段。
- R003 贡献句用 `The contributions of this paper can be concluded as follows` + 编号列表。
- R004 Method 分两节：一般 PINNs-ADP 设计（II）再落到二阶仿射/船舶（III）。
- R005 Experiments 标题为 `SIMULATION VERIFICATION`，含仿真与 HiL。
- R006 Conclusion 用 `This article proposes` 收回方法，再用 `These future works will focus on` 指向后续。

## Candidate phrases

- `this work investigates` (abstract)
- `the proposed method efficiently realizes` (abstract)
- `The contributions of this paper can be concluded as follows.` (introduction)
- `This article proposes a PINNs-based adaptive optimized control method` (conclusion)
- `These future works will focus on` (conclusion)

## House style

自称是 `this work` / `the proposed method` / `this paper` / `This article proposes` / `our research`。未见 `Here we`。`The contributions of this paper` 与 `This article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The abundant knowledge of data and physics models can be simultaneously utilized in learning-based modeling, prediction, and control methods, which makes the balance between model efficiency, accuracy, and complexity.
- p.1 abstract: Thus, this work investigates the physics-informed neural networks (PINNs)-based adaptive optimized control method with essential learning designs for the whole learning framework.
- p.1 abstract: The proposed method is applied to automated vessel control problems, and its effectiveness and practical applicability are demonstrated through comparative simulations and hardware-in-the-loop tests.
- p.1 introduction: DISCUSSIONS on the crucial importance of abundant data toward learning-based modeling, prediction, and control methods for many practical control problems have highlighted its efficiency in compensating for the inaccuracies of physics-based models and achieving a balance between model accuracy and complexity [1].
- p.1 introduction: However, these models risk losing generalization under untrained sets because neural networks (NNs) are not easily interpretable [5].
- p.2 introduction: Therefore, with essential and significant requirements to fully utilize information from physics and data for an efficient learning mechanism for optimal learning-based control, our research focuses on developing a PINNs-based adaptive optimized control method with essential learning designs for the whole learning framework, which is shown in Fig. 1.
- p.2 introduction: The contributions of this paper can be concluded as follows.
- p.3 method: Controlling dynamical systems with state-variables x(t) ∈ Rn subject to control inputs u(t) ∈ Rm
- p.4 method: This section introduces the theoretical part of the PINNs-enabled adaptive optimized control algorithm design, which involves the control law decomposition design, PINNs model training, RL-based learning design, and learning convergence analysis, which will be utilized in the next section with application to the actual physical system.
- p.4 method: The second-order affine systems commonly arise in a significant and large category of real-world systems, for example, for the system modules of automated vessels, autonomous vehicles and multirobot coordination.
- p.7 experiments: This section demonstrates the proposed PINNs-based adaptive optimized control method for the automated surface vessel control problem with an appropriate comparison.
- p.7 experiments: The simulation results demonstrate that the PINNs-based method can promote control performance with both fewer control errors and the accumulated performance index compared with pure physics-based or data-driven methods.
- p.9 experiments: Meanwhile, from the comparison, a suitable deeper NN structure (T2) has promoted the performance of the PINNs method compared with the NN structure T1.
- p.9 conclusion: This article proposes a PINNs-based adaptive optimized control method for control-affine systems, applied to second-order automated vessel control.
- p.9 conclusion: These future works will focus on enhancing the consideration of onboard computational limitations, environmental disturbances, and robustness to acknowledge the complexities of real-world implementation.
