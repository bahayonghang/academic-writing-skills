---
key: KUMVDDYB
title: "Predictive Monitoring of Industrial Processes and Quality Indices via Joint Training of Soft Sensor and Time-Series Forecasting"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2026.3664090"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED FRAMEWORK` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评机制模型、软测量、Transformer/Informer、小波与 MambaMoE）。Introduction 末为编号贡献，无节序路标句。Method 拆成 Preliminaries + Proposed Framework。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `Predictive monitoring of` — "Predictive monitoring of industrial processes and quality indices, particularly free calcium oxide (f-CaO) in cement production, is of critical importance." (p.1)
- introduction: `ENSURING stable quality` — "ENSURING stable quality and optimizing energy consumption in cement clinker production hinges on the predictive monitoring of free calcium oxide (f-CaO) [1], [2]." (p.1；栏首掉字)
- method: `The proposed framework` — "The proposed framework comprises three components: a soft sensor model, a multitask time-series forecasting model, and a joint training strategy that synergistically co-optimizes them." (p.3, III)
- experiments: `We evaluated the` — "We evaluated the proposed method on a real-world industrial dataset collected at the Jidong cement plant in Yangquan, Shanxi, over an approximately two-year period." (p.7)
- conclusion: `This article has` — "This article has presented a joint training framework to address the critical challenge of predictive f-CaO monitoring under asynchronous data sampling conditions." (p.11)

## Gap transitions

- however (abstract): "However, it is significantly constrained by the asynchronous sampling between high-frequency process data and delayed laboratory quality measurements." (p.1)
- to address (abstract): "To address this challenge, this article proposes a joint modeling framework that collaboratively optimizes a multiscale attention Kolmogorov–Arnold network (MSAKAN) soft sensor and a MambaMoE time-series forecasting model." (p.1)
- despite (introduction): "Despite these significant advances, current deep-learning-based soft sensors still face persistent limitations that hinder their full potential in dynamic industrial environments." (p.1)
- however (experiments): "However, this enhanced focus on quality prediction introduces a clear tradeoff." (p.9)
- despite (conclusion): "Despite these achievements, we observe a characteristic tradeoff of MTL: the specialization required for accurate quality prediction induces a slight degradation in the generalized forecasting performance for raw process variables." (p.11)

## Hedge verbs

- propose / causal / abstract: "this article proposes a joint modeling framework"
- demonstrate / causal / abstract: "Experimental results on a real-world cement plant dataset demonstrate the effectiveness of the proposed framework."
- show / causal / abstract: "These results confirm the synergy of the proposed approach and show substantial performance gains over state-of-the-art baselines."
- indicate / associative / experiments: "These results indicate a complementary effect between multiscale feature extraction and advanced nonlinear mapping"

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. PRELIMINARIES`，无 `organized as follows` (p.2)
- method → experiments: Proposed Framework 结束后 `IV. CASE STUDY` (p.7)
- experiments → conclusion: 消融后 `V. CONCLUSION` (p.11)

## Candidate rules

- R002 Related Work 并入 Introduction。
- R004 贡献列表变体：`The primary contributions of this work are presented as follows.`
- R005 结论 `Despite these achievements` + `Future work will investigate`。
- R009 摘要用 `this article proposes` 点名框架。

## Candidate phrases

- `this article proposes` (abstract)
- `The primary contributions of this work are presented as follows.` (introduction)
- `This article has presented` (conclusion)
- `Future work will investigate` (conclusion)

## House style

自称 `this article` / `this work` / `we propose` / `we introduce`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Predictive monitoring of industrial processes and quality indices, particularly free calcium oxide (f-CaO) in cement production, is of critical importance.
- p.1 abstract: However, it is significantly constrained by the asynchronous sampling between high-frequency process data and delayed laboratory quality measurements.
- p.1 abstract: To address this challenge, this article proposes a joint modeling framework that collaboratively optimizes a multiscale attention Kolmogorov–Arnold network (MSAKAN) soft sensor and a MambaMoE time-series forecasting model.
- p.1 abstract: Experimental results on a real-world cement plant dataset demonstrate the effectiveness of the proposed framework.
- p.1 abstract: These results confirm the synergy of the proposed approach and show substantial performance gains over state-of-the-art baselines.
- p.1 introduction: ENSURING stable quality and optimizing energy consumption in cement clinker production hinges on the predictive monitoring of free calcium oxide (f-CaO) [1], [2].
- p.1 introduction: Despite these significant advances, current deep-learning-based soft sensors still face persistent limitations that hinder their full potential in dynamic industrial environments.
- p.2 introduction: The primary contributions of this work are presented as follows.
- p.3 method: The proposed framework comprises three components: a soft sensor model, a multitask time-series forecasting model, and a joint training strategy that synergistically co-optimizes them.
- p.7 experiments: We evaluated the proposed method on a real-world industrial dataset collected at the Jidong cement plant in Yangquan, Shanxi, over an approximately two-year period.
- p.9 experiments: However, this enhanced focus on quality prediction introduces a clear tradeoff.
- p.10 experiments: These results indicate a complementary effect between multiscale feature extraction and advanced nonlinear mapping, which is important for modeling complex industrial processes.
- p.11 conclusion: This article has presented a joint training framework to address the critical challenge of predictive f-CaO monitoring under asynchronous data sampling conditions.
- p.11 conclusion: Despite these achievements, we observe a characteristic tradeoff of MTL: the specialization required for accurate quality prediction induces a slight degradation in the generalized forecasting performance for raw process variables.
- p.11 conclusion: Future work will investigate advanced multitask optimization techniques, such as task-specific gating mechanisms and dynamic uncertainty-based loss weighting, to better balance targeted quality accuracy against overall forecasting performance.
