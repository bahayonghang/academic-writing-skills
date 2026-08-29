---
skill: trellis-plan-review
version: 0.2.0
task_dir: 'D:\Documents\Code\Agents\academic-writing-skills\.trellis\tasks\08-25-thesis-zh-quality-closure'
task_name: 08-25-thesis-zh-quality-closure
task_status: planning
verdict: 需返回规划
blocking: 10
should_fix: 2
notes: 3
generated_at: 2026-08-25T21:30:56.8440599+08:00
---

# Trellis 规划审阅报告

## 结论

需返回规划 — 阻断 10 / 应修 2 / 提示 3

父任务与 6 个子任务的方向基本一致，但目前只有
`08-25-thesis-zh-visible-prose-ir` 具备 design/implement 和非占位 manifest；其余
关键链路仍停留在 PRD。`task.py validate` 的通过只证明文件结构合法，不能抵消验收
追踪、契约一致性和实现机制上的 No-Go。

## 审阅范围与方法

- 范围：父任务 `08-25-thesis-zh-quality-closure`，以及
  `08-25-thesis-zh-visible-prose-ir`、`08-25-thesis-zh-semantic-artifacts`、
  `08-25-thesis-zh-mode-contract`、`08-25-thesis-zh-re-audit-gate`、
  `08-25-thesis-zh-rule-governance`、`08-25-thesis-zh-output-eval`。
- 规划证据：逐份读取 `task.json`、`prd.md`、可用的 `design.md`、`implement.md`、
  `implement.jsonl`、`check.jsonl` 和父任务 `research/evidence-audit.md`。
- 仓库证据：核验被引用的实现、测试、contract、fixture、文档镜像、manifest 与
  Trellis workflow；未修改规划或产品文件。
- 预检：对 7 个任务分别运行 `plan_precheck.py`；对 7 个任务分别运行
  `task.py validate`。后者全部结构通过，但父任务和 5 个 PRD-only 子任务均显示
  0 条可执行/检查 entry。
- 网络校准：只把官方文档和开源仓库当作设计先例，不把仓库自述、fixture 或计划
  当成实际质量证据。

## 问题清单

### TPR-01 · 阻断 · 七份 PRD 的验收条款没有稳定 ID，manifest 无法建立闭环

- Location: 父任务 `prd.md:65-91`；六个子任务各自 `## Acceptance Criteria`；
  `08-25-thesis-zh-visible-prose-ir/{implement.jsonl,check.jsonl}`。
- Claim: 父子任务可按 requirements/acceptance criteria 实施、检查并汇总关闭。
- Evidence: 重新统计 7 个 Acceptance Criteria 区域，共 89 条 checkbox，稳定
  `AC-*` ID 为 0；visible-prose 两份真实 manifest 引用 `R1`—`R7`，但预检将这些
  引用判为 undefined，因为 PRD 未提供 Trellis 可识别的 requirement/AC 标识。
  其余任务 manifest 仍为 `_example`。
- Impact: 实现条目、检查条目和父任务 closure 无法追到唯一验收条款；即使测试绿，
  也无法证明 89 个条款中哪些已覆盖、部分覆盖或遗漏。
- Route: 为父任务和各子任务建立稳定、唯一的 requirement/AC 标识并在两类
  manifest 中显式引用；或先把 manifest/预检的识别规则改为支持当前标题格式，
  再以预检零 undefined 引用作为 readiness gate。

### TPR-02 · 阻断 · 五个实质性子任务仍是 PRD-only 占位计划

- Location: `08-25-thesis-zh-semantic-artifacts`、`08-25-thesis-zh-mode-contract`、
  `08-25-thesis-zh-re-audit-gate`、`08-25-thesis-zh-rule-governance`、
  `08-25-thesis-zh-output-eval` 的任务目录。
- Claim: 父任务依赖链可依次进入实现并在末尾统一验收。
- Evidence: 上述 5 个任务没有 `design.md`、`implement.md`，两份 jsonl 均只有
  `_example`；它们分别涉及新 schema/IO、orchestrator/权限状态机、根因 diff、
  规则单一 owner、输出评测与报告口径，均非可由 PRD 直接机械落地的单文件改动。
  父任务 `prd.md:51-63` 又把它们设为后续任务的硬依赖。
