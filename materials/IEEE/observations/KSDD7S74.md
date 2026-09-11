---
key: KSDD7S74
title: "Automatic Deep Extraction of Robust Dynamic Features for Industrial Big Data Modeling and Soft Sensor Application"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2019.2945411"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. AUTOMATIC DYNAMIC FEATURE EXTRACTOR` → `III. ROBUST DYNAMIC FEATURE WITH ATTENTION SMOOTHING` → `IV. TRANFER ROBUST DYNAMIC FEATURES TO ENSEMBLE TREES` → `V. CASE STUDY` → `VI. CONCLUSIONS AND FUTURE WORK`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 AR / LDS / HMM / RNN-LSTM）。Introduction 末有 `The rest of this paper is organized as follows`。Method 在 II–IV。Experiments 标题为 `CASE STUDY`。Conclusion 与 Future Work 并为一节。早录 PDF 无期刊页码，页码按 PDF 页计。

## Openers

- abstract: `Dynamic is one` — "Dynamic is one of the main bottlenecks in the industrial soft sensor application, due to the difficulties in representing and extracting dynamic data features." (p.1)
- introduction: `IN modern industrial` — "IN modern industrial processes, many key process variables and quality-related variables need to be measured accurately, which can improve the production process [1]." (p.1)
- method: `The Encoder-Decoder sequence` — "The Encoder-Decoder sequence to sequence model has been introduced for the first time in 2014 by Google [19]." (p.2, II.A)
- experiments: `The debutanizer distillation` — "The debutanizer distillation process is a conventional part of the desulfuring and naphtha splitter plant." (p.6, V.A)
- conclusion: `In the present` — "In the present paper, in order to make full use of RNN sequence representation and strong fitting ability of ensemble trees, an ensemble tree soft sensing model was proposed, with an introduction of an automatic dynamic feature extractor." (p.8)

## Gap transitions

- however (introduction): "However, due to the limitation of actual measuring instruments, many pivotal variables can hardly be obtained directly, such as the quality of product, the content of process gas and some melt indices [2]." (p.1)
- however (introduction): "To date, however, most dynamic models are linear, which means their nonlinear representation abilities of process data are weaker than some existing non-linear models such as neural network (NN) [10], support vector machine (SVM) [11] and so on." (p.1)
- however (introduction): "However, all of above applications designed models as an end-to-end mode, and only used RNN to represent the sequence data, but did not analyze the dynamic features of data in RNN." (p.1)
- in this paper (introduction): "In this paper, in order to utilize the ability of representing sequence of RNN and the advantage of strong learning models, an ensemble tree soft sensing model is proposed." (p.2)
- meanwhile (abstract): "Meanwhile, an end-to-end deep network owns the ability to characterize sequence data information, but its fitting ability requires improvements in practical applications." (p.1)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "an ensemble tree model with transferable and robust dynamic features extracted by a newly developed automatic dynamic feature extractor is proposed"; "an ensemble tree soft sensing model is proposed"; "an ensemble tree soft sensing model was proposed"
- show / causal / abstract: "application results on a debutanizer distillation process show that the incorporation of robust dynamic features can significantly improve the soft sensing performance"
- infer / causal / experiments, conclusion: "From the RMSE results, it can be inferred that the dynamic features can significantly improve the prediction accuracy"; "it can be inferred that the dynamic features are useful for regression modeling"

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows. The automatic dynamic feature extractor is described in section II. The smoothing approach for the extracted dynamic vector by attention is presented in section III. Transferring of the robust dynamic features to ensemble tree is developed in section IV. A detailed case study is provided in section V for performance evaluation, followed by the conclusion and future work." (p.2)
- method → experiments: Algorithm I 后 `V. CASE STUDY` (p.6)
- experiments → conclusion: 云平台实现后 `VI. CONCLUSIONS AND FUTURE WORK` (p.8)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–V。
- R004 贡献用 `The main contribution of the paper can be summarized as follows.` + Firstly/Then/Finally。
- R005 Conclusion 与 Future Work 并为一节：`VI. CONCLUSIONS AND FUTURE WORK`。
- R009 结论 `In the present paper, ... was proposed`。

## Candidate phrases

- `In this paper, an ensemble tree model ... is proposed` (abstract)
- `In this paper, in order to utilize` (introduction)
- `The main contribution of the paper can be summarized as follows.` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `In future work, the dynamic feature extractor can be pre-trained` (conclusion)

## House style

自称是 `In this paper` / `In the present paper` / `the paper` / `is proposed`。`In this paper` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。未见 `this article`。

## Quotes

- p.1 abstract: Dynamic is one of the main bottlenecks in the industrial soft sensor application, due to the difficulties in representing and extracting dynamic data features.
- p.1 abstract: Meanwhile, an end-to-end deep network owns the ability to characterize sequence data information, but its fitting ability requires improvements in practical applications.
- p.1 abstract: In this paper, an ensemble tree model with transferable and robust dynamic features extracted by a newly developed automatic dynamic feature extractor is proposed.
- p.1 abstract: Finally, application results on a debutanizer distillation process show that the incorporation of robust dynamic features can significantly improve the soft sensing performance, compared to traditional methods.
- p.1 introduction: IN modern industrial processes, many key process variables and quality-related variables need to be measured accurately, which can improve the production process [1].
- p.1 introduction: However, due to the limitation of actual measuring instruments, many pivotal variables can hardly be obtained directly, such as the quality of product, the content of process gas and some melt indices [2].
- p.1 introduction: To date, however, most dynamic models are linear, which means their nonlinear representation abilities of process data are weaker than some existing non-linear models such as neural network (NN) [10], support vector machine (SVM) [11] and so on.
- p.2 introduction: In this paper, in order to utilize the ability of representing sequence of RNN and the advantage of strong learning models, an ensemble tree soft sensing model is proposed.
- p.2 introduction: The main contribution of the paper can be summarized as follows.
- p.2 introduction: The rest of this paper is organized as follows. The automatic dynamic feature extractor is described in section II. The smoothing approach for the extracted dynamic vector by attention is presented in section III. Transferring of the robust dynamic features to ensemble tree is developed in section IV. A detailed case study is provided in section V for performance evaluation, followed by the conclusion and future work.
- p.2 method: The Encoder-Decoder sequence to sequence model has been introduced for the first time in 2014 by Google [19].
- p.6 experiments: The debutanizer distillation process is a conventional part of the desulfuring and naphtha splitter plant.
- p.7 experiments: From the RMSE results, it can be inferred that the dynamic features can significantly improve the prediction accuracy.
- p.8 conclusion: In the present paper, in order to make full use of RNN sequence representation and strong fitting ability of ensemble trees, an ensemble tree soft sensing model was proposed, with an introduction of an automatic dynamic feature extractor.
- p.8 conclusion: With the introduction of the robust dynamic features, the performance of the XGBoost based on method has been significantly improved, compared to other adaptive and deep soft sensor models.
- p.9 conclusion: In future work, the dynamic feature extractor can be pre-trained for some common industrial scenes, such as the debutanizer distillation process, the CO2 absorption process, hot or cold rolling process and so on.
