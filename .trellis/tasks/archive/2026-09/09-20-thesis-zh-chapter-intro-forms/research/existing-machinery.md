# 既有机制与编辑锚点（2026-09-20 实测，`dev` HEAD `efcd5cb`）

## 1. 术语分离（本任务的前提）

仓库里"两形态"一词已经被占用：**位置形态** = 编号引言节（`\chapter` 后直接 `\section{引言}`，`intro_form == "numbered"`）/ 章后导语（`intro_form == "lead"`），由 07-11 任务核实为均合规。用户本次说的"一段式 / 两段式"是**段式**（自然段数量），与位置形态正交：编号引言节可以是一段式（熟料、粉磨）也可以是两段式（烧成、固废焚烧）；章后导语同样两者皆有（锌第 2 章一段、第 3~6 章两段）。任务内所有文档与代码一律用"位置形态"与"段式"两个词，不得再写"两形态"指段数。

## 2. 规则源现状与要改的句子

| 文件 | 锚点 | 现状 | 本任务动作 |
| --- | --- | --- | --- |
| `references/writing/thesis-writing-guide.md` | L42 节题"正文章引言（承上启下两段式，推荐形态）"；L44-47 推荐语；L48-52 两段角色；L54-60 模板；L62-66 弹性口径；L68-77 正反例表；L79 边界 | 只有两段模板；"推荐形态"指段数 | 节题改为"正文章引言（一段式 / 两段式）"；两段模板原样保留；新增一段式六步推进序 + 模板 + 正反例；新增"段式选型"小节；推荐点从"两段"改为"承上句"（D2） |
| `references/writing/method-chapter-guide-zh.md` | §三 L73-77（"承上启下两段式为主动推荐形态"）；L83-84 篇幅"1~3 段"；L94-101 正反例表；L225 阈值表"章引言 1~3 段、300~500 字" | 已承认 1~3 段，但推荐语指两段 | §三追加"段式"一条并链接；正反例表加一段式合规行；§十检查映射加 `CI-*` 行；§九红线不改 |
| `references/writing/structure-guide.md` | L147"章引言宜写成承上启下两段、约 300~500 字：第①段……第②段……" | 唯一把两段写成"宜"的句子 | 改为"宜承上启下、一段或两段、约 300~600 字"，指路 thesis-writing-guide |
| `references/writing/process-chapter-guide-zh.md` | L228-229"承上启下两段式从第 3 章起适用" | 措辞把承上启下等同两段 | 改为"承上启下（一段或两段）从第 3 章起适用"；§十两位置形态表不动 |
| `references/writing/paragraph-roles-zh.md` | "指南分工"第一条"章引言承上启下两段式与弹性口径见……" | 同上 | 改"章引言一段式 / 两段式与弹性口径见……" |
| `references/modules/logic.md` | L31-39 Chapter Intro Specialization（"承上启下、约两段"）；L149-158 PR 表之后 | 无段式说明、无新 flag | 改措辞；新增 `## Chapter Intro Style Checks (--chapter-intro-style)` 小节 |
| `references/modules/routing-rules.md` | L57 章引言条（"两段式为推荐形态"） | 同上 | 改"一段式与两段式均合规、按依赖强度与篇幅选型"；追加触发词"引言写成一段行不行 / 要不要分两段 / 一段式 / 两段式"与 `--chapter-intro-style` |
| `SKILL.md` | L6 `when_to_use`；L28 `last_updated`；L72 `logic` 路由行；L84-91 路由规则；L164 Reference Map（"章引言（承上启下两段式）"） | — | 触发词、路由行命令、Reference Map 措辞、`last_updated`；`version` 不动 |
| `docs/skills/latex-thesis-zh/index.md` L39/L107-127；`docs/zh/.../index.md` L35/L102-122 | `logic` 行与写作参考列表 | — | `logic` 行加段式检查；新 YAML 加一行；被改 references 的 en/zh 镜像同步 |
| `evals/trigger_eval.json`（59 条）、`evals/evals.json`（51 条，id 51 为段落职责） | CRLF；只能 Bash python 追加 | — | +2 正例 +1 负例；+id 52 |

