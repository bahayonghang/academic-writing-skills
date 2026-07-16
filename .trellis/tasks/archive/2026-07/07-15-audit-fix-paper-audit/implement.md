# Implement — 07-15-audit-fix-paper-audit

执行顺序：W1 → W2 → W3，每批 tests-first，批末过 review gate 才进下一批。全程不动 SKILL.md `version`/`last_updated`；不增删 `references/`、`agents/` 文件。**Phase 2 各批末只做「拟提交分组」（记录文件集 + 拟用 commit message），实际 `git commit` 统一在 Phase 3.4（全部 gate + spec update 之后，per `.trellis/workflow.md`）；批内回滚用 `git checkout/stash` 按分组文件集撤销。**

## 批次 0 — 基线确认

- [ ] 确认位于 dev 分支且前置任务 07-15-audit-fix-version-ci 已合入（`tests/contracts/test_skill_versions.py` 绿）；记录 `git rev-parse HEAD` 作 scoped restore 基准。**不执行 `git switch`/`git pull`/`git reset`——工作树可能存在其他任务的无关改动。**
- [ ] 基线：`uv run --extra dev python -m pytest tests/skills/paper_audit -q`（记录通过数，作为回归基准）。
- [ ] 定位存量锁：`grep -rn "reproducibility_partial\|sanitize_issue\|CRITICAL\|4 specialized" tests/ academic-writing-skills/paper-audit/` 存档到任务 notes（防止改动踩现有断言）。

## 批次 W1 — severity/schema（A-PA-1 / A-PA-2）

### W1-a 测试先行

- [ ] 在 `tests/skills/paper_audit/test_paper_audit_deep_review.py` 新增（先红）：
  - `test_sanitize_issue_normalizes_critical_to_major_gate_blocker`：`"CRITICAL"/"Critical"/" critical "` → `major` + `gate_blocker=True`；含显式 `gate_blocker: False` 被覆盖的断言。
  - `test_sanitize_issue_severity_case_insensitive`：`"Major"/"MODERATE"/" Minor "` 归一小写。
  - `test_sanitize_issue_maps_observation_to_minor`。
  - `test_sanitize_issue_field_aliases`：`description`-only → explanation 回落；`location`-only → source_section 回落且 `quote == ""`（不伪造）。
  - `test_load_comment_files_end_to_end_critical_fixture`：tmp_path 写含 `"severity": "CRITICAL"` 的 comments JSON → consolidate 后排最前 + gate_blocker true。
- [ ] 运行确认新用例红、存量绿：`uv run --extra dev python -m pytest tests/skills/paper_audit/test_paper_audit_deep_review.py -q`

### W1-b 实现

- [ ] `scripts/consolidate_review_findings.py`：按 design C1/C2 修改 `sanitize_issue`（`_SEVERITY_ALIASES`、strip+lower、critical 强制 gate_blocker、description/location 别名回落）。
- [ ] `agents/critical_reviewer_agent.md`：severity 表（:115-122）三级化 + gate_blocker 注释；输出示例（:177-227）canonical 字段（title/quote/explanation/severity 小写/source_section/comment_type/source_kind）。
- [ ] `agents/domain_reviewer_agent.md:110`、`agents/methodology_reviewer_agent.md:116`、`agents/literature_reviewer_agent.md:83`：`"Major"` → `"major"` + ISSUE_SCHEMA 转换注记。
- [ ] `references/editorial_decision_standards.md:147-148`：CRITICAL → `major + gate_blocker=true` 语义改写（只动此两行，其余归 W2）。
- [ ] 新增/并入文档契约测试：agent .md 中不再出现 `"severity": "MAJOR"`、`"severity": "CRITICAL"`、`"severity": "Major"`；`ISSUE_SCHEMA.md` 仍为 `"severity": "major|moderate|minor"`（无第四级守卫）。

### W1 review gate（回滚点 1：既有文件按下方两组文件集 `git checkout/stash`，本批新建测试文件单列显式 `rm`；禁用 reset）

