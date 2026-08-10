# latex-thesis-zh 实验结果分析深度审查能力（父任务）

## Goal

解决用户写实验分析时的三个痛点：结果表格没有深入分析（缺次优比较、排序反转、判据
绑定）、对比图没有深入分析（缺轨迹/散点/箱线各自的分析要点）、缺少结合理论部分的分析
（缺证据分级与结构机制映射）。

本任务为父任务：持有需求集、总体设计蓝图、子任务映射与跨子验收，不承担直接实现。

## 权威链（2026-08-10 审阅后收敛）

1. **产品需求权威** = `research/user-spec-results-analysis.md`（用户 spec 原文）。
2. **实施蓝图** = 父 `design.md`（判据、算法、契约边界的实现依据；子任务不复述只引用）。
3. **运行时 LLM 判据权威** = `references/writing/results-analysis-guide-zh.md`（子任务 1
   交付后生效；此后 guide 与 design 冲突时以 guide 为准并回写 design 变更记录）。
4. **脚本层定位** = RA-* 全部为**启发式候选线索**（heuristic cue），输出注明须 LLM 复核，
   不宣称覆盖 R-* 清单。

## 子任务映射

| 子任务 | 交付物 | 依赖 |
| --- | --- | --- |
| `08-10-results-guide-zh` | 新 guide + experiment.md 文档更新 + spec-mapping 无损核对 + 双语文档联动 | 无 |
| `08-10-results-checker-zh` | `--results-analysis` RA-* 检查器 + fixtures/边界矩阵测试 + SKILL.md/routing-rules 路由 + evals + 真实语料标定 | 子 1 的 guide 判据冻结后启动（依赖已写入其 prd） |

## 需求集（子任务按编号认领）

- **R1 新参考 guide**（子 1）：泛化用户 spec §1–§10 为 `results-analysis-guide-zh.md`，
  十一小节结构见父 design §2；域名词降示例；证据阶梯五级须与已落地的
  `method-description-guide-zh.md` §六四级主张证据表做分工声明 + 映射表 + 互链（方法章
  陈述收益用四级表，结果章解释差异用五级阶梯），不复述。
- **R2 检查器**（子 2）：`analyze_experiment.py` 新增 `--results-analysis`，RA-* 判据以父
  design §3 为实现依据；区间收集必须处理 `result_N` 后缀族与逐章区间去重。
- **R3 experiment.md 更新**（子 1）：RA-* 表 + guide 路由；防御性推测契约文本语义不变。
- **R4 路由同步**（子 2）：SKILL.md experiment 行 + routing-rules.md + 歧义速判；version
  不动，last_updated 由后归档的子任务统一改。
- **R5 测试**（子 2）：逐 RA-* 一正一反 + 边界矩阵（重复区间、旗标组合、多文件行号、
  合法阶段对比、无关消融豁免粒度、局部比较误判）+ 现有行为零回归。
- **R6 evals**（子 2）：append-only、ID 唯一、绑定真实 fixture；Bash python 写入。
- **R7 双语文档**（子 1）：manifest + en/zh 页面 + resource sync + docs build。
- **R8 真实语料标定**（子 2）：用 `decrypted/` 本地参考论文只读运行检查器，产出命中/误报
  标定报告；查准率、召回率按仓库口径标 **UNVERIFIED / missing evidence**，合成 fixture
  结果不得表述为真实效果。

## 已收敛决策（不再 open）

1. flag 名定为 `--results-analysis`（与 `--method-narrative` 命名节奏一致）。
2. RA-INTERLEAVE 候选已在子 2 标定后裁掉：4/4 次 PDF-TXT proxy 命中均由分页、表格行或
   段落边界丢失造成。最终运行时检查族固定为其余八项；裁决保留在归档标定报告与 guide
   §阈值与出处中，不对外推断真实论文效果。
3. 任务结构采用父 + 双子（2026-08-10 Codex 审阅建议选项 1；与已归档
   method-description-upgrade 树同构）。
4. 提交策略：实现期间每步只形成可回滚检查点，git commit 统一在各子任务 Phase 3.4 按
   子系统拆分执行。

## Non-Goals

- 不移植到 latex-paper-en / typst-paper / paper-audit（后续任务）。
- 不改 `deai_check.py`（defensive-ai-rhetoric 契约禁止 hedge 正则）。
- 不改 B3/B4/B5、E-*、M-* 现有行为；method-desc 已归档成果只互链不修改。
- 不实现"正文百分比 vs 表内数值自动复核"（LLM 检查项）。
- 不 bump SKILL.md version。
- 用户 spec 中院校/工艺特定内容不进 guide 规则正文，只作示例。

## 跨子验收标准（父级收口）

- [x] 两子任务各自验收全过且归档。
- [x] guide 的 RA-* 映射表与脚本实际行为一致（子 2 完成后回核子 1 文档）。
- [x] SKILL.md / routing-rules.md / experiment.md 三处路由口径一致。
- [x] `just ci` 全绿；`check_resource_sync.py --skill latex-thesis-zh` 与 docs build 通过。
- [x] 真实语料标定报告存在，效果声明遵守 UNVERIFIED 口径。
- [x] R-* 17 项全部落位（RA 线索或 LLM 检查项），`research/spec-mapping.md` 无损核对通过。

## 审阅记录

2026-08-10 Codex 只读审阅 8 项发现全部核实成立，修复已并入父 design 与子任务 prd：
P1 基线过时（method-description-guide 已落地）、P1 区间重复/漏检（parsers.py `_N` 后缀）、
P1 RA-STAGE 误报合规句、P1 RA-CAUSAL 章级豁免假阴性、P1 RA-SHALLOW visible/raw 矛盾与
指标词表缺口、P2 验收边界不足、P2 外部研究缺 URL、P2 规划门未收敛。
