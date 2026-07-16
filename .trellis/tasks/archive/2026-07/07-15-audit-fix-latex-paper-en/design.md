# 技术设计 — 07-15-audit-fix-latex-paper-en

前置阅读：`tex_loader.py` 全文（API 见下）、`parsers.py:115-201/593-622`、
`tests/contracts/test_parsers_alignment.py`、`tests/contracts/test_deai_alignment.py`、
`tests/contracts/test_writing_modules_alignment.py`（§2.6 涉及的 Tier-1 哈希锁）、
`tests/shared/test_en_family_parsers_multifile.py`（可复用的 fixture 样板与既有 tex_loader 测试）。

---

## 0. 关键事实（实读代码得出，纠正两处父 PRD 用语）

1. **ALIGNMENTS 不存字面哈希**。`test_parsers_alignment.py:75-113` 的 `ALIGNMENTS` 是
   `(dotted_path, [copies])` 列表，运行时对各副本成员做 `inspect.getsource`/`repr` 的 md5
   **动态互比**（:121-133）。所谓"更新哈希"实操上是：改 canonical 后把列内副本改到逐字节一致；
   `ALIGNMENTS` 列表本身只在**新增/移除共享成员**时编辑。本任务恰有一处列表编辑（§3.4）。
2. **deai 锁与 parsers 锁是两套**。`test_deai_alignment.py` 锁 `deai_check.py` 三副本
   （en/zh/typst）；其 `ALIGNMENTS`（:134-154）锁 `analyze_document`、`generate_suggestions_json`、
   `_find_pattern_in_section` 等；`__init__`、`main`、`check_section`、`generate_report`
   是**登记过的分歧成员，不锁**（docstring :22-26）。§2.3 的 deai_check 接入方案完全落在不锁成员内。
3. **还有第三套锁：writing-modules Tier-1 哈希锁**。`test_writing_modules_alignment.py`
   `TIER1_HASH_GROUPS`（:71-85）要求 `analyze_abstract.py`（:76）、`analyze_grammar.py`（:77）、
   `analyze_sentences.py`（:78）、`improve_expression.py`（:79）的 **en/typst 副本整文件逐字节一致**
   （sha256，CRLF/BOM 归一后互比）。这四个脚本任何一处 assemble 改动都必须以 loader 无关写法落地并
   同步 typst 副本（§2.6），否则该契约测试红。原 design 漏记了 analyze_abstract 也在此锁内，本版补上。

## 1. tex_loader.assemble() API（现状，零改动）

`latex-paper-en/scripts/tex_loader.py`：

- `assemble(entry: Path) -> AssembledDocument`（:167-235）：按文档序内联展开
  `\input/\include/\subfile`（INCLUDE_RE :24，花括号紧跟命令，不误吞 `\includegraphics`）；
  注释行/行尾注释里的 include 不展开（:204-208）；环检测 visited（:195-197）；缺失文件记入
  `doc.missing` 不中断（:220-221）；编码走 `read_text_robust`（utf-8 → latin-1 → replace，:29-46），
  告警进 `doc.warnings`。`.typ` 入口原样读入、不装配（:177-185）→ 本任务所有脚本对 `.typ`
  输入行为自动保持不变。
- `AssembledDocument`：`content`（拼接文本）、`lines`、`multi_file`、
  `origin(line_no) -> (rel_path, src_line)`（:135-139）、
  `lineref(start, end=None) -> str`（:141-157）——**单文件返回 `Line 15` / `Line 15-20`，
  与旧输出逐字节兼容；多文件返回 `sections/intro.tex:15`**、
  `warning_lines(comment_prefix)`（:159-164）。

单文件不变性由 `lineref` 的设计直接保证（`multi_file=False` 分支 :150-152）；因此"单文件行为
逐字节不变"的验收只需既有测试不改断言即绿。

## 2. assemble 接入设计（R1/R3/R5）

### 2.1 统一接入模式

每个脚本按 `verify_bib.py:25-27` 既有样板引入（try/except ImportError 双路径），入口处：

```python
doc = tex_loader.assemble(file_path)
content, lines = doc.content, doc.lines
```

