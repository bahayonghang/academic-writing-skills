---
key: FWIX9FKS
title: "pSPEA2: Optimization fitness and distance calculations for improving Strength Pareto Evolutionary Algorithm 2 (SPEA2)"
venue: "2016 International Conference on Information Technology Systems and Innovation (ICITSI)"
doi: "10.1109/ICITSI.2016.7858224"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-5"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. ANALYSIS OF SPEA2 ON PISA FRAMEWORK` → `IV. PARALLELISM OF SPEA2 ON PISA FRAMEWORK` → `V. EXPERIMENTAL RESULTS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 `II. RELATED WORK`。`related_work=independent`。Introduction 末有节序路标，指向 Section 2–6（阿拉伯数字）。Method 拆成分析（III）与并行实现（IV）。Experiments 标题为 `EXPERIMENTAL RESULTS`（DTLZ / PISA，串并行对比）。

## Openers

- abstract: `SPEA2 (Strength Pareto` — "SPEA2 (Strength Pareto Evolutionary Algorithm 2) is an evolutionary algorithm based on population, which is solutions to resolve Multi-objective Optimization Problems (MOPs)." (p.1)
- introduction: `Evolutionary Algorithms [1]` — "Evolutionary Algorithms [1] uses some techniques of evolution theory such as selection, mutation, and recombination [2], [3], [4] to provide several potential solutions for Multi-objective Optimization Problems (MOP) [2], [5], [6], [7]." (p.1)
- related_work: `S. Santander-Jimnez and` — "S. Santander-Jimnez and M. A. Vega-Rodrguez paralleled two algorithms: SPEA2 and NSGA2, on OpenMP platform [14]." (p.1)
- method: `Algorithm of SPEA2` — "Algorithm of SPEA2 on PISA framework is showed on algorithm 1 and algorithm 2." (p.2, III)
- experiments: `The test is` — "The test is conducted on Intel(R) Core(TM) i7-4500U processor, 4GB RAM, and 2GB NVidia GEFORCE 820M (2 SM, 96 CUDA cores)." (p.4, V.A)
- conclusion: `In this paper` — "In this paper we propose a parallel algorithm, pSPEA2, to solve MOP." (p.5)

## Gap transitions

- but (introduction): "There have been many studies on improving the solution accuracy of SPEA2, such as CoEvolutionary Learning [12], SPEA2+[13], but only a few studies on trying to improve its computation time." (p.1)
- in this paper (introduction): "In this paper, we present a parallelism on SPEA2 algorithm on PISA framework using multicore accelerator GPGPU (CUDA) [15], [16], [17]." (p.1)
- motivated (method): "Motivated by these results, we decide to parallel both functions." (p.2)
- therefore (conclusion): "We believe the problem lies in transpose kernel which consumes 70% of total running time, therefore there is necessity to study this further." (p.5)
- in the future (conclusion): "In the future, we would like to explore the implementation and application of pSPEA2 particularly in hypervolume data science." (p.5)

## Hedge verbs

- aim / causal / abstract: "Our aim is to improve SPEA2 performance to process a population using parallelism in GPU."
- present / causal / introduction: "we present a parallelism on SPEA2 algorithm"
- propose / causal / conclusion: "we propose a parallel algorithm, pSPEA2, to solve MOP"
- show / causal / abstract, experiments: "The result shows that speed up increase approximately 1.5 times."; "The result shows that we achieve 1.5 times speed up than serial algorithm."
- believe / speculative / conclusion: "We believe the problem lies in transpose kernel"
- would like / speculative / conclusion: "we would like to explore the implementation and application of pSPEA2"

## Cross-section linkers

