---
key: P7PCNFQG
title: "A Spatiotemporal Industrial Soft Sensor Modeling Scheme for Quality Prediction With Missing Data"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3400358"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. GAIN-BASED DATA IMPUTATION AND KNNMI-GAT-BASED SPATIAL FEATURE EXTRACTION` → `III. TAMGU-BASED TEMPORAL FEATURE EXTRACTION FOR QUALITY PREDICTION` → `IV. INDUSTRIAL CASE STUDIES: APPLICATION TO HRP` → `V. CONCLUSION AND FUTURE WORK`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mechanism/data-based、SVM/PLS/PCR/ANN、RNN/LSTM/GRU/MGU）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `INDUSTRIAL CASE STUDIES: APPLICATION TO HRP`。Conclusion 标题含 `FUTURE WORK`。

## Openers

- abstract: `Quality prediction is` — "Quality prediction is important for precise control of industrial processes and improvements of product quality." (p.1)
- introduction: `WITH the evolution` — "WITH the evolution of economy and technology, advanced industrial processes, like pharmaceutical process, metallurgy, and chemistry engineering, are gradually becoming more complex and large-scale." (p.1)
- method: `In this section` — "In this section, the principles of GAIN-based data imputation method is briefly introduced." (p.2, II)
- experiments: `The effectiveness of` — "The effectiveness of the new spatiotemporal industrial soft sensor scheme for quality prediction is verified by the HRP." (p.5, IV)
- conclusion: `A practical spatiotemporal` — "A practical spatiotemporal industrial soft sensor modeling framework has been presented for quality prediction with missing data in this article." (p.8)

## Gap transitions

- however (abstract): "However, the temporal features may be often considered by the conventional methods, ignoring the important spatial features, which makes the soft sensor models not have stronger generalization abilities because of insufficient feature information for quality prediction." (p.1)
- to overcome (abstract): "To overcome those problems, a novel spatiotemporal industrial soft sensor modeling scheme is designed for quality prediction." (p.1)
- however (introduction): "However, it is difficult for the common sensors to effectively respond to changes of quality variables in high latency, fast frequency, and hostile environments." (p.1)
- to address (introduction): "To address this issue, the soft sensor modeling technologies are developed and applied to build the relationships between process and quality variables" (p.1)
- motivated by (introduction): "Motivated by the aforementioned discussions, a novel spatiotemporal industrial soft sensor modeling framework is designed for quality prediction with missing data." (p.2)
- although (conclusion): "Although the proposed industrial soft sensor model is performed well in quality prediction with missing data, the model is built from the spatial and temporal perspectives." (p.8)

## Hedge verbs

- is designed / causal / abstract, introduction: "a novel spatiotemporal industrial soft sensor modeling scheme is designed"; "a novel spatiotemporal industrial soft sensor modeling framework is designed"
- demonstrate / causal / abstract: "sufficient simulation experiments are conducted by a typical industrial process, hot rolling process (HRP), to demonstrate the superiority of the proposed scheme"
- has been presented / causal / conclusion: "A practical spatiotemporal industrial soft sensor modeling framework has been presented"
- needs further discussion / speculative / conclusion: "How to integrate other diversity information to improve the quality prediction performance needs further discussion."

## Cross-section linkers

- introduction → method: "This article is organized as follows. Section II gives the structure of GAIN and the kNNMI-GAT-based spatial feature extraction method. Section III presents the TAMGU-based temporal feature extraction method for quality prediction. After that, two case studies on the real HRP are provided in Section IV. At last, Section V gives the conclusions and outlooks." (p.2)
- method → experiments: Algorithm 1 后 `IV. INDUSTRIAL CASE STUDIES: APPLICATION TO HRP` (p.5)
- experiments → conclusion: "To sum up, based on the above extensive simulation experiments and detailed discussions" 后 `V. CONCLUSION AND FUTURE WORK` (p.8)

## Candidate rules

- R002 Introduction 无独立 Related Work，软测量类别与 RNN 变体评述写在引言中段，并以 First/Second/Finally 三点不足 + `Motivated by` 收束。
- R003 Introduction 末用 `This article is organized as follows` 指向 II–V。
- R004 贡献用 `The contributions and innovations are as follows` + 编号动名词条目。
- R005 Conclusion 标题为 `CONCLUSION AND FUTURE WORK`；先被动完成句收回框架，再用 `Although` + `needs further discussion` 指向后续。

## Candidate phrases

- `To overcome those problems, a novel` (abstract)
- `Motivated by the aforementioned discussions, a novel` (introduction)
- `This article is organized as follows.` (introduction)
- `has been presented for quality prediction with missing data in this article` (conclusion)
- `needs further discussion` (conclusion)

## House style

自称 `this article` / `the proposed scheme` / `in this article`。未见 `Here we`、`In this paper`。`in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Quality prediction is important for precise control of industrial processes and improvements of product quality.
- p.1 abstract: However, the temporal features may be often considered by the conventional methods, ignoring the important spatial features, which makes the soft sensor models not have stronger generalization abilities because of insufficient feature information for quality prediction.
- p.1 abstract: To overcome those problems, a novel spatiotemporal industrial soft sensor modeling scheme is designed for quality prediction.
- p.1 abstract: Finally, sufficient simulation experiments are conducted by a typical industrial process, hot rolling process (HRP), to demonstrate the superiority of the proposed scheme compared with some classical and advanced algorithms.
- p.1 introduction: WITH the evolution of economy and technology, advanced industrial processes, like pharmaceutical process, metallurgy, and chemistry engineering, are gradually becoming more complex and large-scale.
- p.1 introduction: However, it is difficult for the common sensors to effectively respond to changes of quality variables in high latency, fast frequency, and hostile environments.
- p.1 introduction: To address this issue, the soft sensor modeling technologies are developed and applied to build the relationships between process and quality variables, providing decision information of adjustment schemes for industrial field engineers and laying foundations for industrial process production automation [1], [2], [3], [4].
- p.2 introduction: Motivated by the aforementioned discussions, a novel spatiotemporal industrial soft sensor modeling framework is designed for quality prediction with missing data.
- p.2 introduction: This article is organized as follows. Section II gives the structure of GAIN and the kNNMI-GAT-based spatial feature extraction method. Section III presents the TAMGU-based temporal feature extraction method for quality prediction. After that, two case studies on the real HRP are provided in Section IV. At last, Section V gives the conclusions and outlooks.
- p.2 method: In this section, the principles of GAIN-based data imputation method is briefly introduced.
- p.4 method: In this section, the proposed TAMGU-based temporal feature extraction method is given.
- p.5 experiments: The effectiveness of the new spatiotemporal industrial soft sensor scheme for quality prediction is verified by the HRP.
- p.8 experiments: To sum up, based on the above extensive simulation experiments and detailed discussions, it can be seen that the proposed spatiotemporal industrial soft sensor modeling scheme is qualified for quality prediction tasks compared with the existing soft sensor modeling methods, which will provide technical support for the quality prediction of industrial processes represented by HRP.
- p.8 conclusion: A practical spatiotemporal industrial soft sensor modeling framework has been presented for quality prediction with missing data in this article.
- p.8 conclusion: Although the proposed industrial soft sensor model is performed well in quality prediction with missing data, the model is built from the spatial and temporal perspectives. How to integrate other diversity information to improve the quality prediction performance needs further discussion.
