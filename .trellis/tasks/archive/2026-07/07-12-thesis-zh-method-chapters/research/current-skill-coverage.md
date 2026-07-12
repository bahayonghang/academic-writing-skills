# 现状盘点：latex-thesis-zh 对正文方法章+实验（第3~6章）的能力覆盖

- **任务**：盘点 `academic-writing-skills/latex-thesis-zh`（v5.3.0）当前对正文方法章与实验部分的写作指导与自动诊断能力，找空白
- **范围**：internal（源码 + references + evals 全量核实）
- **日期**：2026-07-12
- **一句话结论**：**第2章（过程分析章）已由 07-11 任务系统化覆盖，绪论也有专章；但第3~6章正文方法章几乎是"指导薄、脚本无"的空白区**——方法章骨架/形式化/方法设计只有 `thesis-writing-guide.md` 的"方法章三问"一句话，实验自动检查因依赖全局 `discussion`/`related` 节而对工业过程论文大面积失效。

---

## 一、能力清单逐项裁定（12 项）

| # | 能力 | 裁定 | 主要证据 |
|---|------|------|----------|
| 1 | 方法章章内骨架指导（节序列） | **部分覆盖（薄）** | `thesis-writing-guide.md:119-137` 方法章三问；`structure-guide.md:122` 推荐结构；无专章骨架指南 |
| 2 | 章引言承上启下检查（第3章及以后） | **已覆盖（最强项）** | `analyze_logic.py:510` `_check_chapter_intro` + `:442` `_check_chapter_mainline` |
| 3 | 问题形式化/数学描述写作指导 | **部分覆盖（仅第2章）** | `process-chapter-guide-zh.md:115-127` §5 仅面向第2章；方法章无 |
| 4 | 方法设计写作指导（公式/伪代码/结构图） | **空白** | 仅 `thesis-writing-guide.md:127` 一句"设计：输入/流程/结构/输出" |
| 5 | 实验部分写作指导（含工业验证） | **部分覆盖** | `thesis-writing-guide.md:139-151` 六层；`experiment.md`；工业验证章仅一处带过 |
| 6 | 实验相关自动检查 | **部分覆盖（对本类论文大面积失效）** | `analyze_experiment.py:111/142/190/218` 四项启发式依赖全局节 |
| 7 | 结果表格/图规范检查 | **部分覆盖** | `check_tables.py`、`check_references.py`；加粗最优值无检查 |
| 8 | 章小结写作指导与检查 | **指导已覆盖 / 脚本弱** | `thesis-writing-guide.md:72-101` 详；脚本仅 S1 查"有无导语" |
| 9 | 章间递进/与第二章框架呼应 | **部分覆盖** | `_check_chapter_mainline` 查桥接；框架呼应闭合无检查 |
| 10 | 小论文拼接感（正文章节） | **部分覆盖（P-PAPER 仅第2章）** | `analyze_logic.py:1609` P-PAPER 只扫第2章；F-MD/F-NOTE 全局 |
| 11 | over-claim/去AI（正文章节） | **已覆盖（通用）** | `deai_check.py --analyze` 覆盖全章；`over-claim-guard.md` |
| 12 | evals 正文章节路由 | **部分覆盖** | 有 experiment/方法章/章节主线用例；无 `--process-chapter` 路由用例 |

---

## 二、脚本 vs 纯 LLM 指导（关键区分）

### 已有脚本自动检查（`[Script]` 启发式）

| 脚本 | 检查项 | 触发条件 / 局限 |
|------|--------|----------------|
| `analyze_logic.py:510` `_check_chapter_intro` | 章引言承上启下、相对指代、篇幅 | 全部正文章（绪论/结论除外），第2章特判跳过"承上"，**第3章起完整适用** |
| `analyze_logic.py:442` `_check_chapter_mainline` | 多章缺前章桥接→整体主线偏罗列 | ≥2 章"本章/本文"开头且无桥接词才报 |
| `analyze_logic.py:1623` `_check_process_chapter`（`--process-chapter`） | P-FLOW/P-DERIVE/P-FRAME/P-ORDER/P-PAPER | **默认只定位第2章**，`--section` 可覆盖；章式预判非过程章只出 Info |
| `analyze_experiment.py:111` `_check_discussion_depth`（B3） | 归因语言占比 <15% → Major | **需 `discussion` 节存在** |
| `analyze_experiment.py:142` `_check_discussion_structure` | 论辩维度覆盖 <2 → Major | **需 `discussion` 节 ≥6 可见行** |
| `analyze_experiment.py:190` `_check_results_literature_echo`（B4） | related 引用键未在 discussion 复现 → Major | **需同时存在 `related` 与 `discussion` 节** |
| `analyze_experiment.py:218` `_check_conclusion_completeness`（B5） | 结论缺局限/启示/发现 | 需 `conclusion` 节；工作正常 |
| `check_format.py:60` F-MD / F-NOTE | Markdown 加粗残留 / 草稿备注 | **全局扫全部章**（07-11 已加，覆盖第3~6章源码卫生） |
| `check_tables.py` | 三线表/表题位置/精度一致 | 全局 |
| `check_references.py` | 未定义 `\ref`/未引用 label/缺图表题 | 全局 |

### 纯 LLM 指导（无脚本落地）

- 方法章三问（动机/设计/优势）：`thesis-writing-guide.md:119-137` —— 仅文档
- 实验六层叙事（设置→有效性→消融→机理→文献回溯→局限）：`thesis-writing-guide.md:139-151` + `experiment.md` prompt —— 改写靠 LLM
- 问题数学形式化：`process-chapter-guide-zh.md:115` §5 —— 仅第2章文档，无脚本
- 方法/框架图、伪代码、公式推导呈现规范：**无**

