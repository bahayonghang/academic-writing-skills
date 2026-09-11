---
key: ILVRU38T
title: "Semi-Supervised Probabilistic Learning Network for Soft Sensor Modeling With Partially Labeled Data"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2025.3576122"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED APPROACH: SS-PLN` → `IV.`（收敛分析，接在方法后）→ `V. CASE STUDY` → `VI. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。作者稿分页为 1–13。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLM / DNN-PLM / VAE，再列三项挑战）。Introduction 末无 `The rest of this article` 路标，直接进 Preliminaries。Method 为 `III. PROPOSED APPROACH: SS-PLN`。Experiments 标题为 `V. CASE STUDY`（糖结晶 + 炼钢）。

## Openers

- abstract: `Deep probabilistic learning` — "Deep probabilistic learning networks have been applied in industrial soft sensors." (p.1)
- introduction: `IN industrial processes` — "IN industrial processes, acquiring real-time information regarding process variables holds great significance in ensuring production safety and maintaining stable operation [1]–[3]." (p.1；栏首掉字)
- method: `This work focuses` — "This work focuses on soft sensing tasks under a semi-supervised leaning context." (p.3, III.A)
- experiments: `In this section` — "In this section, the feasibility and efficacy of the proposed SS-PLN are evaluated through two real-life industrial processes, including a sugar crystallization process and a steel-making process." (p.7, V)
- conclusion: `The current work` — "The current work presented a novel semi-supervised probabilistic latent network (SS-PLN) that addressed three critical challenges in industrial soft sensing: 1) latent variable inference through optimal control signal optimization, 2) probabilistic modeling via mean-covariance parameterization with DNN backends, 3) effective utilization of partially labeled data through divergence minimization between the supervised component (S-PLN) and unsupervised component (U-PLN)." (p.12)

## Gap transitions

- however (abstract): "However, they face significant challenges in latent variable inference, deep learning backend implementation, and labeled data scarcity." (p.1)
- to address (abstract): "To address these challenges, this work proposes a novel semi-supervised probabilistic learning network (SS-PLN) for soft sensor modeling with partially labeled data." (p.1)
- however (introduction): "However, the direct measurement of certain quality variables is often hindered by harsh acquisition environments and the high costs associated with physical sensors, creating challenges for efficient process optimization and quality control." (p.1)
- however (introduction): "However, traditional PLMs (e.g., probabilistic principal component analysis) struggle to adapt to modern industrial applications." (p.1)
- despite (introduction): "Despite the progress, designing deep PLMs for soft sensing tasks faces three pivotal challenges from the perspective of latent variable inference and model construction: 1) inaccurate inference of latent variables, 2) model implementation with DNN backends, and 3) handling partially labeled data." (p.2)
- for addressing (introduction): "For addressing the aforementioned issues, this paper proposes a new semi-supervised probabilistic learning network (SS-PLN)." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, method: "this work proposes a novel semi-supervised probabilistic learning network (SS-PLN)"; "this paper proposes a new semi-supervised probabilistic learning network (SS-PLN)"; "SS-PLN is proposed in this paper"
- validate / causal / abstract: "The feasibility and effectiveness of the proposed SS-PLN are validated through comparisons with recent semi-supervised learning methods"
- confirm / causal / conclusion: "the state-of-the-art performance confirms the efficacy and superiority of the proposed SS-PLN"
- may / speculative / introduction: "This omission might lead to inaccurate inference results of latent variable."
- could / speculative / conclusion: "investigation of advanced pseudo-labeling techniques to potentially unlock performance improvement could yield significant insights"

## Cross-section linkers

- introduction → preliminaries: 贡献列表后直接 `II. PRELIMINARIES` / `A. Variational Inference`，无节序路标句 (p.2)
- method → experiments: 收敛证明后 `V. CASE STUDY`："In this section, the feasibility and efficacy of the proposed SS-PLN are evaluated through two real-life industrial processes" (p.7)
- experiments → conclusion: 伪标签分析后直接 `VI. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 贡献句用 `this work proposes a novel ... (SS-PLN)`，三项挑战先编号再逐项 `The first issue is addressed`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段；无 `The rest of this article is organized as follows`。
- R003 贡献用 `This paper mainly contributes in the following aspects:` + 编号列表。
- R004 Experiments 标题为 `CASE STUDY`，先给对比方法清单再分过程。
- R005 Conclusion 用 `The current work presented` 收回三项挑战，再用 `For future work, it is of interest to`。

## Candidate phrases

- `this work proposes a novel semi-supervised probabilistic learning network (SS-PLN)` (abstract)
- `To address these challenges, this work proposes` (abstract)
- `This paper mainly contributes in the following aspects:` (introduction)
- `The current work presented a novel` (conclusion)
- `For future work, it is of interest to` (conclusion)

## House style

自称是 `this work` / `this paper` / `The current work` / `the proposed SS-PLN`。未见 `Here we`。`this work proposes` 与 `this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 开篇；引言用 `this paper proposes`，结论用 `The current work presented`。

## Quotes

- p.1 abstract: Deep probabilistic learning networks have been applied in industrial soft sensors.
- p.1 abstract: However, they face significant challenges in latent variable inference, deep learning backend implementation, and labeled data scarcity.
- p.1 abstract: To address these challenges, this work proposes a novel semi-supervised probabilistic learning network (SS-PLN) for soft sensor modeling with partially labeled data.
- p.1 abstract: The feasibility and effectiveness of the proposed SS-PLN are validated through comparisons with recent semi-supervised learning methods, using data from two industrial processes.
- p.1 introduction: IN industrial processes, acquiring real-time information regarding process variables holds great significance in ensuring production safety and maintaining stable operation [1]–[3].
- p.1 introduction: However, traditional PLMs (e.g., probabilistic principal component analysis) struggle to adapt to modern industrial applications.
- p.2 introduction: Despite the progress, designing deep PLMs for soft sensing tasks faces three pivotal challenges from the perspective of latent variable inference and model construction: 1) inaccurate inference of latent variables, 2) model implementation with DNN backends, and 3) handling partially labeled data.
- p.2 introduction: For addressing the aforementioned issues, this paper proposes a new semi-supervised probabilistic learning network (SS-PLN).
- p.2 introduction: This paper mainly contributes in the following aspects:
- p.3 method: This work focuses on soft sensing tasks under a semi-supervised leaning context.
- p.3 method: Motivated by handling the aforementioned challenging problems, SS-PLN is proposed in this paper.
- p.7 experiments: In this section, the feasibility and efficacy of the proposed SS-PLN are evaluated through two real-life industrial processes, including a sugar crystallization process and a steel-making process.
- p.8 experiments: As illustrated, under each scenario of LSR, the proposed SS-PLN outperforms its peers in terms of all the evaluation metrics of RMSE, MAE and R2.
- p.12 conclusion: The current work presented a novel semi-supervised probabilistic latent network (SS-PLN) that addressed three critical challenges in industrial soft sensing: 1) latent variable inference through optimal control signal optimization, 2) probabilistic modeling via mean-covariance parameterization with DNN backends, 3) effective utilization of partially labeled data through divergence minimization between the supervised component (S-PLN) and unsupervised component (U-PLN).
- p.12 conclusion: Comprehensive experiments were conducted on two actual-run industrial processes, i.e., the sugar crystallization and steel-making processes, where the state-of-the-art performance confirms the efficacy and superiority of the proposed SS-PLN.
- p.12 conclusion: For future work, it is of interest to extend SS-PLN through mixture distributions and skewed distributions to better model the complex non-Gaussian characteristics within process data.
