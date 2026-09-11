---
key: AK72N6XT
title: "FIGAN: a missing industrial data imputation method customized for soft sensor application"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2021.3132037"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。独立 Related Work。`related_work=independent`（II.A 工业缺失填补，II.B GAIN）。Introduction 末用 `The remainder of the paper is organized as follows` 路标，指向 Section II–V。Method 分问题陈述、结构、损失函数、训练流程。Experiments 分 Task #1 / Task #2，案例为转炉炼钢与青霉素发酵。

## Openers

- abstract: `Missing data is` — "Missing data is quite common in the industrial field, resulting in problems in downstream applications, as most data driven methods used in these applications rely on complete and high-quality dataset to build a high-quality model." (p.1)
- introduction: `MISSING data is` — "MISSING data is a fundamental problem in industrial field." (p.1；栏首掉字)
- method: `In this section` — "In this section, the necessity of this study is analyzed first." (p.3, III)
- experiments: `Our experiments involve` — "Our experiments involve two tasks." (p.7, IV)
- conclusion: `This paper proposes` — "This paper proposes FIGAN, a customized data imputation method for industrial soft sensor." (p.10)

## Gap transitions

- therefore (introduction): "Therefore, current methods cope with missing data first and then handle the downstream applications." (p.1)
- however (introduction): "However, they require complete data in the training process." (p.2)
- however (introduction): "However, the soft sensor introduced brings about a problem which existing MDI methods don't encounter." (p.2)
- but (introduction): "But performance in terms of reconstruction of missing data might not be a perfect proxy for the accuracy of the downstream model." (p.2)
- however (related work): "However, few research has been reported." (p.2)
- but (related work): "But in these methods, the data imputation process still receives no feedback from the downstream task for further improvement." (p.2)

## Hedge verbs

- design / causal / abstract: "a new method termed fine-tuned imputation GAN (FIGAN) is designed"
- propose / causal / introduction, conclusion: "A fine-tuned imputation GAN (FIGAN) for industrial soft sensing with missing data is proposed in this paper"; "This paper proposes FIGAN"
- show / causal / abstract, experiments: "Case studies on a converter steelmaking process and a penicillin fermentation process show the feasibility of the proposed FIGAN"; "The results in Table VI show that FIGAN outperforms other three models"
- would be / speculative / abstract: "Enhanced accuracy for the final industrial soft sensor would be possible"
- noted / causal / conclusion: "It is noted that such customization can be readily transferred to other downstream applications"

## Cross-section linkers

- introduction → related work: "The remainder of the paper is organized as follows. Section II provides a brief introduction to the related work. Section III presents the proposed FIGAN, followed by case studies on a converter steelmaking process and a penicillin fermentation process in Section IV. Lastly, conclusions and future works are given in Section V." (p.2)
- related work → method: GAIN 结构说明后 `III. METHODOLOGY` (p.3)
- method → experiments: 训练流程后 `IV. EXPERIMENTS` (p.7)
- experiments → conclusion: 伪标签结果后 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 TASE 可前置 `Note to Practitioners—`，practitioner 段用 `The focus of this study is to develop`。
- R002 独立 Related Work，再进入 `III. METHODOLOGY`。
- R003 Introduction 末用 `The remainder of the paper is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions are summarized as below:` + 编号。
- R005 Conclusion 用 `This paper proposes` 收回，再用 `It is noted that such customization can be readily transferred`。

## Candidate phrases

- `In this paper, a new method termed fine-tuned imputation GAN (FIGAN) is designed to` (abstract)
- `The contributions are summarized as below:` (introduction)
- `The remainder of the paper is organized as follows.` (introduction)
- `Our experiments involve two tasks.` (experiments)
- `This paper proposes FIGAN, a customized data imputation method for` (conclusion)
- `It is noted that such customization can be readily transferred to` (conclusion)

## House style

自称 `In this paper` / `this paper proposes` / `this study` / `the proposed FIGAN` / `our proposed model`。未见 `Here we`、`In this article`。`In this paper` 与 `This paper proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Missing data is quite common in the industrial field, resulting in problems in downstream applications, as most data driven methods used in these applications rely on complete and high-quality dataset to build a high-quality model.
- p.1 abstract: In this paper, a new method termed fine-tuned imputation GAN (FIGAN) is designed to achieve customized data imputation for industrial soft sensor.
- p.1 abstract: Case studies on a converter steelmaking process and a penicillin fermentation process show the feasibility of the proposed FIGAN.
- p.1 practitioners: The focus of this study is to develop a customized data imputation method for specific downstream applications such as soft sensing.
- p.1 introduction: MISSING data is a fundamental problem in industrial field.
- p.1 introduction: Therefore, current methods cope with missing data first and then handle the downstream applications.
- p.2 introduction: However, they require complete data in the training process.
- p.2 introduction: But performance in terms of reconstruction of missing data might not be a perfect proxy for the accuracy of the downstream model.
- p.2 introduction: A fine-tuned imputation GAN (FIGAN) for industrial soft sensing with missing data is proposed in this paper.
- p.2 introduction: The contributions are summarized as below:
- p.2 introduction: The remainder of the paper is organized as follows. Section II provides a brief introduction to the related work. Section III presents the proposed FIGAN, followed by case studies on a converter steelmaking process and a penicillin fermentation process in Section IV. Lastly, conclusions and future works are given in Section V.
- p.2 related work: Missing data imputation is indispensable in industrial modeling since most algorithms cannot use data with missing values directly.
- p.2 related work: But in these methods, the data imputation process still receives no feedback from the downstream task for further improvement.
- p.3 method: In this section, the necessity of this study is analyzed first.
- p.7 experiments: Our experiments involve two tasks.
- p.8 experiments: The results in Table VI show that FIGAN outperforms other three models on over half of the element compositions and on most of off-line measurements, performing the best in average.
- p.10 conclusion: This paper proposes FIGAN, a customized data imputation method for industrial soft sensor.
- p.10 conclusion: Validations on a converter steel-making dataset and a penicillin fermentation dataset show the effectiveness of FIGAN.
- p.10 conclusion: It is noted that such customization can be readily transferred to other downstream applications with missing data such as anomaly detection.
