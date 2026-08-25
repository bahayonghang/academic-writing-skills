# 执行计划：共享可见正文 IR 与已复现缺陷修复

## 既有 dirt 冻结清单（TPR-10，2026-08-25 `dev` 工作树）

实现不得把下列路径纳入本子任务的格式化、暂存、回滚或提交。它们属于用户已有
Trellis 改动或本规划产物以外的 dirt：

```
M  .gitignore
M  .trellis/.template-hashes.json
M  .trellis/.version
M  .trellis/config.yaml
M  .trellis/scripts/common/config.py
M  .trellis/scripts/common/git_context.py
M  .trellis/scripts/common/paths.py
M  .trellis/scripts/common/task_store.py
M  .trellis/scripts/common/workflow_phase.py
M  .trellis/scripts/task.py
?? .trellis/reviews/
?? .trellis/scripts/common/spec_inject.py
?? .trellis/scripts/common/spec_match.py
?? .trellis/scripts/common/workflow_selection.py
?? .trellis/tasks/08-25-thesis-zh-mode-contract/
?? .trellis/tasks/08-25-thesis-zh-output-eval/
?? .trellis/tasks/08-25-thesis-zh-quality-closure/
?? .trellis/tasks/08-25-thesis-zh-re-audit-gate/
?? .trellis/tasks/08-25-thesis-zh-rule-governance/
?? .trellis/tasks/08-25-thesis-zh-semantic-artifacts/
```

本子任务规划目录 `.trellis/tasks/08-25-thesis-zh-visible-prose-ir/` 只允许更新
规划文件，不得在实现提交里夹带上述无关路径。

`git status` 出现 `.trellis/` 或 fixture **不能**证明工作树只含本任务改动。

## 格式化、回滚、提交规则（TPR-10）

- 格式化只对当步触及的文件：`uv run ruff format <file> ...`，禁止 `ruff format .`
- 回滚使用显式路径：`git restore --source=HEAD -- <file> ...` 或删除本步新增文件。
  禁止无路径的 `git checkout` / `git restore`
- 提交节奏遵循 `.trellis/workflow.md` Phase 3.4：先列出本会话编辑文件与
  unrecognized dirt，一次性请用户确认后再 `git add <files>`。不在 S1-S7 每步
  自动独立提交。用户未确认前保持未提交

## 执行顺序

严格按 S1 → S7。S1 的基线快照是全部回归的对照，缺它后续无法证明修好了什么。

### S1 — 冻结基线（先做，不改任何生产代码）

- [ ] 建 `research/baseline-snapshots/`，对
      `academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`
      跑 10 个 `extract_visible_text` 消费者（`analyze_conclusion`
      `analyze_experiment` `analyze_literature` `analyze_logic` `blind_review`
      `check_format` `check_spec` `check_style_zh` `deai_batch` `deai_check`），
      stdout 存文件
- [ ] 保存 21 个 `main()` 入口的 `--help` 文本（`PYTHONIOENCODING=utf-8`）。
      本子任务只回归 `deai_check.py` 与 `analyze_logic.py` 的编码；其余 help
      快照供严格不变面对照
- [ ] 建 B1/B2/B3 fixture 于
      `academic-writing-skills/latex-thesis-zh/evals/fixtures/quality-regressions/`：
      B1 必须含符号表、绪论、过程章、方法章、成果章五个 include，且过程章同时含
      过程+框架双信号、方法章不同时含双信号；记录改造前实跑输出（与 design.md
      的 B1-B3 对照）
- [ ] 建 `research/approved-deltas/` 空目录，放入五项差异面的预期说明文件
      （D-V1-INTRO / D-V1-PROC / D-V2-RATE / D-V3-CH / D-DEDUP）

**验证**：`git status --porcelain` 中本步新增仅限
`research/baseline-snapshots/`、`research/approved-deltas/`、
`evals/fixtures/quality-regressions/` 与本任务规划目录。生产脚本零改动。
冻结清单内的既有 dirt 仍在，视为排除项而不是失败。

### S2 — 先写失败测试

- [ ] `tests/skills/latex_thesis_zh/test_visible_prose.py`：节点 kind、
      section_role（含无 mainmatter 默认 body、标题路径冲突 → unverified）、
      source span round-trip、`visible_zh_chars` 分母口径
- [ ] `test_process_chapter.py` 增 V1 case：B1 唯一选中 `process.tex`；去掉双信号
      后无 `--section` 要求显式指定
- [ ] `test_deai_tense_zh.py` 或新 `test_deai_thresholds.py` 增 V2 / V3 case：
      `min_sample-1/min_sample/min_sample+1` 性质测试；`>=2000` 同密度 1/2/4 倍；
      7 次「首先」在 table/math vs 正文
- [ ] `tests/skills/latex_thesis_zh/test_cli_encoding.py`：V4 pipe；另用替身覆盖
      `reconfigure` 不可用 → 修复提示或 `skipped`

**验证**：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -q`
新增 case 全部失败，且失败原因与 design.md 的 B1-B4 一致（不是 import 错误）。

**review gate**：确认失败信息指向真实缺陷，再进 S3。不提交。

### S3 — 实现 `visible_prose.py`

触及文件：`academic-writing-skills/latex-thesis-zh/scripts/visible_prose.py`

- [ ] `ProseNode` dataclass + `ProseIR` 容器（含 `visible_zh_chars`、
      `visible_sentences`、`ir_version`）
- [ ] `build_ir(doc: AssembledDocument) -> ProseIR`：栈式容器扫描
      （table / math / float / list / control / comment）
- [ ] `ProseIR.channel(name)` 投影视图
- [ ] `ensure_utf8_stdio() -> str` helper（返回值见 design.md）
- [ ] 章节角色分类器：四信号 + 无 mainmatter 默认 body + 冲突 unverified
- [ ] 过程章双信号选择函数（供 S5 调用；不在本步改 `analyze_logic.py`）

**验证**：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_visible_prose.py -q`
绿；`uv run ruff format academic-writing-skills/latex-thesis-zh/scripts/visible_prose.py && uv run ruff check academic-writing-skills/latex-thesis-zh/scripts/visible_prose.py`；
`pyright` error 数不增。

