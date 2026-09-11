---
key: AJGQQGHD
title: "Feature Mode Decomposition: New Decomposition Theory for Rotating Machinery Fault Diagnosis"
venue: "IEEE Transactions on Industrial Electronics"
doi: "10.1109/TIE.2022.3156156"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-7,10-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROPOSED METHOD` → `III` 仿真（单故障 / 复合故障） → `IV` 实测 → `V. DISCUSSION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 EMD / EEMD / LMD / EWT / VMD）。Introduction 末有 `The rest of this article is organized as follows` 路标，指向 Section II–VI。Method 分 FIR 滤波器组、滤波更新、模式选择。Experiments 拆成仿真（III）与实测（IV），另有独立 `DISCUSSION`。

## Openers

- abstract: `In this article` — "In this article, a new decomposition theory, feature mode decomposition (FMD), is tailored for the feature extraction of machinery fault." (p.1)
- introduction: `CONDITION monitoring and` — "CONDITION monitoring and fault diagnosis of machinery equipment have critical signification to improve their availability, safety, and reliability, thus reducing the operation and maintenance costs, and achieving downtime minimization and productivity maximization." (p.1；栏首掉字)
- method: `In this article` — "In this article, an FMD method is proposed for the adaptive filtering mode and machinery fault feature-oriented decomposition target." (p.2, II)
- experiments: `Bearing compound fault` — "Bearing compound fault diagnosis is always considered a challenging task compared with the single fault diagnosis [29]." (p.6, III.B)
- conclusion: `Decomposition methods were` — "Decomposition methods were considered one of the most effective tools for signal multicomponent analysis." (p.11)

## Gap transitions

- therefore (introduction): "Therefore, the periodic impulses in the vibration signal are always considered as the important indicators of machinery fault." (p.1)
- yet (introduction): "Yet, with the advancement of modern equipment towards high integration, the structure and composition are increasingly complex resulting in more components and interferences in the measured signal that seriously decreases the signal-to-noise ratio (SNR) of the signal as well as affects the extraction of fault information." (p.1)
- however (introduction): "However, some limitations, i.e., mode mixing and boundary effect etc., that restrict its performance in machinery fault diagnosis." (p.1)
- although (introduction): "Although plenty of improvements [12], [13] have mitigated the problems derived from these decomposition theories, EEMD and LMD are essentially recursive as well as data-driven methods that never consider the form of fault feature." (p.2)
- although (introduction): "Although numerous efforts have been devoted to parameter selection, it is still elusive to use VMD without any prior knowledge." (p.2)
- motivated by (introduction): "Motivated by these limitations, a new adaptive decomposition theory, called feature mode decomposition (FMD), is proposed in this article." (p.2)
- despite (conclusion): "Despite the advantages, improvements in the proposed FMD still need to be investigated in further research." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a new decomposition theory … is tailored"; "FMD, is proposed in this article"; "FMD, was proposed in this article"
- demonstrate / causal / abstract: "The superiority of the FMD is demonstrated to adaptively and accurately decompose the fault mode"
- verify / causal / experiments, conclusion: "the results from simulations A and B, as well as experiments A and B, verify the conclusion"; "These superiorities were verified by the numerical and experimental data"
- reveal / causal / conclusion: "The results reveal that the proposed FMD was a more suitable alternative"
- would be / speculative / conclusion: "the research about the optimal selection of these parameters would be significant, which might indicate the future research direction"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. The proposed FMD is elaborated through four parts in Section II. To verify the effectiveness of FMD, two simulation cases with bearing single fault and compound fault are applied in Section III. In Section IV, the real data from wind turbine bearing single fault and wheel bearing compound fault is further used for verification. The results and comparison of the proposed FMD and most popular decomposition method, VMD are discussed in Section V. Finally, the conclusion is drawn in Section VI." (p.2)
- method → experiments: 流程说明后进入仿真 / 实测 (p.6)
- experiments → discussion: 复合故障结果后 `V. DISCUSSION` (p.10)
- discussion → conclusion: 计算时间段落后 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `In this article, a new … theory, [NAME], is tailored for`。
- R002 Introduction 无独立 Related Work，用编号问题列表收口，再 `Motivated by these limitations, … is proposed in this article`。
- R003 贡献用 `The main contributions of this article are summarized as follows.` + 编号。
- R004 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI，实验后另设 `DISCUSSION`。
- R005 Conclusion 先收回方法，再用 `Despite the advantages` 承认参数与冗余迭代局限。

