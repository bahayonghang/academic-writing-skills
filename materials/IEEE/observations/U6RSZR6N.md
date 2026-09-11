---
key: U6RSZR6N
title: "Large-Scale and Knowledge-Based Dynamic Multiobjective Optimization for MSWI Process Using Adaptive Competitive Swarm Optimization"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2023.3308922"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. MIMO MODELING OF THE MSWI PROCESS` → `III. ADAPTIVE LARGE-SCALE MULTIOBJECTIVE OPTIMIZATION FOR THE MIMO-MSWI MODELING` → `IV.`（NOx/CE 动态多目标优化）→ `V.`（实验）→ `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 LSTM、MISO/MIMO、PSO/GA、CSO）。Introduction 末有节序路标，指向 Section II–VI。

## Openers

- abstract: `Municipal solid waste` — "Municipal solid waste incineration (MSWI) process is a complex industrial process with strong nonlinearity." (p.379)
- introduction: `MUNICIPAL solid waste` — "MUNICIPAL solid waste (MSW) has been one of the noticeable and severe environment and public health issues [1], [2]." (p.379；栏首掉字)
- method: `Since the MSWI process` — "Since the MSWI process involve complex physical changes and chemical reactions, the modeling based on mechanism analysis is difficult to realize." (p.381, II)
- experiments: `The proposed ALMOCSO algorithm` — "The proposed ALMOCSO algorithm and the comparison algorithms are independently run 30 times on the same experimental platform, and the statistical data are analyzed to be the final results." (p.387, V.C)
- conclusion: `In order to reduce` — "In order to reduce the NOx emissions and improve the CE in the MSWI process, the multiobjective optimization on the MSWI process is studied in this article." (p.389)

## Gap transitions

- nevertheless (introduction): "Nevertheless, due to the unstable heating value and component of MSW, it is easy to result in excessive pollutant emissions and low-combustion efficiency (CE) in the MSWI process [5]." (p.379)
- therefore (introduction): "Therefore, the primary optimization objectives of the MSWI process are to improve the CE and reduce the NOx emissions." (p.379)
- however (introduction): "However, there are some obvious shortcomings in this study." (p.380)
- however (introduction): "However, the major studies based on swarm intelligence algorithms remains on SOPs in industrial process." (p.380)
- therefore (introduction): "Therefore, it is a promising scheme that uses it to solve both LSMOPs and DMOPs." (p.380)
- therefore (experiments): "Therefore, the proposed methodology has a promising prospect in the application of the MSWI process and other industrial process." (p.389)

## Hedge verbs

- propose / causal / abstract, introduction: "A comprehensive evaluation system is proposed"; "an adaptive large-scale multiobjective CSO (ALMOCSO) algorithm is proposed"
- indicate / causal / abstract: "The results indicate that the modeling accuracy is satisfactory"
- demonstrate / causal / introduction: "The results demonstrate that both CE and NOx emission are improved."
- show / causal / conclusion: "The results show that the optimization effects of both modeling and concerned combustion outcomes are satisfactory"

## Cross-section linkers

- introduction → method: "The remainder of this article is organized as follows. Section II elaborates the MIMO model of the MSWI process. The large-scale multiobjective optimization for the MIMO-MSWI model is introduced detailedly in Section III. The multiobjective optimization of the NOx emissions and the CE in the MSWI process are outlined in Section IV. The experimental studies are conducted in Section V, and the conclusions are drawn in Section VI." (p.380)
- method → experiments: Section III–IV 方法后接实验比较段 "C. Results Comparison" (p.387)
- experiments → conclusion: "Based on the above experimental results and analysis, it can be concluded that the proposed ALMOCSO algorithm has certain advantages..." 随后 `VI. CONCLUSION` (p.389)

## Candidate rules

- R001 贡献用 `The contributions of this article are summarized as follows.` + 编号列表。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–VI。
- R004 Conclusion 用编号列表收回建模、算法、历史 POS 与量化结果。
- R005 未来工作用 `It is our pursuit and future efforts to`。

## Candidate phrases

- `To solve this problem, the multiobjective optimization studies are conducted` (abstract)
- `The contributions of this article are summarized as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this article, the multiobjective optimization of the MSWI process is studied` (introduction)
- `the multiobjective optimization on the MSWI process is studied in this article` (conclusion)

## House style

自称是 `this article` / `the proposed methodology` / `the proposed ALMOCSO algorithm`。未见 `Here we`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.379 abstract: Municipal solid waste incineration (MSWI) process is a complex industrial process with strong nonlinearity.
- p.379 abstract: It is a challenge to build a model for the MSWI process and carry out the corresponding optimization works.
- p.379 abstract: To solve this problem, the multiobjective optimization studies are conducted for both modeling and concerned indexes of the MSWI process, including the nitrogen oxides (NOx) emissions and the combustion efficiency (CE).
- p.379 abstract: Finally, the feasibility and effectiveness of the proposed methodology for optimizing the MSWI process are confirmed by the experiments using the data collected from a real MSWI plant.
- p.379 abstract: The results indicate that the modeling accuracy is satisfactory, and the CE is improved over 10% and the reduction of the NOx emissions is achieved 15.58%.
- p.379 introduction: MUNICIPAL solid waste (MSW) has been one of the noticeable and severe environment and public health issues [1], [2].
- p.379 introduction: Nevertheless, due to the unstable heating value and component of MSW, it is easy to result in excessive pollutant emissions and low-combustion efficiency (CE) in the MSWI process [5].
- p.379 introduction: Therefore, the primary optimization objectives of the MSWI process are to improve the CE and reduce the NOx emissions.
- p.380 introduction: However, there are some obvious shortcomings in this study.
- p.380 introduction: In this article, the multiobjective optimization of the MSWI process is studied, and three aspects of research are carried out, including the MIMO data-driven modeling of the MSWI process, large-scale multiobjective optimization of the MIMO-MSWI model, and dynamic multiobjective optimization of the NOx emissions, and the CE in the MSWI process.
- p.380 introduction: The contributions of this article are summarized as follows.
- p.380 introduction: The remainder of this article is organized as follows.
- p.381 method: Since the MSWI process involve complex physical changes and chemical reactions, the modeling based on mechanism analysis is difficult to realize.
- p.387 experiments: The proposed ALMOCSO algorithm and the comparison algorithms are independently run 30 times on the same experimental platform, and the statistical data are analyzed to be the final results.
- p.389 experiments: Therefore, the proposed methodology has a promising prospect in the application of the MSWI process and other industrial process.
- p.389 conclusion: In order to reduce the NOx emissions and improve the CE in the MSWI process, the multiobjective optimization on the MSWI process is studied in this article.
- p.389 conclusion: The results show that the optimization effects of both modeling and concerned combustion outcomes are satisfactory, where the NOx emissions are reduced by 15.58% and the CE is increased by 10.20%.
- p.389 conclusion: It is our pursuit and future efforts to establish a more accurate and generalized MIMO-MSWI model.
