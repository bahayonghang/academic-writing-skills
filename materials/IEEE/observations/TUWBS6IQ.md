---
key: TUWBS6IQ
title: "Comprehensive Production Index Prediction Using Dual-Scale Deep Learning in Mineral Processing"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2024.3421570"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. COMPREHENSIVE PRODUCTION INDEX IN MINERAL PROCESSING` → `III. DUAL-SCALE PREDICTION FOR COMPREHENSIVE PRODUCTION INDEX` → `IV. INDUSTRIAL CASE EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 RNN / difference LSTM / MR-SAE / MENN / HSGN 等）。Introduction 贡献列表后直接进入 II，未见 `The rest of this article is organized`。Method 在 III。Experiments 标题为 `INDUSTRIAL CASE EXPERIMENT`。

## Openers

- abstract: `In mineral processing` — "In mineral processing, the dynamic nature of industrial data poses challenges for decision-makers in accurately assessing current production statuses." (p.1)
- introduction: `IRON ore is` — "IRON ore is a non-renewable mineral resource, which is closely related to the development and construction of the country." (p.1；栏首掉字)
- method: `The high-precision prediction` — "The high-precision prediction of CPIs not only needs to consider the operational decision values (slow process) but also needs to mine the HF dynamic characteristics from the production process data." (p.5, III)
- experiments: `The experimental dataset` — "The experimental dataset comes from the production data of a magnetite concentrator in the last three years." (p.9, IV.A)
- conclusion: `This article tackles` — "This article tackles the challenge of low accuracy in data-driven industrial index prediction models arising from varying data acquisition frequencies in complex industrial processes." (p.13–14)

## Gap transitions

- however (introduction): "However, when faced with industrial data exhibiting varying sampling frequencies, some scholars resort to aggregating HF data into lower frequencies [20] (e.g., averaging or downsampling), employing data dimensionality reduction algorithms [21], feature extraction methods [22], [23], or smoothing low-frequency (LF) data to maintain consistent time series relationships." (p.1)
- nevertheless (introduction): "Nevertheless, these methods often overlook the intrinsic characteristics of the data, leading to limited modeling accuracy." (p.1)
- however (introduction): "However, the method assumes that the process data and quality data exhibit self-correlation or dynamic correlation." (p.2)
- in order to (contributions): "In order to address industrial data with varying sampling frequencies, we devised HFLF units within a dual-scale DL network." (p.2)
- although (conclusion): "Although we use Cloud-Edge collaboration technology for online collaborative prediction and self-tuning DL network, it presents several limitations and potential challenges are listed as follows." (p.14)

## Hedge verbs

- introduce / causal / abstract: "we introduce the high-frequency (HF) unit and low-frequency (LF) unit"
- propose / causal / abstract, introduction: "within our proposed dual-scale deep learning (DL) network"; "We proposed a self-tuning training mechanism"
- validate / causal / abstract, introduction: "Validated through online industrial experiments"; "we validated that the dual-scale modeling method"
- demonstrate / causal / conclusion: "Industrial experiment results demonstrate that the proposed method surpasses the compared neural networks"
- may / speculative / conclusion: "High-latency or low-bandwidth networks may result in delays and inefficiencies in data transmission and model updates."

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. COMPREHENSIVE PRODUCTION INDEX IN MINERAL PROCESSING`，无组织句 (p.2)
- method → experiments: Cloud-Edge 训练机制后 `IV. INDUSTRIAL CASE EXPERIMENT` (p.9)
- experiments → conclusion: 消融实验后 `V. CONCLUSION` (p.13)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R004 贡献用 `The main contributions are summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `Although` 列出局限（隐私、时延、边缘算力）。
- R010 Introduction 末可无 `The rest of this article is organized`，贡献后直接进入领域节。

## Candidate phrases

- `To improve the accuracy of CPIs’ prediction, we introduce` (abstract)
- `The main contributions are summarized as follows.` (introduction)
- `we validated that the dual-scale modeling method proposed in this article` (introduction)
- `This article tackles the challenge of` (conclusion)
- `Although we use Cloud-Edge collaboration technology` (conclusion)

## House style

自称是 `we introduce` / `our proposed` / `proposed in this article` / `This article tackles`。未见 `Here we`、`In this paper`。`proposed in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In mineral processing, the dynamic nature of industrial data poses challenges for decision-makers in accurately assessing current production statuses.
- p.1 abstract: To improve the accuracy of CPIs’ prediction, we introduce the high-frequency (HF) unit and low-frequency (LF) unit within our proposed dual-scale deep learning (DL) network.
- p.1 abstract: Validated through online industrial experiments, our method significantly enhances CPIs’ prediction accuracy compared to the baseline approaches.
- p.1 introduction: IRON ore is a non-renewable mineral resource, which is closely related to the development and construction of the country.
- p.1 introduction: However, when faced with industrial data exhibiting varying sampling frequencies, some scholars resort to aggregating HF data into lower frequencies [20] (e.g., averaging or downsampling), employing data dimensionality reduction algorithms [21], feature extraction methods [22], [23], or smoothing low-frequency (LF) data to maintain consistent time series relationships.
- p.1 introduction: Nevertheless, these methods often overlook the intrinsic characteristics of the data, leading to limited modeling accuracy.
- p.2 introduction: The main contributions are summarized as follows.
- p.2 introduction: Through online experiments conducted in a magnetite concentrator using three years’ worth of industrial data for training, we validated that the dual-scale modeling method proposed in this article for CPIs’ prediction surpasses the performance of the comparison method.
- p.5 method: The high-precision prediction of CPIs not only needs to consider the operational decision values (slow process) but also needs to mine the HF dynamic characteristics from the production process data.
- p.5 method: In this article, we will design a special DL network to model the dual-scale system.
- p.9 experiments: The experimental dataset comes from the production data of a magnetite concentrator in the last three years.
- p.13–14 conclusion: This article tackles the challenge of low accuracy in data-driven industrial index prediction models arising from varying data acquisition frequencies in complex industrial processes.
- p.14 conclusion: Industrial experiment results demonstrate that the proposed method surpasses the compared neural networks in CPIs’ prediction modeling.
- p.14 conclusion: Although we use Cloud-Edge collaboration technology for online collaborative prediction and self-tuning DL network, it presents several limitations and potential challenges are listed as follows.
