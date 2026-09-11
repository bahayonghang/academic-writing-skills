---
key: YCSHC26Z
title: "A Temporal Convolutional-Based Kolmogorov-Arnold Network for Industrial Soft Sensor Modeling"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3578182"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,5-6,10-13"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. CONSTRUCTION OF THE SOFT SENSOR MODEL` → `IV. SIMULATION AND EXPERIMENT STUDY` → `V. CONCLUSIONS`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR / ICA / PLS / SVR / ELM / LSTM / CNN / TCN）。Introduction 末有 `The rest of this article is organized as follows`，指向 Section II–V。Method 在 III。Experiments 标题为 `SIMULATION AND EXPERIMENT STUDY`（BSM1 废水 + 烟气脱硫 + CO2 吸收塔）。

## Openers

- abstract: `Multi-timescale characteristics, nonlinearity` — "Multi-timescale characteristics, nonlinearity and dynamic features exist extensively in modern industrial processes, impairing the predictive performance and accuracy of soft sensor modeling for primary variables." (p.1)
- introduction: `ADVANCED control, decision-making` — "ADVANCED control, decision-making and optimization techniques play significant and irreplaceable roles in energy saving, green production and profit maximization within modern industrial processes [1]–[3]." (p.1；栏首掉字)
- method: `The proposed FAIT-KBiLSTM` — "The proposed FAIT-KBiLSTM model consists of a two-stage architecture to capture the intricate and dynamic coupling relationships among process variables while ensuring robust long-term prediction accuracy." (p.3, III)
- experiments: `This section presents` — "This section presents the simulation of the industrial wastewater treatment process (WWTP), along with experimental studies on flue gas desulfurization and CO2 absorption column processes." (p.5, IV)
- conclusion: `This article proposed` — "This article proposed a novel FAIT-KBiLSTM model to effectively leverage multiscale local spatiotemporal features for soft sensors in complex industrial processes." (p.12)

## Gap transitions

- to address (abstract): "To address this challenge, a multi-timescale neural network-based soft sensor model, consisting of two modules, is designed for complex industrial processes." (p.1)
- however (introduction): "However, in practical industrial processes, process variables often exhibit distinct local spatiotemporal characteristics due to the interconnected topological structures and physicochemical reactions at play." (p.2)
- despite (introduction): "Despite their effectiveness in extracting local correlations, these methods face limitations due to the restricted receptive fields imposed by the finite size of CNN convolution kernels." (p.2)
- however (introduction): "However, a common limitation of these methods lies in their use of shared convolutional filters across layers, which primarily capture the average temporal features from the data in the previous layer." (p.2)
- although (conclusion): "Although FAIT-KBiLSTM demonstrated strong performance in industrial soft sensor modeling, there remains room for further improvement." (p.12)

## Hedge verbs

- design / causal / abstract: "a multi-timescale neural network-based soft sensor model ... is designed"
- propose / causal / introduction: "this paper proposes an advanced soft-sensing method, called FAIT-KBiLSTM"
- demonstrate / causal / abstract, conclusion: "demonstrating promising potential for real-world applications"; "Experimental results ... demonstrated that FAIT-KBiLSTM outperforms existing models"
- show / causal / experiments: "Table IX shows the comparison of the prediction performance"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. The multi-scale characteristics of process variables is presented in Section II. In Section III, FAIT-KBiLSTM is described in detail, and it is also analyzed what roles the multiscale convolutional layers and attention mechanisms play in the prediction model. In Section IV, FAIT-KBiLSTM is applied in wastewater treatment process, flue gas desulfurization process and CO2 absorption column. In conclusion, Section V offers some final remarks." (p.3)
- method → experiments: KAN 公式后 `IV. SIMULATION AND EXPERIMENT STUDY` (p.5)
- experiments → conclusion: sensitivity 分析后 `V. CONCLUSIONS` (p.12)

## Candidate rules

- R001 abstract 用被动 `is designed` / `is validated`，少用 `we propose`。
- R002 Introduction 无独立 Related Work；贡献句用 `this paper proposes`，路标句改用 `The rest of this article is organized as follows`。
- R003 路标末句用 `In conclusion, Section V offers some final remarks.` 而非 `Section V concludes this article`。
- R005 Conclusion 标题为 `CONCLUSIONS`（复数），首句 `This article proposed a novel`，再用 `Although ... there remains room for further improvement` 与 `Future research will aim to`。

## Candidate phrases

- `To address this challenge, a ... model, consisting of two modules, is designed for` (abstract)
- `Inspired by the above works, this paper proposes an advanced soft-sensing method, called` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In conclusion, Section V offers some final remarks.` (introduction)
- `This article proposed a novel ... model to` (conclusion)
- `Future research will aim to refine network parameters and incorporate domain-specific knowledge` (conclusion)

## House style

自称混用 `this paper proposes`（引言）与 `this article` / `This article proposed`（路标与结论）。未见 `Here we`。`this paper proposes` 与 `This article proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Multi-timescale characteristics, nonlinearity and dynamic features exist extensively in modern industrial processes, impairing the predictive performance and accuracy of soft sensor modeling for primary variables.
- p.1 abstract: To address this challenge, a multi-timescale neural network-based soft sensor model, consisting of two modules, is designed for complex industrial processes.
- p.1 abstract: The superiority of the designed soft sensor model is validated through practical applications in wastewater treatment process and flue gas desulfurization, demonstrating promising potential for real-world applications.
- p.1 introduction: ADVANCED control, decision-making and optimization techniques play significant and irreplaceable roles in energy saving, green production and profit maximization within modern industrial processes [1]–[3].
- p.2 introduction: However, in practical industrial processes, process variables often exhibit distinct local spatiotemporal characteristics due to the interconnected topological structures and physicochemical reactions at play.
- p.2 introduction: Despite their effectiveness in extracting local correlations, these methods face limitations due to the restricted receptive fields imposed by the finite size of CNN convolution kernels.
- p.2 introduction: However, a common limitation of these methods lies in their use of shared convolutional filters across layers, which primarily capture the average temporal features from the data in the previous layer.
- p.2 introduction: Inspired by the above works, this paper proposes an advanced soft-sensing method, called FAIT-KBiLSTM, for industrial soft sensor modeling.
- p.3 introduction: The rest of this article is organized as follows. The multi-scale characteristics of process variables is presented in Section II. In Section III, FAIT-KBiLSTM is described in detail, and it is also analyzed what roles the multiscale convolutional layers and attention mechanisms play in the prediction model. In Section IV, FAIT-KBiLSTM is applied in wastewater treatment process, flue gas desulfurization process and CO2 absorption column. In conclusion, Section V offers some final remarks.
- p.3 method: The proposed FAIT-KBiLSTM model consists of a two-stage architecture to capture the intricate and dynamic coupling relationships among process variables while ensuring robust long-term prediction accuracy.
- p.5 experiments: This section presents the simulation of the industrial wastewater treatment process (WWTP), along with experimental studies on flue gas desulfurization and CO2 absorption column processes.
- p.12 conclusion: This article proposed a novel FAIT-KBiLSTM model to effectively leverage multiscale local spatiotemporal features for soft sensors in complex industrial processes.
- p.12 conclusion: Experimental results from wastewater treatment and flue gas desulfurization processes demonstrated that FAIT-KBiLSTM outperforms existing models in predicting quality variables.
- p.12 conclusion: Although FAIT-KBiLSTM demonstrated strong performance in industrial soft sensor modeling, there remains room for further improvement.
- p.12 conclusion: Future research will aim to refine network parameters and incorporate domain-specific knowledge into the models to enhance their performance.
