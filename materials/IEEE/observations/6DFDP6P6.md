---
key: 6DFDP6P6
title: "A differential evolution-based hybrid NSGA-II for multi-objective optimization"
venue: "2015 IEEE 7th International Conference on Cybernetics and Intelligent Systems (CIS) and IEEE Conference on Robotics, Automation and Mechatronics (RAM)"
doi: "10.1109/ICCIS.2015.7274552"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-6"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. MULTI-OBJECTIVE OPTIMIZATION PROBLEMS` → `III. HYBRID MULTI-OBJECTIVE OPTIMIZATION ALGORITHM DMNSGA-II` → `IV. SIMULATION WITH INSTANCES AND PERFORMANCE COMPARISON` → `V. CONCLUSION`。前置 `Abstract—` 与 `Keywords-`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 VEGA / MOGA / NSGA-II、动态拥挤距离、INSGA-II、DE / MODE / NSDE）。Introduction 末有 `The major contributions of this paper are two-fold`，无 `The rest of this paper is organized`。Method 标题为 `HYBRID MULTI-OBJECTIVE OPTIMIZATION ALGORITHM DMNSGA-II`。Experiments 标题为 `SIMULATION WITH INSTANCES AND PERFORMANCE COMPARISON`（ZDT1/3/4/6）。

## Openers

- abstract: `To improve the` — "To improve the search accuracy and diversity of non-dominated sorting genetic algorithm (NSGA-II), an improved algorithm DMNSGA-II referencing to the strategy of differential evolution to strengthen local search is proposed in this paper." (p.81)
- introduction: `In real life` — "In real life, the number of designing target in many complex systems is always more than one, and they are mutual restraint so as to couldn't achieve optimal at the same time[1][2]." (p.81)
- method: `Since the poor` — "Since the poor search accuracy and global search capability of NSGA-II, in this section, we present the DMNSGA-II." (p.83, III.C)
- experiments: `Test problems are` — "Test problems are suggested by Zitzler et al.[21], with aiming at multi-objective optimizing." (p.83, IV.A)
- conclusion: `In this paper` — "In this paper, a new hybrid evolutionary algorithm is designed to improve the convergence and maintain the diversity." (p.86)

## Gap transitions

- however (introduction): "However, it should be noted, its global search capability is good, but the search accuracy is relatively poor and the diveristy remains to be enhance because of the blind spots." (p.81)
- however (introduction): "However, they did not consider the convergence while improving the distribution of solutions[14]." (p.81)
- however / therefor (introduction): "However, the above works also confronts the problem of slow convergence rate and fall into local optimum easier. Therefor they cannot solve the MOPs effectively." (p.81)
- how to / in this paper (introduction): "How to enhance the local search capability and improve the convergence, while enjoying the benefits of optimal solution set approximate to Pareto front and well-balanced distribution by NSGA-II strategy, is an important but under-explored research problem. In this paper, we introduce the differential evolution (DE) and NSGA-II based genetic algorithm and propose a new differential evolution-based and mutation-preserved nondominated sorting genetic algorithm (DMNSGA-II), with the aim of improving the search accuracy and convergence." (p.81–82)
- however (experiments): "DMNSGA-II performs better than NSDE in ZDT1 and ZDT3 in term of convergence metric. However, though its convergence metric is slightly worse in ZDT4 and ZDT6, DMNSGA-II is able to converge to true Pareto front * PF well and distribute uniformly." (p.84)
- although (experiments): "On ZDT6, although the two results are close to * PF , but the population distribution of DMNSGA-II is more uniform than NSGA-II, the global search capability of it is superior to NSGA-II's." (p.86)
- in the future (conclusion): "In the future, differential operator in DMNSGA-II can be improved to enhance the convergence, and use other benchmark problems to test the algorithm." (p.86)

## Hedge verbs

- propose / causal / abstract, introduction: "an improved algorithm DMNSGA-II ... is proposed in this paper"; "we introduce ... and propose a new ... (DMNSGA-II)"
- present / causal / method: "in this section, we present the DMNSGA-II"
- demonstrate / causal / abstract: "simulation results demonstrate that the proposed algorithm can achieve a good overall performance"
- design / causal / conclusion: "a new hybrid evolutionary algorithm is designed to improve the convergence and maintain the diversity"
- can / speculative / conclusion: "the proposed DMNSGA-II algorithm can efficiently improve convergence"; "differential operator in DMNSGA-II can be improved"

## Cross-section linkers

- introduction → preliminaries: 贡献两折列表后直接 `II. MULTI-OBJECTIVE OPTIMIZATION PROBLEMS`，无节序路标 (p.82)
- method → experiments: 伪代码 Fig. 2 后直接 `IV. SIMULATION WITH INSTANCES AND PERFORMANCE COMPARISON` (p.83)
- experiments → conclusion: Fig. 4 对比段落后直接 `V. CONCLUSION` (p.86)

