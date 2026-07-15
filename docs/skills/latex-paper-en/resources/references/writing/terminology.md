# Academic Terminology Reference


## Table of contents

- [Usage / Instructions for use](#usage-使用说明)
- [1. Deep Learning / Deep Learning](#1-deep-learning-深度学习)
  - [1.1 Basic Concepts / Basic Concepts](#11-basic-concepts-基础概念)
  - [1.2 Training / Training related](#12-training-训练相关)
  - [1.3 Model Architecture / Model Architecture](#13-model-architecture-模型架构)
- [2. Time Series / Time Series](#2-time-series-时间序列)
  - [2.1 Basic Concepts / Basic Concepts](#21-basic-concepts-基础概念)
  - [2.2 Analysis Methods / Analysis Methods](#22-analysis-methods-分析方法)
  - [2.3 Models / Model](#23-models-模型)
  - [2.4 Evaluation / Evaluation Index](#24-evaluation-评估指标)
- [3. Industrial Control / Industrial Control](#3-industrial-control-工业控制)
  - [3.1 Basic Concepts / Basic Concepts](#31-basic-concepts-基础概念)
  - [3.2 Control Methods / Control Methods](#32-control-methods-控制方法)
  - [3.3 Industrial Systems / Industrial Systems](#33-industrial-systems-工业系统)
  - [3.4 Fault & Anomaly / Fault and Anomaly](#34-fault-anomaly-故障与异常)
  - [3.5 Data Characteristics / Data Characteristics](#35-data-characteristics-数据特性)
- [4. Cross-Domain Terms / Cross-Domain Terms](#4-cross-domain-terms-跨领域术语)
  - [4.1 General Academic / General Academic](#41-general-academic-通用学术)
  - [4.2 Data & Processing / Data & Processing](#42-data-processing-数据与处理)
- [5. Usage Examples / Usage Examples](#5-usage-examples-使用示例)
  - [❌ Chinglish → ✅ Academic English](#chinglish-academic-english)
- [Notes / Notes](#notes-备注)

---

> Academic terminology comparison list - deep learning, time series, industrial control field

## Usage/Instructions for use

When translating Chinese academic text to English, refer to this terminology list to ensure:
1. Consistent terminology throughout the paper
2. Domain-appropriate expressions
3. Commonly accepted translations in the field

---

## 1. Deep Learning / Deep Learning

### 1.1 Basic Concepts/Basic Concepts

|Chinese|English|Notes|
|------|---------|-------|
|deep learning|deep learning| |
|neural network|neural network| |
|convolutional neural network|convolutional neural network (CNN)| |
|recurrent neural network|recurrent neural network (RNN)| |
|long short term memory network|long short-term memory (LSTM)| |
|gated loop unit|gated recurrent unit (GRU)| |
|Transformer|Transformer|Keep the original text, capitalize the first letter|
|attention mechanism|attention mechanism| |
|self-attention|self-attention| |
|bullish attention|multi-head attention| |
|feedforward neural network|feed-forward neural network| |
|residual connection|residual connection / skip connection| |
|layer normalization|layer normalization| |
|batch normalization|batch normalization| |

### 1.2 Training / training related

|Chinese|English|Notes|
|------|---------|-------|
|loss function|loss function| |
|optimizer|optimizer| |
|learning rate|learning rate| |
|gradient descent|gradient descent| |
|Backpropagation|backpropagation| |
|overfitting|overfitting| |
|Underfitting|underfitting| |
|regularization|regularization| |
|Dropout|dropout|lower case|
|Stop early|early stopping| |
|weight decay|weight decay| |
|batch size|batch size| |
|Round/Cycle|epoch| |
|convergence|convergence| |
|gradient disappears|vanishing gradient| |
|gradient explosion|exploding gradient| |

### 1.3 Model Architecture / Model Architecture

|Chinese|English|Notes|
|------|---------|-------|
|encoder|encoder| |
|decoder|decoder| |
|embedding layer|embedding layer| |
|Hidden layer|hidden layer| |
|output layer|output layer| |
|activation function|activation function| |
|Pooling|pooling| |
|Fully connected layer|fully connected layer / dense layer| |
|Feature extraction|feature extraction| |
|Feature fusion|feature fusion| |
|multi-scale|multi-scale| |
|end-to-end|end-to-end| |

---

## 2. Time Series / time series

### 2.1 Basic Concepts/Basic Concepts

|Chinese|English|Notes|
|------|---------|-------|
|time series|time series| |
|Time series data|temporal data / time-series data| |
|time step|time step| |
|sliding window|sliding window| |
|Timestamp|timestamp| |
|Sampling frequency|sampling frequency/sampling rate| |
|Sampling interval|sampling interval| |

### 2.2 Analysis Methods / Analysis methods

|Chinese|English|Notes|
|------|---------|-------|
|Time series prediction|time series forecasting| |
|single step prediction|single-step prediction| |
|multi-step forecast|multi-step prediction| |
|long term forecast|long-term forecasting| |
|short term forecast|short-term forecasting| |
|trend|trend| |
|Seasonal|seasonality| |
|cyclical|periodicity/cyclicity| |
|stationarity|stationarity| |
|autocorrelation|autocorrelation| |
|lag|lag| |
|difference|differencing| |

### 2.3 Models/models

|Chinese|English|Notes|
|------|---------|-------|
|autoregressive model|autoregressive model (AR)| |
|moving average|moving average (MA)| |
|autoregressive moving average|ARMA| |
|Autoregressive integrated moving average|ARIMA| |
|Exponential smoothing|exponential smoothing| |
|Timing decomposition|time series decomposition| |
|state space model|state space model| |
|TimingTransformer|Temporal Transformer| |
|Sequential convolutional network|temporal convolutional network (TCN)| |

### 2.4 Evaluation / evaluation indicators

|Chinese|English|Notes|
|------|---------|-------|
|mean square error|mean squared error (MSE)| |
|root mean square error|root mean squared error (RMSE)| |
|mean absolute error|mean absolute error (MAE)| |
|mean absolute percentage error|mean absolute percentage error (MAPE)| |
|Symmetric mean absolute percentage error|symmetric MAPE (sMAPE)| |
|coefficient of determination|coefficient of determination (R²)| |

---

## 3. Industrial Control / Industrial Control

### 3.1 Basic Concepts/Basic Concepts

|Chinese|English|Notes|
|------|---------|-------|
|Industrial control system|industrial control system (ICS)| |
|process control|process control| |
|control loop|control loop| |
|closed loop control|closed-loop control| |
|open loop control|open-loop control| |
|feedback control|feedback control| |
|Feedforward control|feedforward control| |
|set value|setpoint| |
|process variables|process variable (PV)| |
|control variables|control variable / manipulated variable (MV)| |
|disturbance|disturbance| |

### 3.2 Control Methods/Control Methods

|Chinese|English|Notes|
|------|---------|-------|
|PID control|PID control| |
|Proportional control|proportional control| |
|Integral control|integral control| |
|Differential control|derivative control| |
|model predictive control|model predictive control (MPC)| |
|adaptive control|adaptive control| |
|Robust control|robust control| |
|optimal control|optimal control| |
|Intelligent control|intelligent control| |

### 3.3 Industrial Systems / Industrial Systems

|Chinese|English|Notes|
|------|---------|-------|
|programmable logic controller|programmable logic controller (PLC)| |
|Distributed control system|distributed control system (DCS)| |
|Monitoring and data collection|SCADA|Supervisory Control and Data Acquisition|
|Human-computer interface|human-machine interface (HMI)| |
|sensor|sensor| |
|actuator|actuator| |
|Frequency converter|variable frequency drive (VFD)| |

### 3.4 Fault & Anomaly / Fault and Anomaly

|Chinese|English|Notes|
|------|---------|-------|
|fault detection|fault detection| |
|Troubleshooting|fault diagnosis| |
|Failure prediction|fault prediction / fault prognosis| |
|Anomaly detection|anomaly detection| |
|Predictive maintenance|predictive maintenance| |
|remaining useful life|remaining useful life (RUL)| |
|health status|health state / health condition| |
|Degenerate|degradation| |
|Call the police|alarm| |
|threshold|threshold| |

### 3.5 Data Characteristics / Data Characteristics

|Chinese|English|Notes|
|------|---------|-------|
|Industrial data|industrial data| |
|sensor data|sensor data| |
|multivariable|multivariate| |
|High dimensional data|high-dimensional data| |
|noise|noise| |
|Missing values|missing values| |
|Imbalanced data|imbalanced data| |
|Label scarcity|label scarcity| |

---

## 4. Cross-Domain Terms/Cross-Domain Terms

### 4.1 General Academic / General Academic

|Chinese|English|Notes|
|------|---------|-------|
|propose|propose/present| |
|method|method/approach| |
|frame|framework| |
|Model|model| |
|algorithm|algorithm| |
|experiment|experiment| |
|verify|validation/verification| |
|Evaluate|evaluation/assessment| |
|benchmark|baseline/benchmark| |
|ablation experiment|ablation study| |
|Comparative experiment|comparative experiment| |
|case study|case study| |
|generalization ability|generalization capability| |
|Interpretability|interpretability / explainability| |
|robustness|robustness| |
|Scalability|scalability| |

### 4.2 Data & Processing / Data and Processing

|Chinese|English|Notes|
|------|---------|-------|
|Dataset|dataset| |
|training set|training set| |
|Validation set|validation set| |
|test set|test set| |
|Data preprocessing|data preprocessing| |
|data augmentation|data augmentation| |
|normalization|normalization| |
|standardization|standardization| |
|feature engineering|feature engineering| |
|Dimensionality reduction|dimensionality reduction| |

---

## 5. Usage Examples / Usage examples

### ❌ Chinglish → ✅ Academic English

|Chinese original|❌ Literal translation|✅ Academic expression|
|----------|---------|-------------|
|This article proposes a new method|This paper puts forward a new method|We propose a novel approach|
|achieved very good results|get good effect|achieves superior performance|
|Compared with traditional methods|Compared with traditional method|Compared with conventional methods|
|Experimental results show|Experiment result shows|Experimental results demonstrate that|
|of great significance|has important meaning|is of significant importance|

---

## Notes/notes

1. Use the full name when a term first appears, and abbreviate it later.
2. Proper nouns (such as Transformer, LSTM) remain in the original text
3. Adapt terminology usage to specific conference/journal requirements
4. This table can be expanded according to specific research directions
