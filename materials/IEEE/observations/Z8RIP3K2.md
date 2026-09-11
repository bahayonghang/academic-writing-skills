---
key: Z8RIP3K2
title: "A Multitarget Online Fuzzy Stochastic Configuration Network for Industry Data Modeling"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2025.3577008"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. MULTITARGET ONLINE FUZZY STOCHASTIC CONFIGURATION NETWORK` → `IV.`（theoretical analysis：universal approximation / online convergence / complexity）→ `V. PERFORMANCE EVALUATION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 FNN / SCN / F-SCN / 在线 SCN / 多目标 SCN）。Introduction 末有编号贡献与节序路标，指向 Section II–VI。Method 标题为 `MULTITARGET ONLINE FUZZY STOCHASTIC CONFIGURATION NETWORK`。Experiments 标题为 `PERFORMANCE EVALUATION`（垃圾焚烧炉温 + 风机功率）。

## Openers

- abstract: `To address the` — "To address the challenge of multitarget parameters and nonstationary data streams in industrial data modeling, this article proposes a multitarget online fuzzy stochastic configuration network (MOF-SCN) modeling method." (p.2792)
- introduction: `WITH the development` — "WITH the development of technologies such as sensors, the industrial internet, and data storage, vast amounts of operational data are typically obtained in industrial processes." (p.2792)
- method: `To enhance the` — "To enhance the accurate modeling of nonstationary data in MIMO industrial processes, this article proposes a MOF-SCN for industrial data modeling." (p.2795, III)
- experiments: `To validate the` — "To validate the effectiveness of the MOF-SCN in industrial data modeling tasks, this section presents comparative experiments focused on two specific cases: furnace temperature modeling in municipal solid waste incineration processes and power prediction for wind turbines." (p.2799, V)
- conclusion: `To construct an` — "To construct an accurate and adaptive multitarget data model for industrial processes, this article proposes a MOF-SCN modeling method." (p.2802)

## Gap transitions

- however (introduction): "However, since artificial neural networks are often considered “black-box” models, although they exhibit good predictive performance, it is difficult to explain their internal mechanisms and decision-making processes." (p.2792)
- however (introduction): "However, since industrial processes often exhibit nonstationary characteristics, the accuracy and adaptability of neural network models built offline gradually degrade over time, leading to model mismatch issues [18]." (p.2792)
- therefore (introduction): "Therefore, it is necessary to optimize the model structure and parameters through real-time analysis of online industrial process data streams." (p.2793)
- although (introduction): "Although the aforementioned methods have shown good modeling performance in industrial data modeling for nonstationary processes, further research is needed on how to dynamically adjust the structure and parameters of the F-SCN." (p.2793)
- although (conclusion): "Although the experimental results demonstrate the effectiveness of the proposed method in industrial data modeling, there are some limitations that deserve attention." (p.2802)

## Hedge verbs

- propose / causal / abstract, introduction, method: "this article proposes a multitarget online fuzzy stochastic configuration network (MOF-SCN) modeling method"; "this article proposes a MOF-SCN for industrial data modeling"
- demonstrate / causal / abstract, experiments: "Comparative experiments on two real-world industrial datasets demonstrate that the proposed method significantly outperforms"
- indicate / causal / introduction: "Experimental results indicate that the MOF-SCN method demonstrates significant advantages"
- may / speculative / preliminaries: "which may result in a less compact model structure"
- remain / speculative / conclusion: "how to effectively reduce the computational complexity of the algorithm remains a topic worthy of further investigation"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II provides a detailed account of the implementation process and problem analysis for both the SCN and FSCN models. Section III focuses on the implementation of the MOF-SCN model. Section IV presents theoretical analysis for MOF-SCN. Section V is devoted to the experimental evaluations conducted. Finally, Section VI concludes this article." (p.2793)
- preliminaries → method: problem analysis 后接 `III. MULTITARGET ONLINE FUZZY STOCHASTIC CONFIGURATION NETWORK` (p.2795)
- method → experiments: 复杂度分析后接 `V. PERFORMANCE EVALUATION` (p.2799)
- experiments → conclusion: 计算代价讨论后直接 `VI. CONCLUSION` (p.2802)

