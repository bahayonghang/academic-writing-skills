---
key: 5GBFPUF4
title: "Self-Modified Dynamic Domain Adaptation for Industrial Soft Sensing"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2026.3663257"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`，分 DA for soft sensors 与 dynamic DA）。`related_work=independent`。Introduction 末有 `The rest of the article is organized as follows` 路标，指向 II–V。Method 在 III。Experiments 标题为 `CASE STUDY`（两个氨合成工业案例）。

## Openers

- abstract: `Data-driven soft sensors` — "Data-driven soft sensors have been widely applied to estimating important yet difficult-to-measure quality-relevant variables in industrial processes." (p.1)
- introduction: `THE significant improvement` — "THE significant improvement in data monitoring and product production efficiency is attributed to the development of advanced monitoring and control optimization technologies." (p.1)
- method: `In this section` — "In this section, we present the proposed method in detail." (p.3, III)
- experiments: `In this section` — "In this section, we evaluate the performance of the proposed SDDA framework using two real-world industrial cases from the ammonia synthesis process (ASP) [44]." (p.7, IV)
- conclusion: `In this paper` — "In this paper, we propose a novel dynamic domain adaptation soft sensing model based on the self-modified mechanism and a feature alignment module." (p.12)

## Gap transitions

- however (introduction): "However, product quality effectively monitoring in the chemical industry faces challenges because of rapid changes in working conditions [1], [2] and the high costs and delays associated with online monitoring data [3]." (p.1)
- however (introduction): "In practical industrial processes, however, factors such as variation in the operating environment and sensor degradation [17] can result in distribution discrepancy among domains [18]." (p.2)
- however (introduction): "To the best of our knowledge, however, most of the classic domain adaptation methods do not consider the dynamic auto-correlations embedded in the industrial processes." (p.2)
- however (related work): "However, most of them are developed based on static models and do not take the potential dynamic characteristics into account in industrial processes." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a Self-modified Dynamic Domain Adaptation (SDDA) soft sensor approach"; "In this paper, we propose a novel dynamic domain adaptation soft sensing model"
- demonstrate / causal / abstract, introduction: "We demonstrate the superiority of the proposed method via two real-world industrial cases"; "Demonstrate the superiority and feasibility of the proposed method"
- develop / causal / abstract: "We develop a novel sequential optimization framework"
- show / causal / experiments: "Fig. 7 presents the pointwise predictions"

## Cross-section linkers

- introduction → related work: "The rest of the article is organized as follows: Section II briefly describes data-driven soft sensors and domain adaptation. Section III describes the Self-modified Mechanism and correlative algorithms and the strategy of feature alignment. Section IV shows the results of SDDA application in two practical industrial cases. Finally, we summarize the above work in Section V." (p.2)
- related work → method: TDLVR 局限评述后接 `III. METHODOLOGY` (p.3)
- method → experiments: Algorithm 2 后接 `IV. CASE STUDY` (p.7)
- experiments → conclusion: 敏感性分析后直接 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `In this work, we propose` / `We demonstrate the superiority`，不用 `Here we`。
- R002 TASE 前置 `Note to Practitioners`。
- R003 独立 Related Work；Introduction 末用 `The rest of the article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this article are reflected below:` + 编号列表。
- R005 Experiments 标题为 `CASE STUDY`。
- R006 Conclusion 用 `In this paper, we propose` 收回。

## Candidate phrases

- `In this work, we propose a Self-modified Dynamic Domain Adaptation (SDDA) soft sensor approach` (abstract)
- `We demonstrate the superiority of the proposed method via two real-world industrial cases.` (abstract)
- `The main contributions of this article are reflected below:` (introduction)
- `The rest of the article is organized as follows:` (introduction)
- `In this paper, we propose a novel dynamic domain adaptation soft sensing model` (conclusion)

## House style

自称是 `In this work` / `we propose` / `this article` / `In this paper` / `the proposed method`。未见 `Here we`。`In this work, we propose` 与 `In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Data-driven soft sensors have been widely applied to estimating important yet difficult-to-measure quality-relevant variables in industrial processes.
- p.1 abstract: Existing soft sensor approaches pay little attention to the combined challenge of distribution discrepancy and dynamic feature transfer, referred to as the dynamic domain adaptation challenge.
- p.1 abstract: In this work, we propose a Self-modified Dynamic Domain Adaptation (SDDA) soft sensor approach to solve this problem.
- p.1 abstract: We demonstrate the superiority of the proposed method via two real-world industrial cases.
- p.1 introduction: THE significant improvement in data monitoring and product production efficiency is attributed to the development of advanced monitoring and control optimization technologies.
- p.1 introduction: However, product quality effectively monitoring in the chemical industry faces challenges because of rapid changes in working conditions [1], [2] and the high costs and delays associated with online monitoring data [3].
- p.2 introduction: In practical industrial processes, however, factors such as variation in the operating environment and sensor degradation [17] can result in distribution discrepancy among domains [18].
- p.2 introduction: To the best of our knowledge, however, most of the classic domain adaptation methods do not consider the dynamic auto-correlations embedded in the industrial processes.
- p.2 introduction: The main contributions of this article are reflected below:
- p.2 introduction: The rest of the article is organized as follows: Section II briefly describes data-driven soft sensors and domain adaptation. Section III describes the Self-modified Mechanism and correlative algorithms and the strategy of feature alignment. Section IV shows the results of SDDA application in two practical industrial cases. Finally, we summarize the above work in Section V.
- p.3 related work: However, most of them are developed based on static models and do not take the potential dynamic characteristics into account in industrial processes.
- p.3 method: In this section, we present the proposed method in detail.
- p.7 experiments: In this section, we evaluate the performance of the proposed SDDA framework using two real-world industrial cases from the ammonia synthesis process (ASP) [44].
- p.12 conclusion: In this paper, we propose a novel dynamic domain adaptation soft sensing model based on the self-modified mechanism and a feature alignment module.
- p.12 conclusion: We demonstrate the effectiveness and superiority of the proposed method in two real industrial cases.
