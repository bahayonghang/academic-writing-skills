---
key: FHRFH9SH
title: "Memory-Adaptive Supervised LSTM Networks for Deep Soft Sensor Development of Industrial Processes"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2024.3398032"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. LSTM NETWORKS FOR SOFT SENSOR DEVELOPMENTS` → `III. THE MEMORY-ADAPTIVE SLSTM NETWORK` → 工业案例（debutanizer / SRU / `C. Tennessee-Eastman process`）→ `V. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLS / PCR / SVM / ANN / SAE / RNN / LSTM / SLSTM）。Section II 是 LSTM/SLSTM 预备，不是 Related Work 标题。Introduction 末有节序路标。Method 为 III。Experiments 为 Section IV 工业基准（摘要写三例，引言路标写两例，正文另有 TE）。作者稿页码为连续阿拉伯数字。

## Openers

- abstract: `In the recent` — "In the recent years, deep long-short term memory (LSTM) networks have achieved tremendous successes for soft-sensor developments of dynamical industrial processes." (p.1)
- introduction: `ENSURING process safety` — "ENSURING process safety and efficiency is a crucial task in the modern industry." (p.1；栏首掉字)
- method: `In this paper` — "In this paper, we respect the industrial practice that quality variables under supervision may be irregularly measured, and furthermore with significant time lags." (p.3, III.A)
- experiments: `In this debutanizer` — "In this debutanizer column (Fig. 4), the bottom butane concentration is considered as an influential variable for process control and monitoring, which is nonetheless difficult to measure." (p.7)
- conclusion: `In this paper` — "In this paper, we proposed a memory-adaptive supervised LSTM (MA-SLSTM) network for deep soft sensor developments of industrial processes." (p.12, V)

## Gap transitions

- however (abstract): "Furthermore, the supervised LSTM models have also been proposed to enhance the prediction accuracy, which however require real-time measurements of quality variables." (p.1)
- however (introduction): "However, traditional data-based methods have difficulty in handling the massive and complex data, where efficacious feature information cannot be extracted from the high-dimensional redundant data [17]." (p.1)
- therefore (introduction): "Therefore, it is essential to draw extreme attention to the online measurement delay and low sampling rate issues during the training process of supervised soft sensing models to address relevant problems in practical applications." (p.2)
- however (experiments): "However, the systematic errors can be eliminated using the proposed MA-SLSTM scheme, resulting in RMSE = 0.0372 and R2 = 0.9841, respectively, the best among all compared methods as listed in Tab. VI." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a novel memory-adaptive supervised LSTM (MA-SLSTM) network"; "this paper proposes a novel memory-adaptive supervised LSTM (MA-SLSTM) framework"
- may / speculative / method: "quality variables under supervision may be irregularly measured"
- show / causal / experiments: "As can be seen from Tab. VI and Fig. 18, for the regular LSTM method without supervision, these exist systematic prediction errors on the validation dataset."
- could / speculative / conclusion: "Combination of the state-of-art approaches with the proposed memory-adaptive scheme could strengthen their advantages."

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows. Section II reviews the classical LSTM network and its supervised form for soft sensor developments of industrial processes. Section III presents main contributions of this paper, namely, the proposed MA-SLSTM network. In addition, numerical techniques for solving the supervised problem are presented. In Section IV, two benchmark industrial problems, the debutanizer column and the sulfur recovery unit, are investigated to explore the proposed methodology. Finally, some conclusions and future research directions are remarked." (p.2)
- method → experiments: III 后进入 debutanizer / SRU / TE 案例 (p.7–11)
- experiments → conclusion: TE 段落后直接 `V. CONCLUSIONS` (p.12)

## Candidate rules

- R001 abstract 用 `In this paper, we propose a novel ... (ACRONYM)`。
- R002 Introduction 无独立 Related Work；Section II 只复习 LSTM/SLSTM。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–V。
- R004 贡献用 `The main novelties of this study are summarized as follows.` + 编号 (1)(2)。
- R005 Conclusion 先收回方法，再用 `Under the established framework of this paper, a number of interesting topics can be further explored.` 列未来工作。

## Candidate phrases

- `In this paper, we propose a novel` (abstract)
- `To address the aforementioned challenges, this paper proposes` (introduction)
- `The main novelties of this study are summarized as follows.` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `In this paper, we proposed a memory-adaptive supervised LSTM (MA-SLSTM) network` (conclusion)

## House style

自称是 `In this paper, we propose` / `this paper proposes` / `this study` / `the proposed method`。未见 `Here we`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `This article`。

## Quotes

- p.1 abstract: In the recent years, deep long-short term memory (LSTM) networks have achieved tremendous successes for soft-sensor developments of dynamical industrial processes.
- p.1 abstract: Furthermore, the supervised LSTM models have also been proposed to enhance the prediction accuracy, which however require real-time measurements of quality variables.
- p.1 abstract: In this paper, we propose a novel memory-adaptive supervised LSTM (MA-SLSTM) network, where the historical states in the deep LSTM models, including the long and short memories over the recent time window, are adaptively updated to track the quality variables.
- p.1 abstract: The advantages of the MA-SLSTM are illustrated through three industrial benchmark cases.
- p.1 introduction: ENSURING process safety and efficiency is a crucial task in the modern industry.
- p.1 introduction: However, traditional data-based methods have difficulty in handling the massive and complex data, where efficacious feature information cannot be extracted from the high-dimensional redundant data [17].
- p.2 introduction: Therefore, it is essential to draw extreme attention to the online measurement delay and low sampling rate issues during the training process of supervised soft sensing models to address relevant problems in practical applications.
- p.2 introduction: To address the aforementioned challenges, this paper proposes a novel memory-adaptive supervised LSTM (MA-SLSTM) framework.
- p.2 introduction: The main novelties of this study are summarized as follows.
- p.2 introduction: The rest of this paper is organized as follows. Section II reviews the classical LSTM network and its supervised form for soft sensor developments of industrial processes. Section III presents main contributions of this paper, namely, the proposed MA-SLSTM network.
- p.3 method: In this paper, we respect the industrial practice that quality variables under supervision may be irregularly measured, and furthermore with significant time lags.
- p.7 experiments: In this debutanizer column (Fig. 4), the bottom butane concentration is considered as an influential variable for process control and monitoring, which is nonetheless difficult to measure.
- p.11 experiments: However, the systematic errors can be eliminated using the proposed MA-SLSTM scheme, resulting in RMSE = 0.0372 and R2 = 0.9841, respectively, the best among all compared methods as listed in Tab. VI.
- p.12 conclusion: In this paper, we proposed a memory-adaptive supervised LSTM (MA-SLSTM) network for deep soft sensor developments of industrial processes.
- p.12 conclusion: The advantage of the new approach is that it does not require any strict assumption on the available measurement of quality variable.
- p.12 conclusion: Under the established framework of this paper, a number of interesting topics can be further explored.
