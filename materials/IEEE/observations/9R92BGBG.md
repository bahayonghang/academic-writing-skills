---
key: 9R92BGBG
title: "Multitask Particle Swarm Optimization With Dynamic On-Demand Allocation"
venue: "IEEE Transactions on Evolutionary Computation"
doi: "10.1109/TEVC.2022.3187512"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,5-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES AND PROBLEM FORMULATION` → `III. MULTITASK PARTICLE SWARM OPTIMIZATION WITH DYNAMIC ON-DEMAND ALLOCATION` → `IV. EXPERIMENT STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 MFEA、均等分配、显式 autocoding、分解式资源分配）。Introduction 末有节序路标，指向 Section II–V。

## Openers

- abstract: `Multitask optimization aims` — "Multitask optimization aims to solve multiple optimization problems in parallel utilizing a single population." (p.1015)
- introduction: `MULTITASK optimization (MTO)` — "MULTITASK optimization (MTO) has received extensive attention in evolutionary computation [1]." (p.1015；栏首掉字)
- method: `In this part, the` — "In this part, the basic concept of MTO and the basic framework of MTPSO are introduced as preliminaries." (p.1016, II)
- experiments: `In this part, simulation` — "In this part, simulation experiments are carried out for the benchmark problems of single-objective MTO and multiobjective MTO, respectively, to testify the effectiveness of MTPSO-DA." (p.1019, IV)
- conclusion: `A novel MTPSO-DA algorithm` — "A novel MTPSO-DA algorithm was introduced to dynamically allocate computing resources on demand in this article." (p.1024)

## Gap transitions

- however (abstract): "However, if the computing resources are limited, allocating the same computing resources to different tasks will cause resource waste and make complex tasks difficult to converge to the optimal solution." (p.1015)
- to address (abstract): "To address this issue, a multitask particle swarm optimization with a dynamic on-demand allocation strategy (MTPSO-DA) is proposed to dynamically allocate computing resources." (p.1015)
- however (introduction): "However, the method of random allocation for computing resources has unreliability, resulting in the waste of computing resources [10]." (p.1015)
- however (introduction): "However, the method of equal allocation can only play a mitigating role [12]." (p.1015)
- however (introduction): "However, the algorithm cannot reasonably allocate resources according to the characteristics of different tasks [15]." (p.1015)
- therefore (introduction): "Therefore, how to reasonably realize the dynamic allocation of computing resources according to the complexity of different tasks to promote the convergence of complex tasks is an urgent problem [30]." (p.1016)
- therefore (conclusion): "Therefore, the MTPSO-DA algorithm designed in this article has opened up a very effective research direction for the allocation of computing resources in MTO." (p.1025)

## Hedge verbs

- propose / causal / abstract, introduction: "a multitask particle swarm optimization with a dynamic on-demand allocation strategy (MTPSO-DA) is proposed"; "The task complexity index is proposed"
- indicate / causal / abstract: "The results indicate that the proposed MTPSO-DA algorithm can achieve dynamic resource allocation."
- demonstrate / causal / experiments: "The experimental results demonstrate that the strategy can dynamically allocate computing resources according to the complexity of tasks."
- show / causal / conclusion: "The results showed the superiority of MTPSO-DA."

## Cross-section linkers

- introduction → method: "The remainder of this article is arranged as follows. Section II briefly gives an overview of the basic concepts related to MTO and multitask PSO (MTPSO). Section III describes the MTPSO-DA algorithm in detail. Section IV analyzes the experimental results. Finally, this article is concluded in Section V." (p.1016)
- method → experiments: 按需分配策略段落后接 `IV. EXPERIMENT STUDIES` (p.1019)
- experiments → conclusion: IGD+ 箱线图分析后接 `V. CONCLUSION` (p.1024)

## Candidate rules

- R001 贡献用 `Concretely, the main contributions of this article are listed as the following three parts.` + 编号列表。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is arranged as follows` 指向 II–V。
- R004 实验节标题用 `EXPERIMENT STUDIES`（单数 EXPERIMENT）。
- R005 Conclusion 用过去时收回方法（`was introduced` / `was proposed` / `The results showed`），再用 `In the future, the MTPSO-DA algorithm will be applied`。

## Candidate phrases

- `To address this issue, a ... is proposed to` (abstract)
- `Motivated by the above discussion, a ... is designed` (introduction)
- `Concretely, the main contributions of this article are listed as the following three parts.` (introduction)
- `The remainder of this article is arranged as follows.` (introduction)
- `A novel MTPSO-DA algorithm was introduced ... in this article.` (conclusion)
- `In the future, the MTPSO-DA algorithm will be applied to practical engineering` (conclusion)

## House style

自称是 `this article` / `the proposed MTPSO-DA algorithm` / `the proposed algorithm`。未见 `Here we`。`in this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1015 abstract: Multitask optimization aims to solve multiple optimization problems in parallel utilizing a single population.
- p.1015 abstract: However, if the computing resources are limited, allocating the same computing resources to different tasks will cause resource waste and make complex tasks difficult to converge to the optimal solution.
- p.1015 abstract: To address this issue, a multitask particle swarm optimization with a dynamic on-demand allocation strategy (MTPSO-DA) is proposed to dynamically allocate computing resources.
- p.1015 abstract: The results indicate that the proposed MTPSO-DA algorithm can achieve dynamic resource allocation.
- p.1015 introduction: MULTITASK optimization (MTO) has received extensive attention in evolutionary computation [1].
- p.1015 introduction: Therefore, how to allocate computing resources to tasks of different difficulty in the MTO evolutionary process is a challenging problem [4].
- p.1015 introduction: However, the method of random allocation for computing resources has unreliability, resulting in the waste of computing resources [10].
- p.1016 introduction: Therefore, how to reasonably realize the dynamic allocation of computing resources according to the complexity of different tasks to promote the convergence of complex tasks is an urgent problem [30].
- p.1016 introduction: Motivated by the above discussion, a multitask particle swarm optimization with a dynamic on-demand allocation strategy (MTPSO-DA) is designed to realize the dynamic computing resource allocation.
- p.1016 introduction: Concretely, the main contributions of this article are listed as the following three parts.
- p.1016 introduction: The remainder of this article is arranged as follows.
- p.1016 method: In this part, the basic concept of MTO and the basic framework of MTPSO are introduced as preliminaries.
- p.1019 experiments: In this part, simulation experiments are carried out for the benchmark problems of single-objective MTO and multiobjective MTO, respectively, to testify the effectiveness of MTPSO-DA.
- p.1023 experiments: The experimental results demonstrate that the strategy can dynamically allocate computing resources according to the complexity of tasks.
- p.1024 conclusion: A novel MTPSO-DA algorithm was introduced to dynamically allocate computing resources on demand in this article.
- p.1025 conclusion: The results showed the superiority of MTPSO-DA.
- p.1025 conclusion: Therefore, the MTPSO-DA algorithm designed in this article has opened up a very effective research direction for the allocation of computing resources in MTO.
- p.1025 conclusion: In the future, the MTPSO-DA algorithm will be applied to practical engineering to demonstrate its effectiveness.
