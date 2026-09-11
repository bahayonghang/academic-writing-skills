---
key: VKY8J22K
title: "CoUDA: Continual Unsupervised Domain Adaptation for Industrial Fault Diagnosis Under Dynamic Working Conditions"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3538135"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（`II. RELATED WORK`，下分 UDA / Metric and Representation Learning / Continual UDA）。Introduction 末有节序路标，指向 Section II–V。Method 标题为 `METHODOLOGY`。Experiments 标题为 `EXPERIMENTS`。

## Openers

- abstract: `Unsupervised domain adaptation` — "Unsupervised domain adaptation (UDA) has recently gained attention in fault diagnosis due to its ability to address domain shift problems arising from changes in working conditions." (p.4072)
- introduction: `Intelligent fault diagnosis` — "Intelligent fault diagnosis is crucial for ensuring the safety and reliability of industries [1]." (p.4072)
- related_work: `In the field` — "In the field of fault diagnosis, UDA has been widely used to address domain shift problems." (p.4073)
- method: `The definition of` — "The definition of the continual domain shift problem in industrial fault diagnosis is first introduced." (p.4074, III.A)
- experiments: `The Shandong University` — "The Shandong University of Science and Technology (SDUST) dataset [27] with various working conditions is adopted to verify the superiority of the proposed CoUDA framework." (p.4078)
- conclusion: `In this study` — "In this study, we propose a novel continual UDA framework, CoUDA, for fault diagnosis under dynamic working conditions from the perspective of metric and representation learning." (p.4081)

## Gap transitions

- however (abstract): "However, when faced with the continual domain shift problem inherent in real-world industries with dynamic working conditions, UDA often suffers from catastrophic forgetting." (p.4072)
- to address (abstract): "To address this challenge, we propose a novel replay-free continual UDA framework, CoUDA, for fault diagnosis under dynamic working conditions." (p.4072)
- unfortunately (introduction): "Unfortunately, the replay mechanism does not strictly uphold the privacy of the historical data, and thus may produce more serious data privacy issues." (p.4073)
- to address (introduction): "To address the above challenges, this work proposes a novel continual UDA framework, CoUDA, for industrial fault diagnosis under dynamic working conditions." (p.4073)
- in contrast (related_work): "In contrast, we adhere to stricter privacy constraints and propose a novel CoUDA framework without replay, namely, CoUDA, to achieve fault diagnosis under dynamic working conditions." (p.4074)

## Hedge verbs

- propose / causal / abstract, introduction, related_work, conclusion: "we propose a novel replay-free continual UDA framework, CoUDA"; "this work proposes a novel continual UDA framework, CoUDA"; "In this study, we propose"
- demonstrate / causal / abstract, experiments, conclusion: "Experimental results demonstrate the superiority of the proposed CoUDA"; "The experimental results on the SDUST dataset, across six domain scenarios, demonstrate that CoUDA has outstanding performance"
- show / causal / experiments: "As shown in Table VIII, the storage memory of CoUDA is 8.52 M, which is lower than that of all baseline methods."
- may / speculative / introduction: "Unfortunately, the replay mechanism does not strictly uphold the privacy of the historical data, and thus may produce more serious data privacy issues."

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. Section II reviews the related studies. Section III presents the details of the proposed CoUDA. Section IV provides the case studies and experimental results analysis. Finally, Section V concludes this article." (p.4073)
- related_work → method: 综述对比后 `III. METHODOLOGY` (p.4074)
- method → experiments: 损失与算法说明后 `IV. EXPERIMENTS` (p.4078)
- experiments → conclusion: 计算复杂度后直接 `V. CONCLUSION` (p.4081)

## Candidate rules

- R006 独立 Related Work：`II. RELATED WORK` 紧接 Introduction。
- R001 摘要缺口后用 `To address this challenge, we propose`。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this work can be summarized as follows` + 编号列表。
- R005 结论用 `Therefore, exploring ... will be an important research direction in the future`。

## Candidate phrases

- `To address this challenge, we propose` (abstract)
- `To address the above challenges, this work proposes` (introduction)
- `The main contributions of this work can be summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this study, we propose` (conclusion)
- `exploring other optimization strategies to reduce the training time will be an important research direction in the future` (conclusion)

## House style

自称是 `we propose` / `this work proposes` / `In this study, we propose`。未见 `Here we`、`In this paper`。`we propose` 与 `In this study` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.4072 abstract: Unsupervised domain adaptation (UDA) has recently gained attention in fault diagnosis due to its ability to address domain shift problems arising from changes in working conditions.
- p.4072 abstract: However, when faced with the continual domain shift problem inherent in real-world industries with dynamic working conditions, UDA often suffers from catastrophic forgetting.
- p.4072 abstract: To address this challenge, we propose a novel replay-free continual UDA framework, CoUDA, for fault diagnosis under dynamic working conditions.
- p.4072 abstract: Experimental results demonstrate the superiority of the proposed CoUDA in achieving robust fault diagnosis under dynamic working conditions.
- p.4072 introduction: Intelligent fault diagnosis is crucial for ensuring the safety and reliability of industries [1].
- p.4073 introduction: Unfortunately, the replay mechanism does not strictly uphold the privacy of the historical data, and thus may produce more serious data privacy issues.
- p.4073 introduction: To address the above challenges, this work proposes a novel continual UDA framework, CoUDA, for industrial fault diagnosis under dynamic working conditions.
- p.4073 introduction: The main contributions of this work can be summarized as follows.
- p.4073 introduction: The rest of this article is organized as follows. Section II reviews the related studies. Section III presents the details of the proposed CoUDA. Section IV provides the case studies and experimental results analysis. Finally, Section V concludes this article.
- p.4073 related_work: In the field of fault diagnosis, UDA has been widely used to address domain shift problems.
- p.4074 related_work: In contrast, we adhere to stricter privacy constraints and propose a novel CoUDA framework without replay, namely, CoUDA, to achieve fault diagnosis under dynamic working conditions.
- p.4074 method: The definition of the continual domain shift problem in industrial fault diagnosis is first introduced.
- p.4078 experiments: The Shandong University of Science and Technology (SDUST) dataset [27] with various working conditions is adopted to verify the superiority of the proposed CoUDA framework.
- p.4079 experiments: The proposed CoUDA has demonstrated state-of-the-art performance, achieving the highest ACC, AAD, and BWT across all six domain scenarios.
- p.4081 conclusion: In this study, we propose a novel continual UDA framework, CoUDA, for fault diagnosis under dynamic working conditions from the perspective of metric and representation learning.
- p.4081 conclusion: The experimental results on the SDUST dataset, across six domain scenarios, demonstrate that CoUDA has outstanding performance in continual UDA for fault diagnosis tasks.
- p.4081 conclusion: Therefore, exploring other optimization strategies to reduce the training time will be an important research direction in the future.
