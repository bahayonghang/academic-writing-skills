---
key: 2Q5GWEE7
title: "Cooperative Dynamic Multiobjective Optimization With Multi-Time-Scale for MSWI Process"
venue: "IEEE Transactions on Industrial Electronics"
doi: "10.1109/TIE.2025.3563676"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → `IV. EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评机理仿真、单目标加权、静态多目标、规律性动态响应、废水处理多时间尺度）。II 为 Preliminaries（MSWI Process / CSO Algorithm）。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `IV. EXPERIMENTAL STUDIES`（北京真实焚烧厂现场 + 仿真对比）。

## Openers

- abstract: `Municipal solid waste` — "Municipal solid waste incineration (MSWI) process is a complex industrial process characterized by multiple subsystems, inherent nonlinearities, and stochastic and time-varying dynamic behaviors, posing significant challenges for operational optimization." (p.1)
- introduction: `THE municipal solid` — "THE municipal solid waste (MSW) has posed severe threat to public health, and the pollution of MSW is responsible for about 1 million people deaths and economic losses of about 360 billion dollar annually [1], [2]." (p.1；栏首掉字)
- method: `Based on the` — "Based on the above analysis, a cooperative dynamic optimization scheme is proposed for the MSWI process, as shown in Fig. 2." (p.4, III)
- experiments: `An industrial field` — "An industrial field implementation experiment is conducted in this section, deploying the proposed methodology in a real MSWI plant." (p.8, IV)
- conclusion: `In this article` — "In this article, a cooperative dynamic optimization scheme was proposed for the MSWI process." (p.11)

## Gap transitions

- however (introduction): "However, the inherent complexity and variability of MSW composition render the MSWI process highly nonstationary, manifesting in several operational challenges including fluctuating emissions of pollutants, suboptimal energy recovery efficiency, and high operating costs [4]." (p.1)
- consequently (introduction): "Consequently, it is of great significance to design the optimization scheme for the MSWI process to address the above issues and ensure the system operating at optimal set-points." (p.1)
- however (introduction): "However, the MSWI process is treated as a static system and fails to account for the dynamic nature of the MSWI process." (p.2)
- to the best of our knowledge (introduction): "To the best of our knowledge, there is currently no research on cooperative dynamic optimization with multi-time-scale for the MSWI process." (p.2)
- to address (introduction): "To address the aforementioned challenges, this article focuses on two critical technological demands in operational optimization for the MSWI process." (p.2)
- in contrast (preliminaries): "In contrast, data-driven modeling emerges as an effective alternative for dynamic modeling, circumventing computational calculations." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, method: "a two-layer multiobjective competitive swarm optimization algorithm ... is proposed"; "a cooperative dynamic optimization scheme is proposed"
- demonstrate / causal / abstract: "the simulation results further demonstrate that the proposed algorithm achieves superior performance"
- can (ability) / causal / introduction: "Swarm intelligence algorithms ... can be effectively integrated with dynamic response strategies"
- shown / causal / conclusion: "The proposed HDR-TMCSO algorithm shown outstanding convergence and diversity"
- may / speculative / introduction: "This underlying assumption of these methods, however, may not adequately address the complex and stochastic nature of environmental variations"

## Cross-section linkers

- introduction → preliminaries / method / experiments / conclusion: "The remainder of this article is organized as follows. Section II elaborates the preliminaries. The data-driven surrogate-assisted cooperative dynamic optimization scheme of the MSWI process, the dynamic response strategy, and the proposed TMCSO algorithm are introduced in detail in Section III. The experimental studies are conducted in Section IV, and the conclusions are drawn in Section V." (p.2)
- preliminaries → method: CSO 段落后直接 `III. METHODOLOGY` (p.4)
- method → experiments: Decision-Making Strategy 后直接 `IV. EXPERIMENTAL STUDIES` (p.8)
- experiments → conclusion: Parameter Setting 讨论后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `It is the first time to report an attempt toward` 声明空白，再用 First/Second/Moreover/Finally 四步展开。
- R002 Introduction 无独立 Related Work；用 `To the best of our knowledge, there is currently no research on` 收口空白。
- R003 贡献用 `The main contributions can be summarized as follows.` + 编号列表。
- R004 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R005 Conclusion 用 `In this article, ... was proposed`，再用编号 1)–4) 收回方案、模型、HDR、现场指标。

## Candidate phrases

- `It is the first time to report an attempt toward` (abstract)
- `To address the aforementioned challenges, this article focuses on` (introduction)
- `The main contributions can be summarized as follows.` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this article, a cooperative dynamic optimization scheme was proposed` (conclusion)

## House style

自称是 `this article` / `In this article` / `the proposed method` / `we` 少见。未见 `Here we`。`this article` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`（全文用 `article`）。

## Quotes

- p.1 abstract: Municipal solid waste incineration (MSWI) process is a complex industrial process characterized by multiple subsystems, inherent nonlinearities, and stochastic and time-varying dynamic behaviors, posing significant challenges for operational optimization.
- p.1 abstract: It is the first time to report an attempt toward tackling the operational optimization with multi-time-scale for the MSWI process.
- p.1 abstract: Finally, the proposed method is deployed and validated in a real MSWI plant, and the simulation results further demonstrate that the proposed algorithm achieves superior performance, specifically with the nitrogen oxides (NOx), SO2, and HCl emissions reduced by 12.72%, 22.81%, and 15.97%, respectively, the main steam flow and its stability improved by 5.25% and 59.62%, respectively, and the usages of urea solution and limestone slurry decreased by 17.23% and 11.74%, respectively.
- p.1 introduction: THE municipal solid waste (MSW) has posed severe threat to public health, and the pollution of MSW is responsible for about 1 million people deaths and economic losses of about 360 billion dollar annually [1], [2].
- p.1 introduction: However, the inherent complexity and variability of MSW composition render the MSWI process highly nonstationary, manifesting in several operational challenges including fluctuating emissions of pollutants, suboptimal energy recovery efficiency, and high operating costs [4].
- p.2 introduction: To the best of our knowledge, there is currently no research on cooperative dynamic optimization with multi-time-scale for the MSWI process.
- p.2 introduction: To address the aforementioned challenges, this article focuses on two critical technological demands in operational optimization for the MSWI process.
- p.2 introduction: The main contributions can be summarized as follows.
- p.2 introduction: The remainder of this article is organized as follows. Section II elaborates the preliminaries. The data-driven surrogate-assisted cooperative dynamic optimization scheme of the MSWI process, the dynamic response strategy, and the proposed TMCSO algorithm are introduced in detail in Section III. The experimental studies are conducted in Section IV, and the conclusions are drawn in Section V.
- p.4 method: Based on the above analysis, a cooperative dynamic optimization scheme is proposed for the MSWI process, as shown in Fig. 2.
- p.8 experiments: An industrial field implementation experiment is conducted in this section, deploying the proposed methodology in a real MSWI plant.
- p.11 conclusion: In this article, a cooperative dynamic optimization scheme was proposed for the MSWI process.
- p.11 conclusion: The HDR strategy performed brilliantly in handling the stochastic changes of optimization environment, and it greatly improved the EOR of complex DMOPs.
- p.11 conclusion: Specifically, the NOx, SO2, and HCl emissions were decreased by 12.72%, 22.81%, and 15.97%, respectively; the MSF was increased by 5.25%, and its stability was increased by 59.62%; and the usages of urea solution and limestone slurry were decreased by 17.23% and 11.74%, respectively.
