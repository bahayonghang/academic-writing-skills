---
key: 52JUWBYN
title: "Regularized Decoupling Transformer-Based Variable Selection and Soft Sensor Modeling for Fermentation Processes"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3562969"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. REGULARIZED DECOUPLING TRANSFORMER-BASED SOFT SENSOR MODELING` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `ABBREVIATIONS`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLS/PCR/SVR、CNN/RNN 与 TF 软测量）。`II. PRELIMINARIES` 铺 Transformer 位置编码与多头注意力。Introduction 末有节序路标，指向 Section 2–5。Method 在 III。Experiments 标题为 `CASE STUDIES`（青霉素仿真 / 真实青霉素 / 红霉素）。作者稿页码 1–14。

## Openers

- abstract: `Soft sensor modeling` — "Soft sensor modeling of fermentation processes is crucial to enhance yield and quality." (p.1)
- introduction: `Fermentation processes are` — "Fermentation processes are essential in modern food, pharmaceutical, chemical, and other industries." (p.1；栏首掉字 F)
- method: `In the field` — "In the field of industrial process control and quality prediction, product quality indicators are often associated with multiple process variables (such as temperature, pressure, flow rate, etc.)." (p.4, III)
- experiments: `The proposed RDTF` — "The proposed RDTF model's effectiveness in soft sensing across industrial fermentation processes, including simulated and real penicillin production scenarios and a real erythromycin production process, is evaluated." (p.6, IV)
- conclusion: `This study proposes` — "This study proposes a novel variable selection and soft sensor modeling method based on RDTF to address the nonlinear and dynamic characteristics in fermentation processes and mitigate information redundancy between variables." (p.12)

## Gap transitions

- however (abstract): "Soft sensor modeling of fermentation processes is crucial to enhance yield and quality. However, the nonlinear and dynamic characteristics of these processes, coupled with variable redundancy, often degrade model performance." (p.1)
- however (introduction): "However, CNN and RNN frameworks cannot manage long-term dependencies." (p.2)
- however (introduction): "However, directly using latent variables outputted by the TF model for regression may lead to skewed latent variables, collinearity, and redundancy within these variables, thereby diminishing the quality of information and weakening the performance of the soft sensing model." (p.2)
- to address (abstract/introduction): "A variable selection and soft sensor modeling scheme based on regularized decoupling Transformer (RDTF) is proposed in this study to address these issues." (p.1); "To address these issues, this study proposes a variable selection and soft sensor modeling scheme based on regularized decoupling Transformer (RDTF)." (p.2)
- future (conclusion): "Future research can integrate known process mechanism information with data-driven network models to develop accurate and robust soft sensor models." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "is proposed in this study"; "this study proposes a variable selection and soft sensor modeling scheme"; "This study proposes a novel variable selection and soft sensor modeling method"
- verify / causal / abstract, introduction: "the effectiveness of the proposed RDTF is verified through a simulated penicillin fermentation process case"
- demonstrate / causal / introduction, experiments, conclusion: "The potential of the proposed scheme in industrial applications is demonstrated"; "The results demonstrate that the proposed RDTF model surpasses the other models"; "The results demonstrate that the RDTF-based modeling scheme achieves superior predictive accuracy"
- show / causal / experiments: "As shown in Table II, the results of different evaluation metrics indicate"

## Cross-section linkers

- introduction → later sections: "The structure of this study is as follows: A brief overview of TF technology is illustrated in Section 2. In Section 3, the fermentation process soft sensing model using RDTF is elucidated. The proposed RDTF model is applied a simulated penicillin fermentation process case and real penicillin and erythromycin production cases in Section 4. The conclusions are presented in Section 5." (p.3)
- preliminaries → method: Preliminaries 末接 `III. REGULARIZED DECOUPLING TRANSFORMER-BASED SOFT SENSOR MODELING` (p.4)
- method → experiments: 评价指标段落后直接 `IV. CASE STUDIES` (p.6)
- experiments → conclusion: 红霉素段落后直接 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 缺口用 `However` + 过程特性，贡献用 `is proposed in this study to address these issues`。
- R002 Introduction 无独立 Related Work；已有方法评述写在引言中段，`II. PRELIMINARIES` 只铺 Transformer。
- R003 Introduction 末用 `The structure of this study is as follows` 指向 Section 2–5。
- R004 贡献用 `The main contributions of this study include the following` + 编号列表。
- R005 Conclusion 用 `This study proposes` 收回方法，再用 `Future research can` 指向后续。

## Candidate phrases

- `is proposed in this study to address these issues` (abstract)
- `To address these issues, this study proposes` (introduction)
- `The main contributions of this study include the following:` (introduction)
- `The structure of this study is as follows:` (introduction)
- `These results highlight RDTF's potential for industrial applications.` (abstract)
- `Future research can integrate known process mechanism information` (conclusion)

## House style

自称是 `this study` / `we need` / `the proposed RDTF` / `the proposed method`。未见 `Here we`。`This study proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。路标用 `this study`。

## Quotes

- p.1 abstract: Soft sensor modeling of fermentation processes is crucial to enhance yield and quality.
- p.1 abstract: However, the nonlinear and dynamic characteristics of these processes, coupled with variable redundancy, often degrade model performance.
- p.1 abstract: A variable selection and soft sensor modeling scheme based on regularized decoupling Transformer (RDTF) is proposed in this study to address these issues.
- p.1 abstract: Across multiple real fermentation cases, the model achieves R2 values exceeding 0.95 and consistently outperforms existing models in terms of accuracy and stability.
- p.1 introduction: Fermentation processes are essential in modern food, pharmaceutical, chemical, and other industries.
- p.2 introduction: However, CNN and RNN frameworks cannot manage long-term dependencies.
- p.2 introduction: To address these issues, this study proposes a variable selection and soft sensor modeling scheme based on regularized decoupling Transformer (RDTF).
- p.2 introduction: The main contributions of this study include the following:
- p.3 introduction: The structure of this study is as follows: A brief overview of TF technology is illustrated in Section 2. In Section 3, the fermentation process soft sensing model using RDTF is elucidated. The proposed RDTF model is applied a simulated penicillin fermentation process case and real penicillin and erythromycin production cases in Section 4. The conclusions are presented in Section 5.
- p.4 method: In the field of industrial process control and quality prediction, product quality indicators are often associated with multiple process variables (such as temperature, pressure, flow rate, etc.).
- p.6 experiments: The proposed RDTF model's effectiveness in soft sensing across industrial fermentation processes, including simulated and real penicillin production scenarios and a real erythromycin production process, is evaluated.
- p.7 experiments: From the evaluation metrics of all models in the table, it is evident that the proposed soft sensing model RDTF substantially outperforms the other models.
- p.12 conclusion: This study proposes a novel variable selection and soft sensor modeling method based on RDTF to address the nonlinear and dynamic characteristics in fermentation processes and mitigate information redundancy between variables.
- p.12 conclusion: The results demonstrate that the RDTF-based modeling scheme achieves superior predictive accuracy with its R² values consistently exceeding 0.95 across various scenarios.
- p.12 conclusion: Future research can integrate known process mechanism information with data-driven network models to develop accurate and robust soft sensor models.
