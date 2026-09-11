---
key: H3GRRH4W
title: "A Novel Data Augmentation Method Based on Denoising Diffusion Probabilistic Model for Fault Diagnosis Under Imbalanced Data"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3366991"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. BRIEF INTRODUCTION OF PRELIMINARY KNOWLEDGE` → `III. PROPOSED METHOD` → `IV. EXPERIMENT` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评算法级/数据级不平衡方法、GAN/VAE，再以 Table I 归类）。Introduction 末有编号贡献与节序路标，指向 Section II–V。Method 标题为 `PROPOSED METHOD`。Experiments 标题为 `EXPERIMENT`（CWRU + 两套实测轴承台）。

## Openers

- abstract: `Imbalanced data constitute` — "Imbalanced data constitute a significant challenge in intelligent fault diagnosis cases because they can result in degraded diagnosis accuracy, which can in turn jeopardize the safety and reliability of industrial equipment." (p.7820)
- introduction: `AS A widely` — "AS A widely used hardware component in industrial equipment, the fault detection of bearings is of great significance in industrial production [1]." (p.7820；栏首掉字)
- method: `As illustrated in` — "As illustrated in Fig. 1, the overall fault diagnosis framework mainly comprises of the following four components: data acquisition and processing, data augmentation, quality evaluation, and sample augmentation and fault diagnosis modules." (p.7823, III.A)
- experiments: `In this section` — "In this section, to verify the effectiveness of the proposed method, extensive fault diagnosis experiments are conducted using three bearing fault datasets." (p.7824)
- conclusion: `In this article` — "In this article, we propose a novel sample augmentation method based on the diffusion model." (p.7830)

## Gap transitions

- however (abstract): "Generative adversarial networks (GANs) have been effectively used as common data augmentation methods to address this issue. However, their training process is difficult to perform and prone to mode collapse." (p.7820)
- therefore (abstract): "Therefore, this article proposes a novel data augmentation method grounded in a diffusion model." (p.7820)
- however (introduction): "These intelligent fault diagnosis (IFD) methods based on deep learning have produced better outcomes than those of conventional methods. However, the successful application of deep learning technology in fault diagnosis relies heavily on the support provided by large amounts of data." (p.7820)
- therefore (introduction): "Therefore, we propose a novel data augmentation method based on the diffusion model." (p.7821)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a novel data augmentation method"; "we propose a novel data augmentation method"; "In this article, we propose"
- show / causal / abstract: "The experimental results show that our method can generate higher quality and more diverse pseudosamples"
- reveal / causal / conclusion: "the experimental results reveal that compared with the existing data augmentation methods, the proposed method has notable benefits"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II presents a concise introduction to the related models. Section III delineates the proposed approach and the entire framework used to tackle the data imbalance problem. Section IV details the experimental evaluation and validation. Finally, Section V concludes this article." (p.7822)
- method → experiments: 质量评价段落后直接 `IV. EXPERIMENT` (p.7824)
- experiments → conclusion: Case 3 总结后直接 `V. CONCLUSION` (p.7830)

## Candidate rules

- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions of this article can be summarized as follows.` + 编号列表。
- R005 Conclusion 先收回方法，再用 `The limitations and future work are summarized as follows` 指向后续。

## Candidate phrases

- `Therefore, this article proposes a novel` (abstract)
- `The contributions of this article can be summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, we propose a novel` (conclusion)
- `The limitations and future work are summarized as follows:` (conclusion)

## House style

自称 `this article proposes` / `we propose` / `In this article, we propose` / `our method` / `our approach`。未见 `Here we`。`this article proposes` 与 `In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.7820 abstract: Imbalanced data constitute a significant challenge in intelligent fault diagnosis cases because they can result in degraded diagnosis accuracy, which can in turn jeopardize the safety and reliability of industrial equipment.
- p.7820 abstract: Generative adversarial networks (GANs) have been effectively used as common data augmentation methods to address this issue. However, their training process is difficult to perform and prone to mode collapse.
- p.7820 abstract: Therefore, this article proposes a novel data augmentation method grounded in a diffusion model.
- p.7820 abstract: The experimental results show that our method can generate higher quality and more diverse pseudosamples, and achieve superior fault diagnosis performance under imbalanced data.
- p.7820 introduction: AS A widely used hardware component in industrial equipment, the fault detection of bearings is of great significance in industrial production [1].
- p.7820 introduction: These intelligent fault diagnosis (IFD) methods based on deep learning have produced better outcomes than those of conventional methods. However, the successful application of deep learning technology in fault diagnosis relies heavily on the support provided by large amounts of data.
- p.7821 introduction: Therefore, we propose a novel data augmentation method based on the diffusion model.
- p.7822 introduction: The contributions of this article can be summarized as follows.
- p.7822 introduction: The rest of this article is organized as follows. Section II presents a concise introduction to the related models. Section III delineates the proposed approach and the entire framework used to tackle the data imbalance problem. Section IV details the experimental evaluation and validation. Finally, Section V concludes this article.
- p.7823 method: As illustrated in Fig. 1, the overall fault diagnosis framework mainly comprises of the following four components: data acquisition and processing, data augmentation, quality evaluation, and sample augmentation and fault diagnosis modules.
- p.7824 experiments: In this section, to verify the effectiveness of the proposed method, extensive fault diagnosis experiments are conducted using three bearing fault datasets.
- p.7830 conclusion: In this article, we propose a novel sample augmentation method based on the diffusion model.
- p.7830 conclusion: The limitations and future work are summarized as follows:
