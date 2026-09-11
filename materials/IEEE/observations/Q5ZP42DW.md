---
key: Q5ZP42DW
title: "Gated Stacked Target-Related Autoencoder: A Novel Deep Feature Extraction and Layerwise Ensemble Method for Industrial Soft Sensor Application"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2020.3010331"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-7,10-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BASIC STACKED AUTOENCODER AND GATED UNIT THEORIES` → `III. GATED STACKED TARGET-RELATED AUTOENCODER` → `IV. GSTAE-BASED SOFT SENSOR MODELING` → `V. CASE STUDIES` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SAE / ladder network / VWSAE，再指末层特征局限）。Introduction 末有 `The layout of this article is given as follows` 路标，指向 Section II–VI。Method 分 TAE/STAE 与门控集成。Experiments 标题为 `CASE STUDIES`（脱丁烷塔与 CO2 吸收塔）。

## Openers

- abstract: `These days, data-driven` — "These days, data-driven soft sensors have been widely applied to estimate the difficult-to-measure quality variables in the industrial process." (p.1)
- introduction: `IN MODERN industrial` — "IN MODERN industrial processes, it is of great importance to monitor the quality of products and other key variables, in order to keep the process in a safe state and provide an effective control and optimization style [1], [2]." (p.1；栏首掉字)
- method: `To deal with` — "To deal with those problems and improve the performance of SAE-based soft sensors, we propose the novel gated GSTAE in this article." (p.4, III)
- experiments: `In this section` — "In this section, the performance of the proposed GSTAE algorithm is validated on two real chemical industrial process cases." (p.6, V)
- conclusion: `In this article` — "In this article, taking the shortcomings of conventional SAE into consideration, a DL model called GSTAE was proposed to improve the performance of the SAE-based model for the soft sensing application." (p.11)

## Gap transitions

- however (introduction): "However, due to poor measuring environments and expensive analytic costs, it is hard to measure those important variables in time for process control." (p.1)
- nevertheless (abstract): "Nevertheless, conventional SAE-based methods do not take information related to target values in the pretraining stage and just use the feature representations in the last hidden layer for final prediction." (p.1)
- however (introduction): "However, this would lead to a simple reproduction of input, which is just not enough for practical applications." (p.2)
- therefore (introduction): "Therefore, it is necessary to find a more suitable means to establish a connection between input/latent variables and output values in the complex data environment." (p.2)
- however (conclusion): "However, there are some limitations of the proposed approach that need to be paid attention to." (p.11)

## Hedge verbs

- introduce / causal / abstract: "deep stacked autoencoder (SAE) is introduced to construct a soft sensor model"
- propose / causal / abstract, introduction, conclusion: "a novel gated stacked target-related autoencoder (GSTAE) is proposed"; "we propose the novel gated GSTAE"; "a DL model called GSTAE was proposed"
- verify / causal / abstract, conclusion: "the effectiveness and feasibility of the proposed approach are verified in two real industrial cases"; "the effectiveness and superiority of the proposed approaches were verified"
- should be / speculative / introduction, conclusion: "the prediction performance of SAE-based models should be improved"; "The proposed method should be helpful for improving the performance of soft sensors"
- will increase / speculative / conclusion: "the computational burden will increase linearly with the depth of the network"

## Cross-section linkers

- introduction → background: "The layout of this article is given as follows. In Section II, the basic SAE and gated neurons-related methodologies are shortly overviewed. Then, the GSTAE model is proposed in Section III and the soft sensor modeling framework based on GSTAE is shown in Section IV. After that, the effectiveness and feasibility of the proposed approach are demonstrated by constructing two soft sensors for real industrial applications in Section V. Finally, conclusions are made in Section VI." (p.2)
- method → experiments: 建模框架后 `V. CASE STUDIES` (p.6)
- experiments → conclusion: 门控值分析后 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `Nevertheless, conventional [METHOD]-based methods do not` 收缺口，再用 `To this end, a novel [NAME] is proposed`。
- R002 Introduction 无独立 Related Work，基础理论单独成 `II` 预备节。
- R003 Introduction 末用 `The layout of this article is given as follows` 指向 II–VI。
- R004 Experiments 标题可为 `CASE STUDIES`，开句 `the performance of the proposed … is validated on two real … cases`。
- R005 Conclusion 用 `In this article, taking the shortcomings of … into consideration, … was proposed`，再用 `However, there are some limitations`。

## Candidate phrases

- `To this end, a novel gated stacked target-related autoencoder (GSTAE) is proposed for` (abstract)
- `To deal with those problems and improve the performance of SAE-based soft sensors, we propose` (method)
- `The layout of this article is given as follows.` (introduction)
- `In this section, the performance of the proposed GSTAE algorithm is validated on` (experiments)
- `In this article, taking the shortcomings of conventional SAE into consideration, a DL model called GSTAE was proposed` (conclusion)

## House style

自称 `In this article` / `In this work` / `we propose` / `the proposed approach`。未见 `Here we`、`In this paper`。`In this article … was proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: These days, data-driven soft sensors have been widely applied to estimate the difficult-to-measure quality variables in the industrial process.
- p.1 abstract: Nevertheless, conventional SAE-based methods do not take information related to target values in the pretraining stage and just use the feature representations in the last hidden layer for final prediction.
- p.1 abstract: To this end, a novel gated stacked target-related autoencoder (GSTAE) is proposed for improving modeling performance in view of the above two issues.
- p.1 abstract: Finally, the effectiveness and feasibility of the proposed approach are verified in two real industrial cases.
- p.1 introduction: IN MODERN industrial processes, it is of great importance to monitor the quality of products and other key variables, in order to keep the process in a safe state and provide an effective control and optimization style [1], [2].
- p.1 introduction: However, due to poor measuring environments and expensive analytic costs, it is hard to measure those important variables in time for process control.
- p.2 introduction: However, this would lead to a simple reproduction of input, which is just not enough for practical applications.
- p.2 introduction: Therefore, it is necessary to find a more suitable means to establish a connection between input/latent variables and output values in the complex data environment.
- p.2 introduction: The layout of this article is given as follows. In Section II, the basic SAE and gated neurons-related methodologies are shortly overviewed. Then, the GSTAE model is proposed in Section III and the soft sensor modeling framework based on GSTAE is shown in Section IV. After that, the effectiveness and feasibility of the proposed approach are demonstrated by constructing two soft sensors for real industrial applications in Section V. Finally, conclusions are made in Section VI.
- p.4 method: To deal with those problems and improve the performance of SAE-based soft sensors, we propose the novel gated GSTAE in this article.
- p.6 experiments: In this section, the performance of the proposed GSTAE algorithm is validated on two real chemical industrial process cases.
- p.11 conclusion: In this article, taking the shortcomings of conventional SAE into consideration, a DL model called GSTAE was proposed to improve the performance of the SAE-based model for the soft sensing application.
- p.11 conclusion: Moreover, the effectiveness and superiority of the proposed approaches were verified by comparing with other SAE-based methods in two real industrial processes: 1) debutanizer column and 2) CO2 absorption column.
- p.11 conclusion: However, there are some limitations of the proposed approach that need to be paid attention to.
- p.11 conclusion: First, GSTAE was quite sensitive to samples with the poor-quality label since the supervision from target values are enhanced both in pretraining and fine-tuning process.
