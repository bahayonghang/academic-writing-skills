---
key: HEWSK8HQ
title: "Development of data-knowledge-driven predictive model and multi-objective optimization for intelligent optimal control of aluminum electrolysis process"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2024.108664"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Problem formulation` → `3. WCA-NARX network` → `4` 运行优化与决策 → `5. Case study` → `6. Conclusion`。前置 `ABSTRACT`、`ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段机理模型、MPC、无模型控制与数据驱动决策）。Introduction 末有编号贡献 + 节序路标。路标用 `Section II`–`Section VI`，正文标题用阿拉伯数字。Experiments 标题为 `Case study`。

## Openers

- abstract: `Operational optimization of` — "Operational optimization of the Hall-Héroult cell is essential for achieving high efficiency and cost-effectiveness in the aluminum electrolysis process."
- introduction: `It is well known` — "It is well known in the aluminum community that the aluminum electrolysis industry is developing towards being environment-friendly and resource-saving due to legal constraints and energy tension"
- method: `WCA-NARX network is` — "WCA-NARX network is designed for the multi-input and single-output dynamic system consisting of working-conditions-based attention (WCA) module and nonlinear autoregressive network with exogenous input (NARX) network, as shown in Fig. 3." (s.3)
- experiments: `Our research team designed` — "Our research team designed the distributed control system for electrolytic cell in Qingtongxia, China, which was implemented using C# and SQL Server."
- conclusion: `In this paper` — "In this paper, we developed a DMSS for operational optimization in the aluminum electrolysis process."

## Gap transitions

- due to (abstract): "Due to the complicated mechanism and variable working conditions, manual operational decision-making is extensively used in practice."
- however (introduction): "However, this type of control method cannot meet more refined production requirements with the growing market demands"
- however (introduction): "However, the above mentioned data-driven decision-making methods cannot break through the bottleneck of historical optimal operation because these methods only learn the historical optimal operation without further optimization."
- although (introduction): "Although these data-driven decision-making optimization methods can improve control performance in some aspects, directly using these data-driven approaches in real-world aluminum electrolysis process may not satisfy the actual industrial requirements"
- therefore (introduction): "Therefore, the existing decision-making approaches cannot be readily applied to real-world applications."

## Hedge verbs

- develop / causal / abstract, introduction, conclusion: "we develop a data-knowledge-driven decision-making support system"; "This paper presents"; "we developed a DMSS"
- propose / causal / abstract, introduction: "we propose a working-conditions-based attention"; "we propose a novel WCA-NARX"
- demonstrate / causal / abstract: "Real-world industrial experiments demonstrate that DMSS can effectively enhance control performance"
- showed / associative / conclusion: "The experiments on the real-world aluminum electrolysis process showed that the proposed WCA-NARX network can achieve high-performance HBI prediction."

## Cross-section linkers

- introduction → method: "The remainder of this article first introduces the decision-making problem in Section II. In Section III, we describe the WCA-NARX network. Subsequently, the operation optimization module is developed in Section IV. Section V presents our experiments on the aluminum electrolysis process. Section VI concludes this paper."
- method → experiments: 知识引导决策段落后 `5. Case study`
- experiments → conclusion: 工业对比表后 `6. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remainder of this article first introduces`，路标用罗马数字、正文用阿拉伯数字。
- R004 编号贡献：`The main contributions to the proposed DMSS are as follows.`
- R009 自称：`In this paper, we develop` / `This paper presents`

## Candidate phrases

- `In this paper, we develop a data-knowledge-driven` (abstract)
- `This paper presents a data-knowledge-driven decision-making support system (DMSS)` (introduction)
- `The main contributions to the proposed DMSS are as follows.` (introduction)
- `The remainder of this article first introduces` (introduction)
- `In this paper, we developed a DMSS for operational optimization` (conclusion)

## House style

自称 `In this paper, we develop` / `This paper presents` / `we propose` / `we developed`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Operational optimization of the Hall-Héroult cell is essential for achieving high efficiency and cost-effectiveness in the aluminum electrolysis process.
- abstract: In this paper, we develop a data-knowledge-driven decision-making support system (DMSS) to achieve operational optimization for the aluminum electrolysis process.
- abstract: Real-world industrial experiments demonstrate that DMSS can effectively enhance control performance and achieve superior results compared to other competitive methods.
- introduction: It is well known in the aluminum community that the aluminum electrolysis industry is developing towards being environment-friendly and resource-saving due to legal constraints and energy tension
- introduction: Although these data-driven decision-making optimization methods can improve control performance in some aspects, directly using these data-driven approaches in real-world aluminum electrolysis process may not satisfy the actual industrial requirements, as these purely data-driven methods lack guidance from practical experience and knowledge, making the decision results difficult to convince and sometimes even leading to spectacular failures.
- introduction: This paper presents a data-knowledge-driven decision-making support system (DMSS) for the aluminum electrolysis process, which aims at achieving operational optimization by considering the HBI indicator and the operational cost indicator (OCI).
- introduction: The main contributions to the proposed DMSS are as follows.
- introduction: The remainder of this article first introduces the decision-making problem in Section II. In Section III, we describe the WCA-NARX network. Subsequently, the operation optimization module is developed in Section IV. Section V presents our experiments on the aluminum electrolysis process. Section VI concludes this paper.
- method: WCA-NARX network is designed for the multi-input and single-output dynamic system consisting of working-conditions-based attention (WCA) module and nonlinear autoregressive network with exogenous input (NARX) network, as shown in Fig. 3.
- experiments: Our research team designed the distributed control system for electrolytic cell in Qingtongxia, China, which was implemented using C# and SQL Server.
- experiments: Compared to the manual decision-making strategy, HBI can be improved from 3.63 to 0.71 and OCI can be improved from 1.27 to 0.46 by utilizing the DMSS-provided control strategy
- conclusion: In this paper, we developed a DMSS for operational optimization in the aluminum electrolysis process.
- conclusion: Real-world experiments showed that the proposed DMSS achieved optimization results both in HBI and OCI.
- conclusion: In the future work, we will explore how to incrementally update the HBI prediction model by using optimization cases.
