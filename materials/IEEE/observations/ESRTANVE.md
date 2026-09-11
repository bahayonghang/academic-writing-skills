---
key: ESRTANVE
title: "Multiscale Modeling Using GAN and Deep Forest Regression With Application to Dioxin Emission Soft Sensor"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2023.3309389"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. SHORT TIME-SCALE MISSING DATA FILLING USING GAN` → `III. LONG TIME-SCALE SOFT SENSOR MODELING USING IDFR` → `IV. DXN EMISSION SOFT SENSOR MODELING BASED ON ACTUAL INDUSTRIAL PROCESS USING MULTISCALE DATA` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 DL 软测量、RF/DF/DFR、缺失填充统计/VAE/GAN、多时间尺度）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为工业过程案例名。

## Openers

- abstract: `Dioxin (DXN) emission` — "Dioxin (DXN) emission concentration is a key environmental index in the process of municipal solid waste incineration (MSWI)." (p.1)
- introduction: `AT PRESENT, it` — "AT PRESENT, it is necessary to measure and analyze the key operational indexes that relates to the high requirement of complex industrial processes and environmental protection [1]." (p.1；栏首掉字)
- method: `The two modules` — "The two modules used to fill short time-scale missing data are the missing data division module and adversarial generative data filling module." (p.2, II)
- experiments: `The proposed improved` — "The proposed improved GAN-DFR DXN soft sensor for multiscale missing data consists of four modules, namely, missing data division, adversarial generative data filling, input and output data matching, and IDFR modules." (p.7, IV.A)
- conclusion: `This study introduces` — "This study introduces multiscale missing data modeling using an improved GAN-DFR for DXN emission soft sensor modeling." (p.11)

## Gap transitions

- however (abstract): "However, data on the MSWI process have missing and abnormal values, which lead to incomplete data used for modeling." (p.1)
- therefore (abstract): "Therefore, DXN emission soft sensor modeling has to tackle problems, such as missing data, data scale mismatch, and small samples." (p.1)
- however (introduction): "However, some indexes (e.g., production parameters and environmental indicators) are difficult to measure directly because of complex technology and high cost [2]." (p.1)
- however (introduction): "However, DXN modeling data have the problem of small samples and missing values, and the collected input features cannot match DXN emission concentration data directly owing to different measurement methods." (p.1)
- to address (introduction): "To address these issues, an improved GAN-DFR soft sensor modeling method is proposed in this study." (p.2)

## Hedge verbs

- proposes / causal / abstract, introduction: "This study proposes a multiscale missing data modeling"; "an improved GAN-DFR soft sensor modeling method is proposed in this study"
- introduces / causal / conclusion: "This study introduces multiscale missing data modeling"
- are verified / causal / abstract: "The effectiveness and rationality of the proposed method are verified on the real DXN dataset."
- should be improved / speculative / experiments: "the fitting performance of the proposed method should be improved further"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. In Sections II and III, the functions of multiscale missing data filling using GAN and soft sensor modeling using IDFR are, respectively, given in detail. In Section IV, the strategy of the algorithm and the simulation result based on the DXN dataset from the actual MSWI process are shown and the hyperparameters are compared. In Section V, the conclusions are summarized." (p.2)
- method → experiments: Algorithm 2 后 `IV. DXN EMISSION SOFT SENSOR MODELING BASED ON ACTUAL INDUSTRIAL PROCESS USING MULTISCALE DATA` (p.7)
- experiments → conclusion: 消融 Table XII 后 `V. CONCLUSION` (p.11)

## Candidate rules

- R002 Introduction 无独立 Related Work，小样本 ensemble / 缺失填充 / 多尺度评述写在引言中段，并以 `To address these issues` 收束。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this work are listed as follows` + 编号动名词条目。
- R005 摘要与结论自称 `This study`；路标仍用 `this article`。

## Candidate phrases

- `This study proposes a multiscale` (abstract)
- `To address these issues, an improved ... method is proposed in this study` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This study introduces multiscale missing data modeling` (conclusion)

## House style

自称混用 `This study`（摘要/贡献/结论）与 `this article`（路标）。未见 `Here we`、`In this paper`。`This study proposes` 与 `This study introduces` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Dioxin (DXN) emission concentration is a key environmental index in the process of municipal solid waste incineration (MSWI).
- p.1 abstract: However, data on the MSWI process have missing and abnormal values, which lead to incomplete data used for modeling.
- p.1 abstract: Therefore, DXN emission soft sensor modeling has to tackle problems, such as missing data, data scale mismatch, and small samples.
- p.1 abstract: This study proposes a multiscale missing data modeling using improved generative adversarial network (IGAN) and deep forest regression (DFR) to address the abovementioned problems.
- p.1 abstract: The effectiveness and rationality of the proposed method are verified on the real DXN dataset.
- p.1 introduction: AT PRESENT, it is necessary to measure and analyze the key operational indexes that relates to the high requirement of complex industrial processes and environmental protection [1].
- p.1 introduction: However, some indexes (e.g., production parameters and environmental indicators) are difficult to measure directly because of complex technology and high cost [2].
- p.1 introduction: However, DXN modeling data have the problem of small samples and missing values, and the collected input features cannot match DXN emission concentration data directly owing to different measurement methods.
- p.2 introduction: To address these issues, an improved GAN-DFR soft sensor modeling method is proposed in this study.
- p.2 introduction: The main contributions of this work are listed as follows.
- p.2 introduction: The rest of this article is organized as follows. In Sections II and III, the functions of multiscale missing data filling using GAN and soft sensor modeling using IDFR are, respectively, given in detail. In Section IV, the strategy of the algorithm and the simulation result based on the DXN dataset from the actual MSWI process are shown and the hyperparameters are compared. In Section V, the conclusions are summarized.
- p.2 method: The two modules used to fill short time-scale missing data are the missing data division module and adversarial generative data filling module.
- p.4 method: The two modules used to build the soft sensor model are the input and output data matching module and the IDFR module.
- p.7 experiments: The proposed improved GAN-DFR DXN soft sensor for multiscale missing data consists of four modules, namely, missing data division, adversarial generative data filling, input and output data matching, and IDFR modules.
- p.7 experiments: In this study, the proposed method is applied in the MSWI process to verify its effectiveness.
- p.11 conclusion: This study introduces multiscale missing data modeling using an improved GAN-DFR for DXN emission soft sensor modeling.
