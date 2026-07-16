# 多文件工程解析与 section 别名修复（latex-paper-en）— PRD

## Goal

落地父任务 `.trellis/tasks/07-15-skills-deep-audit-opt/prd.md` 登记表 A-EN-1 ~ A-EN-10 十项发现的修复：
消除 latex-paper-en 脚本对 `\input/\include` 多文件工程的系统性盲区、统一 `--section` 别名解析、
补齐 `\begin{abstract}` 环境路由、修复 canonical `parsers.extract_title` 嵌套花括号截断，并清理若干
Low 级缺陷。本任务含 canonical `parsers.py` 改动，是 typst-paper（A-TY-1）与 cover-letter（A-CL-7）
两个子任务的顺序前置（先合本任务）。

## 涉及决策（父任务 D1–D7 中与本任务相关的）

- **D6**：本任务不改 SKILL.md `version` / `last_updated`（版本对齐归 07-15-audit-fix-version-ci；
  `last_updated` 与 CHANGELOG 归父任务集成阶段）。
- **D7**：本任务完成后，07-14 文档子任务 `latex-paper-en` 方可以修好的 SKILL.md 为事实源开工。
- 排序约束（父任务「子任务地图」#2/#3）：本任务先于 cover-letter（A-EN-10 → A-CL-7 三副本同步）；
  与 typst-paper 任务都触碰 parsers 对齐锁，若并行则**先合本任务（en）**。

## Requirements（每项 = 父登记表一条发现；全部要求回归测试，含 Low）

### R1（A-EN-1，High）check_references 多文件假 P0

`check_references.py:356` 只 `path.read_text()` 读入口文件；skeleton `main.tex`（正文全在
`\input{sections/*}`）下跨文件 `\ref` 全部报 "Undefined reference" Critical/P0 并 exit 1。
改为 `tex_loader.assemble()` 装配全文，诊断位置经 `AssembledDocument.origin()/lineref()`
映射回「源文件:行号」。

**AC-R1**
- [ ] 回归测试：tmp_path 多文件 fixture（label 在 `sections/method.tex`、ref 在
  `sections/intro.tex`）修复前 exit 1 / 假 P0，修复后 0 个 undefined-reference issue，exit 0。
- [ ] 多文件模式下文本输出与 JSON 输出的定位为 `sections/xxx.tex:NN` 形态（`lineref` 契约）；
  缺失 include 以 WARN 行呈现（`warning_lines`），不静默。
- [ ] 单文件输入行为逐字节不变（现有 `tests/skills/latex_paper_en` 中 check_references 用例不改断言即绿；
  `Line N` 标签格式不变）。

### R2（A-EN-2，High）analyze_logic / analyze_literature 走 resolve_section_keys

- `analyze_logic.py:676` 裸 `key = section.lower()`：SKILL.md:61 示例命令
  `analyze_logic.py main.tex --section methods` 实际报 "Section not found"（canonical key 是
  `method`）。
- `analyze_literature.py:68` `sections.get(section.lower())`：`--section "related work"` /
  `--section methods` 等别名同样失败。

两处统一走 `parsers.resolve_section_keys`（parsers.py:138，deai_check.py:1066-1075 已是现成消费样板），
未命中时列出 available keys 而非裸报错。

**AC-R2**
- [ ] 回归测试：`analyze_logic` 接受 `methods/methodology/intro/conclusions` 等别名并命中对应区间；
  `analyze_literature` 接受 `related work/literature/related works` 别名；`_2` 重复节一并分析。
- [ ] 未知 section 的错误输出包含 available sections 列表。
- [ ] SKILL.md:61 示例命令在 fixture 论文上实跑成功（exit 0，非 Section-not-found）。

### R3（A-EN-3，High）系统性多文件盲区：分析器批量接入 assemble()

grep 证实除 `verify_bib.py:373-374` 外 0 处 `assemble` 调用。以下入口读文件的**十三个脚本**（十二个分析/检查脚本 + `deai_batch.py`）全部改为
`tex_loader.assemble()`（各 `read_text` / `read_text_robust` 位点）：`deai_check.py:307`、
`analyze_logic.py:671`、`analyze_experiment.py:360`、`analyze_literature.py:145`、
`analyze_abstract.py:211`、`check_figures.py:34`、`check_tables.py:50`、`check_pseudocode.py:56`、
`optimize_title.py:260`，以及父任务裁决补列（◆校正，登记表 A-EN-3 行已更新）的
`analyze_grammar.py:70`、`analyze_sentences.py:84`、`improve_expression.py:59`
（三者当前 `read_text_robust` 单文件读入）；另有同病灶的 `deai_batch.py:30`（父登记表将
deai_batch 归在 A-EN-5 行，此处一并接入，属 A-EN-3 范围澄清，见 Notes）。

