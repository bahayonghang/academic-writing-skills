---
key: IZB5FKGE
title: "Reconstructing causal networks from data for the analysis, prediction, and optimization of complex industrial processes"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2024.109494"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Literature review` → `3. Methodology` → `4. Experimental results and analysis` → `5. Conclusions`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。独立 Related Work（标题为 `Literature review`）。Introduction 末有编号贡献与节序路标。Method 分因果网络重建与可解释预测/PSO 优化。Experiments 用注塑过程 16600 样本，含可观性/可控性分析。

## Openers

- abstract: `Lacking the understanding` — "Lacking the understanding of the first principles leads to the apparent black box attributes of complex industrial processes."
- introduction: `With the development` — "With the development of society and the progress of technology, modern industrial production has become increasingly complex, and market competition has become increasingly fierce, which puts higher requirements for the digitization and informatization of industrial processes (Gao et al., 2020)."
- related_work: `This section reviews` — "This section reviews the works related to the topic of this paper, and some critical discussions are also given."
- method: `As shown in` — "As shown in Fig. 2, the proposed method is divided into four parts."
- experiments: `As a typical` — "As a typical complex industrial process, the IM process can be seen as a multi-stage and multi-variable black box."
- conclusion: `This study addresses` — "This study addresses the challenge of double black boxes in complex industrial decision-making, proposing a research framework of \"causal analysis → performance prediction → process optimization\"."

## Gap transitions

- however (abstract): "However, the existing data-driven models are also black boxes, focusing only on the correlation relationships between data without reflecting causal relationships."
- therefore (abstract): "Therefore, this study addresses the challenge of double black boxes in complex industrial decision-making, proposing a research framework of \"causal analysis → performance prediction → process optimization\"."
- nevertheless (introduction): "Nevertheless, these methods are usually end-to-end and cannot explain the internal operating mechanisms (Sun et al., 2023b)."
- thus (introduction): "Thus, they are also like black boxes, based on which it is difficult to understand complex industrial processes that are also black boxes."
- as shown (introduction): "As shown in Fig. 1, this study proposes a research framework of \"causal analysis → performance prediction → process optimization\", which can support the analysis, prediction, and optimization of complex industrial processes"

## Hedge verbs

- address / causal / abstract, conclusion: "this study addresses the challenge of double black boxes"
- propose / causal / introduction: "this study proposes a research framework"
- show / associative / abstract: "The research results show that by reconstructing the causal relations network from data, the proposed framework can support the analysis, prediction, and optimization of complex industrial processes"
- can / associative / conclusion: "The causal relationship reconstruction method proposed in this paper can effectively reveal the operating mechanism of complex industrial processes."

## Cross-section linkers

- introduction → related_work: "The rest of this paper is organized as follows. Section 2 introduces the works related to this paper, Section 3 gives the data analytics method for complex industrial processes by reconstructing a causal relations network from data, and Section 4 describes the method of prediction and optimization by integrating causal relations."
- related_work → method: 文献评述后 `3. Methodology`
- method → experiments: PSO 步骤后 `4. Experimental results and analysis`
- experiments → conclusion: 闭环洞察段落后 `5. Conclusions`

## Candidate rules

- R001 独立 Related Work，标题为 `Literature review`。
- R003 节序路标：`The rest of this paper is organized as follows`
- R004 编号贡献。
- R009 自称：`this study addresses` / `this study proposes` / `proposed in this paper`

## Candidate phrases

- `Therefore, this study addresses the challenge of` (abstract)
- `this study proposes a research framework of` (introduction)
- `The rest of this paper is organized as follows` (introduction)
- `The causal relationship reconstruction method proposed in this paper` (conclusion)

## House style

自称 `this study addresses` / `this study proposes` / `this paper` / `the proposed framework`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Lacking the understanding of the first principles leads to the apparent black box attributes of complex industrial processes.
- abstract: However, the existing data-driven models are also black boxes, focusing only on the correlation relationships between data without reflecting causal relationships.
- abstract: Therefore, this study addresses the challenge of double black boxes in complex industrial decision-making, proposing a research framework of "causal analysis → performance prediction → process optimization".
- abstract: The research results show that by reconstructing the causal relations network from data, the proposed framework can support the analysis, prediction, and optimization of complex industrial processes, achieving the decision-making goals of safety, robustness, improving quality and efficiency.
- introduction: With the development of society and the progress of technology, modern industrial production has become increasingly complex, and market competition has become increasingly fierce, which puts higher requirements for the digitization and informatization of industrial processes (Gao et al., 2020).
- introduction: Nevertheless, these methods are usually end-to-end and cannot explain the internal operating mechanisms (Sun et al., 2023b).
- introduction: As shown in Fig. 1, this study proposes a research framework of "causal analysis → performance prediction → process optimization", which can support the analysis, prediction, and optimization of complex industrial processes, achieving the decision-making goals of safety, robustness, improving quality and efficiency by reconstructing the causal relations network from data.
- introduction: The rest of this paper is organized as follows. Section 2 introduces the works related to this paper, Section 3 gives the data analytics method for complex industrial processes by reconstructing a causal relations network from data, and Section 4 describes the method of prediction and optimization by integrating causal relations.
- related_work: This section reviews the works related to the topic of this paper, and some critical discussions are also given.
- method: As shown in Fig. 2, the proposed method is divided into four parts.
- experiments: As a typical complex industrial process, the IM process can be seen as a multi-stage and multi-variable black box.
- conclusion: This study addresses the challenge of double black boxes in complex industrial decision-making, proposing a research framework of "causal analysis → performance prediction → process optimization".
- conclusion: The causal relationship reconstruction method proposed in this paper can effectively reveal the operating mechanism of complex industrial processes.
