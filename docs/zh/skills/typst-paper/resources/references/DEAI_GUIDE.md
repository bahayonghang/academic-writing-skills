# Typst学术论文去AI写作指南


## 目录

- [目的（目的）](#目的-purpose)
- [核心原则(Coreprinciples)](#核心原则-core-principles)
  - [1.语法保真优先(语法保真优先)](#1-syntax-fidelity-语法保真优先)
  - [2.零捏造](#2-zero-fabrication-零捏造)
  - [3.信息密度 (提高信息密度)](#3-information-density-提高信息密度)
  - [4.学术克制(克制措辞)](#4-academic-restraint-克制措辞)
- [学术人性化契约](#academic-humanization-contract)
- [需要删除的常见AI写作模式](#common-ai-writing-patterns-to-remove)
  - [类别一：空话口号](#category-1-empty-phrases-空话口号)
  - [类别2：过度确定的语言](#category-2-over-confident-language-过度确定)
  - [类别3：机械结构(机械排比)](#category-3-mechanical-structures-机械排比)
  - [类别4：模糊量化](#category-4-vague-quantification-模糊量化)
  - [类别 5：模板化引言（模板引言）](#category-5-template-introductions-模板引言)
- [结构级痕迹（LLM-判断）](#structural-level-traces-llm-judgment)
- [特定部分指南](#section-specific-guidelines)
  - [摘要（摘要）](#abstract-摘要)
  - [简介(引言)](#introduction-引言)
  - [相关工作（相关工作）](#related-work-相关工作)
  - [方法(方法)](#methods-方法)
  - [结果 (结果)](#results-结果)
  - [讨论（讨论）](#discussion-讨论)
  - [结论(结论)](#conclusion-结论)
- [De-AI 编辑的输出格式](#output-format-for-de-ai-editing)
- [更改类别](#change-categories)
- [Typst 特定语法保留](#typst-specific-syntax-preservation)
  - [受保护元素（永不修改）](#protected-elements-never-modify)
  - [可修改元素（仅限文本）](#modifiable-elements-text-only)
- [快速参考：常见替代品](#quick-reference-common-replacements)
- [参考书目](#bibliography)

---

## 目的（目的）

本指南有助于减少人工智能生成的书写痕迹，同时保持技术准确性和 Typst 语法完整性。

**目标模式**：IEEE TOP期刊（模式一）——简洁、精确、内敛

---

## 核心原则（核心原则）

### 1.语法保真优先
- **切勿修改**：打字机功能（`#set`, `#show`, `#let`）、数学环境、引文（`@cite`）、标签（`<label>`)
- **仅修改**：可见段落文本、章节标题、标题文本
- **保留**：编译时的所有结构完整性

### 2. 零捏造
- **切勿添加**：新数据、指标、比较、实验设置
- **切勿添加**：新的主张、贡献或结论
- **唯一改进**：表达清晰度和自然流畅

### 3. 提高信息密度
- 每句话都必须传达可验证的信息
- 删除没有实质意义的空话
- 用具体的陈述替换模糊的主张（如果有）
- 将无法验证的声明标记为 [待验证]

### 4. 克制措辞
- 避免在没有证据的情况下过度自信的语言
- 对投机声明使用适当的对冲
- 客观地而非夸张地呈现贡献

---

## 学术人性化契约

降低 AI 音调并不是躲避探测器。在平滑散文之前保留 Typst 纸：

1. 保护语法锚点：`@cite`, `<label>`, `#set`, `#show`, `#let`、数学、代码、宏和源布局。
2. 提取学术有效负载：事实/证据、作者立场、章节逻辑、主张-证据链接和边界。
3. 清除payload后，才可去除中文或英文结构外壳。

默认输出应该是调查结果、风险摘要或重写蓝图。仅当用户要求散文时才给出散文建议。将缺少的支持标记为`[PENDING VERIFICATION]` / `待补证`;不要发明引文、基线、指标、实验或结论。

### 双语结构-外壳检查

|类别|通用触发|学术修复|
|----------|----------------|--------------|
|空对比壳|不是 A 而是 B；不仅是A，还有B|仅在指定基线、标准和证据时保留|
|虚假洞察标记|真正的问题； 本质上；本质上;关键是|删除标记并直接陈述有证据支持的主张|
|演讲冒号|我的结论是：;结论是：|使用正常的学术句子或具体的清单名词|
|所指对象模糊|这些东西；由此可见;事物;因素|命名对象、方法、机制、结果或限制|
|模糊比较级|更适合； 更自然|命名比较基线和评估标准|

---

## 需要删除的常见人工智能写作模式

### 第一类：空话口号

|❌ 类AI|✅ 类人|笔记|
|-----------|---------------|-------|
|显着改善|误差减少 X%|使用特定数字|
|综合分析|分析 X、Y、Z|列出分析的内容|
|有效的解决方案|优于基线 X|状态比较指标|
|重要贡献|提出 X 的方法|说明贡献|
|稳健的性能|在 Y 下保持精度|指定条件|
|新颖的方法|通过引入 Y 来扩展 X|解释一下新内容|

**检测模式**：寻找可以用可衡量的主张替换的形容词。

### 第二类：过度确定

|❌绝对|✅ 合格|
|-------------|--------------|
|明显地|结果表明|
|清楚地|证据表明|
|一定|在这些条件下|
|完全地|大多数情况下|
|无疑|看来是|
|总是|在我们的实验中始终如一|
|绝不|很少观察到|

**检测模式**：没有资格或证据的绝对主张。

> 对于分级保守措辞表（因果/第一性/普遍性/效果大小/应用），请参阅[`OVER_CLAIM_GUARD.md`](OVER_CLAIM_GUARD.md).

### 类别3：机械结构（机械排比）

**无实质内容的三部分并行**：
❌“我们的方法**快速**、**准确**、**高效**。”
✅“我们的方法每秒处理 1000 个样本，准确率达 95%。”

**模板转换**：
❌“近年来，深度学习发展迅速。”
✅“自 2020 年以来，深度学习在 X 领域取得了最先进的性能。”

**通用空缺**：
❌“随着科技的飞速发展……”
✅ 直接从具体的问题背景开始。

**检测模式**：可以适用于任何领域任何论文的短语。

### 第四类：模糊量化（模糊量化）

|❌ 模糊|✅ 具体|
|----------|------------|
|许多研究|最近的三项研究 @ref1 @ref2 @ref3|
|大量的实验|X数据集上的实验|
|实质性的收获|提高 12%|
|大多数|78% 的案例|
|明显更好|表现优于 p<0.01|

**检测模式**：没有实际数字或参考的量词。

### 第五类：模板介绍（模板引言）

❌“时间序列预测是一个具有广泛应用的重要问题。”
✅ “时间序列预测对于供应链优化@ref1、能源管理@ref2 和财务规划@ref3 至关重要。”

❌“机器学习已经彻底改变了许多领域。”
✅ “机器学习提高了医疗保健 @ref1、制造 @ref2 和金融 @ref3 领域的预测准确性。”

**检测模式**：任何教科书中都可以出现的广泛概括。

---

## 结构级痕迹（LLM-判断）

这些不是单词或句子级别的讲述——它们存在于文档结构中，所以
脚本无法捕获它们。通过阅读整个草稿来判断它们，并标记任何发现
`[LLM]`。

1. **过度对称的 IMRAD** — 每个部分都填充为相同的形状（介绍总是 4 段；讨论总是“回顾 + 比较 + 暗示 + 限制”）。真正的论文参差不齐：有些部分短，有些部分长。信号：段落计数在各节之间对称。
2. **声明式脚手架转换** — “建立 X 后，我们接下来转向 Y。” /“有了这个，我们就继续……”。真正的写作是隐式过渡的：下一句话不经意间就进入了新的主题。
3. **无立场的讨论**——各自列出了优点和缺点，但没有人承诺。真正的作者采取立场（“我们认为 X 比 Y 更合理，因为……”）。
4. **统一的段落长度** — 80% 的段落由 5-7 个句子组成。真正的节奏各不相同：一个 3 句话的强调段落，旁边是一个 10 句话的论证。

**如何修复**：打破对称性 - 合并薄段落，拆分超载段落，删除已宣布的过渡，并使讨论提交到一个视图。

---

## 特定部分指南

### 摘要（摘要）

**结构**：目的→方法→关键结果（带数字）→结论

**常见的人工智能陷阱**：
- ❌“我们提出了一种新颖的方法......”
- ✅“我们提出了一种基于注意力的机制......”

- ❌“实验结果显示显着改善。”
- ✅“在数据集 X 上，与基线相比，我们的方法将 MAE 降低了 12%。”

- ❌“这项工作对......具有重要意义”
- ✅“此方法可以实现延迟 <10 毫秒的实时预测。”

**限制**：
- 没有具体细节的通用声明（“新颖”、“重要”、“重要”）
- 包括关键结果的具体数字
- 说明具体贡献，而不是一般价值

**例子**：
```typst
// ❌ AI-like
This paper proposes a novel deep learning approach for time series
forecasting. The method achieves significant performance improvements
over existing methods. Experimental results demonstrate the effectiveness
of our approach.

// ✅ Human-like
This paper proposes an attention-based mechanism for multivariate time
series forecasting. Our method reduces MAE by 12% on the UCR archive
compared to the Transformer baseline @ref1. Experimental results show that
the attention mechanism improves long-term dependency capture.
```

---

### 简介（引言）

**结构**：重要性→差距→贡献→组织

**常见的人工智能陷阱**：
- ❌“时间序列预测在现代社会中发挥着重要作用。”
- ✅“时间序列预测对于能源网格优化至关重要@ref1。”

- ❌“然而，现有方法有局限性。”
- ✅“但是，现有方法无法捕获嘈杂环境中的长期依赖关系@ref2 @ref3。”

- ❌“我们的主要贡献如下：”
- ✅“这篇论文做出了三个贡献：”

**贡献声明规则**：
- 每项贡献都必须是可验证的
- 避免在没有证据的情况下使用“新颖”、“第一”、“最先进”
- 说明你做了什么，而不是它有多重要

**例子**：
```typst
// ❌ AI-like
Time series forecasting is very important. Many researchers study this
problem. However, existing methods have some limitations. This paper
proposes a novel method with significant improvements.

// ✅ Human-like
Time series forecasting enables proactive decision-making in energy
management @ref1 and supply chain optimization @ref2. Recent approaches
based on Transformers @ref3 @ref4 show promise but struggle with noisy
data @ref5. This paper proposes a noise-robust attention mechanism that
reduces prediction error by 12% compared to standard Transformers.
```

---

### 相关工作（相关工作）

**结构**：分类→比较→位置

**常见的人工智能陷阱**：
- ❌“Smith等人提出了一个方法，很好。”
- ✅“@smith2020 提出了 X，它在数据集 Z 上实现了 Y 精度。”

- ❌“现有的方法可以分为两种：A和B。”
- ✅“现有方法遵循两个范式：统计方法@ref1@ref2@ref3和深度学习方法@ref4@ref5@ref6。”

- ❌“我们的方法和他们不一样。”
- ✅“与 @ref1 @ref2 不同，我们的方法将注意力机制纳入......”

**指南**：
- 按方法/范式分组，而不是按时间顺序分组
- 比较具体的技术差异
- 说明你的做法有何不同
- 避免含糊的赞扬（“优秀”、“杰出”）

---

### 方法（方法）

**结构**：概述→细节→算法→复杂性

**常见的人工智能陷阱**：
- ❌“我们使用神经网络。它非常强大。”
- ✅“我们使用具有 256 个隐藏单元的 3 层 LSTM。”

- ❌“该算法运行良好。”
- ✅“算法在 100 个时期内收敛。”

- ❌“该模型具有良好的性能。”
- ✅“模型每秒处理 1000 个样本。”

**指南**：
- 提供可重复性的实施细节
- 状态超参数和架构选择
- 如果相关，请包括算法复杂性
- 专注于你所做的事情，而不是它的效果如何（这就是结果）

---

### 结果 (结果)

**结构**：主要结果→消融→分析

**常见的人工智能陷阱**：
- ❌“我们的方法比基线的表现要好得多。”
- ✅“与最佳基线相比，我们的方法将 MAE 降低了 12%。”

- ❌“结果证明了我们方法的有效性。”
- ✅ “@tab:结果表明我们的方法在 4/5 数据集上实现了最低的 MAE。”

- ❌“从图 2 可以看出，我们的方法更优越。”
- ✅“@fig：比较表明，我们的方法在训练数据减少 50% 的情况下仍能保持准确性。”

**指南**：
- 仅报告事实和数字
- 不要解释原因（这是讨论）
- 避免解释性语言（没有数字的“优越”、“优于”）
- 让表格/数字说明一切

---

### 讨论（讨论）

**结构**：解释→机制→局限性→未来的工作

**常见的人工智能陷阱**：
- ❌“良好的性能证明我们的方法是优秀的。”
- ✅“准确性的提高表明注意力机制捕获了长期依赖性。”

- ❌“我们的方法没有任何限制。”
- ✅“我们的方法需要更多的训练时间（基线为 2.3 小时，而基线为 1.5 小时）。”

- ❌“未来的工作包括更多的实验。”
- ✅“未来的工作将探索注意力机制的可解释性。”

**指南**：
- 解释机制，而不仅仅是结果
- 确认故障和边界条件
- 诚实地陈述限制
- 提出今后的具体工作

---

### 结论（结论）

**结构**：总结→回答研究问题→未来的工作

**常见的人工智能陷阱**：
- ❌“在本文中，我们提出了一种新方法，取得了重大改进。”
- ✅“这篇论文提出了一种基于注意力的机制，可以将 MAE 降低 12%。”

- ❌“我们的工作具有重要的理论和实践价值。”
- ✅“这项工作可以利用有限的计算资源进行实时预测。”

- ❌“未来，我们将不断改进我们的方法。”
- ✅“未来的工作将将此方法扩展到具有缺失数据的多变量时间序列。”

**指南**：
- 直接回答研究问题
- 没有新的结果或声明
- 没有新的实验
- 具体的、可操作的未来工作

---

## De-AI 编辑的输出格式

```typst
// ============================================================
// DE-AI EDITING (Line X - [Section Name])
// ============================================================
// Original: [AI-like text]
// Revised: [Human-like text]
//
// Changes:
// 1. [Type of change]: [details]
// 2. [Type of change]: [details]
//
// ⚠️ [PENDING VERIFICATION]: [claim needing evidence]
// ============================================================

[revised source code]
```

## 更改类别

1. **删除了空短语**：删除了模糊的形容词/副词
2. **增加特异性**：用具体替换模糊
3. **分割长句**：分割句子>50个字
4. **重新排序的结构**：改进的逻辑流程
5. **降级声明**：添加适当的对冲
6. **删除冗余**：删除重复内容
7. **添加主题**：插入缺少的语法主题
8. **固定模板表达式**：用特定替换通用

---

## 特定于 Typst 的语法保留

### 受保护的元素（永不修改）

**1.函数调用**
```typst
#set text(...)      // NEVER modify
#show heading: ...  // NEVER modify
#let func = ...     // NEVER modify
```

**2.引文和参考文献**
```typst
@smith2020          // NEVER modify citation keys
<fig:example>       // NEVER modify labels
@fig:example        // NEVER modify cross-references
```

**3.数学环境**
```typst
$x^2 + y^2 = z^2$   // NEVER modify math content
$ integral x dif x $ // NEVER modify display math
```

**4.标记语法**
```typst
*bold*              // Can modify text, keep markup
_italic_            // Can modify text, keep markup
`code`              // NEVER modify code content
```

### 可修改元素（仅限文本）

**1.段落文本**
```typst
// ✅ Can modify
This method achieves significant improvements.
→ This method reduces error by 12%.
```

**2.标题文本**
```typst
// ✅ Can modify text, keep syntax
= Novel Approach for Time Series
→ = Attention-Based Mechanism for Time Series
```

**3.标题文本**
```typst
// ✅ Can modify text inside caption
#figure(
  ...,
  caption: [This shows significant improvements.]
)
→
#figure(
  ...,
  caption: [This shows 12% error reduction.]
)
```

---

## 快速参考：常见替代品

|❌ 删除|✅ 替换为|
|-----------|-----------------|
|显着改善|[具体指标+数字]|
|综合研究|分析 X、Y、Z|
|有效的解决方案|优于基线 X%|
|新颖的方法|通过引入 Y 来扩展 X|
|稳健的性能|在[条件]下保持准确性|
|显然/显然|证据表明/结果表明|
|许多研究|[数量] 研究 [引用次数]|
|最近几年|自[年份]/[特定时期]以来|
|越来越多|越来越/从 X 到 Y 增长|
|发挥重要作用|使/对于/至关重要/对于|

---

## 参考书目

本指南应与以下各项一起使用：
- [STYLE_GUIDE.md](STYLE_GUIDE.md)：一般学术写作规则
- [COMMON_ERRORS.md](COMMON_ERRORS.md)：要避免的中式英语模式
- [VENUES.md](VENUES.md)：期刊或会议特定要求
- [TYPST_SYNTAX.md](TYPST_SYNTAX.md)：Typst 语法参考
