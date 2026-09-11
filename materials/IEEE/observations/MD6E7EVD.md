---
key: MD6E7EVD
title: "Robust Missing Value Imputation With Proximal Optimal Transport for Low-Quality IIoT Data"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2025.3601130"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PRELIMINARIES` → `IV. METHODOLOGY` → `V. EMPIRICAL INVESTIGATION` → `VI. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCALUTURE`。有独立 Related Work。`related_work=independent`。Introduction 用 `Organization:` 列节序，Related Work 排在 Preliminaries 之前、正文第二节。Method 前有 `PRELIMINARIES`。Experiments 标题为 `EMPIRICAL INVESTIGATION`（脱丁烷塔）。Conclusion 后另立 `LIMITATIONS AND FUTURE WORK`。

## Openers

- abstract: `Accurate imputation of` — "Accurate imputation of missing data is crucial in the Industrial Internet-of-Things (IIoT), where operations are often compromised by noisy samples from harsh environments." (p.82)
- introduction: `MISSING data are` — "MISSING data are a pervalent challenge in Industrial Internet of Things (IIoT) analytics [44], [53], [58], primarily caused by sensor failures under harsh operational conditions [48]." (p.82；栏首掉字)
- related_work: `MDI aims to` — "MDI aims to estimate missing data using observed ones [27], with current techniques falling into discriminative and generative paradigms [15]." (p.83, II)
- method: `This article investigates` — "This article investigates the MDI problem within the context of IIoT." (p.85, IV.A)
- experiments: `The efficacy of` — "The efficacy of POT-I to handle low-quality IIoT data can be empirically justified through the aspects as follows:" (p.88, V)
- conclusion: `This study explores` — "This study explores and enhances the utility of OT for IIoT data imputation, focusing specifically on its capacity to handle noisy data." (p.92)

## Gap transitions

- to address (abstract): "To address this issue, we recast data imputation as a distribution alignment challenge, utilizing the flexibility of optimal transport (OT) to handle noisy samples." (p.82)
- therefore (introduction): "Therefore, each paradigm has unique advantages and defects, and should be evaluated before the application to specific IIoT scenarios." (p.83)
- therefore (introduction): "Therefore, existing techniques treat data missingness independently of data noise, producing imputations that are skewed by the noise in the observed data." (p.83)
- to address (introduction): "To address the challenges posed by noisy samples in IIoT datasets, this work reformulates data imputation as a distribution matching problem and innovatively leverages advanced optimal transport (OT) techniques to eliminate noisy samples from imputation." (p.83)
- despite (related work): "Despite their flexibility and capability, the round-robin and factorization imputers require careful model selection, which is challenging amidst incomplete data [15]." (p.83)
- to this end (conclusion): "To this end, we introduce the POT-I framework, which utilizes a generalized OT model, POT, tailored to match normal samples between distributions while excluding noisy samples." (p.92)

## Hedge verbs

- recast / causal / abstract: "we recast data imputation as a distribution alignment challenge"
- introduce / causal / abstract, introduction: "we first introduce the Proximal Optimal Transport (POT) problem"; "we introduce the Proximal Optimal Transport (POT) problem"
- propose / causal / abstract: "we propose the POT-I framework"
- demonstrate / causal / abstract: "Experiments on real-world IIoT datasets demonstrate the superiority of POT-I over state-of-the-art imputation methods."
- investigate / causal / method: "This article investigates the MDI problem within the context of IIoT."
- explore / causal / conclusion: "This study explores and enhances the utility of OT for IIoT data imputation"

## Cross-section linkers

- introduction → related work: "Organization: In Section III, we present the technical preliminaries essential for understanding the proposed approach. In Section II, we categorize current data imputation methods into three groups, discussing their strengths and weaknesses. In Section IV, we detail the computational workflow of our proposed method. In Section V, we deploy our method to an industrial case study, specifically focusing on a debutanizer column, and evaluate its performance empirically. In Section VI, we discuss the conclusion, limitations, and potential avenues for future work." (p.83)
- related work → preliminaries: 生成范式缺陷段落后 `III. PRELIMINARIES` (p.84)
- preliminaries → method: 网络单纯形段落后 `IV. METHODOLOGY` (p.85)
- method → experiments: MAE/RMSE 定义后 `V. EMPIRICAL INVESTIGATION` (p.88)
- experiments → conclusion: 超参分析后 `VI. CONCLUSION`，再接 `LIMITATIONS AND FUTURE WORK` (p.92)

