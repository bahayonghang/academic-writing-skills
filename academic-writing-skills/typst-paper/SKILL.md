---
name: typst-paper
version: 1.1.0
category: academic-writing
tags:
  - typst
  - paper
  - chinese
  - english
  - conference
  - journal
  - deep-learning
  - compilation
  - grammar
  - bibliography
description: |
  Typst 学术论文助手（支持中英文论文、会议/期刊投稿）。
  领域：深度学习、时间序列、工业控制、计算机科学。

  触发词（可独立调用任意模块）：
  - "compile", "编译", "typst compile" → 编译模块
  - "format", "格式检查", "lint" → 格式检查模块
  - "grammar", "语法", "proofread", "润色" → 语法分析模块
  - "long sentence", "长句", "simplify", "拆解" → 长难句分析模块
  - "academic tone", "学术表达", "improve writing" → 学术表达模块
  - "logic", "coherence", "逻辑", "衔接", "methodology", "方法论" → 逻辑衔接与方法论深度模块
  - "translate", "翻译", "中译英" → 翻译模块
  - "bib", "bibliography", "参考文献" → 参考文献模块
  - "deai", "去AI化", "humanize", "降低AI痕迹" → 去AI化编辑模块
  - "title", "标题", "title optimization", "create title" → 标题优化模块
  - "template", "模板", "IEEE", "ACM" → 模板配置模块
argument-hint: "[main.typ] [--section <section>] [--module <module>]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(typst *)
---

# Typst 学术论文助手

## 核心原则

1. 绝不修改 `@cite`、`@ref`、`@label`、数学环境内的内容
2. 绝不凭空捏造参考文献条目
3. 绝不在未经许可的情况下修改专业术语
4. 始终先以注释形式输出修改建议
5. Typst 编译速度快（毫秒级），适合实时预览

## 参数约定（$ARGUMENTS）

- `$ARGUMENTS` 用于接收主 `.typ` 路径、目标章节、模块选择等关键信息。
- 若 `$ARGUMENTS` 缺失或含糊，先询问：主 `.typ` 路径、目标范围、所需模块。
- 路径按字面处理，不推断或补全未提供的路径。

## 执行约束

- 仅在用户明确要求时执行脚本/编译命令。
- 涉及清理或覆盖输出文件的操作前先确认。

## 统一输出协议（全部模块）

每条建议必须包含固定字段：
- **严重级别**：Critical / Major / Minor
- **优先级**：P0（阻断）/ P1（重要）/ P2（可改进）

**默认注释模板**（diff-comment 风格）：
```typst
// <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
// 原文：...
// 修改后：...
// 理由：...
// ⚠️ 【待补证】：<需要证据/数据时标记>
```

## 失败处理（全局）

工具/脚本无法执行时，输出包含原因与建议的注释块：
```typst
// ERROR [Severity: Critical] [Priority: P0]: <简要错误>
// 原因：<缺少工具或路径无效>
// 建议：<安装工具/核对路径/重试命令>
```

常见情况：
- **脚本不存在**：确认 `scripts/` 路径与工作目录
- **Typst 未安装**：建议通过 `cargo install typst-cli` 或包管理器安装
- **字体缺失**：使用 `typst fonts` 查看可用字体
- **文件不存在**：请用户提供正确 `.typ` 路径
- **编译失败**：优先定位首个错误并请求日志片段

## 模块（独立调用）

### 模块：编译
**触发词**: compile, 编译, build, typst compile, typst watch

**Typst 编译命令**:
| 命令 | 用途 | 说明 |
|------|------|------|
| `typst compile main.typ` | 单次编译 | 生成 PDF 文件 |
| `typst watch main.typ` | 监视模式 | 文件变化时自动重新编译 |
| `typst compile main.typ output.pdf` | 指定输出 | 自定义输出文件名 |
| `typst compile --format png main.typ` | 其他格式 | 支持 PNG、SVG 等格式 |
| `typst fonts` | 字体列表 | 查看系统可用字体 |

**使用示例**:
```bash
# 基础编译（推荐）
typst compile main.typ

# 监视模式（实时预览）
typst watch main.typ

# 指定输出目录
typst compile main.typ --output build/paper.pdf

# 导出为 PNG（用于预览）
typst compile --format png main.typ

# 查看可用字体
typst fonts

# 使用自定义字体路径
typst compile --font-path ./fonts main.typ
```

