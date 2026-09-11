---
key: KSMRMM9K
title: "AKGNN: When Adaptive Graph Neural Network Meets Kolmogorov-Arnold Network for Industrial Soft Sensors"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3551122"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PRELIMINARIES` → `IV. PROPOSED APPROACH` → `V. EXPERIMENTAL RESULTS` → `VI. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（Section II，含 GNNs / model architecture / Technical Gap Summary）。Introduction 末有编号贡献与节序路标。Method 为 IV。Experiments 为 Section V。early-access 页码 1–13。

## Openers

- abstract: `Data-driven soft` — "Data-driven soft sensors, which estimate quality variables from process variables, are very important to industrial processes." (p.1)
- introduction: `PREDICTING hard-to-measure` — "PREDICTING hard-to-measure quality variables from easy-to-measure, high-dimensional process variables is essential for advancing intelligent manufacturing [1–5], aiding decision-making [6–9], and improving anomaly detection & diagnostic accuracy [10–13]." (p.1；栏首掉字)
- method: `This work primarily` — "This work primarily focuses on industrial soft sensor tasks within continuous processes operating under steady-state conditions, within the context of supervised learning." (p.3, IV.A)
- experiments: `In this section` — "In this section, the following research questions (RQs) are answered to validate the effectiveness of the proposed approach empirically:" (p.6, V)
- conclusion: `In this paper` — "In this paper, we propose a novel model named AKGNN to enhance the performance of DL-based inferential sensor models by leveraging adaptive graph neural network techniques and the Kolmogorov–Arnold representation theorem." (p.10–11)

## Gap transitions

- however (abstract): "However, there remains significant room for enhancement in terms of accuracy in the deep learning (DL) era" (p.1)
- however (abstract): "However, the ground-truth 1) graph structure and 2) (semi-)empirical equations are unavailable in industrial practice." (p.1)
- even-though (introduction): "Even though previous works have proven the success of applying DL techniques for industrial soft sensor modeling, there remains room for improving the application of these DL architectures to industrial process data from the perspective of prediction accuracy." (p.1)
- meanwhile (introduction): "Meanwhile, directly integrating graph structures and (semi-)empirical equations into DL models presents challenges in two main areas:" (p.1)
- despite (related work): "Despite considerable advances in the development of adaptive graphs for GNN-based soft sensor modeling, a rigorous methodological framework for constructing these graphs remains elusive." (p.2)
- however (conclusion): "However, several challenges remain unresolved." (p.11)

## Hedge verbs

- introduce / causal / abstract: "this paper introduces a novel DL-based soft sensor model termed adaptive Kolmogorov Arnold-based graph neural network (AKGNN)."
- propose / causal / introduction, conclusion: "this work introduces"; "we propose a novel model named AKGNN"
- demonstrate / causal / abstract: "various experiments are conducted to demonstrate the effectiveness of the proposed AKGNN."
- formulate / causal / contributions: "We formulate graph construction within adaptive GNNs as an optimization problem"
- validate / causal / experiments: "the following research questions (RQs) are answered to validate the effectiveness"

## Cross-section linkers

- introduction → related work: "The rest of this paper is organized as follows: to better understand the technical gap and concerning background knowledge, related works, and preliminaries are summarized in Section II and Section III, respectively. On this basis, the model derivation and effectiveness validation are proposed in Section IV and Section V, respectively. Finally, the conclusions and future research directions are summarized in Section VI." (p.2)
- related work → method: Technical Gap Summary 后接 `III. PRELIMINARIES`，再 `IV. PROPOSED APPROACH` (p.2–3)
- method → experiments: Algorithm 1 / loss 后接 `V. EXPERIMENTAL RESULTS` (p.6)
- experiments → conclusion: sensitivity 段落后接 `VI. CONCLUSIONS` (p.10)

## Candidate rules

- R001 abstract 用 `this paper introduces` 引出 AKGNN；结论用 `In this paper, we propose`。
- R002 独立 Related Works，末有 `Technical Gap Summary` 编号缺口。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–VI。
- R004 Experiments 用 RQ1–RQ5 组织（Effectiveness / Accuracy / Complexity / Gains / Sensitivity）。
- R005 Conclusion 先收回方法，再用 `However, several challenges remain unresolved` 接 future work。

## Candidate phrases

- `To alleviate these challenges, this paper introduces` (abstract)
- `In summary, the contributions of this manuscript are as follows:` (introduction)
- `The rest of this paper is organized as follows:` (introduction)
- `In this section, the following research questions (RQs) are answered` (experiments)
- `In this paper, we propose a novel model named` (conclusion)

## House style

自称是 `this paper introduces` / `this paper` / `this work` / `we propose` / `we formulate` / `this manuscript`。未见 `Here we`。`this paper introduces` 与 `In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。摘要与结论均用 `this paper`。

## Quotes

- p.1 abstract: Data-driven soft sensors, which estimate quality variables from process variables, are very important to industrial processes.
- p.1 abstract: However, the ground-truth 1) graph structure and 2) (semi-)empirical equations are unavailable in industrial practice.
- p.1 abstract: To alleviate these challenges, this paper introduces a novel DL-based soft sensor model termed adaptive Kolmogorov Arnold-based graph neural network (AKGNN).
- p.1 abstract: Finally, the detailed algorithm for AKGNN is summarised and various experiments are conducted to demonstrate the effectiveness of the proposed AKGNN.
- p.1 introduction: PREDICTING hard-to-measure quality variables from easy-to-measure, high-dimensional process variables is essential for advancing intelligent manufacturing [1–5], aiding decision-making [6–9], and improving anomaly detection & diagnostic accuracy [10–13].
- p.1 introduction: Even though previous works have proven the success of applying DL techniques for industrial soft sensor modeling, there remains room for improving the application of these DL architectures to industrial process data from the perspective of prediction accuracy.
- p.2 introduction: In summary, the contributions of this manuscript are as follows:
- p.2 introduction: The rest of this paper is organized as follows: to better understand the technical gap and concerning background knowledge, related works, and preliminaries are summarized in Section II and Section III, respectively.
- p.2 related work: Despite considerable advances in the development of adaptive graphs for GNN-based soft sensor modeling, a rigorous methodological framework for constructing these graphs remains elusive.
- p.2 related work: In summary, the technical gaps motivating this paper are outlined as follows:
- p.3 method: This work primarily focuses on industrial soft sensor tasks within continuous processes operating under steady-state conditions, within the context of supervised learning.
- p.6 experiments: In this section, the following research questions (RQs) are answered to validate the effectiveness of the proposed approach empirically:
- p.9 experiments: For CA dataset, the AKGNN model surpasses most of the baseline models across several metrics, reducing RMSE by 28.98% to 74.16%, decreasing MAE by 31.92% to 74.79%, and improving R2 by 8.17% to 82.46%.
- p.10 conclusion: In this paper, we propose a novel model named AKGNN to enhance the performance of DL-based inferential sensor models by leveraging adaptive graph neural network techniques and the Kolmogorov–Arnold representation theorem.
- p.11 conclusion: However, several challenges remain unresolved.
- p.11 conclusion: Finally, cold-start problems, where little or no historical data is available, are a common challenge in industrial applications.
