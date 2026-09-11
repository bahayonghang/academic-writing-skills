---
key: 54KSYHLT
title: "Grade Prediction of Froth Flotation Based on Multistep Fusion Transformer Model"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3342458"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. RELEVANT THEORIES OF FROTH FLOTATION` → `III. MODEL STRUCTURE` → `IV. EXPERIMENT AND RESULT ANALYSIS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 RNN/LSTM/GRU 与 Enc–Dec、FR-R、STS-D 等泡沫品位模型）。Introduction 末有编号贡献与节序路标，指向 Section II–V。Method 标题为 `MODEL STRUCTURE`。Experiments 标题为 `EXPERIMENT AND RESULT ANALYSIS`（铅锌厂数据集、超参、对比、复杂度）。

## Openers

- abstract: `Accurate and timely` — "Accurate and timely foam grade prediction plays an important role in the flotation foam industry process." (p.6030)
- introduction: `MINERAL grade is` — "MINERAL grade is an important performance indicator of froth flotation [1], [2]." (p.6030；栏首掉字)
- method: `The overall framework` — "The overall framework of the model in this article is shown in Fig. 3." (p.6032)
- experiments: `The data of` — "The data of the froth flotation process were provided by a lead–zinc froth flotation plant in Guangdong Province." (p.6036)
- conclusion: `This article proposes` — "This article proposes an MSFT model for froth grade prediction, which takes into account the mapping relationship between multiple time series characteristics and froth grade series." (p.6039)

## Gap transitions

- however (abstract): "However, the information between foam characteristic series and foam grade series at different sampling times often does not match, making the prediction result lagging behind." (p.6030)
- however (introduction): "However, these models suitable for industrial monitoring field are not fully applicable to grade prediction in froth flotation, the reason is that the input characteristics and output tags of these models must be consistent in sampling time, and the time interval of each sampling must be equal." (p.6030)
- in view of (introduction): "In view of the above problems, a multistep fusion transformer (MSFT) model was designed for froth grade prediction in this article." (p.6031)
- in response to (method): "In response to the above shortcomings, this article proposes a multistep fusion self-attention structure." (p.6033)

## Hedge verbs

- design / causal / abstract, introduction: "A multistep fusion transformer (MSFT) model is designed in this article"; "a multistep fusion transformer (MSFT) model was designed"
- propose / causal / introduction, method: "We propose an MSFT model for froth grade prediction"; "this article proposes a multistep fusion self-attention structure"
- indicate / associative / experiments: "The above results indicate that derived models, such as RNN and LSTM, have advantages in processing short time series"
- verify / causal / experiments, conclusion: "which verifies the effectiveness of the multistep fusion self-attention mechanism"; "which verifies the effectiveness of the MSFT model"

## Cross-section linkers

- introduction → theories: "The rest of this article is organized as follows. Section II introduces the distribution characteristics of the froth dataset and the input and output of the proposed model. Section III describes the structure of the proposed model in this article. The model of this article and the models in other papers are compared in Section IV. Finally, Section V concludes this article." (p.6031)
- method → experiments: 损失定义后直接 `IV. EXPERIMENT AND RESULT ANALYSIS` (p.6036)
- experiments → conclusion: 复杂度段落后直接 `V. CONCLUSION` (p.6039)

## Candidate rules

- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions are as follows.` + 编号。
- R005 Conclusion 收回方法后用 `In further research, we will` 指向后续。

## Candidate phrases

- `A multistep fusion transformer (MSFT) model is designed in this article.` (abstract)
- `The main contributions are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article proposes an MSFT model for` (conclusion)
- `In further research, we will` (conclusion)

## House style

自称 `this article` / `We propose` / `the model in this article` / `This article proposes`。未见 `Here we`。`is designed in this article` 与 `This article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.6030 abstract: Accurate and timely foam grade prediction plays an important role in the flotation foam industry process.
- p.6030 abstract: However, the information between foam characteristic series and foam grade series at different sampling times often does not match, making the prediction result lagging behind.
- p.6030 abstract: A multistep fusion transformer (MSFT) model is designed in this article.
- p.6030 introduction: MINERAL grade is an important performance indicator of froth flotation [1], [2].
- p.6030 introduction: However, these models suitable for industrial monitoring field are not fully applicable to grade prediction in froth flotation, the reason is that the input characteristics and output tags of these models must be consistent in sampling time, and the time interval of each sampling must be equal.
- p.6031 introduction: In view of the above problems, a multistep fusion transformer (MSFT) model was designed for froth grade prediction in this article. The main contributions are as follows.
- p.6031 introduction: The rest of this article is organized as follows. Section II introduces the distribution characteristics of the froth dataset and the input and output of the proposed model. Section III describes the structure of the proposed model in this article. The model of this article and the models in other papers are compared in Section IV. Finally, Section V concludes this article.
- p.6032 method: The overall framework of the model in this article is shown in Fig. 3.
- p.6033 method: In response to the above shortcomings, this article proposes a multistep fusion self-attention structure.
- p.6036 experiments: The data of the froth flotation process were provided by a lead–zinc froth flotation plant in Guangdong Province.
- p.6038 experiments: Compared with RNN, LSTM, GRU, Transformer, Enc–Dec(RNN), FR-R, STS-D(LSTM), and FlotationNet models, the MSFT model has reduced the baseline by 30.3%, 30.3%, 30%, 66.9%, 30%, 45.8%, 55.2%, and 52.5%, respectively, among all indicators
- p.6039 conclusion: This article proposes an MSFT model for froth grade prediction, which takes into account the mapping relationship between multiple time series characteristics and froth grade series.
- p.6039 conclusion: In further research, we will predict the grade of froth based on the dynamic characteristics of froth and the status of multiple flotation cells to achieve better prediction results.
