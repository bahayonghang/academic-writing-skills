---
skill: trellis-plan-review
version: 0.4.0
task_dir: D:/Documents/Code/Agents/academic-writing-skills/.trellis/tasks/08-30-paper-audit-zh-profile
task_name: 08-30-paper-audit-zh-profile
task_status: planning
review_scope: task-tree
task_count: 3
task_members:
  - 08-30-paper-audit-zh-profile
  - 08-30-zh-dispatch-wiring
  - 08-30-zh-review-criteria
task_statuses:
  08-30-paper-audit-zh-profile: planning
  08-30-zh-dispatch-wiring: planning
  08-30-zh-review-criteria: planning
verdict: 需返回规划
blocking: 8
should_fix: 4
notes: 1
generated_at: 2026-08-30T23:25:22+08:00
---

# Trellis 规划审阅报告

## 审阅范围

本次将根任务及其递归子任务作为一个原子范围审阅，顺序为根任务优先、随后按显式依赖顺序检查子任务：

1. `.trellis/tasks/08-30-paper-audit-zh-profile`（planning）
2. `.trellis/tasks/08-30-zh-dispatch-wiring`（planning）
3. `.trellis/tasks/08-30-zh-review-criteria`（planning）

预检确认任务树、父子反向链接、状态和任务顺序有效；三个任务均未开始实施，因此本次不执行实现后 diff 漂移审阅。审阅依据包括三组 `task.json`、`prd.md`、`design.md`、`implement.md`，关联 Trellis 规范，以及当前仓库中的调度器、脚本 CLI、评分器、报告门禁、代理路由和测试。

## 结论

**需返回规划：阻断 8 / 应修 4 / 提示 1。**

当前规划识别出了正确的中文审阅能力缺口，也给出了清晰的父子拆分和实施顺序；但若按现有设计实施，若干验收标准会因为运行时入口不可达、脚本参数/输出契约不成立、门禁误分类或评分与代理接线缺失而无法稳定满足。应先修订规划，再进入实现。

## Findings

### TPR-01

- **Severity:** blocking
- **Task:** `08-30-paper-audit-zh-profile`
- **Affected tasks:** `08-30-paper-audit-zh-profile`, `08-30-zh-dispatch-wiring`, `08-30-zh-review-criteria`
- **Location:** `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:100`; `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:107`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:36`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:117`; `academic-writing-skills/paper-audit/scripts/audit.py:419`; `academic-writing-skills/paper-audit/scripts/audit.py:1679`; `academic-writing-skills/paper-audit/scripts/audit.py:1735`; `academic-writing-skills/paper-audit/scripts/audit.py:2315`; `academic-writing-skills/paper-audit/scripts/audit.py:2431`
- **Claim:** 规划假定按 `quick-audit`、`deep-review`、`re-audit`、`polish` 划分 `ZH_EXTRA_CHECKS` 就能让各模式稳定选择不同中文检查器，并覆盖 `.tex`、`.typ` 和 `.pdf`。
- **Evidence:** 现有 `run_deep_review()` 和 re-audit 路径都以 `mode="quick-audit"` 回调 `run_audit()`；因此规划中的 `deep-review` 与 `re-audit` 字典项没有选择入口。`polish` 在统一审计分流前走独立路径，并直接解析 `sentences` 检查器；规划又全局抑制中文 `sentences` 且将 `polish` 额外检查设为空，会让中文润色丢失现有表达检查，而不是被 `style_patterns` 替代。格式解析中 `.typ` 只使用 `SCRIPTS_TYPST`，新加到 `SCRIPTS_ZH` 的 LaTeX 检查器不可达；`.pdf` 则可能把 PDF 交给只接受 TeX 源文的检查器，规划没有定义逐脚本格式适用性或跳过规则。
- **Impact:** 根任务 AC3 与 AC8 以及子任务的模式矩阵没有可执行机制；实施后既可能出现死配置，也可能引入 `polish` 回归或对 Typst/PDF 的错误调用。
- **Route:** 在子任务 1 中先给出“真实入口 × 模式 × 格式 × 检查器”的完整可达性矩阵，并明确修改运行时模式传播、`polish` 替换点、Typst 等价脚本或显式豁免、PDF 提取/跳过策略；为每一个矩阵单元配套测试和验收断言。

