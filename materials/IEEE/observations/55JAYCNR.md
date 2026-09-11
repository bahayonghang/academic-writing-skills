---
key: 55JAYCNR
title: "Ensemble Deep Random Vector Functional Link Neural Network Based on Fuzzy Inference System"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2024.3411614"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PROPOSED EDRVFL BASED ON FIS (EDRVFL-FIS)` → `IV. EXPERIMENTS AND RESULTS` → `V.` 讨论（`Discussions Based on the Results`）→ `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立相关工作节 `II. RELATED WORKS`（RVFL / edRVFL / TSK neuro-FIS）。`related_work=independent`。Introduction 末有 `The rest of this article is organized as follows` 路标，指向 II–VI。Method 在 III。Experiments 标题为 `EXPERIMENTS AND RESULTS`（UCI / NDC）。另有独立讨论节。

## Openers

- abstract: `The ensemble deep` — "The ensemble deep random vector functional link (edRVFL) neural network has demonstrated the ability to address the limitations of conventional artificial neural networks." (p.1)
- introduction: `THE efficacy of` — "THE efficacy of neural network (NN)-based models stems from their ability to discern intricate latent patterns within input and output vectors, leveraging their inherent ability to capture complex relationships in data." (p.1；栏首掉字)
- method: `In this section` — "In this section, we fuse the FIS, (i.e., TSK) with the edRVFL structure and propose a hybrid edRVFL-FIS model that has a rich feature representation." (p.4, III)
- experiments: `The section presents` — "The section presents comprehensive details on the datasets and the compared models." (p.6, IV)
- conclusion: `We proposed the` — "We proposed the edRVFL-FIS model, a result of the seamless adaptation of FIS systems with edRVFL, meticulously crafted through a rigorous mathematical framework." (p.11)

## Gap transitions

- however (abstract): "However, since edRVFL generates features for its hidden layers through random projection, it can potentially lose intricate features or fail to capture certain nonlinear features in its base models (hidden layers)." (p.1)
- however (introduction): "However, in BP-based NNs, several challenges arise during the training process, such as potential slowness, susceptibility to local optima [5], and the critical influence of factors such as learning rate and initialization point." (p.1)
- however (introduction): "However, the feature enhancement techniques remain largely unexplored in the context of edRVFL-based models." (p.2)
- therefore (introduction): "Therefore, we propose three variants of the edRVFL-FIS model by incorporating diverse clustering approaches–randomly initialized centers (R-means), K-means, and fuzzy C-means–to establish fuzzy layer centers." (p.2)
- hence (discussions): "Hence, a tailored approach to tuning fuzzy rules is recommended for optimizing the generalization performance of the proposed edRVFL-FIS models." (p.10)

## Hedge verbs

- propose / causal / abstract, introduction, method: "we propose a novel edRVFL based on fuzzy inference system (edRVFL-FIS)"; "we propose an edRVFL based on FIS"; "we fuse the FIS, (i.e., TSK) with the edRVFL structure and propose"
- demonstrate / causal / abstract, conclusion: "Experimental results, statistical tests, discussions, and analyses conducted across UCI and NDC datasets consistently demonstrate"; "The empirical results demonstrate that"
- may / speculative / abstract, conclusion: "it can potentially lose intricate features"; "the presence of redundant features may contribute to increased computational complexity"

## Cross-section linkers

