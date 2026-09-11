---
key: E3GDTUS9
title: "Effective energy consumption forecasting using empirical wavelet transform and long short-term memory"
venue: "Energy"
doi: "10.1016/j.energy.2021.121756"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-4,8-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Literature review on energy consumption forecasting` → `3. Methodology` → `4.` 评价指标 → `5. Experiments and results analysis` → `6. Conclusions`。前置 `abstract` 与 `Keywords`。独立 Related Work（`2. Literature review on energy consumption forecasting`，单模型、混合模型、MARKAL/LEAP）。Introduction 末有字母编号贡献 `(a)`–`(c)` + 节序路标。Method 标题为 `3. Methodology`（EWT、attention-based LSTM、EWT-attention-LSTM）。Experiments 标题为 `5. Experiments and results analysis`（湖北工业用电、中国总用电、美国石油制品）。

## Openers

- abstract: `Energy consumption is` — "Energy consumption is an important issue of global concern."
- introduction: `Energy consumption has` — "Energy consumption has been gradually increasing along with the growth of the economy and the development of the population."
- method: `In this section` — "In this section, the EWT-attention-LSTM model is described."
- experiments: `In this section` — "In this section, the EWT-attention-LSTM model is tested by three real-life data sets."
- conclusion: `This study aims` — "This study aims to apply an enhanced LSTM prediction method based on empirical wavelet transform and attention-based mechanism in the monthly energy consumption forecasting."

## Gap transitions

- although (abstract): "Although there are various energy consumption forecasting methods, the forecasting accuracy still needs to be improved."
- therefore (abstract): "Therefore, the proposed model is a satisfactory method for energy consumption forecasting due to its high accuracy."
- however (introduction): "However, energy consumption is also naturally affected by some coupled factors, such as economic development, national energy policy, energy production capacity, and weather conditions, resulting in a remaining challenge to design a high-precision energy consumption forecasting technology [2]."
- therefore (introduction): "Therefore, it is able to identify and decompose the trend components and the periodic components in the original energy consumption data by EWT."
- however (literature): "However, all methods have disadvantages and advantages."
- therefore (literature): "Therefore, it is quite necessary to design the effective EWT-attention-LSTM model to analyze the interaction between various influencing factors and the specific components of energy consumption."

## Hedge verbs

- applied / causal / abstract: "This study applied a long short-term memory-based model in energy consumption forecasting"
- show / associative / abstract: "Results of one comparative example and two extended applications show the proposed model achieves better prediction accuracy"
- aims / causal / introduction, conclusion: "The main target of this study is to apply the effective LSTM-based model"; "This study aims to apply an enhanced LSTM prediction method"
- employed / causal / introduction: "This is the first time that the EWT-attention-LSTM prediction approach is employed to forecast energy demand."
- achieves / associative / conclusion: "EWT-attention-LSTM model achieves the best predictive effect"

## Cross-section linkers

- introduction → related work: "The remainder of this work is structured as follows: the literature review on energy consumption forecasting is present in Section 2. Next, Section 3 and Section 4 introduce the adopted methods and the evaluation metrics, respectively. Section 5 then presents the experiments. Finally, Section 6 concludes this work."
- related work → method: literature 缺口段落后 `3. Methodology`
- method → experiments: metrics 后 `5. Experiments and results analysis`
- experiments → conclusion: Wilcoxon 检验后 `6. Conclusions`

## Candidate rules

- R001 独立 Related Work：`2. Literature review on energy consumption forecasting`。
- R003 节序路标：`The remainder of this work is structured as follows`
- R004 编号贡献：`the main contributions of this study are as following`
- R009 自称：`This study applied` / `This study aims`

## Candidate phrases

- `This study applied a long short-term memory-based model in energy consumption forecasting` (abstract)
- `The remainder of this work is structured as follows` (introduction)
- `In this section, the EWT-attention-LSTM model is described.` (method)
- `In this section, the EWT-attention-LSTM model is tested by three real-life data sets.` (experiments)
- `This study aims to apply an enhanced LSTM prediction method` (conclusion)

## House style

自称 `This study applied` / `This study aims` / `the proposed model`。少用 `we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Energy consumption is an important issue of global concern.
- abstract: Although there are various energy consumption forecasting methods, the forecasting accuracy still needs to be improved.
- abstract: This study applied a long short-term memory-based model in energy consumption forecasting to achieve a better prediction performance and the more critical influencing factors are emphasized.
- abstract: Therefore, the proposed model is a satisfactory method for energy consumption forecasting due to its high accuracy.
- introduction: Energy consumption has been gradually increasing along with the growth of the economy and the development of the population.
- introduction: The remainder of this work is structured as follows: the literature review on energy consumption forecasting is present in Section 2.
- related-work: Energy consumption prediction is challenging as energy demand is greatly dependent on various factors, such as economic development, national energy policy, weather conditions, and energy production capacity [3].
- method: In this section, the EWT-attention-LSTM model is described.
- experiments: In this section, the EWT-attention-LSTM model is tested by three real-life data sets.
- experiments: The EWT-attention-LSTM prediction model is superior to other prediction methods according to the results of MAE, MAPE, and RMSE.
- conclusion: This study aims to apply an enhanced LSTM prediction method based on empirical wavelet transform and attention-based mechanism in the monthly energy consumption forecasting.
- conclusion: For experiment 2-3, EWT-attention-LSTM model achieves the best predictive effect compared with SVR, BPNN, RNN, GRU, LSTM, and attention-based LSTM model in terms of MAE, MAPE, and RMSE.
