---
key: 29PVLNE4
title: "A Deep Residual PLS for Data-Driven Quality Prediction Modeling in Industrial Process"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2024.124578"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. Introduction` → `II. Partial Least Squares (PLS)` → `III. Deep Residual Partial Least Squares (DRPLS)` → `IV. Case Studies` → `V. Conclusion`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 DPCA / residual deep PCA / SPCA / DPLS / GDPLS / DeKPLS）。Introduction 末有节序路标，指向 Section II–V。Method 为 II（PLS 预备）+ III（DRPLS）。Experiments 标题为 `Case Studies`（工业加氢裂化）。

## Openers

- abstract: `Partial least squares` — "Partial least squares (PLS) model is the most typical data-driven method for quality-related industrial tasks like soft sensor." (p.1)
- introduction: `IN industrial processes` — "IN industrial processes, it is essential to timely measure the key quality variables for effective process monitoring, control and optimization [1]−[5]." (p.1；栏首掉字)
- method: `PLS is a` — "PLS is a classical multivariate statistical algorithm, which can simplify the data structure, make correlation analysis and establish regression model by finding a latent variable space to reconstruct both the input and output data." (p.2, II)
- experiments: `In this section` — "In this section, a case study on an industrial hydrocracking process is used to validate the effectiveness of the proposed DRPLS." (p.4, IV)
- conclusion: `In this paper` — "In this paper, a DRPLS is proposed for quality prediction in industrial process." (p.8, V)

## Gap transitions

- however (abstract): "However, only linear relations are captured between the input and output data in the PLS." (p.1)
- although (introduction): "Although these methods show good performance in feature extraction with multiple nonlinear modules, most of them are unsupervised learning methods." (p.2)
- however (introduction): "However, the above methods only focus on the information from latent variables, with no consideration of the residual subspace in PLS." (p.2)
- although (method): "Although linear features of raw data can be extracted with the 1st PLS, abundant nonlinear information still remains in the residual subspace and fails to be utilized." (p.4)
- however (conclusion): "However, it is a difficult task to determine the forms and types of nonlinear transformations in the proposed DRPLS method." (p.8)

## Hedge verbs

- propose / causal / abstract, introduction: "a deep residual PLS (DRPLS) framework is proposed for quality prediction in this paper"; "a novel deep residual PLS (DRPLS) is proposed in this paper"
- indicate / speculative / method: "It is indicated that the nonlinear relations between input and output data still remain in the residual subspace."
- show / causal / experiments: "Model applications on hydrocracking process show that the prediction performance of DRPLS is superior to those of some typical nonlinear PLS methods and deep learning methods."
- may / speculative / conclusion: "For future work, we may pay more attention to dealing with this problem."

## Cross-section linkers

- introduction → method: "The remaining parts of this paper are organized as follows. In Section II, PLS is briefly introduced. Section III provides the detailed description of the proposed DRPLS model. Then, DRPLS is applied to an industrial hydrocracking process for product quality prediction in Section IV. Finally, conclusions are given in Section V." (p.2)
- method → experiments: "To evaluate the performance of the proposed DRPLS, two indices are calculated on the testing set" 随后 `IV. Case Studies` (p.4)
- experiments → conclusion: 结果段落后直接 `V. Conclusion` (p.8)

## Candidate rules

- R001 abstract 贡献句用 `a ... framework is proposed ... in this paper`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有浅层/深层 PLS 评述写在引言中段。
- R003 Introduction 末用 `The remaining parts of this paper are organized as follows` 指向 II–V。
- R004 Conclusion 先收回方法，再用 `However` 承认局限，`For future work, we may` 指向后续。

## Candidate phrases

- `a deep residual PLS (DRPLS) framework is proposed for quality prediction in this paper` (abstract)
- `To alleviate the above problems, a novel deep residual PLS (DRPLS) is proposed in this paper.` (introduction)
- `The remaining parts of this paper are organized as follows.` (introduction)
- `In this paper, a DRPLS is proposed for quality prediction in industrial process.` (conclusion)
- `For future work, we may pay more attention to dealing with this problem.` (conclusion)

## House style

自称是 `this paper` / `the proposed DRPLS` / `we may`。未见 `Here we`。`in this paper` 与 `is proposed` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 以外的 `This article`。

## Quotes

- p.1 abstract: Partial least squares (PLS) model is the most typical data-driven method for quality-related industrial tasks like soft sensor.
- p.1 abstract: However, only linear relations are captured between the input and output data in the PLS.
- p.1 abstract: To fully utilize data information in PLS residual subspaces, a deep residual PLS (DRPLS) framework is proposed for quality prediction in this paper.
- p.1 abstract: The effectiveness of the proposed DRPLS is validated on an industrial hydrocracking process.
- p.1 introduction: IN industrial processes, it is essential to timely measure the key quality variables for effective process monitoring, control and optimization [1]−[5].
- p.2 introduction: Although these methods show good performance in feature extraction with multiple nonlinear modules, most of them are unsupervised learning methods.
- p.2 introduction: However, the above methods only focus on the information from latent variables, with no consideration of the residual subspace in PLS.
- p.2 introduction: To alleviate the above problems, a novel deep residual PLS (DRPLS) is proposed in this paper.
- p.2 introduction: The remaining parts of this paper are organized as follows. In Section II, PLS is briefly introduced. Section III provides the detailed description of the proposed DRPLS model. Then, DRPLS is applied to an industrial hydrocracking process for product quality prediction in Section IV. Finally, conclusions are given in Section V.
- p.2 method: PLS is a classical multivariate statistical algorithm, which can simplify the data structure, make correlation analysis and establish regression model by finding a latent variable space to reconstruct both the input and output data.
- p.4 method: Although linear features of raw data can be extracted with the 1st PLS, abundant nonlinear information still remains in the residual subspace and fails to be utilized.
- p.4 experiments: In this section, a case study on an industrial hydrocracking process is used to validate the effectiveness of the proposed DRPLS.
- p.6 experiments: As can be seen, PLS has the worst prediction performance because it is a linear regression method.
- p.8 conclusion: In this paper, a DRPLS is proposed for quality prediction in industrial process.
- p.8 conclusion: Model applications on hydrocracking process show that the prediction performance of DRPLS is superior to those of some typical nonlinear PLS methods and deep learning methods.
- p.8 conclusion: However, it is a difficult task to determine the forms and types of nonlinear transformations in the proposed DRPLS method.
- p.8 conclusion: For future work, we may pay more attention to dealing with this problem.
