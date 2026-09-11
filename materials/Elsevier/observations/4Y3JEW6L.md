---
key: 4Y3JEW6L
title: "Prediction of NOx emission concentration from coal-fired power plant based on joint knowledge and data driven"
venue: "Energy"
doi: "10.1016/j.energy.2023.127044"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. The boiler and mechanistic knowledge` → `3. The VMD and informer` → `4. The proposed models` → `5. Forecast results and analysis` → `6. Discussion` → `7. Conclusions`。前置 `ABSTRACT` 与 `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 knowledge driven vs data driven、joint driven、VMD、Informer）。Introduction 末有项目符号贡献 + 节序路标。Method 标题为 `4. The proposed models`（MEVMD、combined feature selection、adaptive segmentation、ME-INF）。Experiments 标题为 `5. Forecast results and analysis`（Caojing 四季数据集 D1–D4）。

## Openers

- abstract: `Accurate NOx concentration` — "Accurate NOx concentration prediction is of great significance for the pollutant emission control and safe operation of coal-fired power plants."
- introduction: `One of the main` — "One of the main sources of atmospheric pollutants, nitrogen oxides (NOx), is produced in huge quantities during the operation of coal-fired power plants [1]."
- method: `Data driven models` — "Data driven models are deficient in predicting data with nonlinear characteristics [15]."
- experiments: `In the research` — "In the research, historical operational data of 1000 MW coal-fired generating units at Shanghai Caojing Power Plant are used for NOx concentration prediction comparison experiments."
- conclusion: `Establishing an accurate` — "Establishing an accurate and stable NOx emission concentration prediction model is the foundation for realizing denitrification and environmental protection in coal-fired power plants."

## Gap transitions

- however (introduction): "However, CEMS measurement is hampered by issues such as a harsh working environment, signal interference, and its own failure [5]."
- therefore (introduction): "Therefore, it is critical to develop an accurate NOx emission concentration prediction model from coal-fired units for denitrification and environmental protection [6]."
- however (introduction): "However, the knowledge driven model requires a number of assumptions that are challenging to meet in actual production, and the model parameters are numerous and complicated to calculate [10]."
- however (introduction): "However, one of the major challenges is the inability of VMD to decompose adaptively."

## Hedge verbs

- propose / causal / abstract, introduction: "We propose a NOx emission concentration prediction method based on joint knowledge and data driven."; "This paper proposes a hybrid model based on joint knowledge and data driven."
- indicate / associative / abstract: "The experimental results indicate that the proposed method predicts the NOx concentration better than several comparative models."
- demonstrate / causal / conclusion: "In comparison to other methods, the experimental results demonstrate the model’s strong generalization and prediction accuracy."
- confirmed / associative / introduction: "several researchers, including Li et al. [22], Yi et al. [23], and Wang et al. [24], confirmed that the joint driven method produces excellent results"
- may / speculative / discussion: "We may try to develop other algorithms for predicting distorted data in future research."

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows. Section 2 describes the boiler in this research and NOx generation mechanism. Section 3 discusses the VMD, Informer, and Methodology. Section 4 presents the proposed prediction model in detail. Section 5 conducts a comparison experiment to validate the model performance. The final section concludes this paper."
- method → experiments: overall prediction model 后 `5. Forecast results and analysis`
- experiments → conclusion: Discussion 局限后 `7. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is organized as follows`
- R004 编号贡献：`The contributions of this paper are as follows.`
- R009 自称：`We propose` / `This paper proposes`

## Candidate phrases

- `We propose a NOx emission concentration prediction method based on joint knowledge and data driven` (abstract)
- `This paper proposes a hybrid model based on joint knowledge and data driven` (introduction)
- `The contributions of this paper are as follows.` (introduction)
- `The rest of this paper is organized as follows` (introduction)
- `A hybrid prediction model based on joint knowledge and data driven is proposed` (conclusion)

## House style

自称 `We propose` / `This paper proposes` / `we introduce` / `we employ`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Accurate NOx concentration prediction is of great significance for the pollutant emission control and safe operation of coal-fired power plants.
- abstract: We propose a NOx emission concentration prediction method based on joint knowledge and data driven.
- abstract: The experimental results indicate that the proposed method predicts the NOx concentration better than several comparative models.
- introduction: One of the main sources of atmospheric pollutants, nitrogen oxides (NOx), is produced in huge quantities during the operation of coal-fired power plants [1].
- introduction: Therefore, it is critical to develop an accurate NOx emission concentration prediction model from coal-fired units for denitrification and environmental protection [6].
- introduction: This paper proposes a hybrid model based on joint knowledge and data driven.
- introduction: The rest of this paper is organized as follows. Section 2 describes the boiler in this research and NOx generation mechanism.
- method: Data driven models are deficient in predicting data with nonlinear characteristics [15].
- experiments: In the research, historical operational data of 1000 MW coal-fired generating units at Shanghai Caojing Power Plant are used for NOx concentration prediction comparison experiments.
- experiments: Therefore, the proposed model improves the prediction accuracy of NOx concentration significantly.
- conclusion: Establishing an accurate and stable NOx emission concentration prediction model is the foundation for realizing denitrification and environmental protection in coal-fired power plants.
- conclusion: In comparison to other methods, the experimental results demonstrate the model’s strong generalization and prediction accuracy.
