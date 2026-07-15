# Module: Title Optimization
**Trigger words**: title, title, title optimization, create title, improve title

**Goal**: Generate and optimize academic paper titles according to IEEE/ACM/Springer/NeurIPS best practices.

**Script Usage**:
```bash
# 根据内容生成标题候选
uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --generate

# 优化现有标题（按词边界删除无效词）
uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --optimize

# 检查标题质量（评分 + 问题清单）
uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --check

# 强制语言（默认自动检测）
uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --check --lang en
```

> Available flags:`--generate` / `--optimize` / `--check` / `--lang {en,zh}`。
> The script does not provide interactive mode or `--compare` (the agent is not interactive); if you need to compare multiple titles,
> Run `--check` on each candidate individually and compare the scores.

**Title Quality Standards** (based on IEEE Author Center and top conferences/journals):

|standard|weight|illustrate|
|------|------|------|
|**Simplicity**| 25% |Delete "A Study of", "Research on", "Novel", "New"|
|**Searchability**| 30% |Core terms (method + problem) within first 65 characters|
|**length**| 15% |Best: 10-15 words (English) / 15-25 words (Chinese)|
|**Specificity**| 20% |Specific method/problem name, avoid generalities|
|**Normative**| 10% |Avoid uncommon abbreviations (except common abbreviations such as AI, LSTM, DNA, etc.)|

## Title generation workflow

**Step 1: Content Analysis**
Extracted from the abstract/introduction:
- **Research Question**: What challenge is being addressed?
- **Research Methods**: What methods are proposed?
- **Application areas**: What application scenarios?
- **Core Contribution**: What are the main results? (optional)

**Step 2: Keyword Extraction**
Identify 3-5 core keywords:
- Method keywords: "Transformer", "Graph Neural Network", "Reinforcement Learning"
- Question keywords: "Time Series Forecasting", "Fault Detection", "Image Segmentation"
- Field keywords: "Industrial Control", "Medical Imaging", "Autonomous Driving"

**Step 3: Title Template Selection**
Common patterns for top conferences/journals:

|model|Example (English)|Example (Chinese)|Applicable scenarios|
|------|-------------|-------------|----------|
|Method for Problem|"Transformer for Time Series Forecasting"|"Transformer method for time series forecasting"|general studies|
|Method: Problem in Domain|"Graph Neural Networks: Fault Detection in Industrial Systems"|"Graph Neural Networks: Fault Detection in Industrial Systems"|Field specialization|
|Problem via Method|"Time Series Forecasting via Attention Mechanisms"|"Time series prediction based on attention mechanism"|Method focus|
|Method + Key Feature|"Lightweight Transformer for Real-Time Detection"|"Lightweight Transformer real-time detection method"|Performance focus|

**Step 4: Generate title candidates**
Generate 3-5 candidate titles with different focuses:
1. method-focused
2. problem focused
3. Application focused
4. Balanced type (recommended)
5. Concise variant

**Step 5: Quality Score**
Each candidate title receives an overall score (0-100), breakdown scores for each criterion, and specific suggestions for improvement.

## Title optimization rules

**Delete invalid words**:

**English**:
|avoid using|reason|
|----------|------|
|A Study of|Redundant (all papers are studies)|
|Research on|Redundant (all papers are research)|
|Novel/New|Implied by publication|
|Improved/Enhanced|Vague without specifics|
|Based on|Often unnecessary|
|Using/Utilizing|Can be replaced with prepositions|

**Chinese**:
|avoid using|reason|
|----------|------|
|Research on...|Redundant (all papers are research)|
|Exploration of|redundant and unspecific|
|new/novel|Publication means novelty|
|Improved/Optimized|Not specific, need to explain how to improve|
|Based on|can be reduced to a direct statement|

**Example of recommended structure**:

**English**:
```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"

Good: "Attention-Based LSTM for Multivariate Time Series Prediction"
Bad:  "An Improved LSTM Model Using Attention Mechanism for Prediction"
```

**Chinese**:
```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究

好：注意力机制的多变量时间序列预测方法
差：基于注意力机制的改进型多变量时间序列预测模型研究
```

## Keyword layout strategy

- **First 65 characters (English) / First 20 characters (Chinese)**: The most important keywords (method + question)
- **Avoid beginnings**: Articles (A, An, The) / "About", "For"
- **Preferred**: nouns and technical terms over verbs and adjectives

## Abbreviation usage guidelines

|acceptable|Avoid in titles|
|----------|--------------|
|AI, ML, DL|Obscure domain-specific acronyms|
|LSTM, GRU, CNN|Chemical formulas (unless very common)|
|IoT, 5G, GPS|Lab-specific abbreviations|
|DNA, RNA, MRI|Non-standard method names|

## Conference/Journal Special Requirements

**IEEE Transactions**：
- Avoid subscripted formulas
- Use Title Case (capitalize the first letter of the main word)
- Typical length: 10-15 words

**ACM Conferences**：
- Use more creative titles and colon subtitles
- Typical length: 8-12 words

**Springer Journals**:
- Prefer descriptive rather than creative, can be longer (up to 20 words)

**NeurIPS/ICML**:
- Be concise and powerful (8-12 words), method names usually stand out

## Output format

**English paper**:
```typst
// ============================================================
// TITLE OPTIMIZATION REPORT
// ============================================================
// Current Title: "A Novel Study on Time Series Forecasting Using Deep Learning"
// Quality Score: 45/100
//
// Issues Detected:
// 1. [Critical] Contains "Novel Study" (remove ineffective words)
// 2. [Major] Vague method description ("Deep Learning" too broad)
//
// Recommended Titles (Ranked):
// 1. "Transformer-Based Time Series Forecasting for Industrial Control" [Score: 92/100]
// 2. "Attention Mechanisms for Multivariate Time Series Prediction" [Score: 88/100]
//
// Suggested Typst Update:
// #align(center)[
//   #text(size: 18pt, weight: "bold")[
//     Transformer-Based Time Series Forecasting for Industrial Control
//   ]
// ]
// ============================================================
```

**Chinese Paper**:
```typst
// ============================================================
// 标题优化报告
// ============================================================
// 当前标题："关于基于深度学习的时间序列预测的研究"
// 质量评分：48/100
//
// 推荐标题（按评分排序）：
// 1. "工业控制系统时间序列预测的Transformer方法" [评分: 94/100]
// 2. "多变量时间序列预测的注意力机制研究" [评分: 89/100]
// ============================================================
```

**Typst title setting example**:

**English paper**:
```typst
#align(center)[
  #text(size: 18pt, weight: "bold")[
    Transformer-Based Time Series Forecasting for Industrial Control
  ]
]
```

**Chinese Paper**:
```typst
#align(center)[
  #text(size: 18pt, weight: "bold", font: "Source Han Serif")[
    工业控制系统时间序列预测的Transformer方法
  ]

  #v(0.5em)

  #text(size: 14pt, font: "Times New Roman")[
    Transformer-Based Time Series Forecasting for Industrial Control Systems
  ]
]
```

Reference resources:
- [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/)
- [Royal Society Blog on Title Optimization](https://royalsociety.org/blog/2025/01/title-abstract-and-keywords-a-practical-guide-to-maximizing-the-visibility-and-impact-of-your-papers/)

