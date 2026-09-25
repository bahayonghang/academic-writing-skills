---
skill: trellis-plan-review
version: 0.5.0
task_dir: D:/Documents/Code/Agents/academic-writing-skills/.trellis/tasks/09-10-paper-audit-zh-thesis-fidelity
task_name: 09-10-paper-audit-zh-thesis-fidelity
task_status: planning
review_scope: single-task
task_count: 1
task_members:
  - 09-10-paper-audit-zh-thesis-fidelity
task_statuses:
  09-10-paper-audit-zh-thesis-fidelity: planning
verdict: 可执行
blocking: 0
should_fix: 0
notes: 0
generated_at: 2026-09-10T22:03:00+08:00
---

# Trellis 规划审阅报告

## 审阅范围

- 根任务：`09-10-paper-audit-zh-thesis-fidelity`
- 模式：`single-task`
- 任务数量：1
- 有序成员（根优先；顺序不代表依赖）：`09-10-paper-audit-zh-thesis-fidelity` — `planning`
- 当前 HEAD：`41c0cf7447989391e96a3bd79c8e7e697cf8d0f6`，与 `task.json.meta.planning_head`、PRD、design 一致。
- 已读 `task.json`、PRD、design、implement、两份 JSONL、`research/audit-chain.md`、`research/probe-results.json`、场景合同、先例报告，以及引用的当前源码、工作流和相关 spec。旧归档任务不属于本审阅的成员；历史写作验收不能替代本任务验收。
- 权限为只读审阅；唯一持久写入是本报告。未修改规划或产品，未启动、实现、提交、归档本任务，未安装依赖或执行远程写入。

## 结论

可执行 — 阻断 0 / 应修 0 / 提示 0

**GO：规划具备进入后续授权实施的条件。** 本结论不授予实施权限；当前仍应保持 `planning`，按 `implement.md:5` 等待用户明确实施指令后才可 `task.py start`。本次没有发现需要修订的规划问题，不应为产生修改而重写计划。

## 问题清单

无。

## 未能核实

- 新旧审稿规则对 E01—E08、E12、E15 的实际模型输出及独立语义核读结果：本任务尚未实施，也尚未采集该组 before/after reviewer 原始响应。计划在 `implement.md:9` 明确先采旧响应，在第5步采新响应；这些 AC 保持未完成，不能以现有 probe、eval JSON 或历史写作输出替代。
- 真实学位论文的总体审查质量、真实盲评收益、学校版式与现场验收、五宿主 fresh-session/provider benchmark：无本次实际效果证据，继续 `UNVERIFIED / missing evidence`。PRD 已明确其不属于本增量任务新增完成门槛。
- 第三方先例的实际效果与安全性：本次独立审阅未运行第三方技能。先例报告只把其设计作为参考，未据人气或源码可读性声称效果优越；这不构成计划缺陷。

## 可靠部分

### Pass 0：机械预检与基线

本次实际运行：

```powershell
rtk proxy python -X utf8 C:/Users/lyh/.agents/skills/trellis-plan-review/scripts/plan_precheck.py .trellis/tasks/09-10-paper-audit-zh-thesis-fidelity --include-descendants
```

返回 exit 0：一个成员、零阻断、12处引用均可解析，R1—R5 与 AC1—AC5 可追溯，无 `_example` 等阻断残留。目标报告路径被 Git 忽略。每份 JSONL 均为真实 spec/research 条目。

当前 Git HEAD 与规划基线一致。记录的五份 probe 源码 SHA-256 与当前工作树逐一匹配，涉及 `audit.py`、`zh_check_adapters.py`、`prepare_review_workspace.py`、`consolidate_review_findings.py` 和中文 `check_consistency.py`。复用了研究者本轮实跑的原始 stdout/stderr/返回码与输入，没有把它描述为独立重跑，更未重跑整套1908测试来替代本任务的效果验证。

### Pass 1—2：事实、推论与调用链

