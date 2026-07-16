# cover-letter 声明与事实匹配精度（A-CL-1 … A-CL-11）

## Goal

修复父任务 `07-15-skills-deep-audit-opt` 登记表中 cover-letter 技能的 11 项发现：
journal_fit claim 计数误报 LOW（A-CL-1）、`.tex` 注释被当活 claim（A-CL-2）、数字单位裸 `s`
误配（A-CL-3）、方向词-only 宽松分支可误配（A-CL-4）、长度双报无 dedup（A-CL-5）、顶刊
scope_fit 系统性 LOW（A-CL-6）、`_extract_title_local` fork 待删（A-CL-7，阻塞）、
`_exit_code` 混类型脆弱（A-CL-8）、`source_section` 硬编码（A-CL-9）、自定义模板缺 tier
静默回退（A-CL-10）、通讯作者模式覆盖缺口文档化（A-CL-11）。

## 范围与非目标

- 只改 `academic-writing-skills/cover-letter/` 下的 scripts / references，及 `tests/skills/cover_letter/` 测试。
- **不改** `scripts/parsers.py` / `scripts/tex_loader.py`（vendored 副本，归 latex-paper-en 任务 + ALIGNMENTS 哈希锁管）。
- **不改** SKILL.md 的 `version` / `last_updated`（父任务 D1/D6：版本归 version-ci 子任务，last_updated 归集成阶段）。
- **不改** evals/evals.json（新测试夹具用 tmp_path 内联合成，不新增 evals 条目）。

## 依赖与顺序（硬约束）

1. **前置**：`07-15-audit-fix-version-ci`（A-REL-1）已恢复绿基线后开工。
2. **A-CL-7 阻塞依赖**：只在 `07-15-audit-fix-latex-paper-en` 落地 **A-EN-10**（canonical
   `parsers.extract_title` 平衡花括号修复，见 cover-letter 副本 `scripts/parsers.py:605` 现存
   非贪婪 `\{(.+?)\}`）**并完成三副本（en/audit/cover-letter）重同步**之后执行。规划为最后
   一个批次，批次入口显式检查 cover-letter 副本已同步（`tests/contracts/test_parsers_alignment.py` 绿）。
3. 其余 10 项与兄弟任务无耦合，可先行。

## Requirements 与验收标准（每项含回归测试，Low 也不例外）

### A-CL-1（High）journal_fit `_count_claims` 复用 `extract_claims`

`journal_fit_check.py:106-113` 只数 `\bwe (report|present|...)\b`，漏掉 `our work
demonstrates` / 纯数值句等 `LETTER_CLAIM_PATTERNS` 覆盖的真 claim，导致 evidence_density
假 LOW → 整体 LOW exit 2。

- [ ] `_count_claims` 改为 `len(build_letter_claim_map.extract_claims(text))`（bare import，与本目录既有 `from parsers import LatexParser` 同风格）。
- [ ] `TIER_BUDGETS`（journal_fit_check.py:43-47）数值不变；语义由"第一人称 report 动词句"改为"claim-bearing 句"，在 docstring 与 `references/MODE_GUIDE.md:95`（heuristic limitations 段）同步改述。
- [ ] 校准测试：`evals/fixtures/journal_fit_fixture_letter.md` + nature → evidence_density 为 HIGH（2 条 claim ∈ [2,5]）；`align_check_fixture_letter.md` + ieee-trans → HIGH（5 条 ∈ [3,6]）。
- [ ] 回归测试：4 条非 "we report" 风格真 claim 的合成信不再判 LOW；零 claim 信仍 LOW。

### A-CL-2（High）`.tex` letter 在 claim 抽取前剥 `%` 注释

`build_letter_claim_map.py:307`（main 原文直读）与 `align_check.py:304→311`
（run_align_check 原文直读后进 build_claim_map）不剥注释；`_strip_tex_comments` 已存在但
只用于 disclosure（align_check.py:242-243）。样板：`presubmission_check._strip_latex_comment/_line_views`（:197-224）。

- [ ] 剥注释函数单源化：公开 `strip_tex_comments` 收敛到 `build_letter_claim_map.py`，`align_check.py` 改为 import（disclosure 路径行为不变）。
- [ ] 两条 claim 管道入口在 `suffix == ".tex"` 时前置剥注释；`.md` letter 完全不受影响（`%` 是正文百分号）。
- [ ] 测试：`.tex` 信中 `% Our work demonstrates a 99\% reduction ...` 注释行不产生 claim 候选与 finding；活行内 `47\%`（转义）保留；`.md` 信含 `%` 的 claim 抽取不变。
- [ ] 说明：journal-fit 的 `.tex` 读取走 `LatexParser.clean_text`（parsers.py:339 已剥注释），不在本项范围内，design 记录即可。

