---
key: 8MXNV43T
title: "Time Series Prediction Method of Industrial Process With Limited Data Based on Transfer Learning"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3191980"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PROPOSED MODEL` → `IV. EXPERIMENTAL VERIFICATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（`RELATED WORKS`：工业时序预测 + 迁移学习）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `EXPERIMENTAL VERIFICATION`（太阳能发电 + 加热炉温度）。

## Openers

- abstract: `Industrial time series` — "Industrial time series, as a kind of data that responds to production process information, can be analyzed and predicted for effective monitoring of industrial production processes." (p.6872)
- introduction: `TIME series as` — "TIME series, as a kind of structured data that reflects the dynamic changes of various indicators in the industrial data, contains information of industrial production process at each moment." (p.6872)
- related_work: `In the actual` — "In the actual production process, industrial time series prediction can be divided into low-frequency time series prediction and high-frequency time series prediction according to the data sampling frequency." (p.6873)
- method: `To address the` — "To address the problems of limited data volume and cold start in industrial time series modeling, we use historical data of similar equipment or similar working conditions to assist the modeling of data under existing moments." (p.6874)
- experiments: `To verify the` — "To verify the effectiveness of the proposed industrial time series prediction method, we conducted one-step and multistep time series prediction experiments on the open-source solar power plant energy output dataset and the real heating furnace operation dataset." (p.6877)
- conclusion: `In conclusion we` — "In conclusion, we propose an industrial time series prediction method with limited data and verify the effectiveness of the method on the solar power plant dataset and the real heating furnace operation dataset." (p.6880)

## Gap transitions

- to address (abstract): "To address the aforementioned problems, we propose a new time series prediction method for industrial processes under limited data based on dynamic transfer learning in this work." (p.6872)
- however (introduction): "However, these data-driven industrial process modeling methods face the following difficulties." (p.6872)
- unfortunately (introduction): "Unfortunately, few studies have applied transfer learning methods to industrial time series forecasting." (p.6873)
- therefore (introduction): "Therefore, this article considers how to build a dynamic transfer learning model based on the neural network structure" (p.6873)
- however (related_work): "However, such methods require a large amount of training data, and the computational cost increases as the number of hidden layers increases." (p.6874)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a new time series prediction method ... in this work"; "we propose a new transfer learning framework"; "we propose an industrial time series prediction method"
- demonstrate / causal / abstract: "experiments on two real-world datasets ... demonstrate the effectiveness of the proposed method"
- show / causal / method: "The aforementioned analysis shows that the existing multistep prediction model based on LSTM does not make good use of the output of the previous moment"
- can / speculative / conclusion: "the proposed one-step and multistep time series prediction methods can significantly improve the prediction accuracy"

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. Section II introduces the related work of the industrial time series prediction model based on transfer learning. Section III introduces the method in detail and theoretical background. In Section IV, the method is verified by experiments, and the results are analyzed and discussed. Finally, Section V concludes this article." (p.6873)
- related_work → method: 综述后 `III. PROPOSED MODEL` (p.6874)
- method → experiments: 框架总结后 `IV. EXPERIMENTAL VERIFICATION` (p.6877)
- experiments → conclusion: 结果讨论后 `V. CONCLUSION` (p.6880)

## Candidate rules

- R006 独立 Related Work（`RELATED WORKS`）。
- R007 摘要用 `To address the aforementioned problems, we propose` 点名方法。
- R004 贡献为编号列表（引言后半）。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法，强调一步/多步与网络通用性；未见单独 Limitations 段。

## Candidate phrases

- `To address the aforementioned problems, we propose` (abstract)
- `we propose a new time series prediction method ... in this work` (abstract)
- `The rest of this article is organized as follows.` (introduction)
- `In conclusion, we propose` (conclusion)

## House style

自称 `we propose` / `in this work` / `this article` / `In conclusion, we propose`。未见 `Here we`。有 `in this work`，未见 `In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.6872 abstract: Industrial time series, as a kind of data that responds to production process information, can be analyzed and predicted for effective monitoring of industrial production processes.
- p.6872 abstract: To address the aforementioned problems, we propose a new time series prediction method for industrial processes under limited data based on dynamic transfer learning in this work.
- p.6872 abstract: Compared with other commonly used methods, experiments on two real-world datasets of solar power generation prediction and heating furnace temperature prediction demonstrate the effectiveness of the proposed method.
- p.6872 introduction: TIME series, as a kind of structured data that reflects the dynamic changes of various indicators in the industrial data, contains information of industrial production process at each moment.
- p.6872 introduction: However, these data-driven industrial process modeling methods face the following difficulties.
- p.6873 introduction: Unfortunately, few studies have applied transfer learning methods to industrial time series forecasting.
- p.6873 introduction: Therefore, this article considers how to build a dynamic transfer learning model based on the neural network structure, which determines which hidden layers can be transferred based on minimizing the differences between the source and target domains, so that the historical data information of similar operating conditions or equipment can effectively assist the parameter prediction needs under the limited data at the current moment.
- p.6873 introduction: The rest of this article is organized as follows. Section II introduces the related work of the industrial time series prediction model based on transfer learning. Section III introduces the method in detail and theoretical background. In Section IV, the method is verified by experiments, and the results are analyzed and discussed. Finally, Section V concludes this article.
- p.6873 related_work: In the actual production process, industrial time series prediction can be divided into low-frequency time series prediction and high-frequency time series prediction according to the data sampling frequency.
- p.6874 related_work: However, such methods require a large amount of training data, and the computational cost increases as the number of hidden layers increases.
- p.6874 method: To address the problems of limited data volume and cold start in industrial time series modeling, we use historical data of similar equipment or similar working conditions to assist the modeling of data under existing moments.
- p.6877 experiments: To verify the effectiveness of the proposed industrial time series prediction method, we conducted one-step and multistep time series prediction experiments on the open-source solar power plant energy output dataset and the real heating furnace operation dataset.
- p.6878 experiments: Therefore, when the data are limited, reasonable feature mapping can obviously improve the prediction accuracy of the neural network by making full use of the historical data of similar equipment or similar working conditions.
- p.6880 conclusion: In conclusion, we propose an industrial time series prediction method with limited data and verify the effectiveness of the method on the solar power plant dataset and the real heating furnace operation dataset.
- p.6880 conclusion: Experiments have proven that the proposed one-step and multistep time series prediction methods can significantly improve the prediction accuracy and solve the problem of industrial time series prediction with limited data.
