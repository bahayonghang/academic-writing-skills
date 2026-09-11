---
key: 2D6ENKZ8
title: "Joint training of a predictor network and a generative adversarial network for time series forecasting: A case study of bearing prognostics"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2022.117415"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Proposed HP-JT prognostics method` → `3. Case studies` → `4. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段物理/虚拟健康指标、model-based 与 data-driven RUL、LSTM/CNN、GAN 数据增强）。Introduction 末有编号贡献（`1.` / `2.`）+ 节序路标。Method 含 data preparation、offline training、online RUL、benchmark models。Experiments 标题为 `3. Case studies`（toy + XJTU-SY）。

## Openers

- abstract: `The lack of` — "The lack of bearing run-to-failure data has been one of the challenges in developing and practically implementing robust bearing prognostics models."
- introduction: `As one of` — "As one of the most common and critical components in rotating machines, the rolling element bearings play a crucial part in rotating machinery."
- method: `Three different stages` — "Three different stages of the proposed method for bearing elements failure prognostics are summarized in Fig. 1 (a)-(c), illustrating data preparation, offline training of HP-JT, and finally, online RUL prediction."
- experiments: `Two case studies` — "Two case studies are employed to demonstrate the effectiveness of the proposed method."
- conclusion: `In this paper` — "In this paper, we propose a novel HP-JT method for forecasting the bearing health condition and predicting the bearing remaining useful life."

## Gap transitions

- therefore (introduction): "Therefore, accurate prediction of bearing remaining useful life (RUL) improves productivity and reduces maintenance costs."
- however (introduction): "However, the model-based approaches require accurate estimation of the model parameters."
- although (introduction): "Although the data-driven approaches have shown promising results, they often face the following challenges:"
- besides (introduction): "Besides, data-driven approaches heavily rely on a large amount of training data to acquire degradation information."

## Hedge verbs

- proposes / causal / abstract: "This paper proposes a new Generative Adversarial Network (GAN) based prognostics method for RUL prediction."
- propose / causal / abstract, introduction: "We propose a novel joint training strategy"; "This paper proposes a GAN-based LSTM predictor"
- demonstrate / causal / abstract, experiments: "We demonstrate the utility and performance of the proposed method through two examples."
- show / associative / abstract: "The results from the case studies show that the proposed method can generate time series representing the real-data distribution."
- find / associative / conclusion: "We find that the GAN-LSTM architecture adds significant diversity to the training data"

## Cross-section linkers

- introduction → method: "The remainder of this paper is organized as follows. Section 2 introduces the proposed framework and the models used for comparison."
- method → experiments: "Section 3 includes two case studies to evaluate the proposed method."
- experiments → conclusion: 可靠性曲线段落后 `4. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remainder of this paper is organized as follows`
- R004 编号贡献：`Our main contributions are summarized as follows:`
- R009 自称：`This paper proposes` / `we propose` / `In this paper, we propose`

## Candidate phrases

- `This paper proposes a new Generative Adversarial Network (GAN) based prognostics method` (abstract)
- `We propose a novel joint training strategy` (abstract)
- `Our main contributions are summarized as follows:` (introduction)
- `The remainder of this paper is organized as follows` (introduction)
- `In this paper, we propose a novel HP-JT method` (conclusion)

## House style

自称 `This paper proposes` / `We propose` / `we demonstrate` / `In this paper, we propose`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The lack of bearing run-to-failure data has been one of the challenges in developing and practically implementing robust bearing prognostics models.
- abstract: This paper proposes a new Generative Adversarial Network (GAN) based prognostics method for RUL prediction.
- abstract: We propose a novel joint training strategy to integrate the training process of a bearing health predictor within the GAN architecture.
- abstract: Compared to HP, the proposed method decreases the bearing RUL prediction average error by 29.4% in a five-fold cross-validation study.
- introduction: As one of the most common and critical components in rotating machines, the rolling element bearings play a crucial part in rotating machinery.
- introduction: Although the data-driven approaches have shown promising results, they often face the following challenges:
- introduction: Our main contributions are summarized as follows:
- introduction: The remainder of this paper is organized as follows. Section 2 introduces the proposed framework and the models used for comparison.
- experiments: Two case studies are employed to demonstrate the effectiveness of the proposed method.
- conclusion: In this paper, we propose a novel HP-JT method for forecasting the bearing health condition and predicting the bearing remaining useful life.
- conclusion: For the XJTU dataset, the HP-JT method achieves a 29.4% reduction in RMSE and a 25% reduction in MAE compared to the HP method.
