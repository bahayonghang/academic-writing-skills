---
key: E6GKXSTX
title: "Long Sequence Multivariate Time-Series Forecasting for Industrial Processes Using SASGNN"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3424214"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROCESS DESCRIPTION AND PROBLEM FORMULATION` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 GMM/PSO、hierarchical processing、LSTM、difference-LSTM、XGBoost-GRU、GNN/GC）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `In process industries` — "In process industries, the processes are usually very long, which results in long residence of the material in the process." (p.1)
- introduction: `PROCESS industries usually` — "PROCESS industries usually consist of several substages, and each stage requires time to run, resulting in a long residence time for materials in the process." (p.1)
- method: `The architecture of` — "The architecture of the proposed SASGNN is shown in Fig. 2, which consists of two modules: graph structure learning module and long sequence forecasting module." (p.3)
- experiments: `In this section` — "In this section, the effectiveness of the proposed SASGNN is evaluated in a tungsten flotation plant and the superiority of SASGNN is demonstrated by comparing it with other popular deep learning-based MTSF methods." (p.6)
- conclusion: `In this article` — "In this article, a novel SASGNN model is proposed to realize effective long sequence MTSF for complex process industries." (p.10)

## Gap transitions

- however (abstract): "However, many current MTSF methods do not consider the relationships between variables adequately, making it difficult to achieve satisfactory results for long sequence forecasting." (p.1)
- to address (abstract): "To address this problem, a novel sparse attention spectral graph neural network (SASGNN) is proposed." (p.1)
- therefore (introduction): "Therefore, the control is always delayed." (p.1)
- to address (introduction): "To address the above-mentioned challenges, in this article, a sparse attention spectral graph neural network (SASGNN) is proposed to realize effective long sequence MTSF for industrial processes by taking the tungsten flotation process as an example." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a novel sparse attention spectral graph neural network (SASGNN) is proposed"; "This study proposes a novel graph structure learning method"; "a novel SASGNN model is proposed"
- show / causal / abstract: "Experimental results show the superior and stable performance for long sequence forecasting using the SASGNN."
- aim / causal / introduction: "in this article, we aim to achieve effective long sequence MTSF"
- demonstrate / causal / experiments: "the superiority of SASGNN is demonstrated by comparing it with other popular deep learning-based MTSF methods"
- will consider / speculative / conclusion: "Future work will consider dynamic graph structures"

## Cross-section linkers

- introduction → process: "The rest of this article is organized as follows. Section II describes the tungsten flotation process and the formulated problem. Section III presents the detailed description of the proposed SASGNN. Section IV validates the effectiveness of the proposed method through a case study. Finally, Section V concludes this article." (p.2)
- method → experiments: 复杂度分析后 `IV. CASE STUDY` (p.6)
- experiments → conclusion: 消融结果后 `V. CONCLUSION` (p.10)

## Candidate rules

- R002 Introduction 无独立 Related Work，MTSF/GNN 评述写在引言中段，并以编号挑战列表收束。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this article are as follows`；条目可用 `This study proposes`。
- R005 Conclusion 先收回方法，再用 `Future work will consider` 指向后续。

## Candidate phrases

- `To address this problem, a novel ... is proposed` (abstract)
- `in this article, we aim to achieve` (introduction)
- `The main contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a novel SASGNN model is proposed to` (conclusion)
- `Future work will consider` (conclusion)

## House style

自称 `this article` / `we aim` / `This study proposes` / `the proposed SASGNN`。未见 `Here we`、`In this paper`。`In this article` 与 `This study proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In process industries, the processes are usually very long, which results in long residence of the material in the process.
- p.1 abstract: However, many current MTSF methods do not consider the relationships between variables adequately, making it difficult to achieve satisfactory results for long sequence forecasting.
- p.1 abstract: To address this problem, a novel sparse attention spectral graph neural network (SASGNN) is proposed.
- p.1 abstract: Experimental results show the superior and stable performance for long sequence forecasting using the SASGNN.
- p.1 introduction: PROCESS industries usually consist of several substages, and each stage requires time to run, resulting in a long residence time for materials in the process.
- p.1 introduction: Therefore, the control is always delayed.
- p.1 introduction: Thus, in this article, we aim to achieve effective long sequence MTSF for more optimal and timely control in process industries and to use it as a key tool for modeling complex processes and driving the transformation of process industries to intelligent manufacturing [4].
- p.2 introduction: To address the above-mentioned challenges, in this article, a sparse attention spectral graph neural network (SASGNN) is proposed to realize effective long sequence MTSF for industrial processes by taking the tungsten flotation process as an example.
- p.2 introduction: The main contributions of this article are as follows.
- p.2 introduction: This study proposes a novel graph structure learning method that employs SAM instead of the traditional attention mechanism to reduce computational complexity and learns the latent relationships between variables in a data-driven manner.
- p.2 introduction: The rest of this article is organized as follows. Section II describes the tungsten flotation process and the formulated problem. Section III presents the detailed description of the proposed SASGNN. Section IV validates the effectiveness of the proposed method through a case study. Finally, Section V concludes this article.
- p.3 method: The architecture of the proposed SASGNN is shown in Fig. 2, which consists of two modules: graph structure learning module and long sequence forecasting module.
- p.6 experiments: In this section, the effectiveness of the proposed SASGNN is evaluated in a tungsten flotation plant and the superiority of SASGNN is demonstrated by comparing it with other popular deep learning-based MTSF methods.
- p.10 conclusion: In this article, a novel SASGNN model is proposed to realize effective long sequence MTSF for complex process industries.
- p.10 conclusion: Future work will consider dynamic graph structures to address the working condition drift problem and explore ways to reduce the computational complexity of SASGNN as the number of nodes increases.
