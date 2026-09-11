---
key: DBWS2RE2
title: "A Comprehensively Improved Interval Type-2 Fuzzy Neural Network for NOx Emissions Prediction in MSWI Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3245640"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PROBLEM FORMULATION AND PRELIMINARIES` → `III. COMPREHENSIVELY IMPROVED IT2FNN (CI-IT2FNN)` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 GPR/SVR/BPNN/LSTM/FNN/IT2FNN 结构与参数学习）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `CASE STUDY`（燃气轮机基准 + 真实 MSWI）。

## Openers

- abstract: `The accurate and` — "The accurate and timely prediction of nitrogen oxides (NOx) emissions ensures eco-friendly and efficient operations for municipal solid waste incineration (MSWI) plants." (p.11286)
- introduction: `THE municipal solid` — "THE municipal solid waste incineration (MSWI) has become a widely adopted municipal solid waste (MSW) disposal technology in the world with the advantages of harmless, reduction, and resource." (p.11286)
- method: `In this article` — "In this article, NRS is introduced to extract the fuzzy rules and initialize the consequent parameters." (p.11288)
- experiments: `In this section` — "In this section, before evaluating the prediction ability of CI-IT2FNN with real industrial data, the proposed approach is first verified by a benchmark problem." (p.11292)
- conclusion: `In this article` — "In this article, a comprehensively improved IT2FNN was proposed for NOx emissions prediction in MSWI processes." (p.11295)

## Gap transitions

- however (introduction): "However, the emissions including nitrogen oxides (NOx) may exceed the standard due to the unstable operation of the incinerator." (p.11286)
- however (introduction): "However, the generalization performance of these conventional machine learning models may be limited when facing complex nonlinear problems." (p.11286)
- nevertheless (introduction): "Nevertheless, the ignored process uncertainty may limit the model accuracy [13]." (p.11286)
- however (introduction): "However, how to determine the structure and parameters of FNNs to obtain an accurate prediction model fast is still a challenging problem." (p.11287)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "This article proposes a comprehensively improved interval type-2 fuzzy neural network (CI-IT2FNN)"; "a comprehensively improved IT2FNN (CI-IT2FNN) is proposed in this article"; "a comprehensively improved IT2FNN was proposed"
- demonstrate / causal / abstract: "the proposed CI-IT2FNN demonstrates its effectiveness and superiority on NOx emissions prediction"
- show / causal / experiments: "showing the effectiveness of the NRS-based structure design method and the adaptive FMFs"
- may / speculative / introduction, conclusion: "the ignored process uncertainty may limit the model accuracy"; "it may be more suitable" 未见此篇 conclusion 用 may；conclusion 用 "is still a challenge problem"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section II reviews the MSWI process and IT2FNN. The design details of the proposed CI-IT2FNN are presented in Section III. In Section IV, the feasibility and superiority of the proposed method are verified based on the benchmark dataset and the real MSWI dataset. Finally, Section V concludes this article." (p.11287)
- method → experiments: 预测流程 Step 5 后 `IV. CASE STUDY` (p.11292)
- experiments → conclusion: 效率分析后 `V. CONCLUSION` (p.11295)

## Candidate rules

- R009 摘要用 `This article proposes` 点名 CI-IT2FNN。
- R002 Introduction 无独立 Related Work，FNN/IT2FNN 评述写在引言中段。
- R004 贡献列表：`The main contributions of this article can be summarized as follows.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法，再用 `Hence, ... will be taken into consideration in future studies` 指向后续。

## Candidate phrases

- `This article proposes a comprehensively improved` (abstract)
- `The main contributions of this article can be summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a comprehensively improved IT2FNN was proposed` (conclusion)

## House style

自称 `This article proposes` / `is proposed in this article` / `the proposed CI-IT2FNN`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.11286 abstract: The accurate and timely prediction of nitrogen oxides (NOx) emissions ensures eco-friendly and efficient operations for municipal solid waste incineration (MSWI) plants.
- p.11286 abstract: Due to the high nonlinearity and uncertainty in MSWI processes, constructing an efficient prediction model remains challenging.
- p.11286 abstract: This article proposes a comprehensively improved interval type-2 fuzzy neural network (CI-IT2FNN) for NOx emissions prediction.
- p.11286 abstract: Finally, after being evaluated by a benchmark simulation, the proposed CI-IT2FNN demonstrates its effectiveness and superiority on NOx emissions prediction.
- p.11286 introduction: THE municipal solid waste incineration (MSWI) has become a widely adopted municipal solid waste (MSW) disposal technology in the world with the advantages of harmless, reduction, and resource.
- p.11286 introduction: However, the emissions including nitrogen oxides (NOx) may exceed the standard due to the unstable operation of the incinerator.
- p.11286 introduction: However, the generalization performance of these conventional machine learning models may be limited when facing complex nonlinear problems.
- p.11286 introduction: Nevertheless, the ignored process uncertainty may limit the model accuracy [13].
- p.11287 introduction: However, how to determine the structure and parameters of FNNs to obtain an accurate prediction model fast is still a challenging problem.
- p.11287 introduction: The main contributions of this article can be summarized as follows.
- p.11287 introduction: The rest of this article is organized as follows. Section II reviews the MSWI process and IT2FNN. The design details of the proposed CI-IT2FNN are presented in Section III. In Section IV, the feasibility and superiority of the proposed method are verified based on the benchmark dataset and the real MSWI dataset. Finally, Section V concludes this article.
- p.11288 method: In this article, NRS is introduced to extract the fuzzy rules and initialize the consequent parameters.
- p.11292 experiments: In this section, before evaluating the prediction ability of CI-IT2FNN with real industrial data, the proposed approach is first verified by a benchmark problem.
- p.11292 experiments: As can be seen, the curve of the predicted almost coincides with the curve of the actual values, demonstrating the effectiveness of the proposed algorithm.
- p.11295 conclusion: In this article, a comprehensively improved IT2FNN was proposed for NOx emissions prediction in MSWI processes.
- p.11295 conclusion: Based on the bench mark and the real industrial applications, the effectiveness and superiority of CI-IT2FNN was verified.
- p.11295 conclusion: Hence, to better adapt to nonstationary environments, the online adjustment of structure size and parameters will be taken into consideration in future studies.
