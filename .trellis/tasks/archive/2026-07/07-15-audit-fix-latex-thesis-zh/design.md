# 技术设计 — 07-15-audit-fix-latex-thesis-zh

> 依据：本任务 prd.md（A-ZH-1..9 + D5）。所有行号已核实于当前 dev。
> zh 副本约定：`latex-thesis-zh/scripts/parsers.py` 是按技能副本（保留中文 docstring，`clean_text` 有意缺席且被 `test_parsers_alignment.py:158-166` 锁定为「zh 无」），zh 不在 deai strict 锁内。**本设计不新增/删除 zh 的 `clean_text`。**

## (a) R1/A-ZH-1：conclusion 章节规则 + SECTION_KEY_ALIASES

### 锚定策略（LaTeX 与 Typst 统一）

统一采用**全串锚定 + 可选后缀**的精确式规则（与 abstract/introduction 等既有精确式规则同族）：

```python
("conclusion", 2, r"^(?:结论|总结)(?:与展望)?$"),   # LaTeX, parsers.py:183
("conclusion", 1, r"^(?:结论|总结)(?:与展望)?$"),   # Typst,  parsers.py:308（max_level 保持 1 不变）
```

覆盖：`结论`、`总结`、`结论与展望`、`总结与展望`。
不匹配（过匹配守卫）：`结论性章节`、`实验结论分析`、`总结报告`、`结语`（后者不在本次范围，保持最小改动）。

- 分类入口是 `normalize_heading_title`（:209-216，去 `\quad`/空白）后的整串标题，`^…$` 锚定即全串匹配，`结论性章节` 天然不命中。
- Typst 侧 :308 现为未锚定 `(?:结论|总结与展望)`——改锚定后，原本被子串误配为 conclusion 的标题（如 `结论性章节`）不再命中，属**误报修复类默认行为变化**，按 spec 约定双声明。
- 规则顺序不动：conclusion 精确式在 method/experiment 等 contains 式之前（:178-188 / :303-313），`总结与展望` 不会先落入其它键。
- 废弃的 `SECTION_PATTERNS` 字典（:162-172 / :291-301，注释已标 Deprecated）**不改**——外科手术原则，且无消费方。

### SECTION_KEY_ALIASES（:96-122）

新增一条：`"结论与展望": "conclusion"`（`结论`/`总结`/`总结与展望` 已存在 :119-121）。`resolve_section_keys`（:125-139）逻辑不动。

### 对齐锁影响（已核对 tests/contracts/test_parsers_alignment.py）

zh 在 ALIGNMENTS 中被锁的只有三项：`_normalize_whitespace`(:77)、`LatexParser.PRESERVE_PATTERNS`(:82)、`TypstParser.PRESERVE_PATTERNS`(:83)。**本项改动的 `SECTION_TITLE_RULES`（LaTeX/Typst）、`SECTION_KEY_ALIASES`、`_classify_heading` 的 zh 副本均不在锁内**（:96/:102/:106/:110/:112 的锁列表都是 en/typst/audit/cover_letter），因此不需要 ALIGNMENTS 更新；约束是**不得顺手改**上述三个 zh 已锁成员。

### 下游联动

`analyze_conclusion.py:173` 的跳过分支由 split_sections 直接驱动，无需改代码，只补端到端回归。按 spec「检查器适配新结构形态要跑完整输出回归并扫兄弟检查器」：grep 消费 `sections.get("conclusion")`/`"conclusion"` 键的兄弟脚本（analyze_experiment / analyze_logic / analyze_abstract）各跑一次完整输出回归，确认无同型漏检或新增误报。

## (b) R2+R3/A-ZH-2+A-ZH-3：verify_bib 平衡扫描器（D5）+ 编码

### 复用先例，不造第三套解析器

bib-search-citation 的 `search_bib.py` 已实现工业级扫描：`split_top_level`(:652)、`_scan_entry_span`(:734，引号内花括号字面处理、未闭合返回 closed=False)、`parse_fields`(:724)、`resolve_field_value`(:699)、`parse_bib_entries`(:777，@comment/@preamble 跳过、@string 宏、截断条目 warning+resync)。

