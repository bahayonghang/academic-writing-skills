---
key: BT92GHKE
title: "Machine learning for industrial sensing and control: A survey and practical perspective"
venue: "Control Engineering Practice"
doi: "10.1016/j.conengprac.2024.105841"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8,20-36"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Motivation`（含 `1.1. Overview and scope`）→ `2. Mathematical modeling approaches` → `3` 软测量（含 `3.5. Challenges in soft sensor development`）→ `4. Data-driven and hybrid modeling approaches for optimization and control` → `5. Discussion`（含 `5.1. Conclusions`）。前置 Abstract / Keywords。无独立 Related Work。`related_work=inlined`（Motivation 与各应用节内嵌综述）。Survey 无独立 Experiments；应用证据在 soft sensing 与 control 两节。Motivation 末有范围说明。PDF 为期刊对应 arXiv preprint。

## Openers

- abstract: `With the rise` — "With the rise of deep learning, there has been renewed interest within the process industries to utilize data on large-scale nonlinear sensing and control problems."
- introduction: `Data analytics and` — "Data analytics and machine learning (ML) ideas are not new to the process industries."
- method: `The core applications` — "The core applications of this paper are soft sensing and process optimization and control."
- experiments: `We revisit data-driven` — "We revisit data-driven and hybrid modeling in the context of solving optimization and control problems."
- conclusion: `Recent advances in` — "Recent advances in machine learning give us renewed optimism for achieving higher levels of automation in the process industries."

## Gap transitions

- despite (introduction): "Despite the longstanding success of many statistical techniques in industry, there is also considerable interest in developing sensing and control technologies based on more recent ML architectures [1, 8, 9]."
- however (scope): "However, we have tried our best to include some of the most critical developments of ML tools in the process industries."
- by contrast (method): "By contrast, data-driven models require little physical knowledge and are fast to deploy or maintain."
- however (control): "However, comparatively little work has been published on embedding hybrid models into MPC to reduce data dependency and infuse physical knowledge for better extrapolation capability [88, 89]."
- despite (RL): "Despite these advances, model-free RL algorithms alone are not sufficiently data-efficient and, therefore, not yet useful in real industrial applications [154]."

## Hedge verbs

- identify / causal / abstract: "We identify key statistical and machine learning techniques that have seen practical success in the process industries."
- highlight / causal / abstract: "As a result, we highlight ways prior knowledge may be integrated into industrial machine learning applications."
- is poised / associative / abstract: "The treatment of methods, problems, and applications presented here is poised to inform and inspire practitioners and researchers to develop impactful data-driven sensing, optimization, and control solutions in the process industries."
- addresses / causal / introduction: "Consequently, this paper addresses the need to dissect and organize the general use of modern ML techniques in industrial applications."
- may / hedge / abstract: "As a result, we highlight ways prior knowledge may be integrated into industrial machine learning applications."
- have strived / causal / conclusion: "Through synthesizing research trends and industrial requirements, we have strived to enable academics and practitioners alike to develop sophisticated yet practical methods for building better models and controllers."

## Cross-section linkers

- motivation → method: "Hybrid modeling is first introduced to provide a conceptual framework underlying core application areas"
- method → soft sensing: "Hybrid models may be used to enable soft sensors (see Section 3) or model-based optimization and control (see Section 4) in a first principles approach."
- soft sensing → control: "4. Data-driven and hybrid modeling approaches for optimization and control"
- control → discussion: "5. Discussion"
- discussion → conclusion: "5.1. Conclusions"

## Candidate rules

- R002 Related Work 并入 Motivation / 各应用节（survey）。
- R003 范围路标：`This paper is a significant extension of Gopaluni et al. [11]`
- R009 自称：`We identify` / `this paper addresses` / `we have strived`

## Candidate phrases

- `We identify key statistical and machine learning techniques that have seen practical success in the process industries.` (abstract)
- `This paper is a significant extension of Gopaluni et al. [11]` (introduction)
- `The core applications of this paper are soft sensing and process optimization and control.` (method)
- `A common challenge is the interpretability and efficiency of purely data-driven methods.` (abstract)
- `Recent advances in machine learning give us renewed optimism for achieving higher levels of automation in the process industries.` (conclusion)

## House style

自称 `We identify` / `this paper addresses` / `we have strived`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: With the rise of deep learning, there has been renewed interest within the process industries to utilize data on large-scale nonlinear sensing and control problems.
- abstract: We identify key statistical and machine learning techniques that have seen practical success in the process industries.
- abstract: A common challenge is the interpretability and efficiency of purely data-driven methods.
- abstract: This suggests a need to carefully balance deep learning techniques with domain knowledge.
- introduction: Data analytics and machine learning (ML) ideas are not new to the process industries.
- introduction: Consequently, this paper addresses the need to dissect and organize the general use of modern ML techniques in industrial applications.
- method: The core applications of this paper are soft sensing and process optimization and control.
- method: The basic idea behind hybrid models is to combine knowledge-driven and data-driven models in such a way as to overcome their respective limitations.
- experiments: We revisit data-driven and hybrid modeling in the context of solving optimization and control problems.
- conclusion: Recent advances in machine learning give us renewed optimism for achieving higher levels of automation in the process industries.
- conclusion: Soft sensing represents the most dominant area regarding industrial applications of statistical and machine learning techniques.
- conclusion: Through synthesizing research trends and industrial requirements, we have strived to enable academics and practitioners alike to develop sophisticated yet practical methods for building better models and controllers.
