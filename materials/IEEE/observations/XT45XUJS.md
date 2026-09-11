---
key: XT45XUJS
title: "A Data-Driven Self-Supervised LSTM-DeepFM Model for Industrial Soft Sensor"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2021.3131471"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. OVERVIEW OF THE PROPOSED FRAMEWORK` → `IV. METHODOLOGY` → `V. CASE STUDY` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 co-training / VAE / LSTM-VAE / SS-PdeepFM；II 为 Preliminaries 再评综述）。Introduction 末有 `The rest of this article organized as follows`（缺 is）。Method 拆成 III 框架总览与 IV 方法。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `Soft sensor, as` — "Soft sensor, as an important paradigm for industrial intelligence, is widely used in industrial production to achieve efficient monitoring and prediction of production status including product quality." (p.5859)
- introduction: `PRODUCTION status prediction` — "PRODUCTION status prediction, such as product quality prediction, is critical for high-quality product delivery and core competencies [1]." (p.5859)
- method: `In this section` — "In this section, as shown in Fig. 2, the overview of the proposed framework, mainly including data processing, pretraining stage, and finetuning stage, is presented." (p.5861, III)
- experiments: `To measure the` — "To measure the proposed method, a case study is presented to illustrate the advantages of our proposed method over the methods based on generation model and depth feature extraction." (p.5864, V)
- conclusion: `In this article` — "In this article, a data-driven self-supervised LSTM-DeepFM model was proposed for industrial soft sensor prediction." (p.5868)

## Gap transitions

- however (introduction): "However, traditional methods of product quality prediction, relying on offline laboratory analysis, are generally untimely." (p.5859)
- however (introduction): "However, due to the complex characteristics of industrial data, data-driven approaches usually have difficulties in modeling." (p.5859)
- however (introduction): "However, the abovementioned models only analyze and model a specific characteristic of industrial data, and cannot achieve fusion learning of various industrial data characteristics." (p.5860)
- to solve (introduction): "To solve the abovementioned problems, a data-driven self-supervised LSTM-deep factorization machine (DeepFM) model is proposed for industrial soft sensor prediction with the main contributions given as follows." (p.5860)
- however (preliminaries): "However, the SAE-based models may trivially copy their inputs to outputs without finding useful patterns in the data." (p.5860)

## Hedge verbs

- propose / causal / abstract, introduction: "a data-driven self-supervised long short-term memory–deep factorization machine (LSTM-DeepFM) model is proposed"; "a data-driven self-supervised LSTM-deep factorization machine (DeepFM) model is proposed"
- demonstrate / causal / abstract, conclusion: "experiments on the real-world mining dataset demonstrate that the proposed method achieves state of the art"; "Experiments on real-world froth flotation dataset demonstrate the effectiveness"
- illustrate / causal / experiments: "a case study is presented to illustrate the advantages of our proposed method"
- conclude / causal / experiments: "we can reject the null hypothesis and conclude that the performance of the two models is significantly different"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article organized as follows. In Section II, the brief review about the data-driven soft sensor, LSTM, and DeepFM is presented. Then, in Section III, the overview of the proposed framework, including data processing, pretraining stage, and finetuning stage, is proposed. Methodology and its corresponding case study are presented in Sections IV and V, respectively. Finally, Section VI concludes this article." (p.5860)
- method → experiments: IV 末接 `V. CASE STUDY` (p.5864)
- experiments → conclusion: ablation 段落后 `VI. CONCLUSION` (p.5868)

## Candidate rules

- R002 Introduction 无独立 Related Work，缺口用编号 First/Second/Third，再 `To solve the abovementioned problems`。
- R003 Introduction 末用 `The rest of this article organized as follows` 指向 II–VI。
- R004 贡献用 `with the main contributions given as follows` + 编号列表。
- R005 Conclusion 先收回方法，再用 `Future work should focus on`。
- R009 结论 `In this article, ... was proposed`。

## Candidate phrases

- `In this article, a data-driven` (abstract, conclusion)
- `To solve the abovementioned problems, a ... model is proposed` (introduction)
- `The rest of this article organized as follows.` (introduction)
- `Experiments on real-world ... dataset demonstrate` (conclusion)
- `Future work should focus on` (conclusion)

## House style

自称是 `In this article` / `is proposed` / `our proposed method` / `we propose`。Method 有 `Here, we introduce two fundamental methods`。未见 `In this paper`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。`Here, we introduce` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.5859 abstract: Soft sensor, as an important paradigm for industrial intelligence, is widely used in industrial production to achieve efficient monitoring and prediction of production status including product quality.
- p.5859 abstract: In this article, a data-driven self-supervised long short-term memory–deep factorization machine (LSTM-DeepFM) model is proposed for industrial soft sensor, in which a framework mainly including pretraining and finetuning stages is proposed to explore diverse industrial data characteristics.
- p.5859 abstract: Finally, experiments on the real-world mining dataset demonstrate that the proposed method achieves state of the art comparing with stacked autoencoder-based models, variational autoencoder-based models, semisupervised parallel DeepFM, etc.
- p.5859 introduction: PRODUCTION status prediction, such as product quality prediction, is critical for high-quality product delivery and core competencies [1].
- p.5859 introduction: However, traditional methods of product quality prediction, relying on offline laboratory analysis, are generally untimely.
- p.5859 introduction: However, due to the complex characteristics of industrial data, data-driven approaches usually have difficulties in modeling.
- p.5860 introduction: However, the abovementioned models only analyze and model a specific characteristic of industrial data, and cannot achieve fusion learning of various industrial data characteristics.
- p.5860 introduction: To solve the abovementioned problems, a data-driven self-supervised LSTM-deep factorization machine (DeepFM) model is proposed for industrial soft sensor prediction with the main contributions given as follows.
- p.5860 introduction: The rest of this article organized as follows. In Section II, the brief review about the data-driven soft sensor, LSTM, and DeepFM is presented. Then, in Section III, the overview of the proposed framework, including data processing, pretraining stage, and finetuning stage, is proposed. Methodology and its corresponding case study are presented in Sections IV and V, respectively. Finally, Section VI concludes this article.
- p.5861 method: In this section, as shown in Fig. 2, the overview of the proposed framework, mainly including data processing, pretraining stage, and finetuning stage, is presented.
- p.5862 method: Here, we introduce two fundamental methods employed in the pretraining stage.
- p.5864 experiments: To measure the proposed method, a case study is presented to illustrate the advantages of our proposed method over the methods based on generation model and depth feature extraction.
- p.5868 conclusion: In this article, a data-driven self-supervised LSTM-DeepFM model was proposed for industrial soft sensor prediction.
- p.5868 conclusion: Experiments on real-world froth flotation dataset demonstrate the effectiveness and superior performance of the proposed approach by comparing with SVR, LGB, VAE-WGAN, VAE-NN, GSTAE, SS-PdeepFM, and SSFAN.
- p.5868 conclusion: Future work should focus on how to maintain process reliability and support continuous improvement, as well as further exploring online model predictive control techniques.
