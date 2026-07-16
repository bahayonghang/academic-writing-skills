# bib查询解析健壮性修复 — 实施清单

约定：tests-first——每批先写会失败的测试，确认红，再实现，确认绿。所有测试新增在
`academic-writing-skills/bib-search-citation/tests/test_bib_search.py`（沿用其 subprocess helper 与
`sys.path` 导入约定，可 `importlib.import_module("search_bib")` 做单元级断言）。

**全程不做 git commit——所有分组留到 Phase 3.4 统一展示确认。** 每批次收束为一个拟提交分组
（记录文件集 + 拟用 message，= 回滚单元）；需回退某批次时用 `git checkout -- <该批次文件集>`
（本批新增文件直接删除）或 `git stash` 暂存排查，不依赖 commit 回退。

统一验证命令（先跑过路径核实：justfile `test` 通过 glob `academic-writing-skills/*/tests` 收录本目录，与下述命令等价覆盖本技能）：

```bash
uv run --extra dev python -m pytest academic-writing-skills/bib-search-citation/tests -q
```

## 批次 0：基线确认

- [ ] 记录基线：上述命令当前 **28 passed**（2026-07-15 实测）。
- [ ] 确认 `just check-versions` 状态：若 A-REL-1（07-15-audit-fix-version-ci）尚未落地则预期红，与本任务无关，记入任务 notes；后续「就地验证」用 lint/typecheck/test 三步替代 `just ci`。

## 批次 1：D-3（A-BIB-3）+ D-4（A-BIB-4）纯匹配逻辑

- [ ] 写测试（预期红）：
  - `test_has_code_word_boundary_negatives`：`search_bib.has_code({"note": t})` 对 `"reported results"` / `"encoder-decoder"` / `"barcode"` / `"we encode the signal"` 均 False。
  - `test_has_code_word_boundary_positives`：`"code available"` / `"github.com/x"` / `"source code released"` / `"CodeAvailable"` 均 True。
  - `test_has_code_fixture_flags_stable`：library.bib 端到端 `--query "forecasting has:code sort:title limit:5"` 返回集与修复前一致（Doe/Roe/Lee 三条，flags.code 全 True）。
  - `test_year_disambiguation_suffix`：单元 `entry_year({"year": "{2024a}"}) == 2024`、`entry_year({"year": "{20245}"}) is None`；端到端 tmp_path bib `year={2024a}` + `--query "widget year>=2024"` 能返回该条目。
- [ ] 验证红：`uv run --extra dev python -m pytest academic-writing-skills/bib-search-citation/tests -q -k "has_code or disambiguation"`
- [ ] 实现：`CODE_HINT_TERMS` 增 `codeavailable`；新增编译 `CODE_HINT_RE`；`has_code` 改 `CODE_HINT_RE.search`；`YEAR_RE` 改 `\b(1[5-9]\d{2}|20\d{2})[a-z]?\b`；`entry_year` 取 `group(1)`。
- [ ] 验证绿 + 全量本技能测试绿。
- [ ] **拟提交分组 1（回滚单元）**：记录本批次文件集，拟用 message `fix(bib-search-citation): word-boundary has:code terms and year disambiguation suffix (A-BIB-3, A-BIB-4)`，留待 Phase 3.4。

## 批次 2：D-1（A-BIB-1）+ D-5（A-BIB-5）compact query 解析

- [ ] 写测试（预期红）：
  - `test_unbalanced_quote_query_falls_back_with_warning`：`--query "children's early language forecasting"` exit 0；`meta.parse_warnings` 含 `type == "query_tokenizer_fallback"`；`meta.query` 含 `children's`；meta 无 `_query_warnings` 键。
  - `test_fallback_keeps_double_quoted_phrases`：`--query "children's forecasting" + --claim 不参与`，改用 query 内 `claim:"low latency"`，断言结果 `claim_support.claim == "low latency"`（回退模式短语分组仍有效）。
  - `test_balanced_quotes_unchanged`（回归锁）：`--query 'forecasting claim:"low latency" limit:2'`（无孤立引号）exit 0 且 `meta.parse_warnings` 中**无** `query_tokenizer_fallback`。
  - `test_noninteger_control_values_raise_spec_error`：`limit:abc` / `recent:x` / `year:20x4` 三个 query 各 exit 2，stderr JSON `error` 含 `must be an integer`。
- [ ] 验证红（`-k "fallback or noninteger or balanced_quotes"`）。
- [ ] 实现：`_FALLBACK_TOKEN_RE` + `_fallback_tokenize`；`spec_from_compact_query` try/except + `spec["_query_warnings"]`；`main()` pop 并前置拼入 `extra_meta["parse_warnings"]`；`_parse_int` helper 替换 :565/:576 与 `parse_year_filter` 三处 `int()`。
- [ ] 验证绿 + 全量本技能测试绿（重点看 `test_nonpositive_limit_is_rejected` 未受措辞影响）。
- [ ] **拟提交分组 2（回滚单元）**：记录本批次文件集，拟用 message `fix(bib-search-citation): tolerant query tokenizer fallback and SpecError for non-integer values (A-BIB-1, A-BIB-5)`，留待 Phase 3.4。

