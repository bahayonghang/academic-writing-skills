# latex-paper-en 对应优化 (C3)

## Goal

把 C1 的密度/预算运行时切换到英文论文数据，并为 `latex-paper-en` 增加 opt-in 英文
段落弧线诊断。所有数值声明必须区分“5000 词基线等效换算”与“真实英文语料标定”。

父任务：`08-29-writing-rhythm-arc`。依赖 C1 `4b37ddf` 与 C2 `af84e4a` / `401ee53`。

## Evidence boundary

仓库没有 5–10 篇目标会议/期刊的可用英文论文语料。因此：

- `term_thresholds` 只把旧绝对上限按 5000 个可见词基线换算为每万词密度；
- 该换算只在 5000 词处保持绝对 allowance 相等，其他长度按密度机制有意缩放；
- `section_factors.organization=6.6` 借用 C1 中文标定，只是初值；
- P-ARC 的 N=2、τ=0.0200 与形态词表只由受控样本锁定运行时，不证明真实论文精度。

上述跨模板/跨 venue 代表性、查准率和召回率均为 **UNVERIFIED**，不得写成“英文语料标定”。

## Requirements

- R1：EN `term_thresholds` 采用 `per_10k_words`；旧上限乘 2，明确 5000 词基线等价
  与长度缩放边界（父任务 R1.1/R1.2/R1.4）。
- R2：新增 `P-ARC-LEAD/CLOSE/LINK/FLAT`，形态沿用 C2，词表与长度单位换成英文
  （父任务 R2.1–R2.3）。
- R3：同步 EN references、路由、双语 docs 与 manifest（父任务 R2.5）。

### R1 密度与序列词

- `latex-paper-en/scripts/deai_check.py` 的 YAML 和 `DEFAULT_THRESHOLDS` 同步切换；缺 YAML
  也不得回退到旧数据。
- 可见英文词使用运行时 canonical regex `\b[A-Za-z][A-Za-z'-]*\b`；连字符词计 1，
  公式/结构命令先由 parser 排除。不得另写 `\S+` 分母。
- `density_fallback.min_corpus=1500`；不足 1500 词按 1500 词 allowance 回退。
- `throat_clearing` 由旧全文 allowance 1 换算为 `budget_per_10k=2.0`、`min_budget=1`；
  同样只在 5000 词基线等价。
- `sequence_terms` 为 `first/second/then/finally/next`。它们只匹配小写独立词；
  `first-order`、`FIRST` 及其他连字符复合词不计。
- 序列词匹配逻辑属于三副本共享锁：若改 EN canonical，必须同步 ZH/Typst 的同一函数，
  但不改变 Typst 阈值数据。

### R2 英文段落弧线

- 新增 `--paragraph-arc`；默认关闭时输出逐字节不变。
- 合格段至少 40 个可见英文词。LEAD/CLOSE/LINK/FLAT 只报告可复算形态信号。
- `introduction`/`related` 中连续 2 个原始相邻合格段同时缺 LEAD+CLOSE 时，追加一条
  Minor/P2 汇总；单项 finding 始终 Info/P3。
- τ 暂取 0.0200：先把 token Jaccard 四舍五入到 4 位，严格 `< τ` 报 LINK；等于通过。
- 公式、图表、表格、算法、代码、列表、item、abstract、conclusion、acknowledgment、
  appendix 为豁免/硬边界；标题后首段不豁免（EN 无 S1 导语检查）。
- 所有 finding 含 `[Script] P-ARC-*` 与 `Meaning-Check: NEEDS-LLM`，不输出自动改写。

## Non-goals and constraints

- 不在无真实语料时调出“更合理”的 EN 密度数值或宣称准确率。
- 不改 funnel、tri-section、cross-section、motivation-thread 与既有方法叙述行为。
- 不给 EN 增加 S1 导语检查；不改 Typst 阈值数据。
- `logic` 模块不加改写契约；SKILL.md 若需触碰只改 `last_updated`。
- 不改 `justfile`、`pyproject.toml`。

## Acceptance Criteria

- [x] AC1（R1）对每个旧上限 A，5000 个可见词时新 allowance 恰为 A；计数 A 不报、
      A+1 报。测试同时证明 1500/10000 词按新密度缩放，不宣称任意长度等价。
- [x] AC2（R1）分母使用 canonical 可见词 regex；连字符词、缩写、撇号词、公式和结构
      命令样本的词数稳定。
- [x] AC3（R1）序列词仅匹配小写独立词；`first-order`、`FIRST` 不误计，三副本逻辑锁通过。
- [x] AC4（R2）缺 topic lead 与缺 wrap-up 分别产生独立 finding 并定位正确行；干净段不报。
- [x] AC5（R2）受保护环境、item、专用章节不报；LINK 与 N=2 都不跨标题、环境、短段、
      豁免段或 section scope；标题后首段仍参与检查。
- [x] AC6（R2）不带 `--paragraph-arc` 时稳定 fixture 输出与改造前基线逐字节一致。
- [x] AC7（R1）YAML 与 references 明示“5000-word baseline conversion, not corpus calibration”、
      所需语料 5–10 篇、半年复审节律及 UNVERIFIED 边界。
- [x] AC8（R3）`just ci`、三副本锁、单技能/全量资源同步、双语 contract 与 docs build 全绿。
- [x] AC9（R2）LINK 显式标记/重叠/空 token/τ 等于和小于边界，以及 FLAT 单句/罗列
      均有正反例。
- [x] AC10（R2）每条 finding 同时含 `[Script] P-ARC-*` 与
      `Meaning-Check: NEEDS-LLM`；`logic` 未增加改写契约。

## Gates

- G1：实现后用 allowance truth table 证明 5000 词基线等价及其他长度的预期缩放；
  任一不符先修口径，不通过“调阈值”掩盖。
- G2：人工阅读受控 EN 样本 finding；只证明运行时与已标注样本一致。真实论文精度继续
  标为 **UNVERIFIED**，等待作者提供 5–10 篇目标 venue 论文。

## Verification record (2026-08-29)

- G1：逐项 allowance truth table 已覆盖 1500/5000/10000 词；5000 词处旧上限 A 与新
  allowance 相等，1500/10000 词按新密度机制缩放。
- G2：`research/g2-synthetic-review.md` 已核对受控样本的 finding、行号、结构化标记和
  无自动改写边界；只证明 synthetic fixture 的运行时一致性。
- 聚焦密度/P-ARC/三副本锁回归：120 passed。
- 全量质量门：`just ci` 通过，1632 passed；Pyright 0 errors、74 个既有 warnings。
- 真实论文 precision/recall、跨 venue 代表性以及 N、tau、术语和 organization factor 的
  外部有效性仍为 **UNVERIFIED**。
