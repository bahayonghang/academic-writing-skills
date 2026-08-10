# C1 执行计划

前置：读父 research/ 三文件（spec 原文核对源、机制事实、引用来源）+ 通读 `analyze_logic.py`
与 `test_body_chapters.py`。判据一律以父 design §2 为准。实施代理不执行 git commit（分组建议
仅供 Phase 3.4）。

## 步骤

### 1. 测试先行（红）

- [x] 新建 `tests/skills/latex_thesis_zh/test_method_narrative.py`（design §3：三 fixture +
      五组断言，含门控三态与长章名定位）。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_method_narrative.py`
  预期失败（开关不存在）。

### 2. 检查器实现（绿）

- [x] `analyze_logic.py`：`--method-narrative` + 显式 `--section` 选章 + 候选章清单非零退出 +
      M-* 三函数（MN_ 常量组）+ M-EDGETABLE 骨架（design §1）。
- [x] 无开关路径行为与现状一致（现有测试全量回归）。
- 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/` 全绿。
- 审查门：diff 审查（无开关零改动、visible text 通道、MN_ 常量注释出处、退出码 2）。

### 3. 参考文件

- [x] 新建 `references/writing/method-description-guide-zh.md`（prd R1 十项）。
- [x] 对照父 research/user-spec-method-description.md 核对 §9/§10 无损转写；确认无本地论文名。
- [x] `references/modules/logic.md` 增 M-* 说明段。

### 4. 工作流接线

- [x] SKILL.md：Reference Map 加行；logic 路由行展示 `--method-narrative --section 〈章名〉`；
      `last_updated` 更新，version 不动。
- 验证：`uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py
  tests/contracts/test_skill_versions.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py`。

### 5. manifest 与双语文档（方向：中文源）

- [x] `uv run python docs/scripts/check_resource_sync.py --write-manifest`（新文件入 manifest，
      核对 sourceLocale=zh）。
- [x] `docs/zh/skills/latex-thesis-zh/resources/references/writing/method-description-guide-zh.md`
      —— 与中文源一致（仅链接目标可重写）。
- [x] `docs/skills/latex-thesis-zh/resources/references/writing/method-description-guide-zh.md`
      —— **完整英文译文**（保留标题层级/代码块/表格形状/inline code token，双语链接目标一致）。
- [x] `references/modules/logic.md` 变更同步其既有双语页对。
- [x] `docs/skills/latex-thesis-zh/index.md` 与 `docs/zh/skills/latex-thesis-zh/index.md` 加行。
- 验证：`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh` +
  `uv run --extra dev python -m pytest tests/contracts/test_docs_bilingual_resources.py`。

### 6. 全量收口

- [x] `just ci` 全绿；prd Acceptance Criteria 逐项勾选。
- [x] 交接物（给 C2/C3）：MN_ 常量清单与函数签名记入父任务 `research/c1-handoff.md`。
- [x] trellis-check 全范围检查 → 进入 3.3 spec 更新、3.4 提交（分组建议见 design §4）。

## 提交分组建议（仅 Phase 3.4 使用）

- A 组：步骤 1-2（检查器 + 测试）。
- B 组：步骤 3-5（参考文件 + 接线 + manifest + 双语页）。
