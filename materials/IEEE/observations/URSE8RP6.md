---
key: URSE8RP6
title: "Attention-Based Interval Aided Networks for Data Modeling of Heterogeneous Sampling Sequences With Missing Values in Process Industry"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3329684"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. ATTENTION-BASED INTERVAL AIDED NETWORK` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评静态深度网络、LSTM/GRU、缺失插补与不规则采样）。Introduction 末有编号贡献，无 `The rest of this article is organized` 路标。Method 标题为 `ATTENTION-BASED INTERVAL AIDED NETWORK`。Experiments 标题为 `CASE STUDIES`（加氢裂化轻石脑油 C5/C6）。

## Openers

- abstract: `In complex process` — "In complex process industries, multivariate time sequences are omnipresent, whose nonlinearities and dynamics present two major challenges for soft sensing of important quality variables." (p.5253)
- introduction: `FOLLOWING the three` — "FOLLOWING the three industrial revolutions, the fast-growing global market has imposed great demands on the production capability of the industry." (p.5253；栏首掉字)
- method: `In AIA-Net` — "In AIA-Net, two mechanisms named ATADI and IATAN are designed to adaptively model the temporal information for heterogeneous sampling sequences with missing values in industrial continuous-flow manufacturing processes." (p.5255)
- experiments: `After AIA-Net is` — "After AIA-Net is constructed, it can be used for soft sensor modeling." (p.5257)
- conclusion: `In this article` — "In this article, AIA-Net was proposed to adaptively model the temporal relationship for heterogeneous sampling sequences with missing values in industrial continuous-flow manufacturing processes." (p.5261)

## Gap transitions

- to this end (abstract): "To this end, attention-based interval-aided networks (AIA-Net) are proposed in this article to adaptively model the temporal information for heterogeneous sampling sequences with missing values in the processes industry." (p.5253)
- however (introduction): "However, these soft sensors are constructed using static deep networks, where data samples are assumed to be independent and identically distributed." (p.5254)
- however (introduction): "However, the existing RNN-based structures are mostly difficult to tackle such irregular sample problems, especially for heterogeneous sampling industrial sequence modeling with missing values." (p.5254)
- currently / however (conclusion): "Currently, the proposed method is applicable to heterogeneous data sequences with random missing values. However, it may not be suitable for scenarios involving block data missing over a period due to sensor and communication failures in severe industrial environments." (p.5261)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "attention-based interval-aided networks (AIA-Net) are proposed in this article"; "AIA-Net was proposed"
- show / causal / experiments: "Fig. 7 shows the framework for soft sensor modeling based on AIA-Net"; "The experiment results are shown in Table I"
- suggest / associative / experiments: "Overall, these results suggest that AIA-LSTM provides the best prediction performance for the C5 content of the light naphtha."

## Cross-section linkers

- introduction → preliminaries: 贡献列表结束后直接 `II. PRELIMINARIES`，无独立路标句 (p.5255)
- method → experiments: "After AIA-Net is constructed, it can be used for soft sensor modeling." 随后 `IV. CASE STUDIES` (p.5257)
- experiments → conclusion: C6 箱线图段落后直接 `V. CONCLUSION` (p.5261)

## Candidate rules

- R004 贡献列表：本篇为 `the main contributions of this article are as follows.` + 编号。
- R007 摘要用 `To this end, ... are proposed in this article` 点名方法缩写。
- R005 结论局限：`Currently, the proposed method is applicable` + `However, it may not be suitable`，再用 `will continue to be addressed ... in the future`。

## Candidate phrases

- `To this end, attention-based interval-aided networks (AIA-Net) are proposed in this article` (abstract)
- `the main contributions of this article are as follows.` (introduction)
- `In this article, AIA-Net was proposed to` (conclusion)
- `The issue of missing block data will continue to be addressed with increased efforts in the future.` (conclusion)

## House style

自称 `are proposed in this article` / `this article is mainly focused` / `In this article, AIA-Net was proposed`。未见 `Here we`。`are proposed in this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.5253 abstract: In complex process industries, multivariate time sequences are omnipresent, whose nonlinearities and dynamics present two major challenges for soft sensing of important quality variables.
- p.5253 abstract: To this end, attention-based interval-aided networks (AIA-Net) are proposed in this article to adaptively model the temporal information for heterogeneous sampling sequences with missing values in the processes industry.
- p.5253 abstract: The proposed AIA-Net is successfully applied to a real hydrocracking process to predict the C5 and C6 content in the light naphtha.
- p.5253 introduction: FOLLOWING the three industrial revolutions, the fast-growing global market has imposed great demands on the production capability of the industry.
- p.5254 introduction: However, these soft sensors are constructed using static deep networks, where data samples are assumed to be independent and identically distributed.
- p.5254 introduction: However, the existing RNN-based structures are mostly difficult to tackle such irregular sample problems, especially for heterogeneous sampling industrial sequence modeling with missing values.
- p.5254 introduction: In particular, the main contributions of this article are as follows.
- p.5255 method: In AIA-Net, two mechanisms named ATADI and IATAN are designed to adaptively model the temporal information for heterogeneous sampling sequences with missing values in industrial continuous-flow manufacturing processes.
- p.5257 experiments: After AIA-Net is constructed, it can be used for soft sensor modeling.
- p.5259 experiments: Overall, these results suggest that AIA-LSTM provides the best prediction performance for the C5 content of the light naphtha.
- p.5261 conclusion: In this article, AIA-Net was proposed to adaptively model the temporal relationship for heterogeneous sampling sequences with missing values in industrial continuous-flow manufacturing processes.
- p.5261 conclusion: Currently, the proposed method is applicable to heterogeneous data sequences with random missing values. However, it may not be suitable for scenarios involving block data missing over a period due to sensor and communication failures in severe industrial environments.
- p.5261 conclusion: The issue of missing block data will continue to be addressed with increased efforts in the future.
