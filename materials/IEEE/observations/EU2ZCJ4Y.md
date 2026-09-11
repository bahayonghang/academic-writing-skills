---
key: EU2ZCJ4Y
title: "Probabilistic fusion model for industrial soft sensing based on quality-relevant feature clustering"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3224975"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. REVIEW ON PARTIAL LEAST SQUARES` → `III. PROPOSED QRFC FOR SOFT SENSING` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR/PLS、核方法、NN、概率混合与可解释性）。Section II 为 PLS 预备，不是 Related Work。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `CASE STUDY`（氨合成一次转化炉 O2）。

## Openers

- abstract: `For most modern` — "For most modern industrial processes with strong nonlinear and multimodal characteristics, the traditional linear PLS-based soft sensor may not work well." (p.9037)
- introduction: `FACED with the` — "FACED with the increasing complexity of modern industrial processes, the maximum economic benefits can be obtained if safe and stable operations are achieved." (p.9037)
- method: `In this article` — "In this article, to model the distribution of the predicted value Y, based on the latent variable T that extracted by the PLS method, a novel QRFC model is proposed, which aims to enhance the prediction capability of the PLS method." (p.9039, III.A)
- experiments: `In this section` — "In this section, the proposed method is applied to develop a soft sensor for a real industrial process in an ammonia synthesis plant (ASP)." (p.9041)
- conclusion: `In the present` — "In the present article, a novel quality-relevant feature clustering (QRFC) model was proposed, which could effectively describe industrial processes with nonlinear and multimode characteristics." (p.9046)

## Gap transitions

- however (introduction): "However, these variables are not easy to measure in real time for a series of reasons such as expensive analyzers, large measurement delays, and maintenance issues." (p.9037)
- however (introduction): "However, while confronting real complex industrial processes that contain strong nonlinear and multimode characteristics, traditional statistical soft-sensing methods (i.e., PCR, PLS, etc.) perform poorly due to their linearity assumptions." (p.9037)
- unfortunately (introduction): "Unfortunately, kernel methods tend to become intractable to compute in large-scale data application scenarios due to the large size of the kernel matrix (size n × n)." (p.9038)
- to this end (introduction): "To this end, this article proposes a novel soft sensor modeling framework based on the PLS method from the perspective of local modeling of probabilistic fusion, called the quality-relevant feature clustering (QRFC) model." (p.9038)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a novel quality-relevant feature clustering (QRFC) model is proposed for the first time in this article"; "this article proposes a novel soft sensor modeling framework"; "a novel quality-relevant feature clustering (QRFC) model was proposed"
- demonstrate / causal / abstract: "The experimental results demonstrate that the proposed method outperforms several other soft sensing approaches."
- may / speculative / abstract, conclusion: "the traditional linear PLS-based soft sensor may not work well"; "it may be more suitable for industrial big data scenarios"
- show / causal / experiments: "As shown in Fig. 3(a), the predictions by the linear PLS-based soft sensor significantly deviate from the true values"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. First, the PLS is reviewed in Section II. Then, the QRFC-based soft sensor framework is given in Section III, which contains the detailed description of the proposed QRFC model and soft sensor development. In the next section, a real case study is carried out for performance evaluation. Finally, Section V concludes the article." (p.9038)
- method → experiments: 评价指标后 `IV. CASE STUDY` (p.9041)
- experiments → conclusion: 参数敏感性后 `V. CONCLUSION` (p.9046)

## Candidate rules

- R009 摘要用 `is proposed for the first time in this article` 点名 QRFC。
- R002 Introduction 无独立 Related Work，非线性/可解释性评述写在引言中段。
- R004 贡献列表：`The main contributions of this article are summarized in the following aspects.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法，再用 `In this case, the QRFC framework can be further extended ... in the future work` 指向小样本。

## Candidate phrases

- `a novel quality-relevant feature clustering (QRFC) model is proposed for the first time in this article` (abstract)
- `To this end, this article proposes` (introduction)
- `The main contributions of this article are summarized in the following aspects.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In the present article, a novel ... model was proposed` (conclusion)

## House style

自称 `this article proposes` / `In the present article` / `the proposed method`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.9037 abstract: For most modern industrial processes with strong nonlinear and multimodal characteristics, the traditional linear PLS-based soft sensor may not work well.
- p.9037 abstract: To this end, based on the PLS, a novel quality-relevant feature clustering (QRFC) model is proposed for the first time in this article from the view of local modeling of probabilistic fusion.
- p.9037 abstract: The experimental results demonstrate that the proposed method outperforms several other soft sensing approaches.
- p.9037 introduction: FACED with the increasing complexity of modern industrial processes, the maximum economic benefits can be obtained if safe and stable operations are achieved.
- p.9037 introduction: However, these variables are not easy to measure in real time for a series of reasons such as expensive analyzers, large measurement delays, and maintenance issues.
- p.9037 introduction: However, while confronting real complex industrial processes that contain strong nonlinear and multimode characteristics, traditional statistical soft-sensing methods (i.e., PCR, PLS, etc.) perform poorly due to their linearity assumptions.
- p.9038 introduction: Unfortunately, kernel methods tend to become intractable to compute in large-scale data application scenarios due to the large size of the kernel matrix (size n × n).
- p.9038 introduction: To this end, this article proposes a novel soft sensor modeling framework based on the PLS method from the perspective of local modeling of probabilistic fusion, called the quality-relevant feature clustering (QRFC) model.
- p.9038 introduction: The main contributions of this article are summarized in the following aspects.
- p.9038 introduction: The rest of this article is organized as follows. First, the PLS is reviewed in Section II. Then, the QRFC-based soft sensor framework is given in Section III, which contains the detailed description of the proposed QRFC model and soft sensor development. In the next section, a real case study is carried out for performance evaluation. Finally, Section V concludes the article.
- p.9039 method: In this article, to model the distribution of the predicted value Y, based on the latent variable T that extracted by the PLS method, a novel QRFC model is proposed, which aims to enhance the prediction capability of the PLS method.
- p.9041 experiments: In this section, the proposed method is applied to develop a soft sensor for a real industrial process in an ammonia synthesis plant (ASP).
- p.9042 experiments: In order to reduce the cost of measuring the O2 content, a data-driven soft sensor can be built here based on the historical data.
- p.9042 experiments: As shown in Fig. 3(a), the predictions by the linear PLS-based soft sensor significantly deviate from the true values, implying that this primary reformer process is strongly nonlinear.
- p.9043 experiments: Therefore, it can be concluded that the predicted O2 concentrations by the QRFC-based soft sensor get better performance.
- p.9046 conclusion: In the present article, a novel quality-relevant feature clustering (QRFC) model was proposed, which could effectively describe industrial processes with nonlinear and multimode characteristics.
- p.9046 conclusion: A real industrial case has demonstrated the effectiveness and feasibility of the QRFC-based soft sensor method.
- p.9046 conclusion: In this case, the QRFC framework can be further extended for industrial small-sample soft sensor modeling in the future work.
