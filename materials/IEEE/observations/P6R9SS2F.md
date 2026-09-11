---
key: P6R9SS2F
title: "Deep Subdomain Learning Adaptation Network: A Sensor Fault-Tolerant Soft Sensor for Industrial Processes"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2022.3231849"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-5,10-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. DEEP SUBDOMAIN LEARNING ADAPTATION NETWORK` → `IV` 实验（TE / 真实过程 / MPD） → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（`RELATED WORKS`）。`related_work=independent`。Introduction 末贡献列表后直接进入 Related Works，无 `The rest of this article is organized`。Related Work 分 Sensor Faults / Domain Adaptation / Principle of Deep Domain Adaptation。Experiments 含 TE 基准与 MPD 真实故障场景。

## Openers

- abstract: `Sensor faults are` — "Sensor faults are non-negligible issues for soft sensor modeling." (p.1)
- introduction: `IN INDUSTRIAL processes, soft` — "IN INDUSTRIAL processes, soft sensors are essential for product quality monitoring and advanced process control (APC)." (p.1)
- method: `To address the sensor` — "To address the sensor fault problem in soft sensor modeling field, we propose a DSLAN to develop a sensor fault-tolerant soft sensor." (p.4, III.A)
- experiments: `The MPD is` — "The MPD is an important chemical intermediate, widely used in the manufacture of azo dyes, oxazine dyes, and reactive dyes." (p.10, 真实故障场景)
- conclusion: `Sensor faults are prevalent` — "Sensor faults are prevalent in actual industrial processes, which have become non-negligible issues for soft sensor modeling." (p.11)

## Gap transitions

- however (abstract): "However, existing deep learning-based soft sensors are fragile and sensitive when considering sensor faults." (p.1)
- to improve (abstract): "To improve the robustness against sensor faults, this article proposes a deep subdomain learning adaptation network (DSLAN) to develop a sensor fault-tolerant soft sensor, which is capable of handling both sensor degradation and sensor failure simultaneously." (p.1)
- however (introduction): "However, many physical sensors suffer from wear and degradation due to prolonged use in harsh temperature and pressure environments, where they are in close contact with chemical reagents and reactants." (p.1)
- there is no unified (introduction): "There is no unified framework in soft sensing field to deal with both sensor degradation and sensor failure, i.e., there is a lack of a sensor fault-tolerant soft sensor." (p.2)
- no research has yet (related work): "No research has yet explored domain adaptation in endowing soft sensors with full fault tolerance, which means the tolerance to both sensor degradation and sensor failure." (p.3)

## Hedge verbs

- propose / causal / abstract, introduction, method: "this article proposes a deep subdomain learning adaptation network (DSLAN)"; "we originally propose a deep subdomain learning adaptation network (DSLAN)"; "we propose a DSLAN"
- present / causal / abstract: "a new probabilistic local maximum mean discrepancy (PLMMD) is presented"
- verify / causal / abstract: "the Tennessee Eastman (TE) benchmark process and two real industrial processes are used to verify the effectiveness of the proposed method"
- aims / speculative / introduction: "Our work aims to improve the robustness of soft sensors against sensor faults"
- outperform / causal / conclusion: "DSLAN outperforms all comparison methods"

## Cross-section linkers

- introduction → related work: 贡献列表后直接 `II. RELATED WORKS`，无节序路标 (p.2)
- related work → method: LMMD 公式后 `III. DEEP SUBDOMAIN LEARNING ADAPTATION NETWORK` (p.4)
- method → experiments: 失效数据插补后进入 TE / 真实过程 / MPD (p.10)
- experiments → conclusion: MPD 结果后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 先 `However` 指出现有软测量脆弱，再 `this article proposes` + 缩写。
- R002 独立 Related Work 标题为 `RELATED WORKS`，再分故障模型、域适应、深度域适应原理。
- R004 贡献用 `the main contributions of this article are as follows.`；引言末无组织句。
- R010 无 `The rest of this article is organized`，贡献后直接 Related Works。
- R005 Conclusion 先重复 abstract 问题句，再 `this article proposes` 收回方法。

## Candidate phrases

- `To improve the robustness against sensor faults, this article proposes` (abstract)
- `there is a lack of a sensor fault-tolerant soft sensor` (introduction)
- `Inspired by fault-tolerant control [15] and transfer learning [16], we originally propose` (introduction)
- `Specifically, the main contributions of this article are as follows.` (introduction)
- `To address the sensor fault problem in soft sensor modeling field, we propose` (method)
- `With the fault tolerance ability, soft sensing technology will take a step toward practical applications.` (abstract, conclusion)

## House style

自称 `this article proposes` / `we originally propose` / `Our work aims` / `we propose` / `our proposed`。未见 `Here we`、`In this paper`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Sensor faults are non-negligible issues for soft sensor modeling.
- p.1 abstract: However, existing deep learning-based soft sensors are fragile and sensitive when considering sensor faults.
- p.1 abstract: To improve the robustness against sensor faults, this article proposes a deep subdomain learning adaptation network (DSLAN) to develop a sensor fault-tolerant soft sensor, which is capable of handling both sensor degradation and sensor failure simultaneously.
- p.1 abstract: Finally, the Tennessee Eastman (TE) benchmark process and two real industrial processes are used to verify the effectiveness of the proposed method.
- p.1 abstract: With the fault tolerance ability, soft sensing technology will take a step toward practical applications.
- p.1 introduction: IN INDUSTRIAL processes, soft sensors are essential for product quality monitoring and advanced process control (APC).
- p.1 introduction: However, many physical sensors suffer from wear and degradation due to prolonged use in harsh temperature and pressure environments, where they are in close contact with chemical reagents and reactants.
- p.2 introduction: There is no unified framework in soft sensing field to deal with both sensor degradation and sensor failure, i.e., there is a lack of a sensor fault-tolerant soft sensor.
- p.2 introduction: Inspired by fault-tolerant control [15] and transfer learning [16], we originally propose a deep subdomain learning adaptation network (DSLAN) to develop a sensor fault-tolerant soft sensor for multimode industrial processes.
- p.2 introduction: Specifically, the main contributions of this article are as follows.
- p.3 related work: No research has yet explored domain adaptation in endowing soft sensors with full fault tolerance, which means the tolerance to both sensor degradation and sensor failure.
- p.4 method: To address the sensor fault problem in soft sensor modeling field, we propose a DSLAN to develop a sensor fault-tolerant soft sensor.
- p.10 experiments: The MPD is an important chemical intermediate, widely used in the manufacture of azo dyes, oxazine dyes, and reactive dyes.
- p.10 experiments: To validate the effectiveness of the proposed sensor fault-tolerant soft sensor, the healthy period (1–340) is treated as the training set, and the degraded period (341–436) and the failed period (437–667) are treated as the testing sets.
- p.11 conclusion: Sensor faults are prevalent in actual industrial processes, which have become non-negligible issues for soft sensor modeling.
- p.11 conclusion: To improve the robustness against sensor faults, this article proposes a sensor fault-tolerant soft sensor based on DSLAN.
- p.11 conclusion: Experimental results on the TE benchmark process and two real industrial processes show that DSLAN outperforms all comparison methods, including typical deep domain adaptation methods and missing data treatment methods, which reveals its powerful sensor fault tolerance ability.
