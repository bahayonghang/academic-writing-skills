# 技术设计 — typst可见文本解析修复

## 0. 函数所有权声明（与 en 子任务的边界）

**本任务独占以下成员**（其余任何 parsers.py 成员不碰）：

| 成员 | 现有锁（test_parsers_alignment.py） | 本任务动作 |
|------|-------------------------------------|-----------|
| `TypstParser.extract_visible_text` | `["en","typst","audit","cover_letter"]`（:86） | 改 5 副本（zh 同码但不入锁），锁行不变 |
| `TypstParser.clean_text` | **当前未锁**（仅 `LatexParser.clean_text` 在 :107 锁 en/audit/cover_letter） | 改 4 副本（zh 无此方法），**新增锁行** |
| `TypstParser.PRESERVE_PATTERNS` | `["en","zh","typst","audit","cover_letter"]`（:83，全五副本） | 改 5 副本（列表**删除** `r"//.*"` 元素），锁行不变 |
| `_strip_typst_line_comment`（新增模块级函数） | 无 | 5 副本新增，**新增锁行（全五副本）** |
| 模块级 `extract_abstract`（仅 Typst heading 分支的 lookahead） | `["en","audit","cover_letter"]`（:89；typst 副本是 Typst-only 变体，**有意不在锁内**） | 改锁内 3 副本 + typst 自有副本，锁行不变 |

**en 子任务（07-15-audit-fix-latex-paper-en）拥有**：`extract_title`（A-EN-10，锁 :88 en/audit/cover_letter）、`LatexParser.split_sections` / `SECTION_TITLE_RULES` 等 LatexParser 成员（A-EN-4，锁 :100-:107）。已逐行核对 ALIGNMENTS（:75-113）：**两任务的成员集合零交集**。文件级仍有重叠（en/audit/cover_letter 三份 parsers.py 双方都编辑）——父任务顺序约束：**并行时 en 先合，本任务在其后 rebase 并重跑对齐测试**。ALIGNMENTS 无存储哈希值（hash 相等性即时计算，:127-133），因此不存在"更新哈希"动作，只有"保持副本字节一致 + 增删锁行"。

## 1. A-TY-1：URL 感知的行注释剥离

### 1.1 缺陷位点（全部已核实）

| 位点 | typst | en | audit | cover-letter | zh |
|------|-------|----|-------|--------------|----|
| `split("//")[0]`（extract_visible_text 预剥离） | :221 | :427 | :437 | :436 | :345 |
| `re.sub(r"//.*", "", content)`（clean_text） | :275 | :481 | :491 | :490 | —（zh 无 clean_text，锁 :158-165 要求 zh 保持无） |
| PRESERVE_PATTERNS 条目 `r"//.*"` | :194 | :400 | :410 | :409 | :321 |
| extract_abstract lookahead `(?=^=\s+\|\Z)` | :417 | :656 | :695 | :665 | —（zh extract_abstract 是 LaTeX-only 变体） |

（路径：`academic-writing-skills/{typst-paper,latex-paper-en,paper-audit,cover-letter,latex-thesis-zh}/scripts/parsers.py`）

### 1.2 算法：`_strip_typst_line_comment(line) -> str`

单遍字符扫描，三个状态/规则（近似 Typst 词法器）：

```python
def _strip_typst_line_comment(line: str) -> str:
    """Strip a Typst line comment, keeping ``//`` that lives inside URLs,
    double-quoted strings, or raw-text backticks (approximates the Typst
    lexer; block comments are handled separately by the callers)."""
    in_string = False  # "..." code-mode strings, e.g. #link("...") args
    in_raw = False     # `...` raw text
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if in_string:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_string = False
        elif in_raw:
            if ch == "`":
                in_raw = False
        elif ch == '"':
            in_string = True
        elif ch == "`":
            in_raw = True
        elif ch == ":" and line.startswith("://", i):
            # URL scheme: consume the token up to the next whitespace, so
            # ``https://example.com//path`` never opens a comment.
            i += 3
            while i < n and not line[i].isspace():
                i += 1
            continue
        elif ch == "/" and line.startswith("//", i):
            return line[:i]
        i += 1
    return line
```

逐用例走查（与 prd R4 一一对应）：

| 输入 | 结果 | 依据 |
|------|------|------|
| `See https://example.com/x for details.` | 原样保留 | `://` 触发 URL token 跳读 |
| `See http://example.com for details.` | 原样保留 | 同上 |
| `https://example.com//path more prose` | 原样保留 | token 跳读吞掉路径 `//` |
| `#link("https://x") hosts the code.` | 原样保留（#link 由 PRESERVE 挖空） | in_string 保护 |
| `#link("//cdn.example.com/l.js") text` | 原样保留 | in_string 保护协议相对形式 |
| `// pure comment` | `""` | 正常注释 |
| `Prose here. // trailing` | `Prose here. ` | 正常注释 |
| `//cdn.example.com`（裸文本） | `""` | **裁决：按注释**（见 §1.4） |
| `a: // comment` | `a: ` | `line[i:i+3] == ": /"` 不构成 `://`，lookahead 不误保护 |
| `` `code // x` prose `` | 原样保留 | in_raw 保护 |
| `/* hidden */ prose // note` | `/* hidden */ prose ` | 扫描器只剥 `// note`；`/* */` 留给 PRESERVE 挖空 |
| 行尾未闭合字符串后出现 `//` | 不剥（保守） | in_string 挂起；按行解析的固有限制，记入 docstring |

