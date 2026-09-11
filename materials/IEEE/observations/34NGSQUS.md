---
key: 34NGSQUS
title: "Self-Supervised-Enabled Open-Set Cross-Domain Fault Diagnosis Method for Rotating Machinery"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3396335"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "10314-10324"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROPOSED SEOC MODEL` → `III. EXPERIMENTS` → `IV. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 DA、MMD/CORAL、adversarial DA、partial DA、open-set EVT/weighting/dual adversarial）。Introduction 末有节序路标，指向 Section II–IV。Experiments 标题为 `EXPERIMENTS`。四节结构，方法紧接引言。

## Openers

- abstract: `Crossing different working` — "Crossing different working conditions is a common scenario in rotating machinery fault diagnosis, which can be solved by cross-domain transfer learning." (p.10314)
- introduction: `THE applications of` — "THE applications of rotary machinery have spurred industrial development [1], [2]." (p.10314)
- method: `The framework of` — "The framework of the proposed SEOC approach is illustrated in Fig. 1." (p.10315)
- experiments: `The original vibration` — "The original vibration signals of the three-phase motor fault are collected on our experimental rig, as shown in Fig. 2." (p.10318)
- conclusion: `In this article` — "In this article, a new SEOC model was proposed for open-set cross-domain fault diagnosis." (p.10323)

## Gap transitions

- however (abstract): "However, the existing diagnosis methods do not consider possibly new and unknown faults, i.e., open-set fault diagnosis scenarios, which would cause diagnosis performance degradation." (p.10314)
- to address (abstract): "To address this issue, in this article, the self-supervised-enabled open-set cross-domain (SEOC) approach is proposed for fault diagnosis of rotary machines under various working conditions." (p.10314)
- however (introduction): "However, rotary machines usually work under extreme conditions, some key components are prone to faults and may cause tremendous property losses and casualties [3], [4], [5]." (p.10314)
- unfortunately (introduction): "Unfortunately, in practical applications, the changing working conditions of rotating machinery equipment would lead to data distribution discrepancy [11], [12]." (p.10314)
- to solve (introduction): "To solve the problem above, this work proposed a self-supervised-enabled open-set cross-domain (SEOC) approach for fault diagnosis of rotating machinery." (p.10315)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "the ... SEOC approach is proposed"; "this work proposed a ... SEOC approach"; "a new SEOC model was proposed"
- illustrate / causal / abstract, experiments: "Experiments on three-phase motor and bearing datasets illustrate the superior and efficient performance"; "compared results ... illustrate that the proposed method"
- would / speculative / abstract, introduction: "which would cause diagnosis performance degradation"; "would lead to data distribution discrepancy"
- will focus / speculative / conclusion: "In the future, we will focus on exploring open-set diagnostic methods"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. In Section II, the proposed SEOC framework is illustrated. In Section III, experiments are investigated to demonstrate the efficacy of the proposed SEOC fault diagnosis framework. Finally, Section IV concludes this article." (p.10315)
- method → experiments: Algorithm 1 与总损失后 `III. EXPERIMENTS` (p.10318)
- experiments → conclusion: 消融表后 `IV. CONCLUSION` (p.10323)

## Candidate rules

- R002 Introduction 无独立 Related Work，DA/open-set 评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–IV。
- R004 贡献用 `The main contributions of this article are as follows`；条目可用 `To overcome` / `To suppress` 目的不定式。
- R005 Conclusion 先收回四模块，再用 `In the future, we will focus on`。

## Candidate phrases

- `To address this issue, in this article, the ... approach is proposed` (abstract)
- `To solve the problem above, this work proposed` (introduction)
- `The main contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a new SEOC model was proposed for` (conclusion)
- `In the future, we will focus on exploring` (conclusion)

## House style

自称 `in this article` / `this work proposed` / `the proposed SEOC method` / `we will focus`。未见 `Here we`、`In this paper`。`in this article` 与 `this work proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.10314 abstract: Crossing different working conditions is a common scenario in rotating machinery fault diagnosis, which can be solved by cross-domain transfer learning.
- p.10314 abstract: However, the existing diagnosis methods do not consider possibly new and unknown faults, i.e., open-set fault diagnosis scenarios, which would cause diagnosis performance degradation.
- p.10314 abstract: To address this issue, in this article, the self-supervised-enabled open-set cross-domain (SEOC) approach is proposed for fault diagnosis of rotary machines under various working conditions.
- p.10314 abstract: Experiments on three-phase motor and bearing datasets illustrate the superior and efficient performance of the proposed SEOC method.
- p.10314 introduction: THE applications of rotary machinery have spurred industrial development [1], [2].
- p.10314 introduction: However, rotary machines usually work under extreme conditions, some key components are prone to faults and may cause tremendous property losses and casualties [3], [4], [5].
- p.10314 introduction: Unfortunately, in practical applications, the changing working conditions of rotating machinery equipment would lead to data distribution discrepancy [11], [12].
- p.10315 introduction: To solve the problem above, this work proposed a self-supervised-enabled open-set cross-domain (SEOC) approach for fault diagnosis of rotating machinery.
- p.10315 introduction: The main contributions of this article are as follows.
- p.10315 introduction: The rest of this article is organized as follows. In Section II, the proposed SEOC framework is illustrated. In Section III, experiments are investigated to demonstrate the efficacy of the proposed SEOC fault diagnosis framework. Finally, Section IV concludes this article.
- p.10315 method: The framework of the proposed SEOC approach is illustrated in Fig. 1.
- p.10318 experiments: The original vibration signals of the three-phase motor fault are collected on our experimental rig, as shown in Fig. 2.
- p.10323 conclusion: In this article, a new SEOC model was proposed for open-set cross-domain fault diagnosis.
- p.10323 conclusion: In the future, we will focus on exploring open-set diagnostic methods for faults of different components in complex mechanical equipment while focusing on problems, such as data imbalance and small samples.
