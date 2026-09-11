---
key: UTR4ASSW
title: "Multispatial-Scale Optimal Control With Multisource Information for Nitrification in Wastewater Treatment Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3552706"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION AND PRELIMINARIES` → `III. MULTISPATIAL-SCALE OPTIMAL CONTROL WITH MULTISOURCE INFORMATION` → `IV. EXPERIMENTAL STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评数学规划最优控制 / 启发式多目标控制 / 知识–数据驱动控制）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `EXPERIMENTAL STUDIES`。

## Openers

- abstract: `The drastic fluctuations` — "The drastic fluctuations of influent pollutant load are inevitable in wastewater treatment process, which makes it difficult for nitrification to regulate dissolved oxygen concentrations with minimal effort to ensure the effluent quality." (p.4990)
- introduction: `NITRIFICATION, making use` — "NITRIFICATION, making use of aerobic microorganisms, is developed to promote the decomposition of organic matter to alleviate water pollution in wastewater treatment process (WWTP) [1]." (p.4990；栏首掉字)
- method: `To achieve optimum` — "To achieve optimum operation of different aerobic areas in nitrification, MSI-MSSOC is used to satisfy the demands of EQ and AE." (p.4992)
- experiments: `With the aim` — "With the aim of ensuring the effectiveness of MSI-MSSOC, the comparison experiments with dynamic multiobjective particle swarm optimization-based optimal control method (DMOPSO-OC) [13], DMOPSO-OC with MSSOM, and NSGAII-based optimal control method (NSGAII-OC) [29] are tested in nitrification based on the simulation platform BSM1." (p.4995)
- conclusion: `In this article` — "In this article, MSI-MSSOC was developed to ensure EQ within minimal energy consumption in case of the drastic fluctuation in pollutant load." (p.4998)

## Gap transitions

- to solve (abstract): "To solve this problem, a multispatial-scale optimal control with multisource information (MSI-MSSOC) is developed in this article." (p.4990)
- however (introduction): "However, with the increase in the volume of wastewater discharge, it is difficult for optimal control to obtain optimal solutions of dissolved oxygen concentration (SO) to meet the growing demand for EQ and AE [4], [5]." (p.4990)
- however (introduction): "However, in practical applications, it is tough to guarantee the quality of process data, which results in an adverse effect on the performance [19], [20]." (p.4991)
- therefore (introduction): "Therefore, for nitrification, how to exploit the process information to regulate SO in different aerobic areas for enhancing EQ and reducing AE is a substantial challenge." (p.4991)
- inspired by (introduction): "Inspired by the above analysis, a multispatial-scale optimal control with multisource information (MSI-MSSOC) is proposed in this article." (p.4991)

## Hedge verbs

- develop / causal / abstract, conclusion: "a multispatial-scale optimal control with multisource information (MSI-MSSOC) is developed in this article"; "MSI-MSSOC was developed"
- propose / causal / introduction: "a multispatial-scale optimal control with multisource information (MSI-MSSOC) is proposed in this article"
- demonstrate / causal / abstract: "The experimental results demonstrate that MSI-MSSOC can achieve the desirable operation performance of nitrification."
- show / causal / experiments, conclusion: "The experimental results showed that MSI-MSSOC could realize the improvement of operation performance in case of a drastic fluctuation in pollutant load."
- indicate / associative / experiments: "The above results indicate that MSI-MSSOC can ensure EQ with minimal effort in case of a drastic fluctuation in pollutant load."

## Cross-section linkers

- introduction → problem: "The remainder of this article is organized as follows: Section II presents the problem formulation. The details of MSI- MSSOC are described in Section III, consisting of the design of MSSOM, AKAS, and KOA. Section IV describes the experimental setup, simulation experimental results, and discussion of MSI-MSSOC. Section V concludes the article." (p.4991)
- method → experiments: 跟踪控制策略后 `IV. EXPERIMENTAL STUDIES` (p.4995)
- experiments → conclusion: 局限段落后直接 `V. CONCLUSION` (p.4998)

