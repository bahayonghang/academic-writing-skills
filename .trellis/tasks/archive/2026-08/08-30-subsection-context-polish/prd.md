# 小节级逻辑润色（三元上下文窗口）

## 源需求

用户原话：

> 进行逻辑优化和语言润色的时候，要细化到 x.x.x 小节，然后分析上一小节的内容并结合下一小节，
> 对这一小节进行润色和优化，优化对应的逻辑等。

拆成三条可实现的要求：

1. 分析单元下沉到小节（编号形如 `2.1.1`），不再以章或语义章节组为最小单元。
2. 处理一个小节时，必须同时读入上一小节与下一小节的内容作为上下文。
3. 修改只落在当前小节；上一/下一小节只作为证据，不产出改写建议。

## 现状缺口

两个 skill 的粒度阶梯都缺「小节」这一层。

**latex-thesis-zh**

| 层级 | 已有机制 | 位置 |
| --- | --- | --- |
| 全文 | `--motivation-thread`、C3 跨章闭合 | `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py` |
| 章 | `--section`（`SECTION_TITLE_RULES` 多数 `max_level=1`）、章引言承上启下 S1/E-* | `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:561` |
| 段 | `--paragraph-arc` 四码 `P-ARC-LEAD/CLOSE/LINK/FLAT` | `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1470` |

