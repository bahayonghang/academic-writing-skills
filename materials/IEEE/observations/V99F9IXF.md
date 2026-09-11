---
key: V99F9IXF
title: "Gaussian-based Interval-Aware Transformer With Interval Embedding for Data Sequence Modeling With Irregular Sampling Frequency in Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3547031"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. GAUSSIAN-BASED INTERVAL-AWARE TRANSFORMER` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLS / PCR / SVM / SAE / CNN / RNN / LSTM / GRU / interval-aware LSTM）。Introduction 末有节序路标，指向 Section II–V。Method 标题为方法全称。Experiments 标题为 `CASE STUDIES`。

## Openers

- abstract: `Temporal feature representation` — "Temporal feature representation is critical for soft sensor modeling in industrial time sequences." (p.1)
- introduction: `MODERN industrial processes` — "MODERN industrial processes now face the challenge of transformation and upgrading because of the customer demands for superb product quality and the government policy of green production." (p.1；栏首掉字)
- method: `In industrial processes` — "In industrial processes, the sampling interval between two continuous records is changeable." (p.3)
- experiments: `In this section` — "In this section, the developed method is applied to an industrial hydrocracking process for quality prediction of C5 and C6 content of the light naphtha." (p.5)
- conclusion: `In this article` — "In this article, Gaussian-Trans are proposed to model industrial data with irregular sampling frequency." (p.9)

## Gap transitions

- however (abstract): "However, the data collected from industrial plants are usually sampled with irregular frequency, making it challenging for traditional methods to handle these temporally changeable relationships." (p.1)
- therefore (abstract): "Therefore, a Gaussian-based interval-aware transformer (GIA-Trans) with interval embedding is proposed in this article to model industrial data with irregular sampling frequency." (p.1)
- although (introduction): "Although these dynamic models are capable of capturing temporal relationships of time sequences, most of them assume that data samples collected from industrial processes are sampled with even frequency so that one uniform state-space model can be used for such relationship representations." (p.2)
- however (introduction): "However, most of the aforementioned models do not consider the irregular sampling frequency of time sequences and it is necessary to make use of these crucial sampling intervals." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a Gaussian-based interval-aware transformer (GIA-Trans) with interval embedding is proposed in this article"; "a Gaussian-based interval-aware transformer (GIA-Trans) is proposed"; "Gaussian-Trans are proposed"
- show / causal / experiments, conclusion: "The experimental results show that GIA-Trans can outperform the LSTM-based and Transformer-based methods."
- may / speculative / method: "Usually, the samples with small intervals tend to be more relevant. If there are large intervals, the samples may have weak correlations."
- indicate / associative / experiments: "The values of pa - pg are smaller than 0.05, which indicate that the seven null hypotheses are rejected."

## Cross-section linkers

- introduction → preliminaries: "The rest of this article are organized as follows. In Section II, transformer framework and self-attention mechanism are briefly introduced. Then, the structure of the proposed GIA-Trans is described in detail in Section III. Next, in Section IV, the effectiveness of the proposed GIA-Trans is validated by two cases in industrial processes. Finally, Section V concludes this article." (p.2)
- method → experiments: 软测量建模段落后 `IV. CASE STUDIES` (p.5)
- experiments → conclusion: t-test 段落后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 摘要缺口后用 `Therefore, a ... is proposed in this article`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this article are organized as follows` 指向 II–V（本篇 `are` 为原文）。
- R004 贡献用 `The main contributions of this article are given as follows` + 编号列表。
- R005 结论用 `In the future, we will explore` 指向后续。

## Candidate phrases

- `Therefore, a Gaussian-based interval-aware transformer (GIA-Trans) with interval embedding is proposed in this article` (abstract)
- `In this article, a Gaussian-based interval-aware transformer (GIA-Trans) is proposed` (introduction)
- `The main contributions of this article are given as follows.` (introduction)
- `The rest of this article are organized as follows.` (introduction)
- `In this article, Gaussian-Trans are proposed` (conclusion)
- `In the future, we will explore` (conclusion)

## House style

自称是 `proposed in this article` / `In this article` / `the proposed GIA-Trans`。未见 `Here we`、`In this paper`。`proposed in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Temporal feature representation is critical for soft sensor modeling in industrial time sequences.
- p.1 abstract: However, the data collected from industrial plants are usually sampled with irregular frequency, making it challenging for traditional methods to handle these temporally changeable relationships.
- p.1 abstract: Therefore, a Gaussian-based interval-aware transformer (GIA-Trans) with interval embedding is proposed in this article to model industrial data with irregular sampling frequency.
- p.1 introduction: MODERN industrial processes now face the challenge of transformation and upgrading because of the customer demands for superb product quality and the government policy of green production.
- p.2 introduction: Although these dynamic models are capable of capturing temporal relationships of time sequences, most of them assume that data samples collected from industrial processes are sampled with even frequency so that one uniform state-space model can be used for such relationship representations.
- p.2 introduction: However, most of the aforementioned models do not consider the irregular sampling frequency of time sequences and it is necessary to make use of these crucial sampling intervals.
- p.2 introduction: In this article, a Gaussian-based interval-aware transformer (GIA-Trans) is proposed to model time series with irregular sampling intervals in industrial processes.
- p.2 introduction: The main contributions of this article are given as follows.
- p.2 introduction: The rest of this article are organized as follows. In Section II, transformer framework and self-attention mechanism are briefly introduced. Then, the structure of the proposed GIA-Trans is described in detail in Section III. Next, in Section IV, the effectiveness of the proposed GIA-Trans is validated by two cases in industrial processes. Finally, Section V concludes this article.
- p.3 method: In industrial processes, the sampling interval between two continuous records is changeable.
- p.5 experiments: In this section, the developed method is applied to an industrial hydrocracking process for quality prediction of C5 and C6 content of the light naphtha.
- p.6 experiments: GIA-Trans has the best prediction performance among all methods because it considers both positional and temporal information and captures these interval-aware temporal features.
- p.9 experiments: The values of pa - pg are smaller than 0.05, which indicate that the seven null hypotheses are rejected.
- p.9 conclusion: In this article, Gaussian-Trans are proposed to model industrial data with irregular sampling frequency.
- p.10 conclusion: The experimental results show that GIA-Trans can outperform the LSTM-based and Transformer-based methods.
- p.10 conclusion: In the future, we will explore multistep ahead prediction of key quality variables in industrial processes with irregular sampling frequences for better operation of industrial systems.
