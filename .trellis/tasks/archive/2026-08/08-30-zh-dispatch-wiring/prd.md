# zh 检查调度修复与专属检查器接通

父任务：`.trellis/tasks/08-30-paper-audit-zh-profile`（需求全集、跨子任务验收在父 `prd.md`）

## Goal

修复 `paper-audit` 在 `lang == "zh"` 路径上的三类调度缺陷（死条目、无声英文回退、bib 输入错位），并把 `latex-thesis-zh` 已有的学位论文专属检查器按模式接入调度链。本子任务只动调度与脚本接线，不写审阅准则文档与 agent（属 C2）。

## Requirements

### R1 消除死条目

1. `ZH_EXTRA_CHECKS`（`scripts/audit.py:301`）中的 `gbt7714` 不再产生 `SKIP gbt7714: script not found`。
2. GB/T 7714 能力由 `latex-thesis-zh/scripts/verify_bib.py` 的 `--standard gb7714` / `gb7714-2025` 承载，不新写检查器。

### R2 修复 `bib` 检查输入

3. `bib` 检查必须接收 `.bib` 路径。复用 `audit.py:62` 的 `_load_bibliography_content` 同源解析逻辑得到 `.bib` 路径；无法解析出 `.bib` 时输出显式 SKIP 原因，不静默空通过。
4. `fmt == ".tex"` 且（`lang == "zh"` 或 `--venue thesis-zh`）时为 `bib` 追加 `--standard gb7714`（design §4 已定标，依据是 `check_spec.py:173` 的现行推荐值与 `verify_bib.py:406`-`:413` 的标准切换提示）。**`.typ` 不追加**——Typst 侧 `verify_bib.py` 只有 `--style`，传 `--standard` 会以 argparse 退出码 2 失败（TPR-02）。
5. 该修复对英文路径同样生效。若既有 EN 测试因 `bib` 首次产出真实 finding 而失败，更新期望值，不通过条件分支回避。

### R3 语言回退显式化

6. `_resolve_script`（`audit.py:379`-`:432`）在 `lang == "zh"` 落到 `SCRIPTS_EN` 时不再静默。每个这样的检查项必须有一个书面判定，落在三档之一：**有意复用**（语言无关）/ **替换**（改为 zh 检查器）/ **抑制**（对中文无意义且无 zh 替代）。
7. 已确认的证据（design 中据此定档，不重新调研）：
   - `check_figures.py`（EN）：DPI / 图片格式 / 编号序列，纯 LaTeX 与图片文件分析 → 有意复用。
   - `check_pseudocode.py`（EN）：**非语言中性**。`_count_words` 是 `len(re.findall(r"[A-Za-z0-9_+-]+", text))`，对纯中文注释恒为 0；`re.match(r"^(?:The|A|An)\b", caption)` 查英文冠词；`:194`-`:195` 要求字面量 `"Input:"` / `"Output:"`。→ zh 下抑制，本地化另立任务（TPR-05）。
   - `analyze_sentences.py`（EN）：`CLAUSE_MARKERS = {"which","that","because",...}`（`:27`），英文从句标记与按词计数 → 替换。
   - `analyze_grammar.py`（EN）：英文语法检查 → 抑制（职能并入下一项）。
   - `check_style_zh.py`（ZH，23.9 KB）：中文口语词 `COLLOQ_MAP`（`:50`）、绝对化词 `ABSOLUTE_TERMS`（`:61`）、搭配错误 `COLLOC_ERRORS`（`:76`）、残缺主语 `SUBJECT_MARKERS`（`:88`）、中西文标点与数字单位、`DEFAULT_MAX_CHARS = 80` 字符级句长（`:45`）；有 `severity` 字段（Info / Warning）与 `--section` / `--json`。它同时覆盖 EN 侧 `grammar` 与 `sentences` 两个键的职能。
8. **替换必须挂在 `sentences` 键上，不能挂在 `grammar` 键上。** `run_polish_precheck`（`audit.py:2254`）早退于统一分流之外，直接调 `_resolve_script("logic", ...)` 与 `_resolve_script("sentences", ...)`，不读 `MODE_CHECKS`。把 zh 替换挂在 `sentences` 上，polish 才能自动拿到 `check_style_zh.py`；挂在 `grammar` 上并抑制 `sentences` 会让中文 polish 直接丢失表达检查（TPR-01）。
9. 运行日志必须能区分"有意复用英文脚本"、"按语言替换"、"按语言抑制"与"未找到脚本"四种情形。当前后三种的输出不可分辨。
10. 格式面必须显式：`.typ` 独占 `SCRIPTS_TYPST`（`audit.py:420`-`:421`），zh 检查器对 Typst 不可达，需显式豁免；`.pdf` 的既有跳过清单（`audit.py:2492` 附近）必须纳入全部新增 zh 检查器（它们都要 TeX 源）（TPR-01）。

