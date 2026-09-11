---
key: 3L3GTH4E
title: "Deep fusion of time series and visual data through temporal Features: A soft-sensor model for FeO content in sintering process"
venue: "Expert Systems with Applications"
doi: "10.1016/j.eswa.2024.126243"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-11"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Methodology`（`2.1. Time series branch` / `2.2` 图像支路 / `2.3. Df-transformer`）→ `3. Experiments`（`3.1. Dataset Introduction` / `3.2. Experimental results and analysis` / `3.3. Ablation experiments` / `3.4. Hyperparameter tuning` / `3.5. Discussion`）。前置 `ABSTRACT` 与 `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 RNN 软测量、多模态融合四类与烧结 FeO 文献）。Introduction 末有编号贡献 + 节序路标。正文无独立 `4. Conclusion`；讨论节收束后接利益声明。

## Openers

- abstract: `The ferrous oxide` — "The ferrous oxide (FeO) content in finished sinter is a key indicator of the thermal reaction state and plays a pivotal role in quality control of the iron ore sintering process."
- introduction: `Ferrous oxide (FeO)` — "Ferrous oxide (FeO) content of sinter is a thermal-state index in the iron ore sintering process, which directly determines the strength, reducibility, productivity, and reduction degradation index of finished sinter, and is of great significance for the subsequent production of iron products (Umadevi et al., 2012)."
- method: `The proposed DF-Transformer` — "The proposed DF-Transformer model is introduced from the following three parts: the time series branch, the image branch, and the overall model architecture, respectively."
- experiments: `The experimental dataset` — "The experimental dataset was provided by the literature (Yang et al., 2023)."
- conclusion: `The proposed DF-Transformer` — "The proposed DF-Transformer model presents significant innovations and contributions in several aspects, emphasizing its unique approach to addressing the challenges of multi-modal data fusion for industrial processes:" (s.3.5)

## Gap transitions

- however (abstract): "However, the sintering process generates multi-source heterogeneous data, which presents significant challenges for efficient information extraction."
- to address (abstract): "To address these challenges, we propose a dual-branch deep-fusion architecture that concurrently processes time series and image data, thereby maximizing the utilization of process information to enhance soft-sensor accuracy."
- however (introduction): "However, the above studies only considered the single-modal time series data, ignoring the information provided by the image data."
- in this paper (introduction): "In this paper, a dual-branch deep-fusion Transformer (DF-Transformer) architecture of time series and vision is proposed for FeO content soft sensor in sinter."

## Hedge verbs

- propose / causal / abstract, introduction: "we propose a dual-branch deep-fusion architecture"; "a dual-branch deep-fusion Transformer (DF-Transformer) architecture of time series and vision is proposed"
- demonstrate / associative / abstract: "Evaluations on a real-world sintering process dataset demonstrate the robustness, flexibility, and efficiency of the proposed deep-fusion architecture."
- show / associative / experiments: "it shows the highest soft-sensor accuracy, reflecting the benefits of deep-fusion"

## Cross-section linkers

- introduction → method: "The rest of this paper is outlined as follows. Section 2 presents the design details of the DF-Transformer algorithm for soft sensing of FeO content in sinter. Section 3 shows the experimental results and analysis on a real industrial case. Section 4 provides some conclusions."
- method → experiments: `3. Experiments` / `3.1. Dataset Introduction`
- experiments → close: `3.5. Discussion` 后接利益声明；正文无独立 Section 4。

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is outlined as follows`
- R004 编号贡献：`The contributions of this work are as follows`
- R009 自称：`we propose` / `In this paper` / `is proposed`

## Candidate phrases

- `To address these challenges, we propose` (abstract)
- `In this paper, a dual-branch deep-fusion Transformer (DF-Transformer) architecture of time series and vision is proposed` (introduction)
- `The contributions of this work are as follows` (introduction)
- `The rest of this paper is outlined as follows` (introduction)
- `The proposed DF-Transformer model presents significant innovations` (s.3.5)

## House style

自称 `we propose` / `In this paper` / `the proposed DF-Transformer`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: The ferrous oxide (FeO) content in finished sinter is a key indicator of the thermal reaction state and plays a pivotal role in quality control of the iron ore sintering process.
- abstract: However, the sintering process generates multi-source heterogeneous data, which presents significant challenges for efficient information extraction.
- abstract: To address these challenges, we propose a dual-branch deep-fusion architecture that concurrently processes time series and image data, thereby maximizing the utilization of process information to enhance soft-sensor accuracy.
- abstract: Evaluations on a real-world sintering process dataset demonstrate the robustness, flexibility, and efficiency of the proposed deep-fusion architecture.
- introduction: Ferrous oxide (FeO) content of sinter is a thermal-state index in the iron ore sintering process, which directly determines the strength, reducibility, productivity, and reduction degradation index of finished sinter, and is of great significance for the subsequent production of iron products (Umadevi et al., 2012).
- introduction: However, the above studies only considered the single-modal time series data, ignoring the information provided by the image data.
- introduction: In this paper, a dual-branch deep-fusion Transformer (DF-Transformer) architecture of time series and vision is proposed for FeO content soft sensor in sinter.
- introduction: The contributions of this work are as follows:
- introduction: The rest of this paper is outlined as follows. Section 2 presents the design details of the DF-Transformer algorithm for soft sensing of FeO content in sinter.
- method: The proposed DF-Transformer model is introduced from the following three parts: the time series branch, the image branch, and the overall model architecture, respectively.
- experiments: The experimental dataset was provided by the literature (Yang et al., 2023).
- experiments: Specifically, the values of RMSE and R2 provided by DF-Transformer are 0.037 and 0.838, respectively.
- discussion: The proposed DF-Transformer model presents significant innovations and contributions in several aspects, emphasizing its unique approach to addressing the challenges of multi-modal data fusion for industrial processes:
- discussion: In summary, the DF-Transformer presents a significant advancement in soft-sensing by effectively fusing heterogeneous data sources, reducing computational costs, and offering flexibility for future modifications.