- Impact: 数据模型、CLI、错误语义、迁移顺序、测试入口和产物所有权仍可在实现时
  任意漂移；父任务依赖图存在，但关键边没有可审阅的实现机制。
- Route: 先为 5 个子任务补齐 design、implement 和真实 manifest；或把范围进一步
  拆为能由现有规范唯一决定的更小任务。父任务作为协调器可以继续不直接实现，
  但应只在所有子任务通过预检后进入 ready。

### TPR-03 · 阻断 · visible-prose 的章节选择器与自带 B1 fixture 不能同时成立

- Location: `08-25-thesis-zh-visible-prose-ir/design.md:7-25,115-146`；同任务
  `prd.md:42-53,88-94`；`evals/fixtures/thesis-project/main.tex:11-31`。
- Claim: B1 同时含符号表、绪论、过程分析章和方法章；角色分类后可自动唯一选择
  正文过程章，特殊章零主线 finding。
- Evidence: design 把 `process` 和 `method` 都归为 `section_role=body`，选择器又把
  所有 `body` 节点作为候选，并规定候选数不等于 1 就要求显式 `--section`。B1 至少
  有过程章和方法章两个 body 候选。既有 thesis-project fixture 又没有
  `\frontmatter`/`\mainmatter` 边界，按当前信号表可能降为 `unverified`。
- Impact: 按设计实现会让核心 V1 自动选择断言失败，或为让测试通过而在实现期临时
  引入 PRD/design 未定义的过程章判据。
- Route: 明确“角色分类”和“过程章选择”是两步还是一步，并为多 body、无
  `mainmatter`、标题/路径冲突分别规定唯一可测试的结果；同步调整 B1 结构或选择
  机制，而不是在测试中绕过歧义。

### TPR-04 · 阻断 · V2 阈值归一公式违背短文本需求且关键常数未闭合

- Location: `08-25-thesis-zh-visible-prose-ir/prd.md:55-63`；同任务
  `design.md:164-196`、`implement.md:59-64,121-126`。
- Claim: 词项阈值按可见正文长度归一，短文本不会因篇幅换算而触发，现有 cap
  无需改动。
- Evidence: PRD 要求短文本不触发；design/implement 却规定
  `visible_zh_chars < min_sample` 时回退原始 `count > cap`。`window` 仍留到实现期
  通过 fixture 或“真实学位论文典型量级”人工决定，分母是否包含不进入分子通道的
  可见节点也未定义。切换点两侧缺少单调性/连续性约束。
- Impact: 同一术语计数可能因文本跨过 `min_sample` 而改变结论；核心 V2 验收没有
  唯一 oracle，且实现需要使用未授权的真实论文量级或临场选择常数。
- Route: 在设计阶段锁定分子、分母、window、边界比较符和短文本策略，并增加
  `min_sample-1/min_sample/min_sample+1` 的性质测试；若真实语料仅用于标定，保持
  `missing evidence`，不要作为实现时的隐式输入。

### TPR-05 · 阻断 · “旧行为不变”与本任务预期改变的输出没有划清边界

- Location: 父任务 `prd.md:87`；visible-prose `prd.md:83-86`；同任务
  `implement.md:65-84`。
- Claim: 旧 analyzer 的命令、flags 和行为保持不变；同时章节覆盖、term threshold
  和 finding 去重会按 V1—V3 改正。
- Evidence: implement 已承认 `analyze_logic.py` 章引言检查覆盖集合会变化，并把
  `deai_check.py` 的触发公式和 finding 去重键改掉；这些都是可观察输出行为，不能
  与无条件的“行为不变”同时由快照证明。
- Impact: 正确修复可能被兼容快照判回归，或为保快照而不实现 PRD；check 阶段没有
  稳定的允许差异集合。
