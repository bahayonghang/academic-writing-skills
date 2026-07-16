# 六技能深度审计优化 — 父任务 PRD（v2.1，含规划期实测校正）

## 背景

五路并行深审覆盖六技能 + 共享基础设施，剔除记忆中记录的有意设计决策后形成本发现登记表。v1 规划经 Codex 审阅返工（v2）：修正 1 项已证实误报（原 paper-audit "literature_search import 不存在函数"——`extract_title/extract_abstract` 实际定义于 paper-audit `scripts/parsers.py:632/664`，Typst 链路实测可用），写回版本决策，拆分 typst/bib 子任务，明确 reviewer 处置方案。**v2.1**：六个子任务规划代理实读代码后回报的约 15 处证据/范围校正已整合进登记表（各行以「◆校正」标注），登记表与子任务 design.md 现已一致。**v2.2**（第二轮审阅返工）：父任务转**纯汇总定位**——不再持有任何可执行实施工作，原集成阶段工作全部移入新终批子任务 `07-15-audit-release-integration`；D7 按现场状态改写并加入停放协议；A-EN-3 三脚本回写 EN 子任务、typst 行注释唯一所有权、PA 共识公式定性、A-CL-9 位置保留、六份 implement 提交时点延后至 Phase 3.4 等修正见各子任务工件。

## 已定决策（不再是开放问题）

| ID | 决策 |
|----|------|
| D1 | **版本方向**：六个 SKILL.md 全部升到 `6.0.0`，不回退 `pyproject.toml`。 |
| D2 | **CRITICAL 兼容策略**：canonical schema 保持 `major\|moderate\|minor` 三级；consolidator 将 `CRITICAL` 归一为 `major + gate_blocker=true`，不新增第四级 severity。 |
| D3 | **专项 reviewer**：本轮**移除**未接线的 specialized-agent 承诺（SKILL.md/roster 文案改为与实际 committee+lanes 一致），反谄媚 surrender 协议以最小形态并入 committee/synthesis；完整接线另立任务 `paper-audit-specialized-reviewer-wiring`（显式非目标）。 |
| D4 | **has:code 修法**：不只给 `code` 加词边界——`repo` 子串同样误判（实测 `reported results`/`encoder-decoder` 均 True）。按 CODE_HINT_TERMS 全词表逐词界定匹配语义 + 负例测试。◆校正：词表须补 `codeavailable`（Zotero camelCase tag），否则词边界化令 `library.bib:10,33` 依赖的 `has:code` 端到端结果集回归。 |
| D5 | **verify_bib 修法**：不做单字符正则补丁；改平衡括号/引号扫描器——实施方案为 vendored bib-search-citation 的成熟扫描器（`_scan_entry_span`/`split_top_level`/`parse_bib_entries`）而非自造第三套解析器；fixture 覆盖 `@`、`^`、嵌套花括号（含两层）与 GBK 编码。 |
| D6 | **version-ci 范围**：只做六 SKILL.md 版本对齐恢复绿色基线；`last_updated`、完整 6.0.0 CHANGELOG、发布门禁归终批子任务 `07-15-audit-release-integration`。 |
| D7 | **文档收尾归属**（v2.3 按现场状态改写）：`07-14-refactor-docs-from-latest-skills` 树**已全部归档**（2026-07-15 复核，含全部子任务），无停放/排序依赖，可直接 start version-ci。遗留义务：本树 PA/ZH 等子任务会修改 SKILL.md 路由与能力文案，而 docs 双语契约（`docs-bilingual-resources.md`）明确 **router 变化必须同步双语 usage.md**——单跑资源 checker 捕获不了概览漂移。故六技能双语概览/usage 页与最终 SKILL 路由的**一致性复查及更新**由终批 `audit-release-integration` R4 承担。 |

## 发现登记表（稳定 ID）

每项含证据（file:line + 复现方式）、处置、验证命令；详细设计在各子任务 `design.md`（均已完成撰写）。

### A-REL 发布链（07-15-audit-fix-version-ci，P0，轻量 PRD-only）

