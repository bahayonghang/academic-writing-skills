---
key: N5YADJYY
title: "From Complexity to Clarity: Structural Process Knowledge-Informed Neural Network for Alumina Concentration Distribution Prediction"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2025.3574777"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROCESS ANALYSIS` → `III. METHOD` → `IV. RESULT AND DISCUSSION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 CFD / machine learning / PINN，再收束到 SPKINN）。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `RESULT AND DISCUSSION`。

## Openers

- abstract: `Maintaining an optimal` — "Maintaining an optimal alumina concentration distribution is crucial for ensuring stable operation and reducing energy consumption in aluminum electrolysis cells." (p.1)
- introduction: `AN OPTIMAL alumina` — "AN OPTIMAL alumina concentration distribution is a prerequisite for stable operation and high current efficiency in aluminum electrolysis cells [1], [2], [3]." (p.1；栏首掉字)
- method: `To enable efficient` — "To enable efficient and accurate prediction of alumina concentration distributions, this work proposes a knowledge-informed neural network architecture that improves the performance of the model in terms of reduced training time, improved predictive accuracy, and greater adaptability." (p.3)
- experiments: `In this section` — "In this section, we conduct a series of experiments on an alumina concentration distribution dataset to confirm the validity of our model with a variety of indicators and illustrations." (p.5, IV)
- conclusion: `To achieve efficient` — "To achieve efficient and accurate prediction of alumina concentration distributions, an SPKINN method is proposed in this article." (p.9)

## Gap transitions

- to address (abstract): "To address these issues, this article proposes a structural process knowledge-informed neural network for alumina concentration distribution prediction with desirable precision and high solving efficiency." (p.1)
- however (introduction): "However, due to the strong coupling of multiple physical fields inside the aluminum electrolysis cell and the complex process involving mass transfer, chemical reactions, and various factors governing the behavior of alumina in the electrolyte, predicting the alumina concentration distribution poses significant challenges [5], [6], [7]." (p.1)
- however (introduction): "PINN-related work has achieved outstanding results. However, these works often construct large-scale and complex deep learning networks with multiple hidden layers to find all possible relationships between inputs and outputs." (p.2)
- to address (introduction): "To address the abovementioned issues, we propose a structural process knowledge-informed neural network (SPKINN), aiming to fill the gap in efficient and accurate prediction of alumina concentration distributions, as illustrated in Fig. 1." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a structural process knowledge-informed neural network"; "we propose a structural process knowledge-informed neural network (SPKINN)"; "an SPKINN method is proposed in this article"
- demonstrate / causal / abstract: "Extensive experiments demonstrate that our method achieves significant performance improvements compared to some state-of-the-art methods."
- indicate / associative / conclusion: "Finally, extensive experimental results indicate that the proposed method has superior performance compared to some state-of-the-art methods."
- show / causal / experiments: "As shown in Table VI, the proposed SPKINN model exhibits the lowest prediction errors among the compared models"

## Cross-section linkers

- introduction → process analysis: "The rest of this article is organized as follows. Section II provides a detailed analysis of the key factors affecting alumina concentration distribution and derives the governing equation for alumina concentration distribution. Section III presents the proposed method in detail, including the flow field pretraining module, the concentration field pretraining module, and the process governing equation fusion training module. In Section IV, we discuss and compare the results of our experiments from several aspects with some state-of-the-art methods. Finally, Section V concludes this article." (p.3)
- method → experiments: 损失项段落后直接 `IV. RESULT AND DISCUSSION` (p.5)
- experiments → conclusion: Mode 2 段落后直接 `V. CONCLUSION` (p.9)

## Candidate rules

- R001 摘要贡献句用 `this article proposes` + 方法全称，不用 `Here we`。
- R002 Introduction 无独立 Related Work，CFD / ML / PINN 评述写在引言中段。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `the main contributions of this article are as follows` + 编号列表。
- R009 结论用 `an SPKINN method is proposed in this article` 收回方法。

## Candidate phrases

- `To address these issues, this article proposes` (abstract)
- `To address the abovementioned issues, we propose` (introduction)
- `the main contributions of this article are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `an SPKINN method is proposed in this article` (conclusion)

## House style

自称是 `this article proposes` / `this work proposes` / `we propose` / `our method`。未见 `Here we`、`In this paper`。`this article proposes` 与 `this work` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Maintaining an optimal alumina concentration distribution is crucial for ensuring stable operation and reducing energy consumption in aluminum electrolysis cells.
- p.1 abstract: To address these issues, this article proposes a structural process knowledge-informed neural network for alumina concentration distribution prediction with desirable precision and high solving efficiency.
- p.1 abstract: Extensive experiments demonstrate that our method achieves significant performance improvements compared to some state-of-the-art methods.
- p.1 introduction: AN OPTIMAL alumina concentration distribution is a prerequisite for stable operation and high current efficiency in aluminum electrolysis cells [1], [2], [3].
- p.1 introduction: However, due to the strong coupling of multiple physical fields inside the aluminum electrolysis cell and the complex process involving mass transfer, chemical reactions, and various factors governing the behavior of alumina in the electrolyte, predicting the alumina concentration distribution poses significant challenges [5], [6], [7].
- p.2 introduction: PINN-related work has achieved outstanding results. However, these works often construct large-scale and complex deep learning networks with multiple hidden layers to find all possible relationships between inputs and outputs.
- p.2 introduction: To address the abovementioned issues, we propose a structural process knowledge-informed neural network (SPKINN), aiming to fill the gap in efficient and accurate prediction of alumina concentration distributions, as illustrated in Fig. 1.
- p.2 introduction: To the best of the authors’ knowledge, this is the first work to achieve an efficient and accurate prediction of alumina concentration distributions.
- p.2 introduction: In summary, the main contributions of this article are as follows.
- p.3 introduction: The rest of this article is organized as follows. Section II provides a detailed analysis of the key factors affecting alumina concentration distribution and derives the governing equation for alumina concentration distribution. Section III presents the proposed method in detail, including the flow field pretraining module, the concentration field pretraining module, and the process governing equation fusion training module. In Section IV, we discuss and compare the results of our experiments from several aspects with some state-of-the-art methods. Finally, Section V concludes this article.
- p.3 method: To enable efficient and accurate prediction of alumina concentration distributions, this work proposes a knowledge-informed neural network architecture that improves the performance of the model in terms of reduced training time, improved predictive accuracy, and greater adaptability.
- p.5 experiments: In this section, we conduct a series of experiments on an alumina concentration distribution dataset to confirm the validity of our model with a variety of indicators and illustrations.
- p.5 experiments: Besides, we have demonstrated the effectiveness and superiority of the proposed model in the alumina concentration distribution prediction problem by comparing it with some state-of-the-art methods.
- p.9 experiments: As shown in Table VI, the proposed SPKINN model exhibits the lowest prediction errors among the compared models, with 6.053 × 10−2 for MRMSE, 2.410 × 10−2 for ML2, and 0.769 for MR2 .
- p.9 conclusion: To achieve efficient and accurate prediction of alumina concentration distributions, an SPKINN method is proposed in this article.
- p.9 conclusion: Finally, extensive experimental results indicate that the proposed method has superior performance compared to some state-of-the-art methods.
