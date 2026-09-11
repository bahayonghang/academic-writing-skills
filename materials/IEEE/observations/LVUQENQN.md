---
key: LVUQENQN
title: "Semi-Supervised Soft Sensor Modeling Based on Ensemble Learning With Pseudolabel Optimization"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2024.3427786"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-18"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. EGA-CPCAN SOFT SENSOR MODEL` → `III. EXPERIMENTS` → `IV. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 mechanism/data-driven、半监督 SVR/PLS/Gaussian、ensemble、attention）。Introduction 末有节序路标，指向 Section II–IV。Method 标题为模型名 `EGA-CPCAN SOFT SENSOR MODEL`。Experiments 标题为 `EXPERIMENTS`。

## Openers

- abstract: `Key quality variables` — "Key quality variables are critical in the industrial production process." (p.1)
- introduction: `THE continuous advancement` — "THE continuous advancement of science and technology and product equipment has brought new opportunities for the development of industrial process control and monitoring." (p.1；栏首掉字)
- method: `Semi-supervised learning is` — "Semi-supervised learning is an efficient method for processing large amounts of unlabeled data while maintaining high accuracy." (p.3, II.A)
- experiments: `This section introduces` — "This section introduces how to utilize the EGA-CPCAN model for predicting key quality indicators in industrial steam volume datasets and industrial debutanizer datasets." (p.6, III)
- conclusion: `Due to the` — "Due to the limitations of traditional semi-supervised soft sensor modeling, which only utilizes a single prediction model and cannot guarantee the quality of predicted pseudolabels, an enhanced model called EGA-CPCAN was proposed in this article." (p.16)

## Gap transitions

- however (abstract): "However, due to the difficulty in obtaining labeled data in industrial fields, a substantial quantity of unlabeled data is not reasonably utilized, which challenges the reliability and accuracy of conventional soft sensor models." (p.1)
- therefore (abstract): "Therefore, a semi-supervised model based on the voting ensemble learning is proposed, which combines the outcomes of multiple models’ predictions and utilizes a genetic optimization algorithm to iteratively optimize the generated pseudolabels, improving the accuracy of pseudolabels." (p.1)
- however (introduction): "However, due to the long sampling period, high response delay, and high investment cost of existing instruments and equipment." (p.1)
- therefore (introduction): "Therefore, it is challenging to gather important quality characteristics [1], [2], [3], [4], [5], [6]." (p.1)
- to address (introduction): "To address this challenge, people need to make reasonable use of these unlabeled data." (p.1)
- in summary / although (introduction): "In summary, although semi-supervised learning based on ensemble learning has shown excellent performance in soft sensor modeling, it also faces some challenges and deficiencies" (p.2)

## Hedge verbs

- is proposed / causal / abstract, introduction, conclusion: "a semi-supervised model based on the voting ensemble learning is proposed"; "This article proposes a semi-supervised soft sensor model"; "an enhanced model called EGA-CPCAN was proposed in this article"
- validate / causal / abstract: "experiments were carried out on industrial debutanizer and industrial steam volume datasets to validate the superior predictive performance of the proposed method"
- can / speculative / experiments: "even with fewer labeled samples, the semi-supervised model proposed in this article can effectively utilize unlabeled data"
- represent / speculative / conclusion: "semi-supervised learning models based on label propagation algorithms represent an important research direction for future work"

## Cross-section linkers

- introduction → method: "This article's remaining structure of this article is as follows. Section II introduces the ensemble learning genetic optimization algorithm channel prior convolutional attention network (EGA-CPCAN). Section III introduces the dataset used in this model and the experiments conducted. Section IV provides the summary." (p.3)
- method → experiments: 评价指标后 `III. EXPERIMENTS` (p.6)
- experiments → conclusion: 误差直方图后 `IV. CONCLUSION` (p.16)

## Candidate rules

- R002 Introduction 无独立 Related Work，监督 / 半监督 / ensemble / attention 评述写在引言中段，并以 `In summary, although` + 编号缺口收束。
- R003 Introduction 末用 `This article's remaining structure of this article is as follows` 指向 II–IV。
- R004 贡献用 `The primary contributions of this article are as follows` + 编号列表。
- R005 Conclusion 先收回方法局限，再用 `Therefore` + `future work` 指向标签传播。

## Candidate phrases

- `Therefore, a semi-supervised model based on` (abstract)
- `This article proposes a semi-supervised soft sensor model that` (introduction)
- `The primary contributions of this article are as follows.` (introduction)
- `an enhanced model called EGA-CPCAN was proposed in this article` (conclusion)
- `represent an important research direction for future work` (conclusion)

## House style

自称 `this article` / `this model` / `our model` / `we employ`。未见 `Here we`、`In this paper`。`This article proposes` 与 `was proposed in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Key quality variables are critical in the industrial production process.
- p.1 abstract: However, due to the difficulty in obtaining labeled data in industrial fields, a substantial quantity of unlabeled data is not reasonably utilized, which challenges the reliability and accuracy of conventional soft sensor models.
- p.1 abstract: Therefore, a semi-supervised model based on the voting ensemble learning is proposed, which combines the outcomes of multiple models’ predictions and utilizes a genetic optimization algorithm to iteratively optimize the generated pseudolabels, improving the accuracy of pseudolabels.
- p.1 introduction: THE continuous advancement of science and technology and product equipment has brought new opportunities for the development of industrial process control and monitoring.
- p.1 introduction: However, due to the long sampling period, high response delay, and high investment cost of existing instruments and equipment.
- p.1 introduction: Therefore, it is challenging to gather important quality characteristics [1], [2], [3], [4], [5], [6].
- p.1 introduction: To address this challenge, people need to make reasonable use of these unlabeled data.
- p.2 introduction: In summary, although semi-supervised learning based on ensemble learning has shown excellent performance in soft sensor modeling, it also faces some challenges and deficiencies: 1) most current semi-supervised models based on ensemble learning only consider integrating one type of model, which makes the prediction model’s generalization ability and accuracy insufficient and 2) most current semi-supervised models based on ensemble learning do not consider combining with deep learning models, which leads to insufficient feature extraction ability of the model, thus affecting the prediction performance of the model.
- p.2 introduction: This article proposes a semi-supervised soft sensor model that uses a pseudolabel optimization algorithm to solve the above problem.
- p.2 introduction: The primary contributions of this article are as follows.
- p.3 introduction: This article's remaining structure of this article is as follows. Section II introduces the ensemble learning genetic optimization algorithm channel prior convolutional attention network (EGA-CPCAN). Section III introduces the dataset used in this model and the experiments conducted. Section IV provides the summary.
- p.3 method: Semi-supervised learning is an efficient method for processing large amounts of unlabeled data while maintaining high accuracy.
- p.6 experiments: This section introduces how to utilize the EGA-CPCAN model for predicting key quality indicators in industrial steam volume datasets and industrial debutanizer datasets.
- p.7 experiments: Based on the information in the table, even with fewer labeled samples, the semi-supervised model proposed in this article can effectively utilize unlabeled data.
- p.16 conclusion: Due to the limitations of traditional semi-supervised soft sensor modeling, which only utilizes a single prediction model and cannot guarantee the quality of predicted pseudolabels, an enhanced model called EGA-CPCAN was proposed in this article.
- p.16 conclusion: Currently, most soft sensor models only utilize features of the data for learning without considering the interactions between features. Therefore, semi-supervised learning models based on label propagation algorithms represent an important research direction for future work.