**单一所有权（本设计的核心不变量）**：扫描器的输出就是行注释语义的最终裁决——PRESERVE 阶段（及任何后续阶段）不得再有 `//` 相关模式复查。扫描器保留下来的 `//`（URL、串内、raw）必须原样进入可见文本管线。

### 1.3 三处调用点改法

1. **extract_visible_text 预剥离**（替换 `if "//" in temp_line: temp_line = temp_line.split("//")[0]`）：
   ```python
   temp_line = _strip_typst_line_comment(temp_line)
   ```
2. **clean_text**：块注释先于行注释（次序必须调换）：
   ```python
   # Remove block comments FIRST: a per-line "//" strip would otherwise eat
   # the "*/" terminator on lines like "still hidden // note */" and leave
   # the block unclosed.
   content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
   content = "\n".join(_strip_typst_line_comment(ln) for ln in content.split("\n"))
   ```
   其余步骤（数学、heading、`#func()`、`@key`、`<label>`、空白清理）逐字节不动。
3. **PRESERVE_PATTERNS**：`r"//.*"` 条目**整条删除**（五副本同步；不是改成 `(?<!:)//.*`）。推导链：
   - **现状排序与死代码判定**：extract_visible_text 内预剥离先跑（typst :220-221），PRESERVE 循环后跑（:224-231）。`split("//")[0]` 把首个 `//` 起的一切都删掉，因此进入 PRESERVE 阶段的行**不可能再含 `//`**——`r"//.*"` 条目在现状下是不可达的死代码。
   - **消费方核查**：全仓 grep `PRESERVE_PATTERNS`，唯一消费点是各副本 extract_visible_text 方法自身（typst :224、en :430、audit :440、cover-letter :439、zh :348），无任何外部消费方。`typst-paper/scripts/typ_loader.py:25` 与 `paper-audit/scripts/typ_loader.py:25` 的 `LINE_COMMENT_RE = re.compile(r"//.*")` 是另一文件的独立机制，不消费 PRESERVE_PATTERNS，不在本任务范围。
   - **为什么删除而非收紧**：扫描器落地后，行内残余的 `//` 恰恰全是扫描器**刻意保留**的三类——URL、双引号串内、raw 文本。任何后置 `//` 正则都会复查并推翻扫描器的裁决：`(?<!:)//.*` 会重新截断 `#link("//cdn…")`（`//` 前一字符是 `"`）、raw 文本（前一字符任意）、`https://host//path`（前一字符是字母），把回归契约要保的三个用例全部打回。行注释语义必须**单一所有权**归扫描器；条目删除后，真行注释永远到不了 PRESERVE 阶段（已被扫描器剥掉），条目也不再有任何合法命中。
   - **契约影响**：`TypstParser.PRESERVE_PATTERNS` 受 :83 全五副本锁（含 zh）。删除是**被锁列表的数据编辑**：五副本各删同一元素、列表其余元素逐项一致，锁的 repr 哈希即时计算自动通过；`tests/contracts/test_parsers_alignment.py` 的该锁行本身零改动。

### 1.4 裁决与取舍（genuinely-ambiguous cases）

- **裸协议相对 URL `//cdn.example.com` → 注释**。Typst 编译器只自动链接 `http(s)://`，裸 `//…` 在 markup 模式下就是注释——按注释处理与真实渲染一致；学术论文散文中裸协议相对 URL 几乎不存在。测试锁定该决策防将来误当 bug 反转。
- **URL/raw 全量进入可见文本（有意的行为变化，取代旧「PRESERVE 残余边缘」取舍）**：条目删除后，`https://host//path` 整个 URL、`#link("…")` 之外的裸 URL、raw 反引号内容（含其中的 `//`）都完整计入可见文本与词数——测试矩阵正向断言（不再是 known-tradeoff）。`#link(...)` 调用本身仍由 `#link\([^)]+\)` 条目整体挖空，串内 `//` 不影响该条目匹配。
- **同行「块注释包住 `//`」的固有限制**：extract_visible_text 的扫描器不识别 `/* */`（块注释由 PRESERVE 的 `/\*.*?\*/` 条目在其后挖空），因此 `text /* b // c */ more` 会在块内 `//` 处被截断为 `text /* b `。这与现状 `split("//")[0]` 的行为**逐字节相同**（零回归），记为已知限制不修；clean_text 侧因块注释先剥无此问题。
- **URL 内 `/*`**：不保护（`/\*.*?\*/` 仍可能命中），真实 URL 中极罕见，记为已知限制，不写代码。

