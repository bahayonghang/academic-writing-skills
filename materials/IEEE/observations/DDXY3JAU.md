---
key: DDXY3JAU
title: "A Data-Driven Scale-Adaptive Time-Frequency Convolutional Network for Long Sequence Time-Series Forecasting"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2025.3619521"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9,13-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PRELIMINARY` → `IV. METHODOLOGY` → `V. EXPERIMENTS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（II，按 Transformer / multi-scale / time-frequency / pre-trained 四段）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–VI。Method 在 IV。Experiments 标题为 `V. EXPERIMENTS`（九数据集 + ablation）。III 为 Preliminary（定义与指标）。

## Openers

- abstract: `Models based on` — "Models based on Transformer variants have consistently demonstrated leading performance in long sequence time series forecasting." (p.6750)
- introduction: `LONG-SEQUENCE time-series forecasting` — "LONG-SEQUENCE time-series forecasting (LSTF) is a critical area in data mining, which is widely applied in fields such as financial market prediction [1], [2], [3], weather forecasting [4], [5], [6], energy demand forecasting [7], [8], [9], traffic flow prediction [10], [11], [12], and medical diagnostics [13], [14], [15], among others [16], [17], [18]." (p.6750；栏首掉字)
- related_work: `Transformer and its` — "Transformer and its variants [2], [28], [34], [37], [38] have been at the forefront of LSTF due to the ability of self-attention to capture long-term dependencies of arbitrary length." (p.6752, II)
- method: `To capture features` — "To capture features in complex real-world time-series data, we propose a data-driven adaptive time-frequency convolutional network for LSTF, comprising a pre-training model and a prediction model, as shown in Fig. 2." (p.6753, IV)
- experiments: `In this section` — "In this section, we address two key questions: (1) How effective is STCNet?" (p.6758, V)
- conclusion: `We propose a` — "We propose a data-driven scale-adaptive convolutional network (STCNet) for long-term time series forecasting." (p.6762)

## Gap transitions

- however (abstract): "However, in some complex application scenarios, Transformers tend to capture low-frequency information in the data while overlooking high-frequency information, which often contains rich non-stationary features." (p.6750)
- to address (abstract): "To address this issue, we explicitly represent both low-frequency and high-frequency information and propose a model called STCNet" (p.6750)
- in summary (introduction): "In summary, existing methods face three main challenges:" (p.6751)
- although (introduction): "Although recent studies[4],[20],[21],[31],[32],[33]transform and model sequences in the frequency domain to capture complex patterns and variations, they often rely on Fourier transforms, which tend to average out important local non-stationary features." (p.6751)
- to address (introduction): "To address these challenges, we propose STCNet, a data-driven, scale-adaptive time-frequency convolutional network for long-sequence time-series forecasting." (p.6751)
- while (conclusion): "While STCNet demonstrates strong performance on non-stationary datasets by focusing on high-frequency components, its improvements on stationary datasets are relatively less pronounced." (p.6762)

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "we ... propose a model called STCNet"; "we propose STCNet"; "We propose a data-driven scale-adaptive convolutional network (STCNet)"
- demonstrate / causal / abstract: "Experimental results on nine datasets demonstrate that STCNet outperforms the current state-of-the-art models"
- show / causal / introduction: "Fig. 1 shows that different datasets contain varying amounts of high- and low-frequency information"
- may / speculative / introduction: "Simple single-scale models may not effectively capture and utilize the information at these varying time scales"; "they may lack sufficient representational capacity"
- suggest / causal / experiments: "The above results suggest that extracting high-frequency non-stationary information is critical"

## Cross-section linkers

- introduction → related work / preliminary / method / experiments / conclusion: "The remainder of this paper is structured as follows: Section II reviews existing methods for long time-series forecasting. Section III defines the problem to be solved and introduces preliminaries. Section IV provides a detailed description of the proposed architecture. Section V presents the experimental methods and results. Finally, Section VI summarizes our forecasting research, analyzes the limitations, and outlines key directions for future research." (p.6752)
- related work → preliminary: Pre-trained models 段落后直接 `III. PRELIMINARY` (p.6752)
- preliminary → method: Evaluation Metrics 后直接 `IV. METHODOLOGY` (p.6753)
- method → experiments: Regression / TTT head 后直接 `V. EXPERIMENTS` (p.6758)
- experiments → conclusion: Ablation Table VI 后直接 `VI. CONCLUSION` (p.6762)

