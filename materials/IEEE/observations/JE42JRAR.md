---
key: JE42JRAR
title: "A Graph-Based Time–Frequency Two-Stream Network for Multistep Prediction of Key Performance Indicators in Industrial Processes"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2024.3447108"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM DEFINITION` → `III. METHODOLOGY` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 AE/RNN/GNN 软测量、ARIMA/VAR、DSTED，再列 Challenge 1–2）。Introduction 末有节序路标，指向 Section II–V。Method 在 `III. METHODOLOGY`。Experiments 标题为 `CASE STUDIES`（垃圾焚烧 + SDS 脱硫）。

## Openers

- abstract: `Deep learning-based` — "Deep learning-based soft sensor modeling methods have been extensively studied and applied to industrial processes in the last decade." (p.1)
- introduction: `ACCURATE estimation of` — "ACCURATE estimation of key performance indicators (KPIs) in industrial processes is of great significance for intelligent manufacturing [1]." (p.1；栏首掉字)
- method: `As shown in` — "As shown in Fig. 1, GTFTS consists of three key modules: 1) multigraph attention layer; 2) two-stream network; and 3) time–frequency feature fusion module." (p.3, III)
- experiments: `In this section` — "In this section, in order to evaluate the effectiveness and generality of the proposed model, we have conducted comprehensive experiments on two real-world industrial cases." (p.8, IV)
- conclusion: `In this article` — "In this article, we propose a time–frequency two-stream network to achieve the multistep prediction of KPIs in industrial processes." (p.13)

## Gap transitions

- however (abstract): "However, existing soft sensor models mainly focus on the current step prediction in real time and ignore the multistep prediction in advance." (p.1)
- however (introduction): "However, these studies focus exclusively on the soft sensor modeling of the current step." (p.1)
- although (introduction): "Although DSTED considered the correlations between the latent variables and the target variable, it overlooked the complex spatial coupling relationships between process variables." (p.2)
- therefore (introduction): "Therefore, an accurate multistep prediction framework is indispensable for the early warning and deployment of actual industrial applications." (p.2)
- in view of (introduction): "In view of these theoretical challenges and real-world industrial needs, in this article, we attempt to go beyond previous time-domain modeling and propose a graph-based time–frequency two-stream network (GTFTS)" (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "in this article, we propose a graph-based time–frequency two-stream network"; "we propose a two-stream network framework"
- show / causal / abstract, experiments: "extensive experiments on two real-world industrial datasets show that the proposed multistep prediction model outperforms the state-of-the-art models"
- demonstrate / causal / introduction: "extensive result analysis and discussion on two real-world datasets demonstrate the superiority and feasibility of our GTFTS model"
- indicate / speculative / experiments: "These results indicate that all the modules are necessary for GTFTS."
- conjecture / speculative / experiments: "We conjecture that there exists some noise contamination in the SDS desulphurization process data"

## Cross-section linkers

- introduction → method: "The remainder of this article is structured as follows. Section II gives the problem definition, and Section III presents the details of the proposed multistep prediction model. In Section IV, we conduct a series of experiments on two industrial cases and compare prediction results of different methods. Finally, we conclude this article in Section V." (p.3)
- method → experiments: 理论分析段落后直接 `IV. CASE STUDIES` (p.8)
- experiments → conclusion: 现场部署与响应时间段落后直接 `V. CONCLUSION` (p.13)

## Candidate rules

- R001 abstract 贡献句用 `in this article, we propose` + 方法全称，再用 `Specifically` / `Furthermore` / `Finally` 铺开模块。
- R002 Introduction 无独立 Related Work，先评软测量再评多步预测，末用编号 `Challenge 1` / `Challenge 2`。
- R003 贡献列表标题用 `The contributions of this article are summarized in three-fold.`，条目用名词短语（`Time–Frequency Joint Framework`）。
- R004 Introduction 末用 `The remainder of this article is structured as follows` 指向 II–V。
- R005 Conclusion 先收回方法三模块，再用 `In the future, we plan to` 指向专家知识与 STFT 频谱泄漏。

## Candidate phrases

- `in this article, we propose` (abstract)
- `To ravel out these two problems` (abstract)
- `The contributions of this article are summarized in three-fold.` (introduction)
- `The remainder of this article is structured as follows.` (introduction)
- `In the future, we plan to incorporate expert knowledge into` (conclusion)

## House style

自称是 `in this article` / `we propose` / `Our main aim` / `the proposed method` / `our GTFTS`。未见 `Here we`。`In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Deep learning-based soft sensor modeling methods have been extensively studied and applied to industrial processes in the last decade.
- p.1 abstract: However, existing soft sensor models mainly focus on the current step prediction in real time and ignore the multistep prediction in advance.
- p.1 abstract: To ravel out these two problems, in this article, we propose a graph-based time–frequency two-stream network to achieve multistep prediction.
- p.1 introduction: ACCURATE estimation of key performance indicators (KPIs) in industrial processes is of great significance for intelligent manufacturing [1].
- p.1 introduction: However, these studies focus exclusively on the soft sensor modeling of the current step.
- p.2 introduction: Although DSTED considered the correlations between the latent variables and the target variable, it overlooked the complex spatial coupling relationships between process variables.
- p.2 introduction: Therefore, an accurate multistep prediction framework is indispensable for the early warning and deployment of actual industrial applications.
- p.2 introduction: In view of these theoretical challenges and real-world industrial needs, in this article, we attempt to go beyond previous time-domain modeling and propose a graph-based time–frequency two-stream network (GTFTS) to model industrial data from time–frequency domains for KPIs multistep prediction.
- p.2 introduction: The contributions of this article are summarized in three-fold.
- p.3 introduction: The remainder of this article is structured as follows. Section II gives the problem definition, and Section III presents the details of the proposed multistep prediction model. In Section IV, we conduct a series of experiments on two industrial cases and compare prediction results of different methods. Finally, we conclude this article in Section V.
- p.3 method: As shown in Fig. 1, GTFTS consists of three key modules: 1) multigraph attention layer; 2) two-stream network; and 3) time–frequency feature fusion module.
- p.8 experiments: In this section, in order to evaluate the effectiveness and generality of the proposed model, we have conducted comprehensive experiments on two real-world industrial cases.
- p.8 experiments: Overall, we can observe that our proposed GTFTS model achieves the best performance in terms of all evaluation metrics among all methods.
- p.10 experiments: These results indicate that all the modules are necessary for GTFTS.
- p.12 experiments: We conjecture that there exists some noise contamination in the SDS desulphurization process data, and the DSTED model is able to use its denoising method to alleviate the disturbance of random noises.
- p.13 conclusion: In this article, we propose a time–frequency two-stream network to achieve the multistep prediction of KPIs in industrial processes.
- p.13–14 conclusion: We validate the proposed method on two industrial cases, and the results verify its effectiveness and feasibility.
- p.14 conclusion: In the future, we plan to incorporate expert knowledge into the deep learning model, improving the interpretability of industrial process modeling.