### R4 接通 zh 专属检查器

11. 下列脚本按 design 判定接入 `script_map`，每项都要指明适用的 lang / fmt / 入口：`check_spec.py`、`blind_review.py`、`check_style_zh.py`、`analyze_abstract.py`、`analyze_conclusion.py`、`analyze_literature.py`、`check_tables.py`。
12. `optimize_title.py` 与 `map_structure.py` 判定为接入或不接入均可，但必须有书面理由（前者是优化取向而非审阅取向，后者是工具性脚本）。
13. **只读边界（TPR-09 修正）**：写回触发分支是 `if args.generate:`（`blind_review.py:794`）。契约是**调度链路绝不传 `--generate`**。`--author` / `--supervisor` 是只读扫描输入，缺失时会跳过部分姓名检测，可按可用元数据决定是否传，不在禁用之列。验收用文件 sha256 与 mtime 不变来证明只读，不用参数黑名单代理。
14. 需要额外输入的脚本（`check_spec.py --bib`、`analyze_literature.py --bib`）复用 R2 的 `.bib` 解析结果。
15. **禁止依赖"优先 JSON、否则文本"的通用猜测式解析（TPR-02）。** 实测 CLI 面：`check_spec.py` / `analyze_abstract.py` / `analyze_conclusion.py` / `check_tables.py` / `check_style_zh.py` 有 `--json`；`blind_review.py` 与 `latex-thesis-zh/scripts/analyze_literature.py` **没有 `--json`**。必须建立逐脚本 adapter registry，登记真实 CLI、输入格式、输出 schema、退出码语义与 issue 映射。
16. **退出码语义必须收紧（TPR-02）。** 现有处理（`audit.py:2528`-`:2545`）只在 `returncode == -1` 时生成错误项；未知参数导致 argparse 退出码 2 且 stdout 为空时会落到 `else: print(f"[audit] {check_name}: clean")`，把失败报成无发现。修改为：任何非零退出码且无可解析输出，一律生成错误项，不得报 clean。
17. 新接通脚本产出的 `AuditIssue.module` 必须能进入 `scholar_eval.MODULE_DIMENSION_MAP`（`scripts/scholar_eval.py:65`）。扩展映射时同步更新其精确相等锁 `tests/skills/paper_audit/test_literature_search.py:578` 与 `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md:53` 的错误矩阵，并定义未知模块 fail-closed 行为（TPR-06）。不改 8 个基础维度与权重。
18. **`gate` 只接纳同时满足三条的检查**：有明确规范依据、对当前模板必需、可确定检测。`check_consistency.py` 只产 `PASS` / `WARNING`（`:237`、`:304`），不入 gate（TPR-03）。

### R5 不动的边界

19. 不改 `SKILL.md:68` 的方法叙述边界（中文方法章叙述仍在 `latex-thesis-zh` 显式工作流）。
20. 不改 issue JSON schema、severity 档位、ScholarEval 的 8 个基础维度与权重、`[Script]` / `[LLM]` 标签语义。
21. 不改 `latex-thesis-zh` 任何脚本的检查逻辑与输出格式。
22. 不新增第三方依赖。不新增语言开关。
23. 不修 `run_deep_review` / `run_reaudit` 的 mode 传播——`audit.py:2441` 的委派使其存在递归风险，属范围外后续项（TPR-01）。

## Acceptance Criteria

每条 AC 后括注对应的 R 条与 design 小节。

