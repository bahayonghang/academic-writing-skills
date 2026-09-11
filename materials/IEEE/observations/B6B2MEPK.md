---
key: B6B2MEPK
title: "A Survey on Soft Sensor of Free Calcium Oxide Content"
venue: "2022 27th International Conference on Automation and Computing (ICAC)"
doi: "10.1109/ICAC55051.2022.9911093"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-6"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. SELECTION OF AUXILIARY VARIABLES` → 数据预处理（Fig.2）→ `IV. TRADITIONAL SOFT MEASUREMENT METHODS` → `V. DEEP LEARNING METHODS` → `VI. RESEARCH DIRECTIONS` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Keywords—`。无独立 Related Work；综述正文即文献评述。`related_work=inlined`（Introduction 中段评机理建模 / 多元统计 / SVM / 浅层与深度网络）。Introduction 末有节序路标（阿拉伯数字 Section 2–5，与正文罗马数字不完全对齐）。无独立 Experiments；IV–V 为方法综述，VI 为展望。

## Openers

- abstract: `The free calcium` — "The free calcium oxide (f-CaO) content of cement clinker is an important indicator of its quality, and soft measurement modeling techniques enable the monitoring of clinker f-CaO content in real-time." (p.1)
- introduction: `As one of` — "As one of the important materials for infrastructure construction, the high-quality production of cement is of great importance for stable construction and life safety [1]." (p.1)
- method: `Figure 1 shows` — "Figure 1 shows that cement goes through three stages from raw material to clinker, namely preheating and pre-decomposition of raw material, calcination of raw material and cooling of clinker." (p.1, II)
- experiments: `Given the features` — "Given the features of nonlinearity, strong coupling and time-varying delay in the process of cement production, a large number of scholars at home and abroad proposed many data-driven soft measurement methods for f-CaO content by using historical data in the cement production process for real-time online supervising of cement clinker f-CaO content." (p.3, IV)
- conclusion: `Real-time online monitoring` — "Real-time online monitoring of the f-CaO content is very important for the control of cement quality and the production optimization process." (p.6)

## Gap transitions

- however (introduction): "However, the method is time-consuming and the measurement accuracy is easily affected by human factors [3], and it is to the disadvantage of the real-time control and optimization of the cement production process." (p.1)
- however (introduction): "However, modern production processes tend to be automated, integrated and holistic." (p.1)
- however (traditional methods): "However, these improved models only utilize the process variables associated with rotary kilns as auxiliary variables and do not consider the cement firing process as a typical process industry where cement quality is influenced by a variety of equipment environments." (p.3)
- however (traditional methods): "However, there are limitations in these traditional soft measurement modelling methods, which make the soft measurement models for f-CaO content less accurate and less adaptable in dynamic environments with multiple operating conditions." (p.3)
- although (research directions): "Although some scholars have proposed some soft measurement methods to achieve real-time online monitoring of cement clinker f-CaO content, they have certain limitations, and there are still relevant issues in the modelling of soft measurement of f-CaO content that need to be studied and solved in depth:" (p.5)
- however (conclusion): "However, because of the complexity of the cement clinker f-CaO production process, the existing soft measurement modelling methods still have some limitations." (p.6)
- therefore (conclusion): "Therefore, future problems related to soft measurement modelling of cement clinker f-CaO still need to be investigated and solved in depth." (p.6)

## Hedge verbs

- introduce / causal / abstract: "In this paper, we introduce and describe the selection and pre-processing of auxiliary variables"
- review / causal / abstract, introduction: "then review data-driven soft measurement models for f-CaO contents and their limitations"; "This paper reviews these literatures"
- propose / causal / traditional methods: "a large number of scholars at home and abroad proposed many data-driven soft measurement methods"
- need / speculative / research directions, conclusion: "need to be studied and solved in depth"; "still need to be investigated and solved in depth"

## Cross-section linkers

- introduction → survey body: "The organization of the paper is as follows: Section 2 introduces the selection of auxiliary variables in the modelling process. Section 3 collates traditional f-CaO soft measurement methods. Section 4 presents the application of deep learning techniques to f-CaO soft measurement. Finally, Section 5 gives future research directions and ideas for f-CaO soft measurement." (p.1)
- traditional → deep learning: 局限段落后接 `V. DEEP LEARNING METHODS` (p.3)
- deep learning → directions: Table 2 后接 `VI. RESEARCH DIRECTIONS` (p.5)
- directions → conclusion: 半监督展望后接 `VII. CONCLUSION` (p.6)

