---
key: ALQGJ9U3
title: "Multiobjective Operation Optimization of Wastewater Treatment Process Based on Reinforcement Self-Learning and Knowledge Guidance"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2022.3164476"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,8-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION`（含 `A. Statement of Operation Optimization Problem in WWTP` / `B. Research Status and Problems of Operation Optimization Modeling in WWTP` / `C. Research Status and Problems of Operation Optimization Methods for WWTP` / `D. Main Works of This Article`）→ `II. OPERATION OPTIMIZATION MODELING METHOD` → `III. MULTIOBJECTIVE OPERATION OPTIMIZATION METHOD` → `IV. DATA EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction B–C 评 first-principles、离线数据驱动、单目标/NSGA-II/MOPSO）。Introduction D 给贡献列表；未见单独节序路标句，节序由 I.D 转入 II。

## Openers

- abstract: `This article proposes` — "This article proposes a multiobjective operation optimization method based on reinforcement self-learning and knowledge guidance for quality assurance and consumption reduction of wastewater treatment process (WWTP) with nonstationary time-varying dynamics." (p.6896)
- introduction: `WITH the development` — "WITH the development of urban modernization, the demand of industry, and daily life for water resources is increasing, leading to a sharp increase in industrial wastewater and domestic sewage." (p.6896；栏首掉字)
- method: `The first task to` — "The first task to realize the operation optimization of WWTP in this article is to develop simple but effective operation index models oriented to multiobjective optimization." (p.6899, II)
- experiments: `To verify the effectiveness` — "To verify the effectiveness and superiority of the proposed operation optimization method, several data experiments, and comparisons are performed on the platform of the international benchmark simulation model 1 (BSM1)." (p.6903, IV)
- conclusion: `Aiming at the problems` — "Aiming at the problems of high EC and EQ indices easily exceeding the limited standards in WWTP, this article proposes a novel multiobjective operation optimization method based on reinforcement self-learning and knowledge guidance for complicated industrial process with strong time-varying dynamics." (p.6907–6908)

## Gap transitions

- however (introduction): "However, if SO5 is too high, the anoxic environment for denitrification may be destroyed" (p.6897)
- however (introduction): "However, the WWTP is subject to strong nonstationary dynamics and time-varying working conditions" (p.6897)
- however (introduction): "However, the above single-objective optimization methods only focus on the reduction of EC, which easily leads to the exceedance of the EQ" (p.6897)
- however (introduction): "However, these conventional MOPSO algorithms usually require a large number of iterations and nondominated sorting operations, thus the computational complexity is large." (p.6898)
- therefore (introduction): "Therefore, it is urgent to realize the operation optimization and control of WWTP" (p.6896)
- moreover (conclusion): "Moreover, the proposed method also has good generalizable applicability." (p.6908)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "This article proposes a multiobjective operation optimization method"; "this article proposes a novel multiobjective operation optimization method"
- show / causal / abstract, experiments: "Data experiments show that the proposed method can effectively reduce energy consumption and ensure effluent quality."
- verify / causal / experiments: "To verify the effectiveness and superiority of the proposed operation optimization method"

## Cross-section linkers

- introduction → method: I.D 贡献列表第 4 条后直接 `II. OPERATION OPTIMIZATION MODELING METHOD` (p.6898–6899)
- method → experiments: 下层跟踪控制段落后接 `IV. DATA EXPERIMENTS` (p.6903)
- experiments → conclusion: Table IV 比较段落后接 `V. CONCLUSION` (p.6907)

## Candidate rules

- R001 Abstract 首句用 `This article proposes` + 方法名。
- R002 Introduction 用 A–D 子节把问题陈述、建模现状、优化现状与本文工作拆开，无独立 Related Work。
- R003 贡献写在 `D. Main Works of This Article`，用 `the superiorities of the proposed method are mainly reflected in the following several aspects.`
- R004 实验节标题用 `DATA EXPERIMENTS`，开篇绑定 BSM1 基准。
- R005 Conclusion 先收回方法，再用 `In the future, the authors will further research` 指向后续。

## Candidate phrases

- `This article proposes a multiobjective operation optimization method based on` (abstract)
- `Focusing on the above problems, this article proposes` (introduction)
- `the superiorities of the proposed method are mainly reflected in the following several aspects.` (introduction)
- `To verify the effectiveness and superiority of the proposed` (experiments)
- `In the future, the authors will further research` (conclusion)

## House style

自称是 `This article` / `this article` / `the proposed method` / `the authors`。未见 `Here we`。`This article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.6896 abstract: This article proposes a multiobjective operation optimization method based on reinforcement self-learning and knowledge guidance for quality assurance and consumption reduction of wastewater treatment process (WWTP) with nonstationary time-varying dynamics.
- p.6896 abstract: Data experiments show that the proposed method can effectively reduce energy consumption and ensure effluent quality.
- p.6896 introduction: WITH the development of urban modernization, the demand of industry, and daily life for water resources is increasing, leading to a sharp increase in industrial wastewater and domestic sewage.
- p.6896 introduction: Therefore, it is urgent to realize the operation optimization and control of WWTP, so as to ensure the EQ standards and reduce the EC, namely, “ensure quality and reduce cost.”
- p.6897 introduction: However, the WWTP is subject to strong nonstationary dynamics and time-varying working conditions, and passive acceptance of influent flow, pollutant composition and concentration, etc.
- p.6897 introduction: However, the above single-objective optimization methods only focus on the reduction of EC, which easily leads to the exceedance of the EQ, thus increase the operation cost.
- p.6898 introduction: However, these conventional MOPSO algorithms usually require a large number of iterations and nondominated sorting operations, thus the computational complexity is large.
- p.6898 introduction: Focusing on the above problems, this article proposes a novel multiobjective operation optimization method for WWTP based on reinforcement self-learning and knowledge guidance, as shown in Fig. 2.
- p.6898 introduction: Compared with the existing operation optimization methods, the superiorities of the proposed method are mainly reflected in the following several aspects.
- p.6899 method: The first task to realize the operation optimization of WWTP in this article is to develop simple but effective operation index models oriented to multiobjective optimization.
- p.6903 experiments: To verify the effectiveness and superiority of the proposed operation optimization method, several data experiments, and comparisons are performed on the platform of the international benchmark simulation model 1 (BSM1).
- p.6907 conclusion: Aiming at the problems of high EC and EQ indices easily exceeding the limited standards in WWTP, this article proposes a novel multiobjective operation optimization method based on reinforcement self-learning and knowledge guidance for complicated industrial process with strong time-varying dynamics.
- p.6908 conclusion: Various experiments have verified the effectiveness and superiority and practicability of the proposed method.
- p.6908 conclusion: Moreover, the proposed method also has good generalizable applicability.
- p.6908 conclusion: In the future, the authors will further research how to more fully exploit the effective information with common characteristics in the evolutionary computation of heuristic optimization algorithms and perform learning feedback, so as to improve the optimization performance.
