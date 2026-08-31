# paper-audit 中文学位论文审阅 profile 扩充

## Goal

在不拆分 skill 的前提下，让 `paper-audit` 对中文学位论文（大论文）的审阅达到与英文会议/期刊论文（小论文）同等的可用程度。改造沿 `--venue thesis-zh` / `lang == "zh"` 轴进行：修复现有 zh 检查调度缺陷、接通 `latex-thesis-zh` 已有但审稿链路触达不到的检查器、补齐中文学位论文的审阅准则文档与 reviewer agent。

## User Value

用户对同一个 `paper-audit` 说"审稿"时，中文学位论文与英文小论文都应得到与其体裁匹配的审阅意见。当前中文学位论文走审稿链路会得到英文小论文的检查结果：部分检查用英文脚本跑中文正文，学位论文特有的盲审、规范、摘要/结论、工作量与创新性维度完全不出现在报告里。

## Confirmed Facts

以下事实均已在 HEAD `29c3cb3`（2026-08-30）实测确认。此前记录的 `50d06fb` 已不是当前 HEAD，其间含 `c575110 feat(paper-audit): 新增小节上下文审阅通道` 等 paper-audit 变更；本节数据已按 `29c3cb3` 的工作树复核（TPR-13）。

### 语言不是 paper-audit 的主要变化轴

- `paper-audit` 是调度器：语言特定检查委派给 `latex-paper-en` / `latex-thesis-zh` / `typst-paper` 的脚本目录（`academic-writing-skills/paper-audit/scripts/audit.py:372`-`:376`、`:419`-`:432`）。
- 语言分支在 `scripts/` 内共 10 处：`audit.py:422`、`:2089`、`:2278`、`:2468`、`:2476`、`:2512`，`prepare_review_workspace.py:488`、`:490`、`:708`、`:879`。
- `references/` 32 个文件中 8 个含中文/Chinese/GB-T 提及，合计 14 处；`agents/` 19 个 Markdown 中 2 个含 3 处提及；`templates/` 6 个文件 0 处。
- 因此按语言拆成两个 skill 会复制约 95% 的代码与文档以分离约 20 行调度逻辑，并额外制造 `--lang` 语义断裂与触发歧义。本任务不采用该方案。

### 缺陷一：`gbt7714` 是死条目

- `ZH_EXTRA_CHECKS: list[str] = ["consistency", "gbt7714"]`（`audit.py:301`），在 `lang == "zh"` 时追加到检查列表（`audit.py:2477`）。
- `_resolve_script` 的 `script_map`（`audit.py:381`-`:396`）没有 `gbt7714` 键，函数返回 `None`（`audit.py:399`-`:400`）。
- 结果：每次中文审计都打印 `[audit] SKIP gbt7714: script not found`（`audit.py:2489`），GB/T 7714-2015 检查从未执行。`CHECKLIST.md:132` 与 `VENUE_RULES.md:12` 都把该标准列为中文学位论文要求。

### 缺陷二：4 项检查在中文论文上回退到英文脚本

`lang == "zh"` 时候选目录为 `[SCRIPTS_ZH, SCRIPTS_EN]`（`audit.py:423`），`latex-thesis-zh/scripts/` 缺少对应文件时静默回退到英文副本。实测解析矩阵：

| check | zh(.tex) 实际解析到 | 说明 |
|---|---|---|
| `format` / `logic` / `experiment` / `deai` / `bib` | `latex-thesis-zh` | 正确 |
| `consistency` | `latex-thesis-zh` | 正确 |
| `citations` / `references` / `visual` / `presubmission` | `paper-audit` | 自有，语言无关 |
| `grammar` → `analyze_grammar.py` | `latex-paper-en` | 英文脚本跑中文正文 |
| `sentences` → `analyze_sentences.py` | `latex-paper-en` | 英文脚本跑中文正文 |
| `figures` → `check_figures.py` | `latex-paper-en` | 语言中性，有意复用 |
| `pseudocode` → `check_pseudocode.py` | `latex-paper-en` | **非语言中性**，见下 |

