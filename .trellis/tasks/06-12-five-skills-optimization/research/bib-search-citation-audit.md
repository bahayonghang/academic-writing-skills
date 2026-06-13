# bib-search-citation 审计报告（agent 原始产出，2026-06-12）

> 审计方式：全量代码审读 + 临时目录 .bib fixture 实测复现 + 网络调研。仓库内零修改。

## §1 外部环境调研结论（附来源）

1. **BibTeX vs BibLaTeX 字段差异**：biblatex 以 `journaltitle` 取代 `journal`、以 `date`（yyyy-mm-dd）取代/补充 `year`，`journal`/`year` 仅作向后兼容别名保留（biblatex 手册 §2.2.5 Field Aliases）；Zotero Better BibLaTeX 导出原生使用 `journaltitle` + `date`。**本 skill 的 `entry_year()` 已正确回退到 `date` 字段（健康），但 `derive_venue()` 完全遗漏 `journaltitle`（B9，实测确认）**。来源：biblatex 手册 (CTAN mirrors.ctan.org/macros/latex/contrib/biblatex-ms/doc/biblatex-ms.pdf)、economics.utoronto.ca/osborne/latex/BIBTEX.HTM、Zotero Forums discussion/48645、JabRef #521。
2. **GB/T 7714-2025**：2025-12-02 发布、2026-07-01 实施，全部代替 2015 版；新增**数据集、预印本**等新型文献类型著录规则，取消非网络文献访问日期，统一著录符号。对本 skill 的影响是**间接的**：它是检索层而非著录格式层，无需像 ZH skill 那样接 `--standard gb7714-2025`；但新国标驱动中文文献库出现更多 `@dataset`/`@online`/`@software` 条目——实测这些 biblatex 类型可解析、可按 `type:` 过滤（健康），唯 venue 派生缺口（B9）会让这类条目 venue 恒空。来源：std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F、journals.csu.edu.cn/news-detail/1555、cbyys.sppc.edu.cn DOI 10.19619/j.issn.1007-1938.2026.00.011。
3. **Citation key 主流约定**：Zotero Better BibTeX 默认 `auth.lower + shorttitle(3,3) + year`（如 `doeMambaForecasting2024`，纯字母数字）。本 skill 不生成 key 只消费 key，`typst_citations()` 的 `[A-Za-z0-9_-]+` 正则覆盖 BBT 默认格式；DBLP 风格 key（含 `:` `/`）正确回退到 `#cite(label("..."))`——**与主流约定无冲突（健康）**。来源：retorque.re/zotero-better-bibtex/citing/、guides.library.yale.edu/bibtex/zotero-and-latex。
4. **DOI 元数据 API 现状**：本 skill 明确将在线校验排除在边界外（SKILL.md "Do Not Use"，健康）。若未来扩展需注意：Crossref 2025-12-01 起新限流规则；**OpenAlex 2026-02-13 起废除 mailto polite pool、强制 API key（无 key 仅 100 免费 credit 后 409）**；DataCite 2026-07-01 弃用 legacy endpoint。来源：crossref.org/blog/announcing-changes-to-rest-api-rate-limits/、groups.google.com/g/openalex-users/c/rI1GIAySpVQ、docs.openalex.org rate-limits、support.datacite.org/docs/upcoming-changes。

## §2 审计发现总表

以下所有"实测"均为在系统临时目录构造 .bib fixture 后用仓库脚本直接复现的结论。

### P0 — 静默丢数据 / 核心检索契约失真

| # | 发现 | 位置 (file:line) | 证据 |
|---|---|---|---|
| B1 | **花括号值内的裸引号吞掉后续所有条目**。BibTeX 中 brace 定界值内 `"` 是普通字符，但解析器无条件切换 `in_quotes`，之后所有花括号被忽略 | `scripts/search_bib.py:553-572`（`parse_bib_entries` 主循环 `if char == '"': in_quotes = not in_quotes`） | 实测：`title = {Floppy disks of 3" form factor}` 后跟 2 个合法条目的文件，**3 条只解析出 1 条**，且该条 year/venue 全损；无任何警告，`total_entries` 直接少报 |
| B2 | **一个缺失闭括号静默吞掉文件剩余部分，无 resync、无警告**。SKILL.md 承诺"report that entries may have been skipped"，但脚本 meta 中没有任何 parse 异常信号 | `scripts/search_bib.py:552-575`（depth 永不归零时 pos 跑到 EOF）；对照 `SKILL.md:201-202` | 实测：3 条目文件中第 1 条缺 `}`，**只解析出 1 条**（且字段错乱），后 2 条合法条目丢失；输出 JSON 与正常结果无任何区别 |
| B3 | **recency 加分泄漏过 `score>0` 相关性过滤：完全无关的查询返回所有带年份的条目**。`score_entry` 对零文本匹配的条目仍加 `(year-2000)*0.03`，而 `run_search` 用 `score>0` 判定"匹配" | `scripts/search_bib.py:827-829` + `:984` | 实测：对纯预测类文献库查询 `quantum cryptography blockchain consensus`，**返回 5 条结果**（score 0.72–0.75），正确行为是 0 条。假阳性引文源头 |

