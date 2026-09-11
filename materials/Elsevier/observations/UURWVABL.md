---
key: UURWVABL
title: "A knowledge-refined hybrid graph model for quality prediction of industrial processes"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2024.109711"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related works` → 随后给出 KSGraphLSTM 方法 → `4. Case study` → `5. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。独立 Related Work（GNN/LSTM 预备）。Introduction 末有贡献段与节序路标。Experiments 标题为 `Case study`，对象为 debutanizer column。Conclusion 后接 CRediT 与利益声明。

## Openers

- abstract: `The complexity of` — "The complexity of industrial processes has spurred the application of soft sensor techniques for predicting key quality variables based on easy-measurable process variables."
- introduction: `The constant iteration` — "The constant iteration and advancement of technology have propelled industrial processes towards intelligent evolution."
- related_work: `GNN is a` — "GNN is a type of neural network model used for processing graph-structured data, capable of effectively extracting spatial information between data points."
- method: `In order to` — "In order to fully leverage the information of both domain knowledge and quality information, a supervised knowledge-data co-driven soft sensing framework named Knowledge-based Supervised GraphLSTM (KSGraphLSTM) model is proposed in this paper."
- experiments: `An industrial application` — "An industrial application is tested to validate the performance of the proposed KSGraphLSTM soft sensor in this section, which is a debutanizer column."
- conclusion: `This paper investigates` — "This paper investigates a KSGraphLSTM network for nonlinear dynamic soft sensor applications, which is a data-knowledge co-driven method."

## Gap transitions

- however (abstract): "However, these soft sensing models deeply rely on the quality of training data, where the domain knowledge is often ignored."
- to address (abstract): "To address these issues, this paper proposes a supervised framework based on a knowledge-refined hybrid graph network, which contributes to the artificial intelligence application of nonlinear dynamic soft sensors."
- consequently (introduction): "Consequently, in most industrial processes, it is challenging to implement monitoring of relevant quality variables."
- to address (introduction): "To address these issues, soft sensing technology has been widely developed and applied to predict key quality variables in industrial processes."
- therefore (introduction): "Therefore, we propose a method of constructing graph data refining by knowledge to address the issue of incomplete graph structures in complex industrial processes where domain knowledge cannot be fully obtained."

## Hedge verbs

- propose / causal / abstract, introduction: "this paper proposes a supervised framework"; "a ... framework named Knowledge-based Supervised GraphLSTM (KSGraphLSTM) model is proposed in this paper"
- demonstrate / associative / abstract: "the experimental results fully demonstrate the effectiveness and superiority of the method."
- indicate / associative / conclusion: "Experimental results indicate that the proposed KSGraphLSTM outperforms LSTM, SLSTM, VALSTM, and GCN soft sensors in terms of prediction performance."
- investigate / causal / conclusion: "This paper investigates a KSGraphLSTM network"

## Cross-section linkers

- introduction → related_work: "The rest of this paper is organized as follows. Section 2 briefly introduces some preliminaries of GNN and LSTM."
- related_work → method: GNN/LSTM 预备后进入 KSGraphLSTM 构建
- method → experiments: 训练流程后 `4. Case study`
- experiments → conclusion: 误差箱线图后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work。
- R003 节序路标：`The rest of this paper is organized as follows`
- R009 自称：`this paper proposes` / `is proposed in this paper` / `This paper investigates`

## Candidate phrases

- `To address these issues, this paper proposes` (abstract)
- `is proposed in this paper` (introduction)
- `The rest of this paper is organized as follows` (introduction)
- `This paper investigates a KSGraphLSTM network` (conclusion)
- `Experimental results indicate that the proposed` (conclusion)

## House style

自称 `this paper proposes` / `is proposed in this paper` / `This paper investigates` / `the proposed KSGraphLSTM`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The complexity of industrial processes has spurred the application of soft sensor techniques for predicting key quality variables based on easy-measurable process variables.
- abstract: However, these soft sensing models deeply rely on the quality of training data, where the domain knowledge is often ignored.
- abstract: To address these issues, this paper proposes a supervised framework based on a knowledge-refined hybrid graph network, which contributes to the artificial intelligence application of nonlinear dynamic soft sensors.
- abstract: Finally, the proposed framework was applied to an industrial debutanizer column, and the experimental results fully demonstrate the effectiveness and superiority of the method.
- introduction: The constant iteration and advancement of technology have propelled industrial processes towards intelligent evolution.
- introduction: To address these issues, soft sensing technology has been widely developed and applied to predict key quality variables in industrial processes.
- introduction: Therefore, we propose a method of constructing graph data refining by knowledge to address the issue of incomplete graph structures in complex industrial processes where domain knowledge cannot be fully obtained.
- introduction: In order to fully leverage the information of both domain knowledge and quality information, a supervised knowledge-data co-driven soft sensing framework named Knowledge-based Supervised GraphLSTM (KSGraphLSTM) model is proposed in this paper.
- introduction: The rest of this paper is organized as follows. Section 2 briefly introduces some preliminaries of GNN and LSTM.
- experiments: An industrial application is tested to validate the performance of the proposed KSGraphLSTM soft sensor in this section, which is a debutanizer column.
- conclusion: This paper investigates a KSGraphLSTM network for nonlinear dynamic soft sensor applications, which is a data-knowledge co-driven method.
- conclusion: Experimental results indicate that the proposed KSGraphLSTM outperforms LSTM, SLSTM, VALSTM, and GCN soft sensors in terms of prediction performance.
