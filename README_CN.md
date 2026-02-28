# Claude Code 学术写作 Skills

[English](README.md) | [📚 文档](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs)

> 基于 Claude Code 的学术写作助手，支持 LaTeX 和 Typst，涵盖英文论文和中文学位论文。

> **⚠️ 免责声明**:本项目为个人自用状态,不保证功能完善或稳定性。如遇到问题,请通过 [Issues](https://github.com/bahayonghang/academic-writing-skills/issues) 提交反馈。

## 文档

**📖 完整文档请访问 [docs](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs) 目录。**

本地查看文档：

```bash
cd docs
npm install
npm run docs:dev
```

然后在浏览器中打开 http://localhost:5173。

## 功能特性

### latex-paper-en（英文学术论文）
- **格式检查**：集成 ChkTeX 进行 LaTeX 语法检查
- **编译支持**：通过 latexmk 支持 pdfLaTeX/XeLaTeX/LuaLaTeX
- **语法分析**：中式英语检测、弱动词替换建议
- **长难句分析**：复杂句子拆解与重构建议
- **表达优化**：学术语气改进
- **逻辑衔接与方法论**：段落衔接（AXES 模型）、过渡信号词、方法论深度检查 🆕
- **标题优化**：根据 IEEE/ACM/Springer 最佳实践生成和优化论文标题
- **图表标题生成与优化**：按照顶会标准生成极简、一致大小写、无 AI 味的英文及双语 Caption 🆕
- **实验分析生成**：基于核心数据生成包含基线对比、消融研究并符合顶刊连贯叙事规范的实验段落 🆕
- **去AI化编辑**：在保持技术准确性的同时降低 AI 写作痕迹
- **期刊适配**：IEEE、ACM、Springer、NeurIPS、ICML 格式指南
- **引用完整性检查**：未定义引用、未引用的 label、缺少 caption 检测 🆕
- **文献验证**：BibTeX 格式校验，支持可选的 CrossRef/Semantic Scholar 在线验证 🆕

### latex-thesis-zh（中文学位论文）
- **结构映射**：多文件论文结构分析
- **国标检查**：符合 GB/T 7714-2015 参考文献规范
- **模板检测**：支持 thuthesis、pkuthss、ustcthesis、fduthesis 等模板
- **中文学术规范**：口语化表达检测、术语一致性检查
- **逻辑衔接与方法论**：段落衔接（AXES 模型）、过渡信号词、方法论深度检查 🆕
- **标题优化**：根据 GB/T 7713.1-2006 规范生成和优化学位论文标题
- **图表标题生成与优化**：按照顶会标准生成极简、一致大小写、无 AI 味的英文及双语 Caption 🆕
- **实验分析生成**：基于核心数据生成包含基线对比、消融研究并符合核心期刊连贯叙述规范的实验段落 🆕
- **去AI化编辑**：在保持技术准确性的同时降低 AI 写作痕迹
- **编译支持**：XeLaTeX/LuaLaTeX 完整中文支持
- **引用完整性检查**：未定义引用、未引用的 label、缺少 caption 检测 🆕
- **文献验证**：BibTeX 格式校验，支持可选的 CrossRef/Semantic Scholar 在线验证 🆕

### typst-paper（Typst 学术论文）
- **快速编译**：毫秒级编译速度
- **双语支持**：同时支持英文和中文论文
- **格式检查**：页面设置、文本格式、引用检查
- **语法分析**：与 LaTeX 版本相同，适配 Typst 语法
- **逻辑衔接与方法论**：段落衔接（AXES 模型）、过渡信号词、方法论深度检查 🆕
- **去AI化编辑**：降低 AI 写作痕迹
- **标题优化**：双语标题生成和优化（中英文）
- **图表标题生成与优化**：按照顶会标准生成极简、一致大小写、无 AI 味的英文及双语 Caption 🆕
- **实验分析生成**：基于核心数据生成包含基线对比、消融研究的连贯分析段落 🆕
- **期刊模板**：IEEE、ACM、Springer、NeurIPS 模板
- **现代语法**：简洁直观的标记语言
- **引用完整性检查**：未定义引用、未引用的 label、缺少 caption 检测 🆕
- **文献验证**：BibTeX 格式校验，支持可选的 CrossRef/Semantic Scholar 在线验证 🆕

### paper-audit（自动化论文审查）🆕
- **多格式支持**：接受 `.tex`、`.typ` 和 `.pdf` 文件
- **三种审查模式**：self-check（全面审查）、review（重点审查）、gate（投稿门控检查）
- **PDF 视觉排版检查**：页边距溢出、文本/图片块重叠、字体不一致、低分辨率图片、空白页检测
- **引用完整性检查**：未定义引用、未引用的 label、缺少 caption、引用顺序、编号间隙
- **ScholarEval 学术评估**：8 维度质量评分（1-10 分），给出投稿可读性标签
- **实验叙事与标题审查**：检查图表标题格式（Caption Audit）与实验段落的分析深度及连贯叙事（Experiment Narrative） 🆕
- **在线文献验证**：CrossRef + Semantic Scholar API 验证（无需 API 密钥）
- **去AI化编辑**：降低 AI 写作痕迹
- **NeurIPS 对齐评分**：Quality/Clarity/Significance/Originality 1-6 分加权报告

## 输出协议

所有建议采用注释式 diff 格式，并包含固定字段：
- **严重级别**：Critical / Major / Minor
- **优先级**：P0 / P1 / P2

最小模板：
```latex
% <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
% 原文：...
% 修改后：...
% 理由：...
% ⚠️ 【待补证】：<需要证据/数据时标记>
```

## 失败处理

- 缺少编译工具：安装 TeX Live/MiKTeX 并加入 PATH
- 缺少文件/脚本：确认工作目录与 `scripts/` 路径
- 编译失败：优先给出首个错误摘要并请求日志片段

## 安装方法

有两种方式安装这些技能：使用 `skilks`（推荐）或手动安装。

### 方式 1：使用 skilks（推荐）

你可以使用 [skilks](https://github.com/bahayonghang/skilks)（Claude Code 的社区技能管理器）轻松安装：

```bash
# 安装特定技能
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skilks add github.com/bahayonghang/academic-writing-skills/typst-paper
npx skilks add github.com/bahayonghang/academic-writing-skills/paper-audit

# 或一次性安装所有技能
npx skilks add github.com/bahayonghang/academic-writing-skills
```

### 方式 2：手动安装

1. 克隆仓库：

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
```

2. 将 skill 文件夹复制到 Claude Code 的 skills 目录：

#### Linux / macOS

```bash
# 创建 skills 目录（如不存在）
mkdir -p ~/.claude/skills

# 复制 skill 文件夹
cp -r latex-paper-en ~/.claude/skills/
cp -r latex-thesis-zh ~/.claude/skills/
cp -r typst-paper ~/.claude/skills/
cp -r paper-audit ~/.claude/skills/
```

#### Windows (PowerShell)

```powershell
# 创建 skills 目录（如不存在）
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force

# 复制 skill 文件夹
Copy-Item -Recurse "latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "typst-paper" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "paper-audit" "$env:USERPROFILE/.claude/skills/"
```



## 快速开始

直接与 Claude Code 对话并提出需求，技能会根据关键词自动触发。

### 编译配置

| 配置 | 步骤 | 适用场景 |
|------|------|----------|
| `xelatex` | 仅 XeLaTeX | 中文快速编译 |
| `pdflatex` | 仅 PDFLaTeX | 英文快速编译 |
| `latexmk` | LaTeXmk 自动 | 自动处理依赖 |
| `xelatex-bibtex` | xelatex → bibtex → xelatex×2 | 中文 + BibTeX |
| `xelatex-biber` | xelatex → biber → xelatex×2 | 中文 + Biber（推荐）|
| `pdflatex-bibtex` | pdflatex → bibtex → pdflatex×2 | 英文 + BibTeX |
| `pdflatex-biber` | pdflatex → biber → pdflatex×2 | 英文 + Biber |

### 常见使用场景

**编译文档**
- "用 xelatex-biber 编译我的论文"
- "编译 LaTeX 文档"
- "compile my paper"

**翻译（中译英）**
- "翻译这段文字为英文"
- "中译英这个章节"
- "translate this section to English"
- 自动识别领域术语（深度学习、时间序列、工业控制）
- 检测中式英语并提供改进建议

**去AI化编辑（降低AI写作痕迹）**
- "去AI化这段引言"
- "降低这段文字的AI痕迹"
- "deai check my introduction"
- 删除空话口号、过度确定表达、机械排比结构
- 完整保留所有 LaTeX/Typst 语法和引用

**语法与风格**
- "检查摘要的语法"
- "提升学术语气"
- "check grammar in abstract"
- 检测主谓一致、冠词使用、时态一致性
- 建议学术表达改进

**格式检查**
- "检查格式规范"
- "验证国标格式" (中文论文)
- "check format compliance"

**参考文献**
- "验证参考文献"
- "检查引用一致性"
- "verify my bibliography"

**长难句分析**
- "简化这个复杂句子"
- "拆解长难句"
- "simplify this complex sentence"
- 自动触发：英文句子 >50 词或中文句子 >60 字

**逻辑衔接与方法论** 🆕
- "检查引言的逻辑衔接"
- "分析方法论深度"
- "check logical coherence"
- "analyze methodological depth"
- 使用 AXES 模型（主张、例证、解释、意义）检查段落衔接
- 检查过渡信号词和方法论严谨性

**标题优化**
- "优化我的论文标题"
- "生成标题候选方案"
- "optimize my paper title"
- "generate title candidates"
- 遵循 IEEE/ACM/Springer/NeurIPS 最佳实践
- 删除无效词汇（"新型"、"关于...的研究"、"Novel"、"A Study of"）
- 确保关键词（方法+问题）出现在前 65 字符（英文）或前 20 字（中文）
- 提供多个候选方案并评分（0-100 分）

**实验分析优化** 🆕
- "帮我分析这些实验数据，写成 IEEE 顶刊标准的段落"
- "生成消融实验分析"
- "analyze my experiment data and write results section"
- 严格遵循使用连贯段落及 `\paragraph{}` 引导结论的要求，防止过度依赖 itemize
- 充分体现基线对比和重要消融数据

**图表标题优化** 🆕
- "生成符合顶会规范的表标题"
- "优化这张图的标题"
- "生成双语caption"
- 遵循 Title case 和 Sentence case 规范，移除冗余及 AI 感。

**论文自动审查** 🆕
- "帮我全面审查这篇论文"
- "投稿前检查论文质量"
- "审查我的 PDF 排版问题"
- 支持 .tex、.typ、.pdf 文件
- 三种模式：self-check（全面）、review（重点）、gate（投稿门控）
- 添加 --online 可通过 CrossRef/Semantic Scholar 验证参考文献
- 添加 --scholar-eval 可获得 8 维度 ScholarEval 质量评估

**引用完整性检查** 🆕
- "检查论文的图表引用"
- "查找未定义的标签"
- "find undefined labels in my paper"
- 检测：未定义的 \ref{}、未引用的 \label{}、缺少 caption、前向引用

**📖 详细使用方法和示例请查看[文档](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs)。**

## 项目结构

```
academic-writing-skills/
├── latex-paper-en/                   # 英文论文 skill
│   ├── SKILL.md                      # Skill 定义
│   ├── README.md                     # 技能使用说明
│   ├── scripts/                      # Python 工具
│   │   ├── compile.py                # 统一编译器
│   │   ├── check_format.py           # ChkTeX 包装器
│   │   ├── verify_bib.py             # BibTeX 检查器
│   │   ├── optimize_title.py         # 标题优化器 🆕
│   │   ├── analyze_experiment.py     # 实验分析器 🆕
│   │   ├── check_references.py       # 引用完整性检查 🆕
│   │   ├── online_bib_verify.py      # 在线文献验证 🆕
│   │   └── extract_prose.py          # 文本提取器
│   └── resources/                    # 技能资源
│       ├── modules/                  # 模块指令
│       │   ├── COMPILE.md
│       │   └── ...
│       └── references/               # 参考文档
│           ├── STYLE_GUIDE.md        # 写作风格指南
│           ├── VENUES.md             # 期刊/会议规则
│           └── ...
│
├── latex-thesis-zh/                  # 中文论文 skill
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/
│   │   ├── compile.py
│   │   ├── map_structure.py          # 论文结构映射
│   │   ├── check_format.py
│   │   ├── check_consistency.py
│   │   ├── verify_bib.py             # BibTeX 检查器
│   │   ├── optimize_title.py         # 标题优化器 🆕
│   │   ├── analyze_experiment.py     # 实验分析器 🆕
│   │   ├── check_references.py       # 引用完整性检查 🆕
│   │   ├── online_bib_verify.py      # 在线文献验证 🆕
│   │   └── detect_template.py        # 模板检测器
│   └── resources/                    # 技能资源
│       ├── GB_STANDARD.md            # 国标格式规范
│       ├── ACADEMIC_STYLE_ZH.md      # 中文学术规范
│       ├── STRUCTURE_GUIDE.md        # 结构指南
│       └── UNIVERSITIES/             # 学校模板
│           ├── tsinghua.md           # 清华大学
│           ├── pku.md                # 北京大学
│           ├── yanshan.md            # 燕山大学
│           └── generic.md            # 通用模板
│
├── typst-paper/                      # Typst 论文 skill 🆕
│   ├── SKILL.md                      # Skill 定义
│   ├── README.md                     # 使用指南
│   ├── scripts/                      # Python 工具
│   │   ├── compile.py                # Typst 编译器
│   │   ├── check_format.py           # 格式检查器
│   │   ├── verify_bib.py             # 参考文献检查器
│   │   ├── optimize_title.py         # 标题优化器 🆕
│   │   ├── analyze_experiment.py     # 实验分析器 🆕
│   │   ├── check_references.py       # 引用完整性检查 🆕
│   │   └── online_bib_verify.py      # 在线文献验证 🆕
│   └── resources/                    # 技能资源
│       ├── modules/                  # 模块指令
│       └── references/               # 参考文档
│           ├── STYLE_GUIDE.md        # 写作风格指南
│           ├── DEAI_GUIDE.md         # 去AI化指南
│           ├── TEMPLATES.md          # 模板示例
│           └── TYPST_SYNTAX.md       # Typst 语法参考
│
├── paper-audit/                      # 论文审查 skill 🆕
│   ├── SKILL.md                      # Skill 定义
│   ├── scripts/                      # Python 工具
│   │   ├── audit.py                  # 主编排器
│   │   ├── pdf_parser.py             # PDF 文本提取
│   │   ├── detect_language.py        # 语言检测
│   │   ├── report_generator.py       # 报告生成
│   │   ├── check_references.py       # 引用完整性检查 🆕
│   │   ├── visual_check.py           # PDF 视觉排版检查 🆕
│   │   ├── scholar_eval.py           # ScholarEval 评估 🆕
│   │   └── online_bib_verify.py      # 在线文献验证（通过 audit.py）
│   └── resources/
│       └── references/
│           └── SCHOLAR_EVAL_GUIDE.md # ScholarEval 评分指南 🆕
│
└── docs/                             # 文档站点
```

## 系统要求

### LaTeX
- Python 3.8+
- TeX Live 或 MiKTeX（需包含 latexmk、chktex）
- 中文文档需要：XeLaTeX 及中文字体（SimSun、SimHei、KaiTi）

### Typst 🆕
- Python 3.8+
- Typst CLI（通过 `cargo install typst-cli` 或包管理器安装）
- 中文文档需要：中文字体（Source Han Serif、Noto Serif CJK SC）

## 支持的学校模板

| 学校 | 模板名称 | 特殊要求 |
|------|----------|----------|
| 清华大学 | thuthesis | 图表编号格式：图 3-1 |
| 北京大学 | pkuthss | 需包含符号说明章节 |
| 中国科学技术大学 | ustcthesis | - |
| 复旦大学 | fduthesis | - |
| 通用 | ctexbook | 遵循 GB/T 7713.1-2006 |

## 工作流程

### 英文论文审查流程

1. **Layer 0**：格式预检（ChkTeX + BibTeX 验证）
2. **Layer 1**：语法分析（只读模式）
3. **Layer 2**：长难句拆解
4. **Layer 3**：表达重构（注释形式输出）

### 中文论文审查流程

1. **Layer 0**：结构映射（必须首先执行）
2. **Layer 1**：结构完整性检查
3. **Layer 2**：国标格式审查（GB/T 7714）
4. **Layer 3**：中文学术表达检查
5. **Layer 4**：长难句拆解
6. **Layer 5**：表述重构

## 许可证

仅限学术用途 - 不得用于商业用途。

## 贡献

欢迎提交 Issue 和 Pull Request！
