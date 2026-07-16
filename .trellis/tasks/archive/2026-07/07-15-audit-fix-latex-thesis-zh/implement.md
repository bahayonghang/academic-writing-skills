# 实施清单 — 07-15-audit-fix-latex-thesis-zh

> 原则：每批次先写失败测试（tests-first），再实现，再跑批次验证；每批次形成一个**拟提交分组**（= 回滚单元，见文末回滚点）。
> **全程不做 git commit——所有分组留到 Phase 3.4 统一展示确认。**
> zh 副本测试**必须** importlib 按路径加载（spec：testing-and-tooling.md「zh/typst 副本脚本的测试必须 importlib 按路径加载」，样板 `tests/skills/latex_thesis_zh/test_deai_tense_zh.py::_load_zh` 或各文件既有 `_load_zh`）；路径常量只从 `tests.support.paths` 导入。
> **Windows 注意（memory）**：需要重定向脚本 JSON 输出到文件时，逐命令加 `PYTHONIOENCODING=utf-8`，**绝不 export 全局**；跑 pytest 一律不加该变量（会炸 test_skill_contracts 的 subprocess 用例）。

## 批次 0：基线确认

- [ ] `git log --oneline -3` 确认基于 dev；确认 07-15-audit-fix-version-ci 是否已合入（决定 `just ci` 的已知红项预期）。
- [ ] 基线：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh tests/contracts/test_parsers_alignment.py -q` → 记录通过数。

## 批次 1：R1 conclusion 章节规则（A-ZH-1）

- [ ] 新增 `tests/skills/latex_thesis_zh/test_section_rules_zh.py`（importlib 加载 zh parsers，含加载守卫断言 `SECTION_KEY_ALIASES["结论与展望"]` 存在——先红）：
  - LaTeX/Typst 四正例（结论/总结/结论与展望/总结与展望）+ 三负例（结论性章节/实验结论分析/总结报告）；
  - `resolve_section_keys("结论与展望", ...)` 命中；
  - 端到端：合成 `\chapter{结论与展望}` fixture 跑 `analyze_conclusion`，断言无「未识别到结论」跳过提示（命名缺口 ①）。
- [ ] 改 `parsers.py:183`、`:308` 为 `^(?:结论|总结)(?:与展望)?$`；`:96-122` 加 `"结论与展望": "conclusion"`。
- [ ] 兄弟检查器扫描：对同一 fixture 跑 analyze_experiment / analyze_logic 完整输出，确认无同型异常。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_section_rules_zh.py tests/skills/latex_thesis_zh/test_analyze_conclusion.py tests/contracts/test_parsers_alignment.py -q`
- [ ] 拟提交分组 1：记录本批次文件集 + 拟用 message（须声明 Typst 锚定为误报修复类默认行为变化），留待 Phase 3.4。

## 批次 2：R2+R3 verify_bib 扫描器 + 编码（A-ZH-2/3，D5）

- [ ] 新增 `tests/skills/latex_thesis_zh/test_verify_bib_scanner.py`（先红）：
  - `^` 字段、`@` 值、两层嵌套花括号、引号值内花括号、未闭合条目 resync + warning（命名缺口 ②）；
  - GBK：读 `evals/fixtures/thesis-project/references-gbk.bib`，断言条目解析、`gb_langid_hint` 触发、`encoding_warning` 存在（命名缺口 ③）；
  - check_spec：GBK bib 的条目数/年份统计 + bib_note 编码提示。
- [ ] 用 Bash python 以 bytes 写入 `references-gbk.bib`（GB18030，虚构条目），补 `thesis-project/README.md` 埋点行。
- [ ] 新建 `scripts/bib_scan.py`：从 `bib-search-citation/scripts/search_bib.py` 逐字节拷贝 `split_top_level/_scan_entry_span/parse_fields/resolve_field_value/_resolve_value_atom/_find_key_separator/_line_of/parse_bib_entries`（剔除 search 专属部分），文件头标注来源。
- [ ] 改 `verify_bib.py`：`parse()` 走 `read_text_robust` + `parse_bib_entries` 映射；删 `_parse_fields` 与旧 entry_pattern（自产孤儿）；warning → issues。
- [ ] 改 `check_spec.py:336` → `read_text_robust`，bib_note 拼警告。
- [ ] 同步存量测试（若有依赖旧解析盲区的断言）。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_verify_bib_scanner.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_gb7714.py tests/skills/latex_thesis_zh/test_check_spec.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py -q`
- [ ] 拟提交分组 2：记录本批次文件集 + 拟用 message（声明三项假绿修复默认行为变化）。

## 批次 3：R4 check_references 文件归属（A-ZH-4）

- [ ] `test_latex_thesis_zh_multifile.py` 增用例（先红）：thesis-project fixture（或合成 2 文件工程）→ issue dict 含 `file`（rel 路径），文本输出含 `chapters/….tex:行号`（命名缺口 ④）；单文件模式输出仍为 `(Line N)`（字节兼容守卫）。
- [ ] 改 `check_references.py`：`all_files` 键改 `node.rel`；`_add_issue` 加 file 参数；五个 check 传 `lbl.file`/`ref.file`；`_format_issues` 按 multi_file 渲染；main() 传 multi_file。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py -q`
- [ ] 拟提交分组 3：记录本批次文件集 + 拟用 message。

