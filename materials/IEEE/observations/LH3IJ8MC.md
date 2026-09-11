---
key: LH3IJ8MC
title: "Modeling task relationships in multivariate soft sensor with balanced mixture-of-experts"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3202909"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-9"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED METHOD` → `IV. EXPERIMENTS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR/PLS/SVR/ELM、AE/CNN/RNN、硬/软参数共享 MTL 与 seesaw）。Section II 为 MTL/MoE 预备。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `EXPERIMENTS`（硫回收装置 SRU）。

## Openers

- abstract: `Accurate estimation of` — "Accurate estimation of multiple quality variables is critical for building industrial soft sensor models, which have long been confronted with data efficiency and negative transfer issues." (p.6556)
- introduction: `PROCESS industry plays` — "PROCESS industry plays an important role in modern industry and is closely related to key industrial manufacturing such as oil, gas, rare metals, iron, and steel, which forms an integral part of modern human life and national economies." (p.6556)
- method: `Given a size-M` — "Given a size-M set of observed history process variables [x1, x2, . . ., xM] ∈ RM×F , and the corresponding labels corresponding to size-N task [yn1 , yn2 , . . ., ynM] ∈ RM×N ." (p.6558, III.A)
- experiments: `In this section` — "In this section, experiments are conducted to evaluate performance of proposed method and answer the following research topics." (p.6560)
- conclusion: `A novel MTL` — "A novel MTL model combined with MMoE structure and GradNorm algorithm as a dynamic modeling approach in the soft sensor field called BMoE was developed in this article, which can predict multiple variables that are hard to be directly measured in the actual industrial process with good accuracy." (p.6562)

## Gap transitions

- however (abstract): "Methods sharing backbone parameters among tasks address the data efficiency issue; however, they still fail to mitigate the negative transfer problem." (p.6556)
- to address (abstract): "To address this issue, a balanced mixture-of-experts (BMoE) is proposed in this work" (p.6556)
- however (introduction): "However, in process engineering, there are many difficult-to-measure variables that are critical to evaluate process quality." (p.6556)
- however (introduction): "This strategy does enhance data efficiency; however, the task relationship is not depicted, suffering from the risk of negative transfer between conflicting tasks." (p.6557)
- as such (introduction): "As such, both lack of task relationship and the seesaw problem introduce negative transfer, thus, hindering the performance of multitask learning (MTL) models." (p.6557)

## Hedge verbs

- propose / causal / abstract, introduction: "a balanced mixture-of-experts (BMoE) is proposed in this work"; "A BMoE model is proposed to address the negative transfer in MVSS"
- demonstrate / causal / abstract: "Experiments on the typical sulfur recovery unit demonstrate that BMoE models task relationship"
- show / causal / experiments: "The results show that the complexity of our proposed model is concentrated on the back propagation process"
- can / speculative / conclusion: "such models can further improve the efficiency of joint representation learning"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section II presents preliminaries on MoE structure and the GradNorm algorithm. Section III proposes the novel BMoE approach. Section IV shows experiments on famous case studies, the sulfur recovery unit. Finally, Section V concludes the article." (p.6557)
- method → experiments: Algorithm 1 后 `IV. EXPERIMENTS` (p.6560)
- experiments → conclusion: 运行时间后 `V. CONCLUSION` (p.6562)

## Candidate rules

- R007 摘要用 `To address this issue, a ... is proposed in this work`。
- R002 Introduction 无独立 Related Work，MTL/负迁移评述写在引言中段。
- R004 贡献列表：`The contributions of this article are summarized as follows.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法，再用 `As for future work` 指向后续 MTL 与时序模块。

## Candidate phrases

- `To address this issue, a balanced mixture-of-experts (BMoE) is proposed in this work` (abstract)
- `The contributions of this article are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `As for future work` (conclusion)

## House style

自称 `is proposed in this work` / `this article` / `was developed in this article` / `our proposed model`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.6556 abstract: Accurate estimation of multiple quality variables is critical for building industrial soft sensor models, which have long been confronted with data efficiency and negative transfer issues.
- p.6556 abstract: Methods sharing backbone parameters among tasks address the data efficiency issue; however, they still fail to mitigate the negative transfer problem.
- p.6556 abstract: To address this issue, a balanced mixture-of-experts (BMoE) is proposed in this work, which consists of a multigate mixture-of-experts module and a task gradient balancing (TGB) module.
- p.6556 abstract: Experiments on the typical sulfur recovery unit demonstrate that BMoE models task relationship and balances the training process effectively, and achieves better performance than baseline models significantly.
- p.6556 introduction: PROCESS industry plays an important role in modern industry and is closely related to key industrial manufacturing such as oil, gas, rare metals, iron, and steel, which forms an integral part of modern human life and national economies.
- p.6556 introduction: However, in process engineering, there are many difficult-to-measure variables that are critical to evaluate process quality.
- p.6557 introduction: This strategy does enhance data efficiency; however, the task relationship is not depicted, suffering from the risk of negative transfer between conflicting tasks.
- p.6557 introduction: As such, both lack of task relationship and the seesaw problem introduce negative transfer, thus, hindering the performance of multitask learning (MTL) models.
- p.6557 introduction: The contributions of this article are summarized as follows.
- p.6557 introduction: The rest of this article is organized as follows. Section II presents preliminaries on MoE structure and the GradNorm algorithm. Section III proposes the novel BMoE approach. Section IV shows experiments on famous case studies, the sulfur recovery unit. Finally, Section V concludes the article.
- p.6558 method: Given a size-M set of observed history process variables [x1, x2, . . ., xM] ∈ RM×F , and the corresponding labels corresponding to size-N task [yn1 , yn2 , . . ., ynM] ∈ RM×N .
- p.6560 experiments: In this section, experiments are conducted to evaluate performance of proposed method and answer the following research topics.
- p.6561 experiments: In Table II, the proposed BMoE achieves significant improvement compared with different baselines.
- p.6562 experiments: According to Fig. 9, as the H2S prediction task is conducted similarly, with GradNorm block, the SO2 prediction task performs much better, the R2 score of which raises from 0.8286 to 0.8665, which means that the seesaw phenomenon between multitasks has been overcome by the GradNorm block.
- p.6562 conclusion: A novel MTL model combined with MMoE structure and GradNorm algorithm as a dynamic modeling approach in the soft sensor field called BMoE was developed in this article, which can predict multiple variables that are hard to be directly measured in the actual industrial process with good accuracy.
- p.6563 conclusion: As for future work, more MTL methods like subnetwork routing [29], PLS [21], and their reasonable application to the soft sensor field is still worth exploring, such models can further improve the efficiency of joint representation learning while helping solve negative transfer problem.
