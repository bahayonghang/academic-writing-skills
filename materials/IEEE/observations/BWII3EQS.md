---
key: BWII3EQS
title: "Data-Driven Soft Sensor for Hot Strip Mill Process Based on Multiscale Information-Fusion Attention Network"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3450083"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-7,9-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BRIEF INTRODUCTION TO HOT STRIP MILL PROCESS AND ATTENTION MECHANISM` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLSR / KSVR / MDA-JITL / LSSVM / NN / GcForest / SHAP-ANN / attention-LSTM / spatio-temporal AM）。II 为过程与 attention 预备。Introduction 末有 `The rest of this article is organized as follows`，指向 Section II–V。Method 在 III。Experiments 标题为 `EXPERIMENTS`（真实热连轧厂数据）。

## Openers

- abstract: `Mechanical properties (MPs)` — "Mechanical properties (MPs) of the hot strip mill process (HSMP), as key indicators of product quality, are always difficult to measure online due to cost or technological limitations." (p.1)
- introduction: `HOT strip mill` — "HOT strip mill process (HSMP) is a critical step of strip production in modern steelmaking [1], [2]." (p.1；栏首掉字)
- method: `This section elaborates` — "This section elaborates on the proposed MIAN soft sensor." (p.3, III)
- experiments: `In this section` — "In this section, a real-world HSMP is used to conduct the quality prediction performance evaluation of the proposed MIAN soft sensor." (p.7, IV)
- conclusion: `In this paper` — "In this paper, a novel data-driven soft sensor named MIAN for HSMP has been developed, which can predict MPs of the steel strips online." (p.10)

## Gap transitions

- nevertheless (introduction): "Nevertheless, high investment and maintenance costs have also limited its popularity." (p.1)
- however (introduction): "These methods are relatively simple and well-established, however, they are not very good at learning complex feature representations." (p.1)
- however (introduction): "However, they either necessitate the process mechanism knowledge [29] or make insufficient use of the supervision information (ground truth labels) [24]–[28], [30], [31]." (p.2)
- toward this end (introduction): "Toward this end, we propose a novel data-driven soft sensor approach, named multi-scale information-fusion attention network (MIAN) for MP prediction in HSMP." (p.2)
- despite (conclusion): "Despite its effectiveness, it requires sufficient labeled samples and does not specifically distinguish steel grades for training." (p.10)

## Hedge verbs

- propose / causal / abstract, introduction: "a data-driven soft sensor approach, named Multi-scale Information-fusion Attention Network (MIAN), is proposed"; "we propose a novel data-driven soft sensor approach"
- develop / causal / abstract, conclusion: "an Intrinsic Property-guided Feature Extractor (IPFE) is developed"; "a novel data-driven soft sensor named MIAN for HSMP has been developed"
- show / causal / introduction, conclusion: "The experimental results show that MIAN outperforms other state-of-the-art methods"; "Experimental results show that MIAN significantly improves"
- elucidate / causal / abstract: "Extensive experimental results on HSMP data ... elucidate that the proposed soft sensor outperforms the state-of-the-art methods"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II briefly introduces HSMP and attention mechanism. In Section III, the proposed MIAN soft sensor is illustrated and discussed. Extensive verification experiments are conducted in Section IV. Finally, Section V concludes this article and gives future work." (p.2)
- method → experiments: 在线预测公式后 `IV. EXPERIMENTS` (p.7)
- experiments → conclusion: λ 收敛曲线后 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `In this paper, a data-driven soft sensor approach, named ..., is proposed`。
- R002 Introduction 无独立 Related Work；缺口收口用 `Toward this end, we propose`。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V，末句带 `and gives future work`。
- R004 贡献用 `The main contributions of this paper are summarized as follows.` + 编号 1)–2)。
- R005 Conclusion 用现在完成时 `has been developed` / `have been conducted`，再用 `Despite its effectiveness` 与 `Future work will focus on extending`。

## Candidate phrases

- `In this paper, a data-driven soft sensor approach, named ..., is proposed for` (abstract)
- `Toward this end, we propose a novel data-driven soft sensor approach, named` (introduction)
- `The main contributions of this paper are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this paper, a novel data-driven soft sensor named ... has been developed, which can` (conclusion)
- `Future work will focus on extending the proposed method to deal with more complex scenarios, such as` (conclusion)

## House style

自称混用 `In this paper`（摘要、引言、结论）与 `The rest of this article`（路标）。也用 `we propose`。未见 `Here we`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Mechanical properties (MPs) of the hot strip mill process (HSMP), as key indicators of product quality, are always difficult to measure online due to cost or technological limitations.
- p.1 abstract: In this paper, a data-driven soft sensor approach, named Multi-scale Information-fusion Attention Network (MIAN), is proposed for MP prediction of the steel strip in HSMP.
- p.1 abstract: Extensive experimental results on HSMP data collected from a real Iron & Steel Co., Ltd, China elucidate that the proposed soft sensor outperforms the state-of-the-art methods in terms of Root Mean Square Error (RMSE), Mean Absolute Error (MAE), and R-square (R2).
- p.1 introduction: HOT strip mill process (HSMP) is a critical step of strip production in modern steelmaking [1], [2].
- p.1 introduction: Nevertheless, high investment and maintenance costs have also limited its popularity.
- p.1 introduction: These methods are relatively simple and well-established, however, they are not very good at learning complex feature representations.
- p.2 introduction: However, they either necessitate the process mechanism knowledge [29] or make insufficient use of the supervision information (ground truth labels) [24]–[28], [30], [31].
- p.2 introduction: Toward this end, we propose a novel data-driven soft sensor approach, named multi-scale information-fusion attention network (MIAN) for MP prediction in HSMP.
- p.2 introduction: The main contributions of this paper are summarized as follows.
- p.2 introduction: The rest of this article is organized as follows. Section II briefly introduces HSMP and attention mechanism. In Section III, the proposed MIAN soft sensor is illustrated and discussed. Extensive verification experiments are conducted in Section IV. Finally, Section V concludes this article and gives future work.
- p.3 method: This section elaborates on the proposed MIAN soft sensor.
- p.7 experiments: In this section, a real-world HSMP is used to conduct the quality prediction performance evaluation of the proposed MIAN soft sensor.
- p.10 conclusion: In this paper, a novel data-driven soft sensor named MIAN for HSMP has been developed, which can predict MPs of the steel strips online.
- p.10 conclusion: Experimental results show that MIAN significantly improves the soft sensor performance compared with other state-of-the-art methodologies in terms of RMSE, MAE, and R2.
- p.10 conclusion: Despite its effectiveness, it requires sufficient labeled samples and does not specifically distinguish steel grades for training.
- p.10 conclusion: Future work will focus on extending the proposed method to deal with more complex scenarios, such as those where labeled samples are scarce and new steel grades are frequently brought online.