| 核对对象 | 当前源码及观察 | 审阅结论 |
| --- | --- | --- |
| consistency CLI/adapter | `audit.py:2744`、`:2762`、`:2768`、`:2800`；`zh_check_adapters.py:392`；中文 `check_consistency.py:435`、`:459`、`:498`、`:509` | 调用已走既有 producer，缺 consistency 具名 adapter；现有 `--json` 确有固定 INFO 前导、单个 JSON，正常有问题 exit1。D2 无需新 checker 或泛型协议猜测。 |
| clean 伪问题与量化效应 | probe `cases.clean` 有10条 Minor；`scholar_eval.py:62` 为0.5，`:71` 将 CONSISTENCY 归 clarity | 独立送入 ScholarEval 后 `10 - 10 × 0.5 = 5`；这是该组伪 finding 的维度效应，计划未外推整篇论文总分。 |
| Info 两套评分 | `report_generator.py:340`—`:353` 对 Info 使用默认0.25扣分；`scholar_eval.py:154` 已过滤 Info；probe `info_scoring` 的 clarity 为6→5.75和10不变 | D2 修四维评分入口、只回归 ScholarEval，符合实际所有权；无需更改权重或扣分表。 |
| 返回码和解析失败 | `audit.py:637`—`:668` 当前对正常exit1追加Minor；AdapterParseError现有类型在 `zh_check_adapters.py:75` | D2 同时覆盖正常exit0/1、非法JSON、exit2与超时，避免仅补adapter却遗留伪错误；错误政策被限定在 consistency 分支。 |
| Info→deep/gate | `audit.py:422`、`:588`、`:1362`；`export_phase0_context` 包含Info；probe `presubmission_promoted=[]` | CONSISTENCY不在gate eligible，现有PRESUBMISSION筛选只接受Critical/Major。D2保留Info到Phase0/quick/JSON，禁止直接sanitize为moderate，且不扩展gate。 |
| zh首用清单 | `audit.py:2201`—`:2244` 包含白名单、任意位置定义、≤3容差；probe late_definition中checker失败但清单passed=true | 删除zh `.tex`重复项有证据；保留EN/Typst路径并避免新造false ChecklistItem，是最小且一致的机制。 |
| 全文与装配 | `prepare_review_workspace.py:871`—`:896` 读入口，`:701`仅子节装配；`:898`—`:924`构造section/claim map；`audit.py:2042`使用full_text核验quote | D3在`.tex`读取边界装配一次并传递同一对象，覆盖全文、语言、分节、claim map和子节窗口；含英文`.tex`回归，避免先判中文的循环。 |
| 源坐标 | `prepare_review_workspace.py:259`—`:272`用`origin`返回源位置；`audit.py:1315`—`:1327`按section坐标映射PRESUBMISSION | D3明确装配坐标与原文件坐标不可互换，并点名PRESUBMISSION消费者复核；现有origin/summary足以承载，不要求改schema/parser/loader。 |
| summary及覆盖 | `prepare_review_workspace.py:821`会写summary stub；`:938`在工作区准备末尾调用 | D3明确在stub之后持久写入可达文件和warning_lines，经模板输入与最终报告披露，full_text不混警告。 |
| 路径与资源 | `paths.py:67`、`:131`、`:137`、`:145`；consolidator `:191`；zh agent `:22`；`_copy_workspace_references`清单`:836` | 文档旧根目录和canonical目录存在实际冲突，probe同一评论消费0/1相符。D1统一现有路径并只补两份必要规则；上位claim契约已经复制，无兼容层或全量复制。 |
| reviewer语义规则 | `OVER_CLAIM_GUARD.md:52`、`:59`、`:108`、`:117`；claims agent `:14`、模板对应lane；中文准则15行 | 因果和首次具体模板确有需要校准的可达规则。D1保留强证据、理论和合法综合反例，不把规则冲突说成已发生的真实模型错误。 |
| 实际模型运行边界 | `audit.py:1962`明确deterministic fallback；实际深审调用在`:2024`、`:2027` | 计划另用现有native/sequential reviewer采样并保存原始响应，不把fallback、结构测试或同agent批次宣称为独立人工审查。 |

表中产品路径共同前缀为 `academic-writing-skills/paper-audit/scripts/`；明确写“中文”的 `check_consistency.py` 属于 `academic-writing-skills/latex-thesis-zh/scripts/`，Markdown位于paper-audit对应references/agents目录。所有行号均对当前规划基线核对。

### Pass 3：逐 AC 子句→需求→机制

下表逐项列出可观察义务；同一行的并列结果共享所列机制，均已分别核对。这里只判断机制存在，没有把待执行AC打勾。