## Candidate rules

- R001 摘要贡献句用目的不定式 `To improve ... is proposed in this paper`。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段，缺口用 `How to ... is an important but under-explored research problem`。
- R004 贡献用 `The major contributions of this paper are two-fold` + 编号列表。
- R005 Conclusion 先收回方法，再用 `In the future` 指向后续。

## Candidate phrases

- `an improved algorithm DMNSGA-II ... is proposed in this paper` (abstract)
- `simulation results demonstrate that the proposed algorithm can` (abstract)
- `is an important but under-explored research problem` (introduction)
- `In this paper, we introduce ... and propose a new` (introduction)
- `The major contributions of this paper are two-fold:` (introduction)
- `in this section, we present the DMNSGA-II` (method)
- `In the future, differential operator in DMNSGA-II can be improved` (conclusion)

## House style

自称 `is proposed in this paper` / `In this paper, we introduce` / `we propose` / `the proposed algorithm` / `our proposed algorithm`。未见 `Here we`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `This article`。

## Quotes

- p.81 abstract: To improve the search accuracy and diversity of non-dominated sorting genetic algorithm (NSGA-II), an improved algorithm DMNSGA-II referencing to the strategy of differential evolution to strengthen local search is proposed in this paper.
- p.81 abstract: The algorithm uses mutation guiding operator and crossover operator of DE to replace crossover operator in NSGA-II to enhance the local search capability and improve search accuracy. while retaining the mutation operator of NSGA-II to improve diversity.
- p.81 abstract: We use four benchmark test problems to investigate the performance of the DMNSGA-II algorithm, and simulation results demonstrate that the proposed algorithm can achieve a good overall performance in multi-objective optimization.
- p.81 introduction: In real life, the number of designing target in many complex systems is always more than one, and they are mutual restraint so as to couldn't achieve optimal at the same time[1][2].
- p.81 introduction: However, it should be noted, its global search capability is good, but the search accuracy is relatively poor and the diveristy remains to be enhance because of the blind spots.
- p.81 introduction: However, they did not consider the convergence while improving the distribution of solutions[14].
- p.81 introduction: However, the above works also confronts the problem of slow convergence rate and fall into local optimum easier. Therefor they cannot solve the MOPs effectively.
- p.81–82 introduction: How to enhance the local search capability and improve the convergence, while enjoying the benefits of optimal solution set approximate to Pareto front and well-balanced distribution by NSGA-II strategy, is an important but under-explored research problem.
- p.82 introduction: In this paper, we introduce the differential evolution (DE) and NSGA-II based genetic algorithm and propose a new differential evolution-based and mutation-preserved nondominated sorting genetic algorithm (DMNSGA-II), with the aim of improving the search accuracy and convergence.
- p.82 introduction: The major contributions of this paper are two-fold: 1) using the directional mutation operator of DE to intervene and disturb evolutionary direction of a solution; 2) preserving the mutation operator of NSGA-II to improve local search and the ability to escape from local optimum.
- p.82 preliminaries: Multi-objective optimization problem also known as multiple criteria optimization problem, which is concerned with mathematical optimization problems involving more than one objective function to be optimized simultaneously.
- p.83 method: Since the poor search accuracy and global search capability of NSGA-II, in this section, we present the DMNSGA-II.
- p.83 method: The objective of this algorithm is to enhance search accuracy and keep the ability to escape from local optimum.
- p.83 experiments: Test problems are suggested by Zitzler et al.[21], with aiming at multi-objective optimizing.
- p.84 experiments: In order to evaluate the performance of our proposed algorithm, it is coded on MATLAB, running on the computer of Intel Core2 Duo CPU, 2.00GHz, 2GB memory.
- p.84 experiments: DMNSGA-II performs better than NSDE in ZDT1 and ZDT3 in term of convergence metric. However, though its convergence metric is slightly worse in ZDT4 and ZDT6, DMNSGA-II is able to converge to true Pareto front * PF well and distribute uniformly.
- p.86 experiments: On ZDT6, although the two results are close to * PF , but the population distribution of DMNSGA-II is more uniform than NSGA-II, the global search capability of it is superior to NSGA-II's.
- p.86 conclusion: In this paper, a new hybrid evolutionary algorithm is designed to improve the convergence and maintain the diversity.
- p.86 conclusion: Testing by the benchmark problems ZDT1, ZDT3, ZDT4, ZDT6 and comparing with three mentioned algorithms, the proposed DMNSGA-II algorithm can efficiently improve convergence to solve the multi-objective optimization problem.
- p.86 conclusion: In the future, differential operator in DMNSGA-II can be improved to enhance the convergence, and use other benchmark problems to test the algorithm.
