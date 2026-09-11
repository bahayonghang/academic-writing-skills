---
key: CCAG9DW7
title: "Trend and Order Features for Semi-Supervised Time-Series Classification via Multitask Learning"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2025.3616340"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`，四类 SSL：self-labeled / graph / regularization / multitask-learning）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `EXPERIMENT`（UCR 128 + 三个真实数据集）。

## Openers

- abstract: `Multitask learning with` — "Multitask learning with a pretext task has excelled in time-series classification task lacking labeled data." (p.1)
- introduction: `THE time-series data` — "THE time-series data, which are ubiquitous, are the sequence of time-ordered values describing the natural order of things." (p.1；栏首掉字)
- related_work: `In this section` — "In this section, we focus on the related work of SSL." (p.3, II)
- method: `In this section` — "In this section, we first present the task description." (p.3, III)
- experiments: `In this section` — "In this section, we first present the experimental settings used to evaluate the performance of our proposed method." (p.6, IV)
- conclusion: `This article proposes` — "This article proposes TOFL, which extracts the order and the multiscale hierarchically guided trend information from unlabeled time-series data." (p.12)

## Gap transitions

- however (introduction): "However, with the advancement of sensor technologies, unlabeled time-series data are growing exponentially while labeled time-series data are growing linearly." (p.1)
- however (introduction): "However, despite the promise of multitask learning in time-series classification, there are two noteworthy challenges that current methods encounter." (p.1)
- although (introduction): "Although SemiTime [17] has the ability to identify if 2 segments are from the same sample, it fails to recognize the order relation between the two segments." (p.2)
- to address (introduction): "To address this issue, we design the self-sequence order prediction (SOP) task to explore the intrinsic order features of unlabeled data in a self-supervised manner, as shown in Fig. 2." (p.2)
- although (related work): "Although all these methods work on mining potential features of unlabeled data, they all ignore the order and trend features in self-sequences." (p.3)
- although (conclusion): "Although TOFL shows superior performance and broad application potential across various datasets and real-world scenarios, it exhibits certain limitations when dealing with data containing high-frequency noise." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose trend and order features"; "we propose a simple but effective pretext task"
- design / causal / abstract, introduction: "we design a gradual trend fusion (GTF) block"; "we design the self-sequence order prediction (SOP) task"
- demonstrate / causal / abstract: "TOFL demonstrates a high level of competitiveness"
- prove / causal / introduction: "We prove the uniform stability of the SOP task in multitask and improve generalization performance."
- indicate / causal / method: "Theorem 3 indicates that TOFL is limited by the SOP and classification tasks."
- intend / speculative / conclusion: "we intend to incorporate frequency domain analysis techniques into our approach as a crucial direction for future research."

## Cross-section linkers

- introduction → related work: "The remainder of this article is organized as follows. Section II covers the related works about cutting-edge supervised and semi-supervised time-series classification methods. Section III presents the task description and the details of the proposed methodology. Section IV lists the detailed information from the UCR archive and three real-world datasets and compares the state-of-the-art (SOTA) supervised and semi-supervised methods with these datasets. Finally, Section V concludes this article." (p.3)
- related work → method: "In this work, we propose a multitask-learning-based approach to discover the order between self-sequences." 随后 `III. METHODOLOGY` (p.3)
- method → experiments: Theorem 4 后 `IV. EXPERIMENT` (p.6)
- experiments → conclusion: t-SNE 分析后 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 贡献句用 `In this article, we propose` + 方法缩写，不用 `Here we`。
- R002 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R003 贡献用 `the principal contributions of this article are as follows` + 编号列表。
- R004 独立 Related Work 按方法族分四类，段末 `Although all these methods` 收回缺口。
- R005 Conclusion 先收回方法，再用 `Although` 承认高频噪声局限，再用 `we intend to` 指向频域。

## Candidate phrases

- `In this article, we propose` (abstract)
- `the principal contributions of this article are as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this section, we first present the experimental settings used to evaluate the performance of our proposed method.` (experiments)
- `This article proposes TOFL, which extracts` (conclusion)

## House style

自称是 `In this article, we propose` / `this article` / `we design` / `our proposed method` / `This article proposes`。未见 `Here we`。`In this article, we propose` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Multitask learning with a pretext task has excelled in time-series classification task lacking labeled data.
- p.1 abstract: In this article, we propose trend and order features for semi-supervised time-series classification via multitask learning (TOFL).
- p.1 abstract: Specifically, we propose a simple but effective pretext task—self-sequence order prediction (SOP)—to discover the order relation.
- p.1 abstract: TOFL demonstrates a high level of competitiveness and, in most cases, closely matches or even surpasses SOTA methods in terms of accuracy.
- p.1 introduction: THE time-series data, which are ubiquitous, are the sequence of time-ordered values describing the natural order of things.
- p.1 introduction: However, with the advancement of sensor technologies, unlabeled time-series data are growing exponentially while labeled time-series data are growing linearly.
- p.1 introduction: However, despite the promise of multitask learning in time-series classification, there are two noteworthy challenges that current methods encounter.
- p.2 introduction: Although SemiTime [17] has the ability to identify if 2 segments are from the same sample, it fails to recognize the order relation between the two segments.
- p.2 introduction: To address this issue, we design the self-sequence order prediction (SOP) task to explore the intrinsic order features of unlabeled data in a self-supervised manner, as shown in Fig. 2.
- p.2 introduction: In sum, the principal contributions of this article are as follows.
- p.3 introduction: The remainder of this article is organized as follows. Section II covers the related works about cutting-edge supervised and semi-supervised time-series classification methods. Section III presents the task description and the details of the proposed methodology. Section IV lists the detailed information from the UCR archive and three real-world datasets and compares the state-of-the-art (SOTA) supervised and semi-supervised methods with these datasets. Finally, Section V concludes this article.
- p.3 related work: In this section, we focus on the related work of SSL.
- p.3 related work: Although all these methods work on mining potential features of unlabeled data, they all ignore the order and trend features in self-sequences.
- p.3 method: In this section, we first present the task description.
- p.6 experiments: In this section, we first present the experimental settings used to evaluate the performance of our proposed method.
- p.9 experiments: The graph clearly indicates that the accuracy of the “supervised,” TOFL-GTF, and TOFL improves as the label ratio increases.
- p.12 conclusion: This article proposes TOFL, which extracts the order and the multiscale hierarchically guided trend information from unlabeled time-series data.
- p.12 conclusion: Although TOFL shows superior performance and broad application potential across various datasets and real-world scenarios, it exhibits certain limitations when dealing with data containing high-frequency noise.
- p.12 conclusion: In response to these findings, and to improve the model's ability to discern trend and temporal features, we intend to incorporate frequency domain analysis techniques into our approach as a crucial direction for future research.
