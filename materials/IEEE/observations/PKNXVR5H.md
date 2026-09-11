---
key: PKNXVR5H
title: "A Difference Metric Attention With Position Distance-Based Weighting for Transformer in Data Sequence Modeling of Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3488777"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. ATTENTION MECHANISM AND THE TRANSFORMER ARCHITECTURE` → `III. DIFFERENCE METRIC ATTENTION WITH POSITION DISTANCE-BASED WEIGHTING FOR TRANSFORMER` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 FPM/DDM、深度学习软测量、transformer/Informer、点积注意力改进）。`II` 为注意力与 transformer 预备。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `CASE STUDIES`（加氢裂化 C5 与喷气燃料终馏点）。

## Openers

- abstract: `Accurate feature extraction` — "Accurate feature extraction and quality variable prediction are critical problems for time sequences in industrial processes." (p.1)
- introduction: `UNDER the background` — "UNDER the background of energy saving and safe production, industrial processes have been put with stricter demands on monitoring and controlling process performance in real time." (p.1；栏首掉字)
- method: `Similarity reflects the` — "Similarity reflects the relevance between any two records to some extent." (p.4, III)
- experiments: `In this section,` — "In this section, the proposed DMA-trans is applied for soft sensor in an industrial hydrocracking process and extensive experiments are conducted to demonstrate the effectiveness of the DMA-trans." (p.5, IV)
- conclusion: `In this article,` — "In this article, DMA-trans was proposed to fully measure similarities between vectors and capture the distance relevance of samples for transformer." (p.9)

## Gap transitions

- however (abstract): "However, industrial samples often exhibit strong temporal correlations with each other that have different positional distances, making it challenging for conventional data-driven models like long short-term memory (LSTM) and Vanilla transformer to capture these underlying features." (p.1)
- however (introduction): "However, most of these key variables cannot be measured in real time due to the limitations of measurement techniques, time delays, harsh environments, etc." (p.1)
- however (introduction): "However, the data collected from industrial plants are often with high dimensionality and tend to have nonlinear correlations [10], [11], [12], [13]." (p.1)
- to alleviate (introduction): "To alleviate these problems, a novel transformer model is established using a difference metric attention (DMA) with position distance-based weighting (PDW), which is named DMA-trans." (p.2)
- therefore (method): "Therefore, the difference metric attention with position distance-based weighting for transformer (DMA-trans) is proposed to extract these potential features." (p.4)
- hence (conclusion): "Hence, future work may be focus on how to deal with the irregular sampling problems in transformer." (p.9)

## Hedge verbs

- propose / causal / abstract, method: "a difference metric attention with position distance-based weighting is proposed for transformer (DMA-trans)"; "the difference metric attention ... is proposed to extract these potential features"
- may / speculative / abstract: "This may help to extract more potential features because the closer samples tend to have higher relevance"
- demonstrate / causal / experiments: "extensive experiments are conducted to demonstrate the effectiveness of the DMA-trans."
- show / causal / experiments: "Table II gives the prediction results"; "It can be seen that the red curve cannot track well"
- validate / causal / abstract: "The effectiveness of the DMA-trans model is validated in industrial hydrocracking processes"

## Cross-section linkers

- introduction → background: "The rest of this article is organized as follows. In Section II, attention mechanism and transformer are briefly introduced. Then, the DMA-trans is presented in detail in Section III. After that, the proposed model is validated on an industrial hydrocracking process for data sequence modeling in Section IV. Finally, Section V concludes this article." (p.2)
- method → experiments: 建模流程图后直接 `IV. CASE STUDIES` (p.5)
- experiments → conclusion: 注意力热图分析后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `In this article, a ... is proposed for`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；`II` 给注意力/transformer 预备。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this article are as follows.` + 编号列表。
- R005 Conclusion 用过去时 `was proposed`，再用 `Hence, future work may be` 指向后续。

## Candidate phrases

- `In this article, a difference metric attention ... is proposed for transformer (DMA-trans)` (abstract)
- `To alleviate these problems, a novel transformer model is established` (introduction)
- `The main contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, DMA-trans was proposed to fully measure similarities` (conclusion)

## House style

自称是 `In this article` / `the proposed DMA-trans` / `we use`。未见 `Here we`。未见 `In this paper`。`In this article, a ... is proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Accurate feature extraction and quality variable prediction are critical problems for time sequences in industrial processes.
- p.1 abstract: However, industrial samples often exhibit strong temporal correlations with each other that have different positional distances, making it challenging for conventional data-driven models like long short-term memory (LSTM) and Vanilla transformer to capture these underlying features.
- p.1 abstract: In this article, a difference metric attention with position distance-based weighting is proposed for transformer (DMA-trans) in industrial time series modeling.
- p.1 abstract: This may help to extract more potential features because the closer samples tend to have higher relevance while there may be weak correlations if two samples are far in positional distance.
- p.1 abstract: The effectiveness of the DMA-trans model is validated in industrial hydrocracking processes for C5 content of the light naphtha and the final boiling point of the jet fuel.
- p.1 introduction: UNDER the background of energy saving and safe production, industrial processes have been put with stricter demands on monitoring and controlling process performance in real time.
- p.2 introduction: To alleviate these problems, a novel transformer model is established using a difference metric attention (DMA) with position distance-based weighting (PDW), which is named DMA-trans.
- p.2 introduction: The main contributions of this article are as follows.
- p.2 introduction: The rest of this article is organized as follows. In Section II, attention mechanism and transformer are briefly introduced. Then, the DMA-trans is presented in detail in Section III. After that, the proposed model is validated on an industrial hydrocracking process for data sequence modeling in Section IV. Finally, Section V concludes this article.
- p.4 method: Similarity reflects the relevance between any two records to some extent.
- p.4 method: Therefore, the difference metric attention with position distance-based weighting for transformer (DMA-trans) is proposed to extract these potential features.
- p.5 experiments: In this section, the proposed DMA-trans is applied for soft sensor in an industrial hydrocracking process and extensive experiments are conducted to demonstrate the effectiveness of the DMA-trans.
- p.6 experiments: In comparison, the DMA-trans performs the best among these methods, which achieves the highest R2 and the lowest MAE, MSE as well as RMSE.
- p.9 conclusion: In this article, DMA-trans was proposed to fully measure similarities between vectors and capture the distance relevance of samples for transformer.
- p.9 conclusion: Hence, future work may be focus on how to deal with the irregular sampling problems in transformer.