| ID | 严重级 | 发现 | 处置 |
|----|--------|------|------|
| A-REL-1 | Critical | 六 SKILL.md `version: "5.3.0"` ≠ pyproject `6.0.0`，`test_skill_versions` 红（复现 6 失配），`just ci` 失败 | fix：按 D1 六处同步。验证：`uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py -q` |
| A-REL-2 | Low | `last_updated` 陈旧；CHANGELOG 缺 6.0.0 段 | 由终批子任务 `audit-release-integration` 承接（见其 prd/implement） |

### A-EN latex-paper-en（07-15-audit-fix-latex-paper-en，P1）

| ID | 严重级 | 发现（证据） | 处置 |
|----|--------|--------------|------|
| A-EN-1 | High | `check_references.py:356` 只读入口文件 → 跨文件 `\ref` 假 P0 exit 1（fixture 复现） | fix：`tex_loader.assemble()` + origin/lineref |
| A-EN-2 | High | `analyze_logic.py:676` 裸 `.lower()` 无别名 → SKILL.md:61 示例 `--section methods` 实跑失败；`analyze_literature.py:68` 同缺陷（◆校正：SKILL.md:62 实际写的是可用的 `--section related`，故 literature 侧是脚本别名缺陷而非文档示例失败） | fix：统一走 `resolve_section_keys` |
| A-EN-3 | High | 系统性多文件盲区：deai_check/analyze_logic/experiment/literature/abstract/check_figures/tables/pseudocode/optimize_title 只读入口文件（grep 证实 0 处 assemble）。◆校正（已裁决并回写子任务）：同型盲区 analyze_grammar/analyze_sentences/improve_expression 三脚本**已纳入**，共十二脚本。◆v2.2 新事实：这四个 writing 模块（含 analyze_abstract）受第三套锁 `test_writing_modules_alignment.py` TIER1_HASH_GROUPS 约束，en/typst 副本须**整文件字节一致**——字节同步使 typst 副本经 `typ_loader.assemble`（API 与 tex_loader 对齐）顺带获得 .typ 多文件装配，已向 typst 子任务声明排重 | fix：接入 `assemble()`，分批见子任务 design（Batch 4a/4b） |
| A-EN-4 | Medium | `split_sections` 不识别 `\begin{abstract}`（SECTION_TITLE_RULES :191-201 只匹配标题式） | fix：LatexParser.split_sections 注册环境区间；en→audit→cover-letter 三副本同步 |
| A-EN-5 | Medium | `deai_batch.py:274` 裸 `.lower()` 与 deai_check 分歧 | fix：同 A-EN-2 |
| A-EN-6 | Medium | SKILL.md:132/:134 重复行 | fix：删一行 |
| A-EN-7 | Low | `check_figures.py:144` 死表达式 `width/3.0` | fix：删除 |
| A-EN-8 | Low | analyze_logic funnel(:220) `"[" in visible` 误判 | fix：收紧判定 |
| A-EN-9 | Low | check_format `_categorize` 仅英文子串 | doc：注明 best-effort |
| A-EN-10 | Low | `parsers.extract_title` 非贪婪截断嵌套花括号（cover-letter 本地 fork 绕过） | fix：canonical 修复（平衡花括号 + `_strip_balanced_commands`，ALIGNMENTS +1 锁行）后三副本重同步；A-CL-7 随后处理 fork |

◆校正（措辞）：ALIGNMENTS 无字面哈希值，是运行时跨副本相等性比较；"更新哈希"实操 = 同步副本字节一致 + 仅在增删共享成员时编辑锁行列表。

### A-ZH latex-thesis-zh（07-15-audit-fix-latex-thesis-zh，P1）

