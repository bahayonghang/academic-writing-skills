---
key: 8ZN36WRM
title: "WFA-SRNet: A Wavelet-Guided and Feature-Aware Network for Remote Sensing Image Super-Resolution"
venue: "IEEE Transactions on Geoscience and Remote Sensing"
doi: "10.1109/TGRS.2025.3615280"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PROPOSED METHOD` → `IV. EXPERIMENTAL RESULTS AND ANALYSES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立相关工作节 `II. RELATED WORK`（natural image SR / SR for RSIs）。`related_work=independent`。Introduction 末有 `The remainder of this article is organized as follows` 路标，指向 II–V。Method 在 III（FEB / HFE / FA）。Experiments 标题为 `EXPERIMENTAL RESULTS AND ANALYSES`（UC Merced / RSSCN7）。

## Openers

- abstract: `Recently, deep learning-based` — "Recently, deep learning-based remote sensing image super-resolution (RSISR) methods have achieved remarkable progress." (p.1)
- introduction: `REMOTE sensing images` — "REMOTE sensing images (RSIs), acquired via satellites, uncrewed aerial vehicles (UAVs), or airborne platforms, play a vital role in a wide range of Earth observation tasks, including object detection [1], urban planning [2], disaster monitoring [3], and environmental surveillance [4]." (p.1；栏首掉字)
- method: `In this section` — "In this section, we first describe the architecture of the proposed WFA-SRNet network." (p.4, III)
- experiments: `In this section` — "In this section, we evaluate the performance of the proposed WFA-SRNet against various state-of-the-art methods in the domain of RSISR." (p.7, IV)
- conclusion: `In this article` — "In this article, we propose WFA-SRNet, a novel SR framework tailored for remote sensing imagery." (p.12)

## Gap transitions

- however (abstract): "However, effectively preserving high-frequency details remains a significant challenge, as these features are critical for downstream tasks such as object detection, change analysis, and scene classification." (p.1)
- moreover (abstract): "Moreover, relying solely on the information contained in low-resolution (LR) images often results in the loss of structural details, thereby degrading reconstruction quality." (p.1)
- to address (abstract): "To address these issues, we propose a novel wavelet-guided and feature-aware super-resolution network (WFA-SRNet)." (p.1)
- however (introduction): "However, directly applying such models to RSISR remains highly challenging." (p.1)
- although (introduction): "Although the aforementioned methods have made significant progress in RSISR, existing models still face several limitations." (p.2)
- unlike (related work): "Unlike existing methods that primarily focus on enhancing overall SR performance, the proposed WFA-SRNet simultaneously emphasizes the restoration of high-frequency structural details and the modeling of nonlocal similarity." (p.3)
- despite (conclusion): "Despite these promising results, our current work remains focused on RGB-based SR tasks." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a novel wavelet-guided and feature-aware super-resolution network (WFA-SRNet)"; "this article proposes a novel RSISR framework"; "we propose WFA-SRNet"
- demonstrate / causal / abstract, conclusion: "Extensive experiments on multiple benchmark remote sensing datasets demonstrate"; "Extensive experiments across multiple benchmarks ... demonstrate"
- may / speculative / experiments: "its attention mechanism does not adequately distinguish informative structures from redundant background, which may limit its performance"

## Cross-section linkers

- introduction → related work: "The remainder of this article is organized as follows. Section II reviews the related literature on image SR, with an emphasis on remote sensing applications. Section III details the architecture and core modules of the proposed WFA-SRNet. Section IV presents the datasets, evaluation metrics, experimental results, and comparative analyses. Finally, Section V concludes the article and outlines future research directions." (p.2)
- related work → method: "Unlike existing methods that primarily focus on enhancing overall SR performance, the proposed WFA-SRNet simultaneously emphasizes the restoration of high-frequency structural details and the modeling of nonlocal similarity." 随后 `III. PROPOSED METHOD` (p.3–4)
- method → experiments: Discussion 后接 `IV. EXPERIMENTAL RESULTS AND ANALYSES` (p.7)
- experiments → conclusion: 效率分析后直接 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `To address these issues, we propose a novel`，不用 `Here we`。
- R002 独立相关工作标题为 `RELATED WORK`，分 natural image SR 与 RSISR。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R004 贡献用 `In summary, the main contributions of this work are as follows.` + 编号列表。
- R005 Conclusion 用 `In this article, we propose` 收回，再用 `Future efforts will explore` 指向后续。

