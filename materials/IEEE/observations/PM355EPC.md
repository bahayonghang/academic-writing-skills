---
key: PM355EPC
title: "Global Dependency Graph Network for Soft Sensing in Process Industry"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2024.3418477"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. SOFT SENSOR FRAMEWORK BASED ON GDGN` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 PLS/SVR/ANN、DL soft sensor、GNN graph learning）。Introduction 无 `The rest of this paper` 路标，贡献列表后直接进入 Preliminaries。Method 标题为框架名。Experiments 标题为 `CASE STUDY`（Pensim + cement clinker）。

## Openers

- abstract: `In the process` — "In the process industry, data-driven soft sensors enhance transparency by mapping the interdependencies among variables triggered by complex reactions." (p.1)
- introduction: `MONITORING product quality` — "MONITORING product quality in real-time within the process industry presents significant challenges due to technical and cost constraints [1], [2]." (p.1)
- preliminaries: `Process variables naturally` — "Process variables naturally depend on each other due to their physical connections." (p.3, II.A)
- method: `The implementation steps` — "The implementation steps of the GDGN-based soft sensor are depicted in Fig. 2, outlined as follows:" (p.3, III.A)
- experiments: `This section initially` — "This section initially validates the physical consistency of GDGN through Pensim [38], a simulated penicillin fermentation process, and subsequently confirms the model's effectiveness within a cement clinker production process." (p.5, IV)
- conclusion: `This work proposes` — "This work proposes a GDGN-based soft sensor, aiming at boosting both performance and explainability through the investigation of variable dependency." (p.10)

## Gap transitions

- yet (abstract): "Yet, they frequently fail to account for the global dependencies that span across spatial and temporal dimensions." (p.1)
- to tackle (abstract): "To tackle this gap, we propose a global dependency graph network (GDGN) soft sensor, informed by both prior knowledge and process data." (p.1)
- nevertheless (introduction): "Nevertheless, most DL-based soft sensors tend to implicitly rather than explicitly explore dependencies [15], which may lead to the models being misled by irrelevant dependencies, ultimately limiting their performance [16]." (p.1–2)
- however (introduction): "However, in practical applications, the accessible prior knowledge is often sparse, resulting in incomplete dependency graphs [25]." (p.2)
- thus (introduction): "Thus, the main challenge lies in effectively integrating process data with prior knowledge to accurately represent dependencies through meaningful graphs, thereby enhancing the utilization of GNNs in industrial soft sensors [30]." (p.2)
- to address (preliminaries): "To address this, process data are used to further refine the local dependency among the four variables, making it more comprehensive." (p.3)

## Hedge verbs

- propose / causal / abstract, conclusion: "we propose a global dependency graph network (GDGN) soft sensor"; "This work proposes a GDGN-based soft sensor"
- introduce / causal / introduction: "In this study, we introduce a global dependency graph network (GDGN) soft sensor"
- validate / causal / abstract, experiments: "The efficacy and physical coherence of the GDGN's prediction logic were validated through two distinct case studies."; "This section initially validates the physical consistency of GDGN"
- demonstrate / causal / experiments: "DL models demonstrate superior performance compared to non-DL models."
- illustrate / causal / conclusion: "Experimental evaluations conducted on the penicillin fermentation process and the cement clinker production process illustrate that GDGN not only outperforms traditional and contemporary methods"

## Cross-section linkers

- introduction → preliminaries: 贡献列表后直接 `II. PRELIMINARIES`，无 `The rest of this paper is organized as follows` (p.2–3)
- preliminaries → method: 问题陈述后 `III. SOFT SENSOR FRAMEWORK BASED ON GDGN` (p.3)
- method → experiments: Algorithm 1 后 `IV. CASE STUDY` (p.5)
- experiments → conclusion: 消融后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `To tackle this gap, we propose` + 方法缩写。
- R002 Introduction 无独立 Related Work，GNN / prior knowledge 评述写在引言中段。
- R003 Introduction 末无节序路标，贡献列表后直接 Preliminaries。
- R004 贡献用 `The main contributions include the following` + 编号列表。
- R005 Conclusion 用 `This work proposes` 收回，并用案例句证明 explainability。

## Candidate phrases

- `To tackle this gap, we propose a` (abstract)
- `In this study, we introduce a global dependency graph network (GDGN) soft sensor` (introduction)
- `The main contributions include the following:` (introduction)
- `This work proposes a GDGN-based soft sensor, aiming at` (conclusion)

## House style

自称是 `we propose` / `In this study, we introduce` / `This work` / `GDGN`。未见 `Here we`。`we propose` 与 `This work proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In the process industry, data-driven soft sensors enhance transparency by mapping the interdependencies among variables triggered by complex reactions.
- p.1 abstract: Yet, they frequently fail to account for the global dependencies that span across spatial and temporal dimensions.
- p.1 abstract: To tackle this gap, we propose a global dependency graph network (GDGN) soft sensor, informed by both prior knowledge and process data.
- p.1 abstract: The efficacy and physical coherence of the GDGN's prediction logic were validated through two distinct case studies.
- p.1 introduction: MONITORING product quality in real-time within the process industry presents significant challenges due to technical and cost constraints [1], [2].
- p.1–2 introduction: Nevertheless, most DL-based soft sensors tend to implicitly rather than explicitly explore dependencies [15], which may lead to the models being misled by irrelevant dependencies, ultimately limiting their performance [16].
- p.2 introduction: However, in practical applications, the accessible prior knowledge is often sparse, resulting in incomplete dependency graphs [25].
- p.2 introduction: Thus, the main challenge lies in effectively integrating process data with prior knowledge to accurately represent dependencies through meaningful graphs, thereby enhancing the utilization of GNNs in industrial soft sensors [30].
- p.2 introduction: In this study, we introduce a global dependency graph network (GDGN) soft sensor, structured around three core phases: learning local dependencies, constructing global dependencies, and elucidating the prediction process.
- p.2 introduction: The main contributions include the following:
- p.3 preliminaries: Process variables naturally depend on each other due to their physical connections.
- p.3 method: The implementation steps of the GDGN-based soft sensor are depicted in Fig. 2, outlined as follows:
- p.5 experiments: This section initially validates the physical consistency of GDGN through Pensim [38], a simulated penicillin fermentation process, and subsequently confirms the model's effectiveness within a cement clinker production process.
- p.7 experiments: Across all testing datasets, DL models demonstrate superior performance compared to non-DL models.
- p.9 experiments: The embedding of incomplete prior knowledge and the construction of the global dependency allows GDGN to achieve more advanced performance than GMCE.
- p.10 experiments: These ablation experiments show that incorporating local-global dependencies and prior knowledge enhances GDGN's performance.
- p.10 conclusion: This work proposes a GDGN-based soft sensor, aiming at boosting both performance and explainability through the investigation of variable dependency.
- p.10 conclusion: Experimental evaluations conducted on the penicillin fermentation process and the cement clinker production process illustrate that GDGN not only outperforms traditional and contemporary methods in soft-sensing efficacy but also enhances explainability.
