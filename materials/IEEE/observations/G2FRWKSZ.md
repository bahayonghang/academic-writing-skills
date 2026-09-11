---
key: G2FRWKSZ
title: "Probabilistic Load Forecasting Based on Adaptive Online Learning"
venue: "IEEE Transactions on Power Systems"
doi: "10.1109/TPWRS.2021.3050837"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-4,8-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. MODELS AND THEORETICAL RESULTS` → `IV` 实现（离线 / 在线对比） → `V` 实验对比 → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段分统计 / 机器学习 / 组合预测，再评 GP、QR 与在线单值方法）。Introduction 末有 `The rest of this paper is organized as follows` 路标，指向 Section II–VI。Method 含 HMM、定理与递推更新。Experiments 用多区域数据集对比 RMSE / MAPE / pinball / ECE。

## Openers

- abstract: `Load forecasting is` — "Load forecasting is crucial for multiple energy management tasks such as scheduling generation capacity, planning supply and demand, and minimizing energy trade costs." (p.1)
- introduction: `LOAD FORECASTING is` — "LOAD FORECASTING is crucial for multiple energy management tasks such as scheduling generation capacity, planning supply and demand, and minimizing energy trade costs [1]–[4]." (p.1；栏首掉字)
- method: `This section first` — "This section first describes the HMM that models loads and observations, we then develop the techniques for online learning and probabilistic forecasting." (p.3, III)
- experiments: `APLF method is` — "APLF method is compared with 11 state-of-the-art techniques based on statistical methods, machine learning, and weighted combination of several forecasts." (p.8, V)
- conclusion: `The paper proposes` — "The paper proposes techniques for adaptive probabilistic load forecasting (APLF) that can adapt to changes in consumption patterns and assess load uncertainties." (p.9)

## Gap transitions

- however (abstract): "However, such techniques cannot assess intrinsic uncertainties in load demand, and cannot capture dynamic changes in consumption patterns." (p.1)
- to address (abstract): "To address these problems, this paper presents a method for probabilistic load forecasting based on the adaptive online learning of hidden Markov models." (p.1)
- on the other hand (introduction): "On the other hand, probabilistic forecasts can evaluate load uncertainty and are essential for optimal stochastic decision making (e.g., unit commitment [19]) [20] while online learning is necessary to harness dynamic changes in consumption patterns [21]." (p.1)
- while (introduction): "Existing techniques that obtain probabilistic forecasts are based on offline learning, while those based on online learning obtain single-value forecasts." (p.2)

## Hedge verbs

- present / causal / abstract: "this paper presents a method for probabilistic load forecasting"
- propose / causal / abstract, conclusion: "We propose learning and forecasting techniques with theoretical guarantees"; "The paper proposes techniques for adaptive probabilistic load forecasting"
- develop / causal / abstract, conclusion: "we develop adaptive online learning techniques that update model parameters recursively"; "We developed online learning techniques that update model parameters"
- show / causal / abstract, experiments: "The results show that the proposed method can significantly improve the performance of existing techniques"; "Table I, and Figures 6 and 7 show that the proposed APLF method achieves high accuracies"
- can improve / causal / conclusion: "the proposed method can improve forecasting performance in a wide range of scenarios"

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows. Section II describes the problem of load forecasting and introduces the performance metrics. In Section III, we present the theoretical results for APLF learning and prediction. Section IV compares the procedures of offline learning and online learning, and describes in detail the implementation of APLF. The performance of APLF and existing techniques is compared in Section V under multiple scenarios. Finally, Section VI draws the conclusions." (p.2)
- method → experiments: 实现细节后进入 Section V 多场景对比 (p.8)
- experiments → conclusion: 训练长度分析后 `VI. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `However, such techniques cannot` 收缺口，再 `To address these problems, this paper presents`。
- R002 Introduction 无独立 Related Work，已有方法按统计 / 机器学习 / 组合预测分组。
- R003 贡献用项目符号 `• We model … • We develop …`。
- R004 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–VI。
- R005 Conclusion 用 `The paper proposes techniques for` 收回，再用 `As shown in the paper, the proposed method can improve`。

## Candidate phrases

- `To address these problems, this paper presents a method for` (abstract)
- `We propose learning and forecasting techniques with theoretical guarantees` (abstract)
- `The rest of this paper is organized as follows.` (introduction)
- `APLF method is compared with 11 state-of-the-art techniques` (experiments)
- `The paper proposes techniques for adaptive probabilistic load forecasting (APLF) that` (conclusion)

## House style

自称 `this paper` / `The paper proposes` / `We propose` / `the proposed method` / `APLF method`。未见 `Here we`、`In this article`。`this paper presents` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Load forecasting is crucial for multiple energy management tasks such as scheduling generation capacity, planning supply and demand, and minimizing energy trade costs.
- p.1 abstract: However, such techniques cannot assess intrinsic uncertainties in load demand, and cannot capture dynamic changes in consumption patterns.
- p.1 abstract: To address these problems, this paper presents a method for probabilistic load forecasting based on the adaptive online learning of hidden Markov models.
- p.1 abstract: We propose learning and forecasting techniques with theoretical guarantees, and experimentally assess their performance in multiple scenarios.
- p.1 abstract: The results show that the proposed method can significantly improve the performance of existing techniques for a wide range of scenarios.
- p.1 introduction: LOAD FORECASTING is crucial for multiple energy management tasks such as scheduling generation capacity, planning supply and demand, and minimizing energy trade costs [1]–[4].
- p.1 introduction: On the other hand, probabilistic forecasts can evaluate load uncertainty and are essential for optimal stochastic decision making (e.g., unit commitment [19]) [20] while online learning is necessary to harness dynamic changes in consumption patterns [21].
- p.2 introduction: Existing techniques that obtain probabilistic forecasts are based on offline learning, while those based on online learning obtain single-value forecasts.
- p.2 introduction: The rest of this paper is organized as follows. Section II describes the problem of load forecasting and introduces the performance metrics. In Section III, we present the theoretical results for APLF learning and prediction. Section IV compares the procedures of offline learning and online learning, and describes in detail the implementation of APLF. The performance of APLF and existing techniques is compared in Section V under multiple scenarios. Finally, Section VI draws the conclusions.
- p.3 method: This section first describes the HMM that models loads and observations, we then develop the techniques for online learning and probabilistic forecasting.
- p.8 experiments: APLF method is compared with 11 state-of-the-art techniques based on statistical methods, machine learning, and weighted combination of several forecasts.
- p.8 experiments: Table I, and Figures 6 and 7 show that the proposed APLF method achieves high accuracies in comparison with existing techniques in every dataset studied.
- p.9 experiments: Numerical results confirm that APLF better captures dynamic changes in consumption patterns than existing methods.
- p.9 conclusion: The paper proposes techniques for adaptive probabilistic load forecasting (APLF) that can adapt to changes in consumption patterns and assess load uncertainties.
- p.9 conclusion: The experimental results show the performance improvement of APLF method in terms of prediction errors and probabilistic forecasts.
- p.9 conclusion: As shown in the paper, the proposed method can improve forecasting performance in a wide range of scenarios using efficient and flexible algorithms for adaptive online learning.
