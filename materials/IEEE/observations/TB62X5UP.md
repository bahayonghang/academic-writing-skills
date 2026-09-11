---
key: TB62X5UP
title: "Semi-Supervised Incremental Soft Sensor Model With Spatiotemporal Graph Regularization for Process Industry"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3500040"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-5,7-8,10-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM DESCRIPTION` → `III. IRRNN MODEL` → `IV. SS-IRRNN WITH SPATIOTEMPORAL GRAPH REGULARIZATION` → `V. PERFORMANCE EVALUATIONS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SSL RVFLN / weighted Gaussian / BLSM / LPSCN / GLSCN / ESN / SSESN / TSG-SSESN）。Introduction 末有 `This article is structured as follows`，指向 Section II–VI。Method 在 III–IV。Experiments 标题为 `PERFORMANCE EVALUATIONS`（数值仿真 + 赤铁矿磨矿粒径）。

## Openers

- abstract: `In some process` — "In some process industries, process variables are readily measurable, whereas real-time detection of industrial indices poses challenges." (p.1)
- introduction: `THE measurement of` — "THE measurement of process industries holds significant importance for enterprises, facilitating quality control, cost reduction, enhancing production efficiency, managing risks, and promoting sustainable development [1], [2], [3]." (p.1；栏首掉字)
- method: `In this section` — "In this section, we introduce the preliminaries, fundamental principles, and learning algorithms of IRRNN." (p.2, III)
- method: `In this section` — "In this section, we first introduce the SS-IRRNN and subsequently propose the SGSS-IRRNN." (p.4, IV)
- experiments: `In this section` — "In this section, we validate our proposed methods, SS-IRRNN and SGSS-IRRNN, through three numerical simulations, specifically modeling a nonlinear dynamical system and predicting chaotic time-series data from the Lorenz and Mackey–Glass (MG) systems." (p.7, V)
- conclusion: `This article proposes` — "This article proposes two soft sensing modeling methods for incomplete data in process industries as follows: SS-IRRNN and SGSS-IRRNN." (p.13)

## Gap transitions

- however (introduction): "However, in numerous industrial processes, such as sewage treatment plant discharge indices [4], harmful gas content in incinerators [5], mineral particle size (PS) during grinding [6], and distillation compositions [7], the operation indices are acquired through laboratory analysis, which is time-consuming." (p.1)
- however (introduction): "However, both methods have notable limitations: the first discards valuable unlabeled data, while the second relies on pseudosamples for modeling." (p.1)
- in summary (introduction): "In summary, while semi-supervised methods demonstrate outstanding performance in soft sensor modeling, they also exhibit two main limitations as follows: 1) most rely on forward neural network models, which are unable to capture temporal dependencies and 2) they lack the ability to automatically construct networks, requiring manual network structure configuration." (p.2)
- while (conclusion): "While the SS-IRRNN and SGSS-IRRNN exhibit promising performance, several key aspects require attention for future work." (p.13)

## Hedge verbs

- introduce / causal / abstract, introduction: "This article introduces an incremental random recurrent neural network (IRRNN)"; "the semi-supervised IRRNN (SS-IRRNN) ... is introduced"
- propose / causal / abstract, introduction, conclusion: "a semi-supervised IRRNN (SS-IRRNN) approach for soft sensor modeling is proposed"; "This article proposes two soft sensing modeling methods"
- demonstrate / causal / abstract, experiments: "demonstrate that the proposed methods exhibit sound performance"; "we validate our proposed methods"
- exhibit / causal / abstract, conclusion: "the proposed methods exhibit sound performance"; "our methods maintain excellent modeling performance"

## Cross-section linkers

- introduction → method: "This article is structured as follows. Section II outlines the semi-supervised modeling problem. Section III introduces the fundamental principles of IRRNN. Section IV presents the proposed soft sensor modeling methods, namely, SS-IRRNN and SGSS-IRRNN. Section V discusses the experimental results. Section VI concludes this article." (p.2)
- method → experiments: Algorithm 1 与 Fig. 5 后 `V. PERFORMANCE EVALUATIONS` (p.7)
- experiments → conclusion: Discussion 三段后 `VI. CONCLUSION` (p.13)

