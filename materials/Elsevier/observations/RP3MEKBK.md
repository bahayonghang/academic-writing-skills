---
key: RP3MEKBK
title: "ADMNet: An adaptive downsampling multi-frequency multi-channel network for long-term time series forecasting"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2024.125588"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work`（`2.1. Time series forecasting` / `2.2. Convolutional neural networks`）→ `3. Methodology` → `4. Experiment` → `5. Conclusion`。前置 `ABSTRACT` 与 `Keywords`。独立 Related Work。`related_work=independent`。Introduction 末有条目贡献列表；未见 `The rest of this paper is organized as follows` 路标。Experiments 标题为 `Experiment`。

## Openers

- abstract: `Long-term time series` — "Long-term time series forecasting finds widespread applications in various domains such as energy, finance, and transportation."
- introduction: `Time series forecasting` — "Time series forecasting is a critical data analysis technique that involves analyzing and modeling historical data to predict future trends and behaviors."
- related_work: `Time series data` — "Time series data is typically arranged in chronological order and exhibits temporal dependencies."
- method: `This paper introduces` — "This paper introduces a time series forecasting method named ADMNet, designed to flexibly capture different cycle features in time series for more effective decomposition."
- experiments: `In this section,` — "In this section, we introduce the datasets, evaluation metrics, comparative models, comparative experiments and their visualization used in this study."
- conclusion: `This paper proposes` — "This paper proposes an Adaptive Down-sampling Multi-frequency Multi-channel Network (ADMNet) for effective utilization of the multiple periodicities present in time series data."

## Gap transitions

- however (abstract): "However, conventional decomposition techniques often rely on fixed-size parameter kernels for sliding averages, leading to inaccurate and unreasonable captures of the underlying periodicities in the time series."
- however (introduction): "However, it is essential to note that the computational nature of self-attention mechanisms introduces the challenge of quadratic time complexity."
- to overcome (introduction): "To overcome this limitation, we propose an enhanced adaptive periodic feature recognizer, which can automatically identify multiple periods in a time series."
- in summary (introduction): "In summary, the main contributions of this paper are as follows:"

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose an enhanced adaptive cyclic feature recognizer"; "This paper proposes an Adaptive Down-sampling Multi-frequency Multi-channel Network (ADMNet)"
- show / associative / abstract, experiments: "Experimental results show that, compared to the current state-of-the-art seven benchmark models, the proposed model achieves an average reduction in mean squared error (MSE) ranging from 6.19% to 22.75%"
- demonstrate / associative / conclusion: "Experimental results demonstrate that ADMNet outperforms state-of-the-art methods on multiple datasets."

## Cross-section linkers

- introduction → related_work: 贡献列表后直接 `2. Related work`
- related_work → method: `3. Methodology`
- method → experiments: `4. Experiment` / "In this section, we introduce the datasets, evaluation metrics, comparative models"
- experiments → conclusion: DJIA 应用段落后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work（`2. Related work`）。
- R004 条目贡献：`the main contributions of this paper are as follows`
- R009 自称：`This paper proposes` / `we propose` / `we introduce`

## Candidate phrases

- `To accurately and flexibly capture the periodicities of time series, we propose` (abstract)
- `To overcome this limitation, we propose` (introduction)
- `In summary, the main contributions of this paper are as follows` (introduction)
- `This paper introduces a time series forecasting method named ADMNet` (method)
- `This paper proposes an Adaptive Down-sampling Multi-frequency Multi-channel Network (ADMNet)` (conclusion)

## House style

自称 `we propose` / `we introduce` / `This paper proposes`。实验节用 `we introduce` / `we conduct`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Long-term time series forecasting finds widespread applications in various domains such as energy, finance, and transportation.
- abstract: However, conventional decomposition techniques often rely on fixed-size parameter kernels for sliding averages, leading to inaccurate and unreasonable captures of the underlying periodicities in the time series.
- abstract: To accurately and flexibly capture the periodicities of time series, we propose an enhanced adaptive cyclic feature recognizer to automatically identify the periodic lengths for sliding average parameter kernel sizing.
- abstract: Experimental results show that, compared to the current state-of-the-art seven benchmark models, the proposed model achieves an average reduction in mean squared error (MSE) ranging from 6.19% to 22.75% across eight datasets, including ETT, Traffic, and Weather.
- introduction: Time series forecasting is a critical data analysis technique that involves analyzing and modeling historical data to predict future trends and behaviors.
- introduction: To overcome this limitation, we propose an enhanced adaptive periodic feature recognizer, which can automatically identify multiple periods in a time series.
- introduction: In summary, the main contributions of this paper are as follows:
- related_work: Time series data is typically arranged in chronological order and exhibits temporal dependencies.
- method: This paper introduces a time series forecasting method named ADMNet, designed to flexibly capture different cycle features in time series for more effective decomposition.
- experiments: In this section, we introduce the datasets, evaluation metrics, comparative models, comparative experiments and their visualization used in this study.
- conclusion: This paper proposes an Adaptive Down-sampling Multi-frequency Multi-channel Network (ADMNet) for effective utilization of the multiple periodicities present in time series data.
- conclusion: Experimental results demonstrate that ADMNet outperforms state-of-the-art methods on multiple datasets.
