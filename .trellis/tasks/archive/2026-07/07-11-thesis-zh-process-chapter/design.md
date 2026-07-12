# design.md — latex-thesis-zh 第二章（过程分析章）优化技术设计

## 设计原则

1. **不新增 Module Router 行**：主线检查挂 `logic`（`--process-chapter` 新 flag），源码卫生挂 `format`（check_format.py 内置检查，无新 flag），避免路由表改动触发 contract 锁与 trigger 评测成本。
2. **脚本管确定性、LLM 管判断**：流程图/框架图引用、"第 X 章"映射覆盖、特性词-因果连接、Markdown 残留等可确定性计算的走 `[Script]`；工艺描述深度是否足以支撑难点、框架图分层是否合理、绪论-第二章是否实质重复等走 `[LLM]`（读指南后给提案）。
3. **细节下沉 references**：SKILL.md 只在 logic 行 Use when 补触发词 + Reference Map 加一行；指南全文放 `references/writing/process-chapter-guide-zh.md`。
4. **形态兼容优先于形态偏好**："编号 2.1 引言"与"章后导语"两种形态均合规（参考论文 4:1 分布），检查器适配两者，指南不强推其一。

## 改动清单

### 脚本（academic-writing-skills/latex-thesis-zh/scripts/）

**analyze_logic.py — ① R2 章引言形态适配（默认行为，bug-fix）**

- `_check_chapter_intro` 现逻辑：章引言块 = 章标题行+1 → 首个 level≥2 小节行-1；`\chapter` 后直接 `\section{引言}` 时 intro_text 为空 → 误报。
- 适配：当章引言块为空（或 <40 字）且首个下级小节标题命中 `INTRO_SECTION_TITLES_ZH = ("引言", "概述", "引 言")` 时，改取**该小节的正文**（小节标题行+1 → 下一同级或更高级标题行-1）作为 intro_text，来源标记 `numbered`，报告行号定位到引言小节标题行。
- **第 2 章特判（research §1/§7）**：参考论文 5/5 的第二章引言均为"本章概述式"（预告本章各节、承接绪论已建立的背景，而非承接前一章结论）。故对**第 2 章**（含"章后导语"与"编号引言节"两形态）只检查"启下（预告各节/本章任务）+ 篇幅"，**不报"缺承上衔接"**；承上启下两段式（含承接前章结论）仅对第 3 章起的正文方法章适用。实现上：`_check_chapter_intro` 的承上检查按章序跳过第 1 个正文章（即第 2 章）。这修正了"把第二章引言当普通承上启下章引言"的偏差。
- 篇幅口径拆分：现有常量改为按形态取值——`lead` 形态沿用 40~900；`numbered` 形态默认 `CHAPTER_INTRO_NUMBERED_MAX_CHARS = 1600`（依 5 篇参考论文引言节实测 600~1500 字定，research/chapter2-content-analysis.md 落盘后校准），下限沿用 40。超限措辞区分"编号引言节过长（细节应下沉后续小节）"。
- 兼容性：锌冶炼式"章后导语"路径零变化；`CHAPTER_INTRO_EXEMPT_TITLES_ZH` 中的"引言"仍只豁免**章标题**含引言的章（含义不变，加注释澄清两处"引言"角色差异）。
- 存量单测 `test_intro_mainline.py` / `test_latex_thesis_zh_scripts.py` 中章引言相关用例同步补两种形态（一正一反）。

**analyze_logic.py — ② R3 `--process-chapter` 主线检查**

- 目标章定位：默认取章号 2（`\chapter` 序列中第 2 个非豁免正文章即"第 2 章"；被 `--section` 覆盖时按用户指定）。定位后先做**章式预判**：章内（标题+正文）出现 `工艺|流程|过程分析|问题描述|总体框架|方案|影响因素` 任一 → 过程分析章，跑 P-*；否则输出一条 Info"该章未见过程分析章特征，若为方法+实验章式请走方法章规则"，不套用 P-*（对应 PRD 边界例验收）。
- 节分类启发式（按小节标题关键词）：
  - 工艺节：`工艺|流程|过程(描述|分析|简介)|系统简介|机理`
  - 难点/问题节：`难点|问题|挑战|影响因素|特性分析`
  - 框架节：`框架|方案|架构|总体|策略`