## Candidate rules

- R001 摘要缺口后用 `To solve this problem, a ... is developed in this article`。
- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The major contributions of MSI-MSSOC are given as follows` + 编号列表。
- R005 结论用 `Future studies will focus on` 指向后续。

## Candidate phrases

- `To solve this problem, a multispatial-scale optimal control with multisource information (MSI-MSSOC) is developed in this article` (abstract)
- `Inspired by the above analysis, a multispatial-scale optimal control with multisource information (MSI-MSSOC) is proposed in this article` (introduction)
- `The major contributions of MSI-MSSOC are given as follows.` (introduction)
- `The remainder of this article is organized as follows:` (introduction)
- `In this article, MSI-MSSOC was developed` (conclusion)
- `Future studies will focus on` (conclusion)

## House style

自称是 `is developed in this article` / `is proposed in this article` / `In this article`。未见 `Here we`、`In this paper`。`developed in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.4990 abstract: The drastic fluctuations of influent pollutant load are inevitable in wastewater treatment process, which makes it difficult for nitrification to regulate dissolved oxygen concentrations with minimal effort to ensure the effluent quality.
- p.4990 abstract: To solve this problem, a multispatial-scale optimal control with multisource information (MSI-MSSOC) is developed in this article.
- p.4990 abstract: The experimental results demonstrate that MSI-MSSOC can achieve the desirable operation performance of nitrification.
- p.4990 introduction: NITRIFICATION, making use of aerobic microorganisms, is developed to promote the decomposition of organic matter to alleviate water pollution in wastewater treatment process (WWTP) [1].
- p.4990 introduction: However, with the increase in the volume of wastewater discharge, it is difficult for optimal control to obtain optimal solutions of dissolved oxygen concentration (SO) to meet the growing demand for EQ and AE [4], [5].
- p.4991 introduction: However, in practical applications, it is tough to guarantee the quality of process data, which results in an adverse effect on the performance [19], [20].
- p.4991 introduction: Therefore, for nitrification, how to exploit the process information to regulate SO in different aerobic areas for enhancing EQ and reducing AE is a substantial challenge.
- p.4991 introduction: Inspired by the above analysis, a multispatial-scale optimal control with multisource information (MSI-MSSOC) is proposed in this article.
- p.4991 introduction: The major contributions of MSI-MSSOC are given as follows.
- p.4991 introduction: The remainder of this article is organized as follows: Section II presents the problem formulation. The details of MSI- MSSOC are described in Section III, consisting of the design of MSSOM, AKAS, and KOA. Section IV describes the experimental setup, simulation experimental results, and discussion of MSI-MSSOC. Section V concludes the article.
- p.4992 method: To achieve optimum operation of different aerobic areas in nitrification, MSI-MSSOC is used to satisfy the demands of EQ and AE.
- p.4995 experiments: With the aim of ensuring the effectiveness of MSI-MSSOC, the comparison experiments with dynamic multiobjective particle swarm optimization-based optimal control method (DMOPSO-OC) [13], DMOPSO-OC with MSSOM, and NSGAII-based optimal control method (NSGAII-OC) [29] are tested in nitrification based on the simulation platform BSM1.
- p.4997 experiments: The above results indicate that MSI-MSSOC can ensure EQ with minimal effort in case of a drastic fluctuation in pollutant load.
- p.4998 conclusion: In this article, MSI-MSSOC was developed to ensure EQ within minimal energy consumption in case of the drastic fluctuation in pollutant load.
- p.4998 conclusion: The experimental results showed that MSI-MSSOC could realize the improvement of operation performance in case of a drastic fluctuation in pollutant load.
- p.4998 conclusion: In this article, it can be concluded that MSI-MSSOC can provide a promising perspective for solving the problems of industrial processes with multispatial-scale property.
- p.4998 conclusion: Future studies will focus on an improved MSI-MSSOC for nitrification and denitrification in WWTP.
