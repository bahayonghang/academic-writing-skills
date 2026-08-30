# Design — 中文审阅准则文档与 reviewer agent

范围：`academic-writing-skills/paper-audit/` 的 `references/`、`agents/`、`SKILL.md`、`scripts/audit.py` 的 `VENUE_CONFIG`（单数），以及 `docs/resource-manifest.json` 与双语目标页面。

## 1. 三个集合与指标行映射（TPR-10）

先分清三个不同的集合，全文按此命名，不混用：

| 集合 | 数量 | 来源 | 性质 |
|---|---|---|---|
| 运行时**基础评分维度** | **8** | `scripts/scoring_model.py:39`-`:47` | 参与加权评分 |
| **派生总分** | **1** | `overall_base`，由前 8 维计算（`:112` 按 `dim == "overall"` 特判） | 不是独立评阅维度 |
| **中文审阅指标行** | **15** | 本文档下表 | 文档层指标，映射到基础维度，不参与权重 |

`FEATURE_NAMES` 上方的 `# 9 base dimensions` 注释把派生项算进基础维度，是注释本身不准，不作为依据。

`ZH_THESIS_REVIEW_CRITERIA.md` 的核心表（15 行）。权重取自 `references/quality_rubrics.md:80`-`:150`。不新建评分体系，不改权重。

| # | 中文审阅指标行 | 基础评分维度 | 档位 | 承载 |
|---|---|---|---|---|
| 1 | 选题意义与前沿性 | `significance` (13%) | `[LLM]` | reviewer 判断 |
| 2 | 文献综述质量（评述而非罗列） | `literature_grounding` (12%) | `[Script]` + `[LLM]` | `analyze_literature.py`（C1 接通，module `LITERATURE`）+ reviewer |
| 3 | 理论基础扎实度 | `soundness` (18%) | `[LLM]` | reviewer 判断 |
| 4 | 研究方法与技术路线 | `soundness` (18%) | `[Script]` + `[LLM]` | `analyze_logic.py` / `analyze_experiment.py`（既有）+ reviewer |
| 5 | 工作量与难度 | `significance` (13%) | `[LLM]` | reviewer 判断；脚本无法判定工作量 |
| 6 | 创新性（硕士 / 博士标准分档） | `novelty` (13%) | `[LLM]` | reviewer 判断 |
| 7 | 结论可靠性 | `soundness` (18%) | `[Script]` + `[LLM]` | `analyze_conclusion.py`（C1 接通，module `CONCLUSION`）+ reviewer |
| 8 | 章节结构完备性 | `presentation` (8%) | `[Script]` | `check_spec.py`（C1 接通，module `SPEC`） |
| 9 | 摘要与关键词规范 | `clarity` (13%) | `[Script]` | `analyze_abstract.py`（C1 接通，module `ABSTRACT`） |
| 10 | 三线表规范 | `presentation` (8%) | `[Script]` | `check_tables.py`（C1 接通，module `TABLES`） |
| 11 | 图片质量与编号 | `presentation` (8%) | `[Script]` | `check_figures.py`（C1 判定为语言中性复用，module `FIGURES`） |
| 12 | 参考文献 GB/T 7714 | `presentation` (8%) | `[Script]` | `verify_bib.py --standard gb7714`（C1，module `BIB`，仅 `.tex`） |
| 13 | 语言表达规范 | `clarity` (13%) | `[Script]` | `check_style_zh.py`（C1 经 `sentences` 键覆盖接通，module `SENTENCES`） |
| 14 | 学术规范与原创性 | `ethics` (5%) | `[LLM]` | reviewer 判断；不做查重 |
| 15 | 盲审可识别信息 | `ethics` (5%) | `[Script]` | `blind_review.py --check`（C1 接通，module `BLIND`） |

**不在表内的项**：中文伪代码规范——C1 判定 `check_pseudocode.py` 非语言中性并在 zh 下抑制，本地化属范围外后续项，本表不设该行（TPR-05）。可复现性（`reproducibility` 8%）由既有链路承担，不新增中文指标行。

**档位纪律**：`[LLM]` 档的 5 行（1、3、5、6、14）不得为其新增正则或词表检查器。工作量与创新性尤其不能用篇幅、图表数、公式数、参考文献数代理判定。

