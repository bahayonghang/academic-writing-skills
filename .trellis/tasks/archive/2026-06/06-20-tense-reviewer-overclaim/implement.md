# Implement — ⑤ 时态信号词检测 / ⑥ reviewer 怀疑点排序 / ① over-claim 进 paper-audit 维度

> 执行序：基线 → ⑤ 文档（热身）→ ⑤ 脚本（EN 基准→typst→zh，含测试）→ ⑤ 流入验证 → ⑥ → ① → SKILL.md 收尾 → 全量校验。
> 每阶段给验证命令与回滚点。EN 为基准副本。

## 前置基线

- [ ] `just ci` 跑一次确认起点全绿（避免把既有红误算到本任务）
- [ ] `git switch -c feat/tense-reviewer-overclaim`（在 dev 上开分支）
- [ ] 记录 4 处 SKILL.md 当前 `version`（en/zh/typst/paper-audit；结束前比对未被 bump）

验证：`uv run --extra dev python -m pytest -q` 起点通过。

---

## 阶段 A — ⑤ 时态参考文档 ×3（低风险热身）

1. EN：新建 `latex-paper-en/references/modules/tense-guide.md`：逐章节时态表（Abstract 各部分 / Intro / Methods 绝对过去 / Results 绝对过去 / Results 描述图表用现在 / Discussion / Caption 绝对现在）+ 信号词自查清单（含 `is`/`are` 的判断级提示）+ 例外（图表/软件/通论）。CS/通用语境例子。
2. Typst：新建 `typst-paper/references/TENSE_GUIDE.md`：英文同 EN。
3. ZH：新建 `latex-thesis-zh/references/writing/tense-guide-zh.md`：中文学位论文语境，聚焦**英文摘要**时态（Background 现在 / Methods·Results 过去 / Conclusion 现在），说明中文正文无时态故脚本只查英文摘要。

验证：人工通读三份结构对齐、zh 非直译；无悬挂引用。
回滚点：`git checkout -- <3 新文件>`。

---

## 阶段 B — ⑤ 脚本层（EN 基准 → typst → zh + 测试）

### B1 EN 实现
1. `latex-paper-en/references/deai/tone-thresholds.yaml`：追加 `tense:` 段（design 2.1）。
2. `latex-paper-en/scripts/deai_check.py`：
   - `DEFAULT_THRESHOLDS` 加 `tense` 默认块；
   - `__init__` 加 `_tense_enabled` / `_tense_signals`；
   - 新增 `_tense_false_positive`（design 2.2）与 `_check_tense`（门控 `method`/`result`，design 2.3）；
   - `check_section` 追加 `results["traces"].extend(self._check_tense(section_name))`。
3. 新建 `tests/test_deai_tense.py`：
   - method/result 段含 "Table results show ..."（现在时）→ 断言 emit tense trace，severity=low，category=tense，provenance=[Script]；
   - "Figure 2 shows ..." / "as shown in Fig. 3" → 断言**不**报（FP 过滤）；
   - introduction 段含 "show" → 断言不报（门控）；
   - 干净过去时文本 → 不报；
   - YAML 无 tense / `enabled:false` → 回退/跳过不报错。

验证：`uv run --extra dev python -m pytest tests/test_deai_tense.py -q` 通过。
回滚点：`git checkout -- latex-paper-en/scripts/deai_check.py <yaml> tests/test_deai_tense.py`。

### B2 镜像 typst
4. `typst-paper/references/AI_TONE_THRESHOLDS.yaml` + `typst-paper/scripts/deai_check.py`：同 B1 逻辑（typst section key 同 en：method/result）。

### B3 镜像 zh（区域门控）
5. `latex-thesis-zh/references/deai/tone-thresholds.yaml`：加 `tense:` 段。
6. `latex-thesis-zh/scripts/deai_check.py`（`ChineseAITraceChecker`）：
   - `__init__` 计算 `self._en_abstract_range`（`\begin{abstract}` 排除 `\begin{cabstract}`，design 2.4）；
   - `_check_tense`：区域门控 + English-line 门控 + FP 过滤；无英文摘要 → no-op；
   - `check_section` 接线。

### B4 副本核对
7. 以 EN `_check_tense`/`_tense_false_positive` 为基准 diff typst（应全同）、zh（差异仅区域门控 vs section 门控，逐行确认）。

