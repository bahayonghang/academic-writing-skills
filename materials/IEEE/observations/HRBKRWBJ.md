---
key: HRBKRWBJ
title: "NFIG-X: Nonlinear Fuzzy Information Granule Series for Long-Term Traffic Flow Time-Series Forecasting"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2023.3261893"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,10-16"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. LITERATURE REVIEW` → `III. PRELIMINARIES` → `IV. NONLINEAR TREND FUZZY GRANULATION` → `V.`（NFIG 序列预测）→ `VI. APPLICATION` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（标题为 `II. LITERATURE REVIEW`，非 `Related Work`）。Introduction 末有节序路标，指向 Section II–VII。

## Openers

- abstract: `Long-term time-series forecasting` — "Long-term time-series forecasting is an extensive research topic and is of great significance in many fields." (p.3582)
- introduction: `SINCE traffic flow forecasting` — "SINCE traffic flow forecasting can provide a decision-making basis for intelligent traffic control and guidance, research on traffic flow forecasting has received continuous attention [1], [2], [3] in the field of intelligent transportation systems (ITSs)." (p.3582；栏首掉字)
- related_work: `Traditional shallow machine` — "Traditional shallow machine learning methods have made numerous contribution to the field of traffic flow prediction." (p.3583, II)
- method: `The traffic flow data` — "The traffic flow data often show a strong periodic trend." (p.3584, III.A)
- experiments: `We start with a` — "We start with a brief introduction to the three traffic flow time-series datasets exploited to validate the forecast performance of the proposed model and six baseline predictor, corresponding to Section VI-A." (p.3591, VI)
- conclusion: `This article investigates` — "This article investigates dynamic traffic flow forecast exploiting the nonlinear trend fuzzy granulation method." (p.3595)

## Gap transitions

- however (abstract): "However, the task of long-term time-series forecasting is accompanied by the problem of increasing cumulative error and decreasing time correlation." (p.3582)
- to overcome (abstract): "To overcome these shortcomings, this article proposes a prediction framework based on the nonlinear fuzzy information granule (NFIG) series, which can boost the long-term performance of most predictors." (p.3582)
- however (introduction): "However, due to the high frequency, randomness, nonlinearity, and other characteristics of traffic flow data, the composition of the data is complex, and it is difficult to make efficient and reliable forecasts [4]." (p.3582)
- nevertheless (introduction): "Nevertheless, most such works focus on the short-term instead of long-term forecasting task and require a large amount of data for model training." (p.3582)
- however (literature): "However, current trend fuzzy granulation prediction techniques focus only on the linear trend characteristics of the data, while ignoring nonlinear fluctuations." (p.3584)
- in conclusion (literature): "In conclusion, there have been numerous efforts to exploit different technical means for the prediction task of traffic flow data with nonlinear, random, and high-frequency characteristics." (p.3584)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a prediction framework"; "We propose NFIG-X"
- show / causal / conclusion: "The results show that the NFIG-X framework has higher accuracy and robustness in long-term forecasting of traffic flow."
- indicate / causal / experiments: "These curves indicate that the NFIG-X framework has improved the forecast accuracy"
- can / speculative / conclusion: "NFIG-X can only be exploited for univariate time-series forecasting at present"

## Cross-section linkers

- introduction → literature: "The remainder of this article is organized as follows. Literature review is presented in Section II. To facilitate the understanding, some necessary preliminaries are introduced in Section III. In Section IV, a Gaussian nonlinear trend fuzzy granulation method and an incremental Gaussian nonlinear trend fuzzy granulation method are proposed. A forecasting method for NFIG series is designed in Section V. In Section VI, the proposed algorithm is compared with other six algorithms in three datasets, and the effectiveness of the proposed algorithm is demonstrated. Finally, Section VII concludes this article." (p.3583)
- method → experiments: Ablation 段落后接 `VI. APPLICATION` (p.3591)
- experiments → conclusion: 实验小结后接 `VII. CONCLUSION` (p.3595)

## Candidate rules

- R001 贡献用 `The contributions of this article that imply originality of the study are highlighted as follows.` + 编号列表。
- R002 独立文献节标题用 `LITERATURE REVIEW` 而非 `RELATED WORK`。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VII。
- R004 实验主节标题用 `APPLICATION`，内部再设 `B. Experiments`。
- R005 Conclusion 用 `Some issues deserve further study.` 再接 `Our next work will focus on`。

## Candidate phrases

- `To overcome these shortcomings, this article proposes` (abstract)
- `The contributions of this article that imply originality of the study are highlighted as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `This article investigates` (conclusion)
- `Some issues deserve further study.` (conclusion)
- `Our next work will focus on` (conclusion)

## House style

自称是 `this article` / `we propose` / `our method` / `the proposed method`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.3582 abstract: Long-term time-series forecasting is an extensive research topic and is of great significance in many fields.
- p.3582 abstract: However, the task of long-term time-series forecasting is accompanied by the problem of increasing cumulative error and decreasing time correlation.
- p.3582 abstract: To overcome these shortcomings, this article proposes a prediction framework based on the nonlinear fuzzy information granule (NFIG) series, which can boost the long-term performance of most predictors.
- p.3582 abstract: Thus, the proposed method is employed for the long-term traffic flow forecasting.
- p.3582 introduction: SINCE traffic flow forecasting can provide a decision-making basis for intelligent traffic control and guidance, research on traffic flow forecasting has received continuous attention [1], [2], [3] in the field of intelligent transportation systems (ITSs).
- p.3582 introduction: However, due to the high frequency, randomness, nonlinearity, and other characteristics of traffic flow data, the composition of the data is complex, and it is difficult to make efficient and reliable forecasts [4].
- p.3582 introduction: Nevertheless, most such works focus on the short-term instead of long-term forecasting task and require a large amount of data for model training.
- p.3582–3583 introduction: In this article, we study nonlinear fuzzy information granule (NFIG) series for long-term traffic flow forecasting, which can dissipate part of the accumulated errors produced by the predictor.
- p.3583 introduction: The contributions of this article that imply originality of the study are highlighted as follows.
- p.3583 introduction: The remainder of this article is organized as follows.
- p.3583 related work: Traditional shallow machine learning methods have made numerous contribution to the field of traffic flow prediction.
- p.3584 related work: However, current trend fuzzy granulation prediction techniques focus only on the linear trend characteristics of the data, while ignoring nonlinear fluctuations.
- p.3584 related work: More importantly, there is no work that applies fuzzy trend granulation techniques to long-term traffic flow forecasting.
- p.3591 experiments: We start with a brief introduction to the three traffic flow time-series datasets exploited to validate the forecast performance of the proposed model and six baseline predictor, corresponding to Section VI-A.
- p.3595 experiments: By conducting experiments on the three traffic flow time series, it can be found from Tables VIII–X and Figs. 10–12 that NFIG-X performs best in most time-series prediction problems.
- p.3595 conclusion: This article investigates dynamic traffic flow forecast exploiting the nonlinear trend fuzzy granulation method.
- p.3596 conclusion: The results show that the NFIG-X framework has higher accuracy and robustness in long-term forecasting of traffic flow.
- p.3596 conclusion: Some issues deserve further study.
- p.3596 conclusion: Our next work will focus on the prediction of multivariate fuzzy granules series.
