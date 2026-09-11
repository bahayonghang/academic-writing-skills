---
key: FM3IATJV
title: "Health Status Prediction for Nonstationary Systems Based on Feature Decoupling of Time Series"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3550624"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. METHODOLOGY` → `III. HIL RESULTS` → `IV. DISCUSSION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 CNN/RNN/TCN/DBN/PatchTST/MLP）。Introduction 末有编号贡献与节序路标。Method 为 Section II。Experiments 标题为 `HIL RESULTS`。另有独立 Discussion（Section IV）。

## Openers

- abstract: `This article proposes` — "This article proposes a nonstationary time series forecasting model based on feature decoupling (NTFFD), which effectively enhances the efficiency of health status assessment and prediction for nonstationary systems in the field of instrumentation and measurement (I&M), while reducing resource consumption in practical industrial applications." (p.1)
- introduction: `THE traction drive` — "THE traction drive control system (TDCS) is pivotal to the operation of ultrahigh-speed maglev trains, acting as the “brain” that optimizes performance metrics like speed and traction load, ensuring safe and efficient train dynamics." (p.1；栏首掉字)
- method: `Assuming that the` — "Assuming that the dynamics of the input time series can be represented as x_{t+1} = F(x_t), where x_t denotes the state of the system and F is the vector field describing the dynamics." (p.2, II)
- experiments: `In this section` — "In this section, hardware-in-the-loop (HIL) testing is conducted to verify the predictive performance of the proposed method." (p.6, III)
- conclusion: `This article introduces` — "This article introduces the NTFFD model, a pioneering nonstationary time series prediction method that utilizes feature decoupling for enhanced system health status prediction." (p.9)

## Gap transitions

- despite (abstract): "Current online prediction methods, despite their advancements, often necessitate complex network architectures and update mechanisms, which hinders efficiency and practical application." (p.1)
- however (introduction): "However, despite the superior performance of intricate deep learning models in certain contexts, they operate under the assumption of static data distributions throughout training and inference [24]." (p.2)
- therefore (introduction): "Therefore, our objective is to develop predictors with simple linear structures capable of dynamically updating the prediction model through online training to adapt to the evolving time series." (p.2)
- moreover (introduction): "Moreover, deep learning models offer a “black box” approach to feature analysis in time series." (p.2)
- consequently (introduction): "Consequently, we disentangle the nonlinear system into a gradual-variant dynamical system and an abrupt-variant dynamical system for simultaneous analysis." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "This article proposes"; "we propose NTFFD"
- introduce / causal / conclusion: "This article introduces the NTFFD model"
- demonstrate / causal / abstract, conclusion: "demonstrating its potential"; "Our empirical evaluation demonstrates that NTFFD outperforms"
- indicate / causal / experiments: "The results indicate that the NTFFD method demonstrates superior competitiveness"
- develop / causal / introduction: "we develop a dynamic weight combination generation method"

## Cross-section linkers

- introduction → method: "The remaining sections of this article are organized as follows. In Section II, we propose a nonstationary time series prediction model based on feature decoupling for system health status prediction, and introduce each module of the model in detail. Section III presents the verification results of HIL, and analyzes the generality and efficiency of the prediction model. Section IV studies the interpretability and stability of the model, and focuses on discussing how to apply the model to the health status prediction of TDCS. Finally, Section V summarizes the article." (p.2)
- method → experiments: 阈值滤波段落后接 `III. HIL RESULTS` (p.6)
- experiments → discussion: 效率段落后接 Section IV Discussion（可解释性/稳定性/TDCS 框架）
- discussion → conclusion: TDCS 框架段落后接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 开篇 `This article proposes` + 方法缩写。
- R002 Introduction 无独立 Related Work；贡献用 `The contributions of this study can be summarized as follows`。
- R003 Introduction 末用 `The remaining sections of this article are organized as follows`。
- R004 Experiments 标题为 `HIL RESULTS`，开篇 `In this section, hardware-in-the-loop (HIL) testing is conducted`。
- R005 Conclusion 用 `This article introduces`，再写 `Our empirical evaluation demonstrates`。

## Candidate phrases

- `This article proposes` (abstract)
- `In this study, we propose` (introduction)
- `The contributions of this study can be summarized as follows.` (introduction)
- `The remaining sections of this article are organized as follows.` (introduction)
- `This article introduces the NTFFD model` (conclusion)

## House style

自称是 `This article proposes` / `This article introduces` / `we propose` / `our method` / `this study`。未见 `Here we`。`This article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: This article proposes a nonstationary time series forecasting model based on feature decoupling (NTFFD), which effectively enhances the efficiency of health status assessment and prediction for nonstationary systems in the field of instrumentation and measurement (I&M), while reducing resource consumption in practical industrial applications.
- p.1 abstract: Current online prediction methods, despite their advancements, often necessitate complex network architectures and update mechanisms, which hinders efficiency and practical application.
- p.1 abstract: Consequently, significant improvements are achieved in both training speed (a 3270% increase) and memory efficiency (a 91% reduction).
- p.1 introduction: THE traction drive control system (TDCS) is pivotal to the operation of ultrahigh-speed maglev trains, acting as the “brain” that optimizes performance metrics like speed and traction load, ensuring safe and efficient train dynamics.
- p.2 introduction: However, despite the superior performance of intricate deep learning models in certain contexts, they operate under the assumption of static data distributions throughout training and inference [24].
- p.2 introduction: Therefore, our objective is to develop predictors with simple linear structures capable of dynamically updating the prediction model through online training to adapt to the evolving time series.
- p.2 introduction: In this study, we propose NTFFD, an innovative nonstationary time series forecasting model for predicting the health status of systems.
- p.2 introduction: The contributions of this study can be summarized as follows.
- p.2 introduction: The remaining sections of this article are organized as follows. In Section II, we propose a nonstationary time series prediction model based on feature decoupling for system health status prediction, and introduce each module of the model in detail.
- p.2 method: Assuming that the dynamics of the input time series can be represented as x_{t+1} = F(x_t), where x_t denotes the state of the system and F is the vector field describing the dynamics.
- p.6 experiments: In this section, hardware-in-the-loop (HIL) testing is conducted to verify the predictive performance of the proposed method.
- p.6 experiments: The results indicate that the NTFFD method demonstrates superior competitiveness in predictive performance, achieving SOTA RMSE for prediction lengths of 48, 96, 144, 192.
- p.9 conclusion: This article introduces the NTFFD model, a pioneering nonstationary time series prediction method that utilizes feature decoupling for enhanced system health status prediction.
- p.9 conclusion: Our empirical evaluation demonstrates that NTFFD outperforms current models in prediction accuracy, model generality, and efficiency across various datasets.
- p.9 conclusion: The NTFFD model is poised to contribute significantly to the fields of predictive maintenance and system health management, with the potential to improve safety and reliability in high-speed rail and other critical industries.