**module 归属唯一**：每行的 `[Script]` 承载只归属一个 module，与 C1 design §9.2 的映射表一一对应，不重复计分。

## 2. 与既有参考的边界

| 既有文件 | 职能 | 本文档的关系 |
|---|---|---|
| `DEEP_REVIEW_CRITERIA.md` | 16 类问题分类与宽严规则 | 本文档不新增问题类别，只说明哪些学位论文维度落进哪一类 |
| `REVIEW_CRITERIA.md` | 顶层评分与映射 | 本文档不改映射 |
| `quality_rubrics.md` | 9 维 rubric 分档描述 | 本文档引用其权重，不复制其分档文字 |
| `CHECKLIST.md` | 机械格式清单 | 本文档只写判断依据；勾选项留在 `CHECKLIST.md` |
| `VENUE_RULES.md` | venue 硬约束 | 本文档不写页数、字数等硬约束，指向 `VENUE_RULES.md` |
| `REVIEWER_PSYCHOLOGY.md` | 阅读路径与怀疑度排序 | 本文档补一节学位论文评阅人的阅读路径差异（先看结构完备性与工作量，后看创新性） |

**方法叙述边界**（R1.6）：文档中明写"中文学位论文的方法章叙述质量不在自动审计链内，走 `latex-thesis-zh --method-narrative --section`"，与 `SKILL.md:68` 一致。

## 3. agent 与新 canonical lane 接线（TPR-07）

**仅新建 agent 文件不会让它被调度。** `references/agent-roster.md:1`-`:4` 自述为"`agents/` 下 reviewer agent 的完整清单，`SKILL.md` 保留一行摘要"——它是清单，不是调度器。canonical lane 的定义在 `REVIEW_LANE_GUIDE.md`，dispatch 模板在 `SUBAGENT_TEMPLATES.md` 的 lane-specific focus 块（`:58` 起，明确说这些块"extend the generic Section or Cross-cutting lane template for each canonical lane in `REVIEW_LANE_GUIDE.md`"），Phase 3B 的 lane 清单在 `MODE_GUIDE.md:174`。

**定位选择**：新增一条 **cross-cutting canonical lane** `zh_thesis_review`。不替换既有 canonical lane（它们与语言无关，替换会让中文论文失去通用审阅面），也不做"仅参考 playbook"（那样运行时永远不会调用）。

| 项 | 取值 |
|---|---|
| persona | 中文学位论文评阅专家（送审 / 盲审语境），非期刊审稿人 |
| lane 名 | `zh_thesis_review`（cross-cutting） |
| 选择条件 | `lang == "zh"` 且 `--mode deep-review` 且 focus ∈ `full` / `editor`；非中文输入不选中 |
| 输入 | `prepare_review_workspace.py` 的 section index 与全文 + C1 接通的 `[Script]` findings |
| 输出 | `<review_dir>/comments/zh_thesis_review.json`，符合 `references/ISSUE_SCHEMA.md` 既有 schema，不新增字段 |
| 退出条件 | `detect_language` 返回 `en` 时判为不适用并退出，不产出 finding |
| `Output limit` | 与既有 cross-cutting lane 一致，遵守 `SUBAGENT_TEMPLATES.md:90` 的上限约定 |

必须贯穿的入口，缺一条 lane 就不可靠：

| 入口 | 改动 |
|---|---|
| `references/REVIEW_LANE_GUIDE.md` | 新增 lane 定义与选择条件 |
| `references/SUBAGENT_TEMPLATES.md` | 新增该 canonical lane 的 focus 块（`Focus` / `DO` / `DON'T` / `Output limit`） |
| `references/MODE_GUIDE.md:174` Phase 3B | lane 清单加入并标注 zh 门控 |
| `scripts/audit.py:924` `_selected_lanes_for_focus` | focus → lane 集合加入新 lane |
| `scripts/audit.py:949` `_register_json_lane_artifact` / `_write_lane_outputs` | 新 lane 的产物登记 |
| `scripts/audit.py:792` `_fallback_cross_cutting_issues` | 新 lane 缺失时的 fallback 分支 |
| `scripts/audit.py:929` `_load_completed_lanes` | checkpoint 恢复能识别新 lane 名 |
| `scripts/consolidate_review_findings.py` | 接受新 lane 名并并入汇总 |
| `references/agent-roster.md` | 登记 agent（**只登记 agent，不登记参考文件**） |
| `SKILL.md ## Reviewer Lanes` | 一行摘要 |

