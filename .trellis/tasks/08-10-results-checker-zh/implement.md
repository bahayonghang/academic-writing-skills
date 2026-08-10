# Implement — 子任务 2（检查器实现与校准）

> 判据权威 = 父 design §3；实现结构 = 子 design。启动前确认子任务 1 guide 判据已冻结。
> commit 统一在 Phase 3.4 按"脚本+测试 / 路由+evals / 标定回写"拆分。

## Step 0 前置

- [ ] 确认子 1 已归档或 guide 判据冻结获用户确认。
- [ ] 读 `method-narrative-contract.md`（M/RA 分界）与
      `test_defensive_ai_rhetoric_contract.py`（RA-CAUSAL 注释措辞不触锁）。
- [ ] 读 testing-and-tooling.md 的 zh 测试加载约定与 evals 工具约定。

## Step 1 区间收集与段落切分

- [ ] 实现双通道收集 + 重叠去重 + `--section` 后缀族过滤（父 design §3.0）。
- [ ] 实现段落三元组切分。
- [ ] 先写去重与后缀族的单测（含"同章实验节 = 全局 result_2"重复 fixture）。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_results_analysis.py -q`

## Step 2 RA-* 判据实现

- [ ] 按父 design §3.1 实现八项 + RA-INTERLEAVE 候选；§3.2 红线逐条落地。
- [ ] RA-CAUSAL 三档、RA-STAGE 语境排除、RA-SHALLOW raw/visible 分探针重点自查。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -q`（含零回归）

## Step 3 边界矩阵测试

- [ ] 六格边界矩阵 fixture + 测试（prd R5 清单）；防误报五形态 fixture。
- [ ] 多文件工程 fixture 验证 `源文件:行号` 定位。
- 验证：同上，全绿后出 G2 命中矩阵报告（贴 PR/任务 notes）。

## Step 4 真实语料标定（R8）

- [ ] `decrypted/` 逐篇只读运行，人工标注，产出 `research/calibration-report.md`。
- [ ] RA-INTERLEAVE / RA-STAGE 裁决；需降级/裁掉时改脚本与测试，并回写 guide
      §阈值与出处（含子 1 RA 映射表如有出入）。
- 验证：裁决后 `uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ tests/contracts/ -q`

## Step 5 路由同步

- [ ] SKILL.md experiment 行 + Reference Map + last_updated（version 不动；不重排其他行）。
- [ ] routing-rules.md 条目 + 歧义速判。
- 验证：`uv run --extra dev python -m pytest tests/contracts/ -q`

## Step 6 evals

- [ ] evals.json + trigger_eval.json 追加（append-only、绑定 Step 3 fixture；Bash python
      写入，`PYTHONIOENCODING=utf-8`）。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ tests/contracts/ -q`

## Step 7 收口

- [ ] `just fix` → `just ci` 退出码 0；prd Acceptance Criteria 回填。
- [ ] Phase 3.3：RA 判据沉淀判定（防误报红线/分档豁免若属可执行契约，进
      `.trellis/spec/academic-writing-skills/`）。
- [ ] Phase 3.4：按"脚本+测试 / 路由+evals / 标定回写"拆 commit，scope `latex-thesis-zh`。
- [ ] 通知父任务做集成收口（父 implement.md 清单）。

## 评审门

- G2（Step 3 后）：命中矩阵报告；误报未清零不得进 Step 5。
- 标定门（Step 4 后）：裁决记录齐备才可收口；效果声明遵守 UNVERIFIED 口径。
