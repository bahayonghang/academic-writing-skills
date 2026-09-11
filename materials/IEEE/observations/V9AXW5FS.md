---
key: V9AXW5FS
title: "TSTFNN: Performance Enhancement for Fuzzy Neural Network in Performance Monitoring of Industrial Flotation Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3330342"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. FNN WITH TWO-STAGE TRAINING` → `IV. EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 FNN 变体、梯度/牛顿/群智能训练、集成与激活函数，再点训练策略缺口）。Introduction 末有编号贡献与节序路标，指向 Section II–V。Method 标题为 `FNN WITH TWO-STAGE TRAINING`。Experiments 标题为 `EXPERIMENTAL STUDIES`（Mackey-Glass、脱丁烷塔、粗选浮选）。

## Openers

- abstract: `Numerous studies on` — "Numerous studies on learning algorithms have been done in the neural networks community, however concerning to training strategy is limited." (p.4919)
- introduction: `MOST industrial processes` — "MOST industrial processes are nonlinear with highly uncertain and time-varying, and usually, it is difficult to obtain their accurate mathematical model[1]." (p.4919；栏首掉字)
- method: `The parameters, including` — "The parameters, including centers, widths and weights, and structure of the FNN are the key impacts on the performance of the network." (p.4921, III.A)
- experiments: `The performance of` — "The performance of TSTFNN is validated by a benchmark simulation and an experiment in a flotation industrial process." (p.4924)
- conclusion: `In this article` — "In this article, we aim to improve the generalization performance of FNN for industrial process identification." (p.4928)

## Gap transitions

- however (abstract): "Numerous studies on learning algorithms have been done in the neural networks community, however concerning to training strategy is limited." (p.4919)
- to enhance (abstract): "In this article, to enhance the performance of fuzzy neural network (FNN) in industrial process identification, an FNN based on two-stage training (TSTFNN) is proposed." (p.4919)
- however (introduction): "Studies concerning on training process, however, are limited according to the best knowledge of authors." (p.4920)
- to enhance (introduction): "To enhance the performance of FNN in industrial process identification, we propose a novel FNN with two-stage training (TSTFNN)." (p.4920)
- to overcome (method): "To overcome these shortcomings, a supervised clustering algorithm is proposed to determine the centers and number of neurons in the rule layer of TSTFNN." (p.4921)

## Hedge verbs

- propose / causal / abstract, introduction, method: "an FNN based on two-stage training (TSTFNN) is proposed"; "we propose a novel FNN with two-stage training"; "a supervised clustering algorithm is proposed"
- show / causal / abstract, experiments: "we show the convergence of TSTFNN"; "showing a good approximation performance"; "The experimental results show that TSTFNN achieves a satisfactory prediction performance"
- aim / speculative / conclusion: "In this article, we aim to improve the generalization performance of FNN"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II describes a basic FNN. Section III gives the details of TSTFNN. Experimental studies are presented in Section IV, and Section V concludes this article." (p.4920)
- method → experiments: 收敛证明后直接 `IV. EXPERIMENTAL STUDIES` (p.4924)
- experiments → conclusion: Discussions 段落后直接 `V. CONCLUSION` (p.4928)

## Candidate rules

- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main novelties and contributions are summarized in the following.` + 编号。
- R001 摘要用 `In this article, to enhance ..., ... is proposed`。
- R005 结论后续：`future work can be concentrated on`。

## Candidate phrases

- `In this article, to enhance the performance of ... is proposed` (abstract)
- `we propose a novel FNN with two-stage training (TSTFNN)` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, we aim to improve` (conclusion)
- `future work can be concentrated on` (conclusion)

## House style

自称 `In this article` / `we propose` / `we aim`。Method 有 `proposed in this paper`（两阶段训练策略段）。未见 `Here we`。`In this article` / `In this paper` / `we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.4919 abstract: Numerous studies on learning algorithms have been done in the neural networks community, however concerning to training strategy is limited.
- p.4919 abstract: In this article, to enhance the performance of fuzzy neural network (FNN) in industrial process identification, an FNN based on two-stage training (TSTFNN) is proposed.
- p.4919 abstract: The experimental results show that TSTFNN achieves a satisfactory prediction performance.
- p.4919 introduction: MOST industrial processes are nonlinear with highly uncertain and time-varying, and usually, it is difficult to obtain their accurate mathematical model[1].
- p.4920 introduction: Studies concerning on training process, however, are limited according to the best knowledge of authors.
- p.4920 introduction: To enhance the performance of FNN in industrial process identification, we propose a novel FNN with two-stage training (TSTFNN).
- p.4920 introduction: The main novelties and contributions are summarized in the following.
- p.4920 introduction: The rest of this article is organized as follows. Section II describes a basic FNN. Section III gives the details of TSTFNN. Experimental studies are presented in Section IV, and Section V concludes this article.
- p.4921 method: To overcome these shortcomings, a supervised clustering algorithm is proposed to determine the centers and number of neurons in the rule layer of TSTFNN.
- p.4922 method: To improve the generalization performance of TSTFNN, a two-stage training strategy based on feedback error classification is proposed in this paper.
- p.4924 experiments: The performance of TSTFNN is validated by a benchmark simulation and an experiment in a flotation industrial process.
- p.4928 experiments: To the best knowledge of the authors, most algorithms only involve one stage training, ignoring the use of samples with poor prediction results.
- p.4928 conclusion: In this article, we aim to improve the generalization performance of FNN for industrial process identification.
- p.4928 conclusion: Two benchmark simulations and experiments in an industrial rougher flotation process show that the generalization performance of TSTFNN is improved by using a two-stage training scheme, and TSTFNN yields better performance than other commonly used methods.
- p.4928 conclusion: Based on the discussion about the results, future work can be concentrated on analyzing why the network performs unsatisfactorily on some samples and using pattern recognize technology to improve the generalization performance of the network.
