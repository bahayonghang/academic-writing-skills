---
key: PQKCZ8X7
title: "Semi-supervised learning for data-driven soft-sensing of biological and chemical processes"
venue: "Chemical Engineering Science"
doi: "10.1016/j.ces.2022.117459"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Methodology` → `3. Case Studies` → `4. Conclusions and Outlook`。前置 `highlights` / `graphical abstract` / `article info` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 MPC/RTO、多速率状态估计、PLS/FDA/ANN/GPR、半监督回归）。Introduction 末无编号贡献列表，有研究范围陈述。Method 为四步评估流程。Experiments 标题为 `3. Case Studies`（Williams-Otto + 生物乙醇）。

## Openers

- abstract: `Continuously operated (bio-)` — "Continuously operated (bio-) chemical processes increasingly suffer from external disturbances, such as feed fluctuations or changes in market conditions."
- introduction: `Continuously operated chemical` — "Continuously operated chemical and bio-chemical processes are subject to various driving forces, which induce fluctuations (Esche and Repke, 2020)."
- method: `A novel, four` — "A novel, four step procedure is proposed to evaluate the capabilities of semi-supervised regression for softsensing in (bio-) chemical plants."
- experiments: `Two (bio-) chemical` — "Two (bio-) chemical processes are used to test the capabilities of the semi-supervised regression framework."
- conclusion: `Constructing soft-sensors for` — "Constructing soft-sensors for (bio-) chemical processes still is an arduous and time-consuming task."

## Gap transitions

- despite (introduction): "Despite large advances in recent years, numerous challenges remain (Alexander et al., 2020)."
- however (introduction): "However, Weigert et al. (2018) previously noted that the made assumptions on measurement frequencies in these works are still quite high."
- to the best of our knowledge (introduction): "To the best of our knowledge, this has not been previously investigated and might open up a host of new possibilities for straightforward construction of soft-sensors for process applications."
- however (abstract): "However, no reliable prediction of process dynamics can be ensured in case of common measurement frequencies for offline quality measurements."

## Hedge verbs

- is proposed / causal / method: "A novel, four step procedure is proposed to evaluate the capabilities of semi-supervised regression for softsensing in (bio-) chemical plants."
- we would like to propose / causal / introduction: "Here, we would like to propose a methodology detailed in Section 2, which allows for a straight forward construction of soft-sensors based on continuous measurement data as well as rarely measured qualities."
- we have shown / associative / conclusion: "With the two case studies of the Williams-Otto and a bioethanol production process, we have shown that even in settings with very few measurements, i.e., every 100 h or every 4 days, predictions of intermediate states is possible with reasonable error."
- can serve / associative / abstract: "The case studies show that semi-supervised regression can serve as a valuable building block in construction of a soft sensor to reliably predict steady state data even in case of very few quality measurements (hourly or daily measurements)."

## Cross-section linkers

- introduction → method: "Here, we would like to propose a methodology detailed in Section 2"
- method → experiments: "Afterwards two case studies are introduced with complex dynamic models serving as ground truth" 后 `3. Case Studies`
- experiments → conclusion: 动态预测分析后 `4. Conclusions and Outlook`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R009 自称：`Here, we would like to propose` / `In the present contribution we have investigated` / `we have shown`

## Candidate phrases

- `Here, we would like to propose a methodology detailed in Section 2` (introduction)
- `A novel, four step procedure is proposed to evaluate the capabilities of semi-supervised regression` (method)
- `In the present contribution we have investigated whether semi-supervised learning can serve as a facilitator` (conclusion)
- `The case studies show that semi-supervised regression can serve as a valuable building block` (abstract)

## House style

自称 `we would like to propose` / `In the present contribution we have investigated` / `we have shown`。第一人称复数为主。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Continuously operated (bio-) chemical processes increasingly suffer from external disturbances, such as feed fluctuations or changes in market conditions.
- abstract: Semi-supervised regression is a possible building block and method from machine learning to construct soft-sensors for such infrequently measured states.
- abstract: The case studies show that semi-supervised regression can serve as a valuable building block in construction of a soft sensor to reliably predict steady state data even in case of very few quality measurements (hourly or daily measurements).
- abstract: However, no reliable prediction of process dynamics can be ensured in case of common measurement frequencies for offline quality measurements.
- introduction: Continuously operated chemical and bio-chemical processes are subject to various driving forces, which induce fluctuations (Esche and Repke, 2020).
- introduction: Despite large advances in recent years, numerous challenges remain (Alexander et al., 2020).
- introduction: However, Weigert et al. (2018) previously noted that the made assumptions on measurement frequencies in these works are still quite high.
- introduction: Here, we would like to propose a methodology detailed in Section 2, which allows for a straight forward construction of soft-sensors based on continuous measurement data as well as rarely measured qualities.
- introduction: To the best of our knowledge, this has not been previously investigated and might open up a host of new possibilities for straightforward construction of soft-sensors for process applications.
- method: A novel, four step procedure is proposed to evaluate the capabilities of semi-supervised regression for softsensing in (bio-) chemical plants.
- experiments: Two (bio-) chemical processes are used to test the capabilities of the semi-supervised regression framework.
- conclusion: Constructing soft-sensors for (bio-) chemical processes still is an arduous and time-consuming task.
- conclusion: In the present contribution we have investigated whether semi-supervised learning can serve as a facilitator for improved prediction of process states, which are seldom measured.
- conclusion: With the two case studies of the Williams-Otto and a bioethanol production process, we have shown that even in settings with very few measurements, i.e., every 100 h or every 4 days, predictions of intermediate states is possible with reasonable error.
