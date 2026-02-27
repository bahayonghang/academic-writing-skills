# claude-scientific-writer vs academic-writing-skills 对比分析报告

> 分析日期：2026-02-27
> 分析对象：[claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) v2.12.0 (以下简称 **CSW**) 与本仓库 academic-writing-skills (以下简称 **AWS**)

---

## 一、项目定位对比

| 维度 | CSW | AWS |
|------|-----|-----|
| **核心定位** | 端到端论文 **生成** 平台 | 已有论文的 **质量改进与审查** 工具集 |
| **目标用户** | 需要从零开始撰写论文的研究者 | 已有草稿、需要润色/审查/编译的研究者 |
| **交互模式** | 自主驱动：给定主题 → 自动研究 → 自动撰写 → 交付 PDF | 模块驱动：用户指定任务 → 按模块执行分析/修改 |
| **外部依赖** | 重度依赖：Perplexity API、Parallel Web Systems API、OpenRouter (Nano Banana Pro / Gemini 3 Pro / FLUX.2 Pro) | 零外部 API 依赖，仅需 Python + LaTeX/Typst 本地工具链 |
| **发布形态** | PyPI 包 + Claude Code 插件 (marketplace) | Claude Code Skill 集合 |
| **许可证** | MIT | — |

**关键洞察**：两者的核心能力是 **互补** 而非竞争关系。CSW 擅长「从 0 到 1」的论文生成；AWS 擅长「从 1 到 N」的质量提升。

---

## 二、功能矩阵对比

### 2.1 写作流程覆盖

| 阶段 | CSW | AWS | 差距分析 |
|------|:---:|:---:|----------|
| 文献检索 | ✅ Perplexity + Parallel Web | ❌ | AWS 无文献检索能力 |
| 大纲规划 | ✅ 两阶段法 (骨架→填充) | ❌ | AWS 不参与结构设计 |
| 初稿撰写 | ✅ 按节研究→撰写 | ❌ | AWS 定位为改进工具，不生成初稿 |
| 编译构建 | ✅ pdflatex + bibtex + latexmk | ✅ 10 种编译配方，自动检测编译器 | AWS 更强：支持 XeLaTeX/LuaLaTeX/中文检测 |
| 格式检查 | ✅ PDF 转图审查 (PyMuPDF) | ✅ chktex + 规则引擎 | 互补：CSW 审视觉；AWS 审语法规则 |
| 语法检查 | ❌ 无专用模块 | ✅ 规则式语法分析器 | AWS 独有 |
| 长句分析 | ❌ | ✅ 可配置阈值，自动建议拆分 | AWS 独有 |
| 学术表达提升 | ❌ | ✅ 弱动词替换 + 冗余短语清理 | AWS 独有 |
| 逻辑分析 | ❌ | ✅ 方法论论证 + 逻辑跳跃检测 | AWS 独有 |
| 去 AI 化 | ❌ | ✅ 4 类 AI 痕迹检测 + 密度评分 | AWS 独有且成熟 |
| 翻译辅助 | ❌ | ✅ 中译英 + 领域术语表 | AWS 独有 |
| 标题优化 | ❌ | ✅ 5 维度评分 (满分 100) | AWS 独有 |
| 参考文献验证 | ✅ BibTeX 完整性强制 | ✅ 交叉引用 + GB/T 7714 合规 | AWS 更深入，支持国标 |
| 同行评审模拟 | ✅ 自动生成 PEER_REVIEW.md | ✅ paper-audit review 模式 | 功能相似，AWS 有量化评分 |
| 质量门禁 | ❌ | ✅ paper-audit gate 模式 (PASS/FAIL) | AWS 独有 |
| 深度润色 | ❌ | ✅ paper-audit polish 模式 (对抗式双 Agent) | AWS 独有且创新 |

### 2.2 格式与语言支持

| 维度 | CSW | AWS |
|------|:---:|:---:|
| LaTeX 英文论文 | ✅ | ✅ |
| LaTeX 中文学位论文 | ❌ | ✅ (5 所高校模板) |
| Typst 论文 | ❌ | ✅ (中英双语) |
| PDF 直接审查 | ✅ (转图片) | ✅ (转 Markdown，结构化) |
| 会议模板 | ✅ (Nature/Science/IEEE/ACM/NeurIPS/ICML/CVPR) | ✅ (IEEE/ACM/Springer/NeurIPS/ICML/CVPR/ICLR/AAAI/COLM) |
| 中文国标支持 | ❌ | ✅ GB/T 7714-2015 |
| 术语一致性检查 | ❌ | ✅ (中英双语术语组) |

