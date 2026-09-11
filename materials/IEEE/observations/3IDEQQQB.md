---
key: 3IDEQQQB
title: "Reinforcement Learning in Process Industries: Review and Perspective"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2024.124227"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,12-18"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. Introduction` → `II. Recent Innovations in Control and Learning Technologies` → `III.`（RL theory，引言路标）→ `IV.`（文献综述，引言路标）→ `V. Discussion`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 supply chain / process control / FDD 既有综述，再声明缺 unified control hierarchy 综述）。Introduction 末有节序路标，指向 Section II–V。无 Experiments 节；应用综述在 Section IV，收束在 `V. Discussion`（非 `Conclusion`）。

## Openers

- abstract: `This survey paper` — "This survey paper provides a review and perspective on intermediate and advanced reinforcement learning (RL) techniques in process industries." (p.1)
- introduction: `REINFORCEMENT learning (RL)` — "REINFORCEMENT learning (RL) has emerged as an effective tool for solving complex decision-making problems in a wide range of fields." (p.1；栏首掉字)
- method: `Process control is` — "Process control is a highly interdisciplinary field that has been evolving from the earliest forms of proportional-integral-derivative (PID) controllers to the more sophisticated optimal control schemes." (p.3, II.A)
- discussion: `Besides these developments` — "Besides these developments in process industries, the RL literature is evolving rapidly in various fields." (p.12, V)

## Gap transitions

- despite (introduction): "Despite these advancements outside process industries, most of the RL methodologies use a combination of learning and process control techniques extensively studied in the optimization and control of process industries [2]." (p.1)
- however (introduction): "However, there is still a lack of a comprehensive review of the state-of-the-art theory, outstanding challenges in the unified control hierarchy, and possible improvements for practical solutions beyond toy problems and small-scale implementations." (p.2)
- however (introduction): "However, Industry 5.0 introduces new challenges like cross-layer network optimization and privacy/security protection." (p.2)
- however (discussion): "However, this approach fails to consider the interconnectedness of multiple levels in most process industries, which can significantly impact the overall performance of the control system." (p.13)

## Hedge verbs

- provide / causal / abstract: "This survey paper provides a review and perspective"
- present / causal / abstract, introduction: "The survey paper presents a comprehensive overview of RL algorithms"; "the main contributions of this manuscript are to show"
- discuss / causal / abstract: "The survey paper discusses the limitations and advantages, trends and new applications"
- highlight / causal / abstract: "it highlights the need for a holistic approach"
- can / speculative / discussion: "applying RL in complex process industries can lead to more efficient, reliable, and sustainable processes"

## Cross-section linkers

- introduction → body: "The manuscript is organized as follows. Section II progressively introduces the motivation behind RL in process industries, Section III mathematically explores the RL theory, Section IV reviews the recent literature with a focus on soft sensor design, process control, fault detection and diagnosis, fault tolerant control, optimization, planning, scheduling, and supply chain management. Then, Section V discusses the outstanding problems and possible extensions that researchers and professionals of process industries can consider." (p.2)
- IV → V: "Besides these developments in process industries, the RL literature is evolving rapidly in various fields." 随后 `V. Discussion` (p.12)

## Candidate rules

- R001 survey 摘要自称 `This survey paper provides` / `The survey paper presents`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，既有综述评述写在引言中段，再用 `However, there is still a lack of a comprehensive review` 立 gap。
- R003 Introduction 末用 `The manuscript is organized as follows` 指向 II–V。
- R004 贡献句用 `the main contributions of this manuscript are to` 并列动词（show / introduce / present / discuss）。
- R005 收束节标题为 `V. Discussion`，不用 `Conclusion`；先局限再趋势再未来。

## Candidate phrases

- `This survey paper provides a review and perspective on` (abstract)
- `The survey paper presents a comprehensive overview of` (abstract)
- `However, there is still a lack of a comprehensive review of` (introduction)
- `the main contributions of this manuscript are to` (introduction)
- `The manuscript is organized as follows.` (introduction)

## House style

自称是 `This survey paper` / `The survey paper` / `this manuscript` / `this article` / `this study`。未见 `Here we`。`In this paper` 仅出现在图表说明（“Color versions of one or more of the figures in this paper”）。`This survey paper` 与 `this manuscript` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: This survey paper provides a review and perspective on intermediate and advanced reinforcement learning (RL) techniques in process industries.
- p.1 abstract: It offers a holistic approach by covering all levels of the process control hierarchy.
- p.1 abstract: The survey paper presents a comprehensive overview of RL algorithms, including fundamental concepts like Markov decision processes and different approaches to RL, such as value-based, policy-based, and actor-critic methods, while also discussing the relationship between classical control and RL.
- p.1 abstract: The survey paper discusses the limitations and advantages, trends and new applications, and opportunities and future prospects for RL in process industries.
- p.1 introduction: REINFORCEMENT learning (RL) has emerged as an effective tool for solving complex decision-making problems in a wide range of fields.
- p.1 introduction: Despite these advancements outside process industries, most of the RL methodologies use a combination of learning and process control techniques extensively studied in the optimization and control of process industries [2].
- p.2 introduction: However, there is still a lack of a comprehensive review of the state-of-the-art theory, outstanding challenges in the unified control hierarchy, and possible improvements for practical solutions beyond toy problems and small-scale implementations.
- p.2 introduction: As a result, the main contributions of this manuscript are to show the developments in deep learning, process control, and RL, introduce advanced RL techniques, present an overview of the recent progress in RL in process industries, and discuss the future prospects in a compact manner.
- p.2 introduction: The manuscript is organized as follows. Section II progressively introduces the motivation behind RL in process industries, Section III mathematically explores the RL theory, Section IV reviews the recent literature with a focus on soft sensor design, process control, fault detection and diagnosis, fault tolerant control, optimization, planning, scheduling, and supply chain management. Then, Section V discusses the outstanding problems and possible extensions that researchers and professionals of process industries can consider.
- p.3 method: Process control is a highly interdisciplinary field that has been evolving from the earliest forms of proportional-integral-derivative (PID) controllers to the more sophisticated optimal control schemes.
- p.12 discussion: Besides these developments in process industries, the RL literature is evolving rapidly in various fields.
- p.13 discussion: However, this approach fails to consider the interconnectedness of multiple levels in most process industries, which can significantly impact the overall performance of the control system.
- p.13 discussion: Overall, applying RL in complex process industries can lead to more efficient, reliable, and sustainable processes with improved performance and reduced operational costs.