行号标签统一改为 `doc.lineref(n)`（替换 f-string 里的 `Line {n}` / `Lines {a}-{b}`）。装配告警
（编码/缺失 include）在输出头部打印 `doc.warning_lines(comment_prefix)`——多文件才会出现，
单文件无告警 → 输出不变。

### 2.2 check_references.py（R1 / A-EN-1）

- `main()`（:355-361）：`path.read_text` → `doc = assemble(path)`；
  `ReferenceChecker(doc.content, str(path), doc=doc)`（新增可选参 `doc: AssembledDocument | None`，
  缺省 None 时内部自建单文件语义，保持类可独测）。
- `LabelInfo/RefInfo`（:40-58）已有 `file` 字段但恒填入口路径。改为 find_labels/find_refs
  （:116-142）在构造时经 `doc.origin(lineno)` 回填 `file` 与新增 `src_line`；`line` 保留**装配行号**
  （排序、ordering/caption 的区间比较 :220-247 依赖全文单调行号，必须用装配坐标）。
- 消息文案中的 `at line {lbl.line}`（:216, :243-244）改为 `at {doc.lineref(lbl.line)}`。
- `_format_issues`（:321-333）：`(Line N)` 前缀改为 `({label})`，label 由 `_add_issue` 新增
  `location` 字段携带（= `doc.lineref(line)`）；单文件 label 即 `Line N`，输出逐字节不变。
- JSON 输出：issue dict 追加 `"file"`/`"source_line"`（加法变更）；`"line"` 语义保持。
- exit 语义不变（有 Critical → 1）。

### 2.3 deai_check.py（R3，对齐锁敏感，最小侵入方案）

只动**不锁成员**：
- `__init__`（:305-331，不锁）：`file_path.read_text` → `assemble`；新增 `self.doc`；
  `self.content/self.lines/self.section_ranges` 全部基于装配文本——锁定的
  `analyze_document`/`_find_pattern_in_section`/`generate_suggestions_json` 消费这些属性，
  **源码零改动**，锁不动。
- 行号呈现：`generate_report`/`check_section`/`main`（均为登记分歧成员，不锁）内的
  `Line {n}` 改 `self.doc.lineref(n)`。
- `--fix-suggestions` JSON：`generate_suggestions_json` 锁定不动；在 `main()`（:1031-1040）
  拿到 suggestions 后**后处理**：遍历条目按 `line` 补 `source_file`/`source_line`
  （`self.doc.origin`）再落盘。加法字段，消费方（tests、SKILL 文档）同步。
- 若实现中发现必须改锁定成员（预计不需要）：回退为"同改 en + typst 两副本逐字节镜像 + zh 保
  docstring"，并在 PR 里声明接管 `Checker.analyze_document` 等哈希——**默认不走此路**，避免与
  typst 任务互踩。

### 2.4 其余脚本（R3/R5 批量）

| 脚本 | 读取位点 | 行号输出位点 | 备注 |
|---|---|---|---|
| analyze_logic.py | :671 | 9 处 `Line/Lines {}` | 与 R2 同文件一次改完 |
| analyze_literature.py | :145 | 5 处 | 与 R2 同文件 |
| analyze_experiment.py | :360 | `_format_issue` :322-325 单点 | 局部 SECTION_ALIASES(:20-27) 本任务不动 |
| analyze_abstract.py | :211 | 报告为节级，无行级标签 | 只换读取；**en+typst Tier-1 锁**，改法与 typst 副本同步走 §2.6 模式 |
| check_figures.py | :34 | 3 处（run() :175 等） | 见下：路径根语义 |
| check_tables.py | :50 | 1 处 | |
| check_pseudocode.py | :56 | 1 处 | 注意 :56 是无 errors 参数的 read_text，assemble 顺带修掉编码炸点 |
| optimize_title.py | `_load_content` :259-260 | 无行级标签 | `_load_content` 内部改 assemble().content；批量模式(_resolve_batch_files)逐文件入口各自装配 |
| deai_batch.py | :30 | 3 处 | `process_section_file`(:191) 是显式单章处理，**保持单文件读**（语义即"处理这个文件"） |

