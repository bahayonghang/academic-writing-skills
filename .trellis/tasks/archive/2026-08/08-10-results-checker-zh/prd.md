# latex-thesis-zh 结果分析检查器 RA-* 实现与校准（子任务 2）

## Goal

在 `analyze_experiment.py` 实现 `--results-analysis` 检查族 RA-*（全部为启发式线索），
配套 fixtures / 边界矩阵测试、SKILL.md 与 routing-rules 路由、evals 追加、真实语料标定。
实现依据 = 父 `08-09-results-analysis-zh/design.md` §3（区间收集算法、段落三元组、
RA_METRIC_TERM_RE、九项判据与十条防误报红线，不复述）。

## 依赖（启动条件）

子任务 1 `08-10-results-guide-zh` 的 guide 判据冻结（归档或用户确认不再变更）后启动：
RA-* 表述、evals 用例与 routing 文案需与 guide 行文对齐；子 2 完成后若脚本行为与 guide
RA 映射表有出入，由本任务回改 guide 文档并提交。

## Requirements（认领父 prd R2 / R4 / R5 / R6 / R8）

### R2 检查器

- `--results-analysis` 旗标 + 双通道区间收集（逐章 EXP_SEC_RE ∪ 全局
  `^(discussion|result)(_\d+)?$` 后缀族）+ `(start,end)` 重叠去重 + `--section` 后缀族
  语义（父 design §3.0）。
- RA-EQUIV / RA-CAUSAL（三档）/ RA-SECONDBEST / RA-SHALLOW / RA-DISTVOCAB /
  RA-UNIVERSAL / RA-STAGE（规范性语境排除）/ RA-TRANSITION；RA-INTERLEAVE 按候选实现。
- 消息模板统一 `[Script] RA-XXX（启发式线索，须 LLM 按证据阶梯复核）：...`；
  RA-CAUSAL 处写 defensive-ai-rhetoric 分界注释。
- 默认模式与 `--per-chapter` 输出零变化。

### R4 路由同步

SKILL.md experiment 行 Use-when + Primary command 补旗标说明、Reference Map 增 guide 行、
last_updated 更新（version 不动）；routing-rules.md experiment 条目 + 歧义速判一条
（结果分析深度 vs over-claim-guard vs deai）。注意 ROUTER_ROW_RE 契约锁与表格格式化
hook 陷阱（不重排其他行）。

### R5 测试（含边界矩阵）

- 逐 RA-* 一正一反 fixture。
- 边界矩阵（审阅 P2-6）：重复区间去重（同章"结果分析"节同时是全局 result_2）；
  `--results-analysis` 与 `--section`/`--per-chapter` 组合语义；多文件工程行号定位
  （lineref 源文件:行号）；合法阶段对比句（规范性语境不误报 RA-STAGE）；无关消融
  （模块 A 有消融、模块 B 被归因 → RA-CAUSAL 降档 Minor 而非静默/Major）；局部比较
  误判（"局部最优/该子集最优"不触发 RA-UNIVERSAL）。
- 防误报五形态对齐 defensive-ai-rhetoric 契约惯例；现有 E-*/B3/B4/B5 零回归断言。

### R6 evals

`evals/evals.json` + `trigger_eval.json` 追加：append-only、ID 唯一、绑定 R5 真实
fixture；Bash python 写入（JSON hook 陷阱）；Windows 重定向加 `PYTHONIOENCODING=utf-8`。

### R8 真实语料标定

`decrypted/` 本地参考论文只读运行 `--results-analysis`，逐命中人工判定真/误报，产出
标定报告（存本任务 research/）；RA-INTERLEAVE 与 RA-STAGE 按报告裁决去留/降级，裁决
回写 guide §阈值与出处。查准/召回一律标 UNVERIFIED / missing evidence（父 design §7）。

## Acceptance Criteria

- [x] RA-* 正/反例与边界矩阵测试全绿；现有测试零回归。
- [x] 重复区间只报一次；`--section` 后缀族语义有测试锁定。
- [x] RA-CAUSAL 三档行为有测试证明（段级豁免 / 章级降档 / 无证据 Major）。
- [x] RA-STAGE 规范性语境排除有正反 fixture（含 spec 合规声明句不误报）。
- [x] SKILL.md / routing-rules.md / evals 同步完成，contracts 测试全绿。
- [x] 标定报告存在，RA-INTERLEAVE/RA-STAGE 去留有明确裁决记录。
- [x] `just ci` 全绿。

## Verification Evidence（2026-08-10）

- Focused RA：`32 passed`；覆盖 result/discussion `_N` 后缀族、精确 `--section`、重叠
  去重、RA-CAUSAL 三档与对象绑定提示、RA-STAGE 同物理行两句身份、十条防误报红线、
  多文件 `源文件:行号`、默认/逐章回归和组合旗标。
- 宽门：`tests/skills/latex_thesis_zh/ tests/contracts/` 为 `720 passed`。
- CI：`just ci` 版本锁、Ruff、Pyright 与 pytest 全绿；pytest `1497 passed`，Pyright
  `0 errors`。仓库既有 warning 不作为本任务效果证据。
- 文档：单技能与全量 resource sync 均通过（257 manifest entries）；`just doc-build`
  通过。公开脚本、SKILL、routing、guide 及英中资源均无已裁掉检查项名称。
- 元数据：SKILL `version` 保持 `6.0.0`，仅将 `last_updated` 从 `2026-08-09` 更新为
  `2026-08-10`；eval id 30 与 trigger query 均为数组尾部追加，防御性契约继续显式锁定
  latex-thesis-zh eval id 29。
- 标定证据：`research/calibration-report.md` 明确区分 PDF-TXT proxy 与 synthetic
  contract evidence；真实 LaTeX 工程查准率/召回率仍为 **UNVERIFIED / missing evidence**。