验证：`uv run --extra dev python -m pytest academic-writing-skills/*/tests/ tests/ -q -k "deai or tense"` 通过。
回滚点：`git checkout -- <deai_check.py ×3, yaml ×3, test 文件>`。

---

## 阶段 C — ⑤ 流入 paper-audit 验证

1. 找/造一个含 method/result 现在时信号词的 `.tex` fixture（复用 evals/fixtures 或 tests fixture）。
2. 实跑 paper-audit deai 模块：`uv run --extra dev python academic-writing-skills/paper-audit/scripts/audit.py <fixture.tex> --check deai`（或等价 CLI），确认 tense trace 出现在 deai 输出且解析不报错。

验证：deai 输出含 `category: tense` 项，audit 流程无异常。
> 若 audit deai 解析对新 category 敏感（预期不会，泛型解析），在此暴露并最小修正。

---

## 阶段 D — ⑥ reviewer 怀疑点排序（paper-audit）

1. 新建 `paper-audit/references/REVIEWER_PSYCHOLOGY.md`（design 4.1）：阅读路径 + 8 层怀疑序 + 找不到 reject 策略 + reviewer 类型。通用学术/CS 语境。
2. `agents/critical_reviewer_agent.md`：新增"按 8 层怀疑序优先 critique"节，引用新文档。
3. `agents/synthesis_agent.md`：合并/roadmap 时按怀疑层级加权（与 severity 协同）。
4. 登记：`SKILL.md` / `AUDIT_GUIDE.md` references 清单加 `REVIEWER_PSYCHOLOGY.md`。

验证：人工通读；`grep` 确认 agent 文件引用路径无悬挂。
回滚点：`git checkout -- <REVIEWER_PSYCHOLOGY.md, 2 agents, SKILL/AUDIT_GUIDE>`。

---

## 阶段 E — ① over-claim 进 paper-audit 维度

1. 新建 `paper-audit/references/OVER_CLAIM_GUARD.md`（design 5.1，镜像 en evidence 版，paper-audit 视角）。
2. `references/SUBAGENT_TEMPLATES.md`：`claims_vs_evidence` lane 加 over-claim DO 项（发 `claim_accuracy`，给 allowed/forbidden_wording）。
3. `agents/claims_evidence_reviewer_agent.md`：扩成显式核查 over-claim 措辞。
4. `references/CHECKLIST.md`：加 over-claim 判据条目。
5. 登记：`SKILL.md` references 清单加 `OVER_CLAIM_GUARD.md`。

验证：人工通读；确认 lane/agent 引用一致、与 `CLAIM_EVIDENCE_CONTRACT.md` 边界互链。
回滚点：`git checkout -- <OVER_CLAIM_GUARD.md, SUBAGENT_TEMPLATES, claims_evidence agent, CHECKLIST, SKILL>`。

---

## 阶段 F — SKILL.md 收尾

1. en/zh/typst SKILL.md：references 清单登记 ⑤ tense 文档；更新 `last_updated`。
2. paper-audit SKILL.md：登记 ⑥① 文档（若 D/E 未登记）；更新 `last_updated`。
3. **确认 4 处 `version` 未变**：`grep -n "^version" <4 SKILL.md>` 与 `pyproject.toml` 比对一致。

回滚点：`git checkout -- <4 SKILL.md>`。

---

## 阶段 G — 全量校验与收尾

1. `just fix`（ruff format + --fix）。
2. `just ci`（lint → typecheck → test）**全绿**。
   - 既有 deai 快照被新 tense trace 打破 → 摸清后更新期望值（确认是预期新增非回归）。
3. 验收清单逐条核对 prd.md。
4. 范围核对：`git diff --name-only` 不含 `bib-search-citation/`、`cover-letter/`；未动任何 `parsers.py`、未动 `scholar_eval.py` 权重。
5. 确认 4 处 SKILL.md `version` 未变、`last_updated` 已更新。

## 提交

- 按子交付物或技能切分 commit（scoped conventional commits），或单 commit
  `feat(skills): tense signal检测 + paper-audit reviewer心理学/over-claim维度`。
- 含 `[AI]` 标记与 Why 行；不自动 push（等用户确认）。

## 校验命令速查

```bash
just ci
uv run --extra dev python -m pytest tests/test_deai_tense.py -q
uv run --extra dev python -m pytest -q -k "deai or tense"
git diff --name-only        # 范围核对
grep -n "^version" academic-writing-skills/*/SKILL.md   # version 未 bump
```
