---
key: DK7Q7LD9
title: "Hidformer: Hierarchical dual-tower transformer using multi-scale mergence for long-term time series forecasting"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2023.122412"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work` → `3. Methodology`（`3.1. Problem definition` / `3.2. Token segmentation` / `3.3. Multi-scale mergence` / `3.5. A dual-tower backbone`）→ `4` 实验（主结果表、消融、lookback、token length、encoder blocks、计算效率、可视化）→ `5. Conclusion and future work`。前置 `ABSTRACT` 与 `Keywords`。独立 Related Work。`related_work=independent`。Introduction 末有编号贡献。未见 `The rest of this paper is organized as follows` 路标。

## Openers

- abstract: `Long-term time series` — "Long-term time series forecasting has received a lot of popularity because of its great practicality."
- introduction: `Time series data` — "Time series data is everywhere, and forecasting is one of the most popular subtasks for time series analysis."
- related_work: `Time series forecasting` — "Time series forecasting is a widely studied problem."
- method: `Here we first` — "Here we first give the problem definition of LTSF." (s.3.1)
- experiments: `We test these` — "We test these variants under 1) multivariate forecasting: Weather, Electricity; 2) univariate forecasting: ETTh1, ETTm1." (消融设置；主结果表见 Table 3)
- conclusion: `This article studies` — "This article studies the popular long-term time series forecasting problem."

## Gap transitions

- however (abstract): "However, the permutation-invariant property of the Transformer and some other prominent shortcomings in the current Transformer-based models, such as missing multi-scale local features and information from the frequency domain, significantly limit their performance."
- however (introduction): "However, in the LTSF situation, the Transformer-based models have not yet achieved satisfactory results."
- to address (introduction): "To address the existing challenges in LSLF, we think a good Transformer-based framework should contain the following characteristics."
- based on (introduction): "Based on our theories, we propose a Hierarchical dual-tower Transformer-based model using multi-scale mergence (Hidformer) to solve the LTSF task."

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a Transformer-based model called Hidformer"; "we propose a Hierarchical dual-tower Transformer-based model"
- demonstrate / associative / abstract: "Recent works have demonstrated that Transformer has strong potential for this task."
- show / associative / abstract, conclusion: "The experimental results show that Hidformer achieves 72 top-1 and 69 top-2 scores out of 88 configurations."; "We verify the effectiveness of Hidformer through experiments on 7 real-world datasets."

## Cross-section linkers

- introduction → related_work: 贡献列表后 `2. Related work`
- related_work → method: `3. Methodology` / `3.1. Problem definition`
- method → experiments: 数据集统计表后接主结果 `Table 3 Multivariate LTSF results`
- experiments → conclusion: 预测可视化段落后 `5. Conclusion and future work`

## Candidate rules

- R001 独立 Related Work（`2. Related work`）。
- R004 编号贡献：`Our contributions are summarized as follows`
- R009 自称：`we propose` / `This article studies`

## Candidate phrases

- `To improve the accuracy of the long-term time series forecasting, we propose` (abstract)
- `Based on our theories, we propose` (introduction)
- `Our contributions are summarized as follows` (introduction)
- `Here we first give the problem definition of LTSF` (method)
- `This article studies the popular long-term time series forecasting problem` (conclusion)

## House style

自称 `we propose` / `This article studies` / `our proposed model`。实验节用 `We test` / `We verify`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Long-term time series forecasting has received a lot of popularity because of its great practicality.
- abstract: However, the permutation-invariant property of the Transformer and some other prominent shortcomings in the current Transformer-based models, such as missing multi-scale local features and information from the frequency domain, significantly limit their performance.
- abstract: To improve the accuracy of the long-term time series forecasting, we propose a Transformer-based model called Hidformer.
- abstract: The experimental results show that Hidformer achieves 72 top-1 and 69 top-2 scores out of 88 configurations.
- introduction: Time series data is everywhere, and forecasting is one of the most popular subtasks for time series analysis.
- introduction: However, in the LTSF situation, the Transformer-based models have not yet achieved satisfactory results.
- introduction: Based on our theories, we propose a Hierarchical dual-tower Transformer-based model using multi-scale mergence (Hidformer) to solve the LTSF task.
- introduction: Our contributions are summarized as follows:
- related_work: Time series forecasting is a widely studied problem. The existing solutions for this problem are mainly divided into three types: (1) statistical methods, (2) recurrent neural networks (RNNs), and (3) Transformer-based methods.
- method: Here we first give the problem definition of LTSF.
- experiments: We test these variants under 1) multivariate forecasting: Weather, Electricity; 2) univariate forecasting: ETTh1, ETTm1.
- conclusion: This article studies the popular long-term time series forecasting problem. We argue the defects that limit the performance of previous Transformer-based models and propose Hidformer.
- conclusion: We verify the effectiveness of Hidformer through experiments on 7 real-world datasets.
