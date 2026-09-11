---
key: 9C9JX4ZS
title: "Latent Probabilistic Dynamic Embedding Supervised Deep Networks With Graph-Guiding for Soft Sensing in Industrial Process"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2025.3643840"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. VARIATIONAL RECURRENT NEURAL NETWORK` → `III. LATENT PROBABILISTIC DYNAMICS EMBEDDING SUPERVISED DEEP NETWORKS WITH GRAPH-GUIDING FOR SOFT SENSING` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners–` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 STAE、dynamic AE/ARAE、RNN/LSTM/GRU、VRNN、VGAE）。II 是 VRNN 预备，不是 Related Work。Introduction 末为编号贡献，无 `The rest of this article is organized` 路标。Method 在 III。Experiments 标题为 `CASE STUDIES`（debutanizer + SRU）。

## Openers

- abstract: `Given the pervasive` — "Given the pervasive presence of feedback mechanisms and inertial loops inherent in industrial processes, increasing research efforts have focused on integrating latent feature dynamics into deep learning architectures to address the issue of strong dynamic autocorrelation in industrial processes." (p.1)
- introduction: `MONITORING, optimising, and controlling` — "MONITORING, optimising, and controlling quality variables is an important aspect of a modern chemical process [1]." (p.1)
- method: `Inspired by predictable` — "Inspired by predictable feature analysis (PFA) [33], [34] [35], a probabilistic dynamic model was developed within latent features to handle complex temporal dependencies in order to capture dynamic features within processes." (p.3, III)
- experiments: `In this section` — "In this section, we validate the proposed GLPDSDN algorithm using a real industrial process." (p.7, IV)
- conclusion: `This article proposed` — "This article proposed a new approach called latent probabilistic dynamic embedding supervised deep networks for soft sensing in industrial processes." (p.14)

## Gap transitions

- however (abstract): "However, the complex temporal dependencies present in latent features and the limitations imposed by traditional alternating training methods have already constrained the performance of such models." (p.1)
- unfortunately (introduction): "Unfortunately, the limitation in extracting dynamic process information hinders their widespread application in soft sensing of industrial processes [9], [10] [11]." (p.1)
- however (introduction): "However, these variations capture the dynamics of latent features by minimizing the variability between an individual feature and a fixed transformation of its previous features." (p.2)
- nevertheless (introduction): "Nevertheless, there is also a strong limitation that the temporal neighborhood structure of the latent variable is stretched or distorted and is different from that of the original data when the original data undergoes a nonlinear transformation." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a latent probabilistic dynamics embedding supervised deep networks for soft sensing"; "we propose a latent probabilistic dynamics embedding supervised deep networks with graph-guiding (GLPDSDN)"
- demonstrate / causal / abstract: "the proposed methods are implemented on two real industrial cases to demonstrate their effectiveness and superiority"
- introduce / causal / abstract: "The article introduces a new approach involving a probability-distribution-based predictive regularization term"
- proposed / causal / conclusion: "This article proposed a new approach"

## Cross-section linkers

- introduction → background: 编号贡献后直接 `II. VARIATIONAL RECURRENT NEURAL NETWORK`，无独立路标句 (p.3)
- background → method: VRNN 推导后接 `III. LATENT PROBABILISTIC DYNAMICS EMBEDDING SUPERVISED DEEP NETWORKS WITH GRAPH-GUIDING FOR SOFT SENSING` (p.3)
- method → experiments: Algorithm 1 / Fig. 4 后接 `IV. CASE STUDIES` (p.7)
- experiments → conclusion: 消融段落后直接 `V. CONCLUSION` (p.14)

## Candidate rules

- R001 abstract 用 `In this paper, we propose` / `The article introduces`，不用 `Here we`。
- R002 TASE 前置 `Note to Practitioners`。
- R003 Introduction 无独立 Related Work；II 为 VRNN 预备节。
- R004 贡献用 `The main contributions are:` + 编号列表。
- R005 Experiments 标题为 `CASE STUDIES`。
- R006 Conclusion 用过去时 `This article proposed`，再用 `Future research will focus on` 指向后续。

## Candidate phrases

- `In this paper, we propose a latent probabilistic dynamics embedding supervised deep networks for soft sensing.` (abstract)
- `The article introduces a new approach involving` (abstract)
- `Motivated by the aforementioned considerations, we propose` (introduction)
- `This article proposed a new approach called` (conclusion)
- `Future research will focus on soft sensor modeling of dynamic processes` (conclusion)

## House style

自称是 `In this paper, we propose` / `The article introduces` / `we propose` / `This article proposed`。未见 `Here we`。`In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。结论用过去时 `This article proposed`。

## Quotes

- p.1 abstract: Given the pervasive presence of feedback mechanisms and inertial loops inherent in industrial processes, increasing research efforts have focused on integrating latent feature dynamics into deep learning architectures to address the issue of strong dynamic autocorrelation in industrial processes.
- p.1 abstract: However, the complex temporal dependencies present in latent features and the limitations imposed by traditional alternating training methods have already constrained the performance of such models.
- p.1 abstract: In this paper, we propose a latent probabilistic dynamics embedding supervised deep networks for soft sensing.
- p.1 abstract: The article introduces a new approach involving a probability-distribution-based predictive regularization term for latent features.
- p.1 abstract: Finally, the proposed methods are implemented on two real industrial cases to demonstrate their effectiveness and superiority.
- p.1 introduction: MONITORING, optimising, and controlling quality variables is an important aspect of a modern chemical process [1].
- p.1 introduction: Unfortunately, the limitation in extracting dynamic process information hinders their widespread application in soft sensing of industrial processes [9], [10] [11].
- p.2 introduction: Nevertheless, there is also a strong limitation that the temporal neighborhood structure of the latent variable is stretched or distorted and is different from that of the original data when the original data undergoes a nonlinear transformation.
- p.2 introduction: Motivated by the aforementioned considerations, we propose a latent probabilistic dynamics embedding supervised deep networks with graph-guiding (GLPDSDN), in which all the parameters of the entire network are adjusted simultaneously using a comprehensive optimizer instead of training the network iteratively.
- p.2 introduction: The main contributions are:
- p.3 method: Inspired by predictable feature analysis (PFA) [33], [34] [35], a probabilistic dynamic model was developed within latent features to handle complex temporal dependencies in order to capture dynamic features within processes.
- p.7 experiments: In this section, we validate the proposed GLPDSDN algorithm using a real industrial process.
- p.14 conclusion: This article proposed a new approach called latent probabilistic dynamic embedding supervised deep networks for soft sensing in industrial processes.
- p.14 conclusion: From the evaluation metrics, the GLPDSDN model has at least 31.1% and 36.8% improvement in MAE, 32.8% and 52.1% improvement in RMSE, and 39.9% and 36.9% improvement in R2 compared with competitive methods on the debutanizer and SRU, respectively.
- p.14 conclusion: Future research will focus on soft sensor modeling of dynamic processes based on irregularly sampled data and developing dynamic graph-guided terms using high-precision models based on systems of time differential equations to address the rapid and significant fluctuations in process data.