## 2. A-TY-2：extract_abstract lookahead

单字符修复：`(?=^=\s+|\Z)` → `(?=^=+\s+|\Z)`（4 处：typst :417、en :656、audit :695、cover-letter :665）。abstract 标题匹配 `^=\s+(?:摘要|[Aa]bstract)` 不变（仍限 level-1）。en/audit/cover_letter 三副本受 :89 锁约束必须逐字节一致（注意 en 系变量名是 `typst_heading_abs`、typst 副本是 `heading_abs`——各自保持原名，锁只覆盖模块级 `extract_abstract` 函数源码，typst 副本不在锁内）。

## 3. ALIGNMENTS 变更（tests/contracts/test_parsers_alignment.py）

```python
# 新增两行（位置：分别紧邻 _strip_typst_markup 行与 LatexParser.clean_text 行）
("_strip_typst_line_comment", ["en", "zh", "typst", "audit", "cover_letter"]),
("TypstParser.clean_text", ["en", "typst", "audit", "cover_letter"]),
```

- 既有行零改动（锁是即时 hash 相等性比较，无存储哈希）。`TypstParser.PRESERVE_PATTERNS` 锁行（:83）保持原样——`r"//.*"` 的删除发生在五份被锁的列表数据里，五副本同步删除即满足锁；contract 测试文件净 diff 恒为 +2 行。
- zh 的 `TypstParser.extract_visible_text` 维持**不入锁**（zh 副本无 `# Same logic as LatexParser…` 注释行等外观差异，属 test 文件 docstring :9-21 记录的有意分歧）；仅修其 `split("//")` 行为并加独立回归测试。
- `test_clean_text_is_canonical_only`（:158-165）不受影响：zh 仍无 clean_text。

## 4. 触碰文件清单

| 文件 | 改动 |
|------|------|
| `academic-writing-skills/latex-paper-en/scripts/parsers.py` | canonical：新增帮助函数 + 三调用点 + PRESERVE 条目 + extract_abstract lookahead |
| `academic-writing-skills/paper-audit/scripts/parsers.py` | 同 en 逐字节镜像 |
| `academic-writing-skills/cover-letter/scripts/parsers.py` | 同 en 逐字节镜像 |
| `academic-writing-skills/typst-paper/scripts/parsers.py` | 帮助函数 + 三调用点 + PRESERVE 条目 + 自有 extract_abstract lookahead |
| `academic-writing-skills/latex-thesis-zh/scripts/parsers.py` | 帮助函数 + extract_visible_text 预剥离 + PRESERVE 条目（无 clean_text/extract_abstract 改动） |
| `tests/contracts/test_parsers_alignment.py` | ALIGNMENTS +2 行 |
| `tests/shared/test_parsers.py` | EN canonical 回归（URL 可见性、clean_text 词数、extract_abstract Keywords） |
| `tests/skills/typst_paper/test_typst_paper_scripts.py` | typst 副本回归（importlib 按路径加载，沿用既有 loader） |
| `tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py` | zh TypstParser URL 回归一条 |

## 5. 风险与回滚

- **deai 行为漂移**：URL 行不再截断且 URL 本体计入可见文本 → deai/时态/密度检查可见文本变多，可能新增/改变 trace。`tests/skills/typst_paper/test_deai_typst.py` 现有 fixture 无 URL（已核），预计零影响；`just ci` 全量兜底。属规范允许的"误报/假绿修复"默认行为变化，commit message 声明。
- **deai 对齐锁**：`test_deai_alignment.py` 只 hash deai_check.py 成员（parsers 仅作 `_SIDECAR_MODULES` 加载依赖，:69），本任务不触发其锁；仍纳入验证命令确认。
- **块注释次序**：clean_text 次序调换有既有用例 `tests/shared/test_parsers.py:75-77` + 新增多行块注释含 `//` 用例双保险。
- **与 en 任务合并冲突**：同文件不同函数，git 通常可自动合并；若 rebase 冲突，以 en 已合入版本为基底重放本任务 hunk，随后必跑 `tests/contracts/test_parsers_alignment.py`。
- **回滚**：实施期间不产生中间 commit（提交统一在 workflow Phase 3.4，见 implement.md）。批次内失败 → `git checkout -- <该批次文件集>`（或 `git stash`）按 implement.md 记录的拟提交分组文件集定点回退；Phase 3.4 提交后仍按分组两 commit 落盘（A-TY-1、A-TY-2），任一出问题单独 `git revert`；无数据/配置迁移。整体回滚点 = 实现开始前的 dev HEAD（implement.md 记录）。
