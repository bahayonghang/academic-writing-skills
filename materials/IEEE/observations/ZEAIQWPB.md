---
key: ZEAIQWPB
title: "TimeDDPM: Time Series Augmentation Strategy for Industrial Soft Sensing"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2023.3339245"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES OF DDPM METHOD` → `III. TIMEDDPM-BASED SOFT SENSOR FRAMEWORK` → `IV.`（两案例，引言路标）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 extended vector / RNN / LSTM / TimeGAN / TimeVAE / DDPM）。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 为数值案例 + 三相流。

## Openers

- abstract: `Soft sensor modeling` — "Soft sensor modeling for dynamic processes has become a trending topic and a pending challenge in industrial data analysis, especially in limited labeled data scenarios." (p.1)
- introduction: `FOR industrial processes` — "FOR industrial processes, precise and real-time forecast of crucial quality variables is imperative to enhance product quality and ensure safe production." (p.1；栏首掉字)
- method: `In practice, it` — "In practice, it is challenging to obtain enough key variables of time-series data through offline tests." (p.3, III.A)
- experiments: `Based on the` — "Based on the expanded new training set, an LSTM soft sensor model is established to evaluate the prediction performance of the test dataset." (p.6)
- conclusion: `A dynamic data` — "A dynamic data augmentation soft sensor method called TimeDDPM is proposed for insufficient time-series data." (p.8)

## Gap transitions

- however (abstract): "However, current time-series data augmentation methods do not consider the spatiotemporal dependencies among samples during the data generation procedure." (p.1)
- to address (abstract): "To address the issue, a time-series denoising diffusion probabilistic model (TimeDDPM) is proposed to construct a soft sensor for finite time-series samples." (p.1)
- however (introduction): "However, most of them are established under steady-state conditions." (p.1)
- however (introduction): "However, these dynamic soft sensor models are trained under the assumption of sufficient training data." (p.2)
- unfortunately (introduction): "Unfortunately, the VAE-based methods necessitate the user to specify a distribution for its probabilistic process." (p.2)

## Hedge verbs

- propose / causal / abstract, conclusion: "a time-series denoising diffusion probabilistic model (TimeDDPM) is proposed"; "A dynamic data augmentation soft sensor method called TimeDDPM is proposed"
- demonstrate / causal / abstract: "Two cases are employed to demonstrate the superiorities of the proposed method"
- develop / causal / introduction: "a data-enhanced method named time-series DDPM (TimeDDPM) is developed"
- exhibit / causal / experiments: "TimeDDPM exhibits the best results between predicted values and the actual test set data"
- would / speculative / conclusion: "it would be necessary to investigate the data imputation-based augmentation models"

## Cross-section linkers

- introduction → method: "The remaining sections are structured as follows. Section II introduces the DDPM method. Section III details the implementation procedure of TimeDDPM. The outcomes of TimeDDPM on two examples are displayed in Section IV. Finally, Section V concludes the study." (p.2)
- method → experiments: III 末进入案例；IV 以数值案例与三相流展开 (p.6)
- experiments → conclusion: 三相流结果段落后直接 `V. CONCLUSION` (p.8)

## Candidate rules

- R001 abstract 先 `However` 指出现有增强忽略时空依赖，再用 `To address the issue, X is proposed`。
- R002 Introduction 无独立 Related Work，TimeGAN / TimeVAE / DDPM 评述写在引言中段。
- R003 Introduction 末用 `The remaining sections are structured as follows` 指向 II–V。
- R004 Conclusion 开篇用被动 `X is proposed for`，不用 `In this paper we`。
- R005 Conclusion 末用局限 + `it would be necessary to investigate` 指向后续。

## Candidate phrases

- `To address the issue, a ... is proposed to` (abstract)
- `Two cases are employed to demonstrate the superiorities of the proposed method` (abstract)
- `The remaining sections are structured as follows.` (introduction)
- `In this study, a data-enhanced method named` (introduction)
- `A dynamic data augmentation soft sensor method called TimeDDPM is proposed for` (conclusion)

## House style

自称是 `In this study` / `the proposed method` / `This work`。未见 `Here we`。未见 `In this paper`。`In this study` 与被动 `is proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Soft sensor modeling for dynamic processes has become a trending topic and a pending challenge in industrial data analysis, especially in limited labeled data scenarios.
- p.1 abstract: However, current time-series data augmentation methods do not consider the spatiotemporal dependencies among samples during the data generation procedure.
- p.1 abstract: To address the issue, a time-series denoising diffusion probabilistic model (TimeDDPM) is proposed to construct a soft sensor for finite time-series samples.
- p.1 abstract: Two cases are employed to demonstrate the superiorities of the proposed method in comparison to several cutting-edge methods.
- p.1 introduction: FOR industrial processes, precise and real-time forecast of crucial quality variables is imperative to enhance product quality and ensure safe production.
- p.2 introduction: However, these dynamic soft sensor models are trained under the assumption of sufficient training data.
- p.2 introduction: Unfortunately, the VAE-based methods necessitate the user to specify a distribution for its probabilistic process.
- p.2 introduction: In this study, a data-enhanced method named time-series DDPM (TimeDDPM) is developed for limited time-series samples.
- p.2 introduction: The remaining sections are structured as follows. Section II introduces the DDPM method. Section III details the implementation procedure of TimeDDPM. The outcomes of TimeDDPM on two examples are displayed in Section IV. Finally, Section V concludes the study.
- p.3 method: In practice, it is challenging to obtain enough key variables of time-series data through offline tests.
- p.6 experiments: Based on the expanded new training set, an LSTM soft sensor model is established to evaluate the prediction performance of the test dataset.
- p.6 experiments: From Fig. 5, TimeDDPM exhibits the best results between predicted values and the actual test set data.
- p.8 conclusion: A dynamic data augmentation soft sensor method called TimeDDPM is proposed for insufficient time-series data.
- p.8 conclusion: The prediction results of a numerical example and an industrial three-phase flow process demonstrate the advantages of TimeDDPM.
- p.8 conclusion: This work only utilizes limited labeled time-series samples for data augmentation.
- p.8 conclusion: In addition, due to the common phenomenon of missing quality variables, it would be necessary to investigate the data imputation-based augmentation models.