### TPR-02

- **Severity:** blocking
- **Task:** `08-30-zh-dispatch-wiring`
- **Affected tasks:** `08-30-zh-dispatch-wiring`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:67`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:95`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:144`; `.trellis/tasks/08-30-zh-dispatch-wiring/implement.md:59`; `academic-writing-skills/latex-thesis-zh/scripts/blind_review.py:768`; `academic-writing-skills/latex-paper-en/scripts/analyze_literature.py:531`; `academic-writing-skills/typst-paper/scripts/verify_bib.py:424`; `academic-writing-skills/paper-audit/scripts/audit.py:465`; `academic-writing-skills/paper-audit/scripts/audit.py:2528`
- **Claim:** 规划把新增脚本视为可以通过通用参数拼接和“优先 JSON、否则解析文本”的统一适配层接入。
- **Evidence:** `blind_review.py` 没有 `--json`，其报告使用 Markdown 标题和 `[HIGH]`/`[P0]`，不符合审计器现有的 `[Severity: ...][Priority: ...]` 文本协议；`analyze_literature.py` 同样没有 `--json`，但实施计划明确要求传入该参数。Typst 的 `verify_bib.py` 只支持 `--style gb-7714-2015-numeric`，不支持计划中的 `--standard gb7714`。现有 JSON 脚本的对象结构也并不统一。审计器对非零退出码仅对启动失败 `-1` 建立错误项，未知参数导致的退出码 2 加空 stdout 可能被解释为无发现。
- **Impact:** 新脚本可能根本无法运行，或在失败时被错误报告为 clean；AC3、AC4 和 AC8 会产生假阴性，不能以当前适配设计验收。
- **Route:** 在设计中逐脚本列出真实 CLI、输入格式、输出 schema、退出码语义和 issue 映射，建立显式 adapter registry；为未知参数、非零退出、空输出、非法 JSON 和各脚本真实样例分别添加回归测试，禁止依赖通用猜测式解析。

### TPR-03

- **Severity:** blocking
- **Task:** `08-30-zh-dispatch-wiring`
- **Affected tasks:** `08-30-zh-dispatch-wiring`, `08-30-zh-review-criteria`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:121`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:133`; `.trellis/tasks/08-30-zh-review-criteria/design.md:61`; `.trellis/tasks/08-30-zh-review-criteria/implement.md:89`; `academic-writing-skills/paper-audit/scripts/audit.py:2200`; `academic-writing-skills/paper-audit/scripts/audit.py:2212`; `academic-writing-skills/paper-audit/scripts/report_generator.py:1225`; `academic-writing-skills/latex-thesis-zh/templates/yanshan/main.tex:52`; `academic-writing-skills/latex-thesis-zh/templates/pkuthss/main.tex:117`
- **Claim:** 规划声称门禁只纳入确定性 blocker，同时把 `consistency`、附录存在性和符号表存在性放入门禁候选。
- **Evidence:** 子任务 1 的 gate 集合包含只产生 PASS/WARNING 的 `consistency`，与同一设计中“只有 spec/blind blocker”的声明矛盾。`extra_checks` 正则缺失时会生成失败清单项，而最终 gate 要求所有 checklist 项通过；因此把附录或符号表缺失作为 `extra_checks` 会直接导致 FAIL。现有燕山和 PKU 模板分别明确符号表/附录为可选或非强制。`blind_review` 目前在 gate 中仅代表确定性的作者信息检测，并没有计划所称的待实现动态语义。
- **Impact:** 合法论文可能因可选章节或质量提示被错误阻断，违反根任务 AC4 的“确定性 blocker”边界，并破坏现有门禁兼容性。
- **Route:** 在规划中建立唯一的 `gateEligible` 规则：只允许有明确规范依据、对当前模板必需且可确定检测的 Critical 进入 gate；把一致性、可选章节和建议项保留在报告层。根据现有静态调用语义直接写清 blind-review gate 决策及测试，不把该决策推迟到实现阶段。

### TPR-04

- **Severity:** blocking
- **Task:** `08-30-zh-review-criteria`
- **Affected tasks:** `08-30-zh-review-criteria`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-zh-review-criteria/prd.md:37`; `.trellis/tasks/08-30-zh-review-criteria/design.md:61`; `.trellis/tasks/08-30-zh-review-criteria/design.md:77`; `academic-writing-skills/paper-audit/scripts/audit.py:305`; `academic-writing-skills/paper-audit/scripts/audit.py:308`; `academic-writing-skills/paper-audit/scripts/audit.py:2144`
- **Claim:** 规划要求 `VENUE_CONFIGS`、`required_sections` 与 checklist 形成可测试的“三集合互为子集或相等”契约，并使用 `bilingual_abstract` 等稳定语义 ID。
- **Evidence:** 当前代码只有单数 `VENUE_CONFIG`；规划引用的 `VENUE_CONFIGS` 不存在。`required_sections` 只在配置定义中出现，没有运行时消费者。venue 规则是自由文本/正则，checklist 是面向人工与机械检查的十项混合集合，仓库没有 `bilingual_abstract` 等稳定 ID，也没有说明三个承担不同职责的集合为何应当相等。当前设计因此既无法按所写符号落地，也无法定义确定的双向集合关系。
- **Impact:** 根任务 AC6 缺少可执行的契约对象和比较算法；强行按集合相等实现会把提示性检查、正则规则和章节要求混为一谈，制造错误门禁或脆弱测试。
- **Route:** 修正为真实的 `VENUE_CONFIG`，先为“章节要求、venue 规则、checklist 项”分别定义稳定 ID 和职责，再给出有方向的映射/覆盖关系以及运行时消费者；如果 `required_sections` 仍无消费者，应在本任务明确接线或从 AC6 中移除，不能仅测试死配置。

