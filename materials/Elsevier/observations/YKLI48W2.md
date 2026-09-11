---
key: YKLI48W2
title: "Multi-parameter co-optimization for NOx emissions control from waste incinerators based on data-driven model and improved particle swarm optimization"
venue: "Energy"
doi: "10.1016/j.energy.2024.132477"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Object description and data preprocessing` → `3. Methodology` → `4. Results and discussion` → `5. Conclusions`。前置 `ABSTRACT` 与 `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 ANN/SVM/AE/LSTM/Bi-LSTM 预测与 GA/PSO 燃烧优化）。Introduction 编号不足 `(1)` / `(2)` 后给出目标，无 `remainder` 路标。Method 含目标函数、SAE-(Bi-LSTM)、改进 PSO。Experiments 标题为 `4. Results and discussion`（NOx 软测量 + 多参数协同优化）。

## Openers

- abstract: `The waste incineration` — "The waste incineration process is complex and variable, posing a great challenge for precise NOx emissions control based on selective non-catalytic reduction (SNCR)."
- introduction: `Municipal solid waste` — "Municipal solid waste incineration (MSWI) has become the mainstream waste treatment technology, owing to its capacity to reduce waste volume and generate electricity."
- method: `This section demonstrates` — "This section demonstrates the strategy for optimizing and controlling NOx emissions in the waste incineration process, as shown in Fig. 2."
- experiments: `The NOx emissions soft` — "The NOx emissions soft sensor model is constructed using the SAE-(Bi-LSTM) model, as mentioned in subsection 3.2."
- conclusion: `This study presents` — "This study presents a co-optimization strategy for combustion and denitrification parameters of the waste incineration process."

## Gap transitions

- therefore (abstract): "Therefore, we propose a combustion (air flow) and denitrification (ammonia flow) parameters co-optimization method to achieve safe, economic, and environmentally friendly control of NOx emissions from waste incineration processes."
- therefore (introduction): "Therefore, synergistic optimization of combustion and denitrification parameters is desired to achieve the precise and economical control of NOx emissions."
- although (introduction): "Although the above studies have achieved some success, there are some shortcomings in the research of NOx emissions optimization."
- however (introduction): "However, combustion optimization alone may often not meet environmental NOx emissions standards."

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a combustion (air flow) and denitrification (ammonia flow) parameters co-optimization method"; "This paper introduces the SAE-(Bi-LSTM) model"
- can / speculative / abstract: "the proposed co-optimization method can control NOx near the target value while saving ammonia consumption"
- demonstrate / associative / results: "These results demonstrate that optimizing air flow and ammonia flow can effectively control NOx emissions"
- presents / causal / conclusion: "This study presents a co-optimization strategy"
- show / associative / conclusion: "The results show that they are in good agreement with the actual values."

## Cross-section linkers

- introduction → object: 目标陈述后直接 `2. Object description and data preprocessing`
- object → method: 特征选择后 `3. Methodology`
- method → experiments: 优化步骤表后 `4. Results and discussion`
- experiments → conclusion: 不确定性分析后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R004 编号不足与贡献：Introduction 不足 `(1)` / `(2)`；结论贡献 `(1)` / `(2)` / `(3)`
- R017 Introduction 末可无节序路标，直接 Object/Method。
- R009 自称：`we propose` / `This paper introduces` / `This study presents`

## Candidate phrases

- `Therefore, we propose a combustion (air flow) and denitrification (ammonia flow) parameters co-optimization method` (abstract)
- `This paper introduces the SAE-(Bi-LSTM) model` (introduction)
- `This study presents a co-optimization strategy` (conclusion)
- `The main contributions are as follows` (conclusion)
- `The results show that the proposed optimization method can control NOx near the target value while saving ammonia consumption` (conclusion)

## House style

自称 `we propose` / `This paper introduces` / `This study presents`。第一人称复数与 `this paper` / `this study` 并用。进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 开篇。

## Quotes

- abstract: The waste incineration process is complex and variable, posing a great challenge for precise NOx emissions control based on selective non-catalytic reduction (SNCR).
- abstract: Therefore, we propose a combustion (air flow) and denitrification (ammonia flow) parameters co-optimization method to achieve safe, economic, and environmentally friendly control of NOx emissions from waste incineration processes.
- abstract: Simultaneously, there is a significant reduction in the standard deviation of fluctuations, decreasing from 9.39 % to 1.35 %, and ammonia consumption decreased by 4.43 %.
- introduction: Municipal solid waste incineration (MSWI) has become the mainstream waste treatment technology, owing to its capacity to reduce waste volume and generate electricity.
- introduction: Therefore, synergistic optimization of combustion and denitrification parameters is desired to achieve the precise and economical control of NOx emissions.
- introduction: This study aims to develop a co-optimization method for air flow and ammonia flow to achieve precise and economic NOx emissions control.
- experiments: The SAE-(Bi-LSTM) model exhibits superior prediction performance with MAPE, RMSE, and MAE for the training set at 1.40 %, 1.98 mg/m3, and 1.61 mg/m3, respectively.
- experiments: These results demonstrate that optimizing air flow and ammonia flow can effectively control NOx emissions at approximately 120 mg/m3 while reducing ammonia consumption by 4.43 %.
- conclusion: This study presents a co-optimization strategy for combustion and denitrification parameters of the waste incineration process.
- conclusion: The optimization case results demonstrate that the proposed strategy effectively controls NOx emissions at the target value of 120 mg/m3 and reduces ammonia consumption by 4.43 %.
- conclusion: The results show that the proposed optimization method can control NOx near the target value while saving ammonia consumption.
