---
key: CVGQTSB5
title: "Quality Prediction Modeling for Industrial Processes Using Multiscale Attention-Based Convolutional Neural Network"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2024.3365068"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. CONVOLUTIONAL NEURAL NETWORK AND ATTENTION MECHANISM` → `III. MULTISCALE ATTENTION-BASED CNN FOR SOFT SENSOR MODELING` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 FPM / 浅层数据驱动 / DBN/SAE/LSTM/Transformer / CNN 局部特征）。Section II 为预备知识而非 Related Work。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDIES`（加氢裂化 + 脱丁烷塔）。

## Openers

- abstract: `Soft sensors have` — "Soft sensors have been increasingly applied for quality prediction in complex industrial processes, which often have different scales of topology and highly coupled spatiotemporal features." (p.2696)
- introduction: `IN MODERN industrial` — "IN MODERN industrial processes, advanced control, decision- making and optimization techniques are playing significant and irreplaceable roles for energy saving, green production and profit maximization [1], [2], [3], [4]." (p.2696；栏首掉字)
- method: `In the actual` — "In the actual industrial processes, the process variables usually have local spatiotemporal patterns due to the complex physicochemical reactions and mass transfer mechanisms." (p.2699, III)
- experiments: `In refineries and` — "In refineries and petrochemical plants, hydrocracking is a significant and effective secondary processing technology for petroleum refining" (p.2701, IV.A)
- conclusion: `This article mainly` — "This article mainly focuses on the problem about how to fully utilize the multiscale local spatiotemporal features for soft sensor in modern multicoupled complex industrial process." (p.2705)

## Gap transitions

- however (abstract): "However, the existing soft sensing models usually face difficulties in extracting the multiscale local spatiotemporal features in multicoupled complex process data and harnessing them to their full potential to improve the prediction performance." (p.2696)
- therefore (abstract): "Therefore, a multiscale attention-based CNN (MSACNN) is proposed in this article to alleviate such problems." (p.2696)
- however (introduction): "However, most of these quality variables are difficult to measure online but are obtained from offline laboratory analysis due to the harsh measuring environment, technique limitations, exorbitant measuring costs, etc." (p.2696)
- however (introduction): "However, process variables are usually associated with strong local spatiotemporal features due to contiguous topology structures and physicochemical reactions in actual industrial processes." (p.2697)
- to address (introduction): "To address these problems, we propose a multiscale attention-based CNN (MSACNN) for effective feature extraction and quality prediction in soft sensor modeling." (p.2697)

## Hedge verbs

- propose / causal / abstract, introduction: "a multiscale attention-based CNN (MSACNN) is proposed in this article"; "we propose a multiscale attention-based CNN (MSACNN)"
- validate / causal / abstract: "The superiority of the proposed MSACNN over the other state-of-the-art methods is validated through the performance evaluation in two real industrial processes."
- indicate / causal / experiments: "which indicate MSACNN can provide better-prediction performance"
- show / causal / experiments, conclusion: "The applications in the hydrocracking and debutanizer column process show that MSACNN outperforms the other models"
- conclude / causal / experiments: "it can be concluded that MSACNN can provide better-prediction performance for the light naphtha isopentane content than the other five models."

## Cross-section linkers

- introduction → preliminaries: "The remainder part of this article is arranged as follows. Section II describes the structure and principles of CNN and attention mechanisms. In Section III, the MSACNN is described in detail, and it is also analyzed what roles the multiscale convolutional layers and attention mechanisms play in the prediction model. In Section IV, MSACNN is applied for the online prediction of the quality variables in two industrial processes of the hydrocracking process and debutanizer column. Section V gives the conclusion of this article." (p.2697)
- preliminaries → method: 注意力公式后直接 `III. MULTISCALE ATTENTION-BASED CNN FOR SOFT SENSOR MODELING` (p.2699)
- method → experiments: 结构说明后 `IV. CASE STUDIES`（加氢裂化起）(p.2701)
- experiments → conclusion: 误差分布段落后直接 `V. CONCLUSION` (p.2705)

## Candidate rules

