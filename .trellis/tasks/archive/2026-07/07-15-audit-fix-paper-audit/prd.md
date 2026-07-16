# consolidation严重级与literature链路(paper-audit) — PRD

## Goal

落地父任务（`07-15-skills-deep-audit-opt`）发现 A-PA-1 ~ A-PA-8，按已定决策 D2（CRITICAL → `major + gate_blocker=true`，canonical schema 保持 `major|moderate|minor` 三级，不新增第四级）与 D3（本轮**移除**未接线的 specialized-agent 承诺，把必要的反谄媚检查并入现有 committee/synthesis）。三条工作流相互独立：W1 severity/schema、W2 reviewer 拓扑、W3 ScholarEval 信号覆盖。

## 范围内发现（按工作流分组）

### W1 — severity/schema 归一（A-PA-1 High、A-PA-2 High）

**R1.1（A-PA-1）** `consolidate_review_findings.sanitize_issue` 目前把 `CRITICAL` 静默降为 `moderate` 且 `gate_blocker=False`（`scripts/consolidate_review_findings.py:44,49-50,75`），违反 `references/editorial_decision_standards.md:147-148`「never suppressed」。要求：severity 大小写不敏感归一；`critical` 归一为 `major` 并**强制** `gate_blocker=true`（覆盖 payload 显式 False）；不新增第四级（D2）。

**R1.2（A-PA-2）** agent 输出模板与 canonical schema（`references/ISSUE_SCHEMA.md:11`）形状不一致：critical_reviewer 用 `MAJOR/CRITICAL` 大写 + `description/location` 字段（`agents/critical_reviewer_agent.md:119,188-190,196-197`）；domain/methodology/literature 用 `"Major"` 首字母大写（`agents/domain_reviewer_agent.md:110`、`methodology_reviewer_agent.md:116`、`literature_reviewer_agent.md:83`）；仅 editor_in_chief 是 canonical 小写（`editor_in_chief_agent.md:96`）。要求：**模板与 sanitizer 双侧修**（理由见 design W1）——模板统一到 ISSUE_SCHEMA 小写三级；sanitizer 增加字段别名回落（`description→explanation`、`location→source_section`，**禁止**把 location 伪造进 `quote`）。

**AC-W1**
- [ ] `sanitize_issue({"severity": "CRITICAL", "gate_blocker": False})` → `severity="major"` 且 `gate_blocker=True`；`"Critical"/" critical "` 同效。
- [ ] `description`-only payload 的 `explanation` 非空；`location`-only payload 的 `source_section` 非空且 `quote` 仍为空串。
- [ ] `observation`（critical_reviewer 旧枚举 :122）归一为 `minor`，不再默认升为 `moderate`。
- [ ] 端到端：含 CRITICAL 的 comments fixture 经 `load_comment_files` + `consolidate_findings` 后排序最前、`gate_blocker=true`。
- [ ] 五个 agent .md 输出示例全部小写三级；`ISSUE_SCHEMA.md:11` 保持 `major|moderate|minor` 不变（守卫测试锁定无第四级）。
- [ ] `editorial_decision_standards.md:147-148` 的「CRITICAL never suppressed」改写为 gate_blocker 语义并与 D2 一致。
- [ ] W1/W2 公开资源内容变更后刷新 `docs/resource-manifest.json` 的 `sourceSha256`，使 inventory contract 与真实源文件一致；双语资源正文同步仍按父任务 D7 留给终批集成任务。
- [ ] 每项修复有回归测试（新增于 `tests/skills/paper_audit/test_paper_audit_deep_review.py` 或姊妹文件）。

### W2 — reviewer 拓扑与文档一致性（A-PA-3 Medium、A-PA-4 Medium）

**R2.1（A-PA-3，按 D3）** 专项 reviewer（methodology/domain/critical/literature）在 MODE_GUIDE/SUBAGENT_TEMPLATES/REVIEW_LANE_GUIDE 中零派发指令（`references/MODE_GUIDE.md:133-199` 只派 committee+lanes），`SKILL.md:207-210`「4 specialized agents」为 over-promise。要求：
- 移除 SKILL.md「dispatches … 4 specialized agents」承诺，文案与实际 committee+lanes 拓扑一致（保留 `revision_coach_agent.md` 字样，测试锁 `tests/skills/paper_audit/test_paper_audit_synthesis.py:98-102`）。
- `references/agent-roster.md:30-38`「Specialized deep-review agents / activation criteria」改为「参考型 playbook，当前不自动派发」，并指向后续接线任务（见非目标）。
- `references/DEEP_REVIEW_CRITERIA.md:19-22` 对 A5-A7/B6-B10/C5 的指针保留，但措辞改为指向参考文件而非派发承诺。
- **不删除**任何 `agents/*.md` / `references/*.md` 文件（docs 双语资源契约，见 design 风险）。