## Candidate rules

- R001 abstract 贡献句用 `This article introduces` + 方法缩写，随后 `is proposed`。
- R002 Introduction 无独立 Related Work，已有 SSL / ESN 评述写在引言中段，用 `In summary, ... two main limitations as follows` 收口。
- R003 Introduction 末用 `This article is structured as follows` 指向 II–VI。
- R004 贡献用 `Our contributions encompass four main aspects.` + 编号列表，每条以 `is proposed` / `is introduced` 收尾。
- R005 Conclusion 先收回两方法，再用 `While ... exhibit promising performance` 承认局限，指向 hyperparameter 与 online learning。

## Candidate phrases

- `This article introduces an incremental random recurrent neural network (IRRNN) that` (abstract)
- `Based on the IRRNN, a semi-supervised IRRNN (SS-IRRNN) approach for soft sensor modeling is proposed.` (abstract)
- `In this article, our aim is to design a semi-supervised soft sensor model for` (problem)
- `This article is structured as follows.` (introduction)
- `This article proposes two soft sensing modeling methods for incomplete data in process industries as follows:` (conclusion)

## House style

自称是 `This article` / `this article` / `In this article` / `we propose` / `our methods`。未见 `Here we`、`In this paper`。`This article introduces` 与 `This article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In some process industries, process variables are readily measurable, whereas real-time detection of industrial indices poses challenges.
- p.1 abstract: This article introduces an incremental random recurrent neural network (IRRNN) that combines incremental architecture construction with random weights.
- p.1 abstract: Based on the IRRNN, a semi-supervised IRRNN (SS-IRRNN) approach for soft sensor modeling is proposed.
- p.1 abstract: Numerical simulation experiments and soft sensing experiments on hematite grinding processes demonstrate that the proposed methods exhibit sound performance when dealing with incomplete datasets.
- p.1 introduction: THE measurement of process industries holds significant importance for enterprises, facilitating quality control, cost reduction, enhancing production efficiency, managing risks, and promoting sustainable development [1], [2], [3].
- p.1 introduction: However, in numerous industrial processes, such as sewage treatment plant discharge indices [4], harmful gas content in incinerators [5], mineral particle size (PS) during grinding [6], and distillation compositions [7], the operation indices are acquired through laboratory analysis, which is time-consuming.
- p.1 introduction: However, both methods have notable limitations: the first discards valuable unlabeled data, while the second relies on pseudosamples for modeling.
- p.2 introduction: In summary, while semi-supervised methods demonstrate outstanding performance in soft sensor modeling, they also exhibit two main limitations as follows: 1) most rely on forward neural network models, which are unable to capture temporal dependencies and 2) they lack the ability to automatically construct networks, requiring manual network structure configuration.
- p.2 introduction: Our contributions encompass four main aspects.
- p.2 introduction: This article is structured as follows. Section II outlines the semi-supervised modeling problem. Section III introduces the fundamental principles of IRRNN. Section IV presents the proposed soft sensor modeling methods, namely, SS-IRRNN and SGSS-IRRNN. Section V discusses the experimental results. Section VI concludes this article.
- p.2 problem: In this article, our aim is to design a semi-supervised soft sensor model for process industries with incomplete data {XU ∪ XL, Y }.
- p.2 method: In this section, we introduce the preliminaries, fundamental principles, and learning algorithms of IRRNN.
- p.4 method: In this section, we first introduce the SS-IRRNN and subsequently propose the SGSS-IRRNN.
- p.7 experiments: In this section, we validate our proposed methods, SS-IRRNN and SGSS-IRRNN, through three numerical simulations, specifically modeling a nonlinear dynamical system and predicting chaotic time-series data from the Lorenz and Mackey–Glass (MG) systems.
- p.13 conclusion: This article proposes two soft sensing modeling methods for incomplete data in process industries as follows: SS-IRRNN and SGSS-IRRNN.
- p.13 conclusion: The experiments demonstrate that our methods maintain excellent modeling performance, even when labeled samples constitute only 3% of the overall sample set.
- p.13 conclusion: While the SS-IRRNN and SGSS-IRRNN exhibit promising performance, several key aspects require attention for future work.
