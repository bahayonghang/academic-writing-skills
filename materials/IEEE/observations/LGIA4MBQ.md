---
key: LGIA4MBQ
title: "Trend-Constrained Physics-Guided Neural Network With Prior-Embedded Slow Feature Analysis for Latent-Variable-Driven Industrial Soft Sensing"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2026.3700271"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. METHODOLOGY` → `IV. APPLICATION TO THE SODIUM ALUMINATE EVAPORATION PROCESS` → `V. CASE STUDIES` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 CNN/LSTM/AE、SFA 变体、PINNs）。Introduction 末有编号贡献与 `The rest of this article is organized as follows`。Method 拆成问题形式化（II）+ METHODOLOGY（III）+ 工业实例化（IV）。Experiments 标题为 `CASE STUDIES`。附录给趋势符号机理推导。

## Openers

- abstract: `In continuous industrial` — "In continuous industrial processes with long-term performance transitions, accurate estimation of key performance indicators is often hindered by slowly evolving latent variables that cannot be measured online, posing a persistent challenge for industrial soft sensing." (p.1)
- introduction: `ACCURATE estimation of` — "ACCURATE estimation of key performance indicators (KPIs) is essential for maintaining operational stability and ensuring product consistency in modern industrial processes [1]." (p.1)
- method: `To address the` — "To address the latent-variable-driven soft sensing problem formulated in Section II, a unified framework integrating prior-knowledge-embedded slow feature analysis and trend-constrained physics-guided learning is developed." (p.3, III)
- experiments: `To validate the` — "To validate the proposed framework instantiated in Section IV, an industrial dataset was collected from the sodium aluminate evaporation process in an alumina plant in southwest China during 2024–2025, with a sampling interval of one hour." (p.7, V.A)
- conclusion: `This article presents` — "This article presents a latent-variable-driven soft sensing framework that integrates PKE-SFA with trend-constrained physics-guided neural networks for industrial processes characterized by slowly evolving unobservable states." (p.11)

## Gap transitions

- despite (introduction): "Despite these advances, as industrial systems evolve over time and process behaviors grow more complex, modeling strategies that depend exclusively on explicit statistical correlations among observable variables increasingly exhibit limitations in characterizing underlying process dynamics." (p.1)
- therefore (introduction): "Therefore, incorporating physical consistency constraints and interpretability mechanisms into SFA has become a critical direction for enhancing the physical credibility of learned representations." (p.2)
- however (introduction): "However, the direct application of PINNs to industrial soft sensing remains challenging." (p.2)
- to address (introduction): "To address the aforementioned limitations, a novel latent-variable-driven industrial soft sensing framework is proposed." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "This article proposes a latent-variable-driven soft sensing framework"; "a novel latent-variable-driven industrial soft sensing framework is proposed"
- demonstrate / causal / abstract, conclusion: "Comparative results demonstrate improved prediction accuracy"; "Experimental validation ... demonstrates that the proposed approach achieves superior physical consistency"
- present / causal / conclusion: "This article presents a latent-variable-driven soft sensing framework"
- confirm / causal / conclusion: "Ablation studies further confirm the synergistic effect of soft physics regularization and hard trend-consistency constraints"

## Cross-section linkers

- introduction → problem: "The rest of this article is organized as follows. Section II formulates the latent-variable-driven soft sensing problem and analyzes its fundamental modeling challenges. Section III presents the proposed integrated framework comprising PKE-SFA and TC-PGNN modules. Section IV details the application to a sodium aluminate evaporation process, including industrial background and mechanism-related modeling considerations. Section V validates the framework through industrial case studies and comparative analysis. Finally, Section VI concludes this article and outlines future research directions." (p.2)
- problem → method: "To address the latent-variable-driven soft sensing problem formulated in Section II, a unified framework integrating prior-knowledge-embedded slow feature analysis and trend-constrained physics-guided learning is developed." (p.3)
- method → application: III 后接工业蒸发过程实例化 (p.6)
- application → experiments: "To validate the proposed framework instantiated in Section IV" 后接 `V. CASE STUDIES` (p.7)
- experiments → conclusion: 知识源消融后 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `This article proposes`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；SFA/PINN 评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 Method 前加 `PROBLEM FORMULATION`，再 `METHODOLOGY`。
- R005 Experiments 标题为 `CASE STUDIES`。
- R006 Conclusion 用 `This article presents`，再用 `Future work will focus on` 指向后续。

## Candidate phrases

- `This article proposes a latent-variable-driven soft sensing framework that` (abstract)
- `The rest of this article is organized as follows.` (introduction)
- `To address the latent-variable-driven soft sensing problem formulated in Section II` (method)
- `This article presents a latent-variable-driven soft sensing framework that` (conclusion)
- `Future work will focus on extending the framework to` (conclusion)

## House style

自称是 `This article proposes` / `the proposed framework` / `This article presents`。被动贡献句较多（`is proposed`）。未见 `Here we`。`This article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In continuous industrial processes with long-term performance transitions, accurate estimation of key performance indicators is often hindered by slowly evolving latent variables that cannot be measured online, posing a persistent challenge for industrial soft sensing.
- p.1 abstract: This article proposes a latent-variable-driven soft sensing framework that integrates slow feature analysis with embedded prior knowledge and a trend-constrained physics-guided neural network.
- p.1 introduction: ACCURATE estimation of key performance indicators (KPIs) is essential for maintaining operational stability and ensuring product consistency in modern industrial processes [1].
- p.1 introduction: Despite these advances, as industrial systems evolve over time and process behaviors grow more complex, modeling strategies that depend exclusively on explicit statistical correlations among observable variables increasingly exhibit limitations in characterizing underlying process dynamics.
- p.2 introduction: Therefore, incorporating physical consistency constraints and interpretability mechanisms into SFA has become a critical direction for enhancing the physical credibility of learned representations.
- p.2 introduction: However, the direct application of PINNs to industrial soft sensing remains challenging.
- p.2 introduction: The rest of this article is organized as follows. Section II formulates the latent-variable-driven soft sensing problem and analyzes its fundamental modeling challenges. Section III presents the proposed integrated framework comprising PKE-SFA and TC-PGNN modules. Section IV details the application to a sodium aluminate evaporation process, including industrial background and mechanism-related modeling considerations. Section V validates the framework through industrial case studies and comparative analysis. Finally, Section VI concludes this article and outlines future research directions.
- p.3 method: To address the latent-variable-driven soft sensing problem formulated in Section II, a unified framework integrating prior-knowledge-embedded slow feature analysis and trend-constrained physics-guided learning is developed.
- p.7 experiments: To validate the proposed framework instantiated in Section IV, an industrial dataset was collected from the sodium aluminate evaporation process in an alumina plant in southwest China during 2024–2025, with a sampling interval of one hour.
- p.8 experiments: The proposed framework achieves significant TCR improvements for all architectures, with eight of nine models exceeding 97% (e.g., MLP improves from 55.83% to 99.38%).
- p.11 conclusion: This article presents a latent-variable-driven soft sensing framework that integrates PKE-SFA with trend-constrained physics-guided neural networks for industrial processes characterized by slowly evolving unobservable states.
- p.11 conclusion: Experimental validation on an industrial sodium aluminate evaporation process demonstrates that the proposed approach achieves superior physical consistency and improved prediction accuracy compared with nine state-of-the-art deep learning baselines.
- p.11 conclusion: Future work will focus on extending the framework to processes with multiple interacting latent mechanisms and developing online adaptive strategies for dynamically updating slow feature extraction as process conditions evolve.
