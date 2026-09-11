---
key: KSFAD4XY
title: "A two-stage multisource heterogeneous information fusion framework for operating condition identification of industrial rotary kilns"
venue: "Advanced Engineering Informatics"
doi: "10.1016/j.aei.2025.103251"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-10,12-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

前置 `Full length article` / `ARTICLE INFO` / `Keywords` / `ABSTRACT`。数字节：`1. Introduction` → `2. Background and preliminary` → `3` TSMHIF 方法（含 `3.4. Joint training strategy`）→ `4. Results and discussion` → `5. Conclusion`。无独立 Related Work。`related_work=inlined`（Introduction 综述火焰图像、过程数据与多源融合后点缺口）。Introduction 末有编号贡献 + 节序路标。Method 前有过程背景节。Experiments 标题为 `Results and discussion`。

## Openers

- abstract: `The operating condition` — "The operating condition identification plays an irreplaceable role for the low-carbon and high-efficiency operation of industrial rotary kilns."
- introduction: `Rotary kilns are` — "Rotary kilns are the core equipment for producing raw materials, widely used in steel, non-ferrous metals, building materials, and other industrial fields [1,2]."
- method: `In the TSMHIF` — "In the TSMHIF framework, achieving satisfactory performance from both the VIF and condition identification networks is challenging due to the intricate balance required during their simultaneous training." (s.3.4)
- experiments: `The architecture of` — "The architecture of the practical operating condition identification system for industrial rotary kilns is depicted in Fig. 9."
- conclusion: `In this study` — "In this study, a two-stage multisource heterogeneous data fusion framework is proposed to identify the operating conditions."

## Gap transitions

- however (abstract): "However, existing single-stage multisource heterogeneous information fusion methods lack a unified framework to simultaneously fuse the complementary properties among visible images, infrared images, and process data, thus limiting the condition recognition accuracy."
- to this end (abstract): "To this end, this paper proposes a two-stage multisource heterogeneous information fusion (TSMHIF) framework for operating condition identification of industrial rotary kilns."
- according to (introduction): "According to our best knowledge, there are no studies investigating the VIF method applied to the operating condition recognition of industrial rotary kilns."
- motivated by (introduction): "Motivated by this challenge, we developed a novel instrument to collect aligned multi-modality flame images."

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this paper proposes"; "we creatively propose"; "a ... framework is proposed"
- show / causal / abstract: "The industrial experiments show that our proposed method exhibits superior performance in terms of identification accuracy, condition prediction deviation, and visual quality of fused images compared to other competitors."
- demonstrate / causal / experiments, conclusion: "Our image fusion results demonstrate that the VIF-based methods exhibit superior condition recognition accuracy compared to single-modality methods."

## Cross-section linkers

- introduction → method: "The subsequent sections of this paper are outlined as follows. Section 2 provides an overview of the background and preliminary of industrial rotary kilns. Section 3 carefully describes the proposed TSMHIF approach. Section 4 validates the superiority of the proposed method by extensive industrial experiments. Finally, Section 5 presents the conclusions."
- method → experiments: 联合训练策略后 `4. Results and discussion`
- experiments → conclusion: 消融实验后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The subsequent sections of this paper are outlined as follows`
- R004 编号贡献：`the primary contributions of this paper are as follows`
- R009 自称：`this paper proposes` / `In this study ... is proposed`

## Candidate phrases

- `To this end, this paper proposes` (abstract)
- `According to our best knowledge, there are no studies` (introduction)
- `In summary, the primary contributions of this paper are as follows` (introduction)
- `The subsequent sections of this paper are outlined as follows` (introduction)
- `In this study, a ... framework is proposed` (conclusion)

## House style

自称 `this paper proposes` / `In this study` / `our proposed method`。`we developed` 用于采集系统。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The operating condition identification plays an irreplaceable role for the low-carbon and high-efficiency operation of industrial rotary kilns.
- abstract: However, existing single-stage multisource heterogeneous information fusion methods lack a unified framework to simultaneously fuse the complementary properties among visible images, infrared images, and process data, thus limiting the condition recognition accuracy.
- abstract: To this end, this paper proposes a two-stage multisource heterogeneous information fusion (TSMHIF) framework for operating condition identification of industrial rotary kilns.
- abstract: The industrial experiments show that our proposed method exhibits superior performance in terms of identification accuracy, condition prediction deviation, and visual quality of fused images compared to other competitors.
- introduction: Rotary kilns are the core equipment for producing raw materials, widely used in steel, non-ferrous metals, building materials, and other industrial fields [1,2].
- introduction: According to our best knowledge, there are no studies investigating the VIF method applied to the operating condition recognition of industrial rotary kilns.
- introduction: In summary, the primary contributions of this paper are as follows:
- introduction: The subsequent sections of this paper are outlined as follows. Section 2 provides an overview of the background and preliminary of industrial rotary kilns.
- method: In the TSMHIF framework, achieving satisfactory performance from both the VIF and condition identification networks is challenging due to the intricate balance required during their simultaneous training.
- experiments: The architecture of the practical operating condition identification system for industrial rotary kilns is depicted in Fig. 9.
- experiments: From Table 7 and Fig. 13, it can be seen that the accuracies of TSMHIF-KF and SSMHIF-KF are 3.02% and 1.09% higher than that of CAVIF-KF, respectively.
- conclusion: In this study, a two-stage multisource heterogeneous data fusion framework is proposed to identify the operating conditions.
- conclusion: In summary, our proposed method yields excellent condition recognition performance in complex industrial settings.
