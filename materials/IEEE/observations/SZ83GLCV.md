---
key: SZ83GLCV
title: "Temperature Co-Optimization of Zinc Roasting Process Based on Fuzzy Synthetic Evaluation and Temperature Adjustable Margin"
venue: "IEEE Transactions on Fuzzy Systems"
doi: "10.1109/TFUZZ.2024.3354835"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROCESS DESCRIPTION` → `III. BRIEF REVIEW OF RELATED METHODS` → `IV. DECISION-MAKING SYSTEM FOR TEMPERATURE CO-OPTIMIZATION OF THE ZRP` → `V. EXPERIMENT RESULTS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work 等价节 `III. BRIEF REVIEW OF RELATED METHODS`（deterioration degree + FSE）。Introduction 仍内嵌 ZRP 温度优化 / OPE / 模糊规则抽取评述。Introduction 末有节序路标，指向 Section II–VI。Method 为 IV，含 Algorithm 1。Experiments 标题为 `EXPERIMENT RESULTS`（工业锌焙烧案例）。

## Openers

- abstract: `The roasting temperature` — "The roasting temperature is critical for enhancing product quality, reducing air pollution, and ensuring the long-term operation of the zinc roasting process." (p.1)
- introduction: `THE zinc roasting` — "THE zinc roasting process (ZRP) is the upstream process of zinc hydrometallurgy and the acid-making process, which converts the zinc concentrate to zinc calcine and sulfur dioxide flue gas [1]." (p.1；栏首掉字)
- related: `To assess the` — "To assess the degree of deterioration between the current and the optimal conditions for the KPIs, the concept of the deterioration degree is introduced [41]." (p.4, III.A)
- method: `The decision-making system` — "The decision-making system for temperature co-optimization of the ZRP is depicted in Fig. 2 and comprises three units: the operating performance evaluation unit, the process model unit, and the co-optimization unit." (p.5, IV)
- experiments: `To assess the` — "To assess the effectiveness of the proposed two-level decision-making system, a specific ZRP in China is selected for investigation [42]." (p.8, V)
- conclusion: `This article proposed` — "This article proposed a two-level decision-making system for the co-optimization of roasting temperature in the ZRP." (p.12)

## Gap transitions

- however (abstract): "However, optimizing the roasting temperature is challenging due to complex reaction mechanisms, feed composition fluctuations, and the coupling relationship with downstream processes." (p.1)
- however (introduction): "However, the evaluation results lacked physical meaning, providing limited guidance for the ZRP process optimization." (p.1)
- however (introduction): "However, these methods are steady-state optimization methods, mainly used for the process design of the ZRP. Therefore, they are not suitable for solving the dynamic optimization problems considered in this article." (p.1)
- although (introduction): "Although the abovementioned MSA methods have achieved good results in the OPE of some industrial processes, they have certain limitations in dealing with the multiscale data and the coexistence of qualitative and quantitative information." (p.2)
- therefore (introduction): "Therefore, it is more suitable for realizing the OPE of the complex industrial process." (p.2)
- however (introduction): "However, existing methods for optimizing the roasting temperature of the ZRP have certain limitations." (p.2)
- to address (introduction): "To address the above challenges, a decision-making framework for co-optimization of the zinc roasting temperature is proposed." (p.2)
- therefore (process): "Therefore, it is imperative to develop a decision-making system for co-optimization of the roasting temperature for two zinc roasters." (p.4)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "a two-level decision-making system for co-optimization of the roasting temperature is proposed"; "This article proposed a two-level decision-making system"
- introduce / causal / abstract, introduction: "the concept of a temperature-adjustable margin is introduced"; "A novel VWDD-FSE model is introduced"
- demonstrate / causal / abstract: "an industrial case study is presented to demonstrate the effectiveness of the proposed two-level decision-making system."
- show / causal / experiments: "Fig. 7 provides a more detailed analysis of the four optimization methods."; "It clearly shows that under co-optimization, the sulfur dioxide concentration remains below the unqualified threshold"
- can / speculative / conclusion: "the proposed approach could be extended to the industrial process, where several production processes share the same set of desulfurization and denitrification equipment."

## Cross-section linkers

