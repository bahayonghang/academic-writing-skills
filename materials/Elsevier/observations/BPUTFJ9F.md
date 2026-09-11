---
key: BPUTFJ9F
title: "Transformer-based auto-encoder with combined multi-head-attention for industrial soft-sensor modeling"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2025.111681"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Background` → `3. Methodology` → `4` 实验（超参、基线对比） → `5. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段机制/数据驱动软测量、自编码器与 Transformer 软测量文献）。Introduction 末有编号贡献。`2. Background` 为 Auto-encoder 与 Transformer 预备。Experiments 用蒸汽流量与 debutanizer 两数据集。

## Openers

- abstract: `Soft-sensor modeling is` — "Soft-sensor modeling is common in industrial production, but high data dimensionality, a lack of labeled features, and inadequate methods complicate extracting nonlinear feature representations."
- introduction: `It is crucial` — "It is crucial for plants and companies to implement monitoring of industrial processes to help reduce costs, minimize pollution, and boost profits (Yuan et al., 2018)."
- method: `The proposed TAE-CMHA` — "The proposed TAE-CMHA model seeks to learn effective nonlinear feature representations from input data to predict the target outcome."
- experiments: `To validate the` — "To validate the performance of the TAE-CMHA model proposed in this paper, we compare it with the SVR, MLP, TNN, AE, and TAE baseline models using two datasets."
- conclusion: `In order to` — "In order to extract good nonlinear feature representations from high-dimensional and label-deficient industrial data, we propose the TAE-CMHA model and the TAE baseline model for soft-sensor modeling."

## Gap transitions

- this paper proposes (abstract): "This paper proposes a Transformer-based auto-encoder with a combined multi-head-attention approach (TAE-CMHA) for soft-sensor modeling, which offers advantages for nonlinear feature representation."
- however (introduction): "However, linear statistical methods have limitations in analyzing nonlinear data."
- therefore (introduction): "Therefore, the auto-encoder was used as the foundational model in this paper due to its feature extraction capabilities."
- based on (introduction): "Based on these observations regarding auto-encoders and the Transformer, an auto-encoder based on Transformer combined multi-head-attention method (TAE-CMHA) is proposed in this paper."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "This paper proposes"; "is proposed in this paper"; "we propose the TAE-CMHA model"
- show / associative / abstract: "The results show that the mean squared error (MSE) of the proposed method reaches a minimum of 0.00297 and the coefficient of determination (R2) is 0.881 in debutanizer column datasets, which shows the advantages of the model."
- conclude / associative / experiments: "Based on the above discussion, we can conclude that TAE-CMHA has better prediction effectiveness than the other five models"

## Cross-section linkers

- introduction → background: 贡献清单后 `2. Background`
- background → method: Transformer decoder 取舍后 `3. Methodology`
- method → experiments: 模型概述后进入第 4 节超参与基线对比
- experiments → conclusion: 误差分布与 parity plot 后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction，另设 `Background` 预备节。
- R004 编号贡献：`The contributions are:`
- R009 自称：`This paper proposes` / `is proposed in this paper`

## Candidate phrases

- `This paper proposes a Transformer-based auto-encoder` (abstract)
- `is proposed in this paper` (introduction)
- `To validate the performance of the TAE-CMHA model proposed in this paper` (experiments)
- `we propose the TAE-CMHA model` (conclusion)

## House style

自称 `This paper proposes` / `is proposed in this paper` / `we propose` / `the TAE-CMHA model proposed in this paper`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Soft-sensor modeling is common in industrial production, but high data dimensionality, a lack of labeled features, and inadequate methods complicate extracting nonlinear feature representations.
- abstract: This paper proposes a Transformer-based auto-encoder with a combined multi-head-attention approach (TAE-CMHA) for soft-sensor modeling, which offers advantages for nonlinear feature representation.
- abstract: The results show that the mean squared error (MSE) of the proposed method reaches a minimum of 0.00297 and the coefficient of determination (R2) is 0.881 in debutanizer column datasets, which shows the advantages of the model.
- introduction: It is crucial for plants and companies to implement monitoring of industrial processes to help reduce costs, minimize pollution, and boost profits (Yuan et al., 2018).
- introduction: However, linear statistical methods have limitations in analyzing nonlinear data.
- introduction: Therefore, the auto-encoder was used as the foundational model in this paper due to its feature extraction capabilities.
- introduction: Based on these observations regarding auto-encoders and the Transformer, an auto-encoder based on Transformer combined multi-head-attention method (TAE-CMHA) is proposed in this paper.
- method: The proposed TAE-CMHA model seeks to learn effective nonlinear feature representations from input data to predict the target outcome.
- experiments: To validate the performance of the TAE-CMHA model proposed in this paper, we compare it with the SVR, MLP, TNN, AE, and TAE baseline models using two datasets.
- conclusion: In order to extract good nonlinear feature representations from high-dimensional and label-deficient industrial data, we propose the TAE-CMHA model and the TAE baseline model for soft-sensor modeling.
- conclusion: The prediction effectiveness of TAE-CMHA model was shown to be better than SVR, MLP, TNN, AE, and TAE through experiments on two datasets.
