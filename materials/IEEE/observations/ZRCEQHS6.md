---
key: ZRCEQHS6
title: "When Process Control Meets Big Data: Data-Driven Cloud-Edge Collaborative Predictive Control Method for Multiple Operating Conditions Processes"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2025.3582880"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. METHODOLOGY` → `III. ILLUSTRATIVE EXAMPLES` → `IV. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 MPC / CCS / explicit MPC / 多工况）。Introduction 末有编号贡献与节序路标，指向 Section II–IV。Method 标题为 `METHODOLOGY`。Experiments 标题为 `ILLUSTRATIVE EXAMPLES`（数值仿真 + CSTR）。

## Openers

- abstract: `Complex industrial processes` — "Complex industrial processes often run under varying operating conditions." (p.1)
- introduction: `INDUSTRIAL development is` — "INDUSTRIAL development is important for social and economic progress [1], [2], [3]." (p.1；栏首掉字排成 `I` / `NDUSTRIAL`)
- method: `The proposed DCECPC` — "The proposed DCECPC includes tasks in the cloud: parallel subspace identification, explicit MPC; and tasks at the edge: real-time control, model mismatch detection; and model updating in the transition stage." (p.2, II)
- experiments: `To quantitatively evaluate` — "To quantitatively evaluate the effectiveness, we use two metrics, the mean square error (MSE) and the integrated absolute error (IAE), which are defined as follows:" (p.7, III.A)
- conclusion: `In this article` — "In this article, a data-driven cloud-edge collaborative control method is proposed to cope with the problem of model mismatch due to the emergence of new operating conditions in industrial processes." (p.12)

## Gap transitions

- however (abstract): "However, in traditional control frameworks, due to the limitation of computational and storage resources of edge devices, control strategies are difficult to update once deployed, which leads to model mismatch after operating condition change and seriously reduces the control performance." (p.1)
- to solve (abstract): "To solve this problem, this article proposes a novel cloud-edge collaborative control method." (p.1)
- however (introduction): "However, traditional MPC often requires large amounts of process data to obtain the predictive model." (p.1)
- although (introduction): "Although there are some control schemes for multiple operating condition processes, these schemes are designed for known operating conditions [17]." (p.2)
- therefore (introduction): "Therefore, some new architectures and control schemes are necessary to cope with the new operating conditions that are constantly emerging in complex industrial processes." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a novel cloud-edge collaborative control method"; "this article proposes a data-driven cloud-edge collaborative predictive control (DCECPC) method"; "a data-driven cloud-edge collaborative control method is proposed"
- verify / causal / abstract: "Finally, extensive experiments verified the superiority of the proposed method."
- ensure / causal / introduction: "This scheme ensures stable control under changing operating conditions."
- can / speculative / method, conclusion: "the proposed cloud-edge collaborative control scheme can adapt to an infinite number of new operating conditions theoretically"; "the proposed method can cope well with the changing operating conditions"

## Cross-section linkers

- introduction → method: "The remainder of this article is structured as follows. In Section II, the proposed cloud-edge collaborative control scheme is described, including parallel subspace identification and explicit MPC in the cloud; real-time control and model mismatch detection at the edge; and excitation strategy in transition stage. In Section III, numerical simulation and CSTR process experiments verify the superiority of the proposed method. Finally, our method is concluded in Section IV." (p.2)
- method → experiments: 过渡阶段结束后接 `III. ILLUSTRATIVE EXAMPLES` (p.7)
- experiments → conclusion: CSTR 控制段落后直接 `IV. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 贡献句用 `this article proposes`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 贡献用 `In summary, the main contributions of this article are as follows.` + 编号列表。
- R004 Introduction 末用 `The remainder of this article is structured as follows` 指向 II–IV。
- R005 Conclusion 先收回方法，再用实验三项（training efficiency / control time / control effectiveness）收束；未见独立 future-work 句。

## Candidate phrases

- `To solve this problem, this article proposes` (abstract)
- `In summary, the main contributions of this article are as follows.` (introduction)
- `The remainder of this article is structured as follows.` (introduction)
- `To quantitatively evaluate the effectiveness, we use two metrics` (experiments)
- `In this article, a data-driven cloud-edge collaborative control method is proposed to cope with` (conclusion)
- `The superiority of the proposed method is extensively verified through experiments` (conclusion)

## House style

自称是 `this article proposes` / `this article` / `we propose` / `our method`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。结论用现在时被动 `is proposed`。

## Quotes

- p.1 abstract: Complex industrial processes often run under varying operating conditions.
- p.1 abstract: However, in traditional control frameworks, due to the limitation of computational and storage resources of edge devices, control strategies are difficult to update once deployed, which leads to model mismatch after operating condition change and seriously reduces the control performance.
- p.1 abstract: To solve this problem, this article proposes a novel cloud-edge collaborative control method.
- p.1 abstract: Finally, extensive experiments verified the superiority of the proposed method.
- p.1 introduction: INDUSTRIAL development is important for social and economic progress [1], [2], [3].
- p.1 introduction: However, traditional MPC often requires large amounts of process data to obtain the predictive model.
- p.2 introduction: Although there are some control schemes for multiple operating condition processes, these schemes are designed for known operating conditions [17].
- p.2 introduction: Therefore, some new architectures and control schemes are necessary to cope with the new operating conditions that are constantly emerging in complex industrial processes.
- p.2 introduction: In summary, the main contributions of this article are as follows.
- p.2 introduction: The remainder of this article is structured as follows. In Section II, the proposed cloud-edge collaborative control scheme is described, including parallel subspace identification and explicit MPC in the cloud; real-time control and model mismatch detection at the edge; and excitation strategy in transition stage. In Section III, numerical simulation and CSTR process experiments verify the superiority of the proposed method. Finally, our method is concluded in Section IV.
- p.2 method: The proposed DCECPC includes tasks in the cloud: parallel subspace identification, explicit MPC; and tasks at the edge: real-time control, model mismatch detection; and model updating in the transition stage.
- p.7 experiments: To quantitatively evaluate the effectiveness, we use two metrics, the mean square error (MSE) and the integrated absolute error (IAE), which are defined as follows:
- p.12 experiments: In conclusion, the proposed method can cope well with the changing operating conditions of the CSTR process and provide good control performance.
- p.12 conclusion: In this article, a data-driven cloud-edge collaborative control method is proposed to cope with the problem of model mismatch due to the emergence of new operating conditions in industrial processes.
- p.12 conclusion: The superiority of the proposed method is extensively verified through experiments in terms of training efficiency, control time, and control effectiveness.