技能安装隔离（各 skill 独立装到 `~/.claude/skills/`）导致**不能跨技能 import**，故做 **vendored 适配**：新建 `latex-thesis-zh/scripts/bib_scan.py`，逐字节拷贝上述五个函数 + `_find_key_separator` + `_line_of`（文件头注释标注来源 `bib-search-citation/scripts/search_bib.py` 与同步义务），**不拷贝** crossref 解析、重复键 Counter、相关性评分等 search 专属逻辑。函数名保持一致，为将来若建立 bib 扫描对齐锁留接口（本任务不建锁——目前无 contract 测试锁 bib 解析，避免范围膨胀）。

### verify_bib.py 改造

1. `parse()`（:63-86）重写：
   ```python
   from tex_loader import read_text_robust          # 带 sys.path fallback，样板 check_references.py:22-26
   from bib_scan import parse_bib_entries

   text, enc_warning = read_text_robust(self.bib_file)
   raw_entries, parse_warnings, _macros = parse_bib_entries(text)
   ```
   映射回既有 entry 形状 `{"type", "key", "fields", "raw"}`（`entry_type→type`、`raw_bib→raw`），`self.entries` 语义不变，`_parse_fields`(:88-96) 与 :73 的 entry_pattern 删除（本次改动产生的孤儿）。
2. 警告落 issues：`enc_warning` → `{"key": "-", "type": "encoding_warning", "severity": "warning", "message": ...}`；`parse_warnings` 中 `unbalanced_entry`/`commented_entry_included` → severity warning 同形转换。放进 `verify()` 的 `results["issues"]`，走既有 FAIL/WARNING/PASS 判定（:133-140）。
3. 行为变化声明（假绿修复例外，均需 commit message 声明 + 存量单测同步）：
   - 值含 `@` 的文件条目数恢复正确（原静默吞并）；
   - 含 `^` 字段恢复解析（原 `$L^2$` 误报 missing_field/caps FAIL）；
   - GBK bib 从「乱码假 PASS」变为「正确解析 + WARNING（encoding_warning）」。
4. `@string` 宏展开随 vendored 代码免费获得；`fields` 值为展开后的字符串，caps 检查（:221-233）语义不变。

### check_spec._load_bib（check_spec.py:318-346）

仅编码修复（父任务处置即如此）：`p.read_text(encoding="utf-8", errors="replace")`（:336）→ `read_text_robust(p)`，warning 拼进返回的 `bib_note` 第三元组元素。条目计数正则（:341）不动——它只数 `@type{` 起始，扫描器级重构对计数收益有限，超出 A-ZH-3 范围。

### fixture（命名缺口 ②③）

- tmp_path 合成：`^` 字段（`title = {The $L^2$ Norm}`）、`@` 值（`note = {mail: a@b.edu}` 后接第二条目）、嵌套花括号（`title = {{Deep {Learning}} Methods}`）、引号值内花括号、未闭合条目 resync。
- 仓库 fixture：`evals/fixtures/thesis-project/references-gbk.bib`，GB18030 编码写入 2-3 条**虚构**中文条目（含中文 author/title、无 langid → 触发 `gb_langid_hint`），`thesis-project/README.md` 补一行埋点说明。单测经 `tests.support.paths.SKILLS_ROOT` 引用。**不改 evals/evals.json**（避免 JSON hook 陷阱；接入 eval 另行任务）。

## (c) R4/A-ZH-4：check_references 文件归属

`LabelInfo.file`/`RefInfo.file`（:57/:66）已存在，缺的只是 issue 落字段与渲染。**决策：不改用 `assemble()`**——该脚本的多文件架构（`iter_files` + 按文件独立扫描，:345-363）本就保留了精确 per-file 行号，切换 assemble+origin 是无收益重写；只对**输出格式**对齐 `tex_loader.lineref` 的多文件显示约定（`源文件:行号`），与兄弟检查器（check_format.py:258、check_tables.py:96 的 `doc.origin`）产出的定位格式一致。

