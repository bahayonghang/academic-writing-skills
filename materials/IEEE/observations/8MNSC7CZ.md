---
key: 8MNSC7CZ
title: "Delayed Bottlenecking: Alleviating Forgetting in Pre-trained Graph Neural Networks"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2024.3516192"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,7-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. DELAYED BOTTLENECKING PRE-TRAINING: CAUSATION, STRATEGY, AND DERIVATION` → `IV. DBP FRAMEWORK` → `V. EXPERIMENTS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 末有贡献列表；未见 `The rest of this paper is organized` 句。Method 分理论（III）与框架（IV）。Experiments 为 V。

## Openers

- abstract: `Pre-training GNNs to` — "Pre-training GNNs to extract transferable knowledge and apply it to downstream tasks has become the de facto standard of graph representation learning." (p.1140)
- introduction: `IN RECENT years,` — "IN RECENT years, Graph Neural Networks (GNNs) have shown prominent performances in various fields including social networking [1], [2], [3], [4], [5], molecular computing [6], [7], [8], [9], [10], web recommendation [9], [11], [12], [13], [14], [15], [16], and bioinformatics [17], [18], [19]." (p.1140)
- related_work: `Recently, Pre-training GNNs` — "Recently, Pre-training GNNs have received significant attention since they can alleviate the heavy reliance of traditional GNNs on data with fine-grained labels." (p.1141, II)
- method: `Given the theoretical` — "Given the theoretical analysis in the previous section, we still have to consider how to integrate the proposed DBP strategy into the actual model design, so that the information control objectives can be applied to graph structure data." (p.1146, IV)
- experiments: `In this section,` — "In this section, we compare the performance of our proposed DBP and various state-of-the-art pre-trained baselines on both chemistry and biology domains." (p.1148, V)
- conclusion: `In this paper,` — "In this paper, we reexamine the pre-training process within the traditional pre-training and fine-tuning framework from the perspective of Information Bottleneck, and confirm that the forgetting phenomenon in the pre-training phase exactly has detrimental effects on downstream tasks." (p.1151)

## Gap transitions

- however (abstract): "However, they have to face an inevitable question: traditional pre-training strategies that aim at extracting useful information about pre-training tasks, may not extract all useful information about the downstream task." (p.1140)
- however (introduction): "However, considering the difference between the pre-training task and downstream tasks, we have to face an inevitable question: can the pre-training process transfer all useful information to the downstream task from large-scale unlabeled data?" (p.1140)
- nevertheless (introduction): "Nevertheless, considering the pre-training task which is artificially designed to extract universal transferable information from unlabeled data and is totally different from the downstream task in general [45], [46], such forgetting behavior is harmful to the learning and transformation of universal knowledge since those dropped information may be useful and of significance to downstream tasks." (p.1141)
- therefore (abstract): "Therefore, we propose a novel Delayed Bottlenecking Pre-training (DBP) framework which maintains as much as possible mutual information between latent representations and training data during pre-training phase by suppressing the compression operation and delays the compression operation to fine-tuning phase to make sure the compression can be guided with labeled fine-tuning data and downstream tasks." (p.1140)
- however (related_work): "However, all these methods paid all their attention to designing self-supervised tasks to maximally extract useful information with regard to the pre-training task from large-scale unlabeled data, ignoring the issue that the knowledge extracted by the pre-training task cannot be completely transferred to the downstream task due to the differences between pre-training and downstream tasks." (p.1141)
- however (related_work): "However, these methods primarily aim to reduce target differences during the fine-tuning stage, without analyzing the entire information transfer process across both stages." (p.1151)

## Hedge verbs

- reexamine / causal / abstract, conclusion: "we reexamine the pre-training process"
- confirm / causal / abstract: "confirm that the forgetting phenomenon in pre-training phase may cause detrimental effects"
- propose / causal / abstract, introduction: "we propose a novel Delayed Bottlenecking Pre-training (DBP) framework"
- demonstrate / causal / abstract, introduction: "Extensive experiments on both chemistry and biology domains demonstrate the effectiveness of DBP"
- may / speculative / abstract: "may not extract all useful information about the downstream task"; "may cause detrimental effects"

## Cross-section linkers

- introduction → related_work: 贡献列表后直接 `II. RELATED WORK` (p.1141)
- theory → framework: "Given the theoretical analysis in the previous section, we still have to consider how to integrate the proposed DBP strategy into the actual model design" 随后 `IV. DBP FRAMEWORK` (p.1146)
- method → experiments: fine-tuning 目标式后直接 `V. EXPERIMENTS` (p.1148)
- experiments → conclusion: complexity analysis 后直接 `VI. CONCLUSION` (p.1151)

