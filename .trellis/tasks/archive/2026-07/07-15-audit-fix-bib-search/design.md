# bib查询解析健壮性修复 — 技术设计

所有 file:line 均已在 2026-07-15 dev 分支实读核实；所有「实测」均已在本机复现。

涉及文件：

- `academic-writing-skills/bib-search-citation/scripts/search_bib.py`
- `academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py`
- `academic-writing-skills/bib-search-citation/references/query-syntax.md`
- `academic-writing-skills/bib-search-citation/references/limitations-and-errors.md`
- `academic-writing-skills/bib-search-citation/tests/test_bib_search.py`

---

## D-1（A-BIB-1）tokenizer 容错：shlex 失败回退自定义切分

### 现状

`spec_from_compact_query`（search_bib.py:498-536）第一行 `tokens = shlex.split(query_text or "")`（:499）。posix 模式下单引号是引界符，`children's` 抛 `ValueError("No closing quotation")`，`main()`（:1414-1420）捕获后 exit 2。

### 备选与取舍

| 方案                                                  | 结论                                                                         |
| ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| A. try shlex → ValueError 时回退自定义正则切分 + 警告 | **选此**。正常输入零行为变化；崩溃输入降级可用并显式告知                     |
| B. 预转义孤立撇号再喂 shlex                           | 弃。判定「哪个引号是孤立的」本身就是解析问题，且会改变合法单引号值的语义     |
| C. shlex 关闭单引号（quotes='"'）                     | 弃。`author:'van Dyke'` 等既有合法单引号分组会静默破坏，属于正常路径行为变化 |

### 实现

```python
_FALLBACK_TOKEN_RE = re.compile(r'(?:[^\s"]+|"[^"]*")+')

def _fallback_tokenize(text: str) -> list[str]:
    tokens = _FALLBACK_TOKEN_RE.findall(text)
    return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] == '"' else t for t in tokens]
```

- `spec_from_compact_query` 改为：`try: tokens = shlex.split(...)` / `except ValueError: tokens = _fallback_tokenize(...)` 并将警告写入 `spec["_query_warnings"]`（list）。
- 回退语义（写入警告 message 与文档）：双引号短语仍分组（整 token 包裹时剥除；`claim:"low latency"` 形式由 `strip_quotes_if_needed`（:599-605）在值侧剥除——已验证 `_fallback_tokenize('children\'s "deep learning" claim:"low latency"')` → `["children's", 'deep learning', 'claim:"low latency"']`）；单引号按字面字符处理，不再分组。
- 警告形状（与既有 parse_warnings 条目一致，:810-819 风格）：

```json
{
  "type": "query_tokenizer_fallback",
  "message": "query contains an unbalanced quote; fell back to whitespace tokenization (double-quoted phrases still group, single quotes are treated literally)"
}
```

### 警告贯通链路

`spec_from_compact_query` 有两个调用点：`load_spec`:302（--query 模式）与 :311（spec.query 内嵌 compact 语法）。`merge_specs`（:347-358）对 base 做 json 深拷贝，`_query_warnings` 作为普通顶层键在两条路径都能存活；`validate_spec`（:271-292）只检查 `filters` 与 `limit`，不受影响。`main()`（:1429-1432）在构造 `extra_meta` 前 `spec.pop("_query_warnings", [])` 并前置拼入 `parse_warnings`，由 `run_search`:1366 现有逻辑带入 `meta.parse_warnings`。

### 错误面契约

- 回退成功：exit 0，正常 JSON 输出 + `meta.parse_warnings` 含 `query_tokenizer_fallback`。
- 不再存在「引号不配对 → exit 2」路径（回退切分不可能失败）。
- 其余 SpecError 路径不变：stderr JSON `{"error": str}` + exit 2。

---

## D-2（A-BIB-2）preview 渲染 warnings 区块

### 现状

`render_preview`（preview_bib_search.py:169-190）只渲染 Query/Filters/Results；`meta.parse_warnings`（search_bib.py:1377）、per-result `warnings`（:1268-1275，list[str]）、`meta.encoding_fallback`（:1380-1381）全部丢失。

### 设计

