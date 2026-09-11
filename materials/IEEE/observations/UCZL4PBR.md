---
key: UCZL4PBR
title: "Inverse Gaussian Process Modeling for Evolutionary Dynamic Multiobjective Optimization"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2021.3070434"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,11-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES AND BACKGROUND` → `III. PROPOSED ALGORITHM` → `IV. EXPERIMENTAL DESIGN` → `V` 实验结果 → `VI` 结论。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（并入 `II. PRELIMINARIES AND BACKGROUND`：问题定义、逆建模、IGP、DMOEA 综述）。`related_work=independent`。Introduction 末有 `The remainder of this article is organized as follows` 路标，指向 Section II–VI。Method 分 IGP 预测器、算法框架、复杂度。Experiments 拆成 design（IV）与 results（V），含 23 个基准与选矿原矿分配。

## Openers

- abstract: `For dynamic multiobjective` — "For dynamic multiobjective optimization problems (DMOPs), it is challenging to track the varying Pareto-optimal front." (p.1)
- introduction: `MANY real-world` — "MANY real-world multiobjective optimization problems (MOPs) involve simultaneous optimization of several time-varying objective functions and/or constraints." (p.1；栏首掉字)
- method: `The details of` — "The details of the proposed algorithm, IGP-DMOEA, are presented in this section." (p.5, III)
- experiments: `This section introduces` — "This section introduces the experimental problems, compared algorithms, performance metrics, and parameter settings used in the experimental studies of this article." (p.6, IV)
- conclusion: `The proposed method` — "The proposed method helps to solve the WIFNWIN problem." (p.12)

## Gap transitions

- however (abstract): "However, the obtained solutions do not necessarily satisfy the desired properties of decision makers in the objective space." (p.1)
- nonetheless (abstract): "Nonetheless, the existing ones have low precision for handling DMOPs with nonlinear correlations between the objective and decision vectors, which greatly limits the application of the inverse models." (p.1)
- unlike (abstract): "Unlike most traditional approaches, this approach exploits the IGP to construct a predictor that maps the historical optimal solutions from the objective space to the decision space." (p.1)
- note that (introduction): "Note that the solutions obtained by traditional approaches do not necessarily meet the desired properties of decision makers in the objective space." (p.1)
- however (background): "However, simple linear inverse models are employed due to their low computational cost." (p.3)
- motivated by (background): "Motivated by the above, an IGP modeling-based prediction approach is proposed to solve a wide range of DMOPs." (p.5)
- although (conclusion): "Although the IGP-DMOEA achieved promising performance for the test instances considered in this article, there are still several issues to be explored in future work." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "an inverse Gaussian process (IGP)-based prediction approach for solving DMOPs is proposed"; "an inverse Gaussian process (IGP) modeling-based prediction approach is proposed"
- demonstrate / causal / abstract: "The experimental results demonstrate that the proposed algorithm can significantly improve the dynamic optimization performance"
- can obtain / causal / abstract: "The proposed method by introducing IGP can obtain solutions with better diversity and convergence"
- exhibit / causal / introduction: "The experimental results exhibit that the proposed algorithm can greatly enhance the quality of the solutions"
- could focus / speculative / conclusion: "Future work could focus on developing strategies to exploit the time-series solutions"

## Cross-section linkers

- introduction → background: "The remainder of this article is organized as follows. In Section II, background information on the DMOPs is first introduced, followed by a review of the existing literature on inverse models and DMOEAs. In addition, the idea of an IGP is also described. Section III presents an elaborate description of the proposed algorithm, that is, the IGP modeling-based dynamic multiobjective evolutionary optimization algorithm (IGP-DMOEA). Section IV provides the experimental designs, including the experimental problems, compared algorithms, performance metrics, and parameter settings. The experimental results and analyses are presented in Section V. Finally, Section VI draws a conclusion and outlines the future work." (p.2)
- background → method: 综述收口后 `III. PROPOSED ALGORITHM` (p.5)
- method → experiments: 复杂度段落后 `IV. EXPERIMENTAL DESIGN` (p.6)
- experiments → conclusion: 结果分析后进入结论段 (p.11–12)

## Candidate rules

- R001 abstract 用 `Unlike most traditional approaches, this approach exploits` 对比决策空间预测。
- R002 独立 `PRELIMINARIES AND BACKGROUND`，含定义、逆建模与 DMOEA 综述。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The major contributions of this article are as follows:` 叙述句，不用编号列表。
- R005 Conclusion 用 `Although the [NAME] achieved promising performance` 承认局限，再用 `Future work could focus on`。

## Candidate phrases

- `Unlike most traditional approaches, this approach exploits the IGP to construct a predictor that` (abstract)
- `The major contributions of this article are as follows:` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `Motivated by the above, an IGP modeling-based prediction approach is proposed to` (background)
- `Although the IGP-DMOEA achieved promising performance for the test instances considered in this article, there are still several issues to be explored in future work.` (conclusion)

## House style

自称 `this article` / `In this article` / `the proposed approach` / `the proposed method` / `we propose`。未见 `Here we`、`In this paper`。`In this article … is proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: For dynamic multiobjective optimization problems (DMOPs), it is challenging to track the varying Pareto-optimal front.
- p.1 abstract: However, the obtained solutions do not necessarily satisfy the desired properties of decision makers in the objective space.
- p.1 abstract: Nonetheless, the existing ones have low precision for handling DMOPs with nonlinear correlations between the objective and decision vectors, which greatly limits the application of the inverse models.
- p.1 abstract: In this article, an inverse Gaussian process (IGP)-based prediction approach for solving DMOPs is proposed.
- p.1 abstract: Unlike most traditional approaches, this approach exploits the IGP to construct a predictor that maps the historical optimal solutions from the objective space to the decision space.
- p.1 abstract: The experimental results demonstrate that the proposed algorithm can significantly improve the dynamic optimization performance and has certain practical significance for solving real-world DMOPs.
- p.1 introduction: MANY real-world multiobjective optimization problems (MOPs) involve simultaneous optimization of several time-varying objective functions and/or constraints.
- p.1 introduction: Note that the solutions obtained by traditional approaches do not necessarily meet the desired properties of decision makers in the objective space.
- p.2 introduction: The major contributions of this article are as follows: first, the proposed method solves the WIFNWIN problem more effectively than traditional DMOEAs, so that the obtained solutions can better meet the demand of decision makers.
- p.2 introduction: The remainder of this article is organized as follows. In Section II, background information on the DMOPs is first introduced, followed by a review of the existing literature on inverse models and DMOEAs.
- p.5 background: Motivated by the above, an IGP modeling-based prediction approach is proposed to solve a wide range of DMOPs.
- p.5 method: The details of the proposed algorithm, IGP-DMOEA, are presented in this section.
- p.6 experiments: This section introduces the experimental problems, compared algorithms, performance metrics, and parameter settings used in the experimental studies of this article.
- p.12 conclusion: The proposed method helps to solve the WIFNWIN problem.
- p.12 conclusion: Therefore, the obtained solutions are more responsive to the demand of decision makers than traditional methods.
- p.12 conclusion: The IGP-DMOEA is compared with several recent DMOEAs for 23 benchmark problems with different dynamic characteristics and a real-world dynamic ROA optimization problem in mineral processing.
- p.12 conclusion: Although the IGP-DMOEA achieved promising performance for the test instances considered in this article, there are still several issues to be explored in future work.
- p.12 conclusion: Future work could focus on developing strategies to exploit the time-series solutions gained in several sequential environments.
