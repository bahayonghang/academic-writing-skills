# Implement — 子任务 2（检查器实现与校准）

> 判据权威 = 父 design §3；实现结构 = 子 design。启动前确认子任务 1 guide 判据已冻结。
> commit 统一在 Phase 3.4 按"脚本+测试 / 路由+evals / 标定回写"拆分。

## Step 0 前置

- [x] 确认子 1 已归档或 guide 判据冻结获用户确认。
- [x] 读 `method-narrative-contract.md`（M/RA 分界）与
      `test_defensive_ai_rhetoric_contract.py`（RA-CAUSAL 注释措辞不触锁）。
- [x] 读 testing-and-tooling.md 的 zh 测试加载约定与 evals 工具约定。

## Step 1 区间收集与段落切分

- [x] 实现双通道收集 + 重叠去重 + `--section` 后缀族过滤（父 design §3.0）。
- [x] 实现段落三元组切分。
- [x] 先写去重与后缀族的单测（含"同章实验节 = 全局 result_2"重复 fixture）。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_results_analysis.py -q`

## Step 2 RA-* 判据实现

- [x] 按父 design §3.1 实现八项；RA-INTERLEAVE 先按候选实现，后由 Step 4 标定裁掉；
      §3.2 红线逐条落地。
- [x] RA-CAUSAL 三档、RA-STAGE 语境排除、RA-SHALLOW raw/visible 分探针重点自查。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -q`（含零回归）

## Step 3 边界矩阵测试

- [x] 六格边界矩阵 fixture + 测试（prd R5 清单）；防误报五形态 fixture。
- [x] 多文件工程 fixture 验证 `源文件:行号` 定位。
- 验证：同上，全绿后出 G2 命中矩阵报告（贴 PR/任务 notes）。

## Step 4 真实语料标定（R8）

- [x] `decrypted/` 逐篇只读运行，人工标注，产出 `research/calibration-report.md`。
- [x] RA-INTERLEAVE / RA-STAGE 裁决；RA-INTERLEAVE 因 4/4 proxy 命中均为误报而删除，
      RA-STAGE 保留 Info/P3；同步修改脚本与测试，并回写 guide
      §阈值与出处（含子 1 RA 映射表如有出入）。
- 验证：裁决后 `uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ tests/contracts/ -q`

## Step 5 路由同步

- [x] SKILL.md experiment 行 + Reference Map + last_updated（version 不动；不重排其他行）。
- [x] routing-rules.md 条目 + 歧义速判。
- 验证：`uv run --extra dev python -m pytest tests/contracts/ -q`

## Step 6 evals

- [x] evals.json + trigger_eval.json 追加（append-only、绑定 Step 3 fixture；Bash python
      写入，`PYTHONIOENCODING=utf-8`）。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ tests/contracts/ -q`

## Step 7 收口

- [x] `just fix` → `just ci` 退出码 0；prd Acceptance Criteria 回填。
- [x] Phase 3.3：RA 判据沉淀判定（防误报红线/分档豁免若属可执行契约，进
      `.trellis/spec/academic-writing-skills/`）。
- [x] Phase 3.4：按最终原子边界合并为单一 `feat(latex-thesis-zh)` commit，
      产品提交 `937327f`。
- [x] 已通知父任务进入跨子集成收口（父 implement.md 清单）。

## 评审门

- [x] G2（Step 3 后）：命中矩阵报告通过；focused RA `32 passed`，防误报边界全绿。
- [x] 标定门（Step 4 后）：裁决记录齐备；效果声明保持 UNVERIFIED / missing evidence。

## 完成证据（2026-08-10）

- Focused RA：`32 passed`；zh skill + contracts：`720 passed`。
- `just ci`：Ruff 通过，Pyright `0 errors`（72 个仓库既有 warnings），pytest
  `1497 passed`。
- 单技能与全量 resource sync 通过（257 entries）；`just doc-build` 通过。
- `results-analysis-checker-contract.md` 已沉淀 CLI、区间 payload、证据窗口、错误矩阵和
  测试断言；真实语料效果仍为 UNVERIFIED / missing evidence。
