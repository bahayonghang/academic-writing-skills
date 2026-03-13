# Claude Code 学术写作 Skills

[English](README.md)

> 专注于学术论文后期排版精修、格式校验与深度润色——拒绝从零代写，全面提升既有文本质量。
>
> 推荐平台：**Claude Code · Codex · Antigravity**

## 技能一览

| 技能 | 适用场景 | 支持格式 |
|---|---|---|
| [`latex-paper-en`](#latex-paper-en) | 英文学术论文 — IEEE / ACM / NeurIPS / ICML / Springer | `.tex` |
| [`latex-thesis-zh`](#latex-thesis-zh) | 中文学位论文 — GB/T 7714 / thuthesis / pkuthss | `.tex` |
| [`typst-paper`](#typst-paper) | 快速编译双语论文 | `.typ` |
| [`paper-audit`](#paper-audit) | 自动化投稿前审查与评分 | `.tex` `.typ` `.pdf` |
| [`industrial-ai-research`](#industrial-ai-research) | Industrial AI 文献综合与研究缺口分析 | — |

---

## 安装方法

### 方式 1：使用 skilks（推荐）

通过 [skilks](https://github.com/bahayonghang/skilks)（Claude Code 社区技能管理器）安装：

```bash
# 安装单个技能
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skilks add github.com/bahayonghang/academic-writing-skills/typst-paper
npx skilks add github.com/bahayonghang/academic-writing-skills/paper-audit
npx skilks add github.com/bahayonghang/academic-writing-skills/industrial-ai-research

# 或一次性安装所有技能
npx skilks add github.com/bahayonghang/academic-writing-skills
```

### 方式 2：手动安装

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills/academic-writing-skills
```

**Linux / macOS**

```bash
mkdir -p ~/.claude/skills
cp -r latex-paper-en latex-thesis-zh typst-paper paper-audit industrial-ai-research ~/.claude/skills/
```

**Windows (PowerShell)**

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force
foreach ($skill in @("latex-paper-en","latex-thesis-zh","typst-paper","paper-audit","industrial-ai-research")) {
    Copy-Item -Recurse $skill "$env:USERPROFILE/.claude/skills/"
}
```

---

## 功能特性

### latex-paper-en

面向 IEEE、ACM、Springer、NeurIPS、ICML 等顶级期刊/会议的英文论文编辑工具。

| 类别 | 功能 |
|---|---|
| **格式与编译** | ChkTeX 语法检查；pdfLaTeX / XeLaTeX / LuaLaTeX（通过 latexmk）|
| **语法** | 中式英语检测、弱动词替换、主谓一致性检查 |
| **长难句** | 复杂句拆解（超过 50 词自动触发）|
| **表达** | 学术语气改进、表达重构 |
| **逻辑** | 段落衔接（AXES 模型）、过渡信号词、方法论深度检查 |
| **标题** | IEEE/ACM/Springer 最佳实践生成；移除无效词；综合评分 0–100 |
| **图表标题** | Title/Sentence case 规范、无 AI 味的图表标题 |
| **实验分析** | 含 SOTA 对比与消融分析的连贯叙事段落 |
| **去AI化** | 人性化 AI 写作，完整保留所有 LaTeX 语法 |
| **反引用堆叠** | 每句最多 2 个并列引用；检测引言/相关工作中的堆叠式引用 |
| **引用** | 未定义 `\ref{}`、未引用 `\label{}`、缺少 caption；BibTeX 格式校验 |
| **在线验证** | CrossRef + Semantic Scholar 文献验证（无需 API 密钥）|
| **翻译** | 中译英学术翻译，自动识别领域术语 |

### latex-thesis-zh

符合 GB/T 7714-2015 及主流高校模板的中文学位论文编辑工具。

| 类别 | 功能 |
|---|---|
| **结构** | 多文件论文结构映射；章节完整性检查 |
| **参考文献** | GB/T 7714-2015 规范合规；BibTeX 格式校验 |
| **模板** | thuthesis / pkuthss / ustcthesis / fduthesis 自动检测 |
| **中文规范** | 口语化表达检测、术语一致性检查 |
| **逻辑** | 段落衔接（AXES 模型）、过渡信号词、方法论深度检查 |
| **标题** | 符合 GB/T 7713.1-2006 规范；中英文双语候选方案 |
| **图表标题** | 顶会标准双语 Caption（中文 + 英文）|
| **实验分析** | 含基线对比与消融覆盖的核心期刊叙事段落 |
| **去AI化** | 降低 AI 写作痕迹，完整保留所有 LaTeX 命令 |
| **反引用堆叠** | 每句最多 2 个并列引用；检测引言/文献综述中的堆叠式并列引用 |
| **编译** | XeLaTeX / LuaLaTeX 完整 CJK 字体支持 |
| **引用** | 与 `latex-paper-en` 相同的完整性检查；支持在线验证 |

**支持的高校模板**

| 高校 | 模板名称 | 说明 |
|---|---|---|
| 清华大学 | thuthesis | 图表编号格式：图 3-1 |
| 北京大学 | pkuthss | 需包含符号说明章节 |
| 中国科学技术大学 | ustcthesis | — |
| 复旦大学 | fduthesis | — |
| 通用 | ctexbook | 遵循 GB/T 7713.1-2006 |

### typst-paper

毫秒级编译的双语 Typst 论文编辑工具。

| 类别 | 功能 |
|---|---|
| **编译** | Typst CLI 封装，含错误摘要 |
| **格式** | 页面设置、文本格式、引用语法检查 |
| **语法** | 与 `latex-paper-en` 相同的检查，适配 Typst 语法 |
| **逻辑** | AXES 段落衔接、过渡信号词、方法论严谨性 |
| **标题** | 双语（中英文）标题生成与优化 |
| **图表标题** | 遵循 IEEE/ACM 标准的双语 Caption |
| **实验分析** | 面向期刊/会议的连贯叙事段落 |
| **去AI化** | 人性化 AI 写作；保留 `@cite`、`<label>`、`$...$` |
| **反引用堆叠** | 每句最多 2 个并列引用；检测引言/相关工作中的堆叠式引用 |
| **期刊模板** | IEEE、ACM、Springer、NeurIPS 模板指引 |
| **引用** | 未定义 `@ref`、未引用标签；支持在线验证 |

### paper-audit

多格式自动化审查工具，包含分层检查与质量评分。

| 类别 | 功能 |
|---|---|
| **输入** | `.tex`、`.typ`、`.pdf` 文件 |
| **模式** | `self-check`（全面审查）· `review`（重点审查）· `gate`（投稿门控）|
| **视觉排版** | 页边距溢出、文本/图片重叠、字体不一致、低分辨率图片、空白页 |
| **引用完整性** | 未定义引用、未引用标签、缺少 caption、编号间隙 |
| **Caption 审查** | Title/Sentence case 规范执行；移除 AI 味 |
| **实验叙事** | 段落连贯性、消融覆盖度、基线对比检查 |
| **ScholarEval** | 8 维度质量评分（1–10 分），附投稿可读性标签 |
| **NeurIPS 评分** | Quality / Clarity / Significance / Originality 1–6 分 |
| **在线验证** | CrossRef + Semantic Scholar（添加 `--online`）；无需 API 密钥 |
| **去AI化** | 全文降低 AI 写作痕迹 |
| **引用堆叠检测** | 检测引言/相关工作中 3 个及以上连续引用未逐篇讨论的 AI 写作痕迹 |

**审查工作流层级**

| 层级 | 检查内容 |
|---|---|
| L0 | 格式预检（语法、编译错误）|
| L1 | 引用完整性（未定义引用、缺少 caption）|
| L2 | 视觉排版（PDF 渲染分析）|
| L3 | Caption 与实验叙事质量 |
| L4 | 去AI化编辑 |
| L5 | ScholarEval / NeurIPS 评分 |

### industrial-ai-research

聚焦 Industrial AI 领域的结构化文献综合工具。

| 类别 | 功能 |
|---|---|
| **研究领域** | 预测性维护、智能调度、异常检测、智能制造、CPS、机器人 |
| **前置确认** | 综合前先确认报告语言、交付模式、时间窗口和研究侧重点 |
| **检索策略** | 优先近期 arXiv + 顶级 IEEE/自动化 venue（T-ASE、CASE、T-II）|
| **输出格式** | research-brief · literature-map · venue-ranked survey · research-gap memo · survey-draft |
| **综述初稿** | 分类体系大纲 → 逐节证据包 → 逐节写作 → 合并 + 质量门；可选 LaTeX 移交 |
| **报告结构** | 检索范围 → 来源分桶 → 候选论文 → 综合结论 → 下一步建议 |

---

## 快速开始

技能根据自然语言自动触发。在 Claude Code 中描述你的任务即可。

### 编译配置

```
用 xelatex-biber 编译我的论文
compile my paper
```

| 配置 | 步骤 | 适用场景 |
|---|---|---|
| `xelatex` | 仅 XeLaTeX | 中文快速编译 |
| `pdflatex` | 仅 PDFLaTeX | 英文快速编译 |
| `latexmk` | LaTeXmk 自动 | 自动处理依赖 |
| `xelatex-biber` | xelatex → biber → xelatex × 2 | 中文 + Biber（推荐）|
| `xelatex-bibtex` | xelatex → bibtex → xelatex × 2 | 中文 + BibTeX |
| `pdflatex-biber` | pdflatex → biber → pdflatex × 2 | 英文 + Biber |
| `pdflatex-bibtex` | pdflatex → bibtex → pdflatex × 2 | 英文 + BibTeX |

### 去AI化编辑

```
去AI化这段引言
降低这段文字的AI痕迹
deai check my introduction
```

删除空话口号、过度确定表达、机械排比结构。完整保留所有 LaTeX/Typst 语法。

### 语法与风格

```
检查摘要的语法
提升相关工作章节的学术语气
detect Chinglish in Section 2
```

### 逻辑与方法论

```
检查引言的逻辑衔接
分析方法论深度
使用 AXES 模型验证段落结构
```

### 标题优化

```
优化我的论文标题
为这篇论文生成 5 个标题候选方案
```

遵循 IEEE/ACM/Springer/NeurIPS 最佳实践。移除无效词（"Novel"、"A Study of"、"关于……的研究"）。综合评分 0–100。确保关键词出现在前 65 字符（英文）/ 前 20 字（中文）。

### 实验分析

```
帮我分析这些实验数据，写成 IEEE 顶刊标准的段落
生成消融实验分析段落
根据这张表格写 SOTA 对比段落
```

输出：连贯叙事段落（LaTeX/Typst），非 itemize 列表。

### 图表标题优化

```
生成符合顶会规范的图表标题
优化这张图的标题
生成图 3 的双语 caption
```

### 参考文献

```
检查论文的图表引用
查找未定义的标签
验证参考文献
```

### 论文审查

```
帮我全面审查这篇论文
投稿前检查论文质量
审查我的 PDF 排版问题
run paper-audit --online --scholar-eval
```

### 翻译

```
翻译这段文字为英文
中译英这个章节
```

自动识别领域术语（深度学习、时间序列、工业控制）。

---

## 输出协议

所有建议采用注释式 diff 格式，包含必填的严重级别和优先级字段：

```latex
% <模块>（第 <N> 行）[Severity: Critical|Major|Minor] [Priority: P0|P1|P2]: <问题概述>
% 原文：<原始文本>
% 修改后：<建议文本>
% 理由：<简要说明>
% ⚠️ 【待补证】：<需要证据/数据时标记>
```

| 严重级别 | 含义 |
|---|---|
| Critical | 阻断投稿（编译失败、未定义引用、缺少必要章节）|
| Major | 显著影响质量（语法错误、逻辑缺口、格式不合规）|
| Minor | 润色级改进（用词选择、风格一致性）|

---

## 系统要求

### LaTeX 技能（`latex-paper-en`、`latex-thesis-zh`）

- Python 3.10+
- TeX Live 或 MiKTeX（包含 `latexmk`、`chktex`）
- 中文文档：XeLaTeX + CJK 字体（SimSun、SimHei、KaiTi）

### Typst 技能（`typst-paper`）

- Python 3.10+
- Typst CLI（`cargo install typst-cli` 或通过包管理器安装）
- 中文文档：思源宋体 / Noto Serif CJK SC

### 论文审查（`paper-audit`）

- Python 3.10+
- `pdfplumber`（PDF 视觉分析；运行 `uv sync` 或 `pip install pdfplumber`）

---

## 项目结构

```
academic-writing-skills/
├── latex-paper-en/
│   ├── SKILL.md                    # Skill 入口与触发关键词
│   ├── agents/                     # Agent 元数据
│   ├── evals/                      # 评测用例
│   ├── examples/                   # 示例 Prompt
│   ├── references/                 # 风格指南、期刊规则、禁用术语
│   └── scripts/
│       ├── parsers.py              # LatexParser / TypstParser 基类
│       ├── compile.py              # 统一编译器（pdflatex/xelatex/latexmk）
│       ├── check_format.py         # ChkTeX 封装
│       ├── verify_bib.py           # BibTeX 格式校验
│       ├── online_bib_verify.py    # CrossRef / Semantic Scholar 查询
│       ├── check_references.py     # \ref / \label / caption 完整性
│       ├── check_figures.py        # 图片使用分析
│       ├── analyze_grammar.py      # 中式英语、弱动词、主谓一致
│       ├── analyze_sentences.py    # 长难句拆解
│       ├── analyze_logic.py        # AXES 衔接、过渡信号词
│       ├── improve_expression.py   # 学术语气重构
│       ├── optimize_title.py       # 标题生成与评分
│       ├── analyze_experiment.py   # 实验叙事生成
│       ├── deai_check.py           # 单段去AI化
│       ├── deai_batch.py           # 全文批量去AI化
│       ├── translate_academic.py   # 中译英领域感知翻译
│       └── extract_prose.py        # 纯文本提取（跳过数学/环境）
│
├── latex-thesis-zh/
│   ├── SKILL.md
│   ├── agents/ · evals/ · examples/ · references/
│   └── scripts/                    # 与 latex-paper-en 相同，另含：
│       ├── map_structure.py        # 多文件论文结构映射
│       ├── detect_template.py      # 模板自动检测
│       └── check_consistency.py    # 术语与符号一致性
│
├── typst-paper/
│   ├── SKILL.md
│   ├── agents/ · evals/ · examples/
│   ├── references/                 # STYLE_GUIDE.md, TYPST_SYNTAX.md, DEAI_GUIDE.md
│   └── scripts/                    # 同等工具链，适配 Typst 语法
│
├── paper-audit/
│   ├── SKILL.md
│   ├── agents/ · examples/ · templates/
│   ├── references/
│   │   └── SCHOLAR_EVAL_GUIDE.md
│   └── scripts/
│       ├── audit.py                # 主编排器
│       ├── parsers.py              # 共享解析基类
│       ├── pdf_parser.py           # PDF 文本与元数据提取
│       ├── visual_check.py         # PDF 排版渲染分析
│       ├── check_references.py     # 引用完整性
│       ├── detect_language.py      # 语言检测
│       ├── scholar_eval.py         # 8 维度 ScholarEval 评分
│       └── report_generator.py     # 结构化审查报告输出
│
└── industrial-ai-research/
    ├── SKILL.md
    ├── agents/ · examples/
    └── references/                 # 来源策略、venue 优先级列表
```

---

## 失败处理

| 问题 | 解决方案 |
|---|---|
| 缺少 LaTeX 工具 | 安装 TeX Live / MiKTeX；确保 `latexmk` 和 `chktex` 已加入 `PATH` |
| 缺少 Typst CLI | `cargo install typst-cli` 或通过包管理器安装 |
| 编译失败 | 摘要首个错误块并提供相关 `.log` 片段 |
| 缺少脚本 | 确认工作目录指向技能根目录 |
| PDF 分析失败 | 安装 `pdfplumber`（`uv sync --extra dev`）|

---

## 贡献

欢迎提交 Issue 和 Pull Request！请将改动限定在相关技能范围内，并在提交前运行 `just ci`。

## 许可证

仅限学术用途 — 不得用于商业用途。

---

## 文档

完整文档请访问 [docs](https://github.com/bahayonghang/academic-writing-skills/tree/main/docs) 目录。

**本地查看：**

```bash
cd docs
npm install
npm run docs:dev
# 在浏览器中打开 http://localhost:5173
```
