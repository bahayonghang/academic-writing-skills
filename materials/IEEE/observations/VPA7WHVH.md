---
key: VPA7WHVH
title: "Prox-STA-LSTM: A Sparse Representation for the Attention-Based LSTM Networks for Industrial Soft Sensor Development"
venue: "IEEE Access"
doi: "10.1109/ACCESS.2024.3409899"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. THE ATTENTION-BASED LSTM` → `III. THE PROX-STA-LSTM` → `IV. CASE STUDY` → `V. CONCLUSION AND DISCUSSION`。前置 `ABSTRACT` 与 `INDEX TERMS`。无独立 Related Work 标题。`related_work=inlined`（Introduction 中段评 PLSR / SVM / ANN / LSTM / attention-LSTM / 稀疏表示；Section II 为 LSTM 预备，引言称为 “related works on LSTM”）。Introduction 末有编号贡献 + 节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDY`（碳吸收器 + debutanizer）。

## Openers

- abstract: `For deep learning` — "For deep learning based soft sensors, the spatiotemporal attention (STA)-LSTM is a newly emerged technique which provides efficient predictions for quality variables of industrial processes." (p.1)
- introduction: `With the increasing` — "With the increasing process scale and complexity of modern industrial production, the real-time assessment and prediction of the critical process variables, referred to as the Key Performance Indicators (KPIs), are of paramount importance." (p.1)
- method: `The success of` — "The success of STA-LSTM soft sensor relies on complex deep network structure and high dimensional data, which inevitably leads to expensive computing costs and memory allocation consumption, limiting the effectiveness of attention-based LSTM methods in practical applications." (p.5, III.A)
- experiments: `In order to` — "In order to validate the performance of the proposed Prox-STA-LSTM model, we undertake case studies, one is a carbon absorber simulation data and the other is the debutanizer column actual data." (p.7, IV)
- conclusion: `In this paper` — "In this paper, we proposed the Prox-STA-LSTM soft sensor, a sparse representation of attention-based LSTM networks." (p.11)

## Gap transitions

- however (abstract): "However, the STA-LSTM methods calls for an enormous network structure, which contains redundant network weights and therefore diminishing the model generalization ability." (p.1)
- however (introduction): "However, most of these methods mentioned above are often linear and/or static, hard to capture intricate dynamic and nonlinear relationships [10]." (p.1)
- however (introduction): "However, when the length of the input sequence become too long, the classical LSTM network has difficulty in training a high-performance soft sensor or even conversely leading to its performance deteriorate." (p.2)
- to address (introduction): "To address these difficulties, sparse modeling presents an avenue to alleviate the training burden and enhance prediction efficiency." (p.2)
- nonetheless (introduction): "Nonetheless, the loss function with an addition of the `1-regularization term is a non-strictly convex function that is not continuously differentiable" (p.3)

## Hedge verbs

- consider / causal / abstract: "In this paper, we consider model sparse representation for the STA-LSTM"
- propose / causal / introduction, conclusion: "we propose the Prox-STA-LSTM model"; "we proposed the Prox-STA-LSTM soft sensor"
- show / causal / abstract: "The results show that Prox-STA-LSTM can successfully sparsify the STA-LSTM networks"
- may / speculative / conclusion: "The proposed proximal-type Adam algorithm may not always be fully satisfied by neural networks deployed in practice"
- could / speculative / method: "a sparse version, which could be more attractive for practical industrial applications"

## Cross-section linkers

- introduction → method: "The subsequent sections of this paper are organized as follows: section II provides a brief description of the related works on LSTM. Section III delineates the Prox-STA-LSTM model in detail, together with its training algorithm. Section IV investigates a carbon absorber and an industrial desulfurization process, with comparisons to various deep learning models such that features of the Prox-STA-LSTM are explored. Concluding remarks and an outline of future research work are presented in Section V." (p.3)
- method → experiments: Algorithm 2 / Fig. 5 后直接 `IV. CASE STUDY` (p.7)
- experiments → conclusion: 案例结果后直接 `V. CONCLUSION AND DISCUSSION` (p.11)

## Candidate rules

- R001 abstract 自称 `In this paper, we consider`，贡献收束用 `The results show that`。
- R002 Introduction 无独立 Related Work 标题；LSTM 预备放在 II，引言中段已评 attention-LSTM 与稀疏表示。
- R003 贡献用 `The major contributions of this paper are listed as follows` + 编号列表。
- R004 Introduction 末用 `The subsequent sections of this paper are organized as follows` 指向 II–V。
- R005 Conclusion 标题为 `CONCLUSION AND DISCUSSION`，先 `In this paper, we proposed`，再用 `may not always` 承认局限。

## Candidate phrases

- `In this paper, we consider` (abstract)
- `In this paper, we propose the Prox-STA-LSTM model` (introduction)
- `The major contributions of this paper are listed as follows:` (introduction)
- `The subsequent sections of this paper are organized as follows:` (introduction)
- `In this paper, we proposed the Prox-STA-LSTM soft sensor` (conclusion)

## House style

自称是 `In this paper` / `we propose` / `we consider` / `our proposed`。未见 `Here we`。`In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: For deep learning based soft sensors, the spatiotemporal attention (STA)-LSTM is a newly emerged technique which provides efficient predictions for quality variables of industrial processes.
- p.1 abstract: However, the STA-LSTM methods calls for an enormous network structure, which contains redundant network weights and therefore diminishing the model generalization ability.
- p.1 abstract: In this paper, we consider model sparse representation for the STA-LSTM to cope with the above problem.
- p.1 abstract: The results show that Prox-STA-LSTM can successfully sparsify the STA-LSTM networks. More importantly, the prediction performances are also enhanced.
- p.1 introduction: With the increasing process scale and complexity of modern industrial production, the real-time assessment and prediction of the critical process variables, referred to as the Key Performance Indicators (KPIs), are of paramount importance.
- p.1 introduction: However, most of these methods mentioned above are often linear and/or static, hard to capture intricate dynamic and nonlinear relationships [10].
- p.2 introduction: To address these difficulties, sparse modeling presents an avenue to alleviate the training burden and enhance prediction efficiency.
- p.3 introduction: In this paper, we propose the Prox-STA-LSTM model, a sparse representation of the STA-LSTM for industrial soft sensor developments, by incorporating the `1-regularization.
- p.3 introduction: The major contributions of this paper are listed as follows:
- p.3 introduction: The subsequent sections of this paper are organized as follows: section II provides a brief description of the related works on LSTM. Section III delineates the Prox-STA-LSTM model in detail, together with its training algorithm.
- p.5 method: The success of STA-LSTM soft sensor relies on complex deep network structure and high dimensional data, which inevitably leads to expensive computing costs and memory allocation consumption, limiting the effectiveness of attention-based LSTM methods in practical applications.
- p.7 experiments: In order to validate the performance of the proposed Prox-STA-LSTM model, we undertake case studies, one is a carbon absorber simulation data and the other is the debutanizer column actual data.
- p.11 conclusion: In this paper, we proposed the Prox-STA-LSTM soft sensor, a sparse representation of attention-based LSTM networks.
- p.11 conclusion: The experimental results of proposed Prox-STA-LSTM model helps reduce redundant parameters and improve generalization performance without compromising accuracy.
- p.11 conclusion: The proposed proximal-type Adam algorithm may not always be fully satisfied by neural networks deployed in practice.
- p.11 conclusion: In general, the balance between model complexity and sparse representation is still an open subject, which deserves further exploration in both theoretical and technical aspects.
