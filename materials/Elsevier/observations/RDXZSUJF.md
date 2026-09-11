---
key: RDXZSUJF
title: "Towards reliable control: Uncertainty-aware domain preserving stacked auto-encoder for data-driven modeling in large-scale industrial systems"
venue: "Control Engineering Practice"
doi: "10.1016/j.conengprac.2025.106383"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related works`（`2.1` 工业质量预测深度学习、`2.2` 不确定性估计）→ `3. Proposed B-UADP-SAE network model` → `4` 案例（数据集、对照、消融、不确定性影响）→ `5. Conclusion`。前置 `A B S T R A C T` 与 `A R T I C L E I N F O` / `Keywords`。独立 Related Work：`2. Related works`。Introduction 末编号贡献（`(1)` / `(2)` / `(3)`）。无 `The remainder of this paper` 路标。Method 含 bootstrap 不确定性、无监督预训练、监督微调。Experiments 为炼铁烧结质量指标对照。

## Openers

- abstract: `Online monitoring of` — "Online monitoring of operational states and quality indices in industrial processes is a vital source of information for enhancing production efficiency."
- introduction: `The stable operation` — "The stable operation of large-scale industrial systems is crucial for product quality and economic efficiency (Dogru et al., 2024; Jiang, Jiang et al., 2021)."
- related_work: `Owing to the` — "Owing to the substantial enhancement in the availability of process data and computational capabilities, deep learning has increasingly been applied to quality prediction in industrial processes due to its ability to handle complex, high-dimensional data (Jiang et al., 2020; Zhu et al., 2023)."
- method: `To mitigate the` — "To mitigate the adverse effects of uncertainty arising from variations in operating conditions and data noise on quality prediction in large-scale ironmaking systems, this paper proposes the B-UADP-SAE framework to predict key quality indices."
- experiments: `To validate the` — "To validate the advantages of the proposed model in data-driven modeling for the industrial predictive test, the following state-of-the-art methods based on SAE are selected for comparison:"
- conclusion: `This paper proposes` — "This paper proposes a new bootstrap-based uncertainty and key-region-aware semisupervised deep-learning method to address the significant uncertainty-related challenges in quality prediction for large-scale ironmaking systems."

## Gap transitions

- to address (abstract, introduction): "To address this issue, this paper proposes an uncertainty-aware key-domain-preserving stacked auto-encoder (UADP-SAE) model developed to capture the spatiotemporal distribution characteristics of dynamic operational changes in industrial systems."
- however (related work / method): "However, traditional SAE primarily focuses on capturing the global structure of data and neglecting the local structural uncertainty introduced by variations in localized operations."
- in summary (related work): "In summary, existing research has largely overlooked the distinct effect of uncertainty during the supervised and unsupervised learning stages, resulting in suboptimal usage of uncertainty to enhance model learning."
- despite (conclusion): "Despite the promising results, there are certain limitations."

## Hedge verbs

- proposes / causal / abstract: "this paper proposes an uncertainty-aware key-domain-preserving stacked auto-encoder (UADP-SAE) model"
- demonstrate / causal / abstract: "Experimental results demonstrate that the proposed method outperforms traditional methods, achieving almost 10% improvement across multiple evaluation metrics for the prediction of three sintered ore quality indicators."
- is proposed / causal / introduction: "a new predictive modeling framework that integrates a bootstrap-based uncertainty estimation method and uncertainty-aware domain-preserving stacked auto-encoder (UADP-SAE) is proposed."
- demonstrate / associative / conclusion: "Extensive experimental results demonstrate that the proposed method outperforms traditional approaches, achieving almost 10% improvement across multiple evaluation metrics for predicting three sintered ore quality indices."

## Cross-section linkers

- introduction → related_work: 编号贡献后 `2. Related works`
- related_work → method: 缺口陈述后 `3. Proposed B-UADP-SAE network model`
- method → experiments: 预测框架后案例 `4`（对照实验 `4.3. Comparison experiments and discussion`）
- experiments → conclusion: 不确定性拒识分析后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Related works`（位于 Introduction 之后、方法之前）。
- R004 编号贡献：`The contributions of this paper are:`
- R009 自称：`this paper proposes` / `This paper proposes`

## Candidate phrases

- `this paper proposes an uncertainty-aware key-domain-preserving stacked auto-encoder (UADP-SAE) model` (abstract)
- `The contributions of this paper are:` (introduction)
- `this paper proposes the B-UADP-SAE framework to predict key quality indices` (method)
- `This paper proposes a new bootstrap-based uncertainty and key-region-aware semisupervised deep-learning method` (conclusion)
- `Experimental results demonstrate that the proposed method outperforms traditional methods` (abstract)

## House style

自称 `this paper proposes` / `This paper proposes` / `is proposed`。`this paper` 为主。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Online monitoring of operational states and quality indices in industrial processes is a vital source of information for enhancing production efficiency.
- abstract: To address this issue, this paper proposes an uncertainty-aware key-domain-preserving stacked auto-encoder (UADP-SAE) model developed to capture the spatiotemporal distribution characteristics of dynamic operational changes in industrial systems.
- abstract: Experimental results demonstrate that the proposed method outperforms traditional methods, achieving almost 10% improvement across multiple evaluation metrics for the prediction of three sintered ore quality indicators.
- introduction: The stable operation of large-scale industrial systems is crucial for product quality and economic efficiency (Dogru et al., 2024; Jiang, Jiang et al., 2021).
- introduction: The contributions of this paper are:
- related_work: Owing to the substantial enhancement in the availability of process data and computational capabilities, deep learning has increasingly been applied to quality prediction in industrial processes due to its ability to handle complex, high-dimensional data (Jiang et al., 2020; Zhu et al., 2023).
- related_work: In summary, existing research has largely overlooked the distinct effect of uncertainty during the supervised and unsupervised learning stages, resulting in suboptimal usage of uncertainty to enhance model learning.
- method: To mitigate the adverse effects of uncertainty arising from variations in operating conditions and data noise on quality prediction in large-scale ironmaking systems, this paper proposes the B-UADP-SAE framework to predict key quality indices.
- method: However, traditional SAE primarily focuses on capturing the global structure of data and neglecting the local structural uncertainty introduced by variations in localized operations.
- experiments: To validate the advantages of the proposed model in data-driven modeling for the industrial predictive test, the following state-of-the-art methods based on SAE are selected for comparison:
- conclusion: This paper proposes a new bootstrap-based uncertainty and key-region-aware semisupervised deep-learning method to address the significant uncertainty-related challenges in quality prediction for large-scale ironmaking systems.
- conclusion: Extensive experimental results demonstrate that the proposed method outperforms traditional approaches, achieving almost 10% improvement across multiple evaluation metrics for predicting three sintered ore quality indices.
