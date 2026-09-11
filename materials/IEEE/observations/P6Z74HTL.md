---
key: P6Z74HTL
title: "Robust Online Sequential RVFLNs for Data Modeling of Dynamic Time-Varying Systems With Application of an Ironmaking Blast Furnace"
venue: "IEEE Transactions on Cybernetics"
doi: "10.1109/TCYB.2019.2920483"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. IMPROVED OS-RVFLNS` → `III. ROBUST OS-RVFLNS` → `IV. R-OS-RVFLNS-BASED ROBUST MODELING OF IRONMAKING BLAST FURNACE` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 first-principle / data-driven、BF 的 statistical / subspace / AI 模型、RVFLNs、OS-RVFLNs、M-estimator RVFLNs）。Introduction 末无 `The rest of this paper is organized` 路标，直接进入 Section II。Method 为 II–III。Experiments 为 IV（高炉工业数据 + 人为异常值）。

## Openers

- abstract: `By dealing with` — "By dealing with robust modeling and online learning together in a unified random vector functional-link networks (RVFLNs) framework, this paper presents a novel robust online sequential RVFLNs for data modeling of dynamic time-varying systems together with its application for a blast furnace (BF) ironmaking process." (p.1)
- introduction: `IT IS well` — "IT IS well known that for the modern process industries, some key variables, such as product quality and production efficiency reflect the operational performance of the whole industrial process, and play an indispensable role in quality control as well as production safety." (p.1；栏首掉字)
- method: `Focusing on the` — "Focusing on the data saturation problem of OS-RVFLNs, this paper proposes an improved online sequential RVFLNs by introducing forgetting factor to adjust the sensitivity to different samples." (p.3, II.B)
- experiments: `As a key` — "As a key production unit in steel manufacturing, the ironmaking BF is used to physically convert and chemically reduce solid iron oxides into liquid hot metal of high quality with low production cost." (p.7, IV.A)
- conclusion: `This paper proposed` — "This paper proposed an R-OS-RVFLNs algorithm for data modeling of complex dynamic time-varying systems, and applied it to online prediction of MIQ indices in ironmaking BF." (p.12)

## Gap transitions

- however (introduction): "However, due to the limitations of the measurement and sensor technology, these production indices are usually difficult to be detected online directly, and the offline assaying process for them takes a long time [1]–[3]." (p.1)
- therefore (introduction): "Therefore, the soft-sensor models for online prediction or estimation of MIQ should be established." (p.1)
- however (introduction): "However, the existing data-driven modeling methods still have the following open issues." (p.2)
- however (introduction): "However, there are no research reports on the above-mentioned challenges until now." (p.2)
- however (experiments): "However, when the outlier contamination rate or the outlier amplitude increases, the modeling accuracy of the robust RVFLNs in [5] and the robust LS-SVM in [33] deteriorate greatly, and only the R-OS-RVFLNs algorithm can keep a very high modeling accuracy with very little RMSE all the time." (p.10)

## Hedge verbs

- present / causal / abstract: "this paper presents a novel robust online sequential RVFLNs"
- propose / causal / introduction, method, conclusion: "this paper deals with “robust modeling” and online learning together in a unified RVFLNs framework for the first time, and proposes"; "this paper proposes an improved online sequential RVFLNs"; "This paper proposed an R-OS-RVFLNs algorithm"
- demonstrate / causal / abstract: "Experiments using actual industrial data of a large BF ironmaking process have demonstrated that the proposed algorithm produces a much stronger robustness and better estimation accuracy than other algorithms."
- show / causal / experiments, conclusion: "which shows that the proposed R-OS-RVFLNs algorithm has much better accuracy"; "It has been shown that when the outlier contamination rate is as high as 50%"

## Cross-section linkers

- introduction → method: 贡献段落后直接 `II. IMPROVED OS-RVFLNS`，无节序路标 (p.3)
- method → experiments: Algorithm 1 与 Cauchy 加权段落后接 `IV. R-OS-RVFLNS-BASED ROBUST MODELING OF IRONMAKING BLAST FURNACE` (p.7)
- experiments → conclusion: Table II / PDF 段落后直接 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `this paper presents a novel` + 方法缩写，再接工业应用。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段，并以编号列表列出 Computational Efficiency / Robustness / Online Learning Ability。
- R003 缺口用 `However, there are no research reports on the above-mentioned challenges until now` 再接 `this paper ... proposes`。
- R004 Introduction 末可无 `The rest of this paper is organized as follows`，直接进入方法节。
- R005 Conclusion 用 `This paper proposed` 收回方法，再用编号列表收两点贡献。

## Candidate phrases

- `this paper presents a novel` (abstract)
- `this paper proposes an improved` (method)
- `However, there are no research reports on the above-mentioned challenges until now.` (introduction)
- `Experiments using actual industrial data ... have demonstrated that` (abstract)
- `This paper proposed an R-OS-RVFLNs algorithm for` (conclusion)

## House style

自称是 `this paper` / `this paper presents` / `this paper proposes` / `the proposed algorithm` / `we use the proposed`。未见 `Here we`。`this paper presents` 与 `this paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper` 开篇，但正文多用 `this paper`。

## Quotes

- p.1 abstract: By dealing with robust modeling and online learning together in a unified random vector functional-link networks (RVFLNs) framework, this paper presents a novel robust online sequential RVFLNs for data modeling of dynamic time-varying systems together with its application for a blast furnace (BF) ironmaking process.
- p.1 abstract: Experiments using actual industrial data of a large BF ironmaking process have demonstrated that the proposed algorithm produces a much stronger robustness and better estimation accuracy than other algorithms.
- p.1 introduction: IT IS well known that for the modern process industries, some key variables, such as product quality and production efficiency reflect the operational performance of the whole industrial process, and play an indispensable role in quality control as well as production safety.
- p.1 introduction: However, due to the limitations of the measurement and sensor technology, these production indices are usually difficult to be detected online directly, and the offline assaying process for them takes a long time [1]–[3].
- p.1 introduction: Therefore, the soft-sensor models for online prediction or estimation of MIQ should be established.
- p.2 introduction: However, the existing data-driven modeling methods still have the following open issues.
- p.2 introduction: However, there are no research reports on the above-mentioned challenges until now.
- p.2 introduction: Focused on these practical challenges, and based on our previous works in [5] and [15], this paper deals with “robust modeling” and online learning together in a unified RVFLNs framework for the first time, and proposes a novel robust online sequential RVFLNs (R-OS-RVFLNs) for data modeling of dynamic time-varying systems together with its application for a BF ironmaking process.
- p.3 method: Focusing on the data saturation problem of OS-RVFLNs, this paper proposes an improved online sequential RVFLNs by introducing forgetting factor to adjust the sensitivity to different samples.
- p.7 experiments: As a key production unit in steel manufacturing, the ironmaking BF is used to physically convert and chemically reduce solid iron oxides into liquid hot metal of high quality with low production cost.
- p.9 experiments: To perform modeling performance and robustness analysis of the proposed R-OS-RVFLNs algorithm, other two OS-RVFLNs-based modeling algorithms with different weighting function are first compared.
- p.10 experiments: However, when the outlier contamination rate or the outlier amplitude increases, the modeling accuracy of the robust RVFLNs in [5] and the robust LS-SVM in [33] deteriorate greatly, and only the R-OS-RVFLNs algorithm can keep a very high modeling accuracy with very little RMSE all the time.
- p.12 conclusion: This paper proposed an R-OS-RVFLNs algorithm for data modeling of complex dynamic time-varying systems, and applied it to online prediction of MIQ indices in ironmaking BF.
- p.12 conclusion: It has been shown that when the outlier contamination rate is as high as 50% and the outlier amplitude is up to five times the difference between the maximum and the minimum of each output, the proposed algorithm still has a good modeling accuracy.
