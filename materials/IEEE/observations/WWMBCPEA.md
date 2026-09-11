---
key: WWMBCPEA
title: "Release Power of Mechanism and Data Fusion: A Hierarchical Strategy for Enhanced MIQ-Related Modeling and Fault Detection in BFIP"
venue: "IEEE/CAA Journal of Automatica Sinica"
doi: "10.1109/JAS.2024.124821"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-19"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. Introduction` → `II. Preliminaries and Problem Formulation` → `III. Methodology of MDCDS` → `IV. BFIP Experiment and Analysis` → `V. Conclusion and Prospect`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 LS-SVR/GNN/RVFLN/KPLS/IKOPLS 与机理建模）。Introduction 编号贡献后有节序路标，指向 II–V。Experiments 标题为 `BFIP Experiment and Analysis`。

## Openers

- abstract: `Data-driven techniques` — "Data-driven techniques are reshaping blast furnace iron-making process (BFIP) modeling, but their “black-box” nature often obscures interpretability and accuracy." (p.1)
- introduction: `CHINA stands unrivaled` — "CHINA stands unrivaled as the world's foremost producer and consumer of steel, commanding a prominent role in the global steel sector." (p.1；栏首掉字)
- method: `Due to the complexity` — "Due to the complexity within the BFIP, we vertically divide the huge blast furnace into zones during the mechanism modeling." (p.4, III.A)
- experiments: `In this section,` — "In this section, the effectiveness of MDCDS modeling and fault detection is fully demonstrated using data from a real BFIP at Liuzhou Iron and Steel Co. Ltd. in Guangxi, China." (p.10, IV)
- conclusion: `This study addresses` — "This study addresses the limitations of data-driven models in BFIP by proposing a hierarchical MDCDS." (p.16)

## Gap transitions

- to-overcome (abstract): "To overcome these limitations, our mechanism and data co-driven strategy (MDCDS) enhances model transparency and molten iron quality (MIQ) prediction." (p.1)
- however (introduction): "However, although China leads in steel production, it has not attained a commensurate standing in the global iron and steel industry and struggles to source high-quality iron ore at affordable prices." (p.1)
- therefore (introduction): "Therefore, it is crucial to establish effective monitoring systems capable of promptly detecting and addressing relevant faults, guaranteeing the smooth and safe operation of BFIP." (p.2)
- however (introduction): "However, most of these approaches have focused solely on single MIQ parameters, ignoring the consideration of multiple parameters simultaneously." (p.2)
- despite (introduction): "Despite the progress that has been made, there are still some challenges that remain to be addressed:" (p.2)
- however (conclusion): "However, our approach cannot cover the time-varying characteristic of the process nor guarantee the robustness of the model, which further promotes our future research as follows." (p.16)

## Hedge verbs

- enhances / causal / abstract: "our mechanism and data co-driven strategy (MDCDS) enhances model transparency"
- demonstrates / causal / abstract: "our MDCDS model demonstrates consistent process alignment, robust feature extraction, and improved MIQ modeling"
- proposed / causal / introduction, conclusion: "Zhou et al. proposed a modeling approach"; "by proposing a hierarchical MDCDS"
- is fully demonstrated / causal / experiments: "the effectiveness of MDCDS modeling and fault detection is fully demonstrated"
- exhibits / causal / experiments: "our proposed MDCDS exhibits superior adaptability to nonstationary scenarios"
- cannot / hedge / conclusion: "our approach cannot cover the time-varying characteristic of the process nor guarantee the robustness of the model"

## Cross-section linkers

- introduction → preliminaries: "The remainder of this paper is structured as follows. Section II draws out the basis of this paper and the problem encountered in BFIP. In Section III, the MDCDS modeling and monitoring process, along with theoretical analysis, is discussed in detail. The empirical BFIP study illustrates the effectiveness of our proposal in Section IV. Finally, this paper wraps up with a conclusion and perspective." (p.3)
- preliminaries → method: BLS 回顾后直接 `III. Methodology of MDCDS` (p.4)
- method → experiments: 故障检测逻辑后 `IV. BFIP Experiment and Analysis` (p.10)
- experiments → conclusion: `F. Summary` 后直接 `V. Conclusion and Prospect` (p.16)

