---
key: Q3QQFWH9
title: "Semi-supervised soft sensor method for fermentation processes based on physical monotonicity and variational autoencoders"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2024.109065"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminary knowledge` → `3. PMVAER` → `4. Results and discussion` → `5. Conclusion`。前置 `ABSTRACT`、`ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段机理模型、数据驱动模型、物理约束与混合建模）。Introduction 末有编号贡献 + 节序路标。Method 拆成预备知识与 PMVAER。Experiments 标题为 `Results and discussion`。

## Openers

- abstract: `Data-driven models have` — "Data-driven models have shown broad application prospects in soft sensor modeling."
- introduction: `The advancements in` — "The advancements in measurement technology, the intensified initiatives toward factory digitization, and the emergence of multiple data collection methods have resulted in the accumulation of considerable actionable data from industrial processes."
- method: `Numerous endeavors have` — "Numerous endeavors have been undertaken to apply VAEs to regression tasks." (s.3)
- experiments: `The proposed PMVAER model` — "The proposed PMVAER model is implemented for simulation and real cases of penicillin production in this section."
- conclusion: `In this study` — "In this study, the proposed PMVAER model is utilized for penicillin fermentation soft sensors."

## Gap transitions

- however (abstract): "However, numerous challenges persist."
- to tackle (abstract): "To tackle these challenges, a semi-supervised soft sensor method (PMVAER) for fermentation processes based on physical monotonicity and variational autoencoders (VAEs) is introduced."
- however (introduction): "However, online measurement of certain crucial variables remains challenging because of issues such as measurement delays, lack of automatic detection instruments, high cost of online sensors, or technical difficulties"
- although (introduction): "Although mixture modeling has found extensive applications in various domains (Bekele, 2021; Wang et al., 2021; Wu and Qiao, 2021), limited research has been conducted on soft measurements of fermentation processes."
- to solve (introduction): "To solve this problem, this paper proposes a semi-supervised soft sensor method (PMVAER) for fermentation processes based on physical monotonicity and variational autoencoders (VAEs)."

## Hedge verbs

- is introduced / causal / abstract: "a semi-supervised soft sensor method (PMVAER) ... is introduced"
- propose / causal / introduction: "this paper proposes a semi-supervised soft sensor method"
- verify / causal / abstract: "Comparisons with five other methods verify that the proposed method exhibits exceptional predictive accuracy"
- illustrate / associative / conclusion: "Two experiments illustrate that the PMVAER model surpasses state-of-the-art existing approaches."
- is better suited / associative / conclusion: "PMVAER is better suited for datasets with limited data volume and significant data fluctuations"

## Cross-section linkers

- introduction → method: "The subsequent sections are arranged as follows. Section 2 provides a concise introduction to VAEs. Section 3 elaborates on the proposed PMVAER model, elucidating its core components and principles. Section 4 illustrates a penicillin simulation alongside a practical penicillin case for experimental investigation, showcasing the experimental research outcomes. Section 5 summarizes the findings and offers a forward-looking perspective on potential future developments in this field."
- method → experiments: 训练步骤与评价指标后 `4. Results and discussion`
- experiments → conclusion: 真实案例鲁棒性段落后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The subsequent sections are arranged as follows`
- R004 编号贡献：`The primary contributions of this work include the following.`
- R009 自称：`this paper proposes` / `this paper introduces`

## Candidate phrases

- `To tackle these challenges, a semi-supervised soft sensor method (PMVAER) ... is introduced` (abstract)
- `To solve this problem, this paper proposes` (introduction)
- `The primary contributions of this work include the following.` (introduction)
- `The subsequent sections are arranged as follows.` (introduction)
- `In this study, the proposed PMVAER model is utilized for` (conclusion)

## House style

自称 `this paper proposes` / `this paper introduces` / `In this study` / `the proposed method`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Data-driven models have shown broad application prospects in soft sensor modeling.
- abstract: However, numerous challenges persist.
- abstract: To tackle these challenges, a semi-supervised soft sensor method (PMVAER) for fermentation processes based on physical monotonicity and variational autoencoders (VAEs) is introduced.
- abstract: Comparisons with five other methods verify that the proposed method exhibits exceptional predictive accuracy along with enhanced generalization ability.
- introduction: The advancements in measurement technology, the intensified initiatives toward factory digitization, and the emergence of multiple data collection methods have resulted in the accumulation of considerable actionable data from industrial processes.
- introduction: Although mixture modeling has found extensive applications in various domains (Bekele, 2021; Wang et al., 2021; Wu and Qiao, 2021), limited research has been conducted on soft measurements of fermentation processes.
- introduction: To solve this problem, this paper proposes a semi-supervised soft sensor method (PMVAER) for fermentation processes based on physical monotonicity and variational autoencoders (VAEs).
- introduction: The primary contributions of this work include the following.
- introduction: The subsequent sections are arranged as follows. Section 2 provides a concise introduction to VAEs.
- method: Numerous endeavors have been undertaken to apply VAEs to regression tasks.
- experiments: The proposed PMVAER model is implemented for simulation and real cases of penicillin production in this section.
- conclusion: In this study, the proposed PMVAER model is utilized for penicillin fermentation soft sensors.
- conclusion: Two experiments illustrate that the PMVAER model surpasses state-of-the-art existing approaches.
- conclusion: Furthermore, the comparison between the simulation and real cases of penicillin production reveals that PMVAER is better suited for datasets with limited data volume and significant data fluctuations, highlighting its superior robustness.