- 检查项（编号续 L-* 之后，用 P-* 前缀，输出 `% 过程分析章 ...` 前缀）：
  - `P-FLOW`（Major/P1）：工艺节范围内无 `\\ref\{fig:` 引用。多工艺小节时任一小节有图即通过。
  - `P-DERIVE`（Major/P1 缺特性词；Minor/P2 有词无因果）：难点/问题节扫特性词表 `PROCESS_TRAIT_RE_ZH =（强?非线性|大?(滞后|时滞|惯性)|强?耦合|时变|多工况|多速率|多源异构|波动|不确定|扰动|长尾|不平衡）` 与因果连接词 `(导致|使得|难以|造成|致使|因而|从而)`；同句/邻句共现视为有推导链。
  - `P-FRAME`（框架图缺→Major/P1；框架空泛→Major/P1；章号映射缺→Info/P3）：框架节范围内 ①须含 `\\ref\{fig:`（缺→Major）；②须覆盖 ≥2 个方法模块名或"第 X 章"指向（否则框架空泛→Major）；③"第 X 章"显式章号映射未覆盖后续方法章 → **Info（推荐加强项）**，措辞为"建议显式标注'第 X 章'章号映射以增强可读性/可答辩性"。**判据依据**：research §4 核实 5 篇范文中 3 篇（史鑫/粉磨/MSW）框架节完全不写章号、用方法模块名组织数据流，靠后续各章引言"根据第 2 章…"反向承接；强制"漏章点名 Major"会对多数真实论文误报，故降 Info。**但用户决策：指南与脚本均将"显式章号映射"作为推荐加强项**（写法更规范、便于盲审与答辩定位），Info 提示主动建议补全，而非中立。系统/工程应用章（如第 6 章）允许缺席映射，只出 Info。
  - `P-ORDER`（Minor/P2）：框架节行号先于难点/问题节行号。
  - `P-PAPER`（Minor/P2）：章内可见正文命中 `(源论文|小论文|[一二两三四五12345]\s*篇(学术)?论文)` → 建议改"核心问题/研究内容"表述；`\cite`、注释内不计。
- 全部检查读 `extract_visible_text` 后的可见正文，注释/数学环境天然排除；多文件工程沿用 tex_loader 展开后的 `源文件:行号` 定位。

**check_format.py — ③ R5 源码卫生检查（默认行为，新增两项）**

- `F-MD`（Major/P1）：可见正文行命中 `\*\*[^*\n]{1,80}\*\*`（Markdown 加粗）→ "LaTeX 中 Markdown 语法按字面星号排版，应改 `\textbf{}`"。仅扫可见文本，数学环境/verbatim/注释排除；`\*\*`（转义星号）不计。
- `F-NOTE`（Info/P3）：可见正文行命中保守词表 `(后续可根据.{0,20}(替换|更新|补充)|此处占位|待补充|待确认|TODO|FIXME)` → "疑似草稿备注泄漏进正文，定稿前应删除或移入注释"。词表刻意收窄避免误伤正常学术让步表述（如"仍需通过实验确认"不命中——不含触发词形）。
- 两项均放入 check_format 默认输出（该脚本本就是全量体检式输出，新增确定性强、误报率低的检查不破坏契约）；如现有测试对输出条数有锁，同步更新。

### references/

- **新文件 `references/writing/process-chapter-guide-zh.md`**（第二章专章，约 250~300 行），内容与 PRD R1 ①~⑩ 一一对应；所有实例句/骨架/框架图分层描述取材 research/ 两份调研文件（5 篇论文原句已注 PDF 页码，可直接引用为正反例）；每个阈值注"学科惯例（依 5 篇流程工业博士论文与公开目录调研），以导师与学校规范为准"。诊断入口块（对齐 introduction-guide-zh.md 开头形式）：

  ```bash
  uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex --process-chapter
  uv run python $SKILL_DIR/scripts/check_format.py main.tex
  ```

