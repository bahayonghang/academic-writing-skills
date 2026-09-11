---
key: X9J2ER9A
title: "Self-Tuning Transfer Dynamic Convolution Autoencoder for Quality Prediction of Multimode Processes With Shifts"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3399932"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. OVERVIEW OF RELATED WORKS` → `III. PROPOSED TDCAE ALGORITHM` → `IV. STDCAE FOR ONLINE COMPENSATION` → `V. CASE STUDY` → `VI. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCLATURE`。独立 Related Work，标题为 `OVERVIEW OF RELATED WORKS`。Introduction 末路标跨页指向 Section II–VI。Method 拆为 TDCAE 与 STDCAE 两节。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `Process shift of` — "Process shift of multimode process involving data distribution and dynamic relation makes traditional transfer learning methods be intractable and even result in negative transfer." (p.1)
- introduction: `IN the last` — "IN the last decade, data-driven quality prediction methods have been widely utilized in modern industrial processes due to the abilities to acquire relations between quality indicators and process measurements in a simple manner [1], [2]." (p.1)
- related_work: `Autoencoder is one` — "Autoencoder is one kind of deep models that can preserve dominant low-dimensional features for high dimension dataset and has gained popularity in recent years for quality prediction [48], nondestructive testing [49], etc." (p.3)
- method: `K steady operating` — "K steady operating modes of a multimode process are denoted as {M1,M2,...,MK}." (p.3, III.A)
- experiments: `In this section` — "In this section, the effectiveness of the proposed TDCAE and STDCAE methods is demonstrated through the TPFF process." (p.6)
- conclusion: `In this article` — "In this article, a new TL modeling framework based on dynamic convolution autoencoder, including TDCAE and STDCAE, has been successfully developed for online prediction of quality indicators for multimode processes with shifts." (p.9)

## Gap transitions

- to tackle (abstract): "To tackle this issue, this article proposes a novel self-tuning transfer dynamic modeling method for quality prediction of multimode processes." (p.1)
- however (introduction): "However, the existing work only considers feature disentanglement with static relation." (p.2)
- in view of this (introduction): "In view of this, this article proposes a transfer dynamic convolution autoencoder (TDCAE) with a feature decomposition structure for quality prediction of multimode dynamic processes with shifts." (p.2)
- to address (method): "To address this, after TDCAE is first adopted to perform prediction for a few labeled dataset from the new mode, the corresponding prediction errors that contain the private information of the target domain are obtained." (p.6)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a novel self-tuning transfer dynamic modeling method"; "this article proposes a transfer dynamic convolution autoencoder (TDCAE)"
- demonstrate / causal / abstract, experiments: "the efficacy of the proposed TDCAE and STDCAE is demonstrated"; "the effectiveness of the proposed TDCAE and STDCAE methods is demonstrated"
- develop / causal / conclusion: "has been successfully developed for online prediction"
- will focus / speculative / conclusion: "Future work will focus on the development of dynamic TL algorithms"
- would be interesting / speculative / conclusion: "it would be interesting to develop a domain generalization TL-based online quality prediction method"

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. We make an overview of related works on Autoencoder, 1DCNN, and VAR for dynamic modeling in Section II. Then, Section III gives the motivation and framework of the proposed TDCAE. Subsequently, an online compensation method called STDCAE is presented in Section IV. In Section V, the effectiveness of the proposed methods is demonstrated through a three-phase flow facility process (TPFF). Finally, Section VI concludes this article." (p.2–3)
- related_work → method: VAR 小节后 `III. PROPOSED TDCAE ALGORITHM` (p.3)
- method → experiments: STDCAE 公式后 `V. CASE STUDY` (p.6)
- experiments → conclusion: 消融后 `VI. CONCLUSION` (p.9)

## Candidate rules

- R006 独立 Related Work，标题可为 `OVERVIEW OF RELATED WORKS`，分 Autoencoder / 1DCNN / VAR 小节。
- R003 Introduction 末用 `The rest of this article is organized as follows`，路标可跨页。
- R004 贡献用 `The major contributions of this work are two-fold`。
- R012 摘要以问题句起，再用 `To tackle this issue, this article proposes`。

## Candidate phrases

- `To tackle this issue, this article proposes` (abstract)
- `In view of this, this article proposes` (introduction)
- `The major contributions of this work are two-fold.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `has been successfully developed for` (conclusion)
- `Future work will focus on the development of` (conclusion)

## House style

自称 `this article proposes` / `this work` / `the proposed TDCAE`。未见 `Here we`、`In this paper`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Process shift of multimode process involving data distribution and dynamic relation makes traditional transfer learning methods be intractable and even result in negative transfer.
- p.1 abstract: To tackle this issue, this article proposes a novel self-tuning transfer dynamic modeling method for quality prediction of multimode processes.
- p.1 abstract: Finally, the efficacy of the proposed TDCAE and STDCAE is demonstrated by a comprehensive study of a three-phase flow facility process.
- p.1 introduction: IN the last decade, data-driven quality prediction methods have been widely utilized in modern industrial processes due to the abilities to acquire relations between quality indicators and process measurements in a simple manner [1], [2].
- p.2 introduction: However, the existing work only considers feature disentanglement with static relation.
- p.2 introduction: In view of this, this article proposes a transfer dynamic convolution autoencoder (TDCAE) with a feature decomposition structure for quality prediction of multimode dynamic processes with shifts.
- p.2 introduction: The major contributions of this work are two-fold.
- p.2 introduction: The rest of this article is organized as follows. We make an overview of related works on Autoencoder, 1DCNN, and VAR for dynamic modeling in Section II. Then, Section III gives the motivation and framework of the proposed TDCAE. Subsequently, an online compensation method called STDCAE is presented in Section IV. In Section V, the effectiveness of the proposed methods is demonstrated through a three-phase flow facility process (TPFF). Finally, Section VI concludes this article.
- p.3 related_work: Autoencoder is one kind of deep models that can preserve dominant low-dimensional features for high dimension dataset and has gained popularity in recent years for quality prediction [48], nondestructive testing [49], etc.
- p.3 method: K steady operating modes of a multimode process are denoted as {M1,M2,...,MK}.
- p.6 experiments: In this section, the effectiveness of the proposed TDCAE and STDCAE methods is demonstrated through the TPFF process.
- p.9 conclusion: In this article, a new TL modeling framework based on dynamic convolution autoencoder, including TDCAE and STDCAE, has been successfully developed for online prediction of quality indicators for multimode processes with shifts.
- p.9 conclusion: Future work will focus on the development of dynamic TL algorithms that incorporate continuous memory mechanisms to avoid catastrophic forgetting of historical transfer tasks.
- p.9 conclusion: Moreover, it would be interesting to develop a domain generalization TL-based online quality prediction method for multimode processes when the target domain unlabeled dataset are not available.
