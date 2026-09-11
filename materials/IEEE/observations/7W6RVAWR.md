---
key: 7W6RVAWR
title: "Adaptive Constraint Penalty-Based Multiobjective Operation Optimization of an Industrial Dynamic System With Complex Multiconstraint"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2023.3341982"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. CONSTRAINED MULTIOBJECTIVE OPERATION OPTIMIZATION PROBLEM OF WWTP` → `III. ONLINE LEARNING MODELING OF OPTIMIZATION OBJECTIVES AND CONSTRAINTS` → `IV. ICMOEA/D FOR OPERATION OPTIMIZATION OF WWTP` → `V. TEST FUNCTION-BASED VERIFICATION` → `VI. ICMOEA/D-BASED OPERATION OPTIMIZATION OF WWTP` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评加权求和、MOEA/D、约束多目标与交叉代差分进化）。Introduction 无单独节序路标句，II 起为问题。Method 在 III–IV。Experiments 分为测试函数（V）与 WWTP（VI）。

## Openers

- abstract: `Aiming at the` — "Aiming at the operation optimization of the wastewater treatment process (WWTP) with nonstationary time-varying dynamics and complex multiconstraint, this article proposes a novel adaptive constraint penalty decomposed multiobjective evolutionary algorithm with synthetical distance (SD)-based cross-generation crossover." (p.4724)
- introduction: `THE OPERATION optimization` — "THE OPERATION optimization of practical industrial processes often involves the simultaneous optimization of multiple conflicting production objectives, that is, the multiobjective optimization problem (MOOP) [1], [2]." (p.4724；栏首掉字)
- method: `In order to` — "In order to solve the CMOOP shown in (2) with the models of optimization and constraint established in Section III, this section proposes an improved decomposition-based constrained MOEA which is based on SD, intergenerational information, and constraint adaptive penalty, namely, ICMOEA/D." (p.4727, IV)
- experiments: `In this section` — "In this section, the performance of the proposed algorithm is tested and analyzed based on 14 frequently used CMOOPs [31]." (p.4730, V)
- conclusion: `In this article` — "In this article, an improved constrained MOEA/D based on cross-generation information of SD and adaptive constraint penalty, namely, ICMOEA/D, is proposed to attack the multiobjective operation optimization problem of the WWTP with time-varying dynamics and complex constraints." (p.4736)

## Gap transitions

- therefore (introduction): "Therefore, the operation optimization of WWTP is a typical MOOP with complex constraints [2]." (p.4724)
- however (introduction): "However, the progress of the optimization degree of each objective during the optimization process is inoperable." (p.4724)
- although (introduction): "Although these algorithms shown good performance in solving MOOPs, they rarely discuss the complex multiconstraint handling problems frequently encountered in engineering optimization, and instead use a simple penalty function method to handle constraints." (p.4725)
- however (introduction): "However, these algorithms generally use the 1-D Euclidean distance to measure the similarity of multidimensional solution vectors or weight vectors" (p.4725)
- aiming at (abstract/introduction): "Aiming at the complex multiconstraint during the operation optimization of WWTP, an adaptive penalty algorithm is further adopted" (p.4724)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a novel adaptive constraint penalty decomposed multiobjective evolutionary algorithm"; "this article proposes an improved constrained MOEA/D"
- verify / causal / abstract, experiments: "the effectiveness, superiority, and practicability of the proposed method are verified through test function experiments as well as operation optimization control experiments of WWTP"
- demonstrate / causal / experiments, conclusion: "This demonstrates that the proposed ICMOEA/D has the best multiobjective optimization performance"; "Both test function verifications and operation optimization control experiment of WWTP demonstrate that the control scheme with the proposed ICMOEA/D can achieve the best performance."
- confirm / causal / experiments: "These results confirm the effectiveness and superiority of the proposed ICMOEA/D in the overall optimization performance"
- indicate / causal / experiments: "This indicates that the constraint-handling ability of the APM technology used in this article is not inferior to the most popular constraint-domination technology"

## Cross-section linkers

