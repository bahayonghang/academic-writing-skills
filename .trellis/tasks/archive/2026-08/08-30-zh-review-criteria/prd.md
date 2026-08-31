# 中文审阅准则文档与 reviewer agent

父任务：`.trellis/tasks/08-30-paper-audit-zh-profile`（需求全集、跨子任务验收在父 `prd.md`）
前置：C1 `.trellis/tasks/08-30-zh-dispatch-wiring` 完成。本子任务的准则文档要引用 C1 落定的检查器清单。

## Goal

补齐 `paper-audit` 缺失的中文学位论文审阅准则：新增一份准则参考文档与一个学位论文评阅人 agent，并在 `VENUE_CONFIG["thesis-zh"]`、`VENUE_RULES.md`、`CHECKLIST.md` 三者之间建立有方向的覆盖关系（不是集合相等，见 design §5）。本子任务只写判断依据与配置，不改调度代码结构（属 C1）。

## Requirements

### R1 审阅准则文档

1. 新增 `references/ZH_THESIS_REVIEW_CRITERIA.md`，覆盖中文学位论文特有的评阅维度：选题意义、文献综述质量、理论基础、研究方法与技术路线、工作量与难度、创新性、结论可靠性、写作规范性、学术规范、盲审可识别信息。
2. **三个集合必须分开命名，不得混用（TPR-10）**：
   - **运行时基础评分维度 = 8 个**：`soundness` / `clarity` / `presentation` / `novelty` / `significance` / `reproducibility` / `ethics` / `literature_grounding`（`scripts/scoring_model.py:39`-`:47`）。
   - **派生总分 = 1 个**：`overall_base`，由前 8 维计算（`:112` 按 `dim == "overall"` 特判）。`FEATURE_NAMES` 上方 `# 9 base dimensions` 的注释把派生项算进基础维度，是注释本身不准，不作为依据。
   - **中文审阅指标行 = 15 行**：C2 新建参考表的行数，见 design §1。它是文档层的指标，不是评分维度。
   每个指标行映射到 8 个基础维度之一，**不新建平行评分体系**，不改权重。
3. 每个指标行必须标明来源档位：`[Script]`（由 C1 接通的检查器承载）或 `[LLM]`（reviewer 判断）。脚本覆盖不到的维度不得伪装成可自动判定。
4. 硕士与博士的创新性、工作量标准差异写为 reviewer 判断依据，不新增 CLI 开关。学位级别在 `latex-thesis-zh` 侧有 `--degree`，`paper-audit` 不复制该轴。
5. 文档必须指明与既有参考的边界，不重复既有内容：`DEEP_REVIEW_CRITERIA.md`（16 类问题分类）、`REVIEW_CRITERIA.md`（顶层评分映射）、`quality_rubrics.md`（9 维 rubric）、`CHECKLIST.md`（机械清单）。
6. 不改动 `SKILL.md:68` 的方法叙述边界。中文方法章叙述仍指向 `latex-thesis-zh --method-narrative --section`，准则文档中明确写出该指路。

### R2 reviewer agent 与 lane 接线

7. 新增 `agents/zh_thesis_reviewer_agent.md`，persona 是中文学位论文评阅专家（送审/盲审语境），不是期刊审稿人。
8. agent 必须遵守既有红线：不改写论文源文件、不编造参考文献与实验结果、每条 finding 锚定原文引用或章节位置、区分 `[Script]` 与 `[LLM]`。
9. **仅登记 agent 文件不足以让它被调度（TPR-07）。** `references/agent-roster.md:1`-`:4` 自述是"agents/ 下 reviewer agent 的清单"，canonical lane 的选择、模板与汇总固化在别处。本任务把该 agent 定位为**新增一条 cross-cutting canonical lane** `zh_thesis_review`，必须贯穿全部规范入口：
   - `references/REVIEW_LANE_GUIDE.md` — lane 定义与选择条件
   - `references/SUBAGENT_TEMPLATES.md` — 该 canonical lane 的 focus 块（含 `Output limit`）
   - `references/MODE_GUIDE.md` Phase 3B — lane 清单与 zh 门控
   - `scripts/audit.py` — `_selected_lanes_for_focus`（`:924`）、lane 输出写入（`_write_lane_outputs`、`_register_json_lane_artifact` `:949`）、cross-cutting fallback（`_fallback_cross_cutting_issues` `:792`）
   - `scripts/consolidate_review_findings.py` — 接受新 lane 名
   - checkpoint：`_load_completed_lanes`（`:929`）按文件名识别 lane，新 lane 名需可被登记与恢复