## Candidate rules

- R001 abstract 用 `this article proposes`，不用 `Here we`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 贡献用 `The main contributions are summarized as follows.` + 编号列表。
- R004 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R005 Conclusion 先收回方法，再用 `Although` 承认局限，`future research will focus on` 指向后续。

## Candidate phrases

- `To address the challenge of ..., this article proposes` (abstract)
- `Based on the above analysis, this article proposes` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `To validate the effectiveness of the MOF-SCN in industrial data modeling tasks` (experiments)
- `To construct an accurate and adaptive multitarget data model for industrial processes, this article proposes` (conclusion)
- `Therefore, future research will focus on fast learning methods for large-scale data and improving model robustness.` (conclusion)

## House style

自称是 `this article proposes` / `this article` / `the proposed method`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。结论用现在时 `this article proposes`。

## Quotes

- p.2792 abstract: To address the challenge of multitarget parameters and nonstationary data streams in industrial data modeling, this article proposes a multitarget online fuzzy stochastic configuration network (MOF-SCN) modeling method.
- p.2792 abstract: Comparative experiments on two real-world industrial datasets demonstrate that the proposed method significantly outperforms in terms of adaptability and accuracy, thereby extending the applicability of F-SCN.
- p.2792 introduction: WITH the development of technologies such as sensors, the industrial internet, and data storage, vast amounts of operational data are typically obtained in industrial processes.
- p.2792–2793 introduction: However, since industrial processes often exhibit nonstationary characteristics, the accuracy and adaptability of neural network models built offline gradually degrade over time, leading to model mismatch issues [18].
- p.2793 introduction: Therefore, it is necessary to optimize the model structure and parameters through real-time analysis of online industrial process data streams.
- p.2793 introduction: Although the aforementioned methods have shown good modeling performance in industrial data modeling for nonstationary processes, further research is needed on how to dynamically adjust the structure and parameters of the F-SCN.
- p.2793 introduction: Based on the above analysis, this article proposes a multitarget online fuzzy SCN (MOF-SCN) method for industrial data modeling to comprehensively enhance the learning ability of F-SCN for multitarget parameters and nonstationary data in industrial processes.
- p.2793 introduction: The rest of this article is organized as follows. Section II provides a detailed account of the implementation process and problem analysis for both the SCN and FSCN models. Section III focuses on the implementation of the MOF-SCN model. Section IV presents theoretical analysis for MOF-SCN. Section V is devoted to the experimental evaluations conducted. Finally, Section VI concludes this article.
- p.2795 method: To enhance the accurate modeling of nonstationary data in MIMO industrial processes, this article proposes a MOF-SCN for industrial data modeling.
- p.2799 experiments: To validate the effectiveness of the MOF-SCN in industrial data modeling tasks, this section presents comparative experiments focused on two specific cases: furnace temperature modeling in municipal solid waste incineration processes and power prediction for wind turbines.
- p.2800 experiments: After implementing the online optimization strategy proposed in this article, the test aRMSE, aMAE, and aMAPE of MOF-SCN-III were reduced by 26.6%, 28.4%, and 25.3%, respectively, compared to OSCN.
- p.2802 conclusion: To construct an accurate and adaptive multitarget data model for industrial processes, this article proposes a MOF-SCN modeling method.
- p.2802 conclusion: The experimental results show that the proposed MOF-SCN outperforms existing randomized learning models in terms of model accuracy and generalization ability.
- p.2802 conclusion: Although the experimental results demonstrate the effectiveness of the proposed method in industrial data modeling, there are some limitations that deserve attention.
- p.2802 conclusion: Therefore, future research will focus on fast learning methods for large-scale data and improving model robustness.
