---
key: DEJ5PHDZ
title: "A Soft Sensor Model Based on RIME-TCN-BiGRU-Attention for Predicting Heavy Calcium Carbonate Particle Size Distribution"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3551474"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. HCC GRINDING PROCESS DATA COLLECTION AND PREPROCESSING` → `IV. TCN DESIGN` → `V. RESULTS AND DISCUSSION` → `VI. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCLATURE`。有独立 Related Work（Section II）。Introduction 末有节序路标。Method 为 III–IV（数据与 TBiGA/RIME）。Experiments 为 `RESULTS AND DISCUSSION`。

## Openers

- abstract: `The online measurement` — "The online measurement of particle size distribution is significant to the particle size control of heavy calcium carbonate (HCC) powder." (p.1)
- introduction: `HEAVY calcium carbonate` — "HEAVY calcium carbonate (HCC) powder is made of natural carbonate minerals, such as calcite, marble, and limestone grinding, and is a commonly used powder inorganic filler, widely used in rubber, plastics, coatings, and other industries." (p.2；栏首掉字)
- method: `TCN is a` — "TCN is a neural network structure derived from CNN [30]." (p.5, IV.A)
- experiments: `In this article` — "In this article, the effectiveness of the model prediction is evaluated by five evaluation indicators: goodness of fit (R^2), MAPE, mean square error (mse), mean absolute error (MAE), and root-mean-squared error (RMSE)." (p.8, V.A)
- conclusion: `Aiming at the` — "Aiming at the measurement of HCC particle size distribution produced by the VRM system, a TBiGA soft sensor model based on MIC and hybrid network structures is proposed, which can effectively enhance the soft-sensing accuracy of HCC particle size distribution." (p.10)

## Gap transitions

- moreover (abstract): "Moreover, the nonlinear, strong coupling, and time-delay characteristics of VRM system pose a major challenge to the realization of high-precision soft sensing for HCC particle size distribution." (p.1)
- however (introduction): "However, there is a strong delay due to the small sampling amount and long sampling interval." (p.2)
- however (introduction): "However, deep learning models can have a good application prospect in industrial process monitoring, for example, the unLSTM can provide reliable monitoring results in industrial fault detection [6]." (p.2)
- therefore (related work): "Therefore, inspired by the above research, a hybrid soft-sensing model based on TBiGA is proposed, which integrates techniques, including maximal information coefficient (MIC), TCN, bidirectional gated recurrent unit (BiGRU), attention mechanism, and RIME algorithm." (p.3)
- although (conclusion): "Although the proposed TBiGA model has high soft-sensing accuracy and generalization ability, in future studies, we will expand the soft sensing of particle size under different working conditions" (p.10)

## Hedge verbs

- propose / causal / abstract, related work: "We propose a soft sensor model combining"; "a hybrid soft-sensing model based on TBiGA is proposed"
- show / causal / abstract: "The results show that compared with other models, the proposed RIME-TCN-BiGRU-Attention (TBiGA) performs well"
- introduce / causal / introduction: "Section IV, the structure of the soft sensor model based on TBiGA ... is introduced in detail."
- verify / causal / conclusion: "the actual data verify the validity of the proposed model"
- perform / causal / experiments: "TBiGA performs best on both VRM1100 and VRM1800 systems"

## Cross-section linkers

- introduction → related work: "The rest of this article is structured as follows. Section II introduces the related work of this study. Section III introduces the grinding process ... In Section IV, the structure of the soft sensor model based on TBiGA ... is introduced in detail. Section V introduces the evaluation method, experimental results, and discussion of the model. In Section VI, we summarize the results of this article, analyze the advantages of the model, and draw conclusion and prospects for the future." (p.2)
- related work → method: 编号贡献 1)–3) 后接 `III. HCC GRINDING PROCESS DATA COLLECTION AND PREPROCESSING` (p.3)
- method → experiments: RIME 优化图后接 `V. RESULTS AND DISCUSSION` (p.8)
- experiments → conclusion: 小提琴图段落后接 `VI. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `We propose` 引出混合模型，再用 `First` / `Second` / `Finally` 分步。
- R002 独立 Related Work；贡献编号列表放在 Related Work 末而非 Introduction。
- R003 Introduction 末用 `The rest of this article is structured as follows` 指向 II–VI。
- R004 Experiments 标题为 `RESULTS AND DISCUSSION`。
- R005 Conclusion 用 `Aiming at` 开篇，再用 `Although` 接 future studies。

## Candidate phrases

- `We propose a soft sensor model combining` (abstract)
- `This article aims to improve` (introduction)
- `The rest of this article is structured as follows.` (introduction)
- `Therefore, inspired by the above research, a hybrid soft-sensing model based on TBiGA is proposed` (related work)
- `Although the proposed TBiGA model has` (conclusion)

## House style

自称是 `We propose` / `This article aims` / `this article` / `the proposed RIME-TBiGA` / `we will expand`。未见 `Here we`。`We propose` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: The online measurement of particle size distribution is significant to the particle size control of heavy calcium carbonate (HCC) powder.
- p.1 abstract: Moreover, the nonlinear, strong coupling, and time-delay characteristics of VRM system pose a major challenge to the realization of high-precision soft sensing for HCC particle size distribution.
- p.1 abstract: We propose a soft sensor model combining maximal information coefficient (MIC), temporal convolutional network (TCN), bidirectional gated recurrent unit (BiGRU), and attention mechanism.
- p.1 abstract: The results show that compared with other models, the proposed RIME-TCN-BiGRU-Attention (TBiGA) performs well in predicting the accuracy of particle size distribution, which is more suitable for online measurement of particle size distribution of HCC.
- p.2 introduction: HEAVY calcium carbonate (HCC) powder is made of natural carbonate minerals, such as calcite, marble, and limestone grinding, and is a commonly used powder inorganic filler, widely used in rubber, plastics, coatings, and other industries.
- p.2 introduction: This article aims to improve the soft-sensing accuracy of HCC powder production in the VRM system by using the RIME algorithm and TCN-BiGRU-Attention (TBiGA) model.
- p.2 introduction: The rest of this article is structured as follows. Section II introduces the related work of this study.
- p.3 related work: Therefore, inspired by the above research, a hybrid soft-sensing model based on TBiGA is proposed, which integrates techniques, including maximal information coefficient (MIC), TCN, bidirectional gated recurrent unit (BiGRU), attention mechanism, and RIME algorithm.
- p.5 method: TCN is a neural network structure derived from CNN [30].
- p.6 method: The structure of TBiGA model proposed in this article is shown in Fig. 4.
- p.8 experiments: In this article, the effectiveness of the model prediction is evaluated by five evaluation indicators: goodness of fit (R^2), MAPE, mean square error (mse), mean absolute error (MAE), and root-mean-squared error (RMSE).
- p.8 experiments: The results show that TBiGA significantly outperforms other methods in terms of prediction accuracy.
- p.10 conclusion: Aiming at the measurement of HCC particle size distribution produced by the VRM system, a TBiGA soft sensor model based on MIC and hybrid network structures is proposed, which can effectively enhance the soft-sensing accuracy of HCC particle size distribution.
- p.10 conclusion: The proposed model achieved 93.69% and 94.92% on VRM1100 and VRM1800, respectively, which is superior to other models in accurate prediction.
- p.10 conclusion: Although the proposed TBiGA model has high soft-sensing accuracy and generalization ability, in future studies, we will expand the soft sensing of particle size under different working conditions by increasing the recognition of different working conditions and increase the soft sensing of particle size distribution indexes such as D50, D97, and specific surface area to further improve the accuracy and generalization ability of the model.