| ID | 严重级 | 发现（证据） | 处置 |
|----|--------|--------------|------|
| A-ZH-1 | High | `parsers.py:183` LaTeX 结论规则锚定 → `结论与展望`/裸`总结` 从不分类（实测）；`SECTION_KEY_ALIASES`(:96) 缺条目。◆校正：Typst(:308) 未锚定规则**能**子串命中 `结论与展望`，症状仅限 LaTeX 侧；Typst 的问题是过匹配+两侧不一致 | fix：统一锚定 `^(?:结论|总结)(?:与展望)?$` + 扩别名（zh 规则不在 ALIGNMENTS 锁内） |
| A-ZH-2 | High | `verify_bib.py:91` `[^^{}]` 丢含 `^` 字段（$L^2$ 假 FAIL 实测）；`:73` `[^@]*?` 丢值含 `@` 整条目（实测 2→1 无警告）。◆校正：`:91` 另只支持一层花括号嵌套，两层同样丢字段 | fix：按 D5 vendored 扫描器（新建 bib_scan.py），一并覆盖 |
| A-ZH-3 | Medium | `verify_bib.py:66` `utf-8 errors=ignore` → GBK 静默乱码 CJK 检查 no-op（实测假 PASS）。◆校正：`check_spec.py:336 _load_bib` 是 `errors="replace"` 非 ignore，但无 GB18030 回退致 CJK 失真的结论不变 | fix：两处改 `tex_loader.read_text_robust` |
| A-ZH-4 | Medium | check_references 多文件输出无文件归属，违反「源文件:行号」契约（12 文件 fixture 实测）。◆校正：per-file 信息已收集（:57/:66 dataclass 字段），缺口仅在 `_add_issue`(:96-112) 落字段与 `_format_issues`(:396-408) 渲染；不切换 assemble（无收益重写），对齐 lineref 输出格式即可 | fix：落字段 + 渲染 |
| A-ZH-5 | Medium | `compile.py:96-109` 中文检测先于 `% !TEX program` → LuaLaTeX 被强制 xelatex；读取 errors=ignore | fix：指令优先 + robust 读取 |
| A-ZH-6 | Medium | `parsers.py:145-147` 标题 `[^}]*` 截断嵌套花括号；extract_title(:417,422) 同因假 PASS | fix：vendored EN `_extract_balanced_block`(:518-538)，contract 锁列表 +`"zh"`（本子任务唯一锁改动） |
| A-ZH-7 | Low | mixed_punctuation 对 `\ref{eq:能量}` 误报 | fix：扩 strip 覆盖 |
| A-ZH-8 | Low | check_consistency(:233-240) 缩写噪声（7 词 stoplist） | fix：扩 stoplist + 最小出现阈值 |
| A-ZH-9 | Low | SKILL.md:67 固定 gb7714(2015)；2025 标准已生效 | doc：路由/MODULE_COMMANDS 注明 `--standard gb7714-2025` 可选（注意字符串锁） |

### A-PA paper-audit（07-15-audit-fix-paper-audit，P1；design 分 W1/W2/W3 三工作流）

| ID | 严重级 | 发现（证据） | 处置 |
|----|--------|--------------|------|
| A-PA-1 | High | consolidator `CRITICAL`→moderate 且 gate_blocker=False，违反「never suppressed」 | fix（W1）：按 D2 `critical→major+gate_blocker=True`（覆盖显式 False） |
| A-PA-2 | High | agent severity/JSON 形状不一致（critical→MAJOR/CRITICAL+description/location；domain 等→Major）→ sanitize 后字段落空 | fix（W1）：模板与 sanitizer 双侧修；字段别名 `description→explanation`、`location→source_section`，禁伪造 quote |
| A-PA-3 | Medium | 专项 reviewer 无派发指令；SKILL.md:207-210 over-promise。◆校正：`apply_frame_lock_advisory` 在 `load_comment_files:125-128` 已接线且有 5 个单测——死的只是生产侧（critical_reviewer 从不被派发） | fix（W2）：按 D3 移除承诺；surrender 协议最小接线进 `committee_logic_agent.md`（dict 输出原生被消费，零脚本改动） |
| A-PA-4 | Medium | editorial_decision_standards(:11-13) 假设 3 reviewer 与 synthesis `ceil(N/2)+1` 矛盾；:101「8-dim」早于 9 维。◆校正：synthesis_agent.md 自身 :30 与 :36（"N-1 of N"）内部矛盾，且 :47/:56/:66/:85 残留四级 severity 枚举，一并纳入 | fix（W2）：统一为**普通多数** `floor(N/2)+1`（N=3→2 票、N=5→3 票，恢复原 standards「2 of 3」意图；原 design 的 `ceil(N/2)+1` 实为超多数且 N=3 时与 CONSENSUS-ALL 退化重合，弃用），synthesis_agent.md:30/:36 一并按此改正 |
| A-PA-5 | Medium | scholar_eval reproducibility 键在从不产出的 `LOGIC+"method"`；evaluate_from_audit 忽略 EXPERIMENT/CITATIONS/BIB/PSEUDOCODE/PRESUBMISSION。◆校正：zh-only CONSISTENCY 模块同样未映射，纳入；另 `gbt7714` 不在 script_map 恒 SKIP（超范围仅记录） | fix（W3）：`MODULE_DIMENSION_MAP`（EXPERIMENT/PSEUDOCODE→reproducibility，CITATIONS/BIB/PRESUBMISSION→presentation，CONSISTENCY→clarity） |
| A-PA-6 | Low/Med | literature_compare 只匹配 `\bibitem`。◆校正：Typst `@key` 提取已存在（audit.py:2508-2509）；真缺口是外置 .bib 的参考文献**题名**未读入 | fix（W3）：`compare_with_literature` 增可选 `bib_content` + 调用侧 .bib 解析；renorm guard(:2496-2501) 原样保留 |
| A-PA-7 | Low | scoring_model None→5.0 进特征不进罚项，校准不对称 | test-only：表征测试，行为改动延后 |
| A-PA-8 | test | （v2 已改）原 import 断言为误报；函数存在且 Typst 链路可用 | test-only：Typst 端到端回归测试防退化 |