- introduction → process: "The rest of this article is organized as follows. Section II details the ZRP and challenges in decision-making. Section III revisits the related methods. Section IV presents the proposed decision-making framework in detail. In Section V, experimental results are presented to illustrate the effectiveness of the proposed method. Finally, Section VI concludes this article." (p.3)
- related → method: III.B 模糊综合评价步骤结束后进入 `IV. DECISION-MAKING SYSTEM FOR TEMPERATURE CO-OPTIMIZATION OF THE ZRP` (p.5)
- method → experiments: 协同设定规则段落后直接 `V. EXPERIMENT RESULTS` (p.8)
- experiments → conclusion: 结果总括后直接 `VI. CONCLUSION` (p.12)

## Candidate rules

- R001 abstract 用 `In this article, a ... is proposed` 给出方法，再用 `Finally, an industrial case study is presented to demonstrate`。
- R002 有独立 `BRIEF REVIEW OF RELATED METHODS`，Introduction 仍评本领域方法并在段末用 `To address the above challenges` 转入贡献。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 贡献用 `The main contributions of this article are summarized as follows.` + 编号列表。
- R005 Conclusion 用过去时 `This article proposed`，末句 `could be extended` 指向后续工业场景。

## Candidate phrases

- `In this article, a ... is proposed.` (abstract)
- `To address the above challenges, a ... is proposed.` (introduction)
- `The main contributions of this article are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article proposed a ... for` (conclusion)

## House style

自称是 `this article` / `the proposed` / `we introduce`（SATAM 定义处）。未见 `Here we`。`In this article` 与 `This article proposed` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: The roasting temperature is critical for enhancing product quality, reducing air pollution, and ensuring the long-term operation of the zinc roasting process.
- p.1 abstract: However, optimizing the roasting temperature is challenging due to complex reaction mechanisms, feed composition fluctuations, and the coupling relationship with downstream processes.
- p.1 abstract: In this article, a two-level decision-making system for co-optimization of the roasting temperature is proposed.
- p.1 abstract: Finally, an industrial case study is presented to demonstrate the effectiveness of the proposed two-level decision-making system.
- p.1 introduction: THE zinc roasting process (ZRP) is the upstream process of zinc hydrometallurgy and the acid-making process, which converts the zinc concentrate to zinc calcine and sulfur dioxide flue gas [1].
- p.1 introduction: However, the evaluation results lacked physical meaning, providing limited guidance for the ZRP process optimization.
- p.1 introduction: However, these methods are steady-state optimization methods, mainly used for the process design of the ZRP. Therefore, they are not suitable for solving the dynamic optimization problems considered in this article.
- p.2 introduction: Although the abovementioned MSA methods have achieved good results in the OPE of some industrial processes, they have certain limitations in dealing with the multiscale data and the coexistence of qualitative and quantitative information.
- p.2 introduction: Therefore, it is more suitable for realizing the OPE of the complex industrial process.
- p.2 introduction: However, existing methods for optimizing the roasting temperature of the ZRP have certain limitations.
- p.2 introduction: To address the above challenges, a decision-making framework for co-optimization of the zinc roasting temperature is proposed.
- p.3 introduction: The main contributions of this article are summarized as follows.
- p.3 introduction: The rest of this article is organized as follows. Section II details the ZRP and challenges in decision-making. Section III revisits the related methods. Section IV presents the proposed decision-making framework in detail. In Section V, experimental results are presented to illustrate the effectiveness of the proposed method. Finally, Section VI concludes this article.
- p.4 process: Therefore, it is imperative to develop a decision-making system for co-optimization of the roasting temperature for two zinc roasters.
- p.4 related: To assess the degree of deterioration between the current and the optimal conditions for the KPIs, the concept of the deterioration degree is introduced [41].
- p.5 method: The decision-making system for temperature co-optimization of the ZRP is depicted in Fig. 2 and comprises three units: the operating performance evaluation unit, the process model unit, and the co-optimization unit.
- p.8 experiments: To assess the effectiveness of the proposed two-level decision-making system, a specific ZRP in China is selected for investigation [42].
- p.11 experiments: Based on the above experimental results, the two-level decision-making system proves to be the most effective approach for achieving optimal operating performance in the ZRP.
- p.12 conclusion: This article proposed a two-level decision-making system for the co-optimization of roasting temperature in the ZRP.
- p.12 conclusion: Besides, considering the current strict requirements for environmental protection, the proposed approach could be extended to the industrial process, where several production processes share the same set of desulfurization and denitrification equipment.
