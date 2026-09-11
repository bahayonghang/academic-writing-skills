---
key: 9DTS6EPJ
title: "Advancements in Soft-Sensor Technologies for Quality Control in Process Manufacturing: A Review"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2025.3549596"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. METHODS` → `III. DATA` → `IV. RESULTS AND DISCUSSION` → `V. CONCLUSIONS`。前置 `Abstract—`、`Index Terms—` 与 `LIST OF ACRONYMS`。无独立 Related Work。`related_work=inlined`（Introduction 用 Table 1 评 2000 年后软测量综述）。`II. METHODS` 是综述检索方法（Kitchenham），不是文献评述节。Introduction 末有节序路标，指向 Section 2–5。综述体，无 Method/Experiments 算法节。

## Openers

- abstract: `Recently, Machine Learning` — "Recently, Machine Learning has become a crucial tool for enhancing process quality control in manufacturing plants." (p.1)
- introduction: `THE manufacturing processes` — "THE manufacturing processes of commonly used goods, such as steel, cement, polymers, oil-based products, and chemicals, entail additional costs owing to their low quality." (p.1；栏首掉字)
- methods: `The methodology used` — "The methodology used in this critical review is based on four stages (Fig. 1)." (p.3, II)
- results: `The development of` — "The development of soft sensors using machine-learning algorithms is an important issue in terms of both science and technology." (p.5, IV)
- conclusion: `Research on soft` — "Research on soft sensors for predicting process quality indicators using machine learning has increased significantly since the year 2000." (p.10)

## Gap transitions

- however (abstract): "However, real-time assessments are often challenging." (p.1)
- nonetheless (introduction): "Nonetheless, real-time quality assessment is not feasible for many of these processes because of its inherent characteristics, absence of suitable devices, installation constraints, and high equipment expenses [4]." (p.2)
- however (introduction): "However, this method entails significant delays of up to 12 hours [5], resulting in blind spots for process-control engineers." (p.2)
- nonetheless (introduction): "Nonetheless, to the best of our knowledge, no review has focused on soft-sensor development and its evolution over the last two decades." (p.2)
- therefore (introduction): "Therefore, the objective of this study is to provide a comprehensive review of soft sensors used in process manufacturing industries since 2000 to predict quality variables." (p.2)
- therefore (introduction): "Therefore, to address these gaps and provide a more comprehensive understanding of the state of the art, this study aims to demonstrate the evolution of soft-sensor algorithms in the process industry for predicting relevant quality indicators." (p.3)

## Hedge verbs

- summarizes / causal / abstract: "This paper summarizes the methodologies implemented in soft-sensor technology during this century."
- aims / speculative / introduction: "this study aims to demonstrate the evolution of soft-sensor algorithms"
- is expected / speculative / conclusion: "deep learning algorithms are expected to be the primary focus of soft-sensor research in the near future"
- are also likely / speculative / conclusion: "traditional algorithms, such as shallow neural networks, support vector machines, and random forests, are also likely to be considered"
- suggest / speculative / results-adjacent: "Osisanwo suggests that if accuracy is the main objective, ANN-based (like DL) or SVM should be selected."

## Cross-section linkers

- introduction → methods: "The remainder of this paper is organized as follows. Section 2 describes the methodology of this review. In Section 3, a basic ML taxonomy for soft sensors is described, along with its historical background. In Section 4, the data from the review are discussed. Finally, conclusions are presented in Section 5." (p.3)
- methods → data: Kitchenham 筛选段落后直接 `III. DATA` (p.3)
- data → results: 历史背景后直接 `IV. RESULTS AND DISCUSSION` (p.5)
- results → conclusion: 性能准则段落后直接 `V. CONCLUSIONS` (p.10)

## Candidate rules

- R001 综述摘要用 `This paper summarizes`，缺口用 `However, real-time assessments are often challenging.`
- R002 Introduction 用 Table 1 评既有综述，再用 `to the best of our knowledge, no review has focused on` 立缺口。
- R003 自称 `this study` / `this review` / `this paper` 混用；路标用 `The remainder of this paper is organized as follows` 且节号写成 Section 2–5。
- R004 `II. METHODS` 写检索协议，不写独立 Related Work。

## Candidate phrases

- `This paper summarizes the methodologies implemented in` (abstract)
- `to the best of our knowledge, no review has focused on` (introduction)
- `Therefore, the objective of this study is to provide a comprehensive review of` (introduction)
- `The remainder of this paper is organized as follows.` (introduction)
- `The methodology used in this critical review is based on` (methods)

## House style

自称是 `This paper` / `this study` / `this review` / `this article`（页眉许可句）。摘要用 `This paper summarizes`。`This paper` / `this study` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。

## Quotes

- p.1 abstract: Recently, Machine Learning has become a crucial tool for enhancing process quality control in manufacturing plants.
- p.1 abstract: However, real-time assessments are often challenging.
- p.1 abstract: This paper summarizes the methodologies implemented in soft-sensor technology during this century.
- p.1 abstract: As data availability and computing power increase, deep learning algorithms will become the primary focus of soft sensor research, which will help lower energy consumption, enhance production rates, and reduce CO2 footprints.
- p.1 introduction: THE manufacturing processes of commonly used goods, such as steel, cement, polymers, oil-based products, and chemicals, entail additional costs owing to their low quality.
- p.2 introduction: Nonetheless, real-time quality assessment is not feasible for many of these processes because of its inherent characteristics, absence of suitable devices, installation constraints, and high equipment expenses [4].
- p.2 introduction: However, this method entails significant delays of up to 12 hours [5], resulting in blind spots for process-control engineers.
- p.2 introduction: Nonetheless, to the best of our knowledge, no review has focused on soft-sensor development and its evolution over the last two decades.
- p.2 introduction: Therefore, the objective of this study is to provide a comprehensive review of soft sensors used in process manufacturing industries since 2000 to predict quality variables.
- p.3 introduction: Therefore, to address these gaps and provide a more comprehensive understanding of the state of the art, this study aims to demonstrate the evolution of soft-sensor algorithms in the process industry for predicting relevant quality indicators.
- p.3 introduction: The remainder of this paper is organized as follows. Section 2 describes the methodology of this review. In Section 3, a basic ML taxonomy for soft sensors is described, along with its historical background. In Section 4, the data from the review are discussed. Finally, conclusions are presented in Section 5.
- p.3 methods: The methodology used in this critical review is based on four stages (Fig. 1).
- p.3 methods: Therefore, from prominent databases more than 390 studies were retrieved and further screened based on specific selection criteria in accordance with Kitchenham and Charters [31].
- p.5 results: The development of soft sensors using machine-learning algorithms is an important issue in terms of both science and technology.
- p.10 conclusion: Research on soft sensors for predicting process quality indicators using machine learning has increased significantly since the year 2000.
- p.10–11 conclusion: With the increasing availability of data and computing power, deep learning algorithms are expected to be the primary focus of soft-sensor research in the near future.
