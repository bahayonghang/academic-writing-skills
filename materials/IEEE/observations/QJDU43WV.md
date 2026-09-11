---
key: QJDU43WV
title: "A Self-Interpretable Soft Sensor Based on Deep Learning and Multiple Attention Mechanism: From Data Selection to Sensor Modeling"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3181692"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评混合驱动 DLSS、GAN 事后解释、注意力与信息瓶颈）。Section II 为统一注意力计算预备。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `EXPERIMENTS`（空气预热器转子热变形）。

## Openers

- abstract: `For deep learning-based` — "For deep learning-based soft sensors, the lack of interpretability and the consequent unreliability has become one of the most important problems." (p.6859)
- introduction: `TO ACCURATELY predict` — "TO ACCURATELY predict process variables and achieve high-quality control of complex industrial processes, soft sensor technology has been widely used given its advantages of fast measurement speed and low cost [1]." (p.6859)
- method: `In general data` — "In general, data selection and sensor modeling are considered as two separate components in soft sensor training." (p.6862, III.A)
- experiments: `A rotary air` — "A rotary air preheater is a boiler exhaust recovery and utilization device commonly used in thermal power plants, but it generally suffers from air leakage due to its structure [35]." (p.6864, IV.A)
- conclusion: `In this article` — "In this article, a self-interpretable DLSS DMASS was proposed and applied to the thermal deformation prediction of the air preheater rotor." (p.6870)

## Gap transitions

- despite (introduction): "Despite deep networks’ powerful feature extraction capability and that the utilization capability of unlabeled data has been proven to further improve sensing performance, DLSSs still face some significant problems that must be solved." (p.6859)
- however (introduction): "However, during the process of variable selection, the DLSS directly deletes the auxiliary variables based on the preset threshold value." (p.6860)
- however (introduction): "However, post hoc interpretation has been increasingly regarded as unreliable, that is, such interpretation is most likely an inaccurate representation of the original model in parts of the feature space [20]." (p.6860)
- therefore (introduction): "Therefore, it is necessary to develop a self-interpretable DLSS that can not only be trained from a supervised dataset to directly solve a soft sensing task but also can provide accurate and unbiased explanations of data selection and sensor modeling." (p.6860)
- although (experiments): "Although the proposed DMASS can achieve satisfactory performance, it also has limitations, which are mainly reflected in the following three points." (p.6869)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a neural network scheme called the deep multiple attention soft sensor (DMASS) ... is proposed"; "a deep multiple attention soft sensor (DMASS) consisting solely of attention mechanisms is proposed"; "a self-interpretable DLSS DMASS was proposed"
- show / causal / experiments: "The experimental results show that integrating the data selection and sensor modeling into one model is advantageous."
- confirm / causal / abstract: "DMASS’s great sensing performance was confirmed through comparison with other novel soft sensors."
- can / speculative / conclusion: "A self-interpretable soft sensor helps users understand and trust what the model has learned"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. The summarized core attention calculation steps are explained in Section II, and the proposed VAM, TLAM, and SAAS are introduced. In Section III, the proposed DMASS is described, including its structure, training scheme, and self-interpretability. Experiments are conducted in Section IV to evaluate and verify DMASS’s performance. Finally, Section V concludes this article." (p.6861)
- method → experiments: 训练测试流程后 `IV. EXPERIMENTS` (p.6864)
- experiments → conclusion: 局限列表后 `V. CONCLUSION` (p.6870)

## Candidate rules

- R009 摘要用 `is proposed` 点名 DMASS。
- R002 Introduction 无独立 Related Work，可解释 DLSS 评述写在引言中段。
- R004 贡献列表：`The primary contributions of this study are as follows.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 实验末用 `Although ... it also has limitations` 编号三点；Conclusion 再用 `in the future` / adversarial training 指向后续。

## Candidate phrases

- `In this article, a neural network scheme called ... is proposed` (abstract)
- `The primary contributions of this study are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a self-interpretable DLSS DMASS was proposed` (conclusion)

## House style

自称 `In this article` / `this study` / `the proposed DMASS`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.6859 abstract: For deep learning-based soft sensors, the lack of interpretability and the consequent unreliability has become one of the most important problems.
- p.6859 abstract: In this article, a neural network scheme called the deep multiple attention soft sensor (DMASS), which consists solely of attention mechanisms, is proposed to develop a self-interpretable soft sensor.
- p.6859 abstract: Meanwhile, DMASS’s great sensing performance was confirmed through comparison with other novel soft sensors.
- p.6859 introduction: TO ACCURATELY predict process variables and achieve high-quality control of complex industrial processes, soft sensor technology has been widely used given its advantages of fast measurement speed and low cost [1].
- p.6859 introduction: Despite deep networks’ powerful feature extraction capability and that the utilization capability of unlabeled data has been proven to further improve sensing performance, DLSSs still face some significant problems that must be solved.
- p.6860 introduction: However, during the process of variable selection, the DLSS directly deletes the auxiliary variables based on the preset threshold value.
- p.6860 introduction: However, post hoc interpretation has been increasingly regarded as unreliable, that is, such interpretation is most likely an inaccurate representation of the original model in parts of the feature space [20].
- p.6860 introduction: Therefore, it is necessary to develop a self-interpretable DLSS that can not only be trained from a supervised dataset to directly solve a soft sensing task but also can provide accurate and unbiased explanations of data selection and sensor modeling.
- p.6861 introduction: The primary contributions of this study are as follows.
- p.6861 introduction: The rest of this article is organized as follows. The summarized core attention calculation steps are explained in Section II, and the proposed VAM, TLAM, and SAAS are introduced. In Section III, the proposed DMASS is described, including its structure, training scheme, and self-interpretability. Experiments are conducted in Section IV to evaluate and verify DMASS’s performance. Finally, Section V concludes this article.
- p.6862 method: In general, data selection and sensor modeling are considered as two separate components in soft sensor training.
- p.6864 experiments: A rotary air preheater is a boiler exhaust recovery and utilization device commonly used in thermal power plants, but it generally suffers from air leakage due to its structure [35].
- p.6869 experiments: The experimental results show that integrating the data selection and sensor modeling into one model is advantageous.
- p.6869 experiments: Although the proposed DMASS can achieve satisfactory performance, it also has limitations, which are mainly reflected in the following three points.
- p.6870 conclusion: In this article, a self-interpretable DLSS DMASS was proposed and applied to the thermal deformation prediction of the air preheater rotor.
- p.6870 conclusion: By comparing with the advanced soft sensors, DMASS’s sensing performance in computational complexity, prediction accuracy, and prediction stability was proved.
- p.6870 conclusion: As most DLSSs are not interpretable, it will be necessary to develop a universal self-interpretable approach in the future.
