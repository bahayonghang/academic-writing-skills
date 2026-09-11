---
key: 46APYMSS
title: "Sketch Assisted Face Image Coding for Human and Machine Vision: A Joint Training Approach"
venue: "IEEE Transactions on Circuits and Systems for Video Technology"
doi: "10.1109/TCSVT.2023.3262251"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,9-15"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PROPOSED ALGORITHM` → `IV.`（实验）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORK`，含 Image-to-Image Translation / Video Coding for Machine）。Introduction 末有节序路标，指向 Section II–V。贡献用项目符号列表。

## Openers

- abstract: `Image coding is` — "Image coding is one of the most fundamental techniques and is widely used in image/video processing and multimedia communications." (p.6086)
- introduction: `IMAGE coding that` — "IMAGE coding that encodes images before transmission, storage, or analyzation is one of the most visible and continuously challenging problems in many image processing fields, such as industrial solutions, satellite remote sensing telemetry systems, smart cities, autonomous vehicles [1], etc." (p.6086；栏首掉字)
- related_work: `Image-to-image translation` — "Image-to-image translation can directly convert an input image into a corresponding output image without changing the content of the image and is widely applied in the fields of image generation, semantic segmentation, style transfer, etc." (p.6087, II.A)
- method: `In this section, we` — "In this section, we present the details of our proposed human- and machine-oriented face image joint coding framework." (p.6088, III)
- experiments: `The machine analysis performance` — "The machine analysis performance is evaluated on LFW dataset associated with three tasks: gender classification, image memorability prediction, and face detection." (p.6094)
- conclusion: `In this paper, we` — "In this paper, we presented a novel face image coding framework with joint training for both human vision and machine vision, which consists of three modules: an image-to-image translation module, a coding module, and a two-stage reconstruction module." (p.6098)

## Gap transitions

- moreover (abstract): "Moreover, the recent emergence of machine vision goes beyond the scope of current coding." (p.6086)
- however (introduction): "However, human vision-oriented image coding always attempts to minimize human perception loss, which causes the falsification of semantic information." (p.6086)
- additionally (introduction): "Additionally, machine-oriented image coding technology, initially used to improve the accuracy of machine analysis tasks, has become a trending topic within the industry." (p.6086–6087)
- nevertheless (introduction): "Nevertheless, most of the existing methods only focus on one particular analysis task, and the reconstruction task as the supplement, rarely considering the relationship between coding and each task" (p.6087)
- to address (introduction): "To address the above problems, we choose to work on popularly studied face images and propose a human- and machine-oriented face image joint coding algorithm" (p.6087)
- therefore (related work): "Therefore, in this paper, we propose a new representation that can satisfy both features to bridge the gap between machine vision and human vision" (p.6088)

## Hedge verbs

- propose / causal / abstract, introduction: "we proposed a sketch assisted face image coding"; "we propose a joint training algorithm"
- demonstrate / causal / abstract, introduction: "The experimental results on challenge datasets demonstrate that our proposed algorithm offers 40.9%-86.6% bitrate savings"
- present / causal / method, conclusion: "we present the details of our proposed"; "we presented a novel face image coding framework"
- observe / causal / experiments: "We can observe that our algorithm has better experimental results for human vision"

## Cross-section linkers

- introduction → related work: "The rest of this paper is organized as follows. Section II reviews some relevant works. Section III first introduces the frameworks and the objective functions of the three modules, and then presents the training strategy of our human- and machine-oriented face image joint coding algorithm. Section IV demonstrates the experimental results and Section V concludes this paper." (p.6087)
- related work → method: VCM 分类评述后接 `III. PROPOSED ALGORITHM` (p.6088)
- method → experiments: 联合训练策略后接实验节（p.6094 起为人机任务评估）
- experiments → conclusion: Run-time 段落后接 `V. CONCLUSION` (p.6098)

## Candidate rules

- R001 贡献用项目符号 `• We design` / `• We propose`，不用编号 `1)`。
- R002 有独立 Related Work，再按任务拆 Image-to-Image Translation 与 VCM。
- R003 Introduction 末用 `The rest of this paper is organized as follows` 指向 II–V。
- R004 Conclusion 用过去时 `we presented` 收回框架，再用 `In our future work, we will devote our efforts to` 指向后续。
- R005 方法节标题用 `PROPOSED ALGORITHM` 而非 `METHODOLOGY`。

## Candidate phrases

- `With these considerations, we proposed` (abstract)
- `To address the above problems, we choose to work on` (introduction)
- `The contributions of our work are summarized as follows:` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `In this paper, we presented a novel` (conclusion)
- `In our future work, we will devote our efforts to` (conclusion)

## House style

自称是 `we proposed` / `we propose` / `our proposed algorithm` / `In this paper`。未见 `Here we`。`In this paper` / `we propose` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.6086 abstract: Image coding is one of the most fundamental techniques and is widely used in image/video processing and multimedia communications.
- p.6086 abstract: Current image coding methods are mainly human-oriented, and the visual quality is always unsatisfactory, especially at low bitrates.
- p.6086 abstract: Moreover, the recent emergence of machine vision goes beyond the scope of current coding.
- p.6086 abstract: With these considerations, we proposed a sketch assisted face image coding for human and machine vision by a joint training approach.
- p.6086 abstract: The experimental results on challenge datasets demonstrate that our proposed algorithm offers 40.9%-86.6% bitrate savings on machine vision and is comparable to state-of-the-art image coding methods on human vision.
- p.6086 introduction: IMAGE coding that encodes images before transmission, storage, or analyzation is one of the most visible and continuously challenging problems in many image processing fields, such as industrial solutions, satellite remote sensing telemetry systems, smart cities, autonomous vehicles [1], etc.
- p.6086 introduction: However, human vision-oriented image coding always attempts to minimize human perception loss, which causes the falsification of semantic information.
- p.6087 introduction: To address the above problems, we choose to work on popularly studied face images and propose a human- and machine-oriented face image joint coding algorithm, where a novel color sparse sketch is designed to bridge the gap between human vision features and machine analysis features.
- p.6087 introduction: The contributions of our work are summarized as follows:
- p.6087 introduction: The rest of this paper is organized as follows.
- p.6087 related work: Image-to-image translation can directly convert an input image into a corresponding output image without changing the content of the image and is widely applied in the fields of image generation, semantic segmentation, style transfer, etc.
- p.6088 related work: Therefore, in this paper, we propose a new representation that can satisfy both features to bridge the gap between machine vision and human vision and simplify the complexity of the network structure in such a mode.
- p.6088 method: In this section, we present the details of our proposed human- and machine-oriented face image joint coding framework.
- p.6094 experiments: The machine analysis performance is evaluated on LFW dataset associated with three tasks: gender classification, image memorability prediction, and face detection.
- p.6094 experiments: We can observe that our algorithm has better experimental results for human vision with 28% − 39% bitstream saving compared to other methods.
- p.6098 conclusion: In this paper, we presented a novel face image coding framework with joint training for both human vision and machine vision, which consists of three modules: an image-to-image translation module, a coding module, and a two-stage reconstruction module.
- p.6098 conclusion: The experimental results showed that our proposed algorithm provided 40.9%-86.6% of bitrate savings on machine vision while being comparable to state-of-the-art image coding methods on human vision.
- p.6098 conclusion: In our future work, we will devote our efforts to improve and enhance the generalization performance of the model so that it can be better applied to natural images.
