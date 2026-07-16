# Design — 07-15-audit-fix-paper-audit

三条工作流**相互独立**：主要改动文件集不重叠（W1 = consolidator + agent 输出模板；W2 = 拓扑/共识文档；W3 = scholar_eval/literature_compare/audit.py 调用侧 + 两个 test-only 项），可独立分组拟提交（实际 commit 统一在 Phase 3.4）、独立回滚。共享点有两个：`editorial_decision_standards.md` 同时被 W1（:147-148 CRITICAL 语义）与 W2（:9-14/:38-43/:87-93/:101）触碰——按行分批编辑，W1 只动 :147-148；W1/W2 的公开资源内容变化共同要求在 W2 收尾刷新 `docs/resource-manifest.json` 的源散列。双语资源正文仍按父任务 D7 由终批集成任务同步。

---

## W1 — severity/schema 归一（A-PA-1 / A-PA-2）

### 现状（已核实）

- `scripts/consolidate_review_findings.py:12` `SEVERITY_ORDER = {"major":0,"moderate":1,"minor":2}`；`:44` `severity = str(...).lower()`；`:49-50` 非法值（含 `critical`）一律回落 `moderate`；`:75` `gate_blocker = bool(issue.get("gate_blocker", severity=="major"))` → CRITICAL 输入最终 `moderate + gate_blocker=False`。
- `sanitize_issue`（:39-77）期望键：`title/quote/explanation/severity/comment_type/source_kind/confidence/source_section/related_sections/root_cause_key/review_lane/gate_blocker/quote_verified`。
- agent 模板实际发出的键：
  - `critical_reviewer_agent.md:184-198`：`dimension/title/description/severity("MAJOR"|"CRITICAL")/location` — explanation、quote、source_section 全落空。
  - `domain_reviewer_agent.md:104-113`、`methodology_reviewer_agent.md:110-119`：weaknesses 形状 `title/problem/why/suggestion/severity("Major")/location`。
  - `literature_reviewer_agent.md:79-84`：`severity: "Major"`。
  - `editor_in_chief_agent.md:96`：小写（canonical，不动）。
  - committee/lane agents（如 `committee_editor_agent.md:33-36`、`SUBAGENT_TEMPLATES.md:22,49`）已约定「Must follow ISSUE_SCHEMA.md」——canonical。

### 契约

**C1. sanitize_issue 归一规则（`consolidate_review_findings.py`）**

```python
_SEVERITY_ALIASES = {"critical": "major", "observation": "minor"}

severity_raw = str(issue.get("severity", "moderate")).strip().lower()
is_critical = severity_raw == "critical"
severity = _SEVERITY_ALIASES.get(severity_raw, severity_raw)
if severity not in SEVERITY_ORDER:
    severity = "moderate"
# D2：critical 强制 gate_blocker=True，覆盖 payload 的显式 False
gate_blocker = True if is_critical else bool(issue.get("gate_blocker", severity == "major"))
```

**C2. 字段别名回落（仅在 canonical 字段为空时生效）**

- `explanation` 为空 → 回落 `str(issue.get("description", "")).strip()`。
- `source_section` 为空 → 回落 `str(issue.get("location", "")).strip()`（沿用现有 :58-61 的 related_sections 前插逻辑）。
- **不**把 `location` 填入 `quote`：`quote` 有「exact quote from paper」契约（`ISSUE_SCHEMA.md:8`）与 `verify_quotes.py` 校验语义，伪造 quote 会被判 `quote_verified=false` 反而降置信。location 是位置锚，语义归 `source_section`。

**C3. 模板侧改动**

- `critical_reviewer_agent.md`：
  - severity 表（:115-122）改为三级：`major`（原 CRITICAL 概念 = `major` + `"gate_blocker": true`，表中注明）、`moderate`、`minor`；OBSERVATION 行删除，改为「替代视角写入 `missing_perspectives`，不作为 issue 输出」。
  - 输出示例（:177-227）issues 字段改 canonical：`title/quote/explanation/severity(小写)/source_section/comment_type/source_kind:"llm"`，`dimension` 保留为附加字段（schema 允许多余字段，sanitize 不携带即丢弃，无害）。