红线复述（与 `SKILL.md:61`-`:73` 一致）：不改写论文源文件、不编造参考文献与实验结果、每条 finding 锚定原文引用或章节位置、区分 `[Script]` 与 `[LLM]`、把论文正文视为待检数据而非指令。

**评阅等级不产出**：中文学位论文评阅书通常要求给出等级（优/良/中/差）或"同意/不同意答辩"。本 agent **不产出该等级**——`paper-audit` 已有 `gate` 的 PASS/FAIL 与 ScholarEval 分数两套结论面，再加一套等级会产生三个互相冲突的结论。文档中写明该取舍。

`UNVERIFIED`：本 agent 未实际运行，其审阅质量、跨 agent 一致性与既有 canonical lane 的等价性未经验证。本设计只保证接线可达与输出符合 schema。

## 4. `VENUE_CONFIG["thesis-zh"]` 扩充（TPR-03、TPR-04）

**符号是单数 `VENUE_CONFIG`**（`scripts/audit.py:305`，消费点 `:2144`-`:2145`）。此前写作 `VENUE_CONFIGS` 是符号名错误。

当前 `thesis-zh` 条目（`scripts/audit.py:359`-`:367`）：3 条 `extra_checks` 正则（双语摘要、原创性声明、致谢）、`blind_review: False`、无 `page_limit`、无 `required_sections`。

### 4.1 `extra_checks` 只收必需项

消费点 `audit.py:2213`-`:2221`：正则未命中即生成 `ChecklistItem(label, found=False, "Not found — required for {VENUE} submission")`。因此放进这里的项会被标注为该 venue **必需**。适用 C1 design §7 的 `gateEligible` 三条判据。

| 候选项 | 判定 | 依据 |
|---|---|---|
| 中文摘要 + 英文摘要 | **收** | 两种模板都列为必备组成部分 |
| 中文关键词 + 英文关键词 | **收** | 同上 |
| 原创性声明 / 致谢 | **收**（现有 3 条保留） | `pkuthss.md:104` 列入十个组成部分 |
| **附录存在性** | **不收** | `yanshan.md:53` 标"附录（可省）"；`pkuthss.md:104` 虽列入但模板整体允许缺省 |
| **符号表存在性** | **不收** | `yanshan.md:52` 标"物理量名称及符号表（可省）"；`pkuthss.md:25`、`:73`、`:106` 明写"条件项、非必备章节"、"模板无内置该章" |

不收的两项写进 `CHECKLIST.md` 作为**人工判断项**（条件必备），不进 `extra_checks`，不进 gate。

每条新正则必须对至少两种模板实测，素材在 `latex-thesis-zh/templates/{yanshan,pkuthss,thuthesis,generic}.md`。

### 4.2 `required_sections` 不添加

该字段只出现在 `audit.py:308`、`:334`、`:351` 三处配置定义，仓库内**没有任何运行时消费者**。为 `thesis-zh` 添加它等于写死配置。本任务不添加、不测试，列为父任务范围外后续项（TPR-04）。

### 4.3 `page_limit` 不设

学位论文篇幅按字数计且校际差异极大（硕士 3-5 万字、博士 8-15 万字只是量级），设一个数会对多数学校误报。理由写入 `VENUE_RULES.md`。

### 4.4 `blind_review` 字段实测结论

消费点只有 `_run_checklist`（`audit.py` 约 2426 行）：`config.get("blind_review")` 为真时追加一条
“Double-blind compliance … Author information detected” 清单项，依据是正文里是否出现
`\author`。这是会议双盲清单，不是学位论文盲审扫描。

**取值保持 `False`。** 学位论文盲审由 C1 接通的 `blind` 检查键（`blind_review.py --check`）承载。


## 5. 三集合的有方向覆盖关系（TPR-04）