`check_pseudocode.py` 的语言依赖（TPR-05，取代此前"英文词表命中数为 0"的错误取证——该取证用了大小写敏感的小写 `\bthe\b` 模式，漏掉了首字母大写冠词与 ASCII 词计数器）：

- `_count_words` 是 `len(re.findall(r"[A-Za-z0-9_+-]+", text))`，对纯中文注释恒返回 0，`> 12` 的长注释阈值永不触发。
- `re.match(r"^(?:The|A|An)\b", caption)` 检测英文冠词开头的 caption。
- `:194`-`:195` 要求字面量 `"Input:"` / `"Output:"`（或 `\Require` / `\Ensure` / `\KwIn` / `\KwOut`）。

因此中文伪代码检查不是"降级 IEEE 严格度"能解决的，需要独立的中文本地化设计。本任务改为在 zh 下**抑制** `pseudocode`，本地化另立任务。

- `latex-thesis-zh/scripts/check_style_zh.py`（23.9 KB，docstring 标注"中文学位论文版本"，CLI 有 `--section` / `--json`）是词级/句级中文检查器，当前没有任何 `script_map` 键指向它。

### 缺陷三：9 个 zh 专属检查器审稿链路完全触达不到

`latex-thesis-zh/scripts/` 中以下脚本不在 `script_map` 任何值内，`paper-audit` 无法调度（均已确认具备 `--json` 或等效只读 CLI）：

| 脚本 | 体量 | 覆盖维度 |
|---|---|---|
| `check_spec.py` | 37.9 KB | 学校规范终检清单（`--bib` / `--year` / `--json`） |
| `blind_review.py` | 33.3 KB | 盲审可识别信息定位（`--check` 为只读模式） |
| `check_style_zh.py` | 23.9 KB | 中文词级/句级风格 |
| `analyze_abstract.py` | 47.1 KB | 摘要结构 T-* |
| `analyze_conclusion.py` | 31.8 KB | 结论章 CC-* |
| `analyze_literature.py` | 24.0 KB | 文献综述（`--bib`） |
| `check_tables.py` | 17.7 KB | 三线表合规 |
| `optimize_title.py` | 19.8 KB | 标题（优化取向，审稿适配性待判定） |
| `map_structure.py` | 10.4 KB | 结构映射（工具性，审稿适配性待判定） |

- `blind_review.py` 的写回触发分支是 `if args.generate:`（`latex-thesis-zh/scripts/blind_review.py:794`），不是 `--author` / `--supervisor` / `--suffix` / `--force`——后两组中 `--author` 与 `--supervisor` 是只读扫描输入，缺失时反而会跳过部分姓名检测。`paper-audit` 的红线是"不改写论文源文件"（`SKILL.md:61`），因此契约是**绝不传 `--generate`**（TPR-09）。

### 缺陷四：模式差异化没有运行时入口

按模式分配 zh 附加检查在当前运行时结构下不可实现（TPR-01）：

| 真实入口 | 传给 `run_audit` 的 mode |
|---|---|
| `main()` else 分支（`audit.py:3225`） | `args.mode`（唯一透传处） |
| `run_audit:2441` → `run_deep_review` → `run_audit`（`:1737`） | 硬编码 `"quick-audit"` |
| `main()` re-audit 分支 → `run_reaudit` → `run_audit`（`:2963`） | 硬编码 `"quick-audit"` |
| `run_audit:2431` → `run_polish_precheck` | 早退，不进 `run_audit` 检查循环 |

