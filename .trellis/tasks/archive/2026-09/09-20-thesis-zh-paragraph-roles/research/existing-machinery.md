# 既有机制与编辑锚点（2026-09-20 实测）

本文记录 `latex-thesis-zh` 中与"正文各级段落职责 / 结构重复"相关的既有规则源、检查码、代码锚点与全部联动锁。行号以 `dev` 分支 HEAD `c7fa2e5` 为准。

## 1. 六个位置的既有覆盖与缺口

| 位置（用户表格） | 既有规则源 | 既有检查码 | 缺口（本任务要补） |
| --- | --- | --- | --- |
| 章引言 | `thesis-writing-guide.md` L42-78（两段式、弹性口径、正反例）；`method-chapter-guide-zh.md` §三 L73-101（禁重复绪论综述、路线预告≠节号目录、两形态均合规）；`structure-guide.md` L147 | `_check_chapter_intro`（承上 Major/Info、启下 Major、相对指代 Minor、篇幅 Minor） | "重新介绍整个行业背景"只有"禁重复绪论综述"一句，无检查；"目录 + 路线预告双写""逐节详列"无规则也无检查 |
| 含子节的总节导语 | `structure-guide.md` L142-147 标题后导语规范（四件事中的两到三件） | S1 `_check_heading_leads`（有无导语、导语过短） | "不重复整章问题和全方法链"无规则也无检查 |
| 具体方法小节首段 | `method-description-guide-zh.md` §三 六角色契约（动机/输入/输出/接口） | M-HEADING / M-SEQWORD（`--method-narrative`） | "首段再列所有研究挑战"无规则也无检查 |
| 公式后段落 | `method-description-guide-zh.md` §五 L103-118（公式前/公式/公式后；"式中"只完成符号释义） | M-EQUATION（编号公式后 3 行内无"式中/其中"，Minor/P2） | "按公式顺序把每个乘加操作再译成文字"无规则也无检查 |
| 实验结果段 | `results-analysis-guide-zh.md` §二 L76-78（不写"报一个数、猜一个原因"流水账）、§八 L248-260（四轴解释基线，不按模型逐个编写原因）、§九 不合格数值复述例 | RA-SHALLOW / RA-SECONDBEST / RA-CAUSAL 等（`experiment --results-analysis`）；B3 防御性推测；E-ATTR | 已充分覆盖；本任务只在新指南中做"位置 → owner"指路，不新增检查码 |
| 本章小结 | `thesis-writing-guide.md` L80-140（五角色、不复述目录、不新增结果、不新增引用）；`method-chapter-guide-zh.md` §六 L150-158（可"首先……最后"串要点；结论≠各章小结）；`structure-guide.md` L148 | 无脚本码（routing-rules L57 走 `logic` + 指南） | "新增论证（引用/公式/图表/推导）"只有"不新增引用"一句，无检查；"重列完整训练/部署流程"与"串要点合规"需要口径协调 |

结论：六行中 3 行（章引言、实验结果段、本章小结）已有规则源但缺"不必反复做"的负面清单；3 行（总节导语、方法小节首段、公式后段落）既无规则也无检查。仓库没有一份把六个位置放在一张表里的合并视图。

## 2. `analyze_logic.py` 可复用锚点

