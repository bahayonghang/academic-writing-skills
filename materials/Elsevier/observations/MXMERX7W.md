---
key: MXMERX7W
title: "Semi-supervised soft sensor development based on dynamic dimensionality reduction-assisted large-scale pseudo label optimization and sample-weighted quality-relevant deep learning"
venue: "Chemical Engineering Science"
doi: "10.1016/j.ces.2024.120387"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-20"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries` → `3. Dynamic dimensionality reduction-assisted large-scale pseudo label optimization` → `4` SEWQAE 建模 → `5` 实施流程 → `6` CTC 与 TE 验证 → `7. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 self-training/co-training、伪标签优化、样本加权与质量相关自编码器）。Introduction 末编号贡献（`(1)` / `(2)`）+ 节序路标。Method 拆成预备、DDR-LSPLO、SEWQAE。Experiments 标题为 `6`（工业 CTC 发酵 + TE）。

## Openers

- abstract: `Data-driven soft sensors` — "Data-driven soft sensors have become popular tools for estimating critical quality variables in the process industry."
- introduction: `The manufacturing industry,` — "The manufacturing industry, which provides essential tools and materials for the survival and production of human beings, is an important force in driving sustained economic and social development (Zhong et al., 2017; Yang et al., 2021; Huang et al., 2024)."
- method: `Previous studies (Jin` — "Previous studies (Jin et al., 2021; Jin et al., 2023) have confirmed that the pseudo label estimation can be achieved through solving an explicit optimization, which can effectively avoid error accumulation and propagation that occur in the self-labeling techniques and thus improve the pseudo label estimation performance."
- experiments: `CTC, with the` — "CTC, with the chemical formula of C22H23ClN2O8, is a broad-spectrum antibiotic with extensive use in the fields of medicine and animal husbandry."
- conclusion: `To address the` — "To address the insufficiency of labeled data in soft sensor modeling, this paper proposes a large-scale pseudo label optimization method called DDR-LSPLO to estimate labels for the unlabeled data."

## Gap transitions

- however (abstract, introduction): "However, in practical applications, it is very common that the unlabeled data are abundant but the labeled data are scarce, which poses a great challenge for developing high-performance data-based soft sensors."
- therefore (introduction): "Therefore, applying soft sensor techniques to measure such critical quality variables in real time has gained increasing popularity (Wang et al., 2009; Ge, 2014; Yuan et al., 2016; Zheng and Song, 2018)."
- nevertheless (introduction): "Nevertheless, traditional supervised machine learning methods cannot leverage information from abundant unlabeled data (Zhou, 2018)."
- to address (introduction): "To address this issue, semi-supervised learning (Mallapragada et al., 2008; Balcan and Blum, 2010; Yu et al., 2020) has received great attention over the last two decades."

## Hedge verbs

- is proposed / causal / abstract: "a dynamic dimensionality reduction-assisted large-scale pseudo label optimization method (DDR-LSPLO) is proposed for achieving sample expansion."
- are verified / causal / abstract: "The effectiveness and superiority of the proposed DDR-LSPLO and SEWQAE methods are verified through an industrial chlortetracycline (CTC) fermentation process and a simulated Tennessee Eastman (TE) chemical process."
- is developed / causal / abstract: "a sample expansion and weighting-based quality-relevant autoencoder (SEWQAE) is developed for semi-supervised soft sensor modeling."
- demonstrate / associative / conclusion: "The application results of the two case studies demonstrate the effectiveness and superiority of the proposed DDR-LSPLO and SEWQAE methods."

## Cross-section linkers

- introduction → preliminaries: "The rest of the paper is structured as follows. Section 2 briefly introduces the basic principles of K-nearest neighbors (KNN), estimation of distribution algorithm (EDA), and autoencoder (AE)."
- preliminaries → method: "Section 3 details the proposed DDR-LSPLO algorithm for solving large-scale pseudo label optimization problems."
- method → experiments: "Section 6 validates the effectiveness and superiority of DDR-LSPLO and SEWQAE through an industrial CTC fermentation process and TE chemical processes."
- experiments → conclusion: TE 散点图后 `7. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of the paper is structured as follows`
- R004 编号贡献：`In summary, the main contributions of this paper are twofold:`
- R009 自称：`this paper proposes` / `is proposed` / `is developed`

## Candidate phrases

- `a dynamic dimensionality reduction-assisted large-scale pseudo label optimization method (DDR-LSPLO) is proposed` (abstract)
- `In summary, the main contributions of this paper are twofold:` (introduction)
- `The rest of the paper is structured as follows` (introduction)
- `this paper proposes a large-scale pseudo label optimization method called DDR-LSPLO` (conclusion)

## House style

自称 `this paper proposes` / `is proposed` / `is developed` / `The rest of the paper is structured as follows`。被动与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Data-driven soft sensors have become popular tools for estimating critical quality variables in the process industry.
- abstract: However, in practical applications, it is very common that the unlabeled data are abundant but the labeled data are scarce, which poses a great challenge for developing high-performance data-based soft sensors.
- abstract: Thus, a dynamic dimensionality reduction-assisted large-scale pseudo label optimization method (DDR-LSPLO) is proposed for achieving sample expansion.
- abstract: The effectiveness and superiority of the proposed DDR-LSPLO and SEWQAE methods are verified through an industrial chlortetracycline (CTC) fermentation process and a simulated Tennessee Eastman (TE) chemical process.
- introduction: The manufacturing industry, which provides essential tools and materials for the survival and production of human beings, is an important force in driving sustained economic and social development (Zhong et al., 2017; Yang et al., 2021; Huang et al., 2024).
- introduction: Therefore, applying soft sensor techniques to measure such critical quality variables in real time has gained increasing popularity (Wang et al., 2009; Ge, 2014; Yuan et al., 2016; Zheng and Song, 2018).
- introduction: Nevertheless, traditional supervised machine learning methods cannot leverage information from abundant unlabeled data (Zhou, 2018).
- introduction: In summary, the main contributions of this paper are twofold:
- introduction: The rest of the paper is structured as follows. Section 2 briefly introduces the basic principles of K-nearest neighbors (KNN), estimation of distribution algorithm (EDA), and autoencoder (AE).
- experiments: CTC, with the chemical formula of C22H23ClN2O8, is a broad-spectrum antibiotic with extensive use in the fields of medicine and animal husbandry.
- conclusion: To address the insufficiency of labeled data in soft sensor modeling, this paper proposes a large-scale pseudo label optimization method called DDR-LSPLO to estimate labels for the unlabeled data.
- conclusion: The application results of the two case studies demonstrate the effectiveness and superiority of the proposed DDR-LSPLO and SEWQAE methods.
