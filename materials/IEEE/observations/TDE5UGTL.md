---
key: TDE5UGTL
title: "Balanced MSE for imbalanced visual regression"
venue: "2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)"
doi: "10.1109/CVPR52688.2022.00777"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

阿拉伯数字标题：`1. Introduction` → `2. Related Works` → `3. Methodology` → `4. Experiments` → `5. Discussion and Conclusion`。前置 `Abstract`（无 Index Terms）。有独立相关工作节 `2. Related Works`（Imbalanced & Long-Tailed Classification / Imbalanced Regression）。`related_work=independent`。Introduction 末有三点贡献，无 `The rest of this paper is organized` 路标。Method 含 Problem Setting、Revisiting MSE、Balanced MSE、与分类的联系、实现选项。Experiments 含 synthetic 与 real-world（age / depth / IHMR）。Conclusion 节含 Future Works 与 Broader Impacts。

## Openers

- abstract: `Data imbalance exists` — "Data imbalance exists ubiquitously in real-world visual regressions, e.g., age estimation and pose estimation, hurting the model’s generalizability and fairness." (p.7916)
- introduction: `Visual regression, where` — "Visual regression, where models learn to predict continuous labels, is one of the most fundamental tasks in machine learning." (p.7916)
- method: `We study a` — "We study a regression task." (p.7918, 3.1)
- experiments: `We construct a` — "We construct a simple one-dimensional linear imbalanced regression dataset, with the training label distribution being normal or exponential and skewed to various extents." (p.7921)
- conclusion: `In conclusion, we` — "In conclusion, we revisit MSE’s probabilistic interpretation and identify its ineffectiveness in imbalanced regression." (p.7923)

## Gap transitions

- however (introduction): "However, in real-world applications, data imbalance is widely encountered, hurting the model’s generalizability and fairness." (p.7916)
- however (introduction): "However, prior works [5, 36] show that reweighting has limited effectiveness on imbalanced classification." (p.7916)
- to mitigate (introduction): "To mitigate the gap, we present a statistically principled loss function, Balanced MSE, for imbalanced regression." (p.7917)
- however (method): "However, as mentioned in the problem setting, we are interested in estimating pbal(y|x) instead of ptrain(y|x)." (p.7918)
- however (method): "However, in modern deep learning tasks, ptrain(y) could be very high-dimensional and has a complex underlying distribution." (p.7920)
- however (impacts): "However, there are still other types of biases in a training dataset besides the mentioned label imbalance." (p.7923)

## Hedge verbs

- identify / causal / abstract, introduction: "we identify that the widely used Mean Square Error (MSE) loss function can be ineffective"; "We identify that MSE carries the label imbalance into predictions"
- propose / causal / abstract, method: "we ... propose a novel loss function, Balanced MSE"; "We propose Balanced MSE to restore pbal(y|x)."
- demonstrate / causal / abstract: "Extensive experiments on both synthetic and three real-world benchmarks demonstrate the effectiveness of Balanced MSE."
- show / causal / introduction, experiments: "Balanced MSE shows clear advantages over existing methods both theoretically and practically."; "We show a visualization of training distribution"
- may / speculative / future work: "Future works may use Balanced MSE as a bridge"

## Cross-section linkers

- introduction → related work: 三点贡献后直接 `2. Related Works` (p.7918)
- related work → method: Imbalanced Regression 段落后接 `3. Methodology` / `3.1. Problem Setting` (p.7918)
- method → experiments: 噪声尺度段落后接 `4. Experiments` (p.7921)
- experiments → conclusion: IHMR 表后接 `5. Discussion and Conclusion` (p.7923)

## Candidate rules

- R001 摘要用 `In this work, we identify` + `propose a novel loss function`。
- R002 独立相关工作分 Classification 与 Regression。
- R003 贡献用 `In summary, our contributions are three-fold:` + 编号。
- R004 Method 先 Problem Setting，再 Revisiting MSE，再提出损失。
- R005 Conclusion 节标题为 `Discussion and Conclusion`，另列 Future Works 与 Broader Impacts。

## Candidate phrases

- `In this work, we identify that the widely used Mean Square Error (MSE) loss function can be ineffective` (abstract)
- `To mitigate the gap, we present a statistically principled loss function` (introduction)
- `In summary, our contributions are three-fold:` (introduction)
- `In conclusion, we revisit MSE’s probabilistic interpretation and identify its ineffectiveness` (conclusion)
- `Future works may use Balanced MSE as a bridge to introduce` (conclusion)

## House style

自称是 `In this work, we identify` / `we propose` / `we present` / `Our work` / `to the best of our knowledge`。未见 `Here we`。`In this work` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.7916 abstract: Data imbalance exists ubiquitously in real-world visual regressions, e.g., age estimation and pose estimation, hurting the model’s generalizability and fairness.
- p.7916 abstract: In this work, we identify that the widely used Mean Square Error (MSE) loss function can be ineffective in imbalanced regression.
- p.7916 abstract: We revisit MSE from a statistical view and propose a novel loss function, Balanced MSE, to accommodate the imbalanced training label distribution.
- p.7916 abstract: Moreover, to the best of our knowledge, Balanced MSE is the first general solution to high-dimensional imbalanced regression in modern context.
- p.7916 introduction: Visual regression, where models learn to predict continuous labels, is one of the most fundamental tasks in machine learning.
- p.7916 introduction: However, in real-world applications, data imbalance is widely encountered, hurting the model’s generalizability and fairness.
- p.7916 introduction: However, prior works [5, 36] show that reweighting has limited effectiveness on imbalanced classification.
- p.7917 introduction: To mitigate the gap, we present a statistically principled loss function, Balanced MSE, for imbalanced regression.
- p.7918 introduction: In summary, our contributions are three-fold: 1) We identify the ineffectiveness of MSE in imbalanced regression and propose a statistically principled loss function, Balanced MSE, that leverages the training label distribution prior to restore a balanced prediction.
- p.7918 related work: Many techniques have been explored for imbalanced & long-tailed classification, for example, resampling [7, 9, 13, 21] and reweighting [6, 10, 16, 17].
- p.7918 related work: Imbalanced regression is relatively under-explored.
- p.7918 method: We study a regression task.
- p.7918 method: However, as mentioned in the problem setting, we are interested in estimating pbal(y|x) instead of ptrain(y|x).
- p.7918 method: We propose Balanced MSE to restore pbal(y|x).
- p.7921 experiments: We construct a simple one-dimensional linear imbalanced regression dataset, with the training label distribution being normal or exponential and skewed to various extents.
- p.7922 experiments: Balanced MSE substantially outperforms the previous methods.
- p.7923 conclusion: In conclusion, we revisit MSE’s probabilistic interpretation and identify its ineffectiveness in imbalanced regression.
- p.7923 conclusion: We therefore propose a statistically principled loss function, Balanced MSE, for imbalanced regression.
- p.7923 conclusion: Future works may use Balanced MSE as a bridge to introduce more approaches that are developed on the imbalanced classification to the imbalanced regression.
- p.7923 conclusion: However, there are still other types of biases in a training dataset besides the mentioned label imbalance.
