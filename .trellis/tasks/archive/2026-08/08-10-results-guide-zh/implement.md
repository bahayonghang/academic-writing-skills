# Implement — 子任务 1（guide 与文档联动）

> 判据权威 = 父 design；每步验证命令实际运行并记录退出码。commit 统一在本任务
> Phase 3.4 按"guide+experiment.md / docs 联动"拆分执行，实现期间只做检查点。

## Step 0 前置

- [x] 读 `.trellis/spec/academic-writing-skills/method-narrative-contract.md`：确认 M-* 与
      RA-* 分界、guide 互链格式约定；记录对本任务的约束点。
- [x] 读 `tests/contracts/test_defensive_ai_rhetoric_contract.py`：确认对 zh
      `experiment.md` 的锁定方式（散列/字符串/结构），决定 Step 2 联动面。
- [x] 通读 `method-description-guide-zh.md`（四级主张表原文）与
      `method-chapter-guide-zh.md` §五（既有实验口径），列互链点清单。

## Step 1 撰写 guide

- [x] 按父 prd R1 十一小节 + 子 design 落地要点撰写
      `references/writing/results-analysis-guide-zh.md`。
- [x] 证据阶梯节：分工声明 + 四级/五级双向映射表 + 互链（父 design §2）。
- [x] R-*↔RA-* 映射表按父 design §3.3 收录，注明启发式线索定性。
- 验证：`rg -c "次优|等价检验|置信上界|选定集|证据阶梯" academic-writing-skills/latex-thesis-zh/references/writing/results-analysis-guide-zh.md`
  （关键判据词全部非零命中）

## Step 2 更新 experiment.md

- [x] 追加 `--results-analysis` 节（RA-* 三列表 + guide 路由行），位置与格式按子 design。
- [x] B3/B4/B5 与防御性推测契约文本语义不变；现有 contract test 无需改动。
- 验证：`uv run --extra dev python -m pytest tests/contracts/test_defensive_ai_rhetoric_contract.py -q`

## Step 3 spec 无损核对

- [x] 产出父任务 `research/spec-mapping.md`（三列表 + 未收录项说明）。
- [x] 逐条比对 `research/user-spec-results-analysis.md` §1–§10 与 R-* 17 项全部有落点。
- 验证：人工核对完成后在本文件回填勾选。

## Step 4 双语文档联动

- [x] `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`
      重建 manifest；校 guide sourceLocale=zh 与 experiment.md 散列。
- [x] en 页完整译文 + zh 页与源一致；链接目标双语同步重写。
- 验证：`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`；
  `just doc-build`

## Step 5 收口

- [x] `just fix` → `just ci`（退出码 0）。
- [x] prd Acceptance Criteria 逐条回填。
- [x] Phase 3.3：判定是否需更新 `.trellis/spec/academic-writing-skills/`（证据分级双表
      分工若属跨技能约定，进 method-narrative-contract.md 或新增条目）。
- [ ] Phase 3.4：按"guide+experiment.md""docs 联动"拆 commit，scope `latex-thesis-zh`。

## 评审门 G1（归档前）

spec-mapping 无损核对通过 + 四级表映射落位 + resource sync/docs build 绿；通过后向用户
确认 guide 判据冻结，子任务 2 方可启动。

## Check 复核记录（2026-08-10）

- `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`：exit 0，257 条。
- `uv run python docs/scripts/check_resource_sync.py`：exit 0，257 条。
- `uv run --extra dev python -m pytest tests/contracts/ -q`：exit 0，212 passed。
- `just doc-build`：exit 0，VitePress build complete。
- `just ci`：exit 0；Ruff 通过，Pyright 0 errors（72 warnings），1465 passed。
- 实现阶段已运行 `just fix`（182 个文件无变化）；Check 阶段未重复运行，并以
  `just ci` 的格式检查复核。
- Phase 3.3 判定：本次规则为 `latex-thesis-zh` 技能内公开指南；跨技能资源同步与防御性
  推测边界已由现有 spec 覆盖，无需新增 `.trellis/spec/` 条目。
