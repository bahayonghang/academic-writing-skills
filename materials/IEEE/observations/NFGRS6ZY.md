---
key: NFGRS6ZY
title: "Fuzzy Stochastic Configuration Networks for Nonlinear System Modeling"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2023.3315368"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED F-SCNS` → `IV. PERFORMANCE EVALUATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 ANN、模糊推理、neuro-fuzzy、SCN）。Introduction 末有节序路标，指向 Section II–V。Method 为 III，含 Algorithm 1。Experiments 标题为 `PERFORMANCE EVALUATION`（非线性辨识 + Mackey-Glass + KEEL + WWTP 软测量）。

## Openers

- abstract: `This article proposes` — "This article proposes a novel randomized neuro-fuzzy model called fuzzy stochastic configuration networks (F-SCNs), which integrates the Takagi–Sugeno (T–S) fuzzy inference system into SCNs to enhance its fuzzy inference capability." (p.1)
- introduction: `NONLINEAR system modeling` — "NONLINEAR system modeling plays a crucial role in soft sensor modeling, fault diagnosis, and control of industrial processes." (p.1；栏首掉字)
- method: `In this section` — "In this section, a novel neuro-fuzzy model called fuzzy SCNs is proposed." (p.3, III)
- experiments: `In this section` — "In this section, the proposed method is applied to four different tasks: nonlinear dynamic system identification, time series prediction, modeling a series of benchmark datasets, and one real industrial case study, to verify the effectiveness and superiority of the proposed method in performing complex uncertain data modeling tasks." (p.5, IV)
- conclusion: `This article proposes` — "This article proposes a novel neuro-fuzzy model called F-SCN, which integrates TS fuzzy inference systems with SCNs." (p.9)

## Gap transitions

- however (introduction): "However, ANNs are black-box models that cannot effectively handle rule-based information such as fuzzy knowledge, expert experience, and lack of interpretation of learned knowledge." (p.1)
- nevertheless (introduction): "Nevertheless, it should be noted that fuzzy inference systems require a large amount of rule-based information to achieve satisfactory accuracy when dealing with large-scale datasets." (p.1)
- however (introduction): "However, these methods suffer from complex iterative processes for parameter learning, and have potential problems, such as slow convergence speed, complex computational process, sensitivity to initial parameters, and learning rate." (p.1)
- although (introduction): "Although numerous studies have demonstrated that SCNs and their variants are feasible for modeling tasks in various domains [22], [23], [24], they have limitations in terms of dealing with uncertain complex fuzzy systems and interpretability." (p.2)
- therefore (introduction): "Therefore, to overcome the defects of traditional neuro-fuzzy models in modeling efficiency and structural design, and to further improve the modeling performance of SCNs for uncertain and fuzzy nonlinear systems, this article proposes a novel neuro-fuzzy model, named fuzzy SCNs (F-SCNs)." (p.2)
- it is worth noting (conclusion): "It is worth noting that the proposed algorithm has some limitations, such as the fuzzy rules need to be manually set, which increases the difficulty of parameter optimization to some extent." (p.9)
- therefore (conclusion): "Therefore, we plan to propose an ensemble version of F-SCN and fuzzy self-organizing SCNs to deal with the randomness of the model." (p.9)

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "This article proposes a novel randomized neuro-fuzzy model"; "a novel neuro-fuzzy model called fuzzy SCNs is proposed"
- show / causal / abstract, experiments: "The results show that the proposed method has good potential for nonlinear system modeling tasks"; "It can be clearly seen from Figs. 4 and 5 that the proposed F-SCNs can fit the system output better"
- verify / causal / abstract, experiments: "to verify the feasibility and effectiveness of the proposed method"; "to verify the effectiveness and superiority of the proposed method"
- can / speculative / abstract, conclusion: "the proposed method has good potential"; "the proposed F-SCNs can achieve better learning and generalization performance"
- plan / speculative / conclusion: "we plan to propose an ensemble version of F-SCN"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows: Section II briefly reviews SCNs and TS fuzzy inference systems. A novel F-SCN is proposed in Section III. A series of experiments are carried out in Section IV to compare the modeling performance of fuzzy SCNs with some classical nonfuzzy and neuro-fuzzy models. Finally, Section V concludes the article." (p.2)
- method → experiments: Algorithm 1 后直接 `IV. PERFORMANCE EVALUATION` (p.5)
- experiments → conclusion: WWTP 软测量段落后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 开篇即 `This article proposes a novel ... called`，把方法名与集成对象写进第一句。
- R002 Introduction 无独立 Related Work，用 `Therefore, to overcome the defects ... this article proposes` 转入方法，贡献改称 `advantages and innovations` 编号列表。
- R003 Introduction 末用 `The rest of this article is organized as follows:` 指向 II–V。
- R004 Experiments 节名 `PERFORMANCE EVALUATION`，开篇用 `the proposed method is applied to four different tasks`。
- R005 Conclusion 复用 `This article proposes`，再用 `It is worth noting that the proposed algorithm has some limitations` + `Therefore, we plan to`。

