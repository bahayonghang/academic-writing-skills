---
key: FDPIX9SM
title: "Reliable Soft Sensors With an Inherent Process Graph Constraint"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3372013"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "8798-8806"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. GRAPH-CONSTRAINED SOFT SENSORS` → `III. SIMULATION STUDY` → `IV. HIGH-LOW TRANSFORMER PROCESS STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 grey models、SJSPCA/LSPCA、GCN、GDN）。无 `The rest of this article is organized`。贡献列表两项后直接进入方法。Experiments 拆为仿真 `III` 与工业案例 `IV`。

## Openers

- abstract: `Nowadays, data-driven models` — "Nowadays, data-driven models have been prevalent in predicting hard-to-measure key quality indicators of industrial processes in order to improve product quality and process safety." (p.8798)
- introduction: `IN MODERN industry` — "IN MODERN industry, fast and accurate measurement and analysis of key quality indicators (KQIs) are of great significance to improve process safety and product quality [1], [2]." (p.8798)
- method: `Recently, with the` — "Recently, with the success of convolutional neural networks (CNNs) [17], researchers have been focusing on ways to apply convolution to arbitrary graphs, considering the fact that two-dimensional images are a special form of graph [18], [19], [20]." (p.8799)
- experiments: `The simulation data` — "The simulation data emulates a process with ten process variables that belong to a unit." (p.8802)
- conclusion: `In this work` — "In this work, we have proposed a new soft sensor model called GCSS that can incorporate a priori process knowledge into data-driven soft sensors." (p.8805)

## Gap transitions

- despite (abstract): "Despite their success, soft sensors suffer from poor reliability." (p.8798)
- in order to (abstract): "In order to alleviate this problem, in this article, we propose a graph-constrained soft-sensor (GCSS) model that uses graph convolutions based on the a priori undirected graph of the process variables." (p.8798)
- however (introduction): "However, many KQIs are difficult or expensive to measure." (p.8798)
- nevertheless (introduction): "Nevertheless, it is easy to find a graph structure in many industrial processes, where process diagrams can be readily obtained as a priori knowledge." (p.8799)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "in this article, we propose a graph-constrained soft-sensor (GCSS) model"; "the graph-constrained soft-sensor (GCSS) model is proposed"; "we have proposed a new soft sensor model"
- enjoy / causal / abstract: "the GCSS model enjoys better generalizability and reliability"
- show / causal / introduction, conclusion: "the GCSS is shown to outperform common soft sensors"; "Simulation and real-world case studies have shown"
- will continue / speculative / conclusion: "In the future, we will continue to find more ways to combine expert knowledge"

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. GRAPH-CONSTRAINED SOFT SENSORS`，无节序路标 (p.8799)
- method → experiments: 流程图抽图步骤后 `III. SIMULATION STUDY` (p.8802)
- simulation → industrial: "One can use our approach proposed in Section II-D to extract the graph, which will be shown in Section IV." (p.8803)
- industrial → conclusion: 残差对比后 `V. CONCLUSION` (p.8805)

## Candidate rules

- R002 Introduction 无独立 Related Work，grey-model/GNN 评述写在引言中段。
- R010 无 `The rest of this article is organized`，贡献后直接进入方法。
- R004 贡献用 `The main contributions of this article are as follows`，可仅两项。
- R013 双实验结构：`SIMULATION STUDY` 后接工业案例，节末用 `which will be shown in Section IV` 衔接。

## Candidate phrases

- `In order to alleviate this problem, in this article, we propose` (abstract)
- `in this article, the graph-constrained soft-sensor (GCSS) model is proposed` (introduction)
- `The main contributions of this article are as follows.` (introduction)
- `In this work, we have proposed a new soft sensor model called` (conclusion)
- `In the future, we will continue to` (conclusion)

## House style

自称 `in this article, we propose` / `In this work, we have proposed` / `our approach`。未见 `Here we`、`In this paper`。`in this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.8798 abstract: Nowadays, data-driven models have been prevalent in predicting hard-to-measure key quality indicators of industrial processes in order to improve product quality and process safety.
- p.8798 abstract: Despite their success, soft sensors suffer from poor reliability.
- p.8798 abstract: In order to alleviate this problem, in this article, we propose a graph-constrained soft-sensor (GCSS) model that uses graph convolutions based on the a priori undirected graph of the process variables.
- p.8798 abstract: With the aid of a priori graph knowledge, the GCSS model enjoys better generalizability and reliability.
- p.8798 introduction: IN MODERN industry, fast and accurate measurement and analysis of key quality indicators (KQIs) are of great significance to improve process safety and product quality [1], [2].
- p.8798 introduction: However, many KQIs are difficult or expensive to measure.
- p.8799 introduction: Nevertheless, it is easy to find a graph structure in many industrial processes, where process diagrams can be readily obtained as a priori knowledge.
- p.8799 introduction: Using this kind of graph, in this article, the graph-constrained soft-sensor (GCSS) model is proposed, as well as a general approach to extract undirected graph of process variables based on process diagrams.
- p.8799 introduction: The main contributions of this article are as follows.
- p.8799 method: Recently, with the success of convolutional neural networks (CNNs) [17], researchers have been focusing on ways to apply convolution to arbitrary graphs, considering the fact that two-dimensional images are a special form of graph [18], [19], [20].
- p.8802 experiments: The simulation data emulates a process with ten process variables that belong to a unit.
- p.8803 experiments: One can use our approach proposed in Section II-D to extract the graph, which will be shown in Section IV.
- p.8805 conclusion: In this work, we have proposed a new soft sensor model called GCSS that can incorporate a priori process knowledge into data-driven soft sensors.
- p.8805 conclusion: Simulation and real-world case studies have shown that our proposed method can improve the soft sensor's generalizability and reliability, even when the process's data distribution has changed to some extent.
- p.8805 conclusion: In the future, we will continue to find more ways to combine expert knowledge into data-driven models to improve the accuracy, reliability, and interpretability of process soft sensors.
