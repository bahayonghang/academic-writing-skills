# 共享可见正文 IR 与已复现缺陷修复

父任务：`.trellis/tasks/08-25-thesis-zh-quality-closure`
证据源：父任务 `research/evidence-audit.md`（勿重复调研）

## Goal

在 `tex_loader.AssembledDocument` 之上建立共享的 typed node 可见正文 IR，
并用它修掉四项已实跑复现的缺陷（V1-V4）。本子任务是后续所有子任务的地基：
语义中间产物、mode 契约、re-audit 都消费同一 IR。

## Scope

**改**：`academic-writing-skills/latex-thesis-zh/scripts/`（新增 `visible_prose.py`；
迁移 `deai_check.py`、`analyze_logic.py` 的过程章定位）、
`tests/skills/latex_thesis_zh/`、`academic-writing-skills/latex-thesis-zh/references/modules/deai.md`、
`docs/` 双语镜像 + `docs/resource-manifest.json`。

**不改**：`parsers.py` 被 `test_parsers_alignment.py` 哈希锁定的成员（父任务决策 3）；
其余 8 个 `extract_visible_text` 消费者（本子任务只迁移 deai 与过程章定位两条路径，
其余留兼容视图，由后续子任务按需迁移）；构建配置；其余 19 个带 `main()` 的脚本入口
的 UTF-8 自设（TPR-06，记为后续工作项）。

## Requirements

- R1：typed node IR（`academic-writing-skills/latex-thesis-zh/scripts/visible_prose.py`）。
  从 `AssembledDocument` 构建节点序列，每个节点至少含：`node_id`、`kind`、
  `section_role`、`source_span{file,start,end}`、`assembled_span{start,end}`、
  `visible_text`、`protected_tokens`、`generated_from`、`analysis_channels`。
  `kind` 取值：`visible_paragraph` / `heading` / `list_item` / `table_cell` /
  `caption` / `math` / `control` / `comment` / `generated`。
  节点默认处理：`math` / `control` / `comment` 保护并排除自然语言 finding；
  `caption` 只进题注与结果证据定位通道；`list_item` / `table_cell` 可进
  贡献/科学问题/结果语义识别但不套段落节奏规则；`generated` 只读。
  IR 必须导出 `visible_zh_chars` 与 `visible_sentences` 供阈值归一使用，
  以及 `ir_version` 供消费者检测 schema 变化。

- R2：章节角色分类与过程章选择是两步，不得把全部 `body` 当作过程章候选（TPR-03）。
  `section_role` 取值：`frontmatter` / `abstract` / `nomenclature` / `body` /
  `appendix` / `achievements` / `acknowledgements` / `unverified`。
  分类信号：include path、标题 role classifier、
  `\frontmatter` / `\mainmatter` / `\appendix` / `\backmatter`、模板专用宏。
  无 `\mainmatter` 时：标题或路径能唯一分类的专章仍赋专章 role；其余未冲突的
  `\chapter` 默认为 `body`，不因缺少 mainmatter 一律降为 `unverified`。
  标题与路径冲突时赋 `unverified`。
  第二步：在 `section_role in {body, unverified}` 的 chapter 上用既有双信号
  （`PROCESS_SIGNAL_RE_ZH` 与 `PROCESS_FRAME_SIGNAL_RE_ZH`，章标题加 level>=2
  小节标题）选择过程章。命中数 = 1 则选中；命中数 ≠ 1 且无 `--section` 时要求
  显式指定，不取首个、不回退「绪论后首个非豁免 chapter」。

- R3：阈值按可见字数归一（修 V2）。不改 `term_thresholds` cap 值。
  计数单位锁定为每 10000 个可见汉字最多 N 次。`min_sample` 锁定为 2000。
  分子：`term_threshold` 通道节点中该词项的出现次数。
  分母：同一通道节点的可见汉字数（不含不进入该通道的节点）。
  短文本策略：`visible_zh_chars < min_sample` 时不触发（不是回退 `count > cap`）。
  `visible_zh_chars >= min_sample` 时整数判定
  `count * 10000 > cap * visible_zh_chars`。
  切换点性质：`min_sample-1` 恒不触发；跨过 `min_sample` 只可能从静默变为按比率
  判定，不会从触发变为静默。真实学位论文量级不作为实现输入（TPR-04）。

- R4：跨行环境体不进入词频计数（修 V3）。IR 的 `table_cell` / `math` /
  `generated` 节点不进入 `term_threshold` 通道。`generated` 判定不只看文件名：
  接受 project adapter 声明，仅有生成注释或路径线索时标 `inferred` 并阻断自动
  写入，无 owner 证据时标 `missing evidence`（本子任务只需 IR 侧标记能力，
  adapter schema 由子任务 2 落地）。

- R5：CLI UTF-8 自设（修 V4）范围缩到本子任务迁移的两个入口：
  `deai_check.py` 与 `analyze_logic.py`（TPR-06）。共享 helper
  `ensure_utf8_stdio()` 在 argparse 之前调用。`reconfigure` 可用则设 UTF-8；
  不可用时若 stderr 可写则输出一行修复命令
  （`PYTHONIOENCODING=utf-8` / `$env:PYTHONIOENCODING='utf-8'`），
  不可写则跳过且不抛异常。本子任务验收只覆盖 subprocess pipe；Windows 原生
  console / GUI 标 **missing evidence**。其余 19 个 `main()` 入口列入后续工作项。

