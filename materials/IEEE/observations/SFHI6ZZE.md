---
key: SFHI6ZZE
title: "Heat Equation Stein Variational Ensemble: Rethinking and Advancing Uncertainty-Aware Soft Sensor Modeling"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3438277"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → `IV. EXPERIMENTS IN REAL INDUSTRIAL PROCESS` → `V. CAPABILITY OF UNCERTAINTY DECOMPOSITION: AN ILLUSTRATIVE NUMERICAL EXAMPLE` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SPLVM、uncertainty propagation、Bayesian networks、MC dropout、SGVI-BNN）。无 `The rest of this article is organized`。贡献列表在 Introduction 末，标 `In conclusion, the primary contributions of this article are as follows`。Experiments 标题为 `EXPERIMENTS IN REAL INDUSTRIAL PROCESS`；另有数值分解节 `V`。

## Openers

- abstract: `Data-driven soft` — "Data-driven soft sensors have been prevalent in industrial key performance indicator prediction." (p.1)
- introduction: `ACCURATE key performance` — "ACCURATE key performance indicator (KPI) prediction is crucial for modern industrial systems, particularly in the realms of operational optimization, product quality assurance, and energy consumption estimation." (p.1)
- method: `In this section` — "In this section, a novel method termed HESVE endowing data-driven soft sensors with the advanced ability of UQ is proposed." (p.4, III.B)
- experiments: `In this section` — "In this section, the blast furnace (BF) ironmaking process[37] is employed as a real-world case study to demonstrate the superiority of HESVE against the baselines." (p.5)
- conclusion: `In this work` — "In this work, an advanced uncertainty-aware soft sensor method called HESVE was proposed, which is motivated by the rethink of uncertainty-aware soft sensors under a Bayesian perspective." (p.8)

## Gap transitions

- however (abstract): "However, rigorously quantifying the uncertainty of predictions has been consistently neglected." (p.1)
- to bridge (abstract): "To bridge this gap, this study interprets uncertainty quantification (UQ) from a Bayesian perspective, which conceptualizes model uncertainty as the parameter distribution, thus distinguishing it from data uncertainty." (p.1)
- however (introduction): "However, the real world where they operate is dynamic due to numerous factors, such as catalysis deactivation, raw material changes, equipment degradation, etc." (p.1)
- therefore (introduction): "Therefore, it is necessary to formally investigate uncertainty-aware soft sensors [21], where the models should be proficient in both accurate point predictions and reliable predictive uncertainty quantification (UQ)." (p.2)

## Hedge verbs

- interpret / causal / abstract: "this study interprets uncertainty quantification (UQ) from a Bayesian perspective"
- propose / causal / abstract, method, conclusion: "a novel UQ method, heat equation stein variational ensemble (HESVE), is proposed"; "a novel method termed HESVE ... is proposed"; "HESVE was proposed"
- demonstrate / causal / abstract, conclusion: "Experiments demonstrate the superiority of HESVE"; "Experiments demonstrated that HESVE provides better accuracy"
- intend / speculative / introduction: "this work intends to advance uncertainty-aware soft sensors"
- will concentrate / speculative / conclusion: "Future work will concentrate on these aspects"

## Cross-section linkers

- introduction → preliminaries: 贡献列表后直接 `II. PRELIMINARIES`，无节序路标 (p.2)
- method → experiments: Algorithm 1 与校准说明后 `IV. EXPERIMENTS IN REAL INDUSTRIAL PROCESS` (p.5)
- experiments → numerical: 消融表后 `V. CAPABILITY OF UNCERTAINTY DECOMPOSITION` (p.8)
- numerical → conclusion: 分解图后 `VI. CONCLUSION` (p.8)

## Candidate rules

- R002 Introduction 无独立 Related Work，UQ 方法评述写在引言中段。
- R004 贡献列表用 `the primary contributions of this article are as follows`；引言末用 `In conclusion` 收束缺口。
- R010 无 `The rest of this article is organized`，贡献后直接进入 Preliminaries。
- R005 Conclusion 先收回方法，再用编号 `Future work will concentrate on these aspects`。

## Candidate phrases

- `To bridge this gap, this study interprets` (abstract)
- `a novel UQ method, ..., is proposed` (abstract)
- `In conclusion, the primary contributions of this article are as follows.` (introduction)
- `In this work, an advanced ... method called HESVE was proposed` (conclusion)
- `Future work will concentrate on these aspects:` (conclusion)

## House style

自称 `this study` / `this work` / `this article` / `our method` / `we present`。未见 `Here we`、`In this paper`。`this study interprets` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Data-driven soft sensors have been prevalent in industrial key performance indicator prediction.
- p.1 abstract: However, rigorously quantifying the uncertainty of predictions has been consistently neglected.
- p.1 abstract: To bridge this gap, this study interprets uncertainty quantification (UQ) from a Bayesian perspective, which conceptualizes model uncertainty as the parameter distribution, thus distinguishing it from data uncertainty.
- p.1 abstract: Based on this interpretation, a novel UQ method, heat equation stein variational ensemble (HESVE), is proposed.
- p.1 abstract: Experiments demonstrate the superiority of HESVE in multiple aspects compared to other state-of-the-art methods.
- p.1 introduction: ACCURATE key performance indicator (KPI) prediction is crucial for modern industrial systems, particularly in the realms of operational optimization, product quality assurance, and energy consumption estimation.
- p.1 introduction: However, the real world where they operate is dynamic due to numerous factors, such as catalysis deactivation, raw material changes, equipment degradation, etc.
- p.2 introduction: Therefore, it is necessary to formally investigate uncertainty-aware soft sensors [21], where the models should be proficient in both accurate point predictions and reliable predictive uncertainty quantification (UQ).
- p.2 introduction: According to the identified gaps and challenges in uncertainty-aware soft sensor modeling, this work intends to advance uncertainty-aware soft sensors. In conclusion, the primary contributions of this article are as follows.
- p.4 method: In this section, a novel method termed HESVE endowing data-driven soft sensors with the advanced ability of UQ is proposed.
- p.5 experiments: In this section, the blast furnace (BF) ironmaking process[37] is employed as a real-world case study to demonstrate the superiority of HESVE against the baselines.
- p.8 conclusion: In this work, an advanced uncertainty-aware soft sensor method called HESVE was proposed, which is motivated by the rethink of uncertainty-aware soft sensors under a Bayesian perspective.
- p.8 conclusion: Experiments demonstrated that HESVE provides better accuracy and uncertainty quality in predictions.
- p.8 conclusion: Future work will concentrate on these aspects: 1) investigating the out-of-distribution performance from theoretical and empirical standpoints, 2) utilizing the estimated uncertainty to facilitate modeling, and 3) validating or improving our method with larger models to further demonstrate the robustness and applicability of our method across various model complexities.
