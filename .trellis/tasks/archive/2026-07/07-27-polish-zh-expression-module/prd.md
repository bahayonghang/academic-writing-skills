# C3 ZH 润色模块补齐：expression 模块 + 中文机械检查脚本

父任务：`.trellis/tasks/07-27-polish-capability-upgrade`
覆盖 findings：**P0-3、P1-1、P2-2**
触及 skill：`latex-thesis-zh`（仅此一个）
依赖：C1 `design.md` 已冻结（`--goal` / `--strength` / 四字段 / `Risk-Flags` 闭集）

## Goal

为 `latex-thesis-zh` 补上完全缺失的**句子级 / 表达级润色能力**：新增 `expression` 模块、实现
`check_style_zh.py`、把孤儿文档 `academic-style-zh.md` 接入路由，覆盖中文特有的可判定项。

## Problem

### P0-3 — ZH 没有任何句子级 / 表达级润色模块

`latex-thesis-zh/SKILL.md:60-78` 的 17 个模块中**没有** `grammar` / `sentences` /
`expression`——而 EN 与 Typst 三个都有。

中文句长处理目前只存在于 `scripts/deai_check.py:630-664` 的 D1，且：需显式传 `--tier` 才启用；
量的是**句长变异系数 CV 过低**（机械均匀＝AI 痕迹）；**不是**"这句 80 字读不懂，该拆"。

结果：「这段句子太长太绕，帮我理顺」「这段太口语，改学术一点」在 ZH 无归属模块。`logic`（论证
层）与 `deai`（AI 痕迹层）都不覆盖这一层。

### P1-1 — `academic-style-zh.md` 是孤儿文档

136 行成熟中文学术规范（口语化纠正 / 绝对化词汇 / 逻辑连接词 / 常见语病 / 标点 / 数字单位），
**不在 SKILL.md Reference Map**、**无模块路由**，全仓仅 `deai/guide.md:557` 与
`tense-guide-zh.md:54` 两处"另见"。P1-1 与 P0-3 是同一个洞的两面：没有模块，文档就无处挂载。

### P2-2 — 中文机械性检查空缺

`academic-style-zh.md:93-136` 列了一批中文特有项：搭配不当（§4.1）、成分残缺（§4.2）、标点
混用（§5.3）、数字与单位（§6）。ZH `references/formatting/` 只有 caption / formula / table
三份，**无数字单位参考**（EN 有 `number-unit-guide.md`，Typst 有 `NUMBER_UNIT_GUIDE.md`）。

**但**：这些项的可自动化程度差异极大，不可一律称为"可机械判定"。逐项分级见 `design.md`。

## Requirements

### R1 — 新增 `expression` 模块（P0-3 + P1-1）

- SKILL.md 路由表新增 `expression` 行（Use when / Primary command / Read next 三列）。
- 新建 `references/modules/expression.md` 作为模块入口，指向
  `references/writing/academic-style-zh.md` 作为规则真相源。
- `academic-style-zh.md` **加入 SKILL.md Reference Map**（关闭 P1-1）。
- 更新 SKILL.md 路由规则与 `references/modules/routing-rules.md`，把 `expression` 放进既有
  「论证/逻辑 → 句子结构 → 词汇/排版」序列的第 2/3 层
  （见 `references/writing/writing-philosophy-zh.md:124-133`）。

### R2 — 实现 `scripts/check_style_zh.py`（P2-2）

按 `design.md` 的逐检查器契约实现，每个检查器须明确：**检查器 ID / 输入区域 / 排除条件 /
输出档位（auto / candidate / llm-only）/ 误报预算**。落地 C1 的四字段契约与
`--goal` / `--strength`。

输出沿用 ZH 既有格式：`% EXPRESSION (源文件:行号) [Severity][Priority] [Script]: ...`，
多文件工程走 `tex_loader.assemble` 的 `lineref`。

### R3 — 新建 `references/formatting/number-unit-guide-zh.md`

规则源：`academic-style-zh.md:125-136` + 仓库已引用的国标——**GB/T 15835**（出版物上数字用法）
与 **GB 3100 / GB/T 3101 / GB/T 3102**（量和单位），标点用 **GB/T 15834**。这些编号已出现在
`templates/yanshan.md:13,62`，与本仓既有事实源一致。

**标准优先级须写明**：学校模板规范 > 通用国标。模板与国标冲突时以
`templates/<template>.md` 快照为准（模板快照是本仓模板事实的唯一权威源）。

不直接复制 EN 版——中文有「概数用汉字」「序数用中文」等 EN 没有的规则。

## Out of Scope