- `domain/methodology/literature_reviewer_agent.md`：示例中 `"Major"` → `"major"`，并加一行注：「若该输出落入 `comments/*.json` 供 consolidation 消费，必须转换为 `references/ISSUE_SCHEMA.md` 记录」。weaknesses/novelty_concerns 人读形状本身不改（这些文件当前是参考 playbook，见 W2）。
- `references/editorial_decision_standards.md:147-148`：「Critical Reviewer CRITICAL findings are never suppressed」→「CRITICAL-rated findings are normalized to `major + gate_blocker=true` (D2) and are never suppressed: they must appear in the final report as Priority 1」。

### 为什么双侧修（alternatives considered）

- **只修模板**：LLM 输出方差无法靠文档 100% 约束；历史 payload / 用户手写 comments 仍会命中降级路径。Rejected。
- **只修 sanitizer**：文档继续教 LLM 输出错误形状，`description/location` 永久停留在别名路径上，schema 契约名存实亡。Rejected。
- **双侧修**（推荐）：模板 = 契约（正道），sanitizer = 运行时兜底（防御纵深）。成本小、均可测试。
- `observation→minor` 是超出 D2 的微小追加：不映射则旧模板产出的 OBSERVATION 会被 :49-50 回落**升级**为 moderate（信息性条目被当缺陷）。映射有明确出处（critical_reviewer :122），测试锁定。

### 风险与回滚

- 风险 1：现有测试锁旧行为——`test_paper_audit_deep_review.py:256-282,886-909` 用到 sanitize/consolidate；改动前先跑定位，若锁「非法值→moderate」需确认其用例不含 critical/observation（经查 :886 附近为默认填充测试，预计不冲突，实施时验证）。
- 风险 2：`gate` 模式消费 `gate_blocker` 的下游（report_generator/render_deep_review_report）语义变化 = 曾被错误放行的 CRITICAL 现在正确阻断——这是**误报/假绿修复类默认行为变化**，按 spec 约定在 commit message 显式声明。
- 回滚：批内不提交（commit 统一延后到 Phase 3.4）；按拟提交分组的文件集 `git checkout -- <W1 文件集>` / `git stash` 整批撤销。Phase 3.4 拆两组拟提交（consolidator+测试 / agent .md 模板+文档契约测试），提交后仍可独立 `git revert`。

---

## W2 — reviewer 拓扑与共识文档（A-PA-3 / A-PA-4，按 D3）

### 现状（已核实）

- 派发拓扑：`MODE_GUIDE.md:133-172` Phase 3A 只派 5 个 committee agent；:174-199 Phase 3B 只派 section + cross-cutting lanes；`SUBAGENT_TEMPLATES.md` 全文无 specialized reviewer 模板。grep `critical_reviewer|domain_reviewer|methodology_reviewer|literature_reviewer` 命中仅：`agent-roster.md:34-37`、`DEEP_REVIEW_CRITERIA.md:19,20,22`（判据指针）。
- over-promise：`SKILL.md:207-210`「Deep-review dispatches 5 committee agents, 6+ lane agents, and 4 specialized agents」；`agent-roster.md:30-33`「Specialized deep-review agents / Read their files for activation criteria」。
- surrender 机制：生产端仅 `critical_reviewer_agent.md:124-173`（从不派发）；消费端 `consolidate_review_findings.py:110-113,125-128` + `apply_frame_lock_advisory`（:80-93）**活代码且有 5 个单测**（`test_paper_audit_deep_review.py:911-1014`）——"死"的是生产侧，不是消费侧。
- 共识数学三处矛盾：`synthesis_agent.md:30`（majority = `>= ceil(N/2)+1`）vs `:36`（`[CONSENSUS-MAJORITY]` = "N-1 of N"）vs `editorial_decision_standards.md:11-13`（固定 3/3、2/3）。另 `synthesis_agent.md:47,56-57,66,85` 出现 `critical` 四级枚举；`editorial_decision_standards.md:101`「Average Score (8-dim)」已过时（9 维见 `scholar_eval.py:37-47`）。

