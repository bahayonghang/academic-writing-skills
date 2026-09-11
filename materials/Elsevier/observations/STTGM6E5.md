---
key: STTGM6E5
title: "Short-term wind power forecasting model based on temporal convolutional network and Informer"
venue: "Energy"
doi: "10.1016/j.energy.2023.129171"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Methodology` → `3. Experimental preparation and framework` → `4. Experiment and analysis` → `5. Conclusion and future work`。前置 `ABSTRACT` 与 `Keywords` / `Abbreviations`。无独立 Related Work。`related_work=inlined`（Introduction 中段物理/统计/人工智能与混合模型、CNN-LSTM、TCN、Transformer/Informer）。Introduction 编号创新点 `(1)` / `(2)` / `(3)` + 节序路标。Method 含 Informer、TCN、AdaBelief。Experiments 标题为 `4. Experiment and analysis`（Kaggle 风电，多步对比 + 优化器对比）。

## Openers

- abstract: `Wind power forecast` — "Wind power forecast remains challenging owing to the unpredictable peculiarity of wind."
- introduction: `For a long` — "For a long time, human society has relied on fossil fuels as its primary source of energy."
- method: `Informer is a` — "Informer is a high-performance prediction algorithm built on Transformer enhancement."
- experiments: `In this experiment` — "In this experiment, we compare the proposed model with Informer, TCN, CNN, GRU, LSTM, XGBoost, and LightGBM."
- conclusion: `In this research` — "In this research, a hybrid prediction model based on TCN and Informer is suggested for wind power prediction."

## Gap transitions

- however (introduction): "However, wind power generation differs from traditional power generating methods in several ways, including seasonality, indirectness, and random fluctuation in wind energy, all of which contribute to the fact that wind power generation technology is more complex."
- however (introduction): "However, this method requires a number of historical statistics and suffers from relatively slow training speed and poor generalization ability."
- in conclusion (introduction): "In conclusion, most of the recent models for wind power prediction are based on neural networks, but these models could be more effective in handling long input sequences."
- although (conclusion): "Although the model proposed in this paper has improved in prediction accuracy, there are several drawbacks that deserve our attention"

## Hedge verbs

- proposes / causal / abstract: "This research proposes a hybrid prediction model based on a temporal convolutional network and an Informer"
- is suggested / causal / introduction, conclusion: "A hybrid prediction model based on TCN and Informer is suggested in this research"
- reveal / associative / abstract: "The findings reveal that the proposed model has the highest prediction accuracy and the best forecast effect."
- demonstrate / associative / introduction: "The experimental findings demonstrate that the model achieves optimal outcomes in all four evaluation metrics"
- can / speculative / conclusion: "the prediction model employing the AdaBelief optimizer can increase prediction accuracy and minimize prediction error"

## Cross-section linkers

- introduction → method: "The rest portions of the essay are arranged as follows: The second section explains the theoretical background of the model, including formula derivation as well as relevant principles."
- method → preparation: "In the third section, we introduce the pre-experimental planning and the experimental structure."
- preparation → experiments: "The outcomes of the experiments are mentioned in the fourth section." / `4. Experiment and analysis`
- experiments → conclusion: "The fifth section presents the experimental conclusions and prospects."

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest portions of the essay are arranged as follows`
- R004 编号贡献：`The innovative points of our research are as follows`
- R009 自称：`This research proposes` / `is suggested in this research` / `the model proposed in this paper`

## Candidate phrases

- `This research proposes a hybrid prediction model based on a temporal convolutional network and an Informer` (abstract)
- `A hybrid prediction model based on TCN and Informer is suggested in this research` (introduction)
- `The innovative points of our research are as follows` (introduction)
- `The rest portions of the essay are arranged as follows` (introduction)
- `In this research, a hybrid prediction model based on TCN and Informer is suggested` (conclusion)

## House style

自称 `This research proposes` / `is suggested in this research` / `the model proposed in this paper` / `we compare`。`this research` / `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Wind power forecast remains challenging owing to the unpredictable peculiarity of wind.
- abstract: This research proposes a hybrid prediction model based on a temporal convolutional network and an Informer to increase the accuracy of wind power forecasting.
- abstract: The findings reveal that the proposed model has the highest prediction accuracy and the best forecast effect.
- introduction: For a long time, human society has relied on fossil fuels as its primary source of energy.
- introduction: A hybrid prediction model based on TCN and Informer is suggested in this research.
- introduction: The rest portions of the essay are arranged as follows: The second section explains the theoretical background of the model, including formula derivation as well as relevant principles.
- experiments: In this experiment, we compare the proposed model with Informer, TCN, CNN, GRU, LSTM, XGBoost, and LightGBM.
- experiments: The hybrid model proposed in this paper is further optimized on the basis of Informer and achieves desirable results in each error index.
- conclusion: In this research, a hybrid prediction model based on TCN and Informer is suggested for wind power prediction.
- conclusion: The hybrid prediction model based on TCN and Informer outperforms other standard prediction models.
- conclusion: Although the model proposed in this paper has improved in prediction accuracy, there are several drawbacks that deserve our attention, and we consider the following aspects for future research.
