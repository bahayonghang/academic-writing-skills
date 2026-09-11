---
key: 7G9ZT3NG
title: "LSTM and Transformer-based framework for bias correction of ERA5 hourly wind speeds"
venue: "Energy"
doi: "10.1016/j.energy.2025.136498"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work` → `3. Dataset` → `4. Method` → `5. Results` → `6. Discussion` → `7. Conclusion`。前置 `ABSTRACT` / `Keywords` / `Abbreviation`。独立 Related Work：`2. Related work`。Introduction 无编号贡献列表，有节序路标。Method 分 time-invariant scaling 与 time-resolved LSTM/Transformer。Experiments 标题为 `5. Results`（170 个独立测站），其后独立 `6. Discussion`。

## Openers

- abstract: `Reanalysis-derived wind` — "Reanalysis-derived wind speeds are central to large-scale wind resource assessment (WRA)."
- introduction: `Addressing climate change` — "Addressing climate change and mitigating its risks to humanity requires significantly expanding renewable energy sources, such as wind and solar, to replace fossil fuel-based energy systems."
- related_work: `Various techniques for` — "Various techniques for BC of reanalysis-derived wind speeds have been explored in the literature."
- method: `The study flow diagram` — "The study flow diagram is illustrated in Fig. 2 and includes the following main steps:"
- experiments: `This section presents` — "This section presents the results of the evaluation of the BC methods."
- conclusion: `Wind speeds derived` — "Wind speeds derived from modern reanalysis datasets have become central to large-scale WRA studies due to their global coverage, extensive record length, and consistent records."

## Gap transitions

- however (abstract): "However, their coarse spatial resolution often introduces significant biases, particularly in complex terrains and coastal areas."
- to the authors' knowledge (introduction): "To the authors' knowledge, no previous attempts have been made to use ML to directly predict a scaling factor that could adjust the long-term mean wind speed from reanalysis data."
- while (introduction): "While a time-invariant scaling factor can improve reanalysis data's long-term mean wind speed, it does not modify its temporal variability."
- additionally (related work): "Additionally, a novel DL framework is introduced for BC of reanalysis-derived wind speeds."

## Hedge verbs

- was introduced / causal / abstract: "A deep learning (DL) framework using LSTMs or Transformers was introduced to correct systematic biases"
- introduces / causal / introduction: "This paper introduces an innovative ML framework for predicting time-invariant and time-resolved scaling factors"
- showed / associative / abstract: "Results showed that the DL framework outperformed a standard bias correction method based on the Global Wind Atlas."
- was proposed / causal / conclusion: "A novel bias correction method using DL models for sequence modeling was proposed and evaluated across Canada."
- indicate / associative / conclusion: "Results from comprehensive evaluations indicate that this framework significantly improves ERA5 wind speeds at most test stations"

## Cross-section linkers

- introduction → related_work: "In the following sections, a survey of related work is presented (Section 2), followed by a description of the dataset (Section 3), the methodology (Section 4), and the presentation of the results (Section 5), which are discussed in Section 6."
- related_work → dataset: 框架陈述后 `3. Dataset`
- dataset → method: 静态协变量后 `4. Method`
- method → results: 评估指标后 `5. Results`
- results → discussion: 分位数评估后 `6. Discussion`
- discussion → conclusion: 离岸局限后 `7. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Related work`（位于 Introduction 之后、Dataset 之前）。
- R003 节序路标：`In the following sections, a survey of related work is presented (Section 2)`
- R009 自称：`This paper introduces` / `was proposed` / `To the authors' knowledge`
- R020 Results 与 Discussion 分节。

## Candidate phrases

- `This paper introduces an innovative ML framework` (introduction)
- `To the authors' knowledge, no previous attempts have been made` (introduction)
- `In the following sections, a survey of related work is presented` (introduction)
- `This section presents the results of the evaluation of the BC methods` (results)
- `A novel bias correction method using DL models for sequence modeling was proposed` (conclusion)

## House style

自称 `This paper introduces` / `was introduced` / `was proposed` / `To the authors' knowledge`。被动提出为主，夹第一人称。进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- abstract: Reanalysis-derived wind speeds are central to large-scale wind resource assessment (WRA).
- abstract: However, their coarse spatial resolution often introduces significant biases, particularly in complex terrains and coastal areas.
- abstract: Specifically, in coastal regions, the DL models increased the explained variability of median wind speed by over 70 % relative to ERA5.
- introduction: Addressing climate change and mitigating its risks to humanity requires significantly expanding renewable energy sources, such as wind and solar, to replace fossil fuel-based energy systems.
- introduction: This paper introduces an innovative ML framework for predicting time-invariant and time-resolved scaling factors for BC of reanalysis-derived wind speeds.
- introduction: In the following sections, a survey of related work is presented (Section 2), followed by a description of the dataset (Section 3), the methodology (Section 4), and the presentation of the results (Section 5), which are discussed in Section 6.
- related_work: Various techniques for BC of reanalysis-derived wind speeds have been explored in the literature.
- experiments: This section presents the results of the evaluation of the BC methods.
- experiments: The TR-LSTM and TR-Transformer emerged as the top performers, achieving the lowest median MAE and RMSE values and the highest median PCC.
- conclusion: A novel bias correction method using DL models for sequence modeling was proposed and evaluated across Canada.
- conclusion: Results from comprehensive evaluations indicate that this framework significantly improves ERA5 wind speeds at most test stations, performing particularly well in high SRL areas such as forest and urban regions.
- conclusion: Overall, this framework represents a promising advancement in improving the accuracy of reanalysis-derived wind data for WRA studies, helping to reduce uncertainties in predicting energy yields.
