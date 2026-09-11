---
key: AM7MV5AL
title: "A Survey on Mixture of Experts in Large Language Models"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2025.3554028"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-23"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

阿拉伯数字标题（综述，非罗马数字）：`1 INTRODUCTION` → `2 BACKGROUND ON MIXTURE OF EXPERTS` → `3` taxonomy → `4` algorithm design → `5 SYSTEM DESIGN OF MIXTURE OF EXPERTS` → `6 APPLICATIONS OF MIXTURE OF EXPERTS` → `7 CHALLENGES & OPPORTUNITIES` → `8 CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立背景节 `2 BACKGROUND ON MIXTURE OF EXPERTS`（dense / sparse MoE）。`related_work=independent`。Introduction 末有 `The remainder of this survey is organized as follows` 路标，指向 Section 2–8。无独立 Experiments；实证评述写在算法与系统节。

## Openers

- abstract: `Large language models` — "Large language models (LLMs) have garnered unprecedented advancements across diverse fields, ranging from natural language processing to computer vision and beyond." (p.1)
- introduction: `IN the current` — "IN the current landscape of artificial general intelligence (AGI), the transformative impact of transformer-based large language models (LLMs) has permeated diverse fields such as natural language processing [1], [2], [3], [4], [5], computer vision [6], [7], and multimodality [8], [9], [10]." (p.1；栏首掉字)
- background: `In transformer-based large` — "In transformer-based large language models (LLMs), each mixture-of-experts (MoE) layer typically consists of a set of N “expert networks” {f1, . . . , fN }, alongside a “gating network” G." (p.2)
- conclusion: `In this survey` — "In this survey, we present a systematic and comprehensive review of the literature on MoE models, serving as a valuable compendium for researchers exploring the landscape of MoE technologies." (p.23)

## Gap transitions

- despite (abstract): "Despite its growing prevalence, there lacks a systematic and comprehensive review of the literature on MoE." (p.1)
- despite (introduction): "Despite the growing popularity and application of mixture of experts (MoE) models across various domains, comprehensive reviews that thoroughly examine and categorize advancements, particularly in the context of MoE in LLMs, remain scarce." (p.1)
- this gap (introduction): "This gap in the literature not only hinders the progress of MoE research but also limits the broader dissemination of knowledge on this topic." (p.2)
- despite (challenges): "Despite their promise, several intrinsic challenges remain, necessitating further collaborative design and engineering" (p.22)
- however (challenges): "However, there is a notable propensity for sparse MoE architectures to overfit to specific tasks or datasets, which undermines their ability to generalize effectively [34], [35], [219], [220]." (p.23)

## Hedge verbs

- seek / causal / abstract: "This survey seeks to bridge that gap, serving as an essential resource for researchers delving into the intricacies of MoE."
- propose / causal / abstract, introduction: "followed by proposing a new taxonomy of MoE"; "introducing a novel taxonomy that organizes recent progress into three categories"
- present / causal / conclusion: "In this survey, we present a systematic and comprehensive review of the literature on MoE models"
- may / speculative / introduction, challenges: "Rumors suggest that the formidable GPT-4 may employ an MoE architecture"; "these methods may compromise model performance"

## Cross-section linkers

- introduction → background: "The remainder of this survey is organized as follows. Section 2 provides a foundational understanding of MoE, contrasting sparse and dense activation of experts. Section 3 introduces our proposed taxonomy for categorizing MoE advancements. Sections 4, 5, and 6 delve into the algorithmic designs, computing system support, and various applications of MoE models, respectively, following the structure outlined in our taxonomy in Figure 3. Finally, in Section 7, we highlight the critical challenges and opportunities for bridging the research-practicality gap, culminating in Section 8 with our conclusions." (p.2)
- applications → challenges: 多模态应用后接 `7 CHALLENGES & OPPORTUNITIES` (p.22)
- challenges → conclusion: "By addressing these challenges, we can unlock the full potential of MoE models" 随后 `8 CONCLUSION` (p.23)

## Candidate rules

- R001 综述 abstract 用 `This survey seeks to bridge that gap`，不用 `Here we`。
- R002 独立背景节标题为 `BACKGROUND ON MIXTURE OF EXPERTS`，用阿拉伯数字节号。
- R003 Introduction 末用 `The remainder of this survey is organized as follows` 指向 2–8。
- R004 Introduction 用 `Our survey aims to address this deficit by providing a clear and comprehensive overview` 定位综述贡献。
- R005 Conclusion 用 `In this survey, we present` 收回，再用 `We hope this survey can contribute to an essential reference` 收束。

## Candidate phrases

- `This survey seeks to bridge that gap, serving as an essential resource` (abstract)
- `Our survey aims to address this deficit by providing a clear and comprehensive overview` (introduction)
- `The remainder of this survey is organized as follows.` (introduction)
- `In this survey, we present a systematic and comprehensive review of the literature on MoE models` (conclusion)
- `We hope this survey can contribute to an essential reference for researchers` (conclusion)

## House style

自称是 `this survey` / `our survey` / `we first` / `we present`。未见 `Here we`。`This survey seeks to bridge that gap` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Large language models (LLMs) have garnered unprecedented advancements across diverse fields, ranging from natural language processing to computer vision and beyond.
- p.1 abstract: Despite its growing prevalence, there lacks a systematic and comprehensive review of the literature on MoE.
- p.1 abstract: This survey seeks to bridge that gap, serving as an essential resource for researchers delving into the intricacies of MoE.
- p.1 introduction: IN the current landscape of artificial general intelligence (AGI), the transformative impact of transformer-based large language models (LLMs) has permeated diverse fields such as natural language processing [1], [2], [3], [4], [5], computer vision [6], [7], and multimodality [8], [9], [10].
- p.1 introduction: Despite the growing popularity and application of mixture of experts (MoE) models across various domains, comprehensive reviews that thoroughly examine and categorize advancements, particularly in the context of MoE in LLMs, remain scarce.
- p.2 introduction: This gap in the literature not only hinders the progress of MoE research but also limits the broader dissemination of knowledge on this topic.
- p.2 introduction: Our survey aims to address this deficit by providing a clear and comprehensive overview of MoE in LLMs, introducing a novel taxonomy that organizes recent progress into three categories: algorithm, system, and application.
- p.2 introduction: The remainder of this survey is organized as follows. Section 2 provides a foundational understanding of MoE, contrasting sparse and dense activation of experts. Section 3 introduces our proposed taxonomy for categorizing MoE advancements. Sections 4, 5, and 6 delve into the algorithmic designs, computing system support, and various applications of MoE models, respectively, following the structure outlined in our taxonomy in Figure 3. Finally, in Section 7, we highlight the critical challenges and opportunities for bridging the research-practicality gap, culminating in Section 8 with our conclusions.
- p.2 background: In transformer-based large language models (LLMs), each mixture-of-experts (MoE) layer typically consists of a set of N “expert networks” {f1, . . . , fN }, alongside a “gating network” G.
- p.22 challenges: Despite their promise, several intrinsic challenges remain, necessitating further collaborative design and engineering
- p.23 challenges: However, there is a notable propensity for sparse MoE architectures to overfit to specific tasks or datasets, which undermines their ability to generalize effectively [34], [35], [219], [220].
- p.23 conclusion: In this survey, we present a systematic and comprehensive review of the literature on MoE models, serving as a valuable compendium for researchers exploring the landscape of MoE technologies.
- p.23 conclusion: We introduce a new taxonomy for MoE models and provide an in-depth analysis that encompasses three distinct vantage points: algorithm design, system design, and practical applications, complemented by a curated collection of open-source implementations, detailed hyperparameter configurations, and thorough empirical assessments.
- p.23 conclusion: We hope this survey can contribute to an essential reference for researchers seeking to rapidly acquaint themselves with MoE models, and that it will actively contribute to the vibrant progression.
