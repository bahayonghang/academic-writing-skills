---
key: VP94XA9Z
title: "Industrial process time-series modeling based on adapted receptive field temporal convolution networks concerning multi-region operations"
venue: "Computers & Chemical Engineering"
doi: "10.1016/j.compchemeng.2020.106877"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. The temporal convolution networks` → `3. The MRO-ARFTCN` → `4. Case study` → `5. Conclusion`。前置 `article info` / `Keywords` 与 `abstract`。无独立 Related Work。`related_work=inlined`（Introduction 中段 first-principles vs data-driven、RNN/CNN/GAN、TCN、层次聚类）。Introduction 末有方法陈述 + 节序路标。Method 含 causal/dilated/residual TCN、层次聚类、adapted receptive field。Experiments 标题为 `4. Case study`（甲醇生产）。

## Openers

- abstract: `Traditionally, recurrent neural` — "Traditionally, recurrent neural networks (RNNs) are employed to deal with industrial process data with time-series characteristics."
- introduction: `As modern industrial` — "As modern industrial processes are becoming more and more complicated, there has been an increasing difficulty in establishing efficient process models (Dietmair and Verl, 2009)."
- method: `Considering that the` — "Considering that the industrial process time series usually involve causal relations, the causal convolution of TCNs takes a specific featured structure to capture this analysis, as shown in Fig. 1."
- experiments: `An industrial methanol` — "An industrial methanol production process is considered here for method validations."
- conclusion: `Industrial process data` — "Industrial process data are always of time-series and causality characteristics."

## Gap transitions

- however (abstract): "However, the time-consuming iterative feature of RNN may result in slow computation speeds and limited modeling accuracies when dealing with high dimensional and long horizon data from industrial operation."
- however (introduction): "However, the increasing complexity of industrial processes poses greater challenges in characterizing the exact theoretical input-output relationship (Wang et al., 2019)."
- nevertheless (introduction): "Nevertheless, traditional numerical methods encounter problems with limited accuracy with dealing with high dimension and long operating horizon problems."
- despite (introduction): "Despite the existing efforts, the receptive field of the TCN still faces challenges of fully utilizations of historical data, as the receptive field increases with the growing number of hidden layers, which no doubt results in heavier computational burdens."
- however (method): "However, it is difficult for the conventional TCN to consider historical data information over long periods, which means too many hidden layers must be added to cover input data."

## Hedge verbs

- is introduced / causal / abstract: "In response to this problem, an adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN) is introduced in this paper."
- demonstrates / associative / abstract: "To verify the effectiveness of the proposed method, an industrial methanol production process is considered, which demonstrates a satisfying fitting result."
- has been proved / associative / abstract: "Additionally, compared with conventional RNNs and long-short-term-memory (LSTM) methods, the MRO-ARFTCN has been proved more tractable and useful for industrial process time-series modeling."
- we propose / causal / introduction: "In this paper, we propose an adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN) which both extracts causal characteristics among data and inherits the forwarding propagations from CNNs."
- we proposed / causal / conclusion: "In order to overcome these weaknesses, we proposed a novel adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN)"
- demonstrated / associative / conclusion: "Industrial process case studies explicitly demonstrated the benefits of the developed structure, compared to the traditional fitting methods."

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows: Section 2 addresses preliminaries of TCN structures; Section 3 introduces the adapted receptive field TCN concerning multi-region operations;"
- method → experiments: "in Section 4, an industrial methanol production process is investigated, where the proposed method, along with some experimental comparisons, are applied;"
- experiments → conclusion: "we conclude this paper and point out the future work in the last section."

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is organized as follows`
- R009 自称：`is introduced in this paper` / `In this paper, we propose` / `we proposed`

## Candidate phrases

- `an adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN) is introduced in this paper` (abstract)
- `In this paper, we propose an adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN)` (introduction)
- `The rest of this paper is organized as follows:` (introduction)
- `An industrial methanol production process is considered here for method validations.` (experiments)
- `we proposed a novel adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN)` (conclusion)

## House style

自称 `is introduced in this paper` / `In this paper, we propose` / `we proposed`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Traditionally, recurrent neural networks (RNNs) are employed to deal with industrial process data with time-series characteristics.
- abstract: In response to this problem, an adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN) is introduced in this paper.
- abstract: Additionally, compared with conventional RNNs and long-short-term-memory (LSTM) methods, the MRO-ARFTCN has been proved more tractable and useful for industrial process time-series modeling.
- introduction: As modern industrial processes are becoming more and more complicated, there has been an increasing difficulty in establishing efficient process models (Dietmair and Verl, 2009).
- introduction: In this paper, we propose an adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN) which both extracts causal characteristics among data and inherits the forwarding propagations from CNNs.
- introduction: The rest of this paper is organized as follows: Section 2 addresses preliminaries of TCN structures; Section 3 introduces the adapted receptive field TCN concerning multi-region operations;
- method: Considering that the industrial process time series usually involve causal relations, the causal convolution of TCNs takes a specific featured structure to capture this analysis, as shown in Fig. 1.
- experiments: An industrial methanol production process is considered here for method validations.
- experiments: Table 2 Testing errors with different methods. Methods The conventional RNN The LSTM The MRO-ARFTCN Errors 0.6940 0.5767 0.2631
- conclusion: Industrial process data are always of time-series and causality characteristics.
- conclusion: In order to overcome these weaknesses, we proposed a novel adapted receptive field temporal convolution network concerning multi-region operations (MRO-ARFTCN), which inherits the capability of effectively extracting causal characteristics among data and the fast computation from forward propagation.
- conclusion: Industrial process case studies explicitly demonstrated the benefits of the developed structure, compared to the traditional fitting methods.
