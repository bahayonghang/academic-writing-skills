# Implement: cover-letter AI 披露一致性 + 结构级 AI 痕迹

前置阅读顺序：`prd.md` → `design.md` → 本文件。研究证据：`../07-05-skills-deep-analysis-optimization/research/bib-cover-findings.md`（CL-3/CL-4 节）。

## 执行清单（按序）

### Step 1 — CL-4 披露一致性 lane（R1 优先）
- [ ] `align_check.py`：新增 `NO_AI_PATTERNS`、`_ai_disclosure_polarity()`、`_sentence_around()`、`_check_ai_disclosure_consistency()`；在 `run_align_check()` claim 循环后调用并追加 issue。模式单源 `from presubmission_check import DECLARATION_PATTERNS`。
- [ ] 稿件/`.tex` 信件逐行剥 `%` 注释后再匹配（防注释披露误报）。
- [ ] 三情形均 `severity="moderate"` / `priority="P2"` / `comment_type="disclosure_consistency"`，字段按 design §1 表。
- [ ] `tests/test_cover_letter_align_check.py` 追加 6 个用例（三情形 + 一致披露不报 + 全无不报 + 注释披露不报）；fixture 文本一律 **raw string**。
- 验证：`uv run --extra dev python -m pytest tests/test_cover_letter_align_check.py -q` 全绿。

### Step 2 — CL-3 阈值 + 聚合 + 结构壳
- [ ] `presubmission_check.py` `_scan_ai_tone`：`>=3` Major/P1 不变；`==2` 新增 Minor/P2。
- [ ] 新增 `_scan_ai_tone_diversity`（code `AI-DIV`）：d=distinct 命中词条数，d≥4 → Major/P1，d==3 → Minor/P2；消息列出词条与次数。
- [ ] 新增 `_scan_parallel_openings`（code `S1`，Minor/P2）：复用 `_paragraphs(views)`，跳过 `Dear` 称呼段；连续 3 段 opening key（前 2 个词 token，lower）相同即报，去重 reported_starts（参照 en `_check_burstiness`，deai_check.py:595）。
- [ ] 新增 `_scan_sentence_length_uniformity`（code `S2`，Minor/P2）：全信 visible text，`[.!?]+` 切句，句数 ≥8 且 CV<0.25 报（参照 en `_check_sentence_length_variance`，deai_check.py:519）。
- [ ] `run_checks()` 注册三个新扫描；`_comment_type_for_code` / `_title_for_code` 补 `S1`/`S2`/`AI-DIV` 分支（→ `"tone"`）。
- [ ] `tests/test_cover_letter_presubmission.py` 追加用例：2 次/3 次同词阶梯、AI-DIV 3/4 档、S1 命中、S2 命中、人写信零误报守卫。
- 验证：`uv run --extra dev python -m pytest tests/test_cover_letter_presubmission.py -q` 全绿。

### Step 3 — 契约文档同步
- [ ] `references/ISSUE_SCHEMA.md`：`comment_type` 枚举 + 语义 + severity guidance 补 `disclosure_consistency`。
- [ ] `references/PRESUBMISSION_RULES.md`：G4 阶梯改述；新增 `AI-DIV`/`S1`/`S2` 规则行、参数与取舍摘要（含不移植 throat-clearing/LID 的理由）。
- [ ] `SKILL.md`：presubmission / align-check 能力描述各补一句；**version 不动**，`last_updated` 已是 2026-07-06。
- [ ] `references/MODE_GUIDE.md`：核对 align-check 段是否列 lane，如列则补。
- ⚠️ SKILL.md 表格改动警惕格式化 hook（ROUTER_ROW_RE 契约测试）。

### Step 4 — evals 样例
- [ ] 新建 `evals/fixtures/ai_slop_letter.md`（3–4 个不同促销词各 1 次 + 3 连平行段首 + 均匀句长）、`evals/fixtures/human_letter.md`（自然人写信）、`evals/fixtures/disclosure_fixture.tex`（含 AI 披露句最小稿件）。
- [ ] 本地实跑确认：ai_slop_letter 至少命中一类结构 trace（S1/S2/AI-DIV），human_letter 上 S1/S2/AI-DIV/AI\* 零命中（验收标准第 2 条）。
- [ ] `evals.json` 追加 #7/#8/#9（design §4）；**必须用 Bash python 读改写，禁 Edit/Write**。
- 验证：`uv run --extra dev python academic-writing-skills/cover-letter/scripts/presubmission_check.py <fixture> --json` 人工核对两个新 fixture 输出。

### Step 5 — 全量验证
- [ ] `just ci`（lint → pyright → 全部测试）全绿；pyright 看 **error 数**（basic 模式，reportOptionalOperand 等是 error）。
- [ ] 确认 `git status` 改动面：仅 `academic-writing-skills/cover-letter/**` + `tests/test_cover_letter_*.py`（验收标准第 3 条：不触 en/zh/typst）。
- [ ] 既有 fixture 若多出新 finding 导致断言失败：先读断言意图，只在"绝无/精确计数"类断言上更新期望，不改 fixture 语义。

## 回滚点
- Step 1 与 Step 2 相互独立，可单独回滚（分别是 align_check.py 与 presubmission_check.py 的纯增量）。
- Step 4 evals.json 追加为数组尾部 append，回滚即删除 #7–#9 三个对象。

## Review gates
- Step 1 后：align-check 三情形 finding 字段完整性（ISSUE_SCHEMA required 七字段）。
- Step 5 后：trellis-check 独立全量质检（对照 PRD 验收三条 + design §5 风险清单）。
