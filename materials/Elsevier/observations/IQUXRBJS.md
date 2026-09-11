---
key: IQUXRBJS
title: "A fuzzy time series forecasting model with both accuracy and interpretability is used to forecast wind power"
venue: "Applied Energy"
doi: "10.1016/j.apenergy.2023.122015"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,10-17"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Fuzzy time series prediction module` → `3. FTS prediction dynamic optimization module` → `4` 实验（`4.4.2 Experiment 2` 等）→ `5. Discussion` → `6. Conclusion and future scope`。前置 `HIGHLIGHTS` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。无独立 Related Work。`related_work=inlined`（Introduction 中段评物理/统计/混合模型、FTS / 时变 / 非平稳模糊集）。Introduction 末有编号创新点 + 节序路标。Method 拆成 FTS 模块与动态优化模块。Experiments 在第 4 节，随后独立 `Discussion`。

## Openers

- abstract: `Considering the current` — "Considering the current research focus on the interpretability and efficiency of wind speed prediction models, this research presents a novel prediction model for dynamic non-stationary fuzzy time series."
- introduction: `Wind energy, as` — "Wind energy, as an environmentally friendly renewable energy source, has the potential to effectively address environmental pollution caused by high energy consumption and pollution from coal-fired power industries [1]."
- method: `Since the FTS` — "Since the FTS [30] prediction model was proposed, the main improvements in FTS prediction models have focused on different membership functions, methods to determine partition sizes, different numbers of fuzzy sets, defuzzification methods, as well as time-varying and non-stationary characteristics." (s.2.1)
- experiments: `In the field` — "In the field of practical engineering, it is necessary to consider the running time of the algorithm, that is, whether the algorithm is efficient." (s.4.4.2)
- conclusion: `Currently, wind speed` — "Currently, wind speed prediction is mainly processed using a mixture model due to its high volatility and heteroscedasticity."

## Gap transitions

- unlike (abstract): "Unlike existing mainstream hybrid systems for wind speed prediction, this model provides detailed explanations for almost every prediction step and eliminates the need for cumbersome data preprocessing steps."
- despite (introduction): "Despite the excellent performance demonstrated by hybrid models, especially deep learning models, in wind speed prediction, their training process remains a black box, lacking theoretical proof and interpretability [28]."
- however (introduction): "However, for the existing fuzzy time series models for short-term wind power prediction research, the subjective determination of parameters often results in the greatly reduced generalization ability of the models."
- however (introduction): "However, this study hopes to break this limitation under the premise that the model has high interpretability; and try to achieve the same level of prediction effect as deep learning."
- therefore (experiments): "Therefore, Experiment 2 is designed to test the efficiency of the model."

## Hedge verbs

- present / causal / abstract: "this research presents a novel prediction model"
- introduce / causal / abstract, conclusion: "this study introduces an enhanced version of the artificial hummingbird algorithm"; "an improved artificial bee colony algorithm SLG-AHA was proposed"
- propose / causal / introduction, method: "this paper proposes a Dynamic Non-Stationary FTS Method (SFTSM)"
- demonstrate / causal / abstract, conclusion: "Experimental results using data from the Shandong Penglai wind farm in China validate the effectiveness of the proposed model"; "The experimental results demonstrate that the proposed dynamic non-stationary FTS prediction model exhibits high stability and prediction accuracy."
- show / causal / experiments: "This result shows that for the time series prediction of wind speed data"

## Cross-section linkers

- introduction → method: "The subsequent sections of this paper are structured as follows. Section 2 provides an introduction to the non-stationary FTS forecasting method. Building upon this foundation, Section 3 presents the dynamic optimization approach for the non-stationary FTS prediction method. In Section 4, we present the experimental setup and report the results obtained from evaluating the proposed method on three distinct datasets. The findings and the superiority of the prediction system developed in this paper are discussed in Section 5. Finally, Section 6 summarizes the key points of the paper and offers future prospects for the proposed prediction system."
- method → experiments: 编码解码后接第 4 节实验
- experiments → conclusion: `5. Discussion` 后 `6. Conclusion and future scope`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The subsequent sections of this paper are structured as follows`
- R004 贡献列表：`this research has several key innovations, including:`
- R009 自称：`this research presents` / `this study introduces` / `this paper proposes`

## Candidate phrases

- `this research presents a novel prediction model for` (abstract)
- `this study introduces an enhanced version of` (abstract)
- `The subsequent sections of this paper are structured as follows.` (introduction)
- `In order to verify the prediction effect of the proposed system` (experiments)
- `this study proposes a dynamic non-stationary FTS prediction model` (conclusion)

## House style

自称 `this research presents` / `this study introduces` / `this paper proposes` / `our proposed model`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Considering the current research focus on the interpretability and efficiency of wind speed prediction models, this research presents a novel prediction model for dynamic non-stationary fuzzy time series.
- abstract: Unlike existing mainstream hybrid systems for wind speed prediction, this model provides detailed explanations for almost every prediction step and eliminates the need for cumbersome data preprocessing steps.
- abstract: Furthermore, this study introduces an enhanced version of the artificial hummingbird algorithm, called SLG-AHA, to further improve the accuracy and stability of fuzzy time series prediction.
- abstract: Experimental results using data from the Shandong Penglai wind farm in China validate the effectiveness of the proposed model by showcasing its superior prediction accuracy and stability.
- introduction: Wind energy, as an environmentally friendly renewable energy source, has the potential to effectively address environmental pollution caused by high energy consumption and pollution from coal-fired power industries [1].
- introduction: Despite the excellent performance demonstrated by hybrid models, especially deep learning models, in wind speed prediction, their training process remains a black box, lacking theoretical proof and interpretability [28].
- introduction: However, this study hopes to break this limitation under the premise that the model has high interpretability; and try to achieve the same level of prediction effect as deep learning.
- introduction: In summary, this research has several key innovations, including:
- introduction: The subsequent sections of this paper are structured as follows. Section 2 provides an introduction to the non-stationary FTS forecasting method.
- method: Since the FTS [30] prediction model was proposed, the main improvements in FTS prediction models have focused on different membership functions, methods to determine partition sizes, different numbers of fuzzy sets, defuzzification methods, as well as time-varying and non-stationary characteristics.
- experiments: In the field of practical engineering, it is necessary to consider the running time of the algorithm, that is, whether the algorithm is efficient.
- experiments: In order to verify the prediction effect of the proposed system, some of the most advanced wind speed prediction models are selected to compare with it.
- conclusion: Currently, wind speed prediction is mainly processed using a mixture model due to its high volatility and heteroscedasticity.
- conclusion: To solve the problems of low interpretability and excessive preprocessing, this study proposes a dynamic non-stationary FTS prediction model.
- conclusion: The experimental results demonstrate that the proposed dynamic non-stationary FTS prediction model exhibits high stability and prediction accuracy.
