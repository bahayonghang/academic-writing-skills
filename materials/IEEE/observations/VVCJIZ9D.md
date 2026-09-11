---
key: VVCJIZ9D
title: "E2AG: Entropy-Regularized Ensemble Adaptive Graph for Industrial Soft Sensor Modeling"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2024.124884"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. Introduction` → `II. Related Works` → `III. Preliminaries` → `IV. Proposed Approach` → `V.` 实验（含 `B. Experimental Protocol` / `C. Baseline Comparison`） → `VI. Conclusions`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 末有节序路标，指向 II–VI。

## Openers

- abstract: `Adaptive graph neural` — "Adaptive graph neural networks (AGNNs) have achieved remarkable success in industrial process soft sensing by incorporating explicit features that delineate the relationships between process variables." (p.1)
- introduction: `PREDICTING hard-to-measure` — "PREDICTING hard-to-measure quality variables from easy-to-obtain, high-dimensional sensory data is essential for advancing intelligent manufacturing [1], aiding decision-making [2], and improving anomaly detection & diagnostic accuracy [3]–[5] in the industrial sector." (p.1；栏首掉字)
- related_work: `Soft sensor modeling` — "Soft sensor modeling faces the challenge of addressing the graph-structured nature of industrial process variables [16], which is rooted in complex spatial coupling relationships." (p.2, II)
- method: `This work is` — "This work is primarily concerned with the supervised industrial soft sensor task." (p.4, IV.A)
- experiments: `The catalysis shift` — "The catalysis shift conversion (CSC) unit, carbon-dioxide absabsorption column (CAC), methanation furance unit (MFU), and primary reformer unit (PRU) from a real ammonia synthesis process are selected to demonstrate the effectiveness of E2AG model." (p.8, V.B；PDF 拼写保留)
- conclusion: `In this study,` — "In this study, to investigate the feasibility of learning row-normalized graphs within the gradient descent-based DL backends and improve the AGNN model efficiency, a novel model named E2AG was proposed." (p.13)

## Gap transitions

- however (introduction): "However, in the realm of industrial process monitoring, soft sensor modeling faces challenges due to complex spatial coupling relations, which can significantly affect prediction accuracy." (p.1)
- even-though (introduction): "Even though these works have proven the concept of the adaptive graph learning strategy, there are two long-ignored issues remaining to be addressed:" (p.2)
- while (related work / intro reprise): "While previous works have achieved considerable success in AGNN-based soft sensor modeling with notable prediction accuracy across various industrial processes, there remain several unresolved issues that motivate this paper:" (p.3)
- however (conclusion): "There are, however, several issues that remain unresolved." (p.13)
- firstly / secondly / finally (conclusion): "Firstly, the function class assumption of the velocity field presents a limitation." (p.13)

## Hedge verbs

- introduces / causal / abstract: "This article introduces a novel GNN framework, termed entropy-regularized ensemble adaptive graph (E2AG)"
- pioneers / causal / abstract: "this work pioneers a novel AGNN learning approach based on mirror descent"
- demonstrating / causal / abstract: "demonstrating the superiority of E2AG in industrial soft sensing applications"
- are selected to demonstrate / causal / experiments: "are selected to demonstrate the effectiveness of E2AG model"
- was proposed / past / conclusion: "a novel model named E2AG was proposed"
- was validated / causal / conclusion: "the efficacy of the E2AG model was validated through its application to two inferential sensor tasks"

## Cross-section linkers

- introduction → related work: "The rest of this paper is organized as follows: To better understand the technical gap and concerning background knowledge, related works, and preliminaries are summarized in Sections II and III, respectively. On this basis, the model derivation and effectiveness validation are proposed in Sections IV and V, respectively. Finally, the conclusions and future research directions are given in Section VI." (p.2)
- related work → preliminaries: 技术缺口复述后 `III. Preliminaries` (p.3)
- method → experiments: 理论分析后进入 V 的 `B. Experimental Protocol` (p.8)
- experiments → conclusion: 敏感性分析后直接 `VI. Conclusions` (p.13)

## Candidate rules

- R001 摘要用 `This article introduces a novel GNN framework, termed` + 方法缩写。
- R002 Introduction 立两项编号缺口，再给独立 `II. Related Works`。
- R003 Introduction 末用 `The rest of this paper is organized as follows:` 指向 II–VI。
- R004 Conclusion 用过去式 `was proposed` / `was validated`，再用 `There are, however, several issues that remain unresolved.` + Firstly/Secondly/Finally。

## Candidate phrases

- `This article introduces a novel` (abstract)
- `The contributions of this paper are listed as follows:` (introduction)
- `The rest of this paper is organized as follows:` (introduction)
- `This work is primarily concerned with` (method)
- `There are, however, several issues that remain unresolved.` (conclusion)

## House style

自称是 `This article` / `this work` / `this paper` / `In this study`。摘要用 `This article introduces`。`This article introduces` 与 `this paper` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。

## Quotes

- p.1 abstract: Adaptive graph neural networks (AGNNs) have achieved remarkable success in industrial process soft sensing by incorporating explicit features that delineate the relationships between process variables.
- p.1 abstract: This article introduces a novel GNN framework, termed entropy-regularized ensemble adaptive graph (E2AG), aimed at enhancing the predictive accuracy of AGNNs.
- p.1 abstract: Specifically, this work pioneers a novel AGNN learning approach based on mirror descent, which is central to ensuring the efficiency of the training procedure and consequently guarantees that the learned graph naturally adheres to the row-normalization requirement intrinsic to the message-passing of GNNs.
- p.1 abstract: Finally, to ascertain the efficacy of the proposed E2AG model, extensive experiments are conducted on real-world industrial datasets.
- p.1 introduction: PREDICTING hard-to-measure quality variables from easy-to-obtain, high-dimensional sensory data is essential for advancing intelligent manufacturing [1], aiding decision-making [2], and improving anomaly detection & diagnostic accuracy [3]–[5] in the industrial sector.
- p.1 introduction: However, in the realm of industrial process monitoring, soft sensor modeling faces challenges due to complex spatial coupling relations, which can significantly affect prediction accuracy.
- p.2 introduction: Even though these works have proven the concept of the adaptive graph learning strategy, there are two long-ignored issues remaining to be addressed:
- p.2 introduction: The contributions of this paper are listed as follows:
- p.2 introduction: The rest of this paper is organized as follows: To better understand the technical gap and concerning background knowledge, related works, and preliminaries are summarized in Sections II and III, respectively.
- p.2 related_work: Soft sensor modeling faces the challenge of addressing the graph-structured nature of industrial process variables [16], which is rooted in complex spatial coupling relationships.
- p.3 related_work: While previous works have achieved considerable success in AGNN-based soft sensor modeling with notable prediction accuracy across various industrial processes, there remain several unresolved issues that motivate this paper:
- p.4 method: This work is primarily concerned with the supervised industrial soft sensor task.
- p.8 experiments: The catalysis shift conversion (CSC) unit, carbon-dioxide absabsorption column (CAC), methanation furance unit (MFU), and primary reformer unit (PRU) from a real ammonia synthesis process are selected to demonstrate the effectiveness of E2AG model.
- p.8 experiments: In this subsection, the question “Does E AG work?” is investigated.
- p.13 conclusion: In this study, to investigate the feasibility of learning row-normalized graphs within the gradient descent-based DL backends and improve the AGNN model efficiency, a novel model named E2AG was proposed.
- p.13 conclusion: Finally, the efficacy of the E2AG model was validated through its application to two inferential sensor tasks.
- p.13 conclusion: There are, however, several issues that remain unresolved.
