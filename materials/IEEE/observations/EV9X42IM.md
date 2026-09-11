---
key: EV9X42IM
title: "Adapt or Perish: Adaptive Sparse Transformer with Attentive Feature Refinement for Image Restoration"
venue: "2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)"
doi: "10.1109/CVPR52733.2024.00285"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

阿拉伯数字标题：`1. Introduction` → `2. Related Work` → `3. Proposed Method` → `4. Experiments` → `5. Conclusions`。前置 `Abstract`（无 Index Terms）。有独立相关工作节 `2. Related Work`（Image Restoration / Vision Transformer）。`related_work=independent`。Introduction 末有三点贡献，无 `The rest of this paper is organized` 路标。Method 含 Overall Pipeline、ASSA、FRFN。Experiments 含 rain streak / raindrop / real haze 与 ablation。Conclusion 另有 `Limitations.` 段。

## Openers

- abstract: `Transformer-based approaches have` — "Transformer-based approaches have achieved promising performance in image restoration tasks, given their ability to model long-range dependencies, which is crucial for recovering clear images." (p.2952)
- introduction: `Image restoration aims` — "Image restoration aims to restore clear images from degraded ones." (p.2952)
- method: `The overview of` — "The overview of our AST pipeline is shown in Fig. 2, given a image I ∈ R^{H×W×3}, AST first employs a convolution layer to produce a low-level feature representation F0 ∈ R^{H×W×C}, where H × W, C are the image resolution and the number of channels, respectively." (p.2954)
- experiments: `In this section` — "In this section, we evaluate the performance of AST on various image restoration tasks, such as rain streak, haze, and raindrop removal." (p.2956)
- conclusion: `The goal of` — "The goal of this work was to recover clear images from the degraded version by adaptively learning the most informative representations and easing the noisy information within features." (p.2959)

## Gap transitions

- however (introduction): "However, their basic unit, convolution, possesses a restricted receptive field and is less effective when modeling long-range dependencies." (p.2952)
- despite (introduction): "Despite attempts to design efficient attention mechanisms [37, 82, 100] to tackle the computational challenge, roadblocks persist for two reasons:" (p.2952)
- unfortunately (introduction): "Unfortunately, since not all query tokens are closely relevant to corresponding ones in the keys, the utilization of all similarities is ineffective for clear image reconstruction." (p.2953)
- hence (introduction): "Hence, we explore another paradigm to ensure that noisy representation features are reduced, and informative ones are retained as far as possible." (p.2953)
- in light of (introduction): "In light of this, we propose an efficient Transformer-based model named Adaptive Sparse Transformer (AST) for image restoration." (p.2953)
- although (related work): "Although these efficient attention varieties effectively address the issue of intensive computation and perform well in removing various degradations, better performance is still profoundly hindered by the irrelevant representation or redundancy within feature maps [8, 114]." (p.2954)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose an Adaptive Sparse Transformer (AST)"; "we propose an efficient Transformer-based model named Adaptive Sparse Transformer (AST)"
- demonstrate / causal / abstract: "Experimental results on commonly used benchmarks have demonstrated the versatility and competitive performance of our method"
- show / causal / introduction, experiments: "showing the superiority of our AST design"; "we show the quantitative results in Tab. 4"
- present / causal / introduction: "We present AST, an efficient Transformer-based model"
- could / speculative / conclusion: "Future work could focus on current limitations"

## Cross-section linkers

- introduction → related work: 三点贡献后直接 `2. Related Work` (p.2953)
- related work → method: "Overall, the main differences between our AST and existing approaches are twofold." 随后 `3. Proposed Method` (p.2954)
- method → experiments: FRFN 段落后接 `4. Experiments`："In this section, we evaluate the performance of AST" (p.2956)
- experiments → conclusion: 感知质量评估后接 `5. Conclusions` (p.2959)

## Candidate rules

