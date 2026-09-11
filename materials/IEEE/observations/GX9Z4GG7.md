---
key: GX9Z4GG7
title: "Constrained Multi-Objective Optimization With Deep Reinforcement Learning Assisted Operator Selection"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2023.123687"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. Introduction` → `II. Related Work and Motivations` → `III. Proposed Methods` → `IV. Experimental Studies` → `V. Conclusions and Future Work`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. Related Work and Motivations`，含 Preliminaries / Adaptive Operator Selection / DRL applications / Motivations）。Introduction 末有节序路标，指向 Section II–V。Method 为 III。Experiments 标题为 `Experimental Studies`（42 个基准问题）。页码 919–931。

## Openers

- abstract: `Solving constrained multi-objective` — "Solving constrained multi-objective optimization problems with evolutionary algorithms has attracted considerable attention." (p.1)
- introduction: `CONSTRAINED multi-objective optimization` — "CONSTRAINED multi-objective optimization problems (CMOPs) contain multiple conflicting objective functions and constraints, which widely exist in real-world applications and scientific research [1]." (p.1；栏首掉字)
- related_work: `Without loss of` — "Without loss of generality, a CMOP can be formulated as" (p.2, II.A)
- method: `In this work` — "In this work, the evolutionary operators are regarded as actions, thus the actions include" (p.4, III.A)
- experiments: `This section presents` — "This section presents the experimental studies." (p.7, IV)
- conclusion: `In this article` — "In this article, we propose a DQL-assisted online operator selection method for CMOPs, filling the research gap in operator selection in CMOPs and introducing DRL techniques to CMOPs." (p.11, V)

## Gap transitions

- however (abstract): "The performance of CMOEAs may be heavily dependent on the operators used, however, it is usually difficult to select suitable operators for the problem at hand." (p.1)
- hence (abstract): "Hence, improving operator selection is promising and necessary for CMOEAs." (p.1)
- although (introduction): "Although ensemble and adaptive selection of operators have received increased attention in the multi-objective optimization community [16]–[18], unfortunately, no research efforts have been dedicated to constrained multi-objective optimization." (p.1)
- however (related_work): "However, when applying DRL to CMOPs, the main challenge is to properly consider constraint satisfaction and feasibility in a DRL model." (p.2)
- nevertheless (conclusion): "Nevertheless, some issues must be addressed regarding the current study of this paper." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "This work proposes an online operator selection framework assisted by Deep Reinforcement Learning."; "This work proposes a DRL-assisted online operator selection framework for CMOPs."
- may / speculative / abstract: "The performance of CMOEAs may be heavily dependent on the operators used"
- demonstrate / causal / introduction, conclusion: "Extensive experimental studies on four popular and challenging CMOP benchmark test suites demonstrated that the OS method can significantly improve the performance of CMOEAs."
- reveal / causal / experiments: "The results clearly show that DRLOS-EMCMO can approximate the CPF and obtain an even distribution in every instance."

## Cross-section linkers

- introduction → related_work: "The remainder of this article is organized as follows. Section II introduces the related work. Section III elaborates on the proposed methods. Then, experiments and analysis are presented in Section IV. Finally, conclusions and future research directions are given in Section V." (p.2)
- related_work → method: "Our proposed DQL model and the DQL-assisted CMOEA framework are elaborated on in the next section." 随后 `III. Proposed Methods` (p.4)
- method → experiments: Remarks 后直接 `IV. Experimental Studies` (p.7)
- experiments → conclusion: ablation 后直接 `V. Conclusions and Future Work` (p.11)

## Candidate rules

- R001 abstract 用 `This work proposes` 而不是 `we propose` 作为框架句。
- R002 独立 `II. Related Work and Motivations`，末节 Motivations 再转入方法。
- R003 Introduction 贡献用 `Specifically, the main contributions are as follows:` + 编号 1)–3)。
- R004 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法，再用 `Nevertheless` 承认局限，`In the future, the following directions are worth trying:` 编号后续。

## Candidate phrases

- `This work proposes an online operator selection framework assisted by` (abstract)
- `The remainder of this article is organized as follows.` (introduction)
- `Specifically, the main contributions are as follows:` (introduction)
- `In this article, we propose a DQL-assisted online operator selection method for CMOPs` (conclusion)
- `In the future, the following directions are worth trying:` (conclusion)

## House style

自称是 `This work proposes` / `this article` / `we propose` / `our methods`。未见 `Here we`。`This work proposes` 与 `In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。摘要未见 `In this paper`；结论有 `the current study of this paper`。

## Quotes

- p.1 abstract: Solving constrained multi-objective optimization problems with evolutionary algorithms has attracted considerable attention.
- p.1 abstract: The performance of CMOEAs may be heavily dependent on the operators used, however, it is usually difficult to select suitable operators for the problem at hand.
- p.1 abstract: Hence, improving operator selection is promising and necessary for CMOEAs.
- p.1 abstract: This work proposes an online operator selection framework assisted by Deep Reinforcement Learning.
- p.1 abstract: The experimental results reveal that the proposed Deep Reinforcement Learning-assisted operator selection significantly improves the performance of these CMOEAs and the resulting algorithm obtains better versatility compared to nine state-of-the-art CMOEAs.
- p.1 introduction: CONSTRAINED multi-objective optimization problems (CMOPs) contain multiple conflicting objective functions and constraints, which widely exist in real-world applications and scientific research [1].
- p.1 introduction: Although ensemble and adaptive selection of operators have received increased attention in the multi-objective optimization community [16]–[18], unfortunately, no research efforts have been dedicated to constrained multi-objective optimization.
- p.2 introduction: This work proposes a DRL-assisted online operator selection framework for CMOPs. Specifically, the main contributions are as follows:
- p.2 introduction: The remainder of this article is organized as follows. Section II introduces the related work. Section III elaborates on the proposed methods. Then, experiments and analysis are presented in Section IV. Finally, conclusions and future research directions are given in Section V.
- p.2 related_work: Without loss of generality, a CMOP can be formulated as
- p.3 related_work: However, traditional reinforcement learning techniques such as Q-learning may be less effective in dealing with such problems because the environment can include an infinite number of states, that is, the search space is continuous but Q-table can only handle discrete state space.
- p.4 method: In this work, the evolutionary operators are regarded as actions, thus the actions include
- p.7 experiments: This section presents the experimental studies.
- p.8 experiments: In summary, our proposed DQL-assisted OS method can improve the performance of these CMOEAs.
- p.11 conclusion: In this article, we propose a DQL-assisted online operator selection method for CMOPs, filling the research gap in operator selection in CMOPs and introducing DRL techniques to CMOPs.
- p.11 conclusion: Experimental studies have demonstrated that the proposed adaptive operator selection method is effective, and the resulting algorithm outperformed nine state-of-the-art CMOEAs.
- p.11 conclusion: Nevertheless, some issues must be addressed regarding the current study of this paper.
- p.11 conclusion: In the future, the following directions are worth trying:
