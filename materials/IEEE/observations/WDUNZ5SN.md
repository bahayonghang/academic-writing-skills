---
key: WDUNZ5SN
title: "Data-Driven Multi-objective Optimization for Municipal Solid Waste Incineration Process"
venue: "2023 5th International Conference on Industrial Artificial Intelligence (IAI)"
doi: "10.1109/IAI59504.2023.10327611"
item_type: conferencePaper
has_pdf: true
status: complete
pages_read: "1-6"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION` → `III. MOPSO_TA-BASED OPERATIONAL OPTIMIZATION` → `IV. EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Keywords—`（非 Index Terms）。无独立 Related Work。`related_work=inlined`（Introduction 中段评 exergy / NSGAII / CFD / Aspen Plus，再转入 data-driven）。Introduction 末有节序路标，指向 Section II–V。Method 在 III（ARBFNN + MOPSO_TA + MADM）。Experiments 标题为 `EXPERIMENTAL STUDIES`。

## Openers

- abstract: `To comply with` — "To comply with the nitrogen oxide emission standards and growing demands for waste reduction, the operational optimization of municipal solid waste incineration (MSWI) process is considered as a multi-objective optimization problem." (p.1)
- introduction: `With the accelerated` — "With the accelerated urbanization process, the phenomenon of “garbage siege” has become more and more serious due to the dramatic increase of municipal solid waste (MSW) [1]." (p.1)
- method: `In this section` — "In this section, the scheme for optimizing the operation of MSWI process is designed with the establishment of the performance index models, multi-objective optimization of the performance indices and the decision-making of the optimal set-point." (p.3)
- experiments: `In this section` — "In this section, experiments, based on the actual operation data collected from an MSWI plant, are presented to verify the effectiveness of DDOOS." (p.5)
- conclusion: `In this paper` — "In this paper, a novel DDOOS was developed to obtain the environment-friendly and efficient operation of MSWI process." (p.6)

## Gap transitions

- however (introduction): "However, it is prone to poor incineration stability, low combustion efficiency and high pollutant emissions due to the complex composition of MSW." (p.1)
- although (introduction): "Although NOx emissions can be controlled by adjusting operating parameters such as primary air flow and secondary air flow, the combustion efficiency would be affected." (p.1)
- therefore (introduction): "Therefore, it would be reasonable to consider the above problem as a multi-objective optimization problem (MOP) from the operational optimization point of view." (p.1)
- however (introduction): "However, municipal solid waste incineration processes are characterized with strong nonlinearity and a large number of parameters, the above optimization methods based on mathematical models are difficult to guarantee the model accuracy, which in turn will affect the optimization results." (p.1)
- although / however (introduction): "Although the optimization method based on simulation models simplifies complex mechanisms, making operational optimization more feasible. However, it usually takes a long time for simulation verification during the optimization." (p.2)
- therefore (introduction): "Therefore, a data-driven optimization strategy (DDOOS) based on two-archive multi-objective particle swarm algorithm is developed to enhance the operational performance of MSWI process." (p.2)
- however (conclusion): "However, due to the fact that the operation conditions change frequently as the composition of the collected waste fluctuates, in our future study, a multi-objective optimization under multiple operation conditions will be designed for MSWI process." (p.6)

## Hedge verbs

- propose / causal / abstract, introduction, method: "the optimization strategy, based on a two-archive particle swarm algorithm, is proposed"; "a MOPSO algorithm based on two-archive mechanism is proposed"
- verify / causal / abstract, experiments: "the experiment results verify the validity and feasibility of the proposed optimization method"; "experiments ... are presented to verify the effectiveness of DDOOS"
- show / causal / introduction, experiments: "The experimental results show the maximum improvements of 13.4%, 10.3% and 14.8%"; "From Fig. 2, it can be seen that"
- develop / causal / introduction, conclusion: "a data-driven optimization strategy (DDOOS) ... is developed"; "a novel DDOOS was developed"

## Cross-section linkers

- introduction → method: "In this article, Section II describes the MSWI process, and defines the problem formulation. The proposed optimization operation method is detailed in Section III. The feasibility and effectivity of the developed methodology are verified with real industrial data in section IV. Finally, we conclude our work in Section V." (p.2)
- method → experiments: 决策式后接 `IV. EXPERIMENTAL STUDIES` (p.5)
- experiments → conclusion: Table I 后接 `V. CONCLUSION` (p.6)

## Candidate rules

- R001 摘要用被动 `the optimization strategy ... is proposed`，正文再用 `In this paper`。
- R002 Introduction 无独立 Related Work，机理 / 仿真 / 数据驱动评述写在引言中段。
- R003 Introduction 末用 `In this article, Section II describes` 指向 II–V。
- R004 贡献用编号句 `The novelties and advantages of the proposed method contain the following parts:`。
- R005 Conclusion 先收回 DDOOS，再用 `However, due to the fact that` + `in our future study`。

## Candidate phrases

- `In this paper, the optimization strategy, based on a two-archive particle swarm algorithm, is proposed to` (abstract)
- `Therefore, a data-driven optimization strategy (DDOOS) based on` (introduction)
- `In this article, Section II describes the MSWI process, and defines the problem formulation.` (introduction)
- `In this paper, a novel DDOOS was developed to obtain` (conclusion)
- `in our future study, a multi-objective optimization under multiple operation conditions will be designed` (conclusion)

## House style

自称是 `In this paper` / `In this article` / `we conclude our work` / `the proposed method` / `in our future study`。未见 `Here we`。`In this paper` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: To comply with the nitrogen oxide emission standards and growing demands for waste reduction, the operational optimization of municipal solid waste incineration (MSWI) process is considered as a multi-objective optimization problem.
- p.1 abstract: In this paper, the optimization strategy, based on a two-archive particle swarm algorithm, is proposed to improve the operation performance of MSWI process.
- p.1 abstract: Finally, the experiment results verify the validity and feasibility of the proposed optimization method based on the practical operation data.
- p.1 introduction: With the accelerated urbanization process, the phenomenon of “garbage siege” has become more and more serious due to the dramatic increase of municipal solid waste (MSW) [1].
- p.1 introduction: However, it is prone to poor incineration stability, low combustion efficiency and high pollutant emissions due to the complex composition of MSW.
- p.1 introduction: Although NOx emissions can be controlled by adjusting operating parameters such as primary air flow and secondary air flow, the combustion efficiency would be affected.
- p.1 introduction: Therefore, it would be reasonable to consider the above problem as a multi-objective optimization problem (MOP) from the operational optimization point of view.
- p.1 introduction: However, municipal solid waste incineration processes are characterized with strong nonlinearity and a large number of parameters, the above optimization methods based on mathematical models are difficult to guarantee the model accuracy, which in turn will affect the optimization results.
- p.2 introduction: Although the optimization method based on simulation models simplifies complex mechanisms, making operational optimization more feasible. However, it usually takes a long time for simulation verification during the optimization.
- p.2 introduction: Therefore, a data-driven optimization strategy (DDOOS) based on two-archive multi-objective particle swarm algorithm is developed to enhance the operational performance of MSWI process.
- p.2 introduction: In this article, Section II describes the MSWI process, and defines the problem formulation. The proposed optimization operation method is detailed in Section III. The feasibility and effectivity of the developed methodology are verified with real industrial data in section IV. Finally, we conclude our work in Section V.
- p.3 method: In this section, the scheme for optimizing the operation of MSWI process is designed with the establishment of the performance index models, multi-objective optimization of the performance indices and the decision-making of the optimal set-point.
- p.5 experiments: In this section, experiments, based on the actual operation data collected from an MSWI plant, are presented to verify the effectiveness of DDOOS.
- p.5 experiments: Compared with actual operation, the optimized CE is improved by 23.45% on average; the NOx emissions are reduced by 25.14% on average.
- p.6 conclusion: In this paper, a novel DDOOS was developed to obtain the environment-friendly and efficient operation of MSWI process.
- p.6 conclusion: According to the experimental results, it can be concluded that the proposed DDOOS can improve CE by 23.45% and reduce NOx emissions by 25.14% on average.
- p.6 conclusion: However, due to the fact that the operation conditions change frequently as the composition of the collected waste fluctuates, in our future study, a multi-objective optimization under multiple operation conditions will be designed for MSWI process.