- Route: 将兼容面拆成 CLI/exit/help/未迁移通道的严格不变面与 V1—V3 的已批准
  语义差异面，并为后者建立逐项 golden delta；不要用一个全量“行为不变”条款覆盖
  两类合同。

### TPR-06 · 阻断 · UTF-8 修复范围和失败语义在 PRD、design、仓库现实间不一致

- Location: visible-prose `prd.md:71-76`；`design.md:198-216`；
  `implement.md:14,29-30,44,66,80`；`academic-writing-skills/latex-thesis-zh/scripts/`。
- Claim: 所有脚本入口在清空 `PYTHONIOENCODING` 后都能稳定输出 UTF-8；无法
  `reconfigure` 时给出明确修复或错误。
- Evidence: 仓库复算得到 24 个 `.py` 文件、21 个 `main()` 入口；implement 先保存
  “26 个脚本”但没有定义计数口径，实际只计划在 `deai_check.py` 和
  `analyze_logic.py` 调 helper。design 对无 `reconfigure` 的流选择静默跳过，
  与“明确修复或错误”相反。Python 官方文档还区分 Windows 控制台与重定向管道的
  编码：当前 V4 subprocess 只证明 pipe 情形，不能外推所有 PowerShell/console 情形。
- Impact: 全入口 AC 无法由两处调用证明，测试替身或重定向流仍可能乱码/静默失效；
  基线清单本身还可能漏项或误报数量。
- Route: 先定义入口清单和 console/pipe/file/test-double 矩阵，再选择集中 wrapper、
  全入口接入或缩窄 AC；对不支持 `reconfigure` 的流规定可断言结果，并以官方编码
  语义限定 V4 的结论。

### TPR-07 · 阻断 · finding schema 的父子字段集与 paper-audit 基准互不相等

- Location: 父任务 `prd.md:82-86`；semantic-artifacts `prd.md:26-38,86-105`；
  `academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md:7-26,44-48`；
  re-audit `prd.md:22-35`。
- Claim: 新 finding schema 与 paper-audit 字段名逐项对齐，并携带后续 re-audit
  所需的证据强度、锚点和根因信息。
- Evidence: 子任务字段集缺少父任务列出的 `claim_strength`、`evidence_anchor`；
  paper-audit 实际 schema 还使用 `explanation`、`comment_type`、`source_section`、
  `allowed_wording`、`forbidden_wording`、`quote_verified` 等字段，且 `source_kind`
  只列 script/llm，而子任务增加 human。与此同时 R3 的 `claim-evidence.json` 又单独
  定义 strength/anchor，未说明 finding 是复制、引用还是禁止重复。
- Impact: “字段集合相等”测试不可能同时满足现有基准和子任务清单；re-audit 的
  evidence delta 没有稳定输入合同。
- Route: 在 design 中选择共享核心+扩展、版本化转换器或严格复用其中一种，并规定
  finding 与 claim-evidence 的字段所有权；随后让父任务、子任务、schema 测试和
  re-audit 输入引用同一份 canonical definition。

### TPR-08 · 阻断 · re-audit 五态缺少可执行的状态转移与身份规则

- Location: re-audit `prd.md:22-39,61-78`。
- Claim: 新源、旧 findings/ledger 能稳定区分 `addressed`、`partial`、
  `unresolved`、`new`、`regressed`，并输出 evidence delta。
- Evidence: PRD 只规定以 `root_cause_key` 比较；未定义 source span 移动、根因拆分/
  合并、证据强度升降与 ledger 历史如何映射五态。五例 fixture 的 AC 只枚举
  `unresolved / addressed / new 或 regressed`，没有 `partial` 的明确 gold；R2 又把
  “应用旧 patch”的写行为放进只读 re-audit 子任务，但没有说明调用 mode 层还是本脚本
  拥有该动作。
- Impact: 不同实现可在同一输入上给出不同状态且都声称满足 PRD；`partial` 和
  `regressed` 无法形成稳定回归测试，权限边界也可能倒置。
- Route: 增加输入版本、identity/transition table、拆分合并策略和每态最小 fixture；
  明确 re-audit 只报告过期 patch，还是调用 mode 层执行阻断，避免形成第二个写入 owner。

