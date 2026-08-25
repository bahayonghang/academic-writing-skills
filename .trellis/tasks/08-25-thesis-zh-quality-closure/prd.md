# latex-thesis-zh 质量闭环优化（P0 + P1）

## Goal

按 `ref/latex-thesis-zh-skill-optimization-plan.md` 的 P0 与 P1 两层，把
`academic-writing-skills/latex-thesis-zh` 从「散装诊断规则」改造为可追踪的质量闭环：
共享可见正文 IR → 语义中间产物 → mode 契约与受控改写 → re-audit / gate，
并治理规则冲突与升级 output eval。

本轮完成口径是 **project-native P0/P1 closure**。不把本轮标成 Qiaomu
Library-ready，也不把未执行的 provider/human 评测写成已完成。

## 规划工件索引（父任务持有，子任务勿重复调研）

- `research/evidence-audit.md` — 手册每条主张在**本仓库副本**的取证结果：
  V1-V9 已复现缺陷（含实跑命令与输出）、C1-C7 本仓库集成面硬约束、
  paper-audit 可适配面、未取证项清单。

## 手册审阅结论（实施前必读）

手册的诊断方向成立，`path:line` 锚点逐条命中本仓库副本，但有三处必须修正：

1. **E1 症状描述错误。** 手册称控制行、跨行公式、figure 环境被 deai「报为平行句式
   或标点候选」——实跑零 finding，该断言在当前代码上恒为真，起不到回归防护作用。
   真实泄漏是生成表格单元格与公式 `\text{}` 内的中文进入文档级词频计数
   （`PRESERVE_PATTERNS` 是单行正则，跨行环境体不被剥离）。E1 按
   `research/evidence-audit.md` V3 重写。
2. **手册对本仓库集成面是盲的。** 七处硬约束（C1-C7）改动必踩，手册一处未提。
   C7（`test_deai_alignment.py` 的 AST 逻辑锁 + typst 值锁）直接决定
   「调 deai 阈值」方案的可行落点。手册写的测试目录
   `tests/latex_thesis_zh/` 路径错误，本仓库是 `tests/skills/latex_thesis_zh/`。
3. **聚合数字与本副本分叉**（100 文件 / md 4911 / py 13375 vs 98 / 6497 / 15238）。
   手册的规模数字不得进入任何验收标准。

## 已定架构决策（2026-08-25，用户裁决）

1. **任务树覆盖 P0 五项 + P1 四项，六个子任务。** 不含 P2（包瘦身、外部先例补研、
   telemetry、发布治理）。
2. **不纳入 Qiaomu Library 仪式性产物。** 不新建 skill 包内 `README.md`、
   `agents/interface.yaml`、`reports/{skill-ir,creation-handoff,prior-art-research,output-evidence}.json`。
   理由：本仓库人类入口在 `docs/skills/<skill>/index.md` 双语页面；`agents/` 下
   只有 `openai.yaml` 且被 `test_openai_yaml_shape` 锁定；skill 包内无 `reports/` 先例。
   手册 §12 Phase 5-6 的 provider A/B、人工盲评、发布流程同样不在范围内。
   本轮状态与终检文案使用 **project-native P0/P1 closure**；Library-ready、
   可移植 Skill IR、trust/licensing、provider A/B、人工盲评保持 **missing evidence**，
   不在 closeout 中写成已满足（TPR-13）。
3. **共享 IR 落地为新增 `scripts/visible_prose.py`，不动被哈希锁定的
   `parsers.py` 成员。** `LatexParser.PRESERVE_PATTERNS` 被
   `tests/contracts/test_parsers_alignment.py:84` 以 md5 锁定跨 en/zh/audit/cover_letter
   四副本；改它会波及另外三个 skill。IR 从 `tex_loader.AssembledDocument` 构建，
   旧 `extract_visible_text` 保留为兼容视图。
4. **写入面默认 dry-run。** `revise` mode 只有显式授权才产生 source patch；
   本任务只改 skill 包与测试，不改任何用户论文。
5. **子任务串行，manifest 单写者。** 每个改 references 的子任务在自己的提交内
   重建 `docs/resource-manifest.json` 并保持该提交 CI 绿；并行会互相覆盖。

## 任务图与依赖

