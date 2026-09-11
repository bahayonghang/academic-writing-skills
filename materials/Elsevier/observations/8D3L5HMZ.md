---
key: 8D3L5HMZ
title: "SA-MSIFF: Soft sensing the cement f-CaO content with a self-adaptive multisource information fusion framework in clinker burning process"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2024.103282"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,8-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Related work` → `3. Methodology` → `4. Experiments and results` → `5. Engineering applications` → `6. Conclusion and future work`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。有独立 `2. Related work`。`related_work=independent`。Introduction 末有编号贡献 + 节序路标。Experiments 后另设工程应用节。

## Openers

- abstract: `The accurate soft` — "The accurate soft sensing of f-CaO content in cement clinker is crucial for the cement industry."
- introduction: `As one of` — "As one of the most fundamental industries in the world, the cement industry produces billions of tons of building materials every year [1]."
- related_work: `In order to` — "In order to develop an enhanced f-CaO content soft sensor that is suitable for practical engineering applications, it is crucial to have a comprehensive understanding of the evolving trends in soft sensing and identify the drawbacks of the previous methods."
- method: `As illustrated in` — "As illustrated in Fig. 2, The SA-MSIFF is realized through the incorporation of two individual modules: the real-time kiln modeling module and the end-to-end f-CaO content modeling module."
- experiments: `To validate the` — "To validate the capability of the proposed SA-MSIFF in f-CaO content soft sensing, a series of offline experiments are conducted to analyze it from multiple perspectives, including modeling efficiency, soft sensing performance, and the rationality of intermediate outputs within the framework."
- conclusion: `This paper introduces` — "This paper introduces SA-MSIFF, a novel approach for soft sensing the f-CaO content in the cement clinker burning process."

## Gap transitions

- however (abstract): "However, existing methods require improvements in terms of effectiveness, practicality, and computational efficiency for industrial applications."
- responding (abstract): "Responding to these needs, this paper proposes a self-adaptive multisource information fusion framework (SA-MSIFF) for f-CaO content soft sensing."
- nonetheless (introduction): "Nonetheless, to meet the requirements of practical engineering applications, further improvements are still needed in terms of effectiveness, practicality, computational efficiency, and other relevant aspects"
- in response (introduction): "In response to the aforementioned needs and to explore the REAL application of soft sensors based on multisource information, this paper introduces a self-adaptive multisource information fusion framework (SA-MSIFF)"

## Hedge verbs

- propose / causal / abstract: "this paper proposes a self-adaptive multisource information fusion framework (SA-MSIFF)"
- introduce / causal / introduction, conclusion: "this paper introduces a self-adaptive multisource information fusion framework (SA-MSIFF)"; "This paper introduces SA-MSIFF, a novel approach"
- indicate / associative / introduction: "The results indicate that the SA-MSIFF can self-adaptively handle the multisource feature extraction and fusion tasks"

## Cross-section linkers

- introduction → related work: "The subsequent sections are organized as follows: Section 2 provides an overview of the related works in f-CaO content soft sensing and discusses the limitations of the previous MSIFF. Section 3 offers the detailed methodology of our SA-MSIFF. Section 4 validates the SA-MSIFF using offline production data. In Section 5, an engineering application case of SA-MSIFF is presented. Finally, conclusions are made in Section 6."
- related work → method: MSIFF 局限段落后 `3. Methodology`
- method → experiments: 半监督损失段落后 `4. Experiments and results`
- experiments → application: 消融对比后 `5. Engineering applications`
- application → conclusion: 在线软测量界面后 `6. Conclusion and future work`

## Candidate rules

- 独立 Related Work（SP-ELS-001）。
- R003 节序路标：`The subsequent sections are organized as follows`
- R004 编号贡献：`The paper's main technical contributions are summarized below`
- R009 自称：`this paper proposes` / `this paper introduces`

## Candidate phrases

- `Responding to these needs, this paper proposes` (abstract)
- `this paper introduces a self-adaptive` (introduction)
- `The subsequent sections are organized as follows` (introduction)
- `To validate the capability of the proposed` (experiments)
- `This paper introduces SA-MSIFF, a novel approach for` (conclusion)

## House style

自称 `this paper proposes` / `this paper introduces` / `our SA-MSIFF` / `our proposed SA-MSIFF method`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。文末有 Generative AI 声明：作者用 ChatGPT (GPT-3.5) 改进行文，随后自行审改。

## Quotes

- abstract: The accurate soft sensing of f-CaO content in cement clinker is crucial for the cement industry.
- abstract: Responding to these needs, this paper proposes a self-adaptive multisource information fusion framework (SA-MSIFF) for f-CaO content soft sensing.
- abstract: Compared to its previous version, MSIFF, the SA-MSIFF achieves a considerable 89.65% reduction in framework training time and an 8.22% decrease in soft sensing error.
- introduction: As one of the most fundamental industries in the world, the cement industry produces billions of tons of building materials every year [1].
- introduction: In response to the aforementioned needs and to explore the REAL application of soft sensors based on multisource information, this paper introduces a self-adaptive multisource information fusion framework (SA-MSIFF) for soft sensing the f-CaO content in the clinker burning process.
- introduction: The subsequent sections are organized as follows: Section 2 provides an overview of the related works in f-CaO content soft sensing and discusses the limitations of the previous MSIFF.
- related_work: In order to develop an enhanced f-CaO content soft sensor that is suitable for practical engineering applications, it is crucial to have a comprehensive understanding of the evolving trends in soft sensing and identify the drawbacks of the previous methods.
- method: As illustrated in Fig. 2, The SA-MSIFF is realized through the incorporation of two individual modules: the real-time kiln modeling module and the end-to-end f-CaO content modeling module.
- experiments: To validate the capability of the proposed SA-MSIFF in f-CaO content soft sensing, a series of offline experiments are conducted to analyze it from multiple perspectives, including modeling efficiency, soft sensing performance, and the rationality of intermediate outputs within the framework.
- experiments: The data used for these experiments are collected from a real cement production line, spanning from October 2022 to December 2022.
- application: To further demonstrate the SA-MSIFF's capability and usability, the engineering applications of the SA-MSIFF are showcased as additional validation.
- conclusion: This paper introduces SA-MSIFF, a novel approach for soft sensing the f-CaO content in the cement clinker burning process.