`academic-writing-skills/latex-thesis-zh/references/writing/paragraph-arc-zh.md` 写明
`P-ARC-LINK` 不跨标题连接段落，代码也以 `segment_id` 阻断
（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1528-1535`），
因此「上一小节末段 ↔ 本小节首段」的接口目前没有任何检查器覆盖。

**paper-audit**

- `academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:112`
  `build_section_index` 用 `parser.split_sections()`，键是 `introduction/method/experiment`
  这类粗语义键；且只把单个源文件原始文本交给它（同文件 `:223-253`），不装配 `\include`。
- `academic-writing-skills/paper-audit/references/REVIEW_LANE_GUIDE.md` 的 lane 是章节组级。
- `academic-writing-skills/paper-audit/agents/section_reviewer_agent.md` 明确单位是
  "one major section or logical section group"。
- `academic-writing-skills/paper-audit/references/POLISH_GUIDE.md` 末段是唯一一处 subsection
  切分：仅当章节 > 1200 词时按 subsection 边界拆成两个 Mentor 调用，目的是控制上下文长度，
  拆开后两侧互不可见邻接内容。

## 需求

### R1 共用语义契约（父任务持有）

两个子任务必须实现同一套「小节单元 + 三元上下文窗口」定义，见 `design.md`。契约覆盖：
单元判定与来源定位（§1）、prev/next 选取与 canonical eligibility（§2.1-2.3）、
**字段级 schema 与出参投影**（§2.4-2.5）、只读边界与协议句真相源（§2.6）、
三个 `S-CTX-*` 码（§3）。

### R2 latex-thesis-zh 落地（子任务 A）

脚本层新增小节游标与跨标题接口检查，输出遵循既有 `[Script]` + `Meaning-Check: NEEDS-LLM` 形态。

### R3 paper-audit 落地（子任务 B）

工作区索引增补小节层与窗口文件；**把 `subsection_context_polish` 接入真实调度链**
（`FOCUS_TO_ALLOWED_LANES`、`ROLE_TO_REVIEW_LANES`、polish state），不只写进文档；
并把 POLISH_GUIDE 的按词数切分改为按小节游标切分并携带邻接上下文。

### R4 一致性锁

新增跨技能契约测试，按 `design.md` §5 指定唯一 canonical / mirror 文件与规范化比较规则。

### R5 多文件装配（TPR-01）

两侧都必须先装配 `\include` / `\input` 再枚举标题，并保留 assembled-line → source 的映射，
对外只暴露 `source_file` + 文件内行号。标题枚举走 `extract_headings()`，不经过
`split_sections()`。机制见 `design.md` §1.1.1。

### R6 无 depth-3 时的行为（TPR-04）

不回退到 depth-2。单元列表为空，不产出任何 `S-CTX-*`，并输出声明。见 `design.md` §1.1。

## 约束

1. 不违反仓库红线：不改 `\cite{}`、`\ref{}`、`\label{}`、数学环境。
2. 新开关默认关闭，不改变任一脚本的既有默认输出。
3. 不 bump 任何 `SKILL.md` 的 `version` 字段（全仓同步于 `pyproject`），只改 `last_updated`。
4. 新增 `references/` 文档必须同步 `docs/resource-manifest.json` 的 `sourceSha256` 与双语页面，
   否则 `tests/contracts/test_docs_bilingual_resources.py` 失败。
5. 不重造既有 owner 的检查：段内形态归 `P-ARC-*`，章引言承上启下归 S1/E-*，
   句级表达归 `check_style_zh.py`，AI 痕迹归 `deai`。新码只覆盖跨小节接口。
6. `--strength` 取值继续避开 `light|medium|heavy`（既定取舍）。
7. **不沿用 `_arc_is_eligible`**；小节级用 `design.md` §2.2 的 canonical eligibility，
   两侧数值相同，不允许按语种自行调整。

## 任务树

| 子任务 | 目录 | 交付 |
| --- | --- | --- |
| A | `.trellis/tasks/08-30-subsection-cursor-zh` | latex-thesis-zh 小节游标、`S-CTX-IN/OUT/ROLE` 三码、`--subsection-context` / `--emit-window`、术语 YAML、references、fixture、evals |
| B | `.trellis/tasks/08-30-subsection-lane-audit` | paper-audit 装配式小节索引、窗口文件、`subsection_context_polish` 接入 `audit.py` 调度链、mirror 协议文件、POLISH_GUIDE 与 ISSUE_SCHEMA 更新 |

执行顺序：A 先行（契约在 zh 侧落地并被测试固化），B 对齐 A 的用词。此顺序写在两个子任务的
`implement.md` 中，不依赖 Trellis 的父子结构表达依赖。

**合同变更 gate**：任一子任务若在实现中发现需要撤销或收窄一条 R（含 rollback 触发），
必须停止实现，返回本任务同步修订父与另一子任务的 PRD/AC，再继续。不得在子任务内部
静默替换数据合同或删码。

## 验收标准（父任务：跨子任务集成）

每条 AC 标注所证明的 R。子句级验收在各子任务 PRD 内。

- [x] **AC-P-01**（R2、R3）A、B 两个子任务各自的验收标准全部通过并归档。
- [x] **AC-P-02**（R1、R4）`tests/contracts/test_subsection_context_contract.py` 存在并通过，
      按 `design.md` §5 锁定三码集合、`S-CTX-DUP` 的负向断言、协议句、depth 定义句与
      「无 depth-3 不回退」声明句，以及 `subsection_context_polish` 在
      `audit.py` 常量中的存在性。
- [x] **AC-P-03**（R1、R5、R6）新增的 depth-3 fixture 上，zh 侧产品游标与
      `academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py` 产出的小节编号
      序列，各自等于同一份**写死的期望序列**，且两者相等；每个期望 ID 还必须能通过
      `analyze_logic.py --emit-window --subsection <id>` 取得窗口。`--subsection-context` 只输出
      命中的 finding，不承担完整枚举职责。只断言「两侧相等」不算通过——必须同时断言等于
      期望序列，防止两个空集合互等而误通过。
- [x] **AC-P-04**（R5）在既有多文件 fixture
      `academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex` 上，
      两侧窗口输出的 `source_file` 指向 `chapters/*.tex`，行号为文件内行号而非装配后全局行号。
- [x] **AC-P-05**（R1）窗口部件数量按 `design.md` §2.3 断言存在性与 `*_status`，
      不断言固定为三个或四个区间。单段小节、短段小节、列表/环境边界各有独立用例。
- [x] **AC-P-06**（R6）在既有 fixture
      `academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`（无 `\subsection`）
      上，两侧均输出「无 depth-3 标题」声明，产出零条 `S-CTX-*`，且不回退到 depth-2。
- [x] **AC-P-07**（R1、R3）只读边界的**行为**验收：构造一份 bait fixture，在 `prev.tail`、
      `next.head`、`parent_lead` 中各放入一个明显可改的表达问题，运行一次
      `subsection_context_polish` lane 与一次 polish Mentor 调用，核对全部改写建议只锚定
      `current`。当前平台无法稳定自动判定 LLM 输出，因此该项为
      **manual + UNVERIFIED**：记录核对结论与日期，不得用字符串契约测试代替。
- [x] **AC-P-08**（R3）`subsection_context_polish` 的启用/禁用矩阵有运行态测试：
      `--focus full` 与 `--focus logic` 下在允许集合中，`--focus methodology` / `literature` 下不在；
      `--mode polish` 的 state file 含 `subsection_windows` 键。
- [x] **AC-P-09**（R2、R3）`just ci` 全绿，pyright error 数不增加。
- [x] **AC-P-10**（R2、R3）两个 `SKILL.md` 的路由表各含一条指向新能力的行，
      且 `version` 未变、`last_updated` 已更新。
- [x] **AC-P-11**（R4）`docs/resource-manifest.json` 已收录新增 references，双语页面存在。

## 未核实项（承接审阅报告）

以下三项在规划阶段无法证实，实现时按标注处理，不得当成已验证：

1. LLM/Mentor 在真实调度中是否严格遵守只读边界 — 由 AC-P-07 以 manual + UNVERIFIED 承接。
2. article / Typst / PDF 输入的最终 subsection 与窗口行为 — article 由子任务 A 的新 fixture 覆盖；
   Typst 与 PDF 在子任务 B 中显式降级为「返回空单元列表 + `subsection_index_status`」，
   不声称支持。
3. 实现漂移 — 三任务均为 `planning`，实现开始后由 `trellis-check` 承接。
