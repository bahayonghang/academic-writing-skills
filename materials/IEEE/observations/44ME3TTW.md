---
key: 44ME3TTW
title: "Squeeze-and-excitation networks"
venue: "Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition"
doi: ""
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

阿拉伯数字标题：`1. Introduction` → `2. Related Work` → `3. Squeeze-and-Excitation Blocks` → `6. Experiments` → `7. Conclusion`。前置 `Abstract`（无 Index Terms）。有独立相关工作节 `2. Related Work`（Deep architectures / Attention and gating mechanisms）。`related_work=independent`。Introduction 中段即给出 SE block 结构，无 `The rest of this paper is organized` 路标。Method 含 Squeeze、Excitation、SE-Inception / SE-ResNet。PDF 页码 7132–7141；第 4–5 节在实验前（复杂度与实现细节），实验为 `6. Experiments`。Zotero 题录无 DOI。

## Openers

- abstract: `Convolutional neural networks` — "Convolutional neural networks are built upon the convolution operation, which extracts informative features by fusing spatial and channel-wise information together within local receptive fields." (p.7132)
- introduction: `Convolutional neural networks` — "Convolutional neural networks (CNNs) have proven to be effective models for tackling a variety of visual tasks [21, 27, 33, 45]." (p.7132)
- method: `The Squeeze-and-Excitation` — "The Squeeze-and-Excitation block is a computational unit which can be constructed for any given transformation Ftr : X → U, X ∈ R^{H′×W′×C′}, U ∈ R^{H×W×C}." (p.7133)
- experiments: `The ImageNet 2012` — "The ImageNet 2012 dataset is comprised of 1.28 million training images and 50K validation images from 1000 classes." (p.7136)
- conclusion: `In this paper` — "In this paper we proposed the SE block, a novel architectural unit designed to improve the representational capacity of a network by enabling it to perform dynamic channel-wise feature recalibration." (p.7139)

## Gap transitions

- in order to (abstract): "In order to boost the representational power of a network, several recent approaches have shown the benefit of enhancing spatial encoding." (p.7132)
- in this work (abstract): "In this work, we focus on the channel relationship and propose a novel architectural unit, which we term the “Squeeze-and-Excitation” (SE) block, that adaptively recalibrates channel-wise feature responses by explicitly modelling interdependencies between channels." (p.7132)
- in contrast (related work): "In contrast, we claim that providing the unit with a mechanism to explicitly model dynamic, non-linear dependencies between channels using global information can ease the learning process, and significantly enhance the representational power of the network." (p.7133)
- in contrast (related work): "In contrast, our proposed SE block is a lightweight gating mechanism, specialised to model channel-wise relationships in a computationally efficient manner and designed to enhance the representational power of basic modules throughout the network." (p.7133)
- to mitigate (method): "To mitigate this problem, we propose to squeeze global spatial information into a channel descriptor." (p.7134)

## Hedge verbs

- propose / causal / abstract, introduction, method: "we ... propose a novel architectural unit"; "we propose a mechanism that allows the network to perform feature recalibration"; "we propose to squeeze global spatial information"
- demonstrate / causal / abstract, conclusion: "We demonstrate that by stacking these blocks together"; "Extensive experiments demonstrate the effectiveness of SENets"
- show / causal / abstract, experiments: "several recent approaches have shown the benefit of enhancing spatial encoding"; "The results in Table 2 shows that SE blocks consistently improve performance"
- find / causal / abstract: "Crucially, we find that SE blocks produce significant performance improvements"
- hope / speculative / conclusion: "which we hope may prove useful for other tasks requiring strong discriminative features"

## Cross-section linkers

- introduction → related work: ILSVRC 成绩段落后接 `2. Related Work` (p.7133)
- related work → method: attention 对比后接 `3. Squeeze-and-Excitation Blocks` (p.7133)
- method → experiments: 训练设置后接 `6. Experiments` / `6.1. ImageNet Classification` (p.7136)
- experiments → conclusion: Excitation 分析后接 `7. Conclusion` (p.7139)

