# Typst 试卷的期刊或会议特定要求

> **摘要索引。** 每个期刊或会议都有自己的快照
> `../templates/`;加载`templates/<venue>.md`当用户命名a时直接
> 具体期刊或会议（`ieee`, `acm`, `neurips`）。该文件仍然是
> 跨期刊或会议概述（比较表、常见错误、预提交
> 检查表、重新提交转换、图形规格）。

## 目录

- [IEEE会议和期刊](#ieee-conferences-and-journals)
  - [格式要求](#format-requirements)
  - [打字机配置](#typst-configuration)
  - [书写风格](#writing-style)
  - [引文样式](#citation-style)
  - [模板](#template)
- [ACM 会议和期刊](#acm-conferences-and-journals)
  - [格式要求](#format-requirements)
  - [打字机配置](#typst-configuration)
  - [书写风格](#writing-style)
  - [引文样式](#citation-styles)
- [施普林格期刊](#springer-journals)
  - [格式要求](#format-requirements)
  - [打字机配置](#typst-configuration)
  - [书写风格](#writing-style)
  - [特殊要求](#special-requirements)
- [NeurIPS / ICML / ICLR（机器学习会议）](#neurips-icml-iclr-machine-learning-conferences)
  - [格式要求](#format-requirements)
  - [打字机配置](#typst-configuration)
  - [书写风格](#writing-style)
  - [特殊要求](#special-requirements)
- [CVPR / ICCV / ECCV（计算机视觉会议）](#cvpr-iccv-eccv-computer-vision-conferences)
  - [格式要求](#format-requirements)
  - [打字机配置](#typst-configuration)
  - [书写风格](#writing-style)
- [AAAI / IJCAI（人工智能会议）](#aaai-ijcai-ai-conferences)
  - [格式要求](#format-requirements)
  - [打字机配置](#typst-configuration)
- [自然/科学（高影响力期刊）](#nature-science-high-impact-journals)
  - [格式要求](#format-requirements)
  - [书写风格](#writing-style)
- [中文期刊(中文期刊)](#chinese-journals-中文期刊)
  - [GB/T 7714-2015 标准](#gbt-7714-2015-standard)
- [对照表](#comparison-table)
- [所有期刊或会议通用提示](#general-tips-for-all-venues)
  - [提交前](#before-submission)
  - [要避免的常见错误](#common-mistakes-to-avoid)
  - [Typst 期刊或会议合规优势](#typst-advantages-for-venue-compliance)
- [会议快速参考表](#conference-quick-reference-table)
- [预提交清单](#pre-submission-checklist)
  - [通用（所有期刊或会议）](#universal-all-venues)
- [重新提交格式转换](#resubmission-format-conversion)
  - [常用转换路径](#common-conversion-paths)
  - [内容迁移原理](#content-migration-principles)
- [图和表规格](#figure-and-table-specifications)
  - [表格（打字机）](#tables-typst)
  - [人物](#figures)

---

## IEEE 会议和期刊

### 格式要求

- **论文尺寸**：US Letter (8.5" × 11")
- **列**：两列格式
- **柱宽**：3.5 英寸（8.89 厘米）
- **柱间距**：0.33 英寸（0.84 厘米）
- **边距**：顶部/底部 0.75 英寸，左侧/右侧 0.625 英寸
- **字体**：Times New Roman 10pt
- **行距**：单行距

### 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 0.75in, left: 0.625in, right: 0.625in),
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(
  font: "Times New Roman",
  size: 10pt
)

#set par(justify: true, leading: 0.55em)
```

### 写作风格

- **语音**：主动语音优先
- **时态**：方法的过去时，结果的现在时
- **图**：文字中为“图 1”，标题为“图 1”
- **表格**：罗马数字（表 I、表 II）
- **方程式**：连续编号

### 引文风格

- 方括号中的数字引用：[1]、[2-4]
- IEEE 参考格式

### 模板

```typst
#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [Your Paper Title],
  authors: (...),
  abstract: [...],
  index-terms: ("Keyword1", "Keyword2"),
  bibliography: bibliography("refs.bib", style: "ieee"),
)
```

### 伪代码

- 更喜欢`algorithmic`类似于 IEEE Typst 伪代码的包，因为它提供了`algorithm-figure`、标题支持和传统的控制流渲染。
- 当用户明确想要更自由的语法时，将 `lovelace` 视为灵活的后备方案。
- 在类似 IEEE 的输出中，将伪代码包装在`algorithm-figure(...)`或者`#figure(...)`带有标题。
- 建议行号是为了方便审查，但此处并不将其作为 IEEE 硬规则强制执行。
- 保持评论简短并将段落级解释移回到正文中。

---

## ACM 会议和期刊

### 格式要求

- **论文尺寸**：US Letter 或 A4
- **列**：两列格式
- **字体**：Linux Libertine 或类似字体
- **字体大小**：9-10pt
- **边距**：左/右 0.75 英寸，顶部/底部 1 英寸

### 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(
  font: "Linux Libertine",
  size: 9pt
)

#set par(justify: true)
```

### 写作风格

- **时态**：一般真理的现在时
- **数字**：始终如一的“图 1”
- **表**：“表 1”一致
- **引文**：数字或作者年份取决于地点

### 引文样式

- **数字**：[1], [2, 3]
- **作者年份**：（Smith 等人，2020）

---

## 施普林格期刊

### 格式要求

- **论文尺寸**：A4
- **列**：单列或两列（特定于期刊或会议）
- **字体**：Times New Roman 或类似字体
- **字体大小**：10-12pt
- **边距**：所有边均为 2.5 厘米

### 打字机配置

```typst
#set page(
  paper: "a4",
  margin: 2.5cm
)

#set text(
  font: "Times New Roman",
  size: 11pt
)

#set par(
  justify: true,
  first-line-indent: 1.5em
)
```

### 写作风格

- **图**：图下标题
- **表格**：表格上方的标题
- **参考文献**：按作者字母顺序排列
- **章节**：编号（1、1.1、1.1.1）

### 特殊要求

- 摘要：150-250字
- 关键词：4-6个关键词
- 致谢：参考文献之前的单独部分

---

## NeurIPS / ICML / ICLR（机器学习会议）

### 格式要求

- **页数限制**：8 页（不包括参考文献）
- **论文尺寸**：美国信函
- **列**：单列
- **字体**：Times New Roman 10pt
- **边距**：所有边均为 1 英寸
- **行距**：单行距

### 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: 1in
)

#set text(
  font: "Times New Roman",
  size: 10pt
)

#set par(
  justify: true,
  leading: 0.65em
)

#set heading(numbering: none)  // No section numbering
```

### 写作风格

- **匿名提交**：删除作者信息以供审核
- **数字**：高质量、灰度可读
- **代码**：仅补充材料
- **可重复性**：包括实施细节

### 特殊要求

- **更广泛的影响声明**：NeurIPS 所需
- **检查表**：完整的再现性检查表
- **补充材料**：单独的 PDF

---

## CVPR / ICCV / ECCV（计算机视觉会议）

### 格式要求

- **页数限制**：8 页（不包括参考文献）
- **论文尺寸**：美国信函
- **列**：两列格式
- **字体**：Times New Roman 10pt
- **边距**：所有边均为 1 英寸

### 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: 1in,
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(
  font: "Times New Roman",
  size: 10pt
)
```

### 写作风格

- **数字**：对于视觉结果至关重要
- **定性结果**：显示视觉比较
- **定量结果**：带有指标的表格
- **消融研究**：必需

---

## AAAI / IJCAI（人工智能会议）

### 格式要求

- **页数限制**：7 页（不包括参考文献）
- **论文尺寸**：美国信函
- **列**：两列格式
- **字体**：Times New Roman 10pt

### 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 1in, left: 0.875in, right: 0.875in),
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.25in)[..]

#set text(
  font: "Times New Roman",
  size: 10pt
)
```

---

## 自然/科学（高影响力期刊）

### 格式要求

- **字数限制**：严格（例如，“自然”字数为 3000 个字）
- **数字**：数量有限（通常为 4-6 个）
- **参考文献**：有限（通常为 30-50 个）
- **补充**：广泛的补充材料

### 写作风格

- **广泛受众**：非专业人士也可以接触到
- **意义**：强调更广泛的影响
- **简洁**：每个字都很重要
- **数字**：出版物质量，不言自明

---

## 中文期刊 (中文期刊)

### GB/T 7714-2015标准

#### 格式要求

- **论文尺寸**：A4
- **边距**：2.5-3 厘米
- **字体**：中文为宋体 (SimSun)，英文为 Times New Roman
- **字体大小**：正文小四（12pt）
- **行距**：1.5 或双倍

#### 打字机配置

```typst
#set page(
  paper: "a4",
  margin: (x: 3.17cm, y: 2.54cm)
)

#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  size: 12pt,
  lang: "zh",
  region: "cn"
)

#set par(
  justify: true,
  leading: 1em,
  first-line-indent: 2em
)

#set heading(numbering: "1.1")
```

#### 引文风格

- **GB/T 7714-2015**：中国国家标准
- **格式**：[序号]作者。 题名[文献标识类型]。 出版地：出版者，出版年：页码。

```typst
// GB/T 7714-2015. Valid hayagriva style ids: gb-7714-2015-numeric /
// -author-date / -note. (GB/T 7714-2025 has no built-in hayagriva style yet.)
#bibliography("refs.bib", style: "gb-7714-2015-numeric")
```

#### 特殊要求

- **摘要**：中英文版本
- **关键字**：两种语言 3-5 个关键字
- **图**：图1、图2（如下图）
- **表格**：表1、表2（表上图下）
- **方程式**：编号为(1)、(2)或(1-1)、(1-2)

---

## 比较表

|期刊或会议|专栏|字体大小|页数限制|引文风格|
| -------- | ------- | --------- | ----------- | ---------------------- |
|IEEE| 2       |10分|各不相同|数字 [1]|
|ACM| 2       |9-10分|各不相同|数字或作者年份|
|施普林格| 1-2     |10-12分|各不相同|按字母顺序|
|神经信息处理系统| 1       |10分|8页|数字 [1]|
|CVPR| 2       |10分|8页|数字 [1]|
|自然| 1       |各不相同|〜3000字|数字 [1]|
|中国人| 1       |12点|各不相同|GB/T 7714-2015|

---

## 适用于所有期刊或会议的一般提示

### 提交前

1. **阅读指南**：检查期刊或会议特定要求
2. **检查模板**：使用官方模板（如果有）
3. **页面限制**：遵守严格的页面限制
4. **数字**：确保高质量和可读性
5. **参考**：针对期刊或会议正确格式
6. **匿名**：如果需要，删除识别信息
7. **补充**：如果允许/需要，请准备

### 要避免的常见错误

- ❌ 论文尺寸错误（US Letter 与 A4）
- ❌ 页边距或字体大小不正确
- ❌ 缺少页码（如果需要）
- ❌ 引用格式不一致
- ❌ 低质量的人物
- ❌ 超出页数限制
- ❌ 匿名投稿作者信息

### Typst 在期刊或会议合规性方面的优势

- ✅ 快速编译以进行快速格式检查
- ✅ 轻松切换模板
- ✅ 整个文档的格式一致
- ✅ 内置支持多种引用样式
- ✅ 简单的图形和表格管理

---

## 会议快速参考表

|会议|页数限制|额外（相机就绪）|关键要求|
| ---------------- | -------------- | -------------------- | --------------------------------- |
|**NeurIPS 2025**|9页| +0                   |强制性清单、简单摘要|
|**ICML 2026**|8页| +1                   |更广泛的影响声明|
|**ICLR 2026**|9 页| +1                   |LLM披露、互审|
|**ACL 2025**|8页（长）|各不相同|限制部分强制|
|**AAAI 2026**|7页| +1                   |严格的样式文件遵守|
|**COLM 2025**|9页| +1                   |语言模型焦点|

**注意**：虽然某些会议需要 LaTeX，但 Typst 提交的内容可能会以 PDF 形式被接受。检查期刊或会议特定要求。

---

## 预提交清单

### 环球影城（所有期刊或会议）

- [ ] 文档编译无错误（`typst compile`）
- [ ] 文本中引用的所有数字
- [ ] 文本中引用的所有表格
- [ ] 没有孤立引用
- [ ] 无占位符文本（TODO、FIXME、XXX）
- [ ] 匿名提交（删除作者信息）
- [ ] 遵守页数限制
- [ ] 始终保持一致的符号
- [ ] 所有首字母缩略词均在首次使用时定义
- [ ] 包括限制部分

---

## 重新提交格式转换

### 常见转化路径

|从 → 到|页面变更|主要调整|
| -------------- | ----------- | -------------------------------------- |
|NeurIPS → ICML| 9 → 8       |削减一页，增加更广泛的影响|
|ICML → ICLR| 8 → 9       |扩大实验，添加LLM披露|
|NeurIPS → ACL| 9 → 8       |NLP 重构，添加限制|
|ICLR → AAAI| 9 → 7       |大幅剪裁，严谨风格|

### 内容迁移原则

1. **从目标模板开始** - 不要合并前导码
2. **仅复制内容部分**（文本、图形、表格、参考书目）
3. 剪切时：将校样移至附录，压缩相关工作
4. 扩展时：添加消融、扩展限制

---

## 图和表规格

### 表格（打字员）

```typst
// Professional table with booktabs-style rules
#table(
  columns: (auto, auto, auto),
  stroke: none,
  table.hline(),
  table.header(
    [*Method*], [*Accuracy ↑*], [*Latency ↓*],
  ),
  table.hline(stroke: 0.5pt),
  [Baseline], [85.2], [45ms],
  [*Ours*], [*92.1*], [38ms],
  table.hline(),
)
```

### 人物

- **矢量格式**首选（SVG for Typst）
- **色盲安全调色板**：Okabe-Ito 或 Paul Tol
- **灰度可读性**：验证数字在没有颜色的情况下是否有效
- **独立的标题**：读者无需正文即可理解
