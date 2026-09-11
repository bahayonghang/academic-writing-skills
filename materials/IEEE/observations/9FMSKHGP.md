---
key: 9FMSKHGP
title: "A Domain Knowledge-Supervised Framework Based on Deep Probabilistic Generation Network for Enhancing Industrial Soft Sensing"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3566821"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATE WORK` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（标题作 `II. RELATE WORK`，mechanism / knowledge / data-driven 三类）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDY`（TEP / CSTH / AEP）。作者稿页码 1–10。

## Openers

- abstract: `Soft sensors have` — "Soft sensors have been widely used in many industrial processes for monitoring and optimization." (p.1)
- introduction: `THE effective operations` — "THE effective operations of complex industrial systems rely on accurate measurement of product quality [1]." (p.1；栏首掉字)
- method: `The DPGN is` — "The DPGN is a deep generative framework that integrates the encoding-decoding architecture of autoencoders." (p.2, III.A)
- experiments: `In this section` — "In this section, the proposed soft-sensing model is evaluated by Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and Coefficient of Determination (R2) on three real industrial processes, as shown in Eq. (8)." (p.3–4, IV)
- conclusion: `In this paper` — "In this paper, we propose a soft-sensing model based on DKSF-DPGN, which addresses the issue of data patterns not aligning with process mechanisms in existing soft-sensing methods." (p.9)

## Gap transitions

- however (abstract): "Existing soft-sensing methods rely on high-quality data. However, the intrinsic patterns of data might deviate from process mechanisms due to an adverse environment, leading to a decrease in accuracy." (p.1)
- to address (abstract): "To address these challenges, we propose a domain knowledge-supervised framework based on a deep probabilistic generative network (DKSF-DPGN)." (p.1)
- despite (introduction): "Despite various successes, existing soft-sensing methods have been considerably criticized for a variety of reasons." (p.1)
- in response (introduction): "In response, we propose a domain knowledge-supervised framework based on a deep probabilistic generative network (DKSF-DPGN)." (p.1)
- despite (related work): "Despite the advancements achieved by the above modeling methods, they still have limitations in the industrial soft-sensing." (p.2)
- in future work (conclusion): "In future work, we plan to introduce meta-learning to the DKSF-DPGN framework." (p.9)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a domain knowledge-supervised framework"; "In this paper, we propose a soft-sensing model based on DKSF-DPGN"
- demonstrate / causal / abstract, conclusion: "Experimental results demonstrate that our model exhibits outstanding accuracy"; "Experimental results and comparative analyses demonstrate that DKSF-DPGN enhances prediction accuracy"
- show / causal / experiments: "The evaluation results of eleven models on the TEP dataset are shown in Table I"; "As shown in Table III, DKSF-DPGN achieves the lowest MAE, MSE, RMSE, and MAPE"
- indicate / causal / experiments: "It indicates that data-driven network has learned a part of the feature structures from knowledge network"

## Cross-section linkers

- introduction → later sections: "The rest of this paper is as follows. Section II reviews the existing industrial soft-sensing methods. Section III develops the DGRN, DKRN, and DKSF-DPGN. Section IV presents experiments on the benchmarks of TEP, CSTH, and the real-world AEP. Section V draws the conclusion." (p.2)
- related work → method: Related Work 末句 "By integrating the advantages of existing methods, DKSF-DPGN not only enhances prediction accuracy but also improves model interpretability." 随后 `III. METHODOLOGY` (p.2)
- method → experiments: Algorithm 1 之后 `IV. CASE STUDY` (p.3)
- experiments → conclusion: 消融段落后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 贡献用 `we propose` + 框架缩写，并用 `The contributions of this work are below` 分点。
- R002 独立 Related Work 按 mechanism / knowledge / data-driven 三类组织，末段收回本文方法。
- R003 Introduction 末用 `The rest of this paper is as follows` 指向 II–V。
- R004 贡献用编号列表 `(1)`–`(4)`。
- R005 Conclusion 用 `In this paper, we propose` 收回方法，再用 `In future work, we plan to` 指向后续。

## Candidate phrases

- `To address these challenges, we propose` (abstract)
- `In response, we propose` (introduction)
- `The rest of this paper is as follows.` (introduction)
- `In this paper, we propose a soft-sensing model based on` (conclusion)
- `In future work, we plan to introduce meta-learning` (conclusion)

## House style

自称是 `we propose` / `In this paper, we propose` / `our model` / `the proposed DKSF-DPGN`。未见 `Here we`。`In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。路标用 `this paper`。

## Quotes

- p.1 abstract: Soft sensors have been widely used in many industrial processes for monitoring and optimization.
- p.1 abstract: Existing soft-sensing methods rely on high-quality data. However, the intrinsic patterns of data might deviate from process mechanisms due to an adverse environment, leading to a decrease in accuracy.
- p.1 abstract: To address these challenges, we propose a domain knowledge-supervised framework based on a deep probabilistic generative network (DKSF-DPGN).
- p.1 abstract: Experimental results demonstrate that our model exhibits outstanding accuracy, as measured by Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Coefficient of Determination (R2), and Mean Absolute Percentage Error (MAPE).
- p.1 introduction: THE effective operations of complex industrial systems rely on accurate measurement of product quality [1].
- p.1 introduction: Despite various successes, existing soft-sensing methods have been considerably criticized for a variety of reasons.
- p.1 introduction: In response, we propose a domain knowledge-supervised framework based on a deep probabilistic generative network (DKSF-DPGN).
- p.2 introduction: The rest of this paper is as follows. Section II reviews the existing industrial soft-sensing methods. Section III develops the DGRN, DKRN, and DKSF-DPGN. Section IV presents experiments on the benchmarks of TEP, CSTH, and the real-world AEP. Section V draws the conclusion.
- p.2 related work: Despite the advancements achieved by the above modeling methods, they still have limitations in the industrial soft-sensing.
- p.2 method: The DPGN is a deep generative framework that integrates the encoding-decoding architecture of autoencoders.
- p.3 experiments: In this section, the proposed soft-sensing model is evaluated by Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and Coefficient of Determination (R2) on three real industrial processes, as shown in Eq. (8).
- p.5 experiments: DKSF-DPGN improves R2 by 36.4%, 57.6%, and 72.1% compared to GSTAE, GCT, and LSTM-DeepFM, respectively.
- p.9 conclusion: In this paper, we propose a soft-sensing model based on DKSF-DPGN, which addresses the issue of data patterns not aligning with process mechanisms in existing soft-sensing methods.
- p.9 conclusion: Experimental results and comparative analyses demonstrate that DKSF-DPGN enhances prediction accuracy while also improving the interpretability.
- p.9 conclusion: In future work, we plan to introduce meta-learning to the DKSF-DPGN framework.
