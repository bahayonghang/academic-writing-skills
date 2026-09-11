---
key: CU3VT5NE
title: "KSLD-TNet: Key Sample Location and Distillation Transformer Network for Multistep Ahead Prediction in Industrial Processes"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2023.3336789"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. TRANSFORMER` → `III. PROPOSED TRANSFORMER NETWORK` → `IV. INDUSTRIAL APPLICATIONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR / PLSR / SVM / DBN / SAE / LSTM / Informer / LogTrans）。Introduction 末有编号贡献列表，无 `The rest of this article is organized as follows` 路标。Method 在 III。Experiments 标题为 `INDUSTRIAL APPLICATIONS`（混合钾洗涤 + 加氢裂化）。

## Openers

- abstract: `The multistep ahead` — "The multistep ahead prediction of crucial quality indicators is the cornerstone for optimizing and controlling industrial processes." (p.1)
- introduction: `INTELLIGENT and efficient` — "INTELLIGENT and efficient industrial process control relies heavily on real-time measurement of key product indicators, which in turn facilitate guide feedback adjustments [1], [2], [3]." (p.1；栏首掉字)
- method: `This section first` — "This section first describes the designed KSL strategy based on multihead attention." (p.3, III)
- experiments: `In this section` — "In this section, the proposed KSLD-TNet method is validated on two real industrial processes." (p.6, IV)
- conclusion: `In this study` — "In this study, a novel lightweight deep learning model based on KSLD-TNet is proposed, which can effectively streamline feature extraction and enhance the extraction of key sample information from the dataset." (p.10)

## Gap transitions

- however (abstract): "However, extracting historical features presents a significant obstacle in achieving this objective." (p.1)
- nevertheless (abstract): "Nevertheless, the lack of a sample simplification mechanism makes deep feature extraction difficult." (p.1)
- however (introduction): "However, these shallow methods are difficult to reflect the nonlinearity of the process." (p.2)
- however (introduction): "However, there are still plenty of issues in practical industrial applications of transformer-based methods." (p.2)
- to address (introduction): "To address the aforementioned problems, this article proposes an innovative key sample location and distillation transformer network (KSLD-TNet) for key product indicator prediction." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a novel key sample location and distillation transformer network (KSLD-TNet)"; "this article proposes an innovative"
- demonstrate / causal / abstract: "to demonstrate the effectiveness of the proposed method"
- can / speculative / introduction, conclusion: "the attention-based transformer network can improve"; "which can effectively streamline feature extraction"
- show / causal / experiments: "Fig. 7 shows the prediction curves of eight methods"
- will / speculative / conclusion: "In future research, we will consider how to use localized key samples for augmentation"

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. TRANSFORMER`，无节序路标 (p.2–3)
- method → experiments: "Generally, the better the performance of the model, the smaller their values will be." 随后 `IV. INDUSTRIAL APPLICATIONS` (p.6)
- experiments → conclusion: "To sum up, the KSLD-TNet proposed in this article performs outstanding in all aspects and has good application potential in industrial processes." 随后 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 贡献句用 `this article proposes a novel` + 方法缩写。
- R002 Introduction 无独立 Related Work，浅层/深度/transformer 评述写在引言中段。
- R003 贡献用 `the main contributions of this article are as follows` + 编号列表；引言末无组织路标。
- R004 Experiments 标题为 `INDUSTRIAL APPLICATIONS`，开篇 `the proposed X method is validated on two real industrial processes`。
- R005 Conclusion 用 `In this study` 收回方法，再用 `In future research, we will consider` 指向后续。

## Candidate phrases

- `this article proposes a novel` (abstract)
- `To address the aforementioned problems, this article proposes` (introduction)
- `the main contributions of this article are as follows.` (introduction)
- `the proposed KSLD-TNet method is validated on two real industrial processes.` (experiments)
- `In this study, a novel lightweight deep learning model based on` (conclusion)

## House style

自称是 `this article` / `In this study` / `Our proposed method` / `we will consider`。未见 `Here we`。未见 `In this paper`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The multistep ahead prediction of crucial quality indicators is the cornerstone for optimizing and controlling industrial processes.
- p.1 abstract: However, extracting historical features presents a significant obstacle in achieving this objective.
- p.1 abstract: Nevertheless, the lack of a sample simplification mechanism makes deep feature extraction difficult.
- p.1 abstract: To explore strategies to overcome these obstacles and enhance the suitability of transformer networks for effective multistep ahead prediction, this article proposes a novel key sample location and distillation transformer network (KSLD-TNet).
- p.1 abstract: Two industrial process datasets are utilized to construct extensive experiments to demonstrate the effectiveness of the proposed method.
- p.1 introduction: INTELLIGENT and efficient industrial process control relies heavily on real-time measurement of key product indicators, which in turn facilitate guide feedback adjustments [1], [2], [3].
- p.2 introduction: However, these shallow methods are difficult to reflect the nonlinearity of the process.
- p.2 introduction: However, there are still plenty of issues in practical industrial applications of transformer-based methods.
- p.2 introduction: To address the aforementioned problems, this article proposes an innovative key sample location and distillation transformer network (KSLD-TNet) for key product indicator prediction.
- p.2 introduction: Specifically, the main contributions of this article are as follows.
- p.3 method: This section first describes the designed KSL strategy based on multihead attention.
- p.6 experiments: In this section, the proposed KSLD-TNet method is validated on two real industrial processes.
- p.10 experiments: To sum up, the KSLD-TNet proposed in this article performs outstanding in all aspects and has good application potential in industrial processes.
- p.10 conclusion: In this study, a novel lightweight deep learning model based on KSLD-TNet is proposed, which can effectively streamline feature extraction and enhance the extraction of key sample information from the dataset.
- p.10 conclusion: Two real industrial datasets have demonstrated the superior performance of the proposed prediction framework.
- p.10 conclusion: In future research, we will consider how to use localized key samples for augmentation to enhance model performance in the context of small sample data.
