# Typst 学术论文 (typst-paper)

现代化的 Typst 学术论文写作助手。

## 概述

`typst-paper` 技能为使用 Typst 进行学术论文写作提供全面支持。Typst 是一个现代化的排版系统，编译速度达到毫秒级。支持中英文论文及主流出版场所。

### 主要功能

- **闪电般的编译速度**（毫秒级 vs LaTeX 的秒级）
- **简洁直观的语法**（比 LaTeX 更易学习）
- **实时预览**支持监视模式
- **格式检查**支持特定场所规则
- **语法分析**用于英文论文
- **学术表达优化**支持中英文
- **中英学术翻译**（深度学习、时间序列、工业控制）
- **去AI化编辑**降低 AI 生成文本痕迹
- **模板支持**（IEEE、ACM、Springer、NeurIPS 等）

## 环境要求

**安装**：
```bash
# 使用 Cargo（Rust 包管理器）
cargo install typst-cli

# 使用 Homebrew（macOS）
brew install typst

# 使用包管理器（Linux）
sudo pacman -S typst  # Arch Linux
```

**验证安装**：
```bash
typst --version
```

## 在 Claude Code 中使用技能

本技能设计用于 Claude Code 等 AI 助手。只需在对话中提及相关触发词，助手就会激活相应模块。

### 参数约定

请求中请尽量包含：
- **主 `.typ` 路径**（执行脚本时必需）
- **目标范围**（章节/段落或全文）
- **模块选择**（编译/格式/语法/模板等）

如信息缺失或含糊，助手会先确认，不会猜测路径或范围。

### 执行约束

- 仅在您明确要求时执行脚本/编译命令。
- 覆盖输出或清理类操作前先确认。

### 触发词

| 模块 | 触发词 | 功能 |
|------|--------|------|
| 编译 | compile, 编译, typst compile | Typst 编译 |
| 格式检查 | format, lint, 格式检查 | 格式检查 |
| 语法分析 | grammar, proofread, 语法 | 语法分析 |
| 长难句 | long sentence, 长句, simplify | 句子分解 |
| 表达 | academic tone, 学术表达 | 表达优化 |
| 逻辑衔接与方法论 | logic, coherence, 逻辑, 衔接, methodology, 方法论 | 逻辑衔接与方法论深度 |
| 翻译 | translate, 翻译, 中译英 | 中英翻译 |
| 参考文献 | bib, bibliography, 参考文献 | 文献检查 |
| 引用完整性 | ref, label, 引用检查, 引用完整性 | 图表引用完整性验证 🆕 |
| 去AI化 | deai, 去AI化, humanize | 降低 AI 痕迹 |
| 模板 | template, IEEE, ACM, 模板 | 模板配置 |
| 标题优化 | title, 标题, title optimization | 标题生成与优化 🆕 |

### 使用示例

**编译论文**：
```
请编译我的 Typst 论文 main.typ
```

**检查语法**：
```
能帮我检查引言部分的语法吗？
```

**翻译成英文**：
```
将以下中文翻译为学术英文（深度学习领域）：
本文提出了一种基于Transformer的方法...
```

## 输出协议

所有建议采用注释式 diff 格式，并包含固定字段：
- **严重级别**：Critical / Major / Minor
- **优先级**：P0 / P1 / P2

最小模板：
```typst
// <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
// 原文：...
// 修改后：...
// 理由：...
// ⚠️ 【待补证】：<需要证据/数据时标记>
```

## 失败处理

- 缺少 Typst：安装 `typst-cli` 并加入 PATH
- 缺少文件/脚本：确认工作目录与 `scripts/` 路径
- 编译失败：优先给出首个错误摘要并请求日志片段

## 模块快速示例

```
检查 main.typ 的格式合规性
```

```
拆解引言中的长句
```

```
提升摘要的学术表达
```

```
验证 references.bib 并检查 main.typ 的引用
```

```
去AI化方法部分并保持事实不变
```

```
提供 Typst 的 IEEE 模板配置
```

## 编译模块

### 基本命令

