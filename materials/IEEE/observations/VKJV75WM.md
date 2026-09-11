---
key: VKJV75WM
title: "Industrial Data Imputation Based on Multiscale Spatiotemporal Information Embedding With Asymmetrical Transformer"
venue: "IEEE Transactions on Neural Networks and Learning Systems"
doi: "10.1109/TNNLS.2025.3527581"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. METHODOLOGY` → 两工业数据集比较实验（燃气轮机 + debutanizer；IV 起于 p.6）→ `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mean/EM/kNN、GAIN、M-RNN、AMSA-VAE、Transformer/iTransformer）。Introduction 末有 `The remaining sections are organized as follows.`。Method 在 III。Experiments 为两真实工业数据集。

## Openers

- abstract: `In the process` — "In the process industry, the challenge of missing data significantly impairs the efficacy of data-driven process monitoring systems and soft sensor modeling, particularly due to issues, such as unbalanced sampling intervals and sensor malfunctions." (p.1)
- introduction: `DATA-DRIVEN soft sensor` — "DATA-DRIVEN soft sensor modeling and real-time monitoring methods have been widely applied in the process industry [1], [2], [3], [4]." (p.1；栏首掉字)
- method: `The reaction time-delay` — "The reaction time-delay properties of industrial time-series data lead to the existence of short-term dependencies, specifically referring to intravariable autocorrelation." (p.3, III.A.1)
- experiments: `To detect toxic` — "To detect toxic gases, nine easily detectable process variables were selected." (p.6；燃气轮机案例)
- conclusion: `To tackle the` — "To tackle the data imputation challenges in process industries, this article introduces an MSST-Former imputation framework based on embedding multiscale spatial information." (p.11)

## Gap transitions

- however (introduction): "However, several problems, including short blackouts, irregular hardware sampling times, delays in laboratory analysis, and even cyberattacks, contribute to persistent and tough challenges with missing data [8], [9], [10]." (p.1)
- therefore (introduction): "Therefore, ensuring data completeness, high quality, and timely updates are critical to the success of data-driven methods." (p.1)
- however (introduction): "However, GAIN does not take into account the dynamic characteristics of the data." (p.1–2)
- therefore (introduction): "Therefore, data imputation is a formidable task due to the complex and coupled nature of the process industry." (p.2)
- to summarize (introduction): "To summarize, to the best of the authors’ knowledge, there are few MDI methods that comprehensively consider the spatiotemporal properties of data from both global and local perspectives to solve the problem of industrial missing data." (p.2)
- therefore (introduction): "Therefore, this article proposes a multiscale spatiotemporal information embedding with asymmetrical Transformer (MSST-Former)." (p.2)

## Hedge verbs

- introduce / causal / abstract, conclusion: "this article introduces a novel data imputation framework"; "this article introduces an MSST-Former imputation framework"
- propose / causal / introduction: "this article proposes a multiscale spatiotemporal information embedding with asymmetrical Transformer (MSST-Former)"
- verify / causal / abstract: "Comparative experiments ... verify the superiority and robustness of the proposed MSST-Former."
- demonstrate / causal / conclusion: "Extensive experiments demonstrate the effectiveness and robustness of the proposed MSST-Former"
- may / speculative / experiments: "High-latency or low-bandwidth networks may result in delays" 未见；实验段用 `achieves` / `demonstrates`

## Cross-section linkers

- introduction → method: "The remaining sections are organized as follows. Section II provides a brief introduction to attention mechanisms and Transformer models. In Section III, the proposed MSST-Former and the corresponding data imputation framework are described in detail. Section IV presents the results of a comparative experiment on two real-world industrial datasets to verify the superiority of the proposed methods. Finally, Section V gives a comprehensive summary of this article." (p.2)
- method → experiments: Algorithm 1 与 MDI 框架后进入燃气轮机/debutanizer 案例 (p.6)
- experiments → conclusion: 软测量下游实验后 `V. CONCLUSION` (p.11)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The remaining sections are organized as follows` 指向 II–V。
- R004 贡献用 `Our contributions are summarized as follows.` + 编号列表。
- R005 Conclusion 先收回三模块，再以实验优越性收束；未见单独 future-work 段。

## Candidate phrases

- `To overcome these limitations, this article introduces a novel data imputation framework` (abstract)
- `To summarize, to the best of the authors’ knowledge` (introduction)
- `Therefore, this article proposes` (introduction)
- `Our contributions are summarized as follows.` (introduction)
- `The remaining sections are organized as follows.` (introduction)

## House style

自称是 `this article introduces` / `this article proposes` / `the proposed MSST-Former` / `we propose`。未见 `Here we`、`In this paper`。`this article introduces` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In the process industry, the challenge of missing data significantly impairs the efficacy of data-driven process monitoring systems and soft sensor modeling, particularly due to issues, such as unbalanced sampling intervals and sensor malfunctions.
- p.1 abstract: To overcome these limitations, this article introduces a novel data imputation framework, termed multiscale spatiotemporal information embedding with asymmetrical Transformer (MSST-Former).
- p.1 abstract: Comparative experiments with several baseline and state-of-the-art models on two real-world industrial datasets verify the superiority and robustness of the proposed MSST-Former.
- p.1 introduction: DATA-DRIVEN soft sensor modeling and real-time monitoring methods have been widely applied in the process industry [1], [2], [3], [4].
- p.1 introduction: However, several problems, including short blackouts, irregular hardware sampling times, delays in laboratory analysis, and even cyberattacks, contribute to persistent and tough challenges with missing data [8], [9], [10].
- p.1 introduction: Therefore, ensuring data completeness, high quality, and timely updates are critical to the success of data-driven methods.
- p.2 introduction: Therefore, data imputation is a formidable task due to the complex and coupled nature of the process industry.
- p.2 introduction: To summarize, to the best of the authors’ knowledge, there are few MDI methods that comprehensively consider the spatiotemporal properties of data from both global and local perspectives to solve the problem of industrial missing data.
- p.2 introduction: Therefore, this article proposes a multiscale spatiotemporal information embedding with asymmetrical Transformer (MSST-Former).
- p.2 introduction: Our contributions are summarized as follows.
- p.2 introduction: The remaining sections are organized as follows. Section II provides a brief introduction to attention mechanisms and Transformer models. In Section III, the proposed MSST-Former and the corresponding data imputation framework are described in detail. Section IV presents the results of a comparative experiment on two real-world industrial datasets to verify the superiority of the proposed methods. Finally, Section V gives a comprehensive summary of this article.
- p.3 method: The reaction time-delay properties of industrial time-series data lead to the existence of short-term dependencies, specifically referring to intravariable autocorrelation.
- p.6 experiments: Particularly, MSST-Former demonstrates a 15.4% (3.086 → 2.612) reduction in RMSE, a 30.0% (0.958 → 0.690) reduction in MAE, and a 1.8% (0.905 → 0.922) improvement in R2 under the 30% missing rate.
- p.11 conclusion: To tackle the data imputation challenges in process industries, this article introduces an MSST-Former imputation framework based on embedding multiscale spatial information.
- p.11 conclusion: Extensive experiments demonstrate the effectiveness and robustness of the proposed MSST-Former, showcasing its superiority over other baseline models.
