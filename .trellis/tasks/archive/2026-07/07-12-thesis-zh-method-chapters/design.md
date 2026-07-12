# Design：latex-thesis-zh 正文方法+实验章优化

对应 prd.md R1~R6。改动面：`analyze_logic.py`、`check_format.py`、`analyze_experiment.py`、references 四份文档 + 一份新指南、SKILL.md、evals.json、tests/。**不动 parsers.py**（ALIGNMENTS 锁）。

## 1. 脚本改动落点总表

| Req | 文件 | 函数/常量 | 变化类型 | 默认行为 |
|-----|------|----------|---------|---------|
| R2a | analyze_logic.py | `_check_heading_leads`（L768） | 修误报 | 变化（误报消除） |
| R2b | check_format.py | `mixed_punctuation` 规则（L34） | 修误报 | 变化 |
| R2c | check_format.py | `oral_vague` 词表（L54） | 修误报 | 变化 |
| R2d | analyze_logic.py | `_needs_method_justification_zh`（L55） | 修误报 | 变化 |
| R2e | analyze_logic.py | `_check_process_chapter` 章式预判（L1415+） | 修误报 | 仅 `--process-chapter` 下 |
| R3a | analyze_logic.py | P-PAPER（L1610）迁出 process-chapter 门 | 泛化+全量报告 | 变化（新增默认输出） |
| R3b | check_format.py | `F-NOTE` 词表（L72） | 扩表 | 变化（新增命中） |
| R3c | check_format.py | 新 `F-PLACEHOLDER` 规则 | 新增 | 变化（新增命中） |
| R3d | analyze_logic.py | 新 `_check_thesis_vs_chapter`（暂定） | 新增 Info | 变化（Info 级） |
| R4a | analyze_experiment.py | main 流程结构提示 | 新增 Info | 变化（假绿→提示） |
| R4b | analyze_experiment.py | 新 `--per-chapter` + E-* 检查族 | 新增 | 零变化（flag 后） |
| R4c | analyze_logic.py | 新 `--first-chapter N` 参数 | 新增 | 零变化（参数缺省不变） |
| R5 | analyze_logic.py | `_check_chapter_intro` 缺承上文案/severity | 口径调整 | 变化（降级路径） |

## 2. 关键设计决策

### D1：P-PAPER 泛化方式（R3a）

把 `PAPER_STITCH_RE`（L1433 附近词表）从 `_check_process_chapter` 中抽出为独立函数 `_check_paper_stitching(lines, parser) -> list[str]`，在默认检查管线（L1742 附近 `out.extend(...)` 序列）中调用：

- 扫描**全部可见正文行**（不再限定单章范围），**每处命中单独一条输出**（放弃"首匹配即 return"）。
- 输出前缀沿用 `P-PAPER`（保持 07-11 文档连续性），模块归 `logic`。
- `--process-chapter` 下不重复输出（从 `_check_process_chapter` 中移除该项，避免双报）。
- 词表维持保守：`源论文|小论文|[一二三N1-9]\s*篇(源)?论文`；注释行天然被 visible 过滤跳过（现行为，保留）。
- **存量单测迁移**：07-11 的 P-PAPER 用例从"--process-chapter 下第2章"改为"默认全章"，断言从"报首处"改为"报全部"。

### D2：F-NOTE 扩表与 F-PLACEHOLDER（R3b/R3c）

`check_format.py` 中 F-NOTE 的 `patterns` 扩为两组常量（模块级，便于配置）：

```python
DRAFT_NOTE_CORE = [...]   # 现有：后续可根据…替换｜此处占位｜待补充｜待确认｜TODO｜FIXME
DRAFT_NOTE_HEDGE = [      # 新增"草稿态对冲"组（fixture P2 驱动，保守词表）
    r"待验证(设计|表述)?", r"暂以占位", r"仍在进行", r"重跑(验证|后补齐)?",
    r"待.{0,6}补齐", r"复算", r"不代表.{0,8}性能",
]
```

严重度：HEDGE 组与 CORE 组同为现 F-NOTE 级别（Info），但输出文案区分"草稿备注"与"未定稿对冲表述"。误报护栏：词表仅在**可见正文**匹配；"复算"单词有正常学术用法（如"复算结果一致"），加负向断言 `复算(?!结果|表明|验证了)` 或要求同句含"后续/将/需"任一先行词——实现时以 fixture ch5 L512（"按第 2 章口径复算"→ 命中）与合成负例（"复算结果一致"→ 不命中）双向锁定。

