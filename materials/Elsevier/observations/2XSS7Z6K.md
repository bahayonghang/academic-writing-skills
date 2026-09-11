---
key: 2XSS7Z6K
title: "Reinforcement learning algorithms: A brief survey"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2023.120495"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-26"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

综述。数字节：`1. Introduction`（`1.1. What distinguishes this survey from the ones that came before it?` / `1.2. Contributions of this survey`）→ `2. Basics of reinforcement learning` → `3` 离散状态动作的 model-free RL → `4` 值函数近似 → `5` model-free DRL 与部分 model-based → `6. Current research work in RL` → `7. Conclusions`。前置 `ABSTRACT`、`Keywords` 与 `Review` 标记。无独立 Related Work。`related_work=inlined`（Introduction 与 1.1 综述对比、全篇按算法族展开文献）。Introduction 末有条目贡献 + 节序路标。无 Experiments 节；综述正文代替实验。

## Openers

- abstract: `Reinforcement Learning (RL)` — "Reinforcement Learning (RL) is a machine learning (ML) technique to learn sequential decision-making in complex problems."
- introduction: `Reinforcement Learning (RL)` — "Reinforcement Learning (RL) is a learning approach in which an artificial intelligence (AI) agent interacts with its surrounding environment by trial-and-error method and learns an optimal behavioral strategy based on the reward signals received from previous interactions."
- method: `In RL literature,` — "In RL literature, the learner or decision-maker is referred to as the agent and the world in which the agent lives and interacts is referred to as the environment." (s.2)
- experiments: `Even though DRL` — "Even though DRL has produced some fantastic results in various fields, it is difficult to replicate these results for problems in every field." (s.6 当前研究，综述无独立实验节)
- conclusion: `This paper only` — "This paper only covers ground-breaking work and important algorithms in order to give a broad overview of RL and discusses future research prospects in this fascinating field."

## Gap transitions

- however (introduction / 1.1): "However, the majority of these studies discuss the applications of RL in particular domains, such as industrial process control (Nian et al., 2020), autonomous vehicles (Kiran et al., 2022; Aradi, 2022), robotics (Singh et al., 2022; Zhu & Zhang, 2021; Khan et al., 2020)"
- even though (s.6): "Even though DRL has produced some fantastic results in various fields, it is difficult to replicate these results for problems in every field."
- therefore (s.6.6 / conclusion 前): 评测平台段强调 "We need richer platforms to bridge the gap between simulation and real-world performance."
- finally (abstract): "Finally, some promising research directions for RL are briefly presented."

## Hedge verbs

- aim / associative / abstract: "The authors aim to develop an initial reference point for researchers commencing their research work in RL."
- cover / associative / abstract: "In this review, the authors cover some fundamental model-free RL algorithms and pathbreaking function approximation-based deep RL (DRL) algorithms"
- discuss / associative / conclusion: "This paper only covers ground-breaking work and important algorithms in order to give a broad overview of RL and discusses future research prospects in this fascinating field."

## Cross-section linkers

- introduction → basics: "The outline of the paper is as follows: Some basic concepts of RL are discussed in Section 2. Section 3 covers the model-free RL algorithms for discrete state and action spaces. ... Finally, Section 7 draws some conclusions."
- s.5 → s.6: `6. Current research work in RL`
- s.6 → conclusion: 评测平台段落后 `7. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction 与分节综述，无独立 Related Work。
- R003 节序路标：`The outline of the paper is as follows`
- R004 条目贡献：`The main contributions are as follows`
- R009 自称：`This review` / `This survey` / `This paper only covers`

## Candidate phrases

- `The authors aim to develop an initial reference point for researchers commencing their research work in RL` (abstract)
- `The main contributions are as follows` (introduction)
- `The outline of the paper is as follows` (introduction)
- `This survey aims to provide a thorough analysis of RL literature` (introduction)
- `This paper only covers ground-breaking work and important algorithms` (conclusion)

## House style

自称 `This review` / `This survey` / `This paper` / `the authors`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Reinforcement Learning (RL) is a machine learning (ML) technique to learn sequential decision-making in complex problems.
- abstract: This review gives a broad overview of RL, covering its fundamental principles, essential methods, and illustrative applications.
- abstract: The authors aim to develop an initial reference point for researchers commencing their research work in RL.
- abstract: Finally, some promising research directions for RL are briefly presented.
- introduction: Reinforcement Learning (RL) is a learning approach in which an artificial intelligence (AI) agent interacts with its surrounding environment by trial-and-error method and learns an optimal behavioral strategy based on the reward signals received from previous interactions.
- introduction: However, the majority of these studies discuss the applications of RL in particular domains, such as industrial process control (Nian et al., 2020), autonomous vehicles (Kiran et al., 2022; Aradi, 2022), robotics (Singh et al., 2022; Zhu & Zhang, 2021; Khan et al., 2020)
- introduction: The presented survey in this paper provides an overall understanding of RL foundations, algorithms and promising research directions and is not confined to any specific application field.
- introduction: The main contributions are as follows:
- introduction: The outline of the paper is as follows: Some basic concepts of RL are discussed in Section 2.
- method: In RL literature, the learner or decision-maker is referred to as the agent and the world in which the agent lives and interacts is referred to as the environment.
- current-research: Even though DRL has produced some fantastic results in various fields, it is difficult to replicate these results for problems in every field.
- conclusion: This paper only covers ground-breaking work and important algorithms in order to give a broad overview of RL and discusses future research prospects in this fascinating field.
- conclusion: RL has achieved some incredible outcomes with the help of DL. Before comprehending DRL, it is necessary to have a thorough grasp of RL.
