---
key: BLM4VHDK
title: "Addressing sensor degradation: raindrop-inspired fault-tolerant graph neural network for soft sensing in industrial processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2026.3703912"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. FRAMEWORK OF RIFTG` → `IV. EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 AE/RNN/Transformer 软测量与 GAEI；II.C `Related Works` 是预备节子节，不是顶层 `RELATED WORK`）。Introduction 末为项目符号贡献，无 `The rest of this article is organized` 路标。Method 标题为 `FRAMEWORK OF RIFTG`。Experiments 标题为 `EXPERIMENTAL STUDIES`（轧钢 + 发电）。

## Openers

- abstract: `Physical sensors usually` — "Physical sensors usually suffer from faults or degradation due to long-term use in the harsh industrial environment, which remains highly challenging for existing learning-based soft sensing models." (p.1)
- introduction: `DEEP learning-based soft` — "DEEP learning-based soft sensing modeling has showcased great superiority in both academic and industry communities during the past few years [1]." (p.1)
- method: `Let graph signal` — "Let graph signal xt ∈ Rm be process variables at any time step t, the graph of historical T time steps can be denoted as X(t−T+1):t = [xt−T+1, xt−T+2, . . ., xt] ∈ Rm×T, where m represents the number of process variables." (p.4, III.A)
- experiments: `We evaluate our` — "We evaluate our proposed RIFTG model on two real-world industrial datasets: steel rolling process and power generating process." (p.7, IV)
- conclusion: `In this article` — "In this article, we discover the limitations of information pollution for traditional deep learning-based soft sensing when sensor degradation occurs." (p.11)

## Gap transitions

- however (abstract): "However, previous studies still face two key challenges: first, how to construct the robust graph structure under sensor degradation, and second, how to eliminate the disturbance of error propagation during node aggregation." (p.1)
- nevertheless (introduction): "Nevertheless, some physical sensors usually suffer from wear and degradation because of long-term use or untimely maintenance under the industrial environment of high temperature and pressure [5]." (p.1)
- although (introduction): "Although GAEI adopts GNNs to capture the spatial coupling relationships, it still overlooks the robust graph structure when sensor degradation occurs." (p.2)
- to tackle (abstract): "To tackle these underexplored issues, we draw inspiration from the natural phenomenon of raindrops falling and propose a new graph-based fault-tolerant soft sensing framework called RIFTG" (p.1)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we ... propose a new graph-based fault-tolerant soft sensing framework called RIFTG"; "we propose an RIFTG framework"
- verify / causal / abstract: "Extensive experimental results on two public industrial datasets verify that RIFTG outperforms state-of-the-art fault-tolerant soft sensing models."
- show / causal / experiments, conclusion: "Experiments show superior accuracy over state-of-the-art fault-tolerant methods"
- achieve / causal / experiments: "our proposed RIFTG model achieves competitive performance on three different types of sensor degradation cases."

## Cross-section linkers

- introduction → preliminaries: 贡献列表后直接 `II. PRELIMINARIES` (p.3)
- related-works subsection → method: 与既有动态/鲁棒图方法对比后 `III. FRAMEWORK OF RIFTG` (p.4)
- method → experiments: Algorithm 1 与复杂度分析后 `IV. EXPERIMENTAL STUDIES` (p.7)
- experiments → conclusion: 退化传感器讨论后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `we ... propose` + 方法缩写 RIFTG，不用 `Here we`。
- R002 无顶层 Related Work；II.C `Related Works` 挂在 PRELIMINARIES 下。
- R003 贡献用项目符号（Fault-tolerant framework / Dynamic robust graph / Hierarchical message operator），不是 “as follows” 编号。
- R004 Experiments 标题为 `EXPERIMENTAL STUDIES`，双工业数据集。
- R005 Conclusion 用 `In this article, we discover` / `we propose`，再用 `In the future, we will incorporate` 指向后续。

## Candidate phrases

- `To tackle these underexplored issues, we draw inspiration from` (abstract)
- `The contributions of this work are summarized as follows.` (introduction)
- `We evaluate our proposed RIFTG model on two real-world industrial datasets` (experiments)
- `In this article, we discover the limitations of` (conclusion)
- `In the future, we will incorporate domain knowledge into` (conclusion)

## House style

自称是 `we propose` / `this work` / `In this article` / `our proposed RIFTG`。未见 `Here we`。`In this article` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`（正文贡献/结论；ablation 有 “this paper is effective” 的口语残留，不晋升）。

## Quotes

- p.1 abstract: Physical sensors usually suffer from faults or degradation due to long-term use in the harsh industrial environment, which remains highly challenging for existing learning-based soft sensing models.
- p.1 abstract: However, previous studies still face two key challenges: first, how to construct the robust graph structure under sensor degradation, and second, how to eliminate the disturbance of error propagation during node aggregation.
- p.1 abstract: To tackle these underexplored issues, we draw inspiration from the natural phenomenon of raindrops falling and propose a new graph-based fault-tolerant soft sensing framework called RIFTG, which can extract the comprehensive and discriminative features and alleviate the impact of sensor degradation.
- p.1 introduction: DEEP learning-based soft sensing modeling has showcased great superiority in both academic and industry communities during the past few years [1].
- p.1 introduction: Nevertheless, some physical sensors usually suffer from wear and degradation because of long-term use or untimely maintenance under the industrial environment of high temperature and pressure [5].
- p.2 introduction: Although GAEI adopts GNNs to capture the spatial coupling relationships, it still overlooks the robust graph structure when sensor degradation occurs.
- p.2 introduction: The contributions of this work are summarized as follows.
- p.4 method: Let graph signal xt ∈ Rm be process variables at any time step t, the graph of historical T time steps can be denoted as X(t−T+1):t = [xt−T+1, xt−T+2, . . ., xt] ∈ Rm×T, where m represents the number of process variables.
- p.7 experiments: We evaluate our proposed RIFTG model on two real-world industrial datasets: steel rolling process and power generating process.
- p.8 experiments: Fourth, our proposed RIFTG model achieves competitive performance on three different types of sensor degradation cases.
- p.11 conclusion: In this article, we discover the limitations of information pollution for traditional deep learning-based soft sensing when sensor degradation occurs.
- p.11 conclusion: Experiments show superior accuracy over state-of-the-art fault-tolerant methods, providing a foundation for decision-making and control in industrial application.
- p.12 conclusion: In the future, we will incorporate domain knowledge into the graph neural networks.
