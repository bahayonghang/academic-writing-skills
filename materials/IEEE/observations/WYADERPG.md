---
key: WYADERPG
title: "Performance-Driven Distillation and Confident Pseudo Labeling for Semi-Supervised Industrial Soft-Sensor Application"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2025.3580633"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PERFORMANCE DRIVEN DISTILLATION` → `III. PSEUDO LABEL CONFIDENCE EVALUATION` → `IV. INDUSTRIAL APPLICATIONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCA/SVM、深度学习软测量、半监督 feature-construction 与 pseudo-label）。Introduction 末为编号贡献，无 `The rest of this article is organized` 路标。Method 拆为蒸馏与伪标签置信度两节。Experiments 标题为 `INDUSTRIAL APPLICATIONS`（氧化铝蒸发与溶出）。

## Openers

- abstract: `In industrial soft-sensor` — "In industrial soft-sensor applications, labeled samples are often scarce and unable to fully represent the dynamic changes in industrial processes." (p.1)
- introduction: `WITH the increasing` — "WITH the increasing automation in industrial processes, real-time measurement of quality variables is crucial for timely control and optimization, promoting stable and sustained operations [1], [2]." (p.1)
- method: `It is common knowledge` — "It is common knowledge that industrial production processes change slowly, and the key variables exhibit complex spatiotemporal coupling relationships." (p.3, II.A)
- experiments: `In this section` — "In this section, the proposed PP-strategy is validated on a real alumina evaporation production process datasets and a real alumina digestion production process datasets." (p.6, IV)
- conclusion: `This article proposed` — "This article proposed a novel method named PP-strategy for soft sensor of industrial quality variables." (p.11)

## Gap transitions

- although (abstract): "Although semi-supervised methods offer a potential solution to this issue, existing feature-construction-based methods cannot ensure the effectiveness of the feature, and pseudo-label-based methods lack an established confidence evaluation standard." (p.1)
- to address (abstract): "To address these challenges, this article first proposes a novel performance-driven distillation strategy, which designs an innovative siameseLSTM structure for training multiple teacher models." (p.1)
- however (introduction): "However, in industries, such as nonferrous metallurgy, quality variables are often element concentration or other values that can only be obtained through laboratory assays" (p.2)
- nevertheless (introduction): "Nevertheless, both types of methods face significant bottlenecks, which limit the application of semi-supervised methods in industrial process soft sensing." (p.2)
- although (conclusion): "Although PP-strategy achieved notable performance and provides solutions to two major challenges in semi-supervised soft sensor, there are still some limitations." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction: "this article first proposes a novel performance-driven distillation strategy"; "this article proposes an innovative performance-driven distillation strategy"
- aim / causal / abstract: "which aims to enhance the generalization of the base soft-sensor model"
- demonstrate / causal / conclusion: "The experimental results demonstrated that the PP-strategy could significantly improve soft sensor performance"
- could / speculative / conclusion: "the PP-strategy could significantly improve"; "which may lead to skepticism from field workers"
- intend / speculative / conclusion: "in our future work, we intend to extend the current research"

## Cross-section linkers

- introduction → method: 编号贡献后直接 `II. PERFORMANCE DRIVEN DISTILLATION`，无独立路标句 (p.3)
- distillation → pseudo-label: 区间预测器段落后接 `III. PSEUDO LABEL CONFIDENCE EVALUATION` (p.5)
- method → experiments: PP-strategy 流程图后接 `IV. INDUSTRIAL APPLICATIONS` (p.6)
- experiments → conclusion: 误差箱线图讨论后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `this article first proposes` / `a semi-supervised soft-sensor framework is proposed`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有方法按 feature-construction / pseudo-label 两类写在引言中段。
- R003 贡献用 `The main contributions of this article are as follows.` + 编号列表。
- R004 Experiments 标题为 `INDUSTRIAL APPLICATIONS`。
- R005 Conclusion 先 `This article proposed`，再用 `Although` 承认局限，`in our future work, we intend to` 指向后续。

## Candidate phrases

- `To address these challenges, this article first proposes` (abstract)
- `The main contributions of this article are as follows.` (introduction)
- `In this section, the proposed PP-strategy is validated on` (experiments)
- `This article proposed a novel method named PP-strategy` (conclusion)
- `Although PP-strategy achieved notable performance` (conclusion)
- `in our future work, we intend to extend the current research` (conclusion)

## House style

自称是 `this article proposes` / `this article` / `we named the framework` / `our future work`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。结论用过去时 `This article proposed`。

## Quotes

- p.1 abstract: In industrial soft-sensor applications, labeled samples are often scarce and unable to fully represent the dynamic changes in industrial processes.
- p.1 abstract: Although semi-supervised methods offer a potential solution to this issue, existing feature-construction-based methods cannot ensure the effectiveness of the feature, and pseudo-label-based methods lack an established confidence evaluation standard.
- p.1 abstract: To address these challenges, this article first proposes a novel performance-driven distillation strategy, which designs an innovative siameseLSTM structure for training multiple teacher models.
- p.1 abstract: Compared with some existing advanced soft sensor frameworks, the prediction results on different datasets show that the root-mean-square error (RMSE) and mean absolute error (MAE) are reduced by an average of 10.76% and 11.18%, respectively, while the correlation coefficient (R2) is averagely increased by 0.1203.
- p.1 introduction: WITH the increasing automation in industrial processes, real-time measurement of quality variables is crucial for timely control and optimization, promoting stable and sustained operations [1], [2].
- p.2 introduction: Nevertheless, both types of methods face significant bottlenecks, which limit the application of semi-supervised methods in industrial process soft sensing.
- p.2 introduction: Inspired by the inherent issues in existing semi-supervised soft sensing modeling methods, this article proposes an innovative performance-driven distillation strategy and a pseudo label confidence evaluation strategy for semi-supervised industrial soft-sensor applications.
- p.2 introduction: The main contributions of this article are as follows.
- p.3 method: It is common knowledge that industrial production processes change slowly, and the key variables exhibit complex spatiotemporal coupling relationships.
- p.5 method: III. PSEUDO LABEL CONFIDENCE EVALUATION
- p.6 experiments: In this section, the proposed PP-strategy is validated on a real alumina evaporation production process datasets and a real alumina digestion production process datasets.
- p.9 experiments: First, under the same ratio of labeled to unlabeled data, the PP-strategy achieves the lowest RMSE and MAE and the highest R2.
- p.11 conclusion: This article proposed a novel method named PP-strategy for soft sensor of industrial quality variables.
- p.11 conclusion: The experimental results demonstrated that the PP-strategy could significantly improve soft sensor performance and outperforms existing comparison methods.
- p.11 conclusion: Although PP-strategy achieved notable performance and provides solutions to two major challenges in semi-supervised soft sensor, there are still some limitations.
- p.11 conclusion: Taking these factors into account, in our future work, we intend to extend the current research in the following directions:
