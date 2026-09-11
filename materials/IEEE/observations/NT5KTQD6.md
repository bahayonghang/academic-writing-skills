---
key: NT5KTQD6
title: "Long-Term Multivariate Time-Series Forecasting Model Based on Gaussian Fuzzy Information Granules"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2024.3449769"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. LONG-TERM MULTIVARIATE TIME-SERIES FORECASTING MODEL BASED ON GFIG` → `IV. EVALUATIONS` → `V. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCLATURE`。有独立 Related Work（`II. RELATED WORKS`，含 Literature Review 与基础知识）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `EVALUATIONS`。

## Openers

- abstract: `Long-term forecasting of` — "Long-term forecasting of multivariate time series has been an important research issue in the field of data mining and knowledge discovery." (p.6424)
- introduction: `TIME-SERIES data mining` — "TIME-SERIES data mining is a process of extracting useful information and knowledge from time-series data." (p.6424；栏首掉字)
- related_work: `In this section` — "In this section, we introduce the research progress of prediction model and clustering model related to GLFIG, respectively." (p.6425, II.A)
- method: `The proposed GFIG-based` — "The proposed GFIG-based model is able to fulfill the task of long-term forecasting well in multivariate time series." (p.6426, III)
- experiments: `In this section` — "In this section, we evaluate our model against other predictive models using eight publicly available datasets." (p.6429, IV)
- conclusion: `In this work` — "In this work, we have presented a long-term prediction model for multivariate time series based on GFIG." (p.6437)

## Gap transitions

- however (abstract): "However, although the method has been universally used in univariate time series, its application for multivariate time series has received little attention." (p.6424)
- however (introduction): "However, these methods struggle with complex data and exhibit limited adaptability to nonlinear relationships." (p.6424)
- however (introduction): "However, we note that the above studies are all centered on GLFIG for prediction, and there is a lack of discussion on Gaussian fuzzy information granules (GFIG) with different polynomial cores" (p.6425)
- in order to (abstract): "In order to utilize the advantages of fuzzy information granularity and fill its gap in solving multivariate time-series forecasting problems." (p.6424)
- to compensate (related work): "To compensate for the lack of GFIG in multivariate time-series studies, the main purpose of this article is to establish a long-term forecasting model framework based on GFIG suitable for multivariate time series" (p.6426)

## Hedge verbs

- design / causal / abstract: "we design a long-term multivariate time-series forecasting modeling framework in light of Gaussian fuzzy information granules"
- propose / causal / introduction: "The main objective of this article is to propose a fuzzy information granule-based long-term forecasting model suitable for multivariate time series."
- show / causal / abstract, experiments: "the results show that our model is able to perform long-term forecasting of multivariate time series with a high satisfactory accuracy"
- prove / causal / conclusion: "Extensive experimental results further prove the long-term prediction ability of our model."
- demonstrate / causal / experiments: "our model demonstrates effective long-term forecasting capabilities across the majority of datasets"

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II summaries the related works. We reveal our proposed model in Section III. Section IV presents an experimental analysis of the model's performance on a number of publicly available datasets and analyzes the prediction results in comparison with those of other models. Finally, Section V concludes this article." (p.6425)
- related work → method: 基础知识与符号说明后直接 `III. LONG-TERM MULTIVARIATE TIME-SERIES FORECASTING MODEL BASED ON GFIG` (p.6426)
- method → experiments: Algorithm 2 / Remark 3 后直接 `IV. EVALUATIONS` (p.6429)
- experiments → conclusion: Discussion 局限段落后直接 `V. CONCLUSION` (p.6437)

## Candidate rules

- R001 abstract 用 `However, although` 双转折标单变量已用、多变量缺口。
- R002 有独立 `II. RELATED WORKS`，预测与聚类分小节后再给 Definition。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 Experiments 节标题用 `EVALUATIONS`，先数据集再消融再对比。
- R005 Conclusion 用 `In this work, we have presented`，再用编号 `Future research directions include the following.`

## Candidate phrases

- `In order to utilize the advantages of ... and fill its gap` (abstract)
- `In view of this purpose, we design` (abstract)
- `The main objective of this article is to propose` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this work, we have presented` (conclusion)

## House style

自称是 `this article` / `we design` / `our model` / `In this work`。未见 `Here we`。`this article` 与 `In this work` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.6424 abstract: Long-term forecasting of multivariate time series has been an important research issue in the field of data mining and knowledge discovery.
- p.6424 abstract: However, although the method has been universally used in univariate time series, its application for multivariate time series has received little attention.
- p.6424 abstract: In order to utilize the advantages of fuzzy information granularity and fill its gap in solving multivariate time-series forecasting problems.
- p.6424 abstract: In view of this purpose, we design a long-term multivariate time-series forecasting modeling framework in light of Gaussian fuzzy information granules.
- p.6424 introduction: TIME-SERIES data mining is a process of extracting useful information and knowledge from time-series data.
- p.6424 introduction: However, these methods struggle with complex data and exhibit limited adaptability to nonlinear relationships.
- p.6425 introduction: However, we note that the above studies are all centered on GLFIG for prediction, and there is a lack of discussion on Gaussian fuzzy information granules (GFIG) with different polynomial cores, and the abovementioned studies are only centered on long-term prediction of univariate time series
- p.6425 introduction: The main objective of this article is to propose a fuzzy information granule-based long-term forecasting model suitable for multivariate time series.
- p.6425 introduction: The rest of this article is organized as follows. Section II summaries the related works. We reveal our proposed model in Section III. Section IV presents an experimental analysis of the model's performance on a number of publicly available datasets and analyzes the prediction results in comparison with those of other models. Finally, Section V concludes this article.
- p.6425 related work: In this section, we introduce the research progress of prediction model and clustering model related to GLFIG, respectively.
- p.6426 related work: To compensate for the lack of GFIG in multivariate time-series studies, the main purpose of this article is to establish a long-term forecasting model framework based on GFIG suitable for multivariate time series, and to analyze and address the issue of GFIG in long-term forecasting of multivariate time series.
- p.6426 method: The proposed GFIG-based model is able to fulfill the task of long-term forecasting well in multivariate time series.
- p.6429 experiments: In this section, we evaluate our model against other predictive models using eight publicly available datasets.
- p.6436 experiments: Based on the findings of the study, our model demonstrates effective long-term forecasting capabilities across the majority of datasets.
- p.6437 conclusion: In this work, we have presented a long-term prediction model for multivariate time series based on GFIG.
- p.6437 conclusion: Extensive experimental results further prove the long-term prediction ability of our model.
- p.6437 conclusion: Future research directions include the following.