在 `render_filter_summary` 行之后追加（仅在对应数据存在时输出，保证无 warnings 时输出逐字节不变）：

```
Encoding: latin-1 fallback (file was not valid UTF-8)
Warnings (7):
  - [unbalanced_entry] entry starting at line 5 is missing a closing '}'; skipped to the next entry
  - [duplicate_key] citation key 'Smith2020' is defined 2 times; ...
  ... and 2 more (see meta.parse_warnings in the JSON output)
```

- 新常量：`WARNINGS_LIMIT = 5`、`WARNING_TEXT_LIMIT = 200`（复用现有 `truncate_text`:37-41 截断单条 message）。
- 渲染规则：条目为 dict 时取 `[type] message`（type 缺省 `warning`，message 缺省整条 `render_simple_value`）；总数写在标题 `Warnings (N):`；仅显示前 5 条，溢出行指回 JSON。
- per-result warnings：`render_entry`（:125-166）末尾（citations 行之后）追加 `  Warning: <truncate 200>`，逐条渲染，不截断条数（现实中每条目最多 1-2 条）。
- `meta.encoding_fallback` 为字符串（如 `"latin-1"`）时输出单行提示；与 SKILL.md:127-128 安全边界（畸形 .bib 须报告）对齐。

### 兼容性

现有 `test_preview_from_stdin_renders_summary_and_hides_raw_bib`、`test_preview_input_file_mode_and_truncation` 均基于无 warnings 的 payload，逐行断言不受影响；`preview_input.json` fixture 无 warnings 字段，零改动。

### 实施中补充：Windows UTF-8 管道输入

per-result duplicate warning 进入 preview 后实测暴露既有输入边界：search 通过
`stdout.buffer` 写 UTF-8，而 preview 的 `sys.stdin.read()` 在 Windows locale/cp936 下会把
warning 中的长横线解成代理字符并在后续 UTF-8 写出时崩溃。`load_payload` 因此改为优先读取
`sys.stdin.buffer` 并显式 UTF-8 解码；无 `buffer` 的 `StringIO` 测试流保持文本回退。真实
duplicate-key 搜索输出管道测试同时锁住 warning 呈现与此编码边界。

---

## D-3（A-BIB-3 / D4）CODE_HINT_TERMS 逐词匹配语义

### 现状

`has_code`（search_bib.py:975-977）`any(term in combined)` 裸子串匹配 `CODE_HINT_TERMS`（:130-138）。实测误判：`reported results`（repo⊂reported）、`encoder-decoder`（code⊂encoder... 实际是 code⊂decoder 前缀链）、`barcode`、`we encode the signal` 均 True。

### 逐词语义表（D4 交付物）

匹配底串：`combined` = CODE_HINT_FIELDS（url/howpublished/note/abstract/annotation/keywords，:129）各值经 `normalize_text` 拼接后 `.lower()`（不变）。所有词统一为**词边界匹配**（`\b词\b`；短语按带边界的词序列匹配，`normalize_text` 已折叠空白）：

| term             | 模式                 | 语义说明 / 验证点                                                                                                                                                    |
| ---------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `github`         | `\bgithub\b`         | `github.com/x` 中 `.` 是非词字符 → 匹配（实测 True）                                                                                                                 |
| `gitlab`         | `\bgitlab\b`         | 同上                                                                                                                                                                 |
| `code`           | `\bcode\b`           | 杀掉 encoder/decoder/barcode/encode（四负例实测 False）；`dress code` 类泛词残留（文档化）                                                                           |
| `repository`     | `\brepository\b`     | `data repository` 仍视为可用性信号；语义否定（`without a linked repository`）不解决（文档化）                                                                        |
| `repo`           | `\brepo\b`           | `reported` 无边界 → False（实测）                                                                                                                                    |
| `source code`    | `\bsource code\b`    | 短语级；被 `code` 蕴含，保留以自文档化                                                                                                                               |
| `code available` | `\bcode available\b` | 同上                                                                                                                                                                 |
| `codeavailable`  | `\bcodeavailable\b`  | **新增**：Zotero tag `CodeAvailable`（camelCase 连写，lower 后无词边界）在词表边界化后会丢失；本仓 fixture `library.bib:10,33` 与 `query-syntax.md` 示例均依赖该 tag |