### 2.3 CSW 独有的扩展功能

| 功能 | 说明 | AWS 是否适合引入 |
|------|------|:---:|
| 科学图表生成 | Nano Banana Pro + Gemini 质量循环 | ⚠️ 需外部 API，与 AWS 零依赖原则冲突 |
| 研究海报 (LaTeX) | beamerposter/tikzposter/baposter | ✅ 高价值，可本地实现 |
| 研究幻灯片 | AI 生成 PDF 演示文稿 | ⚠️ 需外部 API |
| 基金申请书 | NSF/NIH/DOE/DARPA 模板 | ⚠️ 与学术论文定位偏差较大 |
| 临床文档 | CARE/ICH-E3/SOAP 等 | ❌ 领域过于专业 |
| 市场研究报告 | Porter's Five Forces 等 | ❌ 非学术论文范畴 |
| 文学综述 | PRISMA + 多数据库检索 | ⚠️ 需外部 API |
| 假设生成 | 可测试假设制定 | ⚠️ 高度依赖 LLM，无独立脚本价值 |
| 信息图表 | 10 种类型 × 8 种风格 | ❌ 需外部 API |
| MarkItDown 转换 | 15+ 格式转 Markdown | ✅ 可增强 PDF 解析能力 |
| 版本管理 | 草稿自动递增 (v1→v2→v3) | ✅ 简单有效，值得借鉴 |
| ScholarEval 评估 | 8 维度量化评分 | ✅ 可与 paper-audit 评分系统整合 |
| 图形摘要生成 | 每篇论文强制生成 Figure 1 | ⚠️ 需外部 API |
| Paper2Web | 论文转交互式网页 | ⚠️ 与当前定位偏差 |

---

## 三、架构设计对比

### 3.1 技术架构

```
CSW 架构：
┌─────────────────────────────────────────────┐
│  Claude Code Plugin / CLI / Python API      │  ← 三种入口
├─────────────────────────────────────────────┤
│  claude-agent-sdk (Opus 4.6, 500 turns)     │  ← 自主 Agent 循环
│  + Stop Hook (强制完成)                      │
├─────────────────────────────────────────────┤
│  20 Skills (各自独立)                        │  ← 扁平技能集
├─────────────────────────────────────────────┤
│  External APIs                               │  ← 重外部依赖
│  (Perplexity / Parallel Web / OpenRouter)   │
└─────────────────────────────────────────────┘

AWS 架构：
┌─────────────────────────────────────────────┐
│  Claude Code Skill 触发 ($ARGUMENTS)         │  ← 单一入口
├─────────────────────────────────────────────┤
│  SKILL.md (模块路由 + 执行护栏)              │  ← 声明式模块定义
├─────────────────────────────────────────────┤
│  Python Scripts (分析引擎)                    │  ← 规则式+启发式
│  parsers.py → 各 check/analyze 脚本         │
├─────────────────────────────────────────────┤
│  references/ + modules/                      │  ← 知识库
│  (风格指南 / 会议规则 / 术语表)              │
└─────────────────────────────────────────────┘
```

### 3.2 设计哲学差异

| 维度 | CSW | AWS |
|------|-----|-----|
| **自主性** | 高：Agent 自动研究、撰写、编译、审查 | 低：用户指挥，工具执行 |
| **可控性** | 低：500 turn 自动循环，难以中途干预 | 高：每个模块独立触发，可精确控制 |
| **可复现性** | 低：依赖外部 API 实时结果 | 高：规则引擎输出确定性结果 |
| **离线能力** | 无 (核心功能依赖网络) | 完全离线可用 |
| **扩展方式** | 新增 Skill 目录 | 新增模块 (脚本 + 参考文档 + SKILL.md 注册) |

---

## 四、AWS 的核心优势