### 契约

**C4. 承诺移除（不删文件）**

- `SKILL.md:205-211` Reviewer Lanes 段重写为：committee 5 + lanes 6+ + 模式专属 agent（`editor_in_chief_agent.md` for gate、`revision_coach_agent.md` for re-audit、revision-suggestion post-consolidation、`synthesis_agent.md`）；追加一句「Specialized reviewer playbooks under `agents/` are reference material (not auto-dispatched); see `references/agent-roster.md`」。**必须保留** `revision_coach_agent.md` 字样（测试锁 `test_paper_audit_synthesis.py:98-102`）。
- `agent-roster.md:30-38`：标题改「Reference reviewer playbooks (not auto-dispatched)」；正文注明：其判据（A5-A7/B6-B10/C3-C5）已由 committee/lane 判据文档引用；完整派发接线归后续任务 `paper-audit-specialized-reviewer-wiring`（显式指针）。
- `DEEP_REVIEW_CRITERIA.md:19,20,22`：指针措辞 `see A5-A7 in domain_reviewer_agent.md` → `see A5-A7 in domain_reviewer_agent.md (reference playbook)`，判据本体不动。

**C5. 反谄媚最小接线（推荐方案）**

- `agents/committee_logic_agent.md`（committee 中最接近 devil's advocate 的角色）追加浓缩协议（约 15 行）：
  1. 每个将要撤回/软化的 challenge，先给隐式作者反驳打 1-5 分（rubric 引用 `critical_reviewer_agent.md` 的 Surrender-Rate Protocol，不复制全文）；仅 ≥4 允许撤回。
  2. 统计 `challenges_made`、`surrenders`，输出 `surrender_rate = surrenders / max(1, challenges_made)`。
  3. comments 输出形态从 JSON array 改为 dict：`{"issues": [...], "surrender_rate": 0.xx, "frame_lock_alert": bool}` —— `load_comment_files:107-117` 已原生识别该形态，`> 0.6` 自动触发 advisory（:125-128），**零脚本改动**。
- `agents/synthesis_agent.md`：Output discipline 段追加一条：「若任一 lane 被打上 frame_lock advisory（explanation 含 `frame_lock_alert` 标记），`overall_assessment.txt` 必须点名该 lane 并提示置信已降级」。

**替代方案（rejected）**：删除 `apply_frame_lock_advisory` + surrender 分支 + 5 个单测，文档指向后续任务。理由拒绝：消费端代码健康、已测试、无维护负担；D3 要求「必要的反谄媚检查并入现有 committee/synthesis」，删除后后续接线任务需整体重建；最小接线只改两个 .md 提示词，成本低于删除。

**C6. 共识数学统一（普通多数 `floor(N/2)+1`，父 PRD A-PA-4 裁决）**

统一公式为**普通多数（simple majority）`floor(N/2)+1`**：N=3 → 2/3，N=5 → 3/5——恢复 `editorial_decision_standards.md` 原「2 of 3」意图。曾考虑沿用 synthesis 现有的 `ceil(N/2)+1`，rejected：它实为超多数（supermajority，N=3 → 3/3、N=5 → 4/5），且 N=3 时与 ALL 重合，`[CONSENSUS-MAJORITY]` 标签不可达（退化为 CONSENSUS-ALL）。

