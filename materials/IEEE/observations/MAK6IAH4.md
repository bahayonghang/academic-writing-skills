---
key: MAK6IAH4
title: "Triple-Gated Bidirectional Variational Pyramid Network for Multirate Industrial Soft Sensing"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2025.3548053"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "12756-12767"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED METHODS` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 AE/VAE 软测量与 MR-PDDLS / MR-PVAE，再指单向信息流局限）。Introduction 末用 `The structure is as follows` 指向第二至末节。Method 为 `III. PROPOSED METHODS`。Experiments 标题为 `IV. CASE STUDY`（debutanizer column + 燃气轮机 NOx）。

## Openers

- abstract: `In various industrial` — "In various industrial processes, soft sensors have become important tools for predicting key quality variables." (p.12756)
- introduction: `PRECISION measurements of` — "PRECISION measurements of key quality variables form a cornerstone for stable operations and increased product quality in industrial processes [1], [2]." (p.12756；栏首掉字)
- method: `G3-BiVPN is proposed` — "G3-BiVPN is proposed to address the issue of data imbalance caused by industrial process data with multiple sampling rates." (p.12759, III)
- experiments: `In this section` — "In this section, two sets of industrial process data, namely the debutanizer column [29] and power plant gas turbine emission process [20], [30], are used to validate the performance of the proposed G3-BiVPN." (p.12762, IV)
- conclusion: `In this paper` — "In this paper, G3-BiVPN is introduced to address the issue of multiple sampling rates in industrial process data." (p.12766)

## Gap transitions

- however (abstract): "However, traditional soft sensor models only use data from the same sampling moments as the key quality variables, thus wasting information from other sampling moments." (p.12756)
- in light of this (abstract): "In light of this, a novel soft sensor model named triple-gated bidirectional variational pyramid network (G3-BiVPN) is proposed." (p.12756)
- however (introduction): "However, due to the complexity of industrial environments, limitations in sensor technology, high maintenance costs, and the inherent delay in signal transmission, direct measurement of key quality variables becomes challenging [3], [4], [5]." (p.12756)
- nevertheless (introduction): "Nevertheless, traditional soft sensing methods usually overlook different sampling rates among variables, treating them as single-rate." (p.12757)
- however (introduction): "However, with the increasing complexity of modern industry, existing methods are no longer able to handle large-scale multirate missing data effectively." (p.12757)
- in response (introduction): "In response to the aforementioned issues, this paper proposes a multirate soft sensing model named triple-gated bidirectional variational pyramid network (G3-BiVPN)." (p.12757)

## Hedge verbs

- propose / causal / abstract, introduction: "a novel soft sensor model named ... is proposed"; "this paper proposes a multirate soft sensing model"
- introduce / causal / introduction, conclusion: "G3-BiVPN is introduced to address the issue of multiple sampling rates"
- validate / causal / abstract, experiments: "the efficiency of G3-BiVPN has been validated"; "are used to validate the performance"
- demonstrate / causal / conclusion: "the experimental results demonstrate the effectiveness and superiority of the proposed G3-BiVPN"
- can / speculative / introduction, conclusion: "G3-BiVPN can adapt to the complexity of multirate data"; "enabling the model to learn detailed specifics"

## Cross-section linkers

- introduction → preliminaries: "The structure is as follows: the second part introduces the basic knowledge of VAE, BiFPN, and gating mechanism; the third part presents the concrete steps of G3-BiVPN; the fourth part simulates and analyzes the datasets. Finally, the last part provides the conclusions." (p.12757)
- method → experiments: Algorithm 1 与指标公式后 `IV. CASE STUDY` (p.12762)
- experiments → conclusion: 消融段落后直接 `V. CONCLUSION` (p.12766)

## Candidate rules

- R001 abstract 用 `In light of this, a novel ... is proposed` 接在 However 浪费信息之后。
- R002 Introduction 无独立 Related Work；路标用 `The structure is as follows: the second part ...` 而非 `Section II`。
- R003 贡献用 `The main contributions of this paper are as follows:` + (1)(2)(3)。
- R004 Experiments 标题为 `CASE STUDY`，先列五个对比模型再分装置。
- R005 Conclusion 先收回双向信息流，再用 `The assumption in this paper is` 承认同步假设，再给 future 对齐方法。

## Candidate phrases

- `In light of this, a novel soft sensor model named ... is proposed` (abstract)
- `this paper proposes a multirate soft sensing model named` (introduction)
- `The main contributions of this paper are as follows:` (introduction)
- `The structure is as follows:` (introduction)
- `In this paper, G3-BiVPN is introduced to address` (conclusion)

## House style

自称是 `this paper` / `In this paper` / `the proposed G3-BiVPN`。未见 `Here we`。`In this paper` 与 `this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。Note to Practitioners 用方法名直述，少用 we。

## Quotes

- p.12756 abstract: In various industrial processes, soft sensors have become important tools for predicting key quality variables.
- p.12756 abstract: However, traditional soft sensor models only use data from the same sampling moments as the key quality variables, thus wasting information from other sampling moments.
- p.12756 abstract: In light of this, a novel soft sensor model named triple-gated bidirectional variational pyramid network (G3-BiVPN) is proposed.
- p.12756 introduction: PRECISION measurements of key quality variables form a cornerstone for stable operations and increased product quality in industrial processes [1], [2].
- p.12757 introduction: Nevertheless, traditional soft sensing methods usually overlook different sampling rates among variables, treating them as single-rate.
- p.12757 introduction: In response to the aforementioned issues, this paper proposes a multirate soft sensing model named triple-gated bidirectional variational pyramid network (G3-BiVPN).
- p.12757 introduction: The main contributions of this paper are as follows:
- p.12757 introduction: The structure is as follows: the second part introduces the basic knowledge of VAE, BiFPN, and gating mechanism; the third part presents the concrete steps of G3-BiVPN; the fourth part simulates and analyzes the datasets. Finally, the last part provides the conclusions.
- p.12759 method: G3-BiVPN is proposed to address the issue of data imbalance caused by industrial process data with multiple sampling rates.
- p.12762 experiments: In this section, two sets of industrial process data, namely the debutanizer column [29] and power plant gas turbine emission process [20], [30], are used to validate the performance of the proposed G3-BiVPN.
- p.12764 experiments: Among all the models, G3-BiVPN exhibits the best performance, thanks to its triple gating mechanism and bidirectional information flow architecture.
- p.12766 conclusion: In this paper, G3-BiVPN is introduced to address the issue of multiple sampling rates in industrial process data.
- p.12766 conclusion: A distinctive feature of G3-BiVPN is its ability to facilitate bidirectional information flow between data of different sampling rates, enabling the model to learn detailed specifics and features from high sampling rate data while also capturing overarching insights and critical information from low sampling rate data.
- p.12767 conclusion: Finally, the experimental results demonstrate the effectiveness and superiority of the proposed G3-BiVPN in handling multirate industrial process data.
- p.12767 conclusion: The assumption in this paper is that the involved data is synchronized within the least common multiple period.
- p.12767 conclusion: Addressing asynchronous data collection in future research is a key challenge that requires more advanced methods, such as time warping techniques, or probabilistic alignment models, to accurately synchronize the datasets.