- introduction → related work: "The rest of this article is organized as follows. Section II introduces RVFL, edRVFL, and the Takagi–Sugeno–Kang (TSK) neuro-FIS. Section III details the mathematical framework of the proposed edRVFL-FIS model. Experimental results and statistical analyses of proposed and existing models are discussed in Section IV. The discussions based on the empirical findings are done in Section V. Finally, Section VI concludes this article." (p.3)
- related work → method: "The above-discussed related works not only enhance our understanding of existing models but also pave the way for proposing the edRVFL-FIS model." 随后 `III. PROPOSED EDRVFL BASED ON FIS` (p.3)
- method → experiments: 复杂度段落后接 `IV. EXPERIMENTS AND RESULTS` (p.6)
- discussions → conclusion: 模糊规则分析后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `we propose a novel edRVFL based on fuzzy inference system`，不用 `Here we`。
- R002 独立相关工作标题为 `RELATED WORKS`，末用 `pave the way for proposing` 衔接方法。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The article’s key highlights are as follows.` + 编号列表。
- R005 Conclusion 用 `We proposed` 收回，再用 `This issue necessitates further discussion in the future` 指向后续。

## Candidate phrases

- `we propose a novel edRVFL based on fuzzy inference system` (abstract)
- `The article’s key highlights are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `We proposed the edRVFL-FIS model, a result of the seamless adaptation` (conclusion)
- `This issue necessitates further discussion in the future.` (conclusion)

## House style

自称是 `we propose` / `this article` / `the proposed edRVFL-FIS`。未见 `Here we`。`we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: The ensemble deep random vector functional link (edRVFL) neural network has demonstrated the ability to address the limitations of conventional artificial neural networks.
- p.1 abstract: However, since edRVFL generates features for its hidden layers through random projection, it can potentially lose intricate features or fail to capture certain nonlinear features in its base models (hidden layers).
- p.1 abstract: To enhance the feature learning capabilities of edRVFL, we propose a novel edRVFL based on fuzzy inference system (edRVFL-FIS).
- p.1 abstract: Experimental results, statistical tests, discussions, and analyses conducted across UCI and NDC datasets consistently demonstrate the superior performance of all variations of the proposed edRVFL-FIS model over baseline models such as fuzzy broad learning system.
- p.1 introduction: THE efficacy of neural network (NN)-based models stems from their ability to discern intricate latent patterns within input and output vectors, leveraging their inherent ability to capture complex relationships in data.
- p.1 introduction: However, in BP-based NNs, several challenges arise during the training process, such as potential slowness, susceptibility to local optima [5], and the critical influence of factors such as learning rate and initialization point.
- p.2 introduction: However, the feature enhancement techniques remain largely unexplored in the context of edRVFL-based models.
- p.2 introduction: Therefore, we propose three variants of the edRVFL-FIS model by incorporating diverse clustering approaches–randomly initialized centers (R-means), K-means, and fuzzy C-means–to establish fuzzy layer centers.
- p.2 introduction: The article’s key highlights are as follows.
- p.3 introduction: The rest of this article is organized as follows. Section II introduces RVFL, edRVFL, and the Takagi–Sugeno–Kang (TSK) neuro-FIS. Section III details the mathematical framework of the proposed edRVFL-FIS model. Experimental results and statistical analyses of proposed and existing models are discussed in Section IV. The discussions based on the empirical findings are done in Section V. Finally, Section VI concludes this article.
- p.3 related work: The above-discussed related works not only enhance our understanding of existing models but also pave the way for proposing the edRVFL-FIS model.
- p.4 method: In this section, we fuse the FIS, (i.e., TSK) with the edRVFL structure and propose a hybrid edRVFL-FIS model that has a rich feature representation.
- p.6 experiments: The section presents comprehensive details on the datasets and the compared models.
- p.10 discussions: Hence, a tailored approach to tuning fuzzy rules is recommended for optimizing the generalization performance of the proposed edRVFL-FIS models.
- p.11 conclusion: We proposed the edRVFL-FIS model, a result of the seamless adaptation of FIS systems with edRVFL, meticulously crafted through a rigorous mathematical framework.
- p.11 conclusion: The empirical results demonstrate that the proposed edRVFL-FIS adaptably leverages fuzzification and defuzzification features to enhance generalization performance on large datasets.
- p.11 conclusion: Consequently, the presence of redundant features may contribute to increased computational complexity in the proposed models.
- p.11 conclusion: This issue necessitates further discussion in the future.
