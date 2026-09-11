---
key: I8FIUZPA
title: "A stable soft sensor based on causal inference and graph convolutional network for batch processes"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2024.125692"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Preliminaries`（`2.1. Graph convolutional networks` / `2.2. Spatiotemporal attention mechanisms`）→ `3. Proposed soft sensor method` → `4. Case study`（青霉素 / 金霉素两例）→ `5. Conclusion`。前置 `ABSTRACT` 与 `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 GPR/PLS/RVM/ANN、深度学习软测量、GCN 与因果推断）。Introduction 末有编号贡献 + 节序路标。Method 前有 Preliminaries。Experiments 标题为 `Case study`。

## Openers

- abstract: `Data-driven soft sensor` — "Data-driven soft sensor techniques play a crucial role in process control, which can ensure process safety, and improve product quality by measuring key variables that are challenging to measure in batch processes."
- introduction: `Batch processes have` — "Batch processes have been widely used as an important industrial production method in fine chemicals, biopharmaceuticals and metal processing (Mowbray et al., 2022)."
- method: `This section first` — "This section first presents the overall framework of stable soft sensor, followed by introduction to each component." (s.3)
- experiments: `In this section,` — "In this section, we conduct experiments using data from two typical batch processes to validate the proposed method."
- conclusion: `This paper proposes` — "This paper proposes a stable soft sensor for batch processes based on causal inference and GCN to enhance the accuracy and stability of soft sensor."

## Gap transitions

- however (introduction): "However, due to the limitations of sensor technology and the operating environment, it is difficult to directly measure some key variables in batch processes (Rathore et al., 2022)."
- however (introduction): "However, since the production cycles of batch processes are not strictly repetitive, there are differences in data distribution between different batches (Jin et al., 2015)."
- therefore (introduction): "Therefore, a stable soft sensor method based on causal inference and GCN for batch processes is proposed to improve the stability and accuracy of the soft sensor model."
- in this work (abstract): "In this work, a stable soft sensor based on causal inference and graph convolutional networks is proposed for batch processes."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "is proposed for batch processes"; "this paper proposes"
- demonstrate / associative / abstract, conclusion: "Experimental results from two batch processes demonstrate the feasibility and effectiveness of stable soft sensor"; "Experimental results from penicillin fermentation and chlortetracycline fermentation processes demonstrate"
- show / associative / experiments: "These results show that CGCN not only has higher computational efficiency but also significantly reduces storage requirements."

## Cross-section linkers

- introduction → preliminaries: "The rest of paper is organized as follows. Section 2 presents the principles of GCN and the spatiotemporal attention mechanisms."
- method → experiments: "The proposed CGCN-based soft sensor is verified by two industrial case studies in Section 4."
- experiments → conclusion: 金霉素案例限制段落后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of paper is organized as follows`
- R004 编号贡献：`The main contributions of this work are summarized as follows`
- R009 自称：`This paper proposes` / `is proposed`

## Candidate phrases

- `In this work, a stable soft sensor based on causal inference and graph convolutional networks is proposed` (abstract)
- `The main contributions of this work are summarized as follows` (introduction)
- `The rest of paper is organized as follows` (introduction)
- `In this section, we conduct experiments using data from two typical batch processes` (experiments)
- `This paper proposes a stable soft sensor for batch processes` (conclusion)

## House style

自称 `This paper proposes` / `In this work` / `the proposed method`。实验节用 `we conduct`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Data-driven soft sensor techniques play a crucial role in process control, which can ensure process safety, and improve product quality by measuring key variables that are challenging to measure in batch processes.
- abstract: In this work, a stable soft sensor based on causal inference and graph convolutional networks is proposed for batch processes.
- abstract: Experimental results from two batch processes demonstrate the feasibility and effectiveness of stable soft sensor, and the learned causal relationships between variables closely correspond to the fundamental principles of the process.
- introduction: Batch processes have been widely used as an important industrial production method in fine chemicals, biopharmaceuticals and metal processing (Mowbray et al., 2022).
- introduction: However, due to the limitations of sensor technology and the operating environment, it is difficult to directly measure some key variables in batch processes (Rathore et al., 2022).
- introduction: Therefore, a stable soft sensor method based on causal inference and GCN for batch processes is proposed to improve the stability and accuracy of the soft sensor model.
- introduction: The main contributions of this work are summarized as follows:
- introduction: The rest of paper is organized as follows. Section 2 presents the principles of GCN and the spatiotemporal attention mechanisms.
- method: This section first presents the overall framework of stable soft sensor, followed by introduction to each component.
- experiments: In this section, we conduct experiments using data from two typical batch processes to validate the proposed method.
- experiments: These results show that CGCN not only has higher computational efficiency but also significantly reduces storage requirements.
- conclusion: This paper proposes a stable soft sensor for batch processes based on causal inference and GCN to enhance the accuracy and stability of soft sensor.
- conclusion: Experimental results from penicillin fermentation and chlortetracycline fermentation processes demonstrate that compared with the soft sensor models based on RVM, LSTM, GRU, STCL, and SAGE, the CGCN-based soft sensor model has more stable and accurate performance.
