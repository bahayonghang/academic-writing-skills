# 章节识别与 verify_bib 健壮性（latex-thesis-zh）— PRD

> 父任务：`.trellis/tasks/07-15-skills-deep-audit-opt/prd.md`。本子任务承接发现 **A-ZH-1 ~ A-ZH-9** 与决策 **D5**。
> 所有 file:line 均已对照当前 dev 分支代码核实（2026-07-15）。

## Goal

修复 latex-thesis-zh 六个脚本面的行为缺陷（章节分类、bib 解析、文件归属、编译器探测、标题截断）与三项 Low 级噪声/文档项。每项修复（含 Low）配回归测试，`just ci` 保持绿。

## Scope

- 只改 `academic-writing-skills/latex-thesis-zh/` 下的 scripts / SKILL.md / references / evals fixture，及 `tests/`（zh 测试 + 必要的 contract 声明更新）。
- 不动构建配置（justfile / pyproject / hooks）；不 bump SKILL.md version（版本对齐由 07-15-audit-fix-version-ci 负责）；`last_updated` 按父任务 D6 延后到集成阶段，本任务不改。
- 不动 EN/typst/audit/cover-letter 的 parsers 副本（zh 需要的函数在 zh 副本内自足）。

## Requirements 与验收标准

### R1（A-ZH-1，High）conclusion 章节规则识别 `结论与展望` / 裸 `总结`

现状：`parsers.py:183` LaTeX 规则 `^(?:结论|总结与展望)$` 不匹配 `结论与展望` 与裸 `总结`；Typst 规则 `parsers.py:308` 未锚定（子串误配 `结论性章节` 一类标题）；`SECTION_KEY_ALIASES`（:96-122）缺 `结论与展望` 条目。下游 `analyze_conclusion.py:173` 因 split_sections 无 conclusion 键而整体跳过。

**AC**：
- [ ] `LatexParser.split_sections` 对 `\chapter{结论与展望}`、`\chapter{总结}`、`\chapter{结论}`、`\chapter{总结与展望}` 均产出 `conclusion` 键。
- [ ] `TypstParser.split_sections` 对 `= 结论与展望`、`= 总结` 同样产出 `conclusion`；LaTeX/Typst 采用**同一锚定正则**。
- [ ] 负例：标题 `结论性章节`、`实验结论分析`、`总结报告` **不**分类为 conclusion（过匹配守卫）。
- [ ] `resolve_section_keys("结论与展望", ...)` 命中 conclusion（SECTION_KEY_ALIASES 扩条目）。
- [ ] 端到端回归：对 `\chapter{结论与展望}` 文档跑 `analyze_conclusion.py`，不再出现「未识别到结论/总结与展望章」跳过提示。
- [ ] **命名测试缺口 ①**：新增 `结论与展望` 章标题 fixture 的用例（合成 fixture 即可）。
- [ ] `tests/contracts/test_parsers_alignment.py` 全绿（zh 的 SECTION_TITLE_RULES / SECTION_KEY_ALIASES 均不在 zh 锁内，见 design；zh 已锁项 PRESERVE_PATTERNS / `_normalize_whitespace` 不得触碰）。

### R2（A-ZH-2，High + D5）verify_bib 平衡括号/引号扫描器

现状：`verify_bib.py:73` 条目正则 `[^@]*?` 使值内含 `@`（如邮箱）的条目吞并后续条目且无警告（实测 2 条→1 条）；`:91` 字段正则字符类 `[^^{}]` 丢弃含 `^` 的字段（`$L^2$` 标题误报 FAIL），且仅支持一层花括号嵌套。

**处置（D5，已定）**：不做单字符正则补丁；改为平衡括号/引号扫描器，改编自 `bib-search-citation/scripts/search_bib.py` 的 `split_top_level`(:652) / `_scan_entry_span`(:734) / `parse_fields`(:724) / `parse_bib_entries`(:777) 既有实现（vendored 适配，非第三套自造解析器）。

