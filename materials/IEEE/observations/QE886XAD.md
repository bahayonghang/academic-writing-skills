---
key: QE886XAD
title: "Q-Learning-Based Multi-Rate Optimal Control for Process Industries"
venue: "IEEE Transactions on Circuits and Systems II: Express Briefs"
doi: "10.1109/TCSII.2022.3219255"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-5"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. CONTROL PROBLEM` → `III. MULTI-RATE OPTIMAL CONTROL METHOD` → `IV. INDUSTRIAL APPLICATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 lifting / observer-based / dual-rate MPC / ADP，再收口 model-free）。Introduction 末用编号贡献 `i) … ii) … iii)`，无 `The rest of this article is organized as follows`。Method 分 `A. Dynamic Model With Block Lifting Technology`、`B. Q-Learning Controller`、`C. Convergence Analysis`。Experiments 标题为 `INDUSTRIAL APPLICATION`（磨矿过程 HIL）。Express Brief 自称 `this brief`。

## Openers

- abstract: `This brief studies` — "This brief studies the multi-rate optimal control problem for a class of industrial processes, whose controlling rate will be set faster than the sampling rate sometimes." (p.1)
- introduction: `IN MODERN industries` — "IN MODERN industries, hardware restrictions, such as indirect and high precision detection, enlarge the sampling period." (p.1；栏首掉字)
- method: `Consider the following` — "Consider the following continuous time model." (p.2, II)
- experiments: `The proposed optimal` — "The proposed optimal control method is applied to a one-stage grinding process as shown in Fig. 2." (p.4, IV)
- conclusion: `This brief studied` — "This brief studied the model-free optimal control problem based on RL and lifting technology for the multi-rate sample system and applied to a grinding process." (p.5)

## Gap transitions

- however (introduction): "However, the above controllers rely on the accurate models that are always hard to build in practice." (p.1)
- therefore (introduction): "Therefore, it is in urgent need to set up the model-free multi-rate control scheme for the industrial systems." (p.1)
- since (introduction): "Since the initial admissible control in policy iteration (PI) is difficult to obtain in practice, the controller updates in the form of the value iteration (VI) [17]." (p.1)
- thus (method): "Thus, the optimal control gain only depends on matrix H, obtained by iterative estimation with online state and data Xk." (p.3)

## Hedge verbs

- present / causal / abstract: "we present a model-free self-learning control scheme"
- propose / causal / introduction: "the multi-rate optimal controller based on Q-learning is proposed"; "the Q-learning based multi-rate control scheme is proposed"
- show / causal / abstract, experiments: "showing that the proposed approach has high tracking and real-time performance"; "Fig. 4 shows the convergence trend"
- illustrate / causal / experiments: "This experiment illustrates the effectiveness and stability of the proposed method."
- will be studied / speculative / conclusion: "the multi-rate control with the NNs structure will be studied"

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. CONTROL PROBLEM`，无节序路标 (p.1–2)
- method → experiments: 收敛证明后 `IV. INDUSTRIAL APPLICATION` (p.4)
- experiments → conclusion: HIL 结果段落后 `V. CONCLUSION` (p.5)

## Candidate rules

- R001 Express Brief abstract 用 `This brief studies` 开题，再用 `In this brief, we present`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段，缺口用 `However` + `Therefore, it is in urgent need`。
- R003 贡献用 `The contributions are as follows: i) … ii) … iii)`，不用 `The rest of this article`。
- R004 Experiments 标题可为 `INDUSTRIAL APPLICATION`，开句 `The proposed … method is applied to`。
- R005 Conclusion 用 `This brief studied` 收回，再用 `will be studied` 指向非线性扩展。

## Candidate phrases

- `This brief studies the multi-rate optimal control problem` (abstract)
- `In this brief, we present a model-free self-learning control scheme` (abstract)
- `Therefore, it is in urgent need to set up` (introduction)
- `The contributions are as follows:` (introduction)
- `The proposed optimal control method is applied to` (experiments)
- `This brief studied the model-free optimal control problem` (conclusion)

## House style

自称 `this brief` / `In this brief` / `we present` / `the proposed approach` / `the proposed method`。未见 `Here we`、`In this paper`、`In this article`。`In this brief, we present` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: This brief studies the multi-rate optimal control problem for a class of industrial processes, whose controlling rate will be set faster than the sampling rate sometimes.
- p.1 abstract: In this brief, we present a model-free self-learning control scheme for the real-time solution of this problem, combining the lifting technology and Q-learning.
- p.1 abstract: Finally, a hardware-in-loop (HIL) simulation study for process industries is carried out, showing that the proposed approach has high tracking and real-time performance.
- p.1 introduction: IN MODERN industries, hardware restrictions, such as indirect and high precision detection, enlarge the sampling period.
- p.1 introduction: However, the above controllers rely on the accurate models that are always hard to build in practice.
- p.1 introduction: Therefore, it is in urgent need to set up the model-free multi-rate control scheme for the industrial systems.
- p.1 introduction: Since the initial admissible control in policy iteration (PI) is difficult to obtain in practice, the controller updates in the form of the value iteration (VI) [17].
- p.1 introduction: The contributions are as follows: i) a block lifting technology is employed to handle the multi-rare problem with multiple-input multiple-output system, ii) the Q-learning based multi-rate control scheme is proposed to realize the optimal controller, then the convergence is proved, iii) an application case is made on a grinding process to verify the effectiveness of the proposed approach by a self-developed hardware-in-loop simulation platform.
- p.2 method: Consider the following continuous time model.
- p.4 experiments: The proposed optimal control method is applied to a one-stage grinding process as shown in Fig. 2.
- p.4 experiments: Now, the proposed algorithm is used to solve the multi-rate optimal control problem for grinding process, without the dynamics knowledge.
- p.5 experiments: This experiment illustrates the effectiveness and stability of the proposed method.
- p.5 conclusion: This brief studied the model-free optimal control problem based on RL and lifting technology for the multi-rate sample system and applied to a grinding process.
- p.5 conclusion: The experiment has been carried out in a HIL system for grinding process to verify the effectiveness of the proposed method.
- p.5 conclusion: To further strengthen the effectiveness of the proposed approach for the non-linear system, the multi-rate control with the NNs structure will be studied.