### TPR-09 · 阻断 · output-eval 可以只通过 schema/fixture 形状测试而没有执行证据

- Location: output-eval `prd.md:12-18,22-45,67-100`。
- Claim: E1—E9 将证明结构、保源、证据强度和假阳性四个质量面，且 E1—E3 能报告
  带分母和标注版本的 TP/FP/FN。
- Evidence: scope 只新增 `evals.json` 字段、fixture 和一个 pytest 文件，没有规定
  runner/adapter 如何从 case 调用真实 workflow、如何捕获原始输出、如何持久化
  denominator/version/report。R1 虽给 `baseline_output`/`with_skill_output` 字段，
  R2 又只落地 recorded_fixture 与 deterministic_run；没有可审阅机制防止测试只检查
  字段存在和预填 expected 值。OpenAI GDPval 把专家盲比较和 rubric 作为独立证据，
  Qiaomu/output-eval 方法也把静态 fixture 与执行证据分层，二者都不支持把形状测试
  当作输出质量结果。
- Impact: 所有新增测试可能全绿，但“skill 输出更好”、假阳性统计和人类可用性仍未
  被执行；核心子任务会把计划证据误报为结果证据。
- Route: 增加确定性 repo-native runner、原始输出/命令/版本的证据落点和禁止自证的
  测试；或把本子任务的结论明确缩窄为 schema+fixture 准备，并把实际 output eval
  另设 gate。继续保留 provider/human 为 `missing evidence`，无需推翻已定范围。

### TPR-10 · 阻断 · visible-prose 的执行与回滚命令不能保护当前用户改动

- Location: visible-prose `implement.md:7-21,47-48,109-119`；仓库当前工作树；
  `.trellis/workflow.md` 的提交阶段。
- Claim: S1 能冻结干净基线，各阶段可独立提交/回滚且不影响其他改动。
- Evidence: 当前 `dev` 工作树已含用户的 `.trellis` 修改和新增任务；
  `git status` “只显示 `.trellis/` 与 fixture”不能区分本任务与原有 dirt。
  `ruff format .` 会修改全仓库格式面；回滚表直接使用 `git checkout`；“每阶段独立提交”
  与 workflow 的统一变更识别、确认和分批提交步骤不一致。
- Impact: 按计划执行可能把无关 `.trellis` dirt 混入提交、格式化无关文件，或用回滚
  命令覆盖用户改动；基线证据也不再能归因到本任务。
- Route: 在 implement 中记录并排除现有 dirt，所有格式化/暂存/回滚使用明确文件清单
  和非破坏性恢复方案；提交节奏遵循当前 Trellis workflow，除非用户另行授权。

### TPR-11 · 应修 · mode 的强制产物与无输出路径降级没有统一调度前置条件

- Location: mode-contract `prd.md:31-45,90-110`。
- Claim: 每种 mode 的必须输出可机器断言；无授权输出路径时返回摘要与建议文件名；
  “优化/润色”可按授权语义推断 plan 或 revise。
- Evidence: 表中 diagnose/plan/re-audit/gate 都要求文件产物，随后又允许无路径时只返
  摘要；未定义 stdout 是否算合同产物。显式 `--mode revise`、自然语言“优化”、
  源写授权和报告目录授权的优先级/退出码也未给出。
- Impact: CLI、agent 路由和测试可分别实现不同降级逻辑，造成相同请求在不同入口下
  权限和产物不一致。
- Route: 在 design 中给出输入优先级与输出 destination 状态表，并分别覆盖显式 mode、
  模糊请求、无 report 路径、无 source 写授权四类 fixture。

### TPR-12 · 应修 · “推荐/禁止同族套语冲突”的证据被写成已验证直接冲突

- Location: rule-governance `prd.md:45-55,99-103`；父任务
  `research/evidence-audit.md:126-135`；现有 `writing-philosophy-zh.md:49`、
  `academic-style-zh.md:87`、`deai/tone-thresholds.yaml:49-60` 和
  `scripts/deai_check.py` 的 throat-clearing 判定。
