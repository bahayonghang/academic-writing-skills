# typst可见文本解析修复（A-TY-1 / A-TY-2）

> 父任务：`.trellis/tasks/07-15-skills-deep-audit-opt/prd.md`（发现登记表 A-TY 节）。
> 本任务只修 TypstParser 的注释剥离与 extract_abstract 渗漏两项，并同步全部受对齐锁约束的副本。

## Goal

1. **A-TY-1（High）**：`TypstParser.extract_visible_text` 用 `split("//")[0]`（typst 副本 `parsers.py:221`）剥行注释，命中 URL 中的 `//`（`http://`、`https://`）→ 含 URL 的行从 scheme 处被截断，行内后续散文对 deai/时态/信息密度等所有行级检查完全不可见；`clean_text` 的 `re.sub(r"//.*", "", content)`（`parsers.py:275`）同缺陷，殃及词数统计。
2. **A-TY-2（Low）**：模块级 `extract_abstract` 的 heading 式分支 lookahead 只认 level-1（`(?=^=\s+|\Z)`，typst 副本 `parsers.py:417`）→ `== Keywords` 等子标题内容渗入 abstract。

两项缺陷均存在于多个技能副本（见 design.md 副本清单），修复必须按 `tests/contracts/test_parsers_alignment.py` 的 ALIGNMENTS 锁同步。

## Requirements

### R1 — URL 感知的行注释剥离（A-TY-1）

- 新增模块级帮助函数 `_strip_typst_line_comment(line)`：单遍扫描，`//` 仅在以下条件全部满足时视为注释起点——
  - 不在双引号字符串内（覆盖 `#link("https://…")` / `#link("//cdn…")` 等 code-mode 实参）；
  - 不在反引号 raw 文本内（`` `code // not comment` ``）；
  - 不在 URL token 内：扫描到 `://` 时跳过该 token 直到下一个空白（覆盖 `https://example.com//path` 等路径双斜杠）。
- `TypstParser.extract_visible_text` 的预剥离改用该帮助函数（替换 `split("//")[0]`）。
- `TypstParser.clean_text` 改为：先剥块注释 `/* */`（DOTALL），再逐行调用帮助函数剥行注释（顺序调换的原因见 design.md「块注释次序」）。
- **行注释单一所有权（single owner）**：`_strip_typst_line_comment` 是行注释的**唯一**处理机制。`TypstParser.PRESERVE_PATTERNS` 中的 `r"//.*"` 条目**整条删除**（五副本同步；不是改成 `(?<!:)//.*`）。理由：该条目在现状下是死代码（预剥离 `split("//")[0]` 先跑，PRESERVE 阶段已无 `//` 可匹配）；扫描器落地后，行内残余的 `//` 恰恰全是扫描器刻意保留的（URL、串内、raw），任何后置 `//` 正则——含 `(?<!:)` 变体——都会把 `#link("//cdn…")`（前一字符是 `"`）、raw 文本、`https://host//path`（前一字符是字母）重新截断，等于把 bug 换个位置复发。
- **裁定的行为决策**（详见 design.md §裁决）：
  - 行首/空白后的协议相对 URL（`//cdn.example.com`）**按注释处理**——与 Typst 编译器语义一致（Typst 只自动识别 `http(s)://` 链接，裸 `//…` 就是注释）。
  - 引号字符串内的 `//`（含协议相对形式）一律不当注释。
  - URL 路径中的 `/*` 不做保护（真实 URL 中极罕见，非目标）。

### R2 — extract_abstract 停止条件纳入任意级 heading（A-TY-2）

- heading 式 abstract 分支的 lookahead 由 `(?=^=\s+|\Z)` 改为 `(?=^=+\s+|\Z)`，使 `==`/`===` 等任意级 heading 均终止捕获；abstract 标题本身仍只匹配 level-1（`^=\s+(?:摘要|[Aa]bstract)`，不变）。

### R3 — 副本同步与对齐锁

- 两项修复按 design.md 副本清单落到全部受影响副本；ALIGNMENTS 按 design.md 声明更新（新增 `_strip_typst_line_comment` 全五副本锁、`TypstParser.clean_text` 四副本锁）。`TypstParser.PRESERVE_PATTERNS` 的锁行（:83，全五副本）**不变**——删除 `r"//.*"` 是被锁列表的数据编辑，五副本同步删除后 repr 哈希自动保持一致（锁为即时比较，无存储哈希）。
- 本任务**不触碰** en 子任务（07-15-audit-fix-latex-paper-en）拥有的函数（`extract_title`、`LatexParser.split_sections`/SECTION_TITLE_RULES 等）；若两任务并行，en 先合，本任务 rebase 后重验对齐。

