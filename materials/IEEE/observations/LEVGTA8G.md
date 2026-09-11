---
key: LEVGTA8G
title: "MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition"
venue: "IEEE Transactions on Evolutionary Computation"
doi: "10.1109/TEVC.2007.892759"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-20"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. DECOMPOSITION OF MULTIOBJECTIVE OPTIMIZATION` → `III. THE FRAMEWORK OF MULTIOBJECTIVE EVOLUTIONARY ALGORITHM BASED ON DECOMPOSITION (MOEA/D)` → `IV. COMPARISON WITH MOGLS` → `V.`（与 NSGA-II 比较，Introduction 预告）→ `VI.`（更多实验）→ `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 VEGA / PAES / SPEA-II / NSGA-II / TPLS / MOGLS）。Introduction 末有节序路标，指向 Section II–VII。Method 为 II–III。Experiments 为 IV–VI。

## Openers

- abstract: `Decomposition is a` — "Decomposition is a basic strategy in traditional multiobjective optimization." (p.1)
- introduction: `A multiobjective optimization` — "A multiobjective optimization problem (MOP) can be stated as follows:" (p.1)
- method: `Multiobjective evolutionary algorithm` — "Multiobjective evolutionary algorithm based on decomposition (MOEA/D), the algorithm proposed in this paper, needs to decompose the MOP under consideration." (p.4, III.A)
- experiments: `In the following` — "In the following, we first introduce MOGLS and then analyze the complexity of MOGLS and MOEA/D." (p.5, IV)
- conclusion: `Decomposition was widely` — "Decomposition was widely used in traditional mathematical programming methods for solving MOPs." (p.19)

## Gap transitions

- however (abstract): "However, it has not yet been widely used in multiobjective evolutionary optimization." (p.1)
- therefore (introduction): "Therefore, many multiobjective optimization algorithms are to find a manageable number of Pareto optimal vectors which are evenly distributed along the PF, and thus good representatives of the entire PF [1]–[4]." (p.1)
- however (method): "However, not every Pareto optimal vector can be obtained by this approach in the case of nonconcave PFs." (p.3)
- in-contrast (conclusion): "In contrast, most MOEAs treat a MOP as a whole and mainly rely on domination for measuring the solution quality during their search." (p.19)

## Hedge verbs

- propose / causal / abstract, introduction: "This paper proposes a multiobjective evolutionary algorithm based on decomposition (MOEA/D)."; "In this paper, we propose a new multiobjective evolutionary algorithm based on decomposition (MOEA/D)."
- demonstrate / causal / abstract: "Experimental results have demonstrated that MOEA/D with simple decomposition methods outperforms or performs similarly to MOGLS and NSGA-II"
- show / causal / abstract, conclusion: "It has been shown that MOEA/D using objective normalization can deal with disparately-scaled objectives"; "Our analysis has shown that MOEA/D has lower computational complexity"
- outperform / causal / introduction, conclusion: "Overall, MOEA/D outperforms, in terms of solution quality, MOGLS on 0–1 multiobjective knapsack test instances"

## Cross-section linkers

- introduction → method: "This paper is organized as follows. Section II introduces three decomposition approaches for MOPs. Section III presents MOEA/D. Sections IV and V compare MOEA/D with MOGLS and NSGA-II and show that MOEA/D outperforms or performs similarly to MOGLS and NSGA-II. Section VI presents more experimental studies on MOEA/D. Section VII concludes this paper." (p.2)
- method → experiments: 变体讨论后接 `IV. COMPARISON WITH MOGLS` (p.5)
- experiments → conclusion: 可扩展性 / 邻域敏感性段落后直接 `VII. CONCLUSION` (p.19)

## Candidate rules

- R001 abstract 用 `However, it has not yet been widely used` 作缺口，再接 `This paper proposes`。
- R002 Introduction 无独立 Related Work，MOEA 评述写在引言中段，特征用项目符号列出。
- R003 Introduction 末用 `This paper is organized as follows` 指向 II–VII，收句为 `Section VII concludes this paper.`
- R004 Conclusion 先对照传统分解与非分解 MOEA，再用 `This paper has proposed` 收回方法。
- R005 复杂度主张写在 Introduction 特征列表与 Conclusion，不把 big-O 句写成 anti-AI。

## Candidate phrases

- `This paper proposes a multiobjective evolutionary algorithm based on` (abstract)
- `In this paper, we propose a new` (introduction)
- `This paper is organized as follows.` (introduction)
- `Section VII concludes this paper.` (introduction)
- `This paper has proposed a simple and generic` (conclusion)

## House style

自称是 `This paper proposes` / `In this paper, we propose` / `the algorithm proposed in this paper` / `this paper` / `We have shown`。未见 `Here we`。`This paper proposes` 与 `In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见单独的 `In this paper` 开摘要。

## Quotes

- p.1 abstract: Decomposition is a basic strategy in traditional multiobjective optimization.
- p.1 abstract: However, it has not yet been widely used in multiobjective evolutionary optimization.
- p.1 abstract: This paper proposes a multiobjective evolutionary algorithm based on decomposition (MOEA/D).
- p.1 abstract: Experimental results have demonstrated that MOEA/D with simple decomposition methods outperforms or performs similarly to MOGLS and NSGA-II on multiobjective 0–1 knapsack problems and continuous multiobjective optimization problems.
- p.1 introduction: A multiobjective optimization problem (MOP) can be stated as follows:
- p.1 introduction: Therefore, many multiobjective optimization algorithms are to find a manageable number of Pareto optimal vectors which are evenly distributed along the PF, and thus good representatives of the entire PF [1]–[4].
- p.2 introduction: In this paper, we propose a new multiobjective evolutionary algorithm based on decomposition (MOEA/D).
- p.2 introduction: This paper is organized as follows. Section II introduces three decomposition approaches for MOPs. Section III presents MOEA/D. Sections IV and V compare MOEA/D with MOGLS and NSGA-II and show that MOEA/D outperforms or performs similarly to MOGLS and NSGA-II. Section VI presents more experimental studies on MOEA/D. Section VII concludes this paper.
- p.3 method: However, not every Pareto optimal vector can be obtained by this approach in the case of nonconcave PFs.
- p.4 method: Multiobjective evolutionary algorithm based on decomposition (MOEA/D), the algorithm proposed in this paper, needs to decompose the MOP under consideration.
- p.5 experiments: In the following, we first introduce MOGLS and then analyze the complexity of MOGLS and MOEA/D.
- p.19 conclusion: Decomposition was widely used in traditional mathematical programming methods for solving MOPs.
- p.19 conclusion: In contrast, most MOEAs treat a MOP as a whole and mainly rely on domination for measuring the solution quality during their search.
- p.19 conclusion: This paper has proposed a simple and generic evolutionary multiobjective optimization algorithm based on decomposition, called MOEA/D.