- **不走 EN 脚本移植路线**（用户已选新模块 + 新脚本）。
- 不改 `deai_check.py` 的 D1-D5 维度与阈值。
- 不改 EN / Typst 任何文件。
- 不新增 reviewer-response 能力。
- **不检查人称**——见 Constraint 1，该领域已有 owner。

## Constraints（本子任务最易踩的坑）

1. **人称检查不归本模块**。`academic-style-zh.md:43-48` 写「我们 → 本文/本研究」，但既有实现
   已划分了两条**互不相同**的规则：
   - `analyze_abstract.py:936-940` **T-VOICE**：只查第一人称 `笔者|我们|我(?!国)`；
     注释明写 `本文/本论文 are legal (Info)`。
   - `analyze_abstract.py:626,708` **T-OPEN**：`OPEN_BAD` 含 `本文`，但语境是**首句应定位研究
     对象而非方法**，与 T-VOICE 不同维度。

   `check_style_zh.py` **不得实现任何人称检查**，模块文档只写"人称问题见 `abstract` 模块的
   T-VOICE / T-OPEN"。这是本仓已判定的边界，重造必冲突。

2. **数字用法与 spec-check 重叠**。`templates/yanshan.md:151` 的 **YS-36** 已覆盖「数字用法
   符合 GB/T 15835」，判定方式为 `llm`。`expression` 的数字检查须与 YS-36 划清：
   - `expression`：通用可判定项（数值与单位间距、单位斜体、概数/序数用字）
   - `spec-check` YS-36：模板专属的完整数字规范终检
   两者输出须互不重复报告同一问题；模块文档双向写明指路。

3. **单位正斜体与红线冲突**。`academic-style-zh.md:136` 要求「单位使用正体字母（非斜体）」，
   在 LaTeX 中该问题位于**数学环境内**，而红线一是「绝不修改数学环境」。故此检查器
   **只能 report，永不 auto-fix**，且须在输出中说明"需作者手动在数学环境内调整"。

4. **绝对化词汇与 over-claim 边界**。`academic-style-zh.md:59-73` 的绝对化词表（显然/毫无
   疑问/必然/最优…）与 `references/writing/over-claim-guard.md` 的因果/首创/普适表有重叠面。
   `expression` 只处理**词汇层**替换建议；论断强度分级仍归 over-claim-guard，不重复实现。

5. **长句与 deai D1 边界**。`expression` 的长句检查语义是**可读性**（单句过长）；
   `deai_check.py` D1 是**均匀度**（CV 过低）。两者不得报同一条 finding，模块文档写明。

6. `scripts/parsers.py` 的 ZH 副本与 EN canonical 有**有意分歧**（ZH 省略 `clean_text`），由
   `ALIGNMENTS` 锁定。新脚本只**消费** parsers，不修改；若必须改则同步更新 `ALIGNMENTS`。

7. SKILL.md 路由表新增行触发 `ROUTER_ROW_RE` 契约测试；`evals.json` 走 Bash python 写入；
   不给 pytest 加 `PYTHONIOENCODING=utf-8`；Windows 下重定向 JSON 需
   `PYTHONIOENCODING=utf-8` 但不要 export 全局；只改 `last_updated` 不 bump `version`。

## Acceptance Criteria

- [ ] `expression` 出现在 SKILL.md 路由表，三列齐全
- [ ] `references/modules/expression.md` 新建，指向 `academic-style-zh.md` 为规则真相源
- [ ] `academic-style-zh.md` 进入 SKILL.md Reference Map（P1-1 关闭）
- [ ] `check_style_zh.py` 按 `design.md` 逐检查器契约实现，每个检查器有稳定 ID 与档位标注
- [ ] **无人称检查器**（constraint 1）；模块文档指路 T-VOICE / T-OPEN
- [ ] 单位正斜体检查器只 report 不 fix，且输出说明数学环境红线（constraint 3）
- [ ] 数字检查与 YS-36 双向指路，无重复报告（constraint 2）
- [ ] 长句检查与 deai D1 语义区分写入文档，无重复报告（constraint 5）
- [ ] 每个检查器有正例 + 反例测试；反例须覆盖 design 中声明的排除条件
- [ ] 输出含 C1 四字段，`[Script]` 层 `Meaning-Check` 恒 `NEEDS-LLM`；多文件定位为 `源文件:行号`
- [ ] `--goal` / `--strength` 可用，默认 `grammar` / `minimal`
- [ ] `references/formatting/number-unit-guide-zh.md` 新建，含国标编号与模板优先级声明
- [ ] routing-rules 写明 `expression` 与 `deai` / `logic` / `spec-check` / `abstract` /
      `conclusion` 的边界
- [ ] `evals/trigger_eval.json` 新增 `expression` 触发用例（Bash python 写入）
- [ ] `just ci` 全绿，passed ≥ 1338，pyright error = 0
