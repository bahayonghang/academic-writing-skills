---
key: VHZ22IBS
title: "Novel virtual sample generation using conditional GAN for developing soft sensor with small data"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2021.104497"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. The proposed method` → `3. Case study` → `4. Conclusions`。前置 `ABSTRACT`、`ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 SVM/灰色模型/贝叶斯、三类 VSG、GAN）。Introduction 末有节序路标，无编号贡献列表。Method 标题为 `The proposed method`。Experiments 标题为 `Case study`。结论标题为 `Conclusions`（复数）。

## Openers

- abstract: `In terms of data-driven` — "In terms of data-driven soft sensing modeling of industrial processes, it is practically necessary to collect sufficient process data."
- introduction: `In complex industrial processes` — "In complex industrial processes, some key parameters which determine the quality and efficiency of products are hard to directly measure online"
- method: `The presented CGAN-VSG approach` — "The presented CGAN-VSG approach is explained step by step and the rationality of the selected methods is provided in this section."
- experiments: `In this section` — "In this section, a two-dimensional standard function and a three-dimensional standard function are adopted to verify the superior effectiveness of the presented CGAN-VSG approach."
- conclusion: `In this study` — "In this study, a novel virtual sample generation based on conditional generative adversarial networks (CGAN-VSG) is proposed for enhancing soft-sensing with limited data."

## Gap transitions

- unfortunately (abstract): "Unfortunately, sometimes only few samples are available as a result of physical restrictions and time costs, resulting in insufficient data and incomplete data representative."
- to handle (abstract): "To handle those practical issues, a new virtual sample generation approach based on conditional generative adversarial network (CGAN-VSG) is proposed."
- however (introduction): "However, it is difficult to obtain enough representative process data to build soft sensors."
- in order to solve (introduction): "In order to solve the issue of small sample sets, several related researchers have designed and improved a variety of machine learning methods"
- based on these points (introduction): "Based on these points, in this study, a novel VSG method based on conditional generative adversarial networks (CGAN-VSG) is proposed."

## Hedge verbs

- is proposed / causal / abstract, introduction, conclusion: "a new virtual sample generation approach ... is proposed"; "a novel VSG method ... is proposed"
- suggest / associative / abstract: "Simulation results suggest that the presented CGAN-VSG approach is superior to several other state-of-the-art methods"
- confirm / causal / introduction, conclusion: "Simulation results on three case studies confirm the superior performance of CGAN-VSG"; "Simulation results confirm that the presented CGAN-VSG approach is superior"
- verify / causal / experiments: "a two-dimensional standard function and a three-dimensional standard function are adopted to verify the superior effectiveness"

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows. Section 2 introduces the proposed CGAN-VSG method in a detailed manner. Section 3 describes the case study and discusses the results. In Section 4, conclusions are given."
- method → experiments: 实现步骤后 `3. Case study`
- experiments → conclusion: HDPE 软测量结果后 `4. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is organized as follows`
- R009 自称：`is proposed` / `In this study, a novel VSG method ... is proposed`
- 结论节标题用 `Conclusions`（复数）；Introduction 无编号贡献列表。

## Candidate phrases

- `To handle those practical issues, a new virtual sample generation approach ... is proposed.` (abstract)
- `Based on these points, in this study, a novel VSG method ... is proposed.` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `Simulation results suggest that the presented ... approach is superior to` (abstract)
- `In this study, a novel virtual sample generation ... is proposed for enhancing` (conclusion)

## House style

自称 `is proposed` / `in this study` / `the presented CGAN-VSG` / `The rest of this paper`。未见 `In this paper`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: In terms of data-driven soft sensing modeling of industrial processes, it is practically necessary to collect sufficient process data.
- abstract: Unfortunately, sometimes only few samples are available as a result of physical restrictions and time costs, resulting in insufficient data and incomplete data representative.
- abstract: To handle those practical issues, a new virtual sample generation approach based on conditional generative adversarial network (CGAN-VSG) is proposed.
- abstract: Simulation results suggest that the presented CGAN-VSG approach is superior to several other state-of-the-art methods, such as TTD, MTD and bootstrap, in the term of accuracy.
- introduction: In complex industrial processes, some key parameters which determine the quality and efficiency of products are hard to directly measure online
- introduction: However, it is difficult to obtain enough representative process data to build soft sensors.
- introduction: Based on these points, in this study, a novel VSG method based on conditional generative adversarial networks (CGAN-VSG) is proposed.
- introduction: The rest of this paper is organized as follows. Section 2 introduces the proposed CGAN-VSG method in a detailed manner. Section 3 describes the case study and discusses the results. In Section 4, conclusions are given.
- method: The presented CGAN-VSG approach is explained step by step and the rationality of the selected methods is provided in this section.
- experiments: In this section, a two-dimensional standard function and a three-dimensional standard function are adopted to verify the superior effectiveness of the presented CGAN-VSG approach.
- experiments: Therefore, the BP soft-sensing model with the dataset extended by the proposed CGAN-VSG can obtain better performance in accuracy than the BP soft-sensing model with the dataset extended by other VSG methods.
- conclusion: In this study, a novel virtual sample generation based on conditional generative adversarial networks (CGAN-VSG) is proposed for enhancing soft-sensing with limited data.
- conclusion: Simulation results confirm that the presented CGAN-VSG approach is superior to several other state-of-the-art methods, such as TTD, MTD and bootstrap, in terms of accuracy.
- conclusion: In the future work, we will explore how to generate uniform virtual samples in the sparse areas of high-dimensional data and experimental data will be used.