保真锁核对：`tests/contracts/test_thesis_zh_guidance_fidelity.py` 不锁任何章引言句子（已逐行核对 L1-140）；`tests/` 内没有断言"两段式 / 两态均合规 / 推荐形态"字符串的测试（`grep` 仅命中 `test_latex_thesis_zh_scripts.py:801` 注释）。

## 3. `analyze_logic.py` 锚点

| 用途 | 符号 | 行号 |
| --- | --- | --- |
| 承上桥接词 | `CHAPTER_BRIDGE_KEYWORDS_ZH` | L209-219 |
| 启下动词 / 路标词 / 相对指代 | `CHAPTER_PREVIEW_KEYWORDS_ZH` / `CHAPTER_ROADMAP_KEYWORDS_ZH` / `RELATIVE_REF_PATTERNS_ZH` | L228 / L247 / L263 |
| 章号引用（P-FRAME 专用，仅阿拉伯数字） | `CHAPTER_NUM_REF_RE = r"第\s*\d+\s*章"` | L274；用于 L3345 |
| 章号依赖引用（承上检测 + 依赖线索） | `CHAPTER_DEP_REF_RE = r"第\s*[一二三四五六七八九十百\d]+\s*章"` | L277；用于 L531（`_chapter_reuses_prior`）、L712（承上判定）、L3510（PR-INTRO-BG 同句承接排除） |
| 节号目录 | `SECTION_NUM_PREVIEW_RE = r"\d+\.\d+\s*节"` | L278 |
| 豁免标题 / 编号引言节标题 / 篇幅常量 | `CHAPTER_INTRO_EXEMPT_TITLES_ZH` / `INTRO_SECTION_TITLES_ZH` / `CHAPTER_INTRO_MIN_CHARS=40`、`MAX=900`、`NUMBERED_MAX=1600` | L285 / L294 / L295-299 |
| 豁免判定 / Major 输出 / 依赖线索 / 分级输出 | `_is_chapter_intro_exempt` / `_chapter_intro_gap` / `_chapter_reuses_prior` / `_chapter_bridge_gap` | L505 / L513 / L522 / L535 |
| 章引言块定位（返回 `(report_line, intro_text, form)`，**不返回行区间**） | `_chapter_intro_block(chapter, headings, lines, parser)` | L559-619；调用点 L672（默认检查）、L3497（`--paragraph-roles`） |
| 默认章引言检查；文案含"第一段 / 第二段 / 扩展为承上启下两段 / 保留承上启下两段" | `_check_chapter_intro(content, lines, parser, first_chapter=None)` | L622-780；文案 L683、L685、L758、L773 |
| 段落切分（含 `start/end/visible/sentences/is_heading_lead`） | `ArcParagraph`；`_split_arc_paragraphs(content, parser, sections)` | L1263；`grep -n "^def _split_arc_paragraphs"` |
| 句切分 / bigram Jaccard / 行号格式 | `_arc_sentences` / `_arc_jaccard` / `_zh_loc` | L1402 / L1949 / L29 |
| 术语表加载模式（逐字段回退） | `_load_paragraph_arc_terms`、`_load_paragraph_roles_terms` | `grep -n "^def _load_paragraph"` |
| opt-in finding 格式样板（Info/P3 + `Meaning-Check: NEEDS-LLM`） | `_pr_finding(code, start, end, message, current, suggested, rationale)` | `grep -n "^def _pr_finding"` |
| 入口与分支顺序 | `analyze(..., paragraph_roles=False)`；分支 `method_narrative`(L3795/L3907) → 默认 `_check_chapter_intro`(L3879) → `process_chapter`(L3904) → `paragraph_arc`(L3912) → `subsection_context`(L3916) → `paragraph_roles`(L3947) → 兜底 L3960 | L3766-3962 |
| CLI | `main()` `add_argument` L3966-4018；help 文案样式"运行……观察（……；默认关闭）" | — |

其他脚本：`check_style_zh.py` `DEFAULT_MAX_CHARS = 80`（L45，E-LONGSENT 单句长度）——一段式超长句由它负责，本任务不重造。`deai_check.py` / `references/deai/guide.md` 已把"具有重要的理论意义和应用价值"类意义句列为空泛表达——本任务指路不重造。

