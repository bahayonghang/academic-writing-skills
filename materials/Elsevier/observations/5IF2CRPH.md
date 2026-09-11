---
key: 5IF2CRPH
title: "Locally spatiotemporal soft sensor for key indicator prediction in cement production process"
venue: "Chemical Engineering Science"
doi: "10.1016/j.ces.2025.121386"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Process and challenge Statement` → `3. Local modeling with TLSTM model` → `4. Results and Discussion` → `5. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 PCA/CNN/DAE/LSTM、MCC-LSTM、JITL-PLS/SVR/CNN）。Introduction 末编号贡献（`1.` / `2.` / `3.`）。无 `The remainder of this paper` 路标。Method 含 MCC-based TLSTM、JITL 局部建模与实施步骤。Experiments 标题为 `4. Results and Discussion`（水泥厂 f-CaO）。

## Openers

- abstract: `Cement production exemplifies` — "Cement production exemplifies a complex chemical engineering process where chemical reactions and material transformations critically affect product quality."
- introduction: `Cement plays a vital` — "Cement plays a vital role in the construction industry, greatly influencing the safety and effectiveness of infrastructure."
- method: `The framework of` — "The framework of TLSTM is depicted in Fig. 2."
- experiments: `To demonstrate its` — "To demonstrate its effectiveness, JTLSTM is applied to the f-CaO soft sensing task at a large cement plant in China."
- conclusion: `A JTLSTM soft` — "A JTLSTM soft sensor using a dynamic local modeling strategy is proposed to predict f-CaO content online."

## Gap transitions

- however (introduction): "However, the cement production process complexity poses significant challenges to existing soft sensors."
- although (introduction): "Although CNNs are capable of effectively modeling the non-linearity observed in historical production processes, static global soft sensors, constructed on the entirety of historical data, inherently lack dynamic adaptability in describing continuously changing production processes."
- to address (introduction): "To address the outliers in cement production data, as well as the non-linearity and dynamism of the production process, a reliable just-in-time two-dimensional LSTM (denoted as JTLSTM) soft sensor is developed for predicting f-CaO content."
- thus (introduction): "Thus, data-driven soft sensors, which mine information from the data to predict key indicators, have found widespread applications."

## Hedge verbs

- is proposed / causal / abstract: "a just-in-time two-dimensional long short-term memory (JTLSTM) soft sensor with correntropy is proposed for predicting free calcium oxide (f-CaO)"
- demonstrates / causal / abstract: "The soft-sensing task about f-CaO in a practical cement process demonstrates the superiority of JTLSTM compared to several existing soft sensors."
- is developed / causal / introduction: "a reliable just-in-time two-dimensional LSTM (denoted as JTLSTM) soft sensor is developed for predicting f-CaO content."
- outperforms / associative / conclusion: "Comparative evaluation of f-CaO content predictions shows that JTLSTM consistently outperforms several baseline models"

## Cross-section linkers

- introduction → process: 编号贡献与结果句后 `2. Process and challenge Statement`
- process → method: "The ensuing sections illustrate how JTLSTM can be extended to other chemical processes of similar complexities" 后 `3. Local modeling with TLSTM model`
- method → experiments: 实施步骤后 `4. Results and Discussion`
- experiments → conclusion: 基线对照表后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R004 编号贡献：`The main contributions of this paper are:`
- R009 自称：`is proposed` / `is developed` / `The main contributions of this paper are`

## Candidate phrases

- `a just-in-time two-dimensional long short-term memory (JTLSTM) soft sensor with correntropy is proposed` (abstract)
- `The main contributions of this paper are:` (introduction)
- `To demonstrate its effectiveness, JTLSTM is applied to the f-CaO soft sensing task` (experiments)
- `A JTLSTM soft sensor using a dynamic local modeling strategy is proposed` (conclusion)

## House style

自称 `is proposed` / `is developed` / `The main contributions of this paper are`。被动与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Cement production exemplifies a complex chemical engineering process where chemical reactions and material transformations critically affect product quality.
- abstract: To this end, a just-in-time two-dimensional long short-term memory (JTLSTM) soft sensor with correntropy is proposed for predicting free calcium oxide (f-CaO), as a key indicator of cement production.
- abstract: The soft-sensing task about f-CaO in a practical cement process demonstrates the superiority of JTLSTM compared to several existing soft sensors.
- introduction: Cement plays a vital role in the construction industry, greatly influencing the safety and effectiveness of infrastructure.
- introduction: However, the cement production process complexity poses significant challenges to existing soft sensors.
- introduction: Although CNNs are capable of effectively modeling the non-linearity observed in historical production processes, static global soft sensors, constructed on the entirety of historical data, inherently lack dynamic adaptability in describing continuously changing production processes.
- introduction: To address the outliers in cement production data, as well as the non-linearity and dynamism of the production process, a reliable just-in-time two-dimensional LSTM (denoted as JTLSTM) soft sensor is developed for predicting f-CaO content.
- introduction: The main contributions of this paper are:
- experiments: To demonstrate its effectiveness, JTLSTM is applied to the f-CaO soft sensing task at a large cement plant in China.
- conclusion: A JTLSTM soft sensor using a dynamic local modeling strategy is proposed to predict f-CaO content online.
- conclusion: Comparative evaluation of f-CaO content predictions shows that JTLSTM consistently outperforms several baseline models, achieving superior performance as evidenced by its smaller RMSE and larger CE values.
