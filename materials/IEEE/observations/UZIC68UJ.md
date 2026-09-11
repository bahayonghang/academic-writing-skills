---
key: UZIC68UJ
title: "AMCT-Former: An Asynchronous Multi-Rate Continuous-Time Transformer for Industrial Soft Sensing"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2026.3702920"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评插值/重采样、clockwork RNN、层次自注意力、interval-aware Transformer）。II 为 Preliminaries（Transformer 依赖学习 / 不规则序列连续时间表示）。Method 在 III。Experiments 标题为 `IV. CASE STUDY`（WWTP + PPGAS）。Introduction 无单独 “rest of this paper” 路标，贡献列表后直接进入 II。

## Openers

- abstract: `Soft sensors are` — "Soft sensors are essential for online prediction of key quality variables in industrial processes." (p.11159)
- introduction: `IN COMPLEX industrial` — "IN COMPLEX industrial processes, key quality variables are often difficult to measure directly, in real time, and reliably using online instruments, which limits process monitoring, quality control, and operational optimization [1], [2]." (p.11159；栏首掉字)
- method: `This section introduces` — "This section introduces the proposed AMCT-Former framework for asynchronous multi-rate soft sensing." (p.11161, III)
- experiments: `To evaluate the` — "To evaluate the effectiveness of the proposed AMCT-Former, two real-world industrial soft sensing case studies are conducted on a wastewater treatment plant process (WWTP) and a combined-cycle power plant gas turbine process (PPGAS)." (p.11165, IV)
- conclusion: `This paper proposes` — "This paper proposes AMCT-Former, a continuous-time Transformer model for asynchronous multi-rate industrial soft sensing." (p.11169)

## Gap transitions

- however (abstract): "However, practical process data are often affected by asynchronous sensor sampling, delayed laboratory analysis, and heterogeneous update frequencies, resulting in pronounced multi-rate characteristics." (p.11159)
- to address (abstract): "To address this issue, this paper proposes an asynchronous multi-rate continuous-time Transformer, termed AMCT-Former, for industrial soft sensing." (p.11159)
- therefore (introduction): "Therefore, achieving accurate and reliable quality-variable prediction under multiple sampling rates has become an important issue in industrial soft sensor modeling." (p.11159)
- although (introduction): "Although these methods improve the usability of multi-source data and enhance soft-sensor modeling under multi-rate conditions, they are still largely built upon discrete-time representations and cannot explicitly preserve the actual observation times, inter-event intervals, and observation staleness of variables." (p.11160)
- however (introduction): "However, existing Transformer-based models usually rely on regular temporal tokens or interval-aware discrete representations as inputs, making them difficult to directly adapt to asynchronous multi-rate event streams." (p.11160)
- to this end (introduction): "To this end, an asynchronous multi-rate continuous-time Transformer, termed AMCT-Former, is proposed." (p.11160)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this paper proposes an asynchronous multi-rate continuous-time Transformer"; "This paper proposes AMCT-Former"
- demonstrate / causal / abstract, conclusion: "Case studies on two real-world industrial processes demonstrate the effectiveness and superiority of the proposed method"; "Experimental results ... demonstrate that AMCT-Former achieves superior prediction accuracy"
- indicate / causal / practitioners, experiments: "The case studies indicate that AMCT-Former can serve as a practical option"; "This result indicates that continuous-time encoding is a key source of performance improvement"
- may / speculative / practitioners: "forcing all variables onto a unified sampling grid through interpolation or resampling may introduce artificial temporal patterns"
- can (future) / speculative / conclusion: "Uncertainty estimation and abnormal observation detection can be introduced to enhance prediction credibility"

## Cross-section linkers

- introduction → preliminaries: 贡献列表后直接 `II. PRELIMINARIES`，无 `The rest of this paper` (p.11160)
- preliminaries → method: 连续时间 CDE 公式后直接 `III. METHODOLOGY` (p.11161)
- method → experiments: Algorithm 1 后直接 `IV. CASE STUDY` (p.11165)
- experiments → conclusion: Ablation 段落后直接 `V. CONCLUSION` (p.11169)