1. **零外部依赖**：完全本地化运行，无需 API Key，无网络要求，无成本
2. **Typst 支持**：市面上极少有工具支持 Typst 学术写作辅助
3. **中文学位论文深度支持**：5 所高校模板检测 + GB/T 7714 + 术语一致性
4. **去 AI 化检测**：4 类模式 + 密度评分，在 AI 写作普及的背景下极具价值
5. **统一输出协议**：所有模块 `[Severity] [Priority]` 格式，可被 paper-audit 自动解析
6. **对抗式润色 (Polish)**：Critic + Mentor 双 Agent 架构是创新设计
7. **量化评分体系**：NeurIPS 6 分制 + 4 维度加权，具备门禁判断能力
8. **模块正交性**：12 个模块独立触发，可组合使用，符合 UNIX 哲学

---

## 五、优化建议

### 5.1 高优先级 — 低成本高收益

#### P0-1: 引入版本管理机制

**借鉴 CSW**：草稿自动递增版本号 (`v1_draft.tex` → `v2_draft.tex`)。

**实现方案**：在 `compile.py` 中添加 `--versioned` 标志：
- 编译前自动备份当前版本到 `drafts/` 目录
- 文件名格式：`{stem}_v{N}_{timestamp}.{ext}`
- 维护 `drafts/CHANGELOG.md` 记录每次编译的变更摘要

**预计工作量**：0.5 天

---

#### P0-2: 强化 PDF 审查能力

**借鉴 CSW**：PDF → 图片 → 视觉审查循环。

**实现方案**：
- 在 `paper-audit` 中新增 `visual-check` 检查项
- 使用 PyMuPDF 将 PDF 转为图片 (已有依赖)
- 检查项：页边距溢出、图表重叠、字体一致性、分页断裂
- 输出格式与现有 `[Severity] [Priority]` 统一

**预计工作量**：1-2 天

---

#### P0-3: 增加 Figure/Table 引用完整性检查

**当前状态**：`check_figures.py` 已存在但仅检查文件存在和 DPI。

**优化方案**：
- 检查所有 `\ref{fig:*}` / `\ref{tab:*}` 是否有对应 `\label{}`
- 检查所有 `\label{fig:*}` 是否被至少引用一次
- 检查图表编号连续性
- 检查图表是否出现在首次引用之后的合理位置

**预计工作量**：1 天

---

### 5.2 中优先级 — 能力扩展

#### P1-1: 引入 ScholarEval 评估框架

**借鉴 CSW**：8 维度量化评分 (基于 arXiv:2510.16234)。

**实现方案**：
- 在 `paper-audit` 中新增 `scholar-eval` 模式或作为 `review` 模式的扩展
- 8 维度：Novelty、Soundness、Significance、Clarity、Reproducibility、Ethics、Presentation、Overall
- 与现有 4 维度评分 (Quality/Clarity/Significance/Originality) 形成互补
- 提供更细粒度的改进建议

**预计工作量**：2-3 天

---

#### P1-2: 新增引文元数据在线验证

**借鉴 CSW**：`citation-management` Skill 中的 DOI 验证、PubMed/Google Scholar 检索。

**实现方案**（保持可选依赖）：
- 在 `verify_bib.py` 中新增 `--online` 标志
- 通过 CrossRef API (免费，无需 Key) 验证 DOI 有效性
- 通过 Semantic Scholar API (免费) 验证论文元数据
- 离线模式下跳过，保持零依赖的默认行为

**预计工作量**：2 天

---

#### P1-3: 消除 parsers.py 的代码重复

**当前问题**：`parsers.py` 在 4 个 Skill 目录中各有一份拷贝，违反 DRY 原则。

**实现方案**：
- 将 `parsers.py` 提取为共享库 `academic-writing-skills/shared/parsers.py`
- 各 Skill 脚本通过相对导入或 `sys.path` 引用共享版本
- `paper-audit` 的扩展版 (含 `PdfParser`) 继承共享基类

```
academic-writing-skills/
├── shared/
│   ├── __init__.py
│   ├── parsers.py          # LatexParser, TypstParser, DocumentParser ABC
│   └── pdf_parser.py       # PdfParser (optional dependency: pymupdf)
├── latex-paper-en/scripts/  # import from shared
├── latex-thesis-zh/scripts/ # import from shared
├── typst-paper/scripts/     # import from shared
└── paper-audit/scripts/     # import from shared + pdf_parser
```