### TPR-05

- **Severity:** blocking
- **Task:** `08-30-zh-dispatch-wiring`
- **Affected tasks:** `08-30-zh-dispatch-wiring`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-zh-dispatch-wiring/prd.md:25`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:12`; `academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py:111`; `academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py:157`; `academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py:194`; `academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py:216`; `academic-writing-skills/latex-paper-en/scripts/check_pseudocode.py:265`
- **Claim:** 规划把英文 `check_pseudocode.py` 认定为“不依赖英文词表、语言中立”，只需对 `thesis-zh` 降级 IEEE 严格约束即可复用。
- **Evidence:** 该脚本用 ASCII 单词计数，检测英文冠词 `The/A/An`，要求字面量 `Input/Output`，并以英文词数阈值判断伪代码质量；CLI 的 venue 也只接受空值或 `ieee`。这些都是语言相关假设，不是仅有一条 IEEE 严格度需要降级。
- **Impact:** AC2 所依赖的“已证明可复用”事实不成立；直接接入会对中文伪代码产生系统性误报/漏报。
- **Route:** 将此项改为明确的中文本地化设计：定义中文输入/输出标记、长度度量、冠词规则的替代或豁免、venue 传参和中英混排策略，并用中文正例/反例验证；若本期不实现，应从中文默认检查链和 AC 中移除。

### TPR-06

