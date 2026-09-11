---
key: EP4RM8PN
title: "A study of model adaptation in iterative real-time optimization of processes with uncertainties"
venue: "Computers & Chemical Engineering"
doi: "10.1016/j.compchemeng.2018.08.001"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries`（`2.1. Problem formulation`、`2.2. Modifier adaptation`、`2.3. Model adequacy`、`2.4. Convex model approximations`）→ `3. Effective model adaptation`（`3.1. Enforcing model adequacy in the framework of EMA`）→ `4. Simulation study`（`4.1. Process description`、`4.2. Performance without enforcing model adequacy`、`4.3. Performance with enforcing model adequacy`）→ `5. Conclusions`。前置 `ABSTRACT`、`ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 two-step、ISOPE、IGMO、MA、MAWQA、EMA）。Introduction 末有节序路标。Experiments 标题为 `4. Simulation study`（青霉素补料分批反应器 batch-to-batch）。结论节标题为 `Conclusions`（复数）。

## Openers

- abstract: `In real-time` — "In real-time optimization, plant-model mismatch can be handled by adding bias and gradient correction terms to the model-based optimization problem in order to meet the first-order necessary conditions of optimality."
- introduction: `Real-time optimization` — "Real-time optimization (RTO) is used widely to operate industrial processes at economically optimal operating conditions without compromising product quality and process constraints."
- related_work: `The two-step` — "The two-step scheme uses the plant measurements to adapt some of the model parameters such that the model predicts the measured plant outputs well and new operating conditions are computed based on the updated model (Chen and Joseph, 1987; Darby et al., 2011; Jang et al., 1987)."
- method: `Another possible way` — "Another possible way to handle the issue of model adequacy is to adapt the model parameters θ such that the second-order optimality condition can be satisfied iteratively." (s.3)
- experiments: `We investigate the` — "We investigate the performance of the proposed iterative RTO scheme and compare it with different RTO approaches that use model adaptation or a fixed model on a case study of batch-to-batch optimization a fed-batch reactor for penicillin production." (s.4)
- conclusion: `This article proposes` — "This article proposes to perform parameter estimation in order to improve the quality of the model in iterative real-time optimization with modifier adaptation."

## Gap transitions

- however (abstract): "However, since these correction terms do not ensure the satisfaction of the second-order condition of optimality upon convergence, the model that is used in the optimization can be inadequate."
- however (introduction): "However, if there is a structural mismatch, the two-step scheme may not converge to the true plant optimum (Forbes et al., 1994)."
- however (introduction): "However, the traditional MA does not guarantee to reach the plant-optimum if the process model is not adequate."
- unfortunately (s.2.3): "Unfortunately, due to the lack of prior knowledge of the plant optimum, the model-adequacy condition cannot be verified aforehand."
- however (s.3.1): "However, minimizing the output prediction error does not guarantee that the updated model will satisfy the model adequacy criterion even if there exists such values of the parameters which make the model adequate for the modified optimization problem (5)."
- despite (s.4.2): "Despite the presence of structural and parametric mismatch, it can be observed that the predictions of the model are close to the measurements of the plant."
- despite (conclusion): "Despite the fact that accurate plant gradients were available, the standard MA scheme was not capable of converging to the plant optimum as shown in the simulation study."

## Hedge verbs

