---
key: IK9XSCLW
title: "Gaussian mixture TimeVAE for industrial soft sensing with deep time series decomposition and generation"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2024.103355"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries` → `3. Methodology` → `4. Case studies` → `5. Conclusions and future work`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 PCA/SVM、AE/VAE、GMVAE、TimeVAE 与数据增强）。Introduction 末有编号贡献 + 节序路标。Method 前有 Preliminaries。Experiments 标题为 `Case studies`。

## Openers

- abstract: `Most industrial process` — "Most industrial process data is time series data and contains multi-mode characteristics, which poses difficulties and challenges in the establishment of soft sensing models."
- introduction: `As the industrial` — "As the industrial technology advances by leaps and bounds, monitoring of the production process is increasingly being emphasized."
- method: `In order to` — "In order to handle time series data, enhance the complexity of latent variable representation, and decompose temporal information, a GM-TSD model is proposed." (s.3)
- experiments: `This section applies` — "This section applies the soft sensors based on the GM-TSD and the GM-TSD-Gen model to a primary reformer process and a CO2 absorption column for the quality variable prediction to demonstrate the effectiveness."
- conclusion: `In this paper` — "In this paper, a GM-TSD model is proposed, which incorporates Gaussian mixture distributions into the latent space and decouples the latent variables using a time series decomposition approach."

## Gap transitions

- to address (abstract): "To address these issues, this paper proposes a Gaussian mixture based time series decomposition model."
- however (introduction): "However, in industrial processes, complex operating modes arise due to various factors such as production environmental changes, raw material variations, and shifts in production requirements [16]."
- considering (introduction): "Considering the issues mentioned above, this paper takes both the multi-mode feature and time series data into consideration and proposes a Gaussian mixture based time series decomposition (GM-TSD) model."
- furthermore (abstract): "Furthermore, to tackle the problem of poor fitting in peak or extreme data due to information imbalance, it generates virtual time series data."

## Hedge verbs

- propose / causal / abstract, introduction: "this paper proposes a Gaussian mixture based time series decomposition model"; "proposes a Gaussian mixture based time series decomposition (GM-TSD) model"
- show / associative / abstract: "The experimental results show that the proposed models have superior predictive performance compared to other state-of-the-art methods."
- demonstrate / causal / experiments, conclusion: "to demonstrate the effectiveness"; "Experiments on two industrial cases demonstrate that the proposed models can significantly improve the soft sensing performance"

## Cross-section linkers

- introduction → method: "The layout of this paper is organized as follows. In Section 2, the preliminaries on time series analysis and GMVAE are introduced. Section 3 proposes a Gaussian mixture based time series decomposition (GM-TSD) model for soft modeling. Then, a Gaussian mixture based time series decomposition and generation (GM-TSD-Gen) model is proposed. Section 4 utilizes two cases to verify the proposed models. Finally, conclusions are given in Section 5."
- method → experiments: 软传感器指标段落后 `4. Case studies`
- experiments → conclusion: CO2 吸收塔结果后 `5. Conclusions and future work`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The layout of this paper is organized as follows`
- R004 编号贡献：`The main contributions of this paper can be summarized as follows`
- R009 自称：`this paper proposes` / `In this paper, a GM-TSD model is proposed`

## Candidate phrases

- `To address these issues, this paper proposes` (abstract)
- `Considering the issues mentioned above, this paper ... proposes` (introduction)
- `The main contributions of this paper can be summarized as follows` (introduction)
- `The layout of this paper is organized as follows` (introduction)
- `In this paper, a GM-TSD model is proposed` (conclusion)

## House style

自称 `this paper proposes` / `In this paper, a GM-TSD model is proposed` / `the proposed models`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Most industrial process data is time series data and contains multi-mode characteristics, which poses difficulties and challenges in the establishment of soft sensing models.
- abstract: To address these issues, this paper proposes a Gaussian mixture based time series decomposition model.
- abstract: The experimental results show that the proposed models have superior predictive performance compared to other state-of-the-art methods.
- introduction: As the industrial technology advances by leaps and bounds, monitoring of the production process is increasingly being emphasized.
- introduction: However, in industrial processes, complex operating modes arise due to various factors such as production environmental changes, raw material variations, and shifts in production requirements [16].
- introduction: Considering the issues mentioned above, this paper takes both the multi-mode feature and time series data into consideration and proposes a Gaussian mixture based time series decomposition (GM-TSD) model.
- introduction: The layout of this paper is organized as follows.
- method: In order to handle time series data, enhance the complexity of latent variable representation, and decompose temporal information, a GM-TSD model is proposed.
- experiments: This section applies the soft sensors based on the GM-TSD and the GM-TSD-Gen model to a primary reformer process and a CO2 absorption column for the quality variable prediction to demonstrate the effectiveness.
- experiments: The Primary Reformer (PR) process is an integral component of hydrogen manufacturing units in the Ammonia Synthesis process [7].
- conclusion: In this paper, a GM-TSD model is proposed, which incorporates Gaussian mixture distributions into the latent space and decouples the latent variables using a time series decomposition approach.
- conclusion: Experiments on two industrial cases demonstrate that the proposed models can significantly improve the soft sensing performance compared with several other VAE based models.