**编译速度优势**:
- Typst 编译速度通常在毫秒级（vs LaTeX 的秒级）
- 增量编译：只重新编译修改的部分
- 适合实时预览和快速迭代

**中文支持**:
```typst
// 中文字体配置示例
#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  lang: "zh",
  region: "cn"
)
```

---

### 模块：格式检查
**触发词**: format, 格式检查, lint, style check

**检查项目**:
| 类别 | 检查内容 | 标准 |
|------|----------|------|
| 页边距 | 上下左右边距 | 通常 1 英寸（2.54cm）|
| 行间距 | 单倍/双倍行距 | 根据期刊要求 |
| 字体 | 正文字体与大小 | Times New Roman 10-12pt |
| 标题 | 各级标题格式 | 层次清晰，编号正确 |
| 图表 | 标题位置与格式 | 图下表上，编号连续 |
| 引用 | 引用格式一致性 | 数字/作者-年份格式 |

**Typst 格式检查要点**:
```typst
// 页面设置
#set page(
  paper: "a4",  // 或 "us-letter"
  margin: (x: 2.5cm, y: 2.5cm)
)

// 文本设置
#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

// 段落设置
#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em
)

// 标题设置
#set heading(numbering: "1.1")
```

**常见格式问题**:
- ❌ 页边距不一致
- ❌ 字体混用（中英文字体未分离）
- ❌ 图表编号不连续
- ❌ 引用格式不统一

---

### 模块：语法分析（英文）
**触发词**: grammar, 语法, proofread, 润色, article usage

**重点检查领域**:
- 主谓一致
- 冠词使用（a/an/the）
- 时态一致性（方法用过去时，结果用现在时）
- Chinglish 检测

**输出格式**:
```typst
// GRAMMAR（第23行）[Severity: Major] [Priority: P1]: 冠词缺失
// 原文：We propose method for...
// 修改后：We propose a method for...
// 理由：单数可数名词前缺少不定冠词
```

**常见语法错误**:
| 错误类型 | 示例 | 修正 |
|----------|------|------|
| 冠词缺失 | propose method | propose a method |
| 主谓不一致 | The data shows | The data show |
| 时态混乱 | We proposed... The results shows | We proposed... The results show |
| Chinglish | more and more | increasingly |

---

### 模块：长难句分析
**触发词**: long sentence, 长句, simplify, decompose, 拆解

**触发条件**:
- 英文：句子 >50 词 或 >3 个从句
- 中文：句子 >60 字 或 >3 个分句

**输出格式**:
```typst
// 长难句检测（第45行，共67词）[Severity: Minor] [Priority: P2]
// 主干：[主语 + 谓语 + 宾语]
// 修饰成分：
//   - [关系从句] which...
//   - [目的状语] to...
// 建议改写：[简化版本]
```

**拆分策略**:
1. 识别主干结构
2. 提取修饰成分
3. 拆分为多个短句
4. 保持逻辑连贯性

---

### 模块：学术表达
**触发词**: academic tone, 学术表达, improve writing, weak verbs

**英文学术表达**:
| ❌ 弱动词 | ✅ 学术替代 |
|----------|------------|
| use | employ, utilize, leverage |
| get | obtain, achieve, acquire |
| make | construct, develop, generate |
| show | demonstrate, illustrate, indicate |

**中文学术表达**:
| ❌ 口语化 | ✅ 学术化 |
|----------|----------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |
| 可以看出 | 由此可见 |

**输出格式**:
```typst
// EXPRESSION（第23行）[Severity: Minor] [Priority: P2]: 提升学术语气
// 原文：We use machine learning to get better results.
// 修改后：We employ machine learning to achieve superior performance.
// 理由：用学术替代词替换弱动词
```

---

### 模块：逻辑衔接与方法论深度
**触发词**: logic, coherence, 逻辑, 衔接, methodology, 方法论, 论证, argument

**目标**：确保段落间逻辑流畅，强化方法论的严谨性。

**重点检查领域**：

**1. 段落级逻辑衔接（AXES 模型）**：
| 组成部分 | 说明 | 示例 |
|----------|------|------|
| **A**ssertion（主张） | 清晰的主题句，陈述核心观点 | "注意力机制能够提升序列建模效果。" |
| **X**ample（例证） | 支撑主张的具体证据或数据 | "实验中，注意力机制达到95%准确率。" |
| **E**xplanation（解释） | 分析证据为何支撑主张 | "这一提升源于其捕获长程依赖的能力。" |
| **S**ignificance（意义） | 与更广泛论点或下一段的联系 | "这一发现为本文架构设计提供了依据。" |