### A-TY typst-paper（07-15-audit-fix-typst-paper，P1）

| ID | 严重级 | 发现（证据） | 处置 |
|----|--------|--------------|------|
| A-TY-1 | High | `parsers.py:219-221` `split("//")[0]` 命中 `http://` → 含 URL 行截断，下游 deai/时态/密度漏检；clean_text(:275) 同缺陷。◆校正：范围不止 EN vendored——**zh 副本 TypstParser 同款 bug**，且 PRESERVE_PATTERNS 锁（test_parsers_alignment.py:83）跨含 zh 全五副本；zh 仅修 extract_visible_text+PRESERVE 不加 clean_text（保持既有锁形态）；TypstParser.clean_text 当前未入锁，本任务顺势新增锁行 | fix：模块级 `_strip_typst_line_comment` 单遍扫描器（字符串/raw 状态机 + `://` 跳读）为行注释**唯一所有者**——PRESERVE_PATTERNS 的 `r"//.*"` 条目五副本整条删除（核实：新流程下该条目是死代码），无任何 `//` 正则兜底；`https://host//path` 完整可见改为正向断言；裸协议相对 `//cdn...` 按注释处理（扫描器独家裁定）；块注释剥离先于行注释 |
| A-TY-2 | Low | extract_abstract(:416-422) lookahead 只认 level-1 → `== Keywords` 渗入。◆校正：修复须同步**四处**——typst:417（不在锁内）+ en:656/audit:695/cover-letter:665（三副本锁） | fix：`(?=^=\s+\|\Z)` → `(?=^=+\s+\|\Z)` |

### A-BIB bib-search-citation（07-15-audit-fix-bib-search，P1）

