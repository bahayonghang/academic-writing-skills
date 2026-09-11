---
key: FXKHNQWR
title: "Sequential Inverse Optimal Control of Discrete-Time Systems"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2023.123762"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. Introduction` → `II. Problem Formulation` → `III. Sequential IOC for the Noise Free Case` → 噪声情形（Algorithm 2）→ `V. Simulation Examples` → `VI. Discussion` → `VII. Conclusion`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 bilevel IOC / PMP / Euler-Lagrange / 在线 IOC [16] / CLF-based IOC / 噪声 IOC）。Introduction 贡献为编号 1)–3)，无 `The rest of this paper is organized as follows` 路标。Method 为 II–IV。Experiments 标题为 `Simulation Examples`。页码 608–621。

## Openers

- abstract: `This paper presents` — "This paper presents a novel sequential inverse optimal control (SIOC) method for discrete-time systems, which calculates the unknown weight vectors of the cost function in real time using the input and output of an optimally controlled discrete-time system." (p.1)
- introduction: `THE standard optimal` — "THE standard optimal control problem concerns finding the state and input trajectories for a dynamical system." (p.1；栏首掉字)
- method: `Consider the dynamics` — "Consider the dynamics of a discrete system" (p.3, II)
- experiments: `We perform several` — "We perform several simulations in different cases to verify the effectiveness of our method." (p.8, V)
- conclusion: `A sequential method` — "A sequential method for discrete-time IOC is presented in this paper to realize the online estimation of cost weights for either finite or infinite horizon optimal control in cases with significant data noise." (p.11, VII)

## Gap transitions

- conversely (introduction): "Conversely, the second class of IOC research focus on solving this problem by exploiting several optimality equations, such as Pontryagin’s maximum principle-based equations [13], and Euler-Lagrange equations [2]." (p.2)
- however (introduction): "In [16], a method is proposed for the online calculation of discrete-time IOC in both finite and infinite horizons; however, it requires the invertibility condition of a Jacobian." (p.2)
- despite (introduction): "Despite these advancements, notable limitations of CLF-based IOC method persist, including the inability to explicitly specify a clear optimal cost function and the difficulty in selecting and adjusting parameters" (p.2)
- although (introduction): "Although the aforementioned methods are effective in tackling problems of noise for the offline IOC problem of discrete-time finite-horizon LQR, it is still necessary to consider the noisy problem in the IOC method in (1) online calculation and (2) nonlinear system’s IOC method." (p.2)
- although (discussion): "Although the problem of sequential IOC has been solved in this study considering the calculation speed and noisy data, the algorithm still requires improvement in the following areas." (p.11)

## Hedge verbs

- present / causal / abstract, conclusion: "This paper presents a novel sequential inverse optimal control (SIOC) method"; "A sequential method for discrete-time IOC is presented in this paper"
- propose / causal / introduction: "This paper proposes a novel SIOC method to address the issues mentioned above."
- demonstrate / causal / abstract: "The effectiveness of the proposed method is demonstrated through simulation results."
- can / speculative / experiments: "Therefore, our proposed method can effectively improve the calculation speed while preserving the recovery accuracy of IOC."

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. Problem Formulation` (p.3)
- method → experiments: Algorithm 2 后直接 `V. Simulation Examples` (p.8)
- experiments → discussion: "From Simulation 4, it is evident that the proposed method can effectively tackle the noise problem" 随后 `VI. Discussion` (p.10)
- discussion → conclusion: Future Work 后直接 `VII. Conclusion` (p.11)

## Candidate rules

- R001 abstract 用 `This paper presents a novel ... (ACRONYM) method`。
- R002 Introduction 无独立 Related Work，两类 IOC / CLF / 噪声评述写在引言中段。
- R003 Introduction 贡献用 `Contribution of this research comes from three aspects.` + 编号 1)–3)。
- R004 无 `The rest of this paper is organized as follows`；节序靠罗马数字标题推进。
- R005 Conclusion 先收回方法，再用 `More theoretical studies on ... should be conducted for practical applications.` 指向后续。

## Candidate phrases

- `This paper presents a novel sequential inverse optimal control (SIOC) method` (abstract)
- `This paper proposes a novel SIOC method to address the issues mentioned above.` (introduction)
- `Contribution of this research comes from three aspects.` (introduction)
- `We perform several simulations in different cases to verify the effectiveness of our method.` (experiments)
- `A sequential method for discrete-time IOC is presented in this paper` (conclusion)

## House style

自称是 `This paper presents` / `This paper proposes` / `our method` / `in this paper` / `this study`。未见 `Here we`。`This paper presents` 与 `This paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `This article`。

## Quotes

- p.1 abstract: This paper presents a novel sequential inverse optimal control (SIOC) method for discrete-time systems, which calculates the unknown weight vectors of the cost function in real time using the input and output of an optimally controlled discrete-time system.
- p.1 abstract: The proposed method overcomes the limitations of previous approaches by eliminating the need for the invertible Jacobian assumption.
- p.1 abstract: The effectiveness of the proposed method is demonstrated through simulation results.
- p.1 introduction: THE standard optimal control problem concerns finding the state and input trajectories for a dynamical system.
- p.2 introduction: Conversely, the second class of IOC research focus on solving this problem by exploiting several optimality equations, such as Pontryagin’s maximum principle-based equations [13], and Euler-Lagrange equations [2].
- p.2 introduction: In [16], a method is proposed for the online calculation of discrete-time IOC in both finite and infinite horizons; however, it requires the invertibility condition of a Jacobian.
- p.2 introduction: Despite these advancements, notable limitations of CLF-based IOC method persist, including the inability to explicitly specify a clear optimal cost function and the difficulty in selecting and adjusting parameters, which often requires extensive experience and expert knowledge.
- p.2 introduction: This paper proposes a novel SIOC method to address the issues mentioned above.
- p.2 introduction: Contribution of this research comes from three aspects.
- p.3 method: Consider the dynamics of a discrete system
- p.8 experiments: We perform several simulations in different cases to verify the effectiveness of our method.
- p.9 experiments: Therefore, our proposed method can effectively improve the calculation speed while preserving the recovery accuracy of IOC.
- p.10 experiments: Therefore, from Simulations 1 and 2, it is verified that the proposed method can solve the online IOC problem even for the systems that are not applicable in [16].
- p.11 discussion: Although the problem of sequential IOC has been solved in this study considering the calculation speed and noisy data, the algorithm still requires improvement in the following areas.
- p.11 conclusion: A sequential method for discrete-time IOC is presented in this paper to realize the online estimation of cost weights for either finite or infinite horizon optimal control in cases with significant data noise.
- p.11 conclusion: Finally, simulation results illustrate that the sequential IOC algorithm is effective, has a high convergence speed, and can sequentially tackle the problem of noisy data.
- p.11 conclusion: More theoretical studies on the influences of the feature function selection on the solution spaces should be conducted for practical applications.
