---
key: BITTP4Z9
title: "Multiscale Information Granule-Based Time Series Forecasting Model With Two-Stage Prediction Mechanism"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2024.3502775"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8,12-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. MSIG-BASED TWO-STAGE PREDICTION MECHANISM` → `IV` experiments（含 case study / 对比 / 消融）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 为 MSIG 两阶段预测。Experiments 含 ETTh1 case study、常规数据集对比、效率与消融。

## Openers

- abstract: `Impressive advancements have` — "Impressive advancements have been achieved in utilizing information granulation for solving long-term time series prediction problems." (p.982)
- introduction: `TIME series prediction` — "TIME series prediction is an intricate process that analyzes the information correlations between current and historical data to forecast future behavior." (p.982)
- related_work: `In this section,` — "In this section, we review the literature on time series prediction, focusing on the long-term prediction, information granule-based prediction, and multiscale prediction models." (p.983, II)
- method: `In this section,` — "In this section, the MSIG-based two-stage prediction mechanism is introduced in detail." (p.984, III)
- experiments: `To assess the effectiveness` — "To assess the effectiveness of MSIG, we conducted comprehensive experiments on five datasets from real-world scenarios." (p.989, IV.C)
- conclusion: `In this article,` — "In this article, an MSIG-based two-stage prediction mechanism is proposed." (p.994)

## Gap transitions

- however (abstract): "However, most state-of-the-art methods suffer from limitations due to not only using the single-scale information granulation but also the lack of trend information." (p.982)
- to address (abstract): "To address these problems, this article proposes a multiscale information granule-based time series forecasting model." (p.982)
- although (introduction): "Although these models have achieved good performance in short-term prediction, cumulative errors are inevitable for long-term forecasting." (p.982)
- however (introduction): "However, these models in fact iteratively generate long-term forecast values, which can affect the prediction performance." (p.982)
- however (related_work): "However, these methods still face challenges in capturing and leveraging the long-term dependencies." (p.984)
- although (related_work): "Although these methods have shown the benefits of the information granules in time series prediction, they do not make use of dynamic change and multiscale features of time series efficiently." (p.984)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a multiscale information granule-based time series forecasting model"; "an MSIG-based two-stage prediction mechanism is proposed"
- show / causal / abstract: "Comparative analysis shows that the proposed method outperforms existing numeric models and granular models"
- can / speculative / introduction: "information granule-based methods can offer enhanced accuracy and efficiency in prediction"
- demonstrate / causal / experiments: "This demonstrates that trend-based information granulation contributes significantly to improving prediction performance"
- would / speculative / conclusion: "An interesting appealing direction would be to explore more diversified information granules"

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. Section II reviews the related work of information granule-based prediction models and multiscale prediction models. Section III presents the specific implementation process of the proposed prediction model. The experimental results and comparison are carried out in Section IV. Finally, Section V concludes this article and gives future directions of this study." (p.983)
- related_work → method: "In this article, we aim to largely preserve the trend information, and design a multiscale fusion mechanism to capture multiscale features and preserve comprehensive semantic information." 随后 `III. MSIG-BASED TWO-STAGE PREDICTION MECHANISM` (p.984)
- experiments → conclusion: 消融段落后直接 `V. CONCLUSION` (p.994)

## Candidate rules

- R001 Abstract 用 `To address these problems, this article proposes`，再用 First / Then / Finally 三段贡献。
- R002 Introduction 贡献用 `The notable contributions of the proposed method are outlined as follows` + 编号列表。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 Related Work 分 Long-term / Granule-based /（多尺度）三块。
- R005 Conclusion 用 First / Then / Finally 收回三模块，再用 `An interesting appealing direction would be` 指后续。

## Candidate phrases

- `To address these problems, this article proposes` (abstract)
- `The notable contributions of the proposed method are outlined as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, an MSIG-based two-stage prediction mechanism is proposed.` (conclusion)
- `An interesting appealing direction would be to explore` (conclusion)

## House style

自称是 `this article` / `In this article` / `the proposed method` / `we conducted`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。未见 `Here we`。摘要与结论多用被动 `is proposed`。

## Quotes

- p.982 abstract: Impressive advancements have been achieved in utilizing information granulation for solving long-term time series prediction problems.
- p.982 abstract: However, most state-of-the-art methods suffer from limitations due to not only using the single-scale information granulation but also the lack of trend information.
- p.982 abstract: To address these problems, this article proposes a multiscale information granule-based time series forecasting model.
- p.982 abstract: Comparative analysis shows that the proposed method outperforms existing numeric models and granular models in long-term prediction on regular and large data time series.
- p.982 introduction: TIME series prediction is an intricate process that analyzes the information correlations between current and historical data to forecast future behavior.
- p.982 introduction: Although these models have achieved good performance in short-term prediction, cumulative errors are inevitable for long-term forecasting.
- p.982 introduction: However, these models in fact iteratively generate long-term forecast values, which can affect the prediction performance.
- p.983 introduction: To address the aforementioned challenges, a multiscale information granule (MSIG)-based time series forecasting model with two-stage prediction mechanism is proposed in this article.
- p.983 introduction: The notable contributions of the proposed method are outlined as follows.
- p.983 introduction: The rest of this article is organized as follows. Section II reviews the related work of information granule-based prediction models and multiscale prediction models. Section III presents the specific implementation process of the proposed prediction model. The experimental results and comparison are carried out in Section IV. Finally, Section V concludes this article and gives future directions of this study.
- p.983 related_work: In this section, we review the literature on time series prediction, focusing on the long-term prediction, information granule-based prediction, and multiscale prediction models.
- p.984 related_work: Although these methods have shown the benefits of the information granules in time series prediction, they do not make use of dynamic change and multiscale features of time series efficiently.
- p.984 method: In this section, the MSIG-based two-stage prediction mechanism is introduced in detail.
- p.989 experiments: To assess the effectiveness of MSIG, we conducted comprehensive experiments on five datasets from real-world scenarios.
- p.993 experiments: MSIG has achieved the best training and testing efficiency among multiscale fusion prediction models.
- p.994 experiments: The prediction method with trend-based information granulation achieves the best prediction performance.
- p.994 conclusion: In this article, an MSIG-based two-stage prediction mechanism is proposed.
- p.994 conclusion: The experimental results show that MSIG has the best prediction performance in most cases.
- p.995 conclusion: The experimental results confirm the important role of MSIG for long-term prediction.
- p.995 conclusion: An interesting appealing direction would be to explore more diversified information granules to better model the time series.
