---
key: 2ZC6ALPN
title: "A Sentinel-Based Adaptive Hybrid Soft Sensing Method for Industrial Process Monitoring"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3554879"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. SENTINEL-BASED ADAPTIVE HYBRID SOFT SENSING` → `IV. CASE STUDY: APPLICATION ON TAILING GRADE ESTIMATION IN FROTH FLOTATION INDUSTRY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORK`，下设 `A. Soft-Sensing in Industrial Process Monitoring` 与 `B. Hybrid Feature Integration Approaches`）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDY`（浮选尾矿品位）。

## Openers

- abstract: `In dynamic industrial` — "In dynamic industrial environments, effective soft-sensing methods need adapt to real-time variations in process conditions." (p.1)
- introduction: `SOFT sensing has` — "SOFT sensing has been widely used in process monitoring, which employ learning models to estimate key performance indicators (KPIs)." (p.1；栏首掉字)
- method: `As shown in` — "As shown in Fig. 1, SAHSS consists of a deep learning-based monitoring branch (DL-branch), a handcrafted feature-based monitoring branch (HF-branch), and a sentinel controller." (p.3, III)
- experiments: `Froth flotation is` — "Froth flotation is an important mineral concentration method." (p.6, IV.A)
- conclusion: `In this study` — "In this study, to leverage the complementary strength of handcrafted features and deep learning construct a resilient soft sensing model that can adapt to real-time process variations, a SAHSS has been proposed." (p.11–12)

## Gap transitions

- though (abstract): "Though recent efforts have integrated deep learning and handcrafted features to design hybrid feature methods while reducing reliance on diverse training data, existing approaches often rely on fixed fusion strategies, limiting their adaptability." (p.1)
- however (introduction): "However, existing methods primarily rely on fixed fusion strategies that do not account for real-time variations in process conditions." (p.1)
- despite (related work): "Despite both handcrafted and deep learning methods achieved success, handcrafted methods typically lack the capacity to capture the rich and complex visual patterns, while deep learning models often struggle with distribution shifts in dynamic industrial environments." (p.2)
- to address (related work): "To address the respective shortcomings of deep learning and handcrafted feature-based models, several hybrid approaches have been proposed." (p.2)
- however (conclusion): "However, SAHSS lacks full lifelong learning capabilities, and its performance may degrade under drastic process shifts without model retraining." (p.12)
- future work (conclusion): "Future work will focus on incorporating lifelong learning to improve robustness in dynamic industrial environments." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a sentinel-based adaptive hybrid soft sensing (SAHSS) method"; "In this study, we propose a sentinel-based adaptive hybrid soft sensing (SAHSS) method"
- develop / causal / abstract, introduction: "we develop a mixup bidirectional adversarial autoencoder (MixBiAAE)"
- demonstrate / causal / abstract, introduction: "Extensive experiments on an industrial flotation dataset demonstrate that our method outperforms existing hybrid soft sensing techniques"; "Extensive experiments demonstrate significant improvements"
- show / causal / experiments: "Fig. 4 shows reconstruction results of different methods"; "Experiment results are summarized in Fig. 7 and Table IV"

## Cross-section linkers

- introduction → later sections: "The remainder of this article is organized as follows. Section II briefly describes the related work. Details of SAHSS is presented in Section III. Ablation studies and comparison experiments that have been conducted are described in Section IV. Section V concludes this article." (p.2)
- related work → method: Related Work 末句 "Our SAHSS dynamically shifts between feature branches based on real-time feature reliability, optimizing both adaptability and computational efficiency in industrial monitoring settings." 随后 `III. SENTINEL-BASED ADAPTIVE HYBRID SOFT SENSING` (p.2–3)
- method → experiments: Sentinel 段落后直接 `IV. CASE STUDY: APPLICATION ON TAILING GRADE ESTIMATION IN FROTH FLOTATION INDUSTRY` (p.6)
- experiments → conclusion: 结果段落后直接 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 贡献用 `In this study, we propose` + 方法缩写。
- R002 独立 Related Work 分 `A.` 任务综述与 `B.` 方法族综述，末段收回本文方法。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions of this work are threefold` + 编号列表。
- R005 Conclusion 用 `However` 承认局限，再用 `Future work will focus on` 指向后续。

## Candidate phrases

- `In this study, we propose` (abstract, introduction)
- `The contributions of this work are threefold.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `Extensive experiments demonstrate significant improvements` (introduction)
- `However, SAHSS lacks full lifelong learning capabilities` (conclusion)
- `Future work will focus on incorporating lifelong learning` (conclusion)

## House style

自称是 `In this study, we propose` / `we develop` / `our method` / `this article`。未见 `Here we`。`In this study, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。路标用 `this article`。

## Quotes

- p.1 abstract: In dynamic industrial environments, effective soft-sensing methods need adapt to real-time variations in process conditions.
- p.1 abstract: Though recent efforts have integrated deep learning and handcrafted features to design hybrid feature methods while reducing reliance on diverse training data, existing approaches often rely on fixed fusion strategies, limiting their adaptability.
- p.1 abstract: In this study, we propose a sentinel-based adaptive hybrid soft sensing (SAHSS) method, which dynamically shifts between deep learning and handcrafted features to enhance representation adaptability under changing conditions.
- p.1 abstract: Extensive experiments on an industrial flotation dataset demonstrate that our method outperforms existing hybrid soft sensing techniques, offering a robust and adaptive solution for industrial process monitoring.
- p.1 introduction: SOFT sensing has been widely used in process monitoring, which employ learning models to estimate key performance indicators (KPIs).
- p.1 introduction: However, existing methods primarily rely on fixed fusion strategies that do not account for real-time variations in process conditions.
- p.2 introduction: In this study, we propose a sentinel-based adaptive hybrid soft sensing (SAHSS) method, which employs a sentinel to dynamically switch between deep learning monitoring and handcrafted feature monitoring based on real-time feature reliability checks.
- p.2 introduction: The contributions of this work are threefold.
- p.2 introduction: The remainder of this article is organized as follows. Section II briefly describes the related work. Details of SAHSS is presented in Section III. Ablation studies and comparison experiments that have been conducted are described in Section IV. Section V concludes this article.
- p.2 related work: Despite both handcrafted and deep learning methods achieved success, handcrafted methods typically lack the capacity to capture the rich and complex visual patterns, while deep learning models often struggle with distribution shifts in dynamic industrial environments.
- p.3 method: As shown in Fig. 1, SAHSS consists of a deep learning-based monitoring branch (DL-branch), a handcrafted feature-based monitoring branch (HF-branch), and a sentinel controller.
- p.6 experiments: Froth flotation is an important mineral concentration method.
- p.11–12 conclusion: In this study, to leverage the complementary strength of handcrafted features and deep learning construct a resilient soft sensing model that can adapt to real-time process variations, a SAHSS has been proposed.
- p.12 conclusion: However, SAHSS lacks full lifelong learning capabilities, and its performance may degrade under drastic process shifts without model retraining.
- p.12 conclusion: Future work will focus on incorporating lifelong learning to improve robustness in dynamic industrial environments.
