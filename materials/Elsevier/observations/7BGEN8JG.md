---
key: 7BGEN8JG
title: "Fault diagnosis in industrial chemical processes using interpretable patterns based on Logical Analysis of Data"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2017.11.045"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Logical Analysis of Data (LAD)` → `3` TEP 案例 → `4` 黑液回收锅炉案例 → `5. Discussion and future work` → `6. Conclusions`。前置 `a b s t r a c t` 与 `a r t i c l e i n f o` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 MVSPM：PCA/PLS/ICA；分类：ANN/DT/RF/SVM；BN）。Introduction 末有节序路标，无编号贡献列表。Method 为 LAD 三步（binarization、pattern generation、theory formation）。Experiments 拆成两节案例研究。

## Openers

- abstract: `This paper applies` — "This paper applies the Logical Analysis of Data (LAD) to detect and diagnose faults in industrial chemical processes."
- introduction: `Early and accurate` — "Early and accurate fault detection and diagnosis (FDD) in chemical plants has been shown to minimize downtime, improve safety, and reduce manufacturing costs (Maurya, Rengaswamy, & Venkatasubramanian, 2007)."
- method: `Logical Analysis of` — "Logical Analysis of Data is a knowledge discovery approach, based on certain concepts from the fields of optimization and the theory of Boolean functions (Boros et al., 2000)."
- experiments: `The F1-scores %,` — "The F1-scores %, accuracy and training time for LAD and the other classification models are shown in Table 12." (s.4.7 BLRB)
- conclusion: `The Logical Analysis` — "The Logical Analysis of Data (LAD) was applied as an interpretable machine-learning technique for fault detection and diagnosis (FDD) in industrial chemical processes."

## Gap transitions

- due to (introduction): "Due to the interactions between process variables in large-scale processes, it is difficult or even impossible to identify the relationships between the faults’ causes and their effects."
- therefore (introduction): "Therefore, industrial chemical processes require an interpretable FDD method that can identify and analyze the type of fault and find its root causes."
- however (discussion): "However, as shown in Tables 5, 6 and 12, the LAD approach was able to diagnose the faults accurately and proved competitive with the other diagnostic models regardless of the distribution of data."
- in addition to (abstract, discussion): "In addition to its explanatory power, the results show that LAD’s performance is comparable to the most accurate techniques."

## Hedge verbs

- applies / causal / abstract, introduction: "This paper applies the Logical Analysis of Data (LAD)"
- show / associative / abstract: "the results show that LAD’s performance is comparable to the most accurate techniques."
- proved / associative / discussion: "the LAD approach was able to diagnose the faults accurately and proved competitive with the other diagnostic models"
- showed / associative / conclusion: "The method showed substantial improvements in terms of the number of correctly classified faulty observations"

## Cross-section linkers

- introduction → method: "The paper is structured in six sections. Section 2 presents and discusses the basic concept of LAD, as well as its notations and steps."
- method → experiments: "The first case study of the TEP dataset is presented in Section 3. A real case study from the industry is presented in Section 4."
- experiments → discussion: "The research extensions and future directions are discussed in Section 5, followed by concluding remarks in Section 6."

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The paper is structured in six sections`
- R009 自称：`This paper applies` / `We applied the LAD approach`

## Candidate phrases

- `This paper applies the Logical Analysis of Data (LAD)` (abstract)
- `The paper is structured in six sections` (introduction)
- `In addition to its explanatory power, the results show that` (abstract)
- `We applied the LAD approach to two case studies` (conclusion)

## House style

自称 `This paper applies` / `We applied` / `Our objective is`。`this paper` 与第一人称复数并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: This paper applies the Logical Analysis of Data (LAD) to detect and diagnose faults in industrial chemical processes.
- abstract: This machine learning classification technique discovers hidden knowledge in industrial datasets by revealing interpretable patterns, which are linked to underlying physical phenomena.
- abstract: In addition to its explanatory power, the results show that LAD’s performance is comparable to the most accurate techniques.
- introduction: Early and accurate fault detection and diagnosis (FDD) in chemical plants has been shown to minimize downtime, improve safety, and reduce manufacturing costs (Maurya, Rengaswamy, & Venkatasubramanian, 2007).
- introduction: Therefore, industrial chemical processes require an interpretable FDD method that can identify and analyze the type of fault and find its root causes.
- introduction: The paper is structured in six sections. Section 2 presents and discusses the basic concept of LAD, as well as its notations and steps.
- method: Logical Analysis of Data is a knowledge discovery approach, based on certain concepts from the fields of optimization and the theory of Boolean functions (Boros et al., 2000).
- method: In addition to its high accuracy, one of the most important advantages of LAD is its explanatory power (Yacout, Salamanca, & Mortada, 2011).
- discussion: However, as shown in Tables 5, 6 and 12, the LAD approach was able to diagnose the faults accurately and proved competitive with the other diagnostic models regardless of the distribution of data.
- conclusion: The Logical Analysis of Data (LAD) was applied as an interpretable machine-learning technique for fault detection and diagnosis (FDD) in industrial chemical processes.
- conclusion: The LAD performance was comparable to the most accurate one—the Random Forest.