**R2.2（A-PA-3，surrender/frame-lock 机制处置）** `consolidate_review_findings.apply_frame_lock_advisory`（:80-93）及 `load_comment_files` 的 surrender_rate 分支（:110-113,125-128）在消费端已接线且有单测（`test_paper_audit_deep_review.py:911-1014`），但生产端为零——critical_reviewer 从不被派发。要求：按 D3 选择**最小接线**（design 推荐方案）：把浓缩版反谄媚协议（挑战计数、撤回需 rebuttal 评分 ≥4、输出 `surrender_rate`）并入 `agents/committee_logic_agent.md`，其 comments JSON 采用 `{"issues": [...], "surrender_rate": ...}` dict 形态；`agents/synthesis_agent.md` 增加对 frame-lock advisory 的呈现要求。critical_reviewer 完整协议留存为参考文件。

**R2.3（A-PA-4）** 共识数学统一：`editorial_decision_standards.md:9-14` 固定 3-reviewer 假设与 `synthesis_agent.md:30` `>= ceil(N/2)+1` 矛盾，且 synthesis 自身 :36「N-1 of N」与 :30 公式不一致；`editorial_decision_standards.md:101`「Average Score (8-dim)」早于 9 维（`scholar_eval.py:37-47`）。要求：**统一为普通多数（simple majority）`floor(N/2)+1`**（父 PRD A-PA-4 裁决；N=3→2、N=5→3，恢复 editorial 原「2 of 3」意图；ceil 式为超多数且 N=3 时 MAJORITY 退化为 ALL，故弃用）——synthesis :30 的 ceil 公式与 :36 的「N-1 of N」均改写为该式，editorial :9-14 同步；`:101` 改 9-dim；`:38-43,:87-93` 的 Methodology/Domain/Critical Reviewer 称谓映射到实际 committee/lane 角色；`synthesis_agent.md:47,56-57,66,85` 残留的四级 severity 文案改为三级 + gate_blocker 语义。

**AC-W2**
- [ ] 全仓 grep 无「4 specialized」派发承诺残留（父任务验收 D3 条款）。
- [ ] agent-roster 明示「不自动派发」+ 后续任务指针；DEEP_REVIEW_CRITERIA 指针措辞更新。
- [ ] `committee_logic_agent.md` 含 surrender_rate 协议且输出为 dict 形态；`load_comment_files` 对该形态的既有单测保持绿。
- [ ] `synthesis_agent.md` 与 `editorial_decision_standards.md` 引用同一公式 `floor(N/2)+1`（simple majority；两文档均无 `ceil(N/2)+1`、无「N-1 of N」残留）；editorial 无「8-dim」残留；synthesis 无 `critical` 四级枚举残留。
- [ ] 新增文档契约测试锁定上述各点（每项修复含 Low 均有回归测试）。
- [ ] `tests/contracts/test_skill_contracts.py` 与 `tests/skills/paper_audit/test_paper_audit_synthesis.py` 全绿（SKILL.md 表格/字符串锁不破）。

### W3 — ScholarEval 信号覆盖（A-PA-5 Medium、A-PA-6 Low/Med、A-PA-7 Low test-only、A-PA-8 test-only）

**R3.1（A-PA-5）** `scholar_eval.evaluate_from_audit`（:100-146）忽略 EXPERIMENT/CITATIONS/BIB/PSEUDOCODE/PRESUBMISSION（以及 zh-only CONSISTENCY，父 PRD 未列，实测同样未映射）；reproducibility 信号挂在从不产出的 `LOGIC && "method" in message`（:90-97）→ `reproducibility_partial` 恒 10.0。要求：建立显式 `MODULE_DIMENSION_MAP`（模块名以 `audit.py:337-352` script_map + `:257` ZH_EXTRA_CHECKS 的 `.upper()` 产物（:469,:2455）为准核对）；reproducibility 信号改挂 EXPERIMENT（+PSEUDOCODE）；映射表见 design。

