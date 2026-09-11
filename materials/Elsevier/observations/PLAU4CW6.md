---
key: PLAU4CW6
title: "Efficient surrogate-based optimization framework integrating physics-informed neural networks, deep active learning and deep reinforcement learning: Multilayer thin films case study"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2025.113609"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `1.1. Related work` → `1.2. Motivations and contributions` → `1.3. Application to multilayer thin films design` → `2. Methodology` → `4` 实验（PINNs 数据生成 / DAL / DRL / interpretability / ablation） → `5. Limitations and future work` → `6. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。独立 Related Work（`1.1`）。Introduction 末有编号贡献。Method 先综述 PINNs/DAL/DRL 再给框架。Experiments 分阶段对比 FEM、PSO、GA。

## Openers

- abstract: `Surrogate-based optimization has` — "Surrogate-based optimization has been widely applied across various fields."
- introduction: `Surrogate-based optimization (SBO)` — "Surrogate-based optimization (SBO) has emerged as a powerful and efficient approach for solving optimization problems, particularly in scenarios where the evaluation of the objective function is computationally expensive or time-consuming (Grbcic et al., 2025; Parsons et al., 2024; Shukla et al., 2024)."
- related_work: `With the rapid` — "With the rapid development of deep learning, researchers have increasingly integrated it into the optimization processes, significantly enhancing the capabilities of SBO."
- method: `In this section` — "In this section, we first present an overview of the advanced deep learning methods employed in this study, including PINNs, DAL and DRL."
- experiments: `In this part` — "In this part, we construct a DAL surrogate model to predict thermal shock resistance." (s.4.2)
- conclusion: `This paper proposes` — "This paper proposes a novel integrated framework for efficient optimization."

## Gap transitions

- however (abstract): "However, existing frameworks suffer from slow data generation, extensive training data requirement, and inefficient design space exploration."
- to address (abstract): "To address these limitations, we propose a novel optimization framework integrating physics-informed neural networks (PINNs), deep active learning (DAL) and deep reinforcement learning (DRL)."
- despite (introduction): "Despite these advances in SBO, efficiency remains a persistent bottleneck across all its stages."
- therefore (introduction): "Therefore, a new framework that co-designs and tightly integrates advanced deep learning methods across all stages is imperative to achieve a breakthrough in overall efficiency."
- to address (introduction): "To address these issues and further enhance the efficiency of existing SBO approaches, we propose a novel optimization framework that integrates PINNs, DAL and DRL."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a novel optimization framework"; "This paper proposes a novel integrated framework"
- indicate / associative / abstract: "The results indicate that PINNs-based data generation is 38.37 % faster than finite element method, with a relative error below 0.68 %."
- demonstrate / causal / introduction, experiments: "demonstrating the performance of proposed framework"; "demonstrating that PINNs achieve nearly the same accuracy with significantly higher efficiency."

## Cross-section linkers

- introduction → method: 贡献清单后进入 `2. Methodology`
- method → experiments: PINNs/DAL/DRL 流程后进入第 4 节分阶段实验
- experiments → limitations: ablation 与工程延拓后 `5. Limitations and future work`
- limitations → conclusion: 局限段落后 `6. Conclusion`

## Candidate rules

- R001 独立 Related Work 作为 Introduction 子节 `1.1. Related work`。
- R004 编号贡献：`The main contributions of this work can be summarized as follows:`
- R009 自称：`we propose` / `This paper proposes`

## Candidate phrases

- `To address these limitations, we propose` (abstract)
- `Despite these advances in SBO, efficiency remains a persistent bottleneck` (introduction)
- `The main contributions of this work can be summarized as follows` (introduction)
- `This paper proposes a novel integrated framework` (conclusion)

## House style

自称 `we propose` / `This paper proposes` / `our framework`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Surrogate-based optimization has been widely applied across various fields.
- abstract: However, existing frameworks suffer from slow data generation, extensive training data requirement, and inefficient design space exploration.
- abstract: To address these limitations, we propose a novel optimization framework integrating physics-informed neural networks (PINNs), deep active learning (DAL) and deep reinforcement learning (DRL).
- abstract: The results indicate that PINNs-based data generation is 38.37 % faster than finite element method, with a relative error below 0.68 %.
- introduction: Surrogate-based optimization (SBO) has emerged as a powerful and efficient approach for solving optimization problems, particularly in scenarios where the evaluation of the objective function is computationally expensive or time-consuming (Grbcic et al., 2025; Parsons et al., 2024; Shukla et al., 2024).
- introduction: Despite these advances in SBO, efficiency remains a persistent bottleneck across all its stages.
- introduction: Therefore, a new framework that co-designs and tightly integrates advanced deep learning methods across all stages is imperative to achieve a breakthrough in overall efficiency.
- introduction: To address these issues and further enhance the efficiency of existing SBO approaches, we propose a novel optimization framework that integrates PINNs, DAL and DRL.
- introduction: The main contributions of this work can be summarized as follows:
- method: In this section, we first present an overview of the advanced deep learning methods employed in this study, including PINNs, DAL and DRL.
- experiments: In this part, we construct a DAL surrogate model to predict thermal shock resistance.
- conclusion: This paper proposes a novel integrated framework for efficient optimization.
- conclusion: Compared to the existing framework, our framework accelerates the multilayer thin films optimization case by 70.75 h.