1. `all_files` 的键从 `str(node.path)` 改为 `node.rel`（`iter_files` 已提供相对路径，:346-349），LabelInfo/RefInfo.file 随之为 rel 路径；
2. `_add_issue`（:96-112）加 `file: str | None = None` 参数并写入 issue dict；五个 check 方法把 `lbl.file`/`ref.file` 传入；
3. `ThesisReferenceChecker` 增加 `self.multi_file = len(self.all_files) > 1`；
4. `_format_issues`（:396-408）签名加 `multi_file: bool = False`：多文件时位置渲染为 `{file}:{line}`，单文件保持 `(Line {line})` 逐字节兼容；`--json` 恒输出 `file` 键（增量）。

## (d) R5/A-ZH-5：compile.py 指令优先

`_detect_compiler`（:90-116）重排为：
1. `% !TEX program = xelatex|lualatex|pdflatex`（原 :104-109 三条正则，提到最前）；
2. `CHINESE_PATTERNS` 循环（原 :98-102）；
3. fontspec（:112-114）；
4. `pdflatex` 兜底。

读取（:93）改 `read_text_robust`（sys.path fallback import，样板 check_references.py:22-26；`except Exception: return "pdflatex"` 兜底保留）。GBK 中文论文由 GB18030 解码后命中 `[一-鿿]` 特征。指令优先属误报修复（用户显式声明引擎被无视），双声明。

## (e) R6/A-ZH-6：平衡花括号 heading/title 提取

1. vendored `_extract_balanced_block`：从 `latex-paper-en/scripts/parsers.py:518-538` **逐字节**拷入 zh parsers.py（含英文 docstring——为可入锁，接受此函数不用中文 docstring）。
2. `HEADING_PATTERN`（:145-147）改为只定位命令与开括号：
   ```python
   HEADING_PATTERN = re.compile(
       r"\\(?P<command>chapter|section|subsection|subsubsection|paragraph)\*?"
       r"(?:\[[^\]]*\])?\{"
   )
   ```
   `extract_headings`（:258-279）在 match 后调 `_extract_balanced_block(stripped, match.end() - 1, "{", "}")` 取完整 title；返回 `""`（跨行/未闭合）时跳过该行——与旧行为对跨行标题的净效果一致（旧正则同样要求本行闭合）。
3. `extract_title`（:411-426）：`re.search(r"\\ctitle\{", ...)` / `r"\\title(?:\[[^\]]*\])?\{"` 定位后用 `_extract_balanced_block(content, m.end() - 1, "{", "}")` 取值，再走 `_strip_latex_markup`。DOTALL 场景（跨行标题）由字符扫描天然支持。
4. **ALIGNMENTS 更新（显式声明）**：`test_parsers_alignment.py:78` `("_extract_balanced_block", ["en", "typst", "audit", "cover_letter"])` → 列表加入 `"zh"`。这是本任务唯一的 contract 锁改动。zh 的 `HEADING_PATTERN`/`extract_headings`/`extract_title` 均不在 zh 锁内（:88/:101/:104 只锁 en/audit/cover_letter），改动自由；**不得触碰** zh 已锁三项（见 (a)）。
5. 消费方核查（已 grep）：zh 内 `extract_title` 消费方为 analyze_abstract.py:876、check_spec.py:383、optimize_title.py:498，均为纯读取，受益无接口变化；`HEADING_PATTERN` 无 parsers.py 之外的消费方。

## (f) 三个 Low 项

### R7/A-ZH-7 mixed_punctuation

`check_format.py` 新增模块级 `_KEY_ARG_RE`（与 `_PATH_ARG_RE` :55 并列）：

```python
_KEY_ARG_RE = re.compile(
    r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|pageref|label)\*?\{[^}]*\}"
    r"|\\hyperref\[[^\]]*\]"
)
```

在 :274-275 的 `strip_path_args` 分支同处应用（等长空格占位，列号不漂移）。只影响 `strip_path_args: True` 的 mixed_punctuation 一个检查；`missing_space_after_cite`（:77-82）依赖 `\cite{}` 原文匹配，不加此剥离（其 check 无 strip_path_args 标志，天然不受影响）。不改 `visible_only`（改 True 会连带 `$...$`、单行环境剥离，影响面不可控）。

