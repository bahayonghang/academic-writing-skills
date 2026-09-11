---
key: JMJB9UCU
title: "Multi timescale battery modeling: Integrating physics insights to data-driven model"
venue: "Applied Energy"
doi: "10.1016/j.apenergy.2025.126040"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,10-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction`（`1.1 Existing modeling approaches` → `1.2 Related work` → `1.3 Proposed approach and contributions` → `1.4 Paper organization`）→ `2. Multi timescale battery modeling` → `3. Data-driven approach` → `4. Integrating physics into the data-driven approach` → `5. Data` → `6` 训练 → `7. Results and discussion` → `8. Conclusion`。前置 `HIGHLIGHTS` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。无独立 Related Work 节。`related_work=inlined`（引言 1.1–1.2 评 EC / ECM / ML / encoder–decoder）。Introduction 末有编号贡献 + 节序路标。Method 拆成多时间尺度、纯数据驱动与物理嵌入。Experiments 标题为 `Results and discussion`。

## Openers

- abstract: `Developing accurate models` — "Developing accurate models for batteries, capturing ageing effects and nonlinear behaviors, is critical for the development of efficient and effective performance."
- introduction: `As the electric` — "As the electric vehicle (EV) market experiences rapid growth and the demand for stationary energy storage solutions continues to surge, lithium-ion (Li-ion) batteries are emerging as a crucial technology in this industry."
- method: `In the context` — "In the context of lithium-ion batteries, temporal dynamics exhibit distinct scales." (s.2)
- experiments: `The performance of` — "The performance of the proposed model is evaluated for multi-step ahead voltage prediction, state of charge estimation, and health indicators estimation (ℎcap,𝑛[𝑘𝑚], and ℎ𝑟,𝑛[𝑘𝑚])." (s.7)
- conclusion: `This study presents` — "This study presents a physics-informed encoder–decoder framework to model the multi-timescale dynamics of lithium-ion batteries."

## Gap transitions

- however (abstract): "However, most machine learning methods are black boxes, lacking interpretability and requiring large amounts of labeled data."
- however (introduction): "However, batteries experience degradation over their lifetime, leading to decreased performance."
- therefore (introduction): "Therefore, relying on mathematical models is essential to extract valuable insights into battery performance, particularly for estimating SOC and SOH."
- despite (introduction): "Despite their widespread usage, a common limitation of these encoder–decoder-based approaches is their reliance on explicit labels for SOC and SOH."
- to address (introduction): "In this paper, to address the challenges of limited interpretability and reliance on labeled data in ML-based battery modeling, we propose a physics-informed encoder–decoder model."

## Hedge verbs

- propose / causal / abstract, introduction, method: "we propose a physics-informed encoder–decoder model"; "we propose an integration of basic physics principles"
- demonstrate / causal / method: "The data-driven approach presented in Section 3 demonstrates the potential of encoder–decoder models"
- show / causal / experiments: "The results show that 𝑛𝑑 = 50 gives the lowest RMSE, MAPE, and Max."
- indicate / associative / experiments: "The results indicate the model’s ability to predict voltage across these different 𝑛𝑑 accurately."

## Cross-section linkers

- introduction → method: "This paper is organized as follows: We discuss the importance and complexities of general battery multi-timescale modeling in Section 2. Data-driven and physics-informed data-driven model constructions are discussed in Sections 3 and 4, respectively. The data used for model validation is described in Section 5. Section 6 covers model training and algorithms. Section 7 presents the results for single and multiple-cell-based training scenarios. Lastly, Section 8 summarizes conclusions and outlines future directions."
- method → experiments: `5. Data` 与训练节后直接 `7. Results and discussion`
- experiments → conclusion: 比较段落后 `8. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction 小节 `1.2 Related work`。
- R003 节序路标：`This paper is organized as follows`
- R004 贡献列表：`The key contributions of this work are as follows:`
- R009 自称：`In this paper, we propose` / `This study presents`

## Candidate phrases

- `In this paper, we propose a physics-informed encoder–decoder model` (abstract)
- `In this paper, to address the challenges of` (introduction)
- `The key contributions of this work are as follows:` (introduction)
- `This paper is organized as follows:` (introduction)
- `This study presents a physics-informed encoder–decoder framework` (conclusion)

## House style

自称 `In this paper, we propose` / `This study presents` / `Our proposed approach` / `we propose`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Developing accurate models for batteries, capturing ageing effects and nonlinear behaviors, is critical for the development of efficient and effective performance.
- abstract: However, most machine learning methods are black boxes, lacking interpretability and requiring large amounts of labeled data.
- abstract: In this paper, we propose a physics-informed encoder–decoder model that learns from unlabeled data to separate slow-changing battery states, such as state of charge (SOC) and state of health (SOH), from fast transient responses, thereby increasing interpretability compared to conventional methods.
- introduction: As the electric vehicle (EV) market experiences rapid growth and the demand for stationary energy storage solutions continues to surge, lithium-ion (Li-ion) batteries are emerging as a crucial technology in this industry.
- introduction: However, batteries experience degradation over their lifetime, leading to decreased performance.
- introduction: Therefore, relying on mathematical models is essential to extract valuable insights into battery performance, particularly for estimating SOC and SOH.
- introduction: Despite their widespread usage, a common limitation of these encoder–decoder-based approaches is their reliance on explicit labels for SOC and SOH.
- introduction: In this paper, to address the challenges of limited interpretability and reliance on labeled data in ML-based battery modeling, we propose a physics-informed encoder–decoder model.
- introduction: The key contributions of this work are as follows:
- introduction: This paper is organized as follows: We discuss the importance and complexities of general battery multi-timescale modeling in Section 2.
- method: In the context of lithium-ion batteries, temporal dynamics exhibit distinct scales.
- experiments: The performance of the proposed model is evaluated for multi-step ahead voltage prediction, state of charge estimation, and health indicators estimation (ℎcap,𝑛[𝑘𝑚], and ℎ𝑟,𝑛[𝑘𝑚]).
- experiments: The results show that 𝑛𝑑 = 50 gives the lowest RMSE, MAPE, and Max.
- conclusion: This study presents a physics-informed encoder–decoder framework to model the multi-timescale dynamics of lithium-ion batteries.
- conclusion: Future work will focus on improving model accuracy by, e.g., incorporating thermal effects into the model, applying transfer learning techniques to adapt the model to field data, and extending the framework to pack-level battery systems.
