---
key: XMB27RKI
title: "Multi-Rate Layered Operational Optimal Control for Large-Scale Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2021.3105487"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. OOC PROBLEM AND MULTI-RATE LAYERED CONTROL POLICY` → `III. BASIC LOOP LAYER CONTROLLER WITH BLOCK LIFTING AND MPC TECHNIGUES` → `IV. OPERATIONAL CONTROLLER WITH RECURSIVE LIFTING TECHNIQUE AND ACTOR CRITIC NETWORK` → `V. INDUSTRIAL APPLICATION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SOC / RTO / MPC / dual-rate RL）。Introduction 末有 `The rest of this article is organized as follows`。Method 在 III–IV。Experiments 标题为 `INDUSTRIAL APPLICATION`。

## Openers

- abstract: `In large-scale` — "In large-scale process industries, one of the great challenges is to achieve optimum operation of systems with multi-time-scale property and partially unknown models." (p.4749)
- introduction: `THE key problem` — "THE key problem in modern process industries is how to optimize operational indices, such as production efficiency and quality, materials and energy consumption, and so forth [1]." (p.4749)
- method: `In practical industrial` — "In practical industrial processes, the basic loop layer mainly includes multiple unit processes, which usually can be linearized near the operating points." (p.4751, III.A)
- experiments: `The proposed method` — "The proposed method is applied to dense medium separation (DMS) process of coal beneficiation." (p.4756, V)
- conclusion: `Fully considering the` — "Fully considering the multi-time-scale characteristics of two-layer industrial process control system with nonlinear and unknown operational process dynamics, this article innovatively combines lifting, MPC and actor-critic RL techniques to propose a multi-rate layered OOC method." (p.4760)

## Gap transitions

- however (introduction): "The industrial processes, however, are often with multiple interference sources or large disturbance variations that greatly hinder the satisfaction of SOC constraints." (p.4749)
- however (introduction): "However, as described in [2], [8], most RTO systems rely on the steady-state process models." (p.4749)
- therefore (introduction): "Therefore, the above methods cannot directly apply to practical large-scale process industries." (p.4750)
- to this end (abstract): "To this end, this article proposes a novel multi-rate layered operational optimal control (OOC) method, which employs lifting technique to unify the relatively fast dual-rate of basic loop layer and relatively slow single-rate of operational layer." (p.4749)
- motivated (introduction): "Motivated by this issue, this article proposes a novel multi-rate layered control method that focuses on how to combine the model with data to solve the OOC problem." (p.4750)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a novel multi-rate layered operational optimal control (OOC) method"; "this article innovatively combines lifting, MPC and actor-critic RL techniques to propose"
- prove / causal / abstract: "The convergence of the proposed method is proved"
- illustrate / causal / abstract: "dense medium separation (DMS) process is taken as an application case to illustrate the effectiveness of our proposed method"
- demonstrate / causal / conclusion: "the benefits of the proposed method are demonstrated via simulation studies"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section II discusses the OOC problem and multi-rate layered control strategy. Section III details the design of the basic loop layer controller with block lifting technique and MPC. Section IV reports the lifted basic closed-loop model and actor-critic RL algorithm. Section V introduces a typical DMS process and a self-developed simulation platform, and shows the experi-ment results. Finally, Section VI concludes this article." (p.4750)
- method → experiments: IV 收敛分析后 `V. INDUSTRIAL APPLICATION` (p.4756)
- experiments → conclusion: 扰动结果后 `VI. CONCLUSION` (p.4760)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The main contributions are briefly summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `To further strengthen` / `it would be meaningful` 指向后续。
- R009 结论 `this article innovatively combines ... to propose`。

## Candidate phrases

- `To this end, this article proposes a novel` (abstract)
- `Motivated by this issue, this article proposes` (introduction)
- `The main contributions are briefly summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `The proposed method is applied to` (experiments)

## House style

自称是 `this article proposes` / `our proposed method` / `this article innovatively combines`。未见 `Here we`、`In this paper`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.4749 abstract: In large-scale process industries, one of the great challenges is to achieve optimum operation of systems with multi-time-scale property and partially unknown models.
- p.4749 abstract: To this end, this article proposes a novel multi-rate layered operational optimal control (OOC) method, which employs lifting technique to unify the relatively fast dual-rate of basic loop layer and relatively slow single-rate of operational layer.
- p.4749 abstract: The convergence of the proposed method is proved, and dense medium separation (DMS) process is taken as an application case to illustrate the effectiveness of our proposed method via a self-developed simulation platform.
- p.4749 introduction: THE key problem in modern process industries is how to optimize operational indices, such as production efficiency and quality, materials and energy consumption, and so forth [1].
- p.4749 introduction: However, as described in [2], [8], most RTO systems rely on the steady-state process models.
- p.4750 introduction: Therefore, the above methods cannot directly apply to practical large-scale process industries.
- p.4750 introduction: Motivated by this issue, this article proposes a novel multi-rate layered control method that focuses on how to combine the model with data to solve the OOC problem.
- p.4750 introduction: The main contributions are briefly summarized as follows.
- p.4750 introduction: The rest of this article is organized as follows. Section II discusses the OOC problem and multi-rate layered control strategy. Section III details the design of the basic loop layer controller with block lifting technique and MPC. Section IV reports the lifted basic closed-loop model and actor-critic RL algorithm. Section V introduces a typical DMS process and a self-developed simulation platform, and shows the experi-ment results. Finally, Section VI concludes this article.
- p.4751 method: In practical industrial processes, the basic loop layer mainly includes multiple unit processes, which usually can be linearized near the operating points.
- p.4756 experiments: The proposed method is applied to dense medium separation (DMS) process of coal beneficiation.
- p.4758 experiments: From Fig. 6, it can be seen that the control policy obtained by the proposed method can control the operational index smoothly close to the expected value within 1200 s, achieving the optimal control of the operational index r.
- p.4760 conclusion: Fully considering the multi-time-scale characteristics of two-layer industrial process control system with nonlinear and unknown operational process dynamics, this article innovatively combines lifting, MPC and actor-critic RL techniques to propose a multi-rate layered OOC method.
- p.4760 conclusion: In such application study, the benefits of the proposed method are demonstrated via simulation studies, which are carried out on a METSIM-based simulation system.
- p.4760 conclusion: To further strengthen the effectiveness of the proposed method, a research-worthy problem would include the robustness improvement and the admissible controller independent algorithm.
- p.4760 conclusion: Besides, it would be meaningful and interesting to further reduce the resource utilization (e.g, data transfer, processing power, and energy consumption) of layered OOC system by using event-triggered technology.