- Claim: “基于上述分析”一边被推荐，一边被 deai 同族规则禁止；
  throat-clearing 的既有阈值 2 是已判定锁点。
- Evidence: 精确短语“基于上述分析”不在当前 regex 表；现有脚本对命中的
  throat-clearing pattern 逐条产生 finding，没有名为 throat-clearing=2 的阈值。
  父任务证据审计也承认精确短语未列入表，只依据“同族”推导冲突。
- Impact: 治理方向可能合理，但当前事实不足以证明一个可复现的双重判定，且“阈值 2”
  会让字节锁/测试保护不存在的合同。
- Route: 先用当前 analyzer 对最小 fixture 复现真实冲突，再决定是修指南、补
  `applies_when` 还是仅消除语义张力；把 pattern、burstiness 阈值和触发计数分开描述。

### TPR-13 · 提示 · 当前范围是项目原生 P0/P1，不应标成 Qiaomu Library-ready

- Location: 父任务 `prd.md:34-45`；外部质量手册的 Library 目标段；
  `qiaomu-meta/references/{skill-ir-method,gate-selection,output-eval-method}.md`。
- Claim: 本轮按用户决策不新增 README/接口报告目录，不执行 provider A/B、人工盲评，
  以项目原生闭环为目标。
- Evidence: 决策在父任务中写明；Qiaomu 的 Library gate 另外要求可移植 Skill IR、
  trust/licensing、owner 与执行/输出证据。缺少这些证据不违反本轮已定范围。
- Impact: 若 closeout 使用“Library-ready/已完成 Qiaomu 评测”措辞，会把主动延期的
  portability/trust/provider/human 证据误报为已满足。
- Route: 保留用户已经确定的范围，只在任务状态和最终文案中使用“project-native
  P0/P1 closure”等有界表述，并把 Library/provider/human 明列为未来 gate 或
  `missing evidence`。

### TPR-14 · 提示 · 预检仍有 15 处裸路径/行号引用歧义

- Location: visible-prose、mode-contract、rule-governance 等 PRD/design 中的
  `SKILL.md:...`、`routing-rules.md:...`、`tone-thresholds.yaml:...` 引用。
- Claim: 路径/行号足以让实现者定位唯一源文件。
- Evidence: 7 次 `plan_precheck.py` 合计报告 15 条 ambiguous citation；同名文件在
  skill/reference/docs 镜像中并存，裸文件名无法稳定确定 owner。
- Impact: 当前多数引用可人工推断，但后续文档镜像重建或行号漂移后容易核验错副本。
- Route: 改为 repo-relative 完整路径，并优先锚定声明/符号而非易漂移的正文行。

### TPR-15 · 提示 · 任务元数据未解释分支和 package/scope 路由

- Location: 7 个 `task.json`；仓库当前分支。
- Claim: 任务可按 Trellis 元数据选择基线、规范与实现上下文。
- Evidence: 7 个任务均为 `base_branch=main`、`branch=null`、`dev_type=null`、
  `scope=null`、`package=null`，而当前工作分支为 `dev` 且含未提交 Trellis dirt。
- Impact: 不一定改变产品设计，但未来 diff 基线、规范注入和 closeout 归属可能因默认值
  得到不同结果。
- Route: 在任务说明中记录为何以 main 为基线并在 dev 上规划，或补齐 Trellis 能识别
  的 package/scope；不要在未核对现有 dirt 前自动创建/切换分支。

## 未能核实

- IR、artifact、mode、re-audit、governance 和 output-eval 的真实运行效果 — 相关实现
  尚未存在；只能审阅计划机制。
- Windows 原生 PowerShell console、重定向 pipe、CI 和测试替身四种编码路径 — 本轮
  只复算了计划中的 pipe 复现条件并核对 Python 官方语义，未进行原生 GUI/console
  矩阵验证。
- 真实论文上的章节角色精度、词项误报率、TP/FP/FN、PDF 视觉质量 — 用户决定本轮
  不使用真实论文/人工标注，这些应保持 `missing evidence`。
