---
key: PB5CKIYH
title: "Siamese Neural Network and Multimodal Data Fusion Approach for Small-Sample Learning in Industrial Soft Sensor Modeling"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2024.3451148"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGIES` → `IV. CASE STUDY ON SOFT SENSING THE CEMENT CLINKER F-CAO CONTENT` → `V. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 中段已评 PLS / XGBoost / GAN / SNN，再在 II 分 `Multimodal Data Fusion` 与 `SNN-based Soft Sensor Modeling`。Introduction 末有节序路标，指向 Section II–V。Method 标题为 `METHODOLOGIES`。Experiments 标题为水泥熟料 f-CaO 案例。

## Openers

- abstract: `In industrial scenarios` — "In industrial scenarios, soft sensor modeling often faces the challenge of underfitting due to limited available data." (p.1)
- introduction: `SOFT sensing refers` — "SOFT sensing refers to the technique of using easily obtainable variables to infer target variables that are relatively difficult or expensive to measure directly." (p.1；栏首掉字)
- related_work: `With the advancement` — "With the advancement of information and communication technology, the costs of acquiring, storing, and processing image data have significantly decreased." (p.2, II.A)
- method: `To address the` — "To address the challenges of small-sample learning in industrial soft sensor modeling, an SNN-MMDFF is proposed, as depicted in Fig. 1." (p.3, III.A)
- experiments: `To validate the` — "To validate the effectiveness of the proposed SNN-MMDFF in practical industrial applications, a case study is conducted in the cement industry." (p.7, IV.A)
- conclusion: `This paper presents` — "This paper presents an innovative Siamese neural network-based multimodal data fusion framework (SNN-MMDFF) for addressing the challenges of small-sample learning in industrial soft sensor development." (p.13)

## Gap transitions

- therefore (abstract): "Therefore, in the field of industrial soft sensing, it is crucial to develop solutions for regression problems based on small-sample learning." (p.1)
- however (introduction): "However, GAN models are highly sensitive to input data quality, require extensive modeling time, and often encounter issues such as mode collapse and insufficient output stability." (p.2)
- as a result (introduction): "As a result, there remains a significant gap before GANs can be widely adopted for industrial soft sensing tasks." (p.2)
- although (related work): "Although SNNs have been widely applied to many classification problems [24]–[26], their utilization in regression-based industrial soft sensor modeling is still in its early research stages." (p.2)
- however (related work): "However, these SNN-based methods do not consider the essential requirement of regression tasks, which is fitting the relationship between input features and regression targets." (p.2)
- nevertheless (conclusion): "Nevertheless, further investigations are required in various aspects, including the development of more efficient training strategies, optimized loss functions, and improved data sample pairing approaches." (p.13)

## Hedge verbs

- propose / causal / abstract, method: "this paper proposes a Siamese neural network-based multimodal data fusion framework (SNN-MMDFF)"; "an SNN-MMDFF is proposed"
- introduce / causal / introduction: "this paper introduces a novel SNN-based multimodal data fusion framework (SNN-MMDFF)"
- demonstrate / causal / abstract, introduction: "which demonstrates superior performance and robust modeling stability"; "The performance of SNN-MMDFF is demonstrated through its application"
- indicate / causal / experiments: "This indicates that traditional network-based methods are not suitable for small-sample learning regression tasks."
- suggest / causal / experiments: "suggesting that the features extracted by SNN-MMDFF from the process variable data have higher quality."

## Cross-section linkers

- introduction → related work: "The rest of this paper is organized as follows. Section II discusses the current progress of multimodal data fusion techniques and the development of SNN methods for soft sensor modeling. Section III describes the detailed methodologies of the proposed SNN-MMDFF. In Section IV, a case study on soft sensing the cement clinker f-CaO content using SNN-MMDFF is conducted, and the experiment results are presented. Finally, conclusions are made in Section V." (p.2)
- related work → method: SNN 评述后 `III. METHODOLOGIES` (p.3)
- method → experiments: 三阶段训练后 `IV. CASE STUDY ON SOFT SENSING THE CEMENT CLINKER F-CAO CONTENT` (p.7)
- experiments → conclusion: 配对规模分析后 `V. CONCLUSIONS` (p.13)