- `synthesis_agent.md:30`：「>= ceil(N/2)+1」→「>= floor(N/2)+1（simple majority；N=3 即 >=2，N=5 即 >=3）」。
- `synthesis_agent.md:36`：「N-1 of N lanes agree」→「>= floor(N/2)+1 of N lanes agree（与 :30 的 `majority` 量词一致）」——两处修正对齐到同一 `floor(N/2)+1`。
- `editorial_decision_standards.md:9-14`：阈值列从固定 3-reviewer 改 N-lane 公式：ALL = N/N；MAJORITY = `>= floor(N/2)+1` 且非全体（worked examples：N=3 时 2/3，N=5 时 3/5 或 4/5）；SPLIT = 其余。示例保留 N=3 与 N=5 各一行具体数字帮助理解。
- `editorial_decision_standards.md:101`：「Average Score (8-dim)」→「Average Score (9-dim ScholarEval)」。
- `editorial_decision_standards.md:38-43`（Expertise 表）与 `:87-93`（Score Merging 表）：Methodology Reviewer → `committee_methodology` / `evaluation_fairness` lane；Domain Reviewer → `committee_theory` + `committee_literature` / `prior_art` lane；Critical Reviewer → `committee_logic` / `claims_vs_evidence` lane。原名以括号保留（「(formerly Methodology Reviewer playbook)」）以维持与参考 playbook 的可追溯性。
- `synthesis_agent.md:47`（`critical | major | moderate | minor`）→ `major | moderate | minor`（补注：lane 报 CRITICAL 时由 consolidation 归一为 `major + gate_blocker=true`）；`:56-57`「one lane reports CRITICAL while others report MINOR」→ gate_blocker 措辞；`:66`「`critical` blocks gate mode」→「`gate_blocker=true` issues block `gate` mode」；`:85`「singleton CRITICAL findings」→「singleton gate_blocker findings」；`:104`「critical surfaces in gate mode separately」同步。

### 风险与回滚

- 风险 1：docs-bilingual-resources 契约——`references/`、`agents/` 文件增删会破坏 docs manifest/检查器。本工作流**只改内容不增删文件**；实施后跑 `tests/`（含 docs 契约测试）确认。
- 风险 2：SKILL.md 字符串锁与表格 hook——改 SKILL.md 后必须跑 `tests/contracts/test_skill_contracts.py`（ROUTER_ROW_RE）与 `test_paper_audit_synthesis.py`；不动 frontmatter `version`。
- 风险 3：`test_paper_audit_deep_review.py:1017-1024` 锁 critical_reviewer 文档含 surrender 协议——文件保留、协议保留，该锁天然不破；committee_logic 新协议另加新锁。
- 风险 4：公开资源内容变化会使 `test_inventory_only_cli_passes` 因 `sourceSha256` 漂移失败。W2 文档定稿后运行 `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`，仅刷新 inventory；不把该命令误报为双语页面已同步，完整目标页校验留给父任务 D7 的终批任务。
- 回滚：纯文档 + 文档契约测试，批内 `git checkout -- <W2 文件集>` 整批撤销，无代码耦合；Phase 3.4 作单组拟提交。

---

## W3 — ScholarEval 信号覆盖（A-PA-5 / A-PA-6 / A-PA-7 / A-PA-8）

### 现状（已核实）

