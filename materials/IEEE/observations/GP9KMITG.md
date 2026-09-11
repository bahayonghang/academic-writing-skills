---
key: GP9KMITG
title: "BTFormer: A BNN-Based Trend-Aware Time-Series Prediction Model for Industrial Intelligence"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3452181"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. TREND-AWARE BINARY TRANSFORMER FOR INDUSTRIAL TIME-SERIES PREDICTION` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（II.A Industrial Time-Series Prediction；II.B Binary Transformer；II.C Bottleneck of the Binary Transformer）。Introduction 末有节序路标，指向 II–V。Method 在正文中段。Experiments 标题为 `EXPERIMENT`。

## Openers

- abstract: `Prediction of industrial` — "Prediction of industrial time-series is crucial for various Industrial Internet of Things applications." (p.14381)
- introduction: `IN THE Industrial` — "IN THE Industrial Internet of Things, time-series is the primary form of data used in various applications such as remaining useful life (RUL) prediction [1], fault diagnosis [2], and activity recognition [3]." (p.14381；栏首掉字)
- related_work: `Transformer-based time-series` — "Transformer-based time-series prediction has seen rapid advancements in industrial applications [14]." (p.14382, II.A)
- method: `BTFormer has been` — "BTFormer has been proposed in this article to reduce the Mb requirements and improve computational efficiency while maintaining high accuracy." (p.14383, III.A)
- experiments: `RUL prediction and` — "RUL prediction and action recognition are two fundamental tasks in time-series prediction." (p.14386)
- conclusion: `This article proposes` — "This article proposes BTFormer, a binary transformer model for industrial time-series prediction, addressing three key challenges: binary attention information loss, trend information capture, and training process mismatch." (p.14389)

## Gap transitions

- despite (abstract): "Despite the high accuracy of deep learning methods for time-series prediction, the significant memory requirements of deep learning models pose a challenge for the limited computational resources of industrial edge devices." (p.14381)
- to address (abstract): "To address this issue, this work proposes BTFormer, which achieves a high compression rate while maintaining competitive performance." (p.14381)
- however (introduction): "However, in real industrial scenarios, time-series prediction tasks are typically characterized by resource constraints alongside high requirements for real-time processing and accuracy." (p.14381)
- therefore (introduction): "Therefore, it is significant to propose an approach that aims to realize an industrial time-series prediction model with low memory, low-computational complexity, and high accuracy simultaneously." (p.14382)
- however (related work): "However, the transformer architecture inherently has a large model size and computational complexity, which poses a challenge for adapting to resource-constrained edge devices." (p.14382)
- to address (related work): "To address this issue, three mainstream model compression techniques are proposed: pruning [16], quantization [11], and knowledge distillation (KD)[17]." (p.14382)
- in summary (related work): "In summary, existing transformer-based time-series prediction models still face significant challenges in terms of memory requirements and computational complexity." (p.14383)

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "this work proposes BTFormer"; "we propose BTFormer"; "BTFormer has been proposed in this article"; "This article proposes BTFormer"
- demonstrate / causal / abstract: "The experiments demonstrate that BTFormer effectively reduces model memory usage"
- show / causal / introduction, conclusion: "The results show that the BTFormer better fits the attention probabilities"; "Experiments show that BTFormer achieves a 31.0 times reduction"

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II describes related research work. Section III provides a detailed explanation of the proposed methodology. Section IV validates the effectiveness of BTFormer through extensive experiments. Finally, Section V concludes this article." (p.14382)
- related work → method: "Addressing issues such as attention degradation, representation ability decreasing, and optimization mismatch in binary transformers is essential, serving as the primary motivation for this article." 随后 `III. TREND-AWARE BINARY TRANSFORMER` (p.14383)
- method → experiments: Algorithm 3 后直接 `IV. EXPERIMENT` (p.14386)
- experiments → conclusion: 训练曲线段落后直接 `V. CONCLUSION` (p.14389)

## Candidate rules

- R001 摘要用 `this work proposes`。
- R002 本篇有独立 `II. RELATED WORK`，计入 SP-IEEE-001。
- R003 Introduction 末 `The rest of this article is organized as follows`。
- R004 贡献用 `The specific contributions are as follows.` + 编号列表。
- R005 结论 `Future research will explore` + `software and hardware codesign`。

## Candidate phrases

- `To address this issue, this work proposes` (abstract)
- `The specific contributions are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article proposes BTFormer` (conclusion)
- `Future research will explore` (conclusion)

## House style

自称 `this work proposes` / `we propose` / `this article proposes` / `BTFormer has been proposed in this article`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.14381 abstract: Prediction of industrial time-series is crucial for various Industrial Internet of Things applications.
- p.14381 abstract: Despite the high accuracy of deep learning methods for time-series prediction, the significant memory requirements of deep learning models pose a challenge for the limited computational resources of industrial edge devices.
- p.14381 abstract: To address this issue, this work proposes BTFormer, which achieves a high compression rate while maintaining competitive performance.
- p.14381 introduction: IN THE Industrial Internet of Things, time-series is the primary form of data used in various applications such as remaining useful life (RUL) prediction [1], fault diagnosis [2], and activity recognition [3].
- p.14381 introduction: However, in real industrial scenarios, time-series prediction tasks are typically characterized by resource constraints alongside high requirements for real-time processing and accuracy.
- p.14382 introduction: Therefore, it is significant to propose an approach that aims to realize an industrial time-series prediction model with low memory, low-computational complexity, and high accuracy simultaneously.
- p.14382 introduction: The specific contributions are as follows.
- p.14382 introduction: The rest of this article is organized as follows. Section II describes related research work. Section III provides a detailed explanation of the proposed methodology. Section IV validates the effectiveness of BTFormer through extensive experiments. Finally, Section V concludes this article.
- p.14382 related-work: Transformer-based time-series prediction has seen rapid advancements in industrial applications [14].
- p.14382 related-work: However, the transformer architecture inherently has a large model size and computational complexity, which poses a challenge for adapting to resource-constrained edge devices.
- p.14383 related-work: In summary, existing transformer-based time-series prediction models still face significant challenges in terms of memory requirements and computational complexity.
- p.14383 method: BTFormer has been proposed in this article to reduce the Mb requirements and improve computational efficiency while maintaining high accuracy.
- p.14386 experiments: RUL prediction and action recognition are two fundamental tasks in time-series prediction.
- p.14389 conclusion: This article proposes BTFormer, a binary transformer model for industrial time-series prediction, addressing three key challenges: binary attention information loss, trend information capture, and training process mismatch.
- p.14389 conclusion: Future research will explore hybrid models with different quantization levels to further bridge the accuracy gap between binary and full-precision networks in more complicated industrial scenarios.
