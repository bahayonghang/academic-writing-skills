---
key: WI9JPIL2
title: "Human-AI cooperative generative adversarial network (GAN) for quality predictions of small-batch product series"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2025.103327"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,8-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

前置 `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction` → `2. Literature review` → `3. Framework for quality inspection based on the predictive model` → `4. Case study—predicting quality of highly-customized small-batch power transformers` → `5. Conclusions`。独立 Related Work（`2. Literature review`）。`related_work=independent`。Introduction 末点名方法与案例。Experiments 标题为 `Case study`。

## Openers

- abstract: `This paper emphasizes` — "This paper emphasizes the importance and the novel methodology of predicting product quality for smart manufacturing, particularly for small-batched power equipment productions with demand-specified variations in the energy sector."
- introduction: `In recent years` — "In recent years, machine learning (ML) and deep learning (DL) technologies have emerged as effective solutions for enhancing product quality control within companies."
- related_work: `Maintaining high-quality production` — "Maintaining high-quality production is essential for sustaining business operations and fostering brand equity through customer trust."
- method: `This study aims` — "This study aims to develop a robust quality inspection system utilizing a predictive model-based framework."
- experiments: `This section presents` — "This section presents a method for predicting the quality of highly customized products, such as power transformers, thereby enhancing smart manufacturing capabilities of small-batch productions."
- conclusion: `This study makes` — "This study makes substantial advancements in decision-making processes within the realm of smart manufacturing by integrating internal and external supply chain data, encompassing material inspection, production processes, and quality assessments."

## Gap transitions

- however (introduction): "However, the transition towards customization and small-batch production in contemporary enterprises has outpaced traditional production models [5]."
- therefore (introduction): "Therefore, to reduce product quality losses and operational costs, small-batch product manufacturers are placing a greater emphasis on the quality of finished products."
- to address (introduction): "To address the issue of small sample sizes in transformer production, we proposed a Human-AI cooperative Generative Adversarial Network (GAN) for model training and fine-tuning."
- consequently (abstract): "Consequently, the methodology presented in this study has the potential for broad application across diverse industrial manufacturing sectors"

## Hedge verbs

- propose / causal / abstract, introduction: "we proposed a novel method"; "we proposed a Human-AI cooperative Generative Adversarial Network (GAN)"
- indicate / associative / abstract: "The experimental findings indicate that the proposed approach offers manufacturers a powerful tool for predicting the quality of complex, high-value, and highly specialized industrial products"
- demonstrate / causal / experiments, conclusion: "Empirical results, validated through comprehensive real-world datasets, demonstrate the superior performance of the proposed model over conventional methods such as AdaBoost and its variants."

## Cross-section linkers

- introduction → related work: Introduction 末预告文献、方法与案例后 `2. Literature review`
- related work → method: GAN 综述后 `3. Framework for quality inspection based on the predictive model`
- method → experiments: 训练步骤后 `4. Case study—predicting quality of highly-customized small-batch power transformers`
- experiments → conclusion: 局限段落后 `5. Conclusions`

## Candidate rules

- R001 独立 Related Work（`2. Literature review`）。
- R009 自称：`This paper emphasizes` / `we proposed` / `This study introduces`

## Candidate phrases

- `This paper emphasizes the importance and the novel methodology` (abstract)
- `we proposed a novel method using a generative adversarial network (GAN)` (abstract)
- `This study introduces Generative Adversarial Networks (GANs)` (introduction)
- `The experimental findings indicate that the proposed approach` (abstract)
- `This study makes substantial advancements` (conclusion)

## House style

自称 `This paper` / `we proposed` / `This study` / `this article`（对比先前模型时用 `this article includes comparisons`）。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: This paper emphasizes the importance and the novel methodology of predicting product quality for smart manufacturing, particularly for small-batched power equipment productions with demand-specified variations in the energy sector.
- abstract: To predict final product quality, even with a small sample size of a specific transformer type (and unique design specification), we proposed a novel method using a generative adversarial network (GAN) for model training and fine-tuning.
- abstract: The experimental findings indicate that the proposed approach offers manufacturers a powerful tool for predicting the quality of complex, high-value, and highly specialized industrial products, ultimately leading to a reduction in production costs.
- introduction: In recent years, machine learning (ML) and deep learning (DL) technologies have emerged as effective solutions for enhancing product quality control within companies.
- introduction: However, the transition towards customization and small-batch production in contemporary enterprises has outpaced traditional production models [5].
- introduction: To address the issue of small sample sizes in transformer production, we proposed a Human-AI cooperative Generative Adversarial Network (GAN) for model training and fine-tuning.
- related_work: Maintaining high-quality production is essential for sustaining business operations and fostering brand equity through customer trust.
- method: This study aims to develop a robust quality inspection system utilizing a predictive model-based framework.
- experiments: This section presents a method for predicting the quality of highly customized products, such as power transformers, thereby enhancing smart manufacturing capabilities of small-batch productions.
- conclusion: This study makes substantial advancements in decision-making processes within the realm of smart manufacturing by integrating internal and external supply chain data, encompassing material inspection, production processes, and quality assessments.
- conclusion: In conclusion, this study not only provides a significant step forward in addressing the challenges of small-sample, high-customization manufacturing but also lays a robust foundation for advancing human-AI collaboration in industrial contexts.
