---
key: ZVIVPYR4
title: "Advancing Industrial Process Control With Deep Learning-Enhanced Model Predictive Control for Nonlinear Time-Delay Systems"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3567401"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROPOSED METHOD` → `III. CASE STUDY` → `IV. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 Smith predictor / PID / fuzzy / MPC，再评 DL 与 LSTM/GRU）。Introduction 末有节序路标，指向 Section II–IV。Method 在正文中段。Experiments 标题为 `CASE STUDY`（数值仿真 + 工业回转窑）。

## Openers

- abstract: `In the process` — "In the process industries, nonlinear and large time-delay systems pose significant challenges for efficient model predictive control (MPC)." (p.1)
- introduction: `LARGE time-delay and` — "LARGE time-delay and nonlinearity are prevalent in process industries, such as chemical production, power systems, and metallurgy." (p.1；栏首掉字)
- method: `The DNNs-MPC combines` — "The DNNs-MPC combines deep neural networks and MPC to model systems and optimize control." (p.3, II.A)
- experiments: `The efficacy of` — "The efficacy of the algorithm was assessed using key metrics, including mean absolute error (MAE), root mean square error (RMSE), and coefficient of determination (R2) [23], integrated absolute error (IAE), and integrated squared error (ISE) [27]." (p.6, III.A)
- conclusion: `In this research` — "In this research, we have successfully introduced a DNNs-MPC, designed to enhance the control performance of industrial processes with nonlinear dynamics and significant time delays." (p.10)

## Gap transitions

- however (abstract): "The advent of deep learning offers innovative techniques for precise modeling and control; however, deep neural architectures have limited application in control problems." (p.1)
- despite (introduction): "Despite these advancements, integrating DL with traditional control frameworks, such as MPC, remains an emerging field with significant potential for innovation." (p.2)
- therefore (introduction): "Therefore, exploring efficient methods for controlling nonlinear and large time-delay systems is crucial for both theoretical advancement and practical industrial applications." (p.2)
- however (experiments): "However, their performance degrades somehow in the presence of noise, especially for PID and NMPC." (p.7)
- although (conclusion): "Although our method has exhibited commendable performance, it is sensitive to parameter settings." (p.10)
- therefore (conclusion): "Therefore, future research will focus on developing adaptive algorithms that can dynamically tune MPC parameters based on process feedback." (p.10)

## Hedge verbs

- introduce / causal / abstract, conclusion: "This study introduces"; "we have successfully introduced"
- propose / causal / abstract, introduction: "we propose an optimization strategy"; "We propose a DNNs-MPC approach"
- demonstrate / causal / abstract, conclusion: "demonstrating significant improvements"; "Our method has demonstrated superior predictive accuracy"
- show / causal / experiments: "Table II shows that when the noise level increases"; "Fig. 11 shows that as the reference temperature increases"
- aim / speculative / introduction, method: "This study aims to address these challenges"; "The DNNs-MPC model aims to compute the optimal control input"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section II details the research methodology employed. Section III presents experimental results to validate the effectiveness of the proposed approach, followed by a summary. Finally, Section IV concludes this article." (p.3)
- method → experiments: "The detailed execution process of the DNNs-MPC is shown in Algorithm 1." 随后 `III. CASE STUDY` (p.6)
- experiments → conclusion: 结果段落后直接 `IV. CONCLUSION`，无单独讨论节 (p.10)

## Candidate rules

- R001 abstract 贡献句用 `This study introduces` + 方法缩写，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–IV。
- R004 贡献用 `The main contributions of this article are as follows` + 编号列表。
- R005 Conclusion 先收回方法，再用 `Although` 承认局限，`Therefore, future research will` 指向后续。

## Candidate phrases

- `This study introduces` (abstract)
- `we propose an optimization strategy that` (abstract)
- `This study aims to address these challenges by introducing` (introduction)
- `The main contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this research, we have successfully introduced` (conclusion)

## House style

自称是 `This study` / `this article` / `In this research` / `we propose` / `Our method`。未见 `Here we`。`This study introduces` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In the process industries, nonlinear and large time-delay systems pose significant challenges for efficient model predictive control (MPC).
- p.1 abstract: The advent of deep learning offers innovative techniques for precise modeling and control; however, deep neural architectures have limited application in control problems.
- p.1 abstract: This study introduces a deep neural networks-based model predictive control (DNNs-MPC) that can utilize various gradient-based neural network models as predictors, enhancing the predictive capabilities of MPC and improving performance for nonlinear systems with large time-delay.
- p.1 abstract: Concurrently, to address challenges associated with the objective function, we propose an optimization strategy that incorporates three objective functions and employs a multistage weight optimization method to improve control performance and ensure output stability.
- p.1 abstract: Finally, the effectiveness of our method is validated through numerical simulations and a case study of an industrial rotary kiln, demonstrating significant improvements in control performance, system stability, and response accuracy.
- p.1 introduction: LARGE time-delay and nonlinearity are prevalent in process industries, such as chemical production, power systems, and metallurgy.
- p.2 introduction: Despite these advancements, integrating DL with traditional control frameworks, such as MPC, remains an emerging field with significant potential for innovation.
- p.2 introduction: Therefore, exploring efficient methods for controlling nonlinear and large time-delay systems is crucial for both theoretical advancement and practical industrial applications.
- p.2 introduction: This study aims to address these challenges by introducing a class of DNNs-MPC approach.
- p.2 introduction: The main contributions of this article are as follows.
- p.3 introduction: The rest of this article is organized as follows. Section II details the research methodology employed. Section III presents experimental results to validate the effectiveness of the proposed approach, followed by a summary. Finally, Section IV concludes this article.
- p.3 method: The DNNs-MPC combines deep neural networks and MPC to model systems and optimize control.
- p.6 method: The detailed execution process of the DNNs-MPC is shown in Algorithm 1.
- p.6 experiments: The efficacy of the algorithm was assessed using key metrics, including mean absolute error (MAE), root mean square error (RMSE), and coefficient of determination (R2) [23], integrated absolute error (IAE), and integrated squared error (ISE) [27].
- p.7 experiments: However, their performance degrades somehow in the presence of noise, especially for PID and NMPC.
- p.7 experiments: Table II shows that when the noise level increases from w(t) ∼ N(0, 0) to w(t) ∼ N(0, 0.1), the ISE and IAE values of all models increase, indicating that noise negatively affects control performance.
- p.9 experiments: Fig. 11 shows that as the reference temperature increases from 600 °C to 620 °C, significant deviations happen in the performance of each MPC algorithm.
- p.10 conclusion: In this research, we have successfully introduced a DNNs-MPC, designed to enhance the control performance of industrial processes with nonlinear dynamics and significant time delays.
- p.10 conclusion: Our method has demonstrated superior predictive accuracy and control effectiveness through extensive numerical simulations and a real-world case study involving an industrial rotary kiln.
- p.10 conclusion: Although our method has exhibited commendable performance, it is sensitive to parameter settings.
- p.10 conclusion: Therefore, future research will focus on developing adaptive algorithms that can dynamically tune MPC parameters based on process feedback.
