---
key: 7NWCV6Z6
title: "Multirate-Former: An Efficient Transformer-Based Hierarchical Network for Multistep Prediction of Multirate Industrial Processes"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2023.3331407"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-5,7-8,11-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. MULTIRATE-FORMER` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 semisupervised ELM / DNN、down-sampling、interpolation、LSTMa、LSTnet、LogTrans、Informer、mvts-transformer）。II 为 `PRELIMINARIES`（attention + transformer）。Introduction 末有 `The rest of this article is organized as follows`，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDIES`（debutanizer + hydrocracking）。

## Openers

- abstract: `Due to the limitations` — "Due to the limitations of measurement technology and cost in industrial processes, it is difficult to obtain measured values of variables with different properties, such as flow rate and temperature, under uniform sampling rates." (p.1)
- introduction: `IN MODERN industrial` — "IN MODERN industrial processes, it is of great importance to monitor the key quality variables to maintain a safe state of the process and provide effective control and optimization methods [1], [2]." (p.1；栏首掉字)
- method: `Due to the variations` — "Due to the variations in measured variables and the limitations of the measurement techniques, multirate processes are very common in industry, which greatly limits the efficacy of data utilization and accurate process modeling." (p.4, III)
- experiments: `In this section` — "In this section, the proposed Multirate-Former for soft sensor modeling is validated on the two industrial processes." (p.7, IV)
- conclusion: `In this article` — "In this article, a novel transformer-based hierarchical network based on Multirate-Former network is developed for multistep prediction of multirate industrial processes." (p.12)

## Gap transitions

- to address (abstract): "To address this issue, this article proposes a novel quality prediction modeling method based on the transformer modal called Multirate-Former for multirate industrial processes." (p.1)
- however (introduction): "However, it is worth noting that most of these methods are developed under the assumption that the industrial process has a uniform sampling rate without considering the prevalent existence of multirate processes." (p.1)
- unfortunately (introduction): "Unfortunately, these semisupervised methods cannot be extended to multirate processes, i.e., process variables and quality variables with more than three sampling frequencies [22]." (p.1–2)
- therefore (introduction): "Therefore, these two methods of processing data are not suitable for actual industrial processes." (p.2)
- regrettably (introduction): "Regrettably, to the best of the authors knowledge, few existing works utilize transformer networks to address the data-missing and soft sensor modeling problems of multirate data in industrial processes." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "this article proposes a novel quality prediction modeling method"; "this article proposes a novel quality prediction modeling method based on the transformer model"
- demonstrate / causal / abstract, experiments: "Experimental results demonstrate that the proposed method outperforms other state-of-the-art methods"; "the proposed method is demonstrated"
- develop / causal / method, conclusion: "this article develops a novel Multirate-Former network"; "a novel transformer-based hierarchical network ... is developed"
- precede / causal / conclusion: "the proposed Multirate-Former method precedes the other state-of-the-art methods"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. In Section II, the attention mechanism and transformer network are briefly described. Details of the proposed Multirate-Former are given in Section III. Then, in Section IV, the effectiveness of the proposed method is demonstrated on a debutanizer column dataset and an industrial hydrocracking process. Finally, Section V concludes this article." (p.3)
- method → experiments: RMSE/MAE 公式后 `IV. CASE STUDIES` (p.7)
- experiments → conclusion: hydrocracking 曲线后 `V. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `this article proposes a novel ... called` + 方法名。
- R002 Introduction 无独立 Related Work；贡献用 `the main contributions of this article are given as follows.` + 编号 1)–5)。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 方法节标题直接用方法名 `III. MULTIRATE-FORMER`，不以 `PROPOSED METHOD` 命名。
- R005 Conclusion 用 `In this article, a novel ... is developed`，展望用 `In the future research, it is a promising direction to study`。

## Candidate phrases

- `To address this issue, this article proposes a novel quality prediction modeling method based on the transformer modal called` (abstract)
- `Considering the current dilemma of industrial multirate processes and the advantages of transformer networks, this article proposes` (introduction)
- `In summary, the main contributions of this article are given as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a novel transformer-based hierarchical network based on Multirate-Former network is developed for` (conclusion)
- `In the future research, it is a promising direction to study` (conclusion)

## House style

自称是 `this article` / `In this article` / `this study`。未见 `Here we`、`In this paper`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Due to the limitations of measurement technology and cost in industrial processes, it is difficult to obtain measured values of variables with different properties, such as flow rate and temperature, under uniform sampling rates.
- p.1 abstract: To address this issue, this article proposes a novel quality prediction modeling method based on the transformer modal called Multirate-Former for multirate industrial processes.
- p.1 abstract: Experimental results demonstrate that the proposed method outperforms other state-of-the-art methods in dealing with multisampling rate types of industrial process data.
- p.1 introduction: IN MODERN industrial processes, it is of great importance to monitor the key quality variables to maintain a safe state of the process and provide effective control and optimization methods [1], [2].
- p.1 introduction: However, it is worth noting that most of these methods are developed under the assumption that the industrial process has a uniform sampling rate without considering the prevalent existence of multirate processes.
- p.1–2 introduction: Unfortunately, these semisupervised methods cannot be extended to multirate processes, i.e., process variables and quality variables with more than three sampling frequencies [22].
- p.2 introduction: Therefore, these two methods of processing data are not suitable for actual industrial processes.
- p.2 introduction: Regrettably, to the best of the authors knowledge, few existing works utilize transformer networks to address the data-missing and soft sensor modeling problems of multirate data in industrial processes.
- p.2 introduction: In summary, the main contributions of this article are given as follows.
- p.3 introduction: The rest of this article is organized as follows. In Section II, the attention mechanism and transformer network are briefly described. Details of the proposed Multirate-Former are given in Section III. Then, in Section IV, the effectiveness of the proposed method is demonstrated on a debutanizer column dataset and an industrial hydrocracking process. Finally, Section V concludes this article.
- p.4 method: Due to the variations in measured variables and the limitations of the measurement techniques, multirate processes are very common in industry, which greatly limits the efficacy of data utilization and accurate process modeling.
- p.4 method: Hence, this article develops a novel Multirate-Former network for multirate industrial process data modeling, which overcomes the drawbacks of traditional soft sensor models that cannot utilize the whole data samples and cannot capture correlations between samples with different sampling rates.
- p.7 experiments: In this section, the proposed Multirate-Former for soft sensor modeling is validated on the two industrial processes.
- p.12 conclusion: In this article, a novel transformer-based hierarchical network based on Multirate-Former network is developed for multistep prediction of multirate industrial processes.
- p.12 conclusion: From the comparison of prediction RMSE and MAE, the proposed Multirate-Former method precedes the other state-of-the-art methods.
- p.12 conclusion: In the future research, it is a promising direction to study multirate processes with a small number of samples or industrial processes with many measured outliers.
