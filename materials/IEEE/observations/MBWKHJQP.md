---
key: MBWKHJQP
title: "Soft Sensor Modeling Based on Vector- Quantized Weighted-Wasserstein VAE for Polyester Polymerization Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3403267"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PRELIMINARY` → `IV. PROPOSED MODEL` → `V. SOFT SENSOR MODELING ON POLYESTER POLYMERIZATION PROCESS DATASET` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work。Introduction 末路标为 `The rest of the article is organized as follows`（无 `this`）。Experiments 并入过程数据集节 `V`。

## Openers

- abstract: `The uneven distribution` — "The uneven distribution of process industrial data poses a significant challenge for soft sensor modeling." (p.1)
- introduction: `IN THE process` — "IN THE process industry, frequent supervision ensures a high cost of equipment maintenance and a strict demand for precision toward machines [1]." (p.1)
- related_work: `VAE is first` — "VAE is first proposed to integrate variational inference and deep neural networks." (p.2)
- method: `To apply this` — "To apply this model to the process industry data, we need to settle two problems in sequence." (p.3)
- experiments: `The flowchart of` — "The flowchart of the polyester polymerization process for industrial producing with the major process units is shown in Fig. 2 [6], [7], [8]." (p.6)
- conclusion: `In this article` — "In this article, a novel soft sensor model named VQWW-VAE was proposed to solve the uneven distribution of data." (p.9)

## Gap transitions

- hence (abstract): "Hence, it is necessary to employ generative models to generate some new data used for augmenting the distribution fitting ability of the model by the full utilization of sparse regions." (p.1)
- however (introduction): "However, the limitations could not be ignored in the sense that these models are more suitable for specific data types, such as image or text, and include complex feature extraction structures." (p.1)
- therefore (introduction): "Therefore, to better resolve the problem of sparse regions and generate higher quality data, a novel model named vector-quantized weighted-Wasserstein variational autoencoder (VQWW-VAE) is proposed in this work." (p.2)
- although (related_work): "Although various models can be chosen to implement the generating tasks, the limitations of them still cannot be ignored, which can be divided into two aspects." (p.2)

## Hedge verbs

- develop / causal / abstract: "a novel vector-quantized weighted-Wasserstein variational autoencoder based soft sensor is developed in this article"
- propose / causal / introduction, conclusion: "a novel model named ... is proposed in this work"; "a novel soft sensor model named VQWW-VAE was proposed"
- verify / causal / abstract: "the superiority of the proposed soft sensor model with the novel data augmentation strategies is unequivocally verified"
- show / causal / conclusion: "our model showed higher superiority in prediction than others"
- may / speculative / conclusion: "the predictive accuracy of the model may gradually reach a bottleneck"

## Cross-section linkers

- introduction → related_work: "The rest of the article is organized as follows. Section II shows the related work. Section III briefly outlines the VAE. Section IV introduces the proposed model and how to implement the process. Section V verifies the model effectiveness by a soft sensor in the polymerization dataset [17], [31]. Finally, Section VI concludes the article." (p.2)
- related_work → preliminary: 缺口评述后 `III. PRELIMINARY` (p.3)
- method → experiments: Algorithm 1 后 `V. SOFT SENSOR MODELING ON POLYESTER POLYMERIZATION PROCESS DATASET` (p.6)
- experiments → conclusion: 误差图后 `VI. CONCLUSION` (p.9)

## Candidate rules

- R006 独立 Related Work，后接 `PRELIMINARY` 再进入 Proposed Model。
- R003 路标用 `The rest of the article is organized as follows`（可省略 `this`）。
- R004 贡献用 `The main contributions of this article are generalized as follows`。
- R005 Conclusion 先编号收回结论，再用 `In the future` 承认离线模型弱点。

## Candidate phrases

- `is developed in this article to` (abstract)
- `is proposed in this work` (introduction)
- `The main contributions of this article are generalized as follows.` (introduction)
- `The rest of the article is organized as follows.` (introduction)
- `In this article, a novel soft sensor model named ... was proposed to` (conclusion)

## House style

自称 `this article` / `this work` / `our model` / `we need`。未见 `Here we`、`In this paper`。`developed in this article` 与 `proposed in this work` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The uneven distribution of process industrial data poses a significant challenge for soft sensor modeling.
- p.1 abstract: Hence, it is necessary to employ generative models to generate some new data used for augmenting the distribution fitting ability of the model by the full utilization of sparse regions.
- p.1 abstract: To enhance the applicability of generative models in industrial data modeling, a novel vector-quantized weighted-Wasserstein variational autoencoder based soft sensor is developed in this article to solve uneven distribution data.
- p.1 introduction: IN THE process industry, frequent supervision ensures a high cost of equipment maintenance and a strict demand for precision toward machines [1].
- p.1 introduction: However, the limitations could not be ignored in the sense that these models are more suitable for specific data types, such as image or text, and include complex feature extraction structures.
- p.2 introduction: Therefore, to better resolve the problem of sparse regions and generate higher quality data, a novel model named vector-quantized weighted-Wasserstein variational autoencoder (VQWW-VAE) is proposed in this work.
- p.2 introduction: The main contributions of this article are generalized as follows.
- p.2 introduction: The rest of the article is organized as follows. Section II shows the related work. Section III briefly outlines the VAE. Section IV introduces the proposed model and how to implement the process. Section V verifies the model effectiveness by a soft sensor in the polymerization dataset [17], [31]. Finally, Section VI concludes the article.
- p.2 related_work: VAE is first proposed to integrate variational inference and deep neural networks.
- p.2 related_work: Although various models can be chosen to implement the generating tasks, the limitations of them still cannot be ignored, which can be divided into two aspects.
- p.3 method: To apply this model to the process industry data, we need to settle two problems in sequence.
- p.6 experiments: The flowchart of the polyester polymerization process for industrial producing with the major process units is shown in Fig. 2 [6], [7], [8].
- p.9 conclusion: In this article, a novel soft sensor model named VQWW-VAE was proposed to solve the uneven distribution of data.
- p.9 conclusion: In the future, the predictive accuracy of the model may gradually reach a bottleneck.
- p.9 conclusion: Therefore, the offline model needs to be optimized into a just-in-time version in the future.
