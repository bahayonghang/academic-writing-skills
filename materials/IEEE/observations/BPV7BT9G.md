---
key: BPV7BT9G
title: "Multidomain Graph Meta-Learning Network for Few-Shot Prediction in Industrial Processes"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3571082"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-17"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`，下设 `A. Meta-Learning` 与 `B. Spatial Relationship Modeling in Industry`）。`related_work=independent`。Introduction 中段给出两个 open issues 与三点改进，末无单独 `The rest of this article` 句；贡献列表后直接进入 Related Works。Method 在 III。Experiments 标题为 `CASE STUDIES`（四个高炉域）。

## Openers

- abstract: `In process industries` — "In process industries, the scarcity of data highlights the necessity of few-shot learning for accurate industrial predictions." (p.1)
- introduction: `IN PROCESS industries` — "IN PROCESS industries, accurately predicting quality variables is essential to ensure equipment safety and intelligent production." (p.1；栏首掉字)
- method: `The MDGML is` — "The MDGML is built upon a multidomain MAML framework, and the basic setup is illustrated in Fig. 1." (p.3, III.A)
- experiments: `Blast furnace ironmaking` — "Blast furnace ironmaking is a critical process in steel production and a cornerstone of industrial development." (p.8, IV.A)
- conclusion: `In this article` — "In this article, we propose a novel MDGML to address the few-shot problem with inconsistent data domains." (p.15)

## Gap transitions

- however (abstract): "Recently, model-agnostic meta-learning (MAML) has become an effective solution to this challenge. However, the existing MAML in industrial prediction still faces two key issues: 1) training tasks originate from multiple domains and 2) the intervariable coupling relationships are not fully exploited to their potential in cases with limited information." (p.1)
- therefore (abstract): "Therefore, we propose a multidomain graph meta-learning network (MDGML) to enable knowledge transfer and enhance information utilization through domain generalization and graph-based meta-learning." (p.1)
- however (introduction): "However, the industrial environment is typically harsh." (p.1)
- nevertheless (introduction): "Nevertheless, two open issues remain unresolved." (p.1)
- to tackle (introduction): "To tackle these problems, in this article, we propose a multidomain graph meta-learning network (MDGML) for few-shot prediction in industrial processes." (p.2)
- despite (related work): "Despite the success of these methods, they have not paid attention to the problem of learning tasks coming from diverse domains." (p.3)
- future work (conclusion): "Future work is planned to concentrate on the issue of continuous distribution drift in cases where domain boundaries are ambiguous." (p.15)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a multidomain graph meta-learning network (MDGML)"; "in this article, we propose a multidomain graph meta-learning network (MDGML)"; "In this article, we propose a novel MDGML"
- validate / causal / abstract: "the experimental results from four real-world blast furnace datasets validate the effectiveness of the proposed method"
- show / causal / experiments: "the prediction details of the methods are shown in Fig. 8"; "As shown in Table IX, the graph-based representation method used by MDGML takes the longest time"
- demonstrate / causal / experiments: "This demonstrates that adaptive inner optimization contributes to discovering more effective meta-parameters"

## Cross-section linkers

- introduction → related work: 贡献列表后直接 `II. RELATED WORKS`，无 `The rest of this article is organized as follows` (p.2–3)
- related work → method: Related Works 末句 "In particular, our proposed graph meta-learning framework comprehensively leverages the advantages of graph-based methods and few-shot learning." 随后 `III. METHODOLOGY` (p.3)
- method → experiments: Algorithm 1 与 meta-testing 段落后直接 `IV. CASE STUDIES` (p.8)
- experiments → conclusion: 灵敏度段落后直接 `V. CONCLUSION` (p.15)

## Candidate rules

- R001 abstract 缺口用 `However, the existing MAML ... still faces two key issues` + 编号，贡献用 `Therefore, we propose`。
- R002 独立 Related Work 分 meta-learning 与工业空间关系两小节，各节末用 `Despite` 收回缺口。
- R003 Introduction 给出 domain/sample/task 三点改进后接贡献列表；本文无 `The rest of this article is organized as follows`。
- R004 贡献用 `The contributions of this article are summarized as follows` + 编号列表。
- R005 Conclusion 用 `In this article, we propose` 收回方法，并按三点改进复述，再用 `Future work is planned to concentrate on` 指向后续。

## Candidate phrases

- `Therefore, we propose a multidomain graph meta-learning network (MDGML)` (abstract)
- `To tackle these problems, in this article, we propose` (introduction)
- `The contributions of this article are summarized as follows.` (introduction)
- `In this article, we propose a novel MDGML to address` (conclusion)
- `The effectiveness of the method is validated across four blast furnace domains` (conclusion)
- `Future work is planned to concentrate on the issue of continuous distribution drift` (conclusion)

## House style

自称是 `we propose` / `in this article, we propose` / `In this article, we propose` / `our proposed method`。未见 `Here we`。`In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In process industries, the scarcity of data highlights the necessity of few-shot learning for accurate industrial predictions.
- p.1 abstract: However, the existing MAML in industrial prediction still faces two key issues: 1) training tasks originate from multiple domains and 2) the intervariable coupling relationships are not fully exploited to their potential in cases with limited information.
- p.1 abstract: Therefore, we propose a multidomain graph meta-learning network (MDGML) to enable knowledge transfer and enhance information utilization through domain generalization and graph-based meta-learning.
- p.1 abstract: Finally, the experimental results from four real-world blast furnace datasets validate the effectiveness of the proposed method.
- p.1 introduction: IN PROCESS industries, accurately predicting quality variables is essential to ensure equipment safety and intelligent production.
- p.1 introduction: However, the industrial environment is typically harsh.
- p.1 introduction: Nevertheless, two open issues remain unresolved.
- p.2 introduction: To tackle these problems, in this article, we propose a multidomain graph meta-learning network (MDGML) for few-shot prediction in industrial processes.
- p.2 introduction: The contributions of this article are summarized as follows.
- p.3 related work: Despite the success of these methods, they have not paid attention to the problem of learning tasks coming from diverse domains.
- p.3 method: The MDGML is built upon a multidomain MAML framework, and the basic setup is illustrated in Fig. 1.
- p.8 experiments: Blast furnace ironmaking is a critical process in steel production and a cornerstone of industrial development.
- p.10 experiments: It can be concluded that, except for the cases where the MAE for predicting S content under domain 1 with ten-shot and the RMSE under domain 3 with five-shot are the second-best, MDGML achieves the best prediction performance in all other scenarios.
- p.15 conclusion: In this article, we propose a novel MDGML to address the few-shot problem with inconsistent data domains.
- p.15 conclusion: To overcome few-shot limitations, we introduce a meta-learning framework in our method.
- p.15 conclusion: The effectiveness of the method is validated across four blast furnace domains, and a detailed analysis is also carried out to further illustrate the working mechanism of each component.
- p.15 conclusion: Future work is planned to concentrate on the issue of continuous distribution drift in cases where domain boundaries are ambiguous.
