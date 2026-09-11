---
key: KW8NVMG4
title: "Reinforcement learning control for systems with unknown coupling induced by the compensator"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2025.103449"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-10"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

前置 `Full length article` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction`（`1.1. Background` / `1.2. Related work` / `1.3. Contributions`）→ `2. Problem formulation and preliminaries` → `3. Correlation design method of feedback controller and compensator` → `5. Case studies` → `6. Conclusion`。无独立顶层 Related Work。`related_work=inlined`（Introduction 小节 `1.2. Related work`）。Introduction 末有条目式贡献。Method 拆成问题表述与相关设计。Experiments 标题为 `Case studies`。

## Openers

- abstract: `Compensator is a` — "Compensator is a primary method for overcoming external disturbances in industrial processes."
- introduction: `In industrial processes` — "In industrial processes, one of the crucial control objectives is to maintain stable operation within a changing production environment."
- method: `The controlled model` — "The controlled model can be represented in state-space model form as follows:" (s.2)
- experiments: `Industrial alumina evaporation` — "Industrial alumina evaporation process density control is introduced to demonstrate the effectiveness of our method."
- conclusion: `This paper proposes` — "This paper proposes a RL-based correlation learning for controller and compensator method."

## Gap transitions

- however (abstract): "However, in certain cases, compensator may cause coupling between the controller and the disturbance, thereby exacerbating the disturbance variation."
- to this end (abstract): "To this end, a reinforcement learning (RL)-based correlation learning for controller and compensator method is proposed to link the learning processes of the feedback controller and the compensator."
- different from (abstract): "Different from existing methods, the compensator design problem for coupled unknown problems is solved with a lower dimensional exploration space."
- to address (introduction): "To address this issue, we propose a reinforcement learning (RL)-based correlation learning method for controllers and compensators."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a ... method is proposed"; "we propose"; "This paper proposes"
- demonstrate / causal / experiments: "the proposed design method demonstrates superior accuracy and speed compared to all baseline methods."
- suggest / associative / experiments: "These results suggest that correlative learning initializes RL with a control strategy that effectively drives system state convergence"

## Cross-section linkers

- introduction → method: 贡献条目与记号后 `2. Problem formulation and preliminaries`
- method → experiments: 算法伪代码后 `5. Case studies`
- experiments → conclusion: 对比实验后 `6. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction（`1.2. Related work`）。
- R004 贡献列表：`The main novelties and contributions of this work are summarized as follows`
- R009 自称：`this paper proposes` / `we propose`

## Candidate phrases

- `To this end, a ... method is proposed` (abstract)
- `Different from existing methods` (abstract)
- `To address this issue, we propose` (introduction)
- `The main novelties and contributions of this work are summarized as follows` (introduction)
- `This paper proposes a RL-based correlation learning` (conclusion)

## House style

自称 `this paper proposes` / `we propose` / `In this paper`。条目式贡献用项目符号。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Compensator is a primary method for overcoming external disturbances in industrial processes.
- abstract: However, in certain cases, compensator may cause coupling between the controller and the disturbance, thereby exacerbating the disturbance variation.
- abstract: To this end, a reinforcement learning (RL)-based correlation learning for controller and compensator method is proposed to link the learning processes of the feedback controller and the compensator.
- abstract: Different from existing methods, the compensator design problem for coupled unknown problems is solved with a lower dimensional exploration space.
- introduction: In industrial processes, one of the crucial control objectives is to maintain stable operation within a changing production environment.
- introduction: In this paper, an overlooked industrial control problem is highlighted: the coupling between controller actions and changes in external disturbances.
- introduction: To address this issue, we propose a reinforcement learning (RL)-based correlation learning method for controllers and compensators.
- introduction: The main novelties and contributions of this work are summarized as follows.
- method: The controlled model can be represented in state-space model form as follows:
- experiments: Industrial alumina evaporation process density control is introduced to demonstrate the effectiveness of our method.
- experiments: As illustrated in Fig. 4, the proposed design method demonstrates superior accuracy and speed compared to all baseline methods.
- conclusion: This paper proposes a RL-based correlation learning for controller and compensator method.
- conclusion: Compared with traditional control methods. The proposed method has better disturbance rejection ability and dynamic response effect.