- R001 abstract 用 `is proposed in this article to alleviate such problems`，贡献不编号。
- R002 Introduction 无独立 Related Work，浅层 → 全局深度模型 → CNN 局部特征，再给编号贡献。
- R003 贡献列表标题用 `The main contributions of this article are summarized as follows.`
- R004 Introduction 末用 `The remainder part of this article is arranged as follows` 指向 II–V。
- R005 Conclusion 开篇用 `This article mainly focuses on the problem about how to`，收回多尺度卷积与通道注意力，不以未来工作收尾。

## Candidate phrases

- `a ... is proposed in this article to alleviate such problems` (abstract)
- `This article presents a solution to the challenge of` (introduction)
- `The main contributions of this article are summarized as follows.` (introduction)
- `The remainder part of this article is arranged as follows.` (introduction)
- `This article mainly focuses on the problem about how to` (conclusion)

## House style

自称是 `this article` / `is proposed in this article` / `we propose` / `MSACNN`。未见 `Here we`。`this article` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.2696 abstract: Soft sensors have been increasingly applied for quality prediction in complex industrial processes, which often have different scales of topology and highly coupled spatiotemporal features.
- p.2696 abstract: However, the existing soft sensing models usually face difficulties in extracting the multiscale local spatiotemporal features in multicoupled complex process data and harnessing them to their full potential to improve the prediction performance.
- p.2696 abstract: Therefore, a multiscale attention-based CNN (MSACNN) is proposed in this article to alleviate such problems.
- p.2696 introduction: IN MODERN industrial processes, advanced control, decision- making and optimization techniques are playing significant and irreplaceable roles for energy saving, green production and profit maximization [1], [2], [3], [4].
- p.2696 introduction: However, most of these quality variables are difficult to measure online but are obtained from offline laboratory analysis due to the harsh measuring environment, technique limitations, exorbitant measuring costs, etc.
- p.2697 introduction: However, process variables are usually associated with strong local spatiotemporal features due to contiguous topology structures and physicochemical reactions in actual industrial processes.
- p.2697 introduction: This article presents a solution to the challenge of extracting multiscale local spatiotemporal features from complex, multicoupled industrial process data, as well as utilizing them effectively in soft sensor models to enhance quality prediction performance.
- p.2697 introduction: To address these problems, we propose a multiscale attention-based CNN (MSACNN) for effective feature extraction and quality prediction in soft sensor modeling.
- p.2697 introduction: The main contributions of this article are summarized as follows.
- p.2697 introduction: The remainder part of this article is arranged as follows. Section II describes the structure and principles of CNN and attention mechanisms. In Section III, the MSACNN is described in detail, and it is also analyzed what roles the multiscale convolutional layers and attention mechanisms play in the prediction model. In Section IV, MSACNN is applied for the online prediction of the quality variables in two industrial processes of the hydrocracking process and debutanizer column. Section V gives the conclusion of this article.
- p.2699 method: In the actual industrial processes, the process variables usually have local spatiotemporal patterns due to the complex physicochemical reactions and mass transfer mechanisms.
- p.2702 experiments: As shown in Table II, MSACNN has the smallest RMSE value and the largest R2 value compared to LSTM, Transformer, CNN, DCN, and MSCNN, which indicate MSACNN can provide better-prediction performance.
- p.2703 experiments: Combining the distribution statistics in Table III and the boxplot of prediction errors in Fig. 7, it can be concluded that MSACNN can provide better-prediction performance for the light naphtha isopentane content than the other five models.
- p.2705 experiments: It can be easily seen that MSACNN can provide the best-prediction output curve that matches the real output curve.
- p.2705 conclusion: This article mainly focuses on the problem about how to fully utilize the multiscale local spatiotemporal features for soft sensor in modern multicoupled complex industrial process.
- p.2705–2706 conclusion: Thus, a MSACNN is proposed for feature extraction and quality prediction in soft sensor modeling.
- p.2706 conclusion: The applications in the hydrocracking and debutanizer column process show that MSACNN outperforms the other models in terms of prediction performance of quality variables.
