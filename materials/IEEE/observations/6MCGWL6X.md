---
key: 6MCGWL6X
title: "TMoE-P: Toward the Pareto Optimum for Multivariate Soft Sensors"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2024.3504736"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED METHOD` → `IV. EXPERIMENTS` → `V. RELATED WORK` → `VI. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。有独立相关工作节，位置在实验之后：`V. RELATED WORK`（data-driven soft sensor / parameter-sharing paradigm）。`related_work=independent`。Introduction 末有 `The rest of this paper is organized as follows` 路标，指向 II–VI。Method 在 III（OMoE / POW）。Experiments 标题为 `EXPERIMENTS`（SRU）。

## Openers

- abstract: `Multivariate soft sensors` — "Multivariate soft sensors seek to provide accurate estimation of multiple quality variables through the analysis of measurable process variables, representing a significant advance over the traditional focus on single-quality variable sensors within industrial manufacturing." (p.1)
- introduction: `PROCESS monitoring plays` — "PROCESS monitoring plays a significant role in industrial data analytics, directly associated with the manufacture of critical industrial products, e.g., oil, gas, rare metals, iron, and steel." (p.1；栏首掉字)
- method: `In this section` — "In this section, we develop the Objective-aware Mixture-of-Experts (OMoE) module, designed to handle catastrophic interference." (p.3, III.A)
- experiments: `To assess the` — "To assess the effectiveness of TMoE-P in soft sensor applications, three aspects are investigated:" (p.5, IV)
- conclusion: `In this work` — "In this work, we propose a Task-aware Mixture-of-Experts model combining the OMoE and the POW module capable of approaching Pareto optimality (TMoE-P) for the field of MVSS." (p.10)

## Gap transitions

- to address (abstract): "To address these issues, we reformulate multivariate soft sensors as a multi-objective optimization problem and propose the Task-aware Mixture-of-Experts framework for achieving the Pareto optimum (TMoE-P)." (p.1)
- however (introduction): "However, these methods fall short on two key issues that hinder their performance in practice: (1) catastrophic interference" (p.2)
- nonetheless (method): "Nonetheless, this may result in the optimizer prioritizing simple and dominant objectives while neglecting the optimization of others." (p.4)
- however (related work): "However, these methodologies generally concentrate on improving the accuracy of estimating single quality variables while disregarding the similarities and disparities among various quality variables, thus presenting limitations in addressing the comprehensive needs of MVSS." (p.10)
- despite (related work): "Despite the promising advancements in these models, their application in MVSS remains challenging." (p.10)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we reformulate multivariate soft sensors as a multi-objective optimization problem and propose"; "we propose the Task-aware Mixture-of-Experts framework"; "we propose a Task-aware Mixture-of-Experts model"
- devise / causal / abstract: "we devise a Pareto Objective Weighting (POW) module"
- may / speculative / introduction, method: "two critical issues, i.e., catastrophic interference and seesaw optimization, may compromise performance"; "this may result in the optimizer prioritizing"
- reveal / causal / conclusion: "The experimental results on the SRU chemical industry dataset reveal that TMoE-P outperforms"

## Cross-section linkers

