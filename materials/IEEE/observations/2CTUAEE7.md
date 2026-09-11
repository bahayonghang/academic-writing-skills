---
key: 2CTUAEE7
title: "Mechanism-Data-Driven Multiobjective Optimization for Wastewater Treatment Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3364835"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "7810-7819"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. MECHANISM-DATA-DRIVEN MULTIOBJECTIVE OPTIMIZATION` → `IV. SIMULATIONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mechanism-based ASM/WEST 与 data-based critic/LSTM/flexible-objective 优化）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `SIMULATIONS`。

## Openers

- abstract: `Set-point optimization of` — "Set-point optimization of wastewater treatment process (WWTP) is critical for energy savings but is challenging due to complex nonlinear mechanisms and measurement noises." (p.7810)
- introduction: `WASTEWATER treatment process` — "WASTEWATER treatment process (WWTP), including multiple biochemical reactions, is a significant way to recover water resources [1], [2]." (p.7810)
- method: `In this section` — "In this section, the proposed MDD-MO method is systematically presented." (p.7812)
- experiments: `In this section` — "In this section, the proposed MDD-MO is validated on the simulation platform based on the benchmark simulation model No. 1 (BSM1)." (p.7815)
- conclusion: `An optimization method` — "An optimization method combining the mechanisms and process data is developed in this article to optimize WWTP under realistic conditions." (p.7818)

## Gap transitions

- to address (abstract): "To address this optimization problem, a mechanism-data-driven multiobjective optimization method is developed to alleviate deficiencies in mechanisms and process data." (p.7810)
- however (introduction): "However, since the complex and dynamic mechanisms, mechanism models for the set-point optimization suffer from low accuracy [5], [6]." (p.7810)
- therefore (introduction): "Therefore, there are still some open issues in WWTP optimization problems under realistic conditions." (p.7810)
- to solve (introduction): "To solve this problem, the current trend is to apply intelligent computing methods to complex industrial processes, including WWTP [18], [19]." (p.7811)
- although (conclusion): "Although some results have been achieved, future research should focus on the dynamic mechanism-data-driven optimization control of WWTP." (p.7818)

## Hedge verbs

- develop / causal / abstract, conclusion: "a mechanism-data-driven multiobjective optimization method is developed"; "An optimization method ... is developed in this article"
- propose / causal / abstract, introduction: "a weighted indicator-based multiobjective particle swarm optimization algorithm is proposed"; "a mechanism-data-driven multiobjective optimization (MDD-MO) is proposed in this article"
- demonstrate / causal / abstract, introduction: "The results demonstrate that this method can improve the optimization performance of WWTP"; "Simulation experiments ... demonstrate the significant improvement"
- should focus / speculative / conclusion: "future research should focus on the dynamic mechanism-data-driven optimization control of WWTP"
- is expected / speculative / conclusion: "it is expected to decouple dynamic and static components in the mechanism models"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II briefly describes the preliminaries. Section III gives the method in detail. The simulation results are provided to demonstrate the effectiveness of the proposed MDD-MO in Section IV. Finally, the conclusion is given in Section V." (p.7811)
- preliminaries → method: 动机句后 `III. MECHANISM-DATA-DRIVEN MULTIOBJECTIVE OPTIMIZATION` (p.7812)
- method → experiments: WIMOPSO remark 后 `IV. SIMULATIONS` (p.7815)
- experiments → conclusion: Case 3 收束后 `V. CONCLUSION` (p.7818)

## Candidate rules

- R002 Introduction 无独立 Related Work，mechanism/data 两类优化评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this method include three aspects`。
- R005 Conclusion 先收回方法，再用 `Although some results have been achieved, future research should focus on`。

## Candidate phrases

- `To address this optimization problem, a ... method is developed` (abstract)
- `is proposed in this article, which combines the advantages of` (introduction)
- `The main contributions of this method include three aspects.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `is developed in this article to` (conclusion)
- `Although some results have been achieved, future research should focus on` (conclusion)

## House style

自称 `is developed` / `is proposed in this article` / `the proposed MDD-MO`。未见 `Here we`、`In this paper`。被动自称 `is developed in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.7810 abstract: Set-point optimization of wastewater treatment process (WWTP) is critical for energy savings but is challenging due to complex nonlinear mechanisms and measurement noises.
- p.7810 abstract: To address this optimization problem, a mechanism-data-driven multiobjective optimization method is developed to alleviate deficiencies in mechanisms and process data.
- p.7810 abstract: The results demonstrate that this method can improve the optimization performance of WWTP.
- p.7810 introduction: WASTEWATER treatment process (WWTP), including multiple biochemical reactions, is a significant way to recover water resources [1], [2].
- p.7810 introduction: However, since the complex and dynamic mechanisms, mechanism models for the set-point optimization suffer from low accuracy [5], [6].
- p.7810 introduction: Therefore, there are still some open issues in WWTP optimization problems under realistic conditions.
- p.7811 introduction: To solve this problem, the current trend is to apply intelligent computing methods to complex industrial processes, including WWTP [18], [19].
- p.7811 introduction: Based on the above analysis, a mechanism-data-driven multiobjective optimization (MDD-MO) is proposed in this article, which combines the advantages of the mechanism-based and data-based optimization.
- p.7811 introduction: The main contributions of this method include three aspects.
- p.7811 introduction: The rest of this article is organized as follows. Section II briefly describes the preliminaries. Section III gives the method in detail. The simulation results are provided to demonstrate the effectiveness of the proposed MDD-MO in Section IV. Finally, the conclusion is given in Section V.
- p.7812 method: In this section, the proposed MDD-MO method is systematically presented.
- p.7815 experiments: In this section, the proposed MDD-MO is validated on the simulation platform based on the benchmark simulation model No. 1 (BSM1).
- p.7818 conclusion: An optimization method combining the mechanisms and process data is developed in this article to optimize WWTP under realistic conditions.
- p.7818 conclusion: Although some results have been achieved, future research should focus on the dynamic mechanism-data-driven optimization control of WWTP.
