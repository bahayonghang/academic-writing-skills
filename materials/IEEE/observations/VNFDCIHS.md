---
key: VNFDCIHS
title: "CoLLM: Industrial Large–Small Model Collaboration With Fuzzy Decision-Making Agent and Self-Reflection"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2025.3594229"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. METHODS` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORK`，分 large models for time-series 与 collaborative inference）。`related_work=independent`。Introduction 末为三段无编号贡献，无 `The rest of this article is organized` 路标。Method 在 III。Experiments 标题为 `EXPERIMENT`（CMAPSS RUL）。Early-access 页眉页码为 1–11。

## Openers

- abstract: `In industrial applications` — "In industrial applications, large models have exhibited superior generalization capabilities that are unattainable with smaller models." (p.1)
- introduction: `Data-driven industrial intelligence` — "Data-driven industrial intelligence has enabled automated anomaly detection, task planning, and predictive maintenance without relying on expert knowledge [1], [2]." (p.1)
- method: `The fuzzy large-small` — "The fuzzy large-small model collaborative framework employs a cascade inference strategy, adaptively selecting either a large or small model for inference to balance computational efficiency with predictive accuracy." (p.3, III.A)
- experiments: `This section describes` — "This section describes the experimental setup and analysis." (p.6, IV)
- conclusion: `This paper proposes` — "This paper proposes CoLLM, a fuzzy collaborative framework that optimizes computational efficiency and reliability for industrial large models." (p.10)

## Gap transitions

- however (abstract): "However, when faced with edge scenarios and highly diverse industrial samples, their deployment remains challenging due to high computational costs and unreliable output." (p.1)
- to address (abstract): "To address these challenges, we propose CoLLM, a fuzzy large-small model collaborative framework, which dynamically selects between small and large models based on the characteristics exhibited by the samples." (p.1)
- despite (introduction): "Despite their impressive performance, large models still face two major challenges in practical industrial applications." (p.1)
- however (related work): "However, these methods inherently incur substantial inference costs, making real-time inference and deployment on resource-constrained industrial systems challenging." (p.2)
- however (related work): "However, existing methods mainly focus on natural language processing tasks, where routing decisions rely on semantic features such as syntactic complexity and topic consistency." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose CoLLM"; "we propose a fuzzy large-small model collaborative framework"; "This paper proposes CoLLM"
- demonstrate / causal / abstract, conclusion: "Experimental results in industrial time series datasets demonstrate"; "Experiments demonstrate that CoLLM reduces computational costs"
- introduce / causal / related work: "This study introduces a fuzzy neural network (FNN)"
- aim / speculative / conclusion: "We also aim to develop more precise uncertainty estimation methods"

## Cross-section linkers

- introduction → related work: 三段贡献后直接 `II. RELATED WORK`，无独立路标句 (p.2)
- related work → method: "Traditional semantic-based evaluation mechanisms struggle to effectively quantify the processing difficulty of such data." 随后 `III. METHODS` (p.3)
- method → experiments: 三阶段训练后接 `IV. EXPERIMENT` (p.6)
- experiments → conclusion: 大小模型对比段落后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `To address these challenges, we propose CoLLM`，不用 `Here we`。
- R002 独立 Related Work；贡献写在引言末，无编号列表标记。
- R003 Method 标题为 `METHODS`（复数）。
- R004 Experiments 标题为 `EXPERIMENT`（单数）。
- R005 Conclusion 用 `This paper proposes` 收回，再用 `Future work will explore` 指向后续。

## Candidate phrases

- `To address these challenges, we propose CoLLM` (abstract)
- `The main contributions are as follows.` (introduction)
- `This study introduces a fuzzy neural network (FNN) that` (related work)
- `This paper proposes CoLLM, a fuzzy collaborative framework that` (conclusion)
- `Future work will explore integrating CoLLM with` (conclusion)

## House style

自称是 `we propose` / `this paper` / `this study` / `our framework`。未见 `Here we`。`This paper proposes` 与 `we propose CoLLM` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 开篇，结论用 `This paper proposes`。

## Quotes

- p.1 abstract: In industrial applications, large models have exhibited superior generalization capabilities that are unattainable with smaller models.
- p.1 abstract: However, when faced with edge scenarios and highly diverse industrial samples, their deployment remains challenging due to high computational costs and unreliable output.
- p.1 abstract: To address these challenges, we propose CoLLM, a fuzzy large-small model collaborative framework, which dynamically selects between small and large models based on the characteristics exhibited by the samples.
- p.1 abstract: Experimental results in industrial time series datasets demonstrate that our framework improves the computational efficiency of large models up to 14.54x while maintaining or improving prediction accuracy.
- p.1 introduction: Data-driven industrial intelligence has enabled automated anomaly detection, task planning, and predictive maintenance without relying on expert knowledge [1], [2].
- p.1 introduction: Despite their impressive performance, large models still face two major challenges in practical industrial applications.
- p.2 introduction: To address these challenges, we propose a fuzzy large-small model collaborative framework, termed CoLLM, to reduce computational cost while improving reliability for large models.
- p.2 introduction: The main contributions are as follows.
- p.2 related work: However, these methods inherently incur substantial inference costs, making real-time inference and deployment on resource-constrained industrial systems challenging.
- p.2 related work: This study introduces a fuzzy neural network (FNN) that generates confidence scores based on input samples to determine whether to trigger large-model inference.
- p.3 method: The fuzzy large-small model collaborative framework employs a cascade inference strategy, adaptively selecting either a large or small model for inference to balance computational efficiency with predictive accuracy.
- p.6 experiments: This section describes the experimental setup and analysis.
- p.10 conclusion: This paper proposes CoLLM, a fuzzy collaborative framework that optimizes computational efficiency and reliability for industrial large models.
- p.10 conclusion: Experiments demonstrate that CoLLM reduces computational costs of large models by 90% while maintaining accuracy, offering a practical solution for deployment of industrial large models.
- p.10 conclusion: Future work will explore integrating CoLLM with cloud–edge collaboration, where large models are deployed in the cloud and small models at the edge to better balance performance and latency.
