---
key: UQ9UDP8V
title: "SageFormer: Series-Aware Framework for Long-Term Multivariate Time-Series Forecasting"
venue: "IEEE Internet of Things Journal"
doi: "10.1109/JIOT.2024.3363451"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`，含 MTS forecasting / Transformers / inter-series dependencies）。Introduction 末用编号问题 + `Our contributions are threefold`。Method 为 III。Experiments 标题为 `EXPERIMENTS`（真实与合成数据集）。作者稿页码为连续阿拉伯数字。PDF 题名作 `Long-Term Multivariate Time Series Forecasting`（无连字符 Time-Series）。

## Openers

- abstract: `In the burgeoning` — "In the burgeoning ecosystem of Internet of Things, multivariate time series (MTS) data has become ubiquitous, highlighting the fundamental role of time series forecasting across numerous applications." (p.1)
- introduction: `WITH THE rise` — "WITH THE rise of the Internet of Things (IoT), an ever-increasing number of interconnected devices have found their way into our daily lives, from smart homes and industries to healthcare and urban planning [1]." (p.1)
- related_work: `MTS forecasting models` — "MTS forecasting models can generally be categorized into statistical and deep models." (p.2, II.A)
- method: `In this paper` — "In this paper, we concentrate on long-term MTS forecasting tasks." (p.3, III.A)
- experiments: `To evaluate our` — "To evaluate our proposed series-aware framework and SageFormer, extensive experiments have been conducted on six mainstream real-world datasets, including Weather, Traffic, Electricity, ILI(Influenza-Like Illness), and four ETT(Electricity Transformer Temperature) datasets and two synthetic datasets (see Section IV-E)." (p.5, IV.A)
- conclusion: `This paper presented` — "This paper presented the series-aware framework and SageFormer, a novel approach for modeling both intra- and inter-series dependencies in long-term MTS forecasting tasks." (p.11, V)

## Gap transitions

- however (abstract): "However, many prevailing methods either marginalize inter-series dependencies or overlook them entirely." (p.1)
- however (introduction): "However, within these temporal embeddings, inter-series dependencies are not explicitly modeled, leading to inefficiencies in information extraction [12]." (p.1)
- however (introduction): "However, this approach can be suboptimal for certain datasets for completely overlooking inter-series dependencies (see section IV-E0a)." (p.1)
- unlike (related_work): "Unlike the methods mentioned above, our proposed framework serves as a general framework that can be applied to various Transformer-based models" (p.3)

## Hedge verbs

- introduce / causal / abstract, introduction: "this paper introduces a novel series-aware framework"; "We introduce the series-aware framework"
- contend / speculative / introduction: "We contend that the proposed SageFormer addresses two challenges in long-term inter-series dependencies modeling"
- demonstrate / causal / experiments: "Our method consistently improves the forecasting ability of different models, demonstrating that the proposed series-aware framework is an effective, universally applicable framework."
- present / causal / conclusion: "This paper presented the series-aware framework and SageFormer"

## Cross-section linkers

- introduction → related_work: 贡献段落后直接 `II. RELATED WORKS` (p.2)
- related_work → method: "our proposed framework serves as a general framework that can be applied to various Transformer-based models" 随后 `III. METHODOLOGY` (p.3)
- method → experiments: 消息传递段落后直接 `IV. EXPERIMENTS` (p.5)
- experiments → conclusion: 效率分析后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 缺口用 `To bridge this gap, this paper introduces`。
- R002 独立 `II. RELATED WORKS`，按 MTS / Transformers / inter-series 分子节。
- R003 Introduction 贡献用 `Our contributions are threefold:` 一段收束，不用编号列表。
- R004 Conclusion 先收回框架与模型，再用 `We also acknowledged the limitations of our work and briefly delineated potential avenues for future research.`

## Candidate phrases

- `To bridge this gap, this paper introduces` (abstract)
- `we introduce the “series-aware framework”` (introduction)
- `Our contributions are threefold:` (introduction)
- `To evaluate our proposed series-aware framework and SageFormer, extensive experiments have been conducted on` (experiments)
- `This paper presented the series-aware framework and SageFormer` (conclusion)

## House style

自称是 `this paper introduces` / `we introduce` / `Our contributions` / `our proposed SageFormer`。未见 `Here we`。`this paper introduces` 与 `we introduce` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 作为摘要首句；方法节有 `In this paper, we concentrate`。

## Quotes

- p.1 abstract: In the burgeoning ecosystem of Internet of Things, multivariate time series (MTS) data has become ubiquitous, highlighting the fundamental role of time series forecasting across numerous applications.
- p.1 abstract: However, many prevailing methods either marginalize inter-series dependencies or overlook them entirely.
- p.1 abstract: To bridge this gap, this paper introduces a novel series-aware framework, explicitly designed to emphasize the significance of such dependencies.
- p.1 abstract: Extensive experiments on real-world and synthetic datasets validate the superior performance of SageFormer against contemporary state-of-the-art approaches.
- p.1 introduction: WITH THE rise of the Internet of Things (IoT), an ever-increasing number of interconnected devices have found their way into our daily lives, from smart homes and industries to healthcare and urban planning [1].
- p.1 introduction: However, within these temporal embeddings, inter-series dependencies are not explicitly modeled, leading to inefficiencies in information extraction [12].
- p.1 introduction: In this paper, we introduce the “series-aware framework” (Fig. 1a) to bridge this research gap.
- p.2 introduction: Our contributions are threefold: First, we unveil the series-aware framework, a novel extension for Transformer-based models, utilizing global tokens to effectively exploit inter-series dependencies without adding undue complexity.
- p.2 related_work: MTS forecasting models can generally be categorized into statistical and deep models.
- p.3 related_work: Unlike the methods mentioned above, our proposed framework serves as a general framework that can be applied to various Transformer-based models, utilizing graph structures to enhance their ability to represent inter-series dependencies.
- p.3 method: In this paper, we concentrate on long-term MTS forecasting tasks.
- p.5 experiments: To evaluate our proposed series-aware framework and SageFormer, extensive experiments have been conducted on six mainstream real-world datasets, including Weather, Traffic, Electricity, ILI(Influenza-Like Illness), and four ETT(Electricity Transformer Temperature) datasets and two synthetic datasets (see Section IV-E).
- p.6 experiments: Overall, the forecasting results presented distinctly highlight the superior performance of our proposed SageFormer when compared to other baseline models.
- p.11 conclusion: This paper presented the series-aware framework and SageFormer, a novel approach for modeling both intra- and inter-series dependencies in long-term MTS forecasting tasks.
- p.11 conclusion: Our model has demonstrated impressive versatility through extensive experimentation, delivering state-of-the-art performance on real-world and synthetic datasets.
- p.11 conclusion: We also acknowledged the limitations of our work and briefly delineated potential avenues for future research.
