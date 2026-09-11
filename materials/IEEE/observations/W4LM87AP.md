---
key: W4LM87AP
title: "Generalized Cross-Domain Industrial Process Monitoring via Adaptive Discriminative Transfer Dictionary Pair Learning With Attribute Embedding"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2025.3563618"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. COMPONENTS OF ADTDPL FRAMEWORK` → `IV.`（ADTDPL-based monitoring）→ `V. EXPERIMENTS AND ANALYSES` → `VI. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCLATURE`。有独立 Related Work（`II. RELATED WORKS`：typical DL / attribute embedding-based DL）。`related_work=independent`。Introduction 中段已评迁移学习与 DPL。Introduction 末有节序路标，指向 Section II–VI。Experiments 标题为 `EXPERIMENTS AND ANALYSES`（TEP + AEP；Scenario I/II）。

## Openers

- abstract: `Real industrial process` — "Real industrial process data from various domains often exhibit divergent distributions, may occupy distinct feature spaces, and are occasionally unlabeled, which limits the effectiveness of conventional process monitoring methods." (p.1)
- introduction: `EFFICIENT industrial process` — "EFFICIENT industrial process monitoring technologies, featuring automatic mode recognition and anomaly detection, are essential for evaluating working conditions and guiding controls, thereby supporting the high-quality and low-carbon operation of industrial processes [1]." (p.1；栏首掉字)
- related_work: `With the sparse` — "With the sparse representation theory now rigorously validated, DL has made significant strides in efficiently extracting information by capturing the essential structures of data through sparse coding, attracting substantial research attention and broad application in various fields [36], [37]." (p.3, II.A)
- method: `In cross-domain process` — "In cross-domain process monitoring, domains refer to sets of process data along with their associated information [12]." (p.4, III)
- experiments: `In this section` — "In this section, the experimental settings are first clearly outlined, followed by a detailed introduction to the generalized cross-domain industrial process monitoring experiments." (p.9, V)
- conclusion: `In this study` — "In this study, we propose the ADTDPL method for generalized cross-domain industrial process monitoring." (p.13)

## Gap transitions

- to address (abstract): "To address these challenges, we propose an adaptive discriminative transfer dictionary pair learning (ADTDPL) method with attribute embedding for generalized cross-domain industrial process monitoring." (p.1)
- however (introduction): "However, prevailing data-driven methods tend to disregard several tangible challenges:" (p.1)
- however (introduction): "However, the DL-based cross-domain learning methods mentioned above rely on a certain number of labeled target domain samples for training and neglect the situation of inconsistent feature space between the source and target domains." (p.2)
- therefore (introduction): "Therefore, transfer DPL is required to be further studied for unsupervised and heterogeneous cross-domain scenarios." (p.2)
- to cope (introduction): "To cope with the challenges of distributional inconsistencies, labeling difficulties, and feature space differences across real multimode industrial process data, an adaptive discriminative transfer dictionary pair learning (ADTDPL) method with attribute embedding is proposed in this article for generalized cross-domain process monitoring." (p.2)
- in the future (conclusion): "In the future, we will further consider scenarios where new classes appear in the target domain, thereby exploring transfer learning methods oriented toward open-set cross-domain challenges." (p.14)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose an adaptive discriminative transfer dictionary pair learning (ADTDPL) method"; "an adaptive discriminative transfer dictionary pair learning (ADTDPL) method with attribute embedding is proposed in this article"; "we propose the ADTDPL method"
- verify / causal / abstract: "The superior performance of our method for cross-domain process monitoring is verified on the Tennessee Eastman platform and in practical aluminum electrolysis processes (AEPs)."
- demonstrate / causal / introduction, conclusion: "Extensive comparative experiments ... demonstrate the effectiveness and superiority of the proposed ADTDPL."; "Extensive comparative experimental results demonstrate that our proposed method consistently exhibits the superior performance"
- indicate / causal / experiments: "the results presented in Tables III, V, and VIII along with Figs. 5 and 7 indicate:"
- explore / speculative / conclusion: "exploring transfer learning methods oriented toward open-set cross-domain challenges"

## Cross-section linkers

