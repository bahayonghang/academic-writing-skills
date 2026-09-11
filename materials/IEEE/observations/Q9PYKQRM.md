---
key: Q9PYKQRM
title: "On supervised class-imbalanced learning: An updated perspective and some key challenges"
venue: "IEEE Transactions on Artificial Intelligence"
doi: "10.1109/TAI.2022.3160658"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,14-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. CHARACTERISTICS OF THE CLASS-IMBALANCED PROBLEM` → `III` 传统方法综述 → `IV` 深度学习方法 → `V` 评价指标 → `VI` 新兴应用 → `VII` 开放问题 → `VIII. CONCLUSION`。前置 `Abstract—`、`Impact Statement—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 用 Table I 评先前综述，再给本篇贡献列表）。Introduction 末用 `following Fig. 2 after this introduction in Section I` 给出节序路标，指向 II–VIII。Survey 正文以定义、示例、分类综述为主，无 Method / Experiments 分节。

## Openers

- abstract: `The problem of` — "The problem of class imbalance has always been considered as a significant challenge to traditional machine learning and the emerging deep learning research communities." (p.1)
- introduction: `A CLASSIFIER is` — "A CLASSIFIER is a data-driven supervised modeling technique." (p.1；栏首掉字)
- method: `Class imbalance is` — "Class imbalance is known to adversely affect the classification performance over the minority class." (p.3, II)
- experiments: `To empirically observe` — "To empirically observe how a class imbalance in the training set may adversely affect the performance of a classifier, let us consider the following illustrative example." (p.2, Example 1)
- conclusion: `Since its formal` — "Since its formal introduction [7], [8], the problem of class imbalance never lost its relevance over the next couple of decades." (p.14)

## Gap transitions

- unfortunately (abstract): "Unfortunately, the classes that contain a small number of labelled instances usually correspond to rare and significant events." (p.1)
- thus (abstract): "Thus, poor classification accuracy on these classes may lead to severe consequences." (p.1)
- however (introduction): "However, in many real-life problems, it may not be always possible to respect such conditions." (p.1)
- however (introduction): "However, a renewed vigor in research attempts addressing class-imbalanced problems has been observed over the next five years." (p.3)
- furthermore (introduction): "Furthermore, the latest list of future challenges was provided by Krawczyk [13] back in 2016, while a plethora of new applications and data sources emerged over the next four years along with the advent of the deep learning paradigm." (p.3)
- these issues motivated (introduction): "These issues motivated us to present an updated survey focusing on the class-imbalanced problem in classification." (p.3)

## Hedge verbs

- aim / causal / abstract: "In this article, we aim to provide a comprehensive summary of the rich pool of research works"
- explore / causal / abstract: "we explore the plethora of traditional machine learning approaches"
- discuss / causal / abstract, conclusion: "We further discuss the state-of-the-art deep-learning-based approaches"; "We have also briefly discussed the need for special indices"
- highlight / causal / abstract, conclusion: "highlight the need for techniques tailored for such a paradigm"; "We have also highlighted the recently developed deep learning strategies"
- may (speculative) / introduction: "The violation of such conditions by the training set may result in improper learning"
- aims / causal / conclusion: "This survey aims to provide a comprehensive description of this compelling journey"

## Cross-section linkers

- introduction → body: "Therefore, following Fig. 2 after this introduction in Section I, and a characterization of the class-imbalanced problem in Section II, the rest of this article contains a brief surveys of approaches proposed to counter class imbalance in traditional and deep classifiers, respectively, in Sections III and IV, the effect of class imbalance on performance evaluation indices in Section V, a list of emerging real-life problems where class imbalance handling strategies are being applied in Section VI, and a list of open problems and future challenges in Section VII. Finally, Section VIII concludes this article." (p.3)
- open problems → conclusion: 新兴数据源讨论后 `VIII. CONCLUSION` (p.14)

## Candidate rules

- R001 survey abstract 用 `In this article, we aim to provide a comprehensive summary`，再 `Specifically, following a formal definition`。
- R002 TAI 可前置独立 `Impact Statement—`，再接 `Index Terms—`。
- R003 Introduction 用 Table 评先前综述缺口，再用 `These issues motivated us to present an updated survey` + 编号贡献。
- R004 节序路标可挂 mind map：`following Fig. 2 after this introduction in Section I`。
- R005 Conclusion 用 `Since its formal introduction` 收回问题史，再用 `in the hope of encouraging exploration` 指向开放问题。

## Candidate phrases

- `In this article, we aim to provide a comprehensive summary of` (abstract)
- `These issues motivated us to present an updated survey focusing on` (introduction)
- `In essence, our contributions are as follows.` (introduction)
- `Finally, Section VIII concludes this article.` (introduction)
- `This survey aims to provide a comprehensive description of` (conclusion)

## House style

自称 `In this article, we aim` / `we explore` / `this survey` / `our contributions`。未见 `Here we`、`In this paper`。`In this article, we aim` 与 `this survey` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The problem of class imbalance has always been considered as a significant challenge to traditional machine learning and the emerging deep learning research communities.
- p.1 abstract: Unfortunately, the classes that contain a small number of labelled instances usually correspond to rare and significant events.
- p.1 abstract: Thus, poor classification accuracy on these classes may lead to severe consequences.
- p.1 abstract: In this article, we aim to provide a comprehensive summary of the rich pool of research works attempting to combat the adversarial effects of class imbalance efficiently.
- p.1 impact: This survey attempts to bridge this gap while focusing on readability and broader converge highlighting the new developments while mentioning the classical milestones.
- p.1 introduction: A CLASSIFIER is a data-driven supervised modeling technique.
- p.1 introduction: However, in many real-life problems, it may not be always possible to respect such conditions.
- p.2 experiments: To empirically observe how a class imbalance in the training set may adversely affect the performance of a classifier, let us consider the following illustrative example.
- p.3 introduction: However, a renewed vigor in research attempts addressing class-imbalanced problems has been observed over the next five years.
- p.3 introduction: These issues motivated us to present an updated survey focusing on the class-imbalanced problem in classification. In essence, our contributions are as follows.
- p.3 introduction: Therefore, following Fig. 2 after this introduction in Section I, and a characterization of the class-imbalanced problem in Section II, the rest of this article contains a brief surveys of approaches proposed to counter class imbalance in traditional and deep classifiers, respectively, in Sections III and IV, the effect of class imbalance on performance evaluation indices in Section V, a list of emerging real-life problems where class imbalance handling strategies are being applied in Section VI, and a list of open problems and future challenges in Section VII. Finally, Section VIII concludes this article.
- p.3 method: Class imbalance is known to adversely affect the classification performance over the minority class.
- p.14 conclusion: Since its formal introduction [7], [8], the problem of class imbalance never lost its relevance over the next couple of decades.
- p.14 conclusion: This survey aims to provide a comprehensive description of this compelling journey of traditional machine learning as well as the deep learning research communities in search of better approaches to efficiently address the diverse issues associated with class imbalance.
- p.14 conclusion: Finally, in the hope of encouraging exploration in new directions, we have provided an updated list of future research opportunities by detailing the open problems and looming challenges.
