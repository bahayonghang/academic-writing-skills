---
key: NXND566X
title: "DAMPNN: Dynamic Adaptive Message Passing Neural Network for Industrial Soft Sensor"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3475419"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM ANALYSIS` → `III. DAMPNN MODEL` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 AE/RNN、GNN 软测量、预定义图、消息传递、读出）。`II. PROBLEM ANALYSIS` 为工业特性与问题形式化。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `CASE STUDIES`（发电锅炉 + 轧钢）。

## Openers

- abstract: `Data-driven soft sensor` — "Data-driven soft sensor modeling has received much attention in industrial processes." (p.1)
- introduction: `WITH the rapid` — "WITH the rapid advancement of information technology, deep learning-based soft sensor methods have been widely developed to predict quality variables in industrial processes [1]." (p.1；栏首掉字)
- method: `The graph-based soft` — "The graph-based soft sensor aims to predict the target variable according to the historical process variables from the perspective of graph." (p.3, III.A)
- experiments: `The power-generating boiler` — "The power-generating boiler is a common unit in the thermal power plant." (p.5, IV.A)
- conclusion: `In this article,` — "In this article, we proposed a new end-to-end graph neural network framework to achieve soft sensor modeling tasks in industrial processes." (p.10)

## Gap transitions

- however (abstract): "However, existing graph-based soft sensor models still confront several limitations: 1) these models usually depend on predefined graph structures or local dynamic graph; 2) they fail to study dynamic message passing mechanism; 3) they have not considered the importance of extracted features from the entire graph." (p.1)
- to handle (abstract): "To handle these problems, in this study, we develop a dynamic adaptive message passing neural network (DAMPNN) for industrial soft sensor." (p.1)
- although (introduction): "Although these soft sensor models have achieved great development in industrial processes, these models cannot explicitly model inherent spatial coupling relationships between process variables." (p.1)
- despite (introduction): "Despite this progress, they still face several problems." (p.1)
- to handle (introduction): "To handle these issues, in this article, we propose a dynamic adaptive message passing neural network (DAMPNN) for soft sensor modeling in industrial processes." (p.2)

## Hedge verbs

- develop / causal / abstract: "in this study, we develop a dynamic adaptive message passing neural network (DAMPNN)"
- propose / causal / abstract, introduction: "First, we propose an adaptive graph learning module"; "in this article, we propose a dynamic adaptive message passing neural network (DAMPNN)"
- demonstrate / causal / abstract: "comprehensive comparison results on two real-world industrial cases demonstrate that DAMPNN outperforms the existing graph-based soft sensor methods."
- show / causal / conclusion: "The experimental results of the power generating case study showed that the proposed model had obtained a 2% improvement in R2 than the existing SOTA model."

## Cross-section linkers

- introduction → problem: "The rest of this article is organized as follows. Section II provides the problem definition and analysis of industrial characteristics, and Section III illustrates the details of DAMPNN. We carry out a series of comparison experiments on two industrial cases in Section IV. Finally, Section V concludes this article." (p.2)
- method → experiments: 时间复杂度分析后直接 `IV. CASE STUDIES` (p.5)
- experiments → conclusion: 自适应图机理分析后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `in this study, we develop`，编号列出既有方法局限。
- R002 Introduction 无独立 Related Work；`II. PROBLEM ANALYSIS` 承接机理缺口。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The specific contributions can be summarized in threefolds.` + 编号列表。
- R005 Conclusion 用 `In this article, we proposed`，再用 `In the future, we will` 指向后续。

## Candidate phrases

- `To handle these problems, in this study, we develop` (abstract)
- `To handle these issues, in this article, we propose` (introduction)
- `The specific contributions can be summarized in threefolds.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, we proposed a new end-to-end graph neural network framework` (conclusion)

## House style

自称是 `in this study` / `in this article` / `we propose` / `we develop` / `the proposed model`。未见 `Here we`。未见 `In this paper`。`in this study, we develop` 与 `In this article, we proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Data-driven soft sensor modeling has received much attention in industrial processes.
- p.1 abstract: However, existing graph-based soft sensor models still confront several limitations: 1) these models usually depend on predefined graph structures or local dynamic graph; 2) they fail to study dynamic message passing mechanism; 3) they have not considered the importance of extracted features from the entire graph.
- p.1 abstract: To handle these problems, in this study, we develop a dynamic adaptive message passing neural network (DAMPNN) for industrial soft sensor.
- p.1 abstract: Finally, comprehensive comparison results on two real-world industrial cases demonstrate that DAMPNN outperforms the existing graph-based soft sensor methods.
- p.1 introduction: WITH the rapid advancement of information technology, deep learning-based soft sensor methods have been widely developed to predict quality variables in industrial processes [1].
- p.1 introduction: Although these soft sensor models have achieved great development in industrial processes, these models cannot explicitly model inherent spatial coupling relationships between process variables.
- p.1 introduction: Despite this progress, they still face several problems.
- p.2 introduction: To handle these issues, in this article, we propose a dynamic adaptive message passing neural network (DAMPNN) for soft sensor modeling in industrial processes.
- p.2 introduction: The rest of this article is organized as follows. Section II provides the problem definition and analysis of industrial characteristics, and Section III illustrates the details of DAMPNN. We carry out a series of comparison experiments on two industrial cases in Section IV. Finally, Section V concludes this article.
- p.3 method: The graph-based soft sensor aims to predict the target variable according to the historical process variables from the perspective of graph.
- p.5 experiments: The power-generating boiler is a common unit in the thermal power plant.
- p.10 conclusion: In this article, we proposed a new end-to-end graph neural network framework to achieve soft sensor modeling tasks in industrial processes.
- p.10 conclusion: The experimental results of the power generating case study showed that the proposed model had obtained a 2% improvement in R2 than the existing SOTA model.
- p.10 conclusion: In the future, we will combine the mechanism knowledge with graph network to improve the interpretability of the soft sensor model.
