---
key: 2ICHB7KL
title: "Adaptive Multiresampling Learning Based on Dual-Scale Feature Aggregation for Industrial Quality Prediction"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3545055"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM STATEMENT` → `III. AMRL NETWORK` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 LSTM / CNN / GRU / dual-scale 建模与重采样对齐）。未见 `The rest of this article is organized` 路标；贡献列表后直接 `II. PROBLEM STATEMENT`。Experiments 标题为 `CASE STUDIES`。

## Openers

- abstract: `Quality prediction is` — "Quality prediction is essential for optimizing operations and making timely decisions in industrial processes." (p.1)
- introduction: `WITH the development` — "WITH the development of industrial digitalization and intelligence, complex industrial processes gradually shift from a coarse production model to a refined production model." (p.1；栏首掉字)
- method: `In this section` — "In this section, the AMRL network is designed to model fast and slow-scale data to predict the quality index." (p.3)
- experiments: `Froth flotation is` — "Froth flotation is an industrial process for mineral separation based on the surface properties of particles, including hydrophobicity and hydrophilicity [4]." (p.6, IV.A)
- conclusion: `This article addresses` — "This article addresses the challenge of inaccurate industrial quality prediction due to inconsistent data sampling periods in complex industrial processes." (p.10)

## Gap transitions

- however (abstract): "However, the dynamic nature of industrial data, characterized by different sampling periods, presents significant challenges for quality prediction." (p.1)
- to address (abstract): "To address this issue, we propose an adaptive multiresampling learning (AMRL) network that performs deep spatial-temporal feature mining and extraction from dual-scale data, facilitating multistep industrial quality prediction." (p.1)
- however (introduction): 对齐/降采样方法 “These methods have achieved good application results, but lack detailed analysis of spatial-temporal features at different scales, resulting in the loss of intrinsic features of industrial data and limited accuracy of data-driven modeling.” (p.2)
- for the above (introduction): "For the above problems, this work proposes an adaptive multiresampling learning (AMRL) network, which performs adaptive deep feature mining and extraction on fast and slow-scale data, achieving industrial quality multistep prediction at different scales." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose an adaptive multiresampling learning (AMRL) network"; "this work proposes an adaptive multiresampling learning (AMRL) network"
- demonstrate / causal / abstract: "The comparison results demonstrate the superior performance of the AMRL in multistep industrial quality prediction."
- show / causal / experiments: "The prediction curves of the proposed method and eight comparison models are shown in Fig. 8(a)–(i)."
- highlight / causal / experiments: "These results highlight the effectiveness of the proposed AMRL network in enhancing the prediction accuracy of industrial quality."

## Cross-section linkers

- introduction → problem: 贡献列表后直接 `II. PROBLEM STATEMENT`，无独立路标句 (p.2)
- method → experiments: 双尺度特征聚合公式后 `IV. CASE STUDIES` (p.6)
- experiments → conclusion: 多步预测表后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 摘要缺口后用 `To address this issue, we propose` + 方法缩写。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 本篇无 `The rest of this article is organized` 路标。
- R004 贡献用 `The main contributions of this work are as follows` + 编号列表。
- R005 结论用 `Our future research will explore` 指向后续。

## Candidate phrases

- `To address this issue, we propose` (abstract)
- `For the above problems, this work proposes` (introduction)
- `The main contributions of this work are as follows.` (introduction)
- `This article addresses the challenge of` (conclusion)
- `Our future research will explore` (conclusion)

## House style

自称是 `we propose` / `this work proposes` / `This article addresses` / `the proposed method`。未见 `Here we`、`In this paper`。`we propose` 与 `this work` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Quality prediction is essential for optimizing operations and making timely decisions in industrial processes.
- p.1 abstract: However, the dynamic nature of industrial data, characterized by different sampling periods, presents significant challenges for quality prediction.
- p.1 abstract: To address this issue, we propose an adaptive multiresampling learning (AMRL) network that performs deep spatial-temporal feature mining and extraction from dual-scale data, facilitating multistep industrial quality prediction.
- p.1 abstract: The comparison results demonstrate the superior performance of the AMRL in multistep industrial quality prediction.
- p.1 introduction: WITH the development of industrial digitalization and intelligence, complex industrial processes gradually shift from a coarse production model to a refined production model.
- p.2 introduction: These methods have achieved good application results, but lack detailed analysis of spatial-temporal features at different scales, resulting in the loss of intrinsic features of industrial data and limited accuracy of data-driven modeling.
- p.2 introduction: For the above problems, this work proposes an adaptive multiresampling learning (AMRL) network, which performs adaptive deep feature mining and extraction on fast and slow-scale data, achieving industrial quality multistep prediction at different scales.
- p.2 introduction: The main contributions of this work are as follows.
- p.3 method: In this section, the AMRL network is designed to model fast and slow-scale data to predict the quality index.
- p.6 experiments: Froth flotation is an industrial process for mineral separation based on the surface properties of particles, including hydrophobicity and hydrophilicity [4].
- p.9 experiments: Combining the boxplot of prediction errors in Fig. 9, it can be concluded that the proposed method can provide a better prediction performance for the quality index than the other eight models.
- p.10 experiments: These results highlight the effectiveness of the proposed AMRL network in enhancing the prediction accuracy of industrial quality.
- p.10 conclusion: This article addresses the challenge of inaccurate industrial quality prediction due to inconsistent data sampling periods in complex industrial processes.
- p.10 conclusion: This work significantly improves industrial data modeling and prediction for two sampling frequency scales.
- p.10 conclusion: Our future research will explore AMRL’s applicability in various domains and investigate extensions for handling multiple sampling periods.
