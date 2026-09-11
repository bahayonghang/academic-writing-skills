---
key: SKTLVTJT
title: "Addressing Information Asymmetry: Deep Temporal Causality Discovery for Mixed Time Series"
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence"
doi: "10.1109/TPAMI.2025.3553957"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-19"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV.`（theoretical verification and discussions）→ `V. EXPERIMENTS` → `VI.`（limitations and future work）→ `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`，分 Granger causality discovery 与 mixed data modeling）。`related_work=independent`。Introduction 末为编号贡献，无 `The rest of this article is organized` 路标。Method 标题为 `METHODOLOGY`。Experiments 标题为 `EXPERIMENTS`。局限单独成 `VI`，结论为 `VII. CONCLUSION`。

## Openers

- abstract: `While existing causal` — "While existing causal discovery methods mostly focus on continuous time series, causal discovery for mixed time series encompassing both continuous variables (CVs) and discrete variables (DVs) is a fundamental yet underexplored problem." (p.5723)
- introduction: `GOING beyond classification` — "GOING beyond classification and prediction, recognizing causal structures from time series has become an increasingly critical research topic in recent decades [1], [2], [3]." (p.5723)
- method: `In this section` — "In this section, we first present the problem formulation of MiTS causal discovery. Then, the motivation of this study is analyzed with relevant discussions." (p.5725, III)
- experiments: `In this section` — "In this section, we conduct extensive experiments to evaluate the performance of MiTCD with 18 well-acknowledged and advanced temporal causal discovery methods." (p.5731, V)
- conclusion: `In this paper` — "In this paper, we present a generic MiTCD framework for MiTS causal discovery." (p.5739)

## Gap transitions

- despite (introduction): "Despite the remarkable progress, most causal discovery methods are developed with an inherent assumption that the time series data are solely composed of continuous-valued variables." (p.5723)
- however (introduction): "However, these methods may lose vital information or sacrifice fine-grained continuous signals, thereby inevitably yielding non-negligible estimation errors." (p.5723)
- however (related work): "However, most of the above methods are tailored for continuous time series and are therefore inappropriate for MiTS." (p.5725)
- to sum up (related work): "To sum up, existing causal inference methods for mixed data are typically developed using constraint-based or score-based algorithms, which are primarily suited for tabular data and may be limited to linear or bivariate cases in certain domains." (p.5725)
- in the future (limitations): "In the future, it is of interest to exploit the analysis of generalized mixed variables ... by empowering MiTCD with hybrid modeling strategies" (p.5739)

## Hedge verbs

- propose / causal / abstract, related work: "we propose a generic deep mixed time series temporal causal discovery framework"; "we propose a systematic framework for inferring GC relationships for MiTS"
- present / causal / introduction, conclusion: "we present MiTCD, a deep Mixed Time Series Causal Discovery framework"; "we present a generic MiTCD framework"
- validate / causal / abstract: "extensive empirical evaluations and in-depth investigations validate the superior performance of our framework"
- may / speculative / abstract, introduction: "DVs may originate from latent continuous variables (LCVs)"; "these methods may lose vital information"
- can / speculative / conclusion: "pre-trained CAGKE exhibits superior portability and is compatible with various causal discovery approaches"

## Cross-section linkers

- introduction → related work: 编号贡献后直接 `II. RELATED WORKS`，无独立路标句 (p.5724)
- related work → method: "Fortunately, our proposed MiTCD approach can handle multivariate nonlinear temporal causal relationships" 随后 `III. METHODOLOGY` (p.5725)
- method → experiments: 可行性讨论后接 `V. EXPERIMENTS` (p.5731)
- experiments → limitations → conclusion: 多状态离散变量分析后接局限节，再 `VII. CONCLUSION` (p.5739)

## Candidate rules

- R001 abstract 用 `Thereupon, we propose` / `Our key idea is`，不用 `Here we`。
- R002 独立 Related Work；引言中段把挑战命名为 `Information Asymmetry (InfoA)`。
- R003 贡献用 `Our contributions are summarized in three folds:` + 编号列表。
- R004 Experiments 标题为 `EXPERIMENTS`；局限单独成节后再结论。
- R005 Conclusion 用 `In this paper, we present` 收回框架，未见 `Although` 局限句（局限已在 VI）。

## Candidate phrases

- `Thereupon, we propose a generic deep mixed time series temporal causal discovery framework.` (abstract)
- `Our key idea is to adaptively recover LCVs from DVs with the guidance of CVs` (abstract)
- `Our contributions are summarized in three folds:` (introduction)
- `In this section, we conduct extensive experiments to evaluate the performance of MiTCD` (experiments)
- `In this paper, we present a generic MiTCD framework for MiTS causal discovery.` (conclusion)
- `With great generality, MiTCD demonstrates strong performance across multiple benchmark datasets` (conclusion)

## House style

自称是 `This study addresses` / `we propose` / `we present` / `In this paper` / `our framework`。未见 `Here we`。`In this paper` 与 `This study` 进 phrase_bank，不进 anti_ai_patterns。结论用现在时 `we present`。

## Quotes

- p.5723 abstract: While existing causal discovery methods mostly focus on continuous time series, causal discovery for mixed time series encompassing both continuous variables (CVs) and discrete variables (DVs) is a fundamental yet underexplored problem.
- p.5723 abstract: Thereupon, we propose a generic deep mixed time series temporal causal discovery framework.
- p.5723 abstract: Our key idea is to adaptively recover LCVs from DVs with the guidance of CVs and perform causal discovery in a unified continuous-valued space.
- p.5723 abstract: Experimentally, extensive empirical evaluations and in-depth investigations validate the superior performance of our framework.
- p.5723 introduction: GOING beyond classification and prediction, recognizing causal structures from time series has become an increasingly critical research topic in recent decades [1], [2], [3].
- p.5723 introduction: Despite the remarkable progress, most causal discovery methods are developed with an inherent assumption that the time series data are solely composed of continuous-valued variables.
- p.5723 introduction: In this paper, we ascribe the above key challenges as Information Asymmetry (InfoA) problem.
- p.5723 introduction: However, these methods may lose vital information or sacrifice fine-grained continuous signals, thereby inevitably yielding non-negligible estimation errors.
- p.5724 introduction: Enlightened by the aforementioned analysis, we present MiTCD, a deep Mixed Time Series Causal Discovery framework.
- p.5724 introduction: Our contributions are summarized in three folds:
- p.5725 related work: However, most of the above methods are tailored for continuous time series and are therefore inappropriate for MiTS.
- p.5725 method: In this section, we first present the problem formulation of MiTS causal discovery. Then, the motivation of this study is analyzed with relevant discussions.
- p.5731 experiments: In this section, we conduct extensive experiments to evaluate the performance of MiTCD with 18 well-acknowledged and advanced temporal causal discovery methods.
- p.5739 conclusion: In this paper, we present a generic MiTCD framework for MiTS causal discovery.
- p.5739 conclusion: MiTCD mitigates the research obstacle of Information Asymmetry by recovering the latent continuity from DVs under the guidance of observed CVs.
- p.5739 conclusion: With great generality, MiTCD demonstrates strong performance across multiple benchmark datasets with different settings.