| AC子句 | 需求 | 设计/执行机制 | 可判定证据 |
| --- | --- | --- | --- |
| AC1：E01—E08/E12同输入旧新响应、独立核读、新版全满足 | R1/R5 | D1规则；implement第1/5步；场景执行方法第3/4步 | 保存各例原始响应；按必须/禁止结果逐例判分 |
| AC1：输入/规则hash与原始响应，合法反例可空issues | R1/R5 | implement证据表；场景方法第1/4/5步 | hash、调用材料、原始JSON；不以issue数当成功指标 |
| AC1：真实reviewer JSON经文档路径、consolidation及quote核验 | R1 | D1第三/四段；implement第4/5步 | 至少一例实际响应在canonical comments被消费并核验 |
| AC1：两份规则可读、原语言/focus保持 | R1 | D1最小复制清单与原lane条件 | 工作区文件读取及E16路由回归 |
| AC2：clean0、E10逐问题一次、原文件/行号正确 | R2/R3 | D2专属adapter；D3源坐标 | 真实producer→adapter正反输入及原位置断言 |
| AC2：E11 Info/P3、正常exit1无额外错误 | R2 | D2输入映射表与专属返回码分支 | NEEDS-LLM及coverage真实输出、exit0/1对照 |
| AC2：两套评分与空基线一致、gate不新增失败 | R2 | D2评分入口过滤、ScholarEval回归、gate集合保持 | 隔离Info评分对照与gate eligible回归 |
| AC2：Phase0/quick/JSON可见、deep不自动升级 | R2 | D2保留AuditResult、禁止直接sanitize、现有PRESUBMISSION筛选 | 各消费端可见性及不升级断言 |
| AC2：zh重复清单消失、EN/Typst不变 | R2 | D2 `lang=zh && fmt=.tex`条件 | 同输入分支对照及E16 |
| AC2：非法JSON、exit2、超时显式错误 | R2 | D2严格解析和错误路径；implement第2步 | 明确失败输出，不能判clean |
| AC3：子文件全文/section/claim map及quote通过 | R3 | D3统一assembled.content及现有verifier | E13含子文件专有正文/主张/原句 |
| AC3：同次装配一次、subsection源坐标不变 | R3 | D3传同一AssembledDocument、保留origin/_source_span | 装配次数与既有source坐标回归 |
| AC3：E14 summary警告、reviewer输入及最终限制披露 | R3 | D3 stub后写warning_lines；D1 summary读取；场景E14 | 缺include/includeonly等限制可见，不宣称全文已审 |
| AC3：单文件/英文多文件tex、Typst/PDF/overwrite回归 | R3 | D3格式读取边界，implement第3步 | 指定相关workspace/deep-review测试 |
| AC4：四类构建记录的不同判定 | R4 | D4作者构建记录语义审查；E15四子例 | 实际reviewer分别已证/不能通过/不能通过/UNVERIFIED |
| AC4：数值/路径不变、不启动TeX、不外推其它验收 | R4 | D4只审现有context；implement模型证据表 | 原始材料比对及工具调用记录，构建/质量分别陈述 |
| AC5：24 eval/20 trigger对象和顺序、追加唯一ID | R5 | D5 eval白名单；implement第1/5步 | 当前真实数组为24/20，历史对象前缀对照 |
| AC5：paper-audit/tests/contracts、资源单技能/全量、docs及四步CI | R5 | implement Validation Commands | 命令、exit及输出；manifest inventory不能替代双语完整门禁 |
| AC5：评分/维度/gate/schema/写作侧保护面 | R5 | D5只读名单及三组回滚 | 基线diff和保护面核对，不改已有producer或版本字段 |
| AC5：通过/失败/跳过/未验证分列 | R5 | implement证据表与Completion Boundary | 逐AC交付记录，能力缺失时语义AC仍未完成 |

R1—R5反向检查均有对应AC；E09由AC2 clean项承载，E16由AC1/AC2/AC3的语言分支回归及AC5保护面承载，未出现“有需求无验收”。E16中共享英文over-claim的事实保护仍属于R5全场景合同，需要在实施证据中保留相应对照；计划未把它排除。

### Pass 4—6：计数、范围与判据

- 实际JSON数组为24条历史eval、20条trigger；中文准则保留15行，基础评分维度8个。两条本次采样lane的现有上限均为8，E15明确拆为4子例，没有引入新的通过率、学校阈值或量化人气标准。
- D5的公开Markdown为5份references加2份agents，共7份，对应14份两语镜像；SKILL入口单独列入，资源manifest本来不登记SKILL。四个runtime文件足以承载D1/D2/D3边界，路径事实源、consolidator、quote verifier、ScholarEval、共享parser/loader与写作侧保持只读。
- 所有产品步骤均能落到白名单和现有接口；源冻结后再翻译，runtime/源规则串行、checker独立核读，避免同一`audit.py`并发修改。回滚以规则、适配/Info、工作区分组，不回退旧C1/C2/C3。
- `justfile:56`的CI确为check-versions、lint、typecheck、test四步；`doc-build`只调用现有npm构建脚本，不隐式安装。计划明确`uv --no-sync`、`UV_NO_SYNC=1`及工具缺失时暂停依赖步骤。
- 文档门禁与`.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`相符：源/同语镜像保真、另一语完整翻译、manifest、单技能/全量检查、build；新增fragment另核目标id，build不冒充fragment验证。
- 语义场景给出输入、必须结果和禁止结果，要求纯输入去除旧答案、before先于产品修改、按max8分批、原始响应不可改写、任何禁止结果即FAIL。存在可执行判分方法，不用关键词命中替代语义判断，也不要求本计划审阅提前完成产品验收。
- E15的“已证构建”限定为给定合成记录的审查判断；D4明示synthetic、无自动编译，未将一份synthetic构建记录当成本机真实TeX编译成功。

### Pass 7：实施漂移

不适用：唯一成员状态为`planning`。没有用尚未实施的计划项制造缺陷，也没有宣称实现验收已通过。工作树中原有`.gitignore`、`.trellis/.template-hashes.json`和`skills-lock.json`属于计划明确保护的既有改动，本审阅未修改它们。

## 盲区

Agent审阅另一Agent的规划并不构成独立的人类第二意见；双方可能共享盲点。零发现只表示本轮未发现问题，不证明规划完备，也不等于用户批准；后续实施仍须按原始响应、真实消费链和逐AC证据验收。
