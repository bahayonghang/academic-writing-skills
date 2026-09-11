---
key: UBYBQ7HL
title: "Online Sequential Sparse Robust Neural Networks With Random Weights for Imperfect Industrial Streaming Data Modeling"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2023.3326176"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,11-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 NNRW / OS-NNRW / ROS-NNRW / POS-NNRW / GM-R-NNRW）。未见 `The rest of this paper is organized as follows` 路标句；贡献列表后直接进入 II。Method 为 III，含 Algorithm 1。Experiments 标题为 `CASE STUDIES`（WWTP + BFIP）。

## Openers

- abstract: `Industrial streaming data` — "Industrial streaming data exhibits the concept drift characteristic due to the time-variant operating conditions, which degrades the performance of models established by traditional offline batch learning." (p.1)
- introduction: `THE monitoring management` — "THE monitoring management and operation optimization of industrial production mainly depend on the online accurate measurement of key production indicators (KPIs) [1], [2]." (p.1；栏首掉字)
- method: `This section details` — "This section details the proposed OSSR-NNRW algorithm." (p.4, III)
- experiments: `The water pollution` — "The water pollution problem has seriously affected people's living environment," (p.6, IV.A)
- conclusion: `This paper presents` — "This paper presents a novel OSSR-NNRW algorithm for online modeling of imperfect industrial streaming data." (p.11)

## Gap transitions

- therefore (abstract): "Therefore, this paper presents a novel online sequential sparse robust neural networks with random weights (OSSR-NNRW) for imperfect industrial streaming data to achieve highly reliable online modeling of time-variant dynamic systems." (p.1)
- however (introduction): "However, the direct measurement of some KPIs such as composition and mass by physical sensors is costly and less accurate because of the inadequacy of existing measuring devices." (p.1)
- therefore (introduction): "Therefore, establishing an accurate and reliable data-driven model for KPIs is of great practical significance to the actual industrial production operation [3]." (p.1)
- however (introduction): "However, the traditional NNRW based on once offline batch learning is not suitable for the analysis and mining of industrial data streams." (p.2)
- therefore (introduction): "Therefore, the data-driven model needs to have the online learning ability to cope with the time-varying dynamics of process." (p.2)
- nevertheless (introduction): "Nevertheless, the POS-NNRW lacks robustness." (p.2)
- thus (introduction): "Thus, the existing literature has improved one or some aspects of the problems with the NNRW, but there are no research reports that can simultaneously deal with the online robust modeling challenges of imperfect industrial streaming data with multiple outliers and multicollinearity until now." (p.2)

## Hedge verbs

- present / causal / abstract, conclusion: "this paper presents a novel online sequential sparse robust neural networks with random weights (OSSR-NNRW)"; "This paper presents a novel OSSR-NNRW algorithm"
- propose / causal / Note to Practitioners, introduction: "the OSSR-NNRW is proposed for online robust modeling"; "a novel online sequential sparse robust NNRW (OSSR-NNRW) algorithm is proposed"
- introduce / causal / abstract: "we introduce the online sequential learning strategy with forgetting factor"
- validate / causal / abstract: "data experiments on two industrial systems have validated the effectiveness, advancement, and practicality of the proposed method."
- illustrate / causal / conclusion: "The data experiments of the WWTP and the BFIP have illustrated that the proposed algorithm has the online learning ability"

## Cross-section linkers

- introduction → preliminaries: 贡献列表第 2 条后直接 `II. PRELIMINARIES`，无独立组织段 (p.3)
- method → experiments: Algorithm 1 后 `IV. CASE STUDIES` (p.6)
- experiments → conclusion: MIQ 结果段落后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `Therefore, this paper presents a novel` 收束方法缩写。
- R002 TASE 设 `Note to Practitioners—`，用 `To this end, the OSSR-NNRW is proposed` 复述现场用途。
- R003 Introduction 无独立 Related Work，用 `until now` 收束缺口后接 `In this paper, a novel ... is proposed`。
- R004 贡献用 `The contributions of this article are summarized as follows.` + 编号列表；自称在 abstract 用 `this paper`，贡献处用 `this article`。
- R005 Conclusion 用编号三条 `main advantages`，再写 `Due to the above three features`。

## Candidate phrases

- `Therefore, this paper presents a novel` (abstract)
- `In this paper, a novel ... is proposed to` (introduction)
- `The contributions of this article are summarized as follows.` (introduction)
- `This section details the proposed` (method)
- `This paper presents a novel ... for` (conclusion)

## House style

自称混用 `this paper`（abstract / conclusion）与 `this article`（贡献列表）以及 `we introduce` / `we adopt`。未见 `Here we`。`this paper presents` 与 `In this paper` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Industrial streaming data exhibits the concept drift characteristic due to the time-variant operating conditions, which degrades the performance of models established by traditional offline batch learning.
- p.1 abstract: Therefore, this paper presents a novel online sequential sparse robust neural networks with random weights (OSSR-NNRW) for imperfect industrial streaming data to achieve highly reliable online modeling of time-variant dynamic systems.
- p.1 abstract: Second, we introduce the online sequential learning strategy with forgetting factor to realize adaptive updating of model parameters, thus enhancing the online learning ability and overcoming the time-variant dynamics of industrial systems.
- p.1 abstract: Finally, data experiments on two industrial systems have validated the effectiveness, advancement, and practicality of the proposed method.
- p.1 note: To this end, the OSSR-NNRW is proposed for online robust modeling of complex time-variant dynamic systems by combining sparse robust modeling and online learning strategy in a unified framework of neural networks with random weights.
- p.1 introduction: THE monitoring management and operation optimization of industrial production mainly depend on the online accurate measurement of key production indicators (KPIs) [1], [2].
- p.1 introduction: However, the direct measurement of some KPIs such as composition and mass by physical sensors is costly and less accurate because of the inadequacy of existing measuring devices.
- p.1 introduction: Therefore, establishing an accurate and reliable data-driven model for KPIs is of great practical significance to the actual industrial production operation [3].
- p.2 introduction: However, the traditional NNRW based on once offline batch learning is not suitable for the analysis and mining of industrial data streams.
- p.2 introduction: Therefore, the data-driven model needs to have the online learning ability to cope with the time-varying dynamics of process.
- p.2 introduction: Nevertheless, the POS-NNRW lacks robustness.
- p.2 introduction: Thus, the existing literature has improved one or some aspects of the problems with the NNRW, but there are no research reports that can simultaneously deal with the online robust modeling challenges of imperfect industrial streaming data with multiple outliers and multicollinearity until now.
- p.2 introduction: In this paper, a novel online sequential sparse robust NNRW (OSSR-NNRW) algorithm is proposed to achieve highly reliable online modeling of complex industrial systems with time-variant operating conditions and imperfect production data.
- p.2 introduction: The contributions of this article are summarized as follows.
- p.4 method: This section details the proposed OSSR-NNRW algorithm.
- p.6 method: To sum up, the concrete implementation procedures of the proposed OSSR-NNRW algorithm are listed in Algorithm 1.
- p.6 experiments: The water pollution problem has seriously affected people's living environment,
- p.11 experiments: OSSR-NNRW achieves the best robust performance and the highest prediction accuracy among the four modeling methods, so its MIQ prediction value can fit the real value well and has good practicality.
- p.11 conclusion: This paper presents a novel OSSR-NNRW algorithm for online modeling of imperfect industrial streaming data.
- p.11 conclusion: The data experiments of the WWTP and the BFIP have illustrated that the proposed algorithm has the online learning ability to effectively overcome the impact of time-varying conditions on robust modeling, and can be easily implemented in complicated industrial processes.