**AC**：
- [ ] `title = {The $L^2$ Norm}`（含 `^`）字段完整解析，caps 检查不误报 FAIL。
- [ ] 值内含 `@`（`note = {mail: a@b.edu}`）时前后两条条目均被解析（total_entries 正确）。
- [ ] 两层及以上嵌套花括号（`title = {{Deep {Learning}} Methods}`）字段值完整保留。
- [ ] 引号值内的花括号按字面处理；未闭合条目产生 warning 级 issue 并 resync（不静默丢弃后续条目）。
- [ ] `@comment`/`@preamble` 不计入条目；`@string` 宏可展开（随 vendored 代码一并带入）。
- [ ] **命名测试缺口 ②**：`^` 与 `@` 字段 fixture 用例落地（tmp_path 合成 .bib）。
- [ ] 既有 `tests/skills/latex_thesis_zh/test_latex_thesis_zh_gb7714.py`、`test_latex_thesis_zh_scripts.py` verify_bib 段全绿（entry dict 形状 `type/key/fields/raw` 不变）。

### R3（A-ZH-3，Medium）verify_bib 与 check_spec._load_bib 编码健壮化

现状：`verify_bib.py:66` `read_text(encoding="utf-8", errors="ignore")` 把 GBK bib 静默读成乱码，CJK GB 检查全部 no-op（零 CJK note 假 PASS）；`check_spec.py:336` `errors="replace"` 同样无 GB18030 回退。

**AC**：
- [ ] 两处改用 `tex_loader.read_text_robust`（`tex_loader.py:29-43`：utf-8 → GB18030 → replace+警告）。
- [ ] GBK 编码 .bib：中文条目被正确解析，`gb_langid_hint` / 作者截断等 CJK 检查恢复生效，且输出一条编码警告（非静默）。
- [ ] `check_spec` 对 GBK bib 的条目数/年份统计正确，bib_note 含编码提示。
- [ ] **命名测试缺口 ③**：GBK .bib fixture 落地——`evals/fixtures/thesis-project/references-gbk.bib`（GB18030 编码，虚构条目，README 补埋点说明），单测直接引用该文件。
- [ ] 默认行为变化（假绿修复例外）按 spec 约定双声明：更新受影响存量单测 + commit message 声明。

### R4（A-ZH-4，Medium）check_references 多文件输出带文件归属

现状：`check_references.py` 已按文件收集 `LabelInfo.file`/`RefInfo.file`（:57/:66），但 `_add_issue`(:96-112) 不落 file 字段，`_format_issues`(:396-408) 只渲染 `(Line N)`——12 文件工程下行号无从定位，违反 SKILL.md「源文件:行号」契约。

**AC**：
- [ ] issue dict 新增 `file` 字段（源文件相对路径，取 `iter_files` 的 `node.rel`）。
- [ ] 多文件模式文本输出渲染 `chapters/xxx.tex:15` 风格位置（与 `tex_loader.AssembledDocument.lineref` 的多文件格式一致）；单文件模式输出保持逐字节兼容（仍为 `(Line 15)`）。
- [ ] `--json` 输出含 `file` 字段（增量、不破坏既有键）。
- [ ] **命名测试缺口 ④**：多文件 `源文件:行号` 断言——用 thesis-project fixture 或合成多文件工程断言 issue `file` 字段与渲染文本中的 `chapters/….tex:行号`。
- [ ] `tests/skills/latex_thesis_zh/test_latex_thesis_zh_multifile.py` 存量用例全绿。

### R5（A-ZH-5，Medium）compile.py 指令优先 + 健壮读取

现状：`compile.py:97-102` 中文检测先于 `:104-109` 的 `% !TEX program` 指令 → 写明 LuaLaTeX 的中文论文被强制 xelatex；`:93` 入口 `errors="ignore"` 读取。

**AC**：
- [ ] `_detect_compiler` 判定顺序改为：`% !TEX program` 指令 → 中文特征 → fontspec → pdflatex。
- [ ] 回归：含 ctex 且 `% !TEX program = lualatex` 的文档返回 `lualatex`；无指令的中文文档仍返回 `xelatex`（存量行为不变）。
- [ ] 入口读取改 `read_text_robust`；GBK 编码、仅正文含中文的 .tex 也能命中中文特征返回 `xelatex`。
- [ ] 默认行为变化（误报修复例外）双声明。

### R6（A-ZH-6，Medium）平衡花括号的标题/heading 提取

现状：`parsers.py:145-147` `HEADING_PATTERN` 的 `\{(?P<title>[^}]*)\}` 在嵌套花括号（如 `\chapter{基于\textbf{X}的方法}`）处截断；`extract_title` :417/:422 非贪婪 `(.+?)` 同因截断 → `check_spec.py:383` 的标题字数上限检查拿到截短标题假 PASS。

