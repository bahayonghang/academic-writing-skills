---
key: 9QEFAFXT
title: "Knowledge-Data-Based Synchronization States Analysis for Process Monitoring and Its Application to Hydrometallurgical Zinc Purification Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3268411"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES AND BASIC IDEAS` → `III. KNOWLEDGE-DATA-DRIVEN PROCESS MONITORING` → `IV. APPLICATION TO COPPER–COBALT REMOVAL` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评图网络关联、同步现象与耦合矩阵/节点状态缺口）。Introduction 末有编号贡献与节序路标，指向 Section II–V。Method 标题为 `KNOWLEDGE-DATA-DRIVEN PROCESS MONITORING`。Experiments 标题为 `APPLICATION TO COPPER–COBALT REMOVAL`（湿法炼锌除铜除钴）。

## Openers

- abstract: `Modern industrial processes` — "Modern industrial processes generate many interassociated variables, which are more likely to implicit associations knowledge for describing irregular changes at different times to accurately describe behavior changes." (p.546)
- introduction: `PROCESS monitoring has` — "PROCESS monitoring has become the most useful one to meet the increasing demands on ensuring safety and reliability, especially for increasing large-scale, complicated, and intelligent modern processes." (p.546；栏首掉字)
- method: `Above three theorems` — "Above three theorems have proved that the synchronization status of a complex network can be effectively employed to describe global behavior." (p.549)
- experiments: `The configurations of` — "The configurations of the application study on copper–cobalt removal process consist of Python 3.6.8 software, a workstation with 16 CPUs (Intel(R) Xeon(R) Gold 5222 CPU at 3.80-GHz 128-GB RAM) and one GPU (NVIDIA GeForce RTX 2080 Ti at 11.0 GB)." (p.552)
- conclusion: `This article presented` — "This article presented a novel process monitoring method based on knowledge-data-based synchronization states analysis, and unitized it to achieve process monitoring for the copper–cobalt removal process." (p.556)

## Gap transitions

- motivated by (abstract): "Motivated by this issue, a novel knowledge-data-based synchronization states analysis method is proposed in this article for process monitoring." (p.546)
- however (introduction): "However, only data-driven association characteristics without any mechanism/prior knowledge are often concealed to make it decrease to precisely describe irregular changes frequently occurring in industrial processes [2], [3]." (p.546)
- however (introduction): "However, when pushing complex synchronization status into practical application, two keys should be first well solved: the definition of the network coupling matrix and the representation of each node status." (p.547)
- to handle (introduction): "To handle this problem, a novel knowledge-data-based synchronization states analysis method is proposed, and it is applied to process monitoring for the practical hydrometallurgical zinc purification process." (p.547)
- however (conclusion): "However, some problems still need to be solved, such as whether other methods, etc., can determine the coupling matrix." (p.556)

## Hedge verbs

- propose / causal / abstract, introduction: "a novel knowledge-data-based synchronization states analysis method is proposed in this article"; "a novel knowledge-data-based synchronization states analysis method is proposed"
- show / causal / abstract: "The application’s comparable performance shows the applicability and effectiveness of this proposed method."
- demonstrate / causal / conclusion: "Experiments on the copper–cobalt removal process demonstrated the effectiveness and applicability of this proposed method."
- may / speculative / conclusion: "The synchronization status analysis may be the first to unitize it to perceive irregular changes to describe the system behavior."

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II illustrates the preliminaries of this article. Section III addresses the overall process monitoring approach based on synchronization analysis. The details of the hydrometallurgical zinc solution purification case study are described in Section IV. Finally, Section V concludes this article." (p.547)
- method → experiments: 显式/隐式知识段落后直接 `IV. APPLICATION TO COPPER–COBALT REMOVAL` (p.552)
- experiments → conclusion: 对比讨论段落后直接 `V. CONCLUSION` (p.556)

## Candidate rules

- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions can be summarized as follows.` + 编号。
- R007 摘要用 `Motivated by this issue, ... is proposed in this article`。
- R005 结论局限：`However, some problems still need to be solved`，`which is worthy of deep study`。

## Candidate phrases

- `Motivated by this issue, a novel ... method is proposed in this article` (abstract)
- `The main contributions can be summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article presented a novel process monitoring method based on` (conclusion)
- `However, some problems still need to be solved` (conclusion)

## House style

自称 `is proposed in this article` / `this proposed method` / `This article presented`。未见 `Here we`。`is proposed in this article` 与 `This article presented` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.546 abstract: Modern industrial processes generate many interassociated variables, which are more likely to implicit associations knowledge for describing irregular changes at different times to accurately describe behavior changes.
- p.546 abstract: Motivated by this issue, a novel knowledge-data-based synchronization states analysis method is proposed in this article for process monitoring.
- p.546 abstract: The application’s comparable performance shows the applicability and effectiveness of this proposed method.
- p.546 introduction: PROCESS monitoring has become the most useful one to meet the increasing demands on ensuring safety and reliability, especially for increasing large-scale, complicated, and intelligent modern processes.
- p.546 introduction: However, only data-driven association characteristics without any mechanism/prior knowledge are often concealed to make it decrease to precisely describe irregular changes frequently occurring in industrial processes [2], [3].
- p.547 introduction: However, when pushing complex synchronization status into practical application, two keys should be first well solved: the definition of the network coupling matrix and the representation of each node status.
- p.547 introduction: To handle this problem, a novel knowledge-data-based synchronization states analysis method is proposed, and it is applied to process monitoring for the practical hydrometallurgical zinc purification process. The main contributions can be summarized as follows.
- p.547 introduction: The rest of this article is organized as follows. Section II illustrates the preliminaries of this article. Section III addresses the overall process monitoring approach based on synchronization analysis. The details of the hydrometallurgical zinc solution purification case study are described in Section IV. Finally, Section V concludes this article.
- p.549 method: Above three theorems have proved that the synchronization status of a complex network can be effectively employed to describe global behavior.
- p.552 experiments: The configurations of the application study on copper–cobalt removal process consist of Python 3.6.8 software, a workstation with 16 CPUs (Intel(R) Xeon(R) Gold 5222 CPU at 3.80-GHz 128-GB RAM) and one GPU (NVIDIA GeForce RTX 2080 Ti at 11.0 GB).
- p.556 experiments: In summary, the proposed process monitoring method is promising for applying to the hydrometallurgical zinc purification process of its comparable performance.
- p.556 conclusion: This article presented a novel process monitoring method based on knowledge-data-based synchronization states analysis, and unitized it to achieve process monitoring for the copper–cobalt removal process.
- p.556 conclusion: Experiments on the copper–cobalt removal process demonstrated the effectiveness and applicability of this proposed method. However, some problems still need to be solved, such as whether other methods, etc., can determine the coupling matrix. Some false alarm rates are still unacceptable, which is worthy of deep study.
