---
key: 72F9JMSA
title: "Wavelet-Seq2Seq-LSTM with attention for time series forecasting of level of dams in hydroelectric power plants"
venue: "Energy"
doi: "10.1016/j.energy.2023.127350"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related works` → `3. Reservoir level control in hydroelectric power plants` → `4. Wavelet-Seq2Seq-LSTM with attention` → `5. Analysis of results` → `6. Conclusion and future directions of research`。前置 `ABSTRACT` 与 `Keywords`。独立 Related Work（`2. Related works`，时序预测、水库/水电、LSTM/attention/wavelet 文献计量）。Introduction 末有项目符号贡献 + 节序路标。Method 标题为 `4. Wavelet-Seq2Seq-LSTM with attention`（attention、wavelet denoising、limitations、experiment setup）。Experiments 标题为 `5. Analysis of results`（Seq2Seq LSTM、attention、wavelet、统计、ensemble benchmarking）。

## Openers

- abstract: `Reservoir level control` — "Reservoir level control in hydroelectric power plants has importance for the stability of the electric power supply over time and can be used for flood control."
- introduction: `The operation planning` — "The operation planning of hydroelectric plants is based on an economic evaluation, in which the management of the useful volume of the plants is evaluated in relation to the optimization of the generation power system [1], the available volume of the reservoirs with time-dependency results in a variation in the price of electricity, considering the thermal generation [2]."
- method: `This section explains` — "This section explains the structure of the proposed Wavelet-Seq2Seq-LSTM with Attention method."
- experiments: `The first analysis` — "The first analysis to evaluate the proposed method is to study the loss function, the loss function of the training and validation process is shown in Fig. 10."
- conclusion: `The abrupt variation` — "The abrupt variation in the dam level can result in an emergency condition, in which the management responsibility for the power plant and its surroundings becomes to the operation manager of the power plant and the emergency committee previously defined for this situation."

## Gap transitions

- in this sense (abstract): "In this sense, this paper proposes a sequence-to-sequence (Seq2Seq) long short-term memory (LSTM) neural network model with an attention mechanism and wavelet transform for noise reduction to predict reservoir levels for a one-hour horizon in advance."
- even though (related-work): "Even though autoregressive models, such as autoregressive-integrated moving average (ARIMA) are efficient [32], problems with nonlinearity have made new and more sophisticated techniques necessary"
- considering that (introduction): "Considering that this paper forecasts one step ahead horizon, and each record is taken every hour, a forecast of one hour ahead will be obtained."

## Hedge verbs

- proposes / causal / abstract, introduction: "this paper proposes a sequence-to-sequence (Seq2Seq) long short-term memory (LSTM) neural network model"; "this paper proposes the Wavelet-Seq2Seq-LSTM with Attention model"
- demonstrate / causal / abstract: "Results demonstrate that the proposed approach outperforms other LSTM models with a mean squared error of 0.0020 and a mean absolute error of 0.0347."
- prove / associative / conclusion: "This result proves that the attention mechanism can make the Seq2Seq LSTM more robust"
- outperformed / causal / conclusion: "the proposed Wavelet-Seq2Seq-LSTM with Attention outperformed other variations of Seq2Seq-based approaches"
- shows / associative / related-work: "the available literature has demonstrated that the attention mechanism shows promise"

## Cross-section linkers

- introduction → related work: "The remainder of this document is organized in the following manner: Section 2 presents the related works regarding time series forecasting models."
- related work → method: Section 3 工况后 `4. Wavelet-Seq2Seq-LSTM with attention`
- method → experiments: experiment setup 后 `5. Analysis of results`
- experiments → conclusion: related works comparison 后 `6. Conclusion and future directions of research`

## Candidate rules

- R001 独立 Related Work：`2. Related works`。
- R003 节序路标：`The remainder of this document is organized in the following manner`
- R004 编号贡献：`The main contributions of this research are:`
- R009 自称：`this paper proposes` / `In this paper, we leverage`

## Candidate phrases

- `In this sense, this paper proposes a sequence-to-sequence (Seq2Seq) long short-term memory (LSTM) neural network model` (abstract)
- `The main contributions of this research are:` (introduction)
- `The remainder of this document is organized in the following manner` (introduction)
- `This section explains the structure of the proposed Wavelet-Seq2Seq-LSTM with Attention method.` (method)
- `the proposed Wavelet-Seq2Seq-LSTM with Attention outperformed other variations of Seq2Seq-based approaches` (conclusion)

## House style

自称 `this paper proposes` / `we leverage` / `Results demonstrate`。第一人称较少，多用 `this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Reservoir level control in hydroelectric power plants has importance for the stability of the electric power supply over time and can be used for flood control.
- abstract: In this sense, this paper proposes a sequence-to-sequence (Seq2Seq) long short-term memory (LSTM) neural network model with an attention mechanism and wavelet transform for noise reduction to predict reservoir levels for a one-hour horizon in advance.
- abstract: Results demonstrate that the proposed approach outperforms other LSTM models with a mean squared error of 0.0020 and a mean absolute error of 0.0347.
- introduction: The operation planning of hydroelectric plants is based on an economic evaluation, in which the management of the useful volume of the plants is evaluated in relation to the optimization of the generation power system [1]
- introduction: The remainder of this document is organized in the following manner: Section 2 presents the related works regarding time series forecasting models.
- related-work: Time series is a collection of observations made over time in chronological order, which can be utilized for a variety of things, including resolving mathematical puzzles [16]
- method: This section explains the structure of the proposed Wavelet-Seq2Seq-LSTM with Attention method.
- experiments: The first analysis to evaluate the proposed method is to study the loss function, the loss function of the training and validation process is shown in Fig. 10.
- experiments: The best results were found using the BayesShrink method with 6 levels of the wavelet transform, having a smaller error than all the analyses presented until this assessment
- conclusion: The abrupt variation in the dam level can result in an emergency condition, in which the management responsibility for the power plant and its surroundings becomes to the operation manager of the power plant and the emergency committee previously defined for this situation.
- conclusion: This result proves that the attention mechanism can make the Seq2Seq LSTM more robust, reducing its variability for time series prediction.
