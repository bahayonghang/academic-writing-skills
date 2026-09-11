---
key: 75CLNG4H
title: "Multiscale Dilated Window Attention Transformer for Grade Prediction of Zinc Concentrate"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3633377"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. FROTH FLOTATION PROCESS OF LEAD-ZINC ORE` → `III. PROPOSAL OF THE MSDWT FOR FROTH FLOTATION` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 LSTM / encoder–decoder / Transformer 品位预测）。`II.` 是工艺描述，不是文献综述。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `EXPERIMENTS`。

## Openers

- abstract: `Accurate grade prediction` — "Accurate grade prediction of zinc concentrate is crucial for optimizing the flotation mining process." (p.1)
- introduction: `FROTH flotation is` — "FROTH flotation is a widely used and effective method for separating valuable minerals in mineral processing [1]." (p.1；栏首掉字)
- method: `To predict the` — "To predict the grade of zinc concentrate more accurately, it is essential to extract the visual features of the froth surface from videos captured at the top of Cleaner III." (p.2, III.A)
- experiments: `The zinc concentrate` — "The zinc concentrate flotation froth data used in this study were supplied by a lead-zinc flotation plant in Shaoguan, Guangdong Province." (p.7, IV.A)
- conclusion: `The MSDWT model` — "The MSDWT model presented in this article combines an MSDW attention mechanism with hybrid encoding, offering a novel approach to addressing the time-varying nature of flotation froth features." (p.10)

## Gap transitions

- to address (abstract): "To address these challenges, this article proposes a multiscale dilated window attention transformer (MSDWT) model." (p.1)
- despite (introduction): "Despite significant progress in flotation grade prediction, there is still room for improvement as follows." (p.1)
- to address (introduction): "To address these issues, this article proposes the multiscale dilated window attention transformer (MSDWT) model for froth flotation." (p.2)
- therefore (method): "Therefore, it is necessary to identify the video feature vector closest to the grade sampling time, which will serve as the corresponding feature vector x′i for that grade value." (p.3)
- therefore (conclusion): "Therefore, the development of delay-robust alignment methods, such as estimating the delay as a learnable parameter or employing dynamic time warping algorithms, is a crucial direction for future work." (p.10)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a multiscale dilated window attention transformer (MSDWT) model"; "this article proposes the multiscale dilated window attention transformer (MSDWT) model for froth flotation"
- show / causal / abstract, experiments: "Experimental results show that, compared to existing typical models"; "These metrics show that the absolute deviation"
- introduce / causal / method: "This article introduces the MSDWT to address three main challenges in flotation grade prediction"
- demonstrate / causal / experiments, conclusion: "This demonstrates that the MSDWT model is more accurate and effective for grade monitoring tasks"; "Experimental results validate the model's superiority in grade prediction, demonstrating a substantial improvement in accuracy over the existing methods"

## Cross-section linkers

- introduction → later sections: "The rest of the article is organized as follows. Section II discusses the froth flotation process for lead-zinc ore. Section III presents the input-output structure and model architecture proposed in this study. Section IV compares the proposed model with others from the literature. Finally, Section V presents the conclusions." (p.2)
- process → method: 工艺段落后直接 `III. PROPOSAL OF THE MSDWT FOR FROTH FLOTATION` (p.2)
- method → experiments: DAL 段落后直接 `IV. EXPERIMENTS` (p.7)
- experiments → conclusion: 部署段落后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 缺口用 `Traditional methods face challenges`，贡献用 `this article proposes` + 模型缩写。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段，挑战用编号列表。
- R003 Introduction 末用 `The rest of the article is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions of this article are as follows` + 编号列表。
- R005 Conclusion 先对比已有方法，再用 `Therefore` + `future work` 指向后续。

## Candidate phrases

- `To address these challenges, this article proposes` (abstract)
- `To address these issues, this article proposes` (introduction)
- `The contributions of this article are as follows.` (introduction)
- `The rest of the article is organized as follows.` (introduction)
- `Among all the metrics, the MSDWT model proposed in this study outperforms all the others.` (experiments)
- `Therefore, the development of delay-robust alignment methods` (conclusion)

## House style

自称是 `this article proposes` / `this study` / `we plot` / `the proposed zinc concentrate grade prediction model`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。路标用 `the article`。

## Quotes

- p.1 abstract: Accurate grade prediction of zinc concentrate is crucial for optimizing the flotation mining process.
- p.1 abstract: Traditional methods face challenges, including inconsistencies between froth feature capture and X-ray fluorescence (XRF) analysis sampling times, nonstationary sequences, and asymmetric error costs, which hinder practical applications.
- p.1 abstract: To address these challenges, this article proposes a multiscale dilated window attention transformer (MSDWT) model.
- p.1 abstract: Experimental results show that, compared to existing typical models such as transformer, Enc-Dec+RNN, STS-D+LSTM, MSFT, and NST, the RMSE was reduced by 22.6%, 12.4%, 11.0%, 9.9%, and 9.3%, respectively.
- p.1 introduction: FROTH flotation is a widely used and effective method for separating valuable minerals in mineral processing [1].
- p.1 introduction: Despite significant progress in flotation grade prediction, there is still room for improvement as follows.
- p.2 introduction: To address these issues, this article proposes the multiscale dilated window attention transformer (MSDWT) model for froth flotation.
- p.2 introduction: The contributions of this article are as follows.
- p.2 introduction: The rest of the article is organized as follows. Section II discusses the froth flotation process for lead-zinc ore. Section III presents the input-output structure and model architecture proposed in this study. Section IV compares the proposed model with others from the literature. Finally, Section V presents the conclusions.
- p.2 method: To predict the grade of zinc concentrate more accurately, it is essential to extract the visual features of the froth surface from videos captured at the top of Cleaner III.
- p.3 method: This article introduces the MSDWT to address three main challenges in flotation grade prediction: nonstationary distributions, multiscale dependencies, and asymmetric risk.
- p.7 experiments: The zinc concentrate flotation froth data used in this study were supplied by a lead-zinc flotation plant in Shaoguan, Guangdong Province.
- p.8 experiments: Among all the metrics, the MSDWT model proposed in this study outperforms all the others.
- p.10 conclusion: The MSDWT model presented in this article combines an MSDW attention mechanism with hybrid encoding, offering a novel approach to addressing the time-varying nature of flotation froth features.
- p.10 conclusion: Experimental results validate the model's superiority in grade prediction, demonstrating a substantial improvement in accuracy over the existing methods.
- p.10 conclusion: Therefore, the development of delay-robust alignment methods, such as estimating the delay as a learnable parameter or employing dynamic time warping algorithms, is a crucial direction for future work.
