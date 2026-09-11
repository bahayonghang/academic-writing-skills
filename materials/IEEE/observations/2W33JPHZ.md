---
key: 2W33JPHZ
title: "Industrial Process Soft Sensing Based on Bidirectional Optimization Learning of Data Augmentation and Prediction Models Under Limited Data"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3502784"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED METHODS` → `III. BIDIRECTIONAL OPTIMIZATION LEARNING OF DATA AUGMENTATION AND PREDICTION MODELING FRAMEWORK` → `IV.`（`A. Model Evaluation Methods` → `B. Description of The Debutanizer Column` → `C. Compressive Strength of Concrete`）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 AE/SAE/VW-SAE/GSTAE 与四类数据增强）。`II. RELATED METHODS` 是预备知识（AE / STAE / SVR / MIC），不是文献综述。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 在 IV（脱丁烷塔 + 混凝土抗压强度）。

## Openers

- abstract: `Soft sensing techniques` — "Soft sensing techniques are crucial for predicting key quality indicators in industrial processes." (p.1)
- introduction: `WITHIN the intricate` — "WITHIN the intricate landscape of industrial production, the surveillance of product quality variables is paramount [1]." (p.1)
- method: `In industrial process` — "In industrial process soft sensing, feature variables X are used to predict key indicators y, allowing for the inference of critical metrics when direct measurement is not feasible by relying on other measurable data." (p.4, III)
- experiments: `In practical applications` — "In practical applications, various metrics are used to quantitatively assess the performance of models, typically including root mean squared error (RMSE), mean absolute error (MAE), and coefficient of determination (R2)." (p.6, IV.A)
- conclusion: `This article proposes` — "This article proposes a BOL-DAPM to address the poor model performance due to limited data and complex nonlinear relationships between variables in industrial process soft sensing." (p.10)

## Gap transitions

- despite (abstract): "Despite the widespread application of deep learning in the soft sensing domain, challenges such as limited sampling and the complex nonlinear relationships among process variables limit the accuracy and adaptability of soft sensing models." (p.1)
- consequently (abstract): "Consequently, this study develops a bidirectional optimization learning of data augmentation and prediction modeling framework (BOL-DAPM)." (p.1)
- however (introduction): "However, as the sophistication of production processes escalates with the advent of advanced automation, the field of soft sensing confronts formidable challenges." (p.1)
- to address (introduction): "To address these issues, this article proposes a bidirectional optimization learning of data augmentation and prediction modeling framework (BOL-DAPM)." (p.2)
- to address (method): "To address this issue, an improved AE, that is, R-CAE, has been proposed." (p.4)
- future (conclusion): "Future research could further explore how to apply this framework in more varied scenarios and consider more complex industrial data characteristics." (p.10)

## Hedge verbs

- develop / causal / abstract, method: "this study develops a bidirectional optimization learning"; "an improved AE, that is, R-CAE, has been proposed"
- propose / causal / introduction, conclusion: "this article proposes a bidirectional optimization learning"; "This article proposes a BOL-DAPM"
- confirm / causal / abstract: "Experimental validation on datasets from the debutanizer column and concrete compressive strength confirmed that the proposed methods surpass recent comparative approaches"
- show / causal / experiments, conclusion: "As shown in Table IV, the proposed method achieves the best performance"; "Experimental results on the debutanizer column and concrete compressive strength process show that"
- demonstrate / causal / experiments: "demonstrating significant advantages"; "ablation experiments demonstrate that each innovative module plays its respective role"

## Cross-section linkers