- introduction → preliminaries: "The rest of this paper is organized as follows: Section II outlines the technical preliminaries necessary for understanding our proposed method. Section III details the implementation of TMoE-P. Section IV presents the overall performance and ablation study results on the MVSS task for the Sulfur Recovery Unit. Section V reviews relevant literature on data-driven soft sensors and parameter-sharing paradigms. Finally, Section VI summarizes our conclusions and future work." (p.2)
- method → experiments: 学习流程段落后接 `IV. EXPERIMENTS` (p.5)
- experiments → related work: 参数敏感性后接 `V. RELATED WORK` (p.10)
- related work → conclusion: "Our work incorporate a novel multi-objective optimization technology and an improved parameter-sharing paradigm to handle catastrophic interference and seesaw phenomenon issues with both theoretical and empirical guarantees." 随后 `VI. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `To address these issues, we reformulate ... and propose`，不用 `Here we`。
- R002 独立相关工作放在实验之后，标题为 `RELATED WORK`。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–VI。
- R004 贡献用 `The contribution of this paper is summarized as follow:` + 编号列表。
- R005 TASE 前置 `Note to Practitioners—`。Conclusion 用 `In this work, we propose` 收回，再用 `Moving forward, our future research endeavors will concentrate on` 指向后续。

## Candidate phrases

- `To address these issues, we reformulate multivariate soft sensors as a multi-objective optimization problem and propose` (abstract)
- `The contribution of this paper is summarized as follow:` (introduction)
- `The rest of this paper is organized as follows:` (introduction)
- `In this work, we propose a Task-aware Mixture-of-Experts model` (conclusion)
- `Moving forward, our future research endeavors will concentrate on enhancing the fusion mechanism` (conclusion)

## House style

自称是 `we propose` / `this paper` / `this work` / `this study`（Note to Practitioners）。未见 `Here we`。`we propose` 与 `this paper` 进 phrase_bank，不进 anti_ai_patterns。见 `The rest of this paper is organized as follows`。

## Quotes

- p.1 abstract: Multivariate soft sensors seek to provide accurate estimation of multiple quality variables through the analysis of measurable process variables, representing a significant advance over the traditional focus on single-quality variable sensors within industrial manufacturing.
- p.1 abstract: To address these issues, we reformulate multivariate soft sensors as a multi-objective optimization problem and propose the Task-aware Mixture-of-Experts framework for achieving the Pareto optimum (TMoE-P).
- p.1 practitioners: Addressing the burgeoning complexity of estimating multiple quality variables in industrial manufacturing processes, this study introduces a novel Task-aware Mixture-of-Experts framework aiming for the Pareto Optimum (TMoE-P).
- p.1 introduction: PROCESS monitoring plays a significant role in industrial data analytics, directly associated with the manufacture of critical industrial products, e.g., oil, gas, rare metals, iron, and steel.
- p.2 introduction: However, these methods fall short on two key issues that hinder their performance in practice: (1) catastrophic interference, where sharing model parameters regardless of differences in objectives can lead to significant performance degradation due to differences in discriminative representation for each objective.
- p.2 introduction: The contribution of this paper is summarized as follow:
- p.2 introduction: The rest of this paper is organized as follows: Section II outlines the technical preliminaries necessary for understanding our proposed method. Section III details the implementation of TMoE-P. Section IV presents the overall performance and ablation study results on the MVSS task for the Sulfur Recovery Unit. Section V reviews relevant literature on data-driven soft sensors and parameter-sharing paradigms. Finally, Section VI summarizes our conclusions and future work.
- p.3 method: In this section, we develop the Objective-aware Mixture-of-Experts (OMoE) module, designed to handle catastrophic interference.
- p.4 method: Nonetheless, this may result in the optimizer prioritizing simple and dominant objectives while neglecting the optimization of others.
- p.5 experiments: To assess the effectiveness of TMoE-P in soft sensor applications, three aspects are investigated:
- p.10 related work: However, these methodologies generally concentrate on improving the accuracy of estimating single quality variables while disregarding the similarities and disparities among various quality variables, thus presenting limitations in addressing the comprehensive needs of MVSS.
- p.10 related work: Despite the promising advancements in these models, their application in MVSS remains challenging.
- p.10 conclusion: In this work, we propose a Task-aware Mixture-of-Experts model combining the OMoE and the POW module capable of approaching Pareto optimality (TMoE-P) for the field of MVSS.
- p.10 conclusion: The experimental results on the SRU chemical industry dataset reveal that TMoE-P outperforms the SOTA soft sensor model and the conventional regression model.
- p.10 conclusion: Acknowledging the current work’s limitations, our study faces challenges related to executing extensive experiments with a vast array of experts.
- p.10 conclusion: Moving forward, our future research endeavors will concentrate on enhancing the fusion mechanism within the gating network for better scalability and efficacy, extending our model’s modulization capabilities.
