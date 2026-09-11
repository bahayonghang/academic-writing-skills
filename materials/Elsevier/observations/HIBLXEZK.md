---
key: HIBLXEZK
title: "A semi-supervised soft sensor method based on vine copula regression and tri-training algorithm for complex chemical processes"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2022.11.004"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries` → `3. Proposed tri-training VCR method` → `4. Applications` → `5. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR/PLS/copula、半监督与 co-training/tri-training）。Introduction 末有节序路标，指向 Section 2–5。Method 拆成 Preliminaries 与 Proposed method。Experiments 标题为 `Applications`（数值算例 + 硫回收装置工业例）。

## Openers

- abstract: `Soft sensor technology` — "Soft sensor technology is an important solution for timely prediction of some difficult-to-measure variables in the chemical process."
- introduction: `In the process` — "In the process of chemical production, some key variables (e.g., reaction rate, reactant concentration) need to be detected in time."
- method: `This paper intends` — "This paper intends to combine the tri-training strategy with the vine copula regression model for soft sensor modeling." (s.3)
- experiments: `In this section` — "In this section, a numerical example and an industrial example will be used to prove the effectiveness of the tri-training VCR method."
- conclusion: `In view of` — "In view of the fact that there are only a small number of labeled samples and a large number of unlabeled samples in some industrial processes, a semi-supervised soft sensor method based on vine copula regression and tri-training algorithm (tri-training VCR) is proposed in this paper."

## Gap transitions

- to address (abstract): "To address this problem, a semi-supervised soft sensor method based on vine copula regression and tri-training algorithm (tri-training VCR) is proposed in this paper."
- however (introduction): "However, due to technical limitations and economic factors, most of these variables are difficult to measure directly."
- however (introduction): "However, with the continuous development of industrial technology, the chemical process is becoming more and more complicated, so it is usually difficult to obtain an accurate mechanism model"
- to address (introduction): "To address this problem, Noh et al. [20] proposed a regression model based on copula in 2013."
- therefore (introduction): "Therefore, it is more suitable to use probabilistic models to model these data [16]."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "is proposed in this paper"; "a semi-supervised soft sensor method ... is proposed"
- demonstrate / causal / abstract: "A numerical example and an industrial example are used to demonstrate the effectiveness of the proposed method."
- prove / causal / experiments: "will be used to prove the effectiveness of the tri-training VCR method"
- indicate / associative / method: "When the variance of the predicted value is small, it indicates that the model can well describe the distribution near this sample"
- can / speculative / introduction, method: "which can be used to describe arbitrary probability distributions"; "the vine copula regression model can calculate the variance"

## Cross-section linkers

- introduction → method: "The rest of the paper is organized as follows. Section 2 describes the copula, vine copula, and vine copula regression method. Section 3 introduces the detailed steps of the proposed tri-training VCR method. A numerical example and an industrial example of the sulfur recovery unit are used to prove the effectiveness of tri-training VCR method in Section 4. Finally, Section 5 concludes this paper."
- method → experiments: 流程段落后 `4. Applications`
- experiments → conclusion: 工业例结果后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of the paper is organized as follows`
- R009 自称：`is proposed in this paper` / `The method proposed in this paper`
- R010 Applications 节承担 Experiments（数值 + 工业）。

## Candidate phrases

- `To address this problem, a ... method ... is proposed in this paper` (abstract)
- `In this paper, a ... method ... is proposed` (introduction)
- `The rest of the paper is organized as follows` (introduction)
- `This paper intends to combine` (method)
- `is proposed in this paper` (conclusion)

## House style

自称 `this paper` / `the method proposed in this paper` / `is proposed in this paper`。未见 `Here we`。`In this paper` 与 `this paper` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Soft sensor technology is an important solution for timely prediction of some difficult-to-measure variables in the chemical process.
- abstract: To address this problem, a semi-supervised soft sensor method based on vine copula regression and tri-training algorithm (tri-training VCR) is proposed in this paper.
- abstract: A numerical example and an industrial example are used to demonstrate the effectiveness of the proposed method.
- introduction: In the process of chemical production, some key variables (e.g., reaction rate, reactant concentration) need to be detected in time.
- introduction: However, due to technical limitations and economic factors, most of these variables are difficult to measure directly.
- introduction: Therefore, it is more suitable to use probabilistic models to model these data [16].
- introduction: In this paper, a semi-supervised soft sensor method based on vine copula regression and tri-training algorithm (tri-training VCR) is proposed.
- introduction: The rest of the paper is organized as follows. Section 2 describes the copula, vine copula, and vine copula regression method.
- method: This paper intends to combine the tri-training strategy with the vine copula regression model for soft sensor modeling.
- experiments: In this section, a numerical example and an industrial example will be used to prove the effectiveness of the tri-training VCR method.
- conclusion: In view of the fact that there are only a small number of labeled samples and a large number of unlabeled samples in some industrial processes, a semi-supervised soft sensor method based on vine copula regression and tri-training algorithm (tri-training VCR) is proposed in this paper.
