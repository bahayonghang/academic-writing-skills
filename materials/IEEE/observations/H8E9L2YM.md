---
key: H8E9L2YM
title: "Interactive Integrated Design Framework for Optimizing the Structure, Capacity, and Operation of Multienergy Systems via Reinforcement Learning"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3556037"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM DESCRIPTION` → `III. INTERACTIVE INTEGRATED DESIGN FRAMEWORK` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCLATURE`。无独立 Related Work。`related_work=inlined`（Introduction 下 `A. Background and Motivation` / `B. Literature Review` / `C. Contribution and Paper Organization`）。Introduction 末有节序路标，指向 Section II–V。Method 标题为 `INTERACTIVE INTEGRATED DESIGN FRAMEWORK`。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `The complex and` — "The complex and varied source–load characteristics of multienergy systems (MESs) make it difficult to match supply with demand while maintaining economic efficiency." (p.5900)
- introduction: `ENHANCING energy efficiency` — "ENHANCING energy efficiency and the market share of renewable energy sources are considered effective means of achieving carbon neutrality [1]." (p.5901；栏首掉字)
- method: `To solve the` — "To solve the MES integrated design problem described in (25), a bilevel interactive integrated design framework is proposed based on RL." (p.5904)
- experiments: `The effectiveness of` — "The effectiveness of the proposed framework was evaluated by using typical data for the renewable power generation and building loads from a northern Chinese city to develop three scenarios: school (case 1), residential area (case 2), and industrial park (case 3)." (p.5906, IV.A)
- conclusion: `This study proposed` — "This study proposed a RL–based bilevel interactive integrated design framework (i.e., IIDF) for the structure, capacity and operation of MESs." (p.5909)

## Gap transitions

- to address (abstract): "To address this issue, a bilevel interactive integrated design framework (IIDF) is proposed for MESs." (p.5900)
- however (introduction): "However, the MES involves a wide variety of devices types and flexible structural configurations, especially in the context of the complex and diverse energy supply–demand characteristics." (p.5901)
- unfortunately (introduction): "Unfortunately, the structure is flexible and changeable as well as deeply coupled with the capacity configuration and operational scheme, which increases the scale and complexity of an integrated design approach undoubtedly." (p.5902)
- to address (introduction): "To address the above technical challenges, this study provides a new and efficient solution for structure–capacity–operation integrated design of MES." (p.5902)

## Hedge verbs

- propose / causal / abstract, method: "a bilevel interactive integrated design framework (IIDF) is proposed for MESs"; "a bilevel interactive integrated design framework is proposed based on RL"
- demonstrate / causal / abstract, conclusion: "the results demonstrated its effectiveness and superiority"; "The case study has demonstrated that IIDF can make full use of prior knowledge"
- show / causal / experiments: "Table III presents the MES designs of the three methods in cases 1–3."
- may / speculative / experiments: "The increase in natural gas procurement costs may emerge as a critical factor negatively impacting the economic efficiency of the MES"

## Cross-section linkers

- introduction → problem: "The rest of this article is organized as follows. Section II describes the universal MES integrated design problem. Section III introduces the proposed framework. Section IV presents case studies. Finally, Section V concludes this article." (p.5902)
- method → experiments: 容量–运行协同优化段落后 `IV. CASE STUDY` (p.5906)
- experiments → conclusion: 敏感性分析段落后直接 `V. CONCLUSION` (p.5909)

## Candidate rules

- R001 摘要缺口后用 `To address this issue, a ... is proposed`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，文献评述写在 `I.B Literature Review`。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `the main contributions and innovations of this work are as follows` + 编号列表。
- R005 结论用 `Future research aims to` 指向后续。

## Candidate phrases

- `To address this issue, a bilevel interactive integrated design framework (IIDF) is proposed` (abstract)
- `To address the above technical challenges, this study provides` (introduction)
- `the main contributions and innovations of this work are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This study proposed a RL–based bilevel interactive integrated design framework` (conclusion)
- `Future research aims to enhance` (conclusion)

## House style

自称是 `this study` / `this work` / `is proposed` / `we are among the first`。未见 `Here we`、`In this paper`。`this study proposed` 与 `this work` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.5900 abstract: The complex and varied source–load characteristics of multienergy systems (MESs) make it difficult to match supply with demand while maintaining economic efficiency.
- p.5900 abstract: To address this issue, a bilevel interactive integrated design framework (IIDF) is proposed for MESs.
- p.5900 abstract: The performance of IIDF was evaluated against two traditional design methods in three typical scenarios, and the results demonstrated its effectiveness and superiority.
- p.5901 introduction: ENHANCING energy efficiency and the market share of renewable energy sources are considered effective means of achieving carbon neutrality [1].
- p.5901 introduction: However, the MES involves a wide variety of devices types and flexible structural configurations, especially in the context of the complex and diverse energy supply–demand characteristics.
- p.5902 introduction: Unfortunately, the structure is flexible and changeable as well as deeply coupled with the capacity configuration and operational scheme, which increases the scale and complexity of an integrated design approach undoubtedly.
- p.5902 introduction: To address the above technical challenges, this study provides a new and efficient solution for structure–capacity–operation integrated design of MES.
- p.5902 introduction: To the best of the authors knowledge, we are among the first to apply RL [22] to design MES.
- p.5902 introduction: Specifically, the main contributions and innovations of this work are as follows.
- p.5902 introduction: The rest of this article is organized as follows. Section II describes the universal MES integrated design problem. Section III introduces the proposed framework. Section IV presents case studies. Finally, Section V concludes this article.
- p.5904 method: To solve the MES integrated design problem described in (25), a bilevel interactive integrated design framework is proposed based on RL.
- p.5906 experiments: The effectiveness of the proposed framework was evaluated by using typical data for the renewable power generation and building loads from a northern Chinese city to develop three scenarios: school (case 1), residential area (case 2), and industrial park (case 3).
- p.5907 experiments: Table III presents the MES designs of the three methods in cases 1–3.
- p.5907 experiments: IIDF had the lowest JMES in all cases, but the differences in cost between the three methods differed according to the case.
- p.5909 conclusion: This study proposed a RL–based bilevel interactive integrated design framework (i.e., IIDF) for the structure, capacity and operation of MESs.
- p.5909 conclusion: The case study has demonstrated that IIDF can make full use of prior knowledge, such as multienergy flow supply and demand balance, and realize the optimal design of MES under different energy demand scenarios.
- p.5909 conclusion: Future research aims to enhance the adaptability of IIDF to different regional scales, especially the design of regional MES.