| 用途 | 符号 | 行号 |
| --- | --- | --- |
| 绪论背景词（只在绪论漏斗使用） | `INTRO_BACKGROUND_RE_ZH = re.compile(r"(背景\|需求\|近年来\|应用\|场景\|行业\|领域\|现实)")` | L202；唯一调用 L2596 |
| 承上桥接词 / 启下动词 / 路标词 | `CHAPTER_BRIDGE_KEYWORDS_ZH` / `CHAPTER_PREVIEW_KEYWORDS_ZH` / `CHAPTER_ROADMAP_KEYWORDS_ZH`（组织如下/首先/其次/最后…） | L209 / L228 / L247 |
| 相对指代 / "第X章" / 节号目录 | `RELATIVE_REF_PATTERNS_ZH` / `CHAPTER_DEP_REF_RE` / `SECTION_NUM_PREVIEW_RE = r"\d+\.\d+\s*节"` | L263 / L276 / L277 |
| 章引言豁免标题 / 编号引言节标题 / 篇幅常量 | `CHAPTER_INTRO_EXEMPT_TITLES_ZH` / `INTRO_SECTION_TITLES_ZH = ("引言","概述","引 言")` / `CHAPTER_INTRO_MIN_CHARS=40`、`MAX=900`、`NUMBERED_MAX=1600` | L283 / L293 / L294-298 |
| 章引言块定位（章标题→首个 level≥2 标题；编号引言节形态改取该小节正文）、第 2 章特判、`first_chapter` 真实章号 | `_check_chapter_intro(content, lines, parser, first_chapter=None)` | L558-757；块定位逻辑 L600-660 内联在函数体内，**无独立 helper** |
| 章引言 finding 格式 | `_chapter_intro_gap(line, title, observe, suggest)` Major/P1；`_chapter_bridge_gap(...)` 分级 | L512 / L535 |
| 章内"第X章"依赖线索 | `_chapter_reuses_prior(lines, start, end, parser)` | L522 |
| 标题豁免 / 行分类 | `_is_exempt_heading`、`_is_chapter_intro_exempt`、`_classify_lead_gap` | L837 / L504 / L842 |
| S1 导语检查（有无、过短） | `_check_heading_leads(content, lines, parser)`；`LEAD_GUIDE_KEYWORDS_ZH` | L864 / L187 |
| 汉字 bigram token 与 Jaccard | `_thread_tokens`、`_arc_jaccard(left,right)`、`_endpoint_jaccard` | L1024 / L1797 / L1806 |
| 段落切分（含 `is_heading_lead`、`section`、`sentences`、`segment_id`） | `@dataclass ArcParagraph`；`_split_arc_paragraphs(content, parser, sections)` | L1138 / L1449 |
| 术语表加载模式（逐字段回退） | `_load_paragraph_arc_terms(script_dir)`、`_load_subsection_context_terms` | L1186 / L1219 |
| P-ARC finding 格式（Info/P3、`Meaning-Check: NEEDS-LLM`、不复制整句） | `_arc_finding(code, start, end, message, current, suggested, rationale, *, severity="Info", priority="P3")` | L1838 |
| 编号公式块 / 块间可见文本 / 释义引导词 | `_mn_equation_blocks(lines,start,end)`、`_mn_visible_between`、`MN_EQ_GLOSS_RE_ZH = r"式中\|其中"`、`MN_EQUATION_LOOKAHEAD` | L2933 / L2955 / L2665-2683 |
| M-EQUATION 实现（公式后 3 个可见行找"式中/其中"） | `_check_method_equations(lines, start, end, parser)` | L2964 |
| 入口与 opt-in 分支顺序 | `analyze(file_path, section, cross_section, motivation_thread, intro_mainline, process_chapter, first_chapter, method_narrative, paragraph_arc, subsection_context, subsection, emit_window)`；分支顺序 `process_chapter` → `method_narrative` → `paragraph_arc`（L3425）→ `subsection_context`（L3429）→ 兜底 `"% 逻辑/方法论：未检测到规则级逻辑问题。"`（L3461） | L3284-3463 |
| CLI | `main()` argparse；`--paragraph-arc` help 文案样式："运行段落弧线观察（……；默认关闭）" | L3465-3540 |

`parsers.py`：`SECTION_TITLE_RULES` 中 `("summary", 3, r"^本章小结$")`、`("organization", 3, ...)`（L188）；`split_sections` 返回 `dict[str, tuple[int,int]]`，**同一键只保留一个区间**，多章"本章小结"不能靠 `sections["summary"]` 逐章定位，须用 `extract_headings` 按标题逐章取范围。

## 3. 规则源与路由文档编辑锚点

| 文件 | 锚点 |
| --- | --- |
| `SKILL.md` | frontmatter L1-12（`version: "6.0.0"`、`last_updated: "2026-09-19"`、`when_to_use` 含"章引言/本章小结怎么写"）；`logic` 路由行 L72；`## 路由规则` L84-91（"常见歧义速判"一条含"章引言/分章型小结/主线闭合走 `logic`"）；`## Reference Map` L154-181 |
| `references/modules/routing-rules.md` | L50-57：`logic` 默认范围条、`--paragraph-arc` 条、章引言条、本章小结条 |
| `references/modules/logic.md` | `### Chapter Intro Specialization` L31；`## Paragraph Arc Checks` L118；`## Subsection Context Checks` L133；`## Body-Chapter Stitching & Intro Bridging (default)` L149 |
| `references/writing/thesis-writing-guide.md` | 章引言节 L42-78（模板含"本章组织如下：N.1 节……" L58；"两态均合规" L65）；本章小结节 L80-140（"不新增未在原文出现的引用" L140） |
| `references/writing/method-chapter-guide-zh.md` | §三 L73-101；§六 L150-158；§九 红线 L196-213（第 6 条"引言预告方法路线而非节号目录→合法"）；§十 检查映射 L214 |
| `references/writing/structure-guide.md` | 标题后导语规范 L142-149 |
| `references/writing/method-description-guide-zh.md` | §五 L103-118；§十 检查映射 L186-197 |
| `docs/skills/latex-thesis-zh/index.md` | 路由表 `logic` 行 L37；`### Writing References` L107-127 |
| `docs/zh/skills/latex-thesis-zh/index.md` | 路由表 `logic` 行 L33；`### 写作参考` L102-122 |
| `docs/resource-manifest.json` | `{"version":1,"resources":[{skill,kind,source,sourceLocale,sourceSha256,en,zh}]}`，latex-thesis-zh writing 类 23 行 |

