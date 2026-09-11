---
key: AYIUEUGK
title: "Semi-supervised LSTM with historical feature fusion attention for temporal sequence dynamic modeling in industrial processes"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2022.105547"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries` → `3. Methodology` → `4. Case study` → `5. Concluding remarks`。前置 `ABSTRACT`、`ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段浅层模型、深度学习、RNN/LSTM、半监督）。Introduction 末有编号贡献 + 节序路标。Method 拆成预备知识与 Methodology。Experiments 标题为 `Case study`。结论标题为 `Concluding remarks`。

## Openers

- abstract: `In modern industrial processes` — "In modern industrial processes, the data-driven soft sensor technology has been widely used for the prediction of key quality variables."
- introduction: `In modern industrial processes` — "In modern industrial processes, the real-time measurement value of key quality variable is the important indicator to evaluate the production quality of industrial products and ensure the production safety"
- method: `In the actual industrial` — "In the actual industrial processes, harsh production environment and expensive online monitoring equipment are common phenomena." (s.3.1)
- experiments: `The time series regression` — "The time series regression modeling framework based on HFFA-SSLSTM is shown in Fig. 4."
- conclusion: `In this paper` — "In this paper, a semi-supervised LSTM based on HFFA method is proposed for temporal sequence dynamic modeling in industrial processes."

## Gap transitions

- however (abstract): "However, traditional LSTM cannot fully utilize the process data with irregular sampling frequency and the guidance value of historical data samples for feature learning."
- to address (abstract): "To address these issues, a novel semi-supervised LSTM with history feature fusion attention (HFFA-SSLSTM) model is proposed in this paper."
- however (introduction): "However, due to the limitations of expensive measuring instruments and harsh industrial site environment, the values of quality variables are difficult to obtain by on-line measurement"
- however (introduction): "However, the existing methods still cannot effectively solve the three difficult problems issues in industrial process data modeling"
- in order to solve (introduction): "In order to solve the above issues, this paper proposes a novel semi-supervised LSTM with historical feature fusion attention (HFFA-SSLSTM) algorithm"

## Hedge verbs

- is proposed / causal / abstract, introduction, conclusion: "a novel semi-supervised LSTM ... is proposed in this paper"; "this paper proposes"; "is proposed for temporal sequence dynamic modeling"
- demonstrate / causal / abstract: "The experimental results on the actual industrial hydrocracking data set demonstrate the effectiveness"
- show / associative / introduction: "the experimental results based on actual industrial process data show that the proposed algorithm can effectively predict"
- validate / causal / conclusion: "The effectiveness of the proposed HFFA-SSLSTM method is validated on the real industrial hydrocracking process."

## Cross-section linkers

- introduction → method: "The remaining sections of this paper are structured as follows. Section 2 introduces LSTM and attention mechanism. Then, the semi-supervised LSTM is overviewed and the proposed HFFA-SSLSTM is illustrated in detail in Section 3. After that, the effectiveness and feasibility of proposed approach are demonstrated in a real industrial case in Section 4. Finally, conclusions are given in Section 5."
- method → experiments: HFFA 公式后 `4. Case study`
- experiments → conclusion: 误差分布图后 `5. Concluding remarks`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remaining sections of this paper are structured as follows`
- R004 编号贡献：`The main contributions of our paper are given as follows.`
- R009 自称：`is proposed in this paper` / `this paper proposes` / `In this paper, ... is proposed`

## Candidate phrases

- `To address these issues, a novel ... model is proposed in this paper.` (abstract)
- `In order to solve the above issues, this paper proposes` (introduction)
- `The main contributions of our paper are given as follows.` (introduction)
- `The remaining sections of this paper are structured as follows.` (introduction)
- `In this paper, a semi-supervised LSTM based on HFFA method is proposed` (conclusion)

## House style

自称 `is proposed in this paper` / `this paper proposes` / `In this paper` / `our paper`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: In modern industrial processes, the data-driven soft sensor technology has been widely used for the prediction of key quality variables.
- abstract: However, traditional LSTM cannot fully utilize the process data with irregular sampling frequency and the guidance value of historical data samples for feature learning.
- abstract: To address these issues, a novel semi-supervised LSTM with history feature fusion attention (HFFA-SSLSTM) model is proposed in this paper.
- abstract: The experimental results on the actual industrial hydrocracking data set demonstrate the effectiveness of the proposed HFFA-SSLSTM model and its possibility of applicating in real industrial processes.
- introduction: In modern industrial processes, the real-time measurement value of key quality variable is the important indicator to evaluate the production quality of industrial products and ensure the production safety
- introduction: In order to solve the above issues, this paper proposes a novel semi-supervised LSTM with historical feature fusion attention (HFFA-SSLSTM) algorithm to capture meaningful historical dynamic characteristics in the process data.
- introduction: The main contributions of our paper are given as follows.
- introduction: The remaining sections of this paper are structured as follows. Section 2 introduces LSTM and attention mechanism.
- method: In the actual industrial processes, harsh production environment and expensive online monitoring equipment are common phenomena.
- experiments: The time series regression modeling framework based on HFFA-SSLSTM is shown in Fig. 4.
- experiments: Therefore, the proposed HFFA-SSLSTM method can perform the best prediction performance with the smallest RMSE and the largest R2 on the whole data set.
- conclusion: In this paper, a semi-supervised LSTM based on HFFA method is proposed for temporal sequence dynamic modeling in industrial processes.
- conclusion: The effectiveness of the proposed HFFA-SSLSTM method is validated on the real industrial hydrocracking process.
- conclusion: In future research work, we will deeply analyze adaptive optimization models based on different ratios of unlabeled and labeled data to deal with the frequent fluctuation of working conditions in the actual industrial process.