## Candidate rules

- R001 TASE 在 Abstract 后接 `Note to Practitioners—`，强调不要用插值把变量强行对齐到统一网格。
- R002 Introduction 无独立 Related Work；相关工作嵌在多速率软测量与 Transformer 两段评述中。
- R003 贡献用 `The contributions of this study are summarized:` + 编号 (1)(2)(3)，不用 `main contributions of this paper`。
- R004 无 Introduction 末节序路标；节间靠标题切换。
- R005 Conclusion 先 `This paper proposes` 收回框架，再用 `Future work will focus on` 指向部署鲁棒性。

## Candidate phrases

- `To address this issue, this paper proposes` (abstract)
- `To this end, an asynchronous multi-rate continuous-time Transformer, termed AMCT-Former, is proposed.` (introduction)
- `The contributions of this study are summarized:` (introduction)
- `This section introduces the proposed` (method)
- `This paper proposes AMCT-Former` (conclusion)
- `Future work will focus on` (conclusion)

## House style

自称是 `this paper proposes` / `The proposed method` / `this study` / `AMCT-Former`。未见 `Here we`。`this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` / `we propose` 作开篇（摘要用 `this paper proposes`；引言用被动 `is proposed`）。

## Quotes

- p.11159 abstract: Soft sensors are essential for online prediction of key quality variables in industrial processes.
- p.11159 abstract: However, practical process data are often affected by asynchronous sensor sampling, delayed laboratory analysis, and heterogeneous update frequencies, resulting in pronounced multi-rate characteristics.
- p.11159 abstract: To address this issue, this paper proposes an asynchronous multi-rate continuous-time Transformer, termed AMCT-Former, for industrial soft sensing.
- p.11159 abstract: Case studies on two real-world industrial processes demonstrate the effectiveness and superiority of the proposed method for asynchronous multi-rate soft sensing.
- p.11159 introduction: IN COMPLEX industrial processes, key quality variables are often difficult to measure directly, in real time, and reliably using online instruments, which limits process monitoring, quality control, and operational optimization [1], [2].
- p.11160 introduction: Although these methods improve the usability of multi-source data and enhance soft-sensor modeling under multi-rate conditions, they are still largely built upon discrete-time representations and cannot explicitly preserve the actual observation times, inter-event intervals, and observation staleness of variables.
- p.11160 introduction: However, existing Transformer-based models usually rely on regular temporal tokens or interval-aware discrete representations as inputs, making them difficult to directly adapt to asynchronous multi-rate event streams.
- p.11160 introduction: To this end, an asynchronous multi-rate continuous-time Transformer, termed AMCT-Former, is proposed.
- p.11160 introduction: The contributions of this study are summarized:
- p.11161 method: This section introduces the proposed AMCT-Former framework for asynchronous multi-rate soft sensing.
- p.11165 experiments: To evaluate the effectiveness of the proposed AMCT-Former, two real-world industrial soft sensing case studies are conducted on a wastewater treatment plant process (WWTP) and a combined-cycle power plant gas turbine process (PPGAS).
- p.11166 experiments: As reported in Table II, AMCT-Former achieved the best results on the WWTP dataset across all four evaluation metrics, with an MAE of 12.579, an RMSE of 21.385, a MAPE of 1.283%, and an R2 of 0.988.
- p.11169 conclusion: This paper proposes AMCT-Former, a continuous-time Transformer model for asynchronous multi-rate industrial soft sensing.
- p.11169 conclusion: Experimental results on two real-world industrial datasets demonstrate that AMCT-Former achieves superior prediction accuracy and fitting stability over comparison methods, while ablation studies verify the effectiveness and complementarity of its core components.
- p.11169 conclusion: Future work will focus on improving the robustness and reliability of the model in practical industrial deployment.
