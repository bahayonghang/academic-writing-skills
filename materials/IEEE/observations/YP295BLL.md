---
key: YP295BLL
title: "Explainable Artificial Intelligence for Fault Diagnosis of Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3240601"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. ADVERSARIAL AUTO-ENCODER FOR FAULT DETECTION` → `III. SHAP VALUES FOR FAULT DIAGNOSIS` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 CNN/DBN/LSTM/SAE/VAE/GAN/AAE、LIME/DeepLIFT/SHAP、AE/CNN explainer）。Introduction 末无 `The rest of this article is organized as follows`，方法铺垫后直接进入 II。II–III 为检测与诊断方法。Experiments 标题为 `CASE STUDIES`。

## Openers

- abstract: `Process monitoring is` — "Process monitoring is important for ensuring operational reliability and preventing occupational accidents." (p.4)
- introduction: `FAULT detection and` — "FAULT detection and diagnosis (FDD) is an important layer of safety in any industrial process[1]." (p.4；栏首掉字)
- method: `Our approach builds` — "Our approach builds on a previous study [17] on detecting the fault state using the AAE model and achieves a state-of-the-art detection performance." (p.5, II)
- experiments: `To demonstrate the` — "To demonstrate the effectiveness and feasibility of the proposed diagnosis method, a continuous stirred-tank reactor (CSTR) [28] and the TE [29] benchmark processes were considered." (p.7)
- conclusion: `In this article` — "In this article, a new fault diagnosis method for industrial processes was proposed based on the SHAP values that explained the black-box model." (p.10)

SHAP 节首句："SHAP is a representative XAI technique that can be applied to explain the prediction of a black-box model." (p.5, III)。不单列 `related_work` opener。

## Gap transitions

- however (abstract): "However, decisions generated from deep-neural-network-based models are difficult to interpret and cannot provide explanatory insight to users." (p.4)
- we address (abstract): "We address this issue by proposing a new fault diagnosis method using explainable artificial intelligence to break the traditional tradeoff between the accuracy and interpretability of deep learning model." (p.4)
- although (introduction): "Although the above deep learning models are promising for fault detection, their results cannot be easily explained or interpreted, which makes it difficult for human users to trust them." (p.4)
- to solve (introduction): "To solve this problem, there have been an increasing number of studies on ML concerned with addressing this issue, which is known as explainable artificial intelligence (XAI) [18], [19]." (p.4)
- however (introduction): "However, this approach is derived specifically from linear models, such as PCA and CVA." (p.5)
- despite (conclusion): "Despite the considerable results achieved in this study, the proposed method had limitations in estimating the causal effects of process variables." (p.10)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "We address this issue by proposing"; "a new fault diagnosis method ... was proposed"; "We proposed a framework"
- highlight / causal / abstract: "The results highlight that the proposed method achieves the exact fault diagnosis"
- demonstrate / causal / experiments, conclusion: "To demonstrate the effectiveness"; "The results demonstrated that both single fault and multiple faults can be successfully isolated"

## Cross-section linkers

- introduction → method: 引言收束后无节序路标，直接 `II. ADVERSARIAL AUTO-ENCODER FOR FAULT DETECTION` (p.5)
- method → experiments: 流程图段落后直接 `IV. CASE STUDIES` (p.7)
- experiments → conclusion: 故障地图段落后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 摘要用 `We address this issue by proposing`，不用 `Here we`。
- R002 Related Work 并入 Introduction；无独立 RELATED WORK。
- 本篇无 Introduction 节序路标，不计入 R003。
- 本篇无编号贡献列表，不计入 R004。贡献用一段方法铺垫收束。
- R005 结论 `Despite the considerable results` + `promising next steps involve`。

## Candidate phrases

- `We address this issue by proposing` (abstract)
- `Although the above deep learning models are promising for fault detection` (introduction)
- `In this article, a new fault diagnosis method ... was proposed` (conclusion)
- `Despite the considerable results achieved in this study` (conclusion)

## House style

自称 `We address` / `we combined` / `In this article` / `the proposed method`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.4 abstract: Process monitoring is important for ensuring operational reliability and preventing occupational accidents.
- p.4 abstract: However, decisions generated from deep-neural-network-based models are difficult to interpret and cannot provide explanatory insight to users.
- p.4 abstract: We address this issue by proposing a new fault diagnosis method using explainable artificial intelligence to break the traditional tradeoff between the accuracy and interpretability of deep learning model.
- p.4 abstract: The results highlight that the proposed method achieves the exact fault diagnosis for single and multiple faults and, also, distinguishes the global pattern of various fault types.
- p.4 introduction: FAULT detection and diagnosis (FDD) is an important layer of safety in any industrial process[1].
- p.4 introduction: Although the above deep learning models are promising for fault detection, their results cannot be easily explained or interpreted, which makes it difficult for human users to trust them.
- p.5 introduction: In this study, we combined a model-agnostic explainer with an unsupervised fault detection model to diagnose which variables contribute to the faulty state of the chemical process.
- p.5 method: Our approach builds on a previous study [17] on detecting the fault state using the AAE model and achieves a state-of-the-art detection performance.
- p.5 method: SHAP is a representative XAI technique that can be applied to explain the prediction of a black-box model.
- p.7 experiments: To demonstrate the effectiveness and feasibility of the proposed diagnosis method, a continuous stirred-tank reactor (CSTR) [28] and the TE [29] benchmark processes were considered.
- p.10 conclusion: In this article, a new fault diagnosis method for industrial processes was proposed based on the SHAP values that explained the black-box model.
- p.10 conclusion: Despite the considerable results achieved in this study, the proposed method had limitations in estimating the causal effects of process variables.
- p.10 conclusion: Accordingly, promising next steps involve developing an XAI-based fault propagation method that can examine causal inference between the fault status and the physical behavior.