## 4. 现有检查器对一段式的两处实测缺陷

1. **章号列举不被识别为承上**：`CHAPTER_DEP_REF_RE` 只匹配"第 N 章"，不匹配"第 3、4、5 章 / 第 3～5 章 / 第3-5章"。一段式承上常压成一句列举（熟料 6.1 实例），会被判"缺承上"；章内另有"第 X 章"依赖线索时升 Major。属**误报**，按 spec 允许的默认行为变化例外处理（双声明）。
2. **建议文案写死两段**：`bridge_suggest`"在章引言第一段……"、`preview_suggest`"在章引言第二段……"、过简建议"扩展为承上启下两段"、过长建议"保留承上启下两段"。一段式作者按此改会被迫拆段。属**误导性指引**，随第 1 项一并按默认行为变化例外处理；observe 行（首行）不改，存量断言全部落在 observe 行，不受影响。

篇幅阈值 40 / 900 / 1600 覆盖语料一段式 313~577 字区间，不改。

## 5. 联动锁清单（改动前后必跑）

1. `tests/skills/latex_thesis_zh/test_paragraph_arc.py::test_default_output_is_byte_identical_to_pre_change_baseline`：`baseline-sample.tex` 只有 1 个 `\chapter`，`baseline-before.txt` 不含任何章引言 finding（已 grep 核实），故文案与正则修复不触碰基线；新 flag 默认关闭。
2. `tests/skills/latex_thesis_zh/test_polish_unit_zh.py::FROZEN_HASHES["analyze_logic.py"]`：改脚本后必须更新 LF 规范化 sha256（`paragraph-roles-contract.md` §5 已记录）。
3. 存量章引言测试：`test_chapter_intro_forms.py`（直接调用 `_check_chapter_intro`）、`test_body_chapters.py` R4c/R5、`test_latex_thesis_zh_scripts.py` L801-887、`test_process_chapter.py`、`test_paragraph_roles.py`（复用 `_chapter_intro_block`）——断言均为 observe 行子串。
4. `tests/contracts/test_skill_contracts.py`：`ROUTER_ROW_RE`；`test_latex_thesis_zh_module_router_commands_match_script_help`（路由行每个 `--` 选项须出现在 `--help`）；`KEBAB_CASE_FILE_RE`；description 长度（当前 226）。
5. `tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py::SMOKE_COMMANDS`（L99-100 样式）：加 `--chapter-intro-style` 一行。
6. `tests/contracts/test_thesis_zh_guidance_fidelity.py::test_historical_eval_prefix_is_unchanged`：`evals.json` 前 47 条 / `trigger_eval.json` 前 49 条哈希锁，只允许追加。
7. `tests/contracts/test_trigger_evals.py`：query 唯一、正负例下限。
8. `tests/contracts/test_docs_bilingual_resources.py` + `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`：被改 references 与新 YAML 的 en/zh 镜像与 manifest 散列。
9. `tests/contracts/test_subsection_context_contract.py`、`test_paragraph_arc_audit_contract.py`、`test_parsers_alignment.py`、`test_deai_alignment.py`：`analyze_logic.py` 改动后重跑；`parsers.py`、`deai_check.py` 字节不变。

## 6. 既有取舍（勿重开）

- 位置形态两者均合规（4:1）；路线预告 / 节号目录两态均合规；并列方法章可不承上（承上强度 ∝ 章间依赖，纯并列降 Info）；第 2 章概述式不查承上；引言含 `\cite` 合法；不重述行业背景；目录与路线不双写。
- 检查器新能力默认藏在 flag 后；默认行为只允许误报 / 假绿修复例外，且须"同步存量单测 + commit 正文声明"双声明（`testing-and-tooling.md` "Convention: 检查器默认行为变化"）。
- `[Script]` 恒 `Meaning-Check: NEEDS-LLM`；启发式 Info/P3；阈值标 UNVERIFIED；不复制 fixture 整句；私有语料不进公开文件。