## 批次 4：R5 compile 指令优先（A-ZH-5）

- [ ] `test_latex_thesis_zh_scripts.py` compile 段（:479 起）增用例（先红）：ctex + `% !TEX program = lualatex` → `lualatex`；无指令中文 → `xelatex`；GBK 中文 .tex → `xelatex`。
- [ ] 改 `compile.py:90-116`：指令块前移；`read_text_robust` 导入（sys.path fallback）。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py -q`
- [ ] 拟提交分组 4：记录本批次文件集 + 拟用 message（声明指令优先默认行为变化）。

## 批次 5：R6 平衡花括号提取（A-ZH-6）

- [ ] 测试先红：`test_section_rules_zh.py`（或 scripts 测试）加嵌套花括号 heading/extract_title 用例；`test_check_spec.py` 加「嵌套花括号超长标题不再假 PASS」用例。
- [ ] `parsers.py`：vendored `_extract_balanced_block`（EN :518-538 逐字节）；改 `HEADING_PATTERN` + `extract_headings` + `extract_title`。
- [ ] **同一拟提交分组**内更新 `tests/contracts/test_parsers_alignment.py:78` 锁列表加 `"zh"`。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh -q && uv run --extra dev python -m pytest tests/contracts/test_parsers_alignment.py -q`
- [ ] 拟提交分组 5：记录本批次文件集 + 拟用 message（声明 ALIGNMENTS 更新；parsers 与 ALIGNMENTS 必须同组）。

## 批次 6：R7+R8 两个 Low 检查器项

- [ ] `test_latex_thesis_zh_checker_precision.py` 增：`\ref{eq:能量}`/`\label{sec:方法}`/`\cite{张三2024}` 负例 + 真混排正例仍报（先红）。
- [ ] `check_format.py`：加 `_KEY_ARG_RE` 并在 strip_path_args 分支应用。
- [ ] 缩写用例（同文件或 scripts 测试）：单次 IEEE 不报、两次 XYZC 仍报、stoplist 词不报（先红）。
- [ ] `check_consistency.py`：`ABBREV_STOPWORDS`/`ABBREV_MIN_USES` 常量化 + undefined 阈值。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_latex_thesis_zh_checker_precision.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_scripts.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py -q`
- [ ] 拟提交分组 6：记录本批次文件集 + 拟用 message（声明两处误报修复默认行为变化）。

## 批次 7：R9 gb7714-2025 注记（doc）

- [ ] 源级断言测试（先红，放 `test_latex_thesis_zh_gb7714.py` 尾部，仿 :182 风格）：SKILL.md bibliography 行含 `gb7714-2025`；check_spec.py MODULE_COMMANDS 区段含 `gb7714-2025` 注记。
- [ ] 改 SKILL.md:67 Use-when 列、check_spec.py:168-175 注释、`references/modules/bibliography.md`。
- [ ] 验证：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_latex_thesis_zh_gb7714.py tests/contracts/test_skill_contracts.py tests/contracts/test_docs_bilingual_resources.py -q`
- [ ] 拟提交分组 7：记录本批次文件集 + 拟用 message。

## 收尾门（review gate）

- [ ] 全量：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh -q`
- [ ] 契约：`uv run --extra dev python -m pytest tests/contracts -q`
- [ ] `just ci`（lint → pyright → 全测；pyright 看 **error 数**非 warning 数）。
- [ ] `just fix` 后确认无格式漂移（尤其 SKILL.md 表格、evals fixture 未被 hook 重排：`git diff --stat` 应为纯增量）。
- [ ] 自查：diff 中每一行都能追溯到 R1-R9；zh 已锁三项（PRESERVE_PATTERNS ×2、`_normalize_whitespace`）零改动；未触碰 evals.json。
- [ ] 逐拟提交分组检查 message 草稿中默认行为变化声明齐全（R1/R2/R3/R5/R7/R8），待 Phase 3.4 统一展示确认后提交。

## 回滚点

每批次一个拟提交分组（工作区不产生 commit）；任一批次验证红且无法当场修复时，按 scoped restore 回退该组改动——既有文件 `git checkout -- <该批次修改文件>`，本批新建文件（测试/fixture/bib_scan.py 等）单列显式 `rm`（checkout 无法移除新文件）；禁用 reset（本批新增文件直接删除），或先 `git stash` 暂存排查；其余批次不受影响（批次间无代码耦合；唯一跨文件耦合是批次 5 的 parsers + ALIGNMENTS 同组，回退时二者一体回退）。
