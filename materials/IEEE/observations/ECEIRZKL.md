---
key: ECEIRZKL
title: "Time-Series Forecasting in Industrial Environments: A Performance Study and a Novel Late Fusion Framework"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2025.3526362"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10,14-17"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. LITERATURE REVIEW` → `III. METHODOLOGY` → `IV. EXPERIMENTS AND RESULTS` → `V. DISCUSSION` → `VI. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（标题为 `LITERATURE REVIEW`）。`related_work=independent`。Introduction 末有节序路标，指向 taxonomy / methodology / results / discussion。Method 在正文中段。Experiments 标题为 `EXPERIMENTS AND RESULTS`。其后有独立 `DISCUSSION`。

## Openers

- abstract: `In manufacturing environments` — "In manufacturing environments, monitoring of the Overall Equipment Effectiveness (OEE) via soft sensors plays a pivotal role in enhancing productivity and efficiently planning maintenance schedules." (p.1)
- introduction: `IN the era` — "IN the era of Industry 4.0, predictive analytics and monitoring in manufacturing settings have garnered significant attention for their crucial role in process optimization." (p.1；栏首掉字)
- related_work: `This subsection provides` — "This subsection provides a comprehensive taxonomy of deep learning (DL) methods, categorized according to their architectural foundations." (p.2, II.A)
- method: `Time-series forecasting involves` — "Time-series forecasting involves predicting future values based on previously observed data points." (p.5, III.A)
- experiments: `In this section` — "In this section, we present the evaluation dataset of the antenna assembly line and the applied preprocessing, the selected evaluation metrics and the experimental setup." (p.8, IV)
- conclusion: `In this study` — "In this study, we explored the application of advanced deep learning architectures for time series forecasting of Overall Equipment Effectiveness (OEE) in a real-world antenna assembly line." (p.15)

## Gap transitions

- however (abstract): "However, the accurate forecasting of the OEE presents considerable challenges due to the complexity of manufacturing data and equipment interdependence across stages." (p.1)
- however (introduction): "However, these methods often struggle with capturing non-linear patterns, long-range dependencies, and the intricate dynamics of modern manufacturing environments." (p.2)
- despite (literature): "Despite significant advancements, the current state-of-the-art in time series forecasting for industrial applications still faces several key limitations." (p.5)
- to address (literature): "To address these challenges, this study introduces a simple, yet efficient, forecasting method." (p.5)
- however (discussion): "However, some limitations were observed, particularly in long-term forecasting scenarios, where in some cases, simpler fusion techniques outperformed the proposed method." (p.15)

## Hedge verbs

- present / causal / abstract, introduction: "In this study, we present a taxonomy of DL forecasting architectures"; "we will present the model architecture taxonomy"
- propose / causal / abstract, introduction: "a lightweight late fusion Linear architecture is proposed"; "Propose a lightweight late-fusion forecasting method"
- show / causal / abstract, experiments: "The experimental results show that our proposed model consistently matches or outperforms"; "These results confirm the effectiveness of our proposed model"
- demonstrate / causal / experiments, discussion: "demonstrating the generalization capability of the proposed method"; "demonstrated our proposed method's robust performance"
- suggest / speculative / experiments, discussion: "These factors suggest that very complex deep learning methods"; "This suggests a need for refining the EWA mechanism"

## Cross-section linkers

- introduction → literature: "In the following sections, we will present the model architecture taxonomy and related work, outline the methodology proposed in this study, present the results of our model evaluations, and discuss the implications of our findings for the field of time series forecasting in manufacturing." (p.2)
- literature → method: "To address these challenges, this study introduces a simple, yet efficient, forecasting method." 随后 `III. METHODOLOGY` (p.5)
- method → experiments: 方法段落后直接 `IV. EXPERIMENTS AND RESULTS` (p.8)
- experiments → discussion → conclusion: 消融后 `V. DISCUSSION`，再 `VI. CONCLUSIONS` (p.14–15)

## Candidate rules

