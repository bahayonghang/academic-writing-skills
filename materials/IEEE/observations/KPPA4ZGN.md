---
key: KPPA4ZGN
title: "Data-Knowledge-Driven Multiobjective Integrated Optimal Control for Nonlinear Systems"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2024.3443996"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. DATA-KNOWLEDGE-DRIVEN MULTIOBJECTIVE INTEGRATED OPTIMAL CONTROL FOR NONLINEAR SYSTEMS` → `IV. CONVERGENCE AND STABILITY ANALYSIS` → `V. EXPERIMENTAL STUDIES` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评单目标最优控制 / MOC / 数据驱动 MIOC / 迁移学习）。Introduction 末有节序路标，指向 Section II–VI。Method 在 III。Experiments 标题为 `EXPERIMENTAL STUDIES`（非线性系统 + WWTP）。

## Openers

- abstract: `Multiobjective optimal control` — "Multiobjective optimal control (MOC) optimize multiple performance indices of nonlinear systems to obtain setpoints, and design the controller to track the setpoints." (p.6789)
- introduction: `OPTIMAL control, with` — "OPTIMAL control, with the main goal of optimizing operation performance, is a highly effective control strategy that has widespread use in nonlinear systems [1], [2], [3]." (p.6789；栏首掉字)
- method: `The subsequent sections` — "The subsequent sections provide a comprehensive overview of the technical aspects pertaining to DK-MIOC." (p.6791, III)
- experiments: `To demonstrate the` — "To demonstrate the availability of DK-MIOC, its performance is evaluated in both a benchmark example and WWTP." (p.6795, V)
- conclusion: `To address the` — "To address the challenge of insufficient data in nonlinear systems, a novel approach named DK-MIOC was introduced in this article, which integrated optimization and control techniques." (p.6799)

## Gap transitions

- however (abstract): "However, if the feasibility of the controller is not considered, untraceable setpoints may be obtained." (p.6789)
- to address (abstract): "To address this problem, a data-knowledge-driven multiobjective integrated optimal control (DK-MIOC) method is proposed in this article." (p.6789)
- however (introduction): "However, aforementioned optimal control strategies are optimized for a single performance index." (p.6789)
- therefore (introduction): "Therefore, in the optimal control of nonlinear systems, multiple operational indices are taken into account to achieve a more comprehensive and satisfactory control performance [13], [14], [15]." (p.6789)
- however (introduction): "However, in actual industrial processes, the collection of data often encounters associated challenges, such as the limitations of hardware [27] and data pollution [28], which result in insufficient data" (p.6790)

## Hedge verbs

- propose / causal / abstract: "a data-knowledge-driven multiobjective integrated optimal control (DK-MIOC) method is proposed in this article"
- demonstrate / causal / introduction, experiments: "the availability of DK-MIOC is demonstrated through analyzing experimental results"; "Results demonstrate that DK-MIOC is enable to achieve superior system performance"
- show / causal / introduction, experiments: "Experiments in [25] and [26] showed that data-driven MIOC could achieve outstanding control and optimization performance"; "The results of ARC show that the average fluctuation amplitude of DK-MIOC is significantly lower"
- indicate / causal / experiments: "The above results indicate that in the situation of insufficient data, both MIOC and DMOPSO-OC have a larger fluctuation range compared to DK-MIOC."
- infer / speculative / experiments: "it can be inferred that DK-MIOC demonstrates a favorable EQ while simultaneously minimizing EC"

## Cross-section linkers

- introduction → method: "In this article, the remainder parts are arranged as below. The problem formulation of the MIOC framework is described in Section II. Section III gives the technical details of DK-MIOC. In Section IV, the convergence of DK-model and the stability of DK-MIOC are discussed. In Section V, the availability of DK-MIOC is demonstrated through analyzing experimental results. In Section VI, the conclusions of this article are summarized." (p.6790)
- method → analysis: 算法流程表后直接 `IV. CONVERGENCE AND STABILITY ANALYSIS` (p.6794)
- experiments → conclusion: Discussion 段落后直接 `VI. CONCLUSION` (p.6799)

