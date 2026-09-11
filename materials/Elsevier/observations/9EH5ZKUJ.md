---
key: 9EH5ZKUJ
title: "Soft sensor modeling using deep learning with maximum relevance and minimum redundancy for quality prediction of industrial processes"
venue: "ISA Transactions"
doi: "10.1016/j.isatra.2025.02.010"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-19"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. The proposed MRMRRL soft sensor method` → `3. Case studies` → `4. Conclusions`。前置 `ABSTRACT` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 PCR/PLS/MLP/SVR、DBN/SAE/CNN/LSTM/GAN、quality-relevant representation 与 PCA 去冗余）。Introduction 末有编号贡献 `(1)` / `(2)` / `(3)` + 节序路标。Method 含 maximum relevance、KPCA 去冗余、AE layer extension、MRMRRL 训练。Experiments 标题为 `3. Case studies`（debutanizer + TE）。

## Openers

- abstract: `Deep learning techniques` — "Deep learning techniques such as autoencoder (AE) and stacked autoencoders (SAE) have gained growing popularity in soft sensor applications."
- introduction: `With the advent` — "With the advent of Industry 4.0, the process industry is developing towards intelligent and optimal manufacturing, which relies on advanced monitoring, control, and optimization technologies [1–4]."
- method: `Deep learning has` — "Deep learning has been applied to a wide range of fields due to its excellent representation learning capability."
- experiments: `To confirm the` — "To confirm the validity and superiority of the proposed MRMRRL soft sensor method, two case studies are considered, including an industrial debutanizer column process and a TE chemical process."
- conclusion: `To overcome the` — "To overcome the limitations of traditional deep learning algorithms, such as poor correlations between hidden features and output, structure and feature redundancy, and information loss, a new MRMRRL algorithm is proposed to extract hidden features with maximum relevance while ensuring minimum redundancy."

## Gap transitions

- however (abstract): "However, they often encounter several disadvantages, such as poor correlations between the extracted hidden features and the quality variable, inevitable information loss resulting from the layer-wise feature extraction, and information redundancy between the hidden features."
- however (introduction): "However, in actual production processes, the quality variables are usually difficult to measure online due to the complexity and harshness of the production environments, the high cost of analytical instruments, and the large lag time of analysis."
- thus (introduction): "Thus, measuring the critical quality variables in real time is particularly important to avoid a series of problems such as decreased production quality, wasted resources, and increased safety risks."
- to address (introduction): "To address these issues, soft sensor techniques have been proposed and are gaining increasing attention [5–7]."
- though (introduction): "Though deep learning models are good at processing large-volume and complex data sets and can automatically extract features, they often encounter high model complexity and risk of overfitting in the training process."
- to address (introduction): "To address the above-mentioned problems, an enhanced SAE algorithm namely MRMRRL is proposed for soft sensor modeling."

## Hedge verbs

- is proposed / causal / abstract: "Thus, a maximal relevance and minimal redundancy-based representation learning (MRMRRL) is proposed for quality prediction of industrial processes."
- show / associative / abstract: "The experimental results show that, compared with the baseline SAE, the performance of MRMRRL is improved by about 37 % and 38 % for two application examples, respectively."
- demonstrate / associative / abstract: "These results demonstrate the effectiveness and superiority of the proposed MRMRRL approach in extracting quality-related hidden features while ensuring automatic elimination of hidden feature redundancy and maintaining structure simplicity."
- is proposed / causal / introduction: "To address the above-mentioned problems, an enhanced SAE algorithm namely MRMRRL is proposed for soft sensor modeling."
- is improved / associative / conclusion: "Compared with the baseline SAE and NVW-SAE methods, the performance of MRMRRL is improved by about 37 % and 13 % in debutanizer process and by about 38 % and 9 % in TE process, respectively."
- remains / hedge / conclusion: "Evaluating the relevance and redundancy of models remains an open issue that deserves more efforts."

## Cross-section linkers

- introduction → method: "The rest of the paper proceeds as follows. Section 2 revisits the basic principles of AE and SAE."
- method → experiments: "Section 4 confirms the validity and superiority of the MRMRRL proposed method using two application examples."
- experiments → conclusion: "Section 5 draws the conclusions."（正文结论标题为 `4. Conclusions`）

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of the paper proceeds as follows.`
- R004 编号贡献：`The main contributions of this paper are three-fold:`
- R009 自称：`is proposed` / `The main contributions of this paper`

## Candidate phrases

- `a maximal relevance and minimal redundancy-based representation learning (MRMRRL) is proposed for quality prediction of industrial processes` (abstract)
- `The main contributions of this paper are three-fold:` (introduction)
- `The rest of the paper proceeds as follows.` (introduction)
- `To confirm the validity and superiority of the proposed MRMRRL soft sensor method, two case studies are considered` (experiments)
- `a new MRMRRL algorithm is proposed to extract hidden features with maximum relevance while ensuring minimum redundancy` (conclusion)

## House style

自称 `is proposed` / `The main contributions of this paper`。第三人称被动与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Deep learning techniques such as autoencoder (AE) and stacked autoencoders (SAE) have gained growing popularity in soft sensor applications.
- abstract: Thus, a maximal relevance and minimal redundancy-based representation learning (MRMRRL) is proposed for quality prediction of industrial processes.
- abstract: The experimental results show that, compared with the baseline SAE, the performance of MRMRRL is improved by about 37 % and 38 % for two application examples, respectively.
- introduction: With the advent of Industry 4.0, the process industry is developing towards intelligent and optimal manufacturing, which relies on advanced monitoring, control, and optimization technologies [1–4].
- introduction: To address the above-mentioned problems, an enhanced SAE algorithm namely MRMRRL is proposed for soft sensor modeling.
- introduction: The main contributions of this paper are three-fold:
- introduction: The rest of the paper proceeds as follows. Section 2 revisits the basic principles of AE and SAE.
- method: Deep learning has been applied to a wide range of fields due to its excellent representation learning capability.
- experiments: To confirm the validity and superiority of the proposed MRMRRL soft sensor method, two case studies are considered, including an industrial debutanizer column process and a TE chemical process.
- conclusion: To overcome the limitations of traditional deep learning algorithms, such as poor correlations between hidden features and output, structure and feature redundancy, and information loss, a new MRMRRL algorithm is proposed to extract hidden features with maximum relevance while ensuring minimum redundancy.
- conclusion: Compared with the baseline SAE and NVW-SAE methods, the performance of MRMRRL is improved by about 37 % and 13 % in debutanizer process and by about 38 % and 9 % in TE process, respectively.