- audit 管线实际产出的模块名 = `_resolve_script` script_map 键（`audit.py:337-352`：format/grammar/logic/experiment/sentences/deai/citations/bib/figures/pseudocode/consistency/references/visual/presubmission）∪ zh 追加（`:257` `ZH_EXTRA_CHECKS = ["consistency", "gbt7714"]`）经 `.upper()`（`:469,:2455`）。注意：`gbt7714` **不在** script_map → `_resolve_script` 返回 None → 恒 SKIP（`:2413-2415`），不会产生模块名，不入映射（顺带发现，超范围不修）。
- `scholar_eval.evaluate_from_audit`（:100-146）仅映射 LOGIC→soundness（:123）、GRAMMAR+SENTENCES+FORMAT+DEAI→clarity（:126-132）、FIGURES+VISUAL+REFERENCES→presentation（:134-138）；`_check_reproducibility_signals`（:90-97）过滤条件 `module=="LOGIC" and "method" in message` 在实际管线中从不命中 → `reproducibility_partial` 恒 10.0。
- `literature_compare._extract_citation_titles`（:59-75）只匹配 `\bibitem`；`compare_with_literature`（:96-222）的 `coverage_ratio = len(cited_and_found)/total_found`（:194）在 bib_titles 为空时几乎必为 0。**调用侧已提取引用键**：`audit.py:2505-2507`（LaTeX `\cite{}`）、`:2508-2509`（Typst `@key`）——父 PRD「Typst 引用键」措辞部分已成立，真缺口是**参考文献题名**来源（外置 .bib 未读入）。
- renorm guard 健康：`audit.py:2496-2501` 空 `filtered_results` → 不打分、权重重归一（勿破坏）。
- `scoring_model._extract_features`（:132-169）：`_g` None→5.0（:139-141）；`dims_below_5` 只数非 None 且 <5.0（:162-168）。
- `literature_search.extract_search_metadata`（:268-333）经 `from parsers import extract_title/extract_abstract`（:290-291）取题名/摘要；两函数存在于 `scripts/parsers.py:632/:664` 且含 Typst 形态（`#show ...with(title:)` / `#set document(title:)`）。`tests/skills/paper_audit/test_literature_search.py` 现无 Typst e2e 用例。

### 契约

**C7. 模块→维度映射（`scholar_eval.py`）**

新增模块级常量并重写 `evaluate_from_audit` 的分组逻辑：

```python
MODULE_DIMENSION_MAP: dict[str, str] = {
    "LOGIC": "soundness",
    "GRAMMAR": "clarity", "SENTENCES": "clarity", "FORMAT": "clarity",
    "DEAI": "clarity", "CONSISTENCY": "clarity",
    "FIGURES": "presentation", "VISUAL": "presentation", "REFERENCES": "presentation",
    "CITATIONS": "presentation", "BIB": "presentation", "PRESUBMISSION": "presentation",
    "EXPERIMENT": "reproducibility", "PSEUDOCODE": "reproducibility",
}
```

- `_check_reproducibility_signals` 改为基于 EXPERIMENT+PSEUDOCODE 模块 issue 扣分（保留函数名与 `_deduct_score` 复用）；LOGIC+"method" message 启发式删除。
- 每个模块只入一个维度（**不双计**）。alternatives：EXPERIMENT 同时入 soundness——rejected（同一 issue 在两个加权维度扣分，放大权重且违背 deduction 模型独立性）；PRESUBMISSION 入 clarity——rejected（机械提交卫生更贴近 presentation，AI 语气已由 DEAI→clarity 覆盖）；CONSISTENCY 入 presentation——rejected（术语/缩写一致性属表达清晰度）。
- 未知模块（未来新增 check）不映射即不扣分——与现状一致，映射守卫测试会在新增 check 时提醒补表。

**C8. .bib 题名解析（`literature_compare.py` + `audit.py` 调用侧）**

- `literature_compare.py` 新增 `_extract_bibtex_titles(bib_content: str) -> list[str]`：匹配 `title\s*=\s*[{"]...`，花括号形态用平衡扫描容忍一层嵌套（`{{Deep} Learning}`），去除包裹括号与多余空白；忽略 `booktitle`（负例测试）。
- `compare_with_literature(..., bib_content: str = "")` 追加**可选**参数：`bib_titles = _extract_citation_titles(paper_content) + _extract_bibtex_titles(bib_content)`。默认空串 → 行为与现状逐字节一致（向后兼容，签名追加不破坏既有调用）。
- `audit.py` 调用侧（:2502-2515 内）：新增辅助 `_load_bibliography_content(path: Path, content: str, fmt: str) -> str`——.tex 解析 `\bibliography{a,b}`（补 `.bib` 后缀）与 `\addbibresource{a.bib}`；.typ 解析 `bibliography("refs.bib")`（.yml 暂不解析，留注释）。相对入口文件目录解析路径，`_read_source` robust 读取，文件缺失/读失败返回空串并静默跳过（不告警刷屏，literature-search 本就 best-effort）。**位置在 `if literature_context.filtered_results:` 分支内部**，:2496-2501 guard 原样不动。

