---
key: HKL49BUF
title: "Deep Adaptive Input Normalization for Time Series Forecasting"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2019.2944933"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. DEEP ADAPTIVE INPUT NORMALIZATION` → `III. EXPERIMENTAL EVALUATION` → `IV. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 z-score、手工平稳特征、BN / IN / LN / GN）。Introduction 末有 `The rest of the paper is structured as follows` 路标，指向 Section II–IV。PDF 为 6 页 brief 体（页码 1–6）。Experiments 标题为 `EXPERIMENTAL EVALUATION`。结论节标题为 `CONCLUSIONS`。

## Openers

- abstract: `Deep Learning (DL) models` — "Deep Learning (DL) models can be used to tackle time series analysis tasks with great success." (p.1)
- introduction: `Forecasting time series is` — "Forecasting time series is an increasingly important topic, with several applications in various domains [1], [5], [13], [15], [16], [19], [23], [34]." (p.1)
- method: `The goal of the proposed` — "The goal of the proposed method is to learn how the measurements should be normalized by appropriately shifting and scaling them:" (p.2, II)
- experiments: `For evaluating the proposed` — "For evaluating the proposed method a challenging large-scale dataset (FI-2010), that contains limit order book data, was employed [20]." (p.3)
- conclusion: `A deep adaptive normalization` — "A deep adaptive normalization method, that can be trained in an end-to-end fashion, was proposed in this paper." (p.6)

## Gap transitions

- however (abstract): "However, the performance of DL models can degenerate rapidly if the data are not appropriately normalized." (p.1)
- however (introduction): "However, applying deep learning models to time series is challenging due to the non-stationary and multimodal nature of the data." (p.1)
- however (introduction): "However, z-score normalization is unable to efficiently handle non-stationary time series, since the statistics used for the normalization are fixed both during the training and inference." (p.1)
- even though (introduction): "Even though these approaches can indeed lead to slightly better performance when used to train deep learning models, they exhibit significant drawbacks, since they are largely based on heuristically-designed normalization/feature extraction schemes" (p.1)
- to overcome (introduction): "To overcome these limitations, we propose a Deep Adaptive Input Normalization (DAIN) layer that is capable of a) learning how the data should be normalized and b) adaptively changing the applied normalization scheme during inference, according to the distribution of the measurements of the current time series, allowing for effectively handling non-stationary and multimodal data." (p.1)

## Hedge verbs

- propose / causal / abstract, introduction: "a simple, yet effective, neural layer ... is proposed"; "we propose a Deep Adaptive Input Normalization (DAIN) layer"
- demonstrate / causal / abstract, method: "The effectiveness of the proposed method is demonstrated using a large-scale limit order book dataset"; "as also experimentally demonstrated in Section III"
- differ / causal / abstract: "The proposed method differs from traditional normalization methods since it learns how to perform normalization for a given task instead of using a fixed normalization scheme."
- outperform / causal / conclusion: "The proposed method consistently outperformed all the other evaluated normalization approaches."
- can be employed / speculative / conclusion: "alternative and potentially stabler learning approaches, e.g., multiplicative weight updates, can be employed"

## Cross-section linkers

- introduction → method: "The rest of the paper is structured as follows. First, the proposed method is analytically described in Section II. Then, an extensive experimental evaluation is provided in Section III, while conclusions are drawn in Section IV." (p.2)
- method → experiments: 学习率说明后 `III. EXPERIMENTAL EVALUATION` (p.3)
- experiments → conclusion: 超参数段落后 `IV. CONCLUSIONS` (p.6)

## Candidate rules

- R001 abstract 用被动 `is proposed`；开篇 `However` 指向归一化失效。
- R002 Introduction 无独立 Related Work，归一化与 BN/IN 评述写在引言中段。
- R003 Introduction 末用 `The rest of the paper is structured as follows`（brief / 预印本体用 `paper`）。
- R008 宣称 `To the best of our knowledge this is the first time that an adaptive and trainable normalization scheme is proposed`。
- R005 Conclusion 用 `was proposed in this paper` 收回，再用 `There are several interesting future research direction`。

## Candidate phrases

- `In this work, a simple, yet effective, neural layer ... is proposed` (abstract)
- `To overcome these limitations, we propose a Deep Adaptive Input Normalization (DAIN) layer` (introduction)
- `The main contribution of this work is the proposal of` (introduction)
- `The rest of the paper is structured as follows.` (introduction)
- `A deep adaptive normalization method, that can be trained in an end-to-end fashion, was proposed in this paper.` (conclusion)
- `There are several interesting future research direction.` (conclusion)

## House style

自称 `In this work` / `we propose` / `this work` / `this paper`（PDF brief 体）。未见 `Here we`。`In this work ... is proposed` 与 `was proposed in this paper` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this article`。

## Quotes

- p.1 abstract: Deep Learning (DL) models can be used to tackle time series analysis tasks with great success.
- p.1 abstract: However, the performance of DL models can degenerate rapidly if the data are not appropriately normalized.
- p.1 abstract: In this work, a simple, yet effective, neural layer, that is capable of adaptively normalizing the input time series, while taking into account the distribution of the data, is proposed.
- p.1 abstract: The proposed method differs from traditional normalization methods since it learns how to perform normalization for a given task instead of using a fixed normalization scheme.
- p.1 abstract: The effectiveness of the proposed method is demonstrated using a large-scale limit order book dataset, as well as a load forecasting dataset.
- p.1 introduction: Forecasting time series is an increasingly important topic, with several applications in various domains [1], [5], [13], [15], [16], [19], [23], [34].
- p.1 introduction: However, applying deep learning models to time series is challenging due to the non-stationary and multimodal nature of the data.
- p.1 introduction: However, z-score normalization is unable to efficiently handle non-stationary time series, since the statistics used for the normalization are fixed both during the training and inference.
- p.1 introduction: To overcome these limitations, we propose a Deep Adaptive Input Normalization (DAIN) layer that is capable of a) learning how the data should be normalized and b) adaptively changing the applied normalization scheme during inference, according to the distribution of the measurements of the current time series, allowing for effectively handling non-stationary and multimodal data.
- p.1 introduction: The main contribution of this work is the proposal of a deep learning layer that learns how the data should be normalized according to their distribution instead of using fixed normalization schemes.
- p.2 introduction: To the best of our knowledge this is the first time that an adaptive and trainable normalization scheme is proposed and effectively used in deep neural networks.
- p.2 introduction: The rest of the paper is structured as follows. First, the proposed method is analytically described in Section II. Then, an extensive experimental evaluation is provided in Section III, while conclusions are drawn in Section IV.
- p.2 method: The goal of the proposed method is to learn how the measurements should be normalized by appropriately shifting and scaling them:
- p.3 experiments: For evaluating the proposed method a challenging large-scale dataset (FI-2010), that contains limit order book data, was employed [20].
- p.4 experiments: First, an ablation study was performed to identify the effect of each normalization sub-layer on the performance of the proposed method.
- p.6 conclusion: A deep adaptive normalization method, that can be trained in an end-to-end fashion, was proposed in this paper.
- p.6 conclusion: The proposed method consistently outperformed all the other evaluated normalization approaches.
- p.6 conclusion: There are several interesting future research direction.