### P1 — 崩溃 / 主流文献库检索失效 / 契约错位

| # | 发现 | 位置 (file:line) | 证据 |
|---|---|---|---|
| B4 | **强制 utf-8 读取，latin-1 旧 .bib 直接裸 traceback**；文件不存在裸 `FileNotFoundError`。`main()` 只捕获 spec 错误，违反自身 JSON 错误输出契约（stderr JSON + exit 2） | `scripts/search_bib.py:1011-1012`、`:1003-1009` | 实测：latin-1 的 `Fran\xe7ois` → `UnicodeDecodeError`；`--bib nonexistent.bib` → 裸 `FileNotFoundError` |
| B5 | **Windows 非 UTF-8 控制台输出崩溃**：`json.dump(ensure_ascii=False)` 写 stdout，zh-CN 默认 cp936 下任何含非 GBK 字符（Ł、ő、ā 等）的结果直接崩溃 | `scripts/search_bib.py:1016` | 实测（Python 3.14, cp936）：`Łukasz Kaiser` → `UnicodeEncodeError: 'gbk' codec...`。本仓库作者环境即 zh-CN Windows |
| B6 | **LaTeX 重音转义破坏作者/标题检索**：`normalize_text` 不处理 `\"` `\'` 等转义，`G{\"u}nther M{\"u}ller` 归一化成 `G \"u nther M \"u ller` | `scripts/search_bib.py:24`（`LATEX_ESCAPE_RE` 仅覆盖 `\%&_#$`）、`:301-311` | 实测：`author:Müller`、`author:Muller`、`author:Gunther`、`author:López`、`author:Lopez` **全部 0 命中** |
| B7 | **@string 宏不展开、`#` 串接保留原文**：`journal = ieee_tgrs` 的 venue 输出为字面量 `'ieee_tgrs'`；单定义 `@string`（无逗号）被静默跳过 | `scripts/search_bib.py:532-619`（无宏表） | 实测 venue=`'ieee_tgrs'`、`'Journal A # Part B'`。IEEE/ACM 官方 .bib 大量用 @string；按 venue 检索/展示全失效 |
| B8 | **crossref 字段不解析**：子条目不继承父条目的 year/booktitle，年份过滤将其静默排除 | `scripts/search_bib.py:622-638` | 实测：`@inproceedings{crossref_child, crossref={neurips2024}}` → `year=None, venue=''` |
| B9 | **biblatex `journaltitle` 不在 `derive_venue` 候选列表**：Better BibLaTeX 导出库的 venue 恒空，venue 显示、`venue:` 过滤、venue 权重 2.5 的评分全部失效 | `scripts/search_bib.py:634-638` | 实测：`@online{..., journaltitle = {...}}` → `venue=''`。trigger_eval.json:31 还专门有 `venue:NeurIPS` 触发用例 |
| B10 | **带逗号的 `@comment`/`@string` 产生幻影条目并参与检索**（JabRef 导出固定带 `@comment{jabref-meta: ...}`） | `scripts/search_bib.py:541` + `:604-617` | 实测：`@comment{This is a comment, with...mamba}` 被解析为条目并以 **score 3.0 出现在查询结果**；`@string{a={X}, b={Y}}` 产生幻影条目，`total_entries` 虚增 |
| B11 | **`--claim`/`--include-raw-bib`/`--citation-mode`/`--sort`/`--limit`/`--recent-window`/`--return-fields` 在 `--spec-json`/`--spec-file` 模式下全部静默忽略**；SKILL.md:120 称 "when `--claim` was supplied" 无模式限定 | `scripts/search_bib.py:133-140` 对照 `:161-179` | 实测：`--spec-json '{"query":"mamba"}' --claim "..." --include-raw-bib --citation-mode latex` → `claim_support`/`raw_bib`/`citations` **全部缺失** |
| B12 | **未知 filter 键与拼错字段名双重静默失败**：spec 里 `venue_contains`（LLM 易臆造键名）被无声忽略 → 返回未过滤全集；compact 查询拼错 `tilte:accent` → 无声 0 结果 | `scripts/search_bib.py:736-792`、`:410-418` | 实测：`{"filters":{"venue_contains":["Neural"]}}` → matched 9/9；`mamba tilte:accent` → 0 结果且 `applied_filters` 照常回显 |
| B13 | **SKILL.md 自相矛盾：`allowed-tools: Read, Bash(uv *)` 与 Workflow/RTK 段指示的 `rtk find`/`rtk read`/`rtk grep` 互斥**；RTK 是维护者私有全局工具，写进可分发 skill 属于个人环境泄漏 | `SKILL.md:25` vs `SKILL.md:140-155` | 静态矛盾；分发后必然失效或触发权限拦截 |