注意：新纳入的三脚本与 `analyze_abstract.py` 受 `tests/contracts/test_writing_modules_alignment.py`
的 Tier-1 哈希锁约束（en+typst 副本须逐字节一致），改动须以 loader 无关写法落地并同步 typst 副本，
详见 design.md §2.6。三脚本已用 `resolve_section_keys`，无 R2 类别名工作。

**范围外（显式记录，不在本任务动）**：`compile.py`/`generate_table.py`/
`translate_academic.py`/`extract_prose.py`/`online_bib_verify.py` 语义上无需装配。

**AC-R3**
- [ ] 十三个改动脚本每个至少 1 条多文件回归测试：skeleton main + 分节文件下能产出与单文件等价的发现
  （修复前该发现为 0 / Section not found / "No ... detected"）。
- [ ] 每个改动脚本 1 条单文件不变性测试（沿用既有用例即可）：单文件输入输出逐字节不变。
- [ ] 行号标签走 `lineref()`：单文件 `Line N` 不变；多文件 `sections/x.tex:N`
  （improve_expression 的 Revised 建议须落在正确源文件行，见 design §2.6）。
- [ ] deai_check 的 parsers/deai 对齐锁（`tests/contracts/test_deai_alignment.py`）保持绿：
  锁定成员（`analyze_document`、`generate_suggestions_json`、`_find_pattern_in_section` 等）
  源码不动或按 design.md 声明的方案同步镜像。
- [ ] writing-modules Tier-1 锁（`tests/contracts/test_writing_modules_alignment.py`）保持绿：
  `analyze_grammar/analyze_sentences/improve_expression/analyze_abstract` 的 en/typst 副本
  改后逐字节一致（typst 副本同步属本任务；typst 侧由此经 `typ_loader.assemble` 获得 Typst
  多文件装配，须在交付备注向 typst-paper 子任务声明，避免重复实现）。
- [ ] `.typ` 输入在 en 技能安装形态下行为不变（`tex_loader.assemble` 对 `.typ` 原样读入，
  tex_loader.py:177-185）。

### R4（A-EN-4，Medium）split_sections 识别 \begin{abstract} 环境

`parsers.py:191-201` SECTION_TITLE_RULES 只按标题分类，`\begin{abstract}...\end{abstract}`
环境（无 `\section*{Abstract}` 标题的常见形态）不产生 `abstract` 区间 → `deai_check.py --section
abstract`、`deai_batch --section abstract` 等不可达。在 `LatexParser.split_sections` 注册 abstract
环境区间。**canonical parsers.py 改动，须三副本同步（en → paper-audit → cover-letter）**。

**AC-R4**
- [ ] 回归测试：仅含 `\begin{abstract}` 环境的文档 `split_sections` 返回 `abstract` 键且区间正确；
  已有 `\section*{Abstract}` 时不产生重复键；被注释掉的 `% \begin{abstract}` 不误判。
- [ ] `deai_check.py main.tex --section abstract` 在环境式 fixture 上可命中。
- [ ] `tests/contracts/test_parsers_alignment.py` 全绿（`LatexParser.split_sections` 锁 en/audit/
  cover_letter 三副本 hash 一致）。
- [ ] cover-letter（`extract_section_anchors` 消费方）与 paper-audit 测试套件不红。

### R5（A-EN-5，Medium）deai_batch 别名处理与 deai_check 对齐

`deai_batch.py:274` 裸 `args.section.lower()`，与 `deai_check.py:1066-1075` 的
`resolve_section_keys` 行为分歧（`--section methods` 一个能用一个不能）。统一走
`resolve_section_keys`，miss 时列 available sections。

**AC-R5**
- [ ] 回归测试：`deai_batch --section methods` 命中 `method` 区间；未知名列出可用 sections。

### R6（A-EN-6，Low）SKILL.md 重复行

SKILL.md:132 与 :134 重复 "See `examples/` for complete request-to-command walkthroughs."，删一行。

**AC-R6**
- [ ] 重复行删除；`uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py -q` 绿
  （SKILL.md 变更必跑，防格式化 hook / ROUTER_ROW_RE 回归）。

### R7（A-EN-7，Low）check_figures 死表达式

`check_figures.py:142-144` `width / 3.0` 结果未使用 + 陈旧注释，删除。

**AC-R7**
- [ ] 表达式与关联注释删除；回归测试（或既有 DPI 用例）证明 check_quality 输出不变；
  `just lint` 无新告警。

### R8（A-EN-8，Low）introduction funnel 的 "[" 误判

