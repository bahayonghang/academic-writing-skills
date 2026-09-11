---
key: LZT5QKPD
title: "Spatio-temporal feature extraction network based multi-performance indicators synergetic monitoring method for complex industrial processes"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2024.125052"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries`（`2.1. CVA` / `2.2. Tensor decomposition`）→ `3. Methodology` → `4. Case study`（`4.1. TEP` / `4.2. HSMP`）→ `5. Conclusions`。前置 `ABSTRACT` 与 `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段数据补全、性能相关监测、时空特征提取）。Introduction 末有编号缺口 + 编号贡献 + 节序路标。Method 前有 Preliminaries。Experiments 标题为 `Case study`。

## Openers

- abstract: `In the context` — "In the context of smart manufacturing, modern industrial processes are becoming increasingly complex in terms of process flows, product varieties, and performance indicators (PIs)."
- introduction: `Complex industrial process` — "Complex industrial process modeling and monitoring are of practical significance to enhance the digitalization and intelligence level of manufacturing industries, and promote the high-quality development of the industry (Jiang, Yin & Kaynak, 2021)."
- method: `In this section,` — "In this section, the proposed multi-performance indicators synergetic monitoring framework is developed." (s.3)
- experiments: `In this section,` — "In this section, the proposed method is verified on a benchmark dataset, known as TEP, and an actual industrial process scenario, HSMP, respectively."
- conclusion: `In this paper,` — "In this paper, a spatio-temporal feature extraction network based performance-related process monitoring model is developed."

## Gap transitions

- however (abstract): "However, most methods require spatio-temporal correspondence between process variables and PIs, and rarely consider the correlation among various PIs."
- however (introduction): "However, in real industrial scenarios, data often encounter problems such as local missing values, incompletion, and imbalance due to the constraints imposed by sensor equipment and communication limitations."
- therefore (introduction): "Therefore, enhancing the quality of modeling data, exploring process features within complex spatio-temporal region, and developing a multi-performance indicators synergetic process monitoring model are pressing issues in the field of process control and monitoring."
- in this paper (introduction): "Motivated by the above observations, a spatio-temporal feature extraction network-based multi-performance indicators synergetic monitoring framework is presented in this paper."

## Hedge verbs

- present / causal / abstract, introduction: "a spatio-temporal feature extraction network-based multi-performance indicators synergetic monitoring framework is presented"
- demonstrate / associative / abstract, conclusion: "Experimental results on a benchmark dataset and a real industrial process demonstrate the effectiveness of the proposed monitoring model."
- outperform / associative / abstract, experiments: "Overall, the monitoring performance of the proposed method outperforms the traditional ones, in terms of higher fault detection rates and lower false alarm rates."

## Cross-section linkers

- introduction → preliminaries: "The rest of this paper is arranged as follows. In Section 2, technical basics of CVA and tensor decomposition are briefly revisited."
- method → experiments: "In Section 4, the proposed framework is verified on a benchmark, known as Tennessee Eastman process (TEP), and a real HSMP"
- experiments → conclusion: HSMP 实时性段落后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is arranged as follows`
- R004 编号贡献：`The main innovations and contributions are summarized as follows`
- R009 自称：`In this paper` / `is presented` / `is developed`

## Candidate phrases

- `In this paper, a spatio-temporal feature extraction network-based multi-performance indicators synergetic monitoring framework is presented` (abstract)
- `Motivated by the above observations` (introduction)
- `The main innovations and contributions are summarized as follows` (introduction)
- `The rest of this paper is arranged as follows` (introduction)
- `In this paper, a spatio-temporal feature extraction network based performance-related process monitoring model is developed` (conclusion)

## House style

自称 `In this paper` / `is presented` / `the proposed method`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: In the context of smart manufacturing, modern industrial processes are becoming increasingly complex in terms of process flows, product varieties, and performance indicators (PIs).
- abstract: However, most methods require spatio-temporal correspondence between process variables and PIs, and rarely consider the correlation among various PIs.
- abstract: In this paper, a spatio-temporal feature extraction network-based multi-performance indicators synergetic monitoring framework is presented.
- abstract: Overall, the monitoring performance of the proposed method outperforms the traditional ones, in terms of higher fault detection rates and lower false alarm rates.
- introduction: Complex industrial process modeling and monitoring are of practical significance to enhance the digitalization and intelligence level of manufacturing industries, and promote the high-quality development of the industry (Jiang, Yin & Kaynak, 2021).
- introduction: However, in real industrial scenarios, data often encounter problems such as local missing values, incompletion, and imbalance due to the constraints imposed by sensor equipment and communication limitations.
- introduction: In summary, the existing research gaps in performance-related process monitoring fall into three main aspects.
- introduction: Motivated by the above observations, a spatio-temporal feature extraction network-based multi-performance indicators synergetic monitoring framework is presented in this paper.
- introduction: The rest of this paper is arranged as follows. In Section 2, technical basics of CVA and tensor decomposition are briefly revisited.
- method: In this section, the proposed multi-performance indicators synergetic monitoring framework is developed.
- experiments: In this section, the proposed method is verified on a benchmark dataset, known as TEP, and an actual industrial process scenario, HSMP, respectively.
- conclusion: In this paper, a spatio-temporal feature extraction network based performance-related process monitoring model is developed.
- conclusion: Experimental results on a benchmark dataset and a real industrial process demonstrate the effectiveness of the proposed monitoring model.
