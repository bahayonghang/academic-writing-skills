# typst-paper 审计报告（agent 原始产出，2026-06-13）

审计对象：`academic-writing-skills/typst-paper/`（SKILL.md v5.2.0，20 个脚本 / 27 个参考文件 / 3 模板 / 5 示例 / 2 evals），及仓库根 `tests/`、`conftest.py` 相关部分。全部缺陷已用 `python` 导入脚本在系统临时目录复现取证，未修改仓库任何文件。

## §1 外部环境调研结论（每条附来源）

1. **Typst 现行版本为 0.14.2（2025-12），0.15.0-rc1 已于 2026-06-09 发布**。0.14 重点：无障碍/PDF-UA、PDF 1.4-2.0 与 PDF/A 全档支持、字符级 justify；breaking changes 较温和（label/URL/font 列表不允许为空、两个 bibliography style 改名、`--make-deps` 弃用）。0.13（2025-02）引入 par 级 first-line-indent、curve 取代 path。skill 内语法示例与 0.14 基本兼容（详见 §2 例外项）。来源：typst.app/docs/changelog/、typst.app/blog/2025/typst-0.14/、github.com/typst/typst/releases
2. **`page` 函数没有 `column-gutter` 参数**（参数仅 paper/width/.../columns/...），列间距须经 `columns` 函数设置——skill 8 处推荐配置把 `column-gutter` 写进 `#set page(...)`，照抄必编译报错。来源：typst.app/docs/reference/layout/page/
3. **内置 bibliography style 无 `"gb-7714-2015"`**，合法 id 为 `gb-7714-2015-numeric` / `-author-date` / `-note`（另有 `gb-7714-2005-numeric`）；`mla`、`chicago-author-date`、`ieee` 别名有效。hayagriva 对 GB/T 7714-2015 为内置支持 + 可加载自定义 CSL（经 citationberg），但存在已知边缘问题（"第1卷" is-numeric 误判 #439、标准文献类型码误判为 [EB] #312、中文"等"双语处理 #291）；**GB/T 7714-2025 尚无 hayagriva 内置样式**（LaTeX gbt7714 包已有 2025 版）。来源：typst.app/docs/reference/model/bibliography/、github.com/typst/hayagriva issues #439/#312/#291
4. **模板生态**：charged-ieee 现行 **0.1.4**（Typst GmbH 官方维护，skill 钉死 0.1.0）；ACM 有官方化 **clean-acmart**（skill 的 ACM 模板仍是手写 page/text 配置）；pseudocode 包 **algorithmic 现行 1.0.7**（`algorithm-figure`/`style-algorithm` 正是 1.0 才引入的 API，0.1.0 没有）、**lovelace 现行 0.3.1**（API 是 `pseudocode-list`，不存在 `#lovelace[...]` 函数）。来源：typst.app/universe/package/charged-ieee/、algorithmic、lovelace
5. **学术接受度**：2025 年 IJIMAI 成为首个官方接受 Typst 投稿的 JCR 期刊；**IEEE/ACM/arXiv 均不接受 Typst 源文件**（arXiv 要求 LaTeX 源或 PDF 直传），ML 会议靠 PDF 评审 + 社区模板变通。skill 的措辞（VENUES.md:421）克制且准确，未夸大。来源：typst.app/blog/2025/typst-at-ijimai/、github.com/typst/typst/discussions/3799
6. **pandoc 互转**：pandoc 已内置 Typst reader + writer（双向）；reader 是"求值"而非逐命令翻译，复杂工程有损；`--pdf-engine=typst` 比 xelatex 快约 27 倍成为 2025 流行用法。skill 完全未提 pandoc 互转（改投 Word/LaTeX 工作流缺口）。来源：hackage.haskell.org pandoc Typst reader、pandoc.org/typst-property-output.html
7. **typst CLI**：`typst compile [OPTIONS] <INPUT> [OUTPUT]`，OUTPUT 是**位置参数**，无 `--output` flag；PNG/SVG 多页导出要求输出名含页码模板（如 `{p}`）。来源：typst-compile(1) man page