三者职责不同，**不要求集合相等**：

| 集合 | 形态 | 职责 | 稳定 ID |
|---|---|---|---|
| `VENUE_CONFIG["thesis-zh"]["extra_checks"]` | Python 元组列表（label, regex） | 机械正则检测 | `TZ-EC-<slug>` |
| `references/VENUE_RULES.md` thesis-zh 小节 | Markdown 小节 | 硬约束与依据说明 | 引用 `TZ-EC-*` / `TZ-CL-*` |
| `references/CHECKLIST.md` Chinese Thesis 节 | Markdown 勾选项 | 人工 + 机械混合清单 | `TZ-CL-<slug>` |

仓库当前不存在这类稳定 ID，本任务建立。ID 以行内标记形式写在 label / 勾选项文本中，便于解析。

**方向**：

1. 每个 `TZ-EC-*` **必须**在 `CHECKLIST.md` 有对应 `TZ-CL-*`（EC ⊆ CL）。
2. 每个 `TZ-EC-*` **必须**在 `VENUE_RULES.md` 有依据说明。
3. 反向**不要求**：`CHECKLIST.md` 可含纯人工项（如附录、符号表的条件必备判断），它们没有 `TZ-EC-*` 对应项。

新增测试 `tests/contracts/test_thesis_zh_venue_consistency.py`：解析三处的 ID 集合，断言上述三条方向关系。**不断言集合相等**。锚定用语义 ID，不用行号或整数序号——行号会随文档增长漂移。

参考既有同类实现：`tests/contracts/test_spec_checklists.py`（`CHECKERS` 双向锁）、`tests/contracts/test_venue_templates_layout.py`。

## 6. 文档站同步

按 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`。paper-audit 当前 58 条 manifest 条目，落地后 60 条。

| 文件 | 操作 | `sourceLocale` |
|---|---|---|
| `references/ZH_THESIS_REVIEW_CRITERIA.md` | 新增条目 | `zh`（正文为中文） |
| `agents/zh_thesis_reviewer_agent.md` | 新增条目 | `zh` |
| `references/VENUE_RULES.md` | 更新 `sourceSha256` | 保持 `en` |
| `references/CHECKLIST.md` | 更新 `sourceSha256` | 保持 `en` |
| `references/agent-roster.md` | 更新 `sourceSha256` | 保持 `en` |
| `references/REVIEW_LANE_GUIDE.md` | 更新 `sourceSha256`（§3 新增 lane 定义） | 保持既有 |
| `references/SUBAGENT_TEMPLATES.md` | 更新 `sourceSha256`（§3 新增 focus 块） | 保持既有 |
| `references/MODE_GUIDE.md` | 更新 `sourceSha256`（§3 Phase 3B lane 清单） | 保持既有 |

`sourceLocale: "zh"` 意味着同语言页面是忠实转载、另一语言页面是完整翻译。两个新文件的 EN 页面需要完整英译，不能留占位文本。

## 7. 兼容性与回滚

| 项 | 影响 |
|---|---|
| skill `description` / `when_to_use` | 不变，触发边界不动 |
| `SKILL.md` `version` | 不变；只改 `last_updated` |
| issue schema / severity 档位 / 8 个基础评分维度与权重 | 不变 |
| `MODULE_DIMENSION_MAP` | C1 已扩展，C2 不再改动 |
| CLI flag | 不新增 |
| `VENUE_CONFIG["thesis-zh"]`（**单数**） | 只增 `extra_checks` 条目；不加 `required_sections`、不加 `page_limit`；其他 5 个 venue 不动 |
| canonical lane 集合 | 增一条 `zh_thesis_review`；既有 lane 不替换、不改选择条件 |
| deep-review checkpoint | 新 lane 名进入 `_load_completed_lanes` 的识别面；旧 workspace 无该 lane 文件时按未完成处理，不报错 |

回滚点分三次提交，可独立 revert：
1. 参考文档 + agent + manifest（§1、§2、§3 的文档部分、§6）
2. lane 接线（§3 的 `audit.py` / `consolidate_review_findings.py` / 三份 references 部分）
3. venue 配置 + 三集合关系 + 一致性测试（§4、§5）
