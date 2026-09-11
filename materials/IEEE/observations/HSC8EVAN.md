---
key: HSC8EVAN
title: "Knowledge and Data Dual-Driven Fault Diagnosis in Industrial Scenarios: A Survey"
venue: "IEEE Internet of Things Journal"
doi: "10.1109/JIOT.2024.3387538"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,16-22"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. KNOWLEDGE-BASED AND DATA-DRIVEN IE FD METHODS` → `III. KDDD IE FD METHODS` → 挑战与方向（引言路标为 Section IV）→ 新方案（引言路标为 Section V；正文含 federated 子节）→ `VI. CONCLUSION`。前置 `Abstract—`、`Index Terms—` 与 `NOMENCLATURE`。无标题为 Related Work 的独立节，但 `II. KNOWLEDGE-BASED AND DATA-DRIVEN IE FD METHODS` 是独立文献综述，相关工作不内嵌于 Introduction。Survey，无 Method/Experiments 实验节。Introduction 末有节序路标，指向 Section II–VI。

## Openers

- abstract: `Knowledge and data` — "Knowledge and data dual-driven (KDDD) represents a novel paradigm that leverages the strengths of data-driven methods in feature representation and knowledge transfer, while also incorporating expertise accumulated by domain experts." (p.1)
- introduction: `WITH the rapid` — "WITH the rapid advancement of next-generation information technology and advanced industrial operation techniques, the manufacturing industry has undergone a gradual transformation toward digitalization, networking, and intelligence, marking the advent of the Industry 4.0 era [1]." (p.1)
- related_work: `Existing surveys on` — "Existing surveys on data-driven IE FD have extensively covered research in machine learning [13], [18], [19], deep learning [4], [14], [15], [16], [20], [21], [22], and deep transfer learning [3], [17], [23], [24]." (p.3, II)
- method: `The rapid advancement` — "The rapid advancement and widespread adoption of IIoT technologies have resulted in the emergence of complex systems, where component failures can occur unpredictably, thereby compromising system reliability." (p.3, III)
- conclusion: `This article provides` — "This article provides a comprehensive overview and discussion of KDDD methods in the context of IE FD." (p.19, VI)

## Gap transitions

- despite (abstract): "Despite the existence of systematic and valuable reviews on IE FD, there remains a gap in the literature regarding the review of KDDD IE FD methods." (p.1)
- therefore (abstract): "Therefore, conducting a comprehensive investigation into KDDD IE FD methods is of utmost importance and necessity." (p.1)
- consequently (introduction): "Consequently, the practical application of data-driven FD methods, particularly in scenarios with limited samples, becomes challenging [9]." (p.2)
- however (related_work): "However, to the best of our knowledge, there is currently a lack of literature reviews specifically focusing on KDDD IE FD methods." (p.3)
- consequently (future): "Consequently, there is a pressing need to develop robust federated domain generalization methods that fully recognize and understand the relationship between model robustness and generalizability in scenarios with malicious attacks" (p.18)

## Hedge verbs

- represent / causal / abstract: "Knowledge and data dual-driven (KDDD) represents a novel paradigm"
- aim / causal / introduction: "this article aims to provide a comprehensive review of KDDD IE FD methods."
- may / speculative / related_work: "a single knowledge-based method may not be capable of uncovering hidden features within the data."
- offer / causal / related_work: "KDDD methods offer a viable solution to overcome the time-consuming nature of knowledge-based approaches and the instability associated with deep learning models."

## Cross-section linkers

- introduction → related_work: "The subsequent sections of this survey are structured as depicted in Fig. 1. Section II briefly summarizes data-driven and knowledge-based methods for IE FD, highlighting the necessity for KDDD IE FD methods. Section III delves into the detailed integration of prior knowledge with deep learning models. Section IV offers a summary of research challenges and potential research directions of KDDD IE FD methods in practical industrial applications. Following this, Section V presents novel solutions in the field. Finally, Section VI provides a concluding remark to this article." (p.3)
- related_work → taxonomy: "To bridge this gap, this article aims to provide a comprehensive survey in this area." 随后 `III. KDDD IE FD METHODS` (p.3)
- challenges → conclusion: 未来方向段落后直接 `VI. CONCLUSION` (p.19)