- introduction → related work: "The remainder of this article is organized as follows. Section II provides a brief review of related work. In Section III, we elaborate on the components of our ADTDPL framework. The proposed ADTDPL-based generalized cross-domain process monitoring method is detailed in Section IV. Section V presents the experimental settings and the analysis of results. Finally, Section VI offers our conclusion for this article and suggests the potential direction for future research." (p.3)
- related work → method: 属性嵌入综述后 `III. COMPONENTS OF ADTDPL FRAMEWORK` (p.4)
- method → experiments: 在线监控统计量后 `V. EXPERIMENTS AND ANALYSES` (p.9)
- experiments → conclusion: 性能讨论后 `VI. CONCLUSION` (p.13)

## Candidate rules

- R001 abstract 用 `To address these challenges, we propose` + 方法缩写，不用 `Here we`。
- R002 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R003 贡献用 `The main innovations and contributions of this work are summarized as follows` + 编号列表。
- R004 Experiments 标题为 `EXPERIMENTS AND ANALYSES`。
- R005 Conclusion 用 `In this study, we propose`，再用 `In the future, we will further consider` 指向开放集。

## Candidate phrases

- `To address these challenges, we propose` (abstract)
- `The main innovations and contributions of this work are summarized as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this section, the experimental settings are first clearly outlined` (experiments)
- `In this study, we propose the ADTDPL method for` (conclusion)

## House style

自称是 `we propose` / `this article` / `In this study, we propose` / `our proposed method` / `our approach`。未见 `Here we`。`In this study, we propose` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Real industrial process data from various domains often exhibit divergent distributions, may occupy distinct feature spaces, and are occasionally unlabeled, which limits the effectiveness of conventional process monitoring methods.
- p.1 abstract: To address these challenges, we propose an adaptive discriminative transfer dictionary pair learning (ADTDPL) method with attribute embedding for generalized cross-domain industrial process monitoring.
- p.1 abstract: The superior performance of our method for cross-domain process monitoring is verified on the Tennessee Eastman platform and in practical aluminum electrolysis processes (AEPs).
- p.1 introduction: EFFICIENT industrial process monitoring technologies, featuring automatic mode recognition and anomaly detection, are essential for evaluating working conditions and guiding controls, thereby supporting the high-quality and low-carbon operation of industrial processes [1].
- p.1 introduction: However, prevailing data-driven methods tend to disregard several tangible challenges:
- p.2 introduction: However, the DL-based cross-domain learning methods mentioned above rely on a certain number of labeled target domain samples for training and neglect the situation of inconsistent feature space between the source and target domains.
- p.2 introduction: Therefore, transfer DPL is required to be further studied for unsupervised and heterogeneous cross-domain scenarios.
- p.2 introduction: To cope with the challenges of distributional inconsistencies, labeling difficulties, and feature space differences across real multimode industrial process data, an adaptive discriminative transfer dictionary pair learning (ADTDPL) method with attribute embedding is proposed in this article for generalized cross-domain process monitoring.
- p.3 introduction: The main innovations and contributions of this work are summarized as follows.
- p.3 introduction: The remainder of this article is organized as follows. Section II provides a brief review of related work. In Section III, we elaborate on the components of our ADTDPL framework. The proposed ADTDPL-based generalized cross-domain process monitoring method is detailed in Section IV. Section V presents the experimental settings and the analysis of results. Finally, Section VI offers our conclusion for this article and suggests the potential direction for future research.
- p.4 method: In cross-domain process monitoring, domains refer to sets of process data along with their associated information [12].
- p.9 experiments: In this section, the experimental settings are first clearly outlined, followed by a detailed introduction to the generalized cross-domain industrial process monitoring experiments.
- p.9 experiments: To substantiate the efficacy and practicality of the proposed ADTDPL method, extensive experiments are conducted on the Tennessee Eastman benchmark test platform and within an actual aluminum electrolysis industrial process.
- p.13 experiments: Overall, KSVD exhibits the poorest process monitoring performance, while our ADTDPL performs the best.
- p.13 conclusion: In this study, we propose the ADTDPL method for generalized cross-domain industrial process monitoring.
- p.14 conclusion: Extensive comparative experimental results demonstrate that our proposed method consistently exhibits the superior performance of mode identification and anomaly detection in both semi-supervised homogeneous and unsupervised heterogeneous scenarios.
- p.14 conclusion: In the future, we will further consider scenarios where new classes appear in the target domain, thereby exploring transfer learning methods oriented toward open-set cross-domain challenges.