## §2 审计发现总表

### P0 — 宣传功能不存在或对真实论文失效

| # | 发现 | 位置(file:line) | 证据 |
|---|------|----------------|------|
| **T1** | `check_references.py` 对**任何带参考文献引用的论文**都把每个 `@bibkey` 报为 Critical/P0 "Undefined reference"（Typst 中 `@key` 同时是 cite 和 ref，脚本不加载 bib、不做任何排除）；且 `REF_RE`/`LABEL_RE` 不含 `:` → skill 自家 TYPST_SYNTAX.md:189,599 推荐的 `<fig:example>` 冒号标签**两侧都解析不出**（`@fig:arch` 被截成 `@fig` 误报） | scripts/check_references.py:27-29,160-171 | 复现：3 行正常论文（2 cite + 1 `@fig:arch`）→ 3 条 Critical P0 全误报，exit 1 |
| **T2** | 路由表 `experiment` 模块主命令 `analyze_experiment.py main.typ --section experiment` **结构上零检查**：review 模式只有 discussion/conclusion/literature-echo 三类检查，传 `--section experiment` 三分支全部跳过，永远输出 "No issues detected" | SKILL.md:89; scripts/analyze_experiment.py:277-287 | 复现：堆数字无归因的 experiment 章节 → "No issues detected" |
| **T3** | 路由表两条主命令用 `--section methods`，而 `split_sections` 的键是 `method` → **照路由表执行必报 "Section not found"**（logic、expression 两模块）；modules/LOGIC.md:7 同病 | SKILL.md:82,84; references/modules/LOGIC.md:7; scripts/parsers.py:52 | 复现确认 |
| **T4** | **Hayagriva 支持按设计即坏**：`check_required_fields` 把 BibTeX 必填字段表（journal/year）套在 Hayagriva 条目上，而 Hayagriva 用 `date`/`parent` → 每个规范的 Hayagriva article 都报 "missing required fields: journal, year" 并 exit 1；页码 en-dash 建议也是 BibTeX 专属反建议 | scripts/verify_bib.py:29-39,141-145,256-261 | 复现：合法 harry-potter 条目 → 必报缺字段，exit 1 |
| **T5** | verify_bib 引用提取 `@(\w+)` 不含 `-`：连字符键（Hayagriva 官方示例风格）被截断 → 同时误报 "not found: harry" 和 "unused: harry-potter"；前缀过滤 `startswith(("fig","tab","eq","sec",...))` 把 @figueroa2021、@tabular2020 等真实引用键静默丢弃；与 T1 正则互相矛盾 | scripts/verify_bib.py:199-203 | 复现见 T4 输出 |
| **T6** | **不解析 `#include`/`#import`**：多文件工程下 `split_sections` 返回 `{}` → deai_check 章节检查静默消失、analyze_logic funnel/lit-review/tri-section 静默跳过、analyze_literature 报 Section not found。ZH 已有 tex_loader.py，typst 未跟进 | scripts/parsers.py:75-98（所有消费方同病） | 复现：include-only 主文件 → `{}` |
| **T7** | **对模板工程（charged-ieee 等主流形态）标题/摘要全部失效**：`extract_title` 只认 `#set document(title:)`，`extract_abstract` 只认 `#abstract[` 和 `= 摘要`（连英文 `= Abstract` 都不认）→ `ieee.with(title:..., abstract:...)` 形态下 optimize_title `--check` 报 "No title found" exit 1、analyze_abstract 报 "No abstract found" | scripts/parsers.py:206-246,57 | 复现：charged-ieee 样例 → 全空 |
| **T8** | check_format `--venue ieee` 对**用 charged-ieee 模板（skill 自荐模板）的论文必报 Critical** "IEEE requires two-column format" + 8 条误报 warning 并 exit 1——两栏由模板内部设置，脚本只在用户文件里 grep `columns: 2` | scripts/check_format.py:213-218,68-76; 与 templates/ieee.md:51 自相矛盾 | 复现确认 |
| **T9** | **推荐配置不能编译**：`column-gutter` 不是 `page` 参数，skill 8 处把它写入 `#set page(...)`，照抄即 `unexpected argument` | templates/ieee.md:24; templates/acm.md:22; references/VENUES.md:79,138,259,290; references/TEMPLATES.md:42; references/TYPST_SYNTAX.md:312 | 官方文档对照 |
| **T10** | `style: "gb-7714-2015"` 不是合法 style id（应为 `gb-7714-2015-numeric` 等）→ 中文参考文献示例照抄即编译错误 | references/TYPST_SYNTAX.md:285; references/VENUES.md:356 | 官方 style 列表 |
| **T11** | COMPILE.md 教学命令 `typst compile main.typ --output build/paper.pdf` —— typst CLI **无 `--output` flag** → 报错 | references/modules/COMPILE.md:22 | man page |

