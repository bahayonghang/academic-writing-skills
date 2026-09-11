---
key: 4HRZG3NI
title: "Generalized Multi-Objective Reinforcement Learning With Envelope Updates in URLLC-Enabled Vehicular Networks"
venue: "IEEE Transactions on Vehicular Technology"
doi: "10.1109/TVT.2025.3580502"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-17"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. SYSTEM MODEL AND ASSUMPTIONS` → `III.`（MOMDP：state / action / rewards）→ `IV. MULTI-POLICY ENVELOPE MORL ALGORITHM` → `V. SIMULATION AND PERFORMANCE EVALUATION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 DQN / MORL / collision-avoidance，并以 `Table I` 对照已有工作）。Introduction 末有节序路标，指向 Section II–VI。Method 拆为 system model、MOMDP 与 envelope 算法。Experiments 标题为 `SIMULATION AND PERFORMANCE EVALUATION`。附录给单策略 MO-DQN / MO-DDQN。

## Openers

- abstract: `We develop a` — "We develop a novel multi-objective reinforcement learning (MORL) framework to jointly optimize wireless network selection and autonomous driving policies in a multi-band vehicular network operating on conventional sub-6 GHz spectrum and Terahertz frequencies." (p.17666)
- introduction: `FACILITATING ultra-reliable` — "FACILITATING ultra-reliable and low-latency vehicle-to-infrastructure (V2I) communications is a fundamental prerequisite for the realization of autonomous and intelligent transportation systems." (p.17666)
- method: `In contrast to` — "In contrast to conventional DRL, MORL requires the agent to optimize multiple objectives simultaneously." (p.17671, IV)
- experiments: `In this section` — "In this section, we demonstrate the performance of the proposed algorithms and highlight the complex dynamics between wireless connectivity, traffic flow, and AV's speed." (p.17675, V)
- conclusion: `We introduce a` — "We introduce a novel MORL framework tailored for devising joint network selection and autonomous driving policies within a multi-band VNet." (p.17679)

## Gap transitions

- however (introduction): "However, their system model includes only a single BS where handovers (HOs) are not considered." (p.17666)
- to address (abstract): "To address this, we apply a generalized version of the Bellman equation and optimize the convex envelope of multi-objective Q values to learn a unified parametric representation capable of generating optimal policies across all possible preference configurations." (p.17666)
- unlike (introduction): "Unlike scalarized methods, our MO-DDQN-Envelope approach dynamically adjusts preferences, mitigating biases and errors introduced by fixed weightings." (p.17667)
- in contrast (method): "In contrast to single-policy methods, multi-policy MORL methods optimize different objectives simultaneously by maximizing a vector of rewards associated with these objectives." (p.17672)
- although (method): "Although single-policy methods are adequate when we possess prior knowledge of task preferences, the acquired policy is constrained in its adaptability to situations" (p.17671)

## Hedge verbs

- develop / causal / abstract, introduction: "We develop a novel multi-objective reinforcement learning (MORL) framework"; "We develop an MORL framework to design joint network selection"
- propose / causal / introduction, method: "We propose a novel multi-objective MO-DDQN-Envelope"; "A multiple-policy envelope solution for MORL is proposed"
- demonstrate / causal / abstract, conclusion: "Numerical results validate the efficacy"; "Numerical results demonstrate the superiority of our proposed solution"
- show / causal / introduction: "Numerical results shows that the proposed solution outperforms weighted sum-based MORL solutions"
- could / speculative / conclusion: "Future research could enhance the generalization of the MORL model"

## Cross-section linkers

- introduction → system model: "The rest of this work is organized as follows. Section II shows the system model, and Section III provides MOMDP formulation. Section IV introduces the proposed solution. The simulations are presented in SectionV, and SectionVI concludes this research work." (p.17668)
- method → experiments: 复杂度段落后接 `V. SIMULATION AND PERFORMANCE EVALUATION` (p.17675)
- experiments → conclusion: 训练时间比较后直接 `VI. CONCLUSION` (p.17679)