## Candidate rules

- R001 Survey abstract 用 `In this survey, we first ... Subsequently, we ... Additionally, we ... Finally, we conclude this survey`。
- R002 独立文献综述节不叫 Related Work，而叫对象方法总述（`II. KNOWLEDGE-BASED AND DATA-DRIVEN IE FD METHODS`）。
- R003 Introduction 贡献用编号列表 1)–4)，并声明 `To the best of our knowledge, this is the first review dedicated to KDDD IE FD.`
- R004 Conclusion 自称 `This article provides a comprehensive overview`，不以实验收回。

## Candidate phrases

- `Despite the existence of systematic and valuable reviews on` (abstract)
- `there remains a gap in the literature regarding` (abstract)
- `To the best of our knowledge, this is the first review dedicated to` (introduction)
- `The subsequent sections of this survey are structured as depicted in Fig. 1.` (introduction)
- `This article provides a comprehensive overview and discussion of` (conclusion)

## House style

自称是 `this survey` / `this article` / `we first` / `we conclude this survey`。未见 `Here we`。`this article` 与 `In this survey` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Knowledge and data dual-driven (KDDD) represents a novel paradigm that leverages the strengths of data-driven methods in feature representation and knowledge transfer, while also incorporating expertise accumulated by domain experts.
- p.1 abstract: Despite the existence of systematic and valuable reviews on IE FD, there remains a gap in the literature regarding the review of KDDD IE FD methods.
- p.1 abstract: Therefore, conducting a comprehensive investigation into KDDD IE FD methods is of utmost importance and necessity.
- p.1 abstract: In this survey, we first outline the limitations of data-driven and knowledge-based FD methods, highlighting the need for KDDD methods.
- p.1 introduction: WITH the rapid advancement of next-generation information technology and advanced industrial operation techniques, the manufacturing industry has undergone a gradual transformation toward digitalization, networking, and intelligence, marking the advent of the Industry 4.0 era [1].
- p.2 introduction: Consequently, the practical application of data-driven FD methods, particularly in scenarios with limited samples, becomes challenging [9].
- p.2 introduction: To the best of our knowledge, this is the first review dedicated to KDDD IE FD.
- p.3 introduction: The subsequent sections of this survey are structured as depicted in Fig. 1. Section II briefly summarizes data-driven and knowledge-based methods for IE FD, highlighting the necessity for KDDD IE FD methods. Section III delves into the detailed integration of prior knowledge with deep learning models. Section IV offers a summary of research challenges and potential research directions of KDDD IE FD methods in practical industrial applications. Following this, Section V presents novel solutions in the field. Finally, Section VI provides a concluding remark to this article.
- p.3 related_work: Existing surveys on data-driven IE FD have extensively covered research in machine learning [13], [18], [19], deep learning [4], [14], [15], [16], [20], [21], [22], and deep transfer learning [3], [17], [23], [24].
- p.3 related_work: However, to the best of our knowledge, there is currently a lack of literature reviews specifically focusing on KDDD IE FD methods.
- p.3 method: The rapid advancement and widespread adoption of IIoT technologies have resulted in the emergence of complex systems, where component failures can occur unpredictably, thereby compromising system reliability.
- p.18 future: Consequently, there is a pressing need to develop robust federated domain generalization methods that fully recognize and understand the relationship between model robustness and generalizability in scenarios with malicious attacks, and to establish a tradeoff strategy between the two, aiming to unearth domain-invariant features with distinct classification boundaries.
- p.19 conclusion: This article provides a comprehensive overview and discussion of KDDD methods in the context of IE FD.
- p.19 conclusion: The KDDD approach offers a solution to address the limitations of deep learning models, such as instability and lack of explainability, while also addressing the time and effort required by knowledge-based methods.
- p.19 conclusion: The aim of this work is to provide readers with a comprehensive understanding of advanced KDDD IE FD technologies, enabling the design of effective solutions for practical application scenarios.
