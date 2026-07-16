# implement.md — 执行清单（tests-first，批次间设 review gate）

> 快捷命令：
> `CLTEST = uv run --extra dev python -m pytest tests/skills/cover_letter -q`
> `CONTRACTS = uv run --extra dev python -m pytest tests/contracts -q`
> 禁止给 pytest 加 `PYTHONIOENCODING=utf-8`。
>
> **提交纪律（per `.trellis/workflow.md` Phase 3.4）**：Phase 2 各批次**不执行 `git
> commit`**。每批次以 validation gate 收口，登记一条"拟提交分组"：文件集**分列「修改的
> 既有文件」与「本批新建文件」** + 拟 commit message；随后 `git add <本批次全部文件>`
> （新建文件入 index，否则快照捕获不到）再 `git stash create` 记录快照 commit-ish
> （工作区不动）。实际提交统一在 Phase 3.4（所有 gate 通过 + spec 更新之后）按分组顺序执行。
> 回滚一律 **scoped restore，禁用 reset**：既有文件 `git checkout <上一批次快照> --
> <该批修改的既有文件>`；本批新建文件按登记清单**单列显式删除**（`rm <新建文件>`，
> checkout 无法移除新文件）。

## Batch 0 — 基线确认（无代码改动）

- [ ] 确认 `07-15-audit-fix-version-ci` 已合入（`uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py -q` 绿）。
- [ ] 跑 `CLTEST` 与 `CONTRACTS`，记录基线通过数（回滚参照点）。
- [ ] 通读 design.md §0 改动面 + prd.md must-stay-green 清单。

## Batch 1 — claim 抽取与数值验证精度（A-CL-2 / A-CL-3 / A-CL-4）

**Tests first（先写、先跑、确认红）**：

- [ ] `test_cover_letter_align_check.py`：A-CL-2 三用例——tmp `.tex` 信含
  `% Our work demonstrates a 99\% reduction ...` 注释行 → 无对应 claim 候选/finding；
  活行 `47\%` 转义保留；tmp `.md` 信含 `%` 的 claim 抽取不变。
- [ ] `test_cover_letter_scripts.py`：A-CL-3 测试对——"3 seconds" 命中 / "3 sensor
  streams" 双向不命中（`_has_numeric_match` + `_detect_anchors` metric 类型）；
  "47 ms"/"5 GB"/"2.1x" 保持；"3 ppm" 不命中；extract headline_numbers 行为不变。
- [ ] `test_cover_letter_align_check.py`：A-CL-4 正反对——数字与不相干 improvement 相距
  60~160 字符 → False；`("47% reduction", "we report a 47% reduction in latency")` → True。

**实现**：

- [ ] `build_letter_claim_map.py`：新增公开 `strip_tex_comments`（自 align_check 原样迁移）
  + `NUMBER_UNIT_PATTERN` 单源常量；`ANCHOR_PATTERNS["metric"][0]` 与 `main` 的 .tex
  入口接入；`LETTER_CLAIM_PATTERNS` 处补"有意不并入"注释。
- [ ] `align_check.py`：删私有 `_strip_tex_comments` 改 import；`run_align_check` 对
  `.tex` letter 以剥注释文本进 `build_claim_map`（disclosure 入参保持原文）。
- [ ] `verify_letter_against_manuscript.py`：`number_patterns[0]` 改用单源常量；新增
  `_DIRECTION_RE` / `_DIRECTION_WINDOW = 60`，插入 `elif local_direction:` 分支
  （specific 与 keywords 兜底两档不动）；`metric_keywords` 补并集关系注释。
- [ ] `extract_manuscript_facts.py`：`number_patterns[0]` 改用单源常量（import 自 build）。

**验证 / gate**：

- [ ] `CLTEST` 全绿，重点核对 must-stay-green：CL-1 四测试、CL-2 salutation、CL-4 六测试。
- [ ] `uv run --extra dev ruff format --check . && uv run --extra dev ruff check .`；pyright error 数不升。
- [ ] **拟提交分组①**（不 commit，登记 + `git stash create` 快照）：
  文件集 = `build_letter_claim_map.py` / `align_check.py` /
  `verify_letter_against_manuscript.py` / `extract_manuscript_facts.py` +
  `test_cover_letter_align_check.py` / `test_cover_letter_scripts.py`；
  拟 message：`fix(cover-letter): [AI] 🐛 tex注释剥离+数字单位边界+方向词窗口收紧`，
  正文声明默认行为变化（A-CL-2 误报修复 / A-CL-3 误报修复 / A-CL-4 假绿修复）。
- [ ] Review gate：人工过一遍 diff，确认未触碰 parsers.py / tex_loader.py / evals.json。

## Batch 2 — journal_fit 簇（A-CL-1 / A-CL-6 / A-CL-5 / A-CL-10）

