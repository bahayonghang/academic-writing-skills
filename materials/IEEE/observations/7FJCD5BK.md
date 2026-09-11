---
key: 7FJCD5BK
title: "A Scalo Gram-Based CNN Ensemble Method With Density-Aware SMOTE Oversampling for Improving Bearing Fault Diagnosis"
venue: "IEEE Access"
doi: "10.1109/ACCESS.2023.3332243"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,10-17"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. LITERATURE REVIEW` → `III. METHODOLOGY` → `IV. RESULTS AND DISCUSSIONS` → `V. CONCLUSION AND FUTURE WORK`。前置 `ABSTRACT` 与 `INDEX TERMS`。有独立 Related Work（`II. LITERATURE REVIEW`）。Introduction 中段仍评 CNN / transfer learning / 类别不平衡，末有编号贡献 + 节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `RESULTS AND DISCUSSIONS`（CWRU 48 kHz，不平衡与 DA-SMOTE 过采样对照）。

## Openers

- abstract: `Machine learning (ML)` — "Machine learning (ML) based bearing fault detection is an emerging application of Artificial Intelligence (AI) that has proven its utility in effectively classifying various faults for timely measures." (p.1)
- introduction: `In order to` — "In order to ensure reliable performance of mechanical systems, condition monitoring of bearings is paramount." (p.1)
- related_work: `The literature study` — "The literature study pertaining to bearings reveal a scintillating insight into the re-search and development focused on fault detection and diagnosis." (p.3, II)
- method: `An open-source and` — "An open-source and widely used benchmark dataset for the bearing fault diagnosis CWRU (Case Western Reserve University) [27] is used herein for the purpose of evaluating the proposed method against bearing fault diagnosis." (p.4, III.A)
- experiments: `The respective section` — "The respective section provides description in regards to the evaluation of the proposed ensemble technique along with a comparison with some other state-of-the-art methods." (p.10, IV)
- conclusion: `The present study` — "The present study delves into the endeavor of precisely classifying bearing faults for an effective condition monitoring." (p.15)

## Gap transitions

- however (abstract): "However, 1-d signals lack contextual information and higher-dimensional interpretations whereas time-frequency based transformations provide a more appropriate, visually perceivable and explainable representation of the time and frequency changes." (p.1)
- therefore (abstract): "Therefore in this study, a scalogram based representation of the signals is leveraged for classification using the CNN." (p.1)
- however (introduction): "However, the bearing faults classification comes with some challenges, the primary one being the class-imbalance which arises due to varying distribution of faults in real-world systems." (p.2)
- hence (introduction): "Hence an effectively addressed class imbalance remains pivotal for achieving accurate fault classification results." (p.2)
- while (limitations): "While our study proposed innovative take on bearing fault classification under imbalanced settings, there are some limitations that can further be worked upon." (p.15)

## Hedge verbs

- propose / causal / abstract, introduction: "In this study, we proposed a weighted voting ensemble (WVE)"; "Three custom built CNN architectures were proposed"
- provide / causal / abstract: "This study provides a novel density and distance hybrid over-sampling approach"
- contribute / causal / introduction: "This study contributes by leveraging three distinct convolutional neural networks"
- show / causal / conclusion: "The acquired efficiency of our model shows considerable promise"
- can / speculative / limitations: "This can be improved in the future by working on more lightweight models"

## Cross-section linkers

- introduction → related work: "The remaining part of the paper is organized as follows: Section II, the Literature Review is given. In Section III, the methodologies used are described. The Results and Discussions are given in Section IV respectively. While the Section V concludes the paper." (p.2)
- related work → method: Table 1 汇总后直接 `III. METHODOLOGY` (p.4)
- method → experiments: 指标定义后 `IV. RESULTS AND DISCUSSIONS` (p.10)
- experiments → conclusion: `C. LIMITATIONS AND CHALLENGES` 后 `V. CONCLUSION AND FUTURE WORK` (p.15)

## Candidate rules

- R001 abstract 自称 `In this study, we proposed`；过采样贡献用 `This study provides a novel`。
- R002 有独立 `II. LITERATURE REVIEW`。
- R003 贡献用 `This study contributes as follows` + 编号列表。
- R004 Introduction 末用 `The remaining part of the paper is organized as follows` 指向 II–V。
- R005 Conclusion 标题为 `CONCLUSION AND FUTURE WORK`，开篇 `The present study`，末用 `Future investigations will include`。

## Candidate phrases

- `In this study, we proposed` (abstract)
- `This study provides a novel` (abstract)
- `This study contributes as follows:` (introduction)
- `The remaining part of the paper is organized as follows:` (introduction)
- `The present study delves into` (conclusion)

## House style

自称是 `In this study` / `This study` / `we proposed` / `our proposed` / `The present study`。未见 `Here we`。`The remaining part of the paper` 中的 `paper` 仅用于组织路标。`In this study, we proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Machine learning (ML) based bearing fault detection is an emerging application of Artificial Intelligence (AI) that has proven its utility in effectively classifying various faults for timely measures.
- p.1 abstract: In this study, we proposed a weighted voting ensemble (WVE) of three low-computation custom-designed convolutional neural networks (CNNs) to classify bearing faults at 48 KHz.
- p.1 abstract: However, 1-d signals lack contextual information and higher-dimensional interpretations whereas time-frequency based transformations provide a more appropriate, visually perceivable and explainable representation of the time and frequency changes.
- p.1 abstract: Therefore in this study, a scalogram based representation of the signals is leveraged for classification using the CNN.
- p.1 abstract: This study provides a novel density and distance hybrid over-sampling approach namely Density-Aware SMOTE(DA-SMOTE) built upon the SMOTE methodology for a more refined representation of synthetic samples within the minority class distribution.
- p.1 introduction: In order to ensure reliable performance of mechanical systems, condition monitoring of bearings is paramount.
- p.2 introduction: However, the bearing faults classification comes with some challenges, the primary one being the class-imbalance which arises due to varying distribution of faults in real-world systems.
- p.2 introduction: This study contributes as follows:
- p.2 introduction: The remaining part of the paper is organized as follows: Section II, the Literature Review is given. In Section III, the methodologies used are described. The Results and Discussions are given in Section IV respectively. While the Section V concludes the paper.
- p.3 related_work: The literature study pertaining to bearings reveal a scintillating insight into the re-search and development focused on fault detection and diagnosis.
- p.4 method: An open-source and widely used benchmark dataset for the bearing fault diagnosis CWRU (Case Western Reserve University) [27] is used herein for the purpose of evaluating the proposed method against bearing fault diagnosis.
- p.10 experiments: The respective section provides description in regards to the evaluation of the proposed ensemble technique along with a comparison with some other state-of-the-art methods.
- p.15 limitations: While our study proposed innovative take on bearing fault classification under imbalanced settings, there are some limitations that can further be worked upon.
- p.15 conclusion: The present study delves into the endeavor of precisely classifying bearing faults for an effective condition monitoring.
- p.15 conclusion: In summation, our weighted voting ensemble models outshine established transfer learning techniques and models featured in analogous studies concerning the same dataset.
- p.15 conclusion: Future investigations will include further refining of the proposed methodologies and testing them on other datasets with requisite modifications within the oversampling methodology and the data-refining procedures.