**预计工作量**：1 天

---

#### P1-4: 统一脚本之间的重复代码

**当前问题**：`latex-paper-en` 和 `latex-thesis-zh` 中有 8 个几乎相同的脚本 (`compile.py`, `check_format.py`, `verify_bib.py`, `analyze_grammar.py`, `analyze_sentences.py`, `analyze_logic.py`, `deai_check.py`, `optimize_title.py`)。

**实现方案**：
- 将公共逻辑提取到 `shared/` 目录
- 各 Skill 保留 thin wrapper 脚本，仅传入语言/格式相关配置
- 例如 `latex-thesis-zh/scripts/verify_bib.py` 仅添加 GB/T 7714 规则后调用共享引擎

**预计工作量**：2-3 天

---

### 5.3 长期愿景 — 战略性增强

#### P2-1: 引入文献检索能力 (可选模块)

**分析**：这是 AWS 与 CSW 最大的功能差距。但核心挑战在于需要外部 API。

**建议方案**（分层设计）：
- **Layer 0 (零依赖)**：解析现有 `.bib` 文件，生成引文图谱、共引分析
- **Layer 1 (免费 API)**：Semantic Scholar API + CrossRef API (均免费)
- **Layer 2 (付费 API)**：可选集成 Perplexity / Parallel Web Systems

作为新 Skill `literature-assist`，而非修改现有 Skill。

---

#### P2-2: 研究海报 Skill

**借鉴 CSW**：LaTeX beamerposter/tikzposter 模板。

**实现方案**：
- 新 Skill `latex-poster`
- 提供 3 种海报引擎模板 (与 CSW 一致)
- 复用现有 `compile.py` 编译能力
- 添加海报专用格式检查 (字体大小、可读距离、信息密度)

---

#### P2-3: 多文件项目工作流

**借鉴 CSW**：`writing_outputs/` 结构化输出 + `progress.md` 实时日志。

**实现方案**：
- 在 `paper-audit` 中新增 `--project` 模式，扫描整个项目目录
- 生成结构化审查报告到 `audit_reports/` 目录
- 支持增量审查 (仅检查自上次审查后变更的文件)
- 报告包含文件级和项目级汇总

---

## 六、不建议引入的 CSW 功能

| CSW 功能 | 不引入原因 |
|----------|-----------|
| 临床文档 (CARE/ICH-E3/SOAP) | 医疗领域过于专业，偏离学术论文核心定位 |
| 市场研究报告 | 非学术范畴 |
| AI 图片/图表生成 | 需付费外部 API，破坏零依赖原则 |
| 幻灯片生成 | 需外部 API (Nano Banana Pro) |
| 假设生成 | 高度依赖 LLM，无独立脚本/规则价值 |
| Paper2Web/Paper2Video | 偏离论文写作核心工具链定位 |
| Stop Hook 自主循环 | AWS 设计哲学强调用户可控性 |
| Parallel Web Systems 集成 | 付费 API，与零依赖原则冲突 |

---

## 七、总结

### AWS 核心竞争力

```
┌────────────────────────────────────────────────┐
│                AWS 护城河                       │
├────────────────────────────────────────────────┤
│  ✅ 零依赖 · 离线优先 · 完全可控               │
│  ✅ 中英双语 · Typst 先行者 · 国标合规         │
│  ✅ 去 AI 化检测 (市场刚需)                     │
│  ✅ 对抗式润色 (Critic + Mentor 创新架构)       │
│  ✅ 统一输出协议 → 可组合 · 可聚合 · 可门禁     │
└────────────────────────────────────────────────┘
```

### 演进路径建议

```
Phase 1 (1 周)                Phase 2 (2-3 周)            Phase 3 (1-2 月)
─────────────                 ──────────────              ──────────────
P0-1 版本管理                  P1-1 ScholarEval           P2-1 文献检索
P0-2 视觉审查                  P1-2 在线引文验证           P2-2 海报 Skill
P0-3 引用完整性                P1-3 消除代码重复           P2-3 项目工作流
                              P1-4 统一脚本代码
```

**核心原则**：保持 AWS 的「零依赖 + 用户可控 + 模块正交」DNA，选择性吸收 CSW 中与此 DNA 兼容的优秀设计。