**Tests first（新文件 `tests/skills/cover_letter/test_cover_letter_journal_fit.py`，
含 `_load` 惯用法 + 加载守卫 `assert hasattr(module, "TIER_BUDGETS")`）**：

- [ ] A-CL-1：两 fixture 校准（journal_fit_fixture + nature → evidence_density HIGH；
  align_check_fixture + ieee-trans → HIGH）；4 条非 "we report" 句式合成信 ≠ LOW；
  零 claim 信仍 LOW。
- [ ] A-CL-6：fixture 原文 nature → scope_fit LOW（负例）；fixture+一句含 "field" →
  scope_fit HIGH（顶刊 1-hit）；ieee-trans 1-hit → 仍 MEDIUM；含 "broad scientific" 的信
  novelty paradigm 信号不再计入该词。
- [ ] A-CL-5：超长（>420 词）nature 信——`dedup_length=True` → 无长度 LOW/finding 且
  banned-phrase 分支仍触发；默认 False → 与现行为一致。
- [ ] A-CL-10：tmp skill_dir 自定义无 tier 模板 → `warnings` 非空且 tier=mid-journal；
  内置 nature → `warnings == []`。

**实现**：

- [ ] `journal_fit_check.py`：`_count_claims` 复用 `extract_claims`；`_check_scope_fit`
  加 tier 参数 + top-journal 1-hit=HIGH；paradigm_signals 删 `broad scientific`；
  `run_journal_fit(..., dedup_length=False)` + `_check_format_compliance(include_length=...)`
  + evidence 委托说明；`JournalFitResult.warnings` + protocol/JSON 渲染；main 加
  `--dedup-length`。
- [ ] `cover_letter.py`：`build_parser` 加 `--dedup-length`；`_run_journal_fit` 透传
  flag 与 `warnings`。
- [ ] `references/MODE_GUIDE.md`：:95 heuristic 段改述 evidence_density 语义；Mode 2 与
  :123 矩阵补 `--dedup-length` 指引（**先落 parser 再写文档**）。

**验证 / gate**：

- [ ] `CLTEST` 全绿；专项确认既有
  `test_journal_fit_classifies_low_for_underframed_nature`、`test_journal_fit_cli_json_emits_axes`、
  `test_mode_guide_flags_all_exist_in_cli`、`test_unified_cover_letter_cli_json_smoke_all_modes` 绿。
- [ ] **拟提交分组②**（不 commit，登记 + 快照）：
  文件集 = `journal_fit_check.py` / `cover_letter.py` / `references/MODE_GUIDE.md` +
  `test_cover_letter_journal_fit.py`；
  拟 message：`fix(cover-letter): [AI] 🐛 journal-fit claim计数/顶刊scope校准/长度dedup/缺tier警告`，
  正文声明默认行为变化（A-CL-1、A-CL-6 误报修复例外；A-CL-5 藏于 flag 无默认变化）。
- [ ] Review gate。

## Batch 3 — 小修与文档（A-CL-8 / A-CL-9 / A-CL-11）

**Tests first**：

- [ ] A-CL-8：`_exit_code` 混类型（dict + dataclass、severity 空串）不抛异常，
  major→2 / 非空→1 / 空→0。
- [ ] A-CL-9：合成信（`Dear Editor,` + 首段含 claim + 中间段含 claim + `Sincerely,` 落款）
  → 首段 claim 的 `source_section == "opening"`、中间段 claim == `"body"`；issue JSON 与
  claim_map candidate 均含 `char_offset` 且 ≥ 0；`source_section` 恒属扩展后 ISSUE_SCHEMA
  枚举（含 `body`）；`candidate_to_issue` 无 letter_text 直调（既有用法）回退 `body` 不抛。
- [ ] A-CL-11 表征：acmart `\authornote{Corresponding author: x@y.edu}` →
  corresponding = 第一作者、不含 `@`。

**实现**：

- [ ] `cover_letter.py`：`_severity(finding)` 显式类型分支。
- [ ] `build_letter_claim_map.py`：`_locate_sentence`（宽松空白正则 + moving cursor）；
  `build_claim_map` 给 candidate 写 `char_offset`（additive，定位失败 -1）。
- [ ] `align_check.py`：`_VALEDICTION_RE` + `_source_section_for_offset`（header/opening/
  closing/body，见 design §8）；`candidate_to_issue(..., letter_text=None)` 接入；
  `AlignCheckIssue` 末尾追加 `char_offset: int = -1`；`run_align_check` 传入与
  build_claim_map 同一份文本（.tex 为剥注释文本）。
- [ ] `references/ISSUE_SCHEMA.md`：`source_section` 枚举增 `body`；Optional fields 增
  `char_offset`。
- [ ] `extract_manuscript_facts.py`：`CORRESPONDING_AUTHOR_PATTERNS` 注释补缺口说明并
  引用 :42-46 反捏造理由；`references/CLAIM_EVIDENCE_CONTRACT.md` 增 known gaps 两行。

