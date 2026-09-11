---
key: MZF6DDE8
title: "Time Evidence Fusion Network: Multi-Source View in Long-Term Time Series Forecasting"
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence"
doi: "10.1109/TPAMI.2025.3596905"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,12-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III`（架构，无单独罗马数字小节标题出现在摘录首页；正文按 A–E 展开 Normalization / Time Dimension Projection / BPA / Expectation Fusion / Comparison）→ `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（II，含 A. Dempster-Shafer Theory 等）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `IV. EXPERIMENTS`。PDF 页眉仍为 `JOURNAL OF LATEX CLASS FILES`（作者稿）。

## Openers

- abstract: `In practical scenarios` — "In practical scenarios, time series forecasting necessitates not only accuracy but also efficiency." (p.1)
- introduction: `THE evolution of` — "THE evolution of various phenomena is inherently tied to the progression of time, leading to an increasing prevalence of time series data in a multitude of application domains [1], such as medical diagnosis [2]–[4], education [5], weather [6], [7], power system [8], and so on [9]–[11]." (p.1；栏首掉字)
- related_work: `Dempster-Shafer theory, also` — "Dempster-Shafer theory, also known as Evidence Theory, operates on a different framework compared to traditional probability theory [27], [28]." (p.2, II.A)
- method: `To expedite convergence` — "To expedite convergence towards local optima and enhance training efficiency, TEFN incorporates a normalization technique inspired by the Stationary model [48]." (p.4, III.A)
- experiments: `The experimental section` — "The experimental section aims to comprehensively evaluate TEFN’s performance in long-term time series forecasting." (p.6, IV)
- conclusion: `This paper introduces` — "This paper introduces the TEFN, a novel approach for long-term time series forecasting that is particularly well-suited for handling very large datasets." (p.13)

## Gap transitions

- consequently (abstract): "Consequently, the exploration of model architectures remains a perennially trending topic in research." (p.1)
- to address (abstract): "To address these challenges, we propose a novel backbone architecture named Time Evidence Fusion Network (TEFN) from the perspective of information fusion." (p.1)
- therefore (introduction): "Therefore, in order to reduce the error of time series forecasting, we propose the Time Evidence Fusion Network (TEFN) from the perspectives of evidence theory and information fusion." (p.1)
- unlike (introduction): "Unlike convolution, BPA is an expansion process in Figure 2." (p.1)
- while (method comparison): "While DLinear employs seasonal-trend decomposition and LightTS uses sampling techniques, evidence-based framework of TEFN fundamentally differs by modeling uncertainty through mass functions rather than direct feature extraction." (p.6)
- due to (limitations): "Due to fuzzy logic, TEFN is essentially a linear model that cannot handle some nonlinear time series well." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a novel backbone architecture named Time Evidence Fusion Network (TEFN)"; "we propose the Time Evidence Fusion Network (TEFN)"
- demonstrate / causal / abstract: "we conduct extensive experiments to demonstrate that TEFN achieves performance comparable to state-of-the-art methods"
- show / causal / abstract: "our experiments show that TEFN exhibits high robustness, with minimal error fluctuations during hyperparameter selection"
- can / ability / introduction, method: "evidence theory can effectively utilize the uncertainty of time series data"; "By utilizing non-linear membership functions, TEFN can effectively model the non-linear dynamics"
- may / speculative / method, limitations: "other fusion methods may be used"; "using expectations as the fusion method may not necessarily be the optimal pattern"

## Cross-section linkers

- introduction → related work / method / experiments / conclusion: "This paper is organized as follows. We begin by reviewing relevant literature in the Section II. Next, in the Section III, we delve into the architecture and underlying mathematical principles of TEFN. In the Section IV, we present a series of experiments that demonstrate TEFN’s superior performance. Finally, we conclude the paper by summarizing our key findings in the Section V." (p.2)
- related work → method: DSR 例子后进入 III 架构与 Fig. 4 (p.4)
- method → experiments: lightweight 模型对比后直接 `IV. EXPERIMENTS` (p.6)
- experiments → conclusion: Limitation 后直接 `V. CONCLUSION` (p.13)

## Candidate rules

- R001 abstract 用 `To address these challenges, we propose a novel backbone`，再并列 Specifically / Additionally / Lastly 展开模块与实验。
- R002 Introduction 把时间维与通道维写成两个信息源（Fig. 1），用 BPA 对卷积作 `Unlike convolution, BPA is an expansion process`。
- R003 贡献用项目符号三条：BPA backbone / TEFN 网络 / 证据理论进神经网络。
- R004 路标用 `This paper is organized as follows. We begin by reviewing`，定冠词写作 `the Section II`。
- R005 Conclusion 用 `This paper introduces the TEFN`，强调大规模数据下的效率与可解释性。

## Candidate phrases

- `To address these challenges, we propose a novel backbone architecture named` (abstract)
- `Therefore, in order to reduce the error of time series forecasting, we propose` (introduction)
- `The contributions of this article are as follows:` (introduction)
- `This paper is organized as follows.` (introduction)
- `The experimental section aims to comprehensively evaluate` (experiments)
- `This paper introduces the TEFN` (conclusion)

## House style

自称是 `we propose` / `this article` / `This paper introduces` / `TEFN`。未见 `Here we`。`we propose` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。摘要用 `we propose`；贡献列表用 `this article`；结论用 `This paper introduces`。

## Quotes

- p.1 abstract: In practical scenarios, time series forecasting necessitates not only accuracy but also efficiency.
- p.1 abstract: To address these challenges, we propose a novel backbone architecture named Time Evidence Fusion Network (TEFN) from the perspective of information fusion.
- p.1 abstract: Lastly, we conduct extensive experiments to demonstrate that TEFN achieves performance comparable to state-of-the-art methods while maintaining significantly lower complexity and reduced training time.
- p.1 abstract: Therefore, the proposed TEFN balances accuracy, efficiency, stability, and interpretability, making it a desirable solution for time series forecasting.
- p.1 introduction: THE evolution of various phenomena is inherently tied to the progression of time, leading to an increasing prevalence of time series data in a multitude of application domains [1], such as medical diagnosis [2]–[4], education [5], weather [6], [7], power system [8], and so on [9]–[11].
- p.1 introduction: Therefore, in order to reduce the error of time series forecasting, we propose the Time Evidence Fusion Network (TEFN) from the perspectives of evidence theory and information fusion.
- p.1 introduction: Unlike convolution, BPA is an expansion process in Figure 2.
- p.2 introduction: The contributions of this article are as follows:
- p.2 introduction: This paper is organized as follows. We begin by reviewing relevant literature in the Section II. Next, in the Section III, we delve into the architecture and underlying mathematical principles of TEFN. In the Section IV, we present a series of experiments that demonstrate TEFN’s superior performance. Finally, we conclude the paper by summarizing our key findings in the Section V.
- p.4 method: To expedite convergence towards local optima and enhance training efficiency, TEFN incorporates a normalization technique inspired by the Stationary model [48].
- p.4 method: The overall structure of TEFN is depicted in Figure 4. Next, we will elaborate on each module one by one.
- p.6 experiments: The experimental section aims to comprehensively evaluate TEFN’s performance in long-term time series forecasting.
- p.12 limitations: Due to fuzzy logic, TEFN is essentially a linear model that cannot handle some nonlinear time series well.
- p.13 conclusion: This paper introduces the TEFN, a novel approach for long-term time series forecasting that is particularly well-suited for handling very large datasets.
- p.13 conclusion: The model’s parameter efficiency, robustness, and interpretability make it a valuable tool for time series forecasting tasks involving large and complex datasets.
