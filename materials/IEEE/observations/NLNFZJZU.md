---
key: NLNFZJZU
title: "A Graph Neural Network With Dual-Stage Feature Aggregation for Industrial Soft Sensors"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3606039"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PROPOSED METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（Section II）。Introduction 末有编号贡献与节序路标。Method 为 Section III。Experiments 标题为 `CASE STUDY`（废水 COD）。

## Openers

- abstract: `Soft sensing, as` — "Soft sensing, as a key engineering methodology, leverages readily accessible information from auxiliary variables to estimate hard-to-measure targets." (p.1)
- introduction: `UNLIKE traditional physical` — "UNLIKE traditional physical sensors, soft sensors overcome challenges such as high costs, maintenance issues, and degradation in harsh environments." (p.1；栏首掉字)
- method: `In this section` — "In this section, we present the overview of the proposed DA-GNN soft sensing model, which consists of three major parts, that is, the establishment of graph node subregions, neighborhood, and temporal feature aggregations." (p.3, III)
- experiments: `In this section` — "In this section, the effectiveness of the proposed DA-GNN model is evaluated through the soft sensing application of COD in a wastewater treatment process." (p.5, IV)
- conclusion: `This article proposes` — "This article proposes the DA-GNN model for industrial soft sensing, aimed at effectively capturing multivariate interdependence with different conduction scales." (p.8)

## Gap transitions

- however (abstract): "However, most multivariate data reside in structured spaces, where the interactions among different variables are accompanied by scale disparities, posing significant challenges to conventional neural networks." (p.1)
- in-response (abstract): "In response, we propose a novel graph neural network (GNN) with dual-stage feature aggregation (DA-GNN) for soft sensor modeling." (p.1)
- however (introduction): "However, most industrial multivariate data are located in structured, interacting systems." (p.1)
- nevertheless (introduction): "Nevertheless, existing graph-based soft sensing models often neglect the conduction scale differences of multivariate interactions, which impairs the understanding and perception of actual industrial processes." (p.2)
- inspired-by (introduction): "Inspired by the above observations, we propose a novel GNN based on dual-stage feature aggregation (DA-GNN)." (p.2)
- unlike (related work): "Unlike previous works, the proposed DA-GNN model leverages node subregions to capture multivariate local interdependencies along bidirectional dimensions" (p.3)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a novel graph neural network (GNN)"; "we propose a novel GNN based on dual-stage feature aggregation"
- validate / causal / abstract: "Its effectiveness is validated through comparative studies"
- present / causal / method: "we present the overview of the proposed DA-GNN soft sensing model"
- evaluate / causal / experiments: "the effectiveness of the proposed DA-GNN model is evaluated"
- plan / speculative / conclusion: "In future work, we plan to incorporate more novel graph sampling and aggregation schemes"

## Cross-section linkers

- introduction → related work: "The remainder of this article is structured as follows. Section II discusses related works. Section III provides a detailed explanation of the proposed method. Section IV carries out experiments on the industrial case. Section V summarizes the conclusions and outlines directions for future research." (p.2)
- related work → method: "Unlike previous works ..." 后接 `III. PROPOSED METHODOLOGY` (p.3)
- method → experiments: Algorithm 1 后接 `IV. CASE STUDY` (p.5)
- experiments → conclusion: 消融/可行性段落后接 `V. CONCLUSION` (p.8)

## Candidate rules

- R001 abstract 缺口用 `However` + `In response, we propose`。
- R002 独立 Related Works；贡献用 `In summary, our main contributions are as follows`。
- R003 Introduction 末用 `The remainder of this article is structured as follows` 指向 II–V。
- R004 Experiments 标题为 `CASE STUDY`，开篇 `In this section, the effectiveness of the proposed ... is evaluated`。
- R005 Conclusion 用 `This article proposes`，再用 `In future work, we plan to`。

## Candidate phrases

- `In response, we propose a novel` (abstract)
- `Inspired by the above observations, we propose` (introduction)
- `In summary, our main contributions are as follows.` (introduction)
- `The remainder of this article is structured as follows.` (introduction)
- `This article proposes the DA-GNN model` (conclusion)

## House style

自称是 `we propose` / `This article proposes` / `our main contributions` / `the proposed DA-GNN` / `this article`。未见 `Here we`。`we propose` 与 `This article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Soft sensing, as a key engineering methodology, leverages readily accessible information from auxiliary variables to estimate hard-to-measure targets.
- p.1 abstract: However, most multivariate data reside in structured spaces, where the interactions among different variables are accompanied by scale disparities, posing significant challenges to conventional neural networks.
- p.1 abstract: In response, we propose a novel graph neural network (GNN) with dual-stage feature aggregation (DA-GNN) for soft sensor modeling.
- p.1 abstract: Its effectiveness is validated through comparative studies with some classical and advanced algorithms.
- p.1 introduction: UNLIKE traditional physical sensors, soft sensors overcome challenges such as high costs, maintenance issues, and degradation in harsh environments.
- p.1 introduction: However, most industrial multivariate data are located in structured, interacting systems.
- p.2 introduction: Nevertheless, existing graph-based soft sensing models often neglect the conduction scale differences of multivariate interactions, which impairs the understanding and perception of actual industrial processes.
- p.2 introduction: Inspired by the above observations, we propose a novel GNN based on dual-stage feature aggregation (DA-GNN).
- p.2 introduction: In summary, our main contributions are as follows.
- p.2 introduction: The remainder of this article is structured as follows. Section II discusses related works. Section III provides a detailed explanation of the proposed method. Section IV carries out experiments on the industrial case. Section V summarizes the conclusions and outlines directions for future research.
- p.3 related work: Unlike previous works, the proposed DA-GNN model leverages node subregions to capture multivariate local interdependencies along bidirectional dimensions and incorporates a gated recurrent module in the graph space to aggregate holistic temporal features of each variable node.
- p.3 method: In this section, we present the overview of the proposed DA-GNN soft sensing model, which consists of three major parts, that is, the establishment of graph node subregions, neighborhood, and temporal feature aggregations.
- p.5 experiments: In this section, the effectiveness of the proposed DA-GNN model is evaluated through the soft sensing application of COD in a wastewater treatment process.
- p.8 conclusion: This article proposes the DA-GNN model for industrial soft sensing, aimed at effectively capturing multivariate interdependence with different conduction scales.
- p.8 conclusion: Its effectiveness and industrial applicability are validated through comparative studies with multiple baseline models and detailed feasibility analyses.
- p.8 conclusion: In future work, we plan to incorporate more novel graph sampling and aggregation schemes to ensure adaptability.