check_figures 特别点：`self.root_dir = file_path.parent`（:32）不变——assemble 的 include
解析根与图片相对路径根同为入口目录，`\graphicspath`（:49-66）在装配文本上扫描后能看到
preamble 声明 + 分节文件里的 `\includegraphics`，语义正确；`_is_within_root`（:41-47）不受影响。

### 2.5 明确不改的脚本

`verify_bib.py`（已接 assemble :373-374）、`compile.py`（编译器自己展开 include）、
`extract_prose/generate_table/translate_academic/online_bib_verify`（语义上无需装配）。

### 2.6 裁决扩入的三脚本：analyze_grammar / analyze_sentences / improve_expression（R3）

父任务裁决把三脚本纳入 A-EN-3（登记表 ◆校正）。三者结构同源（曾是同一 MVP 模板）：
`read_text_robust` 单文件读入（grammar :69-72 / sentences :83-86 / expression :58-61，均带
`read_text_robust = None` 三级降级）→ `split_sections` → 逐区间逐行扫 `extract_visible_text`。
**别名解析已就位**：三者均已走 `resolve_section_keys`（grammar :79 / sentences :92 /
expression :67），无 R2 类工作，只做 assemble 接入。

**锁约束决定改法（与 §2.1 样板的差异点）**：三脚本 en/typst 副本被 Tier-1 哈希锁整文件互比
（§0 事实 3），改动必须 loader 无关——`typ_loader` 与 `tex_loader` 的 `assemble(entry) ->
AssembledDocument` API 对齐（typ_loader.py:115，同样有 `origin`/`lineref`/`warning_lines`），
故沿既有 import 降级模式扩一层即可，两副本保持逐字节一致：

```python
try:
    from tex_loader import assemble, read_text_robust
except ImportError:
    try:
        from typ_loader import assemble, read_text_robust
    except ImportError:
        assemble = None
        read_text_robust = None
```

`analyze()` 入口：`assemble` 可用时 `doc = assemble(file_path)`，取 `doc.content/doc.lines`，
行号标签 `Line {n}` → `doc.lineref(n)`；`assemble is None` 时保留现行 read_text_robust/
read_text 降级路径（此时 lineref 退化为 f-string `Line {n}`，单文件语义不变）。
装配告警走 `doc.warning_lines(cp)` 打在输出头部（同 §2.1）。

**副作用（必须声明，不是缺陷）**：typst 副本同步后，`.typ` 输入在 typst-paper 技能内解析到
`typ_loader.assemble` → 获得真正的 Typst `#include` 多文件装配。这是同方向修复的顺带收益，
须写入交付备注告知 typst-paper 子任务**勿重复实现**；en 技能内 `.typ` 输入仍走
`tex_loader.assemble` 的原样读入分支，行为不变（AC-R3 末条）。

逐脚本细节：

| 脚本 | 读取位点 | 报告粒度 | 接入要点 |
|---|---|---|---|
| analyze_grammar.py | :70 | 行级 `Line {line_no}`（:106），Original/Revised 建议对 | 逐行扫描 → origin 映射精确；`Line` → `lineref` 单点替换 |
| analyze_sentences.py | :84 | **段落级**：`_iter_paragraphs`（:49-78）跨行拼段，只报段首行（:117） | `lineref(段首行)` 指向段首所在源文件；装配可能使 include 边界两侧无空行的段落合并（assemble 不产生分隔行），fixture 在文件边界放空行保证确定性；段跨文件时定位仍取段首（与现状"段内行近似"同级，不额外建 span 映射） |
| improve_expression.py | :59 | 行级 `Line {line_no}`（:91），**输出的是改写文本**（Revised 供用户回写源文件） | origin 映射的意义与检查器不同：`sections/x.tex:N` 是用户**施改的落点**，标签错文件 = 建议不可用，故 lineref 精度是本脚本的核心验收点；逐行操作 → 映射精确，改写内容本身只依赖 visible text，不受装配影响 |

三脚本的多文件回归测试与 typst 副本同步放 implement.md Batch 4b；闸门 =
`PYT tests/contracts/test_writing_modules_alignment.py -q`（四文件 en/typst 哈希互比全绿）。

## 3. section 别名与 abstract 环境（R2/R4/R5）