| ID | 严重级 | 发现（证据） | 处置 |
|----|--------|--------------|------|
| A-BIB-1 | High | `spec_from_compact_query`(:499) shlex 遇撇号抛 "No closing quotation" exit 2（实测） | fix：try shlex → ValueError 回退正则切分 + `query_tokenizer_fallback` 警告贯通 `meta.parse_warnings`，exit 0；短语引号语义保持 |
| A-BIB-2 | Medium | preview(:169-190) 不呈现 parse_warnings/per-result warnings，违反 SKILL.md 安全边界 | fix：`Warnings (N):` 区块（上限 5 条+截断）+ per-result Warning 行 + Encoding 回退行；无 warnings 时输出逐字节不变 |
| A-BIB-3 | Medium | `has_code` 裸子串：code→encode/barcode，repo→reported（实测四负例 True） | fix：按 D4 全词表词边界化为单一 `CODE_HINT_RE` + 补 `codeavailable`；负例转 False、正例保持、fixture 端到端结果集不变 |
| A-BIB-4 | Medium | `YEAR_RE`(:31) 拒绝 `2024a` 消歧后缀 → 年份过滤静默排除 | fix：`(...)[a-z]?\b` 取 group(1)（2024a→2024，20245 仍 None） |
| A-BIB-5 | Low | 非整数 `limit:/year:` 抛裸 ValueError | fix：`_parse_int` 包三处，措辞对齐 validate_spec:289 |
| A-BIB-6 | Low | 字母开头含冒号自由文本（`genotype:phenotype`）被静默当字段过滤丢出相关性评分。◆校正：`10:30` 不成立——FIELD_OP_RE(:27-29) 要求 field 以 `[A-Za-z_]` 开头，数字开头 token 保留为自由文本 | doc：query-syntax.md 说明 + `unknown_field_filter` message 加「冒号改空格」指引（type 不变） |

### A-CL cover-letter（07-15-audit-fix-cover-letter，P2）

| ID | 严重级 | 发现（证据） | 处置 |
|----|--------|--------------|------|
| A-CL-1 | High | journal_fit `_count_claims`(:106-113) 只数 `we (report\|...)` → 真 claim 大量漏计 → 假 evidence_density LOW → 整体 LOW exit 2。◆校正：现存 fixture 实测计 1 非 0（"we report/propose" 在旧正则内），根因与修法不变 | fix：复用 `build_letter_claim_map.extract_claims`（bare import；TIER_BUDGETS 不动，两 fixture 实算校准过） |
| A-CL-2 | High | claim 管道不剥 `%` 注释 → 注释行假 P1；`_strip_tex_comments` 仅用于 disclosure | fix：`.tex` claim 提取前置剥注释（样板 presubmission `_line_views`） |
| A-CL-3 | Medium | 数字单位裸 `s` 误配（"3 seconds"↔"3 sensor" 实测）；verify:82/build:46/extract:257 三处单位集不一致 | fix：单源常量 `NUMBER_UNIT_PATTERN` 落 build_letter_claim_map，三消费点统一 |
| A-CL-4 | Medium | `_SPECIFIC_METRIC_RE` 与 metric_keywords 对方向词不一致 → 方向词-only 分支 160 字符窗口误配 | fix：新增 `_DIRECTION_WINDOW=60` 分支镜像 local_specific 机制 + fixture |
| A-CL-5 | Medium | journal_fit(:288) 与 presubmission(:633) 长度阈值重叠双报。◆校正：`cover_letter.py:183-201` optimize 模式**不**调 journal-fit，双报仅发生于 MODE_GUIDE:123 的「optimize+可选 journal-fit」代理工作流 | fix：opt-in `--dedup-length`（L1 胜出：两档阶梯更细且 optimize 恒跑），不改 optimize 默认输出 |
| A-CL-6 | Medium | scope_fit(:118-130) 对顶刊紧字数预算过严 → 简洁 Nature letter 系统性 LOW | fix：顶刊 1-hit=HIGH + 从 paradigm_signals 删 "broad scientific" 拆双计分（一并解决原审计 finding 8） |
| A-CL-7 | Low | `_extract_title_local` fork(:224-240) 绕过 canonical 截断 bug。◆校正：fork 同时承担 `\thanks` 剥离而 A-EN-10 仅 balanced-brace——可能只能**缩薄**不能整删（分支 B：必要时上推 canonical） | fix：**阻塞于 A-EN-10**，Batch 4 完成后任务方可归档（v2.3：取消 blocked 完成分支——终批禁改行为代码无人承接）；若探针显示 canonical 未剥 `\thanks`，回 EN 任务补齐而非缩薄 fork |
| A-CL-8 | Low | `_exit_code`(:38-47) 混类型访问脆弱 | fix：显式类型分支 |
| A-CL-9 | Low | align_check:159 硬编码 source_section | fix：位置化——build_claim_map 回定位每句 claim 的 `char_offset`，align_check 按信件真实结构（称呼/空行段界/落款）映射 `header/opening/closing`，其余或定位失败回退诚实标签 `body`（ISSUE_SCHEMA 枚举 +`body`、可选 +`char_offset`）；不做关键词猜测 |
| A-CL-10 | Low | journal_fit:379 缺 tier 静默回退 mid-journal | fix：缺失时警告 |
| A-CL-11 | Low | 通讯作者模式窄（IEEE `\thanks`/acmart `\authornote`） | doc-only：反捏造理由(:42-46) + acmart 表征测试 |