- introduction → problem: 贡献列表后直接 `II. CONSTRAINED MULTIOBJECTIVE OPERATION OPTIMIZATION PROBLEM OF WWTP` (p.4725)
- modeling → algorithm: SW-RBSI 段落后 `IV. ICMOEA/D FOR OPERATION OPTIMIZATION OF WWTP` (p.4727)
- algorithm → experiments: Algorithm 2 后 `V. TEST FUNCTION-BASED VERIFICATION` (p.4730)
- WWTP experiments → conclusion: 七日平均指标表后 `VII. CONCLUSION` (p.4736)

## Candidate rules

- R001 abstract 开篇用 `Aiming at` + 对象，再用 `this article proposes`。
- R002 Introduction 无独立 Related Work，加权求和 → MOEA/D → 约束处理 → 代际信息。
- R003 贡献列表标题用 `The main innovations of this article are as follows.`
- R004 Experiments 先 `TEST FUNCTION-BASED VERIFICATION` 再工业案例节。
- R005 Conclusion 先收回 SD / 交叉代 / APM，再用 `In addition, there are still some challenges for the future study`

## Candidate phrases

- `this article proposes a novel` (abstract)
- `Aiming at the operation optimization of` (abstract)
- `The main innovations of this article are as follows.` (introduction)
- `Focusing on the above practical operation optimization problem and the shortcomings of existing methods` (introduction)
- `is proposed to attack the multiobjective operation optimization problem` (conclusion)

## House style

自称是 `this article` / `this article proposes` / `the proposed method` / `ICMOEA/D`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.4724 abstract: Aiming at the operation optimization of the wastewater treatment process (WWTP) with nonstationary time-varying dynamics and complex multiconstraint, this article proposes a novel adaptive constraint penalty decomposed multiobjective evolutionary algorithm with synthetical distance (SD)-based cross-generation crossover.
- p.4724 abstract: Finally, the effectiveness, superiority, and practicability of the proposed method are verified through test function experiments as well as operation optimization control experiments of WWTP.
- p.4724 introduction: THE OPERATION optimization of practical industrial processes often involves the simultaneous optimization of multiple conflicting production objectives, that is, the multiobjective optimization problem (MOOP) [1], [2].
- p.4724 introduction: Therefore, the operation optimization of WWTP is a typical MOOP with complex constraints [2].
- p.4724 introduction: However, the progress of the optimization degree of each objective during the optimization process is inoperable.
- p.4725 introduction: Although these algorithms shown good performance in solving MOOPs, they rarely discuss the complex multiconstraint handling problems frequently encountered in engineering optimization, and instead use a simple penalty function method to handle constraints.
- p.4725 introduction: Focusing on the above practical operation optimization problem and the shortcomings of existing methods, this article proposes an improved constrained MOEA/D algorithm with synthetical distance (SD)-based intergenerational crossover operation and adaptive constraint penalty, namely, ICMOEA/D.
- p.4725 introduction: The main innovations of this article are as follows.
- p.4727 method: In order to solve the CMOOP shown in (2) with the models of optimization and constraint established in Section III, this section proposes an improved decomposition-based constrained MOEA which is based on SD, intergenerational information, and constraint adaptive penalty, namely, ICMOEA/D.
- p.4730 experiments: In this section, the performance of the proposed algorithm is tested and analyzed based on 14 frequently used CMOOPs [31].
- p.4731 experiments: These results confirm the effectiveness and superiority of the proposed ICMOEA/D in the overall optimization performance (diversity and convergence) in solving CMOOPs.
- p.4732 experiments: This demonstrates that the proposed ICMOEA/D has the best multiobjective optimization performance and multiconstraint handling capability on these problems.
- p.4736 experiments: Therefore, compared with other methods, the proposed ICMOEA/D+IMFAPC can obtain the optimal EQ with minimum EC, and all the EQ indicators satisfy the constraint conditions, effectively reducing the operational costs of the WWTP.
- p.4736 conclusion: In this article, an improved constrained MOEA/D based on cross-generation information of SD and adaptive constraint penalty, namely, ICMOEA/D, is proposed to attack the multiobjective operation optimization problem of the WWTP with time-varying dynamics and complex constraints.
- p.4736 conclusion: Both test function verifications and operation optimization control experiment of WWTP demonstrate that the control scheme with the proposed ICMOEA/D can achieve the best performance.
- p.4737 conclusion: In addition, there are still some challenges for the future study of the ICMOEA/D algorithm.
