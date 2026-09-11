---
key: RV9HXXFB
title: "Data-Driven Robust Multimodal Multiobjective Particle Swarm Optimization"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2024.3357872"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. ROBUST MULTIMODAL MULTIOBJECTIVE PARTICLE SWARM OPTIMIZATION ALGORITHM` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 robust evolutionary optimization、regional scaling、peak detection，再收束到 MMOP 不确定性）。Introduction 末有节序路标，指向 Section II–V。Method 为 III，含 Algorithm 1。Experiments 标题为 `EXPERIMENTS`（benchmark + Kriging + WWTP/BSM2）。

## Openers

- abstract: `For the data-driven` — "For the data-driven multimodal multiobjective optimization problems (MMOPs), the inevitable uncertainties will lead to distortion of multiple peak landscapes, thus causing slow convergence in complex landscapes." (p.1)
- introduction: `MULTIMODAL multiobjective optimization` — "MULTIMODAL multiobjective optimization problems (MMOPs) are ubiquitous in real-world applications of the cybernetic field [1], [2], [3]." (p.1；栏首掉字)
- method: `An RMMPSO algorithm` — "An RMMPSO algorithm is designed to improve multimodal optimization performance in uncertain environments." (p.3, III)
- experiments: `In this section` — "In this section, to verify the optimization performance in MMOPDM, the proposed RMMPSO is compared with the advanced multimodal multiobjective optimization algorithms (MMOAs) by experiments." (p.7, IV)
- conclusion: `Although MMOPs are` — "Although MMOPs are common in reality, the weak resistance to uncertainties of multimodal optimization limits their application." (p.12)

## Gap transitions

- however (introduction): "However, these optimization problems are highly complex since all equivalent optimal solutions are required to be found in multimodal landscapes [4], [5], [6]." (p.1)
- although (introduction): "Although many advanced multimodal multiobjective optimization algorithms have been developed, they fail to provide reliable evolutionary optimization processes in the presence of uncertainties." (p.1)
- however (introduction): "However, the above robust evolutionary strategies were inapplicable for MMOPs in the presence of uncertainties, since these robust strategies lack sustained exploration abilities to cope with multiple peaks in complex multimodal fitness landscapes [4], [23], [24]." (p.2)
- however (introduction): "However, since the limitations of peak detection strategies on multiple objectives, the above method could not handle the uncertainties in MMOPs." (p.2)
- therefore (preliminaries): "Therefore, to solve MMOPDM, the diversity and convergence in both decision space and objective space of the approximation solution set are equally important." (p.2)
- although (conclusion): "Although MMOPs are common in reality, the weak resistance to uncertainties of multimodal optimization limits their application." (p.12)

## Hedge verbs

- design / causal / abstract, method: "a robust multimodal multiobjective particle swarm optimization (RMMPSO) is designed"; "An RMMPSO algorithm is designed"
- propose / causal / abstract, introduction, method: "a perturbation observer is proposed"; "An exploitation strategy based on Lipschitz constant estimation is proposed"; "This article proposes a robust multimodal multiobjective optimization (RMMPSO) to fill this gap."
- demonstrate / causal / abstract: "the effectiveness of RMMPSO is demonstrated"; "The results of experiments demonstrate the superiority of RMMPSO"
- show / causal / experiments: "The following parts show the specific results of the experiments."; "Table II lists the IGDx values"
- can / speculative / conclusion: "the proposed RMMPSO can guarantee superior optimization performance even in the presence of model uncertainties."

## Cross-section linkers

- introduction → preliminaries: "The remainder of this article is arranged as follows. Section II describes the preliminaries. Section III gives the approach. The simulation results are provided to demonstrate the effectiveness of the proposed RMMPSO in Section IV. Finally, the conclusion is given in Section V." (p.2)
- method → experiments: Algorithm 1 与 Remark 3 之后直接 `IV. EXPERIMENTS` (p.7)
- experiments → conclusion: WWTP 结果段落后直接 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `To solve this problem, a ... is designed` 收束方法名，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有鲁棒进化 / 多峰定位评述写在引言中段，再用 `Based on the above discussion` 转入贡献。
- R003 Introduction 末用 `The remainder of this article is arranged as follows` 指向 II–V。
- R004 贡献用 `The main contributions can be summarized as follows.` + 编号列表。
- R005 Conclusion 以 `Although` 收局限语境，再用 `This article proposes ... to fill this gap`，末段 `In further research` / `The future work should`。

