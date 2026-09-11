---
key: ENL9TUPI
title: "FusionMamba: Efficient Remote Sensing Image Fusion With State Space Model"
venue: "IEEE Transactions on Geoscience and Remote Sensing"
doi: "10.1109/TGRS.2024.3496073"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9,12-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS AND MOTIVATIONS` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. DISCUSSION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS AND MOTIVATIONS`，含 DL fusion / SSM / Motivations 三小节）。Introduction 末有节序路标，指向 Section II–VI。

## Openers

- abstract: `Remote sensing image` — "Remote sensing image fusion aims to generate a high-resolution multi/hyper-spectral image by combining a high-resolution image with limited spectral data and a low-resolution image rich in spectral information." (p.1)
- introduction: `Due to hardware limitations,` — "Due to hardware limitations, satellite sensors often struggle to capture high-resolution multi/hyper-spectral images." (p.1)
- related_work: `In recent years, DL-based` — "In recent years, DL-based methods have dominated the remote sensing image fusion community." (p.2, II.A)
- method: `In this section, we` — "In this section, we first introduce the notations (Section III-A) and explore the mathematical foundations of the SSM (Section III-B)." (p.4, III)
- experiments: `In this section, we` — "In this section, we present the quantitative and qualitative evaluation results for representative remote sensing image fusion approaches on the pansharpening and hyper-spectral pansharpening tasks." (p.7, IV)
- conclusion: `In this paper, we` — "In this paper, we propose FusionMamba, an innovative method for efficient remote sensing image fusion." (p.14)

## Gap transitions

- however (abstract): "However, the potential of SSM for information integration remains largely unexplored." (p.1)
- therefore (abstract): "Therefore, we propose FusionMamba, an innovative method for efficient remote sensing image fusion." (p.1)
- however (introduction): "However, they often lead to significant spectral distortions." (p.2)
- however (related work): "However, the methods discussed above primarily concentrate on the application and directionality of the SSM, leaving its potential for information integration largely unexplored." (p.3)
- therefore (related work): "Therefore, we expand the single-input Mamba block to support dual inputs, resulting in the FusionMamba block" (p.3–4)
- first / second (discussion): "Our method exhibits two limitations. First, the FusionMamba block is designed to support only two inputs... Second, the FusionMamba block requires both feature maps to have the same number of channels" (p.13–14)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose FusionMamba"; "we propose FusionMamba, an innovative method"
- demonstrate / causal / abstract, experiments: "Quantitative and qualitative valuation results across six datasets demonstrate that our method achieves state-of-the-art (SOTA) performance"
- indicate / causal / experiments: "indicate that FusionMamba achieves the best overall performance"
- plan / speculative / discussion: "In the future, we plan to expand the dual-input FusionMamba block"

## Cross-section linkers

- introduction → related work: "The rest of this paper is structured as follows. Section II reviews the related works and outlines our motivations. Section III provides a detailed explanation of our method. In Section IV, we present the experimental results... Finally, Sections V and VI cover the discussion and conclusion, respectively." (p.2)
- related work → method: Motivations 段落后接 `III. METHODOLOGY` (p.4)
- method → experiments: Loss function 段落后接 `IV. EXPERIMENTS` (p.7)
- experiments → discussion → conclusion: Ablation 后接 `V. DISCUSSION`，再 `VI. CONCLUSION` (p.12–14)

## Candidate rules

- R001 贡献用 `The contributions of this study are as follows:` + 编号列表。
- R002 有独立 Related Work，且 Related Work 末设 `Motivations` 小节再入方法。
- R003 Introduction 末用 `The rest of this paper is structured as follows` 指向 II–VI。
- R004 Discussion 用 Strengths / Limitations / Future Work 三分结构。
- R005 Conclusion 用 `In this paper, we propose` 收回方法。

## Candidate phrases

- `Therefore, we propose FusionMamba, an innovative method for` (abstract)
- `The contributions of this study are as follows:` (introduction)
- `The rest of this paper is structured as follows.` (introduction)
- `To the best of our knowledge, this study represents` (introduction)
- `In this paper, we propose FusionMamba` (conclusion)

## House style

自称是 `we propose` / `this study` / `our method` / `In this paper`。未见 `Here we`。`In this paper` / `we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Remote sensing image fusion aims to generate a high-resolution multi/hyper-spectral image by combining a high-resolution image with limited spectral data and a low-resolution image rich in spectral information.
- p.1 abstract: However, the potential of SSM for information integration remains largely unexplored.
- p.1 abstract: Therefore, we propose FusionMamba, an innovative method for efficient remote sensing image fusion.
- p.1 abstract: Quantitative and qualitative valuation results across six datasets demonstrate that our method achieves state-of-the-art (SOTA) performance, underscoring the effectiveness of FusionMamba.
- p.1 introduction: Due to hardware limitations, satellite sensors often struggle to capture high-resolution multi/hyper-spectral images.
- p.2 introduction: Given the aforementioned situation, we propose FusionMamba, a novel method for efficient remote sensing image fusion.
- p.2 introduction: The contributions of this study are as follows:
- p.2 introduction: To the best of our knowledge, this study represents the first application of the SSM in hyper-spectral pansharpening and hyper-spectral image super-resolution (HISR) tasks.
- p.2 introduction: The rest of this paper is structured as follows.
- p.2 related work: In recent years, DL-based methods have dominated the remote sensing image fusion community.
- p.3 related work: However, the methods discussed above primarily concentrate on the application and directionality of the SSM, leaving its potential for information integration largely unexplored.
- p.4 method: In this section, we first introduce the notations (Section III-A) and explore the mathematical foundations of the SSM (Section III-B).
- p.7 experiments: In this section, we present the quantitative and qualitative evaluation results for representative remote sensing image fusion approaches on the pansharpening and hyper-spectral pansharpening tasks.
- p.8 experiments: The quantitative evaluation results for the WV3 and GF2 datasets, respectively presented in Tables I and II, indicate that FusionMamba achieves the best overall performance on both the reduced-resolution and full-resolution testing samples.
- p.13 discussion: Our method exhibits two limitations.
- p.14 discussion: In the future, we plan to expand the dual-input FusionMamba block to accommodate an arbitrary number of inputs, each with a variable number of feature channels.
- p.14 conclusion: In this paper, we propose FusionMamba, an innovative method for efficient remote sensing image fusion.
- p.14 conclusion: We evaluate the performance of FusionMamba across six datasets covering three image fusion tasks: pansharpening, hyper-spectral pansharpening, and HISR.