## Candidate rules

- R001 abstract 先肯定 Transformer SOTA，再用 `However` 指出重低频轻高频，`To address this issue, we ... propose`。
- R002 Introduction 用频谱图（Fig. 1）作实证缺口，再列三条挑战，贡献用项目符号对应 challenge 1/2/3。
- R003 Introduction 末用 `The remainder of this paper is structured as follows:` 指向 II–VI。
- R004 Related Work 按方法族分段（Transformer / multi-scale / time-frequency / pre-trained），每段末句收口不足。
- R005 Conclusion 先 `We propose` 收回方法，再用 `While ... To address this limitation, future research could explore`。

## Candidate phrases

- `To address this issue, we explicitly represent` (abstract)
- `To address these challenges, we propose` (introduction)
- `Overall, our main contributions are as follows:` (introduction)
- `The remainder of this paper is structured as follows:` (introduction)
- `In this section, we address two key questions:` (experiments)
- `To address this limitation, future research could explore` (conclusion)

## House style

自称是 `we propose` / `our method` / `this paper` / `STCNet`。未见 `Here we`。`we propose` 与 `In this paper` 不作为 anti_ai。引言路标用 `this paper`。结论开篇用 `We propose` 而非 `In this paper`。

## Quotes

- p.6750 abstract: Models based on Transformer variants have consistently demonstrated leading performance in long sequence time series forecasting.
- p.6750 abstract: However, in some complex application scenarios, Transformers tend to capture low-frequency information in the data while overlooking high-frequency information, which often contains rich non-stationary features.
- p.6750 abstract: To address this issue, we explicitly represent both low-frequency and high-frequency information and propose a model called STCNet, a data-driven scale-adaptive convolutional network that aims to extract diverse features and patterns from the data by learning features across different frequency bands in a balanced manner.
- p.6750 abstract: Experimental results on nine datasets demonstrate that STCNet outperforms the current state-of-the-art models in both effectiveness and efficiency.
- p.6750 introduction: LONG-SEQUENCE time-series forecasting (LSTF) is a critical area in data mining, which is widely applied in fields such as financial market prediction [1], [2], [3], weather forecasting [4], [5], [6], energy demand forecasting [7], [8], [9], traffic flow prediction [10], [11], [12], and medical diagnostics [13], [14], [15], among others [16], [17], [18].
- p.6751 introduction: In summary, existing methods face three main challenges:
- p.6751 introduction: To address these challenges, we propose STCNet, a data-driven, scale-adaptive time-frequency convolutional network for long-sequence time-series forecasting.
- p.6752 introduction: The remainder of this paper is structured as follows: Section II reviews existing methods for long time-series forecasting. Section III defines the problem to be solved and introduces preliminaries. Section IV provides a detailed description of the proposed architecture. Section V presents the experimental methods and results. Finally, Section VI summarizes our forecasting research, analyzes the limitations, and outlines key directions for future research.
- p.6753 method: To capture features in complex real-world time-series data, we propose a data-driven adaptive time-frequency convolutional network for LSTF, comprising a pre-training model and a prediction model, as shown in Fig. 2.
- p.6758 experiments: In this section, we address two key questions: (1) How effective is STCNet?
- p.6762 conclusion: We propose a data-driven scale-adaptive convolutional network (STCNet) for long-term time series forecasting.
- p.6762 conclusion: While STCNet demonstrates strong performance on non-stationary datasets by focusing on high-frequency components, its improvements on stationary datasets are relatively less pronounced.
- p.6762 conclusion: To address this limitation, future research could explore the integration of multi-resolution signal processing techniques—such as wavelet transforms or adaptive frequency decomposition—into the architecture.
