---
key: 9WTUALLC
title: "MetaIndux-TS: Frequency-Aware AIGC Foundation Model for Industrial Time Series"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2025.3577203"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`：generative foundation models / industrial time-series generators）。`related_work=independent`。Introduction 中段已列三条挑战。Introduction 贡献列表后直接进入 Related Work，未见 `The remainder of this article`。Experiments 标题为 `EXPERIMENTS`（CMAPSS + FEMTO）。

## Openers

- abstract: `Implementing advanced AI` — "Implementing advanced AI techniques in industrial manufacturing requires large volumes of annotated sensor data." (p.1)
- introduction: `IN RECENT years` — "IN RECENT years, artificial intelligence generated content (AIGC) technologies have made remarkable progress in various domains [1], [2], including computer vision (CV) [3], natural language processing (NLP) [4], [5], and audio [6], [7]." (p.1；栏首掉字)
- related_work: `The generative foundation` — "The generative foundation models relevant to our work are mainly based on diffusion probabilistic models, such as stable diffusion [20] and Sora [21]." (p.2, II.A)
- method: `This section briefly` — "This section briefly revisits the challenges introduced in Section I and presents the advantages of MetaIndux-TS in addressing these challenges." (p.2–3, III.A)
- experiments: `In order to` — "In order to generate industrial time series for different operating conditions and components, we collected a large dataset of over ten million sampling points, including turbofan engines and bearings in different degradation states." (p.6–7, IV.A)
- conclusion: `This article introduces` — "This article introduces MetaIndux-TS, a frequency-informed AIGC foundation model specifically designed for industrial time-series generation." (p.12)

## Gap transitions

- unfortunately (abstract): "Unfortunately, collecting such data is often impractical due to extreme environments and the manual burden of expert annotation." (p.1)
- however (abstract): "However, existing AIGC models encounter difficulties in generating industrial time series due to their complex temporal dynamics, multichannel intercolumn correlations, and diverse frequency characteristics." (p.1)
- to address (abstract): "To address these challenges, we propose MetaIndux-TS, a frequency-informed AIGC foundation model based on diffusion model frameworks." (p.1)
- despite (introduction): "Despite the significance of foundational generative models, industrial time series exhibit complex temporal dynamics and diverse frequency variables that current generative models struggle to synthesize with high fidelity." (p.1)
- however (related work): "However, they are constrained to single frequency and simple industrial signals, resulting in limited frequency perception and temporal dynamics patterns capturing capabilities." (p.2)
- however (conclusion): "However, MetaIndux-TS has limitations in generating time series that strictly adhere to the physical laws governing industrial equipment." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose MetaIndux-TS"; "A novel AIGC foundation model for industrial time series is proposed"
- show / causal / abstract: "Comprehensive experiments show that MetaIndux-TS outperforms state-of-the-art models"
- demonstrate / causal / experiments: "To demonstrate the significant advantages of our proposed method, we conduct experiments on industrial datasets"
- indicate / causal / experiments: "These results indicate that MetaIndux-TS is able to more accurately model the real data distribution"
- plan / speculative / conclusion: "we plan to explore methods for integrating physical constraints into generative models."

## Cross-section linkers

- introduction → related work: 贡献列表后直接 `II. RELATED WORKS`，无节序路标句 (p.2)
- related work → method: "We propose a channel-frequency attention mechanism to enhance feature representation for frequency-rich data and a temporal-frequency attention mechanism to capture both long-term degradation patterns and short-term variations." 随后 `III. METHODOLOGY` (p.2)
- method → experiments: 对比预测块后 `IV. EXPERIMENTS` (p.6)
- experiments → conclusion: 采样效率表后 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `To address these challenges, we propose` + 方法名，不用 `Here we`。
- R002 Introduction 有独立 Related Work；贡献列表后可直接进入 II，不一定写 remainder 路标。
- R003 贡献用 `Our contribution can be summarized as follows` + 编号列表。
- R004 Method 开篇用 `This section briefly revisits the challenges introduced in Section I`。
- R005 Conclusion 用 `This article introduces`，再用 `However, MetaIndux-TS has limitations` 指向物理约束。

## Candidate phrases

- `To address these challenges, we propose` (abstract)
- `Our contribution can be summarized as follows.` (introduction)
- `This section briefly revisits the challenges introduced in Section I` (method)
- `To demonstrate the significant advantages of our proposed method, we conduct experiments` (experiments)
- `This article introduces MetaIndux-TS, a frequency-informed AIGC foundation model` (conclusion)

## House style

自称是 `we propose` / `This article introduces` / `our proposed method` / `MetaIndux-TS`。未见 `Here we`。`This article introduces` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Implementing advanced AI techniques in industrial manufacturing requires large volumes of annotated sensor data.
- p.1 abstract: Unfortunately, collecting such data is often impractical due to extreme environments and the manual burden of expert annotation.
- p.1 abstract: However, existing AIGC models encounter difficulties in generating industrial time series due to their complex temporal dynamics, multichannel intercolumn correlations, and diverse frequency characteristics.
- p.1 abstract: To address these challenges, we propose MetaIndux-TS, a frequency-informed AIGC foundation model based on diffusion model frameworks.
- p.1 abstract: Comprehensive experiments show that MetaIndux-TS outperforms state-of-the-art models (SSSD, Dit, and TabDDPM), achieving a 57.5% improvement in fidelity and 20.4% in predictive score.
- p.1 introduction: IN RECENT years, artificial intelligence generated content (AIGC) technologies have made remarkable progress in various domains [1], [2], including computer vision (CV) [3], natural language processing (NLP) [4], [5], and audio [6], [7].
- p.1 introduction: Despite the significance of foundational generative models, industrial time series exhibit complex temporal dynamics and diverse frequency variables that current generative models struggle to synthesize with high fidelity.
- p.2 introduction: Our contribution can be summarized as follows.
- p.2 related work: The generative foundation models relevant to our work are mainly based on diffusion probabilistic models, such as stable diffusion [20] and Sora [21].
- p.2 related work: However, they are constrained to single frequency and simple industrial signals, resulting in limited frequency perception and temporal dynamics patterns capturing capabilities.
- p.3 method: This section briefly revisits the challenges introduced in Section I and presents the advantages of MetaIndux-TS in addressing these challenges.
- p.6 experiments: In order to generate industrial time series for different operating conditions and components, we collected a large dataset of over ten million sampling points, including turbofan engines and bearings in different degradation states.
- p.8 experiments: To demonstrate the significant advantages of our proposed method, we conduct experiments on industrial datasets and compare it with several state-of-the-art models.
- p.8 experiments: These results indicate that MetaIndux-TS is able to more accurately model the real data distribution and generate samples that are more similar.
- p.12 conclusion: This article introduces MetaIndux-TS, a frequency-informed AIGC foundation model specifically designed for industrial time-series generation.
- p.12 conclusion: However, MetaIndux-TS has limitations in generating time series that strictly adhere to the physical laws governing industrial equipment.
- p.12 conclusion: In the future, we plan to explore methods for integrating physical constraints into generative models.