## Candidate rules

- R001 摘要用 `our` 自称方法缩写，缺口用 `To overcome these limitations`。
- R002 Introduction 无独立 Related Work；数据驱动与机理文献写在引言中段，再用编号挑战 1)–3)。
- R003 Introduction 末用 `The remainder of this paper is structured as follows.`；Conclusion 标题为 `Conclusion and Prospect`，局限后接编号未来工作。
- R004 Experiments 用真实厂名与故障集 `F1`/`F2`，小结段 `F. Summary` 再进结论。

## Candidate phrases

- `To overcome these limitations, our` (abstract)
- `Despite the progress that has been made, there are still some challenges that remain to be addressed:` (introduction)
- `The remainder of this paper is structured as follows.` (introduction)
- `This study addresses the limitations of` (conclusion)
- `which further promotes our future research as follows.` (conclusion)

## House style

自称是 `our` / `This study` / `this paper` / `our proposal`。摘要用 `our MDCDS`。`this paper` 与 `This study` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。

## Quotes

- p.1 abstract: Data-driven techniques are reshaping blast furnace iron-making process (BFIP) modeling, but their “black-box” nature often obscures interpretability and accuracy.
- p.1 abstract: To overcome these limitations, our mechanism and data co-driven strategy (MDCDS) enhances model transparency and molten iron quality (MIQ) prediction.
- p.1 abstract: Validated against real-world BFIP data, our MDCDS model demonstrates consistent process alignment, robust feature extraction, and improved MIQ modeling—Yielding better fault detection.
- p.1 introduction: CHINA stands unrivaled as the world's foremost producer and consumer of steel, commanding a prominent role in the global steel sector.
- p.1 introduction: However, although China leads in steel production, it has not attained a commensurate standing in the global iron and steel industry and struggles to source high-quality iron ore at affordable prices.
- p.2 introduction: Therefore, it is crucial to establish effective monitoring systems capable of promptly detecting and addressing relevant faults, guaranteeing the smooth and safe operation of BFIP.
- p.2 introduction: However, most of these approaches have focused solely on single MIQ parameters, ignoring the consideration of multiple parameters simultaneously.
- p.2 introduction: Despite the progress that has been made, there are still some challenges that remain to be addressed:
- p.3 introduction: The remainder of this paper is structured as follows. Section II draws out the basis of this paper and the problem encountered in BFIP. In Section III, the MDCDS modeling and monitoring process, along with theoretical analysis, is discussed in detail. The empirical BFIP study illustrates the effectiveness of our proposal in Section IV. Finally, this paper wraps up with a conclusion and perspective.
- p.4 method: Due to the complexity within the BFIP, we vertically divide the huge blast furnace into zones during the mechanism modeling.
- p.10 experiments: In this section, the effectiveness of MDCDS modeling and fault detection is fully demonstrated using data from a real BFIP at Liuzhou Iron and Steel Co. Ltd. in Guangxi, China.
- p.15 experiments: With our proposed MDCDS, we can derive timely and accurate MIQ prediction, circumventing the delays associated with laboratory testing.
- p.15 experiments: For fault detection, our proposed MDCDS exhibits superior adaptability to nonstationary scenarios such as raw material fluctuation and hot stove switching to ensure sufficient detection accuracy.
- p.16 conclusion: This study addresses the limitations of data-driven models in BFIP by proposing a hierarchical MDCDS.
- p.16 conclusion: Overall, by bridging the gap between data-driven methods and mechanistic understanding, our MDCDS approach has blazed a new trail of co-driven modeling and monitoring techniques of complex BFIP.
- p.16 conclusion: However, our approach cannot cover the time-varying characteristic of the process nor guarantee the robustness of the model, which further promotes our future research as follows.