### A-CL-3（Medium）数字+单位正则三处统一，单位加词边界

`verify_letter_against_manuscript.py:82` 单位含裸 `s`（"3 seconds" 与 "3 sensor streams"
同被捕成 needle `3 s` 互相误配）；`build_letter_claim_map.py:46` 同病；
`extract_manuscript_facts.py:257` 无 `s` 但接受 `\%`，三处集合不一致。

- [ ] 单源常量 `NUMBER_UNIT_PATTERN` 定义于 `build_letter_claim_map.py`（该文件已是 `STRONG_CLAIM_PATTERN` 的单源，见 align_check.py:30-31 注释），verify/extract 两处 import。
- [ ] 词字符单位（pp/x/ms/s/seconds/MB/GB/FLOPs）加 `\b`；`%`、`×` 为非词字符不加；保留 `\\?%` 接受 LaTeX 转义。
- [ ] 枚举测试对："3 seconds" 命中、"3 sensor streams" 不命中（双向：claim 侧与 manuscript 侧）、"47 ms"/"5 GB"/"2.1x" 命中、"3 ppm" 不再误命中 `pp`。
- [ ] `LETTER_CLAIM_PATTERNS`（build:26-27，无裸 `s`，语义是"数字+方向动词"触发器）**有意不并入**，design 记录分歧理由。

### A-CL-4（Medium）收紧方向词-only 数值验证分支（CL-1 家族）

`_SPECIFIC_METRIC_RE`（verify:39-43）不含 reduction/improvement，而 `metric_keywords`
（verify:90-95）含 → 方向词-only claim 落入 `elif keywords:` 宽松分支，方向词只要出现在
数字 ±160 字符（`_NUMERIC_WINDOW`）内即可判通过。

- [ ] 新增 `_DIRECTION_RE`（reduction|improvement）与 `_DIRECTION_WINDOW = 60`：claim 内紧邻数字（±`_CLAIM_METRIC_WINDOW`=40）的方向词，必须出现在 manuscript 中该数字 ±60 字符内。
- [ ] fixture 测试：manuscript 为"数字与 improvement 相距 60~160 字符且描述不相干对象"→ 判 False；`_has_numeric_match("47% reduction", "we report a 47% reduction in latency")` 保持 True（既有 pinned 断言）。
- [ ] 不得回退 CL-1 既有硬化（见下方 must-stay-green）。

### A-CL-5（Medium）optimize 工作流长度双报抑制其一

`journal_fit_check.py:288`（word_limit×1.20 → LOW）与 `presubmission_check.py:633-634`
（ratio≥1.20 → Major L1）读同一 template `word_limit`。CLI `--mode optimize`
（cover_letter.py:183-201）只跑 presubmission+align，双报发生在 MODE_GUIDE:123 建议的
"optimize + 可选 journal-fit"组合工作流。

- [ ] 胜出方 = presubmission `L1`（两档细阶梯 Minor/Major、带精确超字数、optimize 恒跑）。
- [ ] `journal_fit_check.py` 与 `cover_letter.py` 新增 `--dedup-length`（默认关，单独跑 journal-fit 行为零变化）；开启时 `_check_format_compliance` 跳过字数子检查（banned phrases 保留），evidence 注明"length delegated to presubmission L1"。
- [ ] `references/MODE_GUIDE.md` Mode 2 注明：optimize 会话中追加 journal-fit 时带 `--dedup-length`。
- [ ] 测试：超长信 nature，flag 开 → 无长度轴 LOW finding 且 banned-phrase 检查仍生效；flag 关 → 与现行为一致。`tests/skills/cover_letter/test_cover_letter_scripts.py::test_mode_guide_flags_all_exist_in_cli` 必须继续绿（文档新 flag 必须真实存在于 `cover_letter.py` parser）。

### A-CL-6（Medium）顶刊 scope_fit 校准 + "broad scientific" 双计分

`_check_scope_fit`（journal_fit_check.py:116-167）对所有 venue 要求 2 hit 才 HIGH；顶刊
350 词预算（templates/nature.md:4）下系统性 LOW。且 "broad scientific" 同时出现在 nature
scope 词表（:120）与 novelty `paradigm_signals`（:173-176）→ 一词双计分（原审计 finding 8）。