- R001 摘要用 `In this work, we propose`，不用 `Here we`。
- R002 独立相关工作分 Image Restoration 与 Vision Transformer。
- R003 贡献用 `Overall, key contributions of this work are three folds:` + 项目符号。
- R004 Experiments 按任务分子节，再接 Analysis and Discussion。
- R005 Conclusion 先收回目标，再单列 `Limitations. Future work could focus on`。

## Candidate phrases

- `In this work, we propose an Adaptive Sparse Transformer (AST) to` (abstract)
- `In light of this, we propose an efficient Transformer-based model named` (introduction)
- `Overall, key contributions of this work are three folds:` (introduction)
- `The goal of this work was to recover` (conclusion)
- `Future work could focus on current limitations` (conclusion)

## House style

自称是 `In this work, we propose` / `we present` / `our method` / `this work`。未见 `Here we`。`In this work, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.2952 abstract: Transformer-based approaches have achieved promising performance in image restoration tasks, given their ability to model long-range dependencies, which is crucial for recovering clear images.
- p.2952 abstract: In this work, we propose an Adaptive Sparse Transformer (AST) to mitigate the noisy interactions of irrelevant areas and remove feature redundancy in both spatial and channel domains.
- p.2952 abstract: Experimental results on commonly used benchmarks have demonstrated the versatility and competitive performance of our method in several tasks, including rain streak removal, real haze removal, and raindrop removal.
- p.2952 introduction: Image restoration aims to restore clear images from degraded ones.
- p.2952 introduction: However, their basic unit, convolution, possesses a restricted receptive field and is less effective when modeling long-range dependencies.
- p.2952 introduction: Despite attempts to design efficient attention mechanisms [37, 82, 100] to tackle the computational challenge, roadblocks persist for two reasons:
- p.2953 introduction: Unfortunately, since not all query tokens are closely relevant to corresponding ones in the keys, the utilization of all similarities is ineffective for clear image reconstruction.
- p.2953 introduction: In light of this, we propose an efficient Transformer-based model named Adaptive Sparse Transformer (AST) for image restoration.
- p.2953 introduction: Overall, key contributions of this work are three folds:
- p.2953 related work: High-quality images are crucial to achieve satisfactory performance for downstream applications, such as recognition [28, 76, 101], segmentation [97, 108, 110], representation learning [42, 84, 112], and reconstruciton [117, 118] in forms of image [45, 83, 115] and video [107, 109, 111].
- p.2954 related work: Although these efficient attention varieties effectively address the issue of intensive computation and perform well in removing various degradations, better performance is still profoundly hindered by the irrelevant representation or redundancy within feature maps [8, 114].
- p.2954 method: The overview of our AST pipeline is shown in Fig. 2, given a image I ∈ R^{H×W×3}, AST first employs a convolution layer to produce a low-level feature representation F0 ∈ R^{H×W×C}, where H × W, C are the image resolution and the number of channels, respectively.
- p.2956 experiments: In this section, we evaluate the performance of AST on various image restoration tasks, such as rain streak, haze, and raindrop removal.
- p.2956 experiments: In Tab. 1, AST-B achieves a gain of 4.48 dB in terms of PSNR metric against the previous best CNN-based method Fu et al. [15] and 0.98 dB against the previous best Transformer-based model DRSformer [8].
- p.2959 conclusion: The goal of this work was to recover clear images from the degraded version by adaptively learning the most informative representations and easing the noisy information within features.
- p.2959 conclusion: Our AST outperforms the relevant baselines that adopt a selection operation (e.g., Top-K selection and Sparse Channel SA) or project features into superpixel space (e.g., Condensed SA) for easing redundancy, while ultimately, it achieves favorable results on several degradation removal tasks.
- p.2959 conclusion: Future work could focus on current limitations (e.g., developing a uniform model for low-quality images with various degradations), as well as opportunities that this task-specific model provides (e.g., injecting priors, like dark channels prior for image dehazing and retinex model prior for removing low-light conditions).