## Candidate rules

- R001 Abstract 用 `In this paper, we reexamine` + `Therefore, we propose a novel ... framework`。
- R002 Introduction 用 `Challenges:` 小标题，再给 `To address these challenges`。
- R003 贡献用 `The main contributions are summarized as follows` + 项目符号。
- R004 Related Work 分 Pre-training GNNs / Mutual Information / IB Theory 三块。
- R005 Experiments 节首用 `In this section, we compare the performance of our proposed DBP and various state-of-the-art`。

## Candidate phrases

- `In this paper, we reexamine the pre-training process within` (abstract)
- `Therefore, we propose a novel Delayed Bottlenecking Pre-training (DBP) framework which` (abstract)
- `The main contributions are summarized as follows:` (introduction)
- `To our knowledge, this is the first paper that aims at` (introduction)
- `In this section, we compare the performance of our proposed` (experiments)

## House style

自称是 `In this paper` / `we propose` / `our proposed DBP` / `we reexamine`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。未见 `this article`。

## Quotes

- p.1140 abstract: Pre-training GNNs to extract transferable knowledge and apply it to downstream tasks has become the de facto standard of graph representation learning.
- p.1140 abstract: However, they have to face an inevitable question: traditional pre-training strategies that aim at extracting useful information about pre-training tasks, may not extract all useful information about the downstream task.
- p.1140 abstract: In this paper, we reexamine the pre-training process within traditional pre-training and fine-tuning frameworks from the perspective of Information Bottleneck (IB) and confirm that the forgetting phenomenon in pre-training phase may cause detrimental effects on downstream tasks.
- p.1140 abstract: Therefore, we propose a novel Delayed Bottlenecking Pre-training (DBP) framework which maintains as much as possible mutual information between latent representations and training data during pre-training phase by suppressing the compression operation and delays the compression operation to fine-tuning phase to make sure the compression can be guided with labeled fine-tuning data and downstream tasks.
- p.1140 abstract: Extensive experiments on both chemistry and biology domains demonstrate the effectiveness of DBP.
- p.1140 introduction: IN RECENT years, Graph Neural Networks (GNNs) have shown prominent performances in various fields including social networking [1], [2], [3], [4], [5], molecular computing [6], [7], [8], [9], [10], web recommendation [9], [11], [12], [13], [14], [15], [16], and bioinformatics [17], [18], [19].
- p.1140 introduction: However, considering the difference between the pre-training task and downstream tasks, we have to face an inevitable question: can the pre-training process transfer all useful information to the downstream task from large-scale unlabeled data?
- p.1141 introduction: To address these challenges, as demonstrated in Fig. 1(b), we propose a novel Delayed Bottlenecking Pre-training (DBP) framework to address the issue of information forgetting during pre-training.
- p.1141 introduction: The main contributions are summarized as follows:
- p.1141 introduction: To our knowledge, this is the first paper that aims at alleviating the influence of such kind of inevitable information forgetting on downstream tasks.
- p.1141 related_work: Recently, Pre-training GNNs have received significant attention since they can alleviate the heavy reliance of traditional GNNs on data with fine-grained labels.
- p.1141 related_work: However, all these methods paid all their attention to designing self-supervised tasks to maximally extract useful information with regard to the pre-training task from large-scale unlabeled data, ignoring the issue that the knowledge extracted by the pre-training task cannot be completely transferred to the downstream task due to the differences between pre-training and downstream tasks.
- p.1146 method: Given the theoretical analysis in the previous section, we still have to consider how to integrate the proposed DBP strategy into the actual model design, so that the information control objectives can be applied to graph structure data.
- p.1148 experiments: In this section, we compare the performance of our proposed DBP and various state-of-the-art pre-trained baselines on both chemistry and biology domains.
- p.1148 experiments: DBP achieves the highest average ROC-AUC score and gain among all self-supervised learning strategies and performs best on six of eight tasks.
- p.1149 experiments: It can be observed that the proposed DBP consistently yields the best performance among all methods across architectures.
- p.1151 conclusion: In this paper, we reexamine the pre-training process within the traditional pre-training and fine-tuning framework from the perspective of Information Bottleneck, and confirm that the forgetting phenomenon in the pre-training phase exactly has detrimental effects on downstream tasks.
- p.1151 conclusion: Then, we propose a DBP framework that maintains as much as possible mutual information during the pre-training phase by suppressing the compression operation and delays the compression operation to fine-tuning phase.