## Candidate phrases

- `To address these issues, we propose a novel wavelet-guided and feature-aware super-resolution network` (abstract)
- `In summary, the main contributions of this work are as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this article, we propose WFA-SRNet, a novel SR framework tailored for` (conclusion)
- `Future efforts will explore the extension of WFA-SRNet to hyperspectral, multispectral, and blind SR scenarios` (conclusion)

## House style

自称是 `we propose` / `this article` / `this work` / `our WFA-SRNet`。未见 `Here we`。`In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Recently, deep learning-based remote sensing image super-resolution (RSISR) methods have achieved remarkable progress.
- p.1 abstract: However, effectively preserving high-frequency details remains a significant challenge, as these features are critical for downstream tasks such as object detection, change analysis, and scene classification.
- p.1 abstract: To address these issues, we propose a novel wavelet-guided and feature-aware super-resolution network (WFA-SRNet).
- p.1 abstract: Extensive experiments on multiple benchmark remote sensing datasets demonstrate that WFA-SRNet achieves superior reconstruction performance, particularly in restoring structural and textural details.
- p.1 introduction: REMOTE sensing images (RSIs), acquired via satellites, uncrewed aerial vehicles (UAVs), or airborne platforms, play a vital role in a wide range of Earth observation tasks, including object detection [1], urban planning [2], disaster monitoring [3], and environmental surveillance [4].
- p.1 introduction: However, directly applying such models to RSISR remains highly challenging.
- p.2 introduction: Although the aforementioned methods have made significant progress in RSISR, existing models still face several limitations.
- p.2 introduction: In summary, the main contributions of this work are as follows.
- p.2 introduction: The remainder of this article is organized as follows. Section II reviews the related literature on image SR, with an emphasis on remote sensing applications. Section III details the architecture and core modules of the proposed WFA-SRNet. Section IV presents the datasets, evaluation metrics, experimental results, and comparative analyses. Finally, Section V concludes the article and outlines future research directions.
- p.3 related work: Unlike existing methods that primarily focus on enhancing overall SR performance, the proposed WFA-SRNet simultaneously emphasizes the restoration of high-frequency structural details and the modeling of nonlocal similarity.
- p.4 method: In this section, we first describe the architecture of the proposed WFA-SRNet network.
- p.7 experiments: In this section, we evaluate the performance of the proposed WFA-SRNet against various state-of-the-art methods in the domain of RSISR.
- p.8 experiments: In the ×2 SR task on UC Merced, WFA-SRNet achieves 34.78 dB in PSNR and 0.9465 in SSIM, surpassing the previous best model EGSRN [31] by 0.55 dB and 0.0059,
- p.12 conclusion: In this article, we propose WFA-SRNet, a novel SR framework tailored for remote sensing imagery.
- p.12 conclusion: Extensive experiments across multiple benchmarks, including UC Merced, RSSCN7, and natural image datasets—demonstrate that WFA-SRNet consistently outperforms state-of-the-art RSISR methods, particularly in reconstructing edge contours and complex textures.
- p.12 conclusion: Despite these promising results, our current work remains focused on RGB-based SR tasks.
- p.12 conclusion: Future efforts will explore the extension of WFA-SRNet to hyperspectral, multispectral, and blind SR scenarios, as well as optimizing its deployment for real-time applications in remote sensing and geospatial analysis.
