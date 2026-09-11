---
key: EZFEA6H5
title: "Dual Cross-Attention Transformer Networks for Temporal Predictive Modeling of Industrial Process"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3385820"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. DUAL CROSS-ATTENTION TRANSFORMER` → `IV. INDUSTRIAL APPLICATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mechanism-driven、PCA/PLS/SVR、ANN/DNN、LSTM 变体、LogSparse/Nonstationary/Informer/Autoformer）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `INDUSTRIAL APPLICATION`。

## Openers

- abstract: `Industrial predictive modeling` — "Industrial predictive modeling plays an important role in process control and optimization." (p.1)
- introduction: `COMPLEX industrial processes` — "COMPLEX industrial processes are usually characterized by high energy consumption and high pollution [1], [2], [3]." (p.1；栏首掉字)
- method: `The proposed DCAFormer` — "The proposed DCAFormer has dual encoder architectures in parallel." (p.3, III)
- experiments: `The real-world production` — "The real-world production data of aluminum electrolysis process are tested to verify DCAFormer." (p.6, IV)
- conclusion: `To address the` — "To address the problem of the conventional transformer model neglecting the dependencies between process variables and nonstationarity trend information in industrial time-series data, this article proposed a novel DCAFormer for industrial quality variable prediction." (p.10)

## Gap transitions

- however (abstract): "While the previous transformer-based industrial predictive models only considered the temporal information of the industrial time-series data, however, the different importance of the process variables is generally ignored." (p.1)
- however (introduction): "However, quality variables are mainly got by offline physical measurement due to its high cost." (p.1)
- however (introduction): "However, it requires the mastery of the domain knowledge, and the prediction performance is highly reliant on the mathematical model." (p.1)
- although (introduction): "Although these transformers contribute to the cross-time attention to learn temporal dependency from time sequences, the dependencies of time series across different variable dimensions and the inherent nonstationary trend information in original time series are not considered in previous works." (p.2)
- to address (conclusion): "To address the problem of the conventional transformer model neglecting the dependencies between process variables and nonstationarity trend information in industrial time-series data, this article proposed a novel DCAFormer for industrial quality variable prediction." (p.10)

## Hedge verbs

- propose / causal / abstract, introduction: "In this article, we propose a novel dual cross-attention-based transformer (DCAFormer)"; "this article proposes a dual cross-attention-based transformer (DCAFormer)"
- show / causal / abstract, conclusion: "The experimental results show that DCAFormer achieves better prediction performance than other competitive transformer models."; "The experimental results show that DCAFormer achieves better prediction performance in terms of RMSE and R2 indexes."
- proposed / causal / conclusion: "this article proposed a novel DCAFormer"
- will explore / speculative / conclusion: "we will explore how to incrementally update the predictive model"

## Cross-section linkers

- introduction → problem: "The structure of the article is as follows. In Section II, the problem formulation is described. In Section III, a detailed description of our proposed DCAFormer is provided. Subsequently, the experimental results are presented in Section IV. In Section V, conclusions are made." (p.2)
- method → experiments: Algorithm 1 与总体架构后 `IV. INDUSTRIAL APPLICATION` (p.6)
- experiments → conclusion: 对比实验 Table IV 后 `V. CONCLUSION` (p.10)

## Candidate rules

- R002 Introduction 无独立 Related Work，机制模型 / 浅层 ML / DNN / LSTM / transformer 变体评述写在引言中段，并以 `Although these transformers` 收束缺口。
- R003 Introduction 末用 `The structure of the article is as follows` 指向 II–V。
- R004 贡献用 `The main contributions of our paper are threefold` + 编号列表（条目数实际为 4）。
- R005 Conclusion 先 `To address the problem` 收回方法，再用 `Meanwhile` + `we will explore` 指向后续。

## Candidate phrases

- `In this article, we propose a novel` (abstract)
- `The main contributions of our paper are threefold.` (introduction)
- `The structure of the article is as follows.` (introduction)
- `this article proposed a novel` (conclusion)
- `we will explore how to incrementally update` (conclusion)

## House style

自称 `this article` / `we propose` / `our proposed DCAFormer`。贡献句出现 `our paper`。未见 `Here we`。`In this article, we propose` 与 `this article proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Industrial predictive modeling plays an important role in process control and optimization.
- p.1 abstract: While the previous transformer-based industrial predictive models only considered the temporal information of the industrial time-series data, however, the different importance of the process variables is generally ignored.
- p.1 abstract: In this article, we propose a novel dual cross-attention-based transformer (DCAFormer) to capture both the cross-time dependencies and the cross-variable dependencies in parallel for better predictability.
- p.1 abstract: The experimental results show that DCAFormer achieves better prediction performance than other competitive transformer models.
- p.1 introduction: COMPLEX industrial processes are usually characterized by high energy consumption and high pollution [1], [2], [3].
- p.1 introduction: However, quality variables are mainly got by offline physical measurement due to its high cost.
- p.1 introduction: However, it requires the mastery of the domain knowledge, and the prediction performance is highly reliant on the mathematical model.
- p.2 introduction: Although these transformers contribute to the cross-time attention to learn temporal dependency from time sequences, the dependencies of time series across different variable dimensions and the inherent nonstationary trend information in original time series are not considered in previous works.
- p.2 introduction: Different from the previous works that the self-attention mechanism only targets temporal dependence, this article proposes a dual cross-attention-based transformer (DCAFormer) to capture both the cross-time dependencies and the cross-variable dependencies of industrial time-series data, as shown in Fig. 1.
- p.2 introduction: The main contributions of our paper are threefold.
- p.2 introduction: The structure of the article is as follows. In Section II, the problem formulation is described. In Section III, a detailed description of our proposed DCAFormer is provided. Subsequently, the experimental results are presented in Section IV. In Section V, conclusions are made.
- p.3 method: The proposed DCAFormer has dual encoder architectures in parallel.
- p.6 experiments: The real-world production data of aluminum electrolysis process are tested to verify DCAFormer.
- p.10 conclusion: To address the problem of the conventional transformer model neglecting the dependencies between process variables and nonstationarity trend information in industrial time-series data, this article proposed a novel DCAFormer for industrial quality variable prediction.
- p.10 conclusion: The experimental results show that DCAFormer achieves better prediction performance in terms of RMSE and R2 indexes. It validates the effectiveness of our proposed DCAFormer.
- p.11 conclusion: Meanwhile, the real-world industrial process data are usually multibatch, which generally makes the established model mismatch, and we will explore how to incrementally update the predictive model to further improve the generalization capacity.