## Candidate rules

- R001 abstract 用 `is proposed in this article`，再用 First / Then / Second / Third / Finally 铺开贡献。
- R002 Introduction 无独立 Related Work，单目标 → 多目标 → 集成最优控制 → 数据不足与迁移学习。
- R003 贡献列表前用 `this article presents the following major contributions.`
- R004 Introduction 末用 `the remainder parts are arranged as below` 指向 II–VI。
- R005 Conclusion 先收回框架/DK-model/COA，再用 `In the future, the implementation of DK-MIOC in real-world industrial operations will be taken into account.`

## Candidate phrases

- `a ... method is proposed in this article` (abstract)
- `To address this problem` (abstract)
- `this article presents the following major contributions.` (introduction)
- `In this article, the remainder parts are arranged as below.` (introduction)
- `a novel approach named DK-MIOC was introduced in this article` (conclusion)

## House style

自称是 `this article` / `is proposed in this article` / `DK-MIOC` / `the proposed DK-model`。未见 `Here we`。`this article` 与 `is proposed in this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.6789 abstract: Multiobjective optimal control (MOC) optimize multiple performance indices of nonlinear systems to obtain setpoints, and design the controller to track the setpoints.
- p.6789 abstract: However, if the feasibility of the controller is not considered, untraceable setpoints may be obtained.
- p.6789 abstract: To address this problem, a data-knowledge-driven multiobjective integrated optimal control (DK-MIOC) method is proposed in this article.
- p.6789 introduction: OPTIMAL control, with the main goal of optimizing operation performance, is a highly effective control strategy that has widespread use in nonlinear systems [1], [2], [3].
- p.6789 introduction: However, aforementioned optimal control strategies are optimized for a single performance index.
- p.6789 introduction: Therefore, in the optimal control of nonlinear systems, multiple operational indices are taken into account to achieve a more comprehensive and satisfactory control performance [13], [14], [15].
- p.6790 introduction: However, in actual industrial processes, the collection of data often encounters associated challenges, such as the limitations of hardware [27] and data pollution [28], which result in insufficient data for establishing predictive models and accurately forecasting future dynamics of systems [29].
- p.6790 introduction: According to the above discussions, a data-knowledge-driven MIOC (DK-MIOC) framework is developed.
- p.6790 introduction: To summarize, this article presents the following major contributions.
- p.6790 introduction: In this article, the remainder parts are arranged as below. The problem formulation of the MIOC framework is described in Section II. Section III gives the technical details of DK-MIOC. In Section IV, the convergence of DK-model and the stability of DK-MIOC are discussed. In Section V, the availability of DK-MIOC is demonstrated through analyzing experimental results. In Section VI, the conclusions of this article are summarized.
- p.6791 method: The subsequent sections provide a comprehensive overview of the technical aspects pertaining to DK-MIOC.
- p.6795 experiments: To demonstrate the availability of DK-MIOC, its performance is evaluated in both a benchmark example and WWTP.
- p.6796 experiments: The results indicated above suggest that the presence of insufficient data can have an impact on the search for setpoints, leading to significant fluctuations in the stepwise optimal control setpoints.
- p.6797 experiments: The above results indicate that in the situation of insufficient data, both MIOC and DMOPSO-OC have a larger fluctuation range compared to DK-MIOC.
- p.6799 conclusion: To address the challenge of insufficient data in nonlinear systems, a novel approach named DK-MIOC was introduced in this article, which integrated optimization and control techniques.
- p.6799 conclusion: Results demonstrate that DK-MIOC is enable to achieve superior system performance even with limited data.
- p.6799 conclusion: In the future, the implementation of DK-MIOC in real-world industrial operations will be taken into account.