- [ ] AC1-1（R1 / design §4）：中文 `.tex` fixture 跑 `--mode quick-audit`，stdout 无 `SKIP gbt7714`。
- [ ] AC1-2（R2、R4 / design §4）：新增测试断言 `bib` 检查的实参第一位是 `.bib` 路径；给定含 GB 违规条目的 `.bib` fixture 时，`Total entries` 大于 0 且至少一条 GB/T 7714 增量 finding 进入 `AuditIssue` 列表。仅 `.tex` 适用——Typst 侧 `verify_bib.py` 无 `--standard`，只有 `--style`。
- [ ] AC1-3（R3 / design §4）：`.bib` 无法解析时，stdout 出现指明原因的 SKIP 行，且该情形有测试覆盖。
- [ ] AC2-1（R6、R9、R10 / design §1、§2、§3）：新增**可达性矩阵**测试，维度为 `真实入口 × lang × fmt × 检查键`。真实入口四条：`main→run_audit`（唯一透传 `args.mode`）、`run_audit:2441→run_deep_review→run_audit`（硬编码 `quick-audit`）、`run_reaudit→run_audit`（硬编码 `quick-audit`）、`run_audit:2431→run_polish_precheck`（早退，只解析 `logic` / `sentences`）。逐单元断言解析结果为 `audit` / `zh` / `en` / `typst` / `suppressed` / `format-skipped` 之一，期望值与 design §1、§2 逐项一致（TPR-01）。
- [ ] AC2-2（R7、R8 / design §1）：zh 下 `grammar` = 抑制、`sentences` = `check_style_zh.py`、`figures` = 有意复用 EN、`pseudocode` = 抑制。有一条专门测试断言 `run_polish_precheck` 在 `lang="zh"` 时拿到的 `sentences` 脚本是 `check_style_zh.py`——这是 polish 不回归的直接证据（TPR-01、TPR-05）。
- [ ] AC2-3（R9 / design §3）：日志可区分四种情形（`lang-neutral-reuse` / `override` / `suppressed` / `missing`），每种至少一条断言。
- [ ] AC3-1（R11、R15 / design §5、§8）：design 判定为接通的 zh 检查器均可从 `audit.py` 调度成功，输出经**其专属 adapter** 解析为带 `[Script]` 标签的 `AuditIssue`。每个 adapter 五类回归测试齐全：真实样例、未知参数（argparse 退出码 2）、非零退出、空输出、非法 JSON（TPR-02）。
- [ ] AC3-2（R12 / design §5）：判定为不接通的项目在 design 中有理由，且 `script_map` 中不存在指向它们的死键。
- [ ] AC3-3（R16 / design §8）：测试断言非零退出码且无可解析输出时生成错误项，stdout 不出现 `clean`（TPR-02）。
- [ ] AC3-4（R17 / design §9）：新增的 module 名全部存在于 `scholar_eval.MODULE_DIMENSION_MAP`；`tests/skills/paper_audit/test_literature_search.py:578` 的相等断言已同步；有一条 fail-closed 测试断言未登记模块会被 guard 捕获而非静默忽略（TPR-06）。
- [ ] AC4-1（R13 / design §5）：测试断言 `blind_review.py` 的调用参数**不含 `--generate`**；并断言只读运行前后 fixture 文件的 sha256 与 mtime 均不变（TPR-09）。
- [ ] AC4-2（R18 / design §7）：测试断言 gate 的 zh 阻断候选集由 `gateEligible` 三条判据产生，不含 `consistency`，也不含任何模板标注为可选的章节存在性检查（TPR-03）。
- [ ] AC5（—）：`just ci` 全绿，测试数不低于开工时实测基线。
- [ ] AC6（R21 / design §10）：`latex-thesis-zh/scripts/` 与 `latex-paper-en/scripts/` 下无文件被修改（`git diff --stat` 验证）。
- [ ] AC7（R17 / design §10）：`tests/skills/paper_audit/test_paper_audit.py:419`-`:422` 的 `test_zh_extra_checks` 仍然通过或已按 design §6 显式迁移；不允许因符号形状变更而静默失效（TPR-11）。

## Notes

- 不要用 `Edit` / `Write` 改 `evals/evals.json`：格式化 hook 会压平数组。写临时 `.py` 文件用 `uv run --extra dev python <file>` 执行（不要用 heredoc，PowerShell 不支持，TPR-12）。
- 不要让全局格式化 hook 对齐 `SKILL.md` 的表格：会触发 `ROUTER_ROW_RE` contract 测试。本子任务原则上不改 `SKILL.md`；若必须改，只改正文不改路由表格式。
- `tests/conftest.py` 只把 EN 与 AUDIT 的 scripts 目录放进 `sys.path` 前排，bare import 拿到的永远是 EN 副本。测试中需要 zh 脚本时用 `importlib.util.spec_from_file_location`。