### S4 — 迁移 `deai_check.py`

触及文件：

- `academic-writing-skills/latex-thesis-zh/scripts/deai_check.py`
- `academic-writing-skills/latex-thesis-zh/references/deai/tone-thresholds.yaml`

**先读 design.md 的「阈值归一」约束表**：`tests/contracts/test_deai_alignment.py`
锁定 `_iter_visible_lines`（AST 跨三副本）、`_apply_tier`、`term_thresholds`
子表的 11 个 CJK 词值（与 typst 同词同值）。这三项**字节不变**。
`window=10000`、`min_sample=2000` 已锁定，本步不得改常数，不得读取真实论文。

- [ ] 新增私有方法消费 IR 的 `term_threshold` 通道（排除 `table_cell` / `math` /
      `generated` / `control` / `comment` / `caption` / `list_item`）；
      **`_iter_visible_lines()` 保持字节不变**供其余 checker 使用
- [ ] `_check_term_threshold()` 判定式改为 R3 整数式；`visible_zh_chars < 2000`
      时不触发
- [ ] `tone-thresholds.yaml`：新增顶层 `term_threshold_scaling`
      （`unit` / `window: 10000` / `min_sample: 2000` / `compare: ">"`）；
      **`term_thresholds` 子表的 cap 值不动**
- [ ] finding 去重：`rule_id + 归一化 source span + evidence hash`（D-DEDUP）
- [ ] `main()` 首行调 `ensure_utf8_stdio()`
- [ ] 其余 checker（parallel_sentences / burstiness / throat_clearing /
      overclaim / tense / punctuation / sentence_length_variance /
      low_information_density）保持既有阈值与行为不变

**验证**：V2 / V3 / V4 case 转绿；未迁移消费者与 `--tier` 快照仍在严格不变面；
`uv run --extra dev python -m pytest tests/contracts/test_deai_alignment.py -q`
全绿。格式化只跑本步两个文件。

### S5 — 迁移过程章定位

触及文件：`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py`

- [ ] `_process_chapter_range()` 改为 design.md 第二步选择器
- [ ] `:587` 的 `body_chapters` 过滤改为 role 过滤（专章不查章引言）
- [ ] `main()` 首行调 `ensure_utf8_stdio()`

**验证**：V1 case 转绿；符号表章与成果章零主线 finding；`analyze_logic.py`
相对 S1 快照的差异只能落入 D-V1-INTRO 与 D-V1-PROC。格式化只跑该文件。

### S6 — 兼容与文档

触及文件：

- `academic-writing-skills/latex-thesis-zh/references/modules/deai.md`
- `academic-writing-skills/latex-thesis-zh/SKILL.md`（只改 `last_updated`）
- `docs/resource-manifest.json` 与对应双语页面（本提交内重建）

- [ ] 确认 `parsers.py` 零改动（`git diff -- academic-writing-skills/latex-thesis-zh/scripts/parsers.py`）
- [ ] 未迁移的 8 个消费者输出与 S1 快照逐字节 diff
- [ ] 写入 `research/approved-deltas/` 的五项实际 diff 清单
- [ ] `references/modules/deai.md`：说明只处理可见正文节点、归一化分母、
      去重与人工复核边界
- [ ] `SKILL.md`：只改 `last_updated`（`version` 保持 `6.0.0`）
- [ ] 重建 `docs/resource-manifest.json` + 双语页面

**验证**：

```
uv run --extra dev python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
uv run --extra dev python -m pytest tests/contracts/ -q
```

### S7 — 全量校验

- [ ] `just ci` 全绿
- [ ] `just doc-build` 成功
- [ ] `git diff --check`（范围限于本任务文件清单）
- [ ] 逐条核对 `prd.md` 的 AC1-AC15
- [ ] 按 Phase 3.4 列出拟提交文件与冻结清单中的 unrecognized dirt，等待用户确认

## 回滚点

| 阶段 | 回滚方式 |
| --- | --- |
| S1-S2 后 | 删除本步新增测试与 fixture / snapshot 文件 |
| S3 后 | 删除 `visible_prose.py` |
| S4 后 | `git restore --source=HEAD -- academic-writing-skills/latex-thesis-zh/scripts/deai_check.py academic-writing-skills/latex-thesis-zh/references/deai/tone-thresholds.yaml`；IR 文件保留 |
| S5 后 | `git restore --source=HEAD -- academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py` |
| S6 后 | 对 docs 镜像重跑 `check_resource_sync.py --write-manifest --inventory-only`；`git restore` SKILL.md 与 deai.md |

禁止回滚冻结清单中的路径。

## 需要人工确认的判断点

1. **S5 输出差异**：role 过滤会改变章引言检查的覆盖章集合。差异清单须人工确认
   每条都落在 D-V1-INTRO（特殊章不该被查），而不是正文章被漏查。
2. **`ensure_utf8_stdio()` 的 helper 落点**：若 `visible_prose.py` 因此超过
   400 行，拆为 `cli_runtime.py`；优先不新增文件。
3. **Phase 3.4 提交清单**：必须把冻结清单列为 unrecognized，不得默纳入库。

`window` 与 `min_sample` 已在 design.md 锁定，实现阶段不再选择常数。