- introduction → later sections: "The layout of this article is as follows. Section II briefly introduces the basic methods related to AE, STAE, SVR, and MIC. Section III introduces the BOL-DAPM framework. Section IV demonstrates the effectiveness and feasibility of the proposed methods through the debutanizer column and concrete compressive strength datasets. Section V concludes the article." (p.2)
- related methods → method: `II. RELATED METHODS` 末接 `III. BIDIRECTIONAL OPTIMIZATION LEARNING` (p.3–4)
- method → experiments: Algorithm 1 之后进入 IV.A 评价指标与 IV.B 脱丁烷塔 (p.6–7)
- experiments → conclusion: 混凝土消融段落后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 缺口用 `Despite` + 挑战，贡献用 `this study develops` + 框架缩写。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段，`II. RELATED METHODS` 只铺预备模型。
- R003 Introduction 末用 `The layout of this article is as follows` 指向 II–V。
- R004 贡献用 `The contributions of this article include the following` + 编号列表。
- R005 Conclusion 用 `This article proposes` 收回框架，再用 `Future research could further explore` 指向后续。

## Candidate phrases

- `Consequently, this study develops` (abstract)
- `To address these issues, this article proposes` (introduction)
- `The contributions of this article include the following.` (introduction)
- `The layout of this article is as follows.` (introduction)
- `As shown in Table IV, the proposed method achieves the best performance across all three key metrics.` (experiments)
- `Future research could further explore how to apply this framework` (conclusion)

## House style

自称是 `this study` / `this article proposes` / `we take` / `the proposed method` / `the proposed methods`。未见 `Here we`。`This article proposes` 与 `this study develops` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Soft sensing techniques are crucial for predicting key quality indicators in industrial processes.
- p.1 abstract: Despite the widespread application of deep learning in the soft sensing domain, challenges such as limited sampling and the complex nonlinear relationships among process variables limit the accuracy and adaptability of soft sensing models.
- p.1 abstract: Consequently, this study develops a bidirectional optimization learning of data augmentation and prediction modeling framework (BOL-DAPM).
- p.1 abstract: Experimental validation on datasets from the debutanizer column and concrete compressive strength confirmed that the proposed methods surpass recent comparative approaches in reducing prediction error, improving the coefficient of determination (R2) and lowering the mean absolute error (MAE), with an average precision performance increase of 35%.
- p.1 introduction: WITHIN the intricate landscape of industrial production, the surveillance of product quality variables is paramount [1].
- p.1 introduction: However, as the sophistication of production processes escalates with the advent of advanced automation, the field of soft sensing confronts formidable challenges.
- p.2 introduction: To address these issues, this article proposes a bidirectional optimization learning of data augmentation and prediction modeling framework (BOL-DAPM).
- p.2 introduction: The contributions of this article include the following.
- p.2 introduction: The layout of this article is as follows. Section II briefly introduces the basic methods related to AE, STAE, SVR, and MIC. Section III introduces the BOL-DAPM framework. Section IV demonstrates the effectiveness and feasibility of the proposed methods through the debutanizer column and concrete compressive strength datasets. Section V concludes the article.
- p.4 method: In industrial process soft sensing, feature variables X are used to predict key indicators y, allowing for the inference of critical metrics when direct measurement is not feasible by relying on other measurable data.
- p.4 method: To address this issue, an improved AE, that is, R-CAE, has been proposed.
- p.6 experiments: In practical applications, various metrics are used to quantitatively assess the performance of models, typically including root mean squared error (RMSE), mean absolute error (MAE), and coefficient of determination (R2).
- p.7 experiments: The debutanizer column is a critical piece of equipment in a refinery, used for separating butane from crude oil.
- p.7 experiments: As shown in Table IV, the proposed method achieves the best performance across all three key metrics.
- p.10 conclusion: This article proposes a BOL-DAPM to address the poor model performance due to limited data and complex nonlinear relationships between variables in industrial process soft sensing.
- p.10 conclusion: Experimental results on the debutanizer column and concrete compressive strength process show that compared to traditional methods, this study reduces prediction errors, improves the R2, and decreases the MAE, with an average performance improvement of about 35%; ablation experiments demonstrate that each innovative module plays its respective role.
- p.10 conclusion: Future research could further explore how to apply this framework in more varied scenarios and consider more complex industrial data characteristics.
