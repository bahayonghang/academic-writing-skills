---
key: J5UBKSPK
title: "Modwkan: Harnessing Maximal Overlap Discrete Wavelet Transform and Kan for Time Series Forecasting"
venue: "ICASSP 2026 - 2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)"
doi: "10.1109/ICASSP55912.2026.11462044"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-5"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

阿拉伯数字标题：`1. INTRODUCTION` → `2. METHOD` → `3. EXPERIMENTS` → `4. CONCLUSION`。前置 `ABSTRACT` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 ARIMA / RNN / Transformer / Autoformer / DLinear，再评 FFT / DWT、AlignTime、THATSN）。Introduction 末无 `The rest of this paper is organized` 路标，直接进入方法。Method 拆成 MFD / KFRL / IFR。Experiments 含 setup、main results、ablation。

## Openers

- abstract: `Existing time series` — "Existing time series forecasting methods have achieved encouraging results by leveraging frequency information to learn data periodic patterns, yet two issues remain." (p.901)
- introduction: `Multivariate time series` — "Multivariate time series forecasting underpins energy scheduling, weather services, and medical treatment [1, 2, 3]." (p.901)
- method: `Given a input` — "Given a input batch of time series data X ∈ R^{B×T×C}, where B, T, and C denote batch size, historical window length, and channel number, respectively, the time series forecasting aims to accurately predicting future values Y ∈ R^{B×H×C} with the horizon window length H." (p.902)
- experiments: `We evaluate the` — "We evaluate the proposed model using six public datasets: Electricity Transformer Datasets (ETTm1, ETTm2, ETTh1, ETTh2), Weather, and Electricity." (p.903)
- conclusion: `This paper presents` — "This paper presents MODWKAN, integrating MODWT for shift-invariant decomposition with dynamic-order KANs for frequency-specific modeling." (p.904)

## Gap transitions

- yet (abstract): "Existing time series forecasting methods have achieved encouraging results by leveraging frequency information to learn data periodic patterns, yet two issues remain." (p.901)
- to address (abstract): "To address these issues, MODWKAN is proposed for time series forecasting." (p.901)
- however (introduction): "However, existing methods mostly use a unified fixed architecture, struggling to balance model size and capability." (p.901)
- despite (introduction): "Despite efforts to improve frequency modeling, these time-frequency-based methods still fail to simultaneously preserve temporal resolution and capture complete dynamics across all frequency components." (p.901)
- to address (introduction): "To address these limitations, we propose MODWKAN, designed to sequentially tackle time-frequency resolution imbalance and inflexible frequency representation learning." (p.901)
- while (conclusion): "While the channel-independent design limits capturing high-dimensional inter-variable correlations, MODWKAN effectively resolves aliasing and fixed-architecture issues." (p.904)

## Hedge verbs

- propose / causal / introduction: "we propose MODWKAN, designed to sequentially tackle"
- demonstrate / causal / abstract: "Experiments conducted on six public datasets, in comparison with ten state-of-the-art methods, demonstrate that MODWKAN achieves competitive performance."
- show / causal / introduction, experiments: "Experimental results on six datasets show that MODWKAN achieves superior performance"; "The results show that the complete MODWKAN achieves more competitive MSE and MAE"
- present / causal / conclusion: "This paper presents MODWKAN"
- confirm / causal / experiments: "This confirms MODWT’s anti-aliased decomposition effectively addresses flaws in traditional time-frequency tools"

## Cross-section linkers

- introduction → method: Introduction 以实验综述收束后直接 `2. METHOD`，无节序路标。(p.901–902)
- method → experiments: IFR 段落后接 `3. EXPERIMENTS` / `3.1. Experimental Setup` (p.903)
- experiments → conclusion: ablation 后直接 `4. CONCLUSION` (p.904)

## Candidate rules

- R001 摘要用被动 `MODWKAN is proposed for`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，时频分解缺陷写在引言中段。
- R003 Introduction 末无 `organized as follows`，贡献嵌入 `To address these limitations, we propose`。
- R004 Experiments 按 Datasets / Comparison Method / Implementation Details 分条。
- R005 Conclusion 先收回方法，再用 `While` 承认通道独立局限。

## Candidate phrases

- `To address these issues, MODWKAN is proposed for` (abstract)
- `To address these limitations, we propose MODWKAN` (introduction)
- `Experiments conducted on six public datasets, in comparison with ten state-of-the-art methods, demonstrate that` (abstract)
- `This paper presents MODWKAN, integrating` (conclusion)

## House style

自称是 `we propose` / `we employ` / `we introduce` / `This paper presents` / `our current framework`。未见 `Here we`。`This paper presents` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 开篇自称（结论用 `This paper presents`）。

## Quotes

- p.901 abstract: Existing time series forecasting methods have achieved encouraging results by leveraging frequency information to learn data periodic patterns, yet two issues remain.
- p.901 abstract: To address these issues, MODWKAN is proposed for time series forecasting.
- p.901 abstract: Experiments conducted on six public datasets, in comparison with ten state-of-the-art methods, demonstrate that MODWKAN achieves competitive performance.
- p.901 introduction: Multivariate time series forecasting underpins energy scheduling, weather services, and medical treatment [1, 2, 3].
- p.901 introduction: However, existing methods mostly use a unified fixed architecture, struggling to balance model size and capability.
- p.901 introduction: Despite efforts to improve frequency modeling, these time-frequency-based methods still fail to simultaneously preserve temporal resolution and capture complete dynamics across all frequency components.
- p.901 introduction: To address these limitations, we propose MODWKAN, designed to sequentially tackle time-frequency resolution imbalance and inflexible frequency representation learning.
- p.901 introduction: Experimental results on six datasets show that MODWKAN achieves superior performance over state-of-the-art baselines spanning three key method categories, while delivering notable reductions in prediction error compared to existing approaches.
- p.902 method: Given a input batch of time series data X ∈ R^{B×T×C}, where B, T, and C denote batch size, historical window length, and channel number, respectively, the time series forecasting aims to accurately predicting future values Y ∈ R^{B×H×C} with the horizon window length H.
- p.903 experiments: We evaluate the proposed model using six public datasets: Electricity Transformer Datasets (ETTm1, ETTm2, ETTh1, ETTh2), Weather, and Electricity.
- p.904 experiments: The results show that the complete MODWKAN achieves more competitive MSE and MAE on ETTh1 and ETTh2 datasets compared to its ablated variants.
- p.904 conclusion: This paper presents MODWKAN, integrating MODWT for shift-invariant decomposition with dynamic-order KANs for frequency-specific modeling.
- p.904 conclusion: While the channel-independent design limits capturing high-dimensional inter-variable correlations, MODWKAN effectively resolves aliasing and fixed-architecture issues.
