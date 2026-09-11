---
key: PDPQLX73
title: "Novel Transformer Based on Gated Convolutional Neural Network for Dynamic Soft Sensor Modeling of Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2021.3086798"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. PROPOSED METHODOLOGY` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 ANN / PCA / PLS / ELM / LSTM / CNN / Transformer）。Introduction 无 `The rest of this article is organized` 路标；贡献列表后直接 `II. PROBLEM FORMULATION`。Method 在 III。Experiments 标题为 `CASE STUDIES`。

## Openers

- abstract: `Industrial process data` — "Industrial process data are usually time-series data collected by sensors, which have the characteristics of high nonlinearity, dynamics, and noises." (p.1521)
- introduction: `WITH the rapid` — "WITH the rapid development of data-measuring technologies and the wide use of the distributed control systems (DCS), recording and collecting data from industrial processes have become more and more easy [1]." (p.1521)
- method: `The overall architecture` — "The overall architecture of the proposed model is shown in Fig. 1." (p.1523, III)
- experiments: `In order to` — "In order to verify the effectiveness of the proposed method, relevant experiments on actual production process data of polypropylene and PTA are conducted by comparing the soft sensor performance of the BP, the ELM, the LSTM, the CNN+LSTM, and the GCT model." (p.1525, IV)
- conclusion: `This article proposed` — "This article proposed a novel GCT for dynamic soft sensor modeling of industrial processes." (p.1528)

## Gap transitions

- meanwhile (abstract): "Meanwhile, the soft-sensing methods considering timing characteristics based on the deep learning are usually faced with gradient vanishing and the difficulty in parallel computing." (p.1521)
- therefore (abstract): "Therefore, a novel Gated Convolutional neural network-based Transformer (GCT) is proposed for dynamic soft sensor modeling of industrial processes." (p.1521)
- however (introduction): "However, due to the complicated reaction process, it is difficult to guarantee system stability at any time, which limits the quality control in actual industrial processes [4]." (p.1521)
- however (introduction): "However, limited by the structure of the networks, these aforementioned methods usually only consider current status and do not fully explore the potential features in the historical data." (p.1522)
- however (introduction): "However, the forward and backward calculations of the recurrence neural network (RNN) are both sequential, which bring the problems of gradient vanishing and gradient explosion [22]." (p.1522)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a novel Gated Convolutional neural network-based Transformer (GCT) is proposed"; "This article proposed a novel GCT"
- show / causal / abstract, experiments: "the experiments ... show that the proposed method achieves state-of-the-art"; "The table shows that the GCT has the best fitting capability"
- indicate / causal / experiments: "Experiment results are shown in Fig. 5, which indicate that the GCT model performs best when w = 12"

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. PROBLEM FORMULATION`，再 `III. PROPOSED METHODOLOGY` (p.1522–1523)
- method → experiments: 指标段落后 `IV. CASE STUDIES` (p.1525)
- experiments → conclusion: 复杂度分析后 `V. CONCLUSION` (p.1528)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R004 贡献用 `The main contributions of this article are shown as follows.` + 编号列表。无节序路标。
- R005 Conclusion 先收回方法，再用 `In the future, we will explore`。
- R009 结论 `This article proposed a novel`。

## Candidate phrases

- `Therefore, a novel ... is proposed for` (abstract)
- `In this article, a novel ... model is proposed` (introduction)
- `The main contributions of this article are shown as follows.` (introduction)
- `In order to verify the effectiveness of the proposed method` (experiments)
- `This article proposed a novel` (conclusion)

## House style

自称是 `In this article` / `is proposed` / `This article proposed` / `we will explore`。未见 `Here we`、`In this paper`。`This article proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1521 abstract: Industrial process data are usually time-series data collected by sensors, which have the characteristics of high nonlinearity, dynamics, and noises.
- p.1521 abstract: Meanwhile, the soft-sensing methods considering timing characteristics based on the deep learning are usually faced with gradient vanishing and the difficulty in parallel computing.
- p.1521 abstract: Therefore, a novel Gated Convolutional neural network-based Transformer (GCT) is proposed for dynamic soft sensor modeling of industrial processes.
- p.1521 abstract: In this article, the experiments in the dynamic soft sensor modeling of polypropylene and purified terephthalic acid industrial processes show that the proposed method achieves state-of-the-art comparing with the back propagation neural network, the extreme learning machine, the long short-term memory (LSTM) and the LSTM based on the CNN.
- p.1521 introduction: WITH the rapid development of data-measuring technologies and the wide use of the distributed control systems (DCS), recording and collecting data from industrial processes have become more and more easy [1].
- p.1521 introduction: However, due to the complicated reaction process, it is difficult to guarantee system stability at any time, which limits the quality control in actual industrial processes [4].
- p.1522 introduction: However, limited by the structure of the networks, these aforementioned methods usually only consider current status and do not fully explore the potential features in the historical data.
- p.1522 introduction: In this article, a novel Gated CNN-based Transformer (GCT) model is proposed to build the dynamic soft sensing model of complex industrial processes.
- p.1522 introduction: The main contributions of this article are shown as follows.
- p.1523 method: The overall architecture of the proposed model is shown in Fig. 1.
- p.1525 experiments: In order to verify the effectiveness of the proposed method, relevant experiments on actual production process data of polypropylene and PTA are conducted by comparing the soft sensor performance of the BP, the ELM, the LSTM, the CNN+LSTM, and the GCT model.
- p.1526 experiments: The table shows that the GCT has the best fitting capability with an increase of the CORR by up to 20% and improvements of the RSE and the MAPE by at least 16.70% and 0.16%, respectively.
- p.1528 conclusion: This article proposed a novel GCT for dynamic soft sensor modeling of industrial processes.
- p.1528 conclusion: Experimental results of the BP, the ELM, the LSTM, the CNN+LSTM, and the GCT on actual production data of polypropylene and PTA showed that the proposed model can achieve state-of-the-art performance.
- p.1528 conclusion: In the future, we will explore the time patterns in the time series data more fully.
- p.1528 conclusion: Considering that in some scenarios, we are not only concerned with a single predictive value, but more concerned with the possible range of key indicators; therefore, we will try to model the probability of key indicators.
