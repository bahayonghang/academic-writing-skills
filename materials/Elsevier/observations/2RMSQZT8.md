---
key: 2RMSQZT8
title: "Physics-informed neural network for chiller plant optimal control with structure-type and trend-type prior knowledge"
venue: "Applied Energy"
doi: "10.1016/j.apenergy.2025.125857"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,10-22"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. General framework of PINN` → `3. Application in chiller plant optimal control` → `4. Data experiment setup` → `5. Results and discussions` → `6. Conclusions and future work`。前置 `HIGHLIGHTS` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 MPC、PINN/PCNN 与 HVAC 定制网络）。Introduction 末有编号贡献 + 节序路标。Method 拆成 PINN 通式与冷机系统应用。Experiments 标题为 `Data experiment setup` + `Results and discussions`，含现场试验。

## Openers

- abstract: `The development of` — "The development of advanced controller for heating, ventilation, and air conditioning (HVAC) system contributes significantly to building energy conservation."
- introduction: `Building sector accounts` — "Building sector accounts for 40 % of global energy consumption as well as 30 % of greenhouse gas emissions, where a large portion of energy is consumed by heating, ventilation and air conditioning (HVAC) system for space heating and cooling [1–3]."
- method: `This section will` — "This section will illustrate the general framework of proposed PINN, where the details of structure-type knowledge and trend-type knowledge as well as their corresponding PINN will be illustrated in following sections." (s.2)
- experiments: `To validate the` — "To validate the proposed method, four-month history data, from June 1st 2024 to September 30th 2024, of investigated system are employed." (s.4)
- conclusion: `This paper proposes` — "This paper proposes a general framework of physics-informed neural network for chiller plant optimal control."

## Gap transitions

- while (abstract): "While the success of these optimal control technologies is highly relied on the accuracy of energy models."
- to solve (abstract): "To solve this problem, this paper proposes a general framework of physics-informed neural network (PINN) to improve the extrapolation performance of energy models."
- however (introduction): "However, most energy models are based on data-driven models, and their generalization ability is a huge concern [23,24]."
- therefore (introduction): "Therefore, how to improve the generalization ability of energy model becomes an urgent problem for the application of optimal control technology [27,28]."
- even though (introduction): "Even though lots of work have been done in HVAC system optimal control and PINN development, the following knowledge gaps are still identified."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this paper proposes a general framework"; "We propose a general framework of PINN"
- demonstrate / causal / abstract, introduction: "The results demonstrate that both the structure-type knowledge and trend-type knowledge can significantly improve the model extrapolation performance."
- show / causal / experiments: "Fig. 10 shows the comparison results of chilled pump and cooling pump energy model under two scenarios."
- indicate / associative / experiments: "This indicates the physics-informed structure can reduce the learning cost of model and provide reliable prediction for extrapolation cases."

## Cross-section linkers

- introduction → method: "The remain sections are organized as follows. Section 2 introduces the general framework of proposed PINN. And the concept of PINN is applied in a commercial chiller plant for its optimal control, which is illustrated in Section 3. Section 4 illustrates the experiment setup. And its results are demonstrated in Section 5. Finally, Section 6 concludes our work as well as the direction of future work."
- method → experiments: 最优控制任务段落后 `4. Data experiment setup`
- experiments → conclusion: 现场试验段落后 `6. Conclusions and future work`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remain sections are organized as follows`
- R004 贡献列表：`the main contributions of this study are summarized as follows.`
- R009 自称：`this paper proposes` / `We propose`

## Candidate phrases

- `To solve this problem, this paper proposes a general framework of` (abstract)
- `the main contributions of this study are summarized as follows.` (introduction)
- `The remain sections are organized as follows.` (introduction)
- `To validate the proposed method, four-month history data` (experiments)
- `This paper proposes a general framework of physics-informed neural network for` (conclusion)

## House style

自称 `this paper proposes` / `We propose` / `this study` / `our proposed T-PINN`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The development of advanced controller for heating, ventilation, and air conditioning (HVAC) system contributes significantly to building energy conservation.
- abstract: To solve this problem, this paper proposes a general framework of physics-informed neural network (PINN) to improve the extrapolation performance of energy models.
- abstract: The results demonstrate that both the structure-type knowledge and trend-type knowledge can significantly improve the model extrapolation performance.
- abstract: And the field experiments showed that the developed PINNs achieved 23.2 % improvement of energy efficiency by resetting system control setpoint.
- introduction: Building sector accounts for 40 % of global energy consumption as well as 30 % of greenhouse gas emissions, where a large portion of energy is consumed by heating, ventilation and air conditioning (HVAC) system for space heating and cooling [1–3].
- introduction: However, most energy models are based on data-driven models, and their generalization ability is a huge concern [23,24].
- introduction: Therefore, how to improve the generalization ability of energy model becomes an urgent problem for the application of optimal control technology [27,28].
- introduction: Even though lots of work have been done in HVAC system optimal control and PINN development, the following knowledge gaps are still identified.
- introduction: To fill in above knowledge gaps, the main contributions of this study are summarized as follows.
- introduction: The remain sections are organized as follows. Section 2 introduces the general framework of proposed PINN.
- method: This section will illustrate the general framework of proposed PINN, where the details of structure-type knowledge and trend-type knowledge as well as their corresponding PINN will be illustrated in following sections.
- experiments: To validate the proposed method, four-month history data, from June 1st 2024 to September 30th 2024, of investigated system are employed.
- experiments: The proposed S-PINN outperformed gray-box model and ANN under all scenarios.
- conclusion: This paper proposes a general framework of physics-informed neural network for chiller plant optimal control.
- conclusion: Developed PINN energy models improved 23.2 % energy efficiency for investigated chiller plant.
