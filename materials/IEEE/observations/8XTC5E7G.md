---
key: 8XTC5E7G
title: "CTFNet: Long-Sequence Time-Series Forecasting Based on Convolution and Time–Frequency Analysis"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2023.3294064"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-5,8-9,13-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PRELIMINARY` → `IV. METHODOLOGY` → `V. EXPERIMENTS` → `VI` 案例（COVID-19） → `VII. CONCLUSION AND FUTURE WORK`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work。`related_work=independent`。Introduction 末有 `The remainder of this article is organized as follows` 路标，指向 Section II–VII。Experiments 标题为 `EXPERIMENTS`。结论节标题含 future work。

## Openers

- abstract: `Although current time-series` — "Although current time-series forecasting methods have significantly improved the state-of-the-art (SOTA) results for long-sequence time-series forecasting (LSTF), they still have difficulty in capturing and extracting the features and dependencies of long-term sequences and suffer from information utilization bottlenecks and high-computational complexity." (p.1)
- introduction: `TIME-SERIES forecasting is` — "TIME-SERIES forecasting is an important business problem in practical applications and a fruitful application area of artificial intelligence [1], [2], [3], [4], [5], [6]." (p.1)
- method: `It is well known` — "It is well known that time-series data can be modeled from both TD and FD, and frequency patterns are a stable feature of complex time series and are reliable and useful information to improve forecasting performance [4]." (p.5, IV)
- experiments: `To comprehensively evaluate` — "To comprehensively evaluate the performance of CTFNet, nine real-world cases in five domains (namely, energy, economics, traffic, weather, and medical) are selected, and 16 outstanding methods (such as MLP-based models, Transformer-based networks, semantic hierarchical constructive learning models, and traditional models) are used as baselines for comparison in the study." (p.8)
- conclusion: `This article proposed CTFNet` — "This article proposed CTFNet, a simple model based on a single-hidden feedforward layer." (p.13)

## Gap transitions

- although (abstract): "Although current time-series forecasting methods have significantly improved the state-of-the-art (SOTA) results for long-sequence time-series forecasting (LSTF), they still have difficulty in capturing and extracting the features and dependencies of long-term sequences and suffer from information utilization bottlenecks and high-computational complexity." (p.1)
- to address (abstract): "To address these issues, a lightweight single-hidden layer feedforward neural network (SLFN) combining convolution mapping and time–frequency decomposition called CTFNet is proposed with three distinctive characteristics." (p.1)
- however (introduction): "However, the existing methods are mostly designed under short-term problem setting, such as predicting 48 points or less [5], [7], [12], [13], [22], [23], [24], [25]." (p.1)
- although (introduction): "At present, although a large number of advanced methods [26], [27], [28], [29] are used to solve long-sequence time-series forecasting (LSTF) problems, the following challenges still exist." (p.1)
- fortunately (introduction): "Fortunately, several recent research is addressing this issue." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "called CTFNet is proposed"; "We propose CTFNet"
- show / causal / abstract: "Our empirical studies with nine benchmark datasets show that compared with state-of-the-art methods, CTFNet can reduce prediction error by 64.7% and 53.7% for multivariate and univariate time series, respectively."
- demonstrate / causal / introduction: "this is the first work that demonstrates the great potential of the single-layer feedforward-based structure in multivariate LSTF"
- achieve / causal / experiments, conclusion: "CTFNet achieves the best performance in almost all the datasets and metrics"; "the proposed model achieves the best forecasting performance on nine benchmark datasets"
- will continue / speculative / conclusion: "In the future, we will continue to study simple and efficient models"

## Cross-section linkers

- introduction → related work: "The remainder of this article is organized as follows. Section II introduces the related work. Section III defines the LSTF problem, the data preprocessing method, and gives the preliminary descriptions of SLFNs and the Moore–Penrose generalized inverse matrix. Section IV presents a detailed description of the proposed model. Section V describes the comparative experiments, and the effectiveness of the proposed model is analyzed and evaluated. Section VI provides a real case study. Section VII draws the conclusions and offers suggestions for future research directions." (p.2)
- related work → preliminary: 深度学习方法综述后 `III. PRELIMINARY` (p.4)
- method → experiments: Algorithm 1 与特征融合后 `V. EXPERIMENTS` (p.8)
- experiments → conclusion: 案例可视化后 `VII. CONCLUSION AND FUTURE WORK` (p.13)

