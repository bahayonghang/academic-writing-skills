---
key: CB9J8LZP
title: "A Spatiotemporal Masked Pre-Training Framework for Nonlinear Dynamic Soft Sensor Development"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3586271"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROBLEM STATEMENT` → `IV. GRAPH-BASED MEMORY UNIT` → `V. SPATIOTEMPORAL MASKED PRE-TRAINING` → `VI. SMPT-BASED SOFT SENSOR DEVELOPMENT` → `VII. CASE STUDY` → `VIII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLS/ELM/GPR、LSTM/GRU/TCN、CNN/GCN 与 spatiotemporal models）。Introduction 末有编号贡献与节序路标。Method 为 IV–VI。Experiments 标题为 `CASE STUDY`（debutanizer + wind power）。early-access 页码 1–11。

## Openers

- abstract: `Data-driven soft` — "Data-driven soft sensors are extensively applied to predicting quality indicators." (p.1)
- introduction: `IN practical industrial` — "IN practical industrial production processes, the accurate and real-time measurement of crucial quality indicators occupies a significant role in process monitoring and feedback control [1]–[3]." (p.1；栏首掉字)
- method: `For a batch` — "For a batch of N time series X = {X_n}_{n=1}^N, several masked series can be generated for each sample X_i via masking a portion of time points randomly, formalizing by:" (p.4, V.A)
- experiments: `In this section` — "In this section, experiments are conducted on a debutanizer column case and a wind power prediction case." (p.5, VII)
- conclusion: `In this article` — "In this article, a soft sensing approach SMPT is proposed for predicting industrial key indicators." (p.10)

## Gap transitions

- nevertheless (abstract): "Nevertheless, most of them suffer from the intricate characteristics of spatiotemporal coupling relations, which hammers their widespread application in process industries." (p.1)
- however (introduction): "However, these works individually and independently model the process variables and time steps, which may prevent them from learning good feature representations of complex temporal and spatial patterns within industrial data." (p.1)
- although (introduction): "Although these approaches encode local spatial dependencies through a graph structure or network architectures, they treat distinct time steps individually and may result in the absence of temporal feature representations." (p.2)
- despite (introduction): "Despite the rapid progress of spatiotemporal modeling techniques, there are two remaining problems in their practical applications:" (p.2)
- however (introduction): "However, most of spatiotemporal models overlook such correlations among different process variables at different time steps and tend to handle the temporal and spatial patterns independently and separately, leading to unsatisfactory prediction results in soft sensing tasks." (p.2)

## Hedge verbs

- present / causal / abstract: "this paper presents a spatiotemporal masked pre-training (SMPT) framework"
- propose / causal / introduction, conclusion: "a spatiotemporal masked pre-training (SMPT) framework is proposed"; "a soft sensing approach SMPT is proposed"
- demonstrate / causal / abstract: "the proposed SMPT empirically presents superior results"
- confirm / causal / experiments: "The results empirically confirm the advantage of our proposed SMPT over it peers."
- validate / causal / conclusion: "The feasibility and effectiveness of SMPT are validated on two industrial datasets."

## Cross-section linkers

- introduction → method: "The rest of this article is structured as follows. In Section II, related preliminaries are introduced. Followed by a problem statement in Section III. Section IV details GMU. Details of the proposed SMPT are given in Section V. Section VI demonstrates the SMPT-based soft sensing. In Section VII, the effectiveness of SMPT is demonstrated by two industrial cases. Eventually, Section VIII concludes this article." (p.2)
- method → experiments: "Overview, the SMPT-based soft sensor algorithm is provided by Algorithm 1, and its flowchart is shown in Fig. 1." 随后 `VII. CASE STUDY` (p.5)
- experiments → conclusion: 噪声稳健性段落后直接 `VIII. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `this paper presents` 引出框架缩写，再用 `To handle those characteristics`。
- R002 Introduction 无独立 Related Work；贡献用 `This article mainly contributes in the following aspects` + 编号列表。
- R003 Introduction 末用 `The rest of this article is structured as follows` 指向 II–VIII。
- R004 Experiments 标题为 `CASE STUDY`，开篇 `In this section, experiments are conducted on`。
- R005 Conclusion 先 `In this article, a ... is proposed`，再用 `For future research`。

## Candidate phrases

- `this paper presents` (abstract)
- `To handle those characteristics` (abstract)
- `This article mainly contributes in the following aspects:` (introduction)
- `The rest of this article is structured as follows.` (introduction)
- `In this article, a soft sensing approach SMPT is proposed` (conclusion)

## House style

自称是 `this paper presents` / `this article` / `we proposed` / `the proposed SMPT` / `our proposed SMPT`。未见 `Here we`。`this paper presents` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。摘要用 `this paper`，结论用 `this article`。

## Quotes

- p.1 abstract: Data-driven soft sensors are extensively applied to predicting quality indicators.
- p.1 abstract: Nevertheless, most of them suffer from the intricate characteristics of spatiotemporal coupling relations, which hammers their widespread application in process industries.
- p.1 abstract: To handle those characteristics, this paper presents a spatiotemporal masked pre-training (SMPT) framework for soft sensing, which eases the masked modeling and guides the feature representation learning.
- p.1 abstract: Compared with nine state-of-the-art (SOTA) methods, the proposed SMPT empirically presents superior results on two industrial datasets, yielding relative reductions in mean absolute error (MAE) of 18.0% and 9.0% over the second-best methods on the two datasets, respectively.
- p.1 introduction: IN practical industrial production processes, the accurate and real-time measurement of crucial quality indicators occupies a significant role in process monitoring and feedback control [1]–[3].
- p.1 introduction: However, these works individually and independently model the process variables and time steps, which may prevent them from learning good feature representations of complex temporal and spatial patterns within industrial data.
- p.2 introduction: Although these approaches encode local spatial dependencies through a graph structure or network architectures, they treat distinct time steps individually and may result in the absence of temporal feature representations.
- p.2 introduction: Despite the rapid progress of spatiotemporal modeling techniques, there are two remaining problems in their practical applications:
- p.2 introduction: This article mainly contributes in the following aspects:
- p.2 introduction: The rest of this article is structured as follows. In Section II, related preliminaries are introduced. Followed by a problem statement in Section III. Section IV details GMU. Details of the proposed SMPT are given in Section V. Section VI demonstrates the SMPT-based soft sensing. In Section VII, the effectiveness of SMPT is demonstrated by two industrial cases. Eventually, Section VIII concludes this article.
- p.4 method: For a batch of N time series X = {X_n}_{n=1}^N, several masked series can be generated for each sample X_i via masking a portion of time points randomly, formalizing by:
- p.5 experiments: In this section, experiments are conducted on a debutanizer column case and a wind power prediction case.
- p.7 experiments: The results empirically confirm the advantage of our proposed SMPT over it peers.
- p.10 conclusion: In this article, a soft sensing approach SMPT is proposed for predicting industrial key indicators.
- p.10 conclusion: Compared with nine SOTA methods, SMPT demonstrates superior prediction accuracy. It achieves relative reductions in MAE of 18.0% and 9.0% over the second-best methods on the two datasets, respectively.
- p.10 conclusion: For future research, it is worth exploring more effective masked time series generation strategies.
