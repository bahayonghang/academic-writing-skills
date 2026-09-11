---
key: TJBED8WM
title: "Online cement clinker quality monitoring: A soft sensor model based on multivariate time series analysis and CNN"
venue: "ISA Transactions"
doi: "10.1016/j.isatra.2021.01.058"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related works` → `3. Cement industry process and variable selection` → `4. Method description` → `5. Experimental result` → `6. Conclusions`。前置 `ABSTRACT` / `Keywords`。独立 `2. Related works`。`related_work=independent`。Introduction 末有节序路标。Method 含 MVTS-CNN 结构、多元时间序列分析、CNN 特征提取、训练。Experiments 含数据集、参数优化、ablation、对比实验。

## Openers

- abstract: `The content of` — "The content of free calcium oxide (f-CaO) in cement clinker is an important index for cement quality."
- introduction: `Cement is an` — "Cement is an important material in national infrastructure construction."
- method: `Taking the time` — "Taking the time series within the active duration distribution range as input data can increase the model’s applicability in different production conditions."
- experiments: `Before analyze the` — "Before analyze the multivariate time series, the entire process time T is set as the longest process time of 55 min."
- conclusion: `According to the` — "According to the problems of time-varying delay, strong coupling and nonlinear in cement production process in the f-CaO content soft sensor modeling, we proposed a soft sensor model based on multivariate time series analysis and CNN (MVTS–CNN) in this paper."

## Gap transitions

- therefore (introduction): "Therefore, it is necessary to develop an online real-time f-CaO content monitoring method."
- however (introduction): "However, most previous works tend to propose their own modeling method for the common characteristics of coupling, time delay and nonlinearity, without considering the process industry exclusive characteristics."
- however (introduction): "However, the active duration of each process in cement clinker production is different, and some further researches are needed for the traditional CNN to extract the features of multivariate and multiple time lengths."
- however (related work): "However, although the rotary kiln is a key equipment in clinker production process, it needs the cooperation of other equipment to complete cement clinker production."
- however (related work): "However, the residence time of material in each equipment is changing in different production conditions, so the timing matching points of input variables are also changing."
- therefore (related work): "Meanwhile, due to their own limitations, it is necessary to explore new approaches and algorithms for the f-CaO content soft sensor modeling."

## Hedge verbs

- is proposed / causal / abstract: "Aiming at the characteristics of strong coupling, time-varying delay and highly non-linearity in cement clinker production, a soft sensor model based on multivariate time series analysis and convolutional neural network (MVTS–CNN) is proposed for the online f-CaO content monitoring."
- demonstrate / associative / abstract: "Compared with traditional CNN, support vector machines (SVM) and long-short term memory networks (LSTM), the results demonstrate that the MVTS–CNN model has higher accuracy, better generalization ability and superior robustness."
- proposed / causal / introduction: "This paper proposed a soft sensor model based on multivariate time series analysis and convolutional neural network (MVTS–CNN) for the online f-CaO content monitoring."
- we proposed / causal / conclusion: "we proposed a soft sensor model based on multivariate time series analysis and CNN (MVTS–CNN) in this paper."
- showed / associative / conclusion: "And the comparative experiments also showed that the MVTS–CNN model has higher accuracy, better generalization ability and superior stability."
- proposes / causal / conclusion: "This paper proposes a novel multivariate segment-to-point soft sensor model for the online f-CaO content monitoring."

## Cross-section linkers

- introduction → related work: "The remainder of this paper is organized as follows: some related works are introduced in Section 2."
- related work → process: "In Section 3, the cement calcination production process and its coupling relationship are reviewed and analyzed"
- process → method: "The proposed MVTS–CNN model is detailed described in Section 4, and its related algorithms are introduced in detail."
- method → experiments: "In Section 5, we optimized the parameters and structures of the MVTS–CNN model and tested the validity of related algorithms."
- experiments → conclusion: "Finally, the conclusion of this paper is made in Section 6."

## Candidate rules

- R001 独立 Related Work：`2. Related works`。
- R003 节序路标：`The remainder of this paper is organized as follows`
- R004 结论编号贡献：`Overall, the contributions and innovations in this paper are as flows:`
- R009 自称：`This paper proposed` / `we proposed` / `This paper proposes`

## Candidate phrases

- `a soft sensor model based on multivariate time series analysis and convolutional neural network (MVTS–CNN) is proposed` (abstract)
- `The remainder of this paper is organized as follows: some related works are introduced in Section 2.` (introduction)
- `This paper proposed a soft sensor model based on multivariate time series analysis and convolutional neural network (MVTS–CNN)` (introduction)
- `we proposed a soft sensor model based on multivariate time series analysis and CNN (MVTS–CNN) in this paper` (conclusion)
- `This paper proposes a novel multivariate segment-to-point soft sensor model` (conclusion)

## House style

自称 `This paper proposed` / `we proposed` / `This paper proposes`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The content of free calcium oxide (f-CaO) in cement clinker is an important index for cement quality.
- abstract: Aiming at the characteristics of strong coupling, time-varying delay and highly non-linearity in cement clinker production, a soft sensor model based on multivariate time series analysis and convolutional neural network (MVTS–CNN) is proposed for the online f-CaO content monitoring.
- abstract: Compared with traditional CNN, support vector machines (SVM) and long-short term memory networks (LSTM), the results demonstrate that the MVTS–CNN model has higher accuracy, better generalization ability and superior robustness.
- introduction: Cement is an important material in national infrastructure construction.
- introduction: However, most previous works tend to propose their own modeling method for the common characteristics of coupling, time delay and nonlinearity, without considering the process industry exclusive characteristics.
- introduction: The remainder of this paper is organized as follows: some related works are introduced in Section 2.
- related work: The data-driven soft sensor modeling based on historical data has been widely developed and applied in recent years [11].
- method: Taking the time series within the active duration distribution range as input data can increase the model’s applicability in different production conditions.
- experiments: According to evaluation indexes of the testing results in Table 9, the test results are analyzed from three aspects:
- conclusion: According to the problems of time-varying delay, strong coupling and nonlinear in cement production process in the f-CaO content soft sensor modeling, we proposed a soft sensor model based on multivariate time series analysis and CNN (MVTS–CNN) in this paper.
- conclusion: This paper proposes a novel multivariate segment-to-point soft sensor model for the online f-CaO content monitoring.
