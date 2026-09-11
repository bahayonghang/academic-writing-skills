---
key: 73ISM2CQ
title: "A Multistep Sequence-to-Sequence Model With Attention LSTM Neural Networks for Industrial Soft Sensor Application"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2023.3266104"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-7,8-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`：LSTM Network + Sequence-to-Sequence Structure）。Introduction 中段仍评 AE / RBM / CNN / RNN / LSTM 软测量，末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDY`（debutanizer + SRU）。

## Openers

- abstract: `Soft sensor technology` — "Soft sensor technology is widely used in industries to handle highly nonlinear, dynamic, time-dependent sequence data of industrial processes for predicting the key variables associated with auxiliary process variables." (p.1)
- introduction: `IN RECENT years` — "IN RECENT years, modern industry has grown rapidly in both scale and complexity, which puts forward extra requirements for process safety and efficiency, as well as the precise control of product quality." (p.1；栏首掉字)
- related_work: `Based on RNN` — "Based on RNN architectures, the LSTM network is proposed for the vanishing and exploding problem of gradient of the conventional RNN networks [40]." (p.3, II.A)
- method: `The complete architecture` — "The complete architecture of the proposed MA-LSTM model is shown in Fig. 1, which can be separated into three basic modules: the encoder, the decoder, and a 1-D weighted convolution module." (p.4, III)
- experiments: `In this section` — "In this section, relevant simulation case studies are carried out on an industrial debutanizer column process and an industrial sulfur recovery unit (SRU) to test the validation of the proposed MA-LSTM soft sensor model." (p.7, IV)
- conclusion: `In this article` — "In this article, a multistep sequence-to-sequence framework with two attention layers based on LSTM with a 1-D weighted convolution layer is designed for the soft sensor modeling application of various dynamic industrial processes." (p.11)

## Gap transitions

- however (introduction): "However, in practical industrial processes, many factors limit the real-time measurement of some quality variables." (p.1)
- however (introduction): "However, most soft sensor modeling methods are actually involved in the sequence-to-point framework, which can only predict the quality variables at a single time point and have limited guiding significance for product quality monitoring." (p.2)
- although (introduction): "Although the encoder–decoder structure will help to implement sequence-to-sequence prediction, the performance is still limited in terms of input delay caused by long input sequence." (p.2)
- to address (introduction): "To address the aforementioned issues, a multistep sequence-to-sequence soft sensor model with attention LSTM neural networks (MA-LSTM) is proposed for industrial processes in this article." (p.2)
- however (conclusion): "However, the calculation of the model cannot be carried out in parallel." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction: "a novel multistep sequence-to-sequence model based on attention LSTM (MA-LSTM) neural networks is proposed"; "MA-LSTM is proposed for industrial processes in this article"
- demonstrate / causal / abstract: "The superiority of the proposed framework is demonstrated through a debutanizer column case and a sulfur recovery process."
- can / speculative / introduction, conclusion: "an LSTM-based method can overcome gradient vanishing"; "the MA-LSTM model can filter and extract important features"
- show / causal / experiments: "Fig. 11 shows the comparison between the predicted values of four models"
- will / speculative / conclusion: "Future research will focus on the advanced neural network models"

## Cross-section linkers

- introduction → related work: "The remainder of this article is structured as follows. Section II introduces some preliminaries about LSTM and sequence-to-sequence structure, and then, Section III illustrates the detailed methodology of the proposed model. To evaluate the performance, two industrial cases are studied with comparative experiments in Section IV. Finally, Section V draws the conclusions." (p.3)
- related work → method: II.B 末 "The application of the framework in soft sensor modeling shows obvious progress" 随后 `III. METHODOLOGY` (p.4)
- method → experiments: 实现步骤与指标后 `IV. CASE STUDY` (p.7)
- experiments → conclusion: SRU 结果段落后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 贡献句用 `In this article, a novel ... is proposed`。
- R002 有独立 `II. RELATED WORKS`（预备性相关工作：LSTM + seq2seq）。
- R003 Introduction 末用 `The remainder of this article is structured as follows` 指向 II–V。
- R004 gap 链为 `However`（sequence-to-point）→ `Although`（encoder–decoder 仍受限）→ `To address the aforementioned issues`。
- R005 Conclusion 先收回框架，再用 `However` 承认不可并行，`Future research will focus on` 指向后续。

## Candidate phrases

- `In this article, a novel ... is proposed to` (abstract)
- `To address the aforementioned issues, a ... is proposed ... in this article.` (introduction)
- `The remainder of this article is structured as follows.` (introduction)
- `In this article, a multistep sequence-to-sequence framework ... is designed for` (conclusion)
- `Future research will focus on` (conclusion)

## House style

自称是 `In this article` / `this article` / `our model` / `the proposed MA-LSTM`。未见 `Here we`。未见 `In this paper`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Soft sensor technology is widely used in industries to handle highly nonlinear, dynamic, time-dependent sequence data of industrial processes for predicting the key variables associated with auxiliary process variables.
- p.1 abstract: In this article, a novel multistep sequence-to-sequence model based on attention LSTM (MA-LSTM) neural networks is proposed to improve the soft sensor modeling performance of industrial processes with strong dynamics and nonlinearity.
- p.1 abstract: The superiority of the proposed framework is demonstrated through a debutanizer column case and a sulfur recovery process.
- p.1 introduction: IN RECENT years, modern industry has grown rapidly in both scale and complexity, which puts forward extra requirements for process safety and efficiency, as well as the precise control of product quality.
- p.1 introduction: However, in practical industrial processes, many factors limit the real-time measurement of some quality variables.
- p.2 introduction: However, most soft sensor modeling methods are actually involved in the sequence-to-point framework, which can only predict the quality variables at a single time point and have limited guiding significance for product quality monitoring.
- p.2 introduction: Although the encoder–decoder structure will help to implement sequence-to-sequence prediction, the performance is still limited in terms of input delay caused by long input sequence.
- p.2 introduction: To address the aforementioned issues, a multistep sequence-to-sequence soft sensor model with attention LSTM neural networks (MA-LSTM) is proposed for industrial processes in this article.
- p.3 introduction: The remainder of this article is structured as follows. Section II introduces some preliminaries about LSTM and sequence-to-sequence structure, and then, Section III illustrates the detailed methodology of the proposed model. To evaluate the performance, two industrial cases are studied with comparative experiments in Section IV. Finally, Section V draws the conclusions.
- p.3 related_work: Based on RNN architectures, the LSTM network is proposed for the vanishing and exploding problem of gradient of the conventional RNN networks [40].
- p.4 method: The complete architecture of the proposed MA-LSTM model is shown in Fig. 1, which can be separated into three basic modules: the encoder, the decoder, and a 1-D weighted convolution module.
- p.7 experiments: In this section, relevant simulation case studies are carried out on an industrial debutanizer column process and an industrial sulfur recovery unit (SRU) to test the validation of the proposed MA-LSTM soft sensor model.
- p.11 conclusion: In this article, a multistep sequence-to-sequence framework with two attention layers based on LSTM with a 1-D weighted convolution layer is designed for the soft sensor modeling application of various dynamic industrial processes.
- p.11 conclusion: However, the calculation of the model cannot be carried out in parallel.
- p.11 conclusion: Future research will focus on the advanced neural network models for the prediction of longer series data, capturing the long-term dependence of dynamic process for multistep quality prediction.
