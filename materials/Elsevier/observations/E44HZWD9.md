---
key: E44HZWD9
title: "Regression generative adversarial network based on bounded losses for prediction of free calcium oxide in cement clinker"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2023.102344"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,8-10,12-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

前置 `Full length article` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction` → `2. Related work` → `3. Cement clinker calcination process and variables analysis` → `4. Proposed method` → `5. Experiment results` → `6. Conclusion`。独立 Related Work（`2. Related work`）。`related_work=independent`。Introduction 末有三条贡献 + 节序路标。Method 前有过程描述节。Experiments 标题为 `Experiment results`。

## Openers

- abstract: `The data imbalance` — "The data imbalance problem caused by multi-time scales phenomenon affects the prediction accuracy, validity and robustness of free calcium oxide (fCaO) content in cement clinker calcination process."
- introduction: `Free calcium oxide` — "Free calcium oxide (fCaO) content is a pivotal quality indicator of cement, it reflects the mass fraction of CaO that not combined with other components during cement clinker calcination process, and it can be simply expressed as yfCaO = (WCaO/Wcement clinker) × 100%."
- related_work: `Data imbalance is` — "Data imbalance is a kind of widespread problem and hinders the further investigation in data-based modeling for prediction [18] or detection [19], which can be solved by fusing generated data and actual data [20]."
- method: `Aiming at fCaO` — "Aiming at fCaO content prediction under multi-time scales imbalance problem, we propose the RGAN which copes with the regression problem under data imbalance problem by multi-time scales data augmentation."
- experiments: `In this paper` — "In this paper, there are 2245 h cement clinker calcination data are used as experiment dataset, i.e. totally more than 3 months production data, which are acquired from cement quality management database of a cement production factory in China."
- conclusion: `In this paper` — "In this paper, we propose a method of fCaO content prediction based on RGAN facing multi-time scales data imbalance problem."

## Gap transitions

- however (introduction): "However, the above investigations pay more attentions to extracting nonlinearity and time variability features from cement manufacturing data to improve prediction performance, whereas the influence of multi-time scales data imbalance is ignored."
- therefore (introduction): "therefore, focusing on the multi-time scales imbalance problem in cement production, inspired by data augmentation [16] and generative adversarial network (GAN)[17], we propose a fCaO content prediction method based on regression generative adversarial network (RGAN)."
- focusing on (abstract): "Focusing on this problem, we propose an regression generative adversarial network model to predict fCaO content, which contains a generator, discriminator and predictor."
- although (related work): "Although these investigations are focus on the data imbalance problem which lack complex inner function relationships of multi variables, they provide the idea of solving data imbalance problem by learning actual data features to enlarge the scale and characteristic space of small samples."

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "we propose"
- demonstrate / causal / abstract: "Experiments implemented by cement production data demonstrate that the proposed model has advantages in accuracy, availability and robustness in fCaO content prediction"
- indicate / associative / experiments: "The above visualization results indicate that the generated data have consistent features with actual data"

## Cross-section linkers

- introduction → related work: "The outline of this paper is: investigations of data driven modeling facing data imbalance problem are analyzed in section 2; Section 3 describes cement calcination process and analyzes related process variables and multi-time scales data imbalance problem. Section 4 illustrates the structure and algorithm of the proposed RGAN; Section 5 shows experiment results; Section 6 is conclusion and the Appendix A is theoretical proof of the convergence and stability of BL-GAN."
- related work → method: 过程分析节后 `4. Proposed method`
- method → experiments: 预测器结构后 `5. Experiment results`
- experiments → conclusion: 横向对比后 `6. Conclusion`

## Candidate rules

- R001 独立 Related Work（`2. Related work`）。
- R003 节序路标：`The outline of this paper is`
- R004 贡献列表：`There are three contributions of this paper`
- R009 自称：`we propose` / `In this paper, we propose`

## Candidate phrases

- `Focusing on this problem, we propose` (abstract)
- `we propose a fCaO content prediction method based on regression generative adversarial network (RGAN)` (introduction)
- `There are three contributions of this paper` (introduction)
- `The outline of this paper is` (introduction)
- `In this paper, we propose a method of fCaO content prediction` (conclusion)

## House style

自称 `we propose` / `In this paper` / `the proposed model`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The data imbalance problem caused by multi-time scales phenomenon affects the prediction accuracy, validity and robustness of free calcium oxide (fCaO) content in cement clinker calcination process.
- abstract: Focusing on this problem, we propose an regression generative adversarial network model to predict fCaO content, which contains a generator, discriminator and predictor.
- abstract: Experiments implemented by cement production data demonstrate that the proposed model has advantages in accuracy, availability and robustness in fCaO content prediction, especially TCI is higher 22.69 percentage points than that of without data augmentation.
- introduction: Free calcium oxide (fCaO) content is a pivotal quality indicator of cement, it reflects the mass fraction of CaO that not combined with other components during cement clinker calcination process, and it can be simply expressed as yfCaO = (WCaO/Wcement clinker) × 100%.
- introduction: However, the above investigations pay more attentions to extracting nonlinearity and time variability features from cement manufacturing data to improve prediction performance, whereas the influence of multi-time scales data imbalance is ignored.
- introduction: There are three contributions of this paper:
- introduction: The outline of this paper is: investigations of data driven modeling facing data imbalance problem are analyzed in section 2; Section 3 describes cement calcination process and analyzes related process variables and multi-time scales data imbalance problem.
- related_work: Data imbalance is a kind of widespread problem and hinders the further investigation in data-based modeling for prediction [18] or detection [19], which can be solved by fusing generated data and actual data [20].
- method: Aiming at fCaO content prediction under multi-time scales imbalance problem, we propose the RGAN which copes with the regression problem under data imbalance problem by multi-time scales data augmentation.
- experiments: In this paper, there are 2245 h cement clinker calcination data are used as experiment dataset, i.e. totally more than 3 months production data, which are acquired from cement quality management database of a cement production factory in China.
- conclusion: In this paper, we propose a method of fCaO content prediction based on RGAN facing multi-time scales data imbalance problem.
- conclusion: Experiments implemented in cement quality management database of a cement production enterprise show that the proposed method effectively generates multi-time scales series data to eliminate data imbalance and improves fCaO content prediction accuracy, validity and robustness.
