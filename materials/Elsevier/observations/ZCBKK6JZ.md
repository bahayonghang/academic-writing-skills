---
key: ZCBKK6JZ
title: "A multi-objective optimization method for industrial park layout design: The trade-off between economy and safety"
venue: "Chemical Engineering Science"
doi: "10.1016/j.ces.2021.116471"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-22"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Problem statement` → `3. Methodology` → `5` 案例（Case 1 / Case 2）→ `6` 算法比较与讨论 → `7. Conclusion`。前置 `highlights` / `article info` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段网格/连续布局、管网 FLUTE、QRA、单目标将安全折算为经济量、MO-MILP）。Introduction 末无编号贡献列表，有案例预告。Method 含目标函数、朝向、不重叠约束、扩展风险图。Experiments 为两案例 + NSGA-II/MOPSO/DMS 对照。

## Openers

- abstract: `The general layout` — "The general layout design significantly impacts the economy and safety performance of an industrial park."
- introduction: `The facility layout` — "The facility layout problem (FLP) is to determine the physical organization of a production system (Meller and Gau, 1996)."
- method: `This work aims` — "This work aims to provide designers with a set of solutions for layout that achieve different trade-offs between economy and safety."
- experiments: `The proposed layout` — "The proposed layout design method is implemented for this case, and NSGA-II is applied to solve the model."
- conclusion: `In this work,` — "In this work, a multi-objective optimization model is proposed for industrial park layout problems, in which a framework of the extended risk map method is developed and integrated."

## Gap transitions

- however (abstract): "However, this conversion is not appropriate."
- however (introduction): "However, non-overlapping constraints are usually difficult to deal with."
- therefore (introduction): "Therefore, safety should be treated as an independent objective, as important as the economy, and an excellent layout design method should provide the designer with a set of solutions and the flexibility to achieve different trade-offs between economy and safety."
- however (introduction): "However, very few works about industrial FLPs have applied multi-objective optimization."

## Hedge verbs

- is proposed / causal / abstract: "In this work, a multi-objective optimization method is proposed to obtain a set of solutions that achieves different trade-offs between economy and safety."
- show / associative / abstract: "The results show that the non-dominated sorting genetic algorithm II (NSGA-II) is more effective for industrial facility layout problems with multi-objective."
- is proposed / causal / conclusion: "In this work, a multi-objective optimization model is proposed for industrial park layout problems"
- seems / hedge / conclusion: "NSGA-II seems more effective for industrial facility layout problems."

## Cross-section linkers

- introduction → problem: 案例预告后 `2. Problem statement`
- problem → method: Given/Determine/Objectives 后 `3. Methodology`
- method → experiments: "The proposed method is compared with a method from literature ... in the first case" 后案例实施
- experiments → conclusion: 算法比较讨论后 `7. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R009 自称：`In this work, a multi-objective optimization method is proposed` / `This work aims to`

## Candidate phrases

- `In this work, a multi-objective optimization method is proposed to obtain a set of solutions that achieves different trade-offs between economy and safety` (abstract)
- `This work aims to provide designers with a set of solutions for layout that achieve different trade-offs between economy and safety` (method)
- `The results show that the non-dominated sorting genetic algorithm II (NSGA-II) is more effective` (abstract)
- `In this work, a multi-objective optimization model is proposed for industrial park layout problems` (conclusion)

## House style

自称 `In this work` / `is proposed` / `This work aims to`。被动与 `this work` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The general layout design significantly impacts the economy and safety performance of an industrial park.
- abstract: In most of the previous works, safety issues are converted to economic numbers in objective functions. However, this conversion is not appropriate.
- abstract: In this work, a multi-objective optimization method is proposed to obtain a set of solutions that achieves different trade-offs between economy and safety.
- abstract: The results show that the non-dominated sorting genetic algorithm II (NSGA-II) is more effective for industrial facility layout problems with multi-objective.
- introduction: The facility layout problem (FLP) is to determine the physical organization of a production system (Meller and Gau, 1996).
- introduction: Therefore, safety should be treated as an independent objective, as important as the economy, and an excellent layout design method should provide the designer with a set of solutions and the flexibility to achieve different trade-offs between economy and safety.
- introduction: However, very few works about industrial FLPs have applied multi-objective optimization.
- method: This work aims to provide designers with a set of solutions for layout that achieve different trade-offs between economy and safety.
- experiments: The proposed layout design method is implemented for this case, and NSGA-II is applied to solve the model.
- conclusion: In this work, a multi-objective optimization model is proposed for industrial park layout problems, in which a framework of the extended risk map method is developed and integrated.
- conclusion: The most significant advantage of the proposed layout model is the ability to provide designers with considerable freedom to achieve different trade-offs between economy and safety, while classical methods with single-objective models can provide only one solution, and designers lose their right to make a trade-off.
- conclusion: NSGA-II seems more effective for industrial facility layout problems.