## Candidate rules

- R001 摘要用 `In this paper, we introduce and describe` + `then review`，综述体裁。
- R002 Introduction 无独立 Related Work，四条过程特性写在引言中段。
- R003 Introduction 末用 `The organization of the paper is as follows`；正文罗马数字与路标阿拉伯数字不完全对齐。
- R004 展望节用编号问题列表（Constructing correlation algorithms / ...）。
- R005 Conclusion 先收回综述范围，再用 `However` + `Therefore, future problems ... still need`。

## Candidate phrases

- `In this paper, we introduce and describe the selection and pre-processing of auxiliary variables` (abstract)
- `The organization of the paper is as follows:` (introduction)
- `Although some scholars have proposed some soft measurement methods to achieve` (research directions)
- `In this paper, the problem of real-time online monitoring of f-CaO in the cement firing process is investigated in depth` (conclusion)

## House style

自称是 `In this paper, we introduce` / `This paper reviews` / `this paper provides some indication`。未见 `Here we`。`In this paper, we introduce` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The free calcium oxide (f-CaO) content of cement clinker is an important indicator of its quality, and soft measurement modeling techniques enable the monitoring of clinker f-CaO content in real-time.
- p.1 abstract: In this paper, we introduce and describe the selection and pre-processing of auxiliary variables in soft measurement models for cement clinker quality, then review data-driven soft measurement models for f-CaO contents and their limitations.
- p.1 abstract: Future research directions and ideas in this field are presented concerning the limitations of current soft measurement methods and the problems in this field.
- p.1 introduction: As one of the important materials for infrastructure construction, the high-quality production of cement is of great importance for stable construction and life safety [1].
- p.1 introduction: However, the method is time-consuming and the measurement accuracy is easily affected by human factors [3], and it is to the disadvantage of the real-time control and optimization of the cement production process.
- p.1 introduction: However, modern production processes tend to be automated, integrated and holistic.
- p.1 introduction: This paper reviews these literatures in terms of both auxiliary variable selection and model methodology construction and describes the advantages and limitations of the model structures constructed in these literatures.
- p.1 introduction: The organization of the paper is as follows: Section 2 introduces the selection of auxiliary variables in the modelling process. Section 3 collates traditional f-CaO soft measurement methods. Section 4 presents the application of deep learning techniques to f-CaO soft measurement. Finally, Section 5 gives future research directions and ideas for f-CaO soft measurement.
- p.1 method: Figure 1 shows that cement goes through three stages from raw material to clinker, namely preheating and pre-decomposition of raw material, calcination of raw material and cooling of clinker.
- p.3 traditional methods: Given the features of nonlinearity, strong coupling and time-varying delay in the process of cement production, a large number of scholars at home and abroad proposed many data-driven soft measurement methods for f-CaO content by using historical data in the cement production process for real-time online supervising of cement clinker f-CaO content.
- p.3 traditional methods: However, these improved models only utilize the process variables associated with rotary kilns as auxiliary variables and do not consider the cement firing process as a typical process industry where cement quality is influenced by a variety of equipment environments.
- p.3 traditional methods: However, there are limitations in these traditional soft measurement modelling methods, which make the soft measurement models for f-CaO content less accurate and less adaptable in dynamic environments with multiple operating conditions.
- p.5 research directions: Although some scholars have proposed some soft measurement methods to achieve real-time online monitoring of cement clinker f-CaO content, they have certain limitations, and there are still relevant issues in the modelling of soft measurement of f-CaO content that need to be studied and solved in depth:
- p.6 conclusion: Real-time online monitoring of the f-CaO content is very important for the control of cement quality and the production optimization process.
- p.6 conclusion: In this paper, the problem of real-time online monitoring of f-CaO in the cement firing process is investigated in depth based on soft measurement techniques in a cement clinker firing system.
- p.6 conclusion: However, because of the complexity of the cement clinker f-CaO production process, the existing soft measurement modelling methods still have some limitations.
- p.6 conclusion: Therefore, future problems related to soft measurement modelling of cement clinker f-CaO still need to be investigated and solved in depth.
