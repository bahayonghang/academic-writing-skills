---
key: YMVFCESB
title: "SENGraph: A Self-Learning Evolutionary and Node-Aware Graph Network for Soft Sensing in Industrial Processes"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2024.3453288"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. SENGRAPH FRAMEWORK` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`：A. Deep Learning for Soft Sensing；B. Graph Neural Networks for Soft Sensing）。Introduction 末有 `The rest of this article is organized as follows.`。Method 在 III。Experiments 标题为 `CASE STUDIES`（发电、造纸、焙烧、SDS 中试）。

## Openers

- abstract: `The last decade` — "The last decade has witnessed the growing prevalence of deep models on soft sensing in industrial processes." (p.1)
- introduction: `IN MODERN industries` — "IN MODERN industries, accurate prediction of quality variables is an important fundamental problem for intelligent control and optimization to improve production efficiency." (p.1；栏首掉字)
- related work: `Deep learning, as` — "Deep learning, as a powerful tool of representation learning, has been extensively utilized in soft sensing modeling in industrial processes recently [22], [23]." (p.2, II.A)
- method: `This section first` — "This section first formalizes the coupling relations of process variables with graph networks." (p.3, III.A)
- experiments: `In this section` — "In this section, we perform extensive comparative and ablation studies to demonstrate the effectiveness and superiority of the proposed SENGraph model on four real-world industrial processes: power generating, papermaking, roasting processes, and sodium-based dry desulfurization system (SDS) desulphurization." (p.7, IV)
- conclusion: `In this article` — "In this article, we propose a new soft sensing framework called SENGraph based on GNNs." (p.14)

## Gap transitions

- however (abstract): "However, most of the existing soft sensing models are developed to learn from regular data in the Euclidean space, ignoring the complex coupling relations among process variables." (p.1)
- however (abstract): "However, the existing graph networks on soft sensing models still suffer from two major issues" (p.1)
- to address (abstract): "To address these problems, we propose a self-learning evolutionary and node-aware graph network (SENGraph) for industrial soft sensing." (p.1)
- however (introduction): "However, different from these techniques that build inside the Euclidean space, new findings have shown that the process variables are embedded with a latent spatial–topological structure of non-Euclidean characteristics [9]." (p.1)
- despite (introduction): "Despite these pioneering efforts, the vanilla implementation of graph networks to soft sensing still faces several domain-specific problems on different levels." (p.1)
- nevertheless (related work): "Nevertheless, the aforementioned soft sensing modeling methods are based on the Euclidean space." (p.2)
- however (related work): "However, these graph structures are either confined by predefined adjacent matrices or a single dynamic graph using Gaussian kernel distance, which is limited to describe the global relationships among process variables." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a self-learning evolutionary and node-aware graph network (SENGraph)"; "In this article, we propose a new soft sensing framework"
- demonstrate / causal / abstract, experiments: "Extensive experimental results and analysis on four real-world industrial datasets demonstrate"; "we perform extensive comparative and ablation studies to demonstrate"
- outperform / causal / abstract: "our proposed SENGraph model outperforms the existing state-of-the-art (SOTA) soft sensing methods"
- plan / speculative / conclusion: "In the future, we plan to conduct graph self-supervised learning"

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II performs literature reviews, and Section III provides the design details of SENGraph. Section IV compares SENGraph with some typical soft sensing models and discusses the experimental results, and Section V concludes this article." (p.2)
- related work → method: "To learn such time-varying dependencies under different working conditions, in this article, we propose an SLG method to learn the spatial coupling relationships from both global and local perspectives." 随后 `III. SENGRAPH FRAMEWORK` (p.3)
- method → experiments: 在线测试步骤后 `IV. CASE STUDIES` (p.7)
- experiments → conclusion: 中试部署后 `V. CONCLUSION` (p.14)

## Candidate rules

- R001 独立 Related Work 用 `II. RELATED WORKS` 分 A/B 子节。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this article are summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `In the future, we plan to`。

## Candidate phrases

- `To address these problems, we propose` (abstract)
- `To address these problems, in this article, we propose` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this section, we perform extensive comparative and ablation studies to demonstrate` (experiments)
- `In this article, we propose a new soft sensing framework` (conclusion)

## House style

自称是 `In this article, we propose` / `our proposed SENGraph` / `we propose`。未见 `Here we`、`In this paper`。`In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The last decade has witnessed the growing prevalence of deep models on soft sensing in industrial processes.
- p.1 abstract: However, most of the existing soft sensing models are developed to learn from regular data in the Euclidean space, ignoring the complex coupling relations among process variables.
- p.1 abstract: To address these problems, we propose a self-learning evolutionary and node-aware graph network (SENGraph) for industrial soft sensing.
- p.1 abstract: Extensive experimental results and analysis on four real-world industrial datasets demonstrate that our proposed SENGraph model outperforms the existing state-of-the-art (SOTA) soft sensing methods.
- p.1 introduction: IN MODERN industries, accurate prediction of quality variables is an important fundamental problem for intelligent control and optimization to improve production efficiency.
- p.1 introduction: Despite these pioneering efforts, the vanilla implementation of graph networks to soft sensing still faces several domain-specific problems on different levels.
- p.2 introduction: To address these problems, in this article, we propose a new Self-learning Evolutionary and Node-aware Graph learning framework called SENGraph for soft sensing in industrial processes.
- p.2 introduction: The rest of this article is organized as follows. Section II performs literature reviews, and Section III provides the design details of SENGraph. Section IV compares SENGraph with some typical soft sensing models and discusses the experimental results, and Section V concludes this article.
- p.2 related work: Deep learning, as a powerful tool of representation learning, has been extensively utilized in soft sensing modeling in industrial processes recently [22], [23].
- p.2 related work: Nevertheless, the aforementioned soft sensing modeling methods are based on the Euclidean space.
- p.3 related work: However, these graph structures are either confined by predefined adjacent matrices or a single dynamic graph using Gaussian kernel distance, which is limited to describe the global relationships among process variables.
- p.3 method: This section first formalizes the coupling relations of process variables with graph networks.
- p.7 experiments: In this section, we perform extensive comparative and ablation studies to demonstrate the effectiveness and superiority of the proposed SENGraph model on four real-world industrial processes: power generating, papermaking, roasting processes, and sodium-based dry desulfurization system (SDS) desulphurization.
- p.14 conclusion: In this article, we propose a new soft sensing framework called SENGraph based on GNNs.
- p.14 conclusion: In the future, we plan to conduct graph self-supervised learning to extract useful features from enormous unlabeled data, so as to solve the label scarcity issue in industrial scenarios.
