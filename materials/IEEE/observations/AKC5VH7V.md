---
key: AKC5VH7V
title: "DLformer: A Dynamic Length Transformer-Based Network for Efficient Feature Representation in Remaining Useful Life Prediction"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2023.3257038"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,9-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. DLFORMER-BASED NETWORK` → `IV` 实验设置 → `V` 实验结果 → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work。`related_work=independent`。Related Work 分 data-driven RUL 与 efficient networks。Introduction 末有 `The rest of this article is organized as follows` 路标，指向 Section II–VI。Experiments 拆成 setting（IV）与 results（V）。

## Openers

- abstract: `Representation learning-based remaining` — "Representation learning-based remaining useful life (RUL) prediction plays a crucial role in improving the security and reducing the maintenance cost of complex systems." (p.1)
- introduction: `COMPLEX system intelligent maintenance` — "COMPLEX system intelligent maintenance is highly important to increase system reliability, enhance operational safety, and reduce maintenance cost." (p.1)
- method: `In this section, we first` — "In this section, we first describe the framework of DLformer and then present the proposed method in detail." (p.3, III)
- experiments: `To evaluate the performance` — "To evaluate the performance of dynamic architecture, we first deactivate the early exit and display the RMSE." (p.9, V.C)
- conclusion: `In this article, a transformer-based` — "In this article, a transformer-based dynamic length neural network, namely, DLformer, is proposed for efficient representation learning." (p.10)

## Gap transitions

- despite (abstract): "Despite the superior performance, the high computational cost of deep networks hinders deploying the models on low-compute platforms." (p.1)
- in contrast (abstract): "In contrast to most RUL prediction methods that learn features of the same sequence length, we consider that each time series has its characteristics and the sequence length should be adjusted adaptively." (p.1)
- therefore (abstract): "Therefore, we focus on sequence length and propose a dynamic length transformer (DLformer) that can adaptively learn sequence representation of different lengths." (p.1)
- however (introduction): "However, most existing methods on speeding up networks focus on reducing the computational redundancy in compressing the network [16], [17], [18] or adjusting the network width or depth [19], [20], [21]." (p.2)
- therefore (related work): "Therefore, it is a challenge that designs dynamic networks and confidence strategies for RUL prediction." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we ... propose a dynamic length transformer (DLformer)"; "we propose a novel dynamic length transformer (DLformer)-based network"; "namely, DLformer, is proposed"
- consider / speculative / abstract: "we consider that each time series has its characteristics"
- show / causal / abstract, experiments: "Experiments on multiple datasets show that DLformer can increase up to 90% inference speed"; "The results demonstrate that the proposed confidence strategy can distinguish “hard” and “easy” samples"
- demonstrate / causal / experiments, conclusion: "Experimental results on multi-datasets demonstrate that DLformer significantly reduces the computational cost"
- will develop / speculative / conclusion: "In the future, we will develop a dynamic approach that can automatically filter out unimportant time steps"

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II introduces the related work about the method for RUL prediction and efficient networks. Section III describes the proposed network in detail. In Section IV, the experimental setting is presented. Experimental results are discussed in Section V. Finally, Section VI concludes this article." (p.2)
- related work → method: 分类动态网络局限后 `III. DLFORMER-BASED NETWORK` (p.3)
- method → experiments: 框架与特征提取后进入实验设置 / 结果 (p.9)
- experiments → conclusion: 推理速度段落后 `VI. CONCLUSION` (p.10)

## Candidate rules

- R001 abstract 用 `Despite` 收性能，再 `Therefore, we focus on ... and propose`。
- R002 独立 Related Work，分 RUL 数据驱动方法与 efficient networks。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The main contribution of this article can be summarized as follows.` + 编号。
- R005 Conclusion 用 `In this article, ... is proposed` 收回，再用 `In the future, we will develop`。

## Candidate phrases

- `Despite the superior performance, the high computational cost` (abstract)
- `Therefore, we focus on sequence length and propose` (abstract)
- `The main contribution of this article can be summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a transformer-based dynamic length neural network, namely, DLformer, is proposed` (conclusion)
- `In the future, we will develop a dynamic approach that` (conclusion)

## House style

自称 `we propose` / `we consider` / `this article` / `In this article` / `our methods`。未见 `Here we`、`In this paper`。`In this article ... is proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Representation learning-based remaining useful life (RUL) prediction plays a crucial role in improving the security and reducing the maintenance cost of complex systems.
- p.1 abstract: Despite the superior performance, the high computational cost of deep networks hinders deploying the models on low-compute platforms.
- p.1 abstract: In contrast to most RUL prediction methods that learn features of the same sequence length, we consider that each time series has its characteristics and the sequence length should be adjusted adaptively.
- p.1 abstract: Therefore, we focus on sequence length and propose a dynamic length transformer (DLformer) that can adaptively learn sequence representation of different lengths.
- p.1 abstract: Experiments on multiple datasets show that DLformer can increase up to 90% inference speed, with less than 5% degradation in model accuracy.
- p.1 introduction: COMPLEX system intelligent maintenance is highly important to increase system reliability, enhance operational safety, and reduce maintenance cost.
- p.2 introduction: However, most existing methods on speeding up networks focus on reducing the computational redundancy in compressing the network [16], [17], [18] or adjusting the network width or depth [19], [20], [21].
- p.2 introduction: To deal with this issue, we propose a novel dynamic length transformer (DLformer)-based network, aiming to adaptively learn feature representation of different lengths conditioned on each sample.
- p.2 introduction: The main contribution of this article can be summarized as follows.
- p.2 introduction: The rest of this article is organized as follows. Section II introduces the related work about the method for RUL prediction and efficient networks. Section III describes the proposed network in detail. In Section IV, the experimental setting is presented. Experimental results are discussed in Section V. Finally, Section VI concludes this article.
- p.3 related work: Therefore, it is a challenge that designs dynamic networks and confidence strategies for RUL prediction.
- p.3 method: In this section, we first describe the framework of DLformer and then present the proposed method in detail.
- p.9 experiments: To evaluate the performance of dynamic architecture, we first deactivate the early exit and display the RMSE.
- p.9 experiments: The results demonstrate that the proposed confidence strategy can distinguish “hard” and “easy” samples, that is, “easy” samples are output in exit 1 and “hard” samples are output in the later exits.
- p.10 conclusion: In this article, a transformer-based dynamic length neural network, namely, DLformer, is proposed for efficient representation learning.
- p.10 conclusion: Experimental results on multi-datasets demonstrate that DLformer significantly reduces the computational cost and achieves comparable performance to the transformer network.
- p.10 conclusion: In the future, we will develop a dynamic approach that can automatically filter out unimportant time steps to reduce computational costs.
