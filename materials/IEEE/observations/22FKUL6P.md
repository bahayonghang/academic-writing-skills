---
key: 22FKUL6P
title: "A Zero-Shot Soft Sensor Modeling Approach Using Adversarial Learning for Robustness Against Sensor Fault"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3187708"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. ADVERSARIAL DEEP LEARNING BACKGROUND` → `III. ROBUST SOFT SENSOR MODELING WITH ADVERSARIAL TRAINING` → `IV. NEURAL NETWORK ARCHITECTURE AND TRAINING` → `V. CASE STUDIES` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评异常值鲁棒软测量、零样本故障分类、对抗迁移/GAN 软测量）。Section II 为对抗学习预备。Introduction 末有节序路标。Experiments 标题为 `CASE STUDIES`（TEP + 多相流 MFP）。

## Openers

- abstract: `Soft sensors are` — "Soft sensors are widely used in many industrial systems to monitor key variables that are difficult to measure, using measurements from other available physical sensors." (p.5891)
- introduction: `SENSORS are ubiquitous` — "SENSORS are ubiquitous in industries as they are the eyes and ears for many processes and equipment." (p.5891)
- method: `In general the` — "In general, the data-driven soft sensor is a multivariate regression problem, where it is desired to regress the difficult-to-measure variable (output) from other available physical sensor measurements (input)." (p.5893, III.A)
- experiments: `In this section` — "In this section, we present case studies to evaluate the efficacy of our proposed method." (p.5895)
- conclusion: `In this article` — "In this article, we propose a data-driven soft sensor modeling framework based on adversarial learning to develop soft sensor models that are robust against sensor faults." (p.5900)

## Gap transitions

- however (abstract): "However, existing learning-based soft sensors are still vulnerable to sensor faults, which could deteriorate the performance of the models." (p.5891)
- however (introduction): "However, some variables are inconvenient to measure due to reasons, such as high cost, slow response time, and other technical limitations." (p.5891)
- however (introduction): "However, one important issue that is yet to be addressed is the robustness of learning-based soft sensor models, in particular, robustness against sensor faults." (p.5891)
- although (introduction): "Although these works aimed to enhance the robustness of soft sensor models, they did not consider the issue of sensor faults." (p.5892)
- therefore (introduction): "Therefore, it would be highly beneficial if a soft sensor model can be trained to be robust against sensor faults under a zero-shot learning regime [13], that is, using only datasets that are fault-free." (p.5892)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a deep learning-based modeling framework"; "we address the aforementioned robustness issue by proposing"; "we propose a data-driven soft sensor modeling framework"
- demonstrate / causal / abstract, introduction: "We demonstrate our approach to the TE benchmark process"; "Experimental validation on two case studies ... demonstrates that the proposed model exhibits high resilience"
- show / causal / abstract, experiments: "show that robustness is achieved"; "The results show that on the original fault-free test data, the GRU-MSE achieves the lowest RMSE."
- could / speculative / conclusion: "future work could further expand the practicality of the method"

## Cross-section linkers

- introduction → method: "The rest of this article is outlined as follows. First, Section II briefly outlines the background of adversarial deep learning. Then, Section III explains the scope and methodology of the proposed method. Section IV describes the deep network architecture as well as the training algorithm for the soft sensor model. The case study is investigated in Section V and conclusions are drawn in Section VI." (p.5892)
- method → experiments: 训练超参后 `V. CASE STUDIES` (p.5895)
- experiments → conclusion: 计算代价后 `VI. CONCLUSION` (p.5900)

## Candidate rules

- R009 摘要用 `In this article, we propose` 点名零样本对抗框架。
- R002 Introduction 无独立 Related Work，鲁棒软测量与对抗学习评述写在引言中段。
- R004 贡献列表：`Overall, we summarize the contributions of our work as follows.`
- R003 Introduction 末用 `The rest of this article is outlined as follows`（outlined 变体）。
- R005 Conclusion 先收回方法，再用 `Hence, future work could` 指向过程故障。

## Candidate phrases

- `In this article, we propose a deep learning-based modeling framework` (abstract)
- `Overall, we summarize the contributions of our work as follows.` (introduction)
- `The rest of this article is outlined as follows.` (introduction)
- `In this article, we propose a data-driven soft sensor modeling framework` (conclusion)

## House style

自称 `In this article, we propose` / `our work` / `the proposed method`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.5891 abstract: Soft sensors are widely used in many industrial systems to monitor key variables that are difficult to measure, using measurements from other available physical sensors.
- p.5891 abstract: However, existing learning-based soft sensors are still vulnerable to sensor faults, which could deteriorate the performance of the models.
- p.5891 abstract: In this article, we propose a deep learning-based modeling framework for developing soft sensor models that are robust to sensor faults.
- p.5891 abstract: We demonstrate our approach to the TE benchmark process and a real industrial multiphase flow process and show that robustness is achieved as the accuracy does not degrade significantly when sensor faults are present during the model evaluation.
- p.5891 introduction: SENSORS are ubiquitous in industries as they are the eyes and ears for many processes and equipment.
- p.5891 introduction: However, some variables are inconvenient to measure due to reasons, such as high cost, slow response time, and other technical limitations.
- p.5891 introduction: However, one important issue that is yet to be addressed is the robustness of learning-based soft sensor models, in particular, robustness against sensor faults.
- p.5892 introduction: Although these works aimed to enhance the robustness of soft sensor models, they did not consider the issue of sensor faults.
- p.5892 introduction: Therefore, it would be highly beneficial if a soft sensor model can be trained to be robust against sensor faults under a zero-shot learning regime [13], that is, using only datasets that are fault-free.
- p.5892 introduction: Overall, we summarize the contributions of our work as follows.
- p.5892 introduction: The rest of this article is outlined as follows. First, Section II briefly outlines the background of adversarial deep learning. Then, Section III explains the scope and methodology of the proposed method. Section IV describes the deep network architecture as well as the training algorithm for the soft sensor model. The case study is investigated in Section V and conclusions are drawn in Section VI.
- p.5893 method: In general, the data-driven soft sensor is a multivariate regression problem, where it is desired to regress the difficult-to-measure variable (output) from other available physical sensor measurements (input).
- p.5895 experiments: In this section, we present case studies to evaluate the efficacy of our proposed method.
- p.5896 experiments: The results show that on the original fault-free test data, the GRU-MSE achieves the lowest RMSE.
- p.5897 experiments: Therefore, the results show that the proposed method is able to train a soft sensor model that is robust to sensor faults.
- p.5900 conclusion: In this article, we propose a data-driven soft sensor modeling framework based on adversarial learning to develop soft sensor models that are robust against sensor faults.
- p.5900 conclusion: Experimental results on the TEP and MFP datasets show that the proposed model achieves robustness as the accuracy does not degrade significantly when sensor faults are introduced during testing.
- p.5900 conclusion: Hence, future work could further expand the practicality of the method to handle the issue of process faults.
