---
key: L2DRK8XT
title: "Reinforcement Learning for Blast Furnace Ironmaking Operation With Safety and Partial Observation Considerations"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2023.3340741"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-7,12-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. PRELIMINARIES OF RL` → `IV` 离线 RL 算法（iRSDDPG） → `V. EXPERIMENT VALIDATION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 CBR、MPC、工业深度 RL 与数字孪生）。Introduction 末有 `The remainder of this article is organized as follows` 路标，指向 Section II–VI。Experiments 标题为 `EXPERIMENT VALIDATION`。

## Openers

- abstract: `Making proper decision online` — "Making proper decision online in complex environment during the blast furnace (BF) operation is a key factor in achieving long-term success and profitability in the steel manufacturing industry." (p.1)
- introduction: `BLAST furnace (BF) ironmaking` — "BLAST furnace (BF) ironmaking process is a crucial part of the iron and steel industry and plays a vital role in many fields, including construction, automotive, and machinery manufacturing." (p.1)
- method: `From the above description` — "From the above description, we can know that the proposed improved deep deterministic policy gradient (iDDPG) framework is an extension of the DDPG algorithm." (p.7, IV)
- experiments: `In this section, we verify` — "In this section, we verify the decision-making method based on our proposed framework within an industrial ironmaking plant." (p.7, V)
- conclusion: `In this article, we propose` — "In this article, we propose a novel decision-making approach for BF ironmaking process based on the offline RL framework." (p.12)

## Gap transitions

- however (abstract): "However, the strict safety requirements make it impossible to explore optimal decisions through online trial and error." (p.1)
- therefore (abstract): "Therefore, this article proposes a novel offline RL approach designed to ensure safety, maximize return, and address issues of partially observed states." (p.1)
- however (introduction): "However, CBR requires a large and diverse case base to work effectively and may not be effective when the new problem is significantly different from the cases in the base." (p.2)
- although (introduction): "Although these methods provide promising strategies for optimal decision-making in industrial processes, they rely on data-driven models to simplify the representation of a core element in RL: the environment." (p.2)
- thus (introduction): "Thus, this work forgoes the standard paradigm of RL and instead attempts to infer the optimal strategy by using offline RL based on a series of suboptimal decision trajectories collected from expert experience." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a novel offline RL approach"; "We propose a novel offline RL framework"; "we propose a novel decision-making approach"
- investigate / causal / abstract: "we investigate a recurrent version of the actor and critic networks"
- demonstrate / causal / abstract: "Verification within the BF smelting process demonstrates the improvements of the proposed algorithm in performance, i.e., safety and return."
- aims / speculative / introduction: "this work aims to provide safe and reliable decision-making support"
- will pursue / speculative / conclusion: "We will pursue further research focusing on model robustness"

## Cross-section linkers

- introduction → problem: "The remainder of this article is organized as follows. Section II introduces the decision-making problem in ironmaking process. Then, the preliminaries of RL are briefly revisited in Section III. Next, Section IV presents the details of the proposed offline RL algorithm considering safety and partial observation issues. Subsequently, the proposed decision-making framework is validated in Section V. Finally, Section VI gives concluding remarks." (p.3)
- method → experiments: Algorithm 1 后 `V. EXPERIMENT VALIDATION` (p.7)
- experiments → conclusion: 消融与收敛分析后 `VI. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `Therefore, this article proposes a novel offline RL approach designed to`。
- R002 Introduction 无独立 Related Work，CBR / MPC / RL 评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The contributions of this article can be summarized as follows.` + 编号。
- R005 Experiments 标题为 `EXPERIMENT VALIDATION`；Conclusion 用 `In this article, we propose` 收回，再用 `We will pursue further research`。

## Candidate phrases

- `Therefore, this article proposes a novel offline RL approach designed to` (abstract)
- `Thus, this work forgoes the standard paradigm of RL and instead attempts to infer` (introduction)
- `The contributions of this article can be summarized as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this article, we propose a novel decision-making approach` (conclusion)
- `We will pursue further research focusing on model robustness` (conclusion)

## House style

自称 `this article proposes` / `this work` / `we propose` / `we investigate` / `our proposed method`。未见 `Here we`、`In this paper`。`this article proposes` 与 `In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Making proper decision online in complex environment during the blast furnace (BF) operation is a key factor in achieving long-term success and profitability in the steel manufacturing industry.
- p.1 abstract: However, the strict safety requirements make it impossible to explore optimal decisions through online trial and error.
- p.1 abstract: Therefore, this article proposes a novel offline RL approach designed to ensure safety, maximize return, and address issues of partially observed states.
- p.1 abstract: Furthermore, we investigate a recurrent version of the actor and critic networks to better capture the complete observations, which solves the partially observed Markov decision process (POMDP) arising from sensor limitations.
- p.1 abstract: Verification within the BF smelting process demonstrates the improvements of the proposed algorithm in performance, i.e., safety and return.
- p.1 introduction: BLAST furnace (BF) ironmaking process is a crucial part of the iron and steel industry and plays a vital role in many fields, including construction, automotive, and machinery manufacturing.
- p.2 introduction: However, CBR requires a large and diverse case base to work effectively and may not be effective when the new problem is significantly different from the cases in the base.
- p.2 introduction: Although these methods provide promising strategies for optimal decision-making in industrial processes, they rely on data-driven models to simplify the representation of a core element in RL: the environment.
- p.2 introduction: Thus, this work forgoes the standard paradigm of RL and instead attempts to infer the optimal strategy by using offline RL based on a series of suboptimal decision trajectories collected from expert experience.
- p.3 introduction: The contributions of this article can be summarized as follows.
- p.3 introduction: The remainder of this article is organized as follows. Section II introduces the decision-making problem in ironmaking process. Then, the preliminaries of RL are briefly revisited in Section III. Next, Section IV presents the details of the proposed offline RL algorithm considering safety and partial observation issues. Subsequently, the proposed decision-making framework is validated in Section V. Finally, Section VI gives concluding remarks.
- p.7 method: From the above description, we can know that the proposed improved deep deterministic policy gradient (iDDPG) framework is an extension of the DDPG algorithm.
- p.7 experiments: In this section, we verify the decision-making method based on our proposed framework within an industrial ironmaking plant.
- p.12 conclusion: In this article, we propose a novel decision-making approach for BF ironmaking process based on the offline RL framework.
- p.12 conclusion: Compared with existing algorithms, our proposed method not only improves the quality of molten iron while ensuring safe operation but also demonstrates superior learning efficiency.
- p.12 conclusion: Although experimental results have verified the potential of the offline RL framework for BF applications, there is still room for exploration.
- p.13 conclusion: We will pursue further research focusing on model robustness and the incorporation of online evaluation and feedback mechanisms to effectively address the challenges posed by actual data distribution.
