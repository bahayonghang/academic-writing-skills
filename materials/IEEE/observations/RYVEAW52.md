---
key: RYVEAW52
title: "Long-Term Time Series Forecasting With Multilinear Trend Fuzzy Information Granules for LSTM in a Periodic Framework"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2023.3298970"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BASIC NOTIONS AND RESULTS` → `III. LONG-TERM TIME SERIES FORECASTING VIA MULTI-LINEAR TREND FIGS FOR LSTM IN A PERIODIC FRAMEWORK` → `IV. EVALUATIONS AND COMPARISONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 ARMA、LSTM、FIG、DTW、多线性趋势粒）。Introduction 末有节序路标，指向 Section II–V。Method 为 III，含 Algorithm 1–3。Experiments 标题为 `EVALUATIONS AND COMPARISONS`（Mackey–Glass / 日气温 / 月太阳黑子 / 月径流）。

## Openers

- abstract: `Considerable research achievements` — "Considerable research achievements have been made in utilizing information granulation as an effective technique for addressing long-term time-series forecasting." (p.1)
- introduction: `TIME series, a` — "TIME series, a prevalent type of data, can be found in various domains, such as finance, environment, energy, biology, and more [1], [2], [3], [4]." (p.1；栏首掉字)
- method: `Numerous researchers have` — "Numerous researchers have put forth various models for GTS analysis." (p.4, III)
- experiments: `In this section` — "In this section, we aim to demonstrate the feasibility and effectiveness of the proposed prediction model by conducting a comparative analysis with other existing models on the data set." (p.8, IV)
- conclusion: `We have developed` — "We have developed a long-term time series forecasting model within the periodic framework of LSTM, incorporating multilinear trend fuzzy information particles." (p.14)

## Gap transitions

- however (abstract): "However, existing studies suffer from limitations in their failure to account for the impact of periodicity on information granulation." (p.1)
- to address (abstract): "To address the aforementioned issues, this article presents a novel approach for long-term time series forecasting by employing a multilinear trend fuzzy information granule (FIG) within a periodic framework for LSTM." (p.1)
- however (introduction): "However, their drawback is the inability to capture the underlying interconnections and analyze the correlation between factors." (p.1)
- nevertheless (introduction): "Nevertheless, most studies primarily focus on the importance of single-point prediction, neglecting the challenge of long-term prediction [17]." (p.1)
- however (introduction): "However, when it comes to long-term forecasting, the accumulation of small errors during data processing can result in cumulative errors." (p.1)
- however (introduction): "However, this approach results in the loss of significant trend information." (p.2)
- nonetheless (introduction): "Nonetheless, the use of back propagation neural network (BPNN) may limit the model's learning capacity." (p.2)
- however (introduction): "However, the division of periods considered in this model is based on conceptual periods rather than the actual characteristics of time series data." (p.2)

## Hedge verbs

- present / causal / abstract: "this article presents a novel approach for long-term time series forecasting"
- propose / causal / introduction: "we propose a time window segmentation algorithm that aligns with the inherent periodicity of the time series."
- demonstrate / causal / abstract, experiments: "Experimental results on open time series demonstrate the superior performance of the proposed forecasting model."; "we aim to demonstrate the feasibility and effectiveness"
- show / causal / experiments: "As shown in Table V, BPNN performs the best on the chaotic Mackey–Glass time series if the prediction range is 1"
- develop / causal / conclusion: "We have developed a long-term time series forecasting model"

## Cross-section linkers

- introduction → notions: "The rest of this article is organized as follows. Section II introduces several key concepts, including l1-trend filtering, GLFIG, distance between GLFIGs, DTW, and LSTM. In Section III, we delve into the detailed predictive modeling. Section IV presents the results of experimental studies conducted on popular time series data sets. Finally, Section V concludes this article." (p.3)
- method → experiments: Step 5 翻译预测结果后直接 `IV. EVALUATIONS AND COMPARISONS` (p.8)
- experiments → conclusion: 模型利弊段落后直接 `V. CONCLUSION` (p.14)

## Candidate rules

- R001 abstract 用 `To address the aforementioned issues, this article presents a novel approach`，方法名放在 `by employing` 之后。
- R002 Introduction 无独立 Related Work，动机与创新分成 `The research motivations are outlined as follows` 与 `The main innovations are outlined as follows` 两组编号。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 Experiments 节名 `EVALUATIONS AND COMPARISONS`，开篇 `we aim to demonstrate`。
- R005 Conclusion 用第一人称完成时 `We have developed`，展望用 `In future research, the following aspects warrant further exploration.`

## Candidate phrases

- `To address the aforementioned issues, this article presents a novel approach` (abstract)
- `The main innovations are outlined as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this section, we aim to demonstrate the feasibility and effectiveness of` (experiments)
- `We have developed a ... model` (conclusion)

## House style

自称是 `this article` / `we` / `our model`。未见 `Here we`。`this article presents` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。Conclusion 用第一人称 `We have developed`。

## Quotes

- p.1 abstract: Considerable research achievements have been made in utilizing information granulation as an effective technique for addressing long-term time-series forecasting.
- p.1 abstract: However, existing studies suffer from limitations in their failure to account for the impact of periodicity on information granulation.
- p.1 abstract: To address the aforementioned issues, this article presents a novel approach for long-term time series forecasting by employing a multilinear trend fuzzy information granule (FIG) within a periodic framework for LSTM.
- p.1 abstract: Experimental results on open time series demonstrate the superior performance of the proposed forecasting model.
- p.1 introduction: TIME series, a prevalent type of data, can be found in various domains, such as finance, environment, energy, biology, and more [1], [2], [3], [4].
- p.1 introduction: However, their drawback is the inability to capture the underlying interconnections and analyze the correlation between factors.
- p.1 introduction: Nevertheless, most studies primarily focus on the importance of single-point prediction, neglecting the challenge of long-term prediction [17].
- p.1 introduction: However, when it comes to long-term forecasting, the accumulation of small errors during data processing can result in cumulative errors.
- p.2 introduction: However, this approach results in the loss of significant trend information.
- p.2 introduction: Nonetheless, the use of back propagation neural network (BPNN) may limit the model's learning capacity.
- p.2 introduction: However, the division of periods considered in this model is based on conceptual periods rather than the actual characteristics of time series data.
- p.3 introduction: The main innovations are outlined as follows.
- p.3 introduction: We integrate the periodicity of time series with granularity prediction.
- p.3 introduction: The rest of this article is organized as follows. Section II introduces several key concepts, including l1-trend filtering, GLFIG, distance between GLFIGs, DTW, and LSTM. In Section III, we delve into the detailed predictive modeling. Section IV presents the results of experimental studies conducted on popular time series data sets. Finally, Section V concludes this article.
- p.4 method: Numerous researchers have put forth various models for GTS analysis.
- p.4 method: This article addresses these challenges by introducing a novel forecasting model.
- p.8 experiments: In this section, we aim to demonstrate the feasibility and effectiveness of the proposed prediction model by conducting a comparative analysis with other existing models on the data set.
- p.14 conclusion: We have developed a long-term time series forecasting model within the periodic framework of LSTM, incorporating multilinear trend fuzzy information particles.
- p.14 conclusion: Experimental analysis verifies the outstanding performance of our model in the task of long-term forecasting.
- p.14 conclusion: In future research, the following aspects warrant further exploration.
