---
key: CCD9K8H7
title: "Domain knowledge guided pseudo-label generation framework for semi-supervised domain generalization fault diagnosis"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2025.103540"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-10,12-15"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

前置 `Full length article` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction` → `2. Proposed method` → `3` 实验设置 → `4. Results and discussion` → `5. Conclusion`。无独立 Related Work。`related_work=inlined`（Introduction 综述 DAFD、MSDGFD、SSL-PL、SemiDGFD 后列三点缺口）。Introduction 末有编号贡献 + 节序路标。Method 标题为 `Proposed method`。

## Openers

- abstract: `Fault diagnosis methods` — "Fault diagnosis methods based on domain generalization have gained significant attention."
- introduction: `With the development` — "With the development of industrial artificial intelligence, fault diagnosis enhances maintenance efficiency through precise monitoring and predictive maintenance."
- method: `In real industry` — "In real industry, it is difficult to comprehensively label all samples due to limited expert resources."
- experiments: `The diagnostic accuracy` — "The diagnostic accuracy of the proposed method is compared with seven others across 12 SemiDGFD tasks using the SDUST gearbox dataset."
- conclusion: `For the problem` — "For the problem of semi-supervised multi-source domain generalization fault diagnosis, this paper proposes a domain knowledge guided pseudo-label generation framework for semi-supervised domain generalization fault diagnosis."

## Gap transitions

- however (abstract): "However, obtaining sufficient labeled samples from various source domains is costly and challenging."
- therefore (abstract): "Therefore, a new semi-supervised domain generalization fault diagnosis method based on a domain knowledge-guided pseudo-label generation framework is proposed."
- nevertheless (introduction): "Nevertheless, in real industrial environments, the characteristics of vibration signals change due to variations in operating speed, load, and ambient noise levels, leading to differences in data distribution"
- to address (introduction): "To address the above problems, this paper proposes a domain knowledge-guided SemiDGFD pseudo-label generation framework."

## Hedge verbs

- propose / causal / abstract, introduction: "a new ... method ... is proposed"; "this paper proposes"
- show / causal / abstract: "Experiments show that the proposed method generates high-quality pseudo-labels and achieves superior diagnostic accuracy in semi-supervised domain generalization fault diagnosis."
- achieve / causal / experiments, conclusion: "the proposed method achieves better accuracy than existing semi-supervised domain generalization fault diagnosis methods."

## Cross-section linkers

- introduction → method: "The paper is structured as follows: Section 2 presents the problem definition and elaborates on the proposed SemiDGFD method. Section 3 details the experimental setup. Section 4 analyzes the performance of the proposed method through experiments. Finally, Section 5 presents the conclusions based on the experimental results."
- method → experiments: 方法架构后实验任务表与 `4. Results and discussion`
- experiments → conclusion: 计算效率分析后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The paper is structured as follows`
- R004 编号贡献：`The main contributions of this study are as follows`
- R009 自称：`this paper proposes` / `a ... method is proposed`

## Candidate phrases

- `Therefore, a new ... method ... is proposed` (abstract)
- `To address the above problems, this paper proposes` (introduction)
- `The main contributions of this study are as follows` (introduction)
- `The paper is structured as follows` (introduction)
- `Experiments show that the proposed method` (abstract)

## House style

自称 `this paper proposes` / `the proposed method` / `this study`。被动 `is proposed` 用于摘要点名。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Fault diagnosis methods based on domain generalization have gained significant attention.
- abstract: However, obtaining sufficient labeled samples from various source domains is costly and challenging.
- abstract: Therefore, a new semi-supervised domain generalization fault diagnosis method based on a domain knowledge-guided pseudo-label generation framework is proposed.
- abstract: Experiments show that the proposed method generates high-quality pseudo-labels and achieves superior diagnostic accuracy in semi-supervised domain generalization fault diagnosis.
- introduction: With the development of industrial artificial intelligence, fault diagnosis enhances maintenance efficiency through precise monitoring and predictive maintenance.
- introduction: To address the above problems, this paper proposes a domain knowledge-guided SemiDGFD pseudo-label generation framework.
- introduction: The main contributions of this study are as follows:
- introduction: The paper is structured as follows: Section 2 presents the problem definition and elaborates on the proposed SemiDGFD method.
- method: In real industry, it is difficult to comprehensively label all samples due to limited expert resources.
- experiments: The diagnostic accuracy of the proposed method is compared with seven others across 12 SemiDGFD tasks using the SDUST gearbox dataset.
- conclusion: For the problem of semi-supervised multi-source domain generalization fault diagnosis, this paper proposes a domain knowledge guided pseudo-label generation framework for semi-supervised domain generalization fault diagnosis.
- conclusion: The main conclusions are as follows: (1) The proposed method achieves better accuracy than existing semi-supervised domain generalization fault diagnosis methods.
