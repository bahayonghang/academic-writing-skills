---
key: XSAB4F7I
title: "Process quality control through Bayesian optimization with adaptive local convergence"
venue: "Chemical Engineering Science"
doi: "10.1016/j.ces.2024.120039"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-18"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Quality control strategy via Bayesian optimization` → `3. Gaussian process model with quality target` → `4. Acquisition function` → `5. Bayesian optimization with adaptive local convergence` → `6. Industrial applications` → `7. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 DoE、DFO、BO/GP、EI 切换 CMA-ES）。Introduction 末无编号贡献，有节序路标。Method 拆成质量控制策略、GP、采集函数与自适应局部收敛。Experiments 标题为 `6. Industrial applications`（连续结晶 + HDPE）。

## Openers

- abstract: `How to take` — "How to take as few experiments as possible to achieve the desired quality target is a challenging and essential topic of process quality control, especially for complex and expensive manufacturing processes with high-dimensional quality outputs."
- introduction: `Quality control (Box` — "Quality control (Box and Draper, 1987; Box and Lucas, 1959) of manufacturing processes aims to search for the optimal operational condition to achieve the desired product quality targets."
- method: `The quality control` — "The quality control problem can be interpreted as the following optimization model for an industrial process with an expected design target."
- experiments: `This section illustrates` — "This section illustrates a continuous crystallization system of potassium chloride from water. (Yue and Kontar, 2020)"
- conclusion: `Quality control aims` — "Quality control aims to meet the desired product quality target via searching for optimal operational conditions."

## Gap transitions

- however (introduction): "However, it is worth noting that the DoE-based process modeling methods require many experiments, leading to substantially high cost of quality control."
- in order to (introduction): "In order to alleviate the drawbacks of the BO methods, the optimization procedure can be improved when running close to the local optimum."
- thus (introduction): "Thus, in the absence of process mechanisms, how to use as few experiments as possible to perform quality control for high-dimensional and small-sample industrial processes is of great engineering significance."
- therefore (method): "Therefore, without process models, the complex manufacturing processes are regarded as black boxes"

## Hedge verbs

- proposes / causal / abstract: "This paper proposes a Bayesian optimization (BO)-based strategy utilizing quality information with adaptive local convergence."
- are presented / causal / abstract: "Two applications with high-dimensional quality outputs are presented to demonstrate the effectiveness of the proposed method."
- are proposed / causal / introduction: "three strategies are proposed to reduce the uncertainty, incorporate the target information and accelerate local convergence."
- we propose / causal / method: "we propose a quality control strategy with adaptive local convergence based on BO methods." (conclusion 复述)

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section 2 provides the framework of a quality control strategy based on the BO method."
- method → experiments: "Two industrial applications, including the crystal size distribution for a continuous crystallizer and the molecular weight distribution for an ethylene homo-polymerization reactor, both with high-dimensional quality outputs, are illustrated in Section 6."
- experiments → conclusion: HDPE 对照后 `7. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this article is organized as follows`
- R009 自称：`This paper proposes` / `we propose` / `three strategies are proposed`

## Candidate phrases

- `This paper proposes a Bayesian optimization (BO)-based strategy utilizing quality information with adaptive local convergence` (abstract)
- `The rest of this article is organized as follows` (introduction)
- `Two applications with high-dimensional quality outputs are presented to demonstrate the effectiveness of the proposed method` (abstract)
- `we propose a quality control strategy with adaptive local convergence based on BO methods` (conclusion)

## House style

自称 `This paper proposes` / `we propose` / `are proposed`。第一人称复数与 `this paper` / `this article` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: How to take as few experiments as possible to achieve the desired quality target is a challenging and essential topic of process quality control, especially for complex and expensive manufacturing processes with high-dimensional quality outputs.
- abstract: This paper proposes a Bayesian optimization (BO)-based strategy utilizing quality information with adaptive local convergence.
- abstract: Two applications with high-dimensional quality outputs are presented to demonstrate the effectiveness of the proposed method.
- introduction: Quality control (Box and Draper, 1987; Box and Lucas, 1959) of manufacturing processes aims to search for the optimal operational condition to achieve the desired product quality targets.
- introduction: Thus, in the absence of process mechanisms, how to use as few experiments as possible to perform quality control for high-dimensional and small-sample industrial processes is of great engineering significance.
- introduction: However, it is worth noting that the DoE-based process modeling methods require many experiments, leading to substantially high cost of quality control.
- introduction: The rest of this article is organized as follows. Section 2 provides the framework of a quality control strategy based on the BO method.
- method: The quality control problem can be interpreted as the following optimization model for an industrial process with an expected design target.
- experiments: This section illustrates a continuous crystallization system of potassium chloride from water. (Yue and Kontar, 2020)
- conclusion: Quality control aims to meet the desired product quality target via searching for optimal operational conditions.
- conclusion: For complex manufacturing processes with high-dimensional quality outputs, in order to reduce the cost, we propose a quality control strategy with adaptive local convergence based on BO methods.
- conclusion: The comparison results in case studies show that the proposed quality control method can efficiently achieve the specified quality target.
