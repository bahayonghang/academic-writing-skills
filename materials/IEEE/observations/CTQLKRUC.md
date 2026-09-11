---
key: CTQLKRUC
title: "A fast and elitist multiobjective genetic algorithm: NSGA-II"
venue: "IEEE Transactions on Evolutionary Computation"
doi: "10.1109/4235.996017"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-16"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. ELITIST MULTIOBJECTIVE EVOLUTIONARY ALGORITHMS` → `III. ELITIST NONDOMINATED SORTING GENETIC ALGORITHM` → `IV. SIMULATION RESULTS` → `V.`（参数交互 / epistasis）→ 约束扩展节 → `VII. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work：Section II 评 SPEA / PAES / Rudolph elitist GA。`related_work=independent`。Introduction 末有节序路标，指向 Section II–结论。Method 为 III。Experiments 为 IV（及后续约束测试）。

## Openers

- abstract: `Multiobjective evolutionary algorithms` — "Multiobjective evolutionary algorithms (EAs) that use nondominated sorting and sharing have been criticized mainly for their: 1) ( 3) computational complexity (where is the number of objectives and is the population size); 2) nonelitism approach; and 3) the need for specifying a sharing parameter." (p.1；公式符号在抽取中缺失)
- introduction: `THE PRESENCE of` — "THE PRESENCE of multiple objectives in a problem, in principle, gives rise to a set of optimal solutions (largely known as Pareto-optimal solutions), instead of a single optimal solution." (p.1；栏首掉字)
- method: `For the sake` — "For the sake of clarity, we first describe a naive and slow procedure of sorting a population into different nondomination levels." (p.3, III.A)
- experiments: `In this section` — "In this section, we first describe the test problems used to compare the performance of NSGA-II with PAES and SPEA." (p.5, IV)
- conclusion: `We have proposed` — "We have proposed a computationally fast and elitist MOEA based on a nondominated sorting approach." (p.14)

## Gap transitions

- instead (introduction): "THE PRESENCE of multiple objectives in a problem, in principle, gives rise to a set of optimal solutions (largely known as Pareto-optimal solutions), instead of a single optimal solution." (p.1)
- however (conclusion): "However, one problem, PAES, was able to converge closer to the true Pareto-optimal front." (p.14)
- although (conclusion): "Although this new definition can be used with any other MOEAs, the real-coded NSGA-II with this definition has been shown to solve four different problems much better than another recently-proposed constraint-handling approach." (p.15)

## Hedge verbs

- suggest / causal / abstract, introduction: "In this paper, we suggest a nondominated sorting-based multiobjective EA (MOEA), called nondominated sorting genetic algorithm II (NSGA-II)"; "In this paper, we suggest a simple constraint-handling strategy with NSGA-II"
- propose / causal / introduction, conclusion: "we address all of these issues and propose an improved version of NSGA, which we call NSGA-II."; "We have proposed a computationally fast and elitist MOEA"
- show / causal / abstract, introduction: "Simulation results on difficult test problems show that the proposed NSGA-II, in most problems, is able to find much better spread of solutions"; "this paper shows that highly epistatic problems may also cause difficulties to MOEAs."
- observe / causal / abstract: "much better performance of NSGA-II is observed."

## Cross-section linkers

- introduction → related work: "In the remainder of the paper, we briefly mention a number of existing elitist MOEAs in Section II. Thereafter, in Section III, we describe the proposed NSGA-II algorithm in details. Section IV presents simulation results of NSGA-II and compares them with two other elitist MOEAs (PAES and SPEA). In Section V, we highlight the issue of parameter interactions, a matter that is important in evolutionary computation research. The next section extends NSGA-II for handling constraints and compares the results with another recently proposed constraint-handling method. Finally, we outline the conclusions of this paper." (p.2)
- related work → method: SPEA / PAES / Rudolph 评述后接 `III. ELITIST NONDOMINATED SORTING GENETIC ALGORITHM` (p.3)
- experiments → conclusion: 约束测试段落后直接 `VII. CONCLUSION` (p.14)