### 3.1 resolve_section_keys 消费样板（现成，读自 parsers.py:138-153）

`resolve_section_keys(query, sections) -> (matched_keys, available_keys)`：吃 canonical 键与
`SECTION_KEY_ALIASES`（:117-135，含 `methods→method`、`related work→related`、`literature→related`），
base 键自动带上 `_2/_3` 重复节。消费样板即 `deai_check.py:1066-1075`。

### 3.2 analyze_logic.py（R2）

`analyze()`（:675-681）改为：

```python
if section:
    matched, available = resolve_section_keys(section, sections)
    if not matched:
        return [f"% ERROR ...: Section not found: {section} (available: {', '.join(available)})"]
    ranges = [sections[k] for k in matched]
```

`:736` `section.lower() == related_key` 改为 `related_key in matched`（matched 提升到函数级变量；
`--section "related work"` 时 related 节的 A1/A3 检查照跑）。import 行（:15-18）补
`resolve_section_keys`。

### 3.3 analyze_literature.py（R2）+ deai_batch.py（R5）

- `_find_section_bounds`（:64-72）改签名为返回 `list[tuple[int,int]]`：显式 `--section` 走
  `resolve_section_keys`；默认仍先试 `related`（含 `related_2`）。`analyze()`（:148-156）迭代
  多区间（沿用单区间逻辑逐区间跑，输出按区间分组）；miss 时错误行附 available 列表。
- `deai_batch.py:273-277`：`args.section.lower()` → `resolve_section_keys(args.section,
  processor.section_ranges)`；miss 打印 available（与 :291-294 的列表输出复用同一格式）；
  多 matched 逐节 `analyze_section`。import（:18-22）补 `resolve_section_keys`。

### 3.4 \begin{abstract} 环境注册（R4）— canonical parsers.py 改动

实现放 `LatexParser.split_sections`（parsers.py:270-273）：

```python
def split_sections(self, content):
    lines_total = len(content.split("\n"))
    headings = self.extract_headings(content)
    sections = _split_sections_from_headings(headings, self._classify_heading, lines_total)
    if "abstract" not in sections:
        # \begin{abstract} 环境形态（IEEE/ACM 常见）：标题规则(:191-201)只认标题式，
        # 环境式 abstract 在此补注册。跳过注释行，取 begin..end 行区间。
        <逐行扫描 \begin{abstract} / \end{abstract}，遵循 extract_headings 同款注释剥离 :309-313>
        sections["abstract"] = (begin_line, end_line)
    return sections
```

设计取舍：
- **不**把 abstract 伪装成 heading 塞进 `extract_headings`——那会污染 `chapter_ranges`
  （:50-74）与 heading 消费方语义。
- `_split_sections_from_headings`（:77-112，四副本锁）**不动**。
- 区间冲突：环境式 abstract 位于首个 `\section` 之前（真实论文形态），与既有区间天然不重叠；
  若同文档已有标题式 abstract 则跳过（`"abstract" not in sections` 守卫）。
- 注释防误判：复用 :309-313 的行内注释剥离 + 整行注释跳过模式，`% \begin{abstract}` 不注册。

**三副本同步**：`LatexParser.split_sections` 在 parsers-ALIGNMENTS :100 锁
`["en","audit","cover_letter"]`。同步顺序 en → `paper-audit/scripts/parsers.py` →
`cover-letter/scripts/parsers.py`，逐字节一致。zh（自有中文变体，未锁此成员）、typst
（无 LatexParser）不动。ALIGNMENTS **列表零编辑**（成员已在锁内）。

下游影响：cover-letter `extract_manuscript_facts.extract_section_anchors`（:218-221）开始返回
`abstract` 键——跑 `tests/skills/cover_letter` 确认无按键集合断言的用例翻红（有则属于该用例
需覆盖新真值，随本任务修正并声明）。

## 4. extract_title 平衡花括号（R10 / A-EN-10）— canonical parsers.py 改动

现状 `parsers.py:596`：`re.search(r"\\title(?:\[[^\]]*\])?\{(.+?)\}", ...)` 两缺陷：
非贪婪在首个 `}` 截断嵌套体；`\title` 与 `{` 间不容空白。且 `_strip_latex_markup`（:582-590）
对 `\thanks{X}` 是**保留 X**（:587 `\1` 替换）→ 资助文本泄入标题。