`analyze_logic.py:220` `"[" in visible` 把数学区间 `[0, 1]`、可选参数残留等当"已引用先前工作"，
使 first_prior 提前成立。收紧为数字引用样式（如 `[12]` / `[3, 7]`）判定；`\cite{` 原判定保留。

**AC-R8**
- [ ] 回归测试：`[0, 1]` / `[k]`（非数字引用）不再置位 first_prior（构造可观察 funnel 输出差异的
  fixture）；`[12]`、`[3,7]` 仍置位。

### R9（A-EN-9，Low，doc-only）check_format 分类局限注记

`check_format.py:31-38` CATEGORY_KEYWORDS 仅英文关键词，`_categorize`（:147-153）对本地化
chktex 输出全落 `other`。不改行为，在 `check_format.py` docstring 与
`references/modules/format.md` 注明 best-effort（英文 locale）语义。

**AC-R9**
- [ ] 两处文档注记落地；行为零变化（不需要新测试，但既有 check_format 用例保持绿）。

### R10（A-EN-10，Low）extract_title 平衡花括号修复（canonical）

`parsers.py:596` 非贪婪 `\{(.+?)\}` 截断嵌套花括号标题；cover-letter 以本地 fork
`extract_manuscript_facts._extract_title_local`（:224-240）绕过。canonical 修复须**完整覆盖该 fork
的三个行为**（fork 删除的前置契约，A-CL-7 依赖）：
1. `\title` 与 `{` 之间容忍空白 / 可选参数（fork :233 `\s*\{`）；
2. 平衡花括号取整个标题体（`_extract_balanced_block`）；
3. 剥离 `\thanks{...}` / `\footnote{...}`（含嵌套花括号体，fork :239 `_strip_balanced_commands`），
   不让资助信息泄入标题。

**AC-R10**
- [ ] 回归测试（在 en 侧固化 fork 用例）：嵌套花括号标题完整提取；`\thanks{... \emph{X} ...}`
  嵌套体被整体剥除；`\title {X}`（带空白）可提取；无 `\title` 时 Typst 分支行为不变。
- [ ] 三副本同步 + `test_parsers_alignment.py` 全绿；ALIGNMENTS 若新增共享 helper 须登记
  （见 design.md）。
- [ ] paper-audit 消费方（parsers.py:632 `extract_title`，literature_search 链路）测试不红。

## 全局验收标准

- [ ] `just ci` 全绿（lint + pyright(basic, 看 error 数) + 全部测试）。前置：07-15-audit-fix-version-ci
  已合入恢复绿基线；本任务不动版本号。
- [ ] 每项修复（含 Low R6–R10）有对应回归测试；R9 doc-only 除外（行为零变化）。
- [ ] `tests/contracts/test_parsers_alignment.py` 与 `test_deai_alignment.py` 全绿；ALIGNMENTS
  变更仅限 design.md 声明的条目；en/audit/cover_letter 三副本被改成员逐字节一致。
  `tests/contracts/test_writing_modules_alignment.py` 全绿（R3 触及的 en+typst Tier-1 组）。
- [ ] SKILL.md 路由表示例命令（:59-:70，至少 logic/literature/deai/experiment 四条 `--section`
  变体）在 fixture 论文上实跑通过。
- [ ] 遵守 CLAUDE.md 红线：不修改 `\cite{}/\ref{}/\label{}`/math 内容语义（本任务只改"读取与定位"，
  不改写用户文档）；不动构建配置；输出协议（`[Severity]`/`[Priority]`/`[Script]`）不变。
- [ ] 单文件输入的所有脚本输出逐字节向后兼容（检查器默认行为变化例外条款仅适用于本任务的
  误报/假绿修复面：R1 假 P0、R2/R5 假 Section-not-found、R4 假不可达、R8 误报——commit message
  按 spec 双声明）。

## Notes

- 父登记表 A-EN-2 表述"SKILL.md 示例命令 `analyze_literature.py --section "related work"` 失败"：
  实际 SKILL.md:62 示例用的是 `--section related`（可用）；`"related work"` 失败是 :68 代码事实
  但非 SKILL.md 示例。已在交付备注回报父任务，不改父 PRD。
- deai_batch 的多文件接入是 A-EN-3 的范围澄清（父表只把它归于 A-EN-5 别名行）。
- analyze_grammar / analyze_sentences / improve_expression 的同型盲区原为父登记表遗漏，
  **父任务已裁决纳入 A-EN-3**（登记表行含 ◆校正标注），本任务在 assemble 批次一并处理（R3）。
  三者与 analyze_abstract 同受 en+typst Tier-1 哈希锁约束，见 design.md §2.6。
