---
key: 5CIIJVTI
title: "Multiple space transfer learning based on maximizing mean variance differences for soft sensor modeling"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2025.130975"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Method` → `3` 对比实验（公开集 + 工业催化裂化）→ `4. Conclusion`。前置 `ABSTRACT` 与 `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段评机理/统计学习/深度学习软测量与 TCA/DAN 等域适应）。Introduction 末无编号贡献、无节序路标，直接进入 Method。Experiments 并入第 3 节（HAR/HHAR/WISDM + 两套催化裂化装置）。

## Openers

- abstract: `The scarcity of` — "The scarcity of labeled data significantly affects the effectiveness of industrial soft sensing."
- introduction: `In industrial processes` — "In industrial processes, real-time monitoring of key indicators is crucial for product quality closed-loop control and real-time optimization."
- method: `Domain adaptation aims` — "Domain adaptation aims to align the features of the source and target domains in the same feature space."
- experiments: `To further assess` — "To further assess the practicality of the MMVD-MSTL method, it is applied to process data from a catalytic cracking unit." (s.3.2)
- conclusion: `Due to the` — "Due to the common approach in domain adaptation methods of aligning source and target domain features into a single feature space, the adaptive performance of soft sensor modeling has been significantly impacted."

## Gap transitions

- however (abstract): "However, existing domain adaptation methods typically align source and target domain features into a single feature space, which may negatively impact the adaptation performance of soft sensor models."
- therefore (abstract): "Therefore, the multiple space transfer learning based on maximizing mean variance discrepancy (MMVD-MSTL) is proposed."
- however (introduction): "However, understanding the mechanisms of complex industrial process can be difficult, leading to inaccuracies in mechanism models and challenges in achieving accurate soft sensor modeling."
- however (introduction): "However, traditional domain adaptation methods based on a single space and single statistical feature cannot comprehensively and adequately express and align the feature distributions between the source and target domains"
- therefore (introduction): "Therefore, a novel soft sensor modeling method called Multiple Spatial Transfer Learning based on Maximizing Mean Variance Differences (MMVD-MSTL) is proposed."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "is proposed"; "this paper proposes a novel soft sensor modeling method"
- demonstrate / causal / abstract, experiments, conclusion: "Comparative experiments ... demonstrate"; "The extreme condition simulation experiments demonstrate"
- show / associative / abstract, experiments: "showing superior adaptation performance"; "Table 3 shows that MMVD-MSTL achieved the best performance"
- may / speculative / abstract, method: "which may negatively impact"; "Key domain information may be lost"
- plan / speculative / conclusion: "In the future, we plan to extend the model by incorporating multi-modal fusion techniques"

## Cross-section linkers

- introduction → method: 方法陈述后直接 `2. Method`
- method → experiments: Algorithm 1 / Fig. 2 后进入公开集与工业对比
- experiments → conclusion: 多空间有效性段落后 `4. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R009 自称：`this paper proposes` / 被动 `is proposed`
- R017 Introduction 末可无节序路标，直接 Method。
- R018 结论先收缺口再给方法名。

## Candidate phrases

- `Therefore, the ... is proposed` (abstract)
- `Therefore, a novel soft sensor modeling method ... is proposed` (introduction)
- `To further assess the practicality of the ... method` (experiments)
- `To address the issue of limited labeled data ... this paper proposes` (conclusion)
- `In the future, we plan to extend the model` (conclusion)

## House style

自称 `this paper proposes` / `we plan` / 被动 `is proposed`。未见 `Here we`。`this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 开篇。

## Quotes

- abstract: The scarcity of labeled data significantly affects the effectiveness of industrial soft sensing.
- abstract: However, existing domain adaptation methods typically align source and target domain features into a single feature space, which may negatively impact the adaptation performance of soft sensor models.
- abstract: Therefore, the multiple space transfer learning based on maximizing mean variance discrepancy (MMVD-MSTL) is proposed.
- introduction: In industrial processes, real-time monitoring of key indicators is crucial for product quality closed-loop control and real-time optimization.
- introduction: However, traditional domain adaptation methods based on a single space and single statistical feature cannot comprehensively and adequately express and align the feature distributions between the source and target domains, affecting the effectiveness of model transfer (Taghiyarrenani et al., 2023).
- introduction: Therefore, a novel soft sensor modeling method called Multiple Spatial Transfer Learning based on Maximizing Mean Variance Differences (MMVD-MSTL) is proposed.
- method: Domain adaptation aims to align the features of the source and target domains in the same feature space.
- experiments: To further assess the practicality of the MMVD-MSTL method, it is applied to process data from a catalytic cracking unit.
- experiments: Table 3 shows that MMVD-MSTL achieved the best performance across RMSE, MAE, and R2 metrics in both transfer directions.
- conclusion: To address the issue of limited labeled data in soft sensor modeling, this paper proposes a novel soft sensor modeling method called MMVD-MSTL.
- conclusion: Comparative experiments on public datasets and industrial datasets demonstrate the excellent performance of the MMVD-MSTL method in downstream tasks.
- conclusion: In the future, we plan to extend the model by incorporating multi-modal fusion techniques to leverage heterogeneous data sources and developing online adaptation mechanisms to ensure real-time robustness in dynamic environments.