`F-PLACEHOLDER`（新规则，Major）：匹配表体行 `(&\s*(---?|—|\\ldots|待填)\s*){2,}`——一行内 ≥2 个空占位单元格才报（单格 `-` 可能是合法负号/缺省记号）。仅在 `tabular/booktabs` 环境行内生效（行含 `&` 且非注释）。

### D3：`--per-chapter` 实验逐章检查（R4b）

`analyze_experiment.py` 新增：

1. **章切分**：用 `\chapter{...}` 正则切正文为章区间（绪论/结论/综述章按标题词排除：`绪论|引言$|结论|总结|展望|综述`）。每章内再按 `\section` 定位两类节：
   - `EXP_SEC_RE = 实验|案例研究|仿真验证|结果(及|与)?分析|应用验证`
   - `METHOD_SEC_RE = 方法|模型|建模|框架|策略|算法|设计`（用于 E-FIG）
2. **E-* 检查族**（全部 `[Script]`，行号 = 命中行或节首行）：

| 代码 | 判定 | Severity | 依据 |
|------|------|----------|------|
| E-DATA | 实验节可见文本无数据来源线索（`数据|样本|工况`）或无划分线索（`训练|测试|验证集|划分|\d+[:：/]\d+`） | Major | 范文 5/5 数据描述四要素 |
| E-ATTR | 实验节归因标记行占比 < 阈值（复用 B3 词表 `ATTRIBUTION_RE`，阈值 15%/最少 3 行，逐章计算） | Major | B3 逐章化 |
| E-REF | 实验节无 `\ref{tab:` 且无 `\ref{fig:` | Major | 图-表-文字呼应 5/5 |
| E-FIG | 方法/框架节无 `\ref{fig:` | Major | 框架图必备 5/5 |
| E-METRIC | 指标词（RMSE/MAE/MAPE/R2/ISE/IAE/HV…）出现但章内无 `equation/align` 环境且无 `[0-9]\.[0-9]\s*节` 复用指涉 | Minor | 指标给公式，首次给全 |
| E-PARAM | 实验节无参数线索（`参数设置|超参|学习率|迭代次数|表.{0,6}参数`） | Minor | 参数必有表 |
| E-ABL | 章内无消融线索（`消融|拆解|变体|去除.{0,6}模块|单独(使用|验证)`） | Info | 消融 5/5 有，但形态多样 |
| E-ECHO | 全章无 `第[2二]章` 回指且无跨章 `\ref` | Info | 3/5 靠反向承接，不得>Info |

   防误报红线锁定（负例单测必备）：无显著性检验/无均值±方差不报；人工经验基线不报（不做基线类型判断）；教科书基础节不触发 E-FIG（只对含"框架/结构/策略/方案"的节要求图）。
3. **R4a 结构提示**：默认模式下，若 `split_sections` 未找到 `discussion` → 输出一条 Info：`B3/B4 需独立讨论/综述章；本论文为逐章实验结构，建议使用 --per-chapter 逐方法章检查`。B5（conclusion）不动。

### D4：`--first-chapter N` 章序声明（R4c）

`analyze_logic.py` 增 argparse 参数 `--first-chapter`（int，默认 None）。传入后：章 order = N-1+文件内序号（现有 order 从 0 计），使单章文件的 `_check_chapter_intro` 第2章特判/承上检查按真实章号走。缺省时行为完全不变。文档口径（modules/logic.md + 指南）：跨章检查（承上启下、章间主线、P-PAPER 全文覆盖）**推荐在装配 document.tex 上运行**；单文件诊断须配 `--first-chapter`。

### D5：章式预判修复（R2e）

`_check_process_chapter` 现有 `PROCESS_CHAPTER_FEATURE_RE` 对"问题描述/总体框架"等通用节名过敏。改为**双信号判定**：须同时命中 ①过程信号（节标题或章标题含 `工艺|流程|过程分析|变量分析`）与 ②框架信号（`总体框架|技术框架|研究方案`），否则判为非过程分析章 → 只输出章式提示 Info 并跳过 P-DERIVE/P-FRAME/P-ORDER（P-FLOW 现已因 flow_secs 为空自然静默，保持）。fixture ch3~6 均无 ①信号，可锁定负例。

### D6：误报修复细则（R2a~R2d）

