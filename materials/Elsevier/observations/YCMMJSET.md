---
key: YCMMJSET
title: "A dual-branch multi-scale encoding and fusion model for multivariate time series forecasting"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2025.113610"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related works` → `3. Proposed method` → `4. Experiments` → `5. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。独立 Related Work。Introduction 末有项目符号贡献。Method 含 dual-branch、downsampling、Fourier 分解、HierFusion。Experiments 含 ablation、可视化、效率与置信区间。

## Openers

- abstract: `Multivariate time series` — "Multivariate time series forecasting is crucial across various critical domains, including weather prediction, finance, traffic management, and industrial manufacturing."
- introduction: `Long-term time series` — "Long-term time series forecasting (LTSF) plays a critical role in various domains, including weather prediction (Lam et al., 2023), financial analysis (Zeng et al., 2023b), traffic scheduling (Xu et al., 2020), and industrial monitoring (Zamanzadeh Darban et al., 2024)."
- related_work: `Time Series Forecasting.` — "Time Series Forecasting. Traditional statistical models such as ETS (Hyndman and Khandakar, 2008; Li et al., 2022), ARMA (Box and Jenkins, 1976), and ARIMA (Hyndman and Athanasopoulos, 2018) have long served as baselines for time series forecasting."
- method: `In multivariate time` — "In multivariate time series forecasting, the goal is to predict the future sequence based on historical observations."
- experiments: `We evaluated the` — "We evaluated the proposed model on eight widely used benchmark datasets, including four ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2) and the Electricity, Traffic, Weather, and Solar datasets."
- conclusion: `This paper proposes` — "This paper proposes a dual-branch multi-scale framework (DBMS), a novel architecture that combines the strengths of Transformer encoders and multi-layer perceptrons (MLPs) to enhance time series forecasting."

## Gap transitions

- to overcome (abstract): "To overcome these limitations, this paper introduces a novel deep learning architecture: the Dual-Branch Multi-Scale Transformer-MLP (DBMS)."
- nevertheless (introduction): "Nevertheless, most existing approaches rely on a single architecture or fixed-scale design, limiting their ability to simultaneously capture both global and local temporal patterns."
- however (introduction): "However, many existing models are restricted to single-scale modeling (Nie et al., 2022; Kim et al., 2024), which limits their ability to represent diverse temporal structures."
- to address (introduction): "To address these issues, this paper proposes a Dual-Branch Multi-Scale Transformer-MLP (DBMS) for long-term time series forecasting."
- in contrast (related_work): "In contrast, our work introduces a dual-branch multi-scale framework that integrates Transformer encoders and MLPs, thereby leveraging their complementary strengths."

## Hedge verbs

- introduce / causal / abstract: "this paper introduces a novel deep learning architecture"
- propose / causal / introduction, conclusion: "this paper proposes a Dual-Branch Multi-Scale Transformer-MLP (DBMS)"; "This paper proposes a dual-branch multi-scale framework (DBMS)"
- demonstrate / associative / abstract, experiments: "Extensive experiments on eight real-world datasets demonstrate that DBMS significantly outperforms existing models"
- show / associative / conclusion: "Extensive evaluations show that DBMS delivers superior prediction accuracy and robustness across multiple benchmark datasets."

## Cross-section linkers

- introduction → related_work: 贡献清单后 `2. Related works`
- related_work → method: 双分支动机段落后 `3. Proposed method`
- method → experiments: Algorithm 1 后 `4. Experiments`
- experiments → conclusion: 效率与置信区间后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Related works`。
- R003 贡献清单用项目符号而非编号句。
- R009 自称：`this paper introduces` / `this paper proposes`

## Candidate phrases

- `To overcome these limitations, this paper introduces` (abstract)
- `To address these issues, this paper proposes` (introduction)
- `The main contributions of this work are as follows` (introduction)
- `This paper proposes a dual-branch multi-scale framework` (conclusion)

## House style

自称 `this paper introduces` / `this paper proposes` / `our work introduces` / `We propose`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Multivariate time series forecasting is crucial across various critical domains, including weather prediction, finance, traffic management, and industrial manufacturing.
- abstract: To overcome these limitations, this paper introduces a novel deep learning architecture: the Dual-Branch Multi-Scale Transformer-MLP (DBMS).
- abstract: Extensive experiments on eight real-world datasets demonstrate that DBMS significantly outperforms existing models based solely on Transformer or MLP, achieving state-of-the-art performance with superior robustness and stability.
- introduction: Long-term time series forecasting (LTSF) plays a critical role in various domains, including weather prediction (Lam et al., 2023), financial analysis (Zeng et al., 2023b), traffic scheduling (Xu et al., 2020), and industrial monitoring (Zamanzadeh Darban et al., 2024).
- introduction: Nevertheless, most existing approaches rely on a single architecture or fixed-scale design, limiting their ability to simultaneously capture both global and local temporal patterns.
- introduction: To address these issues, this paper proposes a Dual-Branch Multi-Scale Transformer-MLP (DBMS) for long-term time series forecasting.
- introduction: The main contributions of this work are as follows:
- related_work: Time Series Forecasting. Traditional statistical models such as ETS (Hyndman and Khandakar, 2008; Li et al., 2022), ARMA (Box and Jenkins, 1976), and ARIMA (Hyndman and Athanasopoulos, 2018) have long served as baselines for time series forecasting.
- method: In multivariate time series forecasting, the goal is to predict the future sequence based on historical observations.
- experiments: We evaluated the proposed model on eight widely used benchmark datasets, including four ETT datasets (ETTh1, ETTh2, ETTm1, ETTm2) and the Electricity, Traffic, Weather, and Solar datasets.
- conclusion: This paper proposes a dual-branch multi-scale framework (DBMS), a novel architecture that combines the strengths of Transformer encoders and multi-layer perceptrons (MLPs) to enhance time series forecasting.
- conclusion: Extensive evaluations show that DBMS delivers superior prediction accuracy and robustness across multiple benchmark datasets.
