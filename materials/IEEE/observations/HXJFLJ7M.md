---
key: HXJFLJ7M
title: "Synchronous Prediction of Multiple Energy Consumption for Cement Clinker Calcination Based on DFF-KAN Model"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2025.3570836"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PRODUCTION PROCESS ANALYSIS AND KEY VARIABLE SELECTION` → `IV. ESTABLISHMENT OF DFF-KAN COAL-ELECTRICITY SYNCHRONIZATION PREDICTION MODEL` → `V. EXPERIMENT AND RESULT ANALYSIS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 末有节序路标，指向 II–VI。

## Openers

- abstract: `The largest energy` — "The largest energy consumption process in cement production is the clinker calcination process." (p.1)
- introduction: `THE typical characteristics` — "THE typical characteristics of cement production process are complex process, strong continuity, and high energy consumption [1]." (p.1；栏首掉字)
- related_work: `The advancement of` — "The advancement of artificial intelligence has demonstrated the effectiveness of machine learning and deep learning techniques in time series prediction." (p.2, II)
- method: `In light of the` — "In light of the prediction modeling analysis of the calcination process presented in Section III, the principal challenges in attaining coal-electricity synchronous prediction are the time-varying delays in production data, the presence of high-dimensional and redundant process parameters, and the strong nonlinear coupling between variables." (p.4, IV)
- experiments: `This section evaluates` — "This section evaluates the performance of the DFF-KAN prediction model to assess its feasibility for synchronous coal-electricity prediction during cement clinker calcination." (p.8, V)
- conclusion: `This article proposes` — "This article proposes a DFF and KAN-based coal-electricity synchronous prediction model, based on the analysis of the coupling relationship between the production process and process parameters in cement clinker calcination." (p.13)

## Gap transitions

- in-order-to (abstract): "In order to address the issue of low energy consumption prediction accuracy resulting from time-varying delay characteristics and the strong coupling of production data, the dynamic feature fusion (DFF)-Kolmogorov–Arnold Network (KAN) algorithm combining DFF and Kolmogorov–Arnold is proposed." (p.1)
- however (introduction): "However, the calcination process is complex, with variables exhibiting strong coupling, time-varying delays, and nonlinearity [5], which complicates the development of an accurate energy consumption prediction model." (p.1)
- therefore (introduction): "It is therefore necessary to develop methods that can enable the synchronous prediction of multiple time series indicators, with a particular focus on coal and electricity consumption." (p.1)
- in-light-of (introduction): "In light of the production characteristics of the cement clinker calcination process, this article leverages production big data and proposes a design combining dynamic feature fusion (DFF) and the Kolmogorov–Arnold Network (KAN) [7]." (p.2)
- however (conclusion): "However, there are areas for further improvement." (p.13)
- therefore (conclusion): "Therefore, advancing sequence prediction and improving the model's generalization ability will be the focus of future research." (p.13)

## Hedge verbs

- is proposed / causal / abstract: "the dynamic feature fusion (DFF)-Kolmogorov–Arnold Network (KAN) algorithm combining DFF and Kolmogorov–Arnold is proposed"
- proposes / causal / introduction, conclusion: "this article leverages production big data and proposes"; "This article proposes a DFF and KAN-based"
- achieves / causal / abstract, experiments: "the proposed DFF-KAN algorithm achieves higher prediction accuracy"
- indicates / speculative / experiments: "which indicates the strong feature extraction capability of model"
- will be / speculative / conclusion: "will be the focus of future research"

## Cross-section linkers

