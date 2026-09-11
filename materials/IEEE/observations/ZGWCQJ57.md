---
key: ZGWCQJ57
title: "A Cloud-Edge Collaborative Soft Sensing Framework for Multiperformance Indicators of Manufacturing Processes With Irregular Sampling"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3488152"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. Introduction` → `II. Problem formulation` → `III. Proposed Framework` → `IV. Case Study` → `V. Conclusion`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SVR/PLS/BP/RF、深度学习 CNN/transformer/LSTM/GRU、不规则采样、cloud-edge collaboration）。Introduction 末有节序路标，指向 Section II–V。作者接受稿，页眉 `VOL. XX, NO. XX`。Experiments 标题为 `Case Study`。

## Openers

- abstract: `In the process` — "In the process industry production, the online sensing of process performance is very important for the optimization and control of the manufacturing process." (p.1)
- introduction: `WITH the wide` — "WITH the wide application of distributed control systems and the great development of information technology, modern manufacturing industries present complex, multi-system, and intelligent characteristics." (p.1)
- method: `This section introduces` — "This section introduces a cloud-edge collaborative soft sensing framework and the proposed model, and describes the structure and algorithm of the proposed model." (p.2, III)
- experiments: `In order to` — "In order to verify the effectiveness and superiority of the method proposed in this paper, some experiments are carried out through the hot strip rolling process." (p.5, IV)
- conclusion: `In this paper` — "In this paper, we propose a cloud-edge collaborative soft sensing modeling framework for multi-quality indicators prediction of industrial processes with irregular sampling." (p.9)

## Gap transitions

- however (abstract): "However, the information island is formed by long processes and multiple systems of complex production processes." (p.1)
- in order to (abstract): "In order to solve the above problems, a cloud-edge collaborative soft sensing framework for multi-performance indicators prediction of manufacturing processes with non-regular sampling is proposed." (p.1)
- therefore (introduction): "Therefore, from the perspective of improving the product quality and the process efficiency, it is urgent to establish an online soft sensor system with multiple performance indicators based on raw material composition and process parameters." (p.1)
- however (introduction): "However, machine learning methods are limited in their abilities to solve the problems such as strong coupling, strong nonlinearity, and temporality in complex industrial processes." (p.1)
- although (introduction): "Although above modeling methods solve the problem of multivariate, nonlinear, and strongly coupled data in industrial processes to some extent, they assume that the data sampling intervals are equal and regular." (p.1)
- although (introduction): "Although the above methods are able to realize soft sensing of performance indicators in industrial processes to a certain extent, they mostly focus on the temporal characteristic, nonlinearities, and high-dimensionality of industrial processes." (p.2)

## Hedge verbs

- is proposed / causal / abstract, introduction: "a cloud-edge collaborative soft sensing framework ... is proposed"; "This paper proposes a cloud-edge collaborative soft sensing framework"
- we propose / causal / conclusion: "In this paper, we propose a cloud-edge collaborative soft sensing modeling framework"
- will next / speculative / conclusion: "we will next explore the correlation between the sampling points to improve the accuracy and real-time performance of soft sensing"

## Cross-section linkers

- introduction → problem: "The rest of the paper is organized as follows. Section II contains the problem description. The prediction framework proposed in this paper and its details are presented in section III. Section IV presents the details of the case study and the experiments, and section V gives the conclusions of this paper and the outlook for future work." (p.2)
- method → experiments: Algorithm 1–2 后 `IV. Case Study` (p.5)
- experiments → conclusion: 分钢种预测后 `V. Conclusion` (p.9)

## Candidate rules

- R002 Introduction 无独立 Related Work，机器学习 / 深度学习 / 不规则采样 / 云边协同评述写在引言中段，并以 `Although the above methods` 收束缺口。
- R003 Introduction 末用 `The rest of the paper is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions in this paper are as follows` + 编号列表。
- R005 Conclusion 先 `In this paper, we propose` 收回框架，再用 `we will next explore` 指向后续。

## Candidate phrases

- `In order to solve the above problems, a ... is proposed` (abstract)
- `This paper proposes a cloud-edge collaborative` (introduction)
- `The main contributions in this paper are as follows:` (introduction)
- `The rest of the paper is organized as follows.` (introduction)
- `In this paper, we propose a` (conclusion)

## House style

自称以 `this paper` / `we propose` / `we establish` 为主。未见 `Here we`、`this article`。`In this paper, we propose` 与 `This paper proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In the process industry production, the online sensing of process performance is very important for the optimization and control of the manufacturing process.
- p.1 abstract: However, the information island is formed by long processes and multiple systems of complex production processes.
- p.1 abstract: In order to solve the above problems, a cloud-edge collaborative soft sensing framework for multi-performance indicators prediction of manufacturing processes with non-regular sampling is proposed.
- p.1 introduction: WITH the wide application of distributed control systems and the great development of information technology, modern manufacturing industries present complex, multi-system, and intelligent characteristics.
- p.1 introduction: Therefore, from the perspective of improving the product quality and the process efficiency, it is urgent to establish an online soft sensor system with multiple performance indicators based on raw material composition and process parameters.
- p.1 introduction: However, machine learning methods are limited in their abilities to solve the problems such as strong coupling, strong nonlinearity, and temporality in complex industrial processes.
- p.1 introduction: Although above modeling methods solve the problem of multivariate, nonlinear, and strongly coupled data in industrial processes to some extent, they assume that the data sampling intervals are equal and regular.
- p.2 introduction: Although the above methods are able to realize soft sensing of performance indicators in industrial processes to a certain extent, they mostly focus on the temporal characteristic, nonlinearities, and high-dimensionality of industrial processes.
- p.2 introduction: This paper proposes a cloud-edge collaborative soft sensing framework for the prediction of multi-quality indicators of industrial processes with irregular sampling.
- p.2 introduction: The main contributions in this paper are as follows:
- p.2 introduction: The rest of the paper is organized as follows. Section II contains the problem description. The prediction framework proposed in this paper and its details are presented in section III. Section IV presents the details of the case study and the experiments, and section V gives the conclusions of this paper and the outlook for future work.
- p.2 method: This section introduces a cloud-edge collaborative soft sensing framework and the proposed model, and describes the structure and algorithm of the proposed model.
- p.5 experiments: In order to verify the effectiveness and superiority of the method proposed in this paper, some experiments are carried out through the hot strip rolling process.
- p.9 conclusion: In this paper, we propose a cloud-edge collaborative soft sensing modeling framework for multi-quality indicators prediction of industrial processes with irregular sampling.
- p.9 conclusion: The method proposed in this paper is able to realize soft sensing of multi-performance indicators for products with irregular sampling in industrial processes, and the results are significantly better than those of existing methods.
- p.9 conclusion: In order to further analyze the trend of the performance between batches, we will next explore the correlation between the sampling points to improve the accuracy and real-time performance of soft sensing.
