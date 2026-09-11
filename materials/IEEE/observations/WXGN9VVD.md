---
key: WXGN9VVD
title: "A fast optimized algorithm based on the NSGA — II for microwave windows"
venue: "2017 Eighteenth International Vacuum Electronics Conference (IVEC)"
doi: "10.1109/IVEC.2017.8289508"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-2"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. BASIC THEORY` → `III. SIMULATION RESULTS`。前置 `Abstract—` 与 `Keywords—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 pillbox 窗、传输线初设与 CST MW / HFSS 三维电磁优化）。无节序路标。无独立 Conclusion；结果段落后接 `ACKNOWLEDGEMENTS` 与 `REFERENCES`。Method 标题为 `BASIC THEORY`。Experiments 标题为 `SIMULATION RESULTS`（W 波段折叠波导行波管窗，MMT / CST / HFSS）。两页短文。

## Openers

- abstract: `Based on the` — "Based on the Mode-Matching Technique (MMT), a fast optimized method based on NSGA-II (Non-Dominated Sorting Genetic Algorithm) algorithm is proposed for design of waveguide windows." (p.1)
- introduction: `AS one sort` — "AS one sort of the most important high-frequency and high-power Vacuum Electronic Devices (VEDs), W-band folded waveguide Traveling-Wave Tubes (TWTs) have promising potential in high-resolution imaging applications [1]." (p.1；栏首掉字)
- method: `The transmission performance` — "The transmission performance of a passive device can be calculated by MMT." (p.1, II)
- experiments: `With the initial` — "With the initial ranges of L, d and dt, the optimization procedure combing MMT and NSGA-II is used to optimize the waveguide window." (p.2, III)
- conclusion: 无独立结论节。收束在结果段：`In the computational` — "In the computational case, however, this method converges rapidly generally in less than fifteen iterations." (p.2)

## Gap transitions

- unlike (abstract): "Unlike the conventional micro-genetic algorithm, we construct two different objective functions as optimal goals of NSGA-II and the values of the objective functions are evaluated fast and accurately by MMT." (p.1)
- in this paper (introduction): "In this paper, we combine the Mode Matching Technique (MMT) with the genetic algorithm to simulate, design, and optimize microwave windows." (p.1)
- however (experiments): "In the computational case, however, this method converges rapidly generally in less than fifteen iterations." (p.2)

## Hedge verbs

- propose / causal / abstract, method: "a fast optimized method based on NSGA-II ... is proposed"; "we proposed two objective functions"
- construct / causal / abstract: "we construct two different objective functions as optimal goals of NSGA-II"
- combine / causal / introduction: "we combine the Mode Matching Technique (MMT) with the genetic algorithm"
- show / causal / abstract, experiments: "the optimized results have shown excellent transmission performance"; "The results have shown excellent transmission performance"

## Cross-section linkers

- introduction → method: 无 `The rest of this paper is organized`。引言末 "This combination will allow us to design a microwave window fast and accurately." 后直接 `II. BASIC THEORY` (p.1)
- method → experiments: 算法步骤 1)–6) 与几何初设后直接 `III. SIMULATION RESULTS` (p.2)
- experiments → conclusion: 无独立结论；收敛句后接 `ACKNOWLEDGEMENTS` (p.2)

## Candidate rules

- R001 摘要贡献句用被动 `a fast optimized method ... is proposed`，并置 `Unlike the conventional`。
- R002 两页短会：无独立 Related Work、无节序路标、无 Conclusion。
- R006 引言用 `In this paper, we combine A with B to` 收束方法。
- R007 结果段用 `however` 把一般遗传算法收敛依赖改写为本文快速收敛。

## Candidate phrases

- `a fast optimized method based on NSGA-II ... is proposed for` (abstract)
- `Unlike the conventional micro-genetic algorithm, we construct` (abstract)
- `In this paper, we combine the Mode Matching Technique (MMT) with the genetic algorithm to` (introduction)
- `When combining the MMT and the NSGA-II algorithm, we proposed` (method)
- `The results have shown excellent transmission performance from` (experiments)

## House style

自称 `In this paper, we combine` / `we construct` / `we proposed`。未见 `Here we`。`In this paper` 与 `we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `This article`。

## Quotes

- p.1 abstract: Based on the Mode-Matching Technique (MMT), a fast optimized method based on NSGA-II (Non-Dominated Sorting Genetic Algorithm) algorithm is proposed for design of waveguide windows.
- p.1 abstract: Unlike the conventional micro-genetic algorithm, we construct two different objective functions as optimal goals of NSGA-II and the values of the objective functions are evaluated fast and accurately by MMT.
- p.1 abstract: For a waveguide window of W-Band folded waveguide Traveling-Wave Tube, the optimized results have shown excellent transmission performance from 83GHz to 103GHz with S11 less than -25dB, which is yielded with population size of 25 in less than fifteen iterations.
- p.1 introduction: AS one sort of the most important high-frequency and high-power Vacuum Electronic Devices (VEDs), W-band folded waveguide Traveling-Wave Tubes (TWTs) have promising potential in high-resolution imaging applications [1].
- p.1 introduction: In this paper, we combine the Mode Matching Technique (MMT) with the genetic algorithm to simulate, design, and optimize microwave windows.
- p.1 introduction: This combination will allow us to design a microwave window fast and accurately.
- p.1 method: The transmission performance of a passive device can be calculated by MMT.
- p.1 method: When combining the MMT and the NSGA-II algorithm, we proposed two objective functions
- p.1 method: The algorithm based on NSGA-II for optimizing waveguide windows of arbitrary geometry can be generalized as follows:
- p.2 experiments: With the initial ranges of L, d and dt, the optimization procedure combing MMT and NSGA-II is used to optimize the waveguide window.
- p.2 experiments: The results have shown excellent transmission performance from 83GHz to 103GHz with S11 less than -25dB.
- p.2 experiments: In the computational case, however, this method converges rapidly generally in less than fifteen iterations.
