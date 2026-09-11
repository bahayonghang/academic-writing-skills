---
key: S9YTRHKB
title: "MR-Transformer: Multiresolution Transformer for Multivariate Time Series Prediction"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2023.3327416"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. METHOD` → `IV. EXPERIMENT SETUP` → `V. EXPERIMENTAL RESULTS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORK`：A. Time Series Forecasting；B. Transformer-Based Models）。Introduction 末有 `The remainder of this article is organized as follows.`（路标写 `Section VI summarizes`，与正文 `VI. CONCLUSION` 一致）。Method 在 III。Experiments 拆成 `IV. EXPERIMENT SETUP` 与 `V. EXPERIMENTAL RESULTS`。

## Openers

- abstract: `Multivariate time series` — "Multivariate time series (MTS) prediction has been studied broadly, which is widely applied in real-world applications." (p.1)
- introduction: `MULTIVARIATE time series` — "MULTIVARIATE time series (MTS) are ubiquitous in the modern manufacturing industry, sensor networks and information services." (p.1)
- related work: `Time series forecasting` — "Time series forecasting is a long-standing problem in the literature, which has received significant attention over the years." (p.2, II.A)
- method: `The basic idea` — "The basic idea of the proposed method MR-Transformer is to model MTS from a comprehensive perspective, for both temporal and variable resolutions." (p.3, III)
- experiments: `In this section` — "In this section, we compare MR-Transformer to several state-of-the-art baselines, including multistep and single-step forecasting scenarios." (p.9, V.A)
- conclusion: `This article proposes` — "This article proposes a novel MR-Transformer model for MTS prediction, modeling MTS from a comprehensive view." (p.12)

## Gap transitions

- despite (abstract): "Despite progress, these methods pay little attention to extracting short-term information in the context, while short-term patterns play an essential role in reflecting local temporal dynamics." (p.1)
- moreover (abstract): "Moreover, we argue that there are both consistent and specific characteristics among multiple variables, which should be fully considered for MTS modeling." (p.1)
- to this end (abstract): "To this end, we propose a multiresolution transformer (MR-Transformer) for MTS prediction, modeling MTS from both the temporal and the variable resolution." (p.1)
- however (introduction): "However, these methods assume a linear dependence over time, and they are not well-suited to model long-term dependencies." (p.1)
- however (introduction): "However, these transformer-based methods pay little attention to extracting short-term information in the context, while short-term patterns play an important role in reflecting local temporal dynamics." (p.1)
- however (introduction): "However, existing transformer-based models mainly focus on modeling variable-consistent features while neglecting the specific features of each variable." (p.2)
- nonetheless (related work): "Nonetheless, these transformer-based methods tend to overlook the importance of extracting multiresolution information from time series, including variable correlations and short-term information within the context." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a multiresolution transformer (MR-Transformer)"; "This article proposes a novel MR-Transformer model"
- argue / speculative / abstract: "Moreover, we argue that there are both consistent and specific characteristics among multiple variables"
- show / causal / abstract, conclusion: "Extensive experiments conducted on real-world time series datasets show"; "Our extensive experiments show"
- demonstrate / causal / abstract: "The visualization analysis also demonstrates the effectiveness of the proposed model."

## Cross-section linkers

- introduction → related work: "The remainder of this article is organized as follows. Section II reviews related works on MTS prediction and transformer-based forecasting models. Section III introduces our MR-Transformer model in detail. In Section IV, we demonstrate the effectiveness of MR-Transformer empirically. Finally, Section VI summarizes the article." (p.2)
- related work → method: "In this work, we propose an adaptive segment attention mechanism to explore the short-term information within segments." 随后 `III. METHOD` (p.3)
- method → experiments: 学习目标后 `IV. EXPERIMENT SETUP`，结果在 `V. EXPERIMENTAL RESULTS` (p.7–9)
- experiments → conclusion: 单变量实验后 `VI. CONCLUSION` (p.12)

## Candidate rules

- R001 独立 Related Work 用 `II. RELATED WORK` 分 A/B 子节。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The major contributions of this article are summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `The limitation of our work is` 指向后续。
- R011 Experiments 可拆成 `IV. EXPERIMENT SETUP` 与 `V. EXPERIMENTAL RESULTS`。

## Candidate phrases

- `To this end, we propose a multiresolution transformer (MR-Transformer)` (abstract)
- `To address the aforementioned limitations, we propose` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `This article proposes a novel MR-Transformer model` (conclusion)
- `The limitation of our work is that` (conclusion)

## House style

自称是 `we propose` / `This article proposes` / `our MR-Transformer`。未见 `Here we`、`In this paper`。`This article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Multivariate time series (MTS) prediction has been studied broadly, which is widely applied in real-world applications.
- p.1 abstract: Despite progress, these methods pay little attention to extracting short-term information in the context, while short-term patterns play an essential role in reflecting local temporal dynamics.
- p.1 abstract: Moreover, we argue that there are both consistent and specific characteristics among multiple variables, which should be fully considered for MTS modeling.
- p.1 abstract: To this end, we propose a multiresolution transformer (MR-Transformer) for MTS prediction, modeling MTS from both the temporal and the variable resolution.
- p.1 abstract: Extensive experiments conducted on real-world time series datasets show that MR-Transformer significantly outperforms the state-of-the-art MTS prediction models.
- p.1 introduction: MULTIVARIATE time series (MTS) are ubiquitous in the modern manufacturing industry, sensor networks and information services.
- p.1 introduction: However, these transformer-based methods pay little attention to extracting short-term information in the context, while short-term patterns play an important role in reflecting local temporal dynamics.
- p.2 introduction: To address the aforementioned limitations, we propose multiresolution transformer (MR-Transformer) for MTS prediction, modeling MTS from a more comprehensive perspective.
- p.2 introduction: The remainder of this article is organized as follows. Section II reviews related works on MTS prediction and transformer-based forecasting models. Section III introduces our MR-Transformer model in detail. In Section IV, we demonstrate the effectiveness of MR-Transformer empirically. Finally, Section VI summarizes the article.
- p.2 related work: Time series forecasting is a long-standing problem in the literature, which has received significant attention over the years.
- p.3 related work: Nonetheless, these transformer-based methods tend to overlook the importance of extracting multiresolution information from time series, including variable correlations and short-term information within the context.
- p.3 method: The basic idea of the proposed method MR-Transformer is to model MTS from a comprehensive perspective, for both temporal and variable resolutions.
- p.9 experiments: In this section, we compare MR-Transformer to several state-of-the-art baselines, including multistep and single-step forecasting scenarios.
- p.12 conclusion: This article proposes a novel MR-Transformer model for MTS prediction, modeling MTS from a comprehensive view.
- p.12 conclusion: The limitation of our work is that it is currently unable to handle the data with missing values, which will also be the direction of our future improvement.
