---
key: J57EGIKD
title: "Multivariate time series representation learning with multi-task graph neural network"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2026.113894"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work` → `3. Preliminary` → `4. Method` → `5. Experiment` → `6. Conclusion`。前置 `A B S T R A C T` 与 `A R T I C L E I N F O` / `Keywords`。独立 Related Work：`2. Related work`（2.1 传统 DL、2.2 GNN）。Introduction 末有编号贡献 `(1)` `(2)` `(3)`，无单独节序路标。Method 按三任务：MTS reconstruction、global-level graph、local-level graph。Experiments 标题为 `5. Experiment`。

## Openers

- abstract: `Multivariate time series` — "Multivariate time series (MTS) representation learning poses a significant challenge in data mining."
- introduction: `Multivariate time series` — "Multivariate time series (MTS) are sequential collections of numerical data commonly observed in various real-life scenarios, such as sleep signals (Kontras et al., 2024), traffic flow (Zheng et al., 2024a), stock markets (Qiu et al., 2025), and other scientific and social domains (Han et al., 2024; Ekambaram et al., 2024)."
- related_work: `This section primarily` — "This section primarily reviews the main DL-based methods currently employed for MTS representation."
- method: `This section elaborates` — "This section elaborates on the proposed model MTGL, which adopts a multi-task architecture as illustrated in Fig. 2."
- experiments: `In this section` — "In this section, we present comprehensive experimental results that compare the proposed model with existing baselines."
- conclusion: `In this paper` — "In this paper, we propose a novel MTS representation model that leverages multi-task learning to capture both global and local-level graph representations."

## Gap transitions

- while (abstract): "While a few methods leverage graph neural networks (GNNs) to model spatial dependencies, but they often do not effectively capture both global and local features simultaneously"
- however (introduction): "However, these methods have often overlooked the spatial dependencies between different channels of time series."
- to overcome / to address (abstract, introduction): "To overcome these limitations, we present MTGL, a novel Multi-Task Graph Neural Network-based MTS Representation Learning Framework."
- in contrast (related work): "In contrast, our MTGL is designed as a multi-task representation learning framework rather than a single-task predictor."

## Hedge verbs

- present / causal / abstract: "we present MTGL, a novel Multi-Task Graph Neural Network-based MTS Representation Learning Framework."
- propose / causal / introduction, conclusion: "we propose a Multi-Task Graph Neural Network-based MTS Representation Learning (MTGL) Framework."; "we propose a novel MTS representation model"
- show / associative / abstract: "Extensive experiments show that the proposed method outperforms existing state-of-the-art baselines"
- demonstrate / causal / introduction, experiments: "The experimental results demonstrate the effectiveness of the model."

## Cross-section linkers

- introduction → related_work: 贡献列表后 `2. Related work`
- related_work → preliminary: GNN 对照后 `3. Preliminary`
- preliminary → method: 符号表后 `4. Method`
- method → experiments: 伪代码后 `5. Experiment`
- experiments → conclusion: 图演化可视化后 `6. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Related work`。
- R004 编号贡献：`The main contributions of this paper are summarized as follows:`
- R009 自称：`we present` / `we propose` / `In this paper, we propose`

## Candidate phrases

- `To overcome these limitations, we present MTGL` (abstract)
- `The main contributions of this paper are summarized as follows:` (introduction)
- `Extensive experiments show that the proposed method outperforms` (abstract)
- `In this paper, we propose a novel MTS representation model` (conclusion)

## House style

自称 `we present` / `we propose` / `our method` / `In this paper, we propose`。第一人称复数为主。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Multivariate time series (MTS) representation learning poses a significant challenge in data mining.
- abstract: To overcome these limitations, we present MTGL, a novel Multi-Task Graph Neural Network-based MTS Representation Learning Framework.
- abstract: Extensive experiments show that the proposed method outperforms existing state-of-the-art baselines on benchmark MTS datasets and the tunnel boring machine dataset.
- introduction: Multivariate time series (MTS) are sequential collections of numerical data commonly observed in various real-life scenarios, such as sleep signals (Kontras et al., 2024), traffic flow (Zheng et al., 2024a), stock markets (Qiu et al., 2025), and other scientific and social domains (Han et al., 2024; Ekambaram et al., 2024).
- introduction: The main contributions of this paper are summarized as follows:
- related_work: This section primarily reviews the main DL-based methods currently employed for MTS representation.
- related_work: In contrast, our MTGL is designed as a multi-task representation learning framework rather than a single-task predictor.
- method: This section elaborates on the proposed model MTGL, which adopts a multi-task architecture as illustrated in Fig. 2.
- experiments: In this section, we present comprehensive experimental results that compare the proposed model with existing baselines.
- conclusion: In this paper, we propose a novel MTS representation model that leverages multi-task learning to capture both global and local-level graph representations.
- conclusion: Our model has demonstrated superior performance across public datasets as well as the TBM dataset.
