---
key: CPRU4S9K
title: "Dynamic historical information incorporated attention deep learning model for industrial soft sensor modeling"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2022.101590"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Background` → `3. Attention-based dynamic stacked autoencoder` → `4. Case study` → `5. Concluding remarks`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 PCR/PLSR/SVM、PCA/PLS、SAE/CNN/RNN、Shang/Ge/Yuan 不规则采样）。Introduction 无编号贡献列表，有节序路标。Method 含 input / attention / output module。Experiments 标题为 `4. Case study`（加氢裂化 C5 / C6）。

## Openers

- abstract: `Due to the` — "Due to the limitations of sampling conditions and sampling techniques in many real industrial processes, the process data under different sampling conditions subject to different sampling frequencies, which leads to irregular interval sampling characteristics of the entire process data."
- introduction: `Modern industry has` — "Modern industry has obvious characteristics of multiple processes, complexity, and continuity."
- method: `Traditional SAE method` — "Traditional SAE method can eliminate the influence of redundant information on feature extraction through layer-by-layer pre-training to extract features from the original data."
- experiments: `In this section` — "In this section, the proposed AD-SAE based on soft sensor model is applied to an actual industrial hydrocracking process to verify the validity of the proposed method."
- conclusion: `In this paper` — "In this paper, a new AD-SAE network is proposed to extract dynamic historical information characteristics of process data with irregular sampling frequencies."

## Gap transitions

- however (abstract): "However, the existing soft sensor modeling methods based on deep learning do not consider introducing dynamic historical information into the feature extraction process."
- to combat (abstract): "To combat this issue, a novel attention-based dynamic stacked autoencoder networks (AD-SAE) for soft sensor modeling is proposed in this paper."
- although (introduction): "Although deep learning in industrial processes is not growing as fast as mainstream areas such as image recognition, there emerges plenty of valuable research emerging."
- however (introduction): "However, this method can only capture the influence of neighboring samples, which is difficult to extract long-range historical features of whole samples."
- to address (introduction): "To address above problems, a novel attention-based dynamic stacked auto-encoder (AD-SAE) model is proposed to extract the abundant feature representation of irregular sampling process data in this paper."

## Hedge verbs

- is proposed / causal / abstract, introduction, conclusion: "is proposed in this paper"; "a novel attention-based dynamic stacked auto-encoder (AD-SAE) model is proposed"
- show / associative / abstract: "The experimental results on the actual hydrocracking process data set show that the proposed method has better performance than traditional methods."
- demonstrate / associative / conclusion: "The experimental results demonstrate that the proposed method has better predictive performance compared with traditional methods."
- believe / speculative / method: "We believe that only considering the impact of historical samples in a short period of time before the current sample can improve model training efficiency"

## Cross-section linkers

- introduction → background: "The remaining parts of this paper are organized as follows. Section 2 simply revisits the structure of SAE."
- background → method: "Then, the proposed AD-SAE method is described in detail as well as the procedure of AD-SAE-based soft sensor modeling in Section 3."
- method → experiments: "Following this, the effectiveness of the proposed method is verified in the hydrocracking process in Section 4."
- experiments → conclusion: "Finally, Section 5 summarizes the main contribution of this paper and gives a perspective for future research."

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remaining parts of this paper are organized as follows`
- R009 自称：`is proposed in this paper` / `In this paper, a new AD-SAE network is proposed` / `this paper introduces`

## Candidate phrases

- `To combat this issue, a novel ... is proposed in this paper` (abstract)
- `To address above problems, a novel ... model is proposed` (introduction)
- `The remaining parts of this paper are organized as follows` (introduction)
- `In this section, the proposed AD-SAE based on soft sensor model is applied` (experiments)
- `In this paper, a new AD-SAE network is proposed` (conclusion)

## House style

自称 `is proposed in this paper` / `In this paper, a new AD-SAE network is proposed` / `this paper introduces` / `we have also conducted`。被动提出与第一人称复数并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Due to the limitations of sampling conditions and sampling techniques in many real industrial processes, the process data under different sampling conditions subject to different sampling frequencies, which leads to irregular interval sampling characteristics of the entire process data.
- abstract: However, the existing soft sensor modeling methods based on deep learning do not consider introducing dynamic historical information into the feature extraction process.
- abstract: To combat this issue, a novel attention-based dynamic stacked autoencoder networks (AD-SAE) for soft sensor modeling is proposed in this paper.
- abstract: The experimental results on the actual hydrocracking process data set show that the proposed method has better performance than traditional methods.
- introduction: Modern industry has obvious characteristics of multiple processes, complexity, and continuity.
- introduction: To address above problems, a novel attention-based dynamic stacked auto-encoder (AD-SAE) model is proposed to extract the abundant feature representation of irregular sampling process data in this paper.
- introduction: The remaining parts of this paper are organized as follows. Section 2 simply revisits the structure of SAE.
- experiments: In this section, the proposed AD-SAE based on soft sensor model is applied to an actual industrial hydrocracking process to verify the validity of the proposed method.
- experiments: Therefore, AD-SAE achieves the best prediction performance with the smallest RMSE and the largest R2, which further demonstrates the rationality and superiority of the proposed method.
- conclusion: In this paper, a new AD-SAE network is proposed to extract dynamic historical information characteristics of process data with irregular sampling frequencies.
- conclusion: The experimental results demonstrate that the proposed method has better predictive performance compared with traditional methods.
