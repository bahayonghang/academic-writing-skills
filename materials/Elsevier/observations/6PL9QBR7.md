---
key: 6PL9QBR7
title: "A modeling method of wide random forest multi-output soft sensor with attention mechanism for quality prediction of complex industrial processes"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2023.102255"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-10"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

前置 `Full length article` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction` → `2. A review of existing methods` → `3. BRF soft sensor algorithm based on attention mechanism` → `4. Industrial case study` → `5. Discussion of results`。独立 Related Work（`2. A review of existing methods`）。`related_work=independent`。Introduction 末有编号贡献。Experiments 标题为 `Industrial case study`。无单独 `Conclusion` 节，收束在 `5. Discussion of results`。

## Openers

- abstract: `Complex industrial production` — "Complex industrial production processes often involve multiple product quality indicators that are interrelated."
- introduction: `With the ongoing` — "With the ongoing innovation and progress of modern industrial technology, the requirements for product quality in various industries have been increasing."
- related_work: `In recent years` — "In recent years, the rise of deep learning technology has brought new opportunities and challenges to soft sensor modeling."
- method: `For complex industrial` — "For complex industrial production processes, there is not always consistency in the relationship between various auxiliary variables and the variables to be measured."
- experiments: `Semiconductor silicon single` — "Semiconductor silicon single crystal (SSSC) is an important raw material for the development of the integrated circuit (IC) industry."
- conclusion: `The proposed method` — "The proposed method of multi-output soft sensor modeling based on attention mechanism in this paper has been effectively validated in the experiment of Cz SSSC growth."

## Gap transitions

- however (introduction): "However, in practical production processes, there are often quality variables that are difficult to measure directly."
- in order to (abstract): "In order to fully capture the complex relationship between measurable variables and difficult-to-measure quality variables, and achieve accurate prediction of multiple output variables to meet the needs of practical industrial sites, this paper proposes a broad random forest-based multi-output soft sensor modeling method"
- therefore (method): "Therefore, this paper proposes a dynamic attention mechanism strategy, which aims to calculate the dynamic attention scores of input process variables in real-time."
- despite (related work): "Despite the significant achievements of deep learning in many fields, it also faces some challenges."

## Hedge verbs

- propose / causal / abstract, method: "this paper proposes"
- demonstrate / causal / abstract, experiments: "the proposed method demonstrates higher prediction accuracy"
- indicate / associative / experiments: "The results in Fig. 5 indicate that there is a strong correlation between the process input variables determined by expert experience and process mechanism analysis and the output quality variables."

## Cross-section linkers

- introduction → related work: 贡献列表后 `2. A review of existing methods`
- related work → method: 综述收束后 `3. BRF soft sensor algorithm based on attention mechanism`
- method → experiments: 伪代码后 `4. Industrial case study`
- experiments → conclusion: 对比结果后 `5. Discussion of results`

## Candidate rules

- R001 独立 Related Work（`2. A review of existing methods`）。
- R004 编号贡献：`The main contributions of this paper are as follows`
- R009 自称：`this paper proposes` / `this paper has been effectively validated`

## Candidate phrases

- `this paper proposes a broad random forest-based multi-output soft sensor modeling method` (abstract)
- `The main contributions of this paper are as follows` (introduction)
- `Therefore, this paper proposes a dynamic attention mechanism strategy` (method)
- `To validate the reliability of the proposed method, it was applied to real industrial cases.` (abstract)
- `In conclusion, the proposed method of multi-output soft sensor modeling based on attention mechanism provides a new solution` (discussion)

## House style

自称 `this paper proposes` / `this study is based on` / `the proposed method`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Complex industrial production processes often involve multiple product quality indicators that are interrelated.
- abstract: In order to fully capture the complex relationship between measurable variables and difficult-to-measure quality variables, and achieve accurate prediction of multiple output variables to meet the needs of practical industrial sites, this paper proposes a broad random forest-based multi-output soft sensor modeling method based on the idea of attention mechanism derived from the concept of broad learning systems.
- abstract: To validate the reliability of the proposed method, it was applied to real industrial cases.
- abstract: The results demonstrated that the multi-output quality variable prediction performance of the proposed soft sensor outperforms existing soft sensors in terms of prediction accuracy.
- introduction: With the ongoing innovation and progress of modern industrial technology, the requirements for product quality in various industries have been increasing.
- introduction: The main contributions of this paper are as follows:
- related_work: In recent years, the rise of deep learning technology has brought new opportunities and challenges to soft sensor modeling.
- method: Therefore, this paper proposes a dynamic attention mechanism strategy, which aims to calculate the dynamic attention scores of input process variables in real-time.
- experiments: Semiconductor silicon single crystal (SSSC) is an important raw material for the development of the integrated circuit (IC) industry.
- experiments: Compared to other soft sensor modeling methods, the proposed method demonstrates higher prediction accuracy and can better assist field operators or control systems in making more accurate control actions.
- conclusion: The proposed method of multi-output soft sensor modeling based on attention mechanism in this paper has been effectively validated in the experiment of Cz SSSC growth.
- conclusion: In conclusion, the proposed method of multi-output soft sensor modeling based on attention mechanism provides a new solution for estimating multiple quality variables in complex industrial production processes, and it has good engineering application prospects and can be extended to other complex industrial fields, such as steel manufacturing processes, urban wastewater treatment processes, etc.