- R6：finding identity 为 `rule_id + 归一化 source span + evidence hash`；
  同一根因的相邻 finding 可合并但必须保留所有 source span。

- R7：兼容层拆为严格不变面与已批准语义差异面（TPR-05）。
  `parsers.extract_visible_text(line)` 保留一个版本周期。未迁移的 8 个消费者
  （`analyze_conclusion` `analyze_experiment` `analyze_literature`
  `blind_review` `check_format` `check_spec` `check_style_zh` `deai_batch`）
  的命令、flag、help、人类可读输出格式与改造前逐字节一致。
  已批准差异：`analyze_logic.py` 章引言覆盖集合（特殊章不再被查）、
  `deai_check.py` 词项触发公式、finding 去重键。差异须写入 golden delta。

- R8：docs manifest、SKILL.md `version` 保持 `6.0.0`、新测试位于
  `tests/skills/latex_thesis_zh/`、路由 `--flag` 与 `--help` 一致、
  `just ci` 与 `just doc-build` 通过。

## Acceptance Criteria

- [ ] AC1（R2）：B1 fixture（include 顺序：符号表 → 绪论 → 工艺章 → 方法章 →
      成果章，无 `\mainmatter`）上，`--process-chapter` 经两步选择唯一选中工艺章
      `process.tex`；符号表章与成果章零主线 finding。改造前该结构选中符号表章
      （design.md 记录改造前实跑输出）
- [ ] AC2（R2）：同一 fixture 去掉工艺章双信号后，无 `--section` 时输出要求显式
      指定，不取首个 body 章；标题与路径冲突的章 `section_role=unverified`
- [ ] AC3（R3）：性质测试覆盖 `min_sample-1` / `min_sample` / `min_sample+1`：
      前者无论 count 均不触发；后两者按 `count * 10000 > cap * visible_zh_chars`
      判定。分母只计 `term_threshold` 通道节点
- [ ] AC4（R3）：同密度内容在 `visible_zh_chars >= 2000` 的 1 / 2 / 4 倍篇幅下，
      4 倍篇幅不再因累计计数产生假阳性
- [ ] AC5（R4）：7 次「首先」全部位于 `tabular` 行与 `equation` 的 `\text{}` 内时，
      `term_threshold` 不触发；同样 7 次出现在正文段落时正常触发
- [ ] AC6（R5）：`PYTHONUTF8=0` 且不设 `PYTHONIOENCODING` 的 subprocess pipe 下，
      `deai_check.py --help` 与 `analyze_logic.py --help` 的中文按 utf-8 解码成功。
      `reconfigure` 不可用的测试替身断言结果为修复提示或 `skipped`。Windows 原生
      console 标 **missing evidence**
- [ ] AC7（R1）：每个 finding 的 source span 可映射回 `源文件:行号`；
      `math`/`control`/`comment` 零自然语言 finding；`caption` / `list_item` /
      `table_cell` 在其允许通道内仍可检索
- [ ] AC8（R6, R7）：finding 去重键为 `rule_id + 归一化 source span + evidence hash`；
      该项属于已批准语义差异面，写入 golden delta
- [ ] AC9（R7）：未迁移的 8 个消费者输出与改造前逐字节一致；其 CLI/flag/help
      快照逐字节一致
- [ ] AC10（R7）：`analyze_logic.py` 章引言覆盖集合的差异逐条列入 golden delta，
      每条可判定为「特殊章不再被查」而非「正文章被漏查」
- [ ] AC11（R8）：`tests/contracts/test_parsers_alignment.py` 全绿，`ALIGNMENTS`
      表未新增 ZH 分歧项
- [ ] AC12（R8）：路由表命令的 `--flag` 与脚本 `--help` 一致
- [ ] AC13（R8）：改 `references/modules/deai.md` 后在本提交内重建
      `docs/resource-manifest.json` + 双语页面，
      `check_resource_sync.py --skill latex-thesis-zh` 通过；SKILL.md 只改
      `last_updated`，`version` 保持 `6.0.0`；新测试位于
      `tests/skills/latex_thesis_zh/`
- [ ] AC14（R8）：`just ci` 全绿；`just doc-build` 成功
- [ ] AC15（R1, R3）：IR 的真实 precision / recall / false-positive rate 标
      **missing evidence**；真实学位论文量级未用作 window 或实现输入

## Constraints

- 不改 `parsers.py` 被哈希锁定的成员；`PRESERVE_PATTERNS` 保持字节不变
- 不改构建配置
- 不修改用户论文
- `[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`
- IR 字段保持最小：按 module 提供投影视图，不让每个消费者拿全量节点
- 不把仓库内既有 `.trellis/` 工具改动与 `.gitignore` 纳入本子任务提交或回滚
- `window` / `min_sample` 在设计阶段锁定，实现不得改用未授权真实论文标定

## Dependencies

无。本子任务是子任务 2-6 的前置。

## 修订记录

- 2026-08-25 审阅返回：TPR-01 R/AC ID；TPR-03 两步选择器且 B1 含成果章；
  TPR-04 锁定阈值公式；TPR-05 兼容面拆分；TPR-06 缩窄 UTF-8 入口并定义失败语义。
