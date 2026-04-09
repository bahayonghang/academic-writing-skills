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
| [`paper-audit`](#paper-audit) | 深度审稿优先的论文审查与投稿门控 | `.tex` `.typ` `.pdf` |
| [`industrial-ai-research`](#industrial-ai-research) | Industrial AI 文献综合与研究缺口分析 | — |

---

## 安装方法

### 方式 1：使用 skills（推荐）

通过 [skills](https://github.com/bahayonghang/skills)（Claude Code 社区技能管理器）安装：

```bash
# 安装单个技能
npx skills add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skills add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add github.com/bahayonghang/academic-writing-skills/typst-paper
npx skills add github.com/bahayonghang/academic-writing-skills/paper-audit
npx skills add github.com/bahayonghang/academic-writing-skills/industrial-ai-research

# 或一次性安装所有技能
npx skills add github.com/bahayonghang/academic-writing-skills
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
| **逻辑** | 段落衔接（AXES 模型）、绪论漏斗链、方法论深度、摘要/结论一致性检查 |
| **文献综述** | 独立的 related work 综合分析与重写蓝图：主题聚合、比较分析、研究空白推导 |
| **标题** | IEEE/ACM/Springer 最佳实践生成；移除无效词；综合评分 0–100 |
| **图表标题** | Title/Sentence case 规范、无 AI 味的图表标题 |
| **伪代码** | 面向 `algorithm2e`、`algorithmicx`、`algpseudocodex` 的 IEEE-safe 审查；检查浮动体、caption/label/引用顺序、长注释和行号建议 |
| **实验分析** | 含 SOTA 对比、消融分析、discussion 分层与结论完整性的连贯叙事段落 |
| **去AI化** | 人性化 AI 写作，完整保留所有 LaTeX 语法，并标出低信息密度空话 |
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
| **逻辑** | 段落衔接（AXES 模型）、绪论漏斗链、章节主线、跨章节逻辑链 |
| **文献综述** | 面向学位论文的文献综述诊断与重写蓝图：拒绝作者年份流水账，强化比较分析与空白推导 |
| **标题** | 符合 GB/T 7713.1-2006 规范；中英文双语候选方案 |
| **图表标题** | 顶会标准双语 Caption（中文 + 英文）|
| **实验分析** | 含基线对比、消融覆盖、discussion 分层与结论完整性的核心期刊叙事段落 |
| **去AI化** | 降低 AI 写作痕迹，完整保留所有 LaTeX 命令，并标出低信息密度套话 |
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
| **逻辑** | AXES 段落衔接、绪论漏斗链、摘要/结论一致性、跨章节逻辑链 |
| **文献综述** | 在保留 `@cite` anchors 与 Typst labels 的前提下，检查 related work 的综合性与研究空白链条 |
| **标题** | 双语（中英文）标题生成与优化 |
| **图表标题** | 遵循 IEEE/ACM 标准的双语 Caption |
| **伪代码** | 面向 `algorithmic`、`algorithm-figure`、`lovelace` 的 IEEE-like 审查，检查 wrapper、caption、style hook 和注释长度 |
| **实验分析** | 面向期刊/会议的连贯叙事段落，并检查 discussion 分层 |
| **去AI化** | 中英文 Typst 去 AI 化；保留 `@cite`、`<label>`、`$...$` |
| **反引用堆叠** | 每句最多 2 个并列引用；检测引言/相关工作中的堆叠式引用 |
| **期刊模板** | IEEE、ACM、Springer、NeurIPS 模板指引 |
| **引用** | 未定义 `@ref`、未引用标签；支持在线验证 |

### paper-audit

以深度审稿为核心的多格式论文审查工具，包含结构化问题清单、修订路线图与投稿门控。

| 类别 | 功能 |
|---|---|
| **输入** | `.tex`、`.typ`、`.pdf` 文件 |
| **模式** | `quick-audit`（快速筛查）· `deep-review`（审稿人风格深审）· `gate`（投稿门控）· `re-audit`（修订回归）|
| **深审产物** | `final_issues.json`、`overall_assessment.txt`、`review_report.md`、`peer_review_report.md`、`revision_roadmap.md` |
| **引用完整性** | 未定义引用、未引用标签、缺少 caption、编号间隙 |
| **Caption 审查** | Title/Sentence case 规范执行；移除 AI 味 |
| **伪代码审查** | IEEE gate 检查浮动算法环境、caption/label/引用顺序，并把行号与长注释归为建议项而非硬阻塞 |
| **实验叙事** | 段落连贯性、基线对比、discussion 深度/分层、结论完整性检查 |
| **深审产物** | `final_issues.json`、`overall_assessment.txt`、`review_report.md`、`revision_roadmap.md` |
| **ScholarEval** | 8 维度质量评分（1–10 分），附投稿可读性标签 |
| **NeurIPS 评分** | Quality / Clarity / Significance / Originality 1–6 分 |
| **在线验证** | CrossRef + Semantic Scholar（添加 `--online`）；无需 API 密钥 |
| **去AI化** | 全文降低 AI 写作痕迹 |
| **引用堆叠检测** | 检测引言/相关工作中 3 个及以上连续引用未逐篇讨论的 AI 写作痕迹 |
| **审查范围说明** | Phase 0 负责脚本化审查；`deep-review` 进一步加入 claim-evidence、符号/数值一致性、评估公平性、自我标准一致性、先验工作定位等 reviewer lanes |
| **文献边界** | `--focus literature` 负责判断 research gap 是否真实、文献定位是否公平，不负责代写综述正文；需要改写时请转交对应写作类 skill |

**审查工作流层级**

| 层级 | 检查内容 |
|---|---|
| L0 | `quick-audit` / `gate` 脚本审查 |
| L1 | deep-review workspace 预处理（sections、summary、claim map）|
| L2 | section review lanes |
| L3 | cross-cutting review lanes |
| L4 | 问题合并与 quote 校验 |
| L5 | 最终报告、路线图与可选评分摘要 |

**快速使用**

| 模式 | 适用时机 | 主产物 |
|---|---|---|
| `quick-audit` | 想快速看投稿风险 | 脚本化报告 + checklist + score summary |
| `deep-review` | 想模拟审稿人深审 | 结构化问题清单 + 修订路线图 + 可选 `peer_review_report.md` |
| `gate` | 只关心 blocker | PASS/FAIL + 阻塞项 |
| `re-audit` | 想验证修订效果 | 问题状态对比 |

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
uv run python academic-writing-skills/paper-audit/scripts/render_deep_review_report.py review_results/paper-slug --style peer-review
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md
```

兼容别名：

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

文档：

- [概览](docs/zh/skills/paper-audit/index.md)
- [工作流](docs/zh/skills/paper-audit/resources/WORKFLOW.md)
- [输出产物](docs/zh/skills/paper-audit/resources/OUTPUTS.md)

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
| **综合规则** | 综述写作必须保留冲突证据，按照“共识 → 分歧 → 局限 → 空白”组织，禁止把相互矛盾的研究强行写成统一结论 |

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

### 伪代码与算法块

```
检查这个 IEEE 伪代码是否还在用 algorithm2e 浮动体
审查这个 algorithm-figure 的 caption 和行号
把这段伪代码改成 IEEE-safe 的写法，但不要伪造 Algorithm 1 规则
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
│       ├── check_pseudocode.py     # IEEE-aware 伪代码检查
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
│       └── check_pseudocode.py     # IEEE-like Typst 伪代码检查
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
│       ├── check_pseudocode.py     # 通过 sibling route 调用的 IEEE 伪代码检查
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