- proposes / causal / abstract: "this paper proposes to only use effective model parameter updates to ensure and to speed up the convergence to the process optimum"
- shows / causal / abstract: "this paper shows that model adequacy can and should be enforced explicitly in model parameter adaptation"
- demonstrate / causal / abstract: "we demonstrate that the proposed model adaptation procedure computes model parameters which make the iterative real-time optimization with modifier-adaptation converge faster and more reliably to the plant optimum"
- will show / causal / s.2.3: "In this contribution, we will show how the use of model adaptation can remedy this deficiency."
- investigate / associative / experiments: "We investigate the performance of the proposed iterative RTO scheme"
- proposes / causal / conclusion: "This article proposes to perform parameter estimation"
- propose / causal / conclusion: "we propose to enforce the model adequacy via slack variables in the objective of the parameter estimation problem"
- will be studied / associative / conclusion: "The combination of this approach with EMA-EA and the analysis of the model inadequacy issue in the presence of measurement noise will be studied in future work."

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows. Section 2 formulates the RTO optimization problem under plant-model mismatch and reviews the concept of MA, model adequacy and convex model approximations for MA. Section 3 presents the EMA scheme and proposes EMA with an explicit model adequacy criterion in the model adaptation. Section 4 presents a simulation study for the iterative (batch to batch) optimization of a fed-batch reactor for the production of penicillin that demonstrates the performance of the proposed scheme. Finally, Section 5 provides a summary and conclusions."
- method → experiments: 松弛变量参数估计段落后 `4. Simulation study`
- experiments → conclusion: 阻尼矩阵比较段落后 `5. Conclusions`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is organized as follows`
- R009 自称：`this paper proposes` / `This article proposes` / `we demonstrate` / `we propose` / `This contribution focuses`
- 实验节标题为 `Simulation study`；结论节标题为 `Conclusions`（复数）。

## Candidate phrases

- `this paper proposes to only use effective model parameter updates` (abstract)
- `Additionally, this paper shows that model adequacy can and should be enforced explicitly` (abstract)
- `we demonstrate that the proposed model adaptation procedure` (abstract)
- `This contribution focuses on improving the reliability of EMA` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `This article proposes to perform parameter estimation` (conclusion)
- `Furthermore, we propose to enforce the model adequacy via slack variables` (conclusion)

## House style

自称 `this paper proposes` / `this paper shows` / `This article proposes` / `we demonstrate` / `we propose` / `This contribution focuses` / `In this study`。第一人称复数与 `this paper` / `this article` 并用。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: In real-time optimization, plant-model mismatch can be handled by adding bias and gradient correction terms to the model-based optimization problem in order to meet the first-order necessary conditions of optimality.
- abstract: However, since these correction terms do not ensure the satisfaction of the second-order condition of optimality upon convergence, the model that is used in the optimization can be inadequate.
- abstract: In the framework of iterative modifier-adaptation, this paper proposes to only use effective model parameter updates to ensure and to speed up the convergence to the process optimum.
- abstract: Additionally, this paper shows that model adequacy can and should be enforced explicitly in model parameter adaptation.
- abstract: By means of a simulation study of maximizing the product yield in a fed-batch reactor, we demonstrate that the proposed model adaptation procedure computes model parameters which make the iterative real-time optimization with modifier-adaptation converge faster and more reliably to the plant optimum.
- introduction: Real-time optimization (RTO) is used widely to operate industrial processes at economically optimal operating conditions without compromising product quality and process constraints.
- introduction: However, if there is a structural mismatch, the two-step scheme may not converge to the true plant optimum (Forbes et al., 1994).
- introduction: However, the traditional MA does not guarantee to reach the plant-optimum if the process model is not adequate.
- introduction: This contribution focuses on improving the reliability of EMA by explicitly considering the adequacy criterion in the parameter estimation step.
- introduction: The rest of this paper is organized as follows.
- related work: The two-step scheme uses the plant measurements to adapt some of the model parameters such that the model predicts the measured plant outputs well and new operating conditions are computed based on the updated model (Chen and Joseph, 1987; Darby et al., 2011; Jang et al., 1987).
- method: Another possible way to handle the issue of model adequacy is to adapt the model parameters θ such that the second-order optimality condition can be satisfied iteratively.
- method: Unfortunately, due to the lack of prior knowledge of the plant optimum, the model-adequacy condition cannot be verified aforehand.
- experiments: We investigate the performance of the proposed iterative RTO scheme and compare it with different RTO approaches that use model adaptation or a fixed model on a case study of batch-to-batch optimization a fed-batch reactor for penicillin production.
- experiments: Despite the presence of structural and parametric mismatch, it can be observed that the predictions of the model are close to the measurements of the plant.
- conclusion: This article proposes to perform parameter estimation in order to improve the quality of the model in iterative real-time optimization with modifier adaptation.
- conclusion: Furthermore, we propose to enforce the model adequacy via slack variables in the objective of the parameter estimation problem to increase the performance of MA with EMA.
- conclusion: Despite the fact that accurate plant gradients were available, the standard MA scheme was not capable of converging to the plant optimum as shown in the simulation study.
- conclusion: The combination of this approach with EMA-EA and the analysis of the model inadequacy issue in the presence of measurement noise will be studied in future work.