**C9. test-only 契约**

- A-PA-7 表征测试（`tests/skills/paper_audit/test_literature_search.py` 现有 scoring_model 测试旁）：`_extract_features({"novelty": None, ...})` → `features["novelty"] == 5.0` 且 `dims_below_5` 不含 None 维；测试 docstring 注明「表征测试：锁定 None→5.0 不对称现状，行为修复延后（A-PA-7）」。
- A-PA-8 Typst e2e（同文件）：两个 .typ 内容 fixture（`#show: ieee.with(title: [...], abstract: [...])` 与 `#set document(title: "...")` + `= Abstract` 节）→ `extract_search_metadata` 的 `title`/`abstract` 非空；断言走真实 `parsers` import 链（bare import 在 conftest 下解析到 EN 副本——**注意**：`tests/conftest.py` 把 AUDIT scripts 也放 sys.path，`literature_search` 内部 `from parsers import ...` 在子进程/同进程语境不同；测试通过 `import literature_search` 后调 `extract_search_metadata`，其内部 import 解析顺序由 sys.path 前排决定，EN 与 AUDIT 的 parsers 对齐锁保证两副本共享面一致，但 `extract_title/extract_abstract` 是否在 EN 副本同样存在需在写测试时用 `importlib` 按路径加载 AUDIT 副本兜底——遵循 `.trellis/spec/academic-writing-skills/testing-and-tooling.md` 的 importlib 模式)。

### 风险与回滚

- 风险 1：存量测试锁旧评分行为（`reproducibility_partial` 恒 10.0 可能被某测试断言）——实施前 `grep -rn "reproducibility_partial" tests/` 定位并随 commit 迁移，commit message 声明「默认行为变化：假绿修复」（spec 约定的双声明）。
- 风险 2：`compare_with_literature` 新参数被三方调用——grep 全仓确认调用点仅 `audit.py:2511`（已核实）与测试。
- 风险 3：.bib 路径解析引入 I/O——限定在 literature-search 分支内（用户显式 `--literature-search` 才触发），失败静默降级为现状行为。
- 回滚点：三个独立文件集分组——(1) scholar_eval 映射+测试；(2) literature_compare+audit.py 调用侧+测试；(3) 两个 test-only。批内按分组 `git checkout/stash` 撤销互不影响；Phase 3.4 按同分组各作一组拟提交，提交后任一 revert 不影响其余。

---

## 测试布局汇总

| 工作流 | 测试文件 | 类型 |
|--------|----------|------|
| W1 | `tests/skills/paper_audit/test_paper_audit_deep_review.py`（扩展 sanitize/consolidate 用例） | 单元 + 端到端 fixture |
| W1/W2 | 新增 `tests/skills/paper_audit/test_paper_audit_topology_docs.py`（或并入 test_paper_audit_synthesis.py）：schema 三级守卫、无 "4 specialized"、公式一致、committee_logic surrender 锁 | 文档契约 |
| W3 | `tests/skills/paper_audit/test_literature_search.py`（映射、.bib、A-PA-7/A-PA-8）+ `test_paper_audit.py`（renorm guard 回归若无现成用例） | 单元 + 回归 |

验证命令（每批）：`uv run --extra dev python -m pytest tests/skills/paper_audit -q`；W2 后加 `uv run --extra dev python -m pytest tests/contracts -q`；收尾 `just ci`。
