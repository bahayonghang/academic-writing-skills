---
key: VY8DW8GV
title: "Fault-Tolerant Soft Sensor Modeling Based on a Two-Dimensional Group Distributionally Robust Optimization Framework"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2025.3561754"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "14396-14406"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. GROUP DISTRIBUTIONALLY ROBUST OPTIMIZATION` → `III. TWO-DIMENSIONAL GROUP DISTRIBUTIONALLY ROBUST OPTIMIZATION` → `IV. EXPERIMENTS AND DISCUSSIONS` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 GPR/HMR/SAE/VAE/CNN/LSTM/GNN/Transformer/MoE，再评 MSaS / DSLAN / TL-LSTM / GRU-AL 的容错范围）。Introduction 末无节序路标，贡献列表后直接进 GDRO 理论节。Method 为 `III. TWO-DIMENSIONAL GROUP DISTRIBUTIONALLY ROBUST OPTIMIZATION`。Experiments 标题为 `IV. EXPERIMENTS AND DISCUSSIONS`（TEP + TPFF）。

## Openers

- abstract: `In industrial automation` — "In industrial automation and intelligence, fault tolerance mechanisms have always been an attractive topic." (p.14396)
- introduction: `IN THE era` — "IN THE era of Industry 4.0, the integration of artificial intelligence and industrial processes has given rise to a paradigm shift in the field of soft sensors [1], [2], [3]." (p.14396；栏首掉字)
- method: `Similar to GDRO` — "Similar to GDRO, the optimization objective of the proposed 2D-GDRO is to minimize the worst-case risk over an uncertainty set as" (p.14399, III.A)
- experiments: `To verify the` — "To verify the effectiveness of the proposed 2D-GDRO framework, we utilize the Tennessee-Eastman process (TEP) and a real three-phase flow facility (TPFF) testbed to evaluate the performance of soft sensors under new faults and different types of faults." (p.14400, IV)
- conclusion: `In this article` — "In this article, a 2D-GDRO framework is proposed for fault-tolerant soft sensor modeling, accompanied by a 2D uncertainty set and triple-interleaved optimization algorithms." (p.14405)

## Gap transitions

- however (introduction): "However, while there is a wealth of studies on fault-tolerant process control [29], there has been limited research dedicated to fault-tolerant soft sensors." (p.14397)
- however (introduction): "However, the existing fault-tolerant soft sensors mentioned above have two significant limitations." (p.14397)
- unfortunately (introduction): "Unfortunately, only GRU-AL exhibits a certain degree of generalization to new faults, while the MSaS family, DSLAN, and TL-LSTM do not possess this ability." (p.14397)
- to overcome (introduction): "To overcome the limitations of existing work, this article proposes a two-dimensional group distributionally robust optimization (2D-GDRO) framework for fault-tolerant soft sensor modeling with generalization to different types of faults and unforeseen new faults." (p.14397)
- however (introduction/method): "However, the number of existing faults in the training set is typically limited in industrial practice." (p.14398)
- in contrast (experiments): "In contrast, the proposed 2D-GDRO achieves the best fault tolerance performance, with the lowest average RMSE and the highest average R2." (p.14404)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a two-dimensional group distributionally robust optimization (2D-GDRO) framework"; "we propose to describe the potential distributions"; "a 2D-GDRO framework is proposed"
- introduce / causal / abstract: "we introduce a triple-interleaved optimization algorithm"
- show / causal / abstract, experiments: "The experimental results show that 2D-GDRO outperforms other training frameworks"; "The findings show that the fault tolerance on the test set f5 deteriorates significantly"
- may / speculative / experiments, method: "the effectiveness of 2D-GDRO may be compromised"; "the performance of the soft sensor model may deteriorate"
- can / speculative / conclusion: "other aspects of reliability, such as interpretability, can be explored"

## Cross-section linkers

- introduction → theory: 贡献列表后直接 `II. GROUP DISTRIBUTIONALLY ROBUST OPTIMIZATION`，无 `The rest of this article` (p.14398)
- theory → method: GDRO 局限段落后 `III. TWO-DIMENSIONAL GROUP DISTRIBUTIONALLY ROBUST OPTIMIZATION` (p.14398)
- method → experiments: 在线测试步骤后 `IV. EXPERIMENTS AND DISCUSSIONS` (p.14400)
- experiments → conclusion: Wilcoxon 检验后直接 `V. CONCLUSION` (p.14405)

