---
key: UUISGG3T
title: "An Adaptive Continual Learning Method for Nonstationary Industrial Time Series Prediction"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3468433"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. CONTINUAL LEARNING` → `III. PROPOSED METHOD` → `IV. EXPERIMENTAL VERIFICATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. CONTINUAL LEARNING`：`A. Overview of Continual Learning` / `B. Problem Statement Based on Continual Learning`）。Introduction 中段已评 CLEAR 等预测向持续学习。无 `The rest of this article is organized as follows`。Method 在正文中段。Experiments 标题为 `EXPERIMENTAL VERIFICATION`（光伏 + 磨矿分级）。

## Openers

- abstract: `Deep learning models` — "Deep learning models have gained significant attention and application in recent years to improve the accuracy and efficiency of industrial time series prediction." (p.1)
- introduction: `INDUSTRIAL time series` — "INDUSTRIAL time series data, as a kind of structured data that reflects information of production processes, can be analyzed and modeled to better understand the operation of industrial systems or equipment, optimize and guide the production processes, etc." (p.1；栏首掉字)
- related_work: `Continual learning is` — "Continual learning is a machine learning paradigm that enables models to learn and adapt to new data distributions by leveraging existing knowledge and experience, without retraining or discarding old knowledge." (p.2, II.A)
- method: `We tailored the` — "We tailored the continual learning methods for nonstationary time series forecasting tasks in two aspects." (p.3, III)
- experiments: `To verify the` — "To verify the effectiveness of our proposed industrial time series prediction method based on adaptive continual learning, we conducted experiments using open-source solar power generation datasets and real grinding and grading process datasets." (p.5, IV)
- conclusion: `Finally, to address` — "Finally, to address the problem of accuracy degradation of prediction models in nonstationary industrial environments, we propose a novel industrial time series prediction method based on adaptive continual learning." (p.9)

## Gap transitions

- however (abstract): "However, the dynamic changes in industrial processes present a key challenge for data-driven models." (p.1)
- to address (abstract): "To address these issues, this article proposes an adaptive continual learning method for nonstationary industrial time series prediction." (p.1)
- therefore (introduction): "Therefore, traditional static models, which are based on the assumption of independent and identically distributed (i.i.d.)[4], face challenges in effectively adapting to nonstationary industrial settings." (p.1)
- however (introduction): "However, continual learning strategies offer a solution for effectively training and updating neural networks on nonstationary industrial data." (p.1)
- in contrast (introduction): "In contrast, this article not only compares various continual learning methods and paradigms, but also introduces an adaptive continual learning method specifically tailored for nonstationary industrial time series prediction." (p.2)
- despite (conclusion): "Despite its effectiveness, our method has certain limitations." (p.9)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes an adaptive continual learning method"; "we propose a novel industrial time series prediction method"
- introduce / causal / introduction: "we introduce intermediate representations as “hints” and propose hint-based network parameter learning."
- validate / causal / abstract: "the superiority of our method is validated on solar power generation data and real data of grinding and grading process."
- demonstrate / causal / experiments: "Our method demonstrates favorable performance in terms of mean error and overcoming forgetting"

## Cross-section linkers

- introduction → related work: 贡献列表后直接 `II. CONTINUAL LEARNING`，无节序路标 (p.2)
- related work → method: 问题陈述后直接 `III. PROPOSED METHOD` (p.3)
- method → experiments: TimeRelu 叙述后直接 `IV. EXPERIMENTAL VERIFICATION` (p.5)
- experiments → conclusion: 资源效率分析后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `this article proposes`，缺口句先写两种常见更新路径再转折。
- R002 独立 `II. CONTINUAL LEARNING`，先方法族综述再给问题陈述。
- R003 贡献用 `the contributions of the article are as follows.` + 编号列表。
- R004 Experiments 标题用 `EXPERIMENTAL VERIFICATION`。
- R005 Conclusion 用 `Finally, to address ... we propose`，再用 `Despite its effectiveness` 承认局限。

## Candidate phrases

- `To address these issues, this article proposes an adaptive continual learning method` (abstract)
- `In contrast, this article not only compares ... but also introduces` (introduction)
- `Based on the above analysis, the contributions of the article are as follows.` (introduction)
- `To verify the effectiveness of our proposed ... method, we conducted experiments using` (experiments)
- `Finally, to address the problem of ... we propose a novel` (conclusion)

## House style

自称是 `this article` / `Our approach` / `we propose` / `our method`。未见 `Here we`。未见 `In this paper`。`this article proposes` 与 `our method` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Deep learning models have gained significant attention and application in recent years to improve the accuracy and efficiency of industrial time series prediction.
- p.1 abstract: However, the dynamic changes in industrial processes present a key challenge for data-driven models.
- p.1 abstract: To address these issues, this article proposes an adaptive continual learning method for nonstationary industrial time series prediction.
- p.1 abstract: Compared with other update methods and different continual learning methods, the superiority of our method is validated on solar power generation data and real data of grinding and grading process.
- p.1 introduction: INDUSTRIAL time series data, as a kind of structured data that reflects information of production processes, can be analyzed and modeled to better understand the operation of industrial systems or equipment, optimize and guide the production processes, etc.
- p.1 introduction: Therefore, traditional static models, which are based on the assumption of independent and identically distributed (i.i.d.)[4], face challenges in effectively adapting to nonstationary industrial settings.
- p.2 introduction: In contrast, this article not only compares various continual learning methods and paradigms, but also introduces an adaptive continual learning method specifically tailored for nonstationary industrial time series prediction.
- p.2 introduction: Based on the above analysis, the contributions of the article are as follows.
- p.2 related_work: Continual learning is a machine learning paradigm that enables models to learn and adapt to new data distributions by leveraging existing knowledge and experience, without retraining or discarding old knowledge.
- p.3 method: We tailored the continual learning methods for nonstationary time series forecasting tasks in two aspects.
- p.5 experiments: To verify the effectiveness of our proposed industrial time series prediction method based on adaptive continual learning, we conducted experiments using open-source solar power generation datasets and real grinding and grading process datasets.
- p.9 conclusion: Finally, to address the problem of accuracy degradation of prediction models in nonstationary industrial environments, we propose a novel industrial time series prediction method based on adaptive continual learning.
- p.9 conclusion: Despite its effectiveness, our method has certain limitations.
- p.9 conclusion: Given these limitations, we plan to continue our research to overcome these challenges in the future.
