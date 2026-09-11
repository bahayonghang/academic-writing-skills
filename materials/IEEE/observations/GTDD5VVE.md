---
key: GTDD5VVE
title: "Controllable Mixture-of-Experts for Multivariate Soft Sensors"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2025.3597838"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "19789-19800"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED METHOD` → `IV.`（实验；A. Experiment Setup / B. Overall Performance）→ `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评线性统计 / 非线性 / 深度学习五类架构与硬/软参数共享，再点 catastrophic interference 与 uncontrollable optimization）。Introduction 末有 `Organization.` 路标，指向 Section II–V。Preliminaries 承担参数共享与控制器文献铺垫。Method 为 `III. PROPOSED METHOD`。Experiments 在 Section IV（锦州/天津核监测站）。

## Openers

- abstract: `Multivariate soft sensors` — "Multivariate soft sensors are critical in industrial manufacturing for providing precise estimations of multiple quality variables and ensuring data reliability and completeness." (p.19789)
- introduction: `MODELLING of quality` — "MODELLING of quality variables via advanced sensor data analysis has become a pivotal aspect in industrial manufacturing landscape [1], [2], widely applied for production efficiency enhancement and safety assurance." (p.19789；栏首掉字)
- method: `In this section` — "In this section, we introduce the Mixture-of-Sequential-Experts (MoSE) module, designed to mitigate catastrophic interference in industrial applications." (p.19791, III.A)
- experiments: `We construct two` — "We construct two industrial datasets from monitoring logs of the Jinzhou and Tianjin stations in China, focusing on two quality variables: GDR and NES mean from 1024-channel NESs." (p.19794, IV.A)
- conclusion: `In this work` — "In this work, we propose a Controllable Mixture-of-Experts (ControlMoE) framework for MVSS, featuring a MoSE module and a PIDC module." (p.19798)

## Gap transitions

- however (abstract): "Existing methods predominantly focus on parameter-sharing architectures while overlooking two fundamental issues: 1) catastrophic interference, where sharing parameters across all tasks leads to performance degradation; 2) uncontrollable optimization, where the optimizer lacks controllability over task priorities, misleading specific tasks converge to unexpected values." (p.19789)
- however (introduction): "However, sensors may fail to function properly under extreme operating conditions [3], leading to challenges in monitoring certain critical quality variables." (p.19789)
- however (introduction): "However, the line of works above primarily focuses on improving single quality variable estimation in the industrial field by developing more efficient and effective architectures." (p.19789)
- despite (introduction): "Despite promising empirical results, these approaches suffer from two critical issues that hinder practical performance: (1) Catastrophic interference: consistently sharing parameters across all tasks can result in significant performance degradation due to task-specific representation demands." (p.19790)
- to tackle (introduction): "To tackle these issues and advance state-of-the-art performance, we introduce the Controllable Mixture-of-Experts (ControlMoE), which consists of two components: a Mixture-of-Sequential-Experts (MoSE) module and a Proportional-Integral-Derivative Calibrating (PIDC) module." (p.19790)

## Hedge verbs

- propose / causal / abstract, method, conclusion: "we propose a controllable Mixture-of-Experts (ControlMoE) framework"; "we propose the PIDC module"; "we propose a Controllable Mixture-of-Experts"
- introduce / causal / introduction: "we introduce the Controllable Mixture-of-Experts (ControlMoE)"
- demonstrate / causal / abstract, introduction, experiments: "demonstrate that ControlMoE achieves superior accuracy"; "to demonstrate the efficacy of ControlMoE"; "we demonstrate how the PIDC module enhances model performance"
- show / causal / experiments: "The results illustrated in Fig. 5 reveal substantial performance enhancements"
- may / speculative / introduction, experiments: "which may lead to catastrophic interference"; "This discrepancy may stem from suboptimal hyperparameter tuning"
- promising / speculative / conclusion: "it is promising to explore efficient gating mechanism for expert ensemble"

## Cross-section linkers

- introduction → preliminaries/method: "Organization. The remainder of this paper is organized as follows: Section II introduces the technical preliminaries. Section III details the implementation of ControlMoE. Section IV demonstrates the effectiveness and superior accuracy of ControlMoE on a nuclear power plant monitoring task. Conclusions and future work are discussed in Section V." (p.19790)
- method → experiments: "Fig. 3 depicts the general architecture of the proposed ControlMoE framework" 随后 Section IV 研究问题列表与 `A. Experiment Setup` (p.19793–19794)
- experiments → conclusion: PID 调参段落后直接 `V. CONCLUSION` (p.19798)