| 命令 | 用途 | 说明 |
|------|------|------|
| `typst compile main.typ` | 单次编译 | 生成 PDF 文件 |
| `typst watch main.typ` | 监视模式 | 文件变化时自动重新编译 |
| `typst compile main.typ output.pdf` | 指定输出 | 自定义输出文件名 |
| `typst compile --format png main.typ` | 其他格式 | 支持 PNG、SVG 等格式 |
| `typst fonts` | 字体列表 | 查看系统可用字体 |

### 使用示例

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

### 编译速度优势

- Typst 编译速度通常在毫秒级（vs LaTeX 的秒级）
- 增量编译：只重新编译修改的部分
- 适合实时预览和快速迭代

### 中文支持

```typst
// 中文字体配置示例
#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  lang: "zh",
  region: "cn"
)
```

## 格式检查模块

### 检查项目

| 类别 | 检查内容 | 标准 |
|------|----------|------|
| 页边距 | 上下左右边距 | 通常 1 英寸（2.54cm）|
| 行间距 | 单倍/双倍行距 | 根据期刊要求 |
| 字体 | 正文字体与大小 | Times New Roman 10-12pt |
| 标题 | 各级标题格式 | 层次清晰，编号正确 |
| 图表 | 标题位置与格式 | 图下表上，编号连续 |
| 引用 | 引用格式一致性 | 数字/作者-年份格式 |

### Typst 格式配置

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

## 语法分析模块

基于 LLM 的语法检查，重点关注：
- 主谓一致
- 冠词使用（a/an/the）
- 时态一致性（方法用过去时，结果用现在时）
- 中式英语检测

### 常见语法错误

| 错误类型 | 示例 | 修正 |
|----------|------|------|
| 冠词缺失 | propose method | propose a method |
| 主谓不一致 | The data shows | The data show |
| 时态混乱 | We proposed... The results shows | We proposed... The results show |
| 中式英语 | more and more | increasingly |

## 长难句分析模块

### 触发条件

- 英文：句子 >50 词 或 >3 个从句
- 中文：句子 >60 字 或 >3 个分句

### 输出格式

```typst
// 长难句检测（第45行，共67词）[Severity: Minor] [Priority: P2]
// 主干：[主语 + 谓语 + 宾语]
// 修饰成分：
//   - [关系从句] which...
//   - [目的状语] to...
// 建议改写：[简化版本]
```

## 学术表达模块

### 英文学术表达

| ❌ 弱动词 | ✅ 学术替代 |
|----------|------------|
| use | employ, utilize, leverage |
| get | obtain, achieve, acquire |
| make | construct, develop, generate |
| show | demonstrate, illustrate, indicate |

### 中文学术表达

| ❌ 口语化 | ✅ 学术化 |
|----------|----------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |
| 可以看出 | 由此可见 |

## 逻辑衔接与方法论深度模块

确保段落间逻辑流畅，强化方法论的严谨性。

### AXES 模型（段落级逻辑衔接）

| 组成部分 | 说明 | 示例 |
|----------|------|------|
| **A**ssertion（主张） | 清晰的主题句，陈述核心观点 | "注意力机制能够提升序列建模效果。" |
| **X**ample（例证） | 支撑主张的具体证据或数据 | "实验中，注意力机制达到95%准确率。" |
| **E**xplanation（解释） | 分析证据为何支撑主张 | "这一提升源于其捕获长程依赖的能力。" |
| **S**ignificance（意义） | 与更广泛论点或下一段的联系 | "这一发现为本文架构设计提供了依据。" |

### 过渡信号词

| 关系类型 | 中文信号词 | 英文对应 |
|----------|------------|----------|
| 递进 | 此外、进一步、更重要的是 | furthermore, moreover |
| 转折 | 然而、但是、相反 | however, nevertheless |
| 因果 | 因此、由此可见、故而 | therefore, consequently |
| 顺序 | 首先、随后、最后 | first, subsequently, finally |
| 举例 | 例如、具体而言、特别是 | for instance, specifically |

### 方法论深度检查清单

- 每个主张都有证据支撑（数据、引用或逻辑推理）
- 方法选择有充分理由（为何选此方法而非其他？）
- 明确承认研究局限性
- 清晰陈述前提假设
- 可复现性细节充分（参数、数据集、评估指标）

### 常见问题