## Candidate phrases

- `In this article, a new decomposition theory, feature mode decomposition (FMD), is tailored for` (abstract)
- `Motivated by these limitations, a new adaptive decomposition theory, called feature mode decomposition (FMD), is proposed in this article.` (introduction)
- `The main contributions of this article are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `Despite the advantages, improvements in the proposed FMD still need to be investigated in further research.` (conclusion)

## House style

自称 `this article` / `In this article` / `the proposed FMD` / `the proposed method`。未见 `Here we`、`In this paper`。`In this article … is proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In this article, a new decomposition theory, feature mode decomposition (FMD), is tailored for the feature extraction of machinery fault.
- p.1 abstract: The superiority of the FMD is demonstrated to adaptively and accurately decompose the fault mode as well as robust to other interferences and noise using simulated and experimental data collected from bearing single and compound fault.
- p.1 abstract: Moreover, it has been demonstrated that FMD has superiority in feature extraction of machinery fault compared with the most popular variational mode decomposition.
- p.1 introduction: CONDITION monitoring and fault diagnosis of machinery equipment have critical signification to improve their availability, safety, and reliability, thus reducing the operation and maintenance costs, and achieving downtime minimization and productivity maximization.
- p.1 introduction: Therefore, the periodic impulses in the vibration signal are always considered as the important indicators of machinery fault.
- p.1 introduction: Yet, with the advancement of modern equipment towards high integration, the structure and composition are increasingly complex resulting in more components and interferences in the measured signal that seriously decreases the signal-to-noise ratio (SNR) of the signal as well as affects the extraction of fault information.
- p.1 introduction: However, some limitations, i.e., mode mixing and boundary effect etc., that restrict its performance in machinery fault diagnosis.
- p.2 introduction: Although plenty of improvements [12], [13] have mitigated the problems derived from these decomposition theories, EEMD and LMD are essentially recursive as well as data-driven methods that never consider the form of fault feature.
- p.2 introduction: Although numerous efforts have been devoted to parameter selection, it is still elusive to use VMD without any prior knowledge.
- p.2 introduction: Motivated by these limitations, a new adaptive decomposition theory, called feature mode decomposition (FMD), is proposed in this article.
- p.2 introduction: The main contributions of this article are summarized as follows.
- p.2 introduction: The rest of this article is organized as follows. The proposed FMD is elaborated through four parts in Section II. To verify the effectiveness of FMD, two simulation cases with bearing single fault and compound fault are applied in Section III. In Section IV, the real data from wind turbine bearing single fault and wheel bearing compound fault is further used for verification. The results and comparison of the proposed FMD and most popular decomposition method, VMD are discussed in Section V. Finally, the conclusion is drawn in Section VI.
- p.2 method: In this article, an FMD method is proposed for the adaptive filtering mode and machinery fault feature-oriented decomposition target.
- p.6 experiments: Bearing compound fault diagnosis is always considered a challenging task compared with the single fault diagnosis [29].
- p.10 discussion: VMD as the existing state-of-the-art and most popular decomposition method has been widely applied in the field of machinery fault diagnosis.
- p.11 conclusion: Decomposition methods were considered one of the most effective tools for signal multicomponent analysis.
- p.11 conclusion: Motivated by this, a new adaptive decomposition theory, FMD, was proposed in this article.
- p.11 conclusion: The results reveal that the proposed FMD was a more suitable alternative for the machinery signal decomposition analysis than the most popular VMD.
- p.11 conclusion: Despite the advantages, improvements in the proposed FMD still need to be investigated in further research.
