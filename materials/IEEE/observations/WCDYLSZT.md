---
key: WCDYLSZT
title: "Data Augmentation Using Time Conditional Variational Autoencoder for Soft Sensor of Industrial Processes With Limited Data"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3427765"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORKS` → `III. METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（`II. RELATED WORKS`：Seasonal Decomposition、VAE、Stacked Autoencoder）。`related_work=independent`。Introduction 末有节序路标，指向 Section 2–5。Experiments 标题为 `CASE STUDY`。作者稿页码 1–14。

## Openers

- abstract: `In order to` — "In order to accurately predict key variables of complex industrial processes, it is necessary to establish reliable data-driven soft sensing models." (p.1)
- introduction: `To ensure the` — "To ensure the safety and efficiency of industrial processes, strict control of various variables is a significant task." (p.1；栏首掉字)
- related_work: `Seasonal decomposition [25]` — "Seasonal decomposition [25] is a method of splitting time-series data into different components." (p.3, II.A)
- method: `After preprocessing real-time` — "After preprocessing real-time industrial data, we can obtain the following dataset D = {(X , Y) } , where X represents N× T×M auxiliary process variables, Yrepresents N×T×m as key quality variables observed at the same time, N is the number of batch sizes, T is the number of time steps, M and m are the dimensions of process variables and quality variables, respectively." (p.4, III.A)
- experiments: `Refining process requires` — "Refining process requires real-time monitoring of the changes in a unit as well as in the whole process." (p.8, IV.A)
- conclusion: `In this article` — "In this article, a data augmentation method based on TimeCVAE is proposed to generate virtual samples, aiming at improve the prediction accuracy of soft sensors for industrial processes with limited data." (p.13)

## Gap transitions

- however (abstract): "However, it is unavoidable to generate similar samples by traditional VSG methods." (p.1)
- to improve (abstract): "To improve the data augmentation performance of complex processes with limited time-series data, this paper introduces a novel VSG method based on Time Conditional Variational Autoencoder (TimeCVAE)." (p.1)
- however (introduction): "However, missing values, low sampling rate and high sample repetition rates usually lead to insufficient training data for data-based soft sensing models [6]." (p.1)
- to address (introduction): "To address the aforementioned issues in current VAE-based data augmentation methods, this paper proposes a new VSG framework based on Time Conditional Variational Autoencoder (TimeCVAE)." (p.2)
- although (conclusion): "Although TimeCVAE has demonstrated significant potential in generating sequential data, it still faces challenges in situations with limited labeled data." (p.13)

## Hedge verbs

- introduces / causal / abstract: "this paper introduces a novel VSG method based on Time Conditional Variational Autoencoder (TimeCVAE)"
- proposes / causal / introduction, conclusion: "this paper proposes a new VSG framework"; "a data augmentation method based on TimeCVAE is proposed"
- is validated / causal / abstract: "The effectiveness of the proposed method is validated through two industrial applications."
- will focus / speculative / conclusion: "Our future research will focus on exploring semi-supervised data augmentation strategy and continuous data augmentation methods"

## Cross-section linkers

- introduction → related work: "The rest of this paper is organized as follow. Section 2 introduces some preliminary knowledge related to the current work. Then, the proposed method based on TimeCVAE is demonstrated in detail. The next section validates the feasibility of the proposed method using two industrial applications including a debutanizer column and a sulfur recovery unit. Finally, conclusions are made in Section 5." (p.3)
- related work → method: SAE 软测量后 `III. METHODOLOGY` (p.4)
- method → experiments: 流程步骤后 `IV. CASE STUDY` (p.8)
- experiments → conclusion: SRU 结果后 `V. CONCLUSION` (p.13)

## Candidate rules

- R002 有独立 `II. RELATED WORKS`，引言末路标称 Section 2 为 preliminary knowledge，正文标题为 RELATED WORKS。
- R003 Introduction 末用 `The rest of this paper is organized as follow` 指向 2–5。
- R004 贡献用 `The main contributions and innovations of this paper are summarized as follows` + 编号列表。
- R005 Conclusion 先 `In this article, a ... method ... is proposed`，再用 `Although` + `Our future research will focus` 指向后续。

## Candidate phrases

- `this paper introduces a novel VSG method based on` (abstract)
- `To address the aforementioned issues in current ... methods, this paper proposes` (introduction)
- `The rest of this paper is organized as follow.` (introduction)
- `In this article, a data augmentation method based on TimeCVAE is proposed` (conclusion)
- `Our future research will focus on exploring` (conclusion)

## House style

自称混用 `this paper`（摘要/引言/路标）与 `this article`（结论）。另有 `we can obtain` / `we propose` 未直接出现于贡献句；方法段用 `we can obtain`。未见 `Here we`。`this paper introduces`、`this paper proposes`、`In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In order to accurately predict key variables of complex industrial processes, it is necessary to establish reliable data-driven soft sensing models.
- p.1 abstract: However, it is unavoidable to generate similar samples by traditional VSG methods.
- p.1 abstract: To improve the data augmentation performance of complex processes with limited time-series data, this paper introduces a novel VSG method based on Time Conditional Variational Autoencoder (TimeCVAE).
- p.1 abstract: The effectiveness of the proposed method is validated through two industrial applications.
- p.1 introduction: To ensure the safety and efficiency of industrial processes, strict control of various variables is a significant task.
- p.1 introduction: However, missing values, low sampling rate and high sample repetition rates usually lead to insufficient training data for data-based soft sensing models [6].
- p.2 introduction: To address the aforementioned issues in current VAE-based data augmentation methods, this paper proposes a new VSG framework based on Time Conditional Variational Autoencoder (TimeCVAE).
- p.3 introduction: The main contributions and innovations of this paper are summarized as follows:
- p.3 introduction: The rest of this paper is organized as follow. Section 2 introduces some preliminary knowledge related to the current work. Then, the proposed method based on TimeCVAE is demonstrated in detail. The next section validates the feasibility of the proposed method using two industrial applications including a debutanizer column and a sulfur recovery unit. Finally, conclusions are made in Section 5.
- p.3 related_work: Seasonal decomposition [25] is a method of splitting time-series data into different components.
- p.4 method: After preprocessing real-time industrial data, we can obtain the following dataset D = {(X , Y) } , where X represents N× T×M auxiliary process variables, Yrepresents N×T×m as key quality variables observed at the same time, N is the number of batch sizes, T is the number of time steps, M and m are the dimensions of process variables and quality variables, respectively.
- p.8 experiments: Refining process requires real-time monitoring of the changes in a unit as well as in the whole process.
- p.13 conclusion: In this article, a data augmentation method based on TimeCVAE is proposed to generate virtual samples, aiming at improve the prediction accuracy of soft sensors for industrial processes with limited data.
- p.13 conclusion: Although TimeCVAE has demonstrated significant potential in generating sequential data, it still faces challenges in situations with limited labeled data.
- p.13 conclusion: Our future research will focus on exploring semi-supervised data augmentation strategy and continuous data augmentation methods to further enhance the quality prediction accuracy of time-varying processes with small data.
