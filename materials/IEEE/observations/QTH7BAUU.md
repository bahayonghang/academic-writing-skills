---
key: QTH7BAUU
title: "Predicting Particle Size of Copper Ore Grinding With Stochastic Configuration Networks"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3431039"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. DESCRIPTION OF COPPER ORE GRINDING PROCESS` → `III. SCN-BASED SOFT SENSOR CONSTRUCTION` → `IV. PERFORMANCE EVALUATION` → `V. RELATED WORK` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work，且置于实验之后。Introduction 末有节序路标，指向 Section II–VI。Experiments 标题为 `PERFORMANCE EVALUATION`。

## Openers

- abstract: `This article presents` — "This article presents a case study on predicting the particle size of copper ore grinding with stochastic configuration networks (SCNs)." (p.1)
- introduction: `THE production of` — "THE production of copper ore dressing involves three sequential subprocesses: grinding; flotation; and thickening." (p.1)
- method: `This section details` — "This section details the process of constructing a SCN-based soft sensor for estimating the product particle size." (p.3)
- experiments: `This section reports` — "This section reports simulation results with comparisons." (p.5)
- related_work: `Accurately predicting particle` — "Accurately predicting particle size is crucial for optimizing grinding operations, improving product quality, and reducing costs." (p.8)
- conclusion: `A nonlinear temporal` — "A nonlinear temporal data modeling method was proposed and applied for predicting product particle of a copper ore grinding process." (p.8)

## Gap transitions

- however (introduction): "However, due to fluctuations in the size of the copper ore and the time lag of the grinding process, it is difficult for operators to evaluate the trend of the product particle size in time, which may cause the product particle size to move outside the suitable range." (p.1)
- therefore (introduction): "Therefore, establishing an accurate product particle size prediction model is important to improve product quality, reduce energy consumption, and increase enterprise economic benefit." (p.1)
- however (introduction): "However, it is hard to achieve satisfied performance in real-time." (p.1)
- unfortunately (introduction): "Unfortunately, there is a lack of practical guidance in the model design and training, although the well-known error back-propagation learning algorithm has been universally used." (p.1)

## Hedge verbs

- present / causal / abstract: "This article presents a case study"
- propose / causal / introduction, conclusion: "in this article, we propose an SCN-based approach"; "A nonlinear temporal data modeling method was proposed"
- demonstrate / causal / abstract, introduction: "Comparative experiments are carried out to demonstrate the effectiveness"; "Results demonstrate the superiority of the proposed method"
- employ / causal / introduction: "we employ the least absolute shrinkage and selection operator (LASSO) [19] to extract the input features"
- will focus / speculative / conclusion: "we will focus on some explorations of different versions of SCN"

## Cross-section linkers

- introduction → process: "The rest of this article is organized as follows. Section II gives a description of copper ore grinding process and formulates a modelling problem. Section III details the proposed framework for problem solving. Section IV reports our experimental results with comparisons to verify the effectiveness of the proposed method, and analyzes the selected input features. Section V reviews some related work. Finally, Section VI concludes this article." (p.2)
- method → experiments: EN 优化与 Fig. 5 后 `IV. PERFORMANCE EVALUATION` (p.5)
- experiments → related_work: 输入敏感性分析后 `V. RELATED WORK` (p.8)
- related_work → conclusion: 综述收束后 `VI. CONCLUSION` (p.8)

## Candidate rules

- R006 独立 Related Work，但置于实验之后、结论之前。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The contributions from this article can be summarized as follows` + 编号列表。
- R011 摘要用 `This article presents a case study on`，不以 `we propose` 起句。

## Candidate phrases

- `This article presents a case study on` (abstract)
- `in this article, we propose an SCN-based approach for` (introduction)
- `The contributions from this article can be summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `we will focus on some explorations of` (conclusion)

## House style

自称 `This article presents` / `in this article, we propose` / `our proposed modelling framework`。未见 `Here we`、`In this paper`。`This article presents` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: This article presents a case study on predicting the particle size of copper ore grinding with stochastic configuration networks (SCNs).
- p.1 abstract: Comparative experiments are carried out to demonstrate the effectiveness and merits of the proposed modeling techniques in terms of the model's accuracy, reliability, and interpretability.
- p.1 introduction: THE production of copper ore dressing involves three sequential subprocesses: grinding; flotation; and thickening.
- p.1 introduction: However, due to fluctuations in the size of the copper ore and the time lag of the grinding process, it is difficult for operators to evaluate the trend of the product particle size in time, which may cause the product particle size to move outside the suitable range.
- p.1 introduction: Therefore, establishing an accurate product particle size prediction model is important to improve product quality, reduce energy consumption, and increase enterprise economic benefit.
- p.1 introduction: Unfortunately, there is a lack of practical guidance in the model design and training, although the well-known error back-propagation learning algorithm has been universally used.
- p.2 introduction: Follow the way as described above, in this article, we propose an SCN-based approach for predicting product particle size of copper ore grinding processes.
- p.2 introduction: The contributions from this article can be summarized as follows.
- p.2 introduction: The rest of this article is organized as follows. Section II gives a description of copper ore grinding process and formulates a modelling problem. Section III details the proposed framework for problem solving. Section IV reports our experimental results with comparisons to verify the effectiveness of the proposed method, and analyzes the selected input features. Section V reviews some related work. Finally, Section VI concludes this article.
- p.3 method: This section details the process of constructing a SCN-based soft sensor for estimating the product particle size.
- p.5 experiments: This section reports simulation results with comparisons.
- p.8 related_work: Accurately predicting particle size is crucial for optimizing grinding operations, improving product quality, and reducing costs.
- p.8 conclusion: A nonlinear temporal data modeling method was proposed and applied for predicting product particle of a copper ore grinding process.
- p.9 conclusion: Along with this research direction addressed in this article, we will focus on some explorations of different versions of SCN for enhancing the model's predictive performance.