**2. 过渡信号词**：
| 关系类型 | 中文信号词 | 英文对应 |
|----------|------------|----------|
| 递进 | 此外、进一步、更重要的是 | furthermore, moreover |
| 转折 | 然而、但是、相反 | however, nevertheless |
| 因果 | 因此、由此可见、故而 | therefore, consequently |
| 顺序 | 首先、随后、最后 | first, subsequently, finally |
| 举例 | 例如、具体而言、特别是 | for instance, specifically |

**3. 方法论深度检查清单**：
- [ ] 每个主张都有证据支撑（数据、引用或逻辑推理）
- [ ] 方法选择有充分理由（为何选此方法而非其他？）
- [ ] 明确承认研究局限性
- [ ] 清晰陈述前提假设
- [ ] 可复现性细节充分（参数、数据集、评估指标）

**4. 常见问题**：
| 问题类型 | 表现 | 修正方法 |
|----------|------|----------|
| 逻辑断层 | 段落间缺乏衔接 | 添加过渡句说明段落关系 |
| 无据主张 | 断言缺乏证据支撑 | 补充引用、数据或推理 |
| 方法论浅薄 | "本文采用X"但无理由 | 解释为何X适合本问题 |
| 隐含假设 | 前提条件未明示 | 显式陈述假设条件 |

**输出格式**：
```typst
// 逻辑衔接（第45行）[Severity: Major] [Priority: P1]: 段落间逻辑断层
// 问题：从问题描述直接跳转到解决方案，缺乏过渡
// 原文：数据存在噪声。本文提出一种滤波方法。
// 修改后：数据存在噪声，这对后续分析造成干扰。因此，本文提出一种滤波方法以解决该问题。
// 理由：添加因果过渡，连接问题与解决方案

// 方法论深度（第78行）[Severity: Major] [Priority: P1]: 方法选择缺乏论证
// 问题：方法选择未说明理由
// 原文：本文采用ResNet作为骨干网络。
// 修改后：本文采用ResNet作为骨干网络，其残差连接结构能有效缓解梯度消失问题，且在特征提取任务中表现优异。
// 理由：用技术原理论证架构选择
```

**分章节指南**：
| 章节 | 逻辑衔接重点 | 方法论深度重点 |
|------|--------------|----------------|
| Abstract | 目的→方法→结果→结论的流畅衔接 | 突出核心贡献 |
| Introduction | 问题→空白→贡献的流畅衔接 | 论证研究意义 |
| Related Work | 按主题分组，显式对比 | 定位与前人工作的关系 |
| Methods | 步骤间逻辑递进 | 论证每个设计选择 |
| Experiments | 设置→结果→分析的流程 | 解释评估指标选择 |
| Discussion | 发现→启示→局限的衔接 | 承认研究边界 |

