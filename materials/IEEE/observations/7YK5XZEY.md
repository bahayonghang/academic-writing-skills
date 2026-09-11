---
key: 7YK5XZEY
title: "Generative AI Empowering Parallel Manufacturing: Building a “6S” Collaborative Production Ecology for Manufacturing 5.0"
venue: "IEEE Transactions on Systems, Man, and Cybernetics: Systems"
doi: "10.1109/TSMC.2024.3349555"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "6522-6536"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PARALLEL MANUFACTURING AND INDUSTRY 5.0` → `IV`（关键技术；引言路标称 Section IV）→ 案例节（光学检测 / 人机交互 / 多机器人任务分配）→ `VI. CHALLENGES` → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work：`II. RELATED WORK`（A. From Manufacturing 4.0 to Manufacturing 5.0；B. GAI for Manufacturing）。`related_work=independent`。Introduction 末有节序路标，指向 Section II–VI（引言路标把结论写成 Section VI，正文实际为 VI Challenges + VII Conclusion）。Method 为 `III. PARALLEL MANUFACTURING AND INDUSTRY 5.0`。Experiments 为三则 case study（DAO-based AOI、LFM 人机交互、去中心化多机器人任务分配）。结论前单列挑战节。

## Openers

- abstract: `Since Manufacturing 4.0` — "Since Manufacturing 4.0 faces various challenges, including the risks of data leakage and privacy violation, the struggle to meet the growing demand for personalization, and the limitations in harnessing human creativity, it has become crucial to embark on a transformation toward Manufacturing 5.0." (p.6522)
- introduction: `THE ADVENT of` — "THE ADVENT of Industry 4.0 has significantly propelled the transformation of the manufacturing industry toward more agile and intelligent production modes (so-called Manufacturing 4.0) [1]." (p.6522；栏首掉字)
- related: `In this section` — "In this section, we first give a history of the development from manufacturing 4.0 to manufacturing 5.0 with parallel intelligence and CPSS." (p.6523, II)
- method: `This section comprehensively` — "This section comprehensively elucidates the basic framework and operational process of DeFACT, a parallel manufacturing framework for Industry 5.0, emphasizing the significant role of BFMs, SE, and blockchain in achieving trustworthy and efficient collaborative production both within and outside the enterprise." (p.6525, III)
- experiments: `We conduct a` — "We conduct a series of experiments involving n = 10 mobile robots x := (x1,..., xn) and m = 10 tasks T := (T1,..., Tm) to empirically validate the efficiency of decentralized task allocation and assess the impact of robots’ communication ranges d on task execution." (p.6531, 案例 C)
- challenges: `This article introduces` — "This article introduces the DeFACT framework as a solution to how to effectively leverage GAI to facilitate the realization of Manufacturing 5.0 with the characteristics of “6S.”" (p.6531, VI)
- conclusion: `In this article` — "In this article, DeFACT is proposed as a parallel manufacturing framework, aiming at building a collaborative manufacturing ecology with characteristics of decentralization, transparency, trustworthiness and efficiency." (p.6532)

## Gap transitions

- however (introduction): "However, centralized organizational structures not only constrain the speed of data storage and sharing, but also raise concerns about data ownership, privacy, confidentiality, security, and the potential for the emergence of data monopolies [2], [3], [4]." (p.6522)
- consequently (introduction): "Consequently, the progression toward Industry 5.0 [6], [7] within the manufacturing sector, i.e., Manufacturing 5.0, is imperative and indispensable." (p.6522)
- however (related): "However, CPS-based Manufacturing 4.0 fails to adequately investigate and address human-related social aspects." (p.6524)
- however (related): "However, there is a scarcity of research that offers a holistic solution to the realization of Manufacturing 5.0 with the integration of GAI." (p.6525)
- therefore (introduction): "Therefore, the main contributions of this article are as follows." (p.6523)
- therefore (conclusion): "Therefore, it is believed that DeFACT can achieve a “6S” collaborative production and facilitate the transition from Manufacturing 4.0 to Manufacturing 5.0, amidst the growing degree of networking and the surging demand for personalization." (p.6533)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a DeFACT framework"; "we propose a parallel manufacturing framework"; "DeFACT is proposed as a parallel manufacturing framework"
- demonstrate / causal / introduction: "The second case demonstrates that DeFACT can enable more natural human–machine interaction"
- validate / causal / abstract, introduction: "the effectiveness and efficiency of DeFACT are experimentally validated"; "The first case validates the ability of DeFACT"
- believe / speculative / conclusion: "it is believed that DeFACT can achieve a “6S” collaborative production"
- can / speculative / abstract, method: "It can organize, coordinate and schedule"; "it has the capability to switch between three modes"

## Cross-section linkers

- introduction → related: "The remainder of this article is organized as follows. Section II introduces the development history of Manufacturing 5.0 and GAI for manufacturing. Section III elaborates the basic framework and operational process of DeFACT for parallel manufacturing and Industry 5.0. Then, its key technologies are presented in Section IV. In Section V, we give some case studies and experimental results to validate its effectiveness. Finally, concluding remarks are provided in Section VI." (p.6523)
- related → method: GAI 制造段落后 `III. PARALLEL MANUFACTURING AND INDUSTRY 5.0` (p.6525)
- case studies → challenges: 任务分配段落后 `VI. CHALLENGES` (p.6531)
- challenges → conclusion: 基础模型能力段落后 `VII. CONCLUSION` (p.6532)

## Candidate rules

- R001 abstract 用 `To this end, we propose a DeFACT framework`；结论用 `In this article, DeFACT is proposed as`。
- R002 独立 `II. RELATED WORK`，子节 A 4.0→5.0 / B GAI for Manufacturing。
- R003 Introduction 末用 `The remainder of this article is organized as follows`；正文实际多出 `VI. CHALLENGES`，结论在 VII。
- R004 贡献用 `Therefore, the main contributions of this article are as follows.` + 编号 1)–3)，并嵌套 a)–c) 案例。
- R005 结论前单列挑战节，结论用 `it is believed that DeFACT can` 收束 6S。

## Candidate phrases

- `To this end, we propose a DeFACT framework` (abstract)
- `This article aims to build a “6S” collaborative production ecology` (introduction)
- `Therefore, the main contributions of this article are as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this article, DeFACT is proposed as a parallel manufacturing framework` (conclusion)

## House style

自称是 `we propose` / `this article` / `In this article` / `DeFACT`。未见 `Here we`。`we propose` 与 `this article aims` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.6522 abstract: Since Manufacturing 4.0 faces various challenges, including the risks of data leakage and privacy violation, the struggle to meet the growing demand for personalization, and the limitations in harnessing human creativity, it has become crucial to embark on a transformation toward Manufacturing 5.0.
- p.6522 abstract: To this end, we propose a DeFACT framework for parallel manufacturing and Manufacturing 5.0, which focuses on safe, efficient and personalized collaborative production.
- p.6522 abstract: Finally, the effectiveness and efficiency of DeFACT are experimentally validated through the design and implementation of three case studies.
- p.6522 introduction: THE ADVENT of Industry 4.0 has significantly propelled the transformation of the manufacturing industry toward more agile and intelligent production modes (so-called Manufacturing 4.0) [1].
- p.6522 introduction: However, centralized organizational structures not only constrain the speed of data storage and sharing, but also raise concerns about data ownership, privacy, confidentiality, security, and the potential for the emergence of data monopolies [2], [3], [4].
- p.6523 introduction: This article aims to build a “6S” collaborative production ecology for Manufacturing 5.0 in the context of the burgeoning rise of GAI: safe in physical spaces, secure in cyberspaces, sustainable in natural ecology, sensitive in individual privacy and rights, service for all, and smartness of all.
- p.6523 introduction: Therefore, the main contributions of this article are as follows.
- p.6523 introduction: The remainder of this article is organized as follows. Section II introduces the development history of Manufacturing 5.0 and GAI for manufacturing. Section III elaborates the basic framework and operational process of DeFACT for parallel manufacturing and Industry 5.0. Then, its key technologies are presented in Section IV. In Section V, we give some case studies and experimental results to validate its effectiveness. Finally, concluding remarks are provided in Section VI.
- p.6523 related: In this section, we first give a history of the development from manufacturing 4.0 to manufacturing 5.0 with parallel intelligence and CPSS.
- p.6524 related: However, CPS-based Manufacturing 4.0 fails to adequately investigate and address human-related social aspects.
- p.6525 related: However, there is a scarcity of research that offers a holistic solution to the realization of Manufacturing 5.0 with the integration of GAI.
- p.6525 method: This section comprehensively elucidates the basic framework and operational process of DeFACT, a parallel manufacturing framework for Industry 5.0, emphasizing the significant role of BFMs, SE, and blockchain in achieving trustworthy and efficient collaborative production both within and outside the enterprise.
- p.6531 experiments: We conduct a series of experiments involving n = 10 mobile robots x := (x1,..., xn) and m = 10 tasks T := (T1,..., Tm) to empirically validate the efficiency of decentralized task allocation and assess the impact of robots’ communication ranges d on task execution.
- p.6531 challenges: This article introduces the DeFACT framework as a solution to how to effectively leverage GAI to facilitate the realization of Manufacturing 5.0 with the characteristics of “6S.”
- p.6532 conclusion: In this article, DeFACT is proposed as a parallel manufacturing framework, aiming at building a collaborative manufacturing ecology with characteristics of decentralization, transparency, trustworthiness and efficiency.
- p.6533 conclusion: Therefore, it is believed that DeFACT can achieve a “6S” collaborative production and facilitate the transition from Manufacturing 4.0 to Manufacturing 5.0, amidst the growing degree of networking and the surging demand for personalization.
