---
key: 9SSFYDTY
title: "Research on an advanced intelligence implementation system for engineering process in industrial field under big data"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2020.113751"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Literature review` → `3. Study of proposed CBR system` → `4. Experiments and discussion` → `5. Conclusion`。前置 `abstract` 与 `article info` / `Keywords`。独立 Related Work：`2. Literature review`（2.1 并行处理、2.2 CBR 与 AI 集成、2.3 BN 学习）。Introduction 末无编号贡献列表，缺口在段内提出后直接给出 IE / DECMBD。Experiments 标题为 `4. Experiments and discussion`（基准集 + 冲压模具 / 注塑模具案例）。

## Openers

- abstract: `To develop an` — "To develop an advanced CBR system to well adapt to the intelligence implementation of new engineering process in the big data environment, Bayesian network (BN) model is introduced to CBR system for knowledge reasoning."
- introduction: `CBR represents knowledge` — "CBR represents knowledge and reuses it in the form of “a case”, which consists of fragments of knowledge instead of abstract rules or complex models of other Artificial Intelligence (AI) methods."
- related_work: `Aiming at lessening` — "Aiming at lessening time costing of learning BN structure process, Hu et al. (2016) propose an approach by combining MapReduce with Max-Min-Hill-Climbing (MMHC) method." (s.2.1)
- method: `Case of CBR` — "Case of CBR system is represented by a set of features including problem features and solution features, which are extracted from lots of crude data of practical cases through feature selection."
- experiments: `The total structure` — "The total structure of system implementation for the experiments is composed of two parts, namely hardware components and soft components."
- conclusion: `In order to` — "In order to construct an advanced CBR system to provide technique support for realizing the intelligence of engineering process in industrial field under big data, this paper develops IE algorithm and DECMBD algorithm to improve knowledge reasoning of CBR system."

## Gap transitions

- however (abstract, introduction): "However, as engineering application is becoming more and more complicated, the number of parameters used to define engineering application grows larger and larger, leading to the seriously reduced efficiency as well as the accuracy of the integrated model."
- aiming at (introduction): "Aiming at this problem, In-External (IE) algorithm is proposed by this paper to assign computation task."
- as a result (introduction): "As a result, by enhancing the efficiency of knowledge reasoning with IE algorithm and the precision with DECMBD algorithm in cases of large number of parameters, this paper tries to construct an advanced CBR system"

## Hedge verbs

- proposes / causal / abstract: "this paper proposes In-External (IE) algorithm"; "this paper proposes Discount Exponential Coefficients of Multivariate Beta Distribution (DECMBD) algorithm"
- tries to construct / hedging / introduction: "this paper tries to construct an advanced CBR system"
- shows / associative / experiments: "Table 2 shows that IE algorithm significantly enhances the efficiency of system working"
- prove / causal / experiments: "the experiments of this case also prove that the proposed IE algorithm can more appropriately assign the computation task of big data"

## Cross-section linkers

- introduction → related_work: Introduction 末段后直接 `2. Literature review`
- related_work → method: 文献综述收束句后 `3. Study of proposed CBR system`
- method → experiments: "4. Experiments and discussion"
- experiments → conclusion: 局限段落后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Literature review`。
- R009 自称：`this paper proposes` / `this paper develops` / `this paper tries to construct`

## Candidate phrases

- `this paper proposes In-External (IE) algorithm` (abstract)
- `this paper proposes Discount Exponential Coefficients of Multivariate Beta Distribution (DECMBD) algorithm` (abstract)
- `Aiming at this problem, In-External (IE) algorithm is proposed by this paper` (introduction)
- `In order to construct an advanced CBR system ... this paper develops` (conclusion)

## House style

自称 `this paper proposes` / `is proposed by this paper` / `this paper develops` / `this paper tries to construct`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: To develop an advanced CBR system to well adapt to the intelligence implementation of new engineering process in the big data environment, Bayesian network (BN) model is introduced to CBR system for knowledge reasoning.
- abstract: For the problem of reduced efficiency, this paper proposes In-External (IE) algorithm to perform the assignment of big data distribution for parallel data processing, which can fully utilize the capacity of Hadoop system and attain the best efficiency of knowledge reasoning.
- abstract: Finally, lots of experiments are performed to validate the effectiveness of the proposed advanced CBR system.
- introduction: CBR represents knowledge and reuses it in the form of “a case”, which consists of fragments of knowledge instead of abstract rules or complex models of other Artificial Intelligence (AI) methods.
- introduction: However, as engineering application is becoming more and more complicated, the number of parameters used to define engineering application grows larger and larger, leading to the seriously reduced efficiency as well as the accuracy of the integrated model.
- related_work: From above comprehensive investigation about the integration of CBR and AI techniques, it can be found that under big data, BN is more appropriate to be integrated with CBR for knowledge reasoning than other AI techniques.
- method: Case of CBR system is represented by a set of features including problem features and solution features, which are extracted from lots of crude data of practical cases through feature selection.
- experiments: The total structure of system implementation for the experiments is composed of two parts, namely hardware components and soft components.
- experiments: Table 2 shows that IE algorithm significantly enhances the efficiency of system working and it has the least average time costing with the least standard deviation among all parallel data processing methods.
- conclusion: In order to construct an advanced CBR system to provide technique support for realizing the intelligence of engineering process in industrial field under big data, this paper develops IE algorithm and DECMBD algorithm to improve knowledge reasoning of CBR system.
- conclusion: The effectiveness of proposed integrated system has been validated by two practical cases, in each of which the popular statistical test method named the Friedman test and Nemenyi post-test is adopted for the efficiency evaluation.
