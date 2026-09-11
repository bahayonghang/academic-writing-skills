---
key: HSFSVT3Z
title: "UGDS-CDM: A novel uncertainty-guided dual-stage conditional diffusion model and vision mamba-KAN integrating expert knowledge for surface defect detection under small samples"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2025.104011"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,14-20,22-24,28-30,38-42"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

前置 `Full length article` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction` → `2. Related works` → `3. Methodology` → `4. Case study` → `5. Conclusion`。独立 Related Work（`2. Related works`，含 SDD、数据增强、few-shot、`2.4. Research gaps`）。`related_work=independent`。Introduction 末有编号贡献 + 节序路标。Experiments 标题为 `Case study`。

## Openers

- abstract: `Surface defect detection` — "Surface defect detection (SDD) is a pivotal component of quality control in manufacturing processes."
- introduction: `Quality inspection and` — "Quality inspection and control are critical components of intelligent manufacturing, ensuring both product reliability and customer satisfaction [1,2]."
- related_work: `SDD plays a` — "SDD plays a vital role in industrial production, particularly in high-precision manufacturing domains such as semiconductors, automotive, and aerospace."
- method: `To address the` — "To address the limitations in handling diverse defects, limited generalization due to sample scarcity, restricted diffusion model applications, and insufficient interpretability in current SDD and few-shot learning techniques, we propose the UGDS-CDM combined with VM-KAN, which integrates expert knowledge for SDD in small-sample scenarios."
- experiments: `To evaluate the` — "To evaluate the robustness and generalization capability of the proposed method, comprehensive experiments were conducted on three defect image datasets."
- conclusion: `This study introduces` — "This study introduces a comprehensive framework to address critical challenges in industrial defect detection, namely limited samples and dynamically evolving environments."

## Gap transitions

- to address (abstract): "To address this issue, this paper proposes an uncertainty-guided dual-stage conditional diffusion model (UGDS-CDM) integrated with a vision mamba Kolmogorov-Arnold Networks (VM-KAN) detection model that incorporates expert knowledge for surface defect detection under small sample conditions."
- nonetheless (introduction): "Nonetheless, several challenges remain, especially in scenarios characterized by high product variability, small-batch manufacturing, frequent process changes, and ongoing product iterations."
- however (introduction): "However, in intelligent manufacturing environments, defective products occur infrequently, often resulting in a severe scarcity—or complete absence—of abnormal sample data [13]."
- despite (introduction): "Despite outperforming human experts in specific tasks [8], the adoption of DL in industrial quality inspection is hindered by several key limitations."

## Hedge verbs

- propose / causal / abstract, introduction: "this paper proposes"; "we propose"
- demonstrate / causal / abstract, experiments: "Extensive experiments on the automotive paint defect dataset demonstrate the robust performance of our proposed method."
- indicate / associative / experiments: "These findings indicate that VM-KAN not only achieved excellent performance metrics but also maintained significant consistency in experimental reproducibility."

## Cross-section linkers

- introduction → related work: "The remainder of this paper is organized as follows. Section 2 reviews recent advances in SDD within the context of manufacturing processes. Section 3 details the proposed UGDS-CDM and the VM-KAN framework. Section 4 presents the experimental setup, performance evaluation, and result analysis. Finally, Section 5 concludes the paper by summarizing key findings and outlining directions for future research."
- related work → method: 缺口列表后 `3. Methodology`
- method → experiments: HMI 系统后 `4. Case study`
- experiments → conclusion: Discussion 与局限后 `5. Conclusion`

## Candidate rules

- R001 独立 Related Work（`2. Related works`）。
- R003 节序路标：`The remainder of this paper is organized as follows`
- R004 编号贡献：`The main contributions of this work are as follows`
- R009 自称：`this paper proposes` / `we propose`

## Candidate phrases

- `To address this issue, this paper proposes` (abstract)
- `The main contributions of this work are as follows` (introduction)
- `The remainder of this paper is organized as follows` (introduction)
- `Extensive experiments on the automotive paint defect dataset demonstrate` (abstract)
- `This study introduces a comprehensive framework` (conclusion)

## House style

自称 `this paper proposes` / `we propose` / `this study introduces`。`we developed` 用于方法模块。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Surface defect detection (SDD) is a pivotal component of quality control in manufacturing processes.
- abstract: To address this issue, this paper proposes an uncertainty-guided dual-stage conditional diffusion model (UGDS-CDM) integrated with a vision mamba Kolmogorov-Arnold Networks (VM-KAN) detection model that incorporates expert knowledge for surface defect detection under small sample conditions.
- abstract: Extensive experiments on the automotive paint defect dataset demonstrate the robust performance of our proposed method.
- introduction: Quality inspection and control are critical components of intelligent manufacturing, ensuring both product reliability and customer satisfaction [1,2].
- introduction: Nonetheless, several challenges remain, especially in scenarios characterized by high product variability, small-batch manufacturing, frequent process changes, and ongoing product iterations.
- introduction: The main contributions of this work are as follows:
- introduction: The remainder of this paper is organized as follows. Section 2 reviews recent advances in SDD within the context of manufacturing processes.
- related_work: SDD plays a vital role in industrial production, particularly in high-precision manufacturing domains such as semiconductors, automotive, and aerospace.
- method: To address the limitations in handling diverse defects, limited generalization due to sample scarcity, restricted diffusion model applications, and insufficient interpretability in current SDD and few-shot learning techniques, we propose the UGDS-CDM combined with VM-KAN, which integrates expert knowledge for SDD in small-sample scenarios.
- experiments: To evaluate the robustness and generalization capability of the proposed method, comprehensive experiments were conducted on three defect image datasets.
- experiments: When compared with the LeNet baseline (89.01 %), the enhanced VM-KAN implementation (96.95 %) shows a 7.94 % improvement in F1 scores, substantiating its superior performance.
- conclusion: This study introduces a comprehensive framework to address critical challenges in industrial defect detection, namely limited samples and dynamically evolving environments.
- conclusion: This study offers novel insights into small-sample defect detection in manufacturing systems and is expected to provide technical support for the intelligent and continuous optimization of quality management practices.
