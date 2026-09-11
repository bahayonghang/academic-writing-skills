---
key: KS9M9DUY
title: "Hierarchical Self-Attention Network for Industrial Data Series Modeling With Different Sampling Rates Between the Input and Output Sequences"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2024.3388151"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. LSTM AND SELF-ATTENTION MECHANISM` → `III. HIERARCHICAL SELF-ATTENTION NETWORK (HSAN)` → hydrocracking case（IBP/FBP；IV 起于 p.6 评测公式后 `A. Hydrocracking Process`）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 first-principle / data-driven / DBN / SAE / RNN / LSTM / attention）。Introduction 末有 `The structure of this article is outlined as follows.`。Method 在 III。Experiments 为加氢裂化案例。

## Openers

- abstract: `For industrial processes` — "For industrial processes, it is significant to carry out the dynamic modeling of data series for quality prediction." (p.1)
- introduction: `IN PROCESS industry` — "IN PROCESS industry, the timely measurement of quality variables is very significant for effective quality control and process monitoring [1], [2], [3], [4], [5], [6]." (p.1；栏首掉字)
- method: `In this section` — "In this section, the HSAN is established for data series modeling with different rates between the input and output sequences in soft sensor modeling." (p.4, III)
- experiments: `In the refining` — "In the refining industry, hydrocracking is one of the most important processing methods that process crude oils into various products." (p.6, IV.A)
- conclusion: `An HSAN model` — "An HSAN model is developed for industrial data sequence modeling with different sampling rates between the input and output parts in this article." (p.9)

## Gap transitions

- however (abstract): "However, there are often different sampling rates between the input and output sequences." (p.1)
- nevertheless (introduction): "Nevertheless, in the actual production, the key quality variables are mostly obtained with off-line analyzers or laboratory tests, which is time-consuming and costly." (p.1)
- therefore (introduction): "Therefore, it is beneficial to provide a timely and low-cost approach to give real-time information about the quality indicators in process industry." (p.1)
- however (introduction): "However, a major of the deep networks, such as DBN [14] and SAE [19], are static models for soft sensor, which assume that the data samples are independent and identically distributed." (p.2)
- although (introduction): "Although LSTM unravels the problems of long-term dependencies to some degree, the performance of LSTM will degrade when the time sequence gets too long." (p.2)
- hence (introduction): "Hence, it is essential to utilize the massive unlabeled data sequences to learn the short-interval dependencies into dynamic prediction modeling." (p.2)
- therefore (conclusion): "Therefore, we aim to overcome the problem of training time costs for the large-scale datasets for future work." (p.9)

## Hedge verbs

- design / causal / abstract: "a hierarchical self-attention network (HSAN) is designed for adaptive dynamic modeling"
- propose / causal / abstract, introduction: "a self-attention layer of variable level is proposed"; "a hierarchical self-attention network (HSAN) is proposed"
- show / causal / abstract: "The experiment on an industrial hydrocracking process shows the effectiveness of HSAN."
- develop / causal / introduction, conclusion: "a hierarchical self-attention network (HSAN) is proposed"; "An HSAN model is developed"
- aim / speculative / conclusion: "we aim to overcome the problem of training time costs"

## Cross-section linkers

- introduction → method: "The structure of this article is outlined as follows. Section II introduces the LSTM and self-attention mechanisms. Section III establishes HSAN for addressing the issue of modeling input–output relations with varying rates in soft measurement modeling. In Section IV, the predictive capabilities of HSAN are validated in the hydrocracking process and compared with traditional and specialized models. Section V concludes by summarizing the advantages of HSAN and outlining the future research directions." (p.3)
- method → experiments: HSAN 预测框架后进入加氢裂化案例与 RMSE 定义 (p.6)
- experiments → conclusion: 推理时延分析后 `V. CONCLUSION` (p.9)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The structure of this article is outlined as follows` 指向 II–V。
- R004 贡献用 `the main contributions of this article are as follows` + 编号列表。
- R005 Conclusion 先收回方法，再用 `Therefore, we aim to` 指向后续。

## Candidate phrases

- `To handle these problems, a hierarchical self-attention network (HSAN) is designed` (abstract)
- `Inspired by this, a hierarchical self-attention network (HSAN) is proposed` (introduction)
- `the main contributions of this article are as follows.` (introduction)
- `The structure of this article is outlined as follows.` (introduction)
- `An HSAN model is developed for industrial data sequence modeling` (conclusion)

## House style

自称是 `in this article` / `a hierarchical self-attention network (HSAN) is proposed` / `the main contributions of this article`。未见 `Here we`、`In this paper`。`in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: For industrial processes, it is significant to carry out the dynamic modeling of data series for quality prediction.
- p.1 abstract: However, there are often different sampling rates between the input and output sequences.
- p.1 abstract: To handle these problems, a hierarchical self-attention network (HSAN) is designed for adaptive dynamic modeling.
- p.1 abstract: The experiment on an industrial hydrocracking process shows the effectiveness of HSAN.
- p.1 introduction: IN PROCESS industry, the timely measurement of quality variables is very significant for effective quality control and process monitoring [1], [2], [3], [4], [5], [6].
- p.1 introduction: Nevertheless, in the actual production, the key quality variables are mostly obtained with off-line analyzers or laboratory tests, which is time-consuming and costly.
- p.1 introduction: Therefore, it is beneficial to provide a timely and low-cost approach to give real-time information about the quality indicators in process industry.
- p.2 introduction: However, a major of the deep networks, such as DBN [14] and SAE [19], are static models for soft sensor, which assume that the data samples are independent and identically distributed.
- p.2 introduction: Although LSTM unravels the problems of long-term dependencies to some degree, the performance of LSTM will degrade when the time sequence gets too long.
- p.2 introduction: Hence, it is essential to utilize the massive unlabeled data sequences to learn the short-interval dependencies into dynamic prediction modeling.
- p.2–3 introduction: Inspired by this, a hierarchical self-attention network (HSAN) is proposed to deal with the aforementioned problems in this article.
- p.3 introduction: To summarize, the main contributions of this article are as follows.
- p.3 introduction: The structure of this article is outlined as follows. Section II introduces the LSTM and self-attention mechanisms. Section III establishes HSAN for addressing the issue of modeling input–output relations with varying rates in soft measurement modeling. In Section IV, the predictive capabilities of HSAN are validated in the hydrocracking process and compared with traditional and specialized models. Section V concludes by summarizing the advantages of HSAN and outlining the future research directions.
- p.4 method: In this section, the HSAN is established for data series modeling with different rates between the input and output sequences in soft sensor modeling.
- p.6 experiments: In the refining industry, hydrocracking is one of the most important processing methods that process crude oils into various products.
- p.9 conclusion: An HSAN model is developed for industrial data sequence modeling with different sampling rates between the input and output parts in this article.
- p.9 conclusion: Therefore, we aim to overcome the problem of training time costs for the large-scale datasets for future work.
