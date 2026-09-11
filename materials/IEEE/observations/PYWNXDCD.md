---
key: PYWNXDCD
title: "Towards Expressive Spectral-Temporal Graph Neural Networks for Time Series Forecasting"
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence"
doi: "10.1109/TPAMI.2025.3545671"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,4-8,9-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PRELIMINARY` → `IV. A THEORETICAL FRAMEWORK OF SPECTRAL-TEMPORAL GRAPH NEURAL NETWORKS` → `V. METHODOLOGY: TEMPORAL GRAPH GEGENBAUER CONVOLUTION` → `VI. EVALUATION` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 末有节序路标，指向 Section II–VII。Method 分理论框架（IV）与 TGGC 实例（V）。Experiments 标题为 `EVALUATION`。

## Openers

- abstract: `Time series forecasting` — "Time series forecasting has remained a focal point due to its vital applications in sectors such as energy management and transportation planning." (p.4926)
- introduction: `GRAPH neural networks` — "GRAPH neural networks (GNNs) have achieved considerable success in static graph representation learning for many tasks [1]." (p.4926)
- related_work: `In this section,` — "In this section, we provide a concise overview of pertinent literature, encompassing contemporary time series forecasting models, spatio-temporal graph neural networks, and recent advancements in spectral graph neural networks." (p.4928, II)
- method: `In this section,` — "In this section, we present a straightforward yet effective instantiation mainly based on the discussion in Section IV-C." (p.4932, V)
- experiments: `In this section,` — "In this section, we evaluate the effectiveness and efficiency of our proposal on 8 real-world datasets by comparing TGGC and TGGC† with over 20 different baselines." (p.4933, VI)
- conclusion: `In this study,` — "In this study, we provide the general formulation of spectral-temporal graph neural networks (SPTGNNS), laying down a theoretical framework for this category of methods." (p.4937)

## Gap transitions

- however (abstract): "However, more is needed to know about the underpinnings of this branch of methods." (p.4926)
- nevertheless (introduction): "Nevertheless, how to model real-world multivariate time series with complex spatial dependencies that evolve remains an open question." (p.4926)
- although (introduction): "Although it demonstrated competitive performance, the theoretical foundations of SPTGNNS remain under-researched, which hinders the understanding of SPTGNNS and the development of follow-up research within this model family." (p.4926)
- however (related_work): "However, these methods struggle to model differently signed time series relations since their graph convolutions operate under the umbrella of message passing, which serves as low-pass filtering assuming local homophiles." (p.4928)
- although (related_work): "Although spectral GNNs pave the way for SPTGNNS, they primarily focus on modeling static graph-structured data without the knowledge telling how to effectively convolute on dynamic graphs for modeling time series data." (p.4928)
- a limitation (conclusion): "A limitation of our approach is that SPTGNNS may face challenges in handling specific types of time series data, such as the underlying graph topology is highly symmetric and node attributes exhibit strong non-stationary or non-periodic behavior." (p.4937)

## Hedge verbs

- establish / causal / abstract, introduction: "we establish a theoretical framework"; "we establish a series of theoretical results"
- propose / causal / abstract, introduction: "we propose a simple instantiation named Temporal Graph Gegenbauer Convolution (TGGC)"
- demonstrate / causal / introduction: "We demonstrate that TGGC can outperform the most representative and related models"
- show / causal / abstract: "Our results show that linear spectral-temporal GNNs are universal under mild assumptions"
- may / speculative / conclusion: "SPTGNNS may face challenges in handling specific types of time series data"

## Cross-section linkers

- introduction → related_work: "The structure of this paper is outlined as follows: Section II provides an overview of the related work, examining various facets in detail. Section III delineates the notations and introduces essential background knowledge. Section IV presents a theoretical framework to deepen the understanding of SPTGNNS, addressing the research questions set forth. Section V showcases our theoretical insights through a novel and straightforward implementation known as TGGC, including its advanced variant TGGC†. Our research findings are evaluated and shared in Section VI, and a concise conclusion encapsulating our discoveries can be found in Section VII." (p.4927)
- theory → method: "Drawing from and to validate these theoretical insights, we present a straightforward, yet effective and novel SPTGNN instantiation, named TGGC" (p.4927); V 节 "mainly based on the discussion in Section IV-C" (p.4932)
- experiments → conclusion: Additional analysis 后直接 `VII. CONCLUSION` (p.4937)

## Candidate rules

- R001 Abstract 用 `In this paper, we establish a theoretical framework`，再用 `we propose a simple instantiation named`。
- R002 Introduction 用编号问题 Q1–Q4 组织缺口，再用 `Our main contributions in this work are summarized as follows`。
- R003 Introduction 末用 `The structure of this paper is outlined as follows` 指向 II–VII。
- R004 Related Work 分 Deep Time Series / STGNN / Spectral GNN 三块，末段接到本文。
- R005 Conclusion 用 `In this study` 收回，再用 `A limitation of our approach is` + `future research will also explore`。

## Candidate phrases

- `In this paper, we establish a theoretical framework that` (abstract)
- `we propose a simple instantiation named` (abstract)
- `Our main contributions in this work are summarized as follows.` (introduction)
- `The structure of this paper is outlined as follows:` (introduction)
- `In this study, we provide the general formulation of` (conclusion)

## House style

自称是 `In this paper` / `In this work` / `In this study` / `we propose` / `our method`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。偶见 `this paper`（节序句）。

## Quotes

- p.4926 abstract: Time series forecasting has remained a focal point due to its vital applications in sectors such as energy management and transportation planning.
- p.4926 abstract: However, more is needed to know about the underpinnings of this branch of methods.
- p.4926 abstract: In this paper, we establish a theoretical framework that unravels the expressive power of spectral-temporal GNNs.
- p.4926 abstract: Our results show that linear spectral-temporal GNNs are universal under mild assumptions, and their expressive power is bounded by our extended first-order Weisfeiler–Leman algorithm on discrete-time dynamic graphs.
- p.4926 abstract: Building on these insights and to demonstrate how powerful spectral-temporal GNNs are based on our framework, we propose a simple instantiation named Temporal Graph Gegenbauer Convolution (TGGC), which significantly outperforms most existing models with only linear components and shows better model efficiency.
- p.4926 introduction: GRAPH neural networks (GNNs) have achieved considerable success in static graph representation learning for many tasks [1].
- p.4926 introduction: Nevertheless, how to model real-world multivariate time series with complex spatial dependencies that evolve remains an open question.
- p.4926 introduction: Although it demonstrated competitive performance, the theoretical foundations of SPTGNNS remain under-researched, which hinders the understanding of SPTGNNS and the development of follow-up research within this model family.
- p.4927 introduction: Our main contributions in this work are summarized as follows.
- p.4927 introduction: The structure of this paper is outlined as follows: Section II provides an overview of the related work, examining various facets in detail. Section III delineates the notations and introduces essential background knowledge. Section IV presents a theoretical framework to deepen the understanding of SPTGNNS, addressing the research questions set forth. Section V showcases our theoretical insights through a novel and straightforward implementation known as TGGC, including its advanced variant TGGC†. Our research findings are evaluated and shared in Section VI, and a concise conclusion encapsulating our discoveries can be found in Section VII.
- p.4928 related_work: In this section, we provide a concise overview of pertinent literature, encompassing contemporary time series forecasting models, spatio-temporal graph neural networks, and recent advancements in spectral graph neural networks.
- p.4928 related_work: However, these methods struggle to model differently signed time series relations since their graph convolutions operate under the umbrella of message passing, which serves as low-pass filtering assuming local homophiles.
- p.4929 method: We address all research questions in this section.
- p.4932 method: In this section, we present a straightforward yet effective instantiation mainly based on the discussion in Section IV-C.
- p.4933 experiments: In this section, we evaluate the effectiveness and efficiency of our proposal on 8 real-world datasets by comparing TGGC and TGGC† with over 20 different baselines.
- p.4935 experiments: Our method consistently outperforms most baselines by significant margins.
- p.4937 conclusion: In this study, we provide the general formulation of spectral-temporal graph neural networks (SPTGNNS), laying down a theoretical framework for this category of methods.
- p.4937 conclusion: Both consistently surpass the majority of baseline methods across diverse real-world benchmarks.
- p.4937 conclusion: A limitation of our approach is that SPTGNNS may face challenges in handling specific types of time series data, such as the underlying graph topology is highly symmetric and node attributes exhibit strong non-stationary or non-periodic behavior.
- p.4937 conclusion: In addition to addressing this limitation, future research will also explore specific scenarios such as time-evolving graph structures and investigating the applicability of our theories to other tasks, such as time series classification and anomaly detection.
