---
key: WRGBWAX4
title: "Knowledge-Informed Neural Network for Nonlinear Model Predictive Control With Industrial Applications"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2023.3341031"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. HAMMERSTEIN SYSTEM` → `III. KNOWLEDGE-INFORMED NEURAL NETWORK-BASED MODEL PREDICTIVE CONTROL` → `IV. NUMERICAL SIMULATION` → `V. PH NEUTRALIZATION PROCESS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 Hammerstein/Wiener、NN-MPC、PINN）。Introduction 末有节序路标，指向 Section II–VI。Method 为 III。Experiments 拆成 IV 数值仿真与 V pH 中和过程。

## Openers

- abstract: `Modern industrial process` — "Modern industrial process control suffers from various difficulties, such as multivariable, multiconstrained, multiobjective, and strong nonlinearity." (p.1)
- introduction: `HIGH energy consumption` — "HIGH energy consumption, resource consumption, and severe environmental contamination are issues that modern industrial processes continue to face [1], [2], [3]." (p.1；栏首掉字)
- method: `The NMPC based` — "The NMPC based on neural network makes full use of the robustness and self-learning ability of neural network, and has received extensive attention in recent years." (p.3, III)
- experiments: `In this part` — "In this part, the viability and efficacy of the suggested KINNMPC approach are examined using a numerical simulation." (p.7, IV)
- conclusion: `In this article` — "In this article, the KINNMPC method is proposed to address the problem of data shortage during data-driven model training." (p.11)

## Gap transitions

- however (abstract): "However, one limitation of MPC is that sufficient data are required to build accurate predictive models." (p.1)
- to this end (abstract): "To this end, this article proposes a knowledge-informed neural network MPC solution." (p.1)
- however (introduction): "However, with the increase in complexity of the process, most modern industrial systems are nonlinear systems." (p.1)
- therefore (introduction): "Therefore, many research efforts have been made on nonlinear MPC (NMPC) [11], [12]." (p.1)
- however (introduction): "However, the input and output data of the system are inevitably contaminated by environmental noises." (p.2)
- however (introduction): "However, gathering and organizing datasets are time-consuming, which means that a lot of real-world industrial systems often cannot provide enough training datasets." (p.2)
- therefore (method): "Therefore, the SR-HSSKE method is proposed in order to extract system structure knowledge, which contains system overparameterization and system structure knowledge extraction." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a knowledge-informed neural network MPC solution"; "a novel knowledge-informed neural network based MPC (KINNMPC) method is proposed"; "the KINNMPC method is proposed"
- verify / causal / abstract: "A numerical simulation and a pH neutralization process experiment are conducted to verify the feasibility and effectiveness of the proposed method."
- indicate / causal / conclusion: "Extensive experiments are presented to validate the results, which indicate the advantages of the proposed method"
- can / speculative / abstract, method: "which can reduce the computational cost of rolling optimization while ensuring prediction performance."
- show / causal / experiments: "The results are shown in Fig. 7 and Table III."

## Cross-section linkers

- introduction → hammerstein: "The remainder of this article is organized as follows. Section II introduces the basic knowledge of Hammerstein system. In Section III, the details of KINNMPC are presented, including the process of system structure knowledge extraction, the construction of the KIFNN model, and the description of the MPC optimization problem. Section IV and Section V present experimental results to demonstrate the effectiveness of the KINNMPC solution. Finally, concluding remarks are given in Section VI." (p.2)
- method → experiments: 稳定性分析后直接 `IV. NUMERICAL SIMULATION` (p.7)
- experiments → conclusion: pH 控制结果后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `To this end, this article proposes` 在 MPC 局限句后给出方法。
- R002 Introduction 无独立 Related Work，用 `In this article, a novel ... is proposed` 转入方法后再给贡献列表。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI，实验拆成 IV 与 V 两节。
- R004 贡献用 `In summary, the main contributions of this article are as follows.` + 编号列表。
- R005 Conclusion 用 `In this article, the ... method is proposed to address`，末句 `Extensive experiments are presented to validate`。

## Candidate phrases

- `To this end, this article proposes` (abstract)
- `In this article, a novel ... method is proposed.` (introduction)
- `In summary, the main contributions of this article are as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this article, the ... method is proposed to address` (conclusion)

## House style

自称是 `this article` / `the proposed method` / `the suggested`（实验段）。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Modern industrial process control suffers from various difficulties, such as multivariable, multiconstrained, multiobjective, and strong nonlinearity.
- p.1 abstract: However, one limitation of MPC is that sufficient data are required to build accurate predictive models.
- p.1 abstract: To this end, this article proposes a knowledge-informed neural network MPC solution.
- p.1 abstract: A numerical simulation and a pH neutralization process experiment are conducted to verify the feasibility and effectiveness of the proposed method.
- p.1 introduction: HIGH energy consumption, resource consumption, and severe environmental contamination are issues that modern industrial processes continue to face [1], [2], [3].
- p.1 introduction: However, with the increase in complexity of the process, most modern industrial systems are nonlinear systems.
- p.1 introduction: Therefore, many research efforts have been made on nonlinear MPC (NMPC) [11], [12].
- p.2 introduction: However, the input and output data of the system are inevitably contaminated by environmental noises.
- p.2 introduction: However, gathering and organizing datasets are time-consuming, which means that a lot of real-world industrial systems often cannot provide enough training datasets.
- p.2 introduction: In this article, a novel knowledge-informed neural network based MPC (KINNMPC) method is proposed.
- p.2 introduction: In summary, the main contributions of this article are as follows.
- p.2 introduction: The remainder of this article is organized as follows. Section II introduces the basic knowledge of Hammerstein system. In Section III, the details of KINNMPC are presented, including the process of system structure knowledge extraction, the construction of the KIFNN model, and the description of the MPC optimization problem. Section IV and Section V present experimental results to demonstrate the effectiveness of the KINNMPC solution. Finally, concluding remarks are given in Section VI.
- p.3 method: The NMPC based on neural network makes full use of the robustness and self-learning ability of neural network, and has received extensive attention in recent years.
- p.3 method: Therefore, the SR-HSSKE method is proposed in order to extract system structure knowledge, which contains system overparameterization and system structure knowledge extraction.
- p.7 experiments: In this part, the viability and efficacy of the suggested KINNMPC approach are examined using a numerical simulation.
- p.9 experiments: However, the proposed KINNMPC method can also well control the system output tracking the setpoint and the performance indicators MSE and ITAE are the best in the case of insufficient training data.
- p.10 experiments: An experiment using an industrial process simulation platform is provided to evaluate the suggested method's practical applicability for actual industrial operations.
- p.11 conclusion: In this article, the KINNMPC method is proposed to address the problem of data shortage during data-driven model training.
- p.11 conclusion: Extensive experiments are presented to validate the results, which indicate the advantages of the proposed method in both computational time requirements for online optimization and the stable performance of insufficient data.