| 问题类型 | 表现 | 修正方法 |
|----------|------|----------|
| 逻辑断层 | 段落间缺乏衔接 | 添加过渡句说明段落关系 |
| 无据主张 | 断言缺乏证据支撑 | 补充引用、数据或推理 |
| 方法论浅薄 | "本文采用X"但无理由 | 解释为何X适合本问题 |
| 隐含假设 | 前提条件未明示 | 显式陈述假设条件 |

### 在 Claude Code 中使用

```
检查引言部分的逻辑衔接
```

```
分析方法部分的方法论深度
```

```
在段落之间添加过渡信号词
```

## 翻译模块（中译英）

### 支持领域

| 领域 | 关键词 |
|------|--------|
| 深度学习 | 神经网络、注意力机制、损失函数 |
| 时间序列 | 时序预测、ARIMA、时间模式 |
| 工业控制 | PID、故障检测、SCADA |

### 翻译流程

1. **领域识别** - 确定专业领域术语
2. **术语确认** - 确认翻译
3. **翻译并注释** - 带注释的翻译
4. **中式英语检查** - 检测并修正常见错误
5. **学术润色** - 最终审查

### 常用学术句式

| 中文 | English |
|------|---------|
| 本文提出... | We propose... / This paper presents... |
| 实验结果表明... | Experimental results demonstrate that... |
| 与...相比 | Compared with... / In comparison to... |
| 综上所述 | In summary / In conclusion |

## 参考文献模块

### Typst 参考文献管理

**方法 1：使用 BibTeX 文件**
```typst
#bibliography("references.bib", style: "ieee")
```

**方法 2：使用 Hayagriva 格式**
```typst
#bibliography("references.yml", style: "apa")
```

### 支持的引用样式

- `ieee` - IEEE 数字引用
- `apa` - APA 作者-年份
- `chicago-author-date` - 芝加哥作者-年份
- `mla` - MLA 人文学科
- `gb-7714-2015` - 中国国标

### 引用示例

```typst
// 文中引用
According to @smith2020, the method...
Recent studies @smith2020 @jones2021 show...

// 参考文献列表
#bibliography("references.bib", style: "ieee")
```

```bash
# 在线验证（CrossRef + Semantic Scholar）
python scripts/verify_bib.py references.bib --online
python scripts/verify_bib.py references.bib --online --email you@example.com
```

## 去AI化编辑模块

在保持 Typst 语法和技术准确性的前提下，降低 AI 写作痕迹。

### 输入要求

1. **源码类型**（必填）：Typst
2. **章节**（必填）：Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion
3. **源码片段**（必填）：直接粘贴（保留原缩进）

### 工作流程

**1. 语法结构识别**
检测 Typst 语法，完整保留：
- 函数调用：`#set`, `#show`, `#let`
- 引用：`@cite`, `@ref`, `@label`
- 数学：`$...$`, `$ ... $`（块级）
- 标记：`*bold*`, `_italic_`, `` `code` ``
- 自定义函数（默认不改）

**2. AI 痕迹检测**：

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

### 硬性约束

- **绝不修改**：`@cite`, `@ref`, `@label`, 数学环境
- **绝不新增**：事实、数据、结论、指标、实验设置、引用编号
- **仅修改**：普通段落文字、标题文本

### 分章节准则

| 章节 | 重点 | 约束 |
|------|------|------|
| Abstract | 目的/方法/关键结果（带数字）/结论 | 禁泛泛贡献 |
| Introduction | 重要性→空白→贡献（可核查） | 克制措辞 |
| Related Work | 按路线分组，差异点具体化 | 具体对比 |
| Methods | 可复现优先（流程、参数、指标定义） | 实现细节 |
| Results | 仅报告事实与数值 | 不解释原因 |
| Discussion | 讲机制、边界、失败、局限 | 批判性分析 |
| Conclusion | 回答研究问题，不引入新实验 | 可执行未来工作 |

## 模板配置模块

模板示例与用法请参考 `references/TEMPLATES.md`。

## 标题优化模块

根据 IEEE/ACM/Springer/NeurIPS 最佳实践，生成和优化学术论文标题。

### 核心原则

基于 IEEE Author Center 及顶级会议/期刊指南：

**英文论文**：
1. **简洁性**：删除 "A Study of", "Research on", "Novel", "New"
2. **可搜索性**：核心术语（方法+问题）在前 65 字符内
3. **长度**：最佳 10-15 词
4. **具体性**：具体方法/问题名称
5. **规范性**：避免生僻缩写

