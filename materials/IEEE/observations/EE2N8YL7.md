---
key: EE2N8YL7
title: "Predicting Water Quality With Nonstationarity: Event-Triggered Deep Fuzzy Neural Network"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2024.3354919"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. EVENT-TRIGGERED DFNN` → `IV.` 实验与应用（水质案例） → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 ANN/ARIMA、DBN、集成深度网络、模糊学习与 event-triggered DBN）。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 在 IV（古北口 / 天桥 + 京津冀应用）。

## Openers

- abstract: `Water quality prediction` — "Water quality prediction is an indispensable task in water environment and source management." (p.2690)
- introduction: `IN THE past` — "IN THE past few decades, water environment and water resource suffered from a series of pollutions, which have been attracting more and more attention from government agencies, academia and civil-society organizations." (p.2690；栏首掉字)
- method: `In the formulated` — "In the formulated problem shown in (3), P1 and P2 are actually caused by the layer-by-layer error back-propagation and unchanged training policy of parameters d : Φ → A." (p.2692, III)
- experiments: `To demonstrate the` — "To demonstrate the effectiveness of ET-DFNN, MAE, and RMSE are used to quantify the prediction accuracy" (p.2695, IV)
- conclusion: `This article is` — "This article is the first attempt to improve the performance of water quality predictive model from characterizing the nonstationarity of water environment dynamic process based on event-triggered deep fuzzy learning." (p.2698)

## Gap transitions

- however (abstract): "However, the state of water environment is a dynamic process where the stationarity of water quality data suffers from time variation and human activities, which leads to a poor prediction accuracy because ANNs receive whole water quality data passively, including abnormal conditions." (p.2690)
- however (introduction): "However, although these methods were successfully used to predict water quality, they have almost reached the ceiling in improving the performance." (p.2690)
- although (introduction): "Although the combination of deep learning and supervised learning performs well in addressing the first difficulty mentioned above, they have not well-solved the problems of uncertainties and outlier data caused by the time variation and human activities [25], [26], [27], [28], [29], [30], [31]." (p.2691)
- therefore (introduction): "Therefore, the event-driven strategy is considered as a promising solution to address the second difficulty." (p.2691)
- motivated by (introduction): "Motivated by the analysis mentioned above, this article proposes an event-triggered deep fuzzy neural network (ET-DFNN) to improve the performance of water quality prediction." (p.2691)

## Hedge verbs

- propose / causal / abstract, introduction: "we consider such a tough problem in this article and propose an event-triggered deep fuzzy neural network (ET-DFNN)"; "this article proposes an event-triggered deep fuzzy neural network (ET-DFNN)"
- show / causal / abstract, experiments: "The practical data-based experimental results show that the ET-DFNN achieves better prediction performance in accuracy and efficiency than its peers."
- demonstrate / causal / introduction: "The applicability and advantages of ET-DFNN are demonstrated by water quality prediction experiments of water environment in Beijing–Tianjin–Hebei region."
- conclude / causal / experiments: "From these results, we conclude that the ET-DFNN model generally performs better than the other models in water quality prediction"
- indicate / causal / experiments: "which is indicated by the adaptive training strategies d : Φ → A"

## Cross-section linkers

- introduction → problem: "The rest of this article is organized as follows. We formulate the problem in Section II, present ET-DFNN in Section III. Section IV give experimental results and application demonstration. Finally, Section V concludes this aticle." (p.2691)
- problem → method: Remark 2 将 P1/P2 标出后直接 `III. EVENT-TRIGGERED DFNN` (p.2692)
- method → experiments: 收敛分析后进入 IV 水质案例 (p.2695)
- experiments → conclusion: Discussion 五条规律后直接 `V. CONCLUSION` (p.2698)

## Candidate rules

- R001 abstract 用 `We consider such a tough problem in this article and propose`，再用 First / Second / Third 铺开。
- R002 Introduction 无独立 Related Work，用编号困难 1–2，再评模糊学习与事件触发。
- R003 贡献列表标题用 `The major contributions are summarized as follows.`
- R004 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 开篇用 `This article is the first attempt to`，再用 `In the future, we will focus on the following works.` 编号三条。

## Candidate phrases

- `We consider such a tough problem in this article and propose` (abstract)
- `Motivated by the analysis mentioned above, this article proposes` (introduction)
- `The major contributions are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article is the first attempt to` (conclusion)

## House style

自称是 `this article` / `we propose` / `the proposed ET-DFNN`。未见 `Here we`。`this article proposes` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.2690 abstract: Water quality prediction is an indispensable task in water environment and source management.
- p.2690 abstract: However, the state of water environment is a dynamic process where the stationarity of water quality data suffers from time variation and human activities, which leads to a poor prediction accuracy because ANNs receive whole water quality data passively, including abnormal conditions.
- p.2690 abstract: We consider such a tough problem in this article and propose an event-triggered deep fuzzy neural network (ET-DFNN) to pursue the better performance of water quality prediction in the complex water environment.
- p.2690 abstract: Especially, the training efficiency of ET-DFNN is improved by 57.94% on total phosphorus prediction and 48.31% on biochemical oxygen demand prediction, respectively.
- p.2690 introduction: IN THE past few decades, water environment and water resource suffered from a series of pollutions, which have been attracting more and more attention from government agencies, academia and civil-society organizations.
- p.2690 introduction: However, although these methods were successfully used to predict water quality, they have almost reached the ceiling in improving the performance.
- p.2691 introduction: Although the combination of deep learning and supervised learning performs well in addressing the first difficulty mentioned above, they have not well-solved the problems of uncertainties and outlier data caused by the time variation and human activities [25], [26], [27], [28], [29], [30], [31].
- p.2691 introduction: Therefore, the event-driven strategy is considered as a promising solution to address the second difficulty.
- p.2691 introduction: Motivated by the analysis mentioned above, this article proposes an event-triggered deep fuzzy neural network (ET-DFNN) to improve the performance of water quality prediction.
- p.2691 introduction: The major contributions are summarized as follows.
- p.2691 introduction: The rest of this article is organized as follows. We formulate the problem in Section II, present ET-DFNN in Section III. Section IV give experimental results and application demonstration. Finally, Section V concludes this aticle.
- p.2692 method: In this section, we propose an ET-DFNN, and show that P1 and P2 can be addressed by using the deep fuzzy learning and event-triggered learning.
- p.2696 experiments: From Figs. 5 and 6, it is concluded that the trained ET-DFNN not only achieves a satisfactory prediction accuracy, but also has good stability and generalization in predicting future trends.
- p.2697 experiments: From these results, we conclude that the ET-DFNN model generally performs better than the other models in water quality prediction because of the effective combination of event-triggered learning, deep feature learning, and fuzzy learning.
- p.2698 experiments: Especially, when predicting BOD with the more frequent fluctuations than TP, the ET-DFNN is still efficient.
- p.2698 conclusion: This article is the first attempt to improve the performance of water quality predictive model from characterizing the nonstationarity of water environment dynamic process based on event-triggered deep fuzzy learning.
- p.2698 conclusion: The results show that the proposed ET-DFNN generally performs better than the other models in prediction performance, including accuracy and computational complexity as well as their tradeoffs.
- p.2698 conclusion: In the future, we will focus on the following works.