### R4 — 回归测试（每项修复必有，父任务 AC 要求）

- **extract_visible_text**（typst 副本 + EN canonical 各一组）：
  1. `http://` 行内 URL：URL 本体与其后散文均可见；
  2. `https://` 同上；
  3. `https://host//path more prose`：URL（含路径双斜杠）与其后散文**完整可见**（单一所有权决策锁定用例——旧设计在 PRESERVE 阶段挖空该形式，已废弃）；
  4. `#link("https://…") hosts the code.`：#link 调用被挖空、其后散文可见；
  5. `#link("//cdn.example.com/l.js") text`：串内协议相对 URL 不当注释，#link 被挖空、`text` 可见；
  6. 整行 `// comment` → 空串；
  7. 行尾 ` // trailing comment` → 只剩前面散文；
  8. 协议相对 `//cdn.example.com`（裸文本）→ 按注释剥掉（决策锁定用例）；
  9. `a: // comment`（冒号+空格后的真注释）→ 正常剥离；
  10. 反引号 raw 内 `//` 不剥且**保持可见**（PRESERVE 无反引号条目，`//.*` 删除后不再被挖空）；
  11. 同行块注释+行注释 `/* hidden */ prose // note`：块注释由 PRESERVE 挖空、行注释由扫描器剥除、`prose` 可见。
- **clean_text 词数完整性**：多行内容含 URL 行 + 注释行，断言输出词数/文本与预期完全一致（URL 行尾散文保留、注释行删除）；既有 `tests/shared/test_parsers.py:70-77` 两用例保持绿。
- **extract_abstract**：`= Abstract\n…\n== Keywords\n…` → 结果不含 Keywords 内容；`= Abstract\n…\n= Introduction` 行为不变。typst 副本与 EN 锁定三副本（经 hash 锁传导）各有断言。
- **zh 副本 TypstParser**：`extract_visible_text` URL 用例一条（zh 未纳入方法锁，需独立回归）。

### R5 — 约束

- 不改 SKILL.md version / last_updated（父任务 D6：集成阶段统一定稿）。
- 不动 `\cite/\ref/\label`、`@cite`、`<label>`、`$…$` 保护语义（除删除 `r"//.*"` 外，PRESERVE_PATTERNS 其余条目零改动）。
- 检查器默认输出会因 URL 行不再截断而变化——URL 本体现在计入可见文本与词数，属规范允许的「误报/假绿修复」例外，commit message 正文须声明默认行为变化（spec: testing-and-tooling.md 末节）。

## Acceptance Criteria

- [ ] R1/R2 的全部回归测试先红后绿（tests-first）。
- [ ] `uv run --extra dev python -m pytest tests/skills/typst_paper tests/contracts -q` 全绿（含 ALIGNMENTS 新增两行锁）。
- [ ] `uv run --extra dev python -m pytest tests/shared tests/skills/latex_thesis_zh -q` 全绿（EN canonical 与 zh 副本回归）。
- [ ] `just ci` 全绿（lint → pyright error 数为 0 → 全量测试）。
- [ ] 五副本 grep 复核：`split("//")`、`re.sub(r"//.*"` 与 PRESERVE 条目 `r"//.*"` 在 `*/scripts/parsers.py` 中零残留（`typ_loader.py` 的 `LINE_COMMENT_RE` 是独立机制，不在本任务范围）。
- [ ] ALIGNMENTS 净变化仅 +2 锁行；`TypstParser.PRESERVE_PATTERNS` 锁行（:83）零改动。
- [ ] design.md 声明的函数所有权与 07-15-audit-fix-latex-paper-en 无交集（已按 ALIGNMENTS 核对）。

## Out of Scope

- Typst 多行字符串/多行 `#link` 参数跨行的注释判定（extract_visible_text 本就按行工作，行尾未闭合字符串保守不剥）。
- LatexParser 任何行为；zh TypstParser 纳入方法级 hash 锁（保持现有分歧策略）。
- deai_check.py 本体改动（deai 对齐锁不涉及，见 design.md 风险节）。
