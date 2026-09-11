---
key: KK4KH32A
title: "Adaptive Graph Convolution Neural Differential Equation for Spatio-Temporal Time Series Prediction"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2024.3383895"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,8-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. ADAPTIVE GRAPH CONVOLUTION NEURAL DIFFERENTIAL EQUATION` → `IV` experiments（仿真/对比）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 为 AGCNDE。Experiments 在 IV，含消融、图结构可视化与多步预测。

## Openers

- abstract: `Multivariate time series` — "Multivariate time series prediction has aroused widely research interests during decades." (p.3193)
- introduction: `THE real systems` — "THE real systems in various fields such as sociology, transportation, atmospheric science can be regarded as complex nonlinear dynamic systems composed of interactions between multivariate agents." (p.3193)
- related_work: `In this section,` — "In this section, we use two subsections to separately explain how the existing work model the temporal dynamic evolution and spatial topology for multivariate time series." (p.3194, II)
- method: `In this section,` — "In this section, we first introduce the motivation of the proposed model and the prediction process of AGCNDE, then introduce the details of each module separately, and finally introduce the loss function and the complexity analysis." (p.3195, III)
- experiments: `In this subsection,` — "In this subsection, we first introduce the ablation experiment." (p.3200, IV.C)
- conclusion: `In this paper,` — "In this paper, we propose an efficient spatio-temporal time series modelling method for feature interaction discovery and time series prediction." (p.3203)

## Gap transitions

- however (abstract): "However, the spatial heterogeneity and temporal evolution characteristics bring much challenges for high-dimensional time series prediction." (p.3193)
- however (introduction): "However, most of the work generally extracts spatio-temporal features by designing different modules, such as utilizing graph neural network for spatial correlation and using RNN or temporal convolution module for temporal dependence." (p.3193)
- nevertheless (introduction): "Nevertheless, there are always interactions between the temporal and spatial characteristics of many real systems [11]." (p.3193)
- therefore (introduction): "Therefore, how to establish the mechanism-driven model with certain interpretability has gradually become a research hotspot." (p.3194)
- however (related_work): "However, due to the lack of interpretability, the extracted features often cannot truly represent the temporal evolution law of dynamic systems." (p.3194)
- however (experiments): "However, due to the lack of relevant design components of causal analysis, our method cannot learn the causal relationship between the underlying time series." (p.3201)

## Hedge verbs

- introduce / causal / abstract: "a novel adaptive graph convolution module is introduced"
- propose / causal / abstract, introduction, conclusion: "a Koopman-based neural differential equation is proposed"; "We propose a joint framework"; "we propose an efficient spatio-temporal time series modelling method"
- show / causal / abstract, introduction: "Simulation results show the effectiveness"; "The experimental result shows that the graph structure we have learned"
- could / speculative / abstract: "The proposed model could explicitly discover the spatial correlation"
- may / speculative / introduction: "variations of KPI will probably reflect" 未见；introduction 用 "will lead to the lack of interpretability"

## Cross-section linkers

- introduction → related_work: "The rest of the paper is organized as follows. In Section II, we detail the methods related with this research and some specific information about our model. In Section III, we introduce each module in the model. In Section IV, we compare the experimental results with the previous literature and provide a comprehensive discussion of our proposal and the results achieved. In Section V, we present conclusions and final comments." (p.3194)
- related_work → method: "In this paper, an adaptive graph convolution neural differential equation (AGCNDE) based on nonlinear spatio-temporal state transition is proposed." 随后 `III. ADAPTIVE GRAPH CONVOLUTION NEURAL DIFFERENTIAL EQUATION` (p.3195)
- experiments → conclusion: "This confirms the superiority of the AGCNDE and its usefulness from the perspective of modeling nonlinear systems rather than purely fitting data." 随后 `V. CONCLUSION` (p.3203)

## Candidate rules

- R001 Abstract 先 `However` 点空间异质与时间演化，再 `In this paper` 给模块。
- R002 贡献用 `The main contributions in this paper are as follows` + 项目符号。
- R003 Introduction 末用 `The rest of the paper is organized as follows` 指向 II–V。
- R004 Related Work 末用 `In this paper, an ... is proposed` 接到 Method。
- R005 Conclusion 用 `In this paper, we propose` 收回方法，再用 `Simulation results illustrate` 收实验。

## Candidate phrases

- `In this paper, a novel adaptive graph convolution module is introduced` (abstract)
- `The main contributions in this paper are as follows.` (introduction)
- `The rest of the paper is organized as follows.` (introduction)
- `To solve the above challenge,` (introduction)
- `In this paper, we propose an efficient` (conclusion)

## House style

自称是 `In this paper` / `we propose` / `our method` / `the proposed model`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。未见 `this article`。

## Quotes

- p.3193 abstract: Multivariate time series prediction has aroused widely research interests during decades.
- p.3193 abstract: However, the spatial heterogeneity and temporal evolution characteristics bring much challenges for high-dimensional time series prediction.
- p.3193 abstract: In this paper, a novel adaptive graph convolution module is introduced to automatically learn the spatial correlation of multivariate time series and a Koopman-based neural differential equation is proposed to simulate the nonlinear system state evolution.
- p.3193 abstract: The proposed model could explicitly discover the spatial correlation by adaptive graph convolution and reveal the temporal dynamics by neural differential equation, which make the modeling more interpretable.
- p.3193 abstract: Simulation results show the effectiveness on spatio-temporal dynamic discovery and prediction performance.
- p.3193 introduction: THE real systems in various fields such as sociology, transportation, atmospheric science can be regarded as complex nonlinear dynamic systems composed of interactions between multivariate agents.
- p.3193 introduction: However, most of the work generally extracts spatio-temporal features by designing different modules, such as utilizing graph neural network for spatial correlation and using RNN or temporal convolution module for temporal dependence.
- p.3193 introduction: Nevertheless, there are always interactions between the temporal and spatial characteristics of many real systems [11].
- p.3194 introduction: Therefore, how to establish the mechanism-driven model with certain interpretability has gradually become a research hotspot.
- p.3194 introduction: The main contributions in this paper are as follows.
- p.3194 introduction: We propose a joint framework for modeling multivariate time series and learning graph structure, which combines adaptive graph convolution neural network and state transition theory to model time series from the perspective of modeling complex nonlinear systems.
- p.3194 introduction: The rest of the paper is organized as follows. In Section II, we detail the methods related with this research and some specific information about our model. In Section III, we introduce each module in the model. In Section IV, we compare the experimental results with the previous literature and provide a comprehensive discussion of our proposal and the results achieved. In Section V, we present conclusions and final comments.
- p.3194 related_work: In this section, we use two subsections to separately explain how the existing work model the temporal dynamic evolution and spatial topology for multivariate time series.
- p.3195 method: In this section, we first introduce the motivation of the proposed model and the prediction process of AGCNDE, then introduce the details of each module separately, and finally introduce the loss function and the complexity analysis.
- p.3195 method: In this paper, an adaptive graph convolution neural differential equation (AGCNDE) based on nonlinear spatio-temporal state transition is proposed.
- p.3200 experiments: In this subsection, we first introduce the ablation experiment.
- p.3201 experiments: However, due to the lack of relevant design components of causal analysis, our method cannot learn the causal relationship between the underlying time series.
- p.3203 experiments: All in all, AGCNDE has achieved better results on the four data sets.
- p.3203 conclusion: In this paper, we propose an efficient spatio-temporal time series modelling method for feature interaction discovery and time series prediction.
- p.3203 conclusion: Simulation results illustrate that the proposed framework could be regarded as an efficient method for nonlinear dynamical system revealing and multivariate time series prediction.
