---
key: E69DRAXT
title: "BTPNet: A Probabilistic Spatial-Temporal Aware Network for Burn-Through Point Multistep Prediction in Sintering Process"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2024.3415072"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. ANALYSIS OF SINTERING PROCESS AND DATA CHARACTERISTICS` → `III. METHODOLOGY` → `IV. EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SVM / 灰理论 / K-means / AE / DBN / RNN / DSTED）。Introduction 末有 `The remainder of this article is given as follows.`。Method 在 III。Experiments 标题为 `EXPERIMENTAL STUDIES`。

## Openers

- abstract: `Burn-through point` — "Burn-through point (BTP) is a very key factor in maintaining the normal operation of the sintering process, which guarantees the yield and quality of sinter ore." (p.1)
- introduction: `WITH the development` — "WITH the development of industrial 4.0 and smart manufacturing, industrial processes, such as iron and steel, metallurgy, petrochemical, and other fields, have been gradually developing in the direction of informatization and intelligence [1], [2]." (p.1)
- method: `In this section` — "In this section, the multistep prediction of BTP is formalized as a sequence-to-sequence (Seq2Seq) prediction problem, and the basic encoder-decoder framework is just suitable for this task." (p.4, III)
- experiments: `In order to` — "In order to demonstrate the effectiveness of our BTPNet model, we utilize the actual data from the cooperative sintering plant." (p.7, IV.A)
- conclusion: `In this article` — "In this article, a BTPNet model based on spatial-temporal feature fusion and PE is proposed to deal with the problem of BTP multistep prediction." (p.11)

## Gap transitions

- due to (abstract): "Due to the characteristics of time-varying and multivariable coupling in the actual sintering process, it is difficult for traditional soft-sensor models to extract spatial-temporal features and reduce multistep prediction error accumulation." (p.1)
- to address (abstract): "To address these issues, in this study, we propose a probabilistic spatial-temporal aware network, called BTPNet" (p.1)
- therefore (introduction): "Therefore, data-driven soft-sensor methods have been developed and widely used to predict these key variables in modern industrial processes [5], [6], [7]." (p.1)
- therefore (introduction): "Therefore, developing an accurate BTP prediction model is crucial for improving the quality of sinter ore and reducing energy consumption in the sintering process [8]." (p.1)
- however (introduction): "However, in the iron ore sintering process, a typical industrial process, deep learning-based models are rarely developed for BTP multistep prediction." (p.2)
- therefore (introduction): "Therefore, it is necessary to establish an accurate BTP multistep prediction model by considering both temporal and spatial characteristics." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "in this study, we propose a probabilistic spatial-temporal aware network"; "a BTPNet model ... is proposed"
- demonstrate / causal / abstract, experiments: "the experimental results on a real sintering process demonstrate"; "In order to demonstrate the effectiveness"
- outperform / causal / abstract: "the proposed BTPNet model outperforms state-of-the-art multistep prediction models"
- aim / speculative / conclusion: "In the future, we aim to enhance the model’s generalization performance"

## Cross-section linkers

- introduction → method: "The remainder of this article is given as follows. The sintering process is briefly described, and the data characteristics are analyzed in Section II. Section III illustrates the procedures of the BTPNet model. The experimental results are discussed in Section IV. Finally, conclusions and future works are summarized in Section V." (p.2)
- method → experiments: 损失与 Adam 后 `IV. EXPERIMENTAL STUDIES` (p.7)
- experiments → conclusion: 超参敏感性后 `V. CONCLUSION` (p.11)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is given as follows` 指向 II–V。
- R004 贡献用加粗短语标题（`Novel Joint Framework` / `VIAM` / `PE Module`）而非纯编号列表。
- R005 Conclusion 先收回方法，再用 `In the future, we aim to`。

## Candidate phrases

- `To address these issues, in this study, we propose` (abstract)
- `To tackle the aforementioned problems, in this study, we propose` (introduction)
- `The remainder of this article is given as follows.` (introduction)
- `In this article, a BTPNet model ... is proposed to deal with` (conclusion)
- `In the future, we aim to enhance` (conclusion)

## House style

自称是 `in this study, we propose` / `In this article` / `our proposed BTPNet`。未见 `Here we`、`In this paper`。`in this study, we propose` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Burn-through point (BTP) is a very key factor in maintaining the normal operation of the sintering process, which guarantees the yield and quality of sinter ore.
- p.1 abstract: Due to the characteristics of time-varying and multivariable coupling in the actual sintering process, it is difficult for traditional soft-sensor models to extract spatial-temporal features and reduce multistep prediction error accumulation.
- p.1 abstract: To address these issues, in this study, we propose a probabilistic spatial-temporal aware network, called BTPNet, which is used to extract spatial-temporal feature for accurate BTP multistep prediction.
- p.1 abstract: Finally, the experimental results on a real sintering process demonstrate the proposed BTPNet model outperforms state-of-the-art multistep prediction models.
- p.1 introduction: WITH the development of industrial 4.0 and smart manufacturing, industrial processes, such as iron and steel, metallurgy, petrochemical, and other fields, have been gradually developing in the direction of informatization and intelligence [1], [2].
- p.1 introduction: Therefore, developing an accurate BTP prediction model is crucial for improving the quality of sinter ore and reducing energy consumption in the sintering process [8].
- p.2 introduction: However, in the iron ore sintering process, a typical industrial process, deep learning-based models are rarely developed for BTP multistep prediction.
- p.2 introduction: Therefore, it is necessary to establish an accurate BTP multistep prediction model by considering both temporal and spatial characteristics.
- p.2 introduction: To tackle the aforementioned problems, in this study, we propose a multistep encoder-decoder model based on the spatial-temporal feature extraction and probabilistic estimation (PE) method, named BTPNet, to achieve the BTP multistep prediction in advance.
- p.2 introduction: The remainder of this article is given as follows. The sintering process is briefly described, and the data characteristics are analyzed in Section II. Section III illustrates the procedures of the BTPNet model. The experimental results are discussed in Section IV. Finally, conclusions and future works are summarized in Section V.
- p.4 method: In this section, the multistep prediction of BTP is formalized as a sequence-to-sequence (Seq2Seq) prediction problem, and the basic encoder-decoder framework is just suitable for this task.
- p.7 experiments: In order to demonstrate the effectiveness of our BTPNet model, we utilize the actual data from the cooperative sintering plant.
- p.9 experiments: Thus, our proposed BTPNet model based on spatial-temporal feature extraction and PE modules has the greatest capability in predicting BTP in terms of all evaluation metrics, with HR exceeding 94% (RMSE = 1.3025, MAE = 0.9050).
- p.11 conclusion: In this article, a BTPNet model based on spatial-temporal feature fusion and PE is proposed to deal with the problem of BTP multistep prediction.
- p.11 conclusion: In the future, we aim to enhance the model’s generalization performance by using transfer learning or ensemble learning.
