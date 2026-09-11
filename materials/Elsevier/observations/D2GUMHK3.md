---
key: D2GUMHK3
title: "Predictive control research for cement burning system using two-cycle coupling optimization"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2021.116259"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Problem analysis` → `3` 预测控制 → `4. Experiment` → `5. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 RTO/MPC、水泥数据模型、MOO 与 Pareto、闭环校正）。Introduction 末有编号贡献 `(1)` `(2)` + 节序路标（`Part II`–`Part V`）。Method 拆成问题分析与控制节。Experiments 标题为 `4. Experiment`。

## Openers

- abstract: `A stable, high` — "A stable, high quality cement burning system producing clinker with low energy consumption is important for cement company."
- introduction: `China's cement industry` — "China's cement industry is characterized by high energy consumption and poor product quality (Shen et al., 2017)."
- method: `In this section` — "In this section, the process flow of a cement combustion system is analyzed to derive how the production optimization objectives should be optimized with respect to the important controlled variables in the production process." (s.2)
- experiments: `In this section` — "In this section, the real historical data obtained with the Tangxian Jidong cement is used as the training set data and test set data of convolutional neural network to verify the accuracy of the model."
- conclusion: `In this paper` — "In this paper, a multi-objective optimal predictive control model for cement burning system was proposed to address the problems of complex cement burning process, high volatility of each controlled variable by manual regulation, low quality of cement clinker produced by manual regulation and high energy cost consumed in cement burning system."

## Gap transitions

- however (abstract): "However, in the actual operation of the combustion system, there are contradictory indicators such as electricity consumption, coal consumption and clinker quality that are difficult to be jointly optimized"
- in order to (abstract, introduction): "In order to solve the above problems, a multi-objective optimal predictive control model is proposed in this paper."
- nevertheless (introduction): "Nevertheless, the inherent problem that static open-loop optimization used by RTO has poor robustness is not solved."
- in summary (introduction): "In summary, this paper investigates the optimization of the operation of cement combustion systems in a dynamic environment based on the production requirements of the cement industry."

## Hedge verbs

- is proposed / causal / abstract: "a multi-objective optimal predictive control model is proposed in this paper"
- show / associative / abstract: "Experimental results show that the method described in this paper reduces the content of free calcium oxide after cement combustion"
- demonstrated / causal / conclusion: "The experimental results demonstrated that the method described in this paper ensures the improvement of cement clinker quality while reducing the production energy cost of the cement burning system."

## Cross-section linkers

- introduction → method: "The remainder of the paper is organized as follows: Part II is the problem analysis"
- method → experiments: "Part IV presents an experimental study of the described predictive control."
- experiments → conclusion: 成本对照表后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remainder of the paper is organized as follows`（Part II–V）
- R004 编号贡献：`its main innovations are summarized as follows:`
- R009 自称：`is proposed in this paper` / `the method described in this paper`

## Candidate phrases

- `In order to solve the above problems, a multi-objective optimal predictive control model is proposed in this paper` (abstract)
- `its main innovations are summarized as follows:` (introduction)
- `The remainder of the paper is organized as follows` (introduction)
- `the method described in this paper` (abstract, experiments, conclusion)
- `In this paper, a multi-objective optimal predictive control model ... was proposed` (conclusion)

## House style

自称 `is proposed in this paper` / `the method described in this paper` / `In this paper, ... was proposed`。少见 `we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: A stable, high quality cement burning system producing clinker with low energy consumption is important for cement company.
- abstract: In order to solve the above problems, a multi-objective optimal predictive control model is proposed in this paper.
- abstract: Experimental results show that the method described in this paper reduces the content of free calcium oxide after cement combustion, thus improving the quality of cement clinker, while reducing the fluctuations of the control variables in each production process and improving the stability of the combustion system.
- introduction: China's cement industry is characterized by high energy consumption and poor product quality (Shen et al., 2017).
- introduction: In summary, this paper investigates the optimization of the operation of cement combustion systems in a dynamic environment based on the production requirements of the cement industry.
- introduction: The remainder of the paper is organized as follows: Part II is the problem analysis, and by analyzing the process flow and process control of the cement combustion system, a convolutional neural network predictive model of energy consumption and free calcium oxide is established, based on which a multi-conflict objective optimization model in a high-dimensional constraint space is proposed.
- experiments: In this section, the real historical data obtained with the Tangxian Jidong cement is used as the training set data and test set data of convolutional neural network to verify the accuracy of the model.
- experiments: After reaching a certain optimization time, its cost reduction efficiency stops increasing and reaches a stable value of 10% energy cost reduction.
- conclusion: In this paper, a multi-objective optimal predictive control model for cement burning system was proposed to address the problems of complex cement burning process, high volatility of each controlled variable by manual regulation, low quality of cement clinker produced by manual regulation and high energy cost consumed in cement burning system.
- conclusion: The experimental results demonstrated that the method described in this paper ensures the improvement of cement clinker quality while reducing the production energy cost of the cement burning system.
