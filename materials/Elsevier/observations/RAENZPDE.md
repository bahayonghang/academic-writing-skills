---
key: RAENZPDE
title: "A dynamic feature block ensemble soft sensor for cement clinker production using spatiotemporal similarity spectral clustering"
venue: "Control Engineering Practice"
doi: "10.1016/j.conengprac.2025.106740"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction`（`1.1` 背景、`1.2 Related work`、`1.3` 动机与贡献）→ `2. Cement clinker production process` → `3. Methodology` → `4. Results and discussions` → `5. Conclusion`。前置 `a b s t r a c t` 与 `a r t i c l e i n f o` / `Keywords`。无独立 Related Work 节。`related_work=inlined`（Introduction `1.2 Related work`：JITL、集成学习、深度学习）。Introduction `1.3` 条目贡献（三点 bullet）+ 节序路标。Method 含预处理、JS-TS 谱聚类、动态特征分块与加权集成。Experiments 标题为 `4. Results and discussions`（4105 条工业记录，11 个基线）。

## Openers

- abstract: `Accurate prediction of` — "Accurate prediction of free calcium oxide (F-CaO) content is essential for cement clinker quality control."
- introduction: `Cement plays a` — "Cement plays a crucial role in modern infrastructure, from residential buildings to major transportation projects (Shen et al., 2017)."
- method: `The proposed STSSC-DFBE` — "The proposed STSSC-DFBE framework is an integrated solution designed to synergistically address challenges in both the sample and feature spaces for soft sensing in non-stationary processes."
- experiments: `The quality of` — "The quality of clinker largely depends on the distribution of F-CaO within it."
- conclusion: `This study introduces` — "This study introduces the STSSC-DFBE framework, a novel approach designed to overcome the fundamental challenges of high-dimensional, strongly coupled, and dynamic data inherent in the cement clinker production process."

## Gap transitions

- consequently (introduction): "Consequently, process conditions may have substantially changed before analytical feedback becomes available, leading to delayed detection of quality deviations."
- however (related work): "However, they remain fundamentally linear models that construct PLS regressions within local regions, limiting their ability to capture the complex nonlinear dynamics and deeply coupled interactions inherent in cement clinker calcination processes."
- to address (introduction): "To address the limitations of conventional laboratory analysis, various data-driven soft sensing methods (Sun & Ge, 2021) have been developed for cement quality prediction."
- to address (introduction): "To address the challenges outlined above, this paper proposes a STSSC-DFBE framework."

## Hedge verbs

- presents / causal / abstract: "This study presents a Spatiotemporal Similarity Spectral Clustering Dynamic Feature Block Ensemble (STSSC-DFBE) soft sensor for F-CaO concentration estimation."
- proposes / causal / introduction: "To address the challenges outlined above, this paper proposes a STSSC-DFBE framework."
- shows / associative / abstract: "Experimental validation using real industrial data from cement manufacturing facilities shows that STSSC-DFBE achieves R² of 0.7953, with Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) reduced to 0.2045 and 0.1202, respectively."
- demonstrates / associative / conclusion: "Validated on industrial data, the STSSC-DFBE framework demonstrates superior performance in predicting F-CaO content"

## Cross-section linkers

- introduction → process: "The remaining sections of this paper are organized as follows: Section 2 provides a detailed introduction to the steps and processes involved in cement manufacturing"
- process → method: "the proposed soft sensing model is presented in Section 3"
- method → experiments: "experimental results of STSSC-DFBE and baseline methods are analyzed in Section 4"
- experiments → conclusion: 参数敏感性后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction（`1.2 Related work` 为小节，非独立节）。
- R003 节序路标：`The remaining sections of this paper are organized as follows`
- R004 条目贡献：`The main contributions and innovations of this work are summarized as follows:`
- R009 自称：`This study presents` / `this paper proposes` / `This study introduces`

## Candidate phrases

- `This study presents a Spatiotemporal Similarity Spectral Clustering Dynamic Feature Block Ensemble (STSSC-DFBE) soft sensor` (abstract)
- `The remaining sections of this paper are organized as follows` (introduction)
- `The main contributions and innovations of this work are summarized as follows:` (introduction)
- `this paper proposes a STSSC-DFBE framework` (introduction)
- `This study introduces the STSSC-DFBE framework` (conclusion)

## House style

自称 `This study presents` / `this paper proposes` / `This study introduces`。`this study` 与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Accurate prediction of free calcium oxide (F-CaO) content is essential for cement clinker quality control.
- abstract: This study presents a Spatiotemporal Similarity Spectral Clustering Dynamic Feature Block Ensemble (STSSC-DFBE) soft sensor for F-CaO concentration estimation.
- abstract: Experimental validation using real industrial data from cement manufacturing facilities shows that STSSC-DFBE achieves R² of 0.7953, with Root Mean Square Error (RMSE) and Mean Absolute Error (MAE) reduced to 0.2045 and 0.1202, respectively.
- introduction: Cement plays a crucial role in modern infrastructure, from residential buildings to major transportation projects (Shen et al., 2017).
- introduction: Consequently, process conditions may have substantially changed before analytical feedback becomes available, leading to delayed detection of quality deviations.
- introduction: To address the challenges outlined above, this paper proposes a STSSC-DFBE framework.
- introduction: The main contributions and innovations of this work are summarized as follows:
- introduction: The remaining sections of this paper are organized as follows: Section 2 provides a detailed introduction to the steps and processes involved in cement manufacturing, the proposed soft sensing model is presented in Section 3, experimental results of STSSC-DFBE and baseline methods are analyzed in Section 4, and this work is summarized in Section 5.
- method: The proposed STSSC-DFBE framework is an integrated solution designed to synergistically address challenges in both the sample and feature spaces for soft sensing in non-stationary processes.
- experiments: The quality of clinker largely depends on the distribution of F-CaO within it.
- conclusion: This study introduces the STSSC-DFBE framework, a novel approach designed to overcome the fundamental challenges of high-dimensional, strongly coupled, and dynamic data inherent in the cement clinker production process.
- conclusion: Validated on industrial data, the STSSC-DFBE framework demonstrates superior performance in predicting F-CaO content, achieving an R² of 0.7953, an RMSE of 0.2045, and an MAE of 0.1202, consistently outperforming existing methods.
