---
key: QCPJLNGR
title: "Continuous Evolution Learning: A Lightweight Expansion-Based Continuous Learning Method for Train Transmission Systems Fault Diagnosis"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3588608"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROPOSED LIGHTWEIGHT EXPANSION-BASED CONTINUOUS LEARNING FRAMEWORK` → `III. EXPERIMENTAL STUDY` → `IV. CONCLUSION AND FUTURE WORK`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评数据驱动故障诊断、模型扩展持续学习、轻量化与近期 lightweight CL）。Introduction 末为编号贡献与 `The organization of this article is as follows`。Method 标题为框架名。Experiments 标题为 `EXPERIMENTAL STUDY`。Conclusion 与 Future Work 并为一节。

## Openers

- abstract: `The dynamic fault` — "The dynamic fault environment, incremental data accumulation, and specific needs in train transmission systems make continual learning essential for fault diagnosis." (p.8270)
- introduction: `WITH the rapid` — "WITH the rapid development of rail transit, the safety and reliability requirements for subway trains are becoming increasingly stringent [1]." (p.8270)
- method: `Fig. 2 illustrates` — "Fig. 2 illustrates the framework of the proposed method." (p.8272, II.A)
- experiments: `The study utilized` — "The study utilized a self-developed subway bogie fault simulation test bench and the HIT Laboratory’s rotary machinery bearing-gear compound test bench." (p.8275, III)
- conclusion: `To address the` — "To address the high computational cost and delayed evolution caused by insufficient new class samples in existing expansion-based continual learning methods, this paper proposes a novel lightweight continual learning diagnostic framework." (p.8280)

## Gap transitions

- however (introduction): "However, traditional data-driven fault diagnosis methods mostly rely on predefined fault patterns, making it difficult to handle the continuously evolving fault modes of subway train steering systems over long-term operations [7]." (p.8270)
- although (introduction): "Although model expansion-based continual learning offers advantages in fault diagnosis, it faces key challenges." (p.8271)
- however (introduction): "However, most current lightweight design methods focus primarily on static tasks, and their performance tends to degrade in dynamic tasks due to the inability to effectively handle knowledge accumulation and the trade-off between old and new tasks[20]." (p.8271)
- based on (introduction): "Based on the above analysis, a novel lightweight expansion-based continuous learning (LECL) framework is proposed to address the dual challenges of efficient incremental adaptation and long-term retention in evolving fault diagnosis tasks." (p.8271)

## Hedge verbs

- introduce / causal / abstract: "This article introduces a lightweight continual learning method based on model expansion."
- propose / causal / introduction, conclusion: "a novel lightweight expansion-based continuous learning (LECL) framework is proposed"; "this paper proposes a novel lightweight continual learning diagnostic framework"
- validate / causal / introduction: "The proposed method is validated on a custom-built subway train transmission system platform"
- show / causal / conclusion: "Although the proposed method shows clear advantages, several limitations remain."

## Cross-section linkers

- introduction → method: "The organization of this article is as follows: Section II outlines the proposed methodology. Section III provides detailed discussions of the experimental work. Section IV offers the conclusions drawn from the research, along with recommendations for future work." (p.8272)
- method → experiments: 知识增强/压缩总损失后 `III. EXPERIMENTAL STUDY` (p.8275)
- experiments → conclusion: 开集诊断后 `IV. CONCLUSION AND FUTURE WORK` (p.8280)

## Candidate rules

- R001 abstract 用 `This article introduces`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；持续学习/轻量化评述写在引言中段。
- R003 Introduction 末用 `The organization of this article is as follows` 指向 II–IV。
- R004 Conclusion 与 Future Work 并为一节。
- R005 Conclusion 用 `this paper proposes`，再用 `Future work will explore` 指向后续。

## Candidate phrases

- `This article introduces a lightweight continual learning method based on` (abstract)
- `The main contributions of this article are given as follows.` (introduction)
- `The organization of this article is as follows:` (introduction)
- `this paper proposes a novel lightweight continual learning diagnostic framework` (conclusion)
- `Future work will explore integrating` (conclusion)

## House style

自称是 `This article introduces` / `this paper proposes` / `the proposed method`。`this paper` 与 `This article` 并用。未见 `Here we`。`This article introduces` / `this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.8270 abstract: The dynamic fault environment, incremental data accumulation, and specific needs in train transmission systems make continual learning essential for fault diagnosis.
- p.8270 abstract: This article introduces a lightweight continual learning method based on model expansion.
- p.8270 introduction: WITH the rapid development of rail transit, the safety and reliability requirements for subway trains are becoming increasingly stringent [1].
- p.8270 introduction: However, traditional data-driven fault diagnosis methods mostly rely on predefined fault patterns, making it difficult to handle the continuously evolving fault modes of subway train steering systems over long-term operations [7].
- p.8271 introduction: Although model expansion-based continual learning offers advantages in fault diagnosis, it faces key challenges.
- p.8271 introduction: Based on the above analysis, a novel lightweight expansion-based continuous learning (LECL) framework is proposed to address the dual challenges of efficient incremental adaptation and long-term retention in evolving fault diagnosis tasks.
- p.8271 introduction: The main contributions of this article are given as follows.
- p.8272 introduction: The organization of this article is as follows: Section II outlines the proposed methodology. Section III provides detailed discussions of the experimental work. Section IV offers the conclusions drawn from the research, along with recommendations for future work.
- p.8272 method: Fig. 2 illustrates the framework of the proposed method.
- p.8275 experiments: The study utilized a self-developed subway bogie fault simulation test bench and the HIT Laboratory’s rotary machinery bearing-gear compound test bench.
- p.8277 experiments: In Table III, it can be seen that the complete model performs the best in all stages, indicating that the strategy constructed in this paper is effective in the process of continuous diagnosis and evolution.
- p.8280 conclusion: To address the high computational cost and delayed evolution caused by insufficient new class samples in existing expansion-based continual learning methods, this paper proposes a novel lightweight continual learning diagnostic framework.
- p.8280 conclusion: Although the proposed method shows clear advantages, several limitations remain.
- p.8280 conclusion: Future work will explore integrating multimodal data fusion and adaptive dynamic evolution into lightweight continual learning.
