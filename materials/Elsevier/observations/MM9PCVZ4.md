---
key: MM9PCVZ4
title: "Development of novel dynamic machine learning-based optimization of a coal-fired power plant"
venue: "Computers & Chemical Engineering"
doi: "10.1016/j.compchemeng.2022.107848"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-40"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction`（含 `1.1. Background`、`1.2. Literature Review`、`1.3. Novelties of This Work`、`1.4. Organization`）→ `2. Methods` → `3. Results and Analysis` → `4. Conclusion`。前置 Abstract / Keywords。无独立 Related Work。`related_work=inlined`（`1.2. Literature Review` 并入 Introduction：APROS 动态模型、MPC、SVM/GA/PSO、SS-NNO、LSTM）。Introduction 末有项目符号贡献 + 节序路标。Method 含仿真模型、FF-NN/LSTM、PSO。Experiments 标题为 `3. Results and Analysis`。PDF 为 author manuscript / preprint。

## Openers

- abstract: `The increasing fraction` — "The increasing fraction of intermittent renewable energy in the electrical grid is resulting in coal-fired boilers now routinely ramp up and down."
- introduction: `As more intermittent` — "As more intermittent renewable energy is added to the electrical grid, there is greater need for increased flexibility, particularly from traditional fossil fuel power stations [1, 2, 3]."
- method: `In order to` — "In order to determine the effectiveness of dynamic optimization compared to steady-state optimization, a simulated plant is used as a replacement for the actual power plant because we cannot initiate control moves in a real power plant for exploration due to reliability concerns of the station."
- experiments: `The two machine` — "The two machine learning models were trained on the same dataset, with a portion of the dataset excluded to show the model’s ability to generalize – referred to here as the testing data."
- conclusion: `In light of` — "In light of the increasing need for coal-fired power stations to efficiently ramp in response to increasing renewable energy, this work presents a comparison study between steady-state optimization and dynamic optimization, where both methods rely on a neural network and PSO for determining adjustments to manipulated variables."

## Gap transitions

- unfortunately (literature): "Unfortunately, such a numerical model cannot be directly used for online optimization."
- however (literature): "However, the issue remains that first principles models (particularly combustion models that require CFD) are very manually intensive to design and in many cases remain numerically burdensome when placed in an optimization framework."
- however (literature): "However, there is promise in using a purely data-driven approach such as machine learning models for system-wide dynamic optimization because the computational cost is primarily paid in a less frequent training phase."
- however (literature): "however, there is a clear knowledge gap in demonstrating that machine learning can be applied to dynamic optimization of a coal-fired boiler."
- while (literature): "While the dynamic optimization problem is presumably more complex than a steady-state optimization problem, it has already been demonstrated that machine learning models can successfully capture and predict the dynamics of coal-fired boilers."

## Hedge verbs

- demonstrates / causal / abstract: "this work demonstrates the feasibility of extending this to dynamic, neural network-based optimization using a long short-term memory neural network."
- is shown / associative / abstract: "Dynamic optimization with a long short-term memory neural network is shown to both be feasible and beneficial for operation of a coal-fired boiler under changing load."
- seeks / causal / introduction: "This work seeks to demonstrate a novel, feasible method for performing dynamic optimization with a machine learning model."
- presents / causal / conclusion: "this work presents a comparison study between steady-state optimization and dynamic optimization"
- shows / associative / conclusion: "this work shows that it is both possible and beneficial to incorporate system dynamics into the optimization of a coal-fired boiler."
- may / hedge / conclusion: "Future work may include comparing different hyperparameter choices and model choices for dynamic optimization as well as optimizer choice and parameters."

## Cross-section linkers

- introduction → method: "This work is organized as follows. Section 2 describes the dynamic model used for simulation of the behavior and responses of a tangentially-fired boiler to control changes (Section 2.1), neural network configurations used in this study (Section 2.2), and the particle swarm algorithm and its parameters (Section 2.3)."
- method → experiments: "Section 3 shows the results and analysis of both the accuracy of the neural networks (Section 3.1) and their performance in closed-loop control (Section 3.2)."
- experiments → conclusion: "Finally, Section 4 offers some concluding remarks and observations."

## Candidate rules

- R002 Related Work 并入 Introduction（`1.2. Literature Review`）。
- R003 节序路标：`This work is organized as follows.`
- R004 项目符号贡献：`Following is an itemized list of novel contributions in this work:`
- R009 自称：`this work demonstrates` / `This work seeks` / `this work presents`

## Candidate phrases

- `this work demonstrates the feasibility of extending this to dynamic, neural network-based optimization` (abstract)
- `This work seeks to demonstrate a novel, feasible method for performing dynamic optimization with a machine learning model.` (introduction)
- `This work is organized as follows.` (introduction)
- `The D-NNO outperformed the SS-NNO in all five cases, and the SS-NNO consistently outperformed the baseline.` (experiments)
- `this work shows that it is both possible and beneficial to incorporate system dynamics into the optimization of a coal-fired boiler.` (conclusion)

## House style

自称 `this work demonstrates` / `This work seeks` / `this work presents`。`this work` 贯穿全文。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The increasing fraction of intermittent renewable energy in the electrical grid is resulting in coal-fired boilers now routinely ramp up and down.
- abstract: this work demonstrates the feasibility of extending this to dynamic, neural network-based optimization using a long short-term memory neural network.
- abstract: Using the same intervals and a particle swarm optimization algorithm, the dynamic optimization outperforms the steady-state optimization and realizes up to 4.58% improvement in thermal efficiency.
- introduction: As more intermittent renewable energy is added to the electrical grid, there is greater need for increased flexibility, particularly from traditional fossil fuel power stations [1, 2, 3].
- introduction: however, there is a clear knowledge gap in demonstrating that machine learning can be applied to dynamic optimization of a coal-fired boiler.
- introduction: This work is organized as follows. Section 2 describes the dynamic model used for simulation of the behavior and responses of a tangentially-fired boiler to control changes (Section 2.1), neural network configurations used in this study (Section 2.2), and the particle swarm algorithm and its parameters (Section 2.3).
- method: In order to determine the effectiveness of dynamic optimization compared to steady-state optimization, a simulated plant is used as a replacement for the actual power plant because we cannot initiate control moves in a real power plant for exploration due to reliability concerns of the station.
- experiments: The D-NNO outperformed the SS-NNO in all five cases, and the SS-NNO consistently outperformed the baseline.
- experiments: The D-NNO realized relative improvements ranging from 0.56% to 6.05% over the baseline and 0.50% to 4.58% over the SS-NNO.
- conclusion: In light of the increasing need for coal-fired power stations to efficiently ramp in response to increasing renewable energy, this work presents a comparison study between steady-state optimization and dynamic optimization, where both methods rely on a neural network and PSO for determining adjustments to manipulated variables.
- conclusion: The maximum difference between the thermal efficiency of the dynamic optimization and that of the baseline is 6.05%.
- conclusion: this work shows that it is both possible and beneficial to incorporate system dynamics into the optimization of a coal-fired boiler.