- [ ] 选定方案：**top-journal tier 1 hit = HIGH**（不扩词表；`_check_scope_fit` 增加 `tier` 参数）；其余 tier 阈值不变。
- [ ] 双计分处置：从 `_check_novelty_framing` 的 paradigm_signals 中移除 `broad scientific`（它是 scope 词汇不是范式动词）；design 声明这是"1 hit=HIGH 方案本身不解决双计分"的补充修复。
- [ ] 校准测试（Nature fixture 基底）：fixture 原文 0 hit → 仍 LOW（`test_journal_fit_classifies_low_for_underframed_nature` 保持绿）；fixture + 一句含 "field"（或 "broad scientific"）→ scope_fit HIGH；mid-journal 1 hit → 仍 MEDIUM。

### A-CL-7（Low，阻塞批次）删除 `_extract_title_local` fork

`extract_manuscript_facts.py:224-240` 为绕过 canonical `extract_title` 截断 bug 而 fork。

- [ ] 入口检查：A-EN-10 已合入且 cover-letter `scripts/parsers.py` 已重同步（对齐锁测试绿）。
- [ ] 验证 canonical `extract_title` 对 `thanks_author_fixture.tex` 的输出：若已剥 `\thanks`/`\footnote` → 整体删 fork 改调 `parsers.extract_title`；若未剥 → fork 缩为"canonical 提取 + `_strip_balanced_commands` 剥 thanks"薄封装并注明残留原因（design 有两分支预案）。
- [ ] must-stay-green：`test_extract_title_strips_thanks_and_keeps_nested_braces`、`test_extract_manuscript_facts_returns_expected_shape`。

### A-CL-8（Low）`_exit_code` 显式按类型分支

`cover_letter.py:38-47`：`getattr(finding, "severity", "") or finding.get(...)` 对
dataclass finding 且 severity 为空串时会走 `.get` 抛 AttributeError。

- [ ] 改为 `isinstance(finding, dict)` 与对象两分支取值。
- [ ] 测试：dict 与 dataclass 混合列表、severity 空串 → 不抛异常且 exit code 正确（major→2 / 非空→1 / 空→0）。

### A-CL-9（Low）`source_section` 按 claim 实际位置映射

`align_check.py:159` 硬编码 `source_section="contributions"`；ISSUE_SCHEMA.md:16 枚举为
`header|opening|contributions|fit|declarations|closing`。管线现状：`split_sentences`
把 `\n` 压成空格、candidate 只带序号 `id: letter:N`，位置信息全程丢失——先补位置，
再按信件真实结构（段落边界 + LETTER_STRUCTURE 结构标记）映射，**不做关键词猜测**。

- [ ] claim candidate 增 `char_offset`（additive 键）：claim 句在分析用 letter 文本中的
  字符偏移（`.tex` 为 A-CL-2 剥注释后文本；定位失败 = -1）。claim_map JSON 与
  AlignCheckIssue JSON 均输出该字段。
- [ ] `source_section` 由 offset + 信件结构定：称呼（`Dear …,`）前 → `header`；称呼后
  第一段 → `opening`；落款行（Sincerely / Best regards 等）起 → `closing`；其余段落或
  offset=-1 → `body`（诚实回退标签）。`contributions`/`fit`/`declarations` 不再由脚本
  产出（纯散文信无结构标记可据，保留给 LLM lane）。
- [ ] `references/ISSUE_SCHEMA.md`：`source_section` 枚举增 `body`；可选字段表增 `char_offset`。
- [ ] 测试：合成信中已知第一段（紧随称呼）的 claim 报 `opening`、中间段 claim 报 `body`；
  issue JSON 输出含 `char_offset` 且 ≥ 0；`source_section` 恒属扩展后枚举。

### A-CL-10（Low）自定义模板缺 tier 输出警告

`journal_fit_check.py:379` `meta.get("tier") or "mid-journal"` 静默回退。

- [ ] `JournalFitResult` 增 `warnings: list[str]`（additive，缺 tier 时写入一条），JSON 与 protocol 渲染均输出；`cover_letter.py` journal-fit payload 透传。
- [ ] 测试：tmp skill_dir 放无 tier 自定义模板 → warnings 非空且 tier 回退 mid-journal；内置 nature → warnings 为空（内置模板由 `test_templates_have_valid_frontmatter` 保证有 tier，默认输出零变化）。

