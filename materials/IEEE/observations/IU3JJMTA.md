---
key: IU3JJMTA
title: "Knowledge-Data Driven Multitime-Scale Optimal Control for Wastewater Treatment Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3563554"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION AND PRELIMINARIES` → `III. KNOWLEDGE-DATA DRIVEN MULTITIME-SCALE OPTIMAL CONTROL` → `IV. SIMULATION AND EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评化学机理指标 / 数据驱动模型 / 多目标最优控制 / 已有多时间尺度控制）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `SIMULATION AND EXPERIMENTAL STUDIES`。

## Openers

- abstract: `The increasing demand` — "The increasing demand for wastewater treatment processes is to improve the effluent quality and reduce the energy consumption." (p.5022)
- introduction: `WASTEWATER treatment process` — "WASTEWATER treatment process (WWTP) provides a feasible and effective option to alleviate water scarcity and pollution [1],[2]." (p.5022；栏首掉字)
- method: `To achieve the` — "To achieve the optimum operation of WWTP, a KDD- MTSOC method is developed to satisfy the demands of performance indexes with multiple time scales." (p.5024)
- experiments: `To testify the` — "To testify the performance of the proposed KDD-MTSOC, a simulation experiment and a real WWTP experiment are performed." (p.5028)
- conclusion: `To realize the` — "To realize the optimum operation of denitrification reaction in WWTP, KDD-MTSOC integrating KRKS, KDPSO, with the PID controller was developed to achieve multitime-scale optimal control." (p.5031)

## Gap transitions

- however (abstract): "However, due to the existence of different time scales data acquisition for effluent quality and energy consumption, it is difficult to achieve optimum operation of wastewater treatment processes with multitime-scale property." (p.5022)
- to solve (abstract): "To solve this problem, a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is designed in this article." (p.5022)
- although (introduction): "Although the above multiobjective optimal control methods are capable of obtaining satisfying operational performance, the multitime-scale characteristic has been ignored [22]." (p.5023)
- however (introduction): "However, since these methods can establish performance indexes on the least common of multiple time scales to solve the mismatch between multiple time scales, it not only results in the loss of fast-time-scale data, but also the decline of frequency for optimal control." (p.5023)
- however (conclusion): "However, there is still some work that needs to be done to overcome its limitations." (p.5031)

## Hedge verbs

- design / causal / abstract: "a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is designed in this article"
- present / causal / introduction: "a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is presented in this article"
- demonstrate / causal / abstract, experiments: "The experimental results demonstrate that the KDD-MTSOC method can achieve outstanding operational performance."; "The simulation results demonstrated that dynamic Bayesian network can obtain dynamic characteristics of operational performance."
- indicate / associative / introduction, conclusion: "The simulation results indicated that the optimal control method can meet the demand for EQ and EC."; "it can be concluded that the proposed KDD-MTSOC can provide a promising perspective"

## Cross-section linkers

- introduction → problem: "The rest of this article is organized as follows. Section II presents the problem formulation. The details of the proposed KDD-MTSOC are described in Section III, consisting of the design of KRKS, KDPSO algorithm and the proportional integral derivative (PID) controller. Section IV includes experimental setup, simulation experimental results, and discussion of KDD-MTSOC. Finally, Section V concludes this article." (p.5023)
- method → experiments: 收敛分析后 `IV. SIMULATION AND EXPERIMENTAL STUDIES` (p.5028)
- experiments → conclusion: Discussion 编号优势后直接 `V. CONCLUSION` (p.5031)

## Candidate rules

- R001 摘要缺口后用 `To solve this problem, a ... is designed in this article`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `the major contributions of KDD-MTSOC are given as follows` + 编号列表。
- R005 结论用 `However, there is still some work that needs to be done` 承认局限，再指向后续应用。

## Candidate phrases

- `To solve this problem, a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is designed in this article` (abstract)
- `Motivated by the above analysis, a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is presented in this article` (introduction)
- `the major contributions of KDD-MTSOC are given as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `However, there is still some work that needs to be done to overcome its limitations.` (conclusion)

## House style

自称是 `is designed in this article` / `is presented in this article` / `the proposed KDD-MTSOC`。未见 `Here we`、`In this paper`。`designed in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.5022 abstract: The increasing demand for wastewater treatment processes is to improve the effluent quality and reduce the energy consumption.
- p.5022 abstract: However, due to the existence of different time scales data acquisition for effluent quality and energy consumption, it is difficult to achieve optimum operation of wastewater treatment processes with multitime-scale property.
- p.5022 abstract: To solve this problem, a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is designed in this article.
- p.5022 abstract: The experimental results demonstrate that the KDD-MTSOC method can achieve outstanding operational performance.
- p.5022 introduction: WASTEWATER treatment process (WWTP) provides a feasible and effective option to alleviate water scarcity and pollution [1],[2].
- p.5023 introduction: Although the above multiobjective optimal control methods are capable of obtaining satisfying operational performance, the multitime-scale characteristic has been ignored [22].
- p.5023 introduction: However, since these methods can establish performance indexes on the least common of multiple time scales to solve the mismatch between multiple time scales, it not only results in the loss of fast-time-scale data, but also the decline of frequency for optimal control.
- p.5023 introduction: Motivated by the above analysis, a knowledge-data driven multitime-scale optimal control (KDD-MTSOC) is presented in this article.
- p.5023 introduction: Compared with the existing optimal control strategies, the major contributions of KDD-MTSOC are given as follows.
- p.5023 introduction: The rest of this article is organized as follows. Section II presents the problem formulation. The details of the proposed KDD-MTSOC are described in Section III, consisting of the design of KRKS, KDPSO algorithm and the proportional integral derivative (PID) controller. Section IV includes experimental setup, simulation experimental results, and discussion of KDD-MTSOC. Finally, Section V concludes this article.
- p.5024 method: To achieve the optimum operation of WWTP, a KDD- MTSOC method is developed to satisfy the demands of performance indexes with multiple time scales.
- p.5028 experiments: To testify the performance of the proposed KDD-MTSOC, a simulation experiment and a real WWTP experiment are performed.
- p.5030 experiments: As shown in Table I, KDD-MTSOC can achieve the minimum PE, EQ, TC, and IAE.
- p.5031 conclusion: To realize the optimum operation of denitrification reaction in WWTP, KDD-MTSOC integrating KRKS, KDPSO, with the PID controller was developed to achieve multitime-scale optimal control.
- p.5031 conclusion: In this article, it can be concluded that the proposed KDD-MTSOC can provide a promising perspective for solving the problems of complex industrial processes with multitime-scale characteristics.
- p.5031 conclusion: However, there is still some work that needs to be done to overcome its limitations.