### P2 — 质量 / 卫生 / 失同步

| # | 发现 | 位置 (file:line) | 证据 |
|---|---|---|---|
| B14 | 作者匹配仅大小写不敏感子串：`author:"Jane Doe"` 不匹配 `{Doe, Jane}`（实测 0 命中）；无 von/姓-名顺序归一。query-syntax.md:273 把 `author:chen` 匹配 `Cheng` 当优点宣传——假阳性陷阱 | `search_bib.py:755-759`；`references/query-syntax.md:273` | 实测确认 |
| B15 | 计数语义误导：`matched_entries` 只数 filter 匹配，不反映 query 淘汰；preview 显示 "returned=1 of 3 matched" 误导。与 B3 叠加更不可信 | `search_bib.py:979-995`；`preview_bib_search.py:179` | 代码路径明确 |
| B16 | CJK 多关键词检索失效：TOKEN_RE 把整段中文当一个 token，空格分隔的 2–3 字中文词（`预测 光伏`）不命中（被 B3 掩盖仍被返回）。连续子串（`时间序列`）靠 phrase bonus 可命中 | `search_bib.py:23`、`:815-820` | 实测确认 |
| B17 | `limit:0` 被 `int(spec.get("limit", 5) or 5)` 变成 5；负数 limit 走负切片语义 | `search_bib.py:977` | 实测：`limit:0 → returned 5` |
| B18 | 任意 `word:word` 自由文本被吞为 generic field filter（FIELD_OP_RE 几乎匹配一切），与 query-syntax.md:84 承诺不符 → 无声 0 命中 | `search_bib.py:26-28`、`:410-418` | 实测 |
| B19 | 死代码：`spec_from_compact_query` 中 `kind == "free"` 分支不可达；`FIELD_ALIASES` 含 3 个恒等映射 | `search_bib.py:342-343`、`:68-82` | 静态可证 |
| B20 | **测试重复且漂移**：根 `tests/test_bib_search_citation.py`（7 用例）是 skill 内 `tests/test_bib_search.py`（10 用例）的过期子集，缺 recency/claim 3 个用例；`just test` 双重收集（collect-only=17）。根副本是应删未删的孤儿 | 两文件对比；conftest.py:31-32 | 实测 17 collected |
| B21 | 契约测试盲区：`test_skill_contracts.py` 中本 skill 无 `router_help: True`（另四个 skill 都有） | `tests/test_skill_contracts.py:30-36` vs `:503-515` | 配置对比 |
| B22 | 文档站副本失同步：`docs/skills/bib-search-citation/resources/query-syntax.md`（5546B）缺 v5.2 的 claim/recency 全部内容（skill 内版 7554B 有）；zh 版同构 | 两文件 diff | 实测确认 |
| B23 | evals.json 空洞断言：id 2/5 的 `not_contains: "fabricated"/"invented"` 恒通过；id 1 `contains: "query"` 几乎任何回复都含 | `evals/evals.json:23,34,56` | 静态可证 |
| B24 | `argument-hint: "[library.bib] [--query QUERY]"` 暗示位置参数，脚本实际要求命名参数 `--bib`（required） | `SKILL.md:24` vs `search_bib.py:91` | 静态可证 |
| B25 | 多文件库不支持：`--bib` 单文件；SKILL.md 未提应对 | `search_bib.py:91`；`SKILL.md:92` | 设计现状 |
| B26 | `entry_year` 正则 `\b(19|20)\d{2}\b` 不识别 1800s 文献，year=None 后被年份过滤静默排除 | `search_bib.py:624` | 静态可证 |