**R3.2（A-PA-6）** `literature_compare._extract_citation_titles`（:59-75）只识别 `\bibitem` → 外置 .bib 的 LaTeX 论文与 Typst 论文 bib_titles 为空，`coverage_ratio`（:194）趋 0 反向拉低 grounding。要求：新增 BibTeX title 字段解析；audit.py 调用侧（:2502-2515）解析 `\bibliography{}/\addbibresource{}`（.tex）与 `bibliography("…")`（.typ）读入 .bib 内容传入。**不得破坏** `audit.py:2496-2501` 的空结果不打分 renorm guard（守卫回归测试）。注：Typst `@key` 引用键已在 `audit.py:2508-2509` 提取（与父 PRD 措辞的出入见 design）。

**R3.3（A-PA-7，test-only）** `scoring_model._extract_features._g` None→5.0 进特征（:139-141）但 None 不进 `dims_below_5` 罚项（:162-168）——校准不对称。本轮只加表征（characterization）测试锁定现状，行为改动延后。

**R3.4（A-PA-8，test-only）** 父任务已证实「literature_search import 不存在函数」为**误报**（`extract_title/extract_abstract` 定义于 paper-audit `scripts/parsers.py:632/664`，Typst 链路可用）。本轮只补 Typst 端到端回归测试：`extract_search_metadata`（`literature_search.py:268-333`）对 .typ fixture 返回非空 title/abstract，防未来退化、也防误报复发。

**AC-W3**
- [ ] EXPERIMENT 模块 Critical issue → `reproducibility_partial < 10.0`；LOGIC 的 "method" message 不再驱动 reproducibility。
- [ ] CITATIONS/BIB/PSEUDOCODE/PRESUBMISSION/CONSISTENCY 各自落入映射维度并有逐模块断言；映射键集合与 audit.py 实际可产出模块集合一致（守卫测试）。
- [ ] BibTeX fixture（.tex + 外置 .bib）经 `compare_with_literature` 得 `coverage_ratio > 0`；`\bibitem` 旧行为回归不变；空 `bib_content` 行为不变。
- [ ] `filtered_results` 为空时 `literature_grounding` 仍不打分（renorm guard 回归）。
- [ ] A-PA-7 表征测试：None 特征取 5.0 且不计入 dims_below_5（两断言）。
- [ ] A-PA-8 Typst e2e 测试：`#show ...with(title: ..., abstract: [...])` 与 `#set document(title: "...")` 两形态均提取成功。

## 非目标（Out of scope）

1. **专项 reviewer 完整接线**：为 methodology/domain/critical/literature reviewer 建立真实派发（MODE_GUIDE 派发指令、schema 版本化、与 committee 角色去重）另立后续功能任务 **`paper-audit-specialized-reviewer-wiring`**（未建；D3 明示 schema 不兼容且与 committee 角色重叠，不在本任务做）。
2. A-PA-7 的行为修复（None 罚项对称化）——仅表征测试。
3. `scoring_model.json` 权重/系数调整（父任务确认健康项：权重和 1.00、regression fallback 健全）。
4. deai 无 `--analyze` 运行方式（有意设计，勿再触碰）。
5. SKILL.md `version` 字段（归 `07-15-audit-fix-version-ci`，本任务只改文案不动 version/last_updated）。
6. 双语资源正文、usage/概览页与文档站构建同步（按父任务 D7 归终批 `07-15-audit-release-integration`）；本任务仅刷新受影响公开源资源的 manifest 散列，以满足 live inventory contract 和 `just ci`。

## 约束

- 遵守 CLAUDE.md 红线：不动 cite/ref/label/math，不造数据，输出带 `[Script]/[LLM]` 标注。
- 不删任何 `references/`、`agents/` 文件（docs-bilingual-resources 契约）。
- 公开资源内容变化必须刷新 `docs/resource-manifest.json`；这是 CI inventory 维护，不代表双语目标页已完成同步，后者由父任务 D7 的终批任务验收。
- 每项修复（含 Low）配回归测试；test-only 项配表征/回归测试（父任务验收条款）。
- 验证命令：`uv run --extra dev python -m pytest tests/skills/paper_audit -q`；收尾 `just ci`。
