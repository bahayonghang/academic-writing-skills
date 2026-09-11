---
key: UNJAU8VX
title: "Robust Modeling for Industrial Process Based on Frequency Reconstructed Fuzzy Neural Network"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2023.3291488"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM DESCRIPTION` → `III.`（FRFNN 结构/滤波器/软边界/学习）→ `IV.`（收敛分析）→ `V. EXPERIMENTAL STUDIES` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 WBLS、RLM-SVM、TCRFN、IT2FNN、FRSM 相关 FNN）。Introduction 末有节序路标，指向 Section II–VI。

## Openers

- abstract: `The model bias` — "The model bias caused by input outliers is a dramatic obstacle to the application of models in industrial processes." (p.102)
- introduction: `MOST of industrial` — "MOST of industrial processes exhibit strong nonlinearity, multivariable coupling, and multiple space-time scales due to complicated physicochemical reactions and material energy conversion, such as wastewater treatment processes [1], blast furnace processes [2], petrochemical processes [3], and so on [4], [5]." (p.102；栏首掉字)
- method: `In this section, the` — "In this section, the description of outliers in industrial processes is introduced to obtain the reason of the model bias caused by the input outliers." (p.103, II)
- experiments: `To validate the performance` — "To validate the performance for robust modeling, the proposed FRFNN is tested on two real-world industrial datasets with noises and outliers, including electrical energy output prediction of combined cycle power plant (CCPP) and permeability rate prediction of membrane bioreactor (MBR) treatment process." (p.109, V)
- conclusion: `In this article, a` — "In this article, a robust modeling method based on FRFNN is designed to deal with the model bias caused by the input outliers in industrial processes." (p.113)

## Gap transitions

- to cope with (abstract): "To cope with this problem, this article proposes a robust modeling method based on frequency reconstructed fuzzy neural network (FRFNN) for industrial process." (p.102)
- nevertheless (introduction): "Nevertheless, the membership functions in FNNs are often incompatible with the input outlier, which leads to poor outlier-robustness of FNN." (p.102)
- however (introduction): "However, the above input signals for FNNs are always attenuated while data denoising [28]." (p.103)
- except (introduction): "Except equipping with the denoising module, another option is to reinforce membership functions to accommodate input outliers [30]." (p.103)
- therefore (experiments): "Therefore, the proposed robust modeling method based on FRFNN processes the prominent robustness than other methods in the permeability rate prediction of MBR." (p.113)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a robust modeling method"; "a robust modeling method based on frequency reconstructed fuzzy neural network (FRFNN) is proposed"
- demonstrate / causal / abstract, experiments: "The experimental results demonstrate that the proposed robust modeling method can strengthen robustness"
- introduce / causal / abstract: "an adaptive gradient descent algorithm is introduced to update the model parameters"
- show / causal / experiments: "Fig. 4(e) and (f) shows the testing outputs"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. First, in Section II, the description of outliers is introduced as well as the idea of FNN is briefly given. Next, Section III discusses the details of FRFNN... Section IV analyses the convergence of the proposed FRFNN. Section V reports the experimental studies... Finally, Section VI concludes this article." (p.103)
- method → experiments: Section IV 收敛证明后接 `V. EXPERIMENTAL STUDIES` (p.109)
- experiments → conclusion: Discussion 段落后直接 `VI. CONCLUSION` (p.113)

## Candidate rules

- R001 贡献用 `The main contributions of this article are summarized as follows.` + 编号列表。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 Conclusion 先收回方法三件套（滤波器 / FRSM / AGD），再用 `In our future work` 指向后续。
- R005 实验开篇用 `To validate the performance` + 两个真实工业数据集。

## Candidate phrases

- `To cope with this problem, this article proposes` (abstract)
- `The main contributions of this article are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a robust modeling method based on FRFNN is proposed` (introduction)
- `In our future work` (conclusion)

## House style

自称是 `this article` / `the proposed robust modeling method` / `the proposed FRFNN`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.102 abstract: The model bias caused by input outliers is a dramatic obstacle to the application of models in industrial processes.
- p.102 abstract: To cope with this problem, this article proposes a robust modeling method based on frequency reconstructed fuzzy neural network (FRFNN) for industrial process.
- p.102 abstract: Finally, the proposed robust modeling method is tested on two real-world industrial datasets with input outliers.
- p.102 abstract: The experimental results demonstrate that the proposed robust modeling method can strengthen robustness and achieve superior performance over other previous methods.
- p.102 introduction: MOST of industrial processes exhibit strong nonlinearity, multivariable coupling, and multiple space-time scales due to complicated physicochemical reactions and material energy conversion, such as wastewater treatment processes [1], blast furnace processes [2], petrochemical processes [3], and so on [4], [5].
- p.102 introduction: As such, building a robust model with capable to outlier-tolerant is considered as a crucial challenge [10].
- p.102 introduction: Nevertheless, the membership functions in FNNs are often incompatible with the input outlier, which leads to poor outlier-robustness of FNN.
- p.103 introduction: However, the above input signals for FNNs are always attenuated while data denoising [28].
- p.103 introduction: In this article, a robust modeling method based on frequency reconstructed fuzzy neural network (FRFNN) is proposed to cope with the model bias caused by the input outliers.
- p.103 introduction: The main contributions of this article are summarized as follows.
- p.103 introduction: The rest of this article is organized as follows.
- p.103 method: In this section, the description of outliers in industrial processes is introduced to obtain the reason of the model bias caused by the input outliers.
- p.109 experiments: To validate the performance for robust modeling, the proposed FRFNN is tested on two real-world industrial datasets with noises and outliers, including electrical energy output prediction of combined cycle power plant (CCPP) and permeability rate prediction of membrane bioreactor (MBR) treatment process.
- p.113 conclusion: In this article, a robust modeling method based on FRFNN is designed to deal with the model bias caused by the input outliers in industrial processes.
- p.113 conclusion: Finally, the results of experiments containing the electrical energy output prediction of CCPP and the permeability rate prediction of MBR demonstrate that the proposed robust modeling method based on FRFNN acquires superior robustness than other comparison approaches.
- p.113 conclusion: In our future work, due to the superiority of frequency distribution natures for feature representation, some other advanced Fourier representation modes will be studied including but not limited to the Fourier space.