## Candidate phrases

- `This article proposes a novel ... called` (abstract, conclusion)
- `Therefore, to overcome the defects of ..., this article proposes` (introduction)
- `The rest of this article is organized as follows:` (introduction)
- `In this section, a novel ... is proposed.` (method)
- `It is worth noting that the proposed algorithm has some limitations` (conclusion)

## House style

自称是 `This article` / `the proposed method` / `we`（参数设置与展望）。未见 `Here we`。`This article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: This article proposes a novel randomized neuro-fuzzy model called fuzzy stochastic configuration networks (F-SCNs), which integrates the Takagi–Sugeno (T–S) fuzzy inference system into SCNs to enhance its fuzzy inference capability.
- p.1 abstract: A series of simulation experiments are carried out, including nonlinear dynamic system identification, sequence prediction, and benchmark data modeling from the real world to verify the feasibility and effectiveness of the proposed method.
- p.1 abstract: The results show that the proposed method has good potential for nonlinear system modeling tasks compared to some classical neuro-fuzzy and nonfuzzy models.
- p.1 introduction: NONLINEAR system modeling plays a crucial role in soft sensor modeling, fault diagnosis, and control of industrial processes.
- p.1 introduction: However, ANNs are black-box models that cannot effectively handle rule-based information such as fuzzy knowledge, expert experience, and lack of interpretation of learned knowledge.
- p.1 introduction: Nevertheless, it should be noted that fuzzy inference systems require a large amount of rule-based information to achieve satisfactory accuracy when dealing with large-scale datasets.
- p.1 introduction: However, these methods suffer from complex iterative processes for parameter learning, and have potential problems, such as slow convergence speed, complex computational process, sensitivity to initial parameters, and learning rate.
- p.2 introduction: Although numerous studies have demonstrated that SCNs and their variants are feasible for modeling tasks in various domains [22], [23], [24], they have limitations in terms of dealing with uncertain complex fuzzy systems and interpretability.
- p.2 introduction: Therefore, to overcome the defects of traditional neuro-fuzzy models in modeling efficiency and structural design, and to further improve the modeling performance of SCNs for uncertain and fuzzy nonlinear systems, this article proposes a novel neuro-fuzzy model, named fuzzy SCNs (F-SCNs).
- p.2 introduction: Thus, the proposed method has the following advantages and innovations.
- p.2 introduction: The rest of this article is organized as follows: Section II briefly reviews SCNs and TS fuzzy inference systems. A novel F-SCN is proposed in Section III. A series of experiments are carried out in Section IV to compare the modeling performance of fuzzy SCNs with some classical nonfuzzy and neuro-fuzzy models. Finally, Section V concludes the article.
- p.3 method: In this section, a novel neuro-fuzzy model called fuzzy SCNs is proposed.
- p.5 experiments: In this section, the proposed method is applied to four different tasks: nonlinear dynamic system identification, time series prediction, modeling a series of benchmark datasets, and one real industrial case study, to verify the effectiveness and superiority of the proposed method in performing complex uncertain data modeling tasks.
- p.6 experiments: It can be clearly seen from Figs. 4 and 5 that the proposed F-SCNs can fit the system output better than other randomized models.
- p.9 conclusion: This article proposes a novel neuro-fuzzy model called F-SCN, which integrates TS fuzzy inference systems with SCNs.
- p.9 conclusion: Compared with some existing randomized models and neuro-fuzzy models, the results show that the proposed F-SCNs can achieve better learning and generalization performance while ensuring fast learning.
- p.9 conclusion: It is worth noting that the proposed algorithm has some limitations, such as the fuzzy rules need to be manually set, which increases the difficulty of parameter optimization to some extent.
- p.9 conclusion: Therefore, we plan to propose an ensemble version of F-SCN and fuzzy self-organizing SCNs to deal with the randomness of the model.
