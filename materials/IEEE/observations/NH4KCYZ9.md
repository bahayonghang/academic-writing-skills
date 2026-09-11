---
key: NH4KCYZ9
title: "Deep Spatial–Temporal Slow Feature Transfer Network for Multimode Chemical Process Soft Sensing on Imbalanced Data"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3495779"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED TL-STSFE FOR SOFT SENSOR MODELING` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 ELM/DA、LSTM+BDA、SFA、Siamese 慢特征）。`II. PRELIMINARIES` 为 Siamese 与深度 TL。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `CASE STUDY`（BSM1 + 甲烷化炉）。

## Openers

- abstract: `For soft sensor` — "For soft sensor modeling of multimode chemical processes, a common method is to build an individual model corresponding to each mode." (p.1)
- introduction: `SOFT sensors employ` — "SOFT sensors employ easy-to-measure variables for key variable prediction by constructing the regression model [1]." (p.1；栏首掉字)
- method: `In this section,` — "In this section, the STA-based mechanism is embedded into the Siamese network to better capture the relationships between process variables as well as the temporal dependencies across different time steps to enhance the feature representation." (p.3, III.A)
- experiments: `The BSM1 is` — "The BSM1 is a simulation model to replicate actual wastewater treatment processes." (p.5, IV.A)
- conclusion: `In this article,` — "In this article, considering the data imbalance coupled with variable relevance in the multimode chemical process slow feature extraction, a novel TF-STSFE method is proposed." (p.9)

## Gap transitions

- however (abstract): "However, certain individual mode models may not be reliable due to the imbalanced data across different modes." (p.1)
- to address (abstract): "To address this issue, a deep transfer learning method is introduced for soft sensor and a deep transfer spatial–temporal slow feature regression framework (STSFE) is proposed." (p.1)
- however (abstract): "However, the Siamese network fails to consider correlation of variables in quality prediction." (p.1)
- however (introduction): "However, most of these models assume that the training and testing data are in the same distribution." (p.1)
- although (conclusion): "Although TL-STSFE has achieved superior performance, it depends on the quality of source domain data." (p.9)

## Hedge verbs

- introduce / causal / abstract: "a deep transfer learning method is introduced for soft sensor"
- propose / causal / abstract, introduction, conclusion: "a deep transfer spatial–temporal slow feature regression framework (STSFE) is proposed"; "a deep transfer learning-based spatial–temporal attention slow feature (TL-STSFE) regression model is proposed"
- validate / causal / abstract: "The effectiveness of the proposed method is validated through a benchmark sewage treatment case and a real chemical process."
- demonstrate / causal / experiments: "The results show that the proposed method performs well in both two target domains with all ratios, which demonstrate the robustness and effectiveness of the proposed method."

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II presents the Siamese network and fine-tuning strategy in soft sensing. In Section III, the TL-STSFE for soft sensor modeling is introduced. Section IV shows the effectiveness of TL-STSFE using a benchmark sewage treatment case and a real world methanation furnace case. Finally, Section V concludes this article." (p.2)
- method → experiments: 微调叙述后直接 `IV. CASE STUDY` (p.5)
- experiments → conclusion: Wilcoxon 检验后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `To address this issue` + 被动 `is proposed`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；预备节给 Siamese/TL。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions of this article are as follows.` + 编号列表。
- R005 Conclusion 先被动收回方法，再用 `Although` 承认局限，`In future work` 指向后续。

## Candidate phrases

- `To address this issue, a deep transfer learning method is introduced` (abstract)
- `The contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `The effectiveness of the proposed method is validated through` (abstract)
- `In this article, considering ... a novel TF-STSFE method is proposed.` (conclusion)

## House style

自称是 `this article` / `the proposed method` / `we employ`。未见 `Here we`。未见 `In this paper`。`The contributions of this article` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: For soft sensor modeling of multimode chemical processes, a common method is to build an individual model corresponding to each mode.
- p.1 abstract: However, certain individual mode models may not be reliable due to the imbalanced data across different modes.
- p.1 abstract: To address this issue, a deep transfer learning method is introduced for soft sensor and a deep transfer spatial–temporal slow feature regression framework (STSFE) is proposed.
- p.1 abstract: However, the Siamese network fails to consider correlation of variables in quality prediction.
- p.1 abstract: The effectiveness of the proposed method is validated through a benchmark sewage treatment case and a real chemical process.
- p.1 introduction: SOFT sensors employ easy-to-measure variables for key variable prediction by constructing the regression model [1].
- p.1 introduction: However, most of these models assume that the training and testing data are in the same distribution.
- p.2 introduction: The contributions of this article are as follows.
- p.2 introduction: The rest of this article is organized as follows. Section II presents the Siamese network and fine-tuning strategy in soft sensing. In Section III, the TL-STSFE for soft sensor modeling is introduced. Section IV shows the effectiveness of TL-STSFE using a benchmark sewage treatment case and a real world methanation furnace case. Finally, Section V concludes this article.
- p.3 method: In this section, the STA-based mechanism is embedded into the Siamese network to better capture the relationships between process variables as well as the temporal dependencies across different time steps to enhance the feature representation.
- p.5 experiments: The BSM1 is a simulation model to replicate actual wastewater treatment processes.
- p.6 experiments: The results show that the proposed method performs well in both two target domains with all ratios, which demonstrate the robustness and effectiveness of the proposed method.
- p.9 conclusion: In this article, considering the data imbalance coupled with variable relevance in the multimode chemical process slow feature extraction, a novel TF-STSFE method is proposed.
- p.9 conclusion: Although TL-STSFE has achieved superior performance, it depends on the quality of source domain data.
- p.9 conclusion: In future work, the advanced TL techniques can be investigated.