- 把 `:1737` 改成 `mode="deep-review"` 会与 `:2441` 的委派形成无限递归，不可行。
- `run_polish_precheck`（`:2254`）在统一分流前早退，直接 `_resolve_script("logic", ...)` 与 `_resolve_script("sentences", ...)`（`:2298`、`:2317` 附近），完全不读 `MODE_CHECKS` / `ZH_EXTRA_CHECKS`。因此在 zh 下抑制 `sentences` 会让中文 polish 丢掉表达检查，而不会自动换成 `check_style_zh.py`。
- 格式面：`.typ` 分支独占 `SCRIPTS_TYPST`（`audit.py:420`-`:421`），加进 `SCRIPTS_ZH` 的 LaTeX 检查器对 Typst 不可达；`.pdf` 已有一条按检查名的跳过清单（`audit.py:2492` 附近），新增的 zh 检查器都要 TeX 源，必须进该清单。

### 缺陷五：新检查模块不进评分路径

- `scholar_eval.MODULE_DIMENSION_MAP`（`scripts/scholar_eval.py:65`）共 14 个键，不含 `SPEC` / `BLIND` / `ABSTRACT` / `CONCLUSION` / `LITERATURE` / `TABLES`。
- `_parse_script_output` 用 `check_name.upper()` 作为 module 名（`audit.py:465` 及其调用处），因此新检查键会产出未映射模块。
- 边界规范的错误矩阵写明：`Unknown audit module | Ignore for script score; mapping guard test signals new modules`（`.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md:53`）。
- 该 guard 是一处**精确相等锁**：`tests/skills/paper_audit/test_literature_search.py:578` 断言 `MODULE_DIMENSION_MAP == {...}`。扩展映射必须同步改这条断言（TPR-06）。

### 缺陷六：`VENUE_CONFIGS` 符号不存在

- 真实符号是单数 `VENUE_CONFIG: dict[str, dict]`（`audit.py:305`），消费点在 `audit.py:2144`-`:2145`。规划此前统一写作 `VENUE_CONFIGS`，是符号名错误（TPR-04）。
- `required_sections` 只出现在三处配置定义（`audit.py:308`、`:334`、`:351`），仓库内没有任何运行时消费者。`thesis-zh` 当前也没有该字段。
- `extra_checks` 的消费点在 `audit.py:2213`-`:2221`：正则未命中即生成 `ChecklistItem(label, found=False, "Not found — required for {VENUE} submission")`。因此放进 `extra_checks` 的项会被标注为该 venue 的**必需项**。
- 模板证据表明附录与符号表对中文学位论文并非必需：`latex-thesis-zh/templates/yanshan.md:52`-`:53` 把"物理量名称及符号表"与"附录"标为"（可省）"；`templates/pkuthss.md:25`、`:73`、`:106` 把"主要符号对照表"标为"条件项、非必备章节"。把它们写进 `extra_checks` 会对合法论文产生必需项失败（TPR-03）。
- `latex-thesis-zh/scripts/check_consistency.py` 的状态只有 `PASS` / `WARNING`（`:237`、`:304`），不产生确定性阻断项，不具备 gate 资格（TPR-03）。

### 缺陷七：GB/T 7714 检查因输入与开关双重缺失而不可达

- GB/T 7714 的实际实现在 `latex-thesis-zh/scripts/verify_bib.py`：`GB_STANDARDS = {"gb7714", "gb7714-2025"}`（`:49`），增量检查段落在 `:258`，必填字段表在 `:36`，全部只在 `--standard gb7714` / `gb7714-2025` 下生效。
- `audit.py` 调度 `bib` 检查时只在 `online` 为真时追加 `--online` / `--email`（`audit.py:2506`-`:2509`），从不传 `--standard`。默认标准不是 GB 系列，因此增量检查始终关闭。
- `verify_bib.py` 的位置参数是 `bib_file`（`latex-thesis-zh/scripts/verify_bib.py:459`），而 `_run_check_script` 传入的是论文路径（`audit.py:446`、`:2511`）。实测：对 `.tex` 输入，EN 与 ZH 两个副本都返回 `Status: PASS` / `Total entries: 0`，rc=0。`bib` 检查在当前调度下是空通过，两种语言都受影响。
- `audit.py:62` 已有 `_load_bibliography_content(path, content, fmt)` 解析 `.bib`，但只被 ScholarEval 链路使用（`audit.py:2592`），`bib` 检查未复用。
- Typst 侧没有该开关：`typst-paper/scripts/verify_bib.py` 只有 `--style`（3 处命中，取值形如 `gb-7714-2015-numeric`），没有 `--standard`。GB/T 7714 路径只适用于 `.tex`（TPR-02）。
- 附带确认：`references` 检查解析到 `paper-audit/scripts/check_references.py`，它是图表/公式引用完整性检查器（router 版），与参考文献格式无关，语言中性。

