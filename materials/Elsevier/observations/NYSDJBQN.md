---
key: NYSDJBQN
title: "Capturing sequence similarity using local spatiotemporal manifold-regularized dynamic network for semi-supervised industrial quality prediction"
venue: "Control Engineering Practice"
doi: "10.1016/j.conengprac.2025.106374"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries` → `3. Methodology` → `4. Case study` → `5. Conclusion`。前置 `ARTICLE INFO` / `Keywords` 与 `ABSTRACT`。无独立 Related Work。`related_work=inlined`（Introduction 中段静态 data-driven、LSTM/Transformer、四类半监督动态模型与 MR/LMR/TSGR）。Introduction 末有编号贡献 `(1)` / `(2)` / `(3)` + 节序路标。Method 含 DADLnet、LSTMR、LSTMR-DADLnet 质量预测。Experiments 标题为 `4. Case study`（氧化铝溶出过程）。

## Openers

- abstract: `Due to the` — "Due to the dynamics and label-scarcity of most industrial processes, semi-supervised dynamic quality prediction models have gradually become a research hotspot."
- introduction: `In modern production` — "In modern production industries, quality variables are key indicators in explicitly describing the industrial operation status as well as product quality (Lei & Karimi, 2023; Meng et al., 2023)."
- method: `Although LSTM is` — "Although LSTM is highly skilled at capturing long-term dependencies, it is unable to pay more attention to some key input variables at different moments."
- experiments: `To evaluate the` — "To evaluate the performance of the developed LSTMR-DADLnet method, it is applied to predict the quality variable of an actual alumina digestion process."
- conclusion: `In this paper` — "In this paper, a new semi-supervised dynamic model, called LSTMR-DADLnet, was proposed to efficiently mine dynamic information with full utilization of unlabeled data for quality prediction."

## Gap transitions

- however (introduction): "However, due to the limitations of production processes, measurement technology, and economic cost, many quality variables, such as solid content, product concentration, and melt index, are hard or even impossible to be online measured through hardware sensors (Li et al., 2024; Zhou et al., 2021)."
- however (introduction): "However, a common problem in practice is that industrial processes exhibit inherently intricate dynamics due to complex physicochemical reactions, large-scale production facilities, and feedback control strategies."
- unfortunately (introduction): "Unfortunately, for the aforementioned methods, only labeled data from historical data can be used to directly guide the model training, and unlabeled data fails to be fully utilized."
- therefore (introduction): "Therefore, based on the existing research achievements of temporal sequence dynamic models, it is very necessary to develop a semi-supervised dynamic quality prediction framework to make full use of labeled and unlabeled data."
- although (introduction): "Although these methods make up for the defect that unlabeled data cannot be fully utilized, their computational burden is heavy when facing complex industrial processes with a large amount of data, which is not cost-effective."
- however (method): "However, this is not always hold due to the dynamic nature of the process industry, where the current outputs are not only related to the current inputs, but also to the past inputs."

## Hedge verbs

- proposes / causal / abstract: "To deal with these issues, this study proposes a new local spatiotemporal manifold regularization (LSTMR) method."
- is proposed / causal / introduction: "Aiming at the aforementioned problems, a new semi-supervised dynamic model, referred to as local spatiotemporal manifold regularization assisted dual-attention dynamic learning network (LSTMR-DADLnet), is proposed to capture dynamic information and achieve quality prediction with full utilization of all available data, including both labeled samples and unlabeled samples."
- exhibit / associative / abstract: "The applications to an actual alumina digestion process exhibit the superiority of LSTMR-DADLnet."
- prove / associative / introduction: "The applications to an actual alumina digestion process are carried out, and the experimental results prove the superiority of the proposed algorithm in terms of prediction precision and computational efficiency."
- verified / associative / conclusion: "Extensive experiments on an actual alumina digestion process verified the superiority of LSTMR-DADLnet in both prediction precision and computational efficiency."
- may / hedge / conclusion: "Facing the limitations of the proposed method in dealing with new test data with shifted underlying causality, future work will integrate online learning frameworks (e.g., dynamic Bayesian networks or adaptive neural architectures) to handle evolving causality."

## Cross-section linkers

- introduction → preliminaries: "The remainder of this paper is organized as follows: Section 2 provides the preliminaries of MR and serialization of semi-supervised data."
- preliminaries → method: "The detailed construction of LSTMR-DADLnet is given in Section 3."
- method → experiments: "Section 4 presents the experimental verification in an actual alumina digestion process."
- experiments → conclusion: "Finally, conclusion is given in Section 5."

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remainder of this paper is organized as follows`
- R004 编号贡献：`The main contributions of LSTMR-DADLnet includes the following three aspects:`
- R009 自称：`this study proposes` / `is proposed` / `In this paper, a new ... was proposed`

## Candidate phrases

- `To deal with these issues, this study proposes a new local spatiotemporal manifold regularization (LSTMR) method.` (abstract)
- `The main contributions of LSTMR-DADLnet includes the following three aspects:` (introduction)
- `The remainder of this paper is organized as follows:` (introduction)
- `To evaluate the performance of the developed LSTMR-DADLnet method, it is applied to predict the quality variable of an actual alumina digestion process.` (experiments)
- `In this paper, a new semi-supervised dynamic model, called LSTMR-DADLnet, was proposed` (conclusion)

## House style

自称 `this study proposes` / `is proposed` / `In this paper, a new ... was proposed`。第三人称与 `this study` / `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Due to the dynamics and label-scarcity of most industrial processes, semi-supervised dynamic quality prediction models have gradually become a research hotspot.
- abstract: To deal with these issues, this study proposes a new local spatiotemporal manifold regularization (LSTMR) method.
- abstract: The applications to an actual alumina digestion process exhibit the superiority of LSTMR-DADLnet.
- introduction: In modern production industries, quality variables are key indicators in explicitly describing the industrial operation status as well as product quality (Lei & Karimi, 2023; Meng et al., 2023).
- introduction: Unfortunately, for the aforementioned methods, only labeled data from historical data can be used to directly guide the model training, and unlabeled data fails to be fully utilized.
- introduction: The remainder of this paper is organized as follows: Section 2 provides the preliminaries of MR and serialization of semi-supervised data.
- method: Although LSTM is highly skilled at capturing long-term dependencies, it is unable to pay more attention to some key input variables at different moments.
- experiments: To evaluate the performance of the developed LSTMR-DADLnet method, it is applied to predict the quality variable of an actual alumina digestion process.
- experiments: By embedding spatiotemporal attention mechanisms and designing local spatiotemporal manifold regularization, the proposed LSTMR-DADLnet method effectively overcomes the problems of existing methods and achieves the best prediction results in this experiment.
- conclusion: In this paper, a new semi-supervised dynamic model, called LSTMR-DADLnet, was proposed to efficiently mine dynamic information with full utilization of unlabeled data for quality prediction.
- conclusion: Extensive experiments on an actual alumina digestion process verified the superiority of LSTMR-DADLnet in both prediction precision and computational efficiency.