### 实现

`CODE_HINT_TERMS` 仍是唯一事实源（新增 `codeavailable`），模块加载时编译单一正则：

```python
CODE_HINT_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in CODE_HINT_TERMS) + r")\b")

def has_code(fields):
    combined = " ".join(...).lower()  # 不变
    return bool(CODE_HINT_RE.search(combined))
```

### 已验证的行为稳定性

用提案正则对 library.bib 三条目实测：Doe2024Mamba True→True（keywords 含独立词 `code` + url github）、Roe2023Transformer True→True（abstract 含词 `repository`——语义否定残留，文档化）、Lee2025Photovoltaic True→True（`codeavailable` 新词项）。`has:code` 端到端结果集不变，现有 `test_search_bib_json_contract_and_citations` 无需改动。

### 文档

`limitations-and-errors.md` 增补：`has:code` 是提示字段上的词边界启发式，不做语义否定分析（`without a linked repository` 仍为 True）、不排除泛词（`dress code`）；词表与语义以本表为准。

---

## D-4（A-BIB-4）YEAR_RE 消歧后缀

### 现状

`YEAR_RE = re.compile(r"\b(1[5-9]\d{2}|20\d{2})\b")`（search_bib.py:31），仓内唯一使用点是 `entry_year`:953（grep 核实）。`year={2024a}` 中 `4→a` 无词边界 → None（实测），随后被任何年份过滤静默排除（match_filters:1082-1088 year None 即淘汰）。

### 设计

```python
YEAR_RE = re.compile(r"\b(1[5-9]\d{2}|20\d{2})[a-z]?\b")
```

- `entry_year`（:951-956）改取 `match.group(1)`（当前 `group(0)`），返回 int `2024`。
- 适用字段不变：先 `year` 后 `date`（:952 循环顺序）。
- 后缀定义：单个小写 `[a-z]`（BibTeX 年份消歧惯例；不含大写，`2024A` 型号名不误配；正则无 IGNORECASE，现状即区分大小写）。
- 边界核查（实测/推演）：`2024-06-15` → `-` 本就是边界，仍取 2024；`20245` → `[a-z]?` 不消费数字、`\b` 失败，仍 None；`2024ab` → `b` 处无边界，None（两字母消歧极罕见，不支持，文档不承诺）。

---

## D-5（A-BIB-5）非整数值 → SpecError

### 现状

`parse_query_token`：`limit:abc` → :565 `int(value)` 裸 ValueError；`recent:x` → :576 同；`parse_year_filter`（:621-644）:627/:629/:635 三处 `int()` 对 `year:20x4` 同。`main()`:1418 捕获 ValueError 后虽仍 exit 2 + JSON，但 message 是 `invalid literal for int() with base 10: 'abc'`（实测），无行动指引。

### 设计

新增私有 helper，措辞对齐 `validate_spec`:289 已验证路径（`f"limit must be an integer, got {limit!r}"`）：

```python
def _parse_int(value: str, what: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise SpecError(f"{what} must be an integer, got {value!r}") from exc
```

替换点与 `what` 标签：

| 位置           | 调用                                          | 报错前缀                                           |
| -------------- | --------------------------------------------- | -------------------------------------------------- |
| :565           | `_parse_int(value, "limit")`                  | `limit must be an integer, got 'abc'`              |
| :576           | `_parse_int(value, "recent window")`          | `recent window must be an integer, got 'x'`        |
| :627/:629/:635 | `_parse_int(item/value, "year filter value")` | `year filter value must be an integer, got '20x4'` |

正整数校验仍由 `validate_spec`:290-292 兜底（`limit:-3` → "limit must be a positive integer"，现有测试 `test_nonpositive_limit_is_rejected` 已锁）。错误面契约不变：exit 2 + stderr JSON。

---

## D-6（A-BIB-6）冒号自由文本：doc-first + 警告扩展

### 实测校正（与父任务登记表的偏差）

`FIELD_OP_RE`（:27-29）的 field 组是 `[A-Za-z_][A-Za-z0-9_-]*`：

