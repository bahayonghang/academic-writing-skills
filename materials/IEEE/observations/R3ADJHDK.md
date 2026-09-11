---
key: R3ADJHDK
title: "A Multirate Modeling Method for Industrial Quality Index Prediction With Time Delays"
venue: "IEEE Transactions on Automation Science and Engineering"
doi: "10.1109/TASE.2025.3639628"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM STATEMENT` → `III. PROPOSED METHOD` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—`、`Note to Practitioners—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCC/MI、图约束增量网络、HSAN/MsFEFNet/VPTN/LSTMR-DADLnet）。Introduction 末有节序路标，指向 Section II–V。Method 在 III（TDE module / MSM-MRM module）。Experiments 标题为 `IV. CASE STUDIES`（矿物研磨真实数据）。

## Openers

- abstract: `The modeling of` — "The modeling of process data is essential for the prediction of product quality in industrial processes." (p.523)
- introduction: `UNDER the requirement` — "UNDER the requirement for carbon peaking and carbon neutrality, the process industries are urgently pursuing intelligent transformation [1], [2]." (p.523；栏首掉字)
- method: `The overall structure` — "The overall structure of MRM-TD is described in Fig. 2." (p.525, III)
- experiments: `To validate the` — "To validate the effectiveness of MRM-TD, rigorous simulations are conducted using real-world mineral grinding data." (p.530, IV)
- conclusion: `This paper proposed` — "This paper proposed a novel MRM-TD with two modules: TDE and MRM." (p.535)

## Gap transitions

- however (abstract): "However, the multirate process data lead to a mismatch between the input and output of soft sensing models." (p.523)
- to address (abstract): "To address these problems, this paper proposes a multirate modeling method for industrial quality index prediction with time delays (MRM-TD) which integrates two key modules: time delay estimation (TDE) and multirate modeling (MRM)." (p.523)
- despite (introduction): "Despite high computational efficiency, these univariate analysis methods tend to overlook the coupling effects among variables, leading to reduced the estimation accuracy." (p.524)
- despite (introduction): "Despite the notable accomplishments of the previously mentioned methods, research methods that synchronously consider the time delays and multiple sampling rates are still relatively scarce." (p.524)
- motivated by (introduction): "Motivated by these industrial practical problems, this paper proposes a multirate modeling method for industrial quality index prediction with time delays (MRM-TD)" (p.524)
- however (conclusion): "However, industrial environments often introduce noise interference—due to measurement errors, operational variations, and process switches—that degrades the accuracy of soft sensing models." (p.536)

## Hedge verbs

- propose / causal / abstract, introduction: "this paper proposes a multirate modeling method"; "an incremental network with cross sampling rate constraint (CSRN) is proposed"
- indicate / causal / abstract, experiments: "the simulation results of real mineral grinding process dataset indicate that the proposed method performs favorably"; "Table IV indicates that removing our cross sampling rate constraint"
- show / causal / experiments: "the performance of CSRN with and without TDE is shown in Fig. 6"; "Fig. 7 shows the test RMSE fold plot"
- demonstrate / causal / experiments, conclusion: "demonstrating its superior accuracy and robustness"; "underscoring its practical applicability"
- may / speculative / experiments: "these weights may occasionally fall into a configuration that yields exceptional results"

## Cross-section linkers

- introduction → problem / method / experiments / conclusion: "The rest of this paper is organized as follows. The problem statement is presented in Section II. Then, Section III introduces the MRM-TD in detail. Section IV reports the case studies results. Section V concludes this paper." (p.525)
- problem → method: Remark 1 后直接 `III. PROPOSED METHOD` (p.525)
- method → experiments: Algorithm 1 后直接 `IV. CASE STUDIES` (p.530)
- experiments → conclusion: Random SR Testing / Remark 5 后直接 `V. CONCLUSION` (p.535)

## Candidate rules

- R001 TASE 在 Abstract 后接 `Note to Practitioners—`，用工厂语言复述 TDE/MRM 模块。
- R002 Introduction 无独立 Related Work；多采样率与时延两条挑战用编号 `1) Multiple Sampling Rates` / `2) Time Delays` 展开。
- R003 贡献用 `The main contributions of this paper are summarized as follows.` + 编号列表。
- R004 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–V。
- R005 Conclusion 先收回两模块，再用 `However` 承认噪声未建模，`future work will concentrate on` 指向后续。

## Candidate phrases

- `To address these problems, this paper proposes` (abstract)
- `The main contributions of this paper are summarized as follows.` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `To validate the effectiveness of` (experiments)
- `This paper proposed a novel` (conclusion)
- `Accordingly, future work will concentrate on` (conclusion)

## House style

自称是 `this paper proposes` / `this paper` / `our method` / `the proposed method`。未见 `Here we`。`this paper proposes` 与 `In this paper` 进 phrase_bank，不进 anti_ai_patterns。结论段有 `In this paper, MRM-TD is proposed`。

## Quotes

- p.523 abstract: The modeling of process data is essential for the prediction of product quality in industrial processes.
- p.523 abstract: However, the multirate process data lead to a mismatch between the input and output of soft sensing models.
- p.523 abstract: To address these problems, this paper proposes a multirate modeling method for industrial quality index prediction with time delays (MRM-TD) which integrates two key modules: time delay estimation (TDE) and multirate modeling (MRM).
- p.523 abstract: Finally, the simulation results of real mineral grinding process dataset indicate that the proposed method performs favorably.
- p.523 introduction: UNDER the requirement for carbon peaking and carbon neutrality, the process industries are urgently pursuing intelligent transformation [1], [2].
- p.524 introduction: Despite high computational efficiency, these univariate analysis methods tend to overlook the coupling effects among variables, leading to reduced the estimation accuracy.
- p.524 introduction: Despite the notable accomplishments of the previously mentioned methods, research methods that synchronously consider the time delays and multiple sampling rates are still relatively scarce.
- p.525 introduction: The main contributions of this paper are summarized as follows.
- p.525 introduction: The rest of this paper is organized as follows. The problem statement is presented in Section II. Then, Section III introduces the MRM-TD in detail. Section IV reports the case studies results. Section V concludes this paper.
- p.525 method: The overall structure of MRM-TD is described in Fig. 2.
- p.530 experiments: To validate the effectiveness of MRM-TD, rigorous simulations are conducted using real-world mineral grinding data.
- p.535 experiments: The proposed CSRN achieves optimal performance with the lowest average RMSE and MAE, along with the best fitting performance, demonstrating its superior accuracy and robustness.
- p.535 conclusion: This paper proposed a novel MRM-TD with two modules: TDE and MRM.
- p.536 conclusion: Notably, our method maintained its effectiveness even when faced with irregular sampling periods for quality indices, underscoring its practical applicability in industrial settings.
- p.536 conclusion: However, industrial environments often introduce noise interference—due to measurement errors, operational variations, and process switches—that degrades the accuracy of soft sensing models.
- p.536 conclusion: Accordingly, future work will concentrate on enhancing the method’s robustness against complex noise patterns.
