---
key: L8Y3FMJJ
title: "Improving Data-Driven Inferential Sensor Modeling by Industrial Knowledge: A Bayesian Perspective"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2024.3493071"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PRELIMINARIES` → `IV. PROPOSED APPROACH` → `V.` 模型与算法（`Model Architecture Illustration` / `Overall Algorithm`）→ `VI. EXPERIMENTAL RESULTS` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立相关工作节 `II. RELATED WORKS`（GNN inferential sensor / variational inference / technical gaps）。`related_work=independent`。Introduction 末有 `The remainder of this manuscript is organized as follows` 路标，指向 II–VII。Method 拆成知识参数化（IV）与模型算法（V）。Experiments 标题为 `EXPERIMENTAL RESULTS`（CA / PR 两套工业过程）。

## Openers

- abstract: `Accurate quality variable` — "Accurate quality variable inference by process variables is the core of industrial inferential sensor modeling, where recent advancements have seen deep learning (DL) models achieving remarkable success." (p.1)
- introduction: `PREDICTING hard-to-measure` — "PREDICTING hard-to-measure quality variables from high-dimensional easy-to-obtain sensory data plays a crucial role in intelligent manufacturing, supporting decision-making, and enhancing anomaly detection and diagnosis capabilities." (p.1；栏首掉字)
- related work: `This section offers` — "This section offers a concise review of GNN-based data-driven inferential sensor modeling and the application of variational Bayesian inference technique in inferential sensor modeling to highlight existing technical gaps." (p.2)
- method: `In Fig. 2(b)` — "In Fig. 2(b), the model parameters are global parameters, which are shared by all samples." (p.4, IV.A)
- experiments: `In this section` — "In this section, the effectiveness of the proposed approach is validated empirically by answering the following questions." (p.8, VI)
- conclusion: `This study introduced` — "This study introduced a novel GKN model that effectively parameterizes and harnesses knowledge within data-driven industrial inferential sensor modeling to achieve automated knowledge integration." (p.12)

## Gap transitions

- however (abstract): "However, integrating knowledge of unit operations is critical for improving inferential sensor performance, yet it has received little attention." (p.1)
- however (abstract): "However, the divergence computation and normalization constraints are challenging for model implementation." (p.1)
- however (introduction): "However, as industrial processes grow more complex due to technological advancements, obtaining precise mechanistic equations has become increasingly difficult." (p.1)
- despite (introduction): "Despite their successes, integrating prior knowledge into GNNs presents notable challenges." (p.2)
- nevertheless (conclusion): "Nevertheless, several challenges remain unresolved." (p.12)

## Hedge verbs

- introduce / causal / abstract, introduction, conclusion: "this article introduces the gradient knowledge network"; "this article introduces a novel model named gradient knowledge network (GKN)"; "This study introduced a novel GKN model"
- demonstrate / causal / abstract: "various experiments are conducted on two real industrial processes to demonstrate the model's efficacy"
- may / speculative / introduction: "its integration could markedly improve model performance"; "predictive accuracy may be substantially refined"
- show / causal / experiments: "Table I showcases the comparative performance of GKN model"

## Cross-section linkers

- introduction → related work: "The remainder of this manuscript is organized as follows, in Sections II and III, the related works and preliminaries are given to better understand this article. On this basis, the core approach for fusing prior knowledge and data are proposed in Section IV. Consequently, the model expressions and algorithm are summarized in Section V, and experimental analysis is conducted in Section VI. Finally, the conclusions are given in Section VII." (p.2)
- related work → preliminaries: `C. Technical Gaps` 后接 `III. PRELIMINARIES` (p.3)
- method → experiments: Algorithm 2 后接 `VI. EXPERIMENTAL RESULTS` (p.8)
- experiments → conclusion: ablation 后直接 `VII. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `this article introduces` 收回方法，不用 `Here we`。
- R002 独立相关工作标题为 `RELATED WORKS`，末用 `Technical Gaps` 收束。
- R003 Introduction 末用 `The remainder of this manuscript is organized as follows` 指向 II–VII。
- R004 贡献用 `The novelty of this article can be summarized as follows.` + 编号列表。
- R005 Conclusion 用 `This study introduced` 收回，再用 `Nevertheless, several challenges remain unresolved` 指向后续。

## Candidate phrases

- `this article introduces the gradient knowledge network` (abstract)
- `The novelty of this article can be summarized as follows.` (introduction)
- `The remainder of this manuscript is organized as follows` (introduction)
- `This study introduced a novel GKN model that effectively parameterizes` (conclusion)
- `Nevertheless, several challenges remain unresolved.` (conclusion)

## House style

自称是 `this article` / `this study` / `this work` / `the proposed model`。未见 `Here we`。`this article introduces` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Accurate quality variable inference by process variables is the core of industrial inferential sensor modeling, where recent advancements have seen deep learning (DL) models achieving remarkable success.
- p.1 abstract: However, integrating knowledge of unit operations is critical for improving inferential sensor performance, yet it has received little attention.
- p.1 abstract: Addressing this, this article introduces the gradient knowledge network based on the graph neural network’s message-passing mechanism within the variational Bayesian inference framework, which naturally copes with the above-mentioned issues by fusing observational data.
- p.1 introduction: PREDICTING hard-to-measure quality variables from high-dimensional easy-to-obtain sensory data plays a crucial role in intelligent manufacturing, supporting decision-making, and enhancing anomaly detection and diagnosis capabilities.
- p.1 introduction: However, as industrial processes grow more complex due to technological advancements, obtaining precise mechanistic equations has become increasingly difficult.
- p.2 introduction: Despite their successes, integrating prior knowledge into GNNs presents notable challenges.
- p.2 introduction: In summary, this article introduces a novel model named gradient knowledge network (GKN) and its corresponding algorithm based on summarizing the abovementioned techniques.
- p.2 introduction: The novelty of this article can be summarized as follows.
- p.2 introduction: The remainder of this manuscript is organized as follows, in Sections II and III, the related works and preliminaries are given to better understand this article. On this basis, the core approach for fusing prior knowledge and data are proposed in Section IV. Consequently, the model expressions and algorithm are summarized in Section V, and experimental analysis is conducted in Section VI. Finally, the conclusions are given in Section VII.
- p.2 related work: This section offers a concise review of GNN-based data-driven inferential sensor modeling and the application of variational Bayesian inference technique in inferential sensor modeling to highlight existing technical gaps.
- p.3 related work: The discussion above identifies critical technical gaps that motivate this article.
- p.4 method: In Fig. 2(b), the model parameters are global parameters, which are shared by all samples.
- p.8 experiments: In this section, the effectiveness of the proposed approach is validated empirically by answering the following questions.
- p.10 experiments: Table I showcases the comparative performance of GKN model against various baseline models, yielding several insightful observations.
- p.12 conclusion: This study introduced a novel GKN model that effectively parameterizes and harnesses knowledge within data-driven industrial inferential sensor modeling to achieve automated knowledge integration.
- p.12 conclusion: The efficacy of the GKN model was validated through its application to two inferential sensor tasks.
- p.12 conclusion: Nevertheless, several challenges remain unresolved.
- p.12 conclusion: In addition, extending the proposed approach to other DL architectures, such as CNNs, RNNs, and Transformers represents a significant avenue for further research.