新实现（对齐 cover-letter fork `extract_manuscript_facts.py:224-240` 的三个行为）：

```python
latex_match = re.search(r"\\title(?:\[[^\]]*\])?\s*\{", content)
if latex_match:
    body = _extract_balanced_block(content, latex_match.end() - 1, "{", "}")
    if body:
        body = _strip_balanced_commands(body, ("thanks", "footnote"))
        return _strip_latex_markup(body)
    return ""
```

- `_extract_balanced_block` 已在 parsers.py:518-538（四副本锁内，零改动）。
- **新增模块级 helper `_strip_balanced_commands`**：从
  `cover-letter/scripts/extract_manuscript_facts.py:87-105` 原样移植（含嵌套体剥除的 while 循环）。
- 语义保持：`\title{...}` 命中即走 LaTeX 分支返回（body 空则返回 ""），不再落入 Typst 分支——
  与现行 `if latex_match: return` 的分支序（:596-598）一致。

**ALIGNMENTS 编辑（本任务唯一一处列表变更）**：`tests/contracts/test_parsers_alignment.py`
`ALIGNMENTS` 新增一行：

```python
("_strip_balanced_commands", ["en", "audit", "cover_letter"]),
```

`extract_title` 既有锁行（:88）不变，改后三副本同步即绿。typst 副本的 `extract_title`
（typst-paper/scripts/parsers.py:373，Typst-only 版本，无 LaTeX 分支）不在锁内、不动；zh 副本
（:411，自有 \ctitle 变体）不动。

**下游契约（A-CL-7）**：cover-letter 任务将在本任务落地后删除 `_extract_title_local` fork 并直用
canonical。因此本任务必须在 en 侧测试固化 fork 的全部用例（读自 :224-240 与
`_strip_balanced_commands` docstring :88-94）：
1. 嵌套花括号：`\title{Learning {Fast} and {Slow} Dynamics}` → 全文提取；
2. thanks 嵌套体：`\title{X\thanks{Funded by \emph{NSF}.}}` → 标题 = "X"，无 "Funded"；
3. footnote 同理；
4. 空白容忍：`\title {X}` / `\title[short]{X}` → "X"；
5. 无 `\title` → 走 Typst 分支（既有 `tests/shared/test_en_family_parsers_multifile.py:163-171`
   模板用例保持绿）。

消费方回归：paper-audit `parsers.py:632` 同步后 literature_search 链路（父 A-PA-8 曾误报处）
跑 `tests/skills/paper_audit` 全量确认。

## 5. Low 项（R6-R9）

- **R6** SKILL.md：删 :134（与 :132 重复行）。SKILL.md 任何改动后跑
  `tests/contracts/test_skill_contracts.py`（全局格式化 hook 若重排表格会触发 ROUTER_ROW_RE，
  见 memory 陷阱）。不动 `version`/`last_updated`（D6）。
- **R7** check_figures.py：删 :142-144（`width / 3.0` 死表达式 + "Assume typical figure width"
  两行陈旧注释）。`ruff` 本就该报 B018 类问题，删后 lint 干净。
- **R8** analyze_logic.py:220：`or "[" in visible` → `or re.search(r"\[\d+(?:\s*[,-–]\s*\d+)*\]",
  visible)`（数字引用样式 `[12]`/`[3, 7]`/`[1-4]`）。`\\cite{` 原始行判定保留。模块级预编译
  `NUMERIC_CITE_RE` 常量。
- **R9** check_format.py 模块 docstring（:2-9）与 `references/modules/format.md` 各加一句：
  分类基于英文 chktex 消息关键词，非英文 locale 下类别统一落 `other`，计数与 severity 不受影响
  （best-effort）。

## 6. 与 typst-paper 任务的对齐锁协调（父排序约束 #3）

本任务**声明接管**（即本任务改动、要求改后三/四副本一致的成员）：