## Candidate rules

- R001 abstract 先列三点批评，再用 `In this paper, we suggest` 给出 NSGA-II。
- R002 独立 Related Work 节标题为算法族综述（`ELITIST MULTIOBJECTIVE EVOLUTIONARY ALGORITHMS`），不是 `Related Work` 字面。
- R003 Introduction 末用 `In the remainder of the paper` 指向 II–结论。
- R004 Conclusion 用 `We have proposed` 收回方法，再用 `However` 承认单题上 PAES 更近前沿。
- R005 约束扩展用 `we modify the definition of dominance`，不把定义句写成 anti-AI。

## Candidate phrases

- `In this paper, we suggest` (abstract)
- `In this paper, we address all of these issues and propose` (introduction)
- `In the remainder of the paper, we briefly mention` (introduction)
- `Finally, we outline the conclusions of this paper.` (introduction)
- `We have proposed a computationally fast and elitist MOEA based on` (conclusion)

## House style

自称是 `In this paper, we suggest` / `we propose` / `the proposed NSGA-II` / `this paper shows` / `We have proposed`。未见 `Here we`。`In this paper, we suggest` 与 `We have proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Multiobjective evolutionary algorithms (EAs) that use nondominated sorting and sharing have been criticized mainly for their: 1) ( 3) computational complexity (where is the number of objectives and is the population size); 2) nonelitism approach; and 3) the need for specifying a sharing parameter.
- p.1 abstract: In this paper, we suggest a nondominated sorting-based multiobjective EA (MOEA), called nondominated sorting genetic algorithm II (NSGA-II), which alleviates all the above three difficulties.
- p.1 abstract: Simulation results on difficult test problems show that the proposed NSGA-II, in most problems, is able to find much better spread of solutions and better convergence near the true Pareto-optimal front compared to Pareto-archived evolution strategy and strength-Pareto EA—two other elitist MOEAs that pay special attention to creating a diverse Pareto-optimal front.
- p.1 introduction: THE PRESENCE of multiple objectives in a problem, in principle, gives rise to a set of optimal solutions (largely known as Pareto-optimal solutions), instead of a single optimal solution.
- p.1 introduction: In this paper, we address all of these issues and propose an improved version of NSGA, which we call NSGA-II.
- p.2 introduction: In this paper, we suggest a simple constraint-handling strategy with NSGA-II that suits well for any EA.
- p.2 introduction: In the remainder of the paper, we briefly mention a number of existing elitist MOEAs in Section II. Thereafter, in Section III, we describe the proposed NSGA-II algorithm in details. Section IV presents simulation results of NSGA-II and compares them with two other elitist MOEAs (PAES and SPEA). In Section V, we highlight the issue of parameter interactions, a matter that is important in evolutionary computation research. The next section extends NSGA-II for handling constraints and compares the results with another recently proposed constraint-handling method. Finally, we outline the conclusions of this paper.
- p.3 method: For the sake of clarity, we first describe a naive and slow procedure of sorting a population into different nondomination levels.
- p.5 experiments: In this section, we first describe the test problems used to compare the performance of NSGA-II with PAES and SPEA.
- p.14 conclusion: We have proposed a computationally fast and elitist MOEA based on a nondominated sorting approach.
- p.14 conclusion: However, one problem, PAES, was able to converge closer to the true Pareto-optimal front.
- p.15 conclusion: We have also proposed a simple extension to the definition of dominance for constrained multiobjective optimization.
- p.15 conclusion: Although this new definition can be used with any other MOEAs, the real-coded NSGA-II with this definition has been shown to solve four different problems much better than another recently-proposed constraint-handling approach.
- p.15 conclusion: With the properties of a fast nondominated sorting procedure, an elitist strategy, a parameterless approach and a simple yet efficient constraint-handling method, NSGA-II, should find increasing attention and applications in the near future.
