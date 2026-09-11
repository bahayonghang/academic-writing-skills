---
key: H2KSLPA7
title: "Reinforcement Learning Based Decision Making of Operational Indices in Process Industry Under Changing Environment"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2020.3005207"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. DECISION MAKING OF OPERATIONAL INDICES BASED ON REINFORCEMENT LEARNING` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 evolutionary computation / MPC / deep RL）。Introduction 末有 `The remainder of this article is organized as follows`。Method 在 III。Experiments 标题为 `EXPERIMENT`。

## Openers

- abstract: `The plant-wide production` — "The plant-wide production process is composed of multiple unit processes, in which the operational indices of each unit process are assigned and adjusted according to product quality, yield, and actual operating modes." (p.2727)
- introduction: `THE PROCESS industry` — "THE PROCESS industry is a foundation of economic development, which generally includes steel, petroleum, chemical engineering, etc." (p.2727)
- method: `Inspired by behavioral` — "Inspired by behavioral psychology, the RL is to seek the balance between exploration and exploitation by trial-and-error mechanism, in which model-free and active RL methods are of great benefit to solving control and optimization problems with complex environments." (p.2729–2730, III.A)
- experiments: `In this section` — "In this section, the proposed approach is applied to a mineral processing plant for the beneficiation of low-grade iron ore, in which the production line includes several units, namely raw ore processing, shaft furnace roasting, grinding and low- and high-intensity magnetic separation." (p.2731, IV)
- conclusion: `This article proposed` — "This article proposed a RL based decision-making approach of operational indices, which was aiming to solve the problems of irregular changes of operational conditions." (p.2735)

## Gap transitions

- due to (abstract): "Due to the changing operational conditions of the production process, the operational indices cannot be effectively adjusted by most of the model-based methods or evolutionary computation." (p.2727)
- therefore (introduction): "Therefore, the decision making of operational indices is still a challenging problem for optimal operation of the process industry." (p.2727)
- however (introduction): "However, there are still shortcomings in the existing methods." (p.2727)
- therefore (introduction): "Therefore, a real time, model-free RL algorithm is a potential and valuable approach to be considered." (p.2728)
- different from (abstract): "Different from the existing methods, this article presents a multiactor networks ensemble algorithm and an actor-critic framework with stochastic policy to avoid falling into local optimums." (p.2727)

## Hedge verbs

- propose / causal / abstract, conclusion: "a model-free RL algorithm is proposed"; "This article proposed a RL based decision-making approach"
- present / causal / abstract, introduction: "this article presents a multiactor networks ensemble algorithm"; "this article presents a novel decision-making approach"
- demonstrate / causal / abstract: "the results demonstrate the effectiveness of the proposed algorithm"
- illustrate / causal / conclusion: "the simulation results illustrated the effectiveness of the proposed algorithm"

## Cross-section linkers

- introduction → method: "The remainder of this article is organized as follows. Section II describes the decision-making problem of operational indices in process industry. In Section III, the decision-making problem is formulated as a RL problem and the proposed MAE method with stochastic policy based on the AC framework is proposed. Section IV presents the simulation studies based on actual data of a mineral processing plant to illustrate the effectiveness of the proposed approach. Section V concludes this article." (p.2728)
- method → experiments: Algorithm 1 后 `IV. EXPERIMENT` (p.2731)
- experiments → conclusion: actor 数量实验后 `V. CONCLUSION` (p.2735)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions of this article are summarized as follows.`（段落而非编号列表）。
- R005 Conclusion 先收回方法，再用 `The future work will focus on`。
- R009 结论 `This article proposed a RL based`。

## Candidate phrases

- `In this article, the decision making ... is formulated as` (abstract)
- `Different from the existing methods, this article presents` (abstract)
- `The contributions of this article are summarized as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `The future work will focus on` (conclusion)

## House style

自称是 `In this article` / `this article presents` / `This article proposed` / `we investigate`。未见 `Here we`、`In this paper`。`this article presents` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.2727 abstract: The plant-wide production process is composed of multiple unit processes, in which the operational indices of each unit process are assigned and adjusted according to product quality, yield, and actual operating modes.
- p.2727 abstract: Due to the changing operational conditions of the production process, the operational indices cannot be effectively adjusted by most of the model-based methods or evolutionary computation.
- p.2727 abstract: In this article, the decision making of operational indices is formulated as a continuous state, continuous action reinforcement learning (RL) problem and a model-free RL algorithm is proposed, which learns a decision policy to determine the operational indices according to the actual operational conditions.
- p.2727 abstract: Different from the existing methods, this article presents a multiactor networks ensemble algorithm and an actor-critic framework with stochastic policy to avoid falling into local optimums.
- p.2727 abstract: Simulation studies are conducted on actual data of a mineral processing plant and the results demonstrate the effectiveness of the proposed algorithm.
- p.2727 introduction: THE PROCESS industry is a foundation of economic development, which generally includes steel, petroleum, chemical engineering, etc.
- p.2727 introduction: Therefore, the decision making of operational indices is still a challenging problem for optimal operation of the process industry.
- p.2727 introduction: However, there are still shortcomings in the existing methods.
- p.2728 introduction: Therefore, a real time, model-free RL algorithm is a potential and valuable approach to be considered.
- p.2728 introduction: The contributions of this article are summarized as follows.
- p.2728 introduction: The remainder of this article is organized as follows. Section II describes the decision-making problem of operational indices in process industry. In Section III, the decision-making problem is formulated as a RL problem and the proposed MAE method with stochastic policy based on the AC framework is proposed. Section IV presents the simulation studies based on actual data of a mineral processing plant to illustrate the effectiveness of the proposed approach. Section V concludes this article.
- p.2731 experiments: In this section, the proposed approach is applied to a mineral processing plant for the beneficiation of low-grade iron ore, in which the production line includes several units, namely raw ore processing, shaft furnace roasting, grinding and low- and high-intensity magnetic separation.
- p.2733 experiments: It is obvious that the production yields are increased by 6551.6 tons in the period of 30 days and 71.3 tons in one day by the MAE algorithm, which are significantly better than the current system.
- p.2735 conclusion: This article proposed a RL based decision-making approach of operational indices, which was aiming to solve the problems of irregular changes of operational conditions.
- p.2735 conclusion: Through the experiments of real industrial data, the simulation results illustrated the effectiveness of the proposed algorithm.
- p.2735 conclusion: The future work will focus on improving the security of RL algorithms.
- p.2735 conclusion: Furthermore, we will also focus on the synthesis of advanced controllers to cope with constantly changing environment and elevate the operational performance in practices.
