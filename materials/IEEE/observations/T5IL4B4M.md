---
key: T5IL4B4M
title: "A Soft Sensor Modeling Method Based on a Temporally Aware Dynamic Causal Graph Neural Network and Its Applications"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2026.3697037"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. PRELIMINARIES` → `IV. TEMPORALLY AWARE DYNAMIC CAUSAL GRAPH NEURAL NETWORK FOR INDUSTRIAL SOFT SENSOR MODELING` → `V. EXPERIMENTAL VALIDATION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mechanism / knowledge / data-driven，再评 SVR/PLSR/PCA 与 GNN 软测量）。Introduction 末有节序路标，指向 Section II–VI。Method 在 IV。Experiments 标题为 `EXPERIMENTAL VALIDATION`（SRU + 高炉）。

## Openers

- abstract: `Soft sensors are` — "Soft sensors are computational models that estimate difficult-to-measure target variables in real time by utilizing easily measurable process variables." (p.1)
- introduction: `PROCESS industries have` — "PROCESS industries have become increasingly complex due to the high dimensionality of process variables and the growing degree of coupling and nonlinearity among process parameters." (p.1；栏首掉字)
- method: `In industrial processes` — "In industrial processes, the evolution of process variables is influenced not only by the immediate effects of current inputs but also by intricate interactions unfolding overextended temporal horizons." (p.4, IV.A)
- experiments: `To verify the` — "To verify the effectiveness of the proposed T-DCGCN soft sensor model, experiments were conducted on two industrial case studies: a sulfur recovery unit (SRU) and a BF from a steel plant in southern China." (p.7, V)
- conclusion: `Achieving high-precision monitoring` — "Achieving high-precision monitoring and control of industrial processes hinges on the development of accurate and robust soft sensor models." (p.11)

## Gap transitions

- however (abstract): "They have been extensively deployed across a range of complex industrial systems and have demonstrated robust efficacy. However, prevailing methods often struggle to capture time-varying dependency structures and dynamic causal mechanisms among variables, thereby limiting their predictive accuracy and interpretability." (p.1)
- despite (introduction): "Despite recent advances in graph-based industrial soft sensor modeling, several fundamental challenges persist." (p.2)
- to address (introduction): "To address these challenges, this article proposes a temporally aware dynamic causal graph framework for soft sensor modeling, enabling the precise representation of complex industrial processes." (p.2)
- to address (method): "To address these limitations, we propose a multiscale temporal feature extraction method using 1-D convolutional neural networks." (p.4)
- in the future (conclusion): "In the future, we will focus on addressing the issue of data distribution drift and developing hybrid modeling methods by combining the advantages of physics-informed priors and data-driven models, with the aim of enhancing the model's adaptability, interpretability, and reliability in practical applications." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction, method: "we propose a temporally aware dynamic causal graph neural network framework"; "this article proposes a temporally aware dynamic causal graph framework"; "we propose a multiscale temporal feature extraction method"
- demonstrate / causal / abstract, experiments, conclusion: "have demonstrated robust efficacy"; "demonstrate that our method significantly outperforms"; "Experimental results demonstrate that unidirectional causal enhancement"
- show / causal / experiments: "As shown in Table II, T-DCGCN yields the lowest MAE, RMSE, and SD"; "Fig. 11 and Table V present the quantitative comparison results"
- indicate / causal / experiments: "indicating its stronger overall advantage in both prediction accuracy and result stability"

## Cross-section linkers

- introduction → later sections: "The remainder of this article is organized as follows. Section II defines the problem. Section III provides relevant background knowledge. Section IV details the implementation of the proposed framework. Section V presents the experimental results and analysis based on public and real-world industrial case studies. Finally, Section VI concludes this article." (p.3)
- preliminaries → method: "The detailed theoretical formulation is provided in Section IV-B." (p.3)
- method → experiments: 框架段落后直接 `V. EXPERIMENTAL VALIDATION` (p.7)
- experiments → conclusion: 灵敏度段落后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 缺口用 `However, prevailing methods often struggle to`，贡献用 `we propose` + 框架名。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段，挑战用编号列表。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The contributions of this work are summarized as follows` + 编号列表。
- R005 Conclusion 先收回方法，再用 `In the future, we will focus on` 指向后续。

## Candidate phrases

- `To overcome these limitations, we propose` (abstract)
- `To address these challenges, this article proposes` (introduction)
- `The contributions of this work are summarized as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `To verify the effectiveness of the proposed` (experiments)
- `In the future, we will focus on addressing` (conclusion)

## House style

自称是 `we propose` / `this article proposes` / `this study` / `our method` / `the proposed framework`。未见 `Here we`。`we propose` 与 `this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Soft sensors are computational models that estimate difficult-to-measure target variables in real time by utilizing easily measurable process variables.
- p.1 abstract: They have been extensively deployed across a range of complex industrial systems and have demonstrated robust efficacy. However, prevailing methods often struggle to capture time-varying dependency structures and dynamic causal mechanisms among variables, thereby limiting their predictive accuracy and interpretability.
- p.1 abstract: To overcome these limitations, we propose a temporally aware dynamic causal graph neural network framework that enhances both the predictive fidelity and physical plausibility of soft sensor models in industrial environments.
- p.1 abstract: Experiments conducted on both public and real-world industrial datasets demonstrate that our method significantly outperforms mainstream baseline models in terms of prediction accuracy and causal modeling capability.
- p.1 introduction: PROCESS industries have become increasingly complex due to the high dimensionality of process variables and the growing degree of coupling and nonlinearity among process parameters.
- p.2 introduction: Despite recent advances in graph-based industrial soft sensor modeling, several fundamental challenges persist.
- p.2 introduction: To address these challenges, this article proposes a temporally aware dynamic causal graph framework for soft sensor modeling, enabling the precise representation of complex industrial processes.
- p.2 introduction: The contributions of this work are summarized as follows.
- p.3 introduction: The remainder of this article is organized as follows. Section II defines the problem. Section III provides relevant background knowledge. Section IV details the implementation of the proposed framework. Section V presents the experimental results and analysis based on public and real-world industrial case studies. Finally, Section VI concludes this article.
- p.4 method: In industrial processes, the evolution of process variables is influenced not only by the immediate effects of current inputs but also by intricate interactions unfolding overextended temporal horizons.
- p.4 method: To address these limitations, we propose a multiscale temporal feature extraction method using 1-D convolutional neural networks.
- p.7 experiments: To verify the effectiveness of the proposed T-DCGCN soft sensor model, experiments were conducted on two industrial case studies: a sulfur recovery unit (SRU) and a BF from a steel plant in southern China.
- p.8 experiments: As shown in Table II, T-DCGCN yields the lowest MAE, RMSE, and SD, demonstrating its stronger modeling capability for soft sensors in complex industrial processes.
- p.11 conclusion: Achieving high-precision monitoring and control of industrial processes hinges on the development of accurate and robust soft sensor models.
- p.11 conclusion: Experimental results demonstrate that unidirectional causal enhancement not only facilitates the extraction of latent process knowledge but also yields substantial gains in prediction performance.
- p.11 conclusion: In the future, we will focus on addressing the issue of data distribution drift and developing hybrid modeling methods by combining the advantages of physics-informed priors and data-driven models, with the aim of enhancing the model's adaptability, interpretability, and reliability in practical applications.
