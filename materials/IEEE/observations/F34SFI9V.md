---
key: F34SFI9V
title: "A Cooperative Silicon Content Dynamic Prediction Method With Variable Time Delay Estimation in the Blast Furnace Ironmaking Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3268740"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PROBLEM FORMULATION AND MODELING FRAMEWORK PRESENTATION` → `III. DATASET PREPARATION AND SI PREDICTION MODEL` → `IV.`（DMS-PSO-CS）→ `V. DMS-PSO-CS-BASED D-SDAE MODEL FOR VTD ESTIMATION AND SI PREDICTION` → `VI. EXPERIMENT VALIDATION` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 DAE / 加权深度网络 / PCC·MI 时延估计 / LSTM+DE）。Introduction 末有节序路标，指向 Section II–VII。Experiments 标题为 `EXPERIMENT VALIDATION`（数值仿真 + 华南高炉）。

## Openers

- abstract: `Online assessment of` — "Online assessment of the molten iron quality of a blast furnace ironmaking process strongly depends on reliable measurement of silicon (Si) content." (p.626)
- introduction: `BLAST furnace BF` — "BLAST furnace (BF) ironmaking is the foremost technique that is used to produce molten iron in modern ironmaking [1]." (p.626)
- method: `The sampling time` — "The sampling time stamps of the process variables and labeled Si are shown in Fig. 4(a)." (p.628, III.A)
- experiments: `In this section` — "In this section, the effectiveness of the VTD-based D-SDAE modeling framework is verified based on a numerical simulation and a BF ironmaking plant in South China." (p.633)
- conclusion: `Online Si prediction` — "Online Si prediction plays an important role in product quality and thermal state monitoring." (p.636)

## Gap transitions

- however (introduction): "However, Si online measurement is difficult because manual sampling and offline assaying should take approximately 1–1.5 h." (p.626)
- although (introduction): "Although some improvement was achieved, the feature of process dynamics cannot be accurately described by the static deep network." (p.627)
- thus (introduction): "Thus, the variable time delay (VTD) should be identified and removed from the input variables to obtain the original true data pattern." (p.627)
- however (introduction): "However, that algorithm only considered simple linear relationships between variables and cannot capture more complex features of industrial processes." (p.627)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a novel cooperative strategy"; "a cooperative Si prediction model with a VTD estimation method is proposed in this article"; "a VTD-based soft-sensor cooperative training strategy is proposed"
- show / causal / experiments: "Fig. 7 shows the predicted and actual values of Si and the distribution of the prediction error."
- demonstrate / causal / experiments: "our work demonstrates that adopting a cooperative strategy"
- indicate / causal / experiments: "The results indicate that the VTD estimation using MI is superior to that estimation using PCC"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. The problem formulation and the proposed cooperative modeling framework are presented in Section II. Then, Section III introduces dataset construction work and D-SDAE model. Next, the VTD boundary restriction and DMS-PSO-CS algorithm are described in Section IV. Following this, Section V presents a cooperate training strategy. After that, a numerical simulation and real BF ironmaking application is provided in Section VI. Finally, Section VII concludes this article." (p.628)
- method → experiments: Algorithm 2 后直接 `VI. EXPERIMENT VALIDATION` (p.633)
- experiments → conclusion: 优化曲线段落后 `VII. CONCLUSION` (p.636)

## Candidate rules

- R009 摘要用 `In this article, we propose` 点名协作策略。
- R002 Introduction 无独立 Related Work，时延估计与动态软测量评述写在引言中段。
- R004 贡献列表：`The primary contributions of this article are as follows.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VII。
- R005 Conclusion 先收回方法，实验验证后指出结果可作现场参考。

## Candidate phrases

- `In this article, we propose a novel cooperative strategy to` (abstract)
- `The primary contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a VTD-based soft-sensor cooperative training strategy is proposed` (conclusion)

## House style

自称 `In this article, we propose` / `this article` / `our work` / `our proposed method`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.626 abstract: Online assessment of the molten iron quality of a blast furnace ironmaking process strongly depends on reliable measurement of silicon (Si) content.
- p.626 abstract: In this article, we propose a novel cooperative strategy to train the data-driven prediction model and estimate variable time delay (VTD) values.
- p.626 abstract: The effectiveness of the proposed VTD-based D-SDAE model is validated in a numerical simulation and an industrial ironmaking plant, and a marked improvement in the prediction performance is achieved when VTD information is considered.
- p.626 introduction: BLAST furnace (BF) ironmaking is the foremost technique that is used to produce molten iron in modern ironmaking [1].
- p.626 introduction: However, Si online measurement is difficult because manual sampling and offline assaying should take approximately 1–1.5 h.
- p.627 introduction: Although some improvement was achieved, the feature of process dynamics cannot be accurately described by the static deep network.
- p.627 introduction: Thus, the variable time delay (VTD) should be identified and removed from the input variables to obtain the original true data pattern.
- p.627 introduction: However, that algorithm only considered simple linear relationships between variables and cannot capture more complex features of industrial processes.
- p.627 introduction: The primary contributions of this article are as follows.
- p.628 introduction: The rest of this article is organized as follows. The problem formulation and the proposed cooperative modeling framework are presented in Section II. Then, Section III introduces dataset construction work and D-SDAE model. Next, the VTD boundary restriction and DMS-PSO-CS algorithm are described in Section IV. Following this, Section V presents a cooperate training strategy. After that, a numerical simulation and real BF ironmaking application is provided in Section VI. Finally, Section VII concludes this article.
- p.628 method: The sampling time stamps of the process variables and labeled Si are shown in Fig. 4(a).
- p.633 experiments: In this section, the effectiveness of the VTD-based D-SDAE modeling framework is verified based on a numerical simulation and a BF ironmaking plant in South China.
- p.634 experiments: The results indicate that the VTD estimation using MI is superior to that estimation using PCC in the univariate estimation methods.
- p.635 experiments: Fig. 7 shows the predicted and actual values of Si and the distribution of the prediction error.
- p.636 conclusion: Online Si prediction plays an important role in product quality and thermal state monitoring.
- p.636 conclusion: In this article, a VTD-based soft-sensor cooperative training strategy is proposed to focus on the time delay characteristic and process dynamics.
- p.636 conclusion: Experiments in a numerical simulation and an industrial BF show that VTD values can be obtained accurately and reconstructed dataset can effectively improve the prediction performance.
