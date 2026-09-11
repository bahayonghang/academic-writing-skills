---
key: E7J6K8VW
title: "Data Mode Related Interpretable Transformer Network for Predictive Modeling and Key Sample Analysis in Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3227731"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. DATA MODE RELATED INTERPRETABLE TRANSFORMER` → `IV. INDUSTRIAL APPLICATIONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SAE/LSTM/CNN、JITL 多模态、可解释性三路、LogTrans/Informer/mvts-transformer）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `INDUSTRIAL APPLICATIONS`（脱丁烷塔 + 加氢裂化）。

## Openers

- abstract: `Accurate prediction of` — "Accurate prediction of quality variables that are difficult to measure is crucial for industrial process control and optimization." (p.9325)
- introduction: `UNDER the background` — "UNDER the background of carbon peaking and carbon neutrality, industrial processes urgently seek intellectual transformation and upgrading, with real-time monitoring, control, and optimization of processes being among the most important tasks [1], [2]." (p.9325)
- method: `In industrial processes` — "In industrial processes, the data belonging to the same mode have a high correlation." (p.9328, III.A)
- experiments: `In this section` — "In this section, the proposed DMRI-Former network is experimentally simulated in the industrial debutanizer column process and hydrocracking process." (p.9330)
- conclusion: `For the problems` — "For the problems of the industrial process prediction field, a novel DMRI-Former model was proposed for predictive modeling and key sample analysis in this article." (p.9335)

## Gap transitions

- however (abstract): "However, the fluctuations in raw material quality and production conditions may cause industrial process data to be distributed in multiple working conditions." (p.9325)
- to address (abstract): "To address these issues, this article proposes a novel data mode related interpretable transformer network (DMRI-Former) for predictive modeling and key sample analysis in industrial processes." (p.9325)
- however (introduction): "However, there are still three key problems to be solved in the application of data-driven methods in the actual industrial process." (p.9325)
- although (introduction): "Although the existing methods have some research on multimode processes, most of them focus on process monitoring, and the research on multimode soft sensor modeling is limited." (p.9326)
- nevertheless (introduction): "Nevertheless, the methods based on just-in-time face the problems of difficulty in extracting the process dynamic evolution patterns and the frequent updating of modes." (p.9326)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a novel data mode related interpretable transformer network"; "a novel DMRI-Former model was proposed"
- show / causal / experiments: "It can be seen from the experimental results in Table III that the prediction results of PCR are poor."
- verify / causal / abstract: "the superiority of the proposed DMRI-Former is verified in two real-world industrial processes"
- believe / speculative / conclusion: "we believe that the proposed DMRI-Former method has certain generalization and general applicability"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. In Section II, the self-attention mechanism and the original transformer model are briefly introduced. Then, the details of the proposed DMRI-Former model are discussed in Section III. Next, in Section IV, the proposed model is applied to two industrial processes for validation. Finally, Section V concludes this article." (p.9326)
- method → experiments: 软测量框架后 `IV. INDUSTRIAL APPLICATIONS` (p.9330)
- experiments → conclusion: 消融实验后 `V. CONCLUSION` (p.9335)

## Candidate rules

- R009 摘要用 `this article proposes` 点名 DMRI-Former。
- R002 Introduction 无独立 Related Work，多模态/可解释/Transformer 评述写在引言中段。
- R004 贡献列表：`The main contributions of this article are given as follows.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法，再用 `In future research work, we plan to` 指向现场与在线自适应。

## Candidate phrases

- `To address these issues, this article proposes` (abstract)
- `The main contributions of this article are given as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In future research work, we plan to` (conclusion)

## House style

自称 `this article proposes` / `this article` / `the proposed DMRI-Former` / `we plan`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.9325 abstract: Accurate prediction of quality variables that are difficult to measure is crucial for industrial process control and optimization.
- p.9325 abstract: However, the fluctuations in raw material quality and production conditions may cause industrial process data to be distributed in multiple working conditions.
- p.9325 abstract: To address these issues, this article proposes a novel data mode related interpretable transformer network (DMRI-Former) for predictive modeling and key sample analysis in industrial processes.
- p.9325 abstract: Finally, the superiority of the proposed DMRI-Former is verified in two real-world industrial processes compared to other state-of-the-art methods.
- p.9325 introduction: UNDER the background of carbon peaking and carbon neutrality, industrial processes urgently seek intellectual transformation and upgrading, with real-time monitoring, control, and optimization of processes being among the most important tasks [1], [2].
- p.9325 introduction: However, there are still three key problems to be solved in the application of data-driven methods in the actual industrial process.
- p.9326 introduction: Although the existing methods have some research on multimode processes, most of them focus on process monitoring, and the research on multimode soft sensor modeling is limited.
- p.9326 introduction: Nevertheless, the methods based on just-in-time face the problems of difficulty in extracting the process dynamic evolution patterns and the frequent updating of modes.
- p.9326 introduction: To solve the problems of multimode distribution characteristics, poor interpretable ability, and difficult feature extraction of dynamic ultra-long range in the industrial process prediction field mentioned above, this article proposes a novel data mode related interpretable transformer network (DMRI-Former) for predictive modeling and key sample analysis in industrial processes.
- p.9326 introduction: The main contributions of this article are given as follows.
- p.9326 introduction: The rest of this article is organized as follows. In Section II, the self-attention mechanism and the original transformer model are briefly introduced. Then, the details of the proposed DMRI-Former model are discussed in Section III. Next, in Section IV, the proposed model is applied to two industrial processes for validation. Finally, Section V concludes this article.
- p.9328 method: In industrial processes, the data belonging to the same mode have a high correlation.
- p.9330 experiments: In this section, the proposed DMRI-Former network is experimentally simulated in the industrial debutanizer column process and hydrocracking process.
- p.9331 experiments: From all experimental results and analysis, the proposed DMRI-Former has the best prediction performance among all methods.
- p.9335 conclusion: For the problems of the industrial process prediction field, a novel DMRI-Former model was proposed for predictive modeling and key sample analysis in this article.
- p.9335 conclusion: Compared with the other advanced methods, the experimental results in the two different industrial process datasets showed that the proposed DMRI-Former method could achieve the best prediction performance.
- p.9335 conclusion: In future research work, we plan to utilize the proposed method to perform prediction tasks on real industrial sites and provide guidance to field workers.