**最佳实践**（参考 [Elsevier](https://elsevier.blog/logical-academic-writing/)、[Proof-Reading-Service](https://www.proof-reading-service.com/blogs/academic-publishing/a-guide-to-creating-clear-and-well-structured-scholarly-arguments)）：
1. **一段一主题**：每段聚焦单一核心观点
2. **主题句先行**：段首即陈述本段主张
3. **证据链完整**：每个主张都需支撑（数据、引用或逻辑）
4. **显式过渡**：使用信号词标明段落关系
5. **论证而非描述**：解释"为何"，而非仅陈述"是什么"

---

### 模块：翻译（中译英）
**触发词**: translate, 翻译, 中译英, Chinese to English

**翻译流程**:

**步骤 1：领域识别**
确定专业领域术语：
- 深度学习：neural networks, attention, loss functions
- 时间序列：forecasting, ARIMA, temporal patterns
- 工业控制：PID, fault detection, SCADA

**步骤 2：术语确认**
```markdown
| 中文 | English | 领域 |
|------|---------|------|
| 注意力机制 | attention mechanism | DL |
| 时间序列预测 | time series forecasting | TS |
```

**步骤 3：翻译并注释**
```typst
// 原文：本文提出了一种基于Transformer的方法
// 译文：We propose a Transformer-based approach
// 注释："本文提出" → "We propose"（学术标准表达）
```

**步骤 4：Chinglish 检查**
| 中式英语 | 地道表达 |
|----------|----------|
| more and more | increasingly |
| in recent years | recently |
| play an important role | is crucial for |

**常用学术句式**:
| 中文 | English |
|------|---------|
| 本文提出... | We propose... / This paper presents... |
| 实验结果表明... | Experimental results demonstrate that... |
| 与...相比 | Compared with... / In comparison to... |
| 综上所述 | In summary / In conclusion |

---

### 模块：参考文献
**触发词**: bib, bibliography, 参考文献, citation, 引用

**Typst 参考文献管理**:

**方法 1：使用 BibTeX 文件**
```typst
#bibliography("references.bib", style: "ieee")
```

**方法 2：使用 Hayagriva 格式**
```typst
#bibliography("references.yml", style: "apa")
```

**支持的引用样式**:
- `ieee` - IEEE 数字引用
- `apa` - APA 作者-年份
- `chicago-author-date` - 芝加哥作者-年份
- `mla` - MLA 人文学科
- `gb-7714-2015` - 中国国标

**引用示例**:
```typst
// 文中引用
According to @smith2020, the method...
Recent studies @smith2020 @jones2021 show...

// 参考文献列表
#bibliography("references.bib", style: "ieee")
```

**检查项目**:
- 必填字段完整性
- 重复条目检测
- 未使用条目
- 引用格式一致性

---

### 模块：去AI化编辑
**触发词**: deai, 去AI化, humanize, reduce AI traces, 降低AI痕迹

**目标**：在保持 Typst 语法和技术准确性的前提下，降低 AI 写作痕迹。

**输入要求**：
1. **源码类型**（必填）：Typst
2. **章节**（必填）：Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion
3. **源码片段**（必填）：直接粘贴（保留原缩进与换行）

**工作流程**：

**1. 语法结构识别**
检测 Typst 语法，完整保留：
- 函数调用：`#set`, `#show`, `#let`
- 引用：`@cite`, `@ref`, `@label`
- 数学：`$...$`, `$ ... $`（块级）
- 标记：`*bold*`, `_italic_`, `` `code` ``
- 自定义函数（默认不改）

**2. AI 痕迹检测**:
| 类型 | 示例 | 问题 |
|------|------|------|
| 空话口号 | significant, comprehensive, effective | 缺乏具体性 |
| 过度确定 | obviously, necessarily, completely | 过于绝对 |
| 机械排比 | 无实质内容的三段式 | 缺乏深度 |
| 模板表达 | in recent years, more and more | 陈词滥调 |

**3. 文本改写**（仅改可见文本）：
- 拆分长句（英文 >50 词，中文 >50 字）
- 调整词序以符合自然表达
- 用具体主张替换空泛表述
- 删除冗余短语
- 补充必要主语（不引入新事实）

**4. 输出生成**：
```typst
// ============================================================
// 去AI化编辑（第23行 - Introduction）
// ============================================================
// 原文：This method achieves significant performance improvement.
// 修改后：The proposed method improves performance in the experiments.
//
// 改动说明：
// 1. 删除空话："significant" → 删除
// 2. 保留原有主张，避免新增具体指标
//
// ⚠️ 【待补证：需要实验数据支撑，补充具体指标】
// ============================================================

= Introduction
The proposed method improves performance in the experiments...
```

**硬性约束**：
- **绝不修改**：`@cite`, `@ref`, `@label`, 数学环境
- **绝不新增**：事实、数据、结论、指标、实验设置、引用编号
- **仅修改**：普通段落文字、标题文本

**分章节准则**：
| 章节 | 重点 | 约束 |
|------|------|------|
| Abstract | 目的/方法/关键结果（带数字）/结论 | 禁泛泛贡献 |
| Introduction | 重要性→空白→贡献（可核查） | 克制措辞 |
| Related Work | 按路线分组，差异点具体化 | 具体对比 |
| Methods | 可复现优先（流程、参数、指标定义） | 实现细节 |
| Results | 仅报告事实与数值 | 不解释原因 |
| Discussion | 讲机制、边界、失败、局限 | 批判性分析 |
| Conclusion | 回答研究问题，不引入新实验 | 可执行未来工作 |

---

### 模块：标题优化
**触发词**: title, 标题, title optimization, create title, improve title

**目标**：根据 IEEE/ACM/Springer/NeurIPS 最佳实践，生成和优化学术论文标题。

**使用示例**：

**根据内容生成标题**：
```bash
python scripts/optimize_title.py main.typ --generate
# 分析摘要/引言，提出 3-5 个标题候选方案
```

**优化现有标题**：
```bash
python scripts/optimize_title.py main.typ --optimize
# 分析当前标题并提供改进建议
```

**检查标题质量**：
```bash
python scripts/optimize_title.py main.typ --check
# 根据最佳实践评估标题（评分 0-100）
```

**标题质量标准**（基于 IEEE Author Center 及顶级会议/期刊）：

| 标准 | 权重 | 说明 |
|------|------|------|
| **简洁性** | 25% | 删除 "A Study of", "Research on", "Novel", "New" |
| **可搜索性** | 30% | 核心术语（方法+问题）在前 65 字符内 |
| **长度** | 15% | 最佳：10-15 词（英文）/ 15-25 字（中文）|
| **具体性** | 20% | 具体方法/问题名称，避免泛泛而谈 |
| **规范性** | 10% | 避免生僻缩写（除 AI, LSTM, DNA 等通识缩写）|

**标题生成工作流**：

**步骤 1：内容分析**
从摘要/引言中提取：
- **研究问题**：解决什么挑战？
- **研究方法**：提出什么方法？
- **应用领域**：什么应用场景？
- **核心贡献**：主要成果是什么？（可选）

**步骤 2：关键词提取**
识别 3-5 个核心关键词：
- 方法关键词："Transformer", "Graph Neural Network", "Reinforcement Learning"
- 问题关键词："Time Series Forecasting", "Fault Detection", "Image Segmentation"
- 领域关键词："Industrial Control", "Medical Imaging", "Autonomous Driving"

**步骤 3：标题模板选择**
顶级会议/期刊常用模式：

| 模式 | 示例（英文） | 示例（中文） | 适用场景 |
|------|-------------|-------------|----------|
| Method for Problem | "Transformer for Time Series Forecasting" | "时间序列预测的Transformer方法" | 通用研究 |
| Method: Problem in Domain | "Graph Neural Networks: Fault Detection in Industrial Systems" | "图神经网络：工业系统故障检测" | 领域专项 |
| Problem via Method | "Time Series Forecasting via Attention Mechanisms" | "基于注意力机制的时间序列预测" | 方法聚焦 |
| Method + Key Feature | "Lightweight Transformer for Real-Time Detection" | "轻量级Transformer实时检测方法" | 性能聚焦 |

**步骤 4：生成标题候选**
生成 3-5 个不同侧重的候选标题：
1. 方法侧重型
2. 问题侧重型
3. 应用侧重型
4. 平衡型（推荐）
5. 简洁变体

**步骤 5：质量评分**
每个候选标题获得：
- 总体评分（0-100）
- 各标准细分评分
- 具体改进建议

**标题优化规则**：

**❌ 删除无效词汇**：

**英文**：
| 避免使用 | 原因 |
|----------|------|
| A Study of | Redundant (all papers are studies) |
| Research on | Redundant (all papers are research) |
| Novel / New | Implied by publication |
| Improved / Enhanced | Vague without specifics |
| Based on | Often unnecessary |
| Using / Utilizing | Can be replaced with prepositions |

**中文**：
| 避免使用 | 原因 |
|----------|------|
| 关于...的研究 | 冗余（所有论文都是研究） |
| ...的探索 | 冗余且不具体 |
| 新型 / 新颖的 | 发表即意味着新颖 |
| 改进的 / 优化的 | 不具体，需说明如何改进 |
| 基于...的 | 可简化为直接表述 |

**✅ 推荐结构**：

**英文示例**：
```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"

Good: "Graph Neural Networks for Fault Detection"
Bad:  "Research on Novel Fault Detection Based on GNNs"

Good: "Attention-Based LSTM for Multivariate Time Series Prediction"
Bad:  "An Improved LSTM Model Using Attention Mechanism for Prediction"
```

**中文示例**：
```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究

好：图神经网络故障检测方法及其工业应用
差：新型改进的基于图神经网络的故障检测方法研究

好：注意力机制的多变量时间序列预测方法
差：基于注意力机制的改进型多变量时间序列预测模型研究
```

**关键词布局策略**：
- **前 65 字符（英文）/ 前 20 字（中文）**：最重要的关键词（方法+问题）
- **避免开头**：Articles (A, An, The) / "关于"、"对于"
- **优先使用**：名词和技术术语，而非动词和形容词

**缩写使用准则**：
| ✅ 可接受 | ❌ 标题中避免 |
|----------|--------------|
| AI, ML, DL | Obscure domain-specific acronyms |
| LSTM, GRU, CNN | Chemical formulas (unless very common) |
| IoT, 5G, GPS | Lab-specific abbreviations |
| DNA, RNA, MRI | Non-standard method names |

**会议/期刊特殊要求**：

**IEEE Transactions**：
- 避免带下标的公式（除非很简单，如 "Nd–Fe–B"）
- 使用 Title Case（主要词首字母大写）
- 典型长度：10-15 词
- 示例："Deep Learning for Predictive Maintenance in Smart Manufacturing"

**ACM Conferences**：
- 可使用更有创意的标题
- 可使用冒号添加副标题
- 典型长度：8-12 词
- 示例："AttentionFlow: Visualizing Attention Mechanisms in Neural Networks"

**Springer Journals**：
- 偏好描述性而非创意性
- 可稍长（最多 20 词）
- 示例："A Comprehensive Framework for Real-Time Anomaly Detection in Industrial IoT Systems"

**NeurIPS/ICML**：
- 简洁有力（8-12 词）
- 方法名通常突出
- 示例："Transformers Learn In-Context by Gradient Descent"

**输出格式**：

**英文论文**：
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
// 3. [Minor] Length acceptable (9 words) but could be more specific
//
// Recommended Titles (Ranked):
//
// 1. "Transformer-Based Time Series Forecasting for Industrial Control" [Score: 92/100]
//    - Concise: ✅ (8 words)
//    - Searchable: ✅ (Method + Problem in first 50 chars)
//    - Specific: ✅ (Transformer, not just "Deep Learning")
//    - Domain: ✅ (Industrial Control)
//
// 2. "Attention Mechanisms for Multivariate Time Series Prediction" [Score: 88/100]
//    - Concise: ✅ (7 words)
//    - Searchable: ✅ (Key terms upfront)
//    - Specific: ✅ (Attention, Multivariate)
//    - Note: Consider adding domain if space allows
//
// 3. "Deep Learning Approach to Time Series Forecasting in Smart Manufacturing" [Score: 78/100]
//    - Concise: ⚠️ (10 words, acceptable)
//    - Searchable: ✅
//    - Specific: ⚠️ ("Deep Learning" still broad)
//    - Domain: ✅ (Smart Manufacturing)
//
// Keyword Analysis:
// - Primary: Transformer, Time Series, Forecasting
// - Secondary: Industrial Control, Attention, LSTM
// - Searchability: "Transformer Time Series" appears in 1,234 papers (good balance)
//
// Suggested Typst Update:
// #align(center)[
//   #text(size: 18pt, weight: "bold")[
//     Transformer-Based Time Series Forecasting for Industrial Control
//   ]
// ]
// ============================================================
```

**中文论文**：
```typst
// ============================================================
// 标题优化报告
// ============================================================
// 当前标题："关于基于深度学习的时间序列预测的研究"
// 质量评分：48/100
//
// 检测到的问题：
// 1. [严重] 包含"关于...的研究"（删除冗余词汇）
// 2. [重要] 方法描述过于宽泛（"深度学习"太笼统）
// 3. [次要] 长度可接受（18字）但可更具体
//
// 推荐标题（按评分排序）：
//
// 1. "工业控制系统时间序列预测的Transformer方法" [评分: 94/100]
//    - 简洁性：✅ (19字)
//    - 可搜索性：✅ (方法+问题在前15字)
//    - 具体性：✅ (Transformer，而非"深度学习")
//    - 领域性：✅ (工业控制系统)
//
// 2. "多变量时间序列预测的注意力机制研究" [评分: 89/100]
//    - 简洁性：✅ (17字)
//    - 可搜索性：✅ (核心术语靠前)
//    - 具体性：✅ (注意力机制、多变量)
//    - 建议：可考虑添加应用领域
//
// Suggested Typst Update:
// #align(center)[
//   #text(size: 18pt, weight: "bold")[
//     工业控制系统时间序列预测的Transformer方法
//   ]
// ]
// ============================================================
```

**交互式模式**（推荐）：
```bash
python scripts/optimize_title.py main.typ --interactive
# 逐步引导式标题创建，包含用户输入
```

**批量模式**（多篇论文）：
```bash
python scripts/optimize_title.py papers/*.typ --batch --output title_report.txt
```

**标题对比测试**（可选）：
```bash
python scripts/optimize_title.py main.typ --compare "Title A" "Title B" "Title C"
# 对比多个标题候选，提供详细评分
```

**最佳实践总结**：

**英文论文**：
1. **关键词前置**：Method + Problem 放在前 10 词
2. **具体明确**："Transformer" > "Deep Learning" > "Machine Learning"
3. **删除冗余**：去掉 "Novel", "Study", "Research", "Based on"
4. **控制长度**：目标 10-15 词
5. **测试可搜索性**：用这些关键词能找到你的论文吗？
6. **避免生僻**：除非是广泛认可的缩写（AI, LSTM, CNN）
7. **匹配会议风格**：IEEE（描述性）、ACM（创意性）、NeurIPS（简洁性）

**中文论文**：
1. **关键词前置**：方法+问题放在前 20 字
2. **具体明确**："Transformer" > "深度学习" > "机器学习"
3. **删除冗余**：去掉"关于"、"研究"、"新型"、"基于"
4. **控制长度**：目标 15-25 字
5. **测试可搜索性**：用这些关键词能找到你的论文吗？
6. **避免生僻**：除非是广泛认可的术语（AI、LSTM、CNN）
7. **中英对照**：确保英文标题与中文标题对应

**Typst 标题设置示例**：

**英文论文**：
```typst
#align(center)[
  #text(size: 18pt, weight: "bold")[
    Transformer-Based Time Series Forecasting for Industrial Control
  ]
]
```

**中文论文**：
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

参考资源：
- [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/)
- [Royal Society Blog on Title Optimization](https://royalsociety.org/blog/2025/01/title-abstract-and-keywords-a-practical-guide-to-maximizing-the-visibility-and-impact-of-your-papers/)
- [Academic Search Engine Optimization](https://openjournalsystems.com/academic-search-engine-optimization/)

---

### 模块：模板配置
**触发词**: template, 模板, IEEE, ACM, Springer, NeurIPS

模板配置示例与用法已移至参考文档：
- [TEMPLATES.md](references/TEMPLATES.md)

---

## 参考与扩展

为保持 SKILL 精简且易维护，详细示例与扩展内容移至参考文档：

- 期刊/会议规则：`references/VENUES.md`
- Typst 语法与排版：`references/TYPST_SYNTAX.md`
- 写作风格与常见错误：`references/STYLE_GUIDE.md`、`references/COMMON_ERRORS.md`
- 去AI化策略：`references/DEAI_GUIDE.md`
- 模板示例与配置：`references/TEMPLATES.md`

## 最佳实践

本技能遵循 Claude Code Skills 最佳实践：

### 技能设计原则 / Skill Design Principles
1. **职责单一 / Focused Responsibility**：每个模块处理一项特定任务（KISS 原则）
2. **最小权限 / Minimal Permissions**：仅请求必要的工具访问权限
3. **明确触发 / Clear Triggers**：使用特定关键词调用模块
4. **结构化输出 / Structured Output**：所有建议使用统一的 diff-comment 格式

### 使用指南 / Usage Guidelines
1. **先检查编译 / Start with Compilation**：在进行其他检查前，确保文档能正常编译
2. **迭代优化 / Iterative Refinement**：每次只应用一个模块，便于控制修改范围
3. **保护关键元素 / Preserve Protected Elements**：绝不修改 `@cite`、`@ref`、`@label`、数学环境
4. **提交前验证 / Verify Before Commit**：接受修改前仔细审查所有建议

### 与其他工具集成 / Integration with Other Tools
- 配合版本控制（git）跟踪修改历史
- 使用 `typst watch` 实现实时预览（毫秒级编译）
- 导出建议与合作者共同审阅

### Typst 特有优势 / Typst-Specific Advantages
- **编译速度**：毫秒级编译，适合实时预览和快速迭代
- **现代语法**：比 LaTeX 更简洁直观的标记语言
- **增量编译**：只重新编译修改的部分，提高效率

## 注意事项

1. **字体问题**：确保系统安装所需字体（中文建议 Source Han Serif 或 Noto Serif CJK）
2. **模板兼容性**：部分期刊可能仍要求 LaTeX 模板
3. **数学公式**：Typst 数学语法与 LaTeX 略有差异，需要适应