## Candidate phrases

- `To solve this problem, a ... is designed to` (abstract)
- `Based on the above discussion, a ... is designed to` (introduction)
- `The main contributions can be summarized as follows.` (introduction)
- `The remainder of this article is arranged as follows.` (introduction)
- `This article proposes a ... to fill this gap.` (conclusion)

## House style

自称是 `this article` / `the proposed RMMPSO` / `we`（方法描述较少）。未见 `Here we`。`This article proposes` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: For the data-driven multimodal multiobjective optimization problems (MMOPs), the inevitable uncertainties will lead to distortion of multiple peak landscapes, thus causing slow convergence in complex landscapes.
- p.1 abstract: To solve this problem, a robust multimodal multiobjective particle swarm optimization (RMMPSO) is designed to alleviate slow convergence.
- p.1 abstract: Finally, the effectiveness of RMMPSO is demonstrated in terms of multiobjective multimodal benchmark problems with uncertain components and wastewater treatment simulation platform.
- p.1 abstract: The results of experiments demonstrate the superiority of RMMPSO in solving data-driven MMOPs compared to state-of-the-art multimodal multiobjective algorithms.
- p.1 introduction: MULTIMODAL multiobjective optimization problems (MMOPs) are ubiquitous in real-world applications of the cybernetic field [1], [2], [3].
- p.1 introduction: However, these optimization problems are highly complex since all equivalent optimal solutions are required to be found in multimodal landscapes [4], [5], [6].
- p.1 introduction: Although many advanced multimodal multiobjective optimization algorithms have been developed, they fail to provide reliable evolutionary optimization processes in the presence of uncertainties.
- p.2 introduction: However, the above robust evolutionary strategies were inapplicable for MMOPs in the presence of uncertainties, since these robust strategies lack sustained exploration abilities to cope with multiple peaks in complex multimodal fitness landscapes [4], [23], [24].
- p.2 introduction: However, since the limitations of peak detection strategies on multiple objectives, the above method could not handle the uncertainties in MMOPs.
- p.2 introduction: Based on the above discussion, a robust multimodal multiobjective particle swarm optimization (RMMPSO) is designed to alleviate slow convergence in complex landscapes enabled by model uncertainties, thus improving the parallel convergence capability of multimodality in uncertain environments.
- p.2 introduction: The main contributions can be summarized as follows.
- p.2 introduction: The remainder of this article is arranged as follows. Section II describes the preliminaries. Section III gives the approach. The simulation results are provided to demonstrate the effectiveness of the proposed RMMPSO in Section IV. Finally, the conclusion is given in Section V.
- p.2 preliminaries: Therefore, to solve MMOPDM, the diversity and convergence in both decision space and objective space of the approximation solution set are equally important.
- p.3 method: An RMMPSO algorithm is designed to improve multimodal optimization performance in uncertain environments.
- p.7 experiments: In this section, to verify the optimization performance in MMOPDM, the proposed RMMPSO is compared with the advanced multimodal multiobjective optimization algorithms (MMOAs) by experiments.
- p.9 experiments: The results indicate that the proposed RMMPSO gives the best results in most test instances.
- p.12 conclusion: Although MMOPs are common in reality, the weak resistance to uncertainties of multimodal optimization limits their application.
- p.12 conclusion: This article proposes a robust multimodal multiobjective optimization (RMMPSO) to fill this gap.
- p.12 conclusion: It can be concluded that the proposed RMMPSO can guarantee superior optimization performance even in the presence of model uncertainties.
- p.12 conclusion: In further research, it is expected to extend the proposed optimization algorithm to solve other important practical problems, including MMOPs with more than two objectives, and large-scale MMOPs.
