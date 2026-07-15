# Detailed guide to title optimization


## Directory

- [Title quality standards (based on GB/T 7713.1-2006 and international best practices)](#标题质量标准基于-gbt-77131-2006-及国际最佳实践)
- [Title Generation Workflow](#标题生成工作流)
  - [Step 1: Content Analysis](#步骤-1内容分析)
  - [Step 2: Keyword extraction](#步骤-2关键词提取)
  - [Step 3: Title template selection](#步骤-3标题模板选择)
  - [Step 4: Generate title candidates](#步骤-4生成标题候选)
  - [Step 5: Quality Score](#步骤-5质量评分)
- [Title Optimization Rules](#标题优化规则)
  - [❌ Delete invalid words](#删除无效词汇)
  - [✅ Recommended structure](#推荐结构)
- [Chapter title and section title structure](#章标题与小节标题架构)
- [Keyword layout strategy](#关键词布局策略)
- [Guidelines for the use of abbreviations](#缩写使用准则)
- [Special requirements for school template](#学校模板特殊要求)
  - [Tsinghua University (thuthesis)](#清华大学thuthesis)
  - [Peking University (pkuthss)](#北京大学pkuthss)
  - [General Requirements (ctexbook)](#通用要求ctexbook)
- [Chinese and English title comparison](#中英文标题对照)
- [Best Practice Summary](#最佳实践总结)
- [Output format example](#输出格式示例)

---

## Title quality standard (based on GB/T 7713.1-2006 and international best practices)

| Criteria | Weight | Description |
|------|------|------|
| **Simplicity** | 25% | Delete "research on...", "exploration of...", "new type", "improved" |
| **Searchability** | 30% | Core terms (method + problem) appear within the first 20 words |
| **Length** | 15% | Best: 15-25 words; Acceptable: 10-30 words |
| **Specificity** | 20% | Specific method/problem name, avoid generalities |
| **Normative** | 10% | Comply with thesis title specifications and avoid uncommon abbreviations |

## Title generation workflow

### Step 1: Content Analysis
Extracted from the abstract/introduction:
- **Research Question**: What challenge is being addressed?
- **Research Methods**: What methods are proposed?
- **Application Area**: What application scenario?
- **Core Contribution**: What are the main results? (optional)

### Step 2: Keyword extraction
Identify 3-5 core keywords:
- Method keywords: "Transformer", "Graph Neural Network", "Reinforcement Learning"
- Question keywords: "Time series prediction", "Fault detection", "Image segmentation"
- Field keywords: "industrial control", "medical imaging", "autonomous driving"

### Step 3: Title template selection

| Pattern | Example | Applicable scenarios |
|------|------|----------|
| Research on method-based issues | "Research on time series forecasting methods based on Transformer" | Innovative method |
| Problems and methods in the field | "Graph neural network method for fault detection in industrial systems" | Application-oriented |
| Problem methods and applications | "Attention mechanism for time series prediction and its application in industrial control" | Theory + Application |
| Research on domain-oriented methods | "Deep learning predictive maintenance method for intelligent manufacturing" | Domain-specific |

### Step 4: Generate title candidates
Generate 3-5 candidate titles with different focuses:
1. Method-focused type
2. Problem-focused
3. Application-focused
4. Balanced type (recommended)
5. Simple variations

### Step 5: Quality Score
Each candidate title gets:
- Overall rating (0-100)
- Breakdown scores for each standard
- Specific suggestions for improvement

## Title optimization rules

### ❌ Delete invalid words
| Avoid use | Reasons |
|----------|------|
| Research on... | Redundant (all papers are research) |
| Exploration of ... | Redundant and unspecific |
| New / Novel | Published means novel |
| Improved/Optimized | Not specific, need to explain how to improve |
| based on... | can be reduced to a direct statement |

### ✅ Recommended structure
```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究

好：图神经网络故障检测方法及其工业应用
差：新型改进的基于图神经网络的故障检测方法研究

好：注意力机制的多变量时间序列预测方法
差：基于注意力机制的改进型多变量时间序列预测模型研究
```

## Chapter title and section title structure

The table of contents of the dissertation is not only a layout level, but also an entrance for the defense committee to quickly determine the main line of research. The chapter titles of the main method chapter, model chapter, algorithm chapter, and system application chapter should try to reflect:

```text
研究对象 + 问题/任务 + 方法/路径
```

### Three elements of chapter title

| Elements | Function | Example |
|------|------|------|
| Object | Explain which process, system, indicator or scenario the research falls on | Non-stationary industrial process, cement grinding process, unit power consumption, specific surface area |
| Problem/Task | Explain what academic or engineering problem this chapter solves | Anomaly monitoring, root cause diagnosis, time series prediction, operation optimization |
| Method/path | Explain what method or technical path is used to solve the problem in this chapter | Adaptive method, heterogeneous data fusion model, multi-step optimization algorithm, system design |

Good: Time series prediction model of unit power consumption in cement grinding process

Bad: Predictive Model Research

Good: Abnormal path identification and root cause diagnosis based on causal intensity comparison

Bad: Root cause analysis method

Introduction, related work, literature review, summary and outlook, references, acknowledgments and appendices are conventional chapter titles, and it is not mandatory to apply the three elements.

### The relationship between the number of sections and deduction questions

Each chapter is directly under `\section` and is controlled within 5 sections by default. If you really need to expand into more details, you should sink the modules, parameters, and data processing steps to `\subsection` instead of juxtaposing all actions into direct subsections.

Recommended closed loop:

```text
引言 -> 基础理论/问题描述 -> 模型/算法/框架 -> 实验/案例/应用 -> 本章小结
```

Section headings should serve the chapter headings. If the chapter title is "Time series prediction model of unit power consumption in cement grinding process", the subsection title can be "Unit power consumption prediction model framework" or "Cement grinding process prediction experiment". It is not appropriate to just write general titles such as "data collection" and "result discussion" that can be moved to any chapter. If the general title must be retained, the object, problem or method relationship with the chapter title should be supplemented in the introduction.

## Keyword layout strategy
- **First 20 words**: The most important keywords (method + question)
- **Avoid beginnings**: "About", "For", "For" (can be placed in the middle)
- **Preference**: nouns and technical terms over verbs and adjectives

## Guidelines for using abbreviations
| ✅ ACCEPTABLE | ❌ AVOID IN TITLE |
|----------|--------------|
| AI, machine learning, deep learning | Lab-specific abbreviations |
| LSTM, GRU, CNN | Chemical formula (unless extremely common) |
| Internet of Things, 5G, GPS | Non-standard method name abbreviations |
| DNA, RNA, MRI | Abbreviations specific to unfamiliar fields |

## Special requirements for school templates

### Tsinghua University (thuthesis)
- Chinese title: no more than 36 Chinese characters
- English title: corresponding Chinese title translation
- Avoid abbreviations and formulas
- Example: "Research on the application of deep learning in predictive maintenance in intelligent manufacturing"

### Peking University (pkuthss)
- Chinese title: concise and to the point, generally no more than 25 words
- Subtitles can be used (separated by dashes)
- Example: "Graph Neural Network Fault Detection Method - Research on Industrial Control Systems"

### General requirements (ctexbook)
- Comply with GB/T 7713.1-2006 specification
- Chinese title: 15-25 words is appropriate
- English title: Corresponding translation, pay attention to articles and prepositions
- Example: "Transformer-based time series forecasting method and application"

## Comparison of Chinese and English titles

Things to note when translating titles:
- Chinese "Y based on X" is usually translated as "X-Based Y" or "Y via X"
- Avoid word-for-word translation and maintain English expression habits
- Use Title Case for English titles (capitalize the first letter of the main word)

| Chinese title | English title |
|----------|----------|
| Graph Neural Network Methods for Fault Detection in Industrial Systems | Graph Neural Networks for Fault Detection in Industrial Systems |
| Research on time series forecasting based on attention mechanism | Attention-Based Time Series Forecasting |
| Deep Learning Applications in Intelligent Manufacturing | Deep Learning Applications in Smart Manufacturing |

## Best Practice Summary
1. **Keyword prefix**: Method + question are placed in the first 20 words
2. **Be specific**: "Transformer" > "Deep Learning" > "Machine Learning"
3. **Delete redundancy**: Remove "about", "research", "new type", and "based on"
4. **Control length**: Target 15-25 words (Chinese)
5. **Test searchability**: Can your paper be found using these keywords?
6. **Avoid unfamiliar terms**: Unless it is a widely recognized term (AI, LSTM, CNN)
7. **Conform to specifications**: Follow the school template and GB/T 7713.1-2006 standard

## Output format example

```latex
% ============================================================
% 标题优化报告
% ============================================================
% 当前标题："关于基于深度学习的时间序列预测的研究"
% 质量评分：48/100
%
% 检测到的问题：
% 1. [严重] 包含"关于...的研究"（删除冗余词汇）
% 2. [重要] 方法描述过于宽泛（"深度学习"太笼统）
% 3. [次要] 长度可接受（18字）但可更具体
%
% 推荐标题（按评分排序）：
%
% 1. "工业控制系统时间序列预测的Transformer方法" [评分: 94/100]
%    - 简洁性：✅ (19字)
%    - 可搜索性：✅ (方法+问题在前15字)
%    - 具体性：✅ (Transformer，而非"深度学习")
%    - 领域性：✅ (工业控制系统)
%    - 规范性：✅ (符合学位论文规范)
%
% 建议的 LaTeX 更新：
% \title{工业控制系统时间序列预测的Transformer方法}
% \englishtitle{Transformer-Based Time Series Forecasting for Industrial Control Systems}
% ============================================================
```
