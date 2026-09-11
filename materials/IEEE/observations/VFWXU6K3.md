---
key: VFWXU6K3
title: "Multiscale Temporal-Variable Patches Network for Long-Term Prediction of Industrial Key Parameters"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2024.3453435"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8,10-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. PROPOSED METHOD` → `IV. CASES STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 中段已评 soft sensor / long-term forecasting / granular computing / patch models，再在 II 展开 Multi-Head Attention 与 BiGRU。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `CASES STUDIES`（ETT + loosening and conditioning）。

## Openers

- abstract: `In the face` — "In the face of industrial time-delay characteristics, long-term prediction of key parameters is pivotal for industrial optimization and control." (p.1)
- introduction: `ACCURATE prediction of` — "ACCURATE prediction of key parameters is essential for industrial optimization and control, as it provides essential decision support for maintaining the continuous and stable operation of industrial processes [1]." (p.1；栏首掉字)
- related_work: `The attention mechanism` — "The attention mechanism was initially introduced for machine translation tasks and has gained widespread recognition for its outstanding performance in sequence-to-sequence tasks." (p.3, II.A)
- method: `This section provides` — "This section provides a detailed description of MS-TVPNet, which comprises three parts: patch-based inter-variable modeling, cross-scale redundant feature optimization, and patch-based temporal dependencies modeling." (p.4, III)
- experiments: `In this section` — "In this section, the proposed long-term prediction network is validated in two industrial datasets." (p.7, IV)
- conclusion: `In summary, this` — "In summary, this paper presents MS-TVPNet for long-term prediction in industrial processes with time delays." (p.11)

## Gap transitions

- however (abstract): "However, traditional soft sensor models encounter difficulties in addressing long-term prediction." (p.1)
- to address (abstract): "To address these challenges, we propose a multiscale temporal-variable patches network (MS-TVPNet)." (p.1)
- therefore (introduction): "Therefore, it is essential to perceive system changes in advance through long-term predictions." (p.2)
- however (introduction): "However, they are not designed for long-term forecasting and therefore do not perform well with extensive historical data." (p.2)
- to address (introduction): "To address this gap, our research focuses on developing a model specifically tailored to long-term predictions." (p.2)
- despite (conclusion): "Despite its superior performance, MS-TVPNet has some limitations." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a multiscale temporal-variable patches network (MS-TVPNet)"; "we propose a novel multiscale temporal-variable patches network"
- demonstrate / causal / abstract, introduction: "Two industrial datasets are used for extensive experiments to demonstrate the effectiveness of the proposed method."; "we demonstrate the necessity of the proposed architecture through ablation experiments."
- introduce / causal / introduction: "We introduce a cross-scale redundancy optimization mechanism"
- show / causal / experiments, conclusion: "Fig. 12 shows the comparison curves"; "Extensive experiments ... show that MS-TVPNet outperforms nine other long-term prediction models."
- conclude / causal / experiments: "Based on the results, we conclude that MS-TVPNet generally outperforms other structures."

## Cross-section linkers

- introduction → related work: "The rest of this paper is organized as follows. In Section II, the knowledge of Multi-Head Attention mechanism and BiGRU is introduced. In Section III, the MS-TVPNet model is introduced in detail. In Section IV, we validate the effectiveness of MS-TVPNet through comparisons with nine models... Finally, the conclusion is outlined in Section V." (p.3)
- related work → method: BiGRU 段落后直接 `III. PROPOSED METHOD` (p.4)
- method → experiments: 评价度量段落后 `IV. CASES STUDIES` (p.7)
- experiments → conclusion: 消融后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `To address these challenges, we propose` + 方法缩写。
- R002 独立 Related Work 写组件预备知识（Attention / BiGRU），已有方法评述仍在 Introduction 中段。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–V。
- R004 贡献用 `Our main contributions are as follows` + 编号列表。
- R005 Conclusion 先收回方法，再用 `Despite its superior performance` 承认局限，`future research will focus on` 指向后续。

## Candidate phrases

- `To address these challenges, we propose a` (abstract)
- `To address this gap, our research focuses on developing` (introduction)
- `Our main contributions are as follows.` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `In summary, this paper presents` (conclusion)

## House style

自称是 `we propose` / `this paper` / `our research` / `our method`。未见 `Here we`。`we propose` 与 `this paper presents` 进 phrase_bank，不进 anti_ai_patterns。见 `The rest of this paper is organized as follows`。

## Quotes

- p.1 abstract: In the face of industrial time-delay characteristics, long-term prediction of key parameters is pivotal for industrial optimization and control.
- p.1 abstract: However, traditional soft sensor models encounter difficulties in addressing long-term prediction.
- p.1 abstract: To address these challenges, we propose a multiscale temporal-variable patches network (MS-TVPNet).
- p.1 abstract: Two industrial datasets are used for extensive experiments to demonstrate the effectiveness of the proposed method.
- p.1 introduction: ACCURATE prediction of key parameters is essential for industrial optimization and control, as it provides essential decision support for maintaining the continuous and stable operation of industrial processes [1].
- p.2 introduction: Therefore, it is essential to perceive system changes in advance through long-term predictions.
- p.2 introduction: However, they are not designed for long-term forecasting and therefore do not perform well with extensive historical data.
- p.2 introduction: To address this gap, our research focuses on developing a model specifically tailored to long-term predictions.
- p.3 introduction: Given the limitations of the previously mentioned methods, we propose a multiscale temporal-variable patches network (MS-TVPNet) for accurate long-term prediction of industrial key parameters.
- p.3 introduction: Our main contributions are as follows.
- p.3 introduction: The rest of this paper is organized as follows. In Section II, the knowledge of Multi-Head Attention mechanism and BiGRU is introduced. In Section III, the MS-TVPNet model is introduced in detail. In Section IV, we validate the effectiveness of MS-TVPNet through comparisons with nine models, using the open-source Electricity Transformer Temperature (ETT) dataset, as well as real-world data from loosening and controlling processes. Furthermore, we demonstrate the necessity of the proposed architecture through ablation experiments. Finally, the conclusion is outlined in Section V.
- p.4 method: This section provides a detailed description of MS-TVPNet, which comprises three parts: patch-based inter-variable modeling, cross-scale redundant feature optimization, and patch-based temporal dependencies modeling.
- p.7 experiments: In this section, the proposed long-term prediction network is validated in two industrial datasets.
- p.8 experiments: Based on the results, it is evident that MS-TVPNet consistently exhibits outstanding performance across three metrics.
- p.11 experiments: In summary, MS-TVPNet surpasses all ablation structures and demonstrates exceptional performance in the long-term prediction of industrial key parameters.
- p.11 conclusion: In summary, this paper presents MS-TVPNet for long-term prediction in industrial processes with time delays.
- p.11 conclusion: Extensive experiments on the ETT dataset, as well as in loosening and conditioning processes, show that MS-TVPNet outperforms nine other long-term prediction models.
- p.11 conclusion: Despite its superior performance, MS-TVPNet has some limitations.
- p.11 conclusion: To address these issues, future research will focus on adaptively acquiring patches based on model inputs, thereby enhancing the model's flexibility and adaptability.