### 缺陷八：中文学位论文审阅准则缺位
- `VENUE_RULES.md:12` 对 `thesis-zh` 只有一行：`GB/T 7714-2015 bibliography, bilingual abstract, university template`。
- `VENUE_CONFIG["thesis-zh"]`（`audit.py:359`-`:367`）只有 3 条 `extra_checks` 正则（双语摘要、原创性声明、致谢），无 `page_limit`、无 `required_sections`、`blind_review: False`。
- `CHECKLIST.md:130`-`:141` 的 Chinese Thesis 节共 9 项，全部是机械格式项，不含工作量、创新性、章节完备性、答辩关注点等评阅维度。
- `agents/` 19 个 reviewer agent 全部面向期刊/会议评审语境，无学位论文评阅人 persona。
- `SKILL.md:68` 明确把中文学位论文的方法叙述排除在自动审计链之外，要求走 `latex-thesis-zh --method-narrative --section`。该边界是既有决策，本任务不改动。

### 约束面

- `SKILL.md` 版本须与 `pyproject.toml` 全仓一致；单 skill 任务只改 `last_updated`，不 bump `version`（`tests/contracts/test_skill_versions.py`）。
- 新增/修改 `references/` 或 Markdown `agents/` 必须同步 `docs/resource-manifest.json` 的 `sourceSha256` 与 EN/ZH 两个目标页面（`.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`）。paper-audit 当前有 58 条 manifest 条目。
- `paper-audit` severity 与 ScholarEval 模块映射受 `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md` 约束；其模块映射由 `tests/skills/paper_audit/test_literature_search.py:578` 的精确相等断言锁定。
- ScholarEval 的评分维度有三个不同集合，不可混用（TPR-10）：**运行时基础评分维度 8 个**（`scripts/scoring_model.py:39`-`:47` 的 `soundness` / `clarity` / `presentation` / `novelty` / `significance` / `reproducibility` / `ethics` / `literature_grounding`）、**派生总分 1 个**（`overall_base`，由前 8 维计算，`:112` 处按 `dim == "overall"` 特判；`FEATURE_NAMES` 的 `# 9 base dimensions` 注释把派生项算进基础维度，是注释本身不准）、**中文审阅指标行**（C2 新建的参考表行，数量以 C2 design §1 表为准，不是评分维度）。
- `tests/skills/paper_audit/` 现有 6303 行、16 个文件；`tests/contracts/` 有 10 个文件引用 paper-audit。
- 已确定会被本任务破坏、必须同步迁移的既有测试：`tests/skills/paper_audit/test_paper_audit.py:419`-`:422` 的 `test_zh_extra_checks` 直接 `from audit import ZH_EXTRA_CHECKS` 并断言 `"consistency" in ZH_EXTRA_CHECKS`（TPR-11）。

## Requirements

