---
key: N8NLRF36
title: "Time-aware personalized graph convolutional network for multivariate time series forecasting"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2023.122471"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work`（`2.1. Time series forecasting` / `2.2. Graph structure and graph convolution of spatio-temporal GNN`）→ `3. Preliminaries` → `4. Methodology`（`4.1. Overview` / TADG / TCN / DPGC）→ `5. Experiment` → `6. Conclusion`。前置 `ABSTRACT` 与 `Keywords`。独立 Related Work。`related_work=independent`。Introduction 末有条目贡献。未见 `The rest of this paper is organized as follows` 路标。Method 前有 Preliminaries。

## Openers

- abstract: `The use of graph` — "The use of graph structures to model variable dependencies in multivariate time series data holds promise."
- introduction: `Multivariate time series` — "Multivariate time series analysis is an indispensable area of investigation within science and engineering, owing to its pervasive applications in areas such as climate studies (Reichstein et al., 2019), traffic control (Han et al., 2021), and energy management (Liu et al., 2023)."
- related_work: `Time series prediction` — "Time series prediction is a well-explored topic encompassing statistical methods and deep learning techniques."
- method: `The architecture of` — "The architecture of the time-aware personalized graph convolutional network (TPGCN) is shown in Fig. 2." (s.4.1)
- experiments: `To provide a` — "To provide a comprehensive validation of our model TPGCN, we carry out experiments on eight benchmark datasets, consisting of four for single-step prediction (Lai et al., 2018) and four for multi-step prediction (Guo et al., 2022)."
- conclusion: `Within this study,` — "Within this study, we introduce the TPGCN, a time-aware personalized graph convolutional network."

## Gap transitions

- however (abstract): "However, the current approaches ignore that dependencies are dynamic and constrained by heterogeneous information."
- to address (abstract): "To address these limitations, this research introduces a novel approach: a time-aware personalized graph convolutional network (TPGCN)"
- although (introduction): "Although the methods discussed above have yielded notable success, several significant challenges remain unresolved."
- to address (introduction): "To address these challenges, this paper proposes the time-aware personalized graph convolutional network (TPGCN)"

## Hedge verbs

- introduce / causal / abstract, conclusion: "this research introduces a novel approach"; "we introduce the TPGCN"
- propose / causal / introduction: "this paper proposes the time-aware personalized graph convolutional network (TPGCN)"
- demonstrate / associative / abstract, conclusion: "our approach outperforms existing state-of-the-art methods, as demonstrated on eight benchmark datasets"; "Our extensive experiments on eight benchmark datasets demonstrate the efficacy of our proposed approach."

## Cross-section linkers

- introduction → related_work: 贡献列表后 `2. Related work`
- related_work → preliminaries: `3. Preliminaries`
- method → experiments: `5. Experiment` / "To provide a comprehensive validation of our model TPGCN"
- experiments → conclusion: 图结构与注意力分析后 `6. Conclusion`

## Candidate rules

- R001 独立 Related Work（`2. Related work`）。
- R004 条目贡献：`The main contributions are summarized as follows`
- R009 自称：`this paper proposes` / `this research introduces` / `Within this study, we introduce`

## Candidate phrases

- `To address these limitations, this research introduces` (abstract)
- `To address these challenges, this paper proposes` (introduction)
- `The main contributions are summarized as follows` (introduction)
- `To provide a comprehensive validation of our model TPGCN, we carry out experiments` (experiments)
- `Within this study, we introduce the TPGCN` (conclusion)

## House style

自称 `this paper proposes` / `this research introduces` / `Within this study, we introduce`。实验节用 `we carry out`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The use of graph structures to model variable dependencies in multivariate time series data holds promise.
- abstract: However, the current approaches ignore that dependencies are dynamic and constrained by heterogeneous information.
- abstract: To address these limitations, this research introduces a novel approach: a time-aware personalized graph convolutional network (TPGCN) consisting of time-aware discrete graph structure estimation (TADG) and dynamic personalized graph convolutional (DPGC) components.
- abstract: By dynamically fusing these two types of information at every information aggregation, our approach outperforms existing state-of-the-art methods, as demonstrated on eight benchmark datasets.
- introduction: Multivariate time series analysis is an indispensable area of investigation within science and engineering, owing to its pervasive applications in areas such as climate studies (Reichstein et al., 2019), traffic control (Han et al., 2021), and energy management (Liu et al., 2023).
- introduction: Although the methods discussed above have yielded notable success, several significant challenges remain unresolved.
- introduction: To address these challenges, this paper proposes the time-aware personalized graph convolutional network (TPGCN), a construct encompassing two pivotal constituents: time-aware discrete graph structure estimation (TADG) and dynamic personalized graph convolution (DPGC).
- introduction: The main contributions are summarized as follows:
- related_work: Time series prediction is a well-explored topic encompassing statistical methods and deep learning techniques.
- method: The architecture of the time-aware personalized graph convolutional network (TPGCN) is shown in Fig. 2.
- experiments: To provide a comprehensive validation of our model TPGCN, we carry out experiments on eight benchmark datasets, consisting of four for single-step prediction (Lai et al., 2018) and four for multi-step prediction (Guo et al., 2022).
- conclusion: Within this study, we introduce the TPGCN, a time-aware personalized graph convolutional network.
- conclusion: Our extensive experiments on eight benchmark datasets demonstrate the efficacy of our proposed approach.
