---
key: MKCMXU4T
title: "Time-aware rotary transformer for soft sensing of irregularly sampled industrial time sequences"
venue: "IEEE Internet of Things Journal"
doi: "10.1109/JIOT.2025.3558021"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. TIME-AWARE ROTARY TRANSFORMER` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 PLS/ELM/GPR、AE、RNN/LSTM/GRU、Transformer，再评 SIA-LSTM）。Introduction 末有节序路标，指向 II–V。Experiments 标题为 `CASE STUDY`（糖结晶过饱和度与纯度）。

## Openers

- abstract: `As modern industrial` — "As modern industrial processes increase in integration and scale, there exist intricate dynamic time variability and nonlinearity within process data." (p.1)
- introduction: `INDUSTRIAL processes are` — "INDUSTRIAL processes are currently undergoing transformation and upgrades to meet the growing demand for environmentally sustainable production and high-quality products." (p.1；栏首掉字)
- method: `To address the` — "To address the nonuniform sampling issue, the TART-based soft sensor is proposed in this section, which consists of the SIE layer and TARA mechanism." (p.3, III)
- experiments: `In this section,` — "In this section, the feasibility and efficacy of the proposed TART are demonstrated via an actual-run sugar crystallization process." (p.6, IV)
- conclusion: `In this article,` — "In this article, a TART was proposed for soft sensing of irregularly sampled industrial sequence data." (p.11)

## Gap transitions

- nevertheless (abstract): "Nevertheless, process data gathered from industrial plants are usually sampled at irregular intervals, posing a challenge for most mainstream dynamic models to handle the resulting temporally changeable relations in process sequence data." (p.1)
- thus (abstract): "Thus, this article proposes a time-aware rotary Transformer (TART) for soft sensor modeling of irregular sampled time series in industrial processes, which adaptively and efficiently model the temporally changeable dynamics among series data." (p.1)
- although (introduction): "Although these dynamic modeling approaches can extract temporal dependencies from time-series data, most assume that data samples are taken at regular intervals." (p.2)
- however (introduction): "However, in industrial processes, maintaining a uniform sampling interval is challenging due to various operational constraints." (p.2)
- to-address (introduction): "To address this issue, a sampling interval-aware LSTM [21] was proposed to model relations between the previous and current samples via assigning interval-based weights into hidden states." (p.2)
- however (introduction): "However, these methods do not explicitly incorporate timestamp information, limiting their abilities to fully capture temporally changeable correlations." (p.2)

## Hedge verbs

- proposes / causal / abstract: "this article proposes a time-aware rotary Transformer (TART)"
- is proposed / causal / introduction, method: "a time-aware rotary Transformer (TART) is proposed"; "the TART-based soft sensor is proposed in this section"
- demonstrating / causal / abstract: "demonstrating its feasibility and efficacy for soft sensing of practical industrial processes"
- are demonstrated / causal / experiments: "the feasibility and efficacy of the proposed TART are demonstrated"
- was proposed / past / conclusion: "a TART was proposed for soft sensing"
- is clearly validated / causal / conclusion: "the effectiveness of the proposed TART is clearly validated"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is structured as follows. In Section II, the self-attention mechanism and transformer architecture are briefly introduced. Details of the proposed TART are given in Section III. Then, in Section IV, the effectiveness of TART is demonstrated by an actual sugar crystallization process. Eventually, Section V concludes this article." (p.2)
- preliminaries → method: Transformer 结构后直接 `III. TIME-AWARE ROTARY TRANSFORMER` (p.3)
- method → experiments: 式 (33) 与 Fig. 6 后 `IV. CASE STUDY` (p.6)
- experiments → conclusion: 消融段落后直接 `V. CONCLUSION` (p.11)

## Candidate rules

- R001 摘要缺口链：`Nevertheless` 不规则采样 + `Thus, this article proposes` 方法缩写。
- R002 Introduction 无独立 Related Work；动态模型与不规则采样评述写在引言中段。
- R003 贡献用 `The contributions of this article are as follows.` + 编号列表。
- R004 Introduction 末用 `The rest of this article is structured as follows.` 指向 II–V。
- R005 Conclusion 用过去式 `In this article, a TART was proposed`，再用 `As demonstrated by experiments` 收回。

## Candidate phrases

- `Thus, this article proposes a` (abstract)
- `The contributions of this article are as follows.` (introduction)
- `The rest of this article is structured as follows.` (introduction)
- `To address the nonuniform sampling issue, the TART-based soft sensor is proposed in this section` (method)
- `In this article, a TART was proposed` (conclusion)

## House style

自称是 `this article` / `In this article` / `we propose TARA` / `the proposed TART`。未见 `Here we`。`this article proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: As modern industrial processes increase in integration and scale, there exist intricate dynamic time variability and nonlinearity within process data.
- p.1 abstract: Nevertheless, process data gathered from industrial plants are usually sampled at irregular intervals, posing a challenge for most mainstream dynamic models to handle the resulting temporally changeable relations in process sequence data.
- p.1 abstract: Thus, this article proposes a time-aware rotary Transformer (TART) for soft sensor modeling of irregular sampled time series in industrial processes, which adaptively and efficiently model the temporally changeable dynamics among series data.
- p.1 abstract: In comparison with recent predictive modeling methods, the proposed TART achieves state-of-the-art performance, demonstrating its feasibility and efficacy for soft sensing of practical industrial processes.
- p.1 introduction: INDUSTRIAL processes are currently undergoing transformation and upgrades to meet the growing demand for environmentally sustainable production and high-quality products.
- p.1 introduction: To address this problem, soft sensor techniques [2], [3] have been developed to predict hard-to-measure quality variables by constructing inferential models based on easily measurable process variables.
- p.2 introduction: Although these dynamic modeling approaches can extract temporal dependencies from time-series data, most assume that data samples are taken at regular intervals.
- p.2 introduction: However, these methods do not explicitly incorporate timestamp information, limiting their abilities to fully capture temporally changeable correlations.
- p.2 introduction: In this article, a time-aware rotary Transformer (TART) is proposed to make full use of the changeable yet crucial sampling intervals for prediction performance enhancement.
- p.2 introduction: The contributions of this article are as follows.
- p.2 introduction: The rest of this article is structured as follows. In Section II, the self-attention mechanism and transformer architecture are briefly introduced. Details of the proposed TART are given in Section III. Then, in Section IV, the effectiveness of TART is demonstrated by an actual sugar crystallization process. Eventually, Section V concludes this article.
- p.3 method: To address the nonuniform sampling issue, the TART-based soft sensor is proposed in this section, which consists of the SIE layer and TARA mechanism.
- p.6 experiments: In this section, the feasibility and efficacy of the proposed TART are demonstrated via an actual-run sugar crystallization process.
- p.8 experiments: The proposed TART model outperforms its peers, achieving a low RMSE of 0.00442, a MAE of 0.00347, and a high R2 of 0.99317.
- p.11 conclusion: In this article, a TART was proposed for soft sensing of irregularly sampled industrial sequence data.
- p.11 conclusion: As demonstrated by experiments conducted on a real-world sugar crystallization process, the effectiveness of the proposed TART is clearly validated.
