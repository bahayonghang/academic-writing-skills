---
key: S7CJ6P6M
title: "AFEformer: An adaptive frequency enhancement transformer for time series prediction"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2025.112736"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2` Related work（`2.1` Transformer 时序模型；`2.2` 时频域学习） → `3. Methodology` → `4. Experiment` → `5. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。独立 Related Work。Introduction 末有编号贡献 (a)(b)…。Experiments 含九数据集、消融、可视化、复杂度与噪声鲁棒性。

## Openers

- abstract: `Long-term time series` — "Long-term time series forecasting (LTSF), as a key research domain with pervasive applications in real-world scenarios, has garnered sustained interest from both academic and industrial communities."
- introduction: `Time Series Forecasting` — "Time Series Forecasting (TSF) occupies a significant role in data analysis, covering various vital aspects of our daily lives, including energy consumption (Ahmad et al., 2014), transportation planning (He et al., 2022), economic forecasting (Ariyo et al., 2014), weather forecasting (Wu et al., 2023; Zhang et al., 2023), and disease transmission forecasting (Bertozzi et al., 2020)."
- related_work: `In order to` — "In order to more thoroughly reveal the periodic characteristics and frequency components in time series data, we employ frequency domain analysis methods." (s.2.2)
- method: `To enhance the` — "To enhance the performance of long-term forecasting, we propose the AFEformer model, which strengthens key features through feature enhancement techniques in the frequency domain and automatically adapts and learns position information in sequences through the temporal external attention enhancement module (TEAEM), improving long-term prediction capabilities while maintaining linear complexity."
- experiments: `To comprehensively evaluate` — "To comprehensively evaluate the performance and practical value of AFEformer, we carefully selected nine real-world time series forecasting benchmarks for experiments, covering five domains: energy, transportation, economics, weather and disease (Nespoli et al., 2019; Wu et al., 2019)."
- conclusion: `In this comprehensive` — "In this comprehensive study, we introduce AFEformer, an innovative and adaptive frequency enhancement Transformer model designed specifically for long-term time series forecasting."

## Gap transitions

- although (abstract): "Although transformer-based models have demonstrated high predictive capability in capturing long-term temporal dependencies, most of them directly process raw data in the time domain while ignoring the representation of features in the frequency domain."
- to address (abstract): "To address these issues, we innovatively design an adaptive frequency enhancement transformer (AFEformer) with temporal external attention for time series forecasting, which focuses on enhancing important frequency domain features to provide more accurate forecasting."
- however (introduction): "However, there are still some unresolved issues: Firstly, time series can be represented in both the time domain and the frequency domain, yet most existing transformers have overlooked frequency domain information."
- to address (introduction): "To address these limitations, we propose an adaptive frequency enhancement Transformer(AFEformer) with temporal external attention, aimed at achieving robust and efficient long-term time series forecasting with adaptive feature enhancement capabilities to achieve high prediction accuracy."
- although (related_work): "Although previous models have made some progress in accuracy, they rely on subjectively set parameters to filter dominant frequencies, a practice lacking solid statistical theoretical support, which limits the further improvement of model performance."

## Hedge verbs

- design / causal / abstract: "we innovatively design an adaptive frequency enhancement transformer (AFEformer)"
- propose / causal / introduction, method: "we propose an adaptive frequency enhancement Transformer(AFEformer)"; "we propose the AFEformer model"
- demonstrate / associative / abstract, conclusion: "comprehensive experiments demonstrate that AFEformer achieves state-of-the-art forecasting performance"; "we demonstrate that AFEformer consistently outperforms existing TSF methods"
- introduce / causal / conclusion: "we introduce AFEformer"

## Cross-section linkers

- introduction → related_work: 贡献清单后进入第 2 节
- related_work → method: 频域增强动机后 `3. Methodology`
- method → experiments: 复杂度分析后 `4. Experiment`
- experiments → conclusion: 噪声鲁棒性讨论后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work，分子节对比 Transformer 与时频方法。
- R004 编号贡献：`The main contributions of this paper are as follows.`
- R009 自称：`we propose` / `we introduce`

## Candidate phrases

- `To address these issues, we innovatively design` (abstract)
- `To address these limitations, we propose` (introduction)
- `The main contributions of this paper are as follows` (introduction)
- `In this comprehensive study, we introduce` (conclusion)

## House style

自称 `we propose` / `we introduce` / `our proposed AFEformer`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Long-term time series forecasting (LTSF), as a key research domain with pervasive applications in real-world scenarios, has garnered sustained interest from both academic and industrial communities.
- abstract: Although transformer-based models have demonstrated high predictive capability in capturing long-term temporal dependencies, most of them directly process raw data in the time domain while ignoring the representation of features in the frequency domain.
- abstract: To address these issues, we innovatively design an adaptive frequency enhancement transformer (AFEformer) with temporal external attention for time series forecasting, which focuses on enhancing important frequency domain features to provide more accurate forecasting.
- abstract: Regarding long-term forecasting, comprehensive experiments demonstrate that AFEformer achieves state-of-the-art forecasting performance on nine time series forecasting benchmarks.
- introduction: Time Series Forecasting (TSF) occupies a significant role in data analysis, covering various vital aspects of our daily lives, including energy consumption (Ahmad et al., 2014), transportation planning (He et al., 2022), economic forecasting (Ariyo et al., 2014), weather forecasting (Wu et al., 2023; Zhang et al., 2023), and disease transmission forecasting (Bertozzi et al., 2020).
- introduction: To address these limitations, we propose an adaptive frequency enhancement Transformer(AFEformer) with temporal external attention, aimed at achieving robust and efficient long-term time series forecasting with adaptive feature enhancement capabilities to achieve high prediction accuracy.
- introduction: The main contributions of this paper are as follows.
- method: To enhance the performance of long-term forecasting, we propose the AFEformer model, which strengthens key features through feature enhancement techniques in the frequency domain and automatically adapts and learns position information in sequences through the temporal external attention enhancement module (TEAEM), improving long-term prediction capabilities while maintaining linear complexity.
- experiments: To comprehensively evaluate the performance and practical value of AFEformer, we carefully selected nine real-world time series forecasting benchmarks for experiments, covering five domains: energy, transportation, economics, weather and disease (Nespoli et al., 2019; Wu et al., 2019).
- conclusion: In this comprehensive study, we introduce AFEformer, an innovative and adaptive frequency enhancement Transformer model designed specifically for long-term time series forecasting.
- conclusion: Through a series of comprehensive experiments conducted on real-world datasets, we demonstrate that AFEformer consistently outperforms existing TSF methods in long-term forecasting tasks, highlighting its superiority and robustness.