## 批次 3：D-2（A-BIB-2）preview warnings

- [ ] 写测试（预期红）：
  - `test_preview_renders_parse_warnings_from_broken_bib`：broken.bib 搜索输出管道进 preview，断言含 `Warnings (` 与 `[unbalanced_entry]`。
  - `test_preview_renders_per_result_duplicate_warning`：复用 duplicate-key tmp bib（同 `test_duplicate_keys_warn_and_annotate_results` 构造），preview 断言条目块内含 `Warning: duplicate_key`。
  - `test_preview_truncates_long_warning_list`：手工构造含 7 条 parse_warnings 的 payload，断言恰好 5 条 `  - [` 行 + `... and 2 more`。
  - `test_preview_encoding_fallback_line`：构造 `meta.encoding_fallback = "latin-1"` payload，断言 `Encoding: latin-1 fallback` 行。
  - 回归锁：在 `test_preview_from_stdin_renders_summary_and_hides_raw_bib` 增补断言 `"Warnings" not in preview`（干净输入零变化）。
- [ ] 验证红（`-k preview`）。
- [ ] 实现：`preview_bib_search.py` 增 `WARNINGS_LIMIT = 5`、`WARNING_TEXT_LIMIT = 200`、`render_warnings(meta)`；`render_preview` 在 filter 行后拼接；`render_entry` 末尾渲染 per-result `warnings`。
- [ ] 验证绿 + 全量本技能测试绿。
- [ ] **拟提交分组 3（回滚单元）**：记录本批次文件集，拟用 message `fix(bib-search-citation): surface parse and per-result warnings in preview (A-BIB-2)`，留待 Phase 3.4。

## 批次 4：D-6（A-BIB-6）文档 + 警告扩展，及 D-3 残留局限文档

- [ ] 写测试（预期红）：
  - `test_colon_free_text_hint_in_unknown_field_warning`：`--query "signal genotype:phenotype"` exit 0，`meta.parse_warnings` 中 `unknown_field_filter` 条目 message 含 `replace the colon with a space`，`type` 不变。
  - `test_numeric_colon_token_stays_free_text`（表征锁，按实测事实）：`--query "meeting 10:30 forecasting"` 的 `meta.query` 含 `10:30`，`applied_filters` 为空。
- [ ] 验证红（`-k colon`）。
- [ ] 实现：扩展 `_field_filter_warnings` message（含首个 needle 的示例 token，空列表回退）；`query-syntax.md` Edge cases 增「Colons in free text」小节；`limitations-and-errors.md` 增 has:code 词边界启发式残留（语义否定、泛词）、tokenizer 回退语义、year 消歧后缀三点。
- [ ] 人工核对：文档描述与代码行为逐条对照（尤其 `10:30` 按实测写「不受影响」，勿照抄父登记表）。
- [ ] 验证绿 + 全量本技能测试绿。
- [ ] **拟提交分组 4（回滚单元）**：记录本批次文件集，拟用 message `fix(bib-search-citation): colon free-text guidance and warning hint (A-BIB-6)`（docs 改动与代码同一分组，保持行为-文档原子性），留待 Phase 3.4。

## 收尾与评审门

- [ ] `uv run --extra dev ruff format . && uv run --extra dev ruff check --fix .`（即 `just fix`），复查 diff 无越界文件（仅 bib-search-citation 目录 + 本任务目录）。
- [ ] `just lint` / `just typecheck`（pyright 看 **error 数**，basic 模式下 error 会卡 CI）。
- [ ] 全量测试：`just test`（root tests/ + 各技能 tests/ 全绿；关注 tests/contracts 未受影响——本任务未动 SKILL.md）。
- [ ] `just ci`：A-REL-1 已落地，版本门应绿；两份 source reference 的 manifest/双语目标同步按
  用户范围红线留给终批 `audit-release-integration` R4a，因此本任务记录
  `test_manifest_matches_live_public_inventory` 与 `test_inventory_only_cli_passes` 两项预期红，
  确认两者同属 source hash 同步原因，除此之外 lint/typecheck/test 全绿。
- [ ] 评审门（trellis-check 或人工）：
  1. 每个 A-BIB 发现 ↔ 至少一个新测试，映射写进各拟提交分组的 message 草稿 / PR 描述；
  2. 错误面契约表（design.md）逐行抽查复现；
  3. 无 warnings 输入的 preview 输出与基线逐字节 diff 为空；
  4. SKILL.md 与 evals.json 零改动（evals.json 有格式化 hook 陷阱，本任务不触碰）。
- [ ] 更新 task notes：记录与父 PRD 的两处偏差（`10:30` 示例不成立；`codeavailable` 词表补项）供父任务集成阶段回写登记表。
