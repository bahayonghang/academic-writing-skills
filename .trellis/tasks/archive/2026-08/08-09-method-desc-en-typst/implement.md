# C2 执行计划

前置：读父 research/ 三文件；通读 EN/typst `analyze_logic.py` 门控与 TRANSITIONS 区段；
取 C1 journal 的 MN_ 常量交接清单（若 C1 未完成，以父 design §2 直接实现，契约测试 zh 断言
xfail）。实施代理不执行 git commit。

## 步骤

### 1. TRANSITIONS sequence 类 + 回归锁

- [x] EN/typst 两副本增 `sequence` 类（词组=父 design §2.2）。
- [x] 现有 fixture 回归断言：补类后 finding 集合不增。
- 验证：EN/typst 现有 analyze_logic 测试全绿。

### 2. 测试先行（红）

- [x] EN/typst 各新增 M-* 用例（design §5：病例 / 合规 / 无节参数 / 两条红线负例 /
      "Proposed Method" 节名定位 / typst labeled-only 锁定）。
- 验证：pytest 预期失败。

### 3. 检查器实现（绿）

- [x] EN `--section methods` 分支挂四项（design §1）；typst 同构镜像。
- [x] 人工 diff 两副本新增区段确认同构；确认现有 `if not section` 门控零改动。
- 验证：两侧测试全绿 + `tests/contracts/test_writing_modules_alignment.py` 通过。
- 审查门：diff 审查（互斥门控未破坏、MN_ 常量单一来源、无第二套顺序词表）。

### 4. 跨技能契约测试

- [x] 新建 `tests/contracts/test_method_narrative_alignment.py`（design §4；zh 侧按 C1 状态
      决定 live/xfail）。
- 验证：`uv run --extra dev python -m pytest tests/contracts/test_method_narrative_alignment.py`。

### 5. 参考文件

- [x] EN method.md 扩展四节 + 逐边表（design §2）。
- [x] 新建 typst `references/METHOD_SECTION.md`（design §3，authoritative 小写路径）。

### 6. 工作流接线与文档同步（方向：英文源）

- [x] 两个 SKILL.md：Reference Map 加行、`last_updated` 更新、version 不动。
- [x] `check_resource_sync.py --write-manifest`；docs/ 英文页与源一致 + docs/zh 完整中文译文
      （method.md 更新既有页对；METHOD_SECTION.md 新建页对）；两对 index.md 加行。
- 验证：`check_resource_sync.py --skill latex-paper-en` 与 `--skill typst-paper`；
  `uv run --extra dev python -m pytest tests/contracts/`。

### 7. 全量收口

- [x] `just ci` 全绿；prd Acceptance Criteria 逐项勾选。
- [x] 交接物（给 C3）：双调用所需的调用形态与输出合同记入父任务 `research/c2-handoff.md`。
- [x] trellis-check → 3.3 spec 更新 → 3.4 提交（分组建议见 design §6）。

## 提交分组建议（仅 Phase 3.4 使用）

- A 组：步骤 1-4（脚本 + 测试 + 契约测试）。
- B 组：步骤 5-6（参考 + 接线 + manifest + 双语页）。
