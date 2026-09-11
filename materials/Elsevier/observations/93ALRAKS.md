---
key: 93ALRAKS
title: "Enhancing online industrial quality index prediction with a general deep temporal feature extraction and incremental ensemble modeling framework"
venue: "Engineering Applications of Artificial Intelligence"
doi: "10.1016/j.engappai.2025.111104"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related Work`（`2.1` 数据驱动软测量；`2.2` 在线质量指标预测） → `3. Methodology` → `4. Experiment` → `5. Conclusion and future work`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。独立 Related Work。Introduction 有编号贡献与节序路标。Experiments 分静态对比、在线预测、增量更新可视化、消融与鲁棒性。文末有 Generative AI 写作声明。

## Openers

- abstract: `Data-driven modeling methods` — "Data-driven modeling methods for industrial quality index prediction often face the challenge of limited data representation."
- introduction: `Soft sensor-based industrial` — "Soft sensor-based industrial quality index prediction plays a crucial role in modern industrial automation settings."
- related_work: `Compared to static` — "Compared to static soft sensor modeling and quality index prediction methods, online prediction focuses on dynamically updating model parameters within the industrial data stream to ensure continuous prediction accuracy." (s.2.2)
- method: `The structure and` — "The structure and workflow of the proposed TFE-IVBRE framework is shown in Fig. 1."
- experiments: `To explore the` — "To explore the performance differences between soft sensor models that use process data snapshots and those that use process variable data series, and to understand the upper limit of static models’ prediction performance, a series of soft sensors based on static modeling methods are constructed and tested on the DC and SRU datasets."
- conclusion: `To enhance the` — "To enhance the online quality index prediction performance of soft sensors, this paper integrates the powerful temporal feature extraction capabilities of deep networks with the strengths of ensemble learning and variational Bayesian regression for real-time incremental updates."

## Gap transitions

- moreover (abstract): "Moreover, during online prediction, the performance of soft sensors is affected by diverse operating conditions and concept drift in industrial data streams, leading to performance degradation."
- to address (abstract): "To address these challenges, this paper proposes a Temporal Feature Extraction and Incremental Variational Bayesian Regression Ensemble (TFE-IVBRE) framework, which provides a general solution for various online industrial quality index prediction tasks."
- nevertheless (introduction): "Nevertheless, data-driven modeling methods for industrial quality index prediction still face several challenges that need to be addressed."
- to tackle (introduction): "To tackle these challenges, this paper proposes a step-by-step approach to soft sensor modeling that is both versatile and scalable across different industrial scenarios."
- therefore (related_work): "Therefore, there is an urgent need for more efficient online prediction methods."

## Hedge verbs

- propose / causal / abstract, introduction: "this paper proposes a Temporal Feature Extraction and Incremental Variational Bayesian Regression Ensemble (TFE-IVBRE) framework"; "An incremental update strategy is proposed"
- show / associative / abstract: "Experiments in the Debutanizer Column and Sulfur Recovery Unit scenarios show that the prediction performance of TFE-IVBRE significantly outperforms other static and online comparison models"
- demonstrate / associative / abstract: "Finally, the overall model also demonstrates good robustness."
- integrate / causal / conclusion: "this paper integrates the powerful temporal feature extraction capabilities of deep networks"

## Cross-section linkers

- introduction → related_work: "The rest of the paper is organized as follows: Section 2 discusses the advancements and limitations of the data-driven industrial soft sensor modeling methods and online quality index prediction approaches."
- related_work → method: 贝叶斯回归动机后 `3. Methodology`
- method → experiments: 框架细节后进入第 4 节
- experiments → conclusion: 缺失与噪声鲁棒性后 `5. Conclusion and future work`

## Candidate rules

- R001 独立 Related Work。
- R003 节序路标：`The rest of the paper is organized as follows`
- R004 编号贡献。
- R009 自称：`this paper proposes` / `this paper integrates`

## Candidate phrases

- `To address these challenges, this paper proposes` (abstract)
- `To tackle these challenges, this paper proposes` (introduction)
- `The rest of the paper is organized as follows` (introduction)
- `To enhance the online quality index prediction performance of soft sensors, this paper integrates` (conclusion)

## House style

自称 `this paper proposes` / `this paper integrates` / `the proposed TFE-IVBRE`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。文末声明使用 GPT-4.0 改进行文，作者审改后负责。

## Quotes

- abstract: Data-driven modeling methods for industrial quality index prediction often face the challenge of limited data representation.
- abstract: To address these challenges, this paper proposes a Temporal Feature Extraction and Incremental Variational Bayesian Regression Ensemble (TFE-IVBRE) framework, which provides a general solution for various online industrial quality index prediction tasks.
- abstract: Experiments in the Debutanizer Column and Sulfur Recovery Unit scenarios show that the prediction performance of TFE-IVBRE significantly outperforms other static and online comparison models, with the effectiveness of its components validated through ablation studies.
- introduction: Soft sensor-based industrial quality index prediction plays a crucial role in modern industrial automation settings.
- introduction: Nevertheless, data-driven modeling methods for industrial quality index prediction still face several challenges that need to be addressed.
- introduction: To tackle these challenges, this paper proposes a step-by-step approach to soft sensor modeling that is both versatile and scalable across different industrial scenarios.
- introduction: The rest of the paper is organized as follows: Section 2 discusses the advancements and limitations of the data-driven industrial soft sensor modeling methods and online quality index prediction approaches.
- method: The structure and workflow of the proposed TFE-IVBRE framework is shown in Fig. 1.
- experiments: To explore the performance differences between soft sensor models that use process data snapshots and those that use process variable data series, and to understand the upper limit of static models’ prediction performance, a series of soft sensors based on static modeling methods are constructed and tested on the DC and SRU datasets.
- conclusion: To enhance the online quality index prediction performance of soft sensors, this paper integrates the powerful temporal feature extraction capabilities of deep networks with the strengths of ensemble learning and variational Bayesian regression for real-time incremental updates.
- conclusion: Combining minor updates for the VBR sub-models and major updates for the entire ensemble model, an incremental update strategy is proposed.
