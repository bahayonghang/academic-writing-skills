---
key: 8HHXWLS2
title: "Exploring Progress in Multivariate Time Series Forecasting: Comprehensive Benchmarking and Heterogeneity Analysis"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2024.3484454"
item_type: preprint
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PRELIMINARIES` → `IV. BENCHMARK CONSTRUCTION` → `V. HETEROGENEITY ACROSS MTS DATASETS` → `VI. EXPERIMENTS` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 `II. RELATED WORK`（LTSF / STF / MTS benchmarking 三小节）。`related_work=independent`。Introduction 末有贡献列表与节序路标，指向 Section II–VII。Method 标题为 `BENCHMARK CONSTRUCTION`（BasicTS+ 统一训练管线与评估设置）。Experiments 标题为 `EXPERIMENTS`（14 数据集、45+ 模型）。附录 `APPENDIX` 列数据集与基线。

## Openers

- abstract: `Multivariate Time Series` — "Multivariate Time Series (MTS) analysis is crucial to understanding and managing complex systems, such as traffic and energy systems, and a variety of approaches to MTS forecasting have been proposed recently." (p.1)
- introduction: `SENSORS are increasingly` — "SENSORS are increasingly being deployed in complex, real-world systems." (p.1；栏首掉字)
- related_work: `We cover studies` — "We cover studies related to LTSF and STF, which are the two most prominent topics in recent MTS forecasting studies." (p.2)
- method: `We present BasicTS+` — "We present BasicTS+, a benchmark designed for fair, comprehensive, and reproducible evaluation of MTS forecasting solutions, including both STF and LTSF solutions." (p.4, IV)
- experiments: `In this section` — "In this section, we conduct extensive experiments to assess our hypotheses and address controversies in technical approaches." (p.8, VI)
- conclusion: `In this study` — "In this study, we address the seemingly inconsistent experimental findings and difficulties in selecting technical directions in the area of Multivariate Time Series (MTS) forecasting, shedding light on the actual advance achieved." (p.12)

## Gap transitions

- however (abstract): "However, we often observe inconsistent or seemingly contradictory performance findings across different studies." (p.1)
- however (introduction): "However, subsequent studies [16], [28], [27] find that advanced neural networks outperform LTSF-Linear." (p.2)
- however (related_work): "However, a recent study proposes LTSF-Linear [26] and questions the effectiveness of Transformer architectures." (p.3)
- however (related_work): "However, these benchmarks have several limitations." (p.3)
- notably (related_work): "Notably, the motivation and contribution of this study significantly differ from [60]." (p.3)
- to mitigate (introduction): "To mitigate issues such as those exemplified above and to offer insight into the advance achieved, we contribute a comprehensive analysis and comparison of both MTS forecasting datasets and models." (p.2)
- however (method): "However, MAE and MSE represent absolute errors that can be influenced significantly by the range of the data, rendering them less intuitive for interpretation." (p.5)
- conversely (experiments): "Conversely, on datasets with low spatial indistinguishability, adding these spatial modeling components degrades performance, suggesting that modeling spatial dependencies (or named cross-dimension dependencies) on these datasets is not necessary." (p.9)
- therefore (experiments): "Therefore, we emphasize that future research should prioritize more realistic scenarios, such as modeling distribution shifts, predicting with low-quality data, and zero- or few-shot learning." (p.12)

## Hedge verbs

- propose / causal / abstract, introduction: "we first propose BasicTS+, a benchmark designed to enable fair, comprehensive, and reproducible comparison"; "we introduce BasicTS+, a benchmark"
- identify / causal / abstract: "we identify the heterogeneity across different MTS as an important consideration"
- present / causal / method, conclusion: "We present BasicTS+, a benchmark designed for fair, comprehensive, and reproducible evaluation"; "we introduce a novel benchmark called BasicTS+"
- show / causal / experiments: "The results are shown in Table IV."; "The results for LTSF are shown in Table VI."
- find / associative / experiments: "We find a strong relationship between model architecture and data characteristics."; "we find that compared to improving prediction accuracy by designing increasingly complex models"
- believe / speculative / experiments: "we believe that more complex LTSF or STF solutions are only effective if they can significantly outperform these two."
- emphasize / causal / experiments, conclusion: "we emphasize that future research should prioritize more realistic scenarios"; "We emphasize that many conclusions drawn in prior research hold only for certain types of data"

## Cross-section linkers

- introduction → related work: "The paper is organized as follows. Section II provides discussions of related work on LTSF, STF, and MTS forecasting benchmarking. Section III covers preliminaries and essential definitions. Section IV presents the BasicTS+ benchmark. Section V then delves into the heterogeneity among MTS datasets, and provides hypotheses for explaining seemingly contradictory findings. Section VI reports on the application of BasicTS+ to popular models and provides new insights. Section VII concludes the paper." (p.2)
- related work → preliminaries: BasicTS vs BasicTS+ 对比段落后直接 `III. PRELIMINARIES` (p.3–4)
- method → heterogeneity: 评估指标定义后直接 `V. HETEROGENEITY ACROSS MTS DATASETS`；开节 "Next, we put focus on the heterogeneity across MTS datasets" (p.5)
- heterogeneity → experiments: Hypothesis 2 后 "We study this hypothesis in Section VI-C." 再接 `VI. EXPERIMENTS` (p.7–8)
- experiments → conclusion: 未来方向段落后直接 `VII. CONCLUSION` (p.12)

## Candidate rules

- R003 Introduction 末用 `The paper is organized as follows` 指向 II–VII。
- R002 独立 `II. RELATED WORK`，再分子节评 LTSF / STF / benchmarking。
- R004 贡献用 `In summary, we make the following main contributions:` + 项目符号。
- R001 摘要用 `we first propose` / `Second, we identify` / `Third, we apply` 三段贡献。
- R005 Conclusion 用 `In this study, we address` 收回问题，再按 First / Second / Additionally 收束贡献，不另开 future-work 节（未来方向写在 VI.D.4）。

## Candidate phrases

- `However, we often observe inconsistent or seemingly contradictory performance findings` (abstract)
- `we first propose BasicTS+, a benchmark designed to enable fair, comprehensive, and reproducible comparison` (abstract)
- `To mitigate issues such as those exemplified above` (introduction)
- `In summary, we make the following main contributions:` (introduction)
- `The paper is organized as follows.` (introduction)
- `We present BasicTS+, a benchmark designed for fair, comprehensive, and reproducible evaluation` (method)
- `In this study, we address the seemingly inconsistent experimental findings` (conclusion)

## House style

自称 `we first propose` / `we introduce` / `we present` / `In this study, we address` / `This study`。未见 `Here we`。`we propose` 与 `In this study` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。未见 `This article`。

## Quotes

- p.1 abstract: Multivariate Time Series (MTS) analysis is crucial to understanding and managing complex systems, such as traffic and energy systems, and a variety of approaches to MTS forecasting have been proposed recently.
- p.1 abstract: However, we often observe inconsistent or seemingly contradictory performance findings across different studies.
- p.1 abstract: Specifically, we first propose BasicTS+, a benchmark designed to enable fair, comprehensive, and reproducible comparison of MTS forecasting solutions.
- p.1 abstract: Second, we identify the heterogeneity across different MTS as an important consideration and enable classification of MTS based on their temporal and spatial characteristics.
- p.1 abstract: Third, we apply BasicTS+ along with rich datasets to assess the capabilities of more than 45 MTS forecasting solutions.
- p.1 introduction: SENSORS are increasingly being deployed in complex, real-world systems.
- p.2 introduction: However, subsequent studies [16], [28], [27] find that advanced neural networks outperform LTSF-Linear.
- p.2 introduction: To mitigate issues such as those exemplified above and to offer insight into the advance achieved, we contribute a comprehensive analysis and comparison of both MTS forecasting datasets and models.
- p.2 introduction: In summary, we make the following main contributions:
- p.2 introduction: The paper is organized as follows. Section II provides discussions of related work on LTSF, STF, and MTS forecasting benchmarking. Section III covers preliminaries and essential definitions. Section IV presents the BasicTS+ benchmark. Section V then delves into the heterogeneity among MTS datasets, and provides hypotheses for explaining seemingly contradictory findings. Section VI reports on the application of BasicTS+ to popular models and provides new insights. Section VII concludes the paper.
- p.2 related_work: We cover studies related to LTSF and STF, which are the two most prominent topics in recent MTS forecasting studies.
- p.3 related_work: However, a recent study proposes LTSF-Linear [26] and questions the effectiveness of Transformer architectures.
- p.3 related_work: However, these benchmarks have several limitations.
- p.3 related_work: Notably, the motivation and contribution of this study significantly differ from [60].
- p.4 preliminaries: We define key concepts and the forecasting task.
- p.4 method: We present BasicTS+, a benchmark designed for fair, comprehensive, and reproducible evaluation of MTS forecasting solutions, including both STF and LTSF solutions.
- p.5 method: However, MAE and MSE represent absolute errors that can be influenced significantly by the range of the data, rendering them less intuitive for interpretation.
- p.5 heterogeneity: Next, we put focus on the heterogeneity across MTS datasets and delve into its role in explaining the seemingly contradictory experimental findings that suggest that each of two different technical approaches is the best approach to achieve improved forecasting accuracy.
- p.8 experiments: In this section, we conduct extensive experiments to assess our hypotheses and address controversies in technical approaches.
- p.9 experiments: Conversely, on datasets with low spatial indistinguishability, adding these spatial modeling components degrades performance, suggesting that modeling spatial dependencies (or named cross-dimension dependencies) on these datasets is not necessary.
- p.12 experiments: Therefore, we emphasize that future research should prioritize more realistic scenarios, such as modeling distribution shifts, predicting with low-quality data, and zero- or few-shot learning.
- p.12 conclusion: In this study, we address the seemingly inconsistent experimental findings and difficulties in selecting technical directions in the area of Multivariate Time Series (MTS) forecasting, shedding light on the actual advance achieved.
- p.12 conclusion: First, we introduce a novel benchmark called BasicTS+ that is designed to enable fair and reasonable comparisons of MTS forecasting solutions.
- p.12 conclusion: We emphasize that many conclusions drawn in prior research hold only for certain types of data, and considering these conclusions to be more general can lead researchers to make counterproductive inferences.