- introduction → related work: "The remaining part of the paper is organized as follows. Section 2 introduces some related works on parallel algorithm and a benchmarking test. Section 3 is analysis of SPEA2 on PISA Framework. Section 4 how to parallelism of SPEA2 on PISA Framework. We present the experimental results in Section 5 and finally, the concluding remarks and future work in Section 6." (p.1)
- analysis → method: Table I 后 "Motivated by these results, we decide to parallel both functions." 再接 `IV. PARALLELISM OF SPEA2 ON PISA FRAMEWORK` (p.2–3)
- method → experiments: Listing 8 后直接 `V. EXPERIMENTAL RESULTS` (p.4)
- experiments → conclusion: Figure 2 后直接 `VI. CONCLUSION` (p.5)

## Candidate rules

- R003 Introduction 末用 `The remaining part of the paper is organized as follows`，路标用阿拉伯 Section 2–6。
- R002 独立 `II. RELATED WORK`，以作者名开节。
- R001 摘要目标句用 `Our aim is to improve`，结果句用 `The result shows that`。
- R005 Conclusion 用 `In this paper we propose` 收回方法，再用 `therefore` 与 `In the future, we would like to` 指向后续。

## Candidate phrases

- `Our aim is to improve SPEA2 performance to` (abstract)
- `In this paper, we present a parallelism on` (introduction)
- `The remaining part of the paper is organized as follows.` (introduction)
- `Motivated by these results, we decide to` (method)
- `In this paper we propose a parallel algorithm` (conclusion)
- `In the future, we would like to explore` (conclusion)

## House style

自称 `In this paper, we present` / `In this paper we propose` / `Our aim` / `we decide`。未见 `Here we`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `This article`。

## Quotes

- p.1 abstract: SPEA2 (Strength Pareto Evolutionary Algorithm 2) is an evolutionary algorithm based on population, which is solutions to resolve Multi-objective Optimization Problems (MOPs).
- p.1 abstract: Our aim is to improve SPEA2 performance to process a population using parallelism in GPU.
- p.1 abstract: By optimization fitness and distance calculations using transposed data to process in CUDA platform.
- p.1 abstract: The result shows that speed up increase approximately 1.5 times.
- p.1 introduction: Evolutionary Algorithms [1] uses some techniques of evolution theory such as selection, mutation, and recombination [2], [3], [4] to provide several potential solutions for Multi-objective Optimization Problems (MOP) [2], [5], [6], [7].
- p.1 introduction: There have been many studies on improving the solution accuracy of SPEA2, such as CoEvolutionary Learning [12], SPEA2+[13], but only a few studies on trying to improve its computation time.
- p.1 introduction: In this paper, we present a parallelism on SPEA2 algorithm on PISA framework using multicore accelerator GPGPU (CUDA) [15], [16], [17].
- p.1 introduction: The remaining part of the paper is organized as follows. Section 2 introduces some related works on parallel algorithm and a benchmarking test. Section 3 is analysis of SPEA2 on PISA Framework. Section 4 how to parallelism of SPEA2 on PISA Framework. We present the experimental results in Section 5 and finally, the concluding remarks and future work in Section 6.
- p.1 related_work: S. Santander-Jimnez and M. A. Vega-Rodrguez paralleled two algorithms: SPEA2 and NSGA2, on OpenMP platform [14].
- p.2 method: Algorithm of SPEA2 on PISA framework is showed on algorithm 1 and algorithm 2.
- p.2 method: Motivated by these results, we decide to parallel both functions.
- p.4 experiments: The test is conducted on Intel(R) Core(TM) i7-4500U processor, 4GB RAM, and 2GB NVidia GEFORCE 820M (2 SM, 96 CUDA cores).
- p.4 experiments: The result shows that we achieve 1.5 times speed up than serial algorithm.
- p.4 experiments: By analyzing the running time of parallel algorithm, we find that kernel transpose consumes 70% of total running time ( Figure 2).
- p.5 conclusion: In this paper we propose a parallel algorithm, pSPEA2, to solve MOP.
- p.5 conclusion: It achieves 1.5 times better running time than its serial algorithm counterpart.
- p.5 conclusion: We believe the problem lies in transpose kernel which consumes 70% of total running time, therefore there is necessity to study this further.
- p.5 conclusion: In the future, we would like to explore the implementation and application of pSPEA2 particularly in hypervolume data science.