**中文论文**：
1. **简洁性**：删除"关于...的研究"、"新型"、"改进的"
2. **可搜索性**：核心术语在前 20 字内
3. **长度**：最佳 15-25 字
4. **具体性**：具体术语
5. **规范性**：符合规范

### 质量评分

每个标题获得 0-100 分，基于五个标准：
- 简洁性 (25%)
- 可搜索性 (30%)
- 长度 (15%)
- 具体性 (20%)
- 规范性 (10%)

### 在 Claude Code 中使用

**检查现有标题**：
```
检查我的论文标题质量
```

**生成标题候选**：
```
根据摘要生成标题候选方案
```

**优化现有标题**：
```
优化我的论文标题，符合 IEEE 最佳实践
```

### 标题模式

**英文**：
- Method for Problem: "Transformer for Time Series Forecasting"
- Method: Problem in Domain: "Graph Neural Networks: Fault Detection in Industrial Systems"
- Problem via Method: "Time Series Forecasting via Attention Mechanisms"

**中文**：
- 问题的方法: "时间序列预测的Transformer方法"
- 方法及应用: "注意力机制及其在工业控制中的应用"
- 面向领域的方法: "面向智能制造的深度学习方法"

### 好与差的示例

**英文**：
```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"
```

**中文**：
```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究
```

### Typst 标题配置

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

## 期刊/会议特定规则

### IEEE

- 两栏格式，列间距 0.33 英寸
- Times New Roman 10pt
- 主动语态，方法用过去时
- 图表编号：Fig. 1, Table I

### ACM

- 两栏格式，A4 或 US Letter
- 现在时表述一般真理
- 引用格式：数字或作者-年份

### Springer

- 图标题在下，表标题在上
- 参考文献按字母顺序排列

### NeurIPS/ICML

- 8 页限制（不含参考文献）
- 匿名提交（双盲评审）
- 特定格式要求

## Typst 优势总结

### vs LaTeX

| 特性 | Typst | LaTeX |
|------|-------|-------|
| 编译速度 | 毫秒级 | 秒级 |
| 语法 | 简洁直观 | 复杂冗长 |
| 错误提示 | 清晰友好 | 晦涩难懂 |
| 学习曲线 | 平缓 | 陡峭 |
| 实时预览 | 原生支持 | 需要额外工具 |

### 适用场景

- ✅ 快速原型和草稿
- ✅ 需要频繁修改的文档
- ✅ 团队协作（语法简单）
- ✅ 中小型论文（<100 页）
- ⚠️ 复杂数学公式（LaTeX 更成熟）
- ⚠️ 特定期刊模板（可能需要 LaTeX）

## 快速开始

**安装 Typst**：
```bash
# 使用 Cargo（Rust 包管理器）
cargo install typst-cli

# 使用 Homebrew（macOS）
brew install typst

# 使用包管理器（Linux）
sudo pacman -S typst  # Arch Linux
```

**创建第一个论文**：
```bash
# 从模板初始化
typst init @preview/charged-ieee

# 编译
typst compile main.typ

# 监视模式（推荐）
typst watch main.typ
```

**常用命令**：
```bash
# 查看帮助
typst --help

# 查看可用字体
typst fonts

# 指定输出格式
typst compile --format png main.typ

# 使用自定义字体
typst compile --font-path ./fonts main.typ
```

## 推荐工作流

### 草稿快速迭代
1. 编译或监视模式
2. 基础格式检查
3. 语法分析（摘要 + 引言）

### 投稿前检查
1. 期刊/会议格式检查
2. 学术表达优化
3. 去AI化编辑
4. 参考文献验证
5. 模板配置核对（如期刊要求）

## 参考文件

- `references/TYPST_SYNTAX.md`：Typst 语法指南
- `references/STYLE_GUIDE.md`：学术写作规范
- `references/COMMON_ERRORS.md`：常见错误
- `references/VENUES.md`：期刊会议要求
- `references/DEAI_GUIDE.md`：去AI化写作指南
- `references/TEMPLATES.md`：Typst 模板示例
- `scripts/check_references.py`：引用完整性检查器（独立运行）
- `scripts/online_bib_verify.py`：在线文献验证器