### R8/A-ZH-8 缩写 stoplist + 阈值

`check_consistency.py` 抬升为模块级常量：

```python
ABBREV_STOPWORDS = frozenset({
    "PDF", "URL", "HTTP", "HTTPS", "API", "TODO", "FIXME",     # 原 7 词（:237）
    "IEEE", "ACM", "ISO", "IEC", "GB", "DOI", "ISBN", "ISSN",
    "GPU", "CPU", "RAM", "USB", "FPGA", "LED", "MCU",
})
ABBREV_MIN_USES = 2
```

`check_abbreviations`（:211-276）：:237 的内联 list 换用常量；undefined 分支（:246-257）条件加 `len(usage_list) >= ABBREV_MIN_USES`。multiple_definitions 分支不动。词表边界：只收「文档基建/标准机构/通用硬件」类，不收领域缩写（CNN/LSTM 等仍应要求定义）。

### R9/A-ZH-9 gb7714-2025 注记（防契约破坏）

- `SKILL.md:67` bibliography 行只改「Use when」列文案：`GB/T 7714 or BibTeX validation（2026-07 起可加 --standard gb7714-2025 按新国标检查）`。**主命令 backtick 内容不改**——`ROUTER_ROW_RE`（test_skill_contracts.py:163-165）只捕获 module 与 command 两个 backtick 组，Use-when 列自由；`_assert_module_router_commands_match_script_help`（:483-512）要求命令里的 `--` 选项出现在脚本 `--help` 中，`--standard` 已在 help（verify_bib.py:439-445），不新增风险。改表后仍须跑该 contract（hook 重排表格陷阱，见 memory）。
- `check_spec.py:169-175` `MODULE_COMMANDS` 的 bibliography 行**上方加注释**（`# 2026-07-01 起 GB/T 7714-2025 实施，可改用 --standard gb7714-2025`），**不改命令字符串值**——该值直接进 spec-check 的 MODULE 证据输出（:737-738），改值即默认行为变化，无必要。
- `references/modules/bibliography.md` 加一句 2025 选项说明（该文件无字符串锁；docs 双语资源契约只关心文件存在性与 manifest，不锁内容——但改后跑 `tests/contracts/test_docs_bilingual_resources.py` 兜底）。

## (g) 风险与回滚

| 风险 | 缓解 | 回滚点 |
|------|------|--------|
| verify_bib 重写改变存量输出形状，下游（evals、SKILL.md 示例）隐性依赖 | entry dict 形状与 report 文案不变；只增 issue 类型；先跑存量 gb7714/scripts 测试再动 | R2/R3 独立 commit，revert 即回旧正则 |
| Typst conclusion 锚定后原误配文档「少了」conclusion 键 | 属误报修复例外；commit message 双声明；负例测试锁定语义 | R1 独立 commit |
| ALIGNMENTS 加 "zh" 后与 EN 任务（07-15-audit-fix-latex-paper-en 改 canonical parsers）互踩 | 本任务只在 `_extract_balanced_block` 一项加 "zh"；若 EN 任务改了该函数源，本任务 rebase 后重新逐字节拷贝即可（锁会红，红即提醒）；父任务排序约定 en 先合 | R6 独立 commit |
| `all_files` 键改 rel 路径影响 check_references 内部一致性 | 键只在类内部消费（:361/:374/:380-386 已核查），一次性同改 + multifile 存量测试回归 | R4 独立 commit |
| SKILL.md 表格被格式化 hook 重排触发 ROUTER_ROW_RE 断言 | 改后立即跑 `tests/contracts/test_skill_contracts.py`；只动 Use-when 文案 | R9 独立 commit |
| GBK fixture 在 CRLF/编码上被编辑器或 hook 误转码 | 用 Bash python 以 bytes 写入（不走 Edit/Write）；测试断言原始字节可被 GB18030 解码 | fixture 独立 commit |
| compile.py 指令优先改变既有用户工作流 | 仅当文档显式写 `% !TEX program` 才改变结果（尊重显式声明）；双声明 | R5 独立 commit |
