---
key: JSB9VBUA
title: "Data Science and Model Predictive Control: A survey of recent advances on data-driven MPC algorithms"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2024.103327"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,13-15"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

Review。数字节：`1. Introduction` → `2. Category A: Adaptive algorithms` → `3. Category B: Machine learning schemes` → `4. Category C: Behavioural/trajectory-based formulations` → `5. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`，文首标 `Review`。无独立 Related Work 节；文献按三类算法分节综述。`related_work=inlined`（Introduction 中段模型辨识、自适应、强化学习、行为理论）。Introduction 末给出三类分支与范围 Remark。无 Experiments 节。

## Openers

- abstract: `Model Predictive Control` — "Model Predictive Control (MPC) is an established control framework, based on the solution of an optimisation problem to determine the (optimal) control action at each discrete-time sample."
- introduction: `Dating from the` — "Dating from the original algorithms proposed from the process industry in the 80's, e.g. [1,2], Model Predictive Control (MPC) has since become a widely used control technique for the regulation of constrained systems [3]."
- method: `Even though these` — "Even though these data-driven MPC schemes based on trajectory features have been very extensively discussed over the last few years, we offer, next, some general perspectives on these methods, taking into account the previous discussions." (s.4.3 讨论开篇)
- experiments: （综述无实验节）
- conclusion: `In this work` — "In this work, we reviewed the current relevant literature available regarding data-driven MPC algorithms."

## Gap transitions

- nevertheless (abstract): "Nevertheless, identifying good, trustworthy models for complex systems is a task heavily affected by uncertainties."
- as of this (abstract): "As of this, developing MPC algorithms directly from data has recently received a considerable amount of attention over the last couple of years."
- nevertheless (introduction): "Nevertheless, in the case of system with complex dynamics and inaccessible variables, obtaining a trustworthy model is costly and ponderous task, affected by uncertainties and disturbances, as warns De Persis and Tesi [11], Bisoffi et al. [12] and Steentjes et al. [13]."
- despite (introduction): "Despite the growing enthusiasm on such data-driven MPC schemes (as indicates Fig. 2), no study has formally discussed and compared the advantages and deficiencies of the available approaches, up to our best knowledge."

## Hedge verbs

- review / causal / abstract, conclusion: "In this work, we review the available data-based MPC formulations"; "we reviewed the current relevant literature"
- highlight / associative / introduction: "Accordingly, the main contribution of this work is to survey and review the current of body of research on the topic"
- indicate / associative / conclusion: "Many results indicate interesting performances of these adaptive schemes"

## Cross-section linkers

- introduction → categories: "we examine algorithms that are categorised along the three following branches, as indicates Fig. 3"
- category C → conclusion: 行为方法讨论后 `5. Conclusions`
- conclusion 内三类回顾：`First, we highlight` / `We also stress` / `Finally, we discussed`

## Candidate rules

- R002 Related Work 并入 Introduction，综述正文按算法类别分节。
- R003 无标准 remainder 路标；改用 Fig. 3 三类分支。
- R009 自称：`In this work, we review` / `the main contribution of this work is`

## Candidate phrases

- `In this work, we review` (abstract)
- `up to our best knowledge` (introduction)
- `the main contribution of this work is to survey and review` (introduction)
- `In this work, we reviewed` (conclusion)
- `Our aim in this work was to` (conclusion)

## House style

自称 `In this work, we review` / `we surveyed` / `we discuss` / `we highlight`。第一人称复数用于综述立场。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Model Predictive Control (MPC) is an established control framework, based on the solution of an optimisation problem to determine the (optimal) control action at each discrete-time sample.
- abstract: Nevertheless, identifying good, trustworthy models for complex systems is a task heavily affected by uncertainties.
- abstract: In this work, we review the available data-based MPC formulations, which range from reinforcement learning schemes, adaptive controllers, and novel solutions based on behavioural theory and trajectory representations.
- introduction: Dating from the original algorithms proposed from the process industry in the 80's, e.g. [1,2], Model Predictive Control (MPC) has since become a widely used control technique for the regulation of constrained systems [3].
- introduction: Nevertheless, in the case of system with complex dynamics and inaccessible variables, obtaining a trustworthy model is costly and ponderous task, affected by uncertainties and disturbances, as warns De Persis and Tesi [11], Bisoffi et al. [12] and Steentjes et al. [13].
- introduction: Despite the growing enthusiasm on such data-driven MPC schemes (as indicates Fig. 2), no study has formally discussed and compared the advantages and deficiencies of the available approaches, up to our best knowledge.
- introduction: Accordingly, the main contribution of this work is to survey and review the current of body of research on the topic, indicating fundamental connections between the available algorithms.
- conclusion: In this work, we reviewed the current relevant literature available regarding data-driven MPC algorithms.
- conclusion: Our aim in this work was to provide a better comprehension of the state-of-the art on the analysed topic, drawing conclusions on the capabilities and deficiencies of the possible design alternatives.
- conclusion: First, we highlight that the available adaptive algorithms often require an initial model that is a sufficiently fair description of the process, in such a way that stability can be ensured despite the online adaptation procedure.
