---
key: BSQCTG5L
title: "Deep Co-Training Partial Least Squares Model for Semi-Supervised Industrial Soft Sensing"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2025.3540028"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BRIEF INTRODUCTION OF PLS` → `III. METHODOLOGY` → `IV. ONLINE SOFT SENSING OF F-CAO IN CEMENT CLINKER PRODUCTION PROCESS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR/PLS/ANN/SVM 与深度软测量，再评半监督与 co-training）。Introduction 末有节序路标，指向 Section II–末节。Experiments 标题为水泥熟料 F-CaO 在线软测量案例。

## Openers

- abstract: `Data-driven soft sensing` — "Data-driven soft sensing has become quite popular in recent years, which can provide real-time estimations of key variables in industrial processes." (p.1)
- introduction: `KEY PERFORMANCE indicators` — "KEY PERFORMANCE indicators (KPI), such as product quality, energy consumption, equipment health, and Environmental emission indicators, play an important role in modern industries, which usually influences the strategic decisions of leading companies to a large extent." (p.1)
- method: `In this section,` — "In this section, the methodology and main algorithm of the deep CT-PLS model are demonstrated in detail." (p.2, III)
- experiments: `Cement clinker is` — "Cement clinker is an important building material, its production process contains several main equipment and operating units, such as preheater, calciner, rotary kiln, and grate cooler, a simple flowchart is shown in Fig. 2." (p.4, IV)
- conclusion: `In this article,` — "In this article, a deep CT-PLS model has been developed for semi-supervised data-driven predictive modeling and industrial soft sensor applications." (p.7)

## Gap transitions

- however (introduction): "However, a major challenge for KPI control and optimization is due to the lag development of measurement technologies [1], [2], [3]." (p.1)
- although (introduction): "Although more and more data have been recorded and collected with the rapid development of the Industrial Internet of Things and digital technologies, there is still a shortage of technology to measure those KPIs." (p.1)
- therefore (introduction): "Therefore, it has become as a promising tool to provide alternatives for online measuring KPI related variables in modern industries." (p.1)
- however (introduction): "However, the actual performance of deep learning cannot be guaranteed even more unlabeled data samples are incorporated for semi-supervised modeling, since the performance will severely restricted to the limited number of labeled data samples." (p.2)
- although (method): "Although lots of co-training strategies have been proposed in different application fields along the past years, only the very basic form is used in the present article." (p.3)
- however (experiments): "However, when more than 150 unlabeled data samples are included, the performance improvement speed slows down a little bit, since more information has already been capture by the deep CT-PLS model." (p.7)

## Hedge verbs

- propose / causal / abstract: "a deep co-training PLS (deep CT-PLS) model is proposed"
- demonstrate / causal / method: "the methodology and main algorithm of the deep CT-PLS model are demonstrated in detail"
- can / speculative / abstract: "the deep CT-PLS model can significantly improve the soft sensing performance"
- may / speculative / introduction: "the prediction robustness of the model may be improved as well"
- develop / causal / conclusion: "a deep CT-PLS model has been developed"

## Cross-section linkers

- introduction → method: "The remainder of this article is formulated as follows. In Section II, detailed methodology of the deep co-training PLS (deep CT-PLS) model is given, as well as the development of online soft sensing strategy. In the next section, a detailed case study is carried out on a real industrial production plant. Finally, conclusions are made in the last section." (p.2)
- method → experiments: "In summary, a flowchart of the whole modeling process of deep CT-PLS is given in Fig. 1." 随后 `IV. ONLINE SOFT SENSING OF F-CAO IN CEMENT CLINKER PRODUCTION PROCESS` (p.4)
- experiments → conclusion: 融合结果段落后直接 `V. CONCLUSION` (p.7)

## Candidate rules

- R001 Abstract 用 `In this article, a ... model is proposed to extend`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is formulated as follows` 指向 II–末节。
- R004 Method 用 `In this section, the methodology and main algorithm of ... are demonstrated in detail`。
- R005 Conclusion 先收回方法，再用 `For future work, some important issues are worth to be noted`。

## Candidate phrases

- `In this article, a deep co-training PLS (deep CT-PLS) model is proposed` (abstract)
- `The remainder of this article is formulated as follows.` (introduction)
- `In this section, the methodology and main algorithm of` (method)
- `In this article, a deep CT-PLS model has been developed for` (conclusion)
- `For future work, some important issues are worth to be noted.` (conclusion)

## House style

自称是 `In this article` / `this article` / `the present article` / `the proposed method`。未见 `we propose` 作摘要主语；摘要用被动 `is proposed`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。未见 `Here we`。

## Quotes

- p.1 abstract: Data-driven soft sensing has become quite popular in recent years, which can provide real-time estimations of key variables in industrial processes.
- p.1 abstract: How to break through the bottleneck of data-drive models in terms of limited labeled data and high computational complexity should be one of the main recent focuses in the field of industrial soft sensing.
- p.1 abstract: In this article, a deep co-training PLS (deep CT-PLS) model is proposed to extend the ordinary PLS model to the semi-supervised deep form.
- p.1 abstract: Based on the case study on a real industrial production process, the deep CT-PLS model can significantly improve the soft sensing performance.
- p.1 introduction: KEY PERFORMANCE indicators (KPI), such as product quality, energy consumption, equipment health, and Environmental emission indicators, play an important role in modern industries, which usually influences the strategic decisions of leading companies to a large extent.
- p.1 introduction: However, a major challenge for KPI control and optimization is due to the lag development of measurement technologies [1], [2], [3].
- p.1 introduction: Although more and more data have been recorded and collected with the rapid development of the Industrial Internet of Things and digital technologies, there is still a shortage of technology to measure those KPIs.
- p.1 introduction: Therefore, it has become as a promising tool to provide alternatives for online measuring KPI related variables in modern industries.
- p.2 introduction: In this article, this deep PLS model is employed for semi-supervised improvement in the application of industrial soft sensing.
- p.2 introduction: The remainder of this article is formulated as follows. In Section II, detailed methodology of the deep co-training PLS (deep CT-PLS) model is given, as well as the development of online soft sensing strategy. In the next section, a detailed case study is carried out on a real industrial production plant. Finally, conclusions are made in the last section.
- p.2 method: In this section, the methodology and main algorithm of the deep CT-PLS model are demonstrated in detail.
- p.3 method: Although lots of co-training strategies have been proposed in different application fields along the past years, only the very basic form is used in the present article.
- p.4 experiments: Cement clinker is an important building material, its production process contains several main equipment and operating units, such as preheater, calciner, rotary kiln, and grate cooler, a simple flowchart is shown in Fig. 2.
- p.6 experiments: It can be seen in the figure that the prediction accuracy has been significant improved by the deep CT-PLS model, detailed comparisons in terms of the RMSE value are provided in Fig. 4 for the three methods.
- p.7 experiments: However, when more than 150 unlabeled data samples are included, the performance improvement speed slows down a little bit, since more information has already been capture by the deep CT-PLS model.
- p.7 conclusion: In this article, a deep CT-PLS model has been developed for semi-supervised data-driven predictive modeling and industrial soft sensor applications.
- p.8 conclusion: The superior performance of the developed deep CT-PLS model has been well evaluated through a real industrial case study.
- p.8 conclusion: Compared to both ordinary PLS and deep PLS models, promising results have been obtained by the new method.
- p.8 conclusion: For future work, some important issues are worth to be noted.