| 顺序 | 子任务 slug | 交付物 | 依赖 |
| --- | --- | --- | --- |
| 1 | `08-25-thesis-zh-visible-prose-ir` | `visible_prose.py` typed node IR；章节角色分类器（修 V1）；阈值按可见字数归一（修 V2）；生成/表格/公式节点排除（修 V3）；CLI UTF-8 自设（修 V4）；`deai_check` 与 `--process-chapter` 先迁移 | 无 |
| 2 | `08-25-thesis-zh-semantic-artifacts` | artifacts schema + `artifacts.py`（稳定 ID、根因合并、JSON/JSONL IO）；thesis/interface/claim-evidence/result-question 四张 map；logic/literature/experiment 输出 artifact refs | 子任务 1 |
| 3 | `08-25-thesis-zh-mode-contract` | 五 mode 正交契约；`thesis_workflow.py` orchestrator；受控改写 ledger 与 fidelity gate；SKILL.md / routing-rules.md / openai.yaml 更新 | 子任务 2 |
| 4 | `08-25-thesis-zh-re-audit-gate` | `re_audit.py` 根因感知状态 diff；gate 五态语义（pass/fail/skipped/missing evidence/no_script_finding） | 子任务 3 |
| 5 | `08-25-thesis-zh-rule-governance` | writing-philosophy-zh 规则分级与适用条件（修 V7，含跨文件规则冲突）；over-claim-guard 区分性证据门禁（修 V8） | 子任务 1（不依赖 2-4） |
| 6 | `08-25-thesis-zh-output-eval` | `evals.json` 加字段升级（保 C2 四键）；E1-E9 脱敏 fixture；确定性 runner 与执行证据落点 | 子任务 1-5 |

依赖写入各子任务 PRD。子任务 5 与 1 之外无依赖，可在 2-4 进行中并行规划，
但提交须串行（manifest 单写者）。

父任务不做直接实现。父任务从 `planning` 进入 `ready` 的前置：六个子任务均已具备
`design.md`、`implement.md`、非占位 `implement.jsonl`/`check.jsonl`，且各自
`plan_precheck.py` 无 blocking、无 undefined R/AC 引用（TPR-02）。本轮修订规划
不运行 `task.py start`。

## 任务元数据（TPR-15）

- 七个任务 `base_branch=main`：PR 目标为 `main`。当前工作分支是 `dev`，本轮只在
  `dev` 上规划与实现，不自动创建或切换分支。
- `dev_type` / `scope` / `package` 保持空值：规范注入以
  `.trellis/spec/academic-writing-skills/` 与各子任务 manifest 为准，不靠
  `task.json` 空字段推断。
- 规划时工作树已有与本任务无关的 dirt，清单见子任务 1 `implement.md`「既有
  dirt 冻结清单」。实现、格式化、暂存、回滚、提交不得纳入该清单中的路径。

## Requirements

- R1：V1-V4 四项已复现缺陷各有回归测试；测试在改造前失败、改造后通过。子任务 1
  须先提交 failing test，或在其 design.md 记录改造前实跑输出。
- R2：V3 的验收断言按 `research/evidence-audit.md` V3 写，不按手册 E1 原文。
- R3：C1 不被破坏：`tests/contracts/test_parsers_alignment.py` 全绿，
  `ALIGNMENTS` 表未新增 ZH 分歧项（若必须新增，须在子任务 1 design 中说明理由）。
- R4：C2 不被破坏：`evals.json` 保留 `{id, prompt, expected_output, files}` 四键，
  case 数不减。
- R5：C3 不被破坏：路由表每条命令的 `--flag` 均在对应脚本 `--help` 中。
- R6：C4 每个改 references 的子任务在自身提交内完成 manifest 重建 + 双语页面；
  父任务终检重建一次并验证零漂移。
- R7：C5 六个 SKILL.md `version` 仍为 `6.0.0`，只改 `last_updated`。
- R8：C6 新测试位于 `tests/skills/latex_thesis_zh/`。
- R9：C7 不被破坏：`tests/contracts/test_deai_alignment.py` 全绿；
  `term_thresholds` 的 11 个 CJK 词 cap 值、`_iter_visible_lines`、
  `_apply_tier` 字节不变（详表见 `research/evidence-audit.md` C7）。
- R10：finding schema 以子任务 2 `references/schemas/artifacts.md` 为唯一
  canonical definition。采用共享核心 + 已声明扩展，不要求与
  `academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md` 字段集合相等。
  共享核心含 `root_cause_key`、`source_kind`、`confidence`、`missing_evidence`。
  `claim_strength` 与 `evidence_anchor` 的 owner 是 `claim-evidence.json`；
  finding 只保留只读嵌套对象 `claim_snapshot`，禁止顶层第二套可写强度/锚点。
  不引入投稿评分、多评审委员会、desk-reject gate（TPR-07）。
- R11：旧 analyzer 的兼容面拆成两类合同，不得用一条「行为不变」覆盖（TPR-05）：
  （1）严格不变面：未迁移通道的 CLI 命令、flag、help 文本、exit 语义、人类可读
  行格式；（2）已批准语义差异面：V1 章选择/章引言覆盖、V2 词项阈值公式、V3
  计数口径、finding 去重键。差异面须有逐项 golden delta。