### A-CL-11（Low，doc-only）通讯作者模式覆盖缺口注明

`extract_manuscript_facts.py:47` 只信 `\corresponding(author)?{...}`；IEEE `\thanks` /
acmart `\authornote` 不识别 → 回退第一作者。

- [ ] 在 `CORRESPONDING_AUTHOR_PATTERNS` 注释与 `references/CLAIM_EVIDENCE_CONTRACT.md`（或 MODE_GUIDE generate 段）注明缺口，**并引用 :42-46 既有反捏造决策**（free-text 回退曾把 `\thanks` 内邮箱 local part 报成作者，故意不扩猜测式提取）。
- [ ] 表征测试补一条 acmart `\authornote{Corresponding author...}` → 回退第一作者、不含 `@`（与既有 `test_extract_corresponding_author_never_scrapes_thanks_email` 构成双模板锁）。

## Must-stay-green：既往修复回归锁（改动不得触碰其语义）

CL-1 数值窗口硬化（`tests/skills/cover_letter/test_cover_letter_align_check.py`）：

- `test_numeric_match_rejects_metric_swap`
- `test_align_check_metric_swap_yields_unverified_and_finding`
- `test_align_check_numeric_match_requires_local_cooccurrence`
- `test_align_check_does_not_report_manuscript_supported_observed_metrics`
- `test_align_check_works_with_aligned_letter` / `test_align_check_assembles_multifile_manuscript`

CL-2 称呼剥离：`test_split_sentences_strips_salutation`

CL-3 结构性 AI 痕迹（`tests/skills/cover_letter/test_cover_letter_presubmission.py`）：

- `test_ai_tone_repeat_ladder_two_minor_three_major`、`test_ai_tone_diversity_three_minor_four_major`
- `test_parallel_paragraph_openings_flagged_s1`、`test_uniform_sentence_length_flagged_s2`
- `test_human_letter_fixture_has_no_structural_ai_trace_findings`、`test_ai_slop_letter_fixture_hits_a_structural_trace`
- （记忆锁：AI_TONE 阈值 2/3、DIVERSITY 3/4 是有意取舍，不得顺手"修"）

CL-4 披露一致性（同 align_check 测试文件）：

- `test_align_check_flags_manuscript_discloses_letter_silent` / `..._letter_discloses_manuscript_silent`
- `test_align_check_flags_disclosure_polarity_contradiction`
- `test_align_check_consistent_disclosure_no_finding` / `..._both_silent_no_disclosure_finding`
- `test_align_check_commented_manuscript_disclosure_not_flagged`

契约层：`tests/contracts/test_parsers_alignment.py`（本任务不改 parsers 副本，必须始终绿）、
`tests/contracts/test_skill_contracts.py`（若触碰 SKILL.md 表格；本任务计划不改 SKILL.md）。

## 全局约束（CLAUDE.md 红线 + 仓库约定）

- 勿动 `\cite{}/\ref{}/\label{}`/math 内容；勿捏造数据；输出 diff/suggestion 带 severity/priority、`[Script]`/`[LLM]` 标注的既有协议字段不得破坏。
- 新测试一律 `importlib.util.spec_from_file_location` 按路径加载 + 全量恢复 `sys.path`/`sys.modules`（`SCRIPT_DIR_COVER_LETTER` 是 append 不是 prepend），路径常量只从 `tests.support.paths` 导入；新测试文件含一条加载守卫用例。
- 检查器默认行为变化仅限"误报/假绿修复"例外，须双声明（更新存量单测 + commit message 声明）。
- pytest 命令不加 `PYTHONIOENCODING=utf-8`。

## 验收（任务级）

- [ ] 11 项全部落地（A-CL-11 为 doc+表征测试）。**A-CL-7（Batch 4）完成后本任务方可归档——不设 blocked 完成分支**：终批集成任务禁改行为代码（其 R5），无人可承接遗留；若上游 A-EN-10 尚未落地，本任务保持 in_progress 等待，不得提前归档。
- [ ] `uv run --extra dev python -m pytest tests/skills/cover_letter -q` 全绿；must-stay-green 清单逐条绿。
- [ ] `just ci` 全绿（lint + pyright error 数不升 + 全量测试）。
- [ ] 每个默认行为变化的 commit message 正文含"默认行为变化"声明。
