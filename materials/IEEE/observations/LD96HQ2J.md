---
key: LD96HQ2J
title: "A Semi-Supervised Quality Soft Sensing Method Under Multiple Operating Conditions for Complex Product Manufacturing Processes"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3472794"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED SEMI-SUPERVISED QUALITY SOFT SENSING METHOD` → `IV. EXPERIMENTAL AND APPLICATION VALIDATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mechanism/data-driven、局部建模 clustering/ensemble/JITL、concept drift、semi-supervised）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `EXPERIMENTAL AND APPLICATION VALIDATION`。

## Openers

- abstract: `The accurate perception` — "The accurate perception of key quality variables in complex manufacturing processes is a necessary prerequisite for achieving system optimization control and ensuring the safe and stable operation of the system." (p.1)
- introduction: `IN THE complex` — "IN THE complex manufacturing process, the realization of accurate and reliable online measurement of process quality is of great significance in promoting the digital and intelligent development of the manufacturing industry." (p.1；栏首掉字)
- method: `This section will` — "This section will provide a detailed exposition of the soft sensing method proposed in this article, which primarily consists of three parts: 1) dual k-means operating condition identification method assisted by DML; 2) online selective prediction strategy based on the spatiotemporal information adaptive fusion; and 3) high-confidence pseudolabel sample construction method based on JITL and GA." (p.4, III)
- experiments: `To validate the` — "To validate the effectiveness of the aforementioned soft sensing model construction method, this section conducts practical application verification using float glass manufacturing process data." (p.9, IV)
- conclusion: `This article addresses` — "This article addresses the complexity of real industrial processes, including multioperating conditions, time-varying characteristics, and the scarcity of labeled samples." (p.12)

## Gap transitions

- however (introduction): "However, these methods are essentially global modeling techniques, which need to ensure that the modeled data and the real-time data obey the same probability distribution." (p.1)
- although (introduction): "Although many soft sensing methods have been proposed to address the challenges of multioperating conditions, time-varying behavior, and scarcity of labeled samples in complex manufacturing processes, most of these methods are based on the assumption of abundant labeled modeling samples." (p.2)
- to address (introduction): "To address the multioperating condition issue, a dual k-means operating condition identification method assisted by deep metric learning (DML) is proposed." (p.3)
- considering (introduction): "Considering the scarcity of labeled samples, this article proposes a high-confidence pseudolabel sample construction method based on JITL and genetic algorithms (GAs)." (p.3)

## Hedge verbs

- proposes / causal / abstract, introduction, conclusion: "This article proposes a semi-supervised quality soft sensing method"; "this article proposes a high-confidence pseudolabel sample construction method"; "It proposes a semi-supervised quality soft sensing method"
- is proposed / causal / abstract, introduction: "a dual k-means operating condition identification method assisted by deep metric learning (DML) is proposed"
- indicate / causal / experiments: "The data from Table IV indicates that, compared with solely employing JITL for pseudolabel construction, the pseudolabel construction method proposed in this article"
- will further consider / speculative / conclusion: "In the future, we will further consider the complex characteristics of multiple production steps and inherited process quality."

## Cross-section linkers

- introduction → preliminaries: "The remaining sections of this article are structured as follows. Section II will introduce the fundamental principles of several algorithms utilized in this article, such as JITL and DML. Section III provides a detailed exposition of the proposed soft sensing model construction method. In Section IV, the effectiveness of the proposed model is experimentally validated using a real production dataset of float glass. Section V will summarizes the work of this article." (p.3)
- method → experiments: GA 伪标签流程后 `IV. EXPERIMENTAL AND APPLICATION VALIDATION` (p.9)
- experiments → conclusion: 现场应用后 `V. CONCLUSION` (p.12)

## Candidate rules

- R002 Introduction 无独立 Related Work，全局建模 / 局部建模 / concept drift / 半监督评述写在引言中段，并以编号缺口列表收束。
- R003 Introduction 末用 `The remaining sections of this article are structured as follows` 指向 II–V。
- R004 贡献用 `The primary contributions of this article are as follows` + 编号列表。
- R005 Conclusion 先 `This article addresses` 收回问题与方法，再用 `In the future, we will further consider` 指向后续。

## Candidate phrases

- `This article proposes a semi-supervised` (abstract)
- `The primary contributions of this article are as follows.` (introduction)
- `The remaining sections of this article are structured as follows.` (introduction)
- `This article addresses the complexity of` (conclusion)
- `In the future, we will further consider` (conclusion)

## House style

自称 `this article` / `the proposed method` / `we will further consider`。未见 `Here we`、`In this paper`。`This article proposes` 与 `This article addresses` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: The accurate perception of key quality variables in complex manufacturing processes is a necessary prerequisite for achieving system optimization control and ensuring the safe and stable operation of the system.
- p.1 abstract: This article proposes a semi-supervised quality soft sensing method under multiple operating conditions for complex product manufacturing processes.
- p.1 abstract: Finally, the effectiveness of the proposed method is validated through a real manufacturing process, the float glass production process.
- p.1 introduction: IN THE complex manufacturing process, the realization of accurate and reliable online measurement of process quality is of great significance in promoting the digital and intelligent development of the manufacturing industry.
- p.1 introduction: However, these methods are essentially global modeling techniques, which need to ensure that the modeled data and the real-time data obey the same probability distribution.
- p.2 introduction: Although many soft sensing methods have been proposed to address the challenges of multioperating conditions, time-varying behavior, and scarcity of labeled samples in complex manufacturing processes, most of these methods are based on the assumption of abundant labeled modeling samples.
- p.3 introduction: The primary contributions of this article are as follows.
- p.3 introduction: To address the multioperating condition issue, a dual k-means operating condition identification method assisted by deep metric learning (DML) is proposed.
- p.3 introduction: The remaining sections of this article are structured as follows. Section II will introduce the fundamental principles of several algorithms utilized in this article, such as JITL and DML. Section III provides a detailed exposition of the proposed soft sensing model construction method. In Section IV, the effectiveness of the proposed model is experimentally validated using a real production dataset of float glass. Section V will summarizes the work of this article.
- p.4 method: This section will provide a detailed exposition of the soft sensing method proposed in this article, which primarily consists of three parts: 1) dual k-means operating condition identification method assisted by DML; 2) online selective prediction strategy based on the spatiotemporal information adaptive fusion; and 3) high-confidence pseudolabel sample construction method based on JITL and GA.
- p.9 experiments: To validate the effectiveness of the aforementioned soft sensing model construction method, this section conducts practical application verification using float glass manufacturing process data.
- p.12 conclusion: This article addresses the complexity of real industrial processes, including multioperating conditions, time-varying characteristics, and the scarcity of labeled samples.
- p.13 conclusion: These results validate the effectiveness of the proposed approach, and this model has now been deployed and is operational at the actual production site of Hebei Panel Glass Company Ltd.
- p.13 conclusion: In the future, we will further consider the complex characteristics of multiple production steps and inherited process quality.