| 锁成员（parsers-ALIGNMENTS 行号） | 副本 | 变更 |
|---|---|---|
| `LatexParser.split_sections`（:100） | en/audit/cover_letter | abstract 环境注册（§3.4） |
| `extract_title`（:88） | en/audit/cover_letter | 平衡花括号 + thanks 剥离（§4） |
| `_strip_balanced_commands`（**新增行**） | en/audit/cover_letter | 新共享 helper（§4） |

typst 任务接管：`TypstParser.extract_visible_text`（:86，en/typst/audit/cover_letter 四副本）与
TypstParser.clean_text（未锁）——与本任务改动的成员**零交集**，但物理文件相同
（en/audit/cover_letter 三份 parsers.py）。合并顺序：**本任务先合 dev**；typst 任务 rebase 后
再动 TypstParser 成员。deai-ALIGNMENTS 本任务零变更（§2.3 方案 A 下 deai_check 锁定成员源码不动）。

**writing-modules 锁（第三套，§0 事实 3）本任务同样声明接管**：

| Tier-1 组（test_writing_modules_alignment.py 行号） | 副本 | 变更 |
|---|---|---|
| `analyze_abstract.py`（:76） | en/typst | assemble 接入（§2.4 表 + §2.6 模式），整文件字节同步 |
| `analyze_grammar.py`（:77） | en/typst | 同上（§2.6） |
| `analyze_sentences.py`（:78） | en/typst | 同上（§2.6） |
| `improve_expression.py`（:79） | en/typst | 同上（§2.6） |

即本任务会**直接改写 typst-paper/scripts 下这四个文件**（字节镜像，非功能分叉）；typst 子任务
rebase 后见到这四个文件已带 assemble，勿重复实现、勿移出 Tier-1 组。交付备注同步声明
typst 侧 `.typ` 多文件装配的顺带启用（§2.6 副作用）。

## 7. 风险 / 取舍 / 回滚

| 风险 | 缓解 |
|---|---|
| assemble 后装配行号 ≠ 源文件行号，脚本内部比较逻辑（check_references ordering/caption、逻辑链区间）如混用源坐标会错乱 | 设计定死：**内部一律装配坐标，仅在渲染/JSON 边界经 origin/lineref 转源坐标**（§2.2 模式），实现与 review 各按此检查一遍 |
| deai_check 改动外溢到锁定成员导致 deai-ALIGNMENTS 红 | §2.3 只动登记分歧成员 + 每批次跑 `tests/contracts/test_deai_alignment.py`；万一必须动锁成员，走声明式镜像备选路径 |
| JSON 输出加字段破坏下游（paper-audit run_audit 汇聚 check_references/deai JSON） | 只加字段不改既有键；跑 `tests/skills/paper_audit` 全量 + grep paper-audit scripts 对相应 JSON 键的消费点 |
| split_sections 新增 abstract 键改变"默认全文分析"脚本的覆盖范围（如 analyze_logic 无 --section 时 ranges 多出 abstract 区间） | 属"假不可达修复"允许的默认行为变化（spec 例外条款），受影响存量用例同 commit 更新并在 commit message 双声明 |
| cover-letter/paper-audit 副本同步遗漏（改了 en 忘同步） | parsers-ALIGNMENTS 动态互比会直接红——每批次以 `pytest tests/contracts/test_parsers_alignment.py -q` 为闸门 |
| typst 四文件字节镜像遗漏（§2.6/§6 writing-modules 锁） | `pytest tests/contracts/test_writing_modules_alignment.py -q` 为 Batch 4a/4b 闸门，哈希互比直接红 |
| 与 typst 任务并行互踩 parsers.py | 父约束"先合 en"；本 design §6 已声明成员级归属，冲突面为零 |

**回滚形状**：六个独立批次（见 implement.md），每批以自身验证闸门收口并登记为**拟提交分组**
（文件集 + 拟用 commit message）；实际 `git commit` 统一延后到工作流 Phase 3.4（质量检查与
spec 更新完成后，分组一次性呈报用户确认）。因此批内回滚不走 commit revert，而是对该批登记的
文件集做 `git checkout -- <files>`（或先 `git stash push -- <files>` 留证），批间无隐藏耦合
（canonical parsers 批与 assemble 批唯一交点是 deai_check `--section abstract` 用例，
放在 parsers 批之后验证）。