- introduction → related work: "This article is structured as follows. Section II reviews existing machine learning and deep learning methods for energy consumption prediction in process industries, highlighting their advantages, limitations, and recent advancements in the KAN. Section III examines the cement clinker calcination process and identifies key variables affecting coal and electricity consumption. Section IV details the DFF-KAN model configuration. Section V presents an experimental comparison of mainstream deep learning algorithms and DFF-KAN in coal-electricity synchronization prediction. Section VI summarizes the strengths, limitations, and future research directions of the DFF-KAN model." (p.2)
- related work → process: KAN 文献评述末句指向水泥煅烧应用，随后 `III. PRODUCTION PROCESS ANALYSIS AND KEY VARIABLE SELECTION` (p.3)
- process → method: "In light of the prediction modeling analysis of the calcination process presented in Section III" (p.4)
- method → experiments: 式 (29) 与 Table III 后直接 `V. EXPERIMENT AND RESULT ANALYSIS` (p.8)
- experiments → conclusion: 对比段落后直接 `VI. CONCLUSION` (p.13)

## Candidate rules

- R001 摘要用被动 `is proposed` 给出方法缩写，不用 `Here we`。
- R002 Introduction 末用 `The main contributions of this article are as follows.` + 编号列表。
- R003 Introduction 末用 `This article is structured as follows.` 指向 II–VI，且 II 为独立 Related Work。
- R004 Conclusion 先收回方法，再用编号局限 + `will be the focus of future research`。

## Candidate phrases

- `In order to address the issue of` (abstract)
- `The main contributions of this article are as follows.` (introduction)
- `This article is structured as follows.` (introduction)
- `In light of the` (introduction, method)
- `This article proposes a` (conclusion)

## House style

自称是 `this article` / `this article proposes` / `the proposed DFF-KAN` / `we have designed`。未见 `In this paper`。`this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The largest energy consumption process in cement production is the clinker calcination process.
- p.1 abstract: In order to address the issue of low energy consumption prediction accuracy resulting from time-varying delay characteristics and the strong coupling of production data, the dynamic feature fusion (DFF)-Kolmogorov–Arnold Network (KAN) algorithm combining DFF and Kolmogorov–Arnold is proposed.
- p.1 abstract: Compared to five mainstream time series prediction algorithms, the proposed DFF-KAN algorithm achieves higher prediction accuracy with fewer model parameters and shorter training time.
- p.1 introduction: THE typical characteristics of cement production process are complex process, strong continuity, and high energy consumption [1].
- p.1 introduction: However, the calcination process is complex, with variables exhibiting strong coupling, time-varying delays, and nonlinearity [5], which complicates the development of an accurate energy consumption prediction model.
- p.2 introduction: In light of the production characteristics of the cement clinker calcination process, this article leverages production big data and proposes a design combining dynamic feature fusion (DFF) and the Kolmogorov–Arnold Network (KAN) [7].
- p.2 introduction: The main contributions of this article are as follows.
- p.2 introduction: This article is structured as follows. Section II reviews existing machine learning and deep learning methods for energy consumption prediction in process industries, highlighting their advantages, limitations, and recent advancements in the KAN.
- p.2 related_work: The advancement of artificial intelligence has demonstrated the effectiveness of machine learning and deep learning techniques in time series prediction.
- p.4 method: In light of the prediction modeling analysis of the calcination process presented in Section III, the principal challenges in attaining coal-electricity synchronous prediction are the time-varying delays in production data, the presence of high-dimensional and redundant process parameters, and the strong nonlinear coupling between variables.
- p.4 method: In order to address these challenges, this article proposes the DFF-KAN model, which aims to achieve a higher level of prediction accuracy with a reduced number of parameters.
- p.8 experiments: This section evaluates the performance of the DFF-KAN prediction model to assess its feasibility for synchronous coal-electricity prediction during cement clinker calcination.
- p.13 experiments: Therefore, DFF-KAN achieves the best performance in the synchronous prediction of coal and electricity consumption.
- p.13 conclusion: This article proposes a DFF and KAN-based coal-electricity synchronous prediction model, based on the analysis of the coupling relationship between the production process and process parameters in cement clinker calcination.
- p.13 conclusion: However, there are areas for further improvement.
- p.13 conclusion: Therefore, advancing sequence prediction and improving the model's generalization ability will be the focus of future research.
