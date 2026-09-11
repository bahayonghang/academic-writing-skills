---
key: CG7BWB7H
title: "Local machine learning model-based multi-objective optimization for managing system interdependencies in production: A case study from the ironmaking industry"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2024.108099"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-18"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work` → `3. Technical background and problem definition` → `4. Methodology` → `5. Results` → `6. Discussion and outlook` → `7. Conclusions`。前置 `ABSTRACT`、`ARTICLE INFO` / `Keywords`，文首标 `Research paper`。有独立 Related Work。`related_work=independent`。Introduction 末有三项研究问题 + 节序路标（用 prose 指 related work / methodology / results，不用 `Section n`）。Method 标题为 `Methodology`。Experiments 标题为 `Results`，其后另有 `Discussion and outlook`。

## Openers

- abstract: `Modeling interdependencies in` — "Modeling interdependencies in a production process is a vital aspect of process engineering."
- introduction: `Identifying and understanding` — "Identifying and understanding the interdependencies between different aspects of a production process is essential for a comprehensive understanding of the process, making informed decisions, and enhancing process performance, making it a fundamental aspect of effective process engineering"
- related_work: `As a result of` — "As a result of automation requirements in industrial processes and the overall goal to achieve a higher level of operation efficiency and productivity, the manufacturing sector is increasing digitalization efforts (Lu, 2017)."
- method: `In order to tackle` — "In order to tackle the challenges associated with transparent data-driven modeling of process interdependencies within sinter production, a methodology has been proposed."
- experiments: `Following the data pre-processing` — "Following the data pre-processing procedure described in Section 4.1, after the initial data cleaning step, time periods of plant shutdowns were filtered with an added two-hour threshold before and after shutdown occurred."
- conclusion: `This paper proposes` — "This paper proposes an approach for discovering, understanding, and modeling interdependencies in a complex industrial production process."

## Gap transitions

- however (abstract): "However, due to various assumptions and parameter approximation, such approach sometimes struggles to accurately model process dynamics."
- however (introduction): "However, acceptance of these models is often low due to: black-box characteristics of most ML methods"
- however (introduction): "However, these methods rely on simulation or deterministic, first-principle models that are unavailable in cases of complex production processes such as in ironmaking."
- it still remains unclear (introduction): "it still remains unclear how to model overall process behavior and investigate process interdependencies of complex production processes which cannot be represented through first-principle models."
- this paper seeks (introduction): "This paper seeks to address the aforementioned challenges in complex industrial processes."

## Hedge verbs

- is introduced / causal / abstract: "a data-driven approach based on production data is introduced"
- is demonstrated / causal / abstract: "The applicability of the proposed approach is demonstrated through a case study in the ironmaking industry"
- shows potential / associative / abstract: "Such approach shows potential for applications in a broader context"
- seeks to address / causal / introduction: "This paper seeks to address the aforementioned challenges"
- proposes / causal / conclusion: "This paper proposes an approach for discovering, understanding, and modeling interdependencies"

## Cross-section linkers

- introduction → related work: "This paper is divided into seven sections. The related work section gives an insight into the scope of the application of ML models and provides a comparison of domain-driven and data-driven approaches. The following section introduces the sinter production use-case and provides the technical background. The methodology section details the approach. The results section collects and discusses the results of the proposed approach, with final remarks in the conclusion section."
- related work → method: Related Work 末指出现有烧结 ML 未处理相互依赖后接 `3. Technical background`，再接 `4. Methodology`
- method → experiments: 优化算法段落后 `5. Results`
- experiments → conclusion: `6. Discussion and outlook` 后 `7. Conclusions`

## Candidate rules

- R001 独立 Related Work，标题为 `Related work`。
- R003 节序路标用 prose（`The related work section` / `The methodology section`），不用 `Section n`。
- R004 Introduction 用编号研究问题而非贡献列表：`(1) how to model... (2) how to employ... (3) how to orchestrate...`
- R009 自称：`In this paper, a data-driven approach ... is introduced` / `This paper proposes`

## Candidate phrases

- `In this paper, a data-driven approach based on production data is introduced to address the challenge` (abstract)
- `This paper seeks to address the aforementioned challenges` (introduction)
- `This paper is divided into seven sections.` (introduction)
- `In order to tackle the challenges associated with` (method)
- `This paper proposes an approach for discovering, understanding, and modeling interdependencies` (conclusion)

## House style

自称 `In this paper` / `This paper seeks` / `This paper proposes` / `a methodology has been proposed`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Modeling interdependencies in a production process is a vital aspect of process engineering.
- abstract: However, due to various assumptions and parameter approximation, such approach sometimes struggles to accurately model process dynamics.
- abstract: In this paper, a data-driven approach based on production data is introduced to address the challenge of discovering, understanding, and modeling interdependencies in a production process by constructing a constrained multi-objective optimization problem.
- abstract: The applicability of the proposed approach is demonstrated through a case study in the ironmaking industry, whereby a set of Machine Learning and causality-based methods is provided while highlighting the significance of transparency and use of domain knowledge in the development of data-driven models.
- introduction: Identifying and understanding the interdependencies between different aspects of a production process is essential for a comprehensive understanding of the process, making informed decisions, and enhancing process performance, making it a fundamental aspect of effective process engineering
- introduction: This paper seeks to address the aforementioned challenges in complex industrial processes.
- introduction: This paper is divided into seven sections. The related work section gives an insight into the scope of the application of ML models and provides a comparison of domain-driven and data-driven approaches.
- related work: As a result of automation requirements in industrial processes and the overall goal to achieve a higher level of operation efficiency and productivity, the manufacturing sector is increasing digitalization efforts (Lu, 2017).
- method: In order to tackle the challenges associated with transparent data-driven modeling of process interdependencies within sinter production, a methodology has been proposed.
- experiments: Following the data pre-processing procedure described in Section 4.1, after the initial data cleaning step, time periods of plant shutdowns were filtered with an added two-hour threshold before and after shutdown occurred.
- experiments: In a 24-h operation cycle, the introduction of a newly discovered process parameter combination would potentially result in, compared to the current operation, an increase of production output by 9.8%–19.6%.
- conclusion: This paper proposes an approach for discovering, understanding, and modeling interdependencies in a complex industrial production process.
- conclusion: Specifically, solutions from the optimization process propose a potential increase of production output by 9.8%–19.6% at a stable coke consumption (around 6 t/h).