## Candidate rules

- R001 abstract 用 `We develop a novel ... framework`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段，并用 `Table I` 对照。
- R003 贡献用编号子弹（`We develop` / `We propose` / `Numerical results shows`）。
- R004 Introduction 末用 `The rest of this work is organized as follows` 指向 II–VI。
- R005 Conclusion 先收回框架，再用百分数对照，`Future research could` 指向后续。

## Candidate phrases

- `We develop a novel multi-objective reinforcement learning (MORL) framework to jointly optimize` (abstract)
- `Different from the existing research, our contributions can be explained from two perspectives` (introduction)
- `The rest of this work is organized as follows.` (introduction)
- `In this section, we demonstrate the performance of the proposed algorithms` (experiments)
- `Numerical results demonstrate the superiority of our proposed solution over` (conclusion)
- `Future research could enhance the generalization of the MORL model` (conclusion)

## House style

自称是 `We develop` / `we develop` / `We propose` / `our contributions` / `our agent`。脚注出现 `in this paper`。未见 `Here we`。`We develop` 与 `this paper` 进 phrase_bank，不进 anti_ai_patterns。结论用现在时 `We introduce`。

## Quotes

- p.17666 abstract: We develop a novel multi-objective reinforcement learning (MORL) framework to jointly optimize wireless network selection and autonomous driving policies in a multi-band vehicular network operating on conventional sub-6 GHz spectrum and Terahertz frequencies.
- p.17666 abstract: To address this, we apply a generalized version of the Bellman equation and optimize the convex envelope of multi-objective Q values to learn a unified parametric representation capable of generating optimal policies across all possible preference configurations.
- p.17666 abstract: Numerical results validate the efficacy of the envelope-based MORL solution and demonstrate interesting insights related to the inter-dependency of vehicle motion dynamics, HOs, and the communication data rate.
- p.17666 introduction: FACILITATING ultra-reliable and low-latency vehicle-to-infrastructure (V2I) communications is a fundamental prerequisite for the realization of autonomous and intelligent transportation systems.
- p.17666 introduction: However, their system model includes only a single BS where handovers (HOs) are not considered.
- p.17667 introduction: To date, none of the existing research works [2], [3], [4], [6], [7], [8], [9], [10], [11], [13], [14], [15], [16], [17], [18], [23] have considered the inter-dependency of the AV motion dynamics to wireless data rates.
- p.17667 introduction: Unlike scalarized methods, our MO-DDQN-Envelope approach dynamically adjusts preferences, mitigating biases and errors introduced by fixed weightings.
- p.17667–17668 introduction: Numerical results shows that the proposed solution outperforms weighted sum-based MORL solutions with DQN by 12.7%, 18.9%, and 12.3% on average transportation reward, average communication reward, and average HO rate, respectively.
- p.17668 introduction: The rest of this work is organized as follows. Section II shows the system model, and Section III provides MOMDP formulation. Section IV introduces the proposed solution. The simulations are presented in SectionV, and SectionVI concludes this research work.
- p.17671 method: In contrast to conventional DRL, MORL requires the agent to optimize multiple objectives simultaneously.
- p.17672 method: In contrast to single-policy methods, multi-policy MORL methods optimize different objectives simultaneously by maximizing a vector of rewards associated with these objectives.
- p.17675 experiments: In this section, we demonstrate the performance of the proposed algorithms and highlight the complex dynamics between wireless connectivity, traffic flow, and AV's speed.
- p.17679 conclusion: We introduce a novel MORL framework tailored for devising joint network selection and autonomous driving policies within a multi-band VNet.
- p.17679 conclusion: Numerical results demonstrate the superiority of our proposed solution over weighted sum-based MORL solutions with DQN, showcasing improvements of 12.7%, 18.9%, and 12.3% on average transportation reward, average telecommunication reward, and average HO rate, respectively.
- p.17679 conclusion: Future research could enhance the generalization of the MORL model to better adapt to dynamic traffic conditions using well-established strategies such as meta-learning [50].
