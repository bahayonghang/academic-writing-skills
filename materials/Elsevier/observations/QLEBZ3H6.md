---
key: QLEBZ3H6
title: "Multi-objective collaborative optimization in cement calcination process: A time domain rolling optimization method based on Jaya algorithm"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2021.07.012"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Multi-objective collaborative optimization problem description of cement calcination process` → `3. Time domain rolling multi-objective Jaya algorithm` → `4. Testing of the proposed optimization method` → `5. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段评机理模型、软测量与多目标优化）。Introduction 末有编号贡献，无节序路标。Method 拆成问题描述与算法节。Experiments 标题为 `Testing of the proposed optimization method`。

## Openers

- abstract: `Coal consumption and` — "Coal consumption and free calcium oxide (f-CaO) content are two important production indicators in the cement calcination process, and its collaborative optimization is of great significance to improve the production performance."
- introduction: `Research shows that` — "Research shows that China is the largest cement production country in the world, and accounts for more than 60% of the total global cement production [1]."
- method: `Since the cement` — "Since the cement calcination process is a complex production process with continuous change of working conditions, if static single-step solution is used for its optimization, it is not conducive to the dynamic tracking of production indicators on the change of working conditions." (s.3)
- experiments: `In order to` — "In order to verify the effectiveness of the proposed optimization method, this paper uses the actual cement industry production data, from the perspective of multi-objective collaborative optimization of cement calcination process."
- conclusion: `This paper proposes` — "This paper proposes a multi-objective collaborative optimization method for cement calcination process."

## Gap transitions

- however (abstract): "However, due to the multiple dynamic interferences and multiple conflicts between coal consumption and f-CaO, product quality is unstable and coal consumption becomes high."
- to address (abstract): "To address the problems, this paper proposes a multi-objective collaborative optimization method for cement calcination process."
- therefore (introduction): "Therefore, there is great potential for the cement industry to achieve energy saving, emission reduction and sustainable development."
- therefore (introduction): "Therefore, these optimization methods based on mechanism model are not suitable for the cement industry with unstable production conditions."
- therefore (introduction): "Therefore, this paper uses a data-driven method to model the cement calcination process, and proposes a multi-objective collaborative optimization method for cement calcination process."
- therefore (conclusion): "Therefore, taking into account the actual production demand, we should not blindly reduce coal consumption as the ultimate purpose, but should comprehensively consider the fluctuation of f-CaO content."

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "this paper proposes"; "we propose a time domain rolling multi-objective Jaya algorithm"
- demonstrate / causal / abstract: "The test comparison with several common intelligent optimization algorithms demonstrates the advantages of using TDRM-Jaya."
- validate / causal / abstract: "practical industrial data validates the effectiveness of the proposed optimization method"
- show / associative / experiments: "The test results show that when k = h = 30, the coal consumption reduction the most"
- can / speculative / introduction: "it is not only to forecast production indicators, but also to study optimization methods based on data-driven model"

## Cross-section linkers

- introduction → method: 编号贡献后直接 `2. Multi-objective collaborative optimization problem description of cement calcination process`
- method → experiments: 时域滚动策略后 `4. Testing of the proposed optimization method`
- experiments → conclusion: Test III 结论后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R004 编号贡献：`The main contributions of this study can be summarized as follows`
- R009 自称：`this paper proposes` / `we propose`
- R011 Testing 节承担 Experiments。

## Candidate phrases

- `To address the problems, this paper proposes` (abstract)
- `Therefore, this paper uses a data-driven method ... and proposes` (introduction)
- `The main contributions of this study can be summarized as follows` (introduction)
- `In order to verify the effectiveness of the proposed optimization method` (experiments)
- `This paper proposes` (conclusion)

## House style

自称 `this paper proposes` / `we propose` / `the proposed optimization method`。未见 `Here we`。`this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Coal consumption and free calcium oxide (f-CaO) content are two important production indicators in the cement calcination process, and its collaborative optimization is of great significance to improve the production performance.
- abstract: To address the problems, this paper proposes a multi-objective collaborative optimization method for cement calcination process.
- abstract: Besides, practical industrial data validates the effectiveness of the proposed optimization method.
- introduction: Research shows that China is the largest cement production country in the world, and accounts for more than 60% of the total global cement production [1].
- introduction: Therefore, this paper uses a data-driven method to model the cement calcination process, and proposes a multi-objective collaborative optimization method for cement calcination process.
- introduction: The main contributions of this study can be summarized as follows:
- method: Therefore, this paper proposes a time domain rolling multi-objective Jaya [37–41] algorithm to optimize the model.
- experiments: In order to verify the effectiveness of the proposed optimization method, this paper uses the actual cement industry production data, from the perspective of multi-objective collaborative optimization of cement calcination process.
- conclusion: This paper proposes a multi-objective collaborative optimization method for cement calcination process.
- conclusion: Therefore, taking into account the actual production demand, we should not blindly reduce coal consumption as the ultimate purpose, but should comprehensively consider the fluctuation of f-CaO content.