- **Severity:** blocking
- **Task:** `08-30-zh-review-criteria`
- **Affected tasks:** `08-30-zh-review-criteria`, `08-30-zh-dispatch-wiring`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:104`; `.trellis/tasks/08-30-zh-review-criteria/design.md:5`; `.trellis/tasks/08-30-zh-review-criteria/design.md:29`; `academic-writing-skills/paper-audit/scripts/scholar_eval.py:65`; `.trellis/spec/academic-writing-skills/paper-audit-boundary-contracts.md:53`
- **Claim:** 新增 `SPEC`、`BLIND`、`ABSTRACT`、`CONCLUSION`、`LITERATURE`、`TABLES` 模块后，中文指标表和 ScholarEval 能自然覆盖这些检查结果，且无需调整模块到维度的运行时映射。
- **Evidence:** `scholar_eval.py` 的 `MODULE_DIMENSION_MAP` 没有任何上述新模块键；边界规范明确未知 audit module 不参与脚本评分。子任务 1 又计划把新脚本解析成这些新模块名，而根任务范围没有允许或设计相应映射变更。仅新增参考指标表不会改变运行时评分归属。
- **Impact:** 新脚本即使成功发现问题，也会被 ScholarEval 评分路径忽略；根任务 AC5 和“中文审阅指标进入评分/审阅机制”的目标没有实现机制。
- **Route:** 在父子任务范围中明确选择一种方案：为新模块扩展稳定映射并更新规范/测试，或把新检查映射到已有受支持模块；同时定义重复计分、维度权重和未知模块的 fail-closed 行为。

### TPR-07

- **Severity:** blocking
- **Task:** `08-30-zh-review-criteria`
- **Affected tasks:** `08-30-zh-review-criteria`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:104`; `.trellis/tasks/08-30-zh-review-criteria/design.md:44`; `.trellis/tasks/08-30-zh-review-criteria/implement.md:24`; `academic-writing-skills/paper-audit/SKILL.md:129`; `academic-writing-skills/paper-audit/SKILL.md:194`; `academic-writing-skills/paper-audit/references/MODE_GUIDE.md:174`; `academic-writing-skills/paper-audit/references/SUBAGENT_TEMPLATES.md:58`; `academic-writing-skills/paper-audit/references/agent-roster.md:1`
- **Claim:** 新建中文审阅代理并在 `SKILL.md` 与 `agent-roster.md` 登记，就足以使 deep-review/re-audit 的用户可见结果采用该代理；AC 还要求“两个新文件”都登记在 agent roster。
- **Evidence:** 当前 deep-review 的 canonical lanes、fallback 和输出模板分别固化在 `SKILL.md`、`MODE_GUIDE.md`、`SUBAGENT_TEMPLATES.md` 与 lane guide 中；`agent-roster.md` 自身说明它只是代理清单，参考 playbook 不会自动调度。实施计划没有修改 mode guide、canonical lane、模板、checkpoint、fallback 或汇总协议。并且 `zh-review-criteria.md` 是参考文件，不是代理，不应登记到 agent roster；设计/实施实际上也只登记代理文件。
- **Impact:** 代理文件可能存在但运行时永远不会可靠调用，或调用后不能进入标准汇总；根任务 AC5 与子任务 AC5-3 无法由当前变更集证明。
- **Route:** 明确代理是替换既有 canonical lane、增加新 lane，还是仅作为参考代理；随后把选择条件、任务模板、输入/输出、fallback、checkpoint 和最终汇总字段贯穿所有规范入口。将“参考文件登记”改到 references 导航/manifest，agent roster 只登记真实 agent。

### TPR-08

- **Severity:** blocking
- **Task:** `08-30-paper-audit-zh-profile`
- **Affected tasks:** `08-30-paper-audit-zh-profile`, `08-30-zh-dispatch-wiring`, `08-30-zh-review-criteria`
- **Location:** `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:107`; `.trellis/tasks/08-30-zh-dispatch-wiring/implement.md:81`; `.trellis/tasks/08-30-zh-review-criteria/implement.md:125`
- **Claim:** 一个最小中文论文 fixture 将同时证明 quick/deep/re-audit/polish 的路由、五类以上问题、blind/spec blocker 和新报告维度。
- **Evidence:** 子任务 1 对 fixture 的唯一具体内容要求是 `.bib` 含 GB/T 7714 违规；子任务 2 却要求同一 fixture 稳定触发至少五类 deep-review 问题以及 blind/spec gate blocker。规划没有给出每类问题对应的源文本嵌入、目标脚本、期望 severity/module、模式可见性和互不干扰断言，也没有处理部分脚本对格式和 CLI 的差异。
- **Impact:** AC8 只是结果清单，没有可复现的测试机制；实现者无法区分 fixture 缺陷、路由缺陷和解析缺陷，验收可能靠手工调参偶然通过。
- **Route:** 在实施计划中定义 fixture manifest：每个嵌入缺陷的精确片段、所属脚本、预期 module/severity/gate 状态、适用模式/格式及负例；必要时拆成多个最小 fixture，并为四种模式给出确定性快照或结构化断言。

