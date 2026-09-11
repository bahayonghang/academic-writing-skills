---
key: SXFSN4SB
title: "A Novel Semisupervised Approach for Caustic Concentration Prediction in Alumina Production"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3576877"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEMS IN CAUSTIC CONCENTRATION PREDICTION` → `III. SEMISUPERVISED LEARNING WITH TRANSFORMER VARIATIONAL AUTOENCODER` → `IV. INDUSTRIAL EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 semisupervised time-series classification / clustering / generation）。Introduction 末为编号贡献，无 `The rest of this article is organized` 路标。II 是过程与数据缺口，不是综述节。Method 标题为 TVAE。Experiments 标题为 `INDUSTRIAL EXPERIMENTS`。

## Openers

- abstract: `Precise online prediction` — "Precise online prediction of caustic concentration is crucial for optimal control and operating efficiency in alumina production." (p.1)
- introduction: `ALUMINUM has the` — "ALUMINUM has the highest global production volume among nonferrous metals and is widely used across various industries, such as aerospace, automotive, and construction [1]." (p.1)
- method: `Our proposed semisupervised` — "Our proposed semisupervised learning framework uses a novel TVAE, which utilizes the power of Transformer architecture, renowned for its ability to capture long-range dependencies, to effectively model complex relationships in time-series data." (p.3, III)
- experiments: `We conduct extensive` — "We conduct extensive experiments to evaluate our method using a dataset collected from a large-scale Bayer alumina plant." (p.5, IV)
- conclusion: `Our proposed semisupervised` — "Our proposed semisupervised TVAE method demonstrates significant potential for accurate caustic concentration prediction in alumina production." (p.9)

## Gap transitions

- however (abstract): "However, existing supervised learning models rely heavily on a large amounts of labeled assay samples, which are time-consuming and resource intensive to obtain." (p.1)
- to overcome (abstract): "To overcome this challenge, we propose a novel semisupervised learning approach that effectively uses both labeled and unlabeled data." (p.1)
- despite (introduction): "Despite the impressive performance of existing semisupervised time-series learning methods [17], [18], caustic concentration prediction still faces significant challenges." (p.1)
- to overcome (introduction): "To overcome these challenges, in this article, we propose a novel semisupervised transformer variational autoencoder (dubbed TVAE) for precise caustic concentration prediction in the Bayer alumina production process." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a novel semisupervised learning approach"; "in this article, we propose a novel semisupervised transformer variational autoencoder"
- demonstrate / causal / abstract, conclusion: "Experiments on a real-world alumina production process demonstrate the superior performance of our approach"; "Our proposed semisupervised TVAE method demonstrates significant potential"
- showcase / causal / conclusion: "Our experimental results clearly showcase the superior performance of our TVAE"

## Cross-section linkers

- introduction → problem: 贡献列表后直接 `II. PROBLEMS IN CAUSTIC CONCENTRATION PREDICTION` (p.2)
- problem → method: 三项挑战后 `III. SEMISUPERVISED LEARNING WITH TRANSFORMER VARIATIONAL AUTOENCODER` (p.3)
- method → experiments: 联合优化讨论后 `IV. INDUSTRIAL EXPERIMENTS` (p.5)
- experiments → conclusion: 附加消化过程实验后 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `we propose a novel semisupervised learning approach`，不用 `Here we`。
- R002 Introduction 无独立 Related Work；半监督时序方法评述写在引言中段。
- R003 贡献列表后直接进入过程问题节，无节序路标句。
- R004 Experiments 标题为 `INDUSTRIAL EXPERIMENTS`。
- R005 Conclusion 用 `Our proposed ... method demonstrates`，再用 `Future work could explore` 指向后续。

## Candidate phrases

- `To overcome this challenge, we propose a novel` (abstract)
- `To overcome these challenges, in this article, we propose` (introduction)
- `Our contributions are summarized as follows:` (introduction)
- `Our proposed semisupervised TVAE method demonstrates significant potential for` (conclusion)
- `Future work could explore the application of our TVAE to` (conclusion)

## House style

自称是 `we propose` / `in this article` / `Our proposed` / `our approach`。未见 `Here we`。`in this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Precise online prediction of caustic concentration is crucial for optimal control and operating efficiency in alumina production.
- p.1 abstract: However, existing supervised learning models rely heavily on a large amounts of labeled assay samples, which are time-consuming and resource intensive to obtain.
- p.1 abstract: To overcome this challenge, we propose a novel semisupervised learning approach that effectively uses both labeled and unlabeled data.
- p.1 introduction: ALUMINUM has the highest global production volume among nonferrous metals and is widely used across various industries, such as aerospace, automotive, and construction [1].
- p.1 introduction: Despite the impressive performance of existing semisupervised time-series learning methods [17], [18], caustic concentration prediction still faces significant challenges.
- p.2 introduction: To overcome these challenges, in this article, we propose a novel semisupervised transformer variational autoencoder (dubbed TVAE) for precise caustic concentration prediction in the Bayer alumina production process.
- p.2 introduction: Our contributions are summarized as follows:
- p.3 method: Our proposed semisupervised learning framework uses a novel TVAE, which utilizes the power of Transformer architecture, renowned for its ability to capture long-range dependencies, to effectively model complex relationships in time-series data.
- p.5 experiments: We conduct extensive experiments to evaluate our method using a dataset collected from a large-scale Bayer alumina plant.
- p.6 experiments: Table I lists the result of evaluation metrics. Our proposed method outperforms most existing methods, underscoring its efficacy.
- p.9 conclusion: Our proposed semisupervised TVAE method demonstrates significant potential for accurate caustic concentration prediction in alumina production.
- p.9 conclusion: By effectively using both labeled and unlabeled data, our approach overcomes the limitations of traditional fully supervised techniques and existing semisupervised methods that depend heavily on labeled data.
- p.9 conclusion: Future work could explore the application of our TVAE to other industrial processes with similar data characteristics.
