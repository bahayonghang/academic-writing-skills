---
key: IJT3SBXK
title: "Learning Deep Multimanifold Structure Feature Representation for Quality Prediction With an Industrial Application"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2021.3130411"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. STACKED MULTIMANIFOLD AUTOENCODER` → `IV. INDUSTRIAL APPLICATIONS` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 SAE / 流形正则 / 单流形假设）。Introduction 末有 `The rest of this article is organized as follows`。Method 在 III。Experiments 标题为 `INDUSTRIAL APPLICATIONS`。

## Openers

- abstract: `Due to the` — "Due to the existence of complex disturbances and frequent switching of operational conditions characteristics in the real industrial processes, the process data under different operational conditions subject to different distributions, which means there exist different manifold structures under broad operations." (p.5849)
- introduction: `MODERN industrial processes` — "MODERN industrial processes are becoming more and more complicated, which puts forward strict requirements on stable and economical production [1]–[3]." (p.5849)
- method: `The basic idea` — "The basic idea of MMAE method comes from the fact that frequent switching of the actual industrial process operational conditions can cause the process data to be distributed in a multimanifold structure." (p.5852, III.A)
- experiments: `In this section` — "In this section, the performance of the proposed S-MMAE is validated on a real hydrocracking process case." (p.5854, IV)
- conclusion: `Multimanifold was a` — "Multimanifold was a universal phenomenon in industrial processes under a series of complex disturbances or switching operational conditions." (p.5857)

## Gap transitions

- however (introduction): "However, these quality variables are usually quite difficult to measure, which are commonly obtained by using expensive online measuring instruments or lab analysis, thus leading to expensive measurement costs and large time-delay." (p.5849)
- therefore (introduction): "Therefore, the soft sensing technique has been developed for real-time prediction of key quality variables by establishing the correlation between difficult measured quality variables and easy measured process variables, which is widely used in real industrial processes [6], [7]." (p.5849)
- however (introduction): "However, they are limited by their shallow model structures." (p.5849)
- although (introduction): "Although these deep learning approaches have been proposed and successfully applied to real industrial processes, they only take advantage of the global information characterized by data variance to guide feature learning process without considering the local structure information that is beneficial to feature representation." (p.5850)
- however (introduction): "However, classical manifold learning methods are shallow mapping with a nonlinear kernel function, which is limited to providing feasible feature representation." (p.5850)
- to this end (abstract): "To this end, in this article, a novel stacked multimanifold autoencoder (S-MMAE) is proposed for feature extraction and quality prediction." (p.5849)

## Hedge verbs

- propose / causal / abstract, introduction: "a novel stacked multimanifold autoencoder (S-MMAE) is proposed"; "a novel stacked multimanifold autoencoder (S-MMAE) algorithm is proposed"
- demonstrate / causal / abstract, conclusion: "the application results in a practical hydrocracking process demonstrate that the proposed S-MMAE can achieve excellent prediction accuracy"; "the experimental results on actual hydrocracking process data demonstrated that the proposed S-MMAE can significantly improve the prediction performance"
- show / causal / introduction, experiments: "Experimental results show that the proposed approach achieves the excellent quality prediction accuracy"; "Table I shows the comparison of the prediction results"
- aim / causal / method: "the proposed MMAE model aims to capture the multimanifold structure characteristics of multimanifold data"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II reviews the SAE and manifold learning. Section III gives a detail description of the proposed S-MMAE. After that, a real industrial process is used to verify the effectiveness of the proposed method in Section IV. Finally, Section V concludes this article." (p.5850)
- method → experiments: III 指标定义后 `IV. INDUSTRIAL APPLICATIONS` (p.5854)
- experiments → conclusion: 航空煤油结果后直接 `V. CONCLUSION` (p.5857)

## Candidate rules

- R002 Introduction 无独立 Related Work，已有方法评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R001 abstract 贡献句用 `in this article, a novel ... is proposed`。
- R009 结论用过去时收回方法：`was proposed` / `demonstrated`。

## Candidate phrases

- `To this end, in this article, a novel` (abstract)
- `Motivated by the common phenomenon of` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this section, the performance of the proposed` (experiments)
- `the experimental results on actual ... demonstrated that` (conclusion)

## House style

自称是 `in this article` / `is proposed` / `the proposed S-MMAE` / `this research`。未见 `Here we`、`In this paper`。`in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.5849 abstract: Due to the existence of complex disturbances and frequent switching of operational conditions characteristics in the real industrial processes, the process data under different operational conditions subject to different distributions, which means there exist different manifold structures under broad operations.
- p.5849 abstract: To this end, in this article, a novel stacked multimanifold autoencoder (S-MMAE) is proposed for feature extraction and quality prediction.
- p.5849 abstract: At last, the application results in a practical hydrocracking process demonstrate that the proposed S-MMAE can achieve excellent prediction accuracy, which outperforms other state-of-the-art methods.
- p.5849 introduction: MODERN industrial processes are becoming more and more complicated, which puts forward strict requirements on stable and economical production [1]–[3].
- p.5849 introduction: However, these quality variables are usually quite difficult to measure, which are commonly obtained by using expensive online measuring instruments or lab analysis, thus leading to expensive measurement costs and large time-delay.
- p.5849 introduction: Therefore, the soft sensing technique has been developed for real-time prediction of key quality variables by establishing the correlation between difficult measured quality variables and easy measured process variables, which is widely used in real industrial processes [6], [7].
- p.5850 introduction: Although these deep learning approaches have been proposed and successfully applied to real industrial processes, they only take advantage of the global information characterized by data variance to guide feature learning process without considering the local structure information that is beneficial to feature representation.
- p.5850 introduction: Motivated by the common phenomenon of multimanifold in industrial processes, a novel stacked multimanifold autoencoder (S-MMAE) algorithm is proposed to extract comprehensive and effective multimanifold structure features within process data for quality prediction tasks.
- p.5850 introduction: The rest of this article is organized as follows. Section II reviews the SAE and manifold learning. Section III gives a detail description of the proposed S-MMAE. After that, a real industrial process is used to verify the effectiveness of the proposed method in Section IV. Finally, Section V concludes this article.
- p.5852 method: The basic idea of MMAE method comes from the fact that frequent switching of the actual industrial process operational conditions can cause the process data to be distributed in a multimanifold structure.
- p.5854 experiments: In this section, the performance of the proposed S-MMAE is validated on a real hydrocracking process case.
- p.5855 experiments: In this article, the trial-and-error method is utilized for the hyper-parameter selection.
- p.5857 conclusion: Multimanifold was a universal phenomenon in industrial processes under a series of complex disturbances or switching operational conditions.
- p.5857 conclusion: A novel multimanifold structure feature learning method, the S-MMAE model, was proposed to predict the final distillation temperature of high-quality oil products in this research.
- p.5857 conclusion: Finally, the experimental results on actual hydrocracking process data demonstrated that the proposed S-MMAE can significantly improve the prediction performance compared with the existing methods.