- **R2a**：`_check_heading_leads` 在 `\chapter` 与首个 `\section` 之间无正文时，若该 `\section` 标题匹配 `引言|概述`（与 `_check_chapter_intro` 的 07-11 判式复用同一常量），跳过"缺导语"报告。抽公共常量 `NUMBERED_INTRO_SEC_RE` 供两函数共用，防止再次分叉。
- **R2b**：`mixed_punctuation` 检查前先剥离 `\includegraphics(\[.*?\])?\{.*?\}`、`\input{…}`、`\bibliography{…}` 的花括号参数（或将该规则改为 `visible_only=True` 若 parsers 已提供路径剥离——以现有 visible 实现为准，实现时二选一，优先复用 parser 能力）。
- **R2c**：`oral_vague` 词表中"特别"改为带负向断言 `特别(?!说明|地|是)`（保留"特别好/特别大"等口语命中）。
- **R2d**：`_needs_method_justification_zh` 在"本文采用"后若接**定义/口径句式**（同句含 `等级|口径|分级|定义|记作|表示` 或采用对象为四字以上术语短语且句中无比较对象）则不报。保守起见：只加同句关键词负向条件，不做语义判断。

### D7：R3d "本文 vs 本章"（降险实现）

一期只做最保守词面：正文行匹配 `本文(提出|设计|构建)了?` 且**同一行**出现"模型/方法/算法/框架"+英文缩写（`[A-Z]{2,}[A-Za-z0-9-]*`）→ Info（提示核对是否应为"本章"）。方法名与章的绑定关系不做脚本判断（语义级，归 LLM 车道）。若合成负例误报 >0，整项撤为指南查重清单条目（R1⑧已兜底）——此为**预设降级路径**，不算返工。

### D8：`_check_chapter_intro` 缺承上分级（R5）

现"缺承上"输出保持检测逻辑不变，仅当章内**其余部分**出现 `第[一二三四五六七八九\d]+章` 引用（依赖线索：正文复用了前章产出）而引言无承接时维持原 severity；否则降为 Info，文案注明"并列方法章可不承上；若本章复用前章成果，建议在引言以角色复用句显式承接（见 method-chapter-guide-zh.md §3）"。

## 3. method-chapter-guide-zh.md 结构（R1）

体例对齐 process-chapter-guide-zh.md（判别表开篇 → 骨架 → 分节规范 → 检查清单 → 阈值出处表）。十节对应 prd R1①~⑩，末尾附"脚本检查映射表"（每条规范 ↔ 对应 E-*/P-*/F-* 或 LLM 车道），与 07-11 指南同型。预计 14~18K。防误报红线清单直接从 `research/body-chapter-conventions.md` §8 转写，阈值出处表引 5 篇范文 + 清华/中科院源（标"学科惯例，以导师与学校规范为准"）。

## 4. 数据流与兼容性

- 三脚本相互独立（无 import 依赖），E-*/P-PAPER 输出走各自现有 emit 函数，Output Contract 格式不变。
- `split_sections`/parsers.py 不改——章切分在 analyze_experiment.py 内部用正则实现（与 analyze_logic 既有章切分方式一致），避免碰 ALIGNMENTS。
- 与 07-11 的并行安全：本任务改 `analyze_logic.py` 的区域（heading_leads/P-PAPER 抽出/first-chapter/intro 文案）与 07-11 已交付区域有交叠，**开工前先确认 07-11 分支状态并 rebase**；`_check_chapter_intro` 第2章特判逻辑只读不改。

## 5. 测试与回滚

- 新增 `tests/skills/latex_thesis_zh/test_body_chapters.py`（E-* 族 + P-PAPER 泛化 + F-PLACEHOLDER + first-chapter）；误报修复进既有 `test_latex_thesis_zh_checker_precision.py` 追加负例。
- 合成 fixture：`tests/fixtures/latex_thesis_zh/`（若已有目录沿用）造 1 个装配样本（3 章：规范方法章负例 / 问题方法章正例 / 过程分析章边界例）+ 单章文件若干。问题模式取自用户论文但领域内容替换（脱敏规则同 07-11）。
- 回归护栏：跑 07-11 全部存量单测；用户论文只读复测（人工验收步骤，不进 CI）。
- Commit 切分 = 回滚单元：`fix(latex-thesis-zh): R2 误报五连修` / `feat(latex-thesis-zh): R3 拼接+草稿态` / `feat(latex-thesis-zh): R4 实验逐章` / `docs(latex-thesis-zh): R1+R5 指南与口径` / `chore(latex-thesis-zh): R6 路由+evals`。
