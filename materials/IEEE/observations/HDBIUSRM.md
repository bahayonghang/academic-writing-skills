---
key: HDBIUSRM
title: "A Complementary Continual Learning Framework Using Incremental Samples for Remaining Useful Life Prediction of Machinery"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3450077"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARY` → `III. PROPOSED COMPLEMENTARY CONTINUAL LEARNING FRAMEWORK USING INCREMENTAL SAMPLES FOR RUL PREDICTION OF MACHINERY` → `IV. EXPERIMENTAL VERIFICATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 CNN/RNN RUL、Cao/Que/EWC 持续学习；II.A 再分类 replay/parameter isolation/regularization）。Introduction 末有节序路标，指向 II–V。II 为持续学习与网络预备，不是综述节。Experiments 标题为 `EXPERIMENTAL VERIFICATION`。

## Openers

- abstract: `Continual learning is` — "Continual learning is gaining special attention in remaining useful life (RUL) prediction of machinery recently, which enables deep prognostics networks to use incremental samples to progressively improve network performance without laborious retraining." (p.1)
- introduction: `PROGNOSTICS and health` — "PROGNOSTICS and health management (PHM) technology is becoming increasingly important in modern industry, and remaining useful life (RUL) prediction is an important research as a key component of PHM technology [1]." (p.1；栏首掉字)
- method: `This article constructs` — "This article constructs a complementary continual learning framework for RUL prediction of machinery using incremental samples." (p.3, III.A)
- experiments: `In this section` — "In this section, run-to-failure data collected from accelerated degradation tests of rolling element bearings are used to verify the effectiveness of the proposed continual learning framework." (p.6)
- conclusion: `In this article` — "In this article, a complementary continual learning framework was proposed for RUL prediction of machinery using incremental samples." (p.10)

Preliminaries 首句："Deep networks often suffering from catastrophic forgetting when trained with new data." (p.2, II.A)。不单列 `related_work` opener。

## Gap transitions

- nonetheless (abstract): "Nonetheless, current studies exhibit several constraints: 1) An explicit mechanism is lacking in preventing the loss of pivotal memories after multiple continual learning stages. 2) A sampling-enhanced replay technique is lacking for continual learning-based RUL prediction." (p.1)
- to address (abstract): "To address the abovementioned limitations, this article proposes a complementary continual learning framework for RUL prediction of machinery, which contains two novel characteristics, i.e., long-term potentiation and associative replay." (p.1)
- however (introduction): "However, in real industrial applications, it is exceptionally difficult to construct complete training datasets in the short term because of the extremely long cycle of collecting run-to-failure data and the variety of machinery degradation modes." (p.1)
- therefore (introduction): "Therefore, it is expected to endow deep prognostics networks with incremental learning ability, aiming to gradually learn from newly collected datasets and incrementally improving performance without time-consuming retraining." (p.1)
- although (introduction): "Although continual learning-based prognostics methods have shown encouraging results, there are still some limitations as follows:" (p.2)
- to tackle (introduction): "To tackle the aforementioned limitations, this article proposes a complementary continual learning framework for RUL prediction that utilizes incremental samples to incrementally improve performance." (p.2)
- therefore (conclusion): "Therefore, in our future works, we will focus on how to design specialized mechanisms to incorporate RUL prediction properties into continual learning" (p.10)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article proposes a complementary continual learning framework"; "a complementary continual learning framework was proposed"
- indicate / associative / abstract: "Experimental results indicate that the proposed framework can possess lower forgetting"
- show / causal / experiments, conclusion: "The above results show that the introduction of the long-term potentiation mechanism"; "Experiment results showed that the proposed framework can possess lower forgetting"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II provides the preliminary. Section III details the proposed complementary continual learning framework. Section IV validates the proposed framework by performing RUL prediction of bearings and comparing it with existing state-of-the-art methods. Finally, Section V concludes this article." (p.2)
- method → experiments: "Furthermore, the coenhancement of long-term potentiation and associative replay will be experimentally demonstrated in the subsequent section." 随后 `IV. EXPERIMENTAL VERIFICATION` (p.6)
- experiments → conclusion: SOTA 比较后直接 `V. CONCLUSION` (p.10)

## Candidate rules

- R001 摘要用 `this article proposes`，缺口用 `To address the abovementioned limitations`。
- R002 Related Work 并入 Introduction；II 是 PRELIMINARY。
- R003 Introduction 末 `The rest of this article is organized as follows`。
- R004 贡献为编号列表（长时程增强、联想回放、互补框架）。
- R005 结论 `The proposed framework still lacks` + `Therefore, in our future works`。

## Candidate phrases

- `To address the abovementioned limitations, this article proposes` (abstract)
- `To tackle the aforementioned limitations, this article proposes` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, a complementary continual learning framework was proposed` (conclusion)
- `Therefore, in our future works, we will focus on` (conclusion)

## House style

自称 `this article proposes` / `This article constructs` / `In this article` / `the proposed framework`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Continual learning is gaining special attention in remaining useful life (RUL) prediction of machinery recently, which enables deep prognostics networks to use incremental samples to progressively improve network performance without laborious retraining.
- p.1 abstract: Nonetheless, current studies exhibit several constraints: 1) An explicit mechanism is lacking in preventing the loss of pivotal memories after multiple continual learning stages. 2) A sampling-enhanced replay technique is lacking for continual learning-based RUL prediction.
- p.1 abstract: To address the abovementioned limitations, this article proposes a complementary continual learning framework for RUL prediction of machinery, which contains two novel characteristics, i.e., long-term potentiation and associative replay.
- p.1 abstract: Experimental results indicate that the proposed framework can possess lower forgetting and achieve better prognostics performance reinforcement during continual learning.
- p.1 introduction: PROGNOSTICS and health management (PHM) technology is becoming increasingly important in modern industry, and remaining useful life (RUL) prediction is an important research as a key component of PHM technology [1].
- p.1 introduction: However, in real industrial applications, it is exceptionally difficult to construct complete training datasets in the short term because of the extremely long cycle of collecting run-to-failure data and the variety of machinery degradation modes.
- p.2 introduction: Although continual learning-based prognostics methods have shown encouraging results, there are still some limitations as follows:
- p.2 introduction: To tackle the aforementioned limitations, this article proposes a complementary continual learning framework for RUL prediction that utilizes incremental samples to incrementally improve performance.
- p.2 introduction: The rest of this article is organized as follows. Section II provides the preliminary. Section III details the proposed complementary continual learning framework. Section IV validates the proposed framework by performing RUL prediction of bearings and comparing it with existing state-of-the-art methods. Finally, Section V concludes this article.
- p.3 method: This article constructs a complementary continual learning framework for RUL prediction of machinery using incremental samples.
- p.6 method-close: Furthermore, the coenhancement of long-term potentiation and associative replay will be experimentally demonstrated in the subsequent section.
- p.6 experiments: In this section, run-to-failure data collected from accelerated degradation tests of rolling element bearings are used to verify the effectiveness of the proposed continual learning framework.
- p.10 conclusion: In this article, a complementary continual learning framework was proposed for RUL prediction of machinery using incremental samples.
- p.10 conclusion: The proposed framework still lacks some mechanisms tailored to degradation processes of machinery.
- p.10 conclusion: Therefore, in our future works, we will focus on how to design specialized mechanisms to incorporate RUL prediction properties into continual learning, consider the dynamic nature of degradation processes and the variety of the degradation modes, and develop interpretable continual learning-based RUL prediction methods.
