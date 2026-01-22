---
name: typst-paper
description: |
  Typst 学术论文助手（支持中英文论文、会议/期刊投稿）。
  领域：深度学习、时间序列、工业控制、计算机科学。
  
  触发词（可独立调用任意模块）：
  - "compile", "编译", "typst compile" → 编译模块
  - "format", "格式检查", "lint" → 格式检查模块
  - "grammar", "语法", "proofread", "润色" → 语法分析模块
  - "long sentence", "长句", "simplify", "拆解" → 长难句分析模块
  - "academic tone", "学术表达", "improve writing" → 学术表达模块
  - "translate", "翻译", "中译英" → 翻译模块
  - "bib", "bibliography", "参考文献" → 参考文献模块
  - "deai", "去AI化", "humanize", "降低AI痕迹" → 去AI化编辑模块
  - "template", "模板", "IEEE", "ACM" → 模板配置模块
---

# Typst 学术论文助手

## 核心原则

1. 绝不修改 `@cite`、`@ref`、`@label`、数学环境内的内容
2. 绝不凭空捏造参考文献条目
3. 绝不在未经许可的情况下修改专业术语
4. 始终先以注释形式输出修改建议
5. Typst 编译速度快（毫秒级），适合实时预览

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
- **Typst 未安装**：建议通过 `cargo install typst-cli` 或包管理器安装
- **字体缺失**：使用 `typst fonts` 查看可用字体
- **文件不存在**：请用户提供正确 `.typ` 路径

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

### 模块：模板配置
**触发词**: template, 模板, IEEE, ACM, Springer, NeurIPS

**Typst 学术模板**:

**IEEE 模板**:
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

**ACM 模板**:
```typst
// 使用 ACM 两栏格式
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
  column-gutter: 0.33in
)

#set text(font: "Linux Libertine", size: 9pt)
#set par(justify: true)
```

**通用学术论文模板**:
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

**中文论文模板**:
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

---

## 期刊/会议特定规则

**IEEE**:
- 两栏格式，列间距 0.33 英寸
- Times New Roman 10pt
- 主动语态，方法用过去时
- 图表编号：Fig. 1, Table I

**ACM**:
- 两栏格式，A4 或 US Letter
- 现在时表述一般真理
- 引用格式：数字或作者-年份

**Springer**:
- 图标题在下，表标题在上
- 参考文献按字母顺序排列

**NeurIPS/ICML**:
- 8 页限制（不含参考文献）
- 匿名提交（双盲评审）
- 特定格式要求

---

## 完整工作流（可选）

如需完整审查，按顺序执行：

**英文论文**:
1. 格式检查 → 修复格式问题
2. 语法分析 → 修复语法错误
3. 去AI化编辑 → 降低 AI 写作痕迹
4. 长难句分析 → 简化复杂句
5. 学术表达 → 提升学术语气

**中文论文**:
1. 格式检查 → 修复格式问题
2. 去AI化编辑 → 降低 AI 写作痕迹
3. 学术表达 → 改进表达
4. 长难句分析 → 简化复杂句
5. 参考文献 → 验证引用

---

## Typst 优势总结

**vs LaTeX**:
| 特性 | Typst | LaTeX |
|------|-------|-------|
| 编译速度 | 毫秒级 | 秒级 |
| 语法 | 简洁直观 | 复杂冗长 |
| 错误提示 | 清晰友好 | 晦涩难懂 |
| 学习曲线 | 平缓 | 陡峭 |
| 实时预览 | 原生支持 | 需要额外工具 |

**适用场景**:
- ✅ 快速原型和草稿
- ✅ 需要频繁修改的文档
- ✅ 团队协作（语法简单）
- ✅ 中小型论文（<100 页）
- ⚠️ 复杂数学公式（LaTeX 更成熟）
- ⚠️ 特定期刊模板（可能需要 LaTeX）

---

## 输出报告模板

```markdown
# Typst 学术论文审查报告

## 总览
- 整体状态：✅ 符合要求 / ⚠️ 需要修订 / ❌ 重大问题
- 编译状态：[status]
- 模板类型：[detected template]
- 语言：[English / 中文]

## 格式审查
### ✅ 符合项
### ❌ 不符合项

## 语法/表达（N处建议）
[按优先级分组]

## 长难句拆解（M处）
[详细分析]

## 参考文献
- 总数：X 篇
- 引用格式：[style]
- 问题：[issues if any]
```

---

## 参考资源

**Typst 官方资源**:
- [Typst 官网](https://typst.app/)
- [Typst 文档](https://typst.app/docs/)
- [Typst Universe](https://typst.app/universe/) - 模板和包

**学术写作指南**:
- IEEE 写作规范
- ACM 投稿指南
- APA/MLA 引用格式
- GB/T 7714-2015（中文国标）

**工具推荐**:
- Grammarly - 语法检查
- Hemingway Editor - 可读性分析
- Zotero - 参考文献管理
- Typst Web App - 在线编辑器

---

## 快速开始

**安装 Typst**:
```bash
# 使用 Cargo（Rust 包管理器）
cargo install typst-cli

# 使用 Homebrew（macOS）
brew install typst

# 使用包管理器（Linux）
# Arch Linux
sudo pacman -S typst

# Ubuntu/Debian（需要添加 PPA）
# 或直接下载二进制文件
```

**创建第一个论文**:
```bash
# 从模板初始化
typst init @preview/charged-ieee

# 编译
typst compile main.typ

# 监视模式（推荐）
typst watch main.typ
```

**常用命令**:
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

---

## 注意事项

1. **字体问题**：确保系统安装了所需字体（中文需要 Source Han Serif 或 Noto Serif CJK）
2. **模板兼容性**：部分期刊可能仍要求 LaTeX 格式
3. **数学公式**：Typst 数学语法与 LaTeX 略有不同，需要适应
4. **包生态**：Typst 生态相对年轻，某些高级功能可能需要自己实现
5. **版本控制**：Typst 文件是纯文本，适合 Git 版本控制

---

## 常见问题

**Q: Typst 能完全替代 LaTeX 吗？**
A: 对于大多数学术论文，Typst 已经足够。但某些特定期刊模板或复杂排版需求可能仍需 LaTeX。

**Q: 如何处理中文？**
A: 使用 `#set text(lang: "zh", region: "cn")` 并配置中文字体。

**Q: 参考文献格式如何选择？**
A: 根据目标期刊要求选择，Typst 支持 IEEE、APA、MLA、GB7714 等主流格式。

**Q: 编译速度真的快吗？**
A: 是的，Typst 编译通常在毫秒级完成，适合实时预览。

**Q: 如何与团队协作？**
A: 可以使用 Typst Web App 在线协作，或通过 Git 进行版本控制。
