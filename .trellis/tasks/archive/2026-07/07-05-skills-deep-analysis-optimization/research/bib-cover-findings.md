# Research: bib-search-citation + cover-letter deep audit

- **Query**: 深入分析两个 skill 的现存问题（脚本正确性、红线合规、SKILL.md 契约、集成缺口、测试盲区）
- **Scope**: internal
- **Date**: 2026-07-05
- **Baseline**: 2026-06 五技能优化 + 六技能复审已完成，旧问题（B1-B26/C1-C4 等）已清零。本轮只报告**新发现的、有可复现证据**的问题。测试基线：`tests/test_cover_letter_*` + `bib-search-citation/tests/` 共 72 passed（本轮实跑）。

## Findings

### bib-search-citation

#### BIB-1 (medium) — 重复引用键被静默当作两条独立结果返回，无警告
- **文件**: `academic-writing-skills/bib-search-citation/scripts/search_bib.py:777-857`（`parse_bib_entries`）、`892-908`（`inherit_crossref_fields` 只在 `by_key` 里保留最后一条）
- **问题**: 一个 `.bib` 里出现两条同 key 的条目时，`parse_bib_entries` 无条件 `entries.append(...)` 两条；没有去重也没有 `parse_warning`。重复 key 在真实 LaTeX 编译里是错误（`bibtex` 会 warning、`biber` 会 error）。用户搜索时会拿到两条打印为**完全相同** `\cite{Smith2020}` 的结果，却不知道自己的库是坏的。
- **证据（实测 /tmp/dup.bib，两条 `@article{Smith2020,...}`）**:
  ```
  Smith2020 | Duplicate Key Second
  Smith2020 | First Definition
  === 导出引用 ===
  Smith2020 \cite{Smith2020}
  Smith2020 \cite{Smith2020}
  ```
- **建议方向**: 在 `parse_bib_entries` 结束时统计 key 频次，对出现 >1 次的 key 追加一条 `{"type":"duplicate_key","key":...}` 到 warnings（与现有 `unbalanced_entry` / `unknown_field_filter` 同机制）。crossref 已经暗示"最后一条胜出"，warning 能让用户知情。

#### BIB-2 (low) — `%` 行注释掉的条目仍被解析为有效条目
- **文件**: `academic-writing-skills/bib-search-citation/scripts/search_bib.py:793-801`（`parse_bib_entries` 直接 `content.find("@")`，不识别行首 `%`）
- **问题**: 一行 `% @article{Commented2019, ...}` 会被当作正常条目解析并可被搜索/引用。这在**纯 BibTeX 语义上其实是"正确"的**（`.bib` 里 `%` 不是注释符，`@` 无论前面有什么都会触发条目），但与大量用户/工具（JabRef 等常用 `%` 临时禁用条目）的直觉相反。风险：用户以为已禁用的条目重新出现在检索/引用里。
- **证据（实测）**: 对含 `% @article{Commented2019,...}` 的文件搜 `parsed` → `returned 1 / Commented2019`。
- **建议方向**: 二选一——(a) 文档化"本工具与真实 BibTeX 一致，`%` 不禁用条目，请删除或用 `@comment{}` 包裹"；(b) 当某条目起始 `@` 与行首之间只隔一个 `%` 时，追加一条 `commented_entry_included` 的软 warning。倾向 (b)，与"malformed 时如实报告"的既有安全边界一致。

#### bib：已核查、未发现问题的维度
- `@string` 宏展开 + `#` 拼接（`resolve_field_value`/`_resolve_value_atom`）、crossref 继承（`inherit_crossref_fields`）、大括号/引号嵌套（`is_balanced`/`split_top_level`/`_scan_entry_span` 的 `in_quotes` 处理）、LaTeX 重音折叠（`expand_latex_accents`/`ascii_fold`）、latin-1 回退、截断条目 resync、非 ASCII 键名（`typst_citations` 用 `re.fullmatch` 走 `needs_label` 分支、`latex_citations` 原样包裹）——均有对应测试且逻辑正确。
- 搜索排序（`score_entry`/`sort_results`）逻辑自洽：短语命中加权、`year_desc` 用 `-1` 哨兵让无年份排最后、relevance 阈值 `score>0` 过滤 + B3 recency 不泄漏。未发现排序 bug。
- 次要：标准月份宏 `jan..dec` 未预置（`month = jan` 保持 "jan" 不展开成 "January"）。对检索/venue/年份推导无影响（`entry_year` 只读 year/date），仅列为观察项，不建议改动。

### cover-letter