- provider-backed A/B 与 human blind review — 明确不在本轮范围，不能由 fixture、
  pytest 或自动 grader 替代。
- 跨平台安装、安全扫描、外部先例的运行时质量 — 只阅读公开文档/仓库，没有安装或
  执行第三方实现。
- Pass 7 implementation drift — 7 个任务状态均为 planning，尚无已启动实现可比较。

## 可靠部分

- 父任务把 6 个子任务、依赖顺序和单写者/串行提交约束集中列出；除本报告指出的
  schema/验收缺口外，依赖方向没有发现循环。
- evidence audit 对当前 V1/V2/V3 的核心实现位置判断成立：过程章默认选择、
  单行 visible-text 投影和 raw count threshold 均能在现有代码找到。
- 不直接修改 hash-locked `parsers.py`，而以 source-mapped visible-prose IR 提供新投影
  的方向符合现有 contract 边界；但其正确性仍待 TPR-03/04 闭合后验证。
- protected token、数值、单位、cite/ref/label、数学环境、generated owner、
  source hash、claim-strength non-escalation 和默认 dry-run 的保护面彼此一致，值得保留。
- 文档资源要求同时更新 manifest、英文/中文镜像并单独执行 `just doc-build`，与仓库
  现有 docs resource-sync 结构一致。
- 仓库复算确认 docs 英文/中文各 54 个资源文件（合计 108）、`evals.json` 31 个 case、
  `trigger_eval.json` 39 个查询；这些父任务约束可继续作为防回归基线。
- visible-prose 的真实 manifests 所列生产/测试路径均存在；问题是 AC 追踪和设计矛盾，
  不是路径不存在。
- 7 个任务的 `task.py validate` 均通过，说明 YAML/JSONL/目录骨架可解析；本报告只反对
  把这种结构通过解释为实现 readiness。

## 网络搜索与先例校准

| 先例 | 采用/调整/拒绝 | 对本规划的约束 |
| --- | --- | --- |
| [Microsoft Agent Skills 官方文档](https://learn.microsoft.com/en-us/agent-framework/agents/skills) | 采用 progressive disclosure 与 scripts/references 分层；调整为本仓库 manifest/docs 机制 | 支持保持根 `SKILL.md` 精简，但不能替代输入验证、资源边界和执行证据 |
| [OpenAI GDPval](https://openai.com/index/gdpval/) | 采用“自动评分与专家盲评证据分层”；本轮不执行盲评 | 支持把 human/provider 明列 `missing evidence`，不能让 pytest 形状测试代替人类可用性 |
| [yaojingang/yao-meta-skill](https://github.com/yaojingang/yao-meta-skill) | 调整其 output execution/recorded output 思路为 repo-native deterministic runner；拒绝照搬通用交付仪式 | 静态 fixture、执行原始输出、provider 和人工证据必须分层，且 runner/版本/分母要可追溯 |
| [andrehuang/academic-writing-agents](https://github.com/andrehuang/academic-writing-agents) | 采用 review-before-act 与 human-in-the-loop 原则；拒绝多 agent roster 作为本轮必需架构 | 支持 module × mode 和授权边界，不支持为当前单 skill 增加无证据的编排复杂度 |
| [Brandon030722/academic-writing-skill](https://github.com/Brandon030722/academic-writing-skill) | 仅采用来源层级/证据优先的概念；不把仓库自述当效果证据 | 可校准 evidence intake 词汇，但 provenance、license 和 output eval 不足以支撑直接移植 |

Qiaomu gate 的结论是：保留本任务已确定的 project-native 范围；补足 Production+ 所需的
trigger/output 执行证据；不要在缺少 portability、provider/human 与 trust 证据时宣称
Library-ready。source-mapped visible-prose IR 属于针对 LaTeX 论文的本地创新假设，
在当前先例短名单中未见同构实现，但这不是效果或新颖性证明。

## 盲区

An agent reviewing an agent's plan is not an independent second opinion. The reviewer and the
author share most of the same blind spots. A clean report means "this pass found nothing", not
"the plan is complete". Treat the findings as a triage list, not as an approval.
