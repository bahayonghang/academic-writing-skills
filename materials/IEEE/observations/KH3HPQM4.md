---
key: KH3HPQM4
title: "Improved Bi-LSTM With Distributed Nonlinear Extensions and Parallel Inputs for Soft Sensing"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2023.3313631"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-8"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. PROPOSED METHOD` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评机理/数据驱动软测量、FFNN/ELM、RNN/LSTM/Bi-LSTM）。Introduction 末有编号贡献与节序路标，指向 Section II–V。Method 标题为 `PROPOSED METHOD`。Experiments 标题为 `CASE STUDY`（硫回收装置 SRU，H2S）。

## Openers

- abstract: `Industrial soft sensing` — "Industrial soft sensing models have found extensive application in predicting key process variables that are challenging to directly measure." (p.3748)
- introduction: `IN INDUSTRIAL processes` — "IN INDUSTRIAL processes, the accurate measurement of process variables holds significant importance for the tasks, such as precise modeling, intelligent control, and process optimization [1], [2], [3]." (p.3748；栏首掉字)
- method: `For highly nonlinear` — "For highly nonlinear industrial data, input variables of various dimensions may exhibit distinct correlations and effects on the output." (p.3750)
- experiments: `In this section` — "In this section, for assessing the efficacy of the presented DNEPI-Bi-LSTM-based soft sensing, an actual industrial process known as the SRU is used." (p.3752)
- conclusion: `In this article` — "In this article, an enhanced Bi-LSTM model based on DNEPI-Bi-LSTM is proposed for constructing the soft sensing model for complex industrial processes." (p.3754)

## Gap transitions

- however (abstract): "However, the effectiveness of conventional soft sensing models is impacted by the intricate characteristics of process variables, such as high nonlinearity, coupling, and complex dynamicity." (p.3748)
- to address (abstract): "To address this limitation, an enhanced bidirectional long short-term memory (Bi-LSTM) model based on distributed nonlinear extensions integrated with parallel inputs (DNEPI-Bi-LSTM) is proposed for constructing the soft sensing model." (p.3748)
- although (introduction): "Although the above models and their extensions have been successfully applied in many fields, the relationship between the inputs and outputs is ignored, limiting the performance of the above methods." (p.3749)
- to address (introduction): "To address this limitation, this article proposes an enhanced Bi-LSTM model based on distributed nonlinear extensions integrated with parallel inputs (DNEPI-Bi-LSTM) for constructing the industrial soft sensing model." (p.3749)

## Hedge verbs

- propose / causal / abstract, introduction, method, conclusion: "an enhanced ... (DNEPI-Bi-LSTM) is proposed"; "this article proposes an enhanced Bi-LSTM"; "an enhanced Bi-LSTM model based on DNEPI-Bi-LSTM is proposed"
- illustrate / causal / abstract, experiments, conclusion: "Simulation results illustrate that DNEPI-Bi-LSTM outperforms other advanced models"
- confirm / causal / experiments: "confirming that the Bi-LSTM can better handle the complex SRU dataset"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Section II briefly introduces ELM and Bi-LSTM. Section III provides the details about the proposed DNEPI-Bi-LSTM-based industrial soft sensing. Section IV contains one real industrial case SRU to confirm the effectiveness of the proposed DNEPI-Bi-LSTM-based industrial soft sensing. Finally, Section V concludes this article." (p.3749)
- method → experiments: 指标定义后直接 `IV. CASE STUDY` (p.3752)
- experiments → conclusion: 误差箱线图段落后直接 `V. CONCLUSION` (p.3754)

## Candidate rules

- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R004 贡献用 `the main contributions are summarized as follows.` + 编号。
- R007 摘要用 `To address this limitation, ... is proposed` 点名方法缩写。
- R005 结论后续：`In the future work, other nonlinear extension methods will be considered`。

## Candidate phrases

- `To address this limitation, an enhanced ... is proposed` (abstract)
- `the main contributions are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this article, an enhanced Bi-LSTM model based on DNEPI-Bi-LSTM is proposed` (conclusion)
- `In the future work, other nonlinear extension methods will be considered` (conclusion)

## House style

自称 `this article proposes` / `In this article` / `the proposed DNEPI-Bi-LSTM`。未见 `Here we`。`is proposed` 与 `In this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.3748 abstract: Industrial soft sensing models have found extensive application in predicting key process variables that are challenging to directly measure.
- p.3748 abstract: However, the effectiveness of conventional soft sensing models is impacted by the intricate characteristics of process variables, such as high nonlinearity, coupling, and complex dynamicity.
- p.3748 abstract: To address this limitation, an enhanced bidirectional long short-term memory (Bi-LSTM) model based on distributed nonlinear extensions integrated with parallel inputs (DNEPI-Bi-LSTM) is proposed for constructing the soft sensing model.
- p.3748 abstract: Simulation results illustrate that DNEPI-Bi-LSTM outperforms other advanced models in terms of accuracy, showcasing its potential in industrial applications.
- p.3748 introduction: IN INDUSTRIAL processes, the accurate measurement of process variables holds significant importance for the tasks, such as precise modeling, intelligent control, and process optimization [1], [2], [3].
- p.3749 introduction: Although the above models and their extensions have been successfully applied in many fields, the relationship between the inputs and outputs is ignored, limiting the performance of the above methods.
- p.3749 introduction: To address this limitation, this article proposes an enhanced Bi-LSTM model based on distributed nonlinear extensions integrated with parallel inputs (DNEPI-Bi-LSTM) for constructing the industrial soft sensing model.
- p.3749 introduction: In this article, the main contributions are summarized as follows.
- p.3749 introduction: The rest of this article is organized as follows. Section II briefly introduces ELM and Bi-LSTM. Section III provides the details about the proposed DNEPI-Bi-LSTM-based industrial soft sensing. Section IV contains one real industrial case SRU to confirm the effectiveness of the proposed DNEPI-Bi-LSTM-based industrial soft sensing. Finally, Section V concludes this article.
- p.3750 method: For highly nonlinear industrial data, input variables of various dimensions may exhibit distinct correlations and effects on the output.
- p.3752 experiments: In this section, for assessing the efficacy of the presented DNEPI-Bi-LSTM-based soft sensing, an actual industrial process known as the SRU is used.
- p.3754 conclusion: In this article, an enhanced Bi-LSTM model based on DNEPI-Bi-LSTM is proposed for constructing the soft sensing model for complex industrial processes.
- p.3754 conclusion: Simulation results illustrate that DNEPI-Bi-LSTM outperforms other advanced models in terms of accuracy, showcasing its potential in industrial applications
- p.3754 conclusion: In the future work, other nonlinear extension methods will be considered for further improving the prediction performance of the presented methodology.
