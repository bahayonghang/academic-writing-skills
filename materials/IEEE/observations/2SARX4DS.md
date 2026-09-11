---
key: 2SARX4DS
title: "Continual Semisupervised Learning of Echo State Network for Quality Prediction of Multimode Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3575101"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM STATEMENT` → `III. PROPOSED CS2GESN ALGORITHM` → `IV. EXPERIMENTAL RESULTS AND DISCUSSION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 ESN、多模策略、SSL、continual learning 三类）。Introduction 末为 `The main contributions of this work are three-fold as follows` + 编号。无节序路标句。II 是问题陈述。Experiments 标题为 `EXPERIMENTAL RESULTS AND DISCUSSION`（TE + TPFF）。

## Openers

- abstract: `The successive switching` — "The successive switching nature of multimode processes, coupled with data scarcity, challenges traditional quality prediction models." (p.7209)
- introduction: `IN THE competitive` — "IN THE competitive landscape of modern industries, multimode processes are indispensable, enabling the production of diverse and specialized products [1], [2]." (p.7209)
- method: `As a type` — "As a type of randomized RNN for dynamic modeling, ESN consists of three layers, i.e., input layer, reservoir pool layer, and output layer." (p.7211, III.A)
- experiments: `To verify the` — "To verify the effectiveness of the proposed CS2GESN, in this section, two typical multimode industrial cases are investigated, including the Tennessee Eastman (TE) process and the three-phase flow facility (TPFF) process." (p.7214, IV)
- conclusion: `In this article` — "In this article, we have developed the CS2GESN for online prediction of product quality in multimode processes, where each mode arrives successively with sparse labels." (p.7218)

## Gap transitions

- however (introduction): "However, most ESN improvements are difficult to adapt to multimode processes." (p.7209)
- however (introduction): "However, these approaches require all mode datasets during training, which is often difficult in industrial scenarios." (p.7209)
- therefore (introduction): "Therefore, developing a quality prediction model that aligns with the nature of successive switching remains a challenge." (p.7210)
- however (introduction): "However, these SSL-based approaches that require the precollection of datasets of each mode cannot deal with the successive switching nature of multimode processes." (p.7210)
- to this end (abstract): "To this end, we propose a novel continual semisupervised graph echo state network (CS2GESN)." (p.7209)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a novel continual semisupervised graph echo state network"; "this article presents a continual semisupervised dynamic quality prediction method"
- demonstrate / causal / abstract: "The superiority and feasibility of the proposed method are demonstrated through its application to the Tennessee Eastman process and the three-phase flow facility process."
- develop / causal / conclusion: "we have developed the CS2GESN for online prediction of product quality"
- verify / causal / experiments, conclusion: "The comprehensive experimental results of the TE and TPFF processes have verified the effectiveness"

## Cross-section linkers

- introduction → problem: 贡献列表后直接 `II. PROBLEM STATEMENT` (p.7210)
- problem → method: CSSM 思路段落后 `III. PROPOSED CS2GESN ALGORITHM` (p.7211)
- method → experiments: 复杂度分析后 `IV. EXPERIMENTAL RESULTS AND DISCUSSION` (p.7214)
- experiments → conclusion: TPFF 综合表后 `V. CONCLUSION` (p.7218)

## Candidate rules

- R001 abstract 用 `To this end, we propose a novel` + 方法缩写，不用 `Here we`。
- R002 Introduction 无独立 Related Work；ESN/SSL/CL 评述写在引言中段。
- R003 贡献句用 `The main contributions of this work are three-fold as follows`。
- R004 Method 前加 `PROBLEM STATEMENT`。
- R005 Experiments 标题为 `EXPERIMENTAL RESULTS AND DISCUSSION`。
- R006 Conclusion 用 `In this article, we have developed`，再用 `In the future, we will make improvements` 指向后续。

## Candidate phrases

- `To this end, we propose a novel` (abstract)
- `The main contributions of this work are three-fold as follows.` (introduction)
- `To verify the effectiveness of the proposed CS2GESN, in this section` (experiments)
- `In this article, we have developed the CS2GESN for` (conclusion)
- `In the future, we will make improvements in the following two aspects:` (conclusion)

## House style

自称是 `we propose` / `this article presents` / `In this article, we have developed` / `the proposed method`。未见 `Here we`。`In this article, we have developed` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.7209 abstract: The successive switching nature of multimode processes, coupled with data scarcity, challenges traditional quality prediction models.
- p.7209 abstract: To this end, we propose a novel continual semisupervised graph echo state network (CS2GESN).
- p.7209 abstract: The superiority and feasibility of the proposed method are demonstrated through its application to the Tennessee Eastman process and the three-phase flow facility process.
- p.7209 introduction: IN THE competitive landscape of modern industries, multimode processes are indispensable, enabling the production of diverse and specialized products [1], [2].
- p.7209 introduction: However, most ESN improvements are difficult to adapt to multimode processes.
- p.7210 introduction: Therefore, developing a quality prediction model that aligns with the nature of successive switching remains a challenge.
- p.7210 introduction: The main contributions of this work are three-fold as follows.
- p.7211 method: As a type of randomized RNN for dynamic modeling, ESN consists of three layers, i.e., input layer, reservoir pool layer, and output layer.
- p.7214 experiments: To verify the effectiveness of the proposed CS2GESN, in this section, two typical multimode industrial cases are investigated, including the Tennessee Eastman (TE) process and the three-phase flow facility (TPFF) process.
- p.7216 experiments: In summary, from Table II, when SSL and CL are separately applied to the S9–S11 scenarios and the S33–S35 scenarios, neither of them supports the unified modeling objective of aggregating the incomplete process dynamics of the modes, and thus it is difficult to obtain satisfactory performance.
- p.7218 conclusion: In this article, we have developed the CS2GESN for online prediction of product quality in multimode processes, where each mode arrives successively with sparse labels.
- p.7218 conclusion: The comprehensive experimental results of the TE and TPFF processes have verified the effectiveness of the proposed CS2GESN model, achieving a more flexible solution for multimode processes.
- p.7218 conclusion: In the future, we will make improvements in the following two aspects: 1) EWC-based CL methods still have a learning bottleneck despite their low computational complexity, and it is crucial to investigate more advanced CL strategies; 2) we will explore effective combination of SSL with CL to enable mutual promotion in noisy environments.
