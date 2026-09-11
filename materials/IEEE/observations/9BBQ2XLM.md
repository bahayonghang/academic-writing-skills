---
key: 9BBQ2XLM
title: "A$^{2}$RA-NSMTSllm: Adversarially Aligning Retrieval-Augmented LLMs for Nonstationary Multivariate Time Series Forecasting"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3631696"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PROPOSED METHOD` → `IV. EXPERIMENTS` → `V. CONCLUSION AND FUTURE WORK`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work。Introduction 末为 `Our contributions in this work are summarized as follows` + 编号。无 `The rest of this article is organized` 路标。Experiments 标题为 `EXPERIMENTS`。Conclusion 与 Future Work 并为一节。

## Openers

- abstract: `Multivariate time series` — "Multivariate time series (MTS) forecasting is critical in various real-world applications." (p.1805)
- introduction: `MULTIVARIATE time series` — "MULTIVARIATE time series (MTS) forecasting plays a critical role in numerous industrial applications." (p.1805)
- related_work: `Recently, the integration` — "Recently, the integration of LLMs into MTS forecasting has attracted widespread attention." (p.1806)
- method: `Following previous work` — "Following previous work, we measure nonstationarity via distributional statistics and employ the channel-independent strategy [22] for forecasting." (p.1807, III.A)
- experiments: `We evaluate the` — "We evaluate the effectiveness of A2RA-NSMTSllm on six real-world datasets: Solar [2], ETT (ETTm1, ETTm2, ETTh2) [10], weather [10], and ECL [10]." (p.1810)
- conclusion: `This article proposes` — "This article proposes A2RA-NSMTSllm for precise nonstationary MTS forecasting." (p.1815)

## Gap transitions

- however (abstract): "However, these methods often overlook the inherent nonstationarity and domain-specific nature of MTS, as well as the MTS-text modality representation gap, thus limiting the full potential of LLMs in MTS forecasting." (p.1805)
- to address (introduction): "To address these challenges, we propose a novel multiscale model that adversarially aligns retrieval-augmented LLMs for nonstationary MTS forecasting (A2RA-NSMTSllm)." (p.1806)
- despite (introduction): "Despite effective deployment in MTS forecasting, general-purpose pretrained LLMs struggle to comprehensively capture domain-specific temporal patterns." (p.1806)
- however (related_work): "However, the above-mentiond studies only consider a static scale for normalization and denormalization and are unable to comprehensively model the intricate distribution dynamics spanning various scales." (p.1807)

## Hedge verbs

- present / causal / abstract: "In this article, we present A2RA-NSMTSllm"
- propose / causal / introduction, conclusion: "we propose a novel multiscale model"; "This article proposes A2RA-NSMTSllm"
- show / causal / abstract: "Extensive experiments show that A2RA-NSMTSllm achieves superior forecasting performance"
- demonstrate / causal / introduction, conclusion: "Extensive experiments on various real-world benchmarks demonstrate that A2RA-NSMTSllm outperforms"; "A2RA-NSMTSllm demonstrates excellent performance"

## Cross-section linkers

- introduction → related_work: 贡献列表后直接 `II. RELATED WORK` (p.1806)
- related_work → method: 综述缺口后 `III. PROPOSED METHOD` (p.1807)
- method → experiments: 训练目标后 `IV. EXPERIMENTS` (p.1810)
- experiments → conclusion: 效率分析后 `V. CONCLUSION AND FUTURE WORK` (p.1815)

## Candidate rules

- R006 独立 Related Work。
- R004 贡献列表：`Our contributions in this work are summarized as follows.`
- R005 / 结论后续：`Moving forward, we will further optimize` / `an important direction for future work`。
- R009 结论 `This article proposes`。

## Candidate phrases

- `In this article, we present` (abstract)
- `To address these challenges, we propose` (introduction)
- `Our contributions in this work are summarized as follows.` (introduction)
- `This article proposes` (conclusion)

## House style

自称 `In this article, we present` / `we propose` / `this work` / `This article proposes`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1805 abstract: Multivariate time series (MTS) forecasting is critical in various real-world applications.
- p.1805 abstract: However, these methods often overlook the inherent nonstationarity and domain-specific nature of MTS, as well as the MTS-text modality representation gap, thus limiting the full potential of LLMs in MTS forecasting.
- p.1805 abstract: In this article, we present A2RA-NSMTSllm, a novel multiscale model that adversarially aligns retrieval-augmented LLMs for nonstationary MTS forecasting (A2RA-NSMTSllm).
- p.1805 abstract: Extensive experiments show that A2RA-NSMTSllm achieves superior forecasting performance and generalization, outperforming the latest CALF by 8.19%/5.27%, 11.01%/8.66%, and 20.94%/10.84% in MSE/MAE across full-shot, few-shot, and zero-shot scenarios.
- p.1805 introduction: MULTIVARIATE time series (MTS) forecasting plays a critical role in numerous industrial applications.
- p.1806 introduction: Despite effective deployment in MTS forecasting, general-purpose pretrained LLMs struggle to comprehensively capture domain-specific temporal patterns.
- p.1806 introduction: To address these challenges, we propose a novel multiscale model that adversarially aligns retrieval-augmented LLMs for nonstationary MTS forecasting (A2RA-NSMTSllm).
- p.1806 introduction: Our contributions in this work are summarized as follows.
- p.1806 related_work: Recently, the integration of LLMs into MTS forecasting has attracted widespread attention.
- p.1807 related_work: However, the above-mentiond studies only consider a static scale for normalization and denormalization and are unable to comprehensively model the intricate distribution dynamics spanning various scales.
- p.1807 method: Following previous work, we measure nonstationarity via distributional statistics and employ the channel-independent strategy [22] for forecasting.
- p.1810 experiments: We evaluate the effectiveness of A2RA-NSMTSllm on six real-world datasets: Solar [2], ETT (ETTm1, ETTm2, ETTh2) [10], weather [10], and ECL [10].
- p.1815 conclusion: This article proposes A2RA-NSMTSllm for precise nonstationary MTS forecasting.
- p.1815 conclusion: Experimentally, A2RA-NSMTSllm demonstrates excellent performance and generalization across various real-world benchmarks.
- p.1815 conclusion: Moving forward, we will further optimize the architecture of A2RA-NSMTSllm to reduce computational complexity without sacrificing prediction accuracy.
- p.1815 conclusion: Moreover, extending A2RA-NSMTSllm to general-domain MTS forecasting is also an important direction for future work.