## 4. 联动锁清单（改动前后必跑）

1. `tests/skills/latex_thesis_zh/test_paragraph_arc.py::test_default_output_is_byte_identical_to_pre_change_baseline`：默认 `analyze()` 输出对 `tests/fixtures/paragraph_arc/baseline-sample.tex` 逐字节等于 `baseline-before.txt`（`.gitattributes` 标 `-text -diff`）。新 flag 默认关闭即可通过；重构 `_check_chapter_intro` 内联块定位为 helper 时也受此锁约束。
2. `tests/contracts/test_skill_contracts.py`：`ROUTER_ROW_RE`（L166）解析路由表；`test_latex_thesis_zh_module_router_commands_match_script_help`（L525）要求路由行命令里每个 `--` 选项出现在脚本 `--help`；`KEBAB_CASE_FILE_RE`（L163）与 `test_latex_reference_layout_is_discoverable_and_kebab_case`（L276）约束 `references/` 新文件名；`_frontmatter_description` 断言 description 长度。
3. `tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py::SMOKE_COMMANDS`（L90）：新 flag 需加一条 smoke。
4. `tests/contracts/test_thesis_zh_guidance_fidelity.py`：L99-102 锁定 `modules/logic.md` 必含 `(../references/writing/paragraph-arc-zh.md)`、`(../references/writing/subsection-context-zh.md)` 等链接串；L26-80 锁定各指南关键句存在/不存在；`test_historical_eval_prefix_is_unchanged` 锁 `evals.json` 前 47 条与 `trigger_eval.json` 前 49 条哈希（当前 50 条 / 56 条，只允许追加）。
5. `tests/contracts/test_trigger_evals.py`：`query`/`should_trigger`/`category` 必填，query 技能内唯一，正负例数量平衡断言（L118）。
6. `tests/contracts/test_docs_bilingual_resources.py`：live inventory 与 manifest 一致；`_router_tokens` 只解析模块名（新 flag 不改 usage token）；新 `references/**/*.md|yaml` 必须有 manifest 行和 en/zh 镜像页。
7. `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`（`--write-manifest` 重生成散列；`--inventory-only` 只列清单）。
8. `tests/contracts/test_subsection_context_contract.py`、`test_paragraph_arc_audit_contract.py`：不改 S-CTX / P-ARC 语义即不受影响，但 `analyze_logic.py` 改动后必须重跑。
9. `evals/evals.json`（CRLF，最后 id 50，字段 `id/prompt/expected_output/files/assertions`，assertion 类型 `contains/not_contains/regex`）与 `evals/trigger_eval.json`（56 条，最后三条为 unit-polish）只能用 Bash python 追加（spec `testing-and-tooling.md` L122-136）。

## 5. 既有取舍（勿重开）

- 章引言"两形态均合规"（编号引言节 / 章后导语）与"路线预告 / 节号目录两态均合规"是 07 月方法章任务用 5 篇范文核实的口径（`method-chapter-guide-zh.md` §三、§九第 6 条）。本任务只能在其上追加"不双写、不逐节详列"，不能把节号目录判为缺陷。
- 本章小结"启下句只作 Info 推荐"（红线 2）、"单段默认、模板要求可多段"不变。
- 第 2 章引言是"概述式"，承接绪论背景而非前章结论（`_check_chapter_intro` docstring）；新的背景重述检查对第 2 章应跳过。
- `[Script]` 恒 `Meaning-Check: NEEDS-LLM`；Info/P3 启发式；默认输出零变化（spec `testing-and-tooling.md` L224-238）。