#### CL-1 (medium) — align-check 数值校验存在"指标张冠李戴"泄漏
- **文件**: `academic-writing-skills/cover-letter/scripts/verify_letter_against_manuscript.py:57-100`（`_has_numeric_match`），下游 `align_check.py:105-127`（`_has_scope_or_wording_risk`/`candidate_to_issue`）
- **问题**: 邻近窗口校验只要求 claim 里**任意一个** metric 关键词与该数字在稿件窗口内共现即判 `verified`。因此投稿信可以把稿件的数字**安到另一个指标上**仍通过校验：只要两句共享一个泛化词（improvement / reduction）。端到端后果：该 claim 在 align-check 里 strength 停在 `observed`、无 strong 措辞、有 anchor → `_has_scope_or_wording_risk=False` → **不产生 finding**，over-claim 漏网。
- **证据（实测）**: 稿件只测了 "3% **accuracy** improvement"；投稿信写 "3% **throughput** improvement" →
  ```
  verified= True  confidence= medium  | We report ... 3% throughput improvement ...
  unverified_count= 0
  ```
  （"improvement" 落在 "3%" 的 160 字窗口内即命中，"throughput" 被忽略）
- **影响边界**: 已被降级为 `confidence=medium`（非 high），且只在"数字确实存在于稿件 + 共享一个泛化动词"时发生；SOTA/部署/金额类硬 over-claim 仍被正确拦截（下方 CL 已核查项有实测）。
- **建议方向**: 令邻近窗口不仅要求"数字附近有某个 claim 关键词"，还要求**紧贴该数字的那个指标词在稿件与投稿信中一致**（例如取数字后≤N 词的 head noun 对比），或对"数字命中但主指标词不一致"的情况保留 finding / 进一步降置信并加 caveat。现有测试 `test_align_check_numeric_match_requires_local_cooccurrence`(C4) 只覆盖"数字与关键词相距过远"，未覆盖此"同数字异指标"情形。

#### CL-2 (low) — 句子切分把称呼语粘进首个 claim 句
- **文件**: `academic-writing-skills/cover-letter/scripts/build_letter_claim_map.py:64-66`（`split_sentences` 在 `[.!?]` 后切分）
- **问题**: "Dear Editor," 以逗号结尾，不被切开，导致首条 claim 句变成 `"Dear Editor,  We propose ..."`。属外观/引用文本膨胀，会让 finding 的 `quote` 带上称呼语。目前不影响检测正确性（`STRONG_CLAIM_PATTERN` 非 `^` 锚定；opener-cliché 走 presubmission 的按行 visible 文本，另一条路径）。
- **证据（实测 over.md）**: finding 的 quote = `"Dear Editor,  We propose a new framework for widget forecasting that achieves state-of-the..."`
- **建议方向**: `split_sentences` 前先剥掉行首 `Dear ...,` 称呼行，或按空行分段后再切句。低优先。

#### CL-3 (enhancement) — 缺结构级 AI 痕迹检查，AI-tone 阈值偏宽
- **文件**: `academic-writing-skills/cover-letter/scripts/presubmission_check.py:292-311`（`_scan_ai_tone`，`len(matches) < 3` 才不报）
- **缺口**: 同一 AI-tone 词需出现 **3 次以上**才触发。在 ~300 词投稿信里，词汇多样的 AI slop（每个词各 1 次）会整体漏过。en/zh/typst 已于 2026-06-20 加入结构级 AI 痕迹检查（zh 为 `ChineseAITraceChecker`），cover-letter 作为写作类 skill 无对应结构级检查，仅有逐词频次 + 固定黑名单短语。
- **建议方向**: 标记为 enhancement（非 bug）。可移植 en/typst 的结构级 AI 痕迹思路，或把 AI-tone 单词阈值在短文本下调低。

#### CL-4 (enhancement) — 无"投稿信 ↔ 稿件 AI 披露一致性"交叉检查
- **文件**: `academic-writing-skills/cover-letter/scripts/presubmission_check.py:154-162`（`ai_disclosure` 仅在**信内**做存在性检测，由模板 `required_declarations` 驱动）
- **缺口**: 只判断信里有没有 AI 披露语句，不核查其与稿件里 AI 披露的一致性。cover-letter 本就通过 `extract_manuscript_facts` 读稿件，具备做一致性检查的输入。结合 2026-06 en/zh 已引入 AI 披露意识，这是一个功能缺口（enhancement）。
- **建议方向**: 标记 enhancement。可在 align/presubmission 增补：若稿件含 AI 披露而信中无（或反之），给一条 moderate 提醒。属能力增强，非现存 bug。