### P1 — 实现缺陷与契约错位

| # | 发现 | 位置(file:line) | 证据 |
|---|------|----------------|------|
| **T12** | **BIBLIOGRAPHY.md 文档化的是 LaTeX 版 CLI**：`--tex`、`--standard gb7714`、`--json`、`--style vancouver/nature`、输出 `% BIBLIOGRAPHY`、字段 `unused_in_tex` —— 本 skill 的 verify_bib.py 一个都不支持 → 照模块文档执行全部 argparse 报错。CITATION_STYLES.md:3 同病 | references/modules/BIBLIOGRAPHY.md:8-21; references/CITATION_STYLES.md:3; scripts/verify_bib.py:392-396 | `--help` 对照 |
| **T13** | TITLE.md 宣传 `--interactive`（标注"推荐"）与 `--compare "A" "B" "C"` —— optimize_title.py 无此二 flag；`--interactive` 本身违反 agent 不可交互原则 | references/modules/TITLE.md:18,21; scripts/optimize_title.py:417-430 | argparse 无对应 |
| **T14** | SENTENCES.md 宣传 `--threshold 50`（实际 `--max-words/--max-clauses`）且宣称中文">60字或>3分句"触发——但句子切分正则不含中文标点、`\b[\w'-]+\b` 把整段中文数成个位数"词" → **中文长句永远检测不到** | references/modules/SENTENCES.md:7,10-12; scripts/analyze_sentences.py:21-29,64 | 复现：121 字中文长句 → 不触发 |
| **T15** | ABSTRACT.md / TABLES.md 命令全用 `main.tex`；TABLES.md 描述 LaTeX 版行为（toprule/booktabs/`% TABLES`），typst 版实际检查 table.vline/hline/stroke——文档与脚本两张皮 | references/modules/ABSTRACT.md:8-11; references/modules/TABLES.md:8-31 | 对照 check_tables.py:122-199 |
| **T16** | **输出契约违反**（SKILL.md:117 要求 `// MODULE ...`）：analyze_grammar / analyze_sentences / improve_expression 三脚本输出 `%` LaTeX 前缀；online_bib_verify verified 用 `#`、mismatch 用 `%` | analyze_grammar.py:64,86-94; analyze_sentences.py:50,76-83; improve_expression.py:56,75-81; online_bib_verify.py:339-350 | 代码常量 |
| **T17** | generate_table.py 的 `--style {booktabs,plain}` 是**空操作**：`self.style` 从未被读取（ZH 模式 #1 复现） | scripts/generate_table.py:21-22,80-113 | 无消费点 |
| **T18** | compile.py：`--watch --format png` 时 format 被**静默丢弃**；PNG 多页导出默认输出 `main.png`，未加 `{p}` 模板，多页论文必失败 | scripts/compile.py:103-105,97-100 | 复现确认 |
| **T19** | deai_check `--section 未知名` **静默返回 0 traces**：未知 section 设全文范围，但所有子检查器各自早退 → 拼错章节名得到"干净"结论 | scripts/deai_check.py:350-356 与 307-313,383-385,421-423,520-523 | 复现确认 |
| **T20** | em-dash 计数 bug：`count("---")+count("—")+count("——")` 对中文破折号 "——" 一处计 3 → 2 处即超 cap 5 必误报（ZH F5 同病） | scripts/deai_check.py:686 | 复现：2 个 "——" → 计 6 |
| **T21** | split_sections 同名章节覆盖 + 块注释盲区：第二个 "method" 模式标题覆盖前一个；只跳过 `//` 行，`/* */` 内 `= 标题` 仍当真；按 dict 序首中即停 | scripts/parsers.py:75-98,49-58 | 复现确认 |
| **T22** | optimize_title 无效词**子串匹配**："Renewable"含"new"、"Housing"含"using" → Critical 误报；`--optimize` 据此删词破坏标题 | scripts/optimize_title.py:166-172,342-358 | 复现确认 |
| **T23** | **PyYAML 硬依赖崩溃面**：deai_check 构造函数无条件 `import yaml`（yaml 不存在也 import）→ 安装到 ~/.claude/skills/ 后 deai 模块整体 ImportError。对比 verify_bib.py:122-130 的 lazy import 是正例 | scripts/deai_check.py:104,266 | 代码路径 |
| **T24** | check_format 正则 `#set\s+page\([\s\S]*?paper:` 跨全文懒匹配；figure 标签统计不支持嵌套括号（含 `image(...)` 的 figure 永远数不到）；caption 只认 `caption: [` | scripts/check_format.py:50,60,68,140,148 | 正则构造 |
| **T25** | check_references caption 检查：`caption: "..."`/变量形式 → "Missing caption" 误报；标签在 figure 闭括号下一行时静默跳过 | scripts/check_references.py:31,217-239 | 正则与 span 判定 |
| **T26** | examples 与路由表命令不一致：expression 示例用 `--section abstract`（对模板工程必失败，T7），SKILL.md 用 `--section methods`（必报错，T3）——同一模块两处示范两个都跑不通 | examples/expression-and-translation.md:12; SKILL.md:84 | 对照 T3/T7 |
| **T27** | evals.json 12 条全部 `"files": []`、断言只是宽松正则——无 fixture、无脚本行为断言；仓库已对 paper-audit 强制 eval-fixture 绑定，typst 无同等要求（ZH 模式 #14 复现） | evals/evals.json 全部 | 文件内容 |
| **T28** | **测试覆盖缺口**：check_references / check_tables / generate_table / deai_batch / online_bib_verify / translate_academic / analyze_abstract / analyze_grammar / analyze_sentences / improve_expression 共 10 个脚本零测试；conftest.py:21-23 的 `SCRIPT_DIR_TYPST` 是死常量（从未加入 sys.path） | tests/test_typst_paper_scripts.py:59-68; tests/conftest.py:21-23 | T1/T17 重灾区恰在无测试脚本里 |
| **T29** | 不可达脚本：deai_batch.py、check_references.py、online_bib_verify.py 不在路由表/Reference Map/任何模块文档中；generate_table 仅经 TABLES.md 可达但描述是 LaTeX 行为 | SKILL.md:73-92,145-155 | grep 无引用 |

