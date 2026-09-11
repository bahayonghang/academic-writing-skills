---
key: XB9HM6HN
title: "LLM-Enhanced Multi-Agent Transfer Reinforcement Learning for Sensing, Communication, Computing, and Control Co-Optimization in Cyber-Physical Systems"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2025.126005"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

Letter（页眉 `Letter`；开篇 `Dear Editor,`）。无罗马数字 I–VI 主节。功能块序：开场缺口 → 既有启发式/MADRL 评述 → 编号贡献 → `Algorithm framework:` → 案例 `A case study on S3C co-optimization of CPS` → `Experimental Analysis:` → `Conclusion:`。无独立 Related Work。`related_work=inlined`（开场后评 heuristic / MADDPG / MATD3 / MAPPO）。篇幅 3 页（1251–1253）。

## Openers

- letter: `With the rapid` — "With the rapid development of new-generation information and communication technology, the fusion of sensing, communication, computing, and control (S3C) is becoming increasingly significant for cyber-physical systems (CPS)." (p.1)
- method: `In general, an` — "In general, an S3C co-optimization problem can be modeled by a multi-agent POMDP and denoted as" (p.1, Algorithm framework)
- experiments: `To validate the` — "To validate the effectiveness and superiority of the proposed LLMPT-MADRL and solve the S3C co-optimization problem for CPS, we select three benchmark algorithms (i.e., MADDPG, MATD3, and MAPPO) and conduct experiments, where the number of agents is set to 10, the learning rate is set to 0.0003, and the discount factor is set to 0.95." (p.2–3)
- conclusion: `This letter proposed` — "This letter proposed the LLM-enhanced policy transfer framework for MADRL and provided a case study on the S3C co-optimization of CPS." (p.3)

## Gap transitions

- however (open): "However, due to the non-convexity, the curse of dimensionality, and the partial observability faced by CPS, traditional convex optimization algorithms are challenging to deal with S3C co-optimization." (p.1)
- thus (open): "Thus, this letter establishes the S3C problem as a partially observable Markov decision process (POMDP) and proposes a large language model (LLM)-enhanced policy transfer (PT) framework for multi-agent deep reinforcement learning (MADRL), denoted as LLMPT-MADRL." (p.1)
- however (open): "However, MADRL and LLM exhibit heterogeneity in neural network scale." (p.1)
- however (related, inlined): "However, heuristic algorithms with limited adaptability are prone to falling into the local optimum and thus are not suitable for S3C co-optimization of complex CPS." (p.1)
- however (gap): "However, agents in MADRL generally lack prior knowledge about the environment and the objective, resulting in fragile neuronal dynamic characteristics." (p.1)
- motivated (contrib): "Motivated by this, this letter makes the following main contributions." (p.1)

## Hedge verbs

- establish / propose / causal / open: "this letter establishes the S3C problem as a partially observable Markov decision process (POMDP) and proposes"
- design / causal / open: "we further design an adaptive policy transfer loss function"
- show / causal / open, experiments: "Experimental results show that the reward of LLMPT-MADRL is increased by 16.8%"
- demonstrate / causal / inlined related, experiments: "which demonstrates impressive stability"; "which demonstrates the enhancement of LLM-enhanced policy transfer"
- proposed / past / conclusion: "This letter proposed the LLM-enhanced policy transfer framework"

## Cross-section linkers

- open → method: 编号贡献后直接 `Algorithm framework:`，无 `The rest of this article is organized as follows`。(p.1)
- method → case: "Based on POMDP, we propose the LLM-enhanced policy transfer framework for MADRL as shown in Fig. 1" 后接案例约束 (p.1–2)
- case → experiments: "The above S3C co-optimization problem is obviously non-convex, and can be solved by the proposed LLMPT-MADRL algorithm via centralized training and distributed execution." 随后 `Experimental Analysis:` (p.2)
- experiments → conclusion: 表 2 后直接 `Conclusion:` (p.3)

## Candidate rules

- R001 IEEE/CAA letter 用 `Dear Editor,` 起笔，自称 `this letter` 而非 `this paper`。
- R002 贡献用 `this letter makes the following main contributions` + 编号列表。
- R003 方法块用冒号小标题 `Algorithm framework:` / `Experimental Analysis:` / `Conclusion:`，不用罗马数字。
- R004 Conclusion 用过去式 `This letter proposed`，再用百分数收回实验。

## Candidate phrases

- `Thus, this letter establishes` (open)
- `this letter makes the following main contributions` (open)
- `we further design an adaptive` (open)
- `To validate the effectiveness and superiority of the proposed` (experiments)
- `This letter proposed the` (conclusion)

## House style

自称是 `this letter` / `we propose` / `we further design` / `the proposed LLMPT-MADRL`。未见 `In this paper`。`this letter` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 letter: With the rapid development of new-generation information and communication technology, the fusion of sensing, communication, computing, and control (S3C) is becoming increasingly significant for cyber-physical systems (CPS).
- p.1 letter: However, due to the non-convexity, the curse of dimensionality, and the partial observability faced by CPS, traditional convex optimization algorithms are challenging to deal with S3C co-optimization.
- p.1 letter: Thus, this letter establishes the S3C problem as a partially observable Markov decision process (POMDP) and proposes a large language model (LLM)-enhanced policy transfer (PT) framework for multi-agent deep reinforcement learning (MADRL), denoted as LLMPT-MADRL.
- p.1 letter: However, MADRL and LLM exhibit heterogeneity in neural network scale. Thus, we further design an adaptive policy transfer loss function to achieve dynamic adaptation between MADRL and LLM, avoiding the mismatch of policy transfer information.
- p.1 letter: Experimental results show that the reward of LLMPT-MADRL is increased by 16.8%, the system delay is reduced by 24.5%, and the control error is reduced by 10.4% compared with the benchmark MADRL-based algorithms.
- p.1 related-inlined: However, heuristic algorithms with limited adaptability are prone to falling into the local optimum and thus are not suitable for S3C co-optimization of complex CPS.
- p.1 gap: However, agents in MADRL generally lack prior knowledge about the environment and the objective, resulting in fragile neuronal dynamic characteristics.
- p.1 contrib: Motivated by this, this letter makes the following main contributions.
- p.1 method: In general, an S3C co-optimization problem can be modeled by a multi-agent POMDP and denoted as
- p.1 method: Based on POMDP, we propose the LLM-enhanced policy transfer framework for MADRL as shown in Fig. 1, where there are LLM module, MADRL module and policy selection module.
- p.2 case: The above S3C co-optimization problem is obviously non-convex, and can be solved by the proposed LLMPT-MADRL algorithm via centralized training and distributed execution.
- p.2–3 experiments: To validate the effectiveness and superiority of the proposed LLMPT-MADRL and solve the S3C co-optimization problem for CPS, we select three benchmark algorithms (i.e., MADDPG, MATD3, and MAPPO) and conduct experiments, where the number of agents is set to 10, the learning rate is set to 0.0003, and the discount factor is set to 0.95.
- p.3 experiments: The reward of LLMPT-MADRL is always higher than that of MADRL, which demonstrates the enhancement of LLM-enhanced policy transfer.
- p.3 conclusion: This letter proposed the LLM-enhanced policy transfer framework for MADRL and provided a case study on the S3C co-optimization of CPS.
- p.3 conclusion: Experimental results demonstrated that, compared with existing MADRL benchmark algorithms, the proposed LLMPT-MADRL algorithm enhanced reward by more than 16.8%, reduced system delay by 24.5%, and control error by 10.4%.
