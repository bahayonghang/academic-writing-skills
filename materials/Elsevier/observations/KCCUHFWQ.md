---
key: KCCUHFWQ
title: "Methods for automatic control, observation, and optimization in mineral processing plants"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2010.10.016"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节（Review）：`1. Introduction` → `2. Processes and control objectives in the mineral processing industry` → `3. Measurement processing block` → `4. Controllers` → `5. Optimizers` → `6. Conclusion`。前置 `abstract` / `Keywords` 与 Contents 目录。无独立 Related Work。`related_work=inlined`（Introduction 声明非穷尽综述，文献评述分散在各节案例）。Introduction 末有节序路标。Method/Experiments 由测量处理、控制器与优化器三块承担，无独立实验节。

## Openers

- abstract: `For controlling strongly` — "For controlling strongly disturbed, poorly modeled, and difficult to measure processes, such as those involved in the mineral processing industry, the peripheral tools of the control loop (fault detection and isolation system, data reconciliation procedure, observers, soft sensors, optimizers, model parameter tuners) are as important as the controller itself."
- introduction: `This document provides` — "This document provides an overview on the control methods that are available or practically used in mineral processing (MP) plants."
- method: `The tools involved` — "The tools involved in any kind of control loop are designed based on process models." (s.2.5)
- experiments: `As said above` — "As said above, with respect to the economic performance of a MP plant, the controller performance is most probably not as important as the right selection of the set-points." (s.5 Optimizers)
- conclusion: `This paper aimed` — "This paper aimed at describing the basic elements comprised in generalized control loops of mineral processing plants."

## Gap transitions

- although (introduction): "Although the presentation scope is quite large, a limited number of references have been included."
- however (introduction): "However, this kind of plant-wide objective is most of the time not considered, because of the lack of fresh ore mineralogy characterization, and also the difficulty to model size distribution impact over the separation process performance."
- alternatively (introduction): "Alternatively, the plant control objective can be formulated as an objective function to be optimized."
- nevertheless (conclusion): "Nevertheless, control approaches are more important than tools alone."

## Hedge verbs

- describe / associative / abstract, conclusion: "The paper briefly describes each element of this generalized control loop"; "This paper aimed at describing"
- provide / associative / introduction: "This document provides an overview on the control methods"
- may / speculative / section 5, conclusion: "the optimizer that may change the operating set-points"; "the correct adaptation of operating set-points ... may bring very significant improvements"
- should / speculative / introduction: "Product fineness should rather be changed as a function of the raw ore property"
- underline / associative / introduction: "it should be underlined that this proposed scheme, where control and optimization are separated, is a possible architecture"

## Cross-section linkers

- introduction → method: "At first, a brief description of the chain of processes involved in MP plants will be presented. ... Methods such as soft sensors, data reconciliation, fault detection, and feature extraction from images will be presented in the data processing section. An overview of the most common linear control methods will follow ... Finally the main features of the optimization block ... will be presented."
- method → experiments: 建模段落后进入测量处理 / 控制器 / 优化器
- experiments → conclusion: 浸出优化例后 `6. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction 与各技术节（综述体）。
- R003 节序路标：`At first, a brief description ... will be presented`
- R014 综述自称 `This document provides an overview` / `This paper aimed at describing`
- R015 结论用编号主消息：`The three main messages that were delivered are`

## Candidate phrases

- `The paper briefly describes each element of this generalized control loop` (abstract)
- `This document provides an overview on` (introduction)
- `This paper aimed at describing` (conclusion)
- `The three main messages that were delivered are` (conclusion)
- `Success in automation application relies not only on tools, but also on` (conclusion)

## House style

自称 `This document` / `The paper` / `This paper`。未见 `Here we`。`This paper` 进 phrase_bank，不进 anti_ai_patterns。综述体少用 `we propose`。

## Quotes

- abstract: For controlling strongly disturbed, poorly modeled, and difficult to measure processes, such as those involved in the mineral processing industry, the peripheral tools of the control loop (fault detection and isolation system, data reconciliation procedure, observers, soft sensors, optimizers, model parameter tuners) are as important as the controller itself.
- abstract: The paper briefly describes each element of this generalized control loop, while putting emphasis on mineral processing specific cases.
- introduction: This document provides an overview on the control methods that are available or practically used in mineral processing (MP) plants.
- introduction: It is partly an updated version based on a survey conducted a decade ago [1], but it does not aim at delivering an exhaustive literature survey.
- introduction: Alternatively, the plant control objective can be formulated as an objective function to be optimized.
- method: The tools involved in any kind of control loop are designed based on process models.
- experiments: As said above, with respect to the economic performance of a MP plant, the controller performance is most probably not as important as the right selection of the set-points.
- conclusion: This paper aimed at describing the basic elements comprised in generalized control loops of mineral processing plants.
- conclusion: The three main messages that were delivered are: (1) the controllers and optimizers are efficient when the observers have been carefully designed
- conclusion: Nevertheless, control approaches are more important than tools alone.
