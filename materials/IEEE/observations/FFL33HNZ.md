---
key: FFL33HNZ
title: "Quality-Driven Regularization for Deep Learning Networks and Its Application to Industrial Soft Sensors"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2022.3144162"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BACKGROUND` → `III. QUALITY-DRIVEN REGULARIZATION FOR SAE` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR/PLSR/ANN/SVR、SAE、DBN、HELM、L2、VW-SAE）。Introduction 贡献段落后直接 `II. BACKGROUND`，未见 `The rest of this article is organized`。Method 在 III。Experiments 标题为 `CASE STUDY`（加氢裂化航空煤油）。

## Openers

- abstract: `The growth of` — "The growth of data collection in industrial processes has led to a renewed emphasis on the development of data-driven soft sensors." (p.1)
- introduction: `IN THE process` — "IN THE process industry, advanced, optimized control is widely used to proper production to extract maximal economic benefits [1]–[3]." (p.1；栏首掉字)
- method: `Training a traditional` — "Training a traditional SAE requires two steps: an unsupervised layer-by-layer pretraining and a supervised fine-tuning of the network parameters." (p.3, III)
- experiments: `In this section` — "In this section, several comparisons are performed to evaluate the effectiveness of the proposed QR-SAE model in an industrial hydrocracking process." (p.5, IV)
- conclusion: `This article proposes` — "This article proposes applying a special regularization of deep learning to improve the performance of an SAE." (p.9)

## Gap transitions

- however (introduction): "However, online, real-time sensors for these variables are often expensive, difficult to maintain, or have considerable time delay." (p.1)
- to solve (introduction): "To solve these problems, soft sensors have been developed to indirectly estimate those quality variables that are difficult or expensive to measure by establishing mathematical models with other easier-to-measure variables." (p.1)
- in fact (introduction): "In fact, during the unsupervised pretraining of deep neural networks (NNs), it is often difficult to extract output-related features [24], [26]." (p.2)
- to solve (introduction): "To solve this problem, the network parameters must be trained under specific and well-defined constraints in order to eliminate the blindness of the pretraining stage [27]." (p.2)
- however (introduction): "However, in L2-regularization, all network weights have the same constraints." (p.2)
- however (conclusion): "However, it is still a difficult problem for network hyperparameter optimization in practical application scenarios with low-quality data." (p.9)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a new quality-driven regularization (QR) is proposed"; "This article proposes applying a special regularization"
- develop / causal / abstract: "a QR-based SAE (QR-SAE) is developed"
- show / causal / abstract, conclusion: "Comparative experiments show that QR-SAE can extract quality-related features"; "The results show that the QR-SAE achieves the best prediction performance."
- compare / causal / introduction: "Compared with these works, the main contributions of this article are threefold."

## Cross-section linkers

- introduction → method: 贡献段落后直接 `II. BACKGROUND`，无组织句 (p.2)
- method → experiments: 评测指标后 `IV. CASE STUDY` (p.5)
- experiments → conclusion: 预训练相关分析后 `V. CONCLUSION` (p.9)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R004 贡献用 `the main contributions of this article are threefold` 段落枚举。
- R005 Conclusion 先收回方法，再用 `However` 承认局限，`Future work will focus on`。
- R010 Introduction 末可无组织句，贡献后直接进入 `II. BACKGROUND`。

## Candidate phrases

- `In this article, a new quality-driven regularization (QR) is proposed` (abstract)
- `Compared with these works, the main contributions of this article are threefold.` (introduction)
- `In this section, several comparisons are performed to evaluate` (experiments)
- `This article proposes applying a special regularization` (conclusion)
- `Future work will focus on extending the proposed method` (conclusion)

## House style

自称是 `In this article` / `This article proposes` / `the proposed QR-SAE`。未见 `Here we`、`In this paper`。`In this article` / `This article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The growth of data collection in industrial processes has led to a renewed emphasis on the development of data-driven soft sensors.
- p.1 abstract: In this article, a new quality-driven regularization (QR) is proposed for deep networks to learn quality-related features from industrial process data.
- p.1 abstract: Comparative experiments show that QR-SAE can extract quality-related features and achieve accurate prediction performance.
- p.1 introduction: IN THE process industry, advanced, optimized control is widely used to proper production to extract maximal economic benefits [1]–[3].
- p.1 introduction: However, online, real-time sensors for these variables are often expensive, difficult to maintain, or have considerable time delay.
- p.1 introduction: To solve these problems, soft sensors have been developed to indirectly estimate those quality variables that are difficult or expensive to measure by establishing mathematical models with other easier-to-measure variables.
- p.2 introduction: In fact, during the unsupervised pretraining of deep neural networks (NNs), it is often difficult to extract output-related features [24], [26].
- p.2 introduction: To alleviate these problems, a new quality-driven regularization (QR) is proposed for quality-related feature learning in this article.
- p.2 introduction: Compared with these works, the main contributions of this article are threefold.
- p.3 method: Training a traditional SAE requires two steps: an unsupervised layer-by-layer pretraining and a supervised fine-tuning of the network parameters.
- p.5 experiments: In this section, several comparisons are performed to evaluate the effectiveness of the proposed QR-SAE model in an industrial hydrocracking process.
- p.9 conclusion: This article proposes applying a special regularization of deep learning to improve the performance of an SAE.
- p.9 conclusion: The results show that the QR-SAE achieves the best prediction performance.
- p.9 conclusion: However, it is still a difficult problem for network hyperparameter optimization in practical application scenarios with low-quality data.
- p.9 conclusion: Future work will focus on extending the proposed method in more complex scenarios such as with low-quality data that contain a large number of missing and noise values.