1. 不新增 skill、不拆分 `paper-audit`、不改动 skill 触发边界与 `description`。
2. 中文学位论文审阅能力沿 `lang == "zh"` 与 `--venue thesis-zh` 两个既有轴扩充，不引入第三个语言开关。
3. 消除静默失败：任何声明的检查项要么解析到真实脚本，要么从声明中移除。不保留只打印 SKIP 的死条目。
4. 消除无声语言回退：`lang == "zh"` 下每个使用英文脚本的检查项都必须有显式判定结果（保留 / 替换为 zh 脚本 / 跳过），判定依据写入设计文档，并在运行日志中可区分"有意复用"与"回退"。
5. 新接通的 zh 检查器必须是只读的。真正的写回触发参数是 `blind_review.py` 的 `--generate`（`latex-thesis-zh/scripts/blind_review.py:794`），调度链路绝不得传它；`--author` / `--supervisor` 是只读扫描输入，可按可用元数据决定是否传（TPR-09）。
6. 检查项的模式差异化必须建立在**真实运行时入口**上。`run_deep_review`（`audit.py:1737`）与 `run_reaudit`（`audit.py:2963`）都硬编码 `mode="quick-audit"` 回调 `run_audit`，且 `run_audit:2441` 在 `deep-review` 时委派给 `run_deep_review`（改成传 `deep-review` 会无限递归）；`run_polish_precheck`（`audit.py:2431`）在统一分流前早退，直接 `_resolve_script` 取 `logic` / `sentences`，完全不经过 `MODE_CHECKS`。因此本任务**不按模式差异化 zh 附加检查集合**；阻断资格改由独立的 `gateEligible` 规则控制（TPR-01、TPR-03）。
7. `gate` 只接纳同时满足三条的检查：有明确规范依据、对当前模板必需、可确定检测。只产 PASS/WARNING 的检查器与可选章节不得进入 gate（TPR-03）。
8. 新增中文学位论文审阅准则文档与 reviewer agent，覆盖盲审、规范终检、结构完备性、工作量与创新性、摘要/结论/综述质量等学位论文特有维度。
9. 保持 `[Script]` / `[LLM]` 来源标签、issue JSON schema、severity 档位与 ScholarEval 的 8 个基础维度及权重不变。**允许**为新增检查模块扩展 `scholar_eval.MODULE_DIMENSION_MAP` 并同步更新其精确相等锁 `tests/skills/paper_audit/test_literature_search.py:578` 与边界规范——新模块若不入映射会被评分路径静默忽略（TPR-06）。
10. 不改动 `SKILL.md:68` 声明的方法叙述边界（中文方法章叙述仍在 `latex-thesis-zh` 显式工作流中）。
11. 不新增第三方依赖。
12. 中文伪代码检查本期不做。`latex-paper-en/scripts/check_pseudocode.py` 不是语言中性的（`_count_words` 用 `[A-Za-z0-9_+-]+` 只数 ASCII 词、`re.match(r"^(?:The|A|An)\b", caption)` 查英文冠词、`:194`-`:195` 要求字面量 `Input:` / `Output:`），中文本地化需要独立定义标记、度量与中英混排策略，属另立任务（TPR-05）。

## Acceptance Criteria

每条 AC 后括注对应的 R 条与落地机制所在的 design 小节。