10. agent 输出必须符合 `references/ISSUE_SCHEMA.md` 的既有 JSON schema，不新增 schema 字段。
11. agent 必须包含把非中文输入判为不适用并退出的条件，避免在英文论文上产出无意义 finding。
12. **登记面按文件类型分开（TPR-07）**：`ZH_THESIS_REVIEW_CRITERIA.md` 是参考文件，登记进 `SKILL.md ## References` 与 `docs/resource-manifest.json`，**不进 `agent-roster.md`**；`zh_thesis_reviewer_agent.md` 是 agent，登记进 `agent-roster.md` 与 `SKILL.md ## Reviewer Lanes`。

### R3 venue 配置与三集合关系

13. 符号是单数 `VENUE_CONFIG`（`scripts/audit.py:305`，消费点 `:2144`-`:2145`）。此前规划写作 `VENUE_CONFIGS` 是符号名错误，全部改正（TPR-04）。
14. 扩充 `VENUE_CONFIG["thesis-zh"]`（`audit.py:359`-`:367`）的 `extra_checks`。当前只有 3 条正则、`blind_review: False`、无 `page_limit`、无 `required_sections`。
15. **`extra_checks` 只接纳必需项（TPR-03）**。其消费点 `audit.py:2213`-`:2221` 对未命中生成 `ChecklistItem(label, found=False, "Not found — required for {VENUE} submission")`，会把项目标注为该 venue 必需。附录与符号表按模板证据是可选/条件项（`latex-thesis-zh/templates/yanshan.md:52`-`:53` 标"（可省）"；`templates/pkuthss.md:25`、`:73`、`:106` 标"条件项、非必备章节"），**不得进 `extra_checks`**。
16. **不为 `thesis-zh` 添加 `required_sections`（TPR-04）**。该字段只出现在 `audit.py:308`、`:334`、`:351` 三处配置定义，仓库内无运行时消费者。不接线也不测试死配置；该项列为父任务的范围外后续项。
17. `blind_review` 字段取值需实测后定：先读 `audit.py` 中该字段的全部消费点，确认它控制"是否检查匿名化"还是别的行为。**不预先假定 `True`**。无论取值如何，盲审能力由 C1 接通的 `blind` 检查键承载。
18. 扩充 `references/VENUE_RULES.md:12`（当前仅一行）为独立小节。
19. 扩充 `references/CHECKLIST.md:130`-`:141` 的 Chinese Thesis 节（当前 9 项全为机械格式项）。
20. **三集合建立有方向的覆盖关系，不是集合相等（TPR-04）**。三者职责不同：`extra_checks` 是机械正则、`VENUE_RULES.md` 是硬约束说明、`CHECKLIST.md` 是人工+机械混合勾选项。要求：每个 `extra_checks` 项有稳定 ID `TZ-EC-<slug>`，在 `CHECKLIST.md` 有对应 `TZ-CL-<slug>` 并在 `VENUE_RULES.md` 有依据说明（EC ⊆ CL）；反向不要求，`CHECKLIST.md` 可含纯人工项。仓库当前不存在 `bilingual_abstract` 这类稳定 ID，需在本任务建立。

### R4 文档站同步

21. 新增的 `ZH_THESIS_REVIEW_CRITERIA.md` 与 `zh_thesis_reviewer_agent.md` 必须登记进 `docs/resource-manifest.json`（含 `sourceLocale`、`sourceSha256`、`en`、`zh`），并产出两个语言的目标页面。
22. 修改的 `VENUE_RULES.md`、`CHECKLIST.md`、`agent-roster.md`、`REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、`MODE_GUIDE.md` 必须更新对应 `sourceSha256`。
23. 遵守 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`：源资源正文是详细规则事实来源，文档站不得从旧页面反推技能行为。

### R5 不动的边界

24. `SKILL.md` 的 `version` 不变，只更新 `last_updated`。
25. 不改 issue JSON schema、severity 档位、ScholarEval 的 8 个基础维度与权重。C1 已扩展 `MODULE_DIMENSION_MAP`，C2 不再改动它。
26. 不改 skill `description` 与 `when_to_use`（触发边界不动）。
27. 不新增 CLI flag。

## Acceptance Criteria

每条 AC 后括注对应的 R 条与 design 小节。

