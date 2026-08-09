# latex-paper-en 方法节扩展与 typst-paper 镜像

## Goal

扩展 EN `section-writing/method.md` 为逐边接口契约，在 EN/typst `analyze_logic.py` 的
`--section methods` 分支补 M-HEADING / M-SEQWORD / M-EQUATION 与 M-EDGETABLE 骨架，新建 typst
方法节参考镜像，TRANSITIONS 增 `sequence` 类（M-SEQWORD 依赖），并交付跨技能 M-* 判据契约
测试。判据唯一权威 = 父 design §2。

## Requirements

### R1 EN 参考扩展 `references/writing/section-writing/method.md`

在现有 Module Triad / Pre-Writing Table 基础上新增，不推翻现有结构：

1. Pre-Writing Table 后增逐边表：每对相邻模块一行（Upstream output / Connection type /
   Intermediate transform / Downstream use）。
2. 新节 Inter-module interface contract：六类连接类型判据表 + M-NONDIRECT（无直接数据依赖须
   显式排除误读，含例句）。
3. 新节 Equation closure：purpose → equation → symbol gloss → downstream use；与 notation
   一致性检查区分（后者查矛盾，本节查缺失）。
4. 新节 Heading discipline：run-in heading 报幕反模式定义 + 合法用法边界（Related Work 分组、
   实验结论 lead-in，引用 style-guide.md 不复述）。
5. 收益表述：四类主张映射 `claim-evidence-contract.md` 强度梯，互链不复述。
6. 遵守 section-writing 单文件渐进加载预算，扩展后保持单指南体量。

### R2 EN/typst 检查器 `analyze_logic.py`

1. `--section methods` 分支内新增 M-HEADING / M-SEQWORD / M-EQUATION + M-EDGETABLE
   （判据=父 design §2 en/typst 侧；typst M-EQUATION 仅查带 `<label>` 的块级公式——
   决策已在父 design §2.3 定稿，无实现期降级）。无 `--section` 或其他节值不触发。
2. `TRANSITIONS` 词典增 `sequence` 类（词组=父 design §2.2 顺序词起手所用集合，单一来源）；
   `example` 类缺口不在本任务（遗留清单）。`_has_transition` 行为变化以"现有 fixture finding
   集合不增"为回归锁。
3. EN 与 typst 副本 Tier-2 同构（函数集与判据常量一致，MN_ 常量命名与 zh 对齐）。

### R3 typst 参考镜像 `typst-paper/references/METHOD_SECTION.md`

顶层新建：authoritative 注记指向 EN method.md（小写路径）→ Typst 语法差异要点（`==` 小节、
`*...*` 强调、`$..$ <label>` 公式）→ 逐边接口表 Typst 示例 → 诊断入口
`analyze_logic.py main.typ --section methods`。只译要点+语法适配，正文指路 EN 权威源。

### R4 跨技能契约测试（父 design §2.6）

新建 `tests/contracts/test_method_narrative_alignment.py`：importlib 加载三份 analyze_logic
副本，断言结构常量（MN_HEADING_RUN=3 / MN_HEADING_HITS=2 / MN_EQUATION_LOOKAHEAD=3）三方相等；
en/typst 全部 MN_ 正则源串逐字相等；zh 中文正则常量存在。C1 未完成时本测试对 zh 侧标记
xfail 并在 C1 归档后转正（若 C2 先行）。

### R5 测试与文档同步

1. EN/typst M-* 用例：病例三码触发 / 合规零发现 / 无 `--section methods` 不触发 / 红线负例
   （EN Related Work `\textbf{...}`、typst 实验段 `*Title Case Heading.*`）不触发。
2. SKILL.md：EN/typst Reference Map 加行（路由行命令已含 `--section methods`，不改）；
   `last_updated` 更新。
3. 双语契约（方向：英文源）：manifest 更新（method.md sha 变更 + METHOD_SECTION.md 新条目）；
   docs/ 英文页与源一致、docs/zh 页完整中文译文；两对 index.md 加行；
   `check_resource_sync.py --skill latex-paper-en` 与 `--skill typst-paper` 自查。

## Acceptance Criteria

- [x] EN method.md 含逐边表、六类连接表、M-NONDIRECT、公式闭环、Heading discipline，
      Module Triad 原结构未破坏。
- [x] EN/typst `--section methods` 下病例三码触发、合规零发现、无节参数不触发、
      两条红线负例不触发；typst M-EQUATION 仅对 labeled 块公式触发有测试锁定。
- [x] TRANSITIONS 含 `sequence` 类且现有测试无回归（finding 集合不增）。
- [x] `test_method_narrative_alignment.py` 在位并绿（或 zh 侧 xfail 注记明确）。
- [x] typst METHOD_SECTION.md 存在且 authoritative 注记路径小写正确。
- [x] `just ci` 全绿；两技能 `check_resource_sync.py --skill` 通过；两个 SKILL.md version 未变更。

## 排除项

- TRANSITIONS `example` 类扩充、typst `modules/LOGIC.md:86` 大小写修复——移出本任务
  （父 research/repo-recon.md §4 遗留清单）。
- 不改 flow.md / self-review.md / deai 词表；不动 zh 侧实现（契约测试的 zh 断言除外）。
