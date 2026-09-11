---
key: LILATSDE
title: "PromptCast: A New Prompt-Based Learning Paradigm for Time Series Forecasting"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2023.3342137"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROMPT-BASED TIME SERIES FORECASTING` → `III. DATASET DESIGN AND DESCRIPTION` → `IV. BENCHMARK` → `V. CASE STUDIES` → `VI. DISCUSSION AND CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 LSTM/TCN/Transformer 数值预测与 NLP/CV 基础模型）。Introduction 末用三点贡献收束，无单独节序路标句；II 起为任务形式化。Experiments 标题为 `BENCHMARK` 与 `CASE STUDIES`。

## Openers

- abstract: `This paper presents` — "This paper presents a new perspective on time series forecasting." (p.1)
- introduction: `Time series forecasting` — "Time series forecasting is a research-intensive field, especially with the increasing of applying various deep learning frameworks for prediction such as models based on LSTM [1], Temporal Convolutional Network (TCN) [2], and Transformer [3]." (p.1)
- method: `The prompt-based time` — "The prompt-based time series forecasting task is developed from the general time series task." (p.2, II)
- experiments: `In this section` — "In this section, we present our benchmarking study and analysis for the proposed PromptCast task." (p.4, IV)
- conclusion: `In this paper` — "In this paper, we introduce a new task, PromptCast, which utilizes language models to predict time series in a language generation manner." (p.12)

## Gap transitions

- however (introduction): "However, we also notice that this evolution seems mostly limited to the NLP and CV fields." (p.1)
- hence (introduction): "Hence, we are particularly interested in exploring the research question of whether we can take advantage of large-scale pre-trained foundation models and adapt these models for predicting time series." (p.1)
- instead (introduction): "Instead, the input and output of the proposed prompt-based forecasting (Figure 1 (b)) are natural language sentences." (p.1)
- additionally (abstract): "Additionally, in comparison to conventional numerical-based forecasting, PromptCast shows a much better generalization ability under the zero-shot setting." (p.1)
- however (experiments): "However, for the language models, although the performance is lower than the standard setting and the train-from-scratch setting, prompt-based forecasting can still generate reasonable predictions." (p.8)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a new forecasting paradigm: prompt-based time series forecasting (PromptCast)"
- present / causal / abstract, introduction: "This paper presents a new perspective"; "we also present a large-scale dataset (PISA)"
- demonstrate / causal / abstract, conclusion: "The benchmark results with various forecasting settings demonstrate the proposed PromptCast with language generation models is a promising research direction."
- show / causal / abstract, experiments: "PromptCast shows a much better generalization ability under the zero-shot setting"
- indicate / speculative / experiments: "This benchmark answers RQ1 and indicates that prompt-based forecasting with language models is a promising direction for time series forecasting research."

## Cross-section linkers

- introduction → method: 贡献三点后直接 `II. PROMPT-BASED TIME SERIES FORECASTING` (p.2)
- dataset → experiments: 统计段落后直接 `IV. BENCHMARK` (p.4)
- experiments → case studies: 多变量讨论后 `V. CASE STUDIES` (p.11)
- case studies → conclusion: 注意力可视化后 `VI. DISCUSSION AND CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 开篇用 `This paper presents`，贡献用 `we propose` / `we also present`。
- R002 Introduction 无独立 Related Work，用研究问题句 `whether we can take advantage of` 转入方法。
- R003 贡献用 `In summary, our contributions are three-fold:` 加编号括号项。
- R004 Experiments 用 `RQ1` / `RQ2` 组织基准问题。
- R005 Conclusion 节标题为 `DISCUSSION AND CONCLUSION`，先收回任务与数据集，再用 `Broader Impact` / `Limitations and Future Work` 分块。

## Candidate phrases

- `This paper presents a new perspective on` (abstract)
- `we propose a new forecasting paradigm` (abstract)
- `In summary, our contributions are three-fold:` (introduction)
- `To the best of our knowledge, this is the first effort` (introduction)
- `In this paper, we introduce a new task` (conclusion)

## House style

自称是 `This paper` / `In this paper` / `we propose` / `our contributions` / `the proposed PromptCast`。`In this paper` / `This paper presents` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。

## Quotes

- p.1 abstract: This paper presents a new perspective on time series forecasting.
- p.1 abstract: Thus, we propose a new forecasting paradigm: prompt-based time series forecasting (PromptCast).
- p.1 abstract: To support and facilitate the research of this task, we also present a large-scale dataset (PISA) that includes three real-world forecasting scenarios.
- p.1 abstract: Additionally, in comparison to conventional numerical-based forecasting, PromptCast shows a much better generalization ability under the zero-shot setting.
- p.1 introduction: Time series forecasting is a research-intensive field, especially with the increasing of applying various deep learning frameworks for prediction such as models based on LSTM [1], Temporal Convolutional Network (TCN) [2], and Transformer [3].
- p.1 introduction: However, we also notice that this evolution seems mostly limited to the NLP and CV fields.
- p.1 introduction: Hence, we are particularly interested in exploring the research question of whether we can take advantage of large-scale pre-trained foundation models and adapt these models for predicting time series.
- p.1 introduction: To the best of our knowledge, this is the first effort in approaching general time-series forecasting from a language-based perspective without any modifications on the model architectures, resulting also in the first large-scale dataset, PISA (Prompt based tIme Series forecAsting), tailored for the task of prompt-based time series forecasting.
- p.2 introduction: In summary, our contributions are three-fold: (1) We propose a novel prompt-based forecasting paradigm, which differs from the existing forecasting methods.
- p.2 method: The prompt-based time series forecasting task is developed from the general time series task.
- p.4 experiments: In this section, we present our benchmarking study and analysis for the proposed PromptCast task.
- p.8 experiments: This benchmark answers RQ1 and indicates that prompt-based forecasting with language models is a promising direction for time series forecasting research.
- p.8 experiments: However, for the language models, although the performance is lower than the standard setting and the train-from-scratch setting, prompt-based forecasting can still generate reasonable predictions.
- p.8 experiments: This demonstrates a strong generalization ability when time series forecasting is addressed with prompts (RQ2).
- p.12 conclusion: In this paper, we introduce a new task, PromptCast, which utilizes language models to predict time series in a language generation manner.
- p.12 conclusion: The experimental results demonstrate that using language models in the PromptCast setting results in good forecasting performance and generalization ability.
- p.13 conclusion: As the first attempt to create a dataset for the novel PromptCast task, in this dataset release, we have mainly focused on the univariate time series forecasting setting.