- `10:30` → 不匹配（数字开头），保留为自由文本（实测 `parse_query_token("10:30")` 返回 None）。**登记表此示例不成立。**
- `genotype:phenotype` → 匹配，静默转为 `field_contains {"genotype": ["phenotype"]}` 并从 `meta.query` 消失（实测）。

### 设计（不改过滤语义）

1. **文档**：`query-syntax.md` 的 Edge cases 下新增小节「Colons in free text」：
   - 规则：以字母/下划线开头的 `name:value` token 一律解析为字段过滤；数字开头（`10:30`）保留为自由文本。
   - 后果：值不参与相关性评分。
   - 规避：把冒号改为空格（评分 tokenizer `TOKEN_RE`:24 本就按非字母数字切分，`genotype phenotype` 与原文评分等价）；不推荐「JSON spec 里放 query」作为通用规避——`maybe_contains_query_syntax`（:328-344）命中 compact 标记时 spec.query 仍会被重解析。
   - 提示 `meta.parse_warnings` 的 `unknown_field_filter` 会兜底提醒。
   - 同步说明既有行为：`note:`、`title:` 等真实字段名（`KNOWN_ENTRY_FIELDS`:172-195 或库内存在的字段）永远按过滤处理且**不触发警告**。
2. **警告扩展**：`_field_filter_warnings`（:1323-1344）message 从「check for a typo」扩为双向指引（`type` 保持 `unknown_field_filter` 不变，`test_typo_field_filter_emits_warning` 只断言 type，安全）：

```python
message = (
    f"filter field '{field_name}' is not present in any entry; if "
    f"'{field_name}:{example_value}' was meant as free text, replace the colon "
    "with a space; otherwise check the field name for a typo"
)
```

其中 `example_value` 取该 field 首个 needle（函数内 `filters[group][field_name][0]`，需容错空列表回退 `"..."`）。

---

## 错误面契约总表（修复后）

| 输入                                             | 出口           | 形状                                                            |
| ------------------------------------------------ | -------------- | --------------------------------------------------------------- |
| 引号不配对的 --query                             | exit 0         | 正常 JSON；`meta.parse_warnings` 含 `query_tokenizer_fallback`  |
| `limit:abc` / `recent:x` / `year:20x4`           | exit 2         | stderr JSON `{"error": "<what> must be an integer, got '...'"}` |
| `limit:0` / `--limit -1`                         | exit 2（不变） | `{"error": "limit must be a positive integer"}`                 |
| 未知 filter 键（spec-json）                      | exit 2（不变） | `{"error": "unknown filter key(s): ..."}`                       |
| 未知字段过滤（`tilte:x` / `genotype:phenotype`） | exit 0（不变） | `meta.parse_warnings` 含 `unknown_field_filter`（message 扩展） |
| 畸形 .bib                                        | exit 0（不变） | `meta.parse_warnings` + **preview 现在可见**                    |

## 风险与回滚

| 风险                                                | 缓解                                                                               | 回滚                                                    |
| --------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------- |
| D-3 词边界降低召回（未知库中 camelCase/连写提示词） | 新增 `codeavailable`；fixture 三条目实测行为不变；残留局限文档化                   | 单文件单函数改动，`git revert` 该 commit 即回到子串语义 |
| D-1 回退切分与 shlex 语义差异被误当正常路径         | 回退仅在 shlex 抛错时触发 + 显式警告；正常路径零改动并有短语分组回归测试锁住       | 移除 try/except 即还原                                  |
| D-2 改变 preview 逐行输出破坏既有断言               | warnings 区块仅在数据存在时渲染；先跑全量 preview 测试再提交                       | 渲染块独立追加，删除即还原                              |
| D-6 警告 message 措辞被下游锁字符串                 | 全仓 grep 核实仅 `test_typo_field_filter_emits_warning` 断言 `type`，无 message 锁 | 还原 message 字符串                                     |
| `_query_warnings` 内部键泄漏进输出                  | `main()` 显式 pop；测试断言 meta 无该键                                            | —                                                       |
| `just ci` 因 A-REL-1 未落地而 check-versions 红     | implement.md 前置检查；红因与本任务隔离时单跑 lint/typecheck/test                  | —                                                       |
