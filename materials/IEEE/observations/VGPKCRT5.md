---
key: VGPKCRT5
title: "Operational Optimal Tracking Control for Industrial Multirate Systems Subject to Unknown Disturbances"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2023.3305245"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARY` → `III. MPC-BASED TRACKING CONTROLLER DESIGN FOR THE BASIC LOOP` → `IV.`（操作回路优化控制器）→ `V. SIMULATIONS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 RTO/MPC、RL/ADP、多速率、DOB）。Introduction 末有节序路标，指向 Section II–VI。

## Openers

- abstract: `It is well common` — "It is well common for industrial processes to employ a hierarchical control structure involving a basic loop process and an operation loop process with two timescales." (p.180)
- introduction: `OPERATIONAL optimal control` — "OPERATIONAL optimal control of industrial processes has gained wide attention, as it not only establishes distinct control boundaries for various tasks but also improves plant stability, control performance, and profitability [1]." (p.180；栏首掉字)
- method: `The main idea of` — "The main idea of the operational optimal control of industrial processes is to determine the optimal basic loop setpoints as well as to ensure that the corresponding outputs can achieve fast and accurate setpoint tracking." (p.182, II)
- experiments: `In this section, a` — "In this section, a simplified ball mill grinding process is studied as an academic example to verify the effectiveness of the proposed control method." (p.188, V)
- conclusion: `In this article, a` — "In this article, a novel operation optimal tracking control method is proposed to address the multirate problem and unknown disturbances for industrial processes with hierarchical structures." (p.190)

## Gap transitions

- however (abstract): "However, the control system suffers from another multirate challenge where control and sampling rates may differ even within a single loop." (p.180)
- to overcome (abstract): "To overcome these problems, this article develops a novel operational optimal tracking control method for a class of multirate systems subject to unknown disturbances." (p.180)
- however (introduction): "However, in most cases, RTO heavily relies on nonlinear steady-state models, in which model mismatch and disturbances can result in great offset." (p.180)
- however (introduction): "However, if proper precautions are not taken, the control performance may suffer due to inefficient computation and poor implementation" (p.181)
- however (introduction): "However, these control methods are too conservative and incapable of handling unknown disturbances [27]." (p.181)
- while (conclusion): "While the lifting strategy has proved effective in tackling the multirate control issue, it becomes less feasible when state or input constraints are presented." (p.191)

## Hedge verbs

- develop / causal / abstract: "this article develops a novel operational optimal tracking control method"
- propose / causal / introduction, conclusion: "This motivation drives our study to propose a novel operational optimal tracking control approach"; "a novel operation optimal tracking control method is proposed"
- verify / causal / abstract, experiments: "tangible improvements are verified by simulations"; "to verify the effectiveness of the proposed control method"
- indicate / causal / experiments: "The results also indicate that considering the unknown disturbances or not will have a great influence"

## Cross-section linkers

- introduction → method: "The remainder of this article is organized as follows. Section II gives the preliminary of this work. Section III presents a lifting technique as well as the design of an MPC-based tracking controller for the basic loop process. In Section IV, the optimization controller design for the operation loop process is described. Sections V and VI provide simulation results and conclusions, respectively." (p.181–182)
- method → experiments: Theorem 2 稳定性证明后接 `V. SIMULATIONS` (p.188)
- experiments → conclusion: 仿真总结段落后直接 `VI. CONCLUSION` (p.190)

## Candidate rules

- R001 贡献用 `The main contributions of this article are as follows.` + 编号列表。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R004 实验节标题用 `SIMULATIONS` 而非 `EXPERIMENTS`。
- R005 Conclusion 用 `While` 承认局限，再用 `Future work will need to` 指向后续。

## Candidate phrases

- `To overcome these problems, this article develops` (abstract)
- `The main contributions of this article are as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `To this end, this article integrates` (preliminary)
- `In this article, a novel operation optimal tracking control method is proposed` (conclusion)

## House style

自称是 `this article` / `this study` / `our method` / `the proposed method`。未见 `Here we`。`this article develops` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.180 abstract: It is well common for industrial processes to employ a hierarchical control structure involving a basic loop process and an operation loop process with two timescales.
- p.180 abstract: However, the control system suffers from another multirate challenge where control and sampling rates may differ even within a single loop.
- p.180 abstract: To overcome these problems, this article develops a novel operational optimal tracking control method for a class of multirate systems subject to unknown disturbances.
- p.180 abstract: The convergence of the proposed method is analyzed and tangible improvements are verified by simulations.
- p.180 introduction: OPERATIONAL optimal control of industrial processes has gained wide attention, as it not only establishes distinct control boundaries for various tasks but also improves plant stability, control performance, and profitability [1].
- p.180 introduction: However, in most cases, RTO heavily relies on nonlinear steady-state models, in which model mismatch and disturbances can result in great offset.
- p.181 introduction: However, these control methods are too conservative and incapable of handling unknown disturbances [27].
- p.181 introduction: This motivation drives our study to propose a novel operational optimal tracking control approach.
- p.181 introduction: The main contributions of this article are as follows.
- p.181 introduction: The remainder of this article is organized as follows.
- p.182 method: The main idea of the operational optimal control of industrial processes is to determine the optimal basic loop setpoints as well as to ensure that the corresponding outputs can achieve fast and accurate setpoint tracking.
- p.182 method: To this end, this article integrates a model-based basic loop controller and a data-driven optimization controller to address the aforementioned problems to achieve the operational optimal control of the entire system.
- p.188 experiments: In this section, a simplified ball mill grinding process is studied as an academic example to verify the effectiveness of the proposed control method.
- p.189 experiments: The data shows that our method can effectively suppress unknown disturbances.
- p.190 conclusion: In this article, a novel operation optimal tracking control method is proposed to address the multirate problem and unknown disturbances for industrial processes with hierarchical structures.
- p.191 conclusion: While the lifting strategy has proved effective in tackling the multirate control issue, it becomes less feasible when state or input constraints are presented.
- p.191 conclusion: Future work will need to address this issue from both theoretical and practical perspectives, with an additional focus on simplifying the design process of the lifted basic loop controller to enhance flexibility for real-world implementation.