**AC**：
- [ ] `extract_headings` 对嵌套花括号标题返回完整 title（单行内嵌套；跨行标题维持现状跳过）。
- [ ] `extract_title` 对 `\ctitle{基于\textbf{深度学习}的…}` 返回完整、去标记后的标题文本。
- [ ] 回归：构造去标记后长度 > title_max 的嵌套花括号标题，`check_spec` 标题长度检查项不再假 PASS。
- [ ] 复用 EN 副本 `_extract_balanced_block`（`latex-paper-en/scripts/parsers.py:518-538`）逐字节 vendored 到 zh；`tests/contracts/test_parsers_alignment.py:78` 的 `_extract_balanced_block` 锁列表**加入 "zh"**（声明式 ALIGNMENTS 更新，防后续漂移）。
- [ ] zh 既有锁项（LatexParser/TypstParser 的 PRESERVE_PATTERNS、`_normalize_whitespace`）哈希不变，contract 测试全绿。

### R7（A-ZH-7，Low）mixed_punctuation 不误报 `\ref{eq:能量}` 等中文 key

现状：`check_format.py:69-76` mixed_punctuation `visible_only: False`，`_PATH_ARG_RE`(:55) 只剥 `\includegraphics/\input/\bibliography`——`\ref{eq:能量}`、`\label{sec:方法}` 的 `:`+CJK 命中 `[,.:;!?][一-鿿]`。

**AC**：
- [ ] `\ref{eq:能量}`、`\label{sec:方法}`、`\cite{张三2024}` 等 key 参数不再触发 mixed_punctuation（剥离时等长空格占位，列号不漂移）。
- [ ] 正例仍报：正文 `中文,英文标点` 命中不变；`test_latex_thesis_zh_checker_precision.py` R2b 存量三用例全绿。

### R8（A-ZH-8，Low）缩写检查扩 stoplist + 最小出现阈值

现状：`check_consistency.py:233-240` 仅 7 词内联 stoplist（PDF/URL/HTTP/HTTPS/API/TODO/FIXME）→ IEEE/GPU/DOI/GB 等常见非缩写噪声泛滥。

**AC**：
- [ ] stoplist 提升为模块级常量并扩充（至少含 IEEE/ACM/ISO/GB/DOI/GPU/CPU/RAM）；undefined 类 issue 增加最小出现次数阈值（≥2 次才报）。
- [ ] 回归：单次出现的未定义大写串不报；出现 ≥2 次且非 stoplist 的仍报。
- [ ] 默认行为变化（误报修复例外）双声明。

### R9（A-ZH-9，Low，doc）GB/T 7714-2025 路由注记

现状：`SKILL.md:67` bibliography 行主命令固定 `--standard gb7714`（2015 版）；GB/T 7714-2025 已于 2026-07-01 实施，`verify_bib.py:441-445` 早已支持 `--standard gb7714-2025`。

**AC**：
- [ ] SKILL.md:67 该行「Use when」列注明 2026-07-01 起可用 `--standard gb7714-2025`（主命令 backtick 内容不改，避免 ROUTER_ROW_RE / router_help 契约波动）。
- [ ] `check_spec.py:169-175` `MODULE_COMMANDS` 旁注释注明 gb7714-2025 可选（不改命令字符串值，避免 spec-check 输出变化）；`references/modules/bibliography.md` 同步一句说明。
- [ ] 回归测试：源级断言（仿 `test_latex_thesis_zh_gb7714.py:182` 风格）SKILL.md bibliography 行与 check_spec 源码含 `gb7714-2025` 注记。
- [ ] SKILL.md 表格改动后 `tests/contracts/test_skill_contracts.py` 全绿（格式化 hook 重排表格陷阱）。

## 总验收

- [ ] `uv run --extra dev python -m pytest tests/skills/latex_thesis_zh -q` 全绿。
- [ ] `uv run --extra dev python -m pytest tests/contracts/test_parsers_alignment.py tests/contracts/test_skill_contracts.py -q` 全绿。
- [ ] `just ci` 全绿（父任务 A-REL-1 版本失配由 07-15-audit-fix-version-ci 先行恢复绿基线；若其未合入，本任务验证时对该已知红项做说明而非顺手改版本）。
- [ ] 四个命名测试缺口（结论与展望 fixture、`^`/`@` 字段 fixture、GBK .bib fixture、多文件 `源文件:行号` 断言）全部落地。
- [ ] 遵守 CLAUDE.md 红线：不动 `\cite/\ref/\label`/数学环境**内容**（R7 仅检测期等长剥离，不改写源文件）；不造文献数据（GBK fixture 用虚构占位条目）。