- [ ] AC5-1（R1、R2 / design §1）：`references/ZH_THESIS_REVIEW_CRITERIA.md` 存在，含 **15 行**中文审阅指标表（与 design §1 表行数一致），每行标注所映射的**基础评分维度**（8 个之一）、`[Script]` / `[LLM]` 档位与承载脚本。文档中明确区分"8 个基础评分维度 / 1 个派生总分 `overall_base` / 15 行中文审阅指标"三个集合（TPR-10）。`[Script]` 档位逐项指向 C1 实际接通的检查器。
- [ ] AC5-2（R2 / design §3）：`agents/zh_thesis_reviewer_agent.md` 存在，含红线声明、非中文输入退出条件、`ISSUE_SCHEMA.md` 输出约定与 `Output limit`。
- [ ] AC5-3（R2.9、R2.12 / design §3）：登记面按类型分开且完整（TPR-07）：
  - 参考文件进 `SKILL.md ## References` + `docs/resource-manifest.json`，**不在 `agent-roster.md`**（有测试断言）。
  - agent 进 `agent-roster.md` + `SKILL.md ## Reviewer Lanes`。
  - 新 canonical lane `zh_thesis_review` 贯穿 `REVIEW_LANE_GUIDE.md`（定义与选择条件）、`SUBAGENT_TEMPLATES.md`（focus 块）、`MODE_GUIDE.md` Phase 3B（lane 清单与 zh 门控）、`audit.py` 的 `_selected_lanes_for_focus`（`:924`）/ lane 输出登记（`:949`）/ cross-cutting fallback（`:792`）、`consolidate_review_findings.py`、checkpoint 恢复（`_load_completed_lanes` `:929`）。每个入口至少一条断言。
- [ ] AC5-4（R4 / design §6）：`docs/resource-manifest.json` 含两条新条目（字段完整），六个改动资源的 `sourceSha256` 已更新，`just ci` 的 manifest 散列校验与双语页面校验全绿。paper-audit 条目数由 58 增至 60。
- [ ] AC6-1（R3.20 / design §5）：三集合的**有方向覆盖关系**成立且有测试：每个 `TZ-EC-*` 在 `CHECKLIST.md` 有 `TZ-CL-*` 对应项、在 `VENUE_RULES.md` 有依据说明。测试用语义 ID 锚定，不用行号或整数序号。**不断言集合相等**（TPR-04）。
- [ ] AC6-2（R3.15 / design §4、C1 design §7）：`VENUE_CONFIG["thesis-zh"]["extra_checks"]` 中不含附录存在性与符号表存在性检查；有测试引用模板证据（`yanshan.md:52`-`:53`、`pkuthss.md:25`/`:106`）说明理由（TPR-03）。
- [ ] AC6-3（R3.16 / design §4）：`VENUE_CONFIG["thesis-zh"]` **不含** `required_sections` 字段；该决定在 design 中有书面理由（无运行时消费者），不写测试断言死配置（TPR-04）。
- [ ] AC6-4（R3.17 / design §4）：`blind_review` 字段取值有实测依据，实测结论已写回 design §4。
- [ ] AC7-1（R5.24 / implement 阶段 D）：`SKILL.md` 的 `version` 与 `pyproject.toml` 一致且未变，`last_updated` 已更新为落地日期。
- [ ] AC7-2（— / implement 阶段 D）：`just ci` 全绿。
- [ ] AC8（R2、R3 / C1 fixture manifest）：按 C1 建立的 fixture manifest 逐行验收，不用单一 fixture 承担全部断言（TPR-08）。至少：F1 触发 D2 / D3 在 `--mode gate --venue thesis-zh` 下进入阻断集；F3（无附录无符号表，其余合规）在同一命令下**不 FAIL**；`--mode deep-review` 下 `zh_thesis_review` lane 产出并进入 consolidation。

## Notes

- `SKILL.md` 的路由表格不要让全局格式化 hook 对齐，会触发 `ROUTER_ROW_RE` contract 测试。
- `docs/resource-manifest.json` 是 JSON，格式化 hook 会压平数组——写临时 `.py` 文件执行，不用 `Edit` / `Write`，也不用 heredoc（PowerShell 不支持，TPR-12）。
- paper-audit 当前有 58 条 manifest 条目，新增后应为 60 条。
- `UNVERIFIED`：新 agent 未实际运行，其跨 agent 一致性、学术判断质量与既有 canonical lane 的等价性未经验证。本任务只保证接线可达与输出符合 schema，不声称审阅质量。
