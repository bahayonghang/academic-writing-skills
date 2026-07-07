# deai_check 三副本对齐锁测试

## Goal

为 en/zh/typst 三份 `deai_check.py` 副本建立与 `tests/test_parsers_alignment.py` 等价的对齐锁，把"共享逻辑必须同步、分歧必须显式登记"的契约扩展到 deai 系脚本，防止 XA-1 类漂移再次发生。

证据详情：`../07-05-skills-deep-analysis-optimization/research/crosscut-findings.md`（XC-3 / XC-3b）

## 问题清单

- **XC-3 [medium]** deai_check.py 三副本存在事实共享逻辑（`_apply_tier` 的 EN 与 typst 版本字节完全相同）却无对齐锁；时态/over-claim/结构壳逻辑镜像进 zh/typst 后从不被专项测试触达。这正是 test_parsers_alignment.py 当初要防的漂移形态，但 deai_check 没有等价保护。
- **XC-3b [low]** bare `import deai_check` 永远解析到 sys.path 前排的 EN 副本，是 zh/typst 测试的静默陷阱。

### 上锁前需判定的已知分歧（来自 P0 两任务的质检，2026-07-06）

- `burstiness.opening_token_count`：EN=2（en/scripts/deai_check.py:598 附近） vs typst=8（typst/scripts/deai_check.py:719 附近），用法逻辑相同仅默认值不同，疑似 typst 为 CJK 双语有意放宽。上锁时判定：有意 → 登记为分歧条目并写明理由；无意 → 先对齐再锁。
- `presents` 时态信号（SH-1）：en/typst/zh 三侧均已改为 `\bpresents\b`（zh 侧在 07-05-zh-abstract-tense-gating 质检后补齐），上锁时验证三副本一致。
- typst 特有 `_typst_ref_kw_re`（@fig 交叉引用改写护栏）与 zh 特有 `_english_abstract_range` 系（模板摘要环境门控）为语法/语种驱动的有意分歧，应登记而非对齐。

## Requirements

- R1 新建（或扩展）对齐测试：锁定三副本中"应当一致"的函数/常量（如 `_apply_tier`、共享 term 表、tier 阈值结构），以 latex-paper-en 为 canonical。
- R2 有意分歧（zh 的 ChineseAITraceChecker 中文特有逻辑、typst 语法差异）显式登记在 ALIGNMENTS 式映射中并注明理由，沿用 test_parsers_alignment.py 的模式。
- R3 测试内部**必须用 importlib 按路径分别加载**三副本，杜绝 bare import（XC-3b）。
- R4 锁上后人为制造一处漂移验证测试确实会红（验证后还原）。

## Acceptance Criteria

- [ ] 对齐测试覆盖三副本的共享面，`just ci` 全绿。
- [ ] 人为改动 typst 副本共享函数一处 → 对齐测试变红（本地验证，不提交）。
- [ ] 有意分歧清单有注释说明，格式与 test_parsers_alignment.py 一致。

## Notes

- **顺序依赖：必须在 `07-05-zh-abstract-tense-gating` 与 `07-05-typst-deai-sync` 完成后执行**——先把副本修齐，再上锁，否则锁住的是漂移状态。
- 参考 canonical 模式：`tests/test_parsers_alignment.py` 的 ALIGNMENTS 哈希锁。