---

## 三、最大的三个空白（后续优化重点）

### 空白 A：实验自动检查对工业过程论文大面积失效（capability 6，最严重）

`analyze_experiment.py` 的四项脚本检查全部依赖 `parsers.split_sections` 返回**独立的全局** `discussion`/`related`/`conclusion` 节（键定义见 `parsers.py:96-121`）。但工业/过程背景中文博士论文的典型结构（07-11 已确立的过程分析章式）是：

- 综述写在**绪论**里，**无独立"相关工作/文献综述"章** → `related` 键缺失 → **B4 结果-文献回溯永不触发**（死检查）；
- **无独立"讨论"章**，讨论分散嵌在第3~6章各自的"实验分析"节内 → `discussion` 键通常缺失 → **B3 讨论深度 / 讨论结构极少触发**；
- 第3~6章**各有独立实验节**，但 `split_sections` 每个键只返回**一个**范围，脚本**只分析一个全局节**，无法逐方法章检查有效性/消融/机理分层。

后果：一篇标准工业过程博士论文跑 `analyze_experiment.py`，四项检查里三项静默失效，用户拿到"No issues detected"的假绿。**需要按"每个方法章内的实验节"逐章分析，而非依赖全局单节。**

### 空白 B：第3~6章方法章缺专章骨架 + 形式化/方法设计写作规范（capability 1/3/4）

绪论有 `introduction-guide-zh.md`，第2章有 `process-chapter-guide-zh.md`（07-11 新建，15.7K，含判别表/骨架/难点链/框架图规范），但**第3~6章核心方法章只有 `thesis-writing-guide.md` 的"方法章三问"一句话**（动机/设计/优势）。缺：

- 方法章推荐骨架（章引言→问题形式化→方法设计→实验验证→本章小结）的专章指南；
- 问题数学形式化规范面向方法章的版本（§5 只写第2章"为后续各章建统一符号"，方法章如何**沿用/扩展**符号无指导）；
- 方法设计呈现规范：**伪代码/algorithm 环境**、方法结构图、公式推导链的写作约定——`structure-guide.md:145` 只禁"标题后直接进算法环境"，无正面写作规范。

### 空白 C：小论文拼接感/框架呼应在第3章起无诊断（capability 9/10）

工业博士大论文常由已发表英文小论文拼接（paper-to-chapter 场景），拼接痕迹风险贯穿第3~6章，但：

- **P-PAPER（`analyze_logic.py:1609`）只在 `--process-chapter` 下扫第2章**，第3~6章的"源论文/小论文/N篇论文"表述无检查；
- 各方法章应"根据第2章框架"反向承接闭合（`process-chapter-guide-zh.md:145` 承认这是 3/5 范文的合规写法），但**无任何脚本验证第3~6章是否真的回指第2章框架/难点**；
- 跨章符号/术语漂移（`check_consistency.py` 查术语，但拼接产生的**英文残留、`we→本文`遗漏、记号不统一**）无专项检查。

F-MD/F-NOTE 已全局覆盖 Markdown 残留与草稿备注（07-11 成果），是拼接检查目前**唯一**覆盖到第3~6章的部分。

---

## 四、与进行中任务 07-11 的边界（避免重复规划）

07-11（第二章过程分析章优化，PRD 见 `.trellis/tasks/07-11-thesis-zh-process-chapter/prd.md`）**已规划/已实现**的能力，07-12 不应重复：

| 07-11 已覆盖 | 落点 | 对第3~6章是否外溢 |
|---|---|---|
| R1 第二章专章指南 | `process-chapter-guide-zh.md` | 否（仅第2章） |
| R2 章引言形态适配（编号2.1引言 vs 章后导语） | `_check_chapter_intro` | **是**——第3章起的"编号引言节"形态适配同样受益 |
| R3 `--process-chapter` 主线检查（P-FLOW/DERIVE/FRAME/ORDER/PAPER） | `analyze_logic.py` | 否（默认第2章；P-PAPER 只第2章） |
| R4 structure-guide 双轨定位 | `structure-guide.md` | 否 |
| R5 F-MD/F-NOTE 源码卫生 | `check_format.py` | **是**——全局扫描，第3~6章已受益 |
| R6 路由+evals（第二章诊断用例） | SKILL/logic.md/routing-rules/evals | 否（evals 目前**无** `--process-chapter` 路由用例，待 07-11 补） |

**明确留给 07-12 的地盘**：第3~6章核心方法章的骨架指南、形式化/方法设计规范（空白B）、逐方法章实验检查（空白A）、方法章间拼接感/框架呼应诊断（空白C）。07-11 的 P-PAPER 与 process-chapter-guide 是"第2章专用"，07-12 需考虑是否将 P-PAPER 泛化到正文全章、是否新建 method-chapter-guide-zh.md 与绪论/第2章指南对齐三件套。

---

## 五、evals 现状（capability 12）

`evals/evals.json`（22.8K）正文相关用例：

- experiment 模块：L108、L230、L318、L410（实验像项目汇报/讨论分层/机理+消融+文献回溯）——覆盖尚可
- 方法章 logic：L295（方法章动机/设计/技术优势→logic）
- 章节主线：L217（章节主线|桥接|承上）
- **缺口**：无 `--process-chapter`/框架图/工艺流程 路由用例（07-11 R6 待补）；无"本章小结写法"、无"方法章形式化/伪代码"路由用例

---

## 六、未决/需 LLM 判断项（脚本不硬检）

- 方法章三问的"设计/优势"充分性（LLM）
- 实验机理解释是否归因（B3 只查归因词占比，深度靠 LLM）
- 框架呼应是否真实闭合（内容级，非词面）
- 跨章符号一致性中"记号漂移"的语义判断
