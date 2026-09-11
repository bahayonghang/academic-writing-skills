---
key: P6N4JAUP
title: "A Lightweight Group Transformer-Based Time Series Reduction Network for Edge Intelligence and Its Application in Industrial RUL Prediction"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2023.3347227"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. LIGHTWEIGHT GT-MRNET` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`：A. Deep Learning for RUL Prediction；B. Model Compression）。Introduction 末有 `The rest of this article is organized as follows.`。Method 在 III。Experiments 标题为 `EXPERIMENT`（N-CMAPSS）。

## Openers

- abstract: `Recently, deep learning-based` — "Recently, deep learning-based models such as transformer have achieved significant performance for industrial remaining useful life (RUL) prediction due to their strong representation ability." (p.1)
- introduction: `REMAINING useful life` — "REMAINING useful life (RUL) prediction [1], [2], as a crucial aspect in smart manufacturing, can provide early warning information before equipment failure, thus saving maintenance time and reducing maintenance cost." (p.1；栏首掉字)
- related work: `Deep learning-based methods` — "Deep learning-based methods have achieved superior performance, such as long short-term memory (LSTM) [7], [8], CNNs [10], [11], and transformer [15], [16], [17]." (p.2, II.A)
- method: `The framework of` — "The framework of the proposed GT-MRNet is structured by lightweight group transformer blocks, time-series reduction strategy, and multihierarchy learning layer." (p.3, III)
- experiments: `A series of` — "A series of experiments is carried out in this section. All experiments are performed on a workstation equipped with an AMD Ryzen 9 5950X 3.40-GHz CPU with 16 cores and an NVIDIA GeForce GTX 3090 GPU." (p.5, IV)
- conclusion: `In this article` — "In this article, a novel lightweight GT-MRNet method was proposed for edge intelligence in RUL prediction." (p.9)

## Gap transitions

- however (abstract): "However, the high computational cost of deep learning models makes it difficult to meet the requirements of edge intelligence." (p.1)
- however (introduction): "However, their high computational cost and even millions of parameters make it difficult to meet the real-time requirements of practical industrial scenarios." (p.1)
- however (introduction): "However, it is worth noting that most existing model compression methods primarily focus on reducing the complexity of network structure by compressing the network [20], [21], [22] or pruning the network architecture [18], [19]." (p.2)
- different from (introduction): "Different from DLformer [2] simply selecting a fixed time series, we desire to develop a lightweight network with adaptive time series pruning to solve the mentioned two problems in industrial edge scenarios." (p.2)
- however (related work): "However, transformer-based models tend to be computationally intensive and contain millions of parameters, making them unsuitable for deployment on devices with limited computing resources." (p.2)
- however (related work): "However, most of these existing methods focus on the spatial redundancy or temporal redundancy of videos or texts." (p.2–3)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a lightweight group transformer with multihierarchy time-series reduction (GT-MRNet) is proposed"; "a novel lightweight GT-MRNet method was proposed"
- demonstrate / causal / abstract: "Extensive experimental results on the real-world condition datasets demonstrate that the proposed method can significantly reduce up to 74.7% parameters and 91.8% computation cost without sacrificing accuracy."
- verify / causal / experiments: "To verify the superiority of the proposed methods, other state-of-the-art methods are employed"
- may / speculative / conclusion: "Future work may focus on the deployment of lightweight networks in cloud-edge scenarios."

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II introduces the related work about the methods for RUL prediction and model compression. Section III describes the proposed network in detail. In Section IV, the experimental setting and results are presented. Finally, Section V concludes this article." (p.2)
- related work → method: "Moreover, to the authors’ best knowledge, this is the first time to explore time-series reduction in RUL prediction." 随后 `III. LIGHTWEIGHT GT-MRNET` (p.3)
- method → experiments: Algorithm 2 后 `IV. EXPERIMENT` (p.5)
- experiments → conclusion: 效率分析后 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 独立 Related Work 用 `II. RELATED WORKS` 分 A/B 子节。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contribution can be summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `Future work may focus on`。

## Candidate phrases

- `In this article, a lightweight group transformer ... is proposed` (abstract)
- `Different from most existing RUL methods computing all time series` (abstract)
- `The rest of this article is organized as follows.` (introduction)
- `To the authors’ best knowledge, this is the first time to explore` (introduction)
- `In this article, a novel lightweight GT-MRNet method was proposed` (conclusion)

## House style

自称是 `In this article` / `the proposed GT-MRNet` / `we desire to develop`。未见 `Here we`、`In this paper`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Recently, deep learning-based models such as transformer have achieved significant performance for industrial remaining useful life (RUL) prediction due to their strong representation ability.
- p.1 abstract: However, the high computational cost of deep learning models makes it difficult to meet the requirements of edge intelligence.
- p.1 abstract: In this article, a lightweight group transformer with multihierarchy time-series reduction (GT-MRNet) is proposed to alleviate this problem.
- p.1 abstract: Different from most existing RUL methods computing all time series, GT-MRNet can adaptively select necessary time steps to compute the RUL.
- p.1 abstract: Extensive experimental results on the real-world condition datasets demonstrate that the proposed method can significantly reduce up to 74.7% parameters and 91.8% computation cost without sacrificing accuracy.
- p.1 introduction: REMAINING useful life (RUL) prediction [1], [2], as a crucial aspect in smart manufacturing, can provide early warning information before equipment failure, thus saving maintenance time and reducing maintenance cost.
- p.1 introduction: However, their high computational cost and even millions of parameters make it difficult to meet the real-time requirements of practical industrial scenarios.
- p.2 introduction: Different from DLformer [2] simply selecting a fixed time series, we desire to develop a lightweight network with adaptive time series pruning to solve the mentioned two problems in industrial edge scenarios.
- p.2 introduction: The rest of this article is organized as follows. Section II introduces the related work about the methods for RUL prediction and model compression. Section III describes the proposed network in detail. In Section IV, the experimental setting and results are presented. Finally, Section V concludes this article.
- p.2 related work: However, transformer-based models tend to be computationally intensive and contain millions of parameters, making them unsuitable for deployment on devices with limited computing resources.
- p.3 method: The framework of the proposed GT-MRNet is structured by lightweight group transformer blocks, time-series reduction strategy, and multihierarchy learning layer.
- p.5 experiments: A series of experiments is carried out in this section. All experiments are performed on a workstation equipped with an AMD Ryzen 9 5950X 3.40-GHz CPU with 16 cores and an NVIDIA GeForce GTX 3090 GPU.
- p.9 experiments: In conclusion, the GT-MRNet reduces 91.8% FLOPs, 74.7% Params, 12.4% GPU running time, and 79.3% CPU running time compared to transformer
- p.9 conclusion: In this article, a novel lightweight GT-MRNet method was proposed for edge intelligence in RUL prediction.
- p.9 conclusion: Future work may focus on the deployment of lightweight networks in cloud-edge scenarios.