**验证 / gate**：

- [ ] `CLTEST` 全绿；`CONTRACTS` 全绿（references 有改动）。
- [ ] **拟提交分组③**（不 commit，登记 + 快照）：
  文件集 = `cover_letter.py` / `align_check.py` / `build_letter_claim_map.py` /
  `extract_manuscript_facts.py` / `references/ISSUE_SCHEMA.md` /
  `references/CLAIM_EVIDENCE_CONTRACT.md` + `test_cover_letter_scripts.py` /
  `test_cover_letter_align_check.py`；
  拟 message：`fix(cover-letter): [AI] 🐛 exit-code类型分支+source_section位置映射+通讯作者缺口注记`。
- [ ] 阶段性全量：`just ci` 应全绿（若 A-CL-7 长期 blocked，分组①~③即本任务可交付面）。

## Batch 4 —（**BLOCKED on A-EN-10**）删 `_extract_title_local` fork（A-CL-7）

> 入口条件不满足则整批搁置，不得提前动 extract_manuscript_facts 的 title 路径；
> 若父任务排期上 EN 任务长期未落地，在 task notes 标注 blocked 并移交父任务集成阶段。

- [ ] 入口检查 1：`git log --oneline -3 -- academic-writing-skills/cover-letter/scripts/parsers.py`
  确认三副本重同步 commit 已达。
- [ ] 入口检查 2：`uv run --extra dev python -m pytest tests/contracts/test_parsers_alignment.py -q` 绿。
- [ ] 探针：canonical `extract_title` 对 `thanks_author_fixture.tex` 是否剥 `\thanks`
  （design §7 判据）。
- [ ] 分支 A（已剥）：整删 `_extract_title_local`，`extract_facts` 改调
  `parsers.extract_title`，清理因此闲置的 import。
- [ ] 分支 B（未剥——按 EN design §4 的 R10 用例不应发生）：视为 A-EN-10 未按前置契约落地，
  **回到 EN 任务补齐 `\thanks`/footnote 剥离后重走分支 A**；本任务不得以缩薄 fork 收尾归档
  （终批集成任务禁改行为代码，无人可承接遗留）。
- [ ] 验证：`test_extract_title_strips_thanks_and_keeps_nested_braces`、
  `test_extract_manuscript_facts_returns_expected_shape` 绿；`CLTEST` + `CONTRACTS` 全绿。
- [ ] **拟提交分组④**（不 commit，登记 + 快照）：
  文件集 = `extract_manuscript_facts.py` + 相关测试；
  拟 message：`refactor(cover-letter): [AI] ♻️ 删除_extract_title_local fork（A-EN-10落地后）`。

## 收尾（Phase 3）

- [ ] 全量 `just ci` 绿（pyright 看 error 数）。
- [ ] 对照 prd.md 验收清单逐项勾选；must-stay-green 清单逐条确认。
- [ ] Phase 3.3：如有值得沉淀的教训走 `trellis-update-spec`（spec 改动并入对应拟提交分组
  或单列一组）。
- [ ] **Phase 3.4 提交**：所有 gate + spec 更新完成后，按分组①→②→③→④
  顺序执行 `git add <文件集>` + `git commit`（④为必做——A-CL-7 完成后本任务才可归档，
  见 prd 验收）；默认行为变化声明写入对应 commit 正文；不 amend、不 push。
- [ ] task notes 记录：A-CL-7 完成证据（探针结果 + 分支 A/B 走向）、各拟提交分组的最终 commit 哈希。

## 回滚点速查（Phase 2 无 commit；scoped restore，禁用 reset）

| 批次 | 拟提交分组 | 回滚方式 |
|------|-----------|----------|
| 1 | ①注释/单位/方向词 | 既有文件 `git checkout <Batch0基线> -- <分组①修改文件>` + `rm <分组①新建测试文件>`（单源常量一处还原即三处还原） |
| 2 | ②journal-fit 簇 | 既有文件 `git checkout <分组①快照> -- <分组②修改文件>` + `rm <分组②新建文件>`（MODE_GUIDE 文档行随之还原） |
| 3 | ③小修/位置映射/文档 | 既有文件 `git checkout <分组②快照> -- <分组③修改文件>` + `rm <分组③新建文件>`（共享文件 align_check.py/cover_letter.py 以快照为基准，不误伤批次 1/2 成果） |
| 4 | ④fork 删除 | 既有文件 `git checkout <分组③快照> -- <分组④修改文件>` + `rm <分组④新建文件>`（独立分组，不影响 1-3） |

> 快照 = 各批次 gate 通过时先 `git add <本批次全部文件（含新建）>` 再 `git stash create`
> 返回的 commit-ish（记入 task notes）；新建文件必须先 add 才会被快照捕获，回滚时 checkout
> 只还原既有文件，新建文件按各分组登记的清单显式 `rm`。Batch 0 基线即当时的 `HEAD`。
