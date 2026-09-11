---
key: VX5SHCQ3
title: "An online parameter identification and real-time optimization platform for thermal systems and its application"
venue: "Applied Energy"
doi: "10.1016/j.apenergy.2021.118199"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,10-13"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Modeling and simulation method of the cogeneration system` → `3` OPIRTOP 平台 → `4` 数据预处理与参数辨识 → `5. Operation optimization of the cogeneration system` → `6. Conclusion`。前置 `ARTICLE INFO` / `Keywords` / `ABSTRACT`。无独立 Related Work。`related_work=inlined`（Introduction 中段评热电联产简化建模、设计优化与热流法）。Introduction 末有编号贡献 + 节序路标。Method 在第 2 节系统描述与热流模型。Experiments 为 `5.2` 三工况与 `5.3` 现场在线优化。

## Openers

- abstract: `Real-time performance optimization` — "Real-time performance optimization of thermal systems is crucial for energy conservation but also challenging because of the high system complexity and time sensitivity."
- introduction: `Improving the utilization` — "Improving the utilization efficiency of thermal energy is an important yet difficult issue in modern society [1]."
- method: `The cogeneration system` — "The cogeneration system investigated in this work is located in Dongguan, Guangdong province of China." (s.2.1)
- experiments: `The cogeneration system` — "The cogeneration system is first optimized using the developed optimization platform under three typical conditions." (s.5.2)
- conclusion: `In this work,` — "In this work, a complex cogeneration system is first modeled using the heat current method, and an efficient simulation procedure is also proposed based on the H&C algorithm."

## Gap transitions

- however (introduction): "However, practical cogeneration systems are becoming more and more integrated and complex to utilize the thermal energy more effectively [4]."
- although (introduction): "Although the simplifications adopted in current studies enable the efficient analysis of complicated cogeneration systems, they would also introduce inaccuracies and even non-physical errors [18]."
- therefore (introduction): "Therefore, the reliability of such analyses is quite questionable."
- besides (introduction): "Besides, current system optimization studies mainly focus on the design optimization of cogeneration systems, while the system operation optimization with fixed design parameters are few."
- in summary (introduction): "In summary, the real-time operation optimization of cogeneration systems with the accurate system modeling is strongly required for their reliable performance evaluation and improvement."

## Hedge verbs

- develop / causal / abstract, introduction: "an online parameter identification and real-time optimization platform for thermal systems is developed"; "This work develops an online parameter identification and real-time optimization platform"
- propose / causal / abstract, method: "a high-efficiency simulation procedure is proposed using the hierarchical and categorized (H&C) algorithm"
- show / causal / abstract, experiments: "Field test results show that the standard coal consumption of the cogeneration system could be reduced by 0.415 g/kWh"
- demonstrate / causal / introduction: "Mu et al. [22] demonstrated a real-time optimization and controlling strategy of a chilled water plant with parallel chillers."

## Cross-section linkers

- introduction → method: "The remainder of this paper is organized as follows. The cogeneration system is first introduced and modeled using the heat current method in Section 2. An efficient simulation procedure is also proposed for the system based on the H&C algorithm. In Section 3, the OPIRTOP is proposed and developed on the basis of the cogeneration system. Section 4 introduces the data pre-processing and parameter identification technologies adopted in the platform. The cogeneration system is finally optimized employing the platform in Section 5. Field test results are presented to show the capability of the platform."
- method → experiments: 参数辨识后 `5. Operation optimization of the cogeneration system`
- experiments → conclusion: 现场试验结果后 `6. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The remainder of this paper is organized as follows`
- R004 贡献列表：`Specific contributions of this work cover three major aspects:`
- R009 自称：`This work develops` / `In this work` / `Herein`

## Candidate phrases

- `Herein, an online parameter identification and real-time optimization platform for thermal systems is developed` (abstract)
- `This work develops an online parameter identification and real-time optimization platform` (introduction)
- `Specific contributions of this work cover three major aspects:` (introduction)
- `The remainder of this paper is organized as follows.` (introduction)
- `In this work, a complex cogeneration system is first modeled` (conclusion)

## House style

自称 `Herein` / `This work develops` / `In this work` / `the proposed OPIRTOP`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Real-time performance optimization of thermal systems is crucial for energy conservation but also challenging because of the high system complexity and time sensitivity.
- abstract: Herein, an online parameter identification and real-time optimization platform for thermal systems is developed, and a gas-steam combined cycle cogeneration system is used to demonstrate its capability.
- abstract: Field test results show that the standard coal consumption of the cogeneration system could be reduced by 0.415 g/kWh by using the platform, which proves its practicability.
- introduction: Improving the utilization efficiency of thermal energy is an important yet difficult issue in modern society [1].
- introduction: Although the simplifications adopted in current studies enable the efficient analysis of complicated cogeneration systems, they would also introduce inaccuracies and even non-physical errors [18].
- introduction: Therefore, the reliability of such analyses is quite questionable.
- introduction: In summary, the real-time operation optimization of cogeneration systems with the accurate system modeling is strongly required for their reliable performance evaluation and improvement.
- introduction: This work develops an online parameter identification and real-time optimization platform for the real-time operation optimization of thermodynamic systems.
- introduction: Specific contributions of this work cover three major aspects: (1) model a complex cogeneration system with full consideration of physical processes for precision, and proposes a high-efficiency and accurate simulation procedure; (2) build the OPIRTOP for the cogeneration system combining the physical model, genetic algorithm, and machine learning technologies; (3) realize the real-time optimization for the cogeneration system, and verified the platform in the field test.
- introduction: The remainder of this paper is organized as follows. The cogeneration system is first introduced and modeled using the heat current method in Section 2.
- method: The cogeneration system investigated in this work is located in Dongguan, Guangdong province of China.
- experiments: The cogeneration system is first optimized using the developed optimization platform under three typical conditions.
- experiments: Finally, the standard coal consumption is decreased by 0.415 g/kWh.
- conclusion: In this work, a complex cogeneration system is first modeled using the heat current method, and an efficient simulation procedure is also proposed based on the H&C algorithm.
- conclusion: In summary, the developed OPIRTOP is capable of the real-time optimization and operation control for the cogeneration system investigated.
