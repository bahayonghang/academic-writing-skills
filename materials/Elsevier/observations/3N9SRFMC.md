---
key: 3N9SRFMC
title: "Feature ranking for enhancing boosting-based multi-label text categorization"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2018.07.024"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries and problem statement` → `3. Related work` → `4. Boosting algorithms` → `5` 特征加权 → `6. BoWT text representation model` → `7. Experiments and results` → `8. Conclusion`。前置 `a b s t r a c t` 与 `a r t i c l e i n f o` / `Keywords`。独立 Related Work：`3. Related work`。Introduction 提出双重目标（七种特征排序 + RFBoost1），无编号贡献列表。Method 拆成预备、boosting、特征排序与 BoWT。Experiments 标题为 `7. Experiments and results`。

## Openers

- abstract: `Boosting algorithms have` — "Boosting algorithms have been proved effective for multi-label learning."
- introduction: `According to the` — "According to the International Data Corporation (Gantz & Reinsel, 2012), digital data on the Internet will grow to 40,000 exabytes by 2020, from 130 exabytes in 2005."
- related_work: `A simple approach` — "A simple approach to solving the multi-label classification problem involves transforming the multi-label task into a set of single-label subtasks."
- method: `In this section` — "In this section, we describe the boosting algorithms to be evaluated—AdaBoost.MH, RFBoost, and the proposed RFBoost1—and present their mechanisms for performing the weak learning and selecting the weak hypotheses." (s.4)
- experiments: `In this section` — "In this section, we first describe the datasets we used for the evaluation."
- conclusion: `RFBoost is an` — "RFBoost is an improved and accelerated version of AdaBoost.MH which proves to be effective and efficient for multi-label text categorization."

## Gap transitions

- however (introduction): "However, these algorithms are restricted to single-label classification problems, in which each instance (each text, in our case) is assigned to only one class label."
- although (introduction): "Although it is an accurate multi-label classification algorithm, AdaBoost.MH has been criticized for its inefficient processing time (Esuli et al., 2006)." (s.3 亦有同类转折)
- instead of (related work): "Instead of using random feature selection or inner feature selection to decrease the number of features to be examined in each boosting round, as LazyBoosting and BanditBoost respectively do, RFBoost ... addresses this problem by first ranking the features"
- in addition (abstract, conclusion): "In addition, we proposed an accelerated version of RFBoost named “RFBoost1”."

## Hedge verbs

- presents / causal / introduction: "this paper presents and investigates seven feature ranking methods"
- demonstrate / associative / abstract: "Experimental results on four benchmark datasets ... demonstrate that among the methods evaluated for feature ranking, mutual information yields the best performance for RFBoost."
- prove / causal / abstract: "the results prove that RFBoost statistically outperforms both RFBoost1 and AdaBoost.MH on all datasets."
- show / associative / conclusion: "The experimental results show that RFBoost1 accelerates the weak learning without penalizing the classification performance."

## Cross-section linkers

- introduction → preliminaries: 目标陈述后 `2. Preliminaries and problem statement`
- preliminaries → related_work: 复杂度对照后 `3. Related work`
- related_work → method: "4. Boosting algorithms"
- method → experiments: "7. Experiments and results"
- experiments → conclusion: 训练时间图后 `8. Conclusion`

## Candidate rules

- R001 独立 Related Work：`3. Related work`（位于预备之后、方法之前）。
- R009 自称：`this paper presents` / `we proposed` / `The aim of the present paper is twofold`

## Candidate phrases

- `this paper presents and investigates seven feature ranking methods` (abstract/introduction)
- `The aim of the present paper is twofold` (introduction)
- `In addition, we proposed an accelerated version of RFBoost named “RFBoost1”` (conclusion)
- `The experimental results show that` (conclusion)

## House style

自称 `this paper presents` / `we proposed` / `we investigate` / `The aim of the present paper`。第一人称复数为主。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Boosting algorithms have been proved effective for multi-label learning.
- abstract: As feature ranking is the core idea of RFBoost, this paper presents and investigates seven feature ranking methods (information gain, chi-square, GSS-coefficient, mutual information, odds ratio, F1 score, and accuracy) in order to improve RFBoost’s performance.
- abstract: Experimental results on four benchmark datasets for multi-label text categorization (Reuters-21578, 20-Newsgroups, OHSUMED, and TMC2007) demonstrate that among the methods evaluated for feature ranking, mutual information yields the best performance for RFBoost.
- abstract: In addition, the results prove that RFBoost statistically outperforms both RFBoost1 and AdaBoost.MH on all datasets.
- introduction: According to the International Data Corporation (Gantz & Reinsel, 2012), digital data on the Internet will grow to 40,000 exabytes by 2020, from 130 exabytes in 2005.
- introduction: The aim of the present paper is twofold: to investigate several existing feature weighting methods ... in order to improve RFBoost, and to propose an accelerated variant of RFBoost, named “RFBoost1”.
- related_work: A simple approach to solving the multi-label classification problem involves transforming the multi-label task into a set of single-label subtasks.
- experiments: In this section, we first describe the datasets we used for the evaluation.
- experiments: The multiple pairwise comparisons between boosting algorithms (Table 4) showed that RFBoost performs significantly better than both RFBoost1 and AdaBoost.MH.
- conclusion: RFBoost is an improved and accelerated version of AdaBoost.MH which proves to be effective and efficient for multi-label text categorization.
- conclusion: The experimental results show that RFBoost1 accelerates the weak learning without penalizing the classification performance.