- [ ] AC1（R3、R4 / C1 design §4）：`gbt7714` 死条目消除，且 GB/T 7714 检查真正执行。验收方式：中文论文审计 stdout 中不再出现 `SKIP gbt7714`；`bib` 检查接收到解析后的 `.bib` 路径而非论文路径；`.tex` 输入且 `lang == "zh"` 或 `--venue thesis-zh` 时传入 `--standard gb7714`；有测试断言在给定 `.bib` fixture 下 `Total entries` 大于 0 且 GB 增量检查项出现在输出中。`.typ` 输入不适用——`typst-paper/scripts/verify_bib.py` 只有 `--style gb-7714-2015-numeric`，没有 `--standard`（TPR-02）。
- [ ] AC2（R4、R12 / C1 design §1、§2、§3）：存在一份**可达性矩阵**测试，维度为 `真实入口 × lang × fmt × 检查键`，真实入口取 `main→run_audit`、`run_audit→run_deep_review→run_audit`、`run_reaudit→run_audit`、`run_audit→run_polish_precheck` 四条。矩阵逐单元断言解析归属（`audit` / `zh` / `en` / `typst` / 抑制 / 跳过），期望值与 C1 design §1 的判定表一致。`grammar`、`sentences`、`figures`、`pseudocode` 四项在 zh 下的结果必须与判定表逐项相符，其中 `pseudocode` 为抑制（TPR-01、TPR-05）。
- [ ] AC3（R4、R9 / C1 design §5、§8）：`check_spec.py`、`blind_review.py`、`check_style_zh.py`、`analyze_abstract.py`、`analyze_conclusion.py`、`analyze_literature.py`、`check_tables.py` 七项中，design 判定为接通的项目均可从 `audit.py` 调度，其输出经**逐脚本 adapter** 解析为 `AuditIssue` 并带 `[Script]` 来源标签。每个 adapter 至少有真实样例、未知参数（argparse 退出码 2）、非零退出、空输出、非法 JSON 五类回归测试。判定为不接通的项目在 design 中有书面理由（TPR-02）。
- [ ] AC4（R5、R7 / C1 design §5、§7）：`paper-audit` 调度链路中不存在会修改论文源文件的脚本调用。测试断言：`blind_review.py` 的调用参数**不含 `--generate`**；只读运行前后 fixture 文件的 sha256 与 mtime 不变；`gate` 的 zh 阻断候选集只含通过 `gateEligible` 三条判据的项，不含 `consistency`（只产 PASS/WARNING）与任何模板标注为可选的章节存在性检查（TPR-03、TPR-09）。
- [ ] AC5（R8、R9 / C2 design §3、§6、§7）：新增 `references/ZH_THESIS_REVIEW_CRITERIA.md` 与 `agents/zh_thesis_reviewer_agent.md`。登记面按类型分开：参考文件登记进 `SKILL.md ## References` 与 `docs/resource-manifest.json`；agent 登记进 `SKILL.md ## Reviewer Lanes` 与 `references/agent-roster.md`。**参考文件不进 agent roster**。新 lane 的选择条件、任务模板、输入/输出、fallback、checkpoint 与汇总字段贯穿 `REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、`MODE_GUIDE.md` Phase 3B 与 `audit.py` 的 lane 接线（TPR-07）。新增检查模块已进 `MODULE_DIMENSION_MAP` 且其相等锁测试同步更新（TPR-06）。
- [ ] AC6（R8 / C2 design §4、§5）：`VENUE_CONFIG["thesis-zh"]`（**单数**，`audit.py:305`、消费点 `:2144`）的 `extra_checks`、`VENUE_RULES.md` thesis-zh 小节、`CHECKLIST.md` Chinese Thesis 节三者建立**有方向的覆盖关系**：每个 `TZ-EC-*` 正则项必须在 `CHECKLIST.md` 有对应 `TZ-CL-*` 条目并在 `VENUE_RULES.md` 有依据说明（EC ⊆ CL）；反向不要求，`CHECKLIST.md` 可含纯人工项。**不是集合相等**。`required_sections` 无运行时消费者（仅出现在 `audit.py:308`、`:334`、`:351` 三处配置定义），本任务不为 `thesis-zh` 添加该字段，也不纳入 AC6（TPR-04）。
- [ ] AC7（R11 / C2 implement 阶段 D）：`SKILL.md` 的 `version` 字段未变、`last_updated` 已更新；`just ci` 全绿，测试数不低于开工时实测基线。
- [ ] AC8（R4、R8 / C1 implement 阶段 C fixture manifest）：按 fixture manifest 逐行验收，不用单一 fixture 承担全部断言。每个嵌入缺陷有精确片段、所属脚本、预期 module / severity / gate 状态、适用模式与格式，并配一个不应触发该缺陷的负例。四条真实入口各有结构化断言（TPR-08）。

## 任务地图

| 子任务 | 目录 | 交付物 | 主要文件 |
|---|---|---|---|
| C1 zh 检查调度修复与专属检查器接通 | `.trellis/tasks/08-30-zh-dispatch-wiring` | AC1–AC4 | `scripts/audit.py`（`script_map`、`ZH_EXTRA_CHECKS`、`_resolve_script`、adapter registry、退出码处理、`run_polish_precheck`）、`scripts/scholar_eval.py`（`MODULE_DIMENSION_MAP`）、`tests/skills/paper_audit/` |
| C2 中文审阅准则文档与 reviewer agent | `.trellis/tasks/08-30-zh-review-criteria` | AC5–AC6 | `references/ZH_THESIS_REVIEW_CRITERIA.md`、`agents/zh_thesis_reviewer_agent.md`、`references/REVIEW_LANE_GUIDE.md`、`references/SUBAGENT_TEMPLATES.md`、`references/MODE_GUIDE.md`、`VENUE_CONFIG["thesis-zh"]`、`CHECKLIST.md`、`VENUE_RULES.md`、`SKILL.md`、`docs/resource-manifest.json` |

执行顺序：**C1 → C2**。两者都会改 `audit.py`，C1 改调度结构（`script_map` / `_resolve_script` / adapter / 退出码 / polish 替换点），C2 改 `VENUE_CONFIG["thesis-zh"]` 数据与 lane 接线。串行执行避免同文件冲突，且 C2 的准则文档需要引用 C1 落定的检查器清单与模块映射。

AC7、AC8 是跨子任务验收，由父任务在两个子任务完成后统一执行。

## Notes

- 本任务的起点是用户提出的"按 en / zh 拆成两个 skill"。可行性分析（见 Confirmed Facts 第一节）表明语言不是 `paper-audit` 的主要变化轴，拆分收益为负。用户确认真实诉求是**区分中文大论文与英文小论文**，方向改为沿 venue/profile 轴扩充。该判定已固化，不重开。
- 另一项已识别但不在本任务范围内的问题：`audit.py` 3292 行 / 124 KB 单文件，模式调度、检查执行、清单、报告导出混在一起。合理的拆分轴是模式或分层，与本任务正交，另立任务处理。
- 范围说明：修复 `bib` 检查的输入路径（缺陷七）会同时修正英文论文侧的空通过，因为两种语言共用 `audit.py:2511` 这一行调度代码。这不是范围扩张，是同一处缺陷的完整修复。修复后英文侧 `bib` 检查会首次产出真实 finding，可能使既有 EN 相关测试的期望值需要更新——这是预期结果，不是回归。
- 范围外后续项（本任务不做，各自另立）：
  1. `audit.py` 3292 行单文件解构（见上条）。
  2. **中文伪代码检查本地化**：需定义中文 Input/Output 标记、非 ASCII 长度度量、冠词规则豁免、`--venue` 传参与中英混排策略，并用中文正反例验证。本任务在 zh 下抑制 `pseudocode`（TPR-05）。
  3. **模式差异化的 zh 检查集合**：需先修 `run_deep_review` / `run_reaudit` 的 mode 传播（`audit.py:1737`、`:2963`）且不引入 `:2441` 的递归。本任务不做，改用 `gateEligible` 规则控制阻断资格（TPR-01）。
  4. **`required_sections` 接线**：该字段无运行时消费者，本任务不为 `thesis-zh` 添加，也不测试死配置（TPR-04）。
- 审阅状态：本规划已按 `.trellis/reviews/08-30-paper-audit-zh-profile.md`（阻断 8 / 应修 4 / 提示 1）修订。该报告是待分诊列表，不构成批准；修订后仍需复审再进入实现。报告的 4 条 UNVERIFIED（GB/T 7714 规则本身、中文正则召回率与误报率、新 agent 的审阅质量、`just ci` 与端到端矩阵）保持未核实状态，应在实现后补证。
