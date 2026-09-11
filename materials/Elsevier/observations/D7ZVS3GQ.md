---
key: D7ZVS3GQ
title: "CrossWaveNet: A dual-channel network with deep cross-decomposition for Long-term Time Series Forecasting"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2023.121642"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work`（`2.1. RNNs family` / `2.2. Decomposition of time series`）→ `3. Methodology` → `4. Experiment` → `5. Conclusion`。前置 `ABSTRACT` 与 `Keywords`。独立 Related Work。`related_work=independent`。Introduction 末有条目贡献。未见 `The rest of this paper is organized as follows` 路标。Experiments 标题为 `Experiment`。

## Openers

- abstract: `Many real-world applications` — "Many real-world applications require predicting data changes over a longer period, such as early warning for energy consumption and long-term planning for transportation."
- introduction: `Time Series Forecasting` — "Time Series Forecasting (TSF) refers to predicting the future data changes over a certain period of time-based on historical data, and it has widespread applications in various real-life domains such as energy consumption (Bianco et al., 2009), traffic planning (Lv et al., 2014), economic forecasting (Liu et al., 2022), weather forecasting (Alley et al., 2019), and disease spread (Mandal et al., 2020)."
- related_work: `Many practical applications` — "Many practical applications require Long-Term Time Series Forecasting (LTSF), such as early warning systems for energy and traffic planning."
- method: `This paper proposes` — "This paper proposes a long-term time series forecasting method called CrossWaveNet to better capture long-term dependencies."
- experiments: `To demonstrate the` — "To demonstrate the effectiveness of CrossWaveNet, we evaluated the model on six real-world benchmark datasets that cover five major time series domains:"
- conclusion: `In conclusion, this` — "In conclusion, this paper presents CrossWaveNet, a model designed for long-term time series forecasting."

## Gap transitions

- however (abstract): "However, the inherent nature of the permutation-invariant self-attention mechanism in Transformers can lead to the loss of certain temporal patterns."
- therefore (abstract): "Therefore, we propose a dual-channel network with deep cross-decomposition for LTSF, called CrossWaveNet."
- hence (introduction): "Hence, a requirement arises for straightforward and efficient models to recognize and extract temporal dependencies, facilitating more precise predictions of long-term time series patterns and trends."
- in this paper (related_work): "In this paper, we introduce a novel architecture distinct from previous methods for long-term forecasting, referred to as the Dual-Channel Network with Deep Cross-Decomposition."

## Hedge verbs

- propose / causal / abstract, method: "we propose a dual-channel network with deep cross-decomposition"; "This paper proposes a long-term time series forecasting method called CrossWaveNet"
- present / causal / conclusion: "this paper presents CrossWaveNet"
- demonstrate / associative / introduction, conclusion: "Experimental results on six real-world time series datasets demonstrate that CrossWaveNet significantly outperforms state-of-the-art methods"; "Experimental results demonstrate that CrossWaveNet achieves excellent predictive performance"

## Cross-section linkers

- introduction → related_work: 贡献列表后 `2. Related work`
- related_work → method: `3. Methodology`
- method → experiments: `4. Experiment` / `4.1. Dataset description`
- experiments → conclusion: 频率特征基准段落后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work（`2. Related work`）。
- R004 条目贡献：`The contributions can be summarized as follows`
- R009 自称：`Therefore, we propose` / `This paper proposes` / `this paper presents`

## Candidate phrases

- `Therefore, we propose a dual-channel network with deep cross-decomposition` (abstract)
- `The contributions can be summarized as follows` (introduction)
- `This paper proposes a long-term time series forecasting method called CrossWaveNet` (method)
- `To demonstrate the effectiveness of CrossWaveNet, we evaluated the model` (experiments)
- `In conclusion, this paper presents CrossWaveNet` (conclusion)

## House style

自称 `we propose` / `This paper proposes` / `this paper presents`。结论用 `In conclusion`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Many real-world applications require predicting data changes over a longer period, such as early warning for energy consumption and long-term planning for transportation.
- abstract: However, the inherent nature of the permutation-invariant self-attention mechanism in Transformers can lead to the loss of certain temporal patterns.
- abstract: Therefore, we propose a dual-channel network with deep cross-decomposition for LTSF, called CrossWaveNet.
- abstract: Compared with the state-of-the-art methods in long-term forecasting, CrossWaveNet has achieved the highest prediction accuracy and significant relative performance improvement in fields such as energy, transportation, weather, and disease transmission.
- introduction: Time Series Forecasting (TSF) refers to predicting the future data changes over a certain period of time-based on historical data, and it has widespread applications in various real-life domains such as energy consumption (Bianco et al., 2009), traffic planning (Lv et al., 2014), economic forecasting (Liu et al., 2022), weather forecasting (Alley et al., 2019), and disease spread (Mandal et al., 2020).
- introduction: The contributions can be summarized as follows:
- related_work: Many practical applications require Long-Term Time Series Forecasting (LTSF), such as early warning systems for energy and traffic planning.
- related_work: In this paper, we introduce a novel architecture distinct from previous methods for long-term forecasting, referred to as the Dual-Channel Network with Deep Cross-Decomposition.
- method: This paper proposes a long-term time series forecasting method called CrossWaveNet to better capture long-term dependencies.
- experiments: To demonstrate the effectiveness of CrossWaveNet, we evaluated the model on six real-world benchmark datasets that cover five major time series domains:
- conclusion: In conclusion, this paper presents CrossWaveNet, a model designed for long-term time series forecasting.
- conclusion: Experimental results demonstrate that CrossWaveNet achieves excellent predictive performance on multiple time series datasets, outperforming state-of-the-art methods in terms of accuracy and robustness.