#### cover-letter：已核查、未发现问题的维度
- **红线（捏造）**: `generate` 草稿（`cover_letter.py:67-85` `_draft_cover_letter`）只填入 `extract_manuscript_facts` 抽取的 title/contributions/corresponding_author，缺失字段用占位符（`[...to be confirmed]`），未见凭空生成作者/venue/结论。SKILL.md 安全边界明确禁止捏造并要求占位符。
- **over-claim 拦截（正向实测）**: 对 over-claiming 信（SOTA + "deployed across 12 facilities" + "$2M cost savings"），align-check 产出 2 条 finding（major/unsupported 的 SOTA 句 + moderate/observed 的部署金额句），符合预期。
- **输入校验**: 各 mode 的 `_require_path`/`.tex` 后缀校验/venue `choices` 校验齐全（`cover_letter.py`、`journal_fit_check.py:428`、`extract_manuscript_facts.py:293`）。多文件稿件经 `tex_loader.assemble` 展开 `\input/\include` 后再抽取，避免 skeleton 主文件导致 facts 空。
- **journal-fit**: 10 个 venue + generic 的 scope 关键词表（`_check_scope_fit`）与 `VENUES` 完备对齐；overall = 最差子轴；HIGH/MEDIUM/LOW → severity/priority 映射一致。属启发式，SKILL.md 已标注为 `[Script]` 框架提示而非编辑判断。
- **align-check 保守降级**: `verify_claim_candidates` 对无法锚定的 strong/supported 一律降到 observed（偏向报出），不会因降级掩盖 over-claim（除 CL-1 的窄泄漏外）。

### SKILL.md 契约 & 集成
- **版本**: 6 个 SKILL.md `version` 全为 `5.2.0`，与 `pyproject.toml` 一致（符合 memory 的"全仓同步"规则）。两 skill `last_updated: 2026-06-13`。
- **references 断链检查**: cover-letter SKILL.md 引用的 7 个 `references/*.md` 全部存在；bib SKILL.md 引用的 scripts/references/examples 全部存在。未发现断链。
- **跨 skill 路由**: cover-letter → `latex-paper-en`/`latex-thesis-zh`/`paper-audit`/`bib-search-citation` 的"Do Not Use"路由链接均指向真实 skill 目录；`bib-search-citation` 被 cover-letter 正确引用为"库检索/引用核对"出口。无反向断链。
- **参数一致性**: 两 skill 的 `argument-hint`/Module Router 命令与脚本实际 `argparse` 参数一致（含 `--journal/--venue` 别名、`--mode` choices、`--query/--spec-json/--spec-file` 互斥组）。

## 测试盲区
- **BIB**: 无重复 key 测试（BIB-1）；无 `%` 行注释条目测试（BIB-2；现有 `test_comment_and_string_are_not_phantom_entries` 测的是 `@comment{}` 块，非 `%` 行注释）；无月份宏测试（低价值）。
- **cover-letter**: 无"同数字异指标"泄漏测试（CL-1；`test_align_check_numeric_match_requires_local_cooccurrence` 只覆盖"数字与关键词相距过远"，其 line 185 的 sanity 恰恰演示了同款宽松性）；无称呼语粘句测试（CL-2）；无 AI 披露一致性 / 结构级 AI 痕迹测试（CL-3/CL-4，因功能尚未实现）。

## 严重度汇总（按严重度排序）

| 编号 | 严重度 | 位置 | 一句话 |
|---|---|---|---|
| CL-1 | medium | verify_letter_against_manuscript.py:57-100 + align_check.py:105-127 | 邻近窗口只需任意关键词共现，投稿信可把稿件数字张冠李戴到别的指标仍通过校验且不被 flag（已实测，confidence 已降为 medium 限制影响） |
| BIB-1 | medium | search_bib.py:777-857 | 重复引用键被当两条独立结果静默返回，无 duplicate_key warning |
| BIB-2 | low | search_bib.py:793-801 | `%` 行注释掉的条目仍被解析（与真实 BibTeX 一致但违反用户直觉），可能让已禁用条目重现 |
| CL-2 | low | build_letter_claim_map.py:64-66 | 句子切分把 "Dear Editor," 粘进首个 claim 句，仅膨胀 quote |
| CL-3 | enhancement | presubmission_check.py:292-311 | AI-tone 需同词 3+ 次才报，且无 en/zh/typst 那种结构级 AI 痕迹检查 |
| CL-4 | enhancement | presubmission_check.py:154-162 | 只查信内 AI 披露有无，无"信 ↔ 稿件 AI 披露一致性"交叉检查 |

## Caveats / Not Found
- 未发现任何**捏造 bibliography/作者/venue/结论**的红线违规；两 skill 的安全边界文档与实现一致。
- CL-1 是本轮唯一有实测证据的红线相邻（over-claim 泄漏）问题，但影响被 medium 置信度与"需共享泛化动词"的条件收窄；不是无条件放行。
- 未逐一验证每个 venue 模板 body 的措辞正误（属外部事实，2026-06 已核实），本轮只验证 frontmatter 被 `template_meta` 正确解析、脚本据其判定。
