---
key: QFZ4XUD3
title: "A Contrastive Representation Domain Adaptation Method for Industrial Time-Series Cross-Domain Prediction"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3523572"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`：`A. DA Methods` / `B. Contrastive Learning`）。Introduction 中段已列 DA 缺口，再单独开相关工作。无 `The rest of this article is organized as follows`。Method 在正文中段。Experiments 标题为 `EXPERIMENT`（C-MAPSS RUL）。

## Openers

- abstract: `Industrial time-series prediction` — "Industrial time-series prediction is crucial for Industrial Internet of Things." (p.1)
- introduction: `INDUSTRIAL Internet of` — "INDUSTRIAL Internet of Things (IIoT) powered by advanced information technology is leading a disruptive revolution in modern industry [1], [2]." (p.1；栏首掉字)
- related_work: `DA methods can` — "DA methods can be summarized as follows: domain distribution alignment-based methods, normalized statistics-based methods, ensemble-based methods, and decision boundary-based methods, according to their unique research routes and modeling concepts." (p.2, II.A)
- method: `For clarity, we` — "For clarity, we adopt the basic standard notation of DA." (p.3, III.A)
- experiments: `The effectiveness of` — "The effectiveness of CTPA is measured experimentally." (p.6, IV)
- conclusion: `In this article,` — "In this article, a novel DA method, CTPA, for industrial time-series prediction is proposed." (p.9)

## Gap transitions

- however (abstract): "However, conventional methods may overlook the intradomain distribution and the mutual information, leading to incorrect semantic alignment and loss of prediction-relevant information." (p.1)
- to address (abstract): "To address these issues, a contrastive learning-based domain adaptation method, contrastive temporal prediction adaptation, for industrial time-series cross-domain prediction is proposed." (p.1)
- however (introduction): "However, this assumption does not always hold true in real applications." (p.1)
- therefore (introduction): "Therefore, novel approaches are imperative to address issues related to insufficiently labeled data and dynamic working conditions, and to promote more accurate and robust predictions in industrial settings." (p.1)
- despite (introduction): "Despite the remarkable success of DA in cross-domain time-series analysis, several challenges remain in prediction tasks as it is mainly applied to classification tasks." (p.2)
- nonetheless (conclusion): "Nonetheless, the data used for model training may be heterogeneous or even inaccessible in practical applications." (p.9)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a contrastive learning-based domain adaptation method ... is proposed"; "a novel contrastive learning-based DA method, contrastive temporal prediction adaptation (CTPA), is proposed"
- demonstrate / causal / abstract: "The results demonstrate that our method outperforms existing methods."
- verify / causal / abstract, conclusion: "The performance of our method is verified through experiments on CMAPSS dataset."; "The effectiveness of our proposed CTPA is verified through extensive experiments."
- show / causal / experiments: "Experimental results show that our model outperforms LSTM and TCN."

## Cross-section linkers

- introduction → related work: 贡献列表后直接 `II. RELATED WORKS`，无节序路标 (p.2)
- related work → method: "How to exploit the mutual information between samples in regression tasks is a problem to be addressed." 随后 `III. METHODOLOGY` (p.3)
- method → experiments: "The overall loss function in target domain alignment can be summarized as" 随后 `IV. EXPERIMENT` (p.6)
- experiments → conclusion: `F. Sensitivity Analysis` 后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 被动贡献句 `... is proposed`，自称 `our method`，不用 `Here we`。
- R002 独立 `II. RELATED WORKS`，按方法族分小节。
- R003 贡献用 `The contributions are illustrated as follows.` + 编号列表。
- R004 Conclusion 先被动收回方法，再用 `Nonetheless` + `In future research, we will` 指向后续。

## Candidate phrases

- `To address these issues, a ... method ... is proposed.` (abstract)
- `The results demonstrate that our method outperforms existing methods.` (abstract)
- `To cope with the above challenges, a novel ... method ... is proposed.` (introduction)
- `The contributions are illustrated as follows.` (introduction)
- `In this article, a novel DA method, CTPA, for industrial time-series prediction is proposed.` (conclusion)

## House style

自称是 `this article` / `our method` / `we propose` / `the proposed CTPA`。未见 `Here we`。未见 `In this paper`。`In this article` 与 `our method` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Industrial time-series prediction is crucial for Industrial Internet of Things.
- p.1 abstract: However, conventional methods may overlook the intradomain distribution and the mutual information, leading to incorrect semantic alignment and loss of prediction-relevant information.
- p.1 abstract: To address these issues, a contrastive learning-based domain adaptation method, contrastive temporal prediction adaptation, for industrial time-series cross-domain prediction is proposed.
- p.1 abstract: The results demonstrate that our method outperforms existing methods.
- p.1 introduction: INDUSTRIAL Internet of Things (IIoT) powered by advanced information technology is leading a disruptive revolution in modern industry [1], [2].
- p.1 introduction: Therefore, novel approaches are imperative to address issues related to insufficiently labeled data and dynamic working conditions, and to promote more accurate and robust predictions in industrial settings.
- p.2 introduction: Despite the remarkable success of DA in cross-domain time-series analysis, several challenges remain in prediction tasks as it is mainly applied to classification tasks.
- p.2 introduction: The contributions are illustrated as follows.
- p.2 related_work: DA methods can be summarized as follows: domain distribution alignment-based methods, normalized statistics-based methods, ensemble-based methods, and decision boundary-based methods, according to their unique research routes and modeling concepts.
- p.3 method: For clarity, we adopt the basic standard notation of DA.
- p.6 experiments: The effectiveness of CTPA is measured experimentally.
- p.9 conclusion: In this article, a novel DA method, CTPA, for industrial time-series prediction is proposed.
- p.9 conclusion: The effectiveness of our proposed CTPA is verified through extensive experiments.
- p.9 conclusion: Nonetheless, the data used for model training may be heterogeneous or even inaccessible in practical applications.
- p.9 conclusion: In future research, we will explore domain adaption methods in the case where the source and target data are heterogeneous or inaccessible.
