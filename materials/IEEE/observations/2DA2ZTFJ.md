---
key: 2DA2ZTFJ
title: "Bridging Evolutionary Multiobjective Optimization and GPU Acceleration via Tensorization"
venue: "IEEE Transactions on Evolutionary Computation"
doi: "10.1109/TEVC.2025.3555605"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BACKGROUND` → `III. TENSORIZATION METHODOLOGY` → `IV. TENSORIZATION IMPLEMENTATION IN REPRESENTATIVE EMO ALGORITHMS` → `V. MULTIOBJECTIVE ROBOT CONTROL BENCHMARK` → `VI. EXPERIMENTAL STUDY` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立相关工作节，标题为 `II. BACKGROUND`（EMO taxonomy 与 GPU acceleration）。`related_work=independent`。Introduction 末有 `The structure of this article is as follows` 路标，指向 II–VII。Method 拆成张量化方法（III）与三种算法实现（IV）。Experiments 标题为 `EXPERIMENTAL STUDY`。另有独立基准节 V。

## Openers

- abstract: `Evolutionary multiobjective optimization` — "Evolutionary multiobjective optimization (EMO) has made significant strides over the past two decades." (p.1)
- introduction: `In many real-world` — "In many real-world optimization problems (e.g., material design [1], [2], energy management [3], [4], network optimization [5], and portfolio optimization [6]), decision-makers must consider multiple (and often conflicting) objectives simultaneously." (p.1)
- method: `In this section` — "In this section, we present how to adopt the general tensorization methodology in EMO algorithms." (p.3, III)
- experiments: `In this section` — "In this section, we conduct experiments to evaluate the performance of the tensorized EMO algorithms, including TensorNSGA-III, TensorMOEA/D, and TensorHypE." (p.9, VI)
- conclusion: `This article introduces` — "This article introduces a tensorization approach to address the computational limitations of traditional CPU-based EMO algorithms, enhancing both speed and scalability." (p.12)

## Gap transitions

- however (abstract): "However, as problem scales and complexities increase, traditional EMO algorithms face substantial performance limitations due to insufficient parallelism and scalability." (p.1)
- to bridge (abstract): "To bridge the gap, we propose to parallelize EMO algorithms on GPUs via the tensorization methodology." (p.1)
- however (introduction): "However, to fully leverage the potential of GPUs for EMO algorithms, a systematic method of parallelization is necessary, yet little effort has been made in this direction so far." (p.1)
- despite (related work): "Despite these advances, GPU-accelerated EMO algorithms remain in their infancy." (p.3)
- while (conclusion): "While tensorization has substantially improved algorithmic efficiency, opportunities remain to further optimize speed and memory use." (p.13)

## Hedge verbs

- propose / causal / abstract: "we propose to parallelize EMO algorithms on GPUs via the tensorization methodology"
- demonstrate / causal / abstract: "We demonstrate the effectiveness of our approach by applying it to three representative EMO algorithms"
- show / causal / abstract, experiments: "Our experiments show that the tensorized EMO algorithms achieve speedups of up to 1113×"; "Fig. 3 shows that TensorNSGA-III"
- introduce / causal / introduction, conclusion: "we introduce a concise and general tensorization methodology"; "This article introduces a tensorization approach"
- confirm / causal / conclusion: "Our results confirm that tensorized algorithms can significantly accelerate computations"

## Cross-section linkers

- introduction → background: "The structure of this article is as follows: Section II reviews the background and related work. Section III introduces the tensorization methodology for GPU acceleration. Section IV details the implementations of core operations in three representative EMO algorithms. Section V introduces the multiobjective robot control benchmark. Section VI outlines the experimental setup and results. Section VII summarizes the findings and discusses future work." (p.2)
- background → method: "Moreover, many of these implementations rely heavily on CUDA programming [58] and are not open-source, thus making them less accessible, particularly for beginners." 随后 `III. TENSORIZATION METHODOLOGY` (p.3)
- method → experiments: 基准节 V 后接 `VI. EXPERIMENTAL STUDY` (p.9)
- experiments → conclusion: 机器人控制结果后直接 `VII. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `To bridge the gap, we propose to parallelize`，不用 `Here we`。
- R002 独立相关工作标题为 `BACKGROUND`，再分 taxonomy 与 GPU acceleration。
- R003 Introduction 末用 `The structure of this article is as follows` 指向 II–VII。
- R004 贡献用 `The main contributions of this research are as follows:` + 编号列表。
- R005 Experiments 标题为 `EXPERIMENTAL STUDY`。
- R006 Conclusion 用 `This article introduces` 收回，再用 `Future work will focus on` 指向后续。

## Candidate phrases

- `To bridge the gap, we propose to parallelize` (abstract)
- `The main contributions of this research are as follows:` (introduction)
- `The structure of this article is as follows:` (introduction)
- `This article introduces a tensorization approach to address` (conclusion)
- `Future work will focus on refining key operators` (conclusion)

## House style

自称是 `we propose` / `we introduce` / `this article` / `this research` / `our results`。未见 `Here we`。`This article introduces` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Evolutionary multiobjective optimization (EMO) has made significant strides over the past two decades.
- p.1 abstract: However, as problem scales and complexities increase, traditional EMO algorithms face substantial performance limitations due to insufficient parallelism and scalability.
- p.1 abstract: To bridge the gap, we propose to parallelize EMO algorithms on GPUs via the tensorization methodology.
- p.1 abstract: Our experiments show that the tensorized EMO algorithms achieve speedups of up to 1113× compared to their CPU-based counterparts, while maintaining solution quality and effectively scaling population sizes to hundreds of thousands.
- p.1 introduction: In many real-world optimization problems (e.g., material design [1], [2], energy management [3], [4], network optimization [5], and portfolio optimization [6]), decision-makers must consider multiple (and often conflicting) objectives simultaneously.
- p.1 introduction: However, to fully leverage the potential of GPUs for EMO algorithms, a systematic method of parallelization is necessary, yet little effort has been made in this direction so far.
- p.2 introduction: The main contributions of this research are as follows:
- p.2 introduction: The structure of this article is as follows: Section II reviews the background and related work. Section III introduces the tensorization methodology for GPU acceleration. Section IV details the implementations of core operations in three representative EMO algorithms. Section V introduces the multiobjective robot control benchmark. Section VI outlines the experimental setup and results. Section VII summarizes the findings and discusses future work.
- p.3 related work: Despite these advances, GPU-accelerated EMO algorithms remain in their infancy.
- p.3 method: In this section, we present how to adopt the general tensorization methodology in EMO algorithms.
- p.9 experiments: In this section, we conduct experiments to evaluate the performance of the tensorized EMO algorithms, including TensorNSGA-III, TensorMOEA/D, and TensorHypE.
- p.9 experiments: When the population size n reaches 32768, TensorNSGA-III, TensorMOEA/D, and TensorHypE attain speedups of approximately 191×, 1113×, and 186×, respectively, compared to their CPU-based counterparts.
- p.12 conclusion: This article introduces a tensorization approach to address the computational limitations of traditional CPU-based EMO algorithms, enhancing both speed and scalability.
- p.12 conclusion: Our results confirm that tensorized algorithms can significantly accelerate computations while maintaining solution quality comparable to their original CPU-based counterparts.
- p.13 conclusion: While tensorization has substantially improved algorithmic efficiency, opportunities remain to further optimize speed and memory use.
- p.13 conclusion: Future work will focus on refining key operators such as nondominated sorting and exploring new tensorized operators optimized for multi-GPU environments to maximize performance.
