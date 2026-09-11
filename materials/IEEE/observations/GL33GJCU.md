---
key: GL33GJCU
title: "Hybrid Parallel Stochastic Configuration Networks for Industrial Data Analytics"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2021.3096840"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RLEATED WORK`（PDF 标题拼写） → `III. HYBRID PARALLEL SCNS` → `IV. PERFORMANCE EVALUATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（节题为 `RLEATED WORK`）。Introduction 末有 `The rest of this article is organized as follows`。Method 在 III。Experiments 标题为 `PERFORMANCE EVALUATION`。

## Openers

- abstract: `As a class` — "As a class of randomized learner model, stochastic configuration networks (SCNs) have been successfully applied in a few data analytics tasks." (p.2331)
- introduction: `AS THE development` — "AS THE development of computer, communication, and automation technologies, industrial control systems are able to operate and stabilize processes." (p.2331)
- related_work: `Generally, the task` — "Generally, the task of soft sensor modeling is to find the most appropriate nonlinear function f to meet the mapping between the auxiliary variables x that are easy to measure and the primary variables y that are difficult to directly measure." (p.2332, II.A)
- method: `This section details` — "This section details HPSCNs." (p.2333, III)
- experiments: `In this article` — "In this article, root mean squares error (RMSE) is used to evaluate the modeling accuracy and calculate the error tolerance" (p.2336, IV)
- conclusion: `To improve the` — "To improve the performance of SCNs in industrial soft sensor development with large-scale dataset, this article proposed a model and data hybrid parallel incremental learning method for SCNs, called HPSCNs." (p.2340)

## Gap transitions

- however (abstract): "Given the industrial big data modeling tasks, however, the original SCNs potentially lead to excessive training time." (p.2331)
- to this end (abstract): "To this end, this article extends SCNs to a hybrid parallel version, termed hybrid parallel SCNs (HPSCNs)." (p.2331)
- however (introduction): "However, due to technical difficulties and high investment costs, some key variables are usually hard-to-measured in real factories, which may make the available measurement information insufficient for optimization and control purposes." (p.2331)
- however (introduction): "However, those distributed versions both adopted the alternating direction method of multipliers algorithm to build the global unified model, which hardly achieve a good tradeoff between the rapid convergence and fast training." (p.2332)
- motivated (introduction): "Motivated by this industrial practical problem, this article proposes a novel model-data hybrid parallel-incremental learning method for SCNs, called HPSCNs." (p.2332)
- however (conclusion): "However, HPSCN directly selects new nodes according to the residual errors of the two different incremental learning method." (p.2340)

## Hedge verbs

- extend / causal / abstract: "this article extends SCNs to a hybrid parallel version"
- propose / causal / abstract, introduction: "this article proposes an adaptive hyperparameter adjustment method"; "this article proposes a novel model-data hybrid parallel-incremental learning method"
- show / causal / abstract, conclusion: "showing the effectiveness of the proposed algorithm"; "Experimental analysis and investigation show that compared with the original incremental learning methods, HPSCN can achieve fast construction and best comprehensive performance"

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. Section II briefly describes the problem overview and SCNs with point and block increments. Section III introduces hybrid parallel SCNs (HPSCNs) in detail, including theoretical analysis and algorithm description. Then, Section IV reports the performance evaluation results. Finally, Section V concludes this article." (p.2332)
- related_work → method: II.C Remark 后 `III. HYBRID PARALLEL SCNS` (p.2333)
- method → experiments: Algorithm 后 `IV. PERFORMANCE EVALUATION` (p.2336)
- experiments → conclusion: 工业案例后 `V. CONCLUSION` (p.2340)

## Candidate rules

- R006 独立 Related Work（本节题拼写为 `RLEATED WORK`）。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this article are summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `However` 承认冗余节点，再给后续方向。
- R009 结论 `this article proposed a ... method`。

## Candidate phrases

- `To this end, this article extends` (abstract)
- `Motivated by this industrial practical problem, this article proposes` (introduction)
- `The main contributions of this article are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `Experimental analysis and investigation show that` (conclusion)

## House style

自称是 `this article extends` / `this article proposes` / `our proposed algorithms` / `In this article`。未见 `Here we`、`In this paper`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.2331 abstract: As a class of randomized learner model, stochastic configuration networks (SCNs) have been successfully applied in a few data analytics tasks.
- p.2331 abstract: Given the industrial big data modeling tasks, however, the original SCNs potentially lead to excessive training time.
- p.2331 abstract: To this end, this article extends SCNs to a hybrid parallel version, termed hybrid parallel SCNs (HPSCNs).
- p.2331 abstract: Finally, a practical industrial application case is made, where a grinding particle size soft sensor is developed based on HPSCN, showing the effectiveness of the proposed algorithm.
- p.2331 introduction: AS THE development of computer, communication, and automation technologies, industrial control systems are able to operate and stabilize processes.
- p.2331 introduction: However, due to technical difficulties and high investment costs, some key variables are usually hard-to-measured in real factories, which may make the available measurement information insufficient for optimization and control purposes.
- p.2332 introduction: Motivated by this industrial practical problem, this article proposes a novel model-data hybrid parallel-incremental learning method for SCNs, called HPSCNs.
- p.2332 introduction: The main contributions of this article are summarized as follows.
- p.2332 introduction: The rest of this article is organized as follows. Section II briefly describes the problem overview and SCNs with point and block increments. Section III introduces hybrid parallel SCNs (HPSCNs) in detail, including theoretical analysis and algorithm description. Then, Section IV reports the performance evaluation results. Finally, Section V concludes this article.
- p.2332 related_work: Generally, the task of soft sensor modeling is to find the most appropriate nonlinear function f to meet the mapping between the auxiliary variables x that are easy to measure and the primary variables y that are difficult to directly measure.
- p.2333 method: This section details HPSCNs.
- p.2336 experiments: In this article, root mean squares error (RMSE) is used to evaluate the modeling accuracy and calculate the error tolerance
- p.2337 experiments: In order to verify the effectiveness of our proposed algorithms, comparisons among HPSCN, SCN with point increments (SCN) [11], SCN with block increments (BSCN) [23] are made through four benchmark regression cases and a real industrial soft sensing case.
- p.2340 conclusion: To improve the performance of SCNs in industrial soft sensor development with large-scale dataset, this article proposed a model and data hybrid parallel incremental learning method for SCNs, called HPSCNs.
- p.2340 conclusion: Experimental analysis and investigation show that compared with the original incremental learning methods, HPSCN can achieve fast construction and best comprehensive performance.
- p.2340 conclusion: However, HPSCN directly selects new nodes according to the residual errors of the two different incremental learning method.
- p.2340 conclusion: Therefore, it is a meaningful way to reduce the redundant hidden nodes whereas retaining the advantage of block increments for extremely fast modeling.
