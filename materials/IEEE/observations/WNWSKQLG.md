---
key: WNWSKQLG
title: "A Multi-Input Bi-LSTM Autoencoder Model with Wavelet Transform for Air Quality Prediction"
venue: "2024 International Conference on Multimedia Analysis and Pattern Recognition (MAPR)"
doi: "10.1109/MAPR63514.2024.10660818"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-6"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EVALUATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立相关工作节 `II. RELATED WORKS`（Classification approach / Regression approach）。`related_work=independent`。Introduction 末有贡献列表，无 `The rest of this paper is organized` 路标。Method 含 wavelet transform 与 Bi-LSTM Autoencoder。Experiments 标题为 `EVALUATION`。

## Openers

- abstract: `Air pollution is` — "Air pollution is a serious global issue that affects the health of millions of people worldwide." (p.1)
- introduction: `The rapid advancement` — "The rapid advancement of science and technology has accelerated global industrialization and modernization, fostering production and construction activities." (p.1)
- method: `In this section` — "In this section, we describe in detail the components of our proposed air quality prediction model, which include the wavelet transform and a Bi-LSTM Autoencoder." (p.2)
- experiments: `In this section` — "In this section, we provide a detailed analysis, beginning with a data description outlining the characteristics of the data set." (p.4)
- conclusion: `In this study` — "In this study, we developed a multi-input model that combines Bi-LSTM autoencoder architecture and wavelet transformation for the prediction of air quality index." (p.6)

## Gap transitions

- however (abstract): "However, existing approaches have limitations in capturing temporal dependencies and analyzing frequency domain relationships among pollutants." (p.1)
- however (introduction): "However, this progress has resulted in a significant increase in industrial emissions, thereby adversely impacting the environment." (p.1)
- however (introduction): "However, these models also have notable limitations." (p.1)
- to address (introduction): "To address the limitations of current research, an alternative approach that utilizes the long short-term memory (LSTM) model, a type of recurrent neural network, has emerged as a promising solution." (p.1)
- however (introduction): "However, the application of LSTM in air quality prediction remains constrained by its inability to analyze relationships within the frequency domain of pollutant factors." (p.1)
- however (method): "However, air quality datasets often contain air pollution components with complex relationships; thus, using Bi-LSTM alone would not guarantee an accurate prediction." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, method: "we propose a novel multi-input model"; "this study proposes a multi-input model"; "we propose using the discrete wavelet transform (DWT)"
- show / causal / abstract, experiments: "The evaluation results on the public air quality dataset show that our model achieves lowest mean absolute error (MAE) of 6.72"; "The results show that our model achieves the best MSE and MAE metrics."
- demonstrate / causal / introduction, conclusion: "The experimental results demonstrate that the proposed model outperforms competitor models."; "This result demonstrates the robustness and potential applicability of this model"
- introduce / causal / introduction: "We introduce a method for decomposing air quality data into frequency components"

## Cross-section linkers

- introduction → related work: 贡献三条后直接 `II. RELATED WORKS`："In this section, we survey some recent studies exploring various deep learning and machine learning techniques for predicting air quality." (p.2)
- related work → method: Regression 综述后接 `III. METHODOLOGY` (p.2)
- method → experiments: 预测式后接 `IV. EVALUATION` (p.4)
- experiments → conclusion: 对比表后接 `V. CONCLUSION` (p.6)

## Candidate rules

- R001 摘要用 `In this study, we propose a novel`，不用 `Here we`。
- R002 独立相关工作标题为 `RELATED WORKS`，再分 Classification / Regression。
- R003 贡献用 `The main contributions of this paper are summarized as follows:` + 项目符号。
- R004 Experiments 标题为 `EVALUATION`，节首 `In this section, we provide a detailed analysis`。
- R005 Conclusion 用 `In this study, we developed` 收回，再用 `Experimental results show that`。

## Candidate phrases

- `In this study, we propose a novel multi-input model based on` (abstract)
- `The main contributions of this paper are summarized as follows:` (introduction)
- `In this section, we describe in detail the components of our proposed` (method)
- `In this study, we developed a multi-input model that combines` (conclusion)

## House style

自称是 `In this study, we propose` / `this study proposes` / `We propose` / `our proposed model` / `this paper`。未见 `Here we`。`In this study, we propose` 进 phrase_bank，不进 anti_ai_patterns。贡献句用 `this paper`。

## Quotes

- p.1 abstract: Air pollution is a serious global issue that affects the health of millions of people worldwide.
- p.1 abstract: However, existing approaches have limitations in capturing temporal dependencies and analyzing frequency domain relationships among pollutants.
- p.1 abstract: In this study, we propose a novel multi-input model based on Bidirectional Long Short-Term Memory (Bi-LSTM) architecture, incorporating wavelet transformation for enhanced air quality prediction.
- p.1 abstract: The evaluation results on the public air quality dataset show that our model achieves lowest mean absolute error (MAE) of 6.72 compared to existing methods, highlighting its potential for real-world applications in public health protection.
- p.1 introduction: The rapid advancement of science and technology has accelerated global industrialization and modernization, fostering production and construction activities.
- p.1 introduction: However, this progress has resulted in a significant increase in industrial emissions, thereby adversely impacting the environment.
- p.1 introduction: However, these models also have notable limitations.
- p.1 introduction: To address the limitations of current research, an alternative approach that utilizes the long short-term memory (LSTM) model, a type of recurrent neural network, has emerged as a promising solution.
- p.1 introduction: However, the application of LSTM in air quality prediction remains constrained by its inability to analyze relationships within the frequency domain of pollutant factors.
- p.2 introduction: The main contributions of this paper are summarized as follows:
- p.2 related work: In this section, we survey some recent studies exploring various deep learning and machine learning techniques for predicting air quality.
- p.2 method: In this section, we describe in detail the components of our proposed air quality prediction model, which include the wavelet transform and a Bi-LSTM Autoencoder.
- p.2 method: Therefore, in this study, we propose using the discrete wavelet transform (DWT) for signal decomposition, leveraging its ability to represent the signal as a combination of mutually orthogonal wavelet basis functions.
- p.3 method: However, air quality datasets often contain air pollution components with complex relationships; thus, using Bi-LSTM alone would not guarantee an accurate prediction.
- p.4 experiments: In this section, we provide a detailed analysis, beginning with a data description outlining the characteristics of the data set.
- p.5 experiments: The results show that our model achieves the best MSE and MAE metrics.
- p.6 conclusion: In this study, we developed a multi-input model that combines Bi-LSTM autoencoder architecture and wavelet transformation for the prediction of air quality index.
- p.6 conclusion: Experimental results show that our model significantly outperforms traditional methods like SVR, XGBoost, and Bi-LSTM in terms of MSE and MAE.
- p.6 conclusion: This result demonstrates the robustness and potential applicability of this model in the domains of environmental monitoring and public health.