### P2 — 质量与维护性

| # | 发现 | 位置(file:line) | 证据 |
|---|------|----------------|------|
| **T30** | 包版本过时/虚构组合：charged-ieee 钉 0.1.0（现行 0.1.4）3 处；测试 fixture `@preview/algorithmic:0.1.0` 调用 1.0 才有的 API；lovelace fixture 0.1.0（现行 0.3.1）调用不存在的 `#lovelace[...]` → fixture 真实 Typst 下不能编译，纯 regex 巧合通过 | templates/ieee.md:51; references/TEMPLATES.md:12; references/VENUES.md:103; tests/test_typst_paper_scripts.py:121,144,165 | §1.4 |
| **T31** | **Markdown 粗体泄漏进 Typst 示例**：VENUES.md:475 `[**Ours**]`（Typst 渲染不出粗体）；EXPERIMENT.md:21 与 analyze_experiment.py:38-39 要求 `**Title Case Heading.**` 起段并"禁止 `*...*`"——Typst 中 `*...*` 才是 strong，指导生成无效标记 | references/VENUES.md:475; references/modules/EXPERIMENT.md:21; scripts/analyze_experiment.py:38-39 | Typst 语法事实 |
| **T32** | **模块互相打架**：EXPRESSION/COMMON_ERRORS 推荐 use→employ/utilize、Notably、numerous；deai 模块把 notably(cap 3)、It is worth noting that、numerous(cap 3)、robust performance 全列为 AI 痕迹；EXPERIMENT.md:31 还示范 "demonstrates robust performance"——按 expression 润色再跑 deai 会被自家工具打回 | improve_expression.py:18-29; COMMON_ERRORS.md:56-60,151; AI_TONE_THRESHOLDS.yaml:21-26,54-56; EXPERIMENT.md:31 | 词表交叉对照 |
| **T33** | 孤儿引用文件 6 个：AI_TONE_TERMS.md、BEST_PRACTICES.md、REVIEWER_PERSPECTIVE.md、TERMINOLOGY.md、TRANSLATION_GUIDE.md、references/TEMPLATES.md 无入链；TEMPLATES.md 与 templates/*.md 双源冗余（charged-ieee 版本已漂移） | references/ 目录 | grep 引用计数 0 |
| **T34** | `errors="ignore"/"replace"` 静默吞编码错误共 14 处 | 14 个脚本 read 路径（详见原报告） | grep 列表 |
| **T35** | TYPST_SYNTAX.md 个别事实问题：`<eq:line>` 称 "Numbered equation"（实际需 `#set math.equation(numbering:)` 才编号）；"The method [1] shows..." 不是 Typst 引用语法（应为 `#cite(<key>, form:...)`）；539-548 嵌套围栏破坏渲染 | references/TYPST_SYNTAX.md:136-137,252-253,539-548 | 官方文档对照 |
| **T36** | NeurIPS 页数双源不一致：templates/neurips.md:13 "8 pages" vs VENUES.md:419 "9 pages"（后者正确）——路由优先加载错的那份 | templates/neurips.md:13; references/VENUES.md:419 | 两文件对照 |
| **T37** | `$SKILL_DIR` 约定无说明；模块文档另用 `../scripts/`、`scripts/` 两种相对路径，三种写法并存（ZH 模式 #10 复现） | SKILL.md:77-91; references/modules/* | grep 对照 |
| **T38** | analyze_experiment 对不存在的文件路径静默转入 prompt 生成模式：文件名拼错 → 输出 LLM prompt 而非报错 | scripts/analyze_experiment.py:306-308 | 分支逻辑 |
| **T39** | analyze_grammar `_apply_rules` 整行 lower() 后替换作为 "Revised" 输出（大小写全毁）；规则库仅 4 条玩具规则，与 GRAMMAR.md 宣称体量不符 | scripts/analyze_grammar.py:46-51,20-44 | 代码 |
| **T40** | 杂项死代码：analyze_literature 的 "literature"/"related work" 键永不存在；translate_academic 字面省略号永不匹配；check_tables `_result()` 重复全量重扫 + P3 超契约；analyze_abstract docstring 全是 main.tex | analyze_literature.py:70-74; translate_academic.py:48; check_tables.py:77,196; analyze_abstract.py:6-9 | 代码 |

## §3 确认健康、无需动的部分

- **SKILL.md 骨架**：165 行，渐进式加载、description 触发词质量好、Do-Not-Use 边界清晰、安全边界含 prompt-injection 防护，同类最佳实践。
- **check_pseudocode.py**：与 algorithmic 1.0.7 现行 API 一致（全 skill 里 Typst 事实最新的部分），分级合理，有测试。
- **verify_bib 的 BibTeX 半边**：平衡大括号解析、嵌套字段值、重复键检查、@comment/@string/@preamble 跳过，质量好且有测试。
- **online_bib_verify.py**：纯 stdlib、限速、CrossRef polite pool、DOI→标题回退，端点正确。
- **deai_check 主体设计**：阈值数据驱动、D1-D5 维度标注、双语词表，root 测试覆盖充分（除 T19/T20/T23）。
- **parsers.py 哈希对齐**：锁定生效，typst 拷贝与 EN canonical 仅差一行注释。
- **trigger_eval.json**：10 正 7 负，负样本精确覆盖姊妹 skill 边界。
- **大文件均有 TOC**。
- **外部事实大体准确的部分**：VENUES.md 会议页数速查表与现实一致；Typst 投稿接受度措辞克制；hayagriva 双格式支持陈述正确。
- **契约测试基础设施**：router-help 校验已存在（但只校验 flag 不校验 section 取值——T3 是测试盲区而非缺失）。

## §4 建议修复分组

**第 1 组：止血——让路由表的承诺成立（P0，先做）**：T3/T26（`--section method` 别名表）、T2（experiment 实际检查）、T1（check_references bib 白名单 + `:` 字符集）、T4/T5（Hayagriva 独立字段表 + citation 正则修复）。

**第 2 组：让脚本对真实论文形态生效（P0）**：T7（模板形参形态 + `= Abstract`，需同步 EN/audit/cover-letter 拷贝与哈希锁）、T6（typ_loader 多文件装配，移植 ZH 方案）、T8（检测模板 import 时跳过版式检查）。

**第 3 组：修文档里的 Typst 事实错误（P0/P1，纯文档，风险低）**：T9（8 处 column-gutter）、T10（gb-7714-2015-numeric）、T11（CLI 位置参数 + `{p}`）、T12-T15（五个模块文档按脚本 `--help` 重写）、T30/T31/T35/T36（包版本/粗体/eq 编号/NeurIPS 页数）。

**第 4 组：实现层缺陷（P1）**：T16（comment prefix 统一）、T17（--style 删或实现）、T18（watch+format）、T19/T20（未知 section 报错；em-dash 互斥匹配）、T21（同名聚合+块注释）、T22（`\b` 边界）、T23（yaml lazy import）、T24/T25（平衡括号+caption 放宽）。

**第 5 组：测试与评测补全（P1）**：T28（10 个零覆盖脚本补测试 + SCRIPT_DIR_TYPST 处理）、T27（evals 绑定 fixture：charged-ieee 风格 + bare 风格迷你工程，.bib/.yml 双参考文献）、T30（fixture 包版本改真实可编译组合）。

**第 6 组：一致性与瘦身（P2，最后）**：T32（expression/deai 词表冲突对照）、T33（孤儿文件六选二处理）、T34/T37-T40（编码、$SKILL_DIR 说明、prompt 模式显式开关、大小写保留、死代码清理）。

**总体判断**：骨架（路由、安全边界、测试基建、deai/pseudocode 两模块）在平均线以上，但存在两类系统性塌方——(a) 约半数模块文档描述的是 LaTeX 姊妹版脚本的 CLI 与行为（T12-T15），(b) 脚本层对"真实 Typst 论文的两种主流形态"（模板工程、多文件工程）整体失效（T6-T8，T1 对任何带引用的论文失效）。ZH 审计清单 18 个模式中 14 个在本 skill 复现（仅 #9 Gemini 残留、#13 rglob 两项未中招）。
