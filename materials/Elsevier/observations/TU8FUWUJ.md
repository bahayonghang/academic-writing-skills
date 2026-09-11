---
key: TU8FUWUJ
title: "Data/mechanism hybrid-driven modeling of blast furnace smelting system and global sequential optimization"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2024.103235"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-4,8-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Mechanism modeling for blast furnace smelting systems` → `3. Data-driven modeling for blast furnace smelting systems` → `4` 全局顺序优化（`4.2. Global sequential optimization design` / `4.3. Overall modeling and optimization framework`）→ `5. Case study` → `6. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 CVA-SIM、GRU-RNN、IKOPLS、I-N-SIM、OS-RVFLN 与烧结优化）。Introduction 末用 Table 1 对齐挑战与贡献。Method 拆成机理模型、BLASIM 与顺序优化。Experiments 标题为 `Case study`。

## Openers

- abstract: `Within the crucial` — "Within the crucial domain of blast furnace ironmaking and sintering, the quality of sinter ore and molten iron holds supreme importance, with direct implications for downstream processes."
- introduction: `As the backbone` — "As the backbone of national economy, iron and steel industry has significantly contributed to global production."
- method: `The production of` — "The production of molten iron significantly affects the economic efficiency of blast furnace operations." (s.2)
- experiments: `In order to` — "In order to substantiate the efficacy of our proposed method, this section unveils the modeling performance and optimization results of blast furnace ironmaking and sintering processes."
- conclusion: `A hybrid-driven modeling` — "A hybrid-driven modeling and global optimization method is proposed to address the intricacies of blast furnace smelting system modeling and global optimization strategies."

## Gap transitions

- however (abstract): "However, the complexities of utilizing operational experience, understanding mechanisms, leveraging extensive data for precise modeling, and optimizing multiple objectives have persistently posed challenges for engineers."
- however (introduction): "However, for the blast furnace ironmaking process, besides iron quality, iron production, and blast furnace energy consumption also draw the attention of field operators."
- in response (introduction): "In response to the challenges mentioned above, this paper presents a hybrid strategy that combines data-driven and mechanism approaches for modeling and global optimization of complex blast furnace smelting systems."
- therefore (introduction): "Therefore, it is crucial to consider the interconnected processes of sintering and blast furnace from a holistic system perspective"

## Hedge verbs

- propose / causal / abstract, method, conclusion: "we propose an novel data/mechanism hybrid-driven modeling and global sequential optimization framework"; "Here, we propose an optimal nonlinear BLASIM"; "A hybrid-driven modeling and global optimization method is proposed"
- present / causal / introduction: "this paper presents a hybrid strategy"
- suggest / associative / conclusion: "The findings suggest that the proposed BLASIM algorithm holds a significant edge in modeling accuracy"

## Cross-section linkers

- introduction → method: Table 1 贡献后 `2. Mechanism modeling for blast furnace smelting systems`
- mechanism → data-driven: 焦比机理后 `3. Data-driven modeling for blast furnace smelting systems`
- method → experiments: Algorithm 1–2 后 `5. Case study`
- experiments → conclusion: 全局优化结果后 `6. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R004 贡献用 Table 1 与项目符号：`our proposed methodology contributes to the following three main aspects`
- R009 自称：`we propose` / `this paper presents` / `A ... method is proposed`

## Candidate phrases

- `In this research, we propose` (abstract)
- `In response to the challenges mentioned above, this paper presents` (introduction)
- `In summary, our proposed methodology contributes to` (introduction)
- `In order to substantiate the efficacy of our proposed method` (experiments)
- `A hybrid-driven modeling and global optimization method is proposed to address` (conclusion)

## House style

自称 `we propose` / `this paper presents` / `our proposed method` / `our proposed methodology`。第一人称复数常见。进 phrase_bank，不进 anti_ai_patterns。摘要有 `an novel`（冠词未校）。

## Quotes

- abstract: Within the crucial domain of blast furnace ironmaking and sintering, the quality of sinter ore and molten iron holds supreme importance, with direct implications for downstream processes.
- abstract: In this research, we propose an novel data/mechanism hybrid-driven modeling and global sequential optimization framework, with three core contributions
- abstract: To conclude, the proposed methods are thoroughly validated using real-world blast furnace smelting data, affirming the feasibility and efficiency of modeling accuracy and optimization performance.
- introduction: As the backbone of national economy, iron and steel industry has significantly contributed to global production.
- introduction: However, for the blast furnace ironmaking process, besides iron quality, iron production, and blast furnace energy consumption also draw the attention of field operators.
- introduction: In response to the challenges mentioned above, this paper presents a hybrid strategy that combines data-driven and mechanism approaches for modeling and global optimization of complex blast furnace smelting systems.
- introduction: In summary, our proposed methodology contributes to the following three main aspects, with the corresponding challenges detailed in Table 1.
- method: The production of molten iron significantly affects the economic efficiency of blast furnace operations.
- method: Here, we propose an optimal nonlinear BLASIM.
- experiments: In order to substantiate the efficacy of our proposed method, this section unveils the modeling performance and optimization results of blast furnace ironmaking and sintering processes.
- conclusion: A hybrid-driven modeling and global optimization method is proposed to address the intricacies of blast furnace smelting system modeling and global optimization strategies.
- conclusion: The findings suggest that the proposed BLASIM algorithm holds a significant edge in modeling accuracy, and the mechanism model used also meets the usage conditions.
