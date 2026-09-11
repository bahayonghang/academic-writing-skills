---
key: UDY5S5J2
title: "Solving Combinatorial Optimization Problems with Deep Neural Network: A Survey"
venue: "Tsinghua Science and Technology"
doi: "10.26599/TST.2023.9010076"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8,12-17"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

阿拉伯数字标题：`1 Introduction` → `2 Background` → `3 Main Algorithms Solving COPs with DNNs` → `4 Extended Research on COPs` → `5 Applications of COPs Based on DNN` → `6 Conclusion`。前置 `Abstract:` 与 `Key words:`。无独立 Related Work。`related_work=inlined`（Introduction 评 exact / approximate / heuristic，再分 constructive / improvement；全文为综述）。Introduction 末有节序路标，指向 Section 2–6。Method 对应 `Background` 与算法分类。无 Experiments 节。

## Openers

- abstract: `Combinatorial Optimization Problems` — "Combinatorial Optimization Problems (COPs) are a class of optimization problems that are commonly encountered in industrial production and everyday life." (p.1)
- introduction: `Combinatorial Optimization Problems` — "Combinatorial Optimization Problems (COPs) indicate a class of optimization problems." (p.1)
- background: `In the background` — "In the background section, we introduce the fundamental neural network architecture and training methods used in DNN-based algorithms." (p.2)
- algorithms: `The constructive algorithms` — "The constructive algorithms and improvement algorithms are the two primary groups of DNN-based algorithms for solving COPs." (p.4)
- applications: `It is known` — "It is known that traditional algorithms have numerous real-world applications, such as those in Ref. [69,73]." (p.13)
- conclusion: `Herein, we summarize` — "Herein, we summarize the DNN-based algorithms for COPs, which can be divided into constructive and improvement algorithms." (p.14)

## Gap transitions

- however (abstract): "However, as COPs in the real world become more complex, traditional algorithms struggle to generate optimal solutions in a limited amount of time." (p.1)
- however (introduction): "Traditional algorithms solve COPs with satisfactory results. However, they still face various challenges when dealing with more complex problems." (p.2)
- however (algorithms): "The vanilla pointer network can solve some small-scale COPs. However, there remains a gap in solution quality between the pointer network and traditional algorithms." (p.5)
- however (extended): "The DNN-based algorithms perform well on COPs; however, the researchers are still concerned about a few issues." (p.12)
- however (conclusion): "However, some issues should be looked into further in the future." (p.14)

## Hedge verbs

- categorize / causal / abstract: "Herein, we categorize these algorithms into four classes and provide a brief overview of their applications in real-world problems."
- provide / causal / introduction: "This paper provides a brief overview of the DNN-based algorithms that have been proposed for solving COPs in recent years."
- summarize / causal / conclusion: "Herein, we summarize the DNN-based algorithms for COPs"
- outperform / causal / algorithms: "This algorithm outperforms all previously mentioned models, achieving results comparable to commercial solvers."
- seek / causal / conclusion: "the improvement algorithms seek to enhance the performance of traditional algorithms"

## Cross-section linkers

- introduction → background: "This paper provides a brief overview of the DNN-based algorithms that have been proposed for solving COPs in recent years. Section 2 describes the fundamental neural network architecture and training methods used in DNN-based algorithms. Section 3 summarizes the main DNN-based COP-solving algorithms. Section 4 presents extensive research on DNN-based algorithms of multi-objective COPs and algorithms for improving DNN generalization ability. Section 5 discusses some field applications. Section 6 is the conclusion of this survey." (p.2)
- background → algorithms: 训练方法后 `3 Main Algorithms Solving COPs with DNNs` (p.4)
- algorithms → extended: 算法分类后 `4 Extended Research on COPs` (p.12)
- applications → conclusion: 应用段落后 `6 Conclusion` (p.14)

## Candidate rules

- R001 综述摘要用 `Herein, we categorize` 收束分类，不用实验验证句。
- R002 无独立 Related Work；传统算法评述写在 Introduction，网络预备知识写在 `Background`。
- R003 Introduction 末按 Section 2–6 列路标，末句 `Section 6 is the conclusion of this survey`。
- R004 Conclusion 用 `Herein, we summarize` 收回分类，再用 `However, some issues should be looked into further` 列未来问题。
- R005 自称以 `This paper` / `Herein, we` 为主，少用 `In this paper, we propose`。

## Candidate phrases

- `Herein, we categorize these algorithms into four classes` (abstract)
- `This paper provides a brief overview of the DNN-based algorithms` (introduction)
- `Section 6 is the conclusion of this survey.` (introduction)
- `Herein, we summarize the DNN-based algorithms for COPs` (conclusion)
- `However, some issues should be looked into further in the future.` (conclusion)

## House style

自称是 `Herein, we` / `This paper` / `we introduce`。未见 `Here we`。`Herein, we categorize` 与 `This paper provides` 进 phrase_bank，不进 anti_ai_patterns。见 `This paper provides`。未见方法论文常用的 `we propose a ... framework` 作为本文贡献句。

## Quotes

- p.1 abstract: Combinatorial Optimization Problems (COPs) are a class of optimization problems that are commonly encountered in industrial production and everyday life.
- p.1 abstract: However, as COPs in the real world become more complex, traditional algorithms struggle to generate optimal solutions in a limited amount of time.
- p.1 abstract: Herein, we categorize these algorithms into four classes and provide a brief overview of their applications in real-world problems.
- p.1 introduction: Combinatorial Optimization Problems (COPs) indicate a class of optimization problems.
- p.2 introduction: Traditional algorithms solve COPs with satisfactory results. However, they still face various challenges when dealing with more complex problems.
- p.2 introduction: This paper provides a brief overview of the DNN-based algorithms that have been proposed for solving COPs in recent years.
- p.2 introduction: Section 2 describes the fundamental neural network architecture and training methods used in DNN-based algorithms. Section 3 summarizes the main DNN-based COP-solving algorithms. Section 4 presents extensive research on DNN-based algorithms of multi-objective COPs and algorithms for improving DNN generalization ability. Section 5 discusses some field applications. Section 6 is the conclusion of this survey.
- p.2 background: In the background section, we introduce the fundamental neural network architecture and training methods used in DNN-based algorithms.
- p.4 algorithms: The constructive algorithms and improvement algorithms are the two primary groups of DNN-based algorithms for solving COPs.
- p.5 algorithms: The vanilla pointer network can solve some small-scale COPs. However, there remains a gap in solution quality between the pointer network and traditional algorithms.
- p.12 extended: The DNN-based algorithms perform well on COPs; however, the researchers are still concerned about a few issues.
- p.13 applications: Furthermore, DNN-based algorithms are becoming more popular for solving real-world problems.
- p.14 conclusion: Herein, we summarize the DNN-based algorithms for COPs, which can be divided into constructive and improvement algorithms.
- p.14 conclusion: Finally, DNN-based algorithms are becoming increasingly popular in solving real-world COPs, because they do not rely heavily on expert knowledge and can be conveniently applied to various COPs.
- p.14 conclusion: However, some issues should be looked into further in the future.
- p.14 conclusion: In the future, the generalization ability of DNN-based algorithms must be further investigated.
