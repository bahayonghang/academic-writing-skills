---
key: TPBS7EHV
title: "Soft Sensing for Time Series With Irregular Sampling Internals Based on a Denoising Interval Attention LSTM Network"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2025.3598583"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROPOSED APPROACH` → `III.`（软测量应用/去噪验证）→ `IV.`（脱丁烷塔与青霉素发酵）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评机理/数据驱动、SDAE、LSTM/GRU、不规则采样插值与区间 LSTM）。Introduction 末有节序路标，指向 Section II–V。Method 紧接引言。Experiments 为工业案例（debutanizer column + penicillin fermentation）。

## Openers

- abstract: `The prediction of` — "The prediction of key quality variables plays an important role in industrial status identification and monitoring." (p.1)
- introduction: `IN MODERN industrial` — "IN MODERN industrial process control, due to technical or economic reasons, many key physical or chemical quantities are difficult to measure directly by hardware devices in real time [1]." (p.1；栏首掉字)
- method: `The above description` — "The above description indicates that the traditional SDAE model is capable of producing an abstract representation of the original data within the spatial domain." (p.3, II)
- experiments: `The debutanizer column` — "The debutanizer column tries to separate and desulphurize naphtha, which has been widely applied in modern petrochemical refining." (p.6)
- conclusion: `To address the` — "To address the challenges of industrial processes affected by noise and irregular sampling intervals, this article introduces a novel soft sensing model named SSRDAE-IALSTM." (p.12)

## Gap transitions

- unfortunately (introduction): "Unfortunately, shallow neural networks have limited capacity to express complex features within data, while deep learning algorithms have emerged as vital modeling tools in the field of soft sensing technology with their strong feature representation capabilities." (p.1)
- however (introduction): "However, a critical limitation of these methods arises in time series analysis, where they frequently overlook the inherent temporal correlations within the data." (p.2)
- unfortunately (introduction): "Unfortunately, these methods can only capture the influence of the nearest neighbor sample, and cannot focus on the samples of different time steps." (p.2)
- in order to (introduction): "In order to solve the above problems, a stacked supervised and reconstructed input denoising autoencoder integrated with internal attention long short-term memory (SSRDAE-IALSTM) network is proposed for soft sensing modeling." (p.2)
- however (method): "However, each DAE generates high-level hidden features based on the low-level features, which are learned in the preceding stage." (p.3)
- however (conclusion): "However, deployment in real-time industrial settings may encounter challenges such as latency, robustness to unseen noise, and model updating." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a stacked supervised and reconstructed input denoising autoencoder"; "a ... network is proposed for soft sensing modeling"
- show / causal / abstract, experiments: "The experimental results show that the proposed model can enhance the learning ability of process features"; "the proposed model consistently exhibits superior predictive outcomes"
- indicate / causal / method: "The above description indicates that the traditional SDAE model is capable of producing an abstract representation"
- introduce / causal / conclusion: "this article introduces a novel soft sensing model named SSRDAE-IALSTM"
- may / speculative / conclusion: "deployment in real-time industrial settings may encounter challenges such as latency, robustness to unseen noise, and model updating"

## Cross-section linkers

- introduction → method: "The rest of this article is structured as follows. In Section II, the framework and modeling procedures of the proposed SSRDAE-IALSTM model are introduced in detail, followed by the soft sensing application of the proposed approach in Section III. Two industrial processes are verified, and experimental results are given and analyzed in Section IV. Finally, Section V gives the conclusion of this article." (p.3)
- method → experiments: Algorithm 1 与去噪仿真后进入脱丁烷塔案例 (p.6)
- experiments → conclusion: 噪声水平评估后 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `this article proposes` + 方法缩写，不用 `Here we`。
- R002 Introduction 无独立 Related Work；SDAE/LSTM/不规则采样评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is structured as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this work are condensed as follows` + 编号列表。
- R005 Conclusion 用 `this article introduces a novel`，再用 `However, deployment in real-time industrial settings may encounter` 指向后续。

## Candidate phrases

- `To solve the above problems, this article proposes` (abstract)
- `The main contributions of this work are condensed as follows.` (introduction)
- `The rest of this article is structured as follows.` (introduction)
- `this article introduces a novel soft sensing model named` (conclusion)
- `in our feature work, we will utilize lightweight models` (conclusion)

## House style

自称是 `this article proposes` / `this article introduces` / `the proposed model` / `the method proposed in this article`。未见 `Here we`。`this article proposes` 与 `this article introduces` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: The prediction of key quality variables plays an important role in industrial status identification and monitoring.
- p.1 abstract: To solve the above problems, this article proposes a stacked supervised and reconstructed input denoising autoencoder integrated with internal attention long short-term memory (SSRDAE-IALSTM) network for soft sensing modeling.
- p.1 abstract: The experimental results show that the proposed model can enhance the learning ability of process features and obtain better prediction performance than other comparison methods.
- p.1 introduction: IN MODERN industrial process control, due to technical or economic reasons, many key physical or chemical quantities are difficult to measure directly by hardware devices in real time [1].
- p.2 introduction: However, a critical limitation of these methods arises in time series analysis, where they frequently overlook the inherent temporal correlations within the data.
- p.2 introduction: Unfortunately, these methods can only capture the influence of the nearest neighbor sample, and cannot focus on the samples of different time steps.
- p.2 introduction: In order to solve the above problems, a stacked supervised and reconstructed input denoising autoencoder integrated with internal attention long short-term memory (SSRDAE-IALSTM) network is proposed for soft sensing modeling.
- p.2 introduction: The main contributions of this work are condensed as follows.
- p.3 introduction: The rest of this article is structured as follows. In Section II, the framework and modeling procedures of the proposed SSRDAE-IALSTM model are introduced in detail, followed by the soft sensing application of the proposed approach in Section III. Two industrial processes are verified, and experimental results are given and analyzed in Section IV. Finally, Section V gives the conclusion of this article.
- p.3 method: The above description indicates that the traditional SDAE model is capable of producing an abstract representation of the original data within the spatial domain.
- p.6 experiments: The debutanizer column tries to separate and desulphurize naphtha, which has been widely applied in modern petrochemical refining.
- p.7 experiments: As can be seen in Table V and Fig. 7, the proposed model is superior to other comparison methods.
- p.11 experiments: Unfortunately, in the actual data with noise, their predicted values still fluctuate greatly.
- p.12 experiments: This consistent superiority further underscores the effectiveness of the proposed model, primarily attributed to its dual reconstruction mechanism and interval attention framework.
- p.12 conclusion: To address the challenges of industrial processes affected by noise and irregular sampling intervals, this article introduces a novel soft sensing model named SSRDAE-IALSTM.
- p.12 conclusion: The experimental results show that the proposed model achieves good performance when the time series data with irregular sampling intervals contain different levels of noise.
- p.12 conclusion: However, deployment in real-time industrial settings may encounter challenges such as latency, robustness to unseen noise, and model updating.
