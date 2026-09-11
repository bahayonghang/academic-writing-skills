---
key: NRQZJZGW
title: "Novel Semi-Supervised Seasonal-Trend VTN for Multimode Process IoT Soft Sensing"
venue: "IEEE Internet of Things Journal"
doi: "10.1109/JIOT.2025.3602808"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 AE/RNN/LSTM/Transformer 与 VAE/DVAE 软测量）。未见 `The rest of this article is organized as follows`；贡献列表后直接进入 II。Experiments 标题为 `CASE STUDY`（燃气轮机 NOx + SRU SO2）。

## Openers

- abstract: `The rapid development` — "The rapid development of soft sensors has significantly enhanced industrial operations by promoting sustainability, safety, and efficiency." (p.1)
- introduction: `IN MODERN process` — "IN MODERN process industries, the precise and real-time online measurement of quality variables is paramount for optimizing production, enhancing control, and facilitating decision-making." (p.1；栏首掉字)
- method: `In this section,` — "In this section, we present the proposed seasonal-trend variational transformer network (ST-VTN) and introduce the derivation of its formula in detail." (p.3, III)
- experiments: `In this section,` — "In this section, a real-world power plant gas turbine dataset and a sulfur recovery unit (SRU) dataset are utilized to verify the validity of the proposed ST-VTN." (p.5, IV)
- conclusion: `Considering the multimode,` — "Considering the multimode, highly dynamic, and nonlinear characteristics of modern industrial process data, this article proposes a Variational Transformer Network (ST-VTN) based on seasonal-trend decomposition for industrial soft sensor modeling." (p.8)

## Gap transitions

- however (abstract): "However, modern process industries involve highly dynamic systems with multimode and nonlinear data, posing challenges for conventional soft sensor models that assume uniform data distributions." (p.1)
- additionally (abstract): "Additionally, limited target mode data hinders effective training." (p.1)
- to-address (abstract): "To address these issues, we propose the seasonal-trend variational transformer network (ST-VTN), a deep probabilistic model based on seasonal-trend decomposition." (p.1)
- although (introduction): "Although most VAE methods have been successfully applied in soft sensor modeling, they still face several issues." (p.1)
- however (introduction): "However, real-world industrial processes often exhibit multimode characteristics due to changes in production processes, frequent switching between manual and automatic operations, and sensor degradation [17]." (p.2)
- to-address (introduction): "To address the challenges of inadequate explainability, ineffectiveness in capturing multimode dynamic characteristics, and failure to identify underlying seasonal trends in industrial systems, we propose a semi-supervised dynamic variational Transformer network model based on time pattern decomposition (ST-VTN)" (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose the seasonal-trend variational transformer network (ST-VTN)"
- confirm / causal / abstract: "Experiments on gas turbine and sulfur recovery datasets confirm ST-VTN's superior performance"
- present / causal / method: "we present the proposed seasonal-trend variational transformer network (ST-VTN)"
- verify / causal / experiments: "are utilized to verify the validity of the proposed ST-VTN"
- indicate / speculative / experiments: "Results indicate that ST-VTN outperforms other state-of-the-art techniques"
- will focus / speculative / conclusion: "Future work will focus on using a single model to simultaneously predict multiple quality variables"

## Cross-section linkers

- introduction → preliminaries: 贡献条 5 后直接 `II. PRELIMINARIES`，无节序路标。(p.2)
- preliminaries → method: `III. METHODOLOGY` 首句收回 ST-VTN 公式与框架。(p.3)
- method → experiments: "Finally, the implementation of the ST-VTN-based soft sensor is discussed in Section III-D." 随后 `IV. CASE STUDY` (p.3, p.5)
- experiments → conclusion: 消融段落后直接 `V. CONCLUSION` (p.8)

## Candidate rules

- R001 摘要缺口链：`However` 多模/非线性 + `Additionally` 少标签 + `To address these issues, we propose`。
- R002 Introduction 无独立 Related Work；VAE/Transformer 评述写在引言中段。
- R003 贡献用 `The main contributions are as follows.` + 编号列表，不用 `this paper`。
- R004 Experiments 标题为 `CASE STUDY`；结论用 `this article proposes` 收回方法，再用 `Future work will focus on`。

## Candidate phrases

- `To address these issues, we propose` (abstract)
- `The main contributions are as follows.` (introduction)
- `In this section, we present the proposed` (method)
- `are utilized to verify the validity of the proposed` (experiments)
- `this article proposes a` (conclusion)
- `Future work will focus on` (conclusion)

## House style

自称是 `we propose` / `this article proposes` / `the proposed ST-VTN` / `the proposed method`。未见 `In this paper`。`this article proposes` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The rapid development of soft sensors has significantly enhanced industrial operations by promoting sustainability, safety, and efficiency.
- p.1 abstract: However, modern process industries involve highly dynamic systems with multimode and nonlinear data, posing challenges for conventional soft sensor models that assume uniform data distributions.
- p.1 abstract: To address these issues, we propose the seasonal-trend variational transformer network (ST-VTN), a deep probabilistic model based on seasonal-trend decomposition.
- p.1 abstract: Experiments on gas turbine and sulfur recovery datasets confirm ST-VTN's superior performance for multimode regression tasks.
- p.1 introduction: IN MODERN process industries, the precise and real-time online measurement of quality variables is paramount for optimizing production, enhancing control, and facilitating decision-making.
- p.1 introduction: Although most VAE methods have been successfully applied in soft sensor modeling, they still face several issues.
- p.2 introduction: However, real-world industrial processes often exhibit multimode characteristics due to changes in production processes, frequent switching between manual and automatic operations, and sensor degradation [17].
- p.2 introduction: To address the challenges of inadequate explainability, ineffectiveness in capturing multimode dynamic characteristics, and failure to identify underlying seasonal trends in industrial systems, we propose a semi-supervised dynamic variational Transformer network model based on time pattern decomposition (ST-VTN) for multimode industrial soft sensor modeling and time-series analysis.
- p.2 introduction: The main contributions are as follows.
- p.3 method: In this section, we present the proposed seasonal-trend variational transformer network (ST-VTN) and introduce the derivation of its formula in detail.
- p.3 method: As illustrated in Fig. 3, the ST-VTN framework comprises three stages: preprocessing, pre-training, and fine-tuning.
- p.5 experiments: In this section, a real-world power plant gas turbine dataset and a sulfur recovery unit (SRU) dataset are utilized to verify the validity of the proposed ST-VTN.
- p.6 experiments: The proposed ST-VTN achieves robust results for both variables by explicitly capturing the structure of data under different modalities and effectively integrating mode features with regression relationships during the fine-tuning stage.
- p.8 conclusion: Considering the multimode, highly dynamic, and nonlinear characteristics of modern industrial process data, this article proposes a Variational Transformer Network (ST-VTN) based on seasonal-trend decomposition for industrial soft sensor modeling.
- p.8 conclusion: Results indicate that ST-VTN outperforms other state-of-the-art techniques and baseline methods in soft sensor modeling.
- p.8 conclusion: Future work will focus on using a single model to simultaneously predict multiple quality variables and developing multitask foundation models.
