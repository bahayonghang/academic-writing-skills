---
key: Z3TUHT9Z
title: "A Data-Driven Soft Sensor Modeling Method Based on Deep Learning and its Application"
venue: "IEEE Transactions on Industrial Electronics"
doi: "10.1109/TIE.2016.2622668"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. STACKED DENOISING AUTOENCODERS (SDAES)` → `III. SOFT SENSOR MODELING BASED ON DAE-NN` → `IV. CASE STUDY: ESTIMATE OXYGEN-CONTENT IN FLUE GASSES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 FPM / data-driven / ANN / SVR / Gaussian regression，并对比 shallow learning）。Introduction 末有节序路标，指向 Section II–V。Method 为 II–III。Experiments 为 IV（1000-MW 机组烟气含氧量）。

## Openers

- abstract: `Soft sensors have` — "Soft sensors have been widely used in industrial processes." (p.1)
- introduction: `IN MODERN industrial` — "IN MODERN industrial processes, some important process variables that are key indicators of process performance are difficult or impossible to measure online as a result of economic or technical limitations." (p.1；栏首掉字)
- method: `Soft sensors based` — "Soft sensors based on DAE-NN aim to exploit the essential information behind the process data and address the unlabeled data in soft sensor modeling." (p.3, III.A)
- experiments: `Ultrasuperficial units are` — "Ultrasuperficial units are one of the main trends of coal-fired thermal power that can achieve clean coal combustion and greatly improve energy efficiency." (p.4, IV)
- conclusion: `This paper has` — "This paper has introduced deep learning into soft sensor modeling and proposes a soft sensor modeling method based on DAE-NN." (p.8)

## Gap transitions

- however (introduction): "However, the FPM is often not available because of the complexity of the industrial processes mechanism and its large computational time requirement." (p.1)
- comparatively (introduction): "Comparatively, deep learning with multilayer architectures usually has excellent performance in those complex problems [12]." (p.1)
- however (introduction): "However, regression prediction is more popular in industrial process control." (p.2)

## Hedge verbs

- introduce / causal / abstract, conclusion: "This paper introduces deep learning to soft sensor modeling"; "This paper has introduced deep learning into soft sensor modeling"
- propose / causal / abstract, introduction, conclusion: "proposes a novel soft sensor modeling method based on a deep learning network"; "This paper proposes a soft sensor modeling method based on deep learning"
- improve / causal / abstract: "DAE-NN-based soft sensor significantly improves the performance and generalization of data-driven soft sensors."
- indicate / causal / conclusion: "The excellent generalization performance indicates that the DAE-NN-based soft sensor provides a powerful tool for soft sensor modeling."

## Cross-section linkers

- introduction → method: "This paper is organized as follows. Section II describes the DAE. Section III proposes a soft sensor modeling method based on DAE-NN and describes it in detail. A case study on the estimation of oxygen content in flue gasses in ultrasuperficial units is given in Section IV. Finally, the conclusion is provided in Section V." (p.2)
- method → experiments: Step 1–11 流程后接 `IV. CASE STUDY: ESTIMATE OXYGEN-CONTENT IN FLUE GASSES` (p.4)
- experiments → conclusion: 深度与数据量讨论后直接 `V. CONCLUSION` (p.8)

## Candidate rules

- R001 abstract 用 `This paper introduces` + `and proposes a novel`，再接工业应用。
- R002 Introduction 无独立 Related Work，浅层/深度对比写在引言中段。
- R003 Introduction 末用 `This paper is organized as follows` 指向 II–V。
- R004 Conclusion 用 `This paper has introduced ... and proposes` 收回方法，再用 `In future work` 列后续。
- R005 贡献验证用 `The estimated outputs of DAE-NN-based soft sensors match the real values`，不把 match 句写成 anti-AI。

## Candidate phrases

- `This paper introduces deep learning to soft sensor modeling and proposes` (abstract)
- `This paper is organized as follows.` (introduction)
- `This paper proposes a soft sensor modeling method based on` (introduction)
- `This paper has introduced deep learning into soft sensor modeling and proposes` (conclusion)
- `In future work, more sophisticated solving algorithms` (conclusion)

## House style

自称是 `This paper introduces` / `This paper proposes` / `This paper has introduced` / `this paper`。未见 `Here we`。`This paper introduces` 与 `This paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Soft sensors have been widely used in industrial processes.
- p.1 abstract: This paper introduces deep learning to soft sensor modeling and proposes a novel soft sensor modeling method based on a deep learning network that integrates denoising autoencoders with a neural network (DAE-NN).
- p.1 abstract: Deep learning provides a very effective and promising method for soft sensor modeling.
- p.1 introduction: IN MODERN industrial processes, some important process variables that are key indicators of process performance are difficult or impossible to measure online as a result of economic or technical limitations.
- p.1 introduction: However, the FPM is often not available because of the complexity of the industrial processes mechanism and its large computational time requirement.
- p.1 introduction: Comparatively, deep learning with multilayer architectures usually has excellent performance in those complex problems [12].
- p.2 introduction: However, regression prediction is more popular in industrial process control.
- p.2 introduction: This paper proposes a soft sensor modeling method based on deep learning that integrates a denoising autoencoder with a neural network (DAE-NN) to improve the performance and robustness of soft sensors.
- p.2 introduction: This paper is organized as follows. Section II describes the DAE. Section III proposes a soft sensor modeling method based on DAE-NN and describes it in detail. A case study on the estimation of oxygen content in flue gasses in ultrasuperficial units is given in Section IV. Finally, the conclusion is provided in Section V.
- p.3 method: Soft sensors based on DAE-NN aim to exploit the essential information behind the process data and address the unlabeled data in soft sensor modeling.
- p.4 experiments: Ultrasuperficial units are one of the main trends of coal-fired thermal power that can achieve clean coal combustion and greatly improve energy efficiency.
- p.8 conclusion: This paper has introduced deep learning into soft sensor modeling and proposes a soft sensor modeling method based on DAE-NN.
- p.8 conclusion: The excellent generalization performance indicates that the DAE-NN-based soft sensor provides a powerful tool for soft sensor modeling.
- p.8 conclusion: In future work, more sophisticated solving algorithms, such as LBFGS and a conjugate gradient, will be used to improve performance.