- [ ] `uv run --extra dev python -m pytest tests/skills/paper_audit -q` 全绿。
- [ ] `grep -rn "\"severity\": \"\(MAJOR\|CRITICAL\|Major\)\"" academic-writing-skills/paper-audit/agents/` 零命中。
- [ ] `just fix` 后无 diff 噪声。
- [ ] 记录拟提交分组 W1（不 commit，Phase 3.4 执行）：
  - 组 1a：`scripts/consolidate_review_findings.py` + 新增/扩展测试；拟 message `fix(paper-audit): [AI] normalize CRITICAL severity per D2 (major + gate_blocker)`，正文声明默认行为变化（假绿修复：CRITICAL 不再被降为 moderate 放行）。
  - 组 1b：agent .md 模板 + `editorial_decision_standards.md:147-148` + 文档契约测试；拟 message `docs(paper-audit): [AI] align agent output templates to ISSUE_SCHEMA`。

## 批次 W2 — reviewer 拓扑与共识文档（A-PA-3 / A-PA-4）

### W2-a 测试先行

- [ ] 新增 `tests/skills/paper_audit/test_paper_audit_topology_docs.py`（先红）：
  - `test_skill_md_has_no_specialized_dispatch_promise`：SKILL.md 无 `4 specialized`；仍含 `revision_coach_agent.md`。
  - `test_agent_roster_marks_playbooks_not_dispatched`：agent-roster.md 含 not-auto-dispatched 声明与 `paper-audit-specialized-reviewer-wiring` 指针。
  - `test_consensus_formula_consistent`：`synthesis_agent.md` 与 `editorial_decision_standards.md` 均含 `floor(N/2)+1`；两文档均不含 `ceil(N/2)+1`；synthesis 不含 `N-1 of N`；editorial 不含 `8-dim`。
  - `test_synthesis_no_fourth_severity_level`：synthesis_agent.md 无 `critical | major | moderate | minor` 四级枚举行。
  - `test_committee_logic_has_surrender_protocol`：committee_logic_agent.md 含 `surrender_rate` 与 dict 输出形态说明。
- [ ] 运行确认红。

### W2-b 实现（按 design C4/C5/C6）

- [ ] `SKILL.md:205-211` Reviewer Lanes 段重写（保留 revision_coach_agent.md 字样；不动 frontmatter）。
- [ ] `references/agent-roster.md:30-38` 改「Reference reviewer playbooks (not auto-dispatched)」+ 后续任务指针。
- [ ] `references/DEEP_REVIEW_CRITERIA.md:19,20,22` 指针加「(reference playbook)」。
- [ ] `agents/committee_logic_agent.md` 追加浓缩反谄媚协议 + dict 输出形态。
- [ ] `agents/synthesis_agent.md`：:30 与 :36 公式统一为 `floor(N/2)+1`（simple majority）；:47/:56-57/:66/:85/:104 severity 措辞三级化 + gate_blocker；Output discipline 追加 frame-lock advisory 呈现要求。
- [ ] `references/editorial_decision_standards.md`：:9-14 N-lane 公式表（MAJORITY = `floor(N/2)+1`，含 N=3→2/3、N=5→3/5 示例行）；:38-43/:87-93 角色名映射 committee/lane；:101 8-dim→9-dim。
- [ ] W1/W2 公开资源内容定稿后运行 `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` 刷新 `docs/resource-manifest.json` 源散列；此步只维护 live inventory，双语资源正文/usage 同步按父任务 D7 留给 `07-15-audit-release-integration`。

### W2 review gate（回滚点 2：既有文件按 W2 文件集 `git checkout/stash`，本批新建测试文件单列显式 `rm`；禁用 reset）

- [ ] `uv run --extra dev python -m pytest tests/skills/paper_audit -q` 全绿（含 `test_paper_audit_synthesis.py`、`test_paper_audit_deep_review.py:1017` 的 critical_reviewer 协议锁）。
- [ ] `uv run --extra dev python -m pytest tests/contracts -q` 全绿（SKILL.md 表格/ROUTER_ROW_RE 锁；version 锁不受影响）。
- [ ] `uv run python docs/scripts/check_resource_sync.py --inventory-only` 全绿；不得把 inventory-only 结果表述为双语资源正文已同步。
- [ ] `grep -rn "4 specialized" academic-writing-skills/` 零命中（父任务 D3 验收条款）。
- [ ] 记录拟提交分组 W2（不 commit）：全部 W2 文档 + `test_paper_audit_topology_docs.py` + `docs/resource-manifest.json`（manifest 是 W1/W2 累积共享文件，按实际文件边界归 W2）；拟 message `docs(paper-audit): [AI] remove unwired specialized-agent promises per D3; unify consensus math`。

## 批次 W3 — ScholarEval 信号覆盖（A-PA-5 / A-PA-6 / A-PA-7 / A-PA-8）

### W3-a 测试先行