## 子任务地图与排期

```
07-15-audit-fix-version-ci       P0 轻量  A-REL-1                          ← 最先，恢复绿基线
07-15-audit-fix-latex-paper-en   P1 复杂  A-EN-1..10（canonical parsers）
07-15-audit-fix-typst-paper      P1 复杂  A-TY-1..2（TypstParser 五副本+锁行）
07-15-audit-fix-cover-letter     P2 复杂  A-CL-1..11（A-CL-7 阻塞于 A-EN-10）
07-15-audit-fix-latex-thesis-zh  P1 复杂  A-ZH-1..9
07-15-audit-fix-paper-audit      P1 复杂  A-PA-1..8（W1/W2/W3）
07-15-audit-fix-bib-search       P1 复杂  A-BIB-1..6
07-15-audit-release-integration  P2 轻量+ A-REL-2 + 集成门禁               ← 终批，其余全部归档后
```

顺序约束：
1. version-ci 先行（绿基线）。
2. latex-paper-en 先于 cover-letter（A-EN-10 → A-CL-7）。
3. en 与 typst 均触碰 parsers 副本与锁行，函数级零交集已由双方 design.md 核对声明（en 拥有 extract_title/LatexParser 成员；typst 拥有 TypstParser.extract_visible_text/clean_text/PRESERVE_PATTERNS/extract_abstract Typst 分支）；若并行则 en 先合、typst rebase。
4. zh / paper-audit / bib-search 相互独立可穿插（zh 的 bib_scan.py vendored 自 bib-search 现有代码，不依赖 A-BIB 修复落地）。
5. 行为修复全部完成后 → 终批子任务 `audit-release-integration` 执行 A-REL-2 + 集成复查 + 六技能双语概览/usage 与 SKILL 路由一致性复查更新（D7）+ 资源同步 + `just doc-build`。**父任务本身无实施工作（纯汇总：需求集、任务地图、跨子验收）**。

## 验收标准（父任务）

- [x] 登记表所有 fix 项落地，**每项修复（含 Low）有回归测试**；test-only 项有表征/回归测试。
- [x] `just ci` 全绿；parsers/deai 对齐锁按各 design.md 声明更新且副本一致。
- [x] D1–D7 全部体现（无 "4 specialized agents" 残留、无四级 severity 残留含 synthesis_agent.md :47/:56/:66/:85、has:code 负例过测）。
- [x] 任何时刻仅一个 in_progress 任务（07-14 docs 树已全部归档，无停放依赖）。
- [x] 终批子任务 `audit-release-integration` 完成：`last_updated` 与 CHANGELOG 6.0.0 段定稿（A-REL-2）、跨子任务 parser 副本对齐 + evals 复查、六技能双语概览/usage 与 SKILL 路由一致性复查更新（D7）、资源同步与 `just doc-build` 通过。
- [x] 遵守 CLAUDE.md 红线：勿动 cite/ref/label/math；勿造数据；除版本号外不动构建配置。

## 共享基础设施结论（健康项，无需子任务）

parser ALIGNMENTS 全绿无漂移；tex_loader 在 en/audit/cover-letter 逐字节一致（zh 有意不同）；evals 结构一致 fixtures 齐全；docs 双语契约健康。`tests/contracts` 实测 173 passed / 1 failed（唯一红即 A-REL-1）。

## 超范围记录（不在本任务树内，供未来任务参考）

- `paper-audit-specialized-reviewer-wiring`：完整接线专项 reviewer（schema 兼容化 + 派发协议），D3 显式非目标。
- paper-audit `gbt7714` 检查不在 audit.py script_map、恒 SKIP（A-PA-5 规划期发现，仅记录）。