- **`references/writing/structure-guide.md`**：正文部分第 7 条"第二章：相关工作/文献综述"改双轨表述（工业/过程背景=过程分析章式，指向新指南；CS/方法学=相关工作式；综述已入绪论则不得重复设章）；"直属小节数量"节补一句"过程分析章常见 4~7 直属节（含引言/小结），超 5 节优先检查可合并的变量/数据节"。
- **`references/writing/thesis-writing-guide.md`**："方法章节"一节前加一行指针：第二章为过程分析章式时先读 process-chapter-guide-zh.md。
- **`references/modules/logic.md`**：仿 Intro Mainline 节，新增 `--process-chapter` 检查表（P-FLOW/P-DERIVE/P-FRAME/P-ORDER/P-PAPER 各一行：Rule + Severity）与章式预判说明。
- **`references/modules/format.md`**：追加 F-MD / F-NOTE 两行说明。
- **`references/modules/routing-rules.md`**：新增判据条目——涉及"第二章怎么写""工艺流程分析""总体框架图""章式"时走 `logic --process-chapter` 并补读新指南；"第二章=方法+实验"流派按方法章既有条目处理。

### SKILL.md

- logic 行 Use when 追加"第二章工艺分析/总体框架章式"；Reference Map 加 `references/writing/process-chapter-guide-zh.md` 一行；last_updated 改 2026-07-11，version 不动。改表格时注意全局格式化 hook 会重排表格列宽 → 提交前跑 contract 测试确认 ROUTER_ROW_RE 仍匹配。

### tests/（tests/skills/latex_thesis_zh/）

- 新增 `test_process_chapter.py`：合成 fixture（水处理/通用流程工业领域脱敏样本，双文件：正例章 + 病例章）覆盖 P-FLOW/P-DERIVE/P-FRAME/P-ORDER/P-PAPER 各一正一反 + 章式预判负例（方法章式输出 Info 不套 P-*）+ 默认章定位与 `--section` 覆盖。
- 新增 `test_chapter_intro_forms.py`（或并入 test_intro_mainline.py）：编号引言节形态（含承上正/反例、1600 上限正/反例）、章后导语形态回归、"引言章标题豁免"角色不受影响。
- check_format 测试补 F-MD / F-NOTE 一正一反（`**bold**` 命中、`\*\*` 不命中、"仍需实验确认"不命中）。
- 全部走 conftest 的 `SCRIPT_DIR_ZH` 导入约定。

### evals/

- `evals.json` 追加 2 条：①"帮我看第二章工艺流程分析和总体框架写得对不对" → 断言路由 logic + `--process-chapter` + 读新指南；②"我的第二章直接写方法和实验" → 断言不套过程分析章检查、走方法章规则。走 Bash python 写入（JSON hook 陷阱）。

## 关键取舍

- **P-* 不做自动改写**：只诊断+建议，改写属 `[LLM]` 提案（延续 literature 模块契约）。
- **默认章号 2 而非标题推断**：标题关键词做章式预判而非定位依据，避免"工艺"出现在第 3 章标题时误定位；非 2 章的过程分析章用 `--section` 显式指定。
- **F-MD/F-NOTE 放 format 而非新模块**：源码卫生与排版同属"format 体检"心智模型；也避免 deai（AI 痕迹）语义混淆。
- **P-PAPER 放 logic 而非 blind-review**：它是章式表述规范（写作期），不是送审隐匿动作（定稿期）；blind-review 侧不动。
- **工程应用章在框架图中的地位**：参考论文两种写法并存时降为 Info 提示；research 内容分析若显示 5 篇一致，则按一致口径定级（实现前查 research/chapter2-content-analysis.md）。
- **不做绪论-第二章重复度的脚本检查**：跨章语义重复是 LLM 判断，指南给查重清单，脚本不硬检。

## 兼容与回滚

- `--process-chapter` 为新 flag，默认行为零变化；R2 章引言适配与 R5 format 新增是默认行为变化——前者修误报、后者只增不改，均同步更新存量单测并在 commit message 声明。
- Commit 序列（各自可 revert）：①R2 章引言适配+测试 ②R3 process-chapter+测试 ③R5 format 卫生+测试 ④R1/R4 references 文档 ⑤R6 SKILL.md+routing+evals。
- 不触碰 parsers.py（ALIGNMENTS 锁）；不触碰其他技能目录。