## Candidate rules

- R001 摘要用 `In this work, we focus on ... and propose a novel architectural unit, which we term`。
- R002 独立相关工作分 Deep architectures 与 Attention and gating。
- R003 Introduction 用 `In this paper, we investigate a different aspect` 转入通道关系，无节序路标。
- R004 Method 按 Squeeze / Excitation / Exemplars 分小节。
- R005 Conclusion 用 `In this paper we proposed`，再用 `we hope may prove useful`。

## Candidate phrases

- `In this work, we focus on the channel relationship and propose a novel architectural unit` (abstract)
- `In this paper, we investigate a different aspect of architectural design - the channel relationship` (introduction)
- `To mitigate this problem, we propose to squeeze global spatial information into a channel descriptor.` (method)
- `In this paper we proposed the SE block, a novel architectural unit designed to improve` (conclusion)

## House style

自称是 `In this work, we focus` / `In this paper, we investigate` / `we propose` / `We demonstrate`。未见 `Here we`。`In this paper` 与 `In this work` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.7132 abstract: Convolutional neural networks are built upon the convolution operation, which extracts informative features by fusing spatial and channel-wise information together within local receptive fields.
- p.7132 abstract: In this work, we focus on the channel relationship and propose a novel architectural unit, which we term the “Squeeze-and-Excitation” (SE) block, that adaptively recalibrates channel-wise feature responses by explicitly modelling interdependencies between channels.
- p.7132 abstract: We demonstrate that by stacking these blocks together, we can construct SENet architectures that generalise extremely well across challenging datasets.
- p.7132 abstract: Crucially, we find that SE blocks produce significant performance improvements for existing state-of-the-art deep architectures at minimal additional computational cost.
- p.7132 introduction: Convolutional neural networks (CNNs) have proven to be effective models for tackling a variety of visual tasks [21, 27, 33, 45].
- p.7132 introduction: In this paper, we investigate a different aspect of architectural design - the channel relationship, by introducing a new architectural unit, which we term the “Squeeze-and-Excitation” (SE) block.
- p.7132 introduction: To achieve this, we propose a mechanism that allows the network to perform feature recalibration, through which it can learn to use global information to selectively emphasise informative features and suppress less useful ones.
- p.7133 related work: VGGNets [39] and Inception models [43] demonstrated the benefits of increasing depth.
- p.7133 related work: In contrast, we claim that providing the unit with a mechanism to explicitly model dynamic, non-linear dependencies between channels using global information can ease the learning process, and significantly enhance the representational power of the network.
- p.7133 related work: In contrast, our proposed SE block is a lightweight gating mechanism, specialised to model channel-wise relationships in a computationally efficient manner and designed to enhance the representational power of basic modules throughout the network.
- p.7133 method: The Squeeze-and-Excitation block is a computational unit which can be constructed for any given transformation Ftr : X → U, X ∈ R^{H′×W′×C′}, U ∈ R^{H×W×C}.
- p.7134 method: To mitigate this problem, we propose to squeeze global spatial information into a channel descriptor.
- p.7136 experiments: The ImageNet 2012 dataset is comprised of 1.28 million training images and 50K validation images from 1000 classes.
- p.7136 experiments: The results in Table 2 shows that SE blocks consistently improve performance across different depths with an extremely small increase in computational complexity.
- p.7139 conclusion: In this paper we proposed the SE block, a novel architectural unit designed to improve the representational capacity of a network by enabling it to perform dynamic channel-wise feature recalibration.
- p.7139 conclusion: Extensive experiments demonstrate the effectiveness of SENets which achieve state-of-the-art performance on multiple datasets.
- p.7139 conclusion: In addition, they provide some insight into the limitations of previous architectures in modelling channel-wise feature dependencies, which we hope may prove useful for other tasks requiring strong discriminative features.
