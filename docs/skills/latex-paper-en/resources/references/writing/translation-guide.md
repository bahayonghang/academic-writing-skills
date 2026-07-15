# Academic Translation Guide


## Table of contents

- [Overview / Overview](#overview-概述)
- [1. Translation Principles / Translation Principles](#1-translation-principles-翻译原则)
  - [1.1 Core Principles / Core Principles](#11-core-principles-核心原则)
  - [1.2 Academic Tone / Academic Tone](#12-academic-tone-学术语气)
- [2. Common Chinglish Corrections / Common Chinese English Corrections](#2-common-chinglish-corrections-常见中式英语修正)
  - [2.1 Redundant Expressions / Redundant Expressions](#21-redundant-expressions-冗余表达)
  - [2.2 Verb Improvements / Verb Improvements](#22-verb-improvements-动词改进)
  - [2.3 Structure Improvements / Structure Improvements](#23-structure-improvements-结构改进)
- [3. Section-Specific Guidelines / Translation Guidelines for Each Chapter](#3-section-specific-guidelines-各章节翻译指南)
  - [3.1 Abstract / Abstract](#31-abstract-摘要)
  - [3.2 Introduction / Introduction](#32-introduction-引言)
  - [3.3 Related Work / Related Work](#33-related-work-相关工作)
  - [3.4 Method / Method](#34-method-方法)
  - [3.5 Experiments / Experiments](#35-experiments-实验)
  - [3.6 Conclusion / Conclusion](#36-conclusion-结论)
- [4. Tense Usage Summary / Tense Usage Summary](#4-tense-usage-summary-时态使用总结)
- [5. Translation Workflow / Translation Workflow](#5-translation-workflow-翻译工作流)
  - [Step 1: Terminology Extraction / terminology extraction](#step-1-terminology-extraction-术语提取)
  - [Step 2: Structure Mapping / Structure Mapping](#step-2-structure-mapping-结构映射)
  - [Step 3: Sentence Translation / Sentence Translation](#step-3-sentence-translation-句子翻译)
  - [Step 4: Polish & Review / Polish review](#step-4-polish-review-润色审查)
- [6. Quick Reference Patterns / Quick Reference Templates](#6-quick-reference-patterns-快速参考模板)
  - [6.1 Proposing Method / Proposing method](#61-proposing-method-提出方法)
  - [6.2 Describing Results / Description results](#62-describing-results-描述结果)
  - [6.3 Comparing Methods / Comparative Methods](#63-comparing-methods-比较方法)
  - [6.4 Analyzing Results / Analysis results](#64-analyzing-results-分析结果)
- [7. Domain-Specific Notes / Domain-specific notes](#7-domain-specific-notes-领域特定说明)
  - [Deep Learning Papers](#deep-learning-papers)
  - [Time Series Papers](#time-series-papers)
  - [Industrial Control Papers](#industrial-control-papers)
- [Checklist / Checklist](#checklist-检查清单)

---

> A guide to Chinese-English academic translation – from Chinese draft to English paper

## Overview / Overview

This guide helps translate Chinese academic drafts into English papers that meet international journal/conference standards.
Core Principles: **Accuracy > Fluency > Simplicity**

---

## 1. Translation Principles / Translation Principles

### 1.1 Core Principles / Core Principles

|in principle|illustrate|Example|
|------|------|------|
|**accuracy**|Technical terms must be accurate and cannot be paraphrased|convolution → convolution (not rolling)|
|**consistency**|The same term is unified throughout the text|Don't mix method/approach/technique|
|**Simplicity**|Avoid redundant expressions|❌ in order to → ✅ to|
|**objectivity**|Avoid subjective evaluation words|❌ very good → ✅ effective|

### 1.2 Academic Tone / academic tone

```
❌ 避免:
- 口语化表达 (a lot of, kind of, stuff)
- 绝对化表述 (always, never, perfect)
- 情感化词汇 (amazing, terrible, exciting)

✅ 使用:
- 正式学术词汇 (significant, substantial, considerable)
- 谨慎限定词 (generally, typically, approximately)
- 客观描述 (effective, efficient, accurate)
```

---

## 2. Common Chinglish Corrections / Common Chinese English corrections

### 2.1 Redundant Expressions / redundant expressions

|❌ Chinglish|✅Academic English|illustrate|
|--------------|---------------------|------|
|in recent years|recently|simplify|
|more and more|increasingly|simplify|
|play an important role in|is crucial for / contributes to|simplify|
|make a contribution to|contribute to|simplify|
|have a great influence on|significantly affect|simplify|
|in order to|to|simplify|
|due to the fact that|because / since|simplify|
|a large number of|many / numerous|simplify|
|in the field of|in|simplify|
|it is worth noting that|notably|simplify|

### 2.2 Verb Improvements/verb improvements

|❌Weak Verb|✅ Strong Verb|Context|
|--------------|----------------|---------|
|use|employ, utilize, leverage, adopt|Method usage|
|get|obtain, achieve, acquire, derive|Get results|
|make|construct, develop, generate, create|build|
|do|perform, conduct, execute, carry out|implement|
|show|demonstrate, illustrate, indicate, reveal|exhibit|
|give|provide, offer, present, yield|supply|
|have|possess, exhibit, contain|have|
|put forward|propose, present, introduce|propose|

### 2.3 Structure Improvements/structural improvements

|❌ Chinese Structure|✅ English Structure|
|---------------------|---------------------|
|This article proposes a...|We propose... / This paper presents...|
|First...then...finally...|First,... Subsequently,... Finally,...|
|Achieved by...|... is achieved by/through...|
|is better than|Compared with..., ... outperforms...|
|Experimental results show...|Experimental results demonstrate that...|

---

## 3. Section-Specific Guidelines / Translation Guidelines for Each Chapter

### 3.1 Abstract / Abstract

```
结构: Background → Problem → Method → Results → Conclusion
时态: 
  - 背景/现状: 现在时
  - 本文工作: 现在时 (We propose...)
  - 实验结果: 过去时 (achieved, obtained)
长度: 150-250 words (根据会议/期刊要求)

模板:
[Background] ... remains a challenging problem.
[Problem] Existing methods suffer from...
[Method] In this paper, we propose...
[Results] Experimental results on ... demonstrate that...
[Conclusion] Our approach achieves state-of-the-art performance.
```

### 3.2 Introduction/Introduction

```
结构: Context → Problem → Limitations → Contribution → Organization
时态:
  - 领域背景: 现在时
  - 已有工作: 现在完成时 (have been proposed)
  - 本文贡献: 现在时

贡献陈述模板:
The main contributions of this paper are summarized as follows:
• We propose a novel ... for ...
• We design a ... mechanism to address ...
• Extensive experiments demonstrate that ...
```

### 3.3 Related Work / related work

```
时态: 现在完成时 + 过去时
  - 领域发展: 现在完成时 (have been widely studied)
  - 具体工作: 过去时 (proposed, introduced, developed)

过渡词:
- 同类工作: Similarly, Likewise, Along this line
- 对比: However, In contrast, Unlike
- 扩展: Furthermore, Moreover, Additionally
- 总结: Overall, In summary
```

### 3.4 Method / method

```
时态: 现在时 (描述方法本身)
语态: 被动语态为主，主动语态描述设计决策

结构词:
- 整体描述: consists of, comprises, is composed of
- 步骤: First, Then, Subsequently, Finally
- 公式引入: is defined as, is computed by, is formulated as

公式描述模板:
where $x$ denotes the input, $W$ represents the weight matrix,
and $b$ is the bias term.
```

### 3.5 Experiments / Experiments

```
时态:
  - 实验设置: 过去时 (was conducted, were used)
  - 结果描述: 现在时 (shows, demonstrates)
  - 结果分析: 现在时

比较表达:
- 优于: outperforms, surpasses, exceeds
- 相当: is comparable to, is on par with
- 显著: significantly, substantially, considerably
- 略微: slightly, marginally

数值描述:
- 提升: improves by X%, achieves X% improvement
- 降低: reduces by X%, decreases X%
- 最优: achieves the best/lowest/highest
```

### 3.6 Conclusion / conclusion

```
时态:
  - 总结工作: 过去时 (proposed, presented)
  - 结论陈述: 现在时
  - 未来工作: 将来时 (will, plan to)

模板:
In this paper, we proposed ... for ...
Experimental results demonstrated that ...
In future work, we plan to extend ...
```

---

## 4. Tense Usage Summary/Tense Usage Summary

|Section|Tense|Example|
|---------|-------|---------|
|Abstract - Background|Present|... is an important task|
|Abstract-Method|Present|We propose...|
|Abstract-Results|Past|achieved, obtained|
|Introduction-Background|Present|... has attracted attention|
|Introduction - Contribution|Present|We propose...|
|Related Work-General|Present Perfect|have been proposed|
|Related Work-Specific|Past|proposed, introduced|
|Method|Present|consists of, computes|
|Experiments-Setup|Past|was conducted|
|Experiments-Results|Present|shows, demonstrates|
|Conclusion - Summary|Past|proposed, presented|
|Conclusion - Future|Future|will explore|

---

## 5. Translation Workflow/Translation Workflow

### Step 1: Terminology Extraction / terminology extraction
```
1. 识别中文稿中的专业术语
2. 查阅 terminology.md 确定标准译法
3. 建立本文术语表，确保一致性
```

### Step 2: Structure Mapping / structure mapping
```
1. 分析中文段落结构
2. 调整为英文学术结构（主题句在前）
3. 确保逻辑连接词使用正确
```

### Step 3: Sentence Translation / Sentence Translation
```
1. 识别主干（主谓宾）
2. 处理修饰成分
3. 检查时态和语态
4. 简化冗余表达
```

### Step 4: Polish & Review / polish review
```
1. 检查术语一致性
2. 检查时态正确性
3. 检查 Chinglish
4. 检查学术语气
```

---

## 6. Quick Reference Patterns/Quick Reference Templates

### 6.1 Proposing Method/Proposing method

```latex
% 中文: 本文提出了一种基于...的...方法
We propose a novel [METHOD] based on [TECHNIQUE] for [TASK].
This paper presents a [ADJ] approach to [PROBLEM] using [METHOD].
In this work, we introduce [METHOD] that [BENEFIT].
```

### 6.2 Describing Results/Describing results

```latex
% 中文: 实验结果表明，我们的方法取得了最好的效果
Experimental results demonstrate that our method achieves 
state-of-the-art performance on [DATASET].

Our approach outperforms existing methods by [X]% in terms of [METRIC].

The proposed method achieves [VALUE] [METRIC], which is [X]% higher 
than the best baseline.
```

### 6.3 Comparing Methods/Comparison methods

```latex
% 中文: 与传统方法相比，我们的方法具有以下优势
Compared with conventional methods, our approach offers 
the following advantages: ...

Unlike previous methods that [LIMITATION], our method [ADVANTAGE].

While existing approaches [LIMITATION], we address this by [SOLUTION].
```

### 6.4 Analyzing Results / Analysis results

```latex
% 中文: 这是因为...
This improvement can be attributed to [REASON].
The performance gain is due to [REASON].
This is because [EXPLANATION].

% 中文: 值得注意的是...
It is worth noting that [OBSERVATION].
Notably, [FINDING].
An interesting observation is that [FINDING].
```

---

## 7. Domain-Specific Notes / Domain-specific notes

### Deep Learning Papers
- Model names remain original (BERT, GPT, ResNet)
- Hyperparameters use standard notation ($\alpha$, $\beta$, $\lambda$）
- The loss function is represented by $\mathcal{L}$

### Time Series Papers
- The time index is $t$, and the sequence length is $T$ or $L$.
- Use horizon or forecasting horizon for forecast step size
- Use lookback window or historical window for historical window

### Industrial Control Papers
- Control variables use standard notation ($u$ input, $y$ output, $x$ state)
- Emphasis on practical application scenarios and industrial significance
- Pay attention to statements related to safety and reliability

---

## Checklist/Checklist

Once the translation is complete, please check:

- [ ] Terminology consistent throughout the text
- [ ] Use correct tenses
- [ ] No Chinglish expression
- [ ] No redundant vocabulary
- [ ] Appropriate academic tone
- [ ] Unification of formula symbols
- [ ] Chart title specifications
- [ ] Reference format is correct
