---
key: W4LW6ADR
title: "FICformer: A Multi-factor Fuzzy Bayesian Imputation Cross-former for Big Data-driven Agricultural Decision Support Systems"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2024.3363213"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EXPERIMENTS AND RESULTS` → `V. DISCUSSION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立相关工作节 `II. RELATED WORKS`（missing data imputation / agricultural factor prediction / fuzzy-based prediction）。`related_work=independent`。Introduction 末有 `The rest of this article is organized as follows` 路标，指向 II–VI。Method 在 III（fuzzy Bayesian imputer / DTCAtt / C-Former）。Experiments 标题为 `EXPERIMENTS AND RESULTS`（温室环境数据）。另有独立讨论节 V。

## Openers

- abstract: `Smart agricultural decision` — "Smart agricultural decision support systems leverage big data technology to generate efficient decision recommendations." (p.1)
- introduction: `THE widespread application` — "THE widespread application of decision support systems (DSSs) in agriculture and the environment has enabled rapid assessment of agricultural conditions [1]." (p.1；栏首掉字)
- method: `In order to` — "In order to solve the uncertainty problem of missing data in big data-driven systems and to deeply explore the nonlinear dependencies of environmental factors, a multifactor prediction model based on fuzzy imputation (FICformer) was constructed for smart agriculture environmental prediction." (p.2, III)
- experiments: `The dataset is` — "The dataset is sourced from a smart agriculture big data system." (p.6, IV.A)
- conclusion: `This article introduces` — "This article introduces a sophisticated multifactor forecasting methodology for intelligent agriculture based on the utilization of greenhouse environmental data collected by a data-driven system." (p.12)

## Gap transitions

- however (abstract): "However, missing values in sensor data can lead to cumulative errors and reduced accuracy in data analysis, compromising the precision of these decision systems." (p.1)
- to address (abstract): "To address this issue, we propose an intelligent multifactor prediction framework for smart agriculture environments." (p.1)
- however (related work): "However, except for machine learning methods, the mentioned techniques are used for missing data with individual features, lacking consideration for interfeature correlations, imputation performance is limited." (p.2)
- hence (related work): "Hence, constructing multifactor prediction models is necessary to achieve more accurate results and offer comprehensive decision support." (p.2)
- however (discussion): "However, it is worth noting that when the number of iterations reaches 400, the training time reaches 687 s, which no longer fulfills the requirement of real-time data imputation during production." (p.10)
- therefore (discussion): "Therefore, it is important to consider relevant features with high contributions after attention calculation to avoid wasting computational resources." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose an intelligent multifactor prediction framework"; "We propose a dimensional temporal cross-attention mechanism"
- introduce / causal / introduction, conclusion: "This article introduces a fuzzy Bayesian imputation layer"; "This article introduces a sophisticated multifactor forecasting methodology"
- demonstrate / causal / abstract: "Extensive experiments demonstrate that our proposed model outperforms single-factor prediction"
- may / speculative / related work: "the interdimensionality may contain deeper dependencies"

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II investigates the related works. Section III provides a detailed description of the proposed methodology. Section IV shows the experimental results and visualization, Section V shows a discussion of the experiments. Finally, Section VI concludes this article." (p.2)
- related work → method: "DNFS effectively utilizes its modeling capability for uncertain information, bringing new ideas to agricultural decision-making systems." 随后 `III. METHODOLOGY` (p.2)
- method → experiments: MSE 损失段落后接 `IV. EXPERIMENTS AND RESULTS` (p.6)
- discussion → conclusion: 可解释性段落后直接 `VI. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `To address this issue, we propose`，不用 `Here we`。
- R002 独立相关工作标题为 `RELATED WORKS`，分 imputation / prediction / fuzzy 三块。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The main contributions of this article are as follows.` + 编号列表。
- R005 Conclusion 用 `This article introduces` 收回，再用 `future endeavors will encompass` 指向后续。

## Candidate phrases

- `To address this issue, we propose an intelligent multifactor prediction framework` (abstract)
- `The main contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article introduces a sophisticated multifactor forecasting methodology` (conclusion)
- `future endeavors will encompass multifactor modeling across a variety of agricultural domains` (conclusion)

## House style

自称是 `we propose` / `this article` / `our proposed model`。未见 `Here we`。`This article introduces` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Smart agricultural decision support systems leverage big data technology to generate efficient decision recommendations.
- p.1 abstract: However, missing values in sensor data can lead to cumulative errors and reduced accuracy in data analysis, compromising the precision of these decision systems.
- p.1 abstract: To address this issue, we propose an intelligent multifactor prediction framework for smart agriculture environments.
- p.1 abstract: Extensive experiments demonstrate that our proposed model outperforms single-factor prediction, achieving a 13.6% increase in correlation.
- p.1 introduction: THE widespread application of decision support systems (DSSs) in agriculture and the environment has enabled rapid assessment of agricultural conditions [1].
- p.1 introduction: To address the above issues, we combine fuzzy learning and deep learning predictive modeling for predictive modeling of missing data in smart agriculture.
- p.1 introduction: The main contributions of this article are as follows.
- p.2 introduction: The rest of this article is organized as follows. Section II investigates the related works. Section III provides a detailed description of the proposed methodology. Section IV shows the experimental results and visualization, Section V shows a discussion of the experiments. Finally, Section VI concludes this article.
- p.2 related work: However, except for machine learning methods, the mentioned techniques are used for missing data with individual features, lacking consideration for interfeature correlations, imputation performance is limited.
- p.2 related work: Hence, constructing multifactor prediction models is necessary to achieve more accurate results and offer comprehensive decision support.
- p.2 method: In order to solve the uncertainty problem of missing data in big data-driven systems and to deeply explore the nonlinear dependencies of environmental factors, a multifactor prediction model based on fuzzy imputation (FICformer) was constructed for smart agriculture environmental prediction.
- p.6 experiments: The dataset is sourced from a smart agriculture big data system.
- p.10 discussion: However, it is worth noting that when the number of iterations reaches 400, the training time reaches 687 s, which no longer fulfills the requirement of real-time data imputation during production.
- p.11 discussion: Therefore, it is important to consider relevant features with high contributions after attention calculation to avoid wasting computational resources.
- p.12 conclusion: This article introduces a sophisticated multifactor forecasting methodology for intelligent agriculture based on the utilization of greenhouse environmental data collected by a data-driven system.
- p.13 conclusion: Experimental evaluations conducted within a smart greenhouse context demonstrate the remarkable ability of the FICformer model to forecast greenhouse environment alterations up to 48 h in advance.
- p.13 conclusion: Notably, this experiment exclusively focuses on greenhouse data; however, future endeavors will encompass multifactor modeling across a variety of agricultural domains to augment the model’s generalizability and resilience.