### TPR-09

- **Severity:** should-fix
- **Task:** `08-30-zh-dispatch-wiring`
- **Affected tasks:** `08-30-zh-dispatch-wiring`
- **Location:** `.trellis/tasks/08-30-zh-dispatch-wiring/prd.md:58`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:44`; `academic-writing-skills/latex-thesis-zh/scripts/blind_review.py:769`; `academic-writing-skills/latex-thesis-zh/scripts/blind_review.py:790`
- **Claim:** 规划将 `--author`、`--supervisor`、`--suffix`、`--force` 视为可能触发写回的参数，并据此定义只读边界。
- **Evidence:** 真正触发生成/写入分支的是 `--generate`；`--author` 和 `--supervisor` 是只读扫描输入，缺失时还会跳过部分姓名检测。规划没有明确禁止实际写参数 `--generate`，却禁止了有助于检测的只读参数。
- **Impact:** 边界测试可能放过真实写回风险，同时无谓削弱盲审检测覆盖。
- **Route:** 将契约改为“审计器绝不传 `--generate`”，逐项标注输入参数与写参数；为只读运行增加文件 hash/mtime 不变测试，并按可用元数据决定是否传 author/supervisor。

### TPR-10

- **Severity:** should-fix
- **Task:** `08-30-zh-review-criteria`
- **Affected tasks:** `08-30-zh-review-criteria`, `08-30-paper-audit-zh-profile`
- **Location:** `.trellis/tasks/08-30-zh-review-criteria/prd.md:52`; `.trellis/tasks/08-30-zh-review-criteria/design.md:9`; `.trellis/tasks/08-30-zh-review-criteria/implement.md:31`; `academic-writing-skills/paper-audit/scripts/scoring_model.py:40`; `academic-writing-skills/paper-audit/references/quality_rubrics.md:73`
- **Claim:** AC5-1 要求“10 个维度”，设计表实际列出 15 个 thesis rows，实施步骤又要求 15 行，并把当前评分模型描述成含 `overall` 的同一维度集合。
- **Evidence:** 三处计数相互矛盾；现有评分模型是 8 个基础评分维度加一个计算得到的 `overall_base`，参考规范也明确 overall 是由 8 维计算而来，并非第 9 个独立审阅维度。
- **Impact:** 实现者无法判断是验收 10、15 还是 8+派生总分，测试与文档可能各自通过不同口径。
- **Route:** 将“运行时评分维度”“中文审阅指标行”“派生总分”分成三个命名集合，给出唯一数量、稳定 ID 和映射表，并统一 PRD、设计、实施与测试断言。

### TPR-11

- **Severity:** should-fix
- **Task:** `08-30-zh-dispatch-wiring`
- **Affected tasks:** `08-30-zh-dispatch-wiring`
- **Location:** `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:159`; `.trellis/tasks/08-30-zh-dispatch-wiring/implement.md:103`; `tests/skills/paper_audit/test_paper_audit.py:420`; `academic-writing-skills/paper-audit/scripts/audit.py:301`
- **Claim:** 规划断言没有测试直接引用 `ZH_EXTRA_CHECKS`，因此可安全从 list 改为按模式 dict，实施清单也没有列出相应现有测试迁移。
- **Evidence:** `test_paper_audit.py` 直接导入该符号并断言 `"consistency" in ZH_EXTRA_CHECKS`。list→dict 会改变该断言的语义并直接破坏现有测试或产生误导性通过。
- **Impact:** 实施清单遗漏一个确定的兼容性更新点，现有回归保护会失效。
- **Route:** 在 impacted files 和测试步骤中明确迁移该测试，增加每模式内容、不可变性/复制语义及旧行为兼容断言；若需要保留兼容接口，设计独立的新映射符号。

### TPR-12

- **Severity:** should-fix
- **Task:** `08-30-zh-dispatch-wiring`
- **Affected tasks:** `08-30-zh-dispatch-wiring`, `08-30-zh-review-criteria`
- **Location:** `.trellis/tasks/08-30-zh-dispatch-wiring/implement.md:8`; `.trellis/tasks/08-30-zh-dispatch-wiring/implement.md:30`; `.trellis/tasks/08-30-zh-dispatch-wiring/implement.md:76`; `.trellis/tasks/08-30-zh-review-criteria/implement.md:70`
- **Claim:** 实施验证命令可在本仓库当前 Windows PowerShell 环境直接执行。
- **Evidence:** 当前 PowerShell 环境没有 `tail`；子任务 1 多处使用它。子任务 2 使用 Bash heredoc `python - <<'PY'`，不是 PowerShell 语法。
- **Impact:** 实施者会在非产品问题上阻塞，且复制执行的验证证据不可复现。
- **Route:** 全部换成仓库支持的 `uv run ...`、`Get-Content -Tail` 或临时测试文件/`python -c` 形式，并在计划中按 PowerShell 给出可直接执行的命令。

### TPR-13

- **Severity:** note
- **Task:** `08-30-paper-audit-zh-profile`
- **Affected tasks:** `08-30-paper-audit-zh-profile`, `08-30-zh-dispatch-wiring`, `08-30-zh-review-criteria`
- **Location:** `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:13`; `.trellis/tasks/08-30-paper-audit-zh-profile/prd.md:125`; `.trellis/tasks/08-30-zh-dispatch-wiring/design.md:164`; `.trellis/tasks/08-30-zh-review-criteria/implement.md:159`
- **Claim:** 规划文档中的仓库快照和来源标注足以作为后续实现基线。
- **Evidence:** 根任务记录的 HEAD `50d06fb` 已不是当前 HEAD `29c3cb3`，期间包含 paper-audit 相关变更；所有 PRD/design/implement 末尾还残留 `</content>`/`</invoke>` 导出标签。预检共识别 17 个歧义引用，主要是只写符号名、模糊范围或非规范的 requirement 标注。
- **Impact:** 这些问题当前不单独改变主要结论，但会降低计划的可追溯性，并增加实现时引用漂移风险。
- **Route:** 修订时移除导出残片，刷新 HEAD/清单快照；把关键事实改成精确 `path:line` 或符号签名，并为每条 AC 明确标注对应 requirement 与设计机制。

## UNVERIFIED

- `UNVERIFIED`：本次没有用外部权威文本核验 GB/T 7714 的具体规则选择；只能确认当前规划与仓库脚本 CLI/配置不一致，不能据此证明拟新增正则本身符合标准。
- `UNVERIFIED`：没有对计划中的中文正则在真实论文语料上运行召回率、误报率或性能基准；现有源码与 fixture 只能证明控制流和接口，不证明检测质量。
- `UNVERIFIED`：没有实际运行新中文审阅代理，因此不能证明其跨代理一致性、学术判断质量或与现有 canonical lanes 的等价性。
- `UNVERIFIED`：任务仍处于 planning，本次未运行 `just ci`、端到端模式矩阵或实现后 diff；这些证据应在修订规划获批并实施后补充。

## 已核实的合理部分

- 根任务与两个子任务的父子链接、递归范围和 `C1 → C2` 顺序有效；共享修改 `audit.py` 的风险也已在任务树中显式排序。
- 三个任务均为 planning，当前没有把规划审批误当作实施、提交、归档或推送授权。
- 规划对“检查器只读、写作 helper 不进入审计链”的边界方向正确，并明确不应让 blind-review 生成盲审副本。
- 现有能力盘点中的主要数量经仓库复核大体成立，包括 manifest、references、agents、templates、paper-audit 测试规模和边界规范引用；这些盘点可保留，但应刷新到当前 HEAD。
- 文档中英同步、回滚路径、共享文件冲突以及先接线后扩展审阅标准的总体拆分方向合理。

## Reviewer disclosure

An agent reviewing an agent's plan is not an independent second opinion. The reviewer and the author share most of the same blind spots. A clean report means "this pass found nothing", not "the plan is complete". Treat the findings as a triage list, not as an approval.
