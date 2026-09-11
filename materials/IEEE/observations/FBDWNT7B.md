---
key: FBDWNT7B
title: "Graph Foundation Models: Concepts, Opportunities and Challenges"
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence"
doi: "10.1109/TPAMI.2025.3548729"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8,15-22"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

阿拉伯数字标题：`1 INTRODUCTION` → `2 BACKGROUND` → `3 GRAPH FOUNDATION MODELS` → `4` GNN-based models → `5` LLM-based models → `6` GNN+LLM-based models → `7` future directions → `8 CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。独立 BACKGROUND（2.1 Deep Graph Learning / 2.2 Language Foundation Models），作 related-work 级铺垫。`related_work=independent`。Introduction 末有节序路标，指向 Section 2–8。Survey 无 Experiments 节。

## Openers

- abstract: `Foundation models have` — "Foundation models have emerged as critical components in a variety of artificial intelligence applications, and showcase significant success in natural language processing and several other domains." (p.1)
- introduction: `WITH the rise` — "WITH the rise in computational power and breakthroughs in deep learning techniques, the artificial intelligence (AI) community has introduced the notion of “foundation models”: A foundation model is any model that is trained on broad data and can be adapted to a wide range of downstream tasks [1]." (p.1)
- background: `Before introducing GFMs,` — "Before introducing GFMs, we review background knowledge on deep graph learning and language foundation models." (p.2, §2)
- method: `In this section,` — "In this section, we will first formally define the concepts of graph foundation models, including the definition, key characteristics and key technologies." (p.4, §3)
- conclusion: `The development of` — "The development of foundation models and graph machine learning has spurred the emergence of a new research direction, with the aim to train on broad graph data and apply it to a wide range of downstream graph tasks." (p.16, §8)

## Gap transitions

- despite (abstract): "Despite this burgeoning interest, there is a noticeable lack of clear definitions and systematic analyses pertaining to this new domain." (p.1)
- however (introduction): "These methods, however, were typically limited to transductive learning [13]." (p.1)
- however (introduction): "However, certain challenges of GNN models still persist." (p.1)
- nonetheless (introduction): "Nonetheless, it remains uncertain whether LLMs can effectively handle graph data and associated tasks, and it is crucial to determine how to model graph structures in LLMs." (p.2)
- therefore (introduction): "Therefore, there is also a need to design suitable pre-training tasks and adaptation mechanisms." (p.2)
- to this end (abstract): "To this end, this article introduces the concept of Graph Foundation Models (GFMs), and offers an exhaustive explanation of their key characteristics and underlying technologies." (p.1)

## Hedge verbs

- introduce / causal / abstract: "this article introduces the concept of Graph Foundation Models (GFMs)"
- survey / causal / introduction: "this paper surveys some related researches and categorizes them into three distinct approaches"
- propose / causal / conclusion: "In this article, we propose the concept of graph foundation models (GFMs) for the first time"
- may / speculative / introduction: "as a foundation model scales up, it may spontaneously manifest novel capabilities [2]"
- remain / speculative / introduction: "it remains uncertain whether LLMs can effectively handle graph data"

## Cross-section linkers

- introduction → background: "The subsequent sections are organized as follows. In Section 2, we introduce the background related to GFMs. Section 3 defines GFMs and highlights their similarities and differences with language foundation models. Sections 4 - 6 delve into the relevant works that consider GNN-based models, LLM-based models and GNN+LLM-based models as GFMs, separately. Section 7 engages in a discussion on the future directions of GFMs. In Section 8, we summarize the key points of this paper." (p.2)
- background → GFM definition: "Before introducing GFMs, we review background knowledge on deep graph learning and language foundation models." 随后 `3 GRAPH FOUNDATION MODELS` (p.2–4)
- future → conclusion: §7 Challenges/future 后直接 `8 CONCLUSIONS` (p.16)

## Candidate rules

- R001 Survey 摘要用 `this article introduces the concept of` 立术语，再用 `We proceed to classify` 给分类。
- R002 Introduction 末用 `The subsequent sections are organized as follows` + Section 2–8 路标。
- R003 贡献用 `the contributions of this article can be summarized as follows` + 项目符号。
- R004 独立 BACKGROUND 节承担 related work，不另开 Related Work 标题。
- R005 Conclusion 用 `In this article, we propose the concept of ... for the first time` 收回定义。

## Candidate phrases

- `this article introduces the concept of` (abstract)
- `To the best of our knowledge, this is the first survey towards` (introduction)
- `The subsequent sections are organized as follows.` (introduction)
- `We define a graph foundation model as follows:` (method, §3.1)
- `In this article, we propose the concept of` (conclusion)

## House style

自称是 `this article` / `this paper` / `we propose` / `we proceed to classify`。`this article introduces` 与 `this paper surveys` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。

## Quotes

- p.1 abstract: Foundation models have emerged as critical components in a variety of artificial intelligence applications, and showcase significant success in natural language processing and several other domains.
- p.1 abstract: Despite this burgeoning interest, there is a noticeable lack of clear definitions and systematic analyses pertaining to this new domain.
- p.1 abstract: To this end, this article introduces the concept of Graph Foundation Models (GFMs), and offers an exhaustive explanation of their key characteristics and underlying technologies.
- p.1 abstract: We proceed to classify the existing work related to GFMs into three distinct categories, based on their dependence on graph neural networks and large language models.
- p.1 abstract: In addition to providing a thorough review of the current state of GFMs, this article also outlooks potential avenues for future research in this rapidly evolving domain.
- p.1 introduction: WITH the rise in computational power and breakthroughs in deep learning techniques, the artificial intelligence (AI) community has introduced the notion of “foundation models”: A foundation model is any model that is trained on broad data and can be adapted to a wide range of downstream tasks [1].
- p.1 introduction: These methods, however, were typically limited to transductive learning [13].
- p.1 introduction: However, certain challenges of GNN models still persist.
- p.2 introduction: Nonetheless, it remains uncertain whether LLMs can effectively handle graph data and associated tasks, and it is crucial to determine how to model graph structures in LLMs.
- p.2 introduction: While there is no definitive solution for designing and implementing GFMs, this paper surveys some related researches and categorizes them into three distinct approaches based on their reliance on GNNs and LLMs.
- p.2 introduction: To the best of our knowledge, this is the first survey towards graph foundation models.
- p.2 introduction: Therefore, the contributions of this article can be summarized as follows.
- p.2 introduction: The subsequent sections are organized as follows. In Section 2, we introduce the background related to GFMs. Section 3 defines GFMs and highlights their similarities and differences with language foundation models. Sections 4 - 6 delve into the relevant works that consider GNN-based models, LLM-based models and GNN+LLM-based models as GFMs, separately. Section 7 engages in a discussion on the future directions of GFMs. In Section 8, we summarize the key points of this paper.
- p.2 background: Before introducing GFMs, we review background knowledge on deep graph learning and language foundation models.
- p.4 method: In this section, we will first formally define the concepts of graph foundation models, including the definition, key characteristics and key technologies.
- p.4 method: We define a graph foundation model as follows: Definition A graph foundation model (GFM) is a model that is expected to benefit from the pre-training of broad graph data, and can be adapted to a wide range of downstream graph tasks.
- p.16 conclusion: The development of foundation models and graph machine learning has spurred the emergence of a new research direction, with the aim to train on broad graph data and apply it to a wide range of downstream graph tasks.
- p.16 conclusion: In this article, we propose the concept of graph foundation models (GFMs) for the first time, and provide an introduction to relevant concepts and representative methods.
- p.16 conclusion: We summarize existing works towards GFMs into three main categories based on their reliance on graph neural networks (GNNs) and large language models (LLMs): GNN-based models, LLM-based models, and GNN+LLM-based models.
