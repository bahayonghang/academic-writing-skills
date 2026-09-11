---
key: HWSILSUF
title: "Adaptive Wavelet Normalization Network for Soft Sensor Modeling in Nonstationary Industrial Processes"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3609103"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARY` → `III. METHODOLOGY` → `IV. INDUSTRIAL APPLICATIONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评深度学习软测量与非平稳监测；II.B `Data Normalization Methods in Deep Learning` 是预备节子节）。Introduction 末有编号贡献与 `The rest of this article is organized as follows`。Method 标题为 `METHODOLOGY`。Experiments 标题为 `INDUSTRIAL APPLICATIONS`（浮选精矿品位）。

## Openers

- abstract: `In industrial processes` — "In industrial processes, accurate, real-time soft sensor modeling of key product indices is essential for optimal process control and improved product quality." (p.9846)
- introduction: `IN INDUSTRIAL processes` — "IN INDUSTRIAL processes, accurate real-time monitoring of the key product index is one of the main objectives pursued by enterprises to optimize process control and improve product quality." (p.9846)
- method: `The overall architecture` — "The overall architecture of the proposed AWNN is illustrated in Fig. 2." (p.9848, III)
- experiments: `In this section` — "In this section, we validate the effectiveness of the proposed AWNN in a real froth flotation industrial process, using the concentrate grade soft sensor modeling as a case study." (p.9852, IV)
- conclusion: `This article addressed` — "This article addressed the significant challenge posed by nonstationary data distributions in industrial soft sensor modeling, which often degrade the performance of deep learning approaches." (p.9855)

## Gap transitions

- however (abstract): "However, the nonstationary characteristics inherent in industrial data, i.e., data distribution drift over time, cause significant challenges to soft sensor modeling." (p.9846)
- to overcome (abstract): "To overcome this limitation, we propose a novel plug-and-play normalization method named adaptive wavelet normalization network (AWNN) for soft sensor modeling in nonstationary industrial processes." (p.9846)
- although (introduction): "Although these models are carefully designed with specific network architectures to handle various inherent characteristics of industrial data, such as correlation, temporal pattern, and process knowledge, another significant and universal challenge in complex process industries is nonstationary" (p.9847)
- however (introduction): "However, although these studies noted the performance degradation of soft sensor model due to nonstationary, they have not addressed the fundamental cause of nonstationary at the data level, which is the drift of the statistical properties." (p.9847)
- therefore (introduction): "Therefore, there is a need for a universal and highly adaptable normalization method that is capable of coping with the distribution drift issue of industrial data" (p.9847)

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a novel plug-and-play normalization method named adaptive wavelet normalization network (AWNN)"; "In this article, we propose the adaptive wavelet normalization network (AWNN)"
- demonstrate / causal / abstract, conclusion: "demonstrating its ability to significantly improve the predictive performance"; "we demonstrate that AWNN not only substantially improves"
- introduce / causal / conclusion: "We introduced the AWNN, a novel plug-and-play module"
- show / causal / experiments, conclusion: "Experimental results showed that integrating AWNN significantly boosts"

## Cross-section linkers

- introduction → preliminary: "The rest of this article is organized as follows. Section II provides preliminary background on soft sensors in nonstationary industrial processes and discusses related work on data normalization methods in deep learning. Section III presents the detailed methodology of the AWNN. Section IV describes the experimental setup, including the dataset preparation, evaluation metrics, and implementation details, followed by a presentation and discussion of the comparative results. Finally, Section V concludes this article, summarizes the key findings and suggests directions for future research." (p.9848)
- preliminary → method: 归一化方法缺口后 `III. METHODOLOGY` (p.9848)
- method → experiments: 复杂度分析后 `IV. INDUSTRIAL APPLICATIONS` (p.9852)
- experiments → conclusion: 超参分析后 `V. CONCLUSION` (p.9855)

## Candidate rules

- R001 abstract 用 `we propose a novel plug-and-play` + 方法缩写，不用 `Here we`。
- R002 Introduction 无独立 Related Work；归一化综述写在 II.B。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 Experiments 标题为 `INDUSTRIAL APPLICATIONS`。
- R005 Conclusion 用 `This article addressed` / `We introduced`，再用 `Future work will focus on` 指向后续。

## Candidate phrases

- `To overcome this limitation, we propose a novel plug-and-play` (abstract)
- `In this article, we propose the adaptive wavelet normalization network (AWNN)` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `This article addressed the significant challenge posed by` (conclusion)
- `Future work will focus on extending AWNN’s application to` (conclusion)

## House style

自称是 `we propose` / `In this article` / `This article addressed` / `We introduced`。未见 `Here we`。`In this article, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.9846 abstract: In industrial processes, accurate, real-time soft sensor modeling of key product indices is essential for optimal process control and improved product quality.
- p.9846 abstract: However, the nonstationary characteristics inherent in industrial data, i.e., data distribution drift over time, cause significant challenges to soft sensor modeling.
- p.9846 abstract: To overcome this limitation, we propose a novel plug-and-play normalization method named adaptive wavelet normalization network (AWNN) for soft sensor modeling in nonstationary industrial processes.
- p.9846 introduction: IN INDUSTRIAL processes, accurate real-time monitoring of the key product index is one of the main objectives pursued by enterprises to optimize process control and improve product quality.
- p.9847 introduction: However, although these studies noted the performance degradation of soft sensor model due to nonstationary, they have not addressed the fundamental cause of nonstationary at the data level, which is the drift of the statistical properties.
- p.9847 introduction: In this article, we propose the adaptive wavelet normalization network (AWNN), a plug-and-play adaptive normalization method that is suitable for soft sensor modeling in nonstationary industrial processes.
- p.9848 introduction: The rest of this article is organized as follows. Section II provides preliminary background on soft sensors in nonstationary industrial processes and discusses related work on data normalization methods in deep learning. Section III presents the detailed methodology of the AWNN. Section IV describes the experimental setup, including the dataset preparation, evaluation metrics, and implementation details, followed by a presentation and discussion of the comparative results. Finally, Section V concludes this article, summarizes the key findings and suggests directions for future research.
- p.9848 method: The overall architecture of the proposed AWNN is illustrated in Fig. 2.
- p.9852 experiments: In this section, we validate the effectiveness of the proposed AWNN in a real froth flotation industrial process, using the concentrate grade soft sensor modeling as a case study.
- p.9854 experiments: It can be seen that across all models and H, integrating AWNN consistently leads to improved performance.
- p.9855 conclusion: This article addressed the significant challenge posed by nonstationary data distributions in industrial soft sensor modeling, which often degrade the performance of deep learning approaches.
- p.9855 conclusion: We introduced the AWNN, a novel plug-and-play module designed to enhance model adaptability through a fine-grained, adaptive normalization and denormalization process.
- p.9855 conclusion: Future work will focus on extending AWNN’s application to diverse industrial processes, potentially combining it with online learning or model adaptation techniques to address broader nonstationary challenges, such as distribution shifts and evolving input–output relationships, and to improve responsiveness to rapid changes.
