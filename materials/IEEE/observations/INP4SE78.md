---
key: INP4SE78
title: "Novel Multiscale Trend Decomposition LSTM Based on Feature Selection for Industrial Soft Sensing"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3444896"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED METHOD` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 BP/RBF/ELM、ESN、LSTM/Bi-LSTM、多尺度 LSTM）。Introduction 末无 `The rest of this article is organized as follows`，贡献列表后直接进入 II。II 为随机森林特征重要性与 LSTM 预备，不是综述节。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `Industrial soft sensing` — "Industrial soft sensing plays a crucial role in process modeling, optimization, and control, and is extensively utilized to predict hard-to-measure process variables." (p.14249)
- introduction: `IN THE realm` — "IN THE realm of industrial processes, accurate and timely monitoring is essential for ensuring efficiency and safety." (p.14249；栏首掉字)
- method: `In this section` — "In this section, a novel multiscale trend decomposition LSTM model based on feature selection (FS-MSTD-LSTM) for industrial soft sensing is proposed." (p.14251, III)
- experiments: `In this section` — "In this section, the effectiveness of the proposed FS-MSTD-LSTM soft-sensing model is evaluated using actual industrial data from wastewater treatment plant processes and the SRU process." (p.14253)
- conclusion: `In this article` — "In this article, an improved FS-MSTD-LSTM is proposed for developing soft sensors." (p.14256)

Preliminaries 首句："The evaluation of feature importance can quantitatively describe the contribution of a specific feature in classification or regression tasks." (p.14250, II.A)。不单列 `related_work` opener。

## Gap transitions

- to effectively (abstract): "To effectively manage complex process data with varying time scales, a novel multiscale trend decomposition long short-term memory model based on feature selection (FS-MSTD-LSTM) is proposed." (p.14249)
- consequently (introduction): "Consequently, these limitations have spurred the development and adoption of soft sensing techniques [2]." (p.14249)
- however (introduction): "However, since most process data are dynamic, static neural networks often fail to achieve acceptable accuracy." (p.14249)
- to address (introduction): "To address this limitation, recurrent neural networks (RNNs) have been adopted, as they excel at handling time-series data [10]." (p.14249)
- although (introduction): "Although the above improved models have achieved acceptable performance in kinds of fields, the time scales in data with short-, medium-and long-term scales are ignored, impacting their performance." (p.14250)
- to avoid (introduction): "To avoid this limitation, a novel multiscale trend decomposition long short-term memory integrated with feature selection (FS-MSTD-LSTM) is proposed in this article." (p.14250)

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "a novel ... (FS-MSTD-LSTM) is proposed"; "is proposed in this article"; "an improved FS-MSTD-LSTM is proposed"
- demonstrate / causal / abstract, introduction: "simulations on these datasets demonstrate that the FS-MSTD-LSTM model achieves higher soft sensing accuracy"
- indicate / associative / abstract, introduction: "indicating its superior performance in managing complex process data with varying time scales"
- confirm / causal / conclusion: "Simulations on two industrial datasets confirm the superior performance of FS-MSTD-LSTM"

## Cross-section linkers

- introduction → preliminaries: 贡献列表后无节序路标，直接 `II. PRELIMINARIES` (p.14250)
- method → experiments: 三步预测流程后直接 `IV. CASE STUDY` (p.14253)
- experiments → conclusion: SRU 箱线图后直接 `V. CONCLUSION` (p.14256)

## Candidate rules

- R001 摘要用被动 `is proposed`，不用 `Here we`。
- R002 Related Work 并入 Introduction；II 是 PRELIMINARIES。
- 本篇无 `The rest of this article is organized as follows`，不计入 R003。
- R004 贡献用 `In this article, the key contributions are as follows.` + 编号列表。
- R005 结论 `Moving forward` + `Future work should focus on`。

## Candidate phrases

- `To effectively manage ..., a novel ... is proposed.` (abstract)
- `To avoid this limitation, a novel ... is proposed in this article.` (introduction)
- `In this article, the key contributions are as follows.` (introduction)
- `In this article, an improved FS-MSTD-LSTM is proposed` (conclusion)
- `Future work should focus on` (conclusion)

## House style

自称 `is proposed` / `is proposed in this article` / `In this article` / `the proposed FS-MSTD-LSTM`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.14249 abstract: Industrial soft sensing plays a crucial role in process modeling, optimization, and control, and is extensively utilized to predict hard-to-measure process variables.
- p.14249 abstract: To effectively manage complex process data with varying time scales, a novel multiscale trend decomposition long short-term memory model based on feature selection (FS-MSTD-LSTM) is proposed.
- p.14249 abstract: The performance of the proposed FS-MSTD-LSTM model is evaluated using two industrial datasets, and simulations on these datasets demonstrate that the FS-MSTD-LSTM model achieves higher soft sensing accuracy compared to other related methods, indicating its superior performance in managing complex process data with varying time scales.
- p.14249 introduction: IN THE realm of industrial processes, accurate and timely monitoring is essential for ensuring efficiency and safety.
- p.14249 introduction: However, since most process data are dynamic, static neural networks often fail to achieve acceptable accuracy.
- p.14249 introduction: To address this limitation, recurrent neural networks (RNNs) have been adopted, as they excel at handling time-series data [10].
- p.14250 introduction: Although the above improved models have achieved acceptable performance in kinds of fields, the time scales in data with short-, medium-and long-term scales are ignored, impacting their performance.
- p.14250 introduction: To avoid this limitation, a novel multiscale trend decomposition long short-term memory integrated with feature selection (FS-MSTD-LSTM) is proposed in this article.
- p.14250 introduction: In this article, the key contributions are as follows.
- p.14251 method: In this section, a novel multiscale trend decomposition LSTM model based on feature selection (FS-MSTD-LSTM) for industrial soft sensing is proposed.
- p.14253 experiments: In this section, the effectiveness of the proposed FS-MSTD-LSTM soft-sensing model is evaluated using actual industrial data from wastewater treatment plant processes and the SRU process.
- p.14256 conclusion: In this article, an improved FS-MSTD-LSTM is proposed for developing soft sensors.
- p.14256 conclusion: Simulations on two industrial datasets confirm the superior performance of FS-MSTD-LSTM, demonstrating its effectiveness in managing complex process data with varying time scales.
- p.14256 conclusion: Moving forward, extending the applicability of FS-MSTD-LSTM to dynamically evolving industrial processes remains crucial.
- p.14256 conclusion: Future work should focus on enhancing the model’s adaptability to real-time data streams and its ability to autonomously adjust to changes in process dynamics.