## §3 确认健康、无需动的部分

- **零外部依赖**：两个脚本纯 stdlib，装到 `~/.claude/skills/` 无 import 崩溃风险。
- **无 Gemini/google_web_search 残留、无 TODO/FIXME**。
- **`$SKILL_DIR` 占位符约定全仓 6 个 SKILL.md 一致**。
- **`agents/openai.yaml` 非孤儿**：6 个 skill 均有，且 `test_openai_yaml_shape` 做形状校验。
- **测试覆盖存在**：skill 自带 10 个集成测试（含 stdin/文件双模式、截断、recency、claim、raw_bib 隐藏）。真正问题是 B20 重复与 B21 盲区。
- **嵌套花括号正确处理**：`{{TimeMachine}}`、`{The {GPT} Model}` 剥离正确。
- **biblatex 专有类型可用**：`@online/@software/@dataset` 解析、`type:` 过滤正常；`date` 字段年份回退已实现。
- **引号定界值、字段续行/多行值、字段名大小写**均正确。
- **Typst 引用回退设计正确**：非 `[A-Za-z0-9_-]+` 的 key 回退 `#cite(label("..."))` 并标 `needs_label`。
- **安全边界文案优秀**：.bib 字段视为不可信数据、prompt-injection 防护、claim_support 的 "NOT proof" 双层声明、raw_bib 原样保真。
- **版本同步**：SKILL.md 5.2.0 == pyproject 5.2.0。
- **trigger_eval.json 边界质量好**：17 条含中英、负例覆盖姊妹 skill 边界。
- **preview_bib_search.py**：纯渲染器定位准确，未发现缺陷。
- **`has:pdf` 的 Zotero file 字段 MIME 检查**正确。
- **filter-only 查询语义自洽**：空 query 提前返回 score 0，不受 B3 影响。

## §4 建议修复分组

**A 组 — 解析器鲁棒性（P0，优先）**：B1/B2/B10
重写 `parse_bib_entries` 引号状态机：brace 定界内 `"` 视为普通字符；depth 异常时 resync 到下一个行首 `@` 重扫；`@string/@comment/@preamble` 显式识别（@string 进宏表，另支撑 B7）；`meta` 增加 `parse_warnings`/`skipped_spans`。把本次审计的 quote_trap/broken/phantom 三个 fixture 收编为回归测试。

**B 组 — 检索正确性（P0/P1）**：B3/B6/B7/B8/B9
B3 recency 加分改为仅对已有正分条目加成（或挪到 tie-break）；B6 normalize_text 增加 LaTeX 重音映射表（`{\"u}`→ü + ASCII 折叠）；B9 `derive_venue` 插入 `journaltitle`（一行修复收益最大）；B7 @string 展开 + `#` 串接；B8 crossref 两遍解析继承。

**C 组 — CLI/错误契约（P1）**：B4/B5/B11/B12/B17/B24
文件读取纳入 JSON 错误契约，utf-8 失败回退 latin-1 并 meta 标注；`sys.stdout.reconfigure(encoding="utf-8")`；CLI override 统一应用于三种输入模式（或报 SpecError）；未知 filter 键报错/警告；limit 边界校验；argument-hint 修正。

**D 组 — 文档与测试卫生（P2）**：B13/B14/B15/B16/B18/B19/B20/B21/B22/B23/B25
删 SKILL.md RTK 段（或放宽 allowed-tools 并改通用措辞）；删根目录重复测试文件；加 `router_help` 契约校验；同步 docs 站 query-syntax；修正 query-syntax.md 的 `author:chen` 误导表述；加强 evals 断言；SKILL.md 记录多文件库与 CJK 多关键词限制。

**总体评价**：结构、安全边界、触发边界、渐进式加载（SKILL.md 259 行）属全仓较好水平；但 .bib 解析器对真实世界文件的鲁棒性是系统性短板，叠加 B3 评分泄漏，"检索→引用"主链路在 fixture 之外的真实文献库上可信度不足，A/B 组先行。
