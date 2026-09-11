---
key: 7QCRUAAB
title: "A Review on Soft Sensors for Monitoring, Control, and Optimization of Industrial Processes"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2020.3033153"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-4,10-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED REVIEW WORKS` → `III. PROCEDURES FOR SOFT SENSORS CONSTRUCTION` → `IV.`（问题与进展，引言路标）→ `V.`（工业应用，引言路标）→ `VI. OPEN CHALLENGES AND FUTURE DIRECTIONS` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED REVIEW WORKS`，评既有书与综述）。Introduction 含 `A. Terminology` 与 `B. Scope and Structure of This Article`，末以五个研究问题 + 节序路标指向 II–VI。无 Experiments 节；应用综述在 Section V，开放问题在 VI，收束在 `VII. CONCLUSION`。

## Openers

- abstract: `Over the past` — "Over the past twenty years, numerous research outcomes have been published, related to the design and implementation of soft sensors." (p.1)
- introduction: `IN INDUSTRIAL processes` — "IN INDUSTRIAL processes, sensing enables the Silicon-based monitoring and control systems to gain access to the internal information about the operating statuses, the state trajectories, and the external variations reflected by the environmental factors." (p.1；栏首掉字)
- related_work: `A few books` — "A few books and review/survey type of articles can be seen in literature that discuss soft sensors and the approaches to their design." (p.2, II)
- method: `One of the` — "One of the major efforts of this work lies in finding the answers to the question “How can soft sensors be used to help with monitoring, control and optimization of industrial processes?”" (p.3, III)
- applications: `Most of the` — "Most of the existing research activities have been conducted as performance evaluation of soft sensors in laboratory setups (based on simulations) or with limited amounts of experimental data acquired from real plants." (p.10, V.C)
- conclusion: `This review focuses` — "This review focuses on the key scientific problems in the design and implementation of soft sensors in the context of the modern industry." (p.11)

## Gap transitions

- however (abstract): "However, novel opportunities are accompanied by novel challenges." (p.1)
- while (abstract): "While a few books and review articles are published on the related topics, more focus on the most up-to-the-date advancement is put in this work, from the perspective of systems and control." (p.1)
- besides (introduction): "Besides, it is neither economic nor beneficial to install sensors beyond requirement, because calibration and maintenance will lead to unnecessary workload and cost." (p.1)
- however (related work): "However, there is no work that presents a comprehensive review of the progress over the past two decades (2000–2020) and an outlook for the coming decades or giving answers to the questions proposed in the previous section." (p.2)
- while (conclusion): "While these questions are discussed whenever relevant, they are addressed mainly in the corresponding sections as follows" (p.11)

## Hedge verbs

- aim / causal / abstract: "This work is motivated by these observations and aims to present a comprehensive review"
- present / causal / abstract, related work: "aims to present a comprehensive review"; "this article presents the current industrial practices"
- would like / causal / introduction: "In this article, we would like to mainly explore the answers to the following questions"
- can / speculative / introduction, challenges: "soft sensors can overcome the constraint"; "this can be optimized in the future"
- expected / speculative / conclusion: "it is expected to witness more novel ideas"

## Cross-section linkers

- introduction → related work: "This article is structured as follows. The next section introduces the related surveys and reviews. Section III elaborates the general procedures necessary for soft sensor construction. Section IV summarizes the common problems and advancement in the available solutions. Afterwards, Section V presents a summary of the state-of-the-art applications to the industry, and VI discusses the open challenges and the future directions." (p.2)
- related work → method: II 末 "the most classical and influential papers ... are cited whenever necessary" 随后 `III. PROCEDURES FOR SOFT SENSORS CONSTRUCTION` (p.3)
- applications → challenges: 部署案例后 `VI. OPEN CHALLENGES AND FUTURE DIRECTIONS` (p.11)
- challenges → conclusion: 深度学习挑战段落后 `VII. CONCLUSION` (p.11)

## Candidate rules

- R001 review 摘要自称 `This work`，gap 用 `While a few books and review articles` + `more focus ... is put in this work`。
- R002 有独立 `II. RELATED REVIEW WORKS`，专评既有书与综述的时间跨度与范围。
- R003 Introduction 用编号研究问题 `(Q1)`–`(Q5)`，再用 `This article is structured as follows` 指向各节。
- R004 开放问题节用项目符号（Improving / Filling the gap / Embedded / Exploiting）。
- R005 Conclusion 开篇 `This review focuses on`，并把 Q1–Q5 回指到对应章节。

## Candidate phrases

- `This work is motivated by these observations and aims to present a comprehensive review of` (abstract)
- `In this article, we would like to mainly explore the answers to the following questions` (introduction)
- `This article is structured as follows.` (introduction)
- `Based on the above discussions, this section summarizes the open challenges` (challenges)
- `This review focuses on the key scientific problems in` (conclusion)

## House style

自称是 `This work` / `this article` / `This review` / `we would like`。未见 `Here we`。未见 `In this paper`。`This work` 与 `This review` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Over the past twenty years, numerous research outcomes have been published, related to the design and implementation of soft sensors.
- p.1 abstract: However, novel opportunities are accompanied by novel challenges.
- p.1 abstract: This work is motivated by these observations and aims to present a comprehensive review of the developments since the start of the millennium.
- p.1 abstract: While a few books and review articles are published on the related topics, more focus on the most up-to-the-date advancement is put in this work, from the perspective of systems and control.
- p.1 introduction: IN INDUSTRIAL processes, sensing enables the Silicon-based monitoring and control systems to gain access to the internal information about the operating statuses, the state trajectories, and the external variations reflected by the environmental factors.
- p.1 introduction: Besides, it is neither economic nor beneficial to install sensors beyond requirement, because calibration and maintenance will lead to unnecessary workload and cost.
- p.2 introduction: In this article, we would like to mainly explore the answers to the following questions about soft sensors and soft sensing.
- p.2 introduction: This article is structured as follows. The next section introduces the related surveys and reviews. Section III elaborates the general procedures necessary for soft sensor construction. Section IV summarizes the common problems and advancement in the available solutions. Afterwards, Section V presents a summary of the state-of-the-art applications to the industry, and VI discusses the open challenges and the future directions.
- p.2 related_work: A few books and review/survey type of articles can be seen in literature that discuss soft sensors and the approaches to their design.
- p.2 related_work: However, there is no work that presents a comprehensive review of the progress over the past two decades (2000–2020) and an outlook for the coming decades or giving answers to the questions proposed in the previous section.
- p.3 method: One of the major efforts of this work lies in finding the answers to the question “How can soft sensors be used to help with monitoring, control and optimization of industrial processes?”
- p.10 applications: Most of the existing research activities have been conducted as performance evaluation of soft sensors in laboratory setups (based on simulations) or with limited amounts of experimental data acquired from real plants.
- p.11 challenges: Based on the above discussions, this section summarizes the open challenges to overcome and the future directions that are promising in the coming decade.
- p.11 conclusion: This review focuses on the key scientific problems in the design and implementation of soft sensors in the context of the modern industry.
- p.11 conclusion: In the coming decade and beyond, apart from the efforts to overcome the aforementioned challenges, it is expected to witness more novel ideas, more advanced techniques and broader platforms where soft sensing plays an indispensable role in the monitoring, control and optimization of the industrial processes, not to mention the use in Digital Twins.
