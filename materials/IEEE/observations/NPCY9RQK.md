---
key: NPCY9RQK
title: "Multi-Task Learning for Dense Prediction Tasks: A Survey"
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence"
doi: "10.1109/TPAMI.2021.3054719"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,16-18"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

阿拉伯数字标题：`1 INTRODUCTION` → `2 DEEP MULTI-TASK ARCHITECTURES` → `3` 优化策略 → `4` 实验评估 → `5 RELATED DOMAINS` → `6 CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work 专节；Introduction 内嵌 `Related work.` 段评先前 MTL 综述，后文 `5 RELATED DOMAINS` 扩到多域 / 迁移 / NAS。`related_work=inlined`。Introduction 末用 `Paper overview.` 路标，指向 Section 2–6。Survey 兼实验：Section 4 跨架构与优化做对比。

## Openers

- abstract: `With the advent` — "With the advent of deep learning, many dense prediction tasks, i.e. tasks that produce pixel-level predictions, have seen significant performance improvements." (p.1)
- introduction: `OVER the last` — "OVER the last decade, neural networks have shown impressive results for a multitude of tasks, such as semantic segmentation [1], instance segmentation [2] and monocular depth estimation [3]." (p.1；栏首掉字)
- method: `In this section` — "In this section, we review deep multi-task architectures used in computer vision." (p.2, 2)
- experiments: `We evaluated the` — "We evaluated the task balancing strategies from Section 3.1 under different settings." (p.16, 4)
- conclusion: `In this paper` — "In this paper, we reviewed recent methods for MTL within the scope of deep neural networks." (p.17)

## Gap transitions

- yet (abstract): "Yet, recent multi-task learning (MTL) techniques have shown promising results w.r.t. performance, computations and/or memory footprint, by jointly tackling multiple tasks through a learned shared representation." (p.1)
- yet (introduction): "Yet, many real-world problems are inherently multi-modal." (p.1)
- yet (introduction): "Yet, both works are literature review studies without an empirical evaluation or comparison of the presented techniques." (p.2)
- however (architectures): "However, several recent works took inspiration from both groups of works to jointly solve multiple pixel-level tasks." (p.3)
- yet (conclusion): "Yet, many optimization aspects still remain poorly understood." (p.18)
- surprisingly (experiments): "Surprisingly, in our case, we found that grid-search is competitive or better compared to existing task balancing techniques." (p.16)

## Hedge verbs

- provide / causal / abstract: "we provide a well-rounded view on state-of-the-art deep learning approaches for MTL"
- consider / causal / abstract: "First, we consider MTL from a network architecture point-of-view."
- examine / causal / abstract: "Second, we examine various optimization methods to tackle the joint learning of multiple tasks."
- review / causal / method, conclusion: "we review deep multi-task architectures"; "we reviewed recent methods for MTL"
- hope / speculative / conclusion: "We hope that this work stimulates further research efforts into this problem."
- indicates / causal / conclusion: "our analysis indicates that avoiding gradient competition between tasks can hurt performance"

## Cross-section linkers

- introduction → architectures: "Paper overview. In the following sections, we provide a well-rounded view on state-of-the-art MTL techniques that fall within the defined scope. Section 2 considers different deep multi-task architectures, categorizing them into two main groups: encoder- and decoder-focused approaches. Section 3 surveys various optimization techniques for balancing the influence of the tasks when updating the network's weights. … In Section 4, we provide an extensive experimental evaluation … Section 5 discusses the relations of MTL with other fields. Section 6 concludes the paper." (p.2)
- experiments → related domains: 局限段落后 `5 RELATED DOMAINS` (p.16)
- related domains → conclusion: 鲁棒性讨论后 `6 CONCLUSION` (p.17)

## Candidate rules

- R001 survey abstract 用 `In this survey, we provide a well-rounded view`，贡献用 `Our contributions concern the following. First, … Second, … Finally, …`。
- R002 Introduction 内嵌 `Related work.` 段，不单列 Related Work 节。
- R003 节序路标用 `Paper overview.` 指向 2–6。
- R004 架构分类可提出新 taxonomy，替代 soft/hard parameter sharing。
- R005 Conclusion 用 `In this paper, we reviewed` 收回，再用 `We hope that this work stimulates further research`。

## Candidate phrases

- `In this survey, we provide a well-rounded view on state-of-the-art deep learning approaches for MTL` (abstract)
- `Our contributions concern the following.` (abstract)
- `This paper aims to provide a more unified view on the topic.` (introduction)
- `In this paper, we reviewed recent methods for MTL within the scope of deep neural networks.` (conclusion)
- `We hope that this work stimulates further research efforts into this problem.` (conclusion)

## House style

自称 `In this survey` / `In this paper` / `we provide` / `we review` / `our analysis`。未见 `Here we`、`In this article`。`In this survey, we provide` 与 `In this paper, we reviewed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: With the advent of deep learning, many dense prediction tasks, i.e. tasks that produce pixel-level predictions, have seen significant performance improvements.
- p.1 abstract: Yet, recent multi-task learning (MTL) techniques have shown promising results w.r.t. performance, computations and/or memory footprint, by jointly tackling multiple tasks through a learned shared representation.
- p.1 abstract: In this survey, we provide a well-rounded view on state-of-the-art deep learning approaches for MTL in computer vision, explicitly emphasizing on dense prediction tasks.
- p.1 abstract: Our contributions concern the following. First, we consider MTL from a network architecture point-of-view.
- p.1 introduction: OVER the last decade, neural networks have shown impressive results for a multitude of tasks, such as semantic segmentation [1], instance segmentation [2] and monocular depth estimation [3].
- p.1 introduction: Yet, many real-world problems are inherently multi-modal.
- p.2 introduction: Yet, both works are literature review studies without an empirical evaluation or comparison of the presented techniques.
- p.2 introduction: This paper aims to provide a more unified view on the topic.
- p.2 introduction: Paper overview. In the following sections, we provide a well-rounded view on state-of-the-art MTL techniques that fall within the defined scope.
- p.2 method: In this section, we review deep multi-task architectures used in computer vision.
- p.16 experiments: We evaluated the task balancing strategies from Section 3.1 under different settings.
- p.16 experiments: Surprisingly, in our case, we found that grid-search is competitive or better compared to existing task balancing techniques.
- p.17 conclusion: In this paper, we reviewed recent methods for MTL within the scope of deep neural networks.
- p.17 conclusion: First, we presented an extensive overview of both architectural and optimization based strategies for MTL.
- p.17 conclusion: First, the performance of MTL strongly varies depending on the task dictionary.
- p.18 conclusion: Yet, many optimization aspects still remain poorly understood.
- p.18 conclusion: For example, opposed to recent works, our analysis indicates that avoiding gradient competition between tasks can hurt performance.
- p.18 conclusion: We hope that this work stimulates further research efforts into this problem.
