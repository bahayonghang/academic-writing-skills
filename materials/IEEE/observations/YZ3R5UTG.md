---
key: YZ3R5UTG
title: "FDformer: A Fuzzy Dynamic Transformer-Based Network for Efficient Industrial Time Series Prediction"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2025.3549920"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. FDFORMER-BASED NETWORK` → `IV. EXPERIMENTAL SETUP` → `V. EXPERIMENTS ANALYSIS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORK`，分 efficient networks / fuzzy–deep fusion / dynamic early-exit training）。`related_work=independent`。Introduction 末为编号贡献，无 `The rest of this article is organized` 路标。Method 标题为 `FDFORMER-BASED NETWORK`。Experiments 拆为 `EXPERIMENTAL SETUP` 与 `EXPERIMENTS ANALYSIS`。

## Openers

- abstract: `Industrial time series` — "Industrial time series prediction is highly important for the predictive maintenance of Industrial Internet of Things (IIoT) devices." (p.1)
- introduction: `Predictive maintenance for` — "Predictive maintenance for the Industrial Internet of Things (IIoT) is essential to improve system reliability, enhance operational safety, and reduce maintenance costs." (p.1)
- method: `In this section` — "In this section, we first describe the overall architecture of FDformer and then present the proposed approach in detail." (p.3, III)
- experiments: `We implemented typical` — "We implemented typical neural networks (LSTM, DNN, and Transformer) and their fuzzy dynamic architectures (FD-LSTM, FD-DNN, and FDformer) on each of the four widely used subsets in CMAPSS." (p.8, V.A)
- conclusion: `This paper presents` — "This paper presents a fuzzy dynamic Transformer-based network (FDformer) for efficient industrial time series prediction." (p.11)

## Gap transitions

- however (abstract): "However, time series data from complex industrial scenarios often contain substantial uncertainty." (p.1)
- moreover (abstract): "Moreover, existing static methods often fail to meet the real-time requirements of industrial environments." (p.1)
- to address (abstract): "To address the challenges, this study introduces fuzzy learning into deep learning models to overcome the drawbacks of fixed model representations." (p.1)
- however (related work): "However, most existing dynamic methods are applicable to classification tasks and do not extend to industrial time-series regression problems, where the prediction is RUL for a specific value." (p.2)
- however (related work): "However, to the best of our knowledge, no existing work proposes a fusion model of fuzzy systems with time series dynamic neural networks." (p.2)

## Hedge verbs

- introduce / causal / abstract: "this study introduces fuzzy learning into deep learning models"
- propose / causal / abstract, introduction: "we propose a fuzzy dynamic transformer (FDformer)"; "we propose a fuzzy dynamic Transformer-based network (FDformer)"
- indicate / causal / abstract: "Experiments on multiple datasets indicate that FDformer achieves minimal computational costs"
- demonstrate / causal / introduction: "Experiments on multiple datasets demonstrate that the proposed FDformer significantly accelerates computation"
- will / speculative / conclusion: "In the future, we will explore adaptive fuzzy logic adjustment methods"

## Cross-section linkers

- introduction → related work: 编号贡献后直接 `II. RELATED WORK`，无独立路标句 (p.2)
- related work → method: 训练方法讨论后接 `III. FDFORMER-BASED NETWORK` (p.3)
- method → setup: 训练算法后接 `IV. EXPERIMENTAL SETUP` (p.6)
- setup → experiments: 超参数与 FLOPs 后接 `V. EXPERIMENTS ANALYSIS` (p.8)
- experiments → conclusion: 动态损失权重段落后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `this study introduces` / `we propose`，不用 `Here we`。
- R002 独立 Related Work；引言中段按 uncertainty / compute / early-exit 三条问题推进。
- R003 贡献用 `Our contributions are summarized as follows:` + 编号列表。
- R004 Experiments 拆为 `EXPERIMENTAL SETUP` 与 `EXPERIMENTS ANALYSIS`。
- R005 Conclusion 用 `This paper presents` 收回方法，再用 `In the future, we will` 指向后续。

## Candidate phrases

- `To address the challenges, this study introduces` (abstract)
- `Therefore, we propose a fuzzy dynamic transformer (FDformer)` (abstract)
- `To overcome these challenges, we propose a fuzzy dynamic Transformer-based network (FDformer)` (introduction)
- `Our contributions are summarized as follows:` (introduction)
- `This paper presents a fuzzy dynamic Transformer-based network (FDformer)` (conclusion)
- `In the future, we will explore adaptive fuzzy logic adjustment methods` (conclusion)

## House style

自称是 `this study introduces` / `we propose` / `This paper presents` / `our proposed FDformer`。未见 `Here we`。`this study introduces` 与 `This paper presents` 进 phrase_bank，不进 anti_ai_patterns。结论用现在时 `This paper presents`。

## Quotes

- p.1 abstract: Industrial time series prediction is highly important for the predictive maintenance of Industrial Internet of Things (IIoT) devices.
- p.1 abstract: However, time series data from complex industrial scenarios often contain substantial uncertainty.
- p.1 abstract: To address the challenges, this study introduces fuzzy learning into deep learning models to overcome the drawbacks of fixed model representations.
- p.1 abstract: Therefore, we propose a fuzzy dynamic transformer (FDformer) that can adaptively adjust network depth according to the complexity of individual samples.
- p.1 abstract: Experiments on multiple datasets indicate that FDformer achieves minimal computational costs and excellent prediction accuracy across multiple datasets, outperforming state-of-the-art algorithms.
- p.1 introduction: Predictive maintenance for the Industrial Internet of Things (IIoT) is essential to improve system reliability, enhance operational safety, and reduce maintenance costs.
- p.2 introduction: To overcome these challenges, we propose a fuzzy dynamic Transformer-based network (FDformer) that incorporates fuzzy systems as part of the representation vector learning mechanism for dynamic neural networks.
- p.2 introduction: Our contributions are summarized as follows:
- p.2 related work: However, most existing dynamic methods are applicable to classification tasks and do not extend to industrial time-series regression problems, where the prediction is RUL for a specific value.
- p.2 related work: However, to the best of our knowledge, no existing work proposes a fusion model of fuzzy systems with time series dynamic neural networks.
- p.3 method: In this section, we first describe the overall architecture of FDformer and then present the proposed approach in detail.
- p.6 setup: IV. EXPERIMENTAL SETUP
- p.8 experiments: We implemented typical neural networks (LSTM, DNN, and Transformer) and their fuzzy dynamic architectures (FD-LSTM, FD-DNN, and FDformer) on each of the four widely used subsets in CMAPSS.
- p.11 conclusion: This paper presents a fuzzy dynamic Transformer-based network (FDformer) for efficient industrial time series prediction.
- p.11 conclusion: Experimental results on multiple datasets show that FDformer significantly reduces computational costs and achieves outstanding performance.
- p.11 conclusion: In the future, we will explore adaptive fuzzy logic adjustment methods to address the challenges posed by data of varying quality in complex industrial scenarios.
