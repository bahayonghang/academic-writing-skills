---
key: HR7XMBFP
title: "Novel virtual sample generation method based on data augmentation and weighted interpolation for soft sensing with small data"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2023.120085"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Related methodologies` → `3. The proposed DAWI-VSG method` → `4. Case studies` → `5. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 SVM / Bayesian networks / Grey models，以及 SMOTE、GAN、VAE 与四类 VSG）。`2. Related methodologies` 为 SVD / ABOD / XGboost 预备，不是文献综述。Introduction 末有节序路标，无编号贡献列表。Experiments 标题为 `4. Case studies`（4.1 数值、4.2 PTA）。

## Openers

- abstract: `Data-driven soft` — "Data-driven soft sensing modeling plays an increasingly important role in the prediction of key variables in the process industry."
- introduction: `In the process` — "In the process of complicated chemical production nowadays, it is crucial to monitor and analyze the key variables of products (Gu et al., 2020, 2021a)."
- method: `This section briefly` — "This section briefly describes the methods and principles of SVD, ABOD and XGboost models." (s.2)
- experiments: `In this section` — "In this section, two case studies including the dataset extracted from a 10-dimensional function and the PTA industrial dataset were employed to validate the efficiency and feasibility of the suggested DAWI-VSG."
- conclusion: `Aiming at the` — "Aiming at the small sample problem of complex chemical production processes, this paper proposes the novel DAWI-VSG method, which significantly improves the prediction performance of soft sensor by adding virtual samples."

## Gap transitions

- however (introduction): "However, in practice, physical sensors directly used for measuring and analyzing product variables are increasingly inadequate for production requirement due to complex production environments and expensive measurement costs."
- however (introduction): "However, in the actual production process, the problems of difficult data collection and high cost of sample labeling make the obtained data redundant and unbalanced, and lack of representativeness of the overall (He et al., 2020)."
- to address (s.2.1): "To address this issue, SVD is used for data augmentation to enhance the space and features of the original small samples in this study in order to prepare for better generation of virtual samples."

## Hedge verbs

- is proposed / causal / abstract: "a virtual sample generation method based on data augmentation and weighted interpolation (DAWI-VSG) is proposed"
- showed / associative / abstract: "The results showed that the proposed DAWI-VSG can boost the predictive power of soft sensing"
- demonstrates / causal / experiments: "It demonstrates that the generated samples well-fill the sparse area in the raw space and improve the data diversity."
- prove / causal / experiments: "This proves that our improvements to the FastABOD method are positive and effective."

## Cross-section linkers

- introduction → method: "The remainder of the paper is organized as follows. The second part presents the basic principles and mathematical formulations of the related method."
- method → experiments: "The fourth part presents experiments and results for a standard function dataset and a real industrial dataset."
- experiments → conclusion: PTA 箱线图与 FastABOD 对照表后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction；`2. Related methodologies` 作方法预备。
- R003 节序路标：`The remainder of the paper is organized as follows`
- R009 自称：`In this paper, a virtual sample generation method ... is proposed` / `this paper proposes`

## Candidate phrases

- `In this paper, a virtual sample generation method based on data augmentation and weighted interpolation (DAWI-VSG) is proposed` (abstract)
- `Based on the mentioned considerations, a virtual sample generation approach ... is presented` (introduction)
- `The remainder of the paper is organized as follows` (introduction)
- `Aiming at the small sample problem ... this paper proposes` (conclusion)

## House style

自称 `In this paper, ... is proposed` / `this paper proposes` / `in this study` / `We think that the message of the original samples should be valued`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Data-driven soft sensing modeling plays an increasingly important role in the prediction of key variables in the process industry.
- abstract: In this paper, a virtual sample generation method based on data augmentation and weighted interpolation (DAWI-VSG) is proposed to expand the soft sensing dataset with high-quality samples.
- abstract: The results showed that the proposed DAWI-VSG can boost the predictive power of soft sensing by generating higher quality and more reasonable samples compared to other advanced methods.
- introduction: In the process of complicated chemical production nowadays, it is crucial to monitor and analyze the key variables of products (Gu et al., 2020, 2021a).
- introduction: However, in practice, physical sensors directly used for measuring and analyzing product variables are increasingly inadequate for production requirement due to complex production environments and expensive measurement costs.
- introduction: The remainder of the paper is organized as follows. The second part presents the basic principles and mathematical formulations of the related method.
- method: This section briefly describes the methods and principles of SVD, ABOD and XGboost models.
- experiments: In this section, two case studies including the dataset extracted from a 10-dimensional function and the PTA industrial dataset were employed to validate the efficiency and feasibility of the suggested DAWI-VSG.
- experiments: The MAE of the soft sensor modeling decreases by at most 27.12 % and the MSE by 41.61 % compared to when no virtual samples are added.
- conclusion: Aiming at the small sample problem of complex chemical production processes, this paper proposes the novel DAWI-VSG method, which significantly improves the prediction performance of soft sensor by adding virtual samples.
- conclusion: The results of the experiments demonstrate that the DAWI-VSG surpasses the seven advanced comparison methods.
