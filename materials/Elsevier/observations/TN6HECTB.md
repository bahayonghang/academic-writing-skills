---
key: TN6HECTB
title: "Global data mining: An empirical study of current trends, future forecasts and technology diffusions"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2012.01.150"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Material and methodology` → `3. Results` → 后续含扩散活动段 → `6. Conclusions`。前置 `abstract` 与 `article info` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 KDD 定义、Turban 等定义、应用领域；方法节引用 Pritchard / Broadus / Lotka）。无编号贡献列表。Introduction 末用分析目标收束，不写节序路标。Method 为文献计量材料与 Lotka / K-S。Experiments 标题为 `3. Results`（按年、引用、国家、机构等分布）。

## Openers

- abstract: `Using a bibliometric` — "Using a bibliometric approach, this paper analyzes research trends and forecasts of data mining from 1989 to 2009 by locating heading “data mining” in topic in the SSCI database."
- introduction: `Data mining is` — "Data mining is an interdisciplinary field that combines artificial intelligence, database management, data visualization, machine learning, mathematic algorithms, and statistics."
- method: `Weingart (2003, 2004)` — "Weingart (2003, 2004) pointed at the very influential role of the monopolist citation data producer ISI (Institute for Scientific Information, now Thomson Scientific) as its commercialization of these data (Adam, 2002) rapidly increased the non-expert use of bibliometric analysis such as rankings." (s.2.1)
- experiments: `As Fig. 1 shows` — "As Fig. 1 shows, the article production on data mining has been rising since 1996."
- conclusion: `Using a bibliometric` — "Using a bibliometric approach, the paper analyzes technology trends and forecasts of data mining from 1989 to 2009 by locating heading “data mining” in topic in the SSCI database."

## Gap transitions

- this implies (abstract, conclusion): "This implies that the phenomenon “success breeds success” is more common in higher quality publications."
- besides (introduction/method): "Besides, the analysis also reviews the historical literatures to come out technology diffusions of data mining."
- also (abstract): "Also, the paper performs the K-S test to check whether the analysis follows Lotka’s law."

## Hedge verbs

- analyzes / causal / abstract: "this paper analyzes research trends and forecasts of data mining"
- found / associative / abstract: "we found 1181 articles with data mining"
- indicates / associative / results: "The result indicates that data mining will keep popular in the future."
- shows (K-S) / associative / conclusion: "According to the K-S test, the result shows that the author productivity distribution predicted by Lotka holds for data mining."

## Cross-section linkers

- introduction → method: Introduction 重复摘要级目标后 `2. Material and methodology`
- method → results: K-S 步骤后 `3. Results`
- results → conclusion: 扩散活动段落后 `6. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R009 自称：`this paper analyzes` / `the paper analyzes` / `This paper surveys and classifies`

## Candidate phrases

- `Using a bibliometric approach, this paper analyzes` (abstract)
- `This paper implemented and classified data mining articles using the following eight categories` (abstract)
- `The paper provides a roadmap for future research` (abstract)
- `The results in this paper have several important implications:` (conclusion)

## House style

自称 `this paper analyzes` / `the paper analyzes` / `This paper surveys` / `we found`。结论用编号含义列表。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Using a bibliometric approach, this paper analyzes research trends and forecasts of data mining from 1989 to 2009 by locating heading “data mining” in topic in the SSCI database.
- abstract: This paper implemented and classified data mining articles using the following eight categories—publication year, citation, country/territory, document type, institute name, language, source title and subject area—for different distribution status in order to explore the differences and how data mining technologies have developed in this period and to analyze technology tendencies and forecasts of data mining under the above results.
- abstract: The paper provides a roadmap for future research, abstracts technology trends and forecasts, and facilitates knowledge accumulation so that data mining researchers can save some time since core knowledge will be concentrated in core categories.
- introduction: Data mining is an interdisciplinary field that combines artificial intelligence, database management, data visualization, machine learning, mathematic algorithms, and statistics.
- method: Pritchard (1969, p. 349) defined bibliometrics as “the application of mathematics and statistical methods to books and other media of communication.”
- experiments: As Fig. 1 shows, the article production on data mining has been rising since 1996.
- experiments: The result indicates that data mining will keep popular in the future.
- conclusion: The results in this paper have several important implications:
- conclusion: According to the K-S test, the result shows that the author productivity distribution predicted by Lotka holds for data mining.
- conclusion: This implies that the phenomenon “success breeds success” is more common in higher quality publications.
