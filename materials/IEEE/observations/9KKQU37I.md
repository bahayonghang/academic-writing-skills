---
key: 9KKQU37I
title: "Missing Data Imputation for Industrial Time Series With Adaptive Median Iteration Based on Generative Adversarial Networks"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2024.3457625"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. STACKED ADAPTIVE MEAN ITERATION IMPUTATION FRAMEWORK` → 实验段（hydrocracking / SRU、Baseline Methods、Experimental results） → `V. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 statistical / machine learning / RNN / SAITS / GAIN / SSGAN）。Introduction 末有节序路标，指向 Section II–V。Method 标题为框架名。Experiments 在 IV（路标句写 `In Section IV, experiments are conducted`）。标题与正文缩写并存：题目/摘要用 Median，正文多用 Mean / SAMIIF。

## Openers

- abstract: `Time series in` — "Time series in industrial processes often exhibits missing data caused by inevitable factors such as equipment failures and sensor errors." (p.1)
- introduction: `Time series data` — "Time series data is valuable resource with extensive applications in industrial production [1, 2]." (p.1；栏首掉字 T)
- method: `This part introduces` — "This part introduces the Stacked Adaptive Mean Iteration Imputation Framework for reconstructing missing time-series data in industrial processes." (p.3, III)
- experiments: `We compared our` — "We compared our model with eight other imputation algorithms on the two datasets to verify its effectiveness." (p.7, IV.C)
- conclusion: `To address the` — "To address the issue of missing temporal data in industrial processes, we propose a Stacked Adaptive Median Iterative Imputation Network based on Generative Adversarial Networks." (p.8)

## Gap transitions

- to address (abstract): "To address this issue, this paper proposes an innovative GAN-based Stacked Adaptive Median Iterative Imputation Framework, named as SAMIIF." (p.1)
- however (introduction): "However, this approach may lead to the loss of crucial information, thereby impacting the accuracy of the model [19]." (p.1)
- however (introduction): "However, during the early stages of GAN model training, the ability of the generator to generate samples and the discriminator to discern real from fake samples are initially limited." (p.2)
- to address (introduction): "To address these issues, this paper proposes an innovative unsupervised learning framework called the Stacked Adaptive Mean Iterative Imputation Framework (SAMIIF)." (p.2)
- in comparison (experiments): "In comparison, the proposed SAMIIF algorithm outperforms the other eight algorithms in the experiments." (p.8)
- in the future (conclusion): "In the future, we will further investigate methods for handling MNAR and MAR types of missing data, expanding the applicability of the existing model." (p.8)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this paper proposes an innovative GAN-based Stacked Adaptive Median Iterative Imputation Framework"; "we propose a Stacked Adaptive Median Iterative Imputation Network"
- introduce / causal / abstract, method: "an adaptive learning mechanism framework is introduced"; "an adaptive learning mechanism is introduced"
- validate / causal / abstract: "extensive experiments are conducted to validate the superior performance of the proposed methods"
- demonstrate / causal / introduction: "experiments are conducted to demonstrate the superiority of the proposed method over other baseline approaches."
- show / causal / experiments: "As can be seen from the results of Table II and Fig. 6"

## Cross-section linkers

- introduction → preliminaries: "The remaining parts of this paper is structured as follows: Section II provides a brief introduction of Generative Adversarial Network (GAN). Section III details the proposed Stacked Adaptive Mean Iteration Imputation Framework (SAMIIF). In Section IV, experiments are conducted to demonstrate the superiority of the proposed method over other baseline approaches. Finally, Section V presents a concise summary of the main research findings of this paper." (p.2–3)
- preliminaries → method: GAIN 段落后 `III. STACKED ADAPTIVE MEAN ITERATION IMPUTATION FRAMEWORK` (p.3)
- method → experiments: 网络结构介绍后进入工业数据集与 baseline (p.6–7)
- experiments → conclusion: 结果段落后直接 `V. CONCLUSIONS` (p.8)

## Candidate rules

- R001 abstract 用 `To address this issue, this paper proposes` + 框架缩写。
- R002 Introduction 无独立 Related Work，缺失机制与 GAIN 评述写在引言中段。
- R003 Introduction 末用 `The remaining parts of this paper is structured as follows` 指向 II–V（主谓不一致保留原文）。
- R004 贡献用 `the main contributions of this paper are as follows` + 编号列表。
- R005 Conclusion 先收回方法，再用 `In the future, we will further investigate` 指向 MNAR/MAR。

## Candidate phrases

- `To address this issue, this paper proposes an innovative` (abstract)
- `To address these issues, this paper proposes an innovative unsupervised learning framework called` (introduction)
- `the main contributions of this paper are as follows:` (introduction)
- `The remaining parts of this paper is structured as follows:` (introduction)
- `To address the issue of missing temporal data in industrial processes, we propose` (conclusion)

## House style

自称是 `this paper` / `we propose` / `our model` / `the proposed methods`。未见 `Here we`。`this paper proposes` 与 `In this paper` 进 phrase_bank，不进 anti_ai_patterns。见 `this paper proposes`。

## Quotes

- p.1 abstract: Time series in industrial processes often exhibits missing data caused by inevitable factors such as equipment failures and sensor errors.
- p.1 abstract: Traditional imputation methods usually face challenges in capturing complex data distributions, structures, and time-dependent relationships.
- p.1 abstract: To address this issue, this paper proposes an innovative GAN-based Stacked Adaptive Median Iterative Imputation Framework, named as SAMIIF.
- p.1 abstract: Finally, extensive experiments are conducted to validate the superior performance of the proposed methods on real industrial datasets.
- p.1 introduction: Time series data is valuable resource with extensive applications in industrial production [1, 2].
- p.1 introduction: Hence, the correct handling of missing data and the precise completion of absent data in industrial time series constitute a challenging and pressing task, crucial for ensuring the accuracy of analytical results and the reliability of decisions.
- p.1 introduction: However, this approach may lead to the loss of crucial information, thereby impacting the accuracy of the model [19].
- p.2 introduction: To address these issues, this paper proposes an innovative unsupervised learning framework called the Stacked Adaptive Mean Iterative Imputation Framework (SAMIIF).
- p.2 introduction: In summary, the main contributions of this paper are as follows:
- p.2–3 introduction: The remaining parts of this paper is structured as follows: Section II provides a brief introduction of Generative Adversarial Network (GAN). Section III details the proposed Stacked Adaptive Mean Iteration Imputation Framework (SAMIIF). In Section IV, experiments are conducted to demonstrate the superiority of the proposed method over other baseline approaches. Finally, Section V presents a concise summary of the main research findings of this paper.
- p.3 method: This part introduces the Stacked Adaptive Mean Iteration Imputation Framework for reconstructing missing time-series data in industrial processes.
- p.7 experiments: We compared our model with eight other imputation algorithms on the two datasets to verify its effectiveness.
- p.8 experiments: In comparison, the proposed SAMIIF algorithm outperforms the other eight algorithms in the experiments.
- p.8 experiments: SAMIIF demonstrates outstanding imputation accuracy even at higher missing rates.
- p.8 conclusion: To address the issue of missing temporal data in industrial processes, we propose a Stacked Adaptive Median Iterative Imputation Network based on Generative Adversarial Networks.
- p.8 conclusion: In several real industrial process datasets, we simulated incomplete datasets with different missing rates and compared our method with others, verifying its superiority and stability.
- p.8 conclusion: In the future, we will further investigate methods for handling MNAR and MAR types of missing data, expanding the applicability of the existing model.
