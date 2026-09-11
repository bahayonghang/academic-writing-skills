---
key: AC3KYAM5
title: "BiSDA: Bidirectional Self-Refining Domain Adaptation for Streaming-Evolving Industrial Soft Sensing"
venue: "IEEE Transactions on Industrial Electronics"
doi: "10.1109/TIE.2025.3637394"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. INCREMENTAL SELF-LABELING MECHANISM` → `IV. BIDIRECTIONAL SELF-REFINING DOMAIN ADAPTATION` → `V. CASE STUDY` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`，分 stream learning 与 gradual domain adaptation）。`related_work=independent`。Introduction 末有 `The rest of the article is organized as follows` 路标，指向 II–VI。Method 拆成 ISL 理论（III）与 BiSDA 框架（IV）。Experiments 标题为 `CASE STUDY`（两个氨合成子系统）。

## Openers

- abstract: `In ammonia synthesis` — "In ammonia synthesis processes, key quality variables such as CO2 concentration in the absorption column are difficult to measure directly in real time, necessitating the use of soft sensors." (p.1)
- introduction: `AMMONIA synthesis processes` — "AMMONIA synthesis processes (ASP) are critical to the chemical industry, where ensuring high product quality and operational efficiency is essential for both economic and environmental sustainability [1]." (p.1)
- method: `Here, denote the` — "Here, denote the labeled source samples as XS with labels YS and the unlabeled target domain samples as DT." (p.2, III.A)
- experiments: `In this section` — "In this section, we implement the proposed BiSDA in two real subsystems under streaming-evolving settings including a CO2 absorption column and a CO2 four-stage compression system." (p.6, V)
- conclusion: `In this article` — "In this article, we propose a bidirectional domain adaptation framework, BiSDA, for soft sensing in streaming industrial environments." (p.11)

## Gap transitions

- however (abstract): "However, due to process dynamics, sensor aging, and environmental fluctuations, streaming process data in such systems often exhibits incremental domain shift and complex temporal dependencies, posing serious challenges to conventional soft sensing models." (p.1)
- to address (abstract): "To address these issues, we first formulate the incremental domain shift challenge as an online EM-based objective and propose an incremental self-labeling (ISL) mechanism to solve it accordingly." (p.1)
- unfortunately (introduction): "Unfortunately, to the best of our knowledge, this incremental domain shift problem has not been well-noticed yet in the field of industrial soft sensors." (p.1)
- however (related work): "However, most existing methods do not take the incremental domain shift into consideration." (p.2)
- although (method): "Although the incremental self-labeling mechanism enables progressive adaptation to evolving target data, it can be vulnerable under substantial domain shifts, where early pseudolabels tend to be inaccurate." (p.4)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose an incremental self-labeling (ISL) mechanism"; "we propose a novel streaming-evolving framework"; "we propose a bidirectional domain adaptation framework"
- demonstrate / causal / abstract, introduction: "demonstrates that BiSDA significantly outperforms existing methods"; "Experimental results demonstrate that BiSDA achieves"
- formulate / causal / introduction: "we first propose an EM-based objective to formulate the incremental domain shift challenge"
- validate / causal / introduction: "Validate the BiSDA on two real-world ASP soft sensing tasks"

## Cross-section linkers

- introduction → related work: "The rest of the article is organized as follows. Section II briefly describes the related works. Section III describes the incremental self-labeling mechanism while Section IV introduces the BiSDA-based soft sensors. Section V shows the results of BiSDA application in two practical industrial cases. Finally, we summarize the above work in Section VI." (p.2)
- related work → method: "Compared with our work, however, the GDA falls short because it can be regarded as a greedy version of the proposed method." 随后 `III. INCREMENTAL SELF-LABELING MECHANISM` (p.2)
- method → experiments: BiSDA 软传感器段落后接 `V. CASE STUDY` (p.6)
- experiments → conclusion: 敏感性分析后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `To address these issues, we first formulate` + `we propose`，不用 `Here we`。
- R002 独立 Related Work 后接 ISL 理论节，再落到 BiSDA 方法节。
- R003 Introduction 末用 `The rest of the article is organized as follows` 指向 II–VI。
- R004 贡献用 `In summary, our contributions are as follows.` + 编号列表。
- R005 Experiments 标题为 `CASE STUDY`。
- R006 Conclusion 用 `In this article, we propose` 收回，再用 `we plan to` 指向后续。

## Candidate phrases

- `To address these issues, we first formulate` (abstract)
- `we propose a bidirectional self-refining domain adaptation (BiSDA) framework` (abstract)
- `In summary, our contributions are as follows.` (introduction)
- `The rest of the article is organized as follows.` (introduction)
- `In this article, we propose a bidirectional domain adaptation framework` (conclusion)

## House style

自称是 `we propose` / `we first formulate` / `this article` / `our contributions`。未见 `Here we`（III.A 有 `Here, denote the` 作记号句，非 Nature 式 `Here we`）。`In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In ammonia synthesis processes, key quality variables such as CO2 concentration in the absorption column are difficult to measure directly in real time, necessitating the use of soft sensors.
- p.1 abstract: However, due to process dynamics, sensor aging, and environmental fluctuations, streaming process data in such systems often exhibits incremental domain shift and complex temporal dependencies, posing serious challenges to conventional soft sensing models.
- p.1 abstract: To address these issues, we first formulate the incremental domain shift challenge as an online EM-based objective and propose an incremental self-labeling (ISL) mechanism to solve it accordingly.
- p.1 abstract: Based on ISL, we propose a bidirectional self-refining domain adaptation (BiSDA) framework that combines forward incremental learning and backward self-refinement to simultaneously capture short-term and long-term temporal structures.
- p.1 introduction: AMMONIA synthesis processes (ASP) are critical to the chemical industry, where ensuring high product quality and operational efficiency is essential for both economic and environmental sustainability [1].
- p.1 introduction: Unfortunately, to the best of our knowledge, this incremental domain shift problem has not been well-noticed yet in the field of industrial soft sensors.
- p.2 introduction: In summary, our contributions are as follows.
- p.2 introduction: The rest of the article is organized as follows. Section II briefly describes the related works. Section III describes the incremental self-labeling mechanism while Section IV introduces the BiSDA-based soft sensors. Section V shows the results of BiSDA application in two practical industrial cases. Finally, we summarize the above work in Section VI.
- p.2 related work: However, most existing methods do not take the incremental domain shift into consideration.
- p.2 method: Here, denote the labeled source samples as XS with labels YS and the unlabeled target domain samples as DT.
- p.4 method: Although the incremental self-labeling mechanism enables progressive adaptation to evolving target data, it can be vulnerable under substantial domain shifts, where early pseudolabels tend to be inaccurate.
- p.6 experiments: In this section, we implement the proposed BiSDA in two real subsystems under streaming-evolving settings including a CO2 absorption column and a CO2 four-stage compression system.
- p.11 conclusion: In this article, we propose a bidirectional domain adaptation framework, BiSDA, for soft sensing in streaming industrial environments.
- p.11 conclusion: Experiments on two real ammonia synthesis subsystems validate its superior performance over existing methods.
- p.11 conclusion: As a result, we plan to continuously monitor the domain shift in our future work.
