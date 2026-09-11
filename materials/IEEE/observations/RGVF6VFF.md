---
key: RGVF6VFF
title: "Formulas for Data-Driven Control: Stabilization, Optimality, and Robustness"
venue: "IEEE Transactions on Automatic Control"
doi: "10.1109/TAC.2019.2959924"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PERSISTENCE OF EXCITATION AND WILLEMS et al.’s FUNDAMENTAL LEMMA` → `III. DATA-BASED SYSTEM REPRESENTATIONS` → `IV. DATA-DRIVEN CONTROL DESIGN: STABILIZATION AND OPTIMAL CONTROL` → `V.`（噪声与非线性平衡点，Introduction 已预告 Theorem 5–6）→ `VI.`（输出反馈，Theorem 8）→ `VII. DISCUSSION AND CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work 节。`related_work=inlined`（Introduction 小节 `A. Literature Review` 评 Ziegler–Nichols / adaptive / unfalsified / IFT / VRFT）。Introduction 末有节序路标，指向 Section IV–VII。数值例子嵌在 Theorem 后（batch reactor），无独立 Experiments 节。

## Openers

- abstract: `In a paper` — "In a paper by Willems et al., it was shown that persistently exciting data can be used to represent the input–output behavior of a linear system." (p.1)
- introduction: `LEARNING from data` — "LEARNING from data is essential to every area of science." (p.1；栏首掉字)
- method: `In this section` — "In this section, we revisit the main result in [27] and state a few auxiliary results inspired by subspace identification [2], which will be useful throughout the article." (p.3, II)
- experiments: `As an illustrative` — "As an illustrative example, consider the discretized version of a batch reactor system [34] using a sampling time of 0.1 s" (p.5, IV.A)
- conclusion: `Persistently exciting data` — "Persistently exciting data enable the construction of data-dependent matrices that can replace systems models." (p.13)

## Gap transitions

- despite (introduction): "Despite many developments in this area, data-driven control is not yet well understood even if we restrict the attention to linear dynamics, which contrasts the achievements obtained in system identification." (p.1)
- however (method): "However, this approach is basically equivalent to a model-based approach where the system matrices A and B are first reconstructed using a collection of sample trajectories." (p.4)
- thus (method): "Thus, for design purposes, one can regard GK as a decision variable, and search for the matrix GK that guarantees stability and performance specifications." (p.4)

## Hedge verbs

- derive / causal / abstract: "we derive a parametrization of linear feedback systems that paves the way to solve important control problems using data-dependent linear matrix inequalities only."
- show / causal / abstract, introduction, conclusion: "We also discuss robustness to noise-corrupted measurements and show how the approach can be used to stabilize unstable equilibria of nonlinear systems."; "we have shown the existence of a parametrization of feedback control systems"
- discuss / causal / introduction: "We discuss this fact in Section IV."
- expect / speculative / conclusion: "we expect that our approach could lead to data-driven solutions to many other control problems."

## Cross-section linkers

- introduction → method: "Concluding remarks are given in Section VII." 随后 `II. PERSISTENCE OF EXCITATION AND WILLEMS et al.’s FUNDAMENTAL LEMMA` (p.2–3)
- method → design: "This result will be the key later on for deriving control design methods that avoid the need to identify a parametric model of the system to be controlled." 随后 `IV. DATA-DRIVEN CONTROL DESIGN` (p.3–4)
- design → conclusion: MIMO 推论后直接 `VII. DISCUSSION AND CONCLUSION` (p.13)

## Candidate rules

- R001 abstract 以经典引理开场，再用 `we derive` / `we solve` / `We also discuss`，不用 `Here we`。
- R002 Related Work 作为 Introduction 小节 `A. Literature Review`，不是独立罗马数字节。
- R003 Introduction 末用节号预告 Theorem / Section IV–VII，自称 `this article`。
- R004 数值例子写在定理后 `Illustrative example:`，不单列 Experiments。
- R005 Conclusion 标题为 `DISCUSSION AND CONCLUSION`，先收回范式，再用 `we expect` 指向后续 LMI 问题。

## Candidate phrases

- `Based on this fundamental result, we derive` (abstract)
- `In this article, we first revisit` (introduction)
- `Concluding remarks are given in Section VII.` (introduction)
- `As an illustrative example, consider` (experiments)
- `we expect that our approach could lead to` (conclusion)

## House style

自称是 `we derive` / `we discuss` / `In this article` / `this article` / `our approach`。未见 `Here we`。`In this article` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In a paper by Willems et al., it was shown that persistently exciting data can be used to represent the input–output behavior of a linear system.
- p.1 abstract: Based on this fundamental result, we derive a parametrization of linear feedback systems that paves the way to solve important control problems using data-dependent linear matrix inequalities only.
- p.1 abstract: The result is remarkable in that no explicit system’s matrices identification is required.
- p.1 abstract: We also discuss robustness to noise-corrupted measurements and show how the approach can be used to stabilize unstable equilibria of nonlinear systems.
- p.1 introduction: LEARNING from data is essential to every area of science.
- p.1 introduction: Despite many developments in this area, data-driven control is not yet well understood even if we restrict the attention to linear dynamics, which contrasts the achievements obtained in system identification.
- p.2 introduction: In this article, we first revisit Willems et al.’s fundamental lemma, originally cast in the behavioral framework, through classic state-space descriptions (see Lemma 2).
- p.2 introduction: Concluding remarks are given in Section VII.
- p.3 method: In this section, we revisit the main result in [27] and state a few auxiliary results inspired by subspace identification [2], which will be useful throughout the article.
- p.4 method: However, this approach is basically equivalent to a model-based approach where the system matrices A and B are first reconstructed using a collection of sample trajectories.
- p.5 experiments: As an illustrative example, consider the discretized version of a batch reactor system [34] using a sampling time of 0.1 s
- p.13 conclusion: Persistently exciting data enable the construction of data-dependent matrices that can replace systems models.
- p.13 conclusion: Since LMIs are ubiquitous in systems and control, we expect that our approach could lead to data-driven solutions to many other control problems.
- p.13 conclusion: A remarkable feature of all these results is that: 1) no parametric model of system is identified; 2) stability guarantees come with a finite (computable) number of data points.