## Candidate rules

- R001 abstract 贡献句用 `we propose a ... framework for`，Note to Practitioners 用 `This paper tackles` / `Our proposed framework`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段；理论铺垫放到 `II. PRELIMINARIES`。
- R003 Introduction 末用 `The remainder of this paper is organized as follows` 指向 II–V。
- R004 贡献用 `Contributions. Our main contributions are as follows:` + 编号列表。
- R005 Conclusion 用 `In this work, we propose` 收回双模块，再用 `As for future work, it is promising to`。

## Candidate phrases

- `we propose a controllable Mixture-of-Experts (ControlMoE) framework` (abstract)
- `To tackle these issues and advance state-of-the-art performance, we introduce` (introduction)
- `Our main contributions are as follows:` (introduction)
- `The remainder of this paper is organized as follows:` (introduction)
- `In this work, we propose a Controllable Mixture-of-Experts (ControlMoE) framework` (conclusion)

## House style

自称是 `we propose` / `we introduce` / `this paper` / `this work` / `Our proposed framework`。未见 `Here we`。`This paper tackles`（Note to Practitioners）与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。Note to Practitioners 出现 `This paper`；Organization 用 `this paper`。

## Quotes

- p.19789 abstract: Multivariate soft sensors are critical in industrial manufacturing for providing precise estimations of multiple quality variables and ensuring data reliability and completeness.
- p.19789 abstract: Existing methods predominantly focus on parameter-sharing architectures while overlooking two fundamental issues: 1) catastrophic interference, where sharing parameters across all tasks leads to performance degradation; 2) uncontrollable optimization, where the optimizer lacks controllability over task priorities, misleading specific tasks converge to unexpected values.
- p.19789 abstract: To handle these issues and enhance multivariate modeling, we propose a controllable Mixture-of-Experts (ControlMoE) framework for industrial soft sensors, consisting of a Mixture-of-Sequential-Experts (MoSE) module and a Proportional-Integral-Derivative Calibrating (PIDC) module.
- p.19789 practitioners: This paper tackles the challenges in applying multivariate soft sensors within industrial manufacturing processes, particularly in environments such as nuclear monitoring where precision and control over multiple quality variables are critical.
- p.19789 introduction: MODELLING of quality variables via advanced sensor data analysis has become a pivotal aspect in industrial manufacturing landscape [1], [2], widely applied for production efficiency enhancement and safety assurance.
- p.19789 introduction: However, the line of works above primarily focuses on improving single quality variable estimation in the industrial field by developing more efficient and effective architectures.
- p.19790 introduction: Despite promising empirical results, these approaches suffer from two critical issues that hinder practical performance: (1) Catastrophic interference: consistently sharing parameters across all tasks can result in significant performance degradation due to task-specific representation demands.
- p.19790 introduction: To tackle these issues and advance state-of-the-art performance, we introduce the Controllable Mixture-of-Experts (ControlMoE), which consists of two components: a Mixture-of-Sequential-Experts (MoSE) module and a Proportional-Integral-Derivative Calibrating (PIDC) module.
- p.19790 introduction: Organization. The remainder of this paper is organized as follows: Section II introduces the technical preliminaries. Section III details the implementation of ControlMoE. Section IV demonstrates the effectiveness and superior accuracy of ControlMoE on a nuclear power plant monitoring task. Conclusions and future work are discussed in Section V.
- p.19791 method: In this section, we introduce the Mixture-of-Sequential-Experts (MoSE) module, designed to mitigate catastrophic interference in industrial applications.
- p.19794 experiments: We construct two industrial datasets from monitoring logs of the Jinzhou and Tianjin stations in China, focusing on two quality variables: GDR and NES mean from 1024-channel NESs.
- p.19794 experiments: Our proposed ControlMoE outperforms baselines in both single and multi-task categories, achieving the lowest MAE and the highest R2 metrics on the Jinzhou and Tianjin datasets.
- p.19798 conclusion: In this work, we propose a Controllable Mixture-of-Experts (ControlMoE) framework for MVSS, featuring a MoSE module and a PIDC module.
- p.19798 conclusion: Experimental results showcase ControlMoE’s superiority over existing SOTA soft sensors.
- p.19798 conclusion: As for future work, it is promising to explore efficient gating mechanism for expert ensemble, such as sparse attention, and to expand our model to general industrial applications such as process engineering and healthcare, thereby improving adaptability and efficiency in varying industrial scenarios.
