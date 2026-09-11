---
key: WNCMQEGA
title: "MIE-Net: Motion Information Enhancement Network for Fine-Grained Action Recognition Using RGB Sensors"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2024.3363042"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. METHOD` → 数据集构建（引言路标为 Section IV）→ 实验（引言路标为 Section V；正文含 `B. Experimental Setting` / `C. Ablation Studies` / `D. Comparison With State-of-the-Art`）→ `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORK`，含 temporal modeling / motion representation / multimodal fusion）。Introduction 末有节序路标，指向 Section II–VI。Method 为 III。Experiments 为 Section V。页码 11770–11782。

## Openers

- abstract: `In recent years` — "In recent years, action recognition has received widespread attention, which classifies actions by extracting features from kinds of sensor data." (p.1)
- introduction: `ACTION recognition is` — "ACTION recognition is a fundamental and challenging task in video understanding, playing an important role in other video tasks such as video captioning [1], temporal action detection [2], [3]." (p.1；栏首掉字)
- related_work: `The early method` — "The early method for exploiting temporal information in action recognition was C3D [4], which learns spatio-temporal features effectively by introducing the temporal dimension to 2-D kernels." (p.2, II.A)
- method: `Denote a dataset` — "Denote a dataset as Dataset = {Dtrain, Dtest}, the corresponding annotation can be depicted as Y = {yas}As as=1 , As indicates action class, as = 1, . . . , As." (p.3, III.A)
- experiments: `We evaluate our` — "We evaluate our approach on NVIDIA GeForce GTX 3 × 1080Ti or 1 × 3090 GPUs, and the prototype system is implemented by using the PyTorch framework." (p.7, V.B)
- conclusion: `In this article` — "In this article, we proposed a video action recognition framework, MIE-Net, aiming at learning more fine-grained action information from RGB and motion features in an end-to-end manner." (p.11, VI)

## Gap transitions

- however (abstract): "However, with the growing difficulty of identifying fine-grained actions, certain methods cannot learn sufficient motion and temporal information." (p.1)
- therefore (abstract): "Therefore, an effective information enhancement method is required to reason motion clues in video sequences." (p.1)
- however (introduction): "However, there are still challenges in identifying similar actions with subtle action variations or differences." (p.1)
- however (related_work): "However, these methods aggregate new features and RGB features by simple rules, such as addition and concatenation fusion, without considering the characteristics of each feature." (p.3)
- although (conclusion): "Although our study shows potential in video action recognition, a particular gap exists between theoretical advancements and practical application." (p.11)

## Hedge verbs

- propose / causal / abstract, introduction: "This article proposes an end-to-end video action recognition framework called the motion information enhancement network (MIE-Net)"; "we propose an end-to-end motion information enhancement network (MIE-Net)"
- demonstrate / causal / abstract, introduction: "Experimental results on SLJD, Something-Something v2, and Diving48 datasets demonstrate that the proposed MIE-Net outperforms most state-of-the-art methods."
- suggest / speculative / related_work: "some researchers suggest that utilizing short-term temporal features between adjacent frames, i.e., motion information, can help identify subtle actions."
- think / speculative / experiments: "We think the reason is that it focuses on long-term global modeling via a self-attention mechanism to overcome the shortcomings of the local receptive field of CNN."

## Cross-section linkers

- introduction → related_work: "The manuscript is organized as follows. Section II introduces related work on state-of-the-art action recognition methodologies. Section III explains the details of our proposed framework. Section IV describes the construction process of the proposed dataset. The experiments and the implementation details are illustrated in Section V. Section VI is a conclusion of this article." (p.2)
- related_work → method: "Therefore, this article proposes a method to enhance fine-grained action recognition using motion information" 随后 `III. METHOD` (p.3)
- experiments → conclusion: CAM 可视化后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 用 `This article proposes` + 方法缩写 + 两个组件。
- R002 独立 `II. RELATED WORK`，引言只点问题，方法族评述放到 II。
- R003 Introduction 贡献用 `The contributions of this article are fourfold.` + 编号 1)–4)。
- R004 Introduction 末用 `The manuscript is organized as follows` 指向 II–VI。
- R005 Conclusion 先收回方法，再用 `Although` 承认局限，`In the future, we plan to` 指向后续。

## Candidate phrases

- `This article proposes an end-to-end video action recognition framework called` (abstract)
- `The contributions of this article are fourfold.` (introduction)
- `The manuscript is organized as follows.` (introduction)
- `In this article, we proposed a video action recognition framework, MIE-Net` (conclusion)
- `In the future, we plan to study more lightweight models` (conclusion)

## House style

自称是 `This article proposes` / `we propose` / `our model` / `In this article, we proposed`。未见 `Here we`。`This article proposes` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: In recent years, action recognition has received widespread attention, which classifies actions by extracting features from kinds of sensor data.
- p.1 abstract: However, with the growing difficulty of identifying fine-grained actions, certain methods cannot learn sufficient motion and temporal information.
- p.1 abstract: Therefore, an effective information enhancement method is required to reason motion clues in video sequences.
- p.1 abstract: This article proposes an end-to-end video action recognition framework called the motion information enhancement network (MIE-Net), which consists of two innovative components.
- p.1 abstract: Experimental results on SLJD, Something-Something v2, and Diving48 datasets demonstrate that the proposed MIE-Net outperforms most state-of-the-art methods.
- p.1 introduction: ACTION recognition is a fundamental and challenging task in video understanding, playing an important role in other video tasks such as video captioning [1], temporal action detection [2], [3].
- p.1 introduction: However, there are still challenges in identifying similar actions with subtle action variations or differences.
- p.2 introduction: Thus, we propose an end-to-end motion information enhancement network (MIE-Net) for fine-grained action recognition by incorporating RGB and motion information to capture subtle motion details and employing temporal attention along the channel dimension to improve the network’s learning capabilities.
- p.2 introduction: The contributions of this article are fourfold.
- p.2 introduction: The manuscript is organized as follows. Section II introduces related work on state-of-the-art action recognition methodologies. Section III explains the details of our proposed framework. Section IV describes the construction process of the proposed dataset. The experiments and the implementation details are illustrated in Section V. Section VI is a conclusion of this article.
- p.2 related_work: The early method for exploiting temporal information in action recognition was C3D [4], which learns spatio-temporal features effectively by introducing the temporal dimension to 2-D kernels.
- p.3 related_work: However, these methods aggregate new features and RGB features by simple rules, such as addition and concatenation fusion, without considering the characteristics of each feature.
- p.3 method: In this work, we propose MIE-Net as an end-to-end video action recognition framework, there are five steps as illustrated in Fig. 1.
- p.7 experiments: We evaluate our approach on NVIDIA GeForce GTX 3 × 1080Ti or 1 × 3090 GPUs, and the prototype system is implemented by using the PyTorch framework.
- p.10 experiments: Compared with the baseline method PAN [14], MIE-Net improves 14.4% higher accuracy (94.4% versus 80.0%) by temporal modeling and feature interaction.
- p.11 conclusion: In this article, we proposed a video action recognition framework, MIE-Net, aiming at learning more fine-grained action information from RGB and motion features in an end-to-end manner.
- p.11 conclusion: Although our study shows potential in video action recognition, a particular gap exists between theoretical advancements and practical application.
- p.11 conclusion: In the future, we plan to study more lightweight models that are easy to deploy and extend them to more downstream video tasks, such as temporal action localization and spatio-temporal action detection, to make them more functional and practical.