## Candidate rules

- R001 abstract 用 `To address this issue, we recast` + `we propose the POT-I framework`，不用 `Here we`。
- R002 Introduction 用 `Organization:` 列节序，Related Work 排在 Preliminaries 之前。
- R003 贡献用独立 `Contribution:` 小标题 + 编号列表。
- R004 Method 前加 `PRELIMINARIES`；Experiments 标题为 `EMPIRICAL INVESTIGATION`。
- R005 Conclusion 用 `This study explores`，局限另立 `LIMITATIONS AND FUTURE WORK`。

## Candidate phrases

- `To address this issue, we recast` (abstract)
- `To address the challenges posed by noisy samples` (introduction)
- `This article investigates the MDI problem within the context of` (method)
- `The efficacy of POT-I to handle low-quality IIoT data can be empirically justified through the aspects as follows:` (experiments)
- `To this end, we introduce the POT-I framework` (conclusion)

## House style

自称是 `we recast` / `we propose` / `this work` / `This article investigates` / `This study explores` / `our proposed method`。未见 `Here we`。`This article investigates` 与 `This study explores` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.82 abstract: Accurate imputation of missing data is crucial in the Industrial Internet-of-Things (IIoT), where operations are often compromised by noisy samples from harsh environments.
- p.82 abstract: To address this issue, we recast data imputation as a distribution alignment challenge, utilizing the flexibility of optimal transport (OT) to handle noisy samples.
- p.82 abstract: Subsequently, we propose the POT-I framework, where the objective is to minimize the transport cost of POT.
- p.82 abstract: Experiments on real-world IIoT datasets demonstrate the superiority of POT-I over state-of-the-art imputation methods.
- p.82 introduction: MISSING data are a pervalent challenge in Industrial Internet of Things (IIoT) analytics [44], [53], [58], primarily caused by sensor failures under harsh operational conditions [48].
- p.83 introduction: Therefore, existing techniques treat data missingness independently of data noise, producing imputations that are skewed by the noise in the observed data.
- p.83 introduction: To address the challenges posed by noisy samples in IIoT datasets, this work reformulates data imputation as a distribution matching problem and innovatively leverages advanced optimal transport (OT) techniques to eliminate noisy samples from imputation.
- p.83 introduction: Organization: In Section III, we present the technical preliminaries essential for understanding the proposed approach. In Section II, we categorize current data imputation methods into three groups, discussing their strengths and weaknesses. In Section IV, we detail the computational workflow of our proposed method. In Section V, we deploy our method to an industrial case study, specifically focusing on a debutanizer column, and evaluate its performance empirically. In Section VI, we discuss the conclusion, limitations, and potential avenues for future work.
- p.83 related work: MDI aims to estimate missing data using observed ones [27], with current techniques falling into discriminative and generative paradigms [15].
- p.85 method: This article investigates the MDI problem within the context of IIoT.
- p.85 method: To fill in the gap, we introduce POT-I, a generalized OT imputation framework designed for robust imputation in the presence of noisy samples.
- p.88 experiments: The efficacy of POT-I to handle low-quality IIoT data can be empirically justified through the aspects as follows:
- p.88 experiments: We conduct a case study based on the Debutanizer Column (dc), an exemplary industrial application for desulfuration and naphtha split.
- p.92 conclusion: This study explores and enhances the utility of OT for IIoT data imputation, focusing specifically on its capacity to handle noisy data.
- p.92 conclusion: To this end, we introduce the POT-I framework, which utilizes a generalized OT model, POT, tailored to match normal samples between distributions while excluding noisy samples.
- p.92 limitations: Our research, consistent with prevalent imputation methods [27], [57] and IIoT data-driven models [52], does not account for the potential temporal dynamics present in IIoT datasets, such as trends and rapid changes.