## Candidate rules

- R001 abstract 用 `this paper proposes` + 框架缩写，再用案例句 `is validated in a case study`。
- R002 独立 Related Work 分 multimodal fusion 与 SNN-based modeling 两小节。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–V。
- R004 贡献用 `The main technical contributions of this paper are summarized below` + 编号列表。
- R005 Conclusion 先收回框架，再用 `Nevertheless, further investigations are required` 指向训练策略与配对方法。

## Candidate phrases

- `this paper proposes a Siamese neural network-based multimodal data fusion framework` (abstract)
- `this paper introduces a novel SNN-based multimodal data fusion framework` (introduction)
- `The main technical contributions of this paper are summarized below:` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `This paper presents an innovative` (conclusion)

## House style

自称是 `this paper` / `the proposed SNN-MMDFF` / `we`。未见 `Here we`。`this paper proposes` 与 `this paper introduces` 进 phrase_bank，不进 anti_ai_patterns。见 `this paper proposes`。

## Quotes

- p.1 abstract: In industrial scenarios, soft sensor modeling often faces the challenge of underfitting due to limited available data.
- p.1 abstract: Therefore, in the field of industrial soft sensing, it is crucial to develop solutions for regression problems based on small-sample learning.
- p.1 abstract: Based on these ideas, this paper proposes a Siamese neural network-based multimodal data fusion framework (SNN-MMDFF) for tackling the challenges of small-sample learning in industrial soft sensor modeling.
- p.1 abstract: The SNN-MMDFF is validated in a case study on cement clinker f-CaO content soft sensing, which demonstrates superior performance and robust modeling stability.
- p.1 introduction: SOFT sensing refers to the technique of using easily obtainable variables to infer target variables that are relatively difficult or expensive to measure directly.
- p.2 introduction: However, GAN models are highly sensitive to input data quality, require extensive modeling time, and often encounter issues such as mode collapse and insufficient output stability.
- p.2 introduction: Drawing on the aforementioned insights and the SNN network architecture, this paper introduces a novel SNN-based multimodal data fusion framework (SNN-MMDFF) for addressing small-sample learning challenges in industrial soft sensor applications.
- p.2 introduction: The main technical contributions of this paper are summarized below:
- p.2 introduction: The rest of this paper is organized as follows. Section II discusses the current progress of multimodal data fusion techniques and the development of SNN methods for soft sensor modeling. Section III describes the detailed methodologies of the proposed SNN-MMDFF. In Section IV, a case study on soft sensing the cement clinker f-CaO content using SNN-MMDFF is conducted, and the experiment results are presented. Finally, conclusions are made in Section V.
- p.2 related work: Although SNNs have been widely applied to many classification problems [24]–[26], their utilization in regression-based industrial soft sensor modeling is still in its early research stages.
- p.3 method: To address the challenges of small-sample learning in industrial soft sensor modeling, an SNN-MMDFF is proposed, as depicted in Fig. 1.
- p.7 experiments: To validate the effectiveness of the proposed SNN-MMDFF in practical industrial applications, a case study is conducted in the cement industry.
- p.11 experiments: This indicates that traditional network-based methods are not suitable for small-sample learning regression tasks.
- p.11 experiments: Finally, the performance of SNN-MMDFF surpasses all other methods, demonstrating the superiority of the SNN-MMDFF approach and the promoting effect of flame images on f-CaO content soft sensing.
- p.13 conclusion: This paper presents an innovative Siamese neural network-based multimodal data fusion framework (SNN-MMDFF) for addressing the challenges of small-sample learning in industrial soft sensor development.
- p.13 conclusion: The results demonstrate the superior performance and robust modeling stability of the proposed framework.
- p.13 conclusion: Nevertheless, further investigations are required in various aspects, including the development of more efficient training strategies, optimized loss functions, and improved data sample pairing approaches.