## Candidate rules

- R001 abstract 先 `Although` 收已有 SOTA，再 `To address these issues` + 被动 `is proposed`。
- R002 独立 Related Work，分 spectral / classical / deep-learning 三块。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VII。
- R004 贡献用 `The main contributions of this study are as follows.` + 编号；自称 `this study` 与 `this article` 并用。
- R005 Conclusion 标题为 `CONCLUSION AND FUTURE WORK`，先 `This article proposed`，再用 `In the future, we will`。

## Candidate phrases

- `To address these issues, a lightweight ... called CTFNet is proposed` (abstract)
- `The main contributions of this study are as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `To comprehensively evaluate the performance of CTFNet` (experiments)
- `This article proposed CTFNet, a simple model based on` (conclusion)
- `In the future, we will continue to study` (conclusion)

## House style

自称 `this article` / `this study` / `we propose` / `our model` / `In this work`。未见 `Here we`。`This article proposed` 与 `this study` 进 phrase_bank，不进 anti_ai_patterns。Abstract 有 `in this article, a method for extracting ... is proposed`。未见独立 `In this paper` 开篇。

## Quotes

- p.1 abstract: Although current time-series forecasting methods have significantly improved the state-of-the-art (SOTA) results for long-sequence time-series forecasting (LSTF), they still have difficulty in capturing and extracting the features and dependencies of long-term sequences and suffer from information utilization bottlenecks and high-computational complexity.
- p.1 abstract: To address these issues, a lightweight single-hidden layer feedforward neural network (SLFN) combining convolution mapping and time–frequency decomposition called CTFNet is proposed with three distinctive characteristics.
- p.1 abstract: Our empirical studies with nine benchmark datasets show that compared with state-of-the-art methods, CTFNet can reduce prediction error by 64.7% and 53.7% for multivariate and univariate time series, respectively.
- p.1 introduction: TIME-SERIES forecasting is an important business problem in practical applications and a fruitful application area of artificial intelligence [1], [2], [3], [4], [5], [6].
- p.1 introduction: However, the existing methods are mostly designed under short-term problem setting, such as predicting 48 points or less [5], [7], [12], [13], [22], [23], [24], [25].
- p.1 introduction: At present, although a large number of advanced methods [26], [27], [28], [29] are used to solve long-sequence time-series forecasting (LSTF) problems, the following challenges still exist.
- p.2 introduction: Fortunately, several recent research is addressing this issue.
- p.2 introduction: The main contributions of this study are as follows.
- p.2 introduction: The remainder of this article is organized as follows. Section II introduces the related work. Section III defines the LSTF problem, the data preprocessing method, and gives the preliminary descriptions of SLFNs and the Moore–Penrose generalized inverse matrix. Section IV presents a detailed description of the proposed model. Section V describes the comparative experiments, and the effectiveness of the proposed model is analyzed and evaluated. Section VI provides a real case study. Section VII draws the conclusions and offers suggestions for future research directions.
- p.5 method: It is well known that time-series data can be modeled from both TD and FD, and frequency patterns are a stable feature of complex time series and are reliable and useful information to improve forecasting performance [4].
- p.5 method: To address the above challenges and problems, we propose a very simple yet highly effective lightweight neural network architecture, CTFNet, as shown in Fig. 1.
- p.8 experiments: To comprehensively evaluate the performance of CTFNet, nine real-world cases in five domains (namely, energy, economics, traffic, weather, and medical) are selected, and 16 outstanding methods (such as MLP-based models, Transformer-based networks, semantic hierarchical constructive learning models, and traditional models) are used as baselines for comparison in the study.
- p.9 experiments: For multivariate forecasting, CTFNet achieves the best performance in almost all the datasets and metrics, as shown in Table II.
- p.13 conclusion: This article proposed CTFNet, a simple model based on a single-hidden feedforward layer.
- p.13 conclusion: Finally, extensive experiments show that the proposed model achieves the best forecasting performance on nine benchmark datasets in comparison with the state-of-the-art algorithms.
- p.13 conclusion: In the future, we will continue to study simple and efficient models and explore time-series prediction models that are different from deep-learning networks.