- R12：`just ci` 全绿 **且** `just doc-build` 成功（ci 不含 doc-build，需单独跑）。
- R13：报告中 provider 对照、人工盲评、真实 precision/recall、外部 prior-art、
  跨平台兼容、安装验证、Windows 原生 console 编码一律标 **missing evidence**，
  不以计划冒充结果。终检文案使用 project-native P0/P1 closure。
- R14：`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`（既有红线，不得被新 mode
  绕过）。
- R15：六个子任务均通过预检后，父任务才可进入 ready；父任务终检执行本文件
  AC1-AC16，不直接改生产代码。

## Acceptance Criteria

- [ ] AC1（R1）：V1-V4 四项已复现缺陷各有回归测试，且测试在改造前失败、改造后通过
- [ ] AC2（R2）：V3 的验收断言按 `research/evidence-audit.md` 写，不按手册 E1 原文
- [ ] AC3（R3）：`tests/contracts/test_parsers_alignment.py` 全绿，`ALIGNMENTS`
      表未新增 ZH 分歧项
- [ ] AC4（R4）：`evals.json` 保留 `{id, prompt, expected_output, files}` 四键，
      case 数不减
- [ ] AC5（R5）：路由表每条命令的 `--flag` 均在对应脚本 `--help` 中
- [ ] AC6（R6）：每个改 references 的子任务在自身提交内完成 manifest 重建 +
      双语页面；父任务终检重建一次并验证零漂移
- [ ] AC7（R7）：六个 SKILL.md `version` 仍为 `6.0.0`，只改 `last_updated`
- [ ] AC8（R8）：新测试位于 `tests/skills/latex_thesis_zh/`
- [ ] AC9（R9）：`tests/contracts/test_deai_alignment.py` 全绿；
      `term_thresholds` 的 11 个 CJK 词 cap 值、`_iter_visible_lines`、
      `_apply_tier` 字节不变
- [ ] AC10（R10）：schema 测试对照子任务 2 的 canonical definition（共享核心 +
      扩展映射表 + `claim_snapshot`），不断言与 paper-audit 字段集合相等；
      finding 顶层无独立 `claim_strength`；未引入投稿评分 / review_lane /
      desk-reject
- [ ] AC11（R11）：严格不变面由未迁移通道快照证明；V1-V3 与 finding 去重的
      已批准差异由逐项 golden delta 证明
- [ ] AC12（R12）：`just ci` 全绿且 `just doc-build` 成功
- [ ] AC13（R13）：provider 对照、人工盲评、真实 precision/recall、外部
      prior-art、跨平台兼容、安装验证、Windows 原生 console 编码标
      **missing evidence**；终检文案为 project-native P0/P1 closure
- [ ] AC14（R14）：`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`
- [ ] AC15（R15）：六个子任务均有 design/implement/真实 manifest，且预检无
      blocking、无 undefined R/AC 引用后，父任务才进入 ready
- [ ] AC16（R10, R11, R13）：re-audit 消费同一 canonical finding；output-eval
      的执行证据与 schema 形状测试分层；Library-ready 未写入完成状态

## Constraints

- 红线：不修改 `\cite{}` / `\ref{}` / `\label{}` / 数学环境内容；不虚构文献与实验
  数据；不改保护术语
- 本任务只改 `academic-writing-skills/latex-thesis-zh/`、`tests/`、`docs/` 镜像面；
  不改其余五个 skill 的脚本与 references（除 C1 哈希锁要求的同步）
- 不改构建配置（`justfile`、`pyproject.toml`、CI workflow）——除非子任务 PRD 显式
  授权并说明理由
- `evals.json` 修改走 Bash python 写入（Edit/Write 会触发 JSON 格式化 hook 压平数组）
- 不修改用户论文源文件；`revise` mode 的写入能力只做到「默认 dry-run + 白名单校验」，
  本任务不对任何真实论文执行写入
- 父任务不做直接实现，只做规划、跨子任务验收与终检
- 实现阶段的格式化、暂存、回滚、提交只作用于该子任务文件清单，排除「既有 dirt
  冻结清单」（TPR-10）

## 修订记录

- 2026-08-25 初版：基于手册 + `research/evidence-audit.md` 取证结果建立六子任务树；
  修正手册 E1 症状、补齐 C1-C7 集成面、剔除与本仓库约定冲突的 Library 产物。
- 2026-08-25 审阅返回：按 TPR-01 建立 R/AC 稳定 ID；按 TPR-02 规定 ready 前置；
  按 TPR-05/07/13/15 修订兼容面、schema 真源、closeout 口径与分支元数据说明。
  同日补核：TPR-03 B1 含成果章；TPR-07 `claim_snapshot`；TPR-08 有序转移表与
  F6/F7；TPR-09 E1-E9 合同表；TPR-11 destination 全表；TPR-12 精确短语零
  deai finding。本轮仍为规划修订，不是实现批准。
