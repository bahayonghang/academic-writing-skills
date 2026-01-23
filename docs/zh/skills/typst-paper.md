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

### 触发词

| 模块 | 触发词 | 功能 |
|------|--------|------|
| 编译 | compile, 编译, typst compile | Typst 编译 |
| 格式检查 | format, lint, 格式检查 | 格式检查 |
| 语法分析 | grammar, proofread, 语法 | 语法分析 |
| 长难句 | long sentence, 长句, simplify | 句子分解 |
| 表达 | academic tone, 学术表达 | 表达优化 |
| 翻译 | translate, 翻译, 中译英 | 中英翻译 |
| 参考文献 | bib, bibliography, 参考文献 | 文献检查 |
| 去AI化 | deai, 去AI化, humanize | 降低 AI 痕迹 |
| 模板 | template, IEEE, ACM, 模板 | 模板配置 |

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

### IEEE 模板

```typst
#import "@preview/charged-ieee:0.1.0": ieee

#show: ieee.with(
  title: [Your Paper Title],
  authors: (
    (
      name: "Author Name",
      department: [Department],
      organization: [University],
      location: [City, Country],
      email: "author@email.com"
    ),
  ),
  abstract: [
    Your abstract here...
  ],
  index-terms: ("Machine Learning", "Deep Learning"),
  bibliography: bibliography("references.bib"),
)

// Your content here
```

### ACM 模板

```typst
// ACM 两栏格式
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
  column-gutter: 0.33in
)

#set text(font: "Linux Libertine", size: 9pt)
#set par(justify: true)
```

### 通用学术论文模板

```typst
#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm)
)

#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em
)

#set heading(numbering: "1.1")

// 标题
#align(center)[
  #text(size: 16pt, weight: "bold")[Your Paper Title]
  
  #v(0.5em)
  
  Author Name#super[1], Co-author Name#super[2]
  
  #v(0.3em)
  
  #text(size: 10pt)[
    #super[1]University Name, #super[2]Institution Name
  ]
]

// 摘要
#heading(outlined: false, numbering: none)[Abstract]
Your abstract here...

// 正文
= Introduction
Your content here...
```

### 中文论文模板

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

// 标题
#align(center)[
  #text(size: 18pt, weight: "bold")[论文标题]
  
  #v(0.5em)
  
  作者姓名#super[1]，合作者姓名#super[2]
  
  #v(0.3em)
  
  #text(size: 10.5pt)[
    #super[1]大学名称，#super[2]机构名称
  ]
]

// 摘要
#heading(outlined: false, numbering: none)[摘要]
摘要内容...

*关键词*：关键词1；关键词2；关键词3

// 正文
= 引言
正文内容...
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

## 参考文件

- `references/TYPST_SYNTAX.md`：Typst 语法指南
- `references/STYLE_GUIDE.md`：学术写作规范
- `references/COMMON_ERRORS.md`：常见错误
- `references/VENUES.md`：期刊会议要求
- `references/DEAI_GUIDE.md`：去AI化写作指南

## 下一步

- [编译配置指南](/zh/guides/compilation)
- [格式检查指南](/zh/guides/format-checking)
- [参考文献指南](/zh/guides/bibliography)
