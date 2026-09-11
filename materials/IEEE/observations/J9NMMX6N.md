---
key: J9NMMX6N
title: "Data Mode-Related Generative Adversarial Network for Industrial Soft Sensor Application"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3319677"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. RELATED WORK` → `III. DATA MODE-RELATED GENERATIVE ADVERSARIAL NETWORK WITH REGRESSION` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（`RELATED WORK`：WGAN / WGAN-gp 与软测量数据增强流程）。Introduction 末有编号贡献与节序路标，指向 Section II–V。Method 标题为 `DATA MODE-RELATED GENERATIVE ADVERSARIAL NETWORK WITH REGRESSION`。Experiments 标题为 `CASE STUDY`（燃气轮机 NOx）。

## Openers

- abstract: `Modern industrial data` — "Modern industrial data has become increasingly nonlinear and exhibits multimode characteristics as the scale and complexity of the industry increase, significantly impacting the efficacy of soft sensor modeling." (p.4198)
- introduction: `THE rapid development` — "THE rapid development of modern industry has made industrial processes increasingly complex, resulting in high-dimensional, multimode, and strongly nonlinear industrial data, which presents significant challenges for industrial modeling." (p.4198；栏首掉字)
- related_work: `WGAN was proposed` — "WGAN was proposed by Goodfellow et al. in 2017, which is an improved version of GAN [18]." (p.4199, II.A)
- method: `In realistic industrial` — "In realistic industrial production, industrial data often exhibits multiple modes with distributed peaks in different low-dimensional spaces." (p.4200)
- experiments: `In this section` — "In this section, a real-world industrial case on gas turbine demonstrates the feasibility of the proposed MR-GAN model." (p.4202)
- conclusion: `This article presented` — "This article presented a novel data augmentation approach based on MR-GAN to tackle the challenge of generating high-quality industrial multimode data." (p.4204)

## Gap transitions

- however (abstract): "However, traditional GAN lacks the ability to handle multimode data and regression modeling, resulting in difficulties in generating valid multimode data and capturing the relationship between quality variables and process variables, leading to poor performance in multimode regression tasks." (p.4198)
- to address (abstract): "To address the above issues, this article proposes a novel mode-related generative adversarial network with regression modeling (MR-GAN) for data augmentation-based soft sensor modeling." (p.4198)
- however (introduction): "However, the performance of data-driven models depends on a huge amount of data, which means that only by sampling enough data to train the model can the prediction accuracy be guaranteed." (p.4198)
- however (related_work): "However, in the case of multimode data, the generated data cannot be accurately mapped in the area between different modes." (p.4200)
- to address (method): "To address these limitations, we propose a mode-related GAN with a regression framework in this section, enabling efficient generation of multimode data." (p.4200)

## Hedge verbs

- propose / causal / abstract, introduction, method: "this article proposes a novel mode-related generative adversarial network"; "we propose a mode-related GAN"
- demonstrate / causal / abstract, experiments, conclusion: "a case study on a gas turbine dataset demonstrates the effectiveness"; "demonstrates the feasibility"; "The results unequivocally demonstrated the superiority"
- suggest / associative / experiments: "This result suggests that MR-GAN has better training stability and faster convergence"

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. Section II briefly introduces the GAN network and the WGAN-gp network. In Section III, the detailed MR-GAN framework for soft sensor modeling will be described. In Section IV, the framework will be applied to an industrial example as a validation. Finally, Section V concludes this article." (p.4199)
- related_work → method: WGAN-gp 数据增强流程图后直接 `III. DATA MODE-RELATED GENERATIVE ADVERSARIAL NETWORK WITH REGRESSION` (p.4200)
- method → experiments: Algorithm 1 / 指标段落后直接 `IV. CASE STUDY` (p.4202)
- experiments → conclusion: Wasserstein 距离段落后直接 `V. CONCLUSION` (p.4204)

## Candidate rules

- R006 独立 Related Work：`II. RELATED WORK` 紧接 Introduction。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `The main contributions of this article are given as follows.` + 编号。
- R005 结论局限：`In the future, this study aims to` 与 `hence, developing ... is also a crucial research direction`。

## Candidate phrases

- `To address the above issues, this article proposes a novel` (abstract)
- `The main contributions of this article are given as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article presented a novel data augmentation approach based on` (conclusion)
- `In the future, this study aims to further improve` (conclusion)

## House style

自称 `this article proposes` / `we propose` / `This article presented` / `this study aims`。未见 `Here we`。`this article proposes` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.4198 abstract: Modern industrial data has become increasingly nonlinear and exhibits multimode characteristics as the scale and complexity of the industry increase, significantly impacting the efficacy of soft sensor modeling.
- p.4198 abstract: However, traditional GAN lacks the ability to handle multimode data and regression modeling, resulting in difficulties in generating valid multimode data and capturing the relationship between quality variables and process variables, leading to poor performance in multimode regression tasks.
- p.4198 abstract: To address the above issues, this article proposes a novel mode-related generative adversarial network with regression modeling (MR-GAN) for data augmentation-based soft sensor modeling.
- p.4198 abstract: Finally, a case study on a gas turbine dataset demonstrates the effectiveness of the proposed MR-GAN in multimode soft sensing modeling.
- p.4198 introduction: THE rapid development of modern industry has made industrial processes increasingly complex, resulting in high-dimensional, multimode, and strongly nonlinear industrial data, which presents significant challenges for industrial modeling.
- p.4198 introduction: However, the performance of data-driven models depends on a huge amount of data, which means that only by sampling enough data to train the model can the prediction accuracy be guaranteed.
- p.4199 introduction: The main contributions of this article are given as follows.
- p.4199 introduction: The rest of this article is organized as follows. Section II briefly introduces the GAN network and the WGAN-gp network. In Section III, the detailed MR-GAN framework for soft sensor modeling will be described. In Section IV, the framework will be applied to an industrial example as a validation. Finally, Section V concludes this article.
- p.4199 related_work: WGAN was proposed by Goodfellow et al. in 2017, which is an improved version of GAN [18].
- p.4200 related_work: However, in the case of multimode data, the generated data cannot be accurately mapped in the area between different modes.
- p.4200 method: To address these limitations, we propose a mode-related GAN with a regression framework in this section, enabling efficient generation of multimode data.
- p.4202 experiments: In this section, a real-world industrial case on gas turbine demonstrates the feasibility of the proposed MR-GAN model.
- p.4204 conclusion: This article presented a novel data augmentation approach based on MR-GAN to tackle the challenge of generating high-quality industrial multimode data.
- p.4205 conclusion: In the future, this study aims to further improve the quality of the generated data by incorporating expert knowledge and chemical process knowledge into the MR-GAN model.