- R001 abstract 用 `In this study, we present` 做分类综述，再用 `is proposed` 引出本方法。
- R002 独立 Related Work 标题为 `LITERATURE REVIEW`，按 MLP / RNN / Transformer / TCN 分类。
- R003 Introduction 末用 `In the following sections, we will present` 指向 taxonomy、methodology、results、discussion。
- R004 贡献用 `The main contributions of this study are as follows` + 编号列表。
- R005 结果后设独立 `DISCUSSION`，再用 `VI. CONCLUSIONS` 收回。

## Candidate phrases

- `In this study, we present a taxonomy of` (abstract)
- `This paper introduces a lightweight MLP-based model that` (introduction)
- `The main contributions of this study are as follows:` (introduction)
- `To address these challenges, this study introduces a simple, yet efficient, forecasting method.` (literature)
- `In this study, we explored the application of` (conclusion)

## House style

自称是 `this study` / `This paper` / `our proposed method` / `we present` / `we propose`。未见 `Here we`。`In this study` 与 `This paper introduces` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In manufacturing environments, monitoring of the Overall Equipment Effectiveness (OEE) via soft sensors plays a pivotal role in enhancing productivity and efficiently planning maintenance schedules.
- p.1 abstract: However, the accurate forecasting of the OEE presents considerable challenges due to the complexity of manufacturing data and equipment interdependence across stages.
- p.1 abstract: In this study, we present a taxonomy of DL forecasting architectures, consisting of Multi-Layer Perceptrons (MLPs), Recurrent models, Transformer-based models, and Temporal Convolutional Networks (TCNs), and we perform a comparative study of the state-of-the-art approaches.
- p.1 abstract: The experimental results show that our proposed model consistently matches or outperforms the state-of-the-art models in terms of forecasting efficacy for all forecast horizons, whilst requiring a fraction of the computational resources.
- p.1 introduction: IN the era of Industry 4.0, predictive analytics and monitoring in manufacturing settings have garnered significant attention for their crucial role in process optimization.
- p.2 introduction: However, these methods often struggle with capturing non-linear patterns, long-range dependencies, and the intricate dynamics of modern manufacturing environments.
- p.2 introduction: This paper introduces a lightweight MLP-based model that integrates multiple feature extraction techniques, including i) PatchTST's patching mechanism for efficient short-range feature extraction, a Moving Average (MA) seasonal decomposition scheme, and iii) a Discrete Fourier Transform (DFT) decomposition scheme for mid-to-long-range forecast performance.
- p.2 introduction: The main contributions of this study are as follows:
- p.2 introduction: In the following sections, we will present the model architecture taxonomy and related work, outline the methodology proposed in this study, present the results of our model evaluations, and discuss the implications of our findings for the field of time series forecasting in manufacturing.
- p.5 literature: Despite significant advancements, the current state-of-the-art in time series forecasting for industrial applications still faces several key limitations.
- p.5 literature: To address these challenges, this study introduces a simple, yet efficient, forecasting method.
- p.5 method: Time-series forecasting involves predicting future values based on previously observed data points.
- p.5 method: Our proposed model architecture is a lightweight MLP-based framework designed to address both short-term and long-term forecasting challenges in time-series data.
- p.8 experiments: In this section, we present the evaluation dataset of the antenna assembly line and the applied preprocessing, the selected evaluation metrics and the experimental setup.
- p.10 experiments: Finally, PDFLinearEWA achieves the best results in short- and mid-term forecast horizons (8H, 24H, 48H), while also achieving comparable results to the best models in long-term forecast horizons (72H).
- p.14 discussion: The findings of this study highlight the efficacy of the proposed method in addressing the challenges of predictive maintenance and process optimization in manufacturing, which are pivotal procedures for ZDM.
- p.15 discussion: However, some limitations were observed, particularly in long-term forecasting scenarios, where in some cases, simpler fusion techniques outperformed the proposed method.
- p.15 conclusion: In this study, we explored the application of advanced deep learning architectures for time series forecasting of Overall Equipment Effectiveness (OEE) in a real-world antenna assembly line.
