# 学术写作风格指南（Typst）


## 目录

- [核心原理](#core-principles)
  - [1.清晰度胜过复杂性](#1-clarity-over-complexity)
  - [2.精确度优于模糊度](#2-precision-over-vagueness)
  - [3.主动语音（适当时）](#3-active-voice-when-appropriate)
- [句子长度准则](#sentence-length-guidelines)
- [段落结构](#paragraph-structure)
  - [主题句](#topic-sentence)
  - [支持句子](#supporting-sentences)
  - [过渡](#transition)
- [学术词汇](#academic-vocabulary)
  - [报告动词（中性）](#reporting-verbs-neutral)
  - [报告动词（强一致）](#reporting-verbs-strong-agreement)
  - [报告动词（暂定）](#reporting-verbs-tentative)
  - [报告动词（关键）](#reporting-verbs-critical)
- [过渡词](#transition-words)
  - [添加](#addition)
  - [对比度](#contrast)
  - [原因/影响](#causeeffect)
  - [示例](#example)
  - [序列](#sequence)
- [引文集成（Typst 语法）](#citation-integration-typst-syntax)
  - [积分（作者为主体）](#integral-author-as-subject)
  - [非积分（内容重点）](#non-integral-content-focus)
  - [释义（首选）](#paraphrase-preferred)
  - [直接报价（少量）](#direct-quote-sparingly)
- [常用断面图案](#common-section-patterns)
  - [简介](#introduction)
  - [相关工作](#related-work)
  - [方法论](#methodology)
  - [结果](#results)
  - [结论](#conclusion)
- [打字机特定格式](#typst-specific-formatting)
  - [标题](#headings)
  - [强调](#emphasis)
  - [列表](#lists)
  - [数学](#math)
  - [图表](#figures-and-tables)
  - [交叉引用](#cross-references)

---

## 核心原则

### 1. 清晰性优于复杂性
- 每句话一个想法
- 尽可能避免嵌套子句
- 定义首次使用的术语

### 2. 精确胜于模糊
- 使用具体数字而不是“几个”或“许多”
- 尽可能量化声明
- 避免在没有证据的情况下进行对冲

### 3.主动语态（适当时）
- ✅“我们提出了一种新颖的方法......”
- ✅“本文介绍了……”
- ❌“我们提出了一种新方法......”

## 句子长度指南

|类型|字数统计|使用案例|
|------|------------|----------|
|短的| 10-15 |主要发现、转变|
|中等的| 15-25 |内容最多|
|长的| 25-40 |复杂的关系|
|很长| >40 |⚠️考虑分拆|

## 段落结构

### 主题句
第一句话说出了要点。

### 支持句子
- 证据、例子或阐述
- 典型 3-5 句话
- 清晰的逻辑流程

### 过渡
如果需要，请连接到下一段。

## 学术词汇

### 报告动词（中性）
- 陈述、注释、观察、报告、描述

### 报告动词（强一致）
- 展示、展示、证明、证实、建立

### 报告动词（暂定）
- 暗示、暗示、表明、提议、假设

### 报告动词（关键）
- 主张、主张、断言、断言、坚持

## 过渡词

### 添加
- 此外，此外，此外，此外

### 对比
- 然而，尽管如此，相反，另一方面

### 原因/结果
- 因此，因此，结果，因此

### 例子
- 例如，例如，特别地，特别地

### 顺序
- 第一、第二、随后、最后

## 引文集成（Typst 语法）

### 积分（作者为主体）
```typst
@smith2020 demonstrated that...
According to @jones2021, the method...
```

### 非整体（内容重点）
```typst
Deep learning has shown remarkable success @smith2020 @jones2021 @wang2022.
```

### 释义（首选）
用你自己的话重申这个想法并引用。

### 直接报价（谨慎）
仅用于定义或措辞非常好的想法。

### 反引用堆叠规则（简介及相关工作）

堆叠 3 个以上的参考文献而不进行单独讨论是一种常见的 AI 写作模式，这在顶级场所是不可接受的。这些规则适用于简介和相关工作部分。

**规则：**
1. **每句话最多 2 次集群引用** 无讨论
   - ❌“已经提出了很多方法@smith2020 @jones2021 @wang2022 @li2023 @chen2024。”
   - ✅ “@smith2020 为场景 A 提出了 X。在此基础上，@jones2021 将方法扩展到 B，而 @wang2022 则解决了限制 C。”

2. **每项被引用的作品都必须获得引用**，并且至少具有以下一项：
   - 核心贡献摘要（至少 1 条）
   - 与另一篇引用作品的比较
   - 激励你工作的特定限制

3. **简介和相关工作中的叙述性内容**：
   - 对关键作品使用完整引用（作者作为主题）：“@smith2020 展示了......”
   - 仅保留对既定事实的非完整引用：“梯度下降被广泛使用@smith2020 @jones2021。”

4. **适合漏斗的密度（简介）：**
   - 背景段落（大背景）：最多 2 条对既定事实的集中引用
   - 问题陈述段落：每个引文必须单独讨论
   - 差距/动机段落：每个引用的限制都必须引用特定的论文

5. **分类讨论（相关工作）：**
   - 按方法/方法而不是按时间顺序对作品进行分组
   - 在每个小组中，讨论每项工作的具体贡献和局限性
   - 在作品之间使用比较语言：“与@smith2020不同，@jones2021地址......”

**积极模式（简介）：**
```typst
@smith2020 proposed method X, achieving Y% accuracy on dataset Z.
However, their approach assumes A, which limits applicability to B.
@jones2021 relaxed this assumption by introducing C, but at the cost of D.
In contrast, our method addresses both limitations by...
```

**积极模式（相关工作）：**
```typst
*Transformer-based methods.* @vaswani2017 introduced the self-attention
mechanism for sequence modeling. @li2019 adapted this architecture for
time series, but their method requires $O(n^2)$ memory. @zhou2021 proposed
ProbSparse attention to reduce complexity to $O(n log n)$, though at the
cost of approximation error.
```

**负面模式（禁止）：**
```typst
Many researchers have studied this problem @a2020 @b2021 @c2022 @d2023 @e2024.
Several methods have been proposed @f2020 @g2021 @h2022 @i2023 @j2024 @k2024.
```

## 常见截面图案

### 介绍
1. 一般背景 → 具体问题
2. 现有工作的差距
3. 这项工作的贡献
4. 论文组织

### 相关工作
1. 对现有方法进行分类
2. 比较和对比
3. 定位你的工作

### 方法论
1. 方法概述
2. 详细步骤
3. 选择的理由

### 结果
1. 实验装置
2. 定量结果
3. 定性分析
4. 与基线比较

### 结论
1. 贡献摘要
2. 局限性
3. 未来的工作

## 特定于 Typst 的格式

### 标题
```typst
= Introduction          // Level 1
== Background          // Level 2
=== Related Work       // Level 3
```

### 强调
```typst
*bold text*            // Bold
_italic text_          // Italic
`code text`            // Code/monospace
```

### 列表
```typst
// Unordered list
- Item 1
- Item 2
  - Nested item

// Ordered list
+ First item
+ Second item
  + Nested item
```

### 数学
```typst
// Inline math
The equation $x^2 + y^2 = z^2$ shows...

// Display math
$ x^2 + y^2 = z^2 $

// Numbered equation
$ x = (a + b) / 2 $ <eq:mean>
```

### 图表
```typst
// Figure
#figure(
  image("figure.png", width: 80%),
  caption: [Description of the figure.]
) <fig:example>

// Table
#figure(
  table(
    columns: 3,
    [Header 1], [Header 2], [Header 3],
    [Data 1], [Data 2], [Data 3],
  ),
  caption: [Description of the table.]
) <tab:example>
```

### 交叉引用
```typst
As shown in @fig:example, the method...
Table @tab:example presents the results...
Equation @eq:mean defines the average...
```
