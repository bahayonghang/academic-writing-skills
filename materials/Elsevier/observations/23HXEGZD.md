---
key: 23HXEGZD
title: "MSTFormer: A novel long-term time series prediction model for electricity consumption in the cement calcination process"
venue: "Chemical Engineering Science"
doi: "10.1016/j.ces.2025.122696"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-7,10-21"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work` → `3. Process analysis and variable selection for electricity consumption in the cement calcination process` → `4. The establishment of MSTFormer model` → `5. Experiment and result analysis` → `6. Conclusion`。前置 `ABSTRACT` 与 `Keywords`。独立 Related Work（`2. Related work`，机器学习、RNN/CNN、Transformer/Informer/Autoformer、分解–预测–重构）。Introduction 末有节序路标（指向 related work / method / experiments / conclusion）。Method 含 multi-channel input、VMD、spatiotemporal ProbSparse、gated fusion。Experiments 含 15/30/45/60 min 多长度对比与消融。

## Openers

- abstract: `The cement calcination` — "The cement calcination process is a critical and energy-intensive step in the cement production process, with electricity consumption accounting for the majority of overall energy consumption."
- introduction: `The cement calcination` — "The cement calcination process is a critical and energy-intensive step in the cement production process (Zhang et al., 2021), with electricity consumption accounting for the majority of overall energy consumption (Shen et al., 2017)."
- method: `Based on the` — "Based on the mechanistic analysis of the cement calcination process in the preceding chapter, the primary challenges in long-term electricity consumption forecasting stem from the pronounced long-term dependencies in electricity consumption data."
- experiments: `In this chapter` — "In this chapter, the proposed method is evaluated and validated on real production data from the cement calcination process to demonstrate its effectiveness."
- conclusion: `This study provides` — "This study provides a comprehensive analysis of the cement calcination process and explores the complex coupling relationships among process variables throughout the production workflow."

## Gap transitions

- however (introduction): "However, the cement calcination process is a highly complex physico-chemical reaction process, where electricity consumption is affected by the combined influence of multiple factors, including raw material properties, process parameters, equipment conditions, and environmental disturbances."
- therefore (introduction): "Therefore, the task of long sequence time-series forecasting (LSTF) of electricity consumption in the cement calcination process faces the challenge of modeling complex long-term dependencies."
- unlike (introduction): "Unlike traditional time series forecasting, which focuses on short-term trend modeling. Long sequence time-series forecasting (LSTF) aims to predict numerical evolution over longer time periods"
- nevertheless (introduction): "Nevertheless, cement calcination remains a highly energy-intensive process characterized by substantial complexity and a wide range of influencing factors."
- however (related-work): "However, with the continuous growth in data scale and complexity, traditional machine learning methods are increasingly limited in their modeling capacity and generalization performance (Fachini and Fuly, 2021)."
- to address (method): "To address these issues, this study proposes the MSTFormer model, which combines decomposition algorithms with self-attention mechanisms."

## Hedge verbs

- proposing / causal / abstract: "This paper addresses the challenge of long sequence time-series forecasting (LSTF) for electricity consumption in the cement calcination process by proposing a predictive model, MSTFormer."
- demonstrate / causal / abstract, experiments: "Experimental results on actual cement production datasets demonstrate that MSTFormer outperforms mainstream long-sequence forecasting models"; "to demonstrate its effectiveness"
- propose / causal / method, conclusion: "this study proposes the MSTFormer model"; "we propose MSTFormer"
- outperforms / causal / abstract, experiments: "MSTFormer outperforms mainstream long-sequence forecasting models across various prediction lengths"
- can facilitate / speculative / conclusion: "The proposed model can facilitate energy consumption optimization in the cement industry"

## Cross-section linkers

- introduction → related work: Introduction 末路标后 `2. Related work`
- related work → method: process analysis 后 `4. The establishment of MSTFormer model`
- method → experiments: gated fusion 后 `5. Experiment and result analysis`
- experiments → conclusion: ablation 后 `6. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Related work`。
- R003 节序路标：Introduction 末指向后续节。
- R009 自称：`This paper addresses` / `this study proposes` / `we propose MSTFormer`

## Candidate phrases

- `This paper addresses the challenge of long sequence time-series forecasting (LSTF) ... by proposing a predictive model, MSTFormer` (abstract)
- `To address these issues, this study proposes the MSTFormer model` (method)
- `In this chapter, the proposed method is evaluated and validated on real production data` (experiments)
- `This study provides a comprehensive analysis of the cement calcination process` (conclusion)
- `we propose MSTFormer, a multi-channel time series input-spatiotemporal ProbSparse self-attention model` (conclusion)

## House style

自称 `This paper addresses` / `this study proposes` / `we propose` / `This study provides`。第一人称复数与 `this study` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The cement calcination process is a critical and energy-intensive step in the cement production process, with electricity consumption accounting for the majority of overall energy consumption.
- abstract: This paper addresses the challenge of long sequence time-series forecasting (LSTF) for electricity consumption in the cement calcination process by proposing a predictive model, MSTFormer.
- abstract: Experimental results on actual cement production datasets demonstrate that MSTFormer outperforms mainstream long-sequence forecasting models across various prediction lengths.
- abstract: For 15-minute prediction length, the model achieves an MAE of 0.063 and R2 of 0.991.
- introduction: The cement calcination process is a critical and energy-intensive step in the cement production process (Zhang et al., 2021), with electricity consumption accounting for the majority of overall energy consumption (Shen et al., 2017).
- related-work: As mentioned in Chapter 1, the electricity consumption signal in the cement calcination process is characterized by high time-delay, pronounced nonlinearity, and multivariate coupling (Hao et al., 2020).
- method: To address these issues, this study proposes the MSTFormer model, which combines decomposition algorithms with self-attention mechanisms.
- experiments: In this chapter, the proposed method is evaluated and validated on real production data from the cement calcination process to demonstrate its effectiveness.
- experiments: The proposed model demonstrates superior prediction accuracy at the 15-minute prediction length, with MAE and RMSE reaching 0.063 and 0.099, respectively, and an R2 of 0.991.
- conclusion: This study provides a comprehensive analysis of the cement calcination process and explores the complex coupling relationships among process variables throughout the production workflow.
- conclusion: On this basis, we propose MSTFormer, a multi-channel time series input-spatiotemporal ProbSparse self-attention model that integrates data decomposition and self-attention mechanisms.
- conclusion: Comparative experiments on various decomposition and prediction algorithms indicate that MSTFormer consistently outperforms benchmark methods across all prediction lengths