## Candidate rules

- R001 abstract / 正文贡献句用 `this article proposes a ... framework`；Note to Practitioners 用 `This article addresses`。
- R002 Introduction 无独立 Related Work，容错软测量评述写在引言中段，并用 Table I 对比。
- R003 Introduction 末无节序路标，贡献用 `Specifically, the contributions of this article are as follows:` + 编号列表。
- R004 Experiments 标题为 `EXPERIMENTS AND DISCUSSIONS`，含消融、敏感性与 Wilcoxon 符号秩检验。
- R005 Conclusion 收回框架后用 `Fault tolerance is one aspect of reliability` 转未来 `interpretability`。

## Candidate phrases

- `this article proposes a two-dimensional group distributionally robust optimization (2D-GDRO) framework` (abstract)
- `To overcome the limitations of existing work, this article proposes` (introduction)
- `Specifically, the contributions of this article are as follows:` (introduction)
- `To verify the effectiveness of the proposed` (experiments)
- `In this article, a 2D-GDRO framework is proposed` (conclusion)

## House style

自称是 `this article` / `we propose` / `In this article`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.14396 abstract: In industrial automation and intelligence, fault tolerance mechanisms have always been an attractive topic.
- p.14396 abstract: To develop soft sensors with fault tolerance for different types of faults and unforeseen new faults, this article proposes a two-dimensional group distributionally robust optimization (2D-GDRO) framework for fault-tolerant soft sensor modeling.
- p.14396 abstract: We propose to describe the potential distributions of new fault conditions with an uncertainty set and optimize the soft sensor model by minimizing the worst-case risk over the uncertainty set.
- p.14396 abstract: The experimental results show that 2D-GDRO outperforms other training frameworks in average soft sensing accuracy under new fault conditions.
- p.14396 practitioners: This article addresses the need for fault-tolerant soft sensors in industrial automation, where systems must continue to function reliably despite various types of faults and unforeseen faults.
- p.14396 introduction: IN THE era of Industry 4.0, the integration of artificial intelligence and industrial processes has given rise to a paradigm shift in the field of soft sensors [1], [2], [3].
- p.14397 introduction: However, while there is a wealth of studies on fault-tolerant process control [29], there has been limited research dedicated to fault-tolerant soft sensors.
- p.14397 introduction: Unfortunately, only GRU-AL exhibits a certain degree of generalization to new faults, while the MSaS family, DSLAN, and TL-LSTM do not possess this ability.
- p.14397 introduction: To overcome the limitations of existing work, this article proposes a two-dimensional group distributionally robust optimization (2D-GDRO) framework for fault-tolerant soft sensor modeling with generalization to different types of faults and unforeseen new faults.
- p.14398 introduction: Specifically, the contributions of this article are as follows:
- p.14399 method: Similar to GDRO, the optimization objective of the proposed 2D-GDRO is to minimize the worst-case risk over an uncertainty set as
- p.14400 experiments: To verify the effectiveness of the proposed 2D-GDRO framework, we utilize the Tennessee-Eastman process (TEP) and a real three-phase flow facility (TPFF) testbed to evaluate the performance of soft sensors under new faults and different types of faults.
- p.14404 experiments: In contrast, the proposed 2D-GDRO achieves the best fault tolerance performance, with the lowest average RMSE and the highest average R2.
- p.14405 conclusion: In this article, a 2D-GDRO framework is proposed for fault-tolerant soft sensor modeling, accompanied by a 2D uncertainty set and triple-interleaved optimization algorithms.
- p.14405 conclusion: Experimental validation using two industrial processes has demonstrated the superior fault tolerance performance of 2D-GDRO over existing training frameworks, showcasing excellent average accuracy under new fault conditions.
- p.14405 conclusion: Fault tolerance is one aspect of reliability of soft sensors. In future work, other aspects of reliability, such as interpretability, can be explored.