- [ ] `tests/skills/paper_audit/test_literature_search.py`（或就近文件）新增（先红；A-PA-7/A-PA-8 为 test-only，可能直接绿——绿即锁定现状，符合预期）：
  - `test_module_dimension_map_covers_audit_modules`：映射覆盖 EXPERIMENT/CITATIONS/BIB/PSEUDOCODE/PRESUBMISSION/CONSISTENCY 且 soundness/clarity/presentation 原键不变。
  - `test_reproducibility_signal_from_experiment_module`：EXPERIMENT Critical → `reproducibility_partial < 10.0`；LOGIC+"method" message 不再影响。
  - `test_extract_bibtex_titles`：`title = {...}`（含一层嵌套花括号）、`title = "..."`、`booktitle` 负例。
  - `test_compare_with_literature_bib_content`：.bib fixture → `coverage_ratio > 0`；`bib_content=""` 与 `\bibitem` 路径行为不变（回归）。
  - `test_literature_grounding_unscored_when_no_results`：renorm guard 回归（若已有等价用例则引用不重复）。
  - `test_extract_features_none_defaults_characterization`（A-PA-7，docstring 注明表征测试、行为修复延后）。
  - `test_extract_search_metadata_typst_end_to_end`（A-PA-8，两个 .typ 形态；按 testing-and-tooling.md 的 importlib 模式加载 AUDIT 副本，含加载守卫断言）。
- [ ] 定位并记录锁旧行为的存量断言：`grep -rn "reproducibility_partial" tests/`。

### W3-b 实现

- [ ] `scripts/scholar_eval.py`：新增 `MODULE_DIMENSION_MAP`（design C7），重写 `evaluate_from_audit` 分组与 `_check_reproducibility_signals`；同 commit 迁移受影响存量断言。
- [ ] `scripts/literature_compare.py`：新增 `_extract_bibtex_titles`；`compare_with_literature` 追加可选参数 `bib_content=""`（design C8）。
- [ ] `scripts/audit.py`：新增 `_load_bibliography_content` 辅助并在 `:2502` 分支内接线（`\bibliography{}/\addbibresource{}` / Typst `bibliography("...")`，robust 读取，缺失静默跳过）；**逐行核对 :2496-2501 guard 未被移动/改写**。
- [ ] 自查：`grep -rn "compare_with_literature(" academic-writing-skills/ tests/` 确认全部调用点兼容。

### W3 review gate（回滚点 3：既有文件按下方三组文件集 `git checkout/stash`，本批新建测试文件单列显式 `rm`；禁用 reset）

- [ ] `uv run --extra dev python -m pytest tests/skills/paper_audit -q` 全绿。
- [ ] 手工冒烟（可选但推荐）：构造 tmp .tex + .bib，`python scripts/scholar_eval.py --audit-json <含 EXPERIMENT issue 的 fixture> --json` 观察 `reproducibility_partial != 10.0`（**验证走 JSON/python API，不 grep 渲染报告**——check_format 截断教训同类）。
- [ ] 记录拟提交分组 W3（不 commit）：
  - 组 3a：`scholar_eval.py` + 映射测试 + 迁移的存量断言；拟 message 声明默认行为变化（假绿修复：reproducibility 恒 10.0 → 真实扣分）。
  - 组 3b：`literature_compare.py` + `audit.py` 调用侧 + 测试。
  - 组 3c：两个 test-only（A-PA-7 表征 / A-PA-8 Typst e2e）。

## 收尾（Phase 3）

- [ ] 全量：`just ci`（lint → pyright → 全部测试；pyright 看 error 数不是 warning 数）。
- [ ] Phase 3.3 spec update：按 `.trellis/workflow.md` 走判断（即使结论是"无需更新"）。
- [ ] **Phase 3.4 统一提交**：按已记录的拟提交分组（1a/1b/W2/3a/3b/3c，共 5-6 组）依次 `git commit`；组 1a 与 3a 的 message 正文带默认行为变化双声明（假绿修复）。
- [ ] `git log --oneline` 核对各 commit 独立可 revert、文件集与拟提交分组一致。
- [ ] 回填父任务：A-PA-1..8 处置状态、发现的父 PRD 与代码出入（见 design 各节「现状」）；确认 `07-14` paper-audit 文档子任务可解锁。
- [ ] 不要顺手 bump SKILL.md version（归 version-ci 子任务）；不要跑 `PYTHONIOENCODING=utf-8` 前缀的 pytest。
