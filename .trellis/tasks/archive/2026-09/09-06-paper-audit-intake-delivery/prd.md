# paper-audit 意图门控与交付形态治理

## Goal

把 codex 在实践中提出的 paper-audit 优化建议转化为可验收的改动：
用户已显式指定模式时不再被旧产物检测强制二次确认；
审查的交付形态按权限分级，禁止落盘时有可执行的对话审查路径；
已授权落盘时目标目录明确，不静默覆盖旧产物。

本轮只改 skill 文档层（`SKILL.md` 与三份 references）与其公开镜像，不改脚本 CLI、schema 或评分。

## Background

取证日期 2026-09-06，分支 dev，起始 HEAD 8000ffe，起始工作树干净。

codex 建议引用的路径是论文仓库部署副本
`D:/Documents/LYH/200-Learning/00博士毕业/毕业论文/thesis/.agents/skills/paper-audit/`。
已逐行比对，该副本与本仓库源文件内容一致，因此改动落在本仓库源，
部署副本由用户自行重装同步（用户 2026-09-06 明确选择"仅本仓库"）。

已复现的三处缺陷定位：

- `academic-writing-skills/paper-audit/references/MODE_GUIDE.md:30`
  `### Auto-Detection at Intake` 下四类检测（旧报告存在、修订标记、长文 polish、审稿信）
  均写成无条件"ask whether"，没有"用户已显式指定模式则跳过"的分支。
  `MODE_GUIDE.md:55` 的收尾句"let the user confirm or decline"同样无条件。
- `academic-writing-skills/paper-audit/SKILL.md:134`
  deep-review Phase 1 硬绑 `--output-dir ./review_results`；
  `scripts/prepare_review_workspace.py:952` 的 `--output-dir` 默认值同为 `./review_results`。
  文档没有区分"不得修改论文""不得写入仓库""完全不得落盘"三种约束，
  也没有禁止落盘时的替代审查路径。
- `academic-writing-skills/paper-audit/SKILL.md:61` 只声明了"不改论文源文件"一级边界。

已确认必须保留的项（codex 明确列为保留）：

- `academic-writing-skills/paper-audit/references/workflow-detail.md:6`
  工作区覆盖前的明确确认。
- `academic-writing-skills/paper-audit/references/MODE_GUIDE.md:24`
  re-audit 对 `--previous-report` 的依赖。
- `academic-writing-skills/paper-audit/SKILL.md:61` 审稿不改正文的授权边界。

已知约束：

- `tests/skills/paper_audit/test_paper_audit_synthesis.py:106` 锁定
  `MODE_GUIDE.md` 必须包含 `Auto-Detection at Intake` 小节，
  且该小节必须对审稿信输入 dispatch `revision_coach_agent`。小节不可删除，只能条件化。
- `tests/skills/paper_audit/test_zh_thesis_lane_wiring.py:27` 也读取 `MODE_GUIDE.md`。
- `docs/resource-manifest.json` 为 `MODE_GUIDE.md`、`workflow-detail.md`、`output-layout.md`
  各存了 `sourceSha256` 与 en/zh 两份镜像路径；
  `docs/scripts/check_resource_sync.py` 与 `tests/contracts/test_docs_bilingual_resources.py` 强制一致。
  `SKILL.md` 不在 manifest 中。
- 落盘行为已于 2026-09-06 实跑确认，结果见
  [write-behavior.md](../09-06-paper-audit-delivery-tiers/research/write-behavior.md)：
  `quick-audit`、`gate`、`re-audit` 不落盘；
  `polish` 落盘到 **论文文件所在目录** 的 `.polish-state/`（`scripts/audit.py:2509`），
  因此 polish 在 T2 就被挡住，不只 T3；
  `deep-review` 必然落盘（静态证据 `audit.py:2704`、`audit.py:1961-1968`、
  `prepare_review_workspace.py:952`），未实跑。
  实跑推翻了原先"polish 不建工作区"的静态推断。

## Requirements

- R1（意图门控）：用户已显式指定模式时直接执行该模式。
  旧报告、修订标记、文档长度、审稿信文件只作为上下文陈述一句，不构成模式选择题。
  仅当检测信号与已指定模式存在实质冲突（会改变审查范围或改变结论）时才提问。
- R2（保留项不削弱）：模式未指定时四类检测仍照常提问；
  覆盖既有审查工作区前仍有明确确认；
  re-audit 仍依赖前次报告，但路径可从现有上下文唯一确定时先自行查找并陈述，
  无法唯一确定时才停下只问该路径；审稿与正文修改的授权边界不变。
- R3（交付形态分级）：显式区分三级约束并给出每级允许与禁止的动作——
  T1 不得修改论文源文件、T2 不得写入仓库、T3 完全不得落盘。
  级别可由用户一句话选定，不需要逐步骤重新确认。
- R4（不落盘审查路径）：T3 下提供不依赖任何文件写入的审查路径；
  该路径下不创建 `review_results`；
  无法运行的必要脚本检查按名列出并声明证据缺失。
- R5（对话检查不冒充脚本验证）：对话级结论与脚本级结论在输出中可区分，
  复用现有 `[Script]` / `[LLM]` provenance，不新造标记体系。
- R6（输出目录明确）：已授权落盘时提示中显式给出目标目录路径；
  目标已存在同名产物时按 `workflow-detail.md` 现有规则确认，不静默覆盖。
- R7（不扩大权限）：本轮只收窄默认持久化写入。
  不新增自动写入、自动执行、自动联网行为；`allowed-tools` 不放宽；不新增依赖。
- R8（同步与证据）：改动的 references 同步 docs 双语镜像与 manifest 散列；
  新增可复跑的 eval 用例；`just ci`、`docs/scripts/check_resource_sync.py`、`just doc-build` 通过；
  按 qiaomu-meta 证据分层标注 design advantage / validated advantage / hypothesis，
  未取得的证据写 missing evidence，不以计划充当证据。

## Task Map

| 子任务 | 父需求 | 交付责任 |
| --- | --- | --- |
| 09-06-paper-audit-intake-gating | R1、R2、R8 | `MODE_GUIDE.md` Auto-Detection 条件化，及其镜像/manifest/测试同步 |
| 09-06-paper-audit-delivery-tiers | R3、R4、R5、R6、R7、R8 | `SKILL.md`、`workflow-detail.md`、`output-layout.md` 三级边界与不落盘路径 |
| 09-06-paper-audit-intake-delivery-verify | R8 及跨子任务 | eval 用例、`docs/skills/paper-audit/index.md` 说明、集成验收、证据标注 |

父任务拥有 codex 建议来源、跨子任务范围与合并验收，不直接实现产品。
公共文件所有权与串行顺序见 [设计](design.md) 与 [实施计划](implement.md)。

## Acceptance Criteria

- [x] AC1（R1）：用户明确要求 `quick-audit` 且论文目录存在 `*audit_report*` 文件时，
      按 `MODE_GUIDE.md` 新规则不产生模式二次确认；检测信号以一句陈述出现，不含选择题。
      → intake-gating 场景 S1 实测响应（validated）。
- [x] AC2（R1）：文档给出"实质冲突"的可判定定义，并至少含一个提问正例与一个不提问反例，
      两例的差别只在冲突是否影响审查范围或结论。
      → `MODE_GUIDE.md` 实质冲突三触发条件（Scope / Result / Delivery level）
      加旧报告反例与审稿信正例。Delivery level 为一致性核对 C1 补入。
- [x] AC3（R2）：模式未指定时四类检测仍提问；
      `test_paper_audit_synthesis.py:106` 的 `Auto-Detection at Intake` 与
      `revision_coach_agent` dispatch 两项断言继续通过；
      `workflow-detail.md` 覆盖确认段落保持存在。
      → 场景 S2 实测响应；`just ci` 1756 passed 含该两项断言。
- [x] AC4（R2）：`--previous-report` 缺失时，文档要求先在现有上下文中查找唯一候选并陈述；
      候选为零或多于一个时才停下只问该路径。
      → 唯一候选分支由场景 S4 实测；零候选／多候选分支仅文档规则（design，见交付说明）。
- [x] AC5（R3）：`SKILL.md` 含三级交付边界的显式区分，每级列出允许动作与禁止动作，
      且三级互不重叠、覆盖完整。
      → `Delivery Boundary` 节；互斥与完整性为 design advantage（文档结构自证）。
- [x] AC6（R4）：T3 下不创建 `review_results`；给出的审查路径不写任何文件；
      deep-review 在 T3 下不可用这一事实被明写，并给出降级选项与其能力差距。
      → 场景 D1 实测响应。deep-review 必然落盘这一前提仅有静态读码证据（design）。
- [x] AC7（R4）：T3 下无法运行的脚本检查按名列出（至少覆盖 consolidation、quote 校验、报告渲染三类），
      并统一标 `missing evidence`。
      → 按对抗核查 F4／N1 拆为两组：丢失证据的标 `missing evidence`，
      两个渲染器标"仅未产出"。**统一标记的原始表述已被否决**——
      把渲染器算作证据缺失会误报，见 delivery-tiers 核查记录 F4。
- [x] AC8（R5）：文档明确禁止用对话检查冒充完整脚本验证，
      并指明区分手段是现有 `[Script]` / `[LLM]` provenance。
      → 按脚本是否实际运行判定 provenance（对抗核查项 A 修正）；未新造标记体系。
- [x] AC9（R6）：已授权落盘时提示显式给出目标目录路径；不静默覆盖。
      → 场景 D2、D4 实测响应，均给出展开后的绝对路径并要求确认。
- [x] AC10（R7）：diff 中不新增自动写入、自动网络或自动执行；
      `SKILL.md` frontmatter 的 `allowed-tools` 与 `argument-hint` 未放宽；
      未新增运行期依赖。
      → 改动共 15 个文件（12 `.md` + 3 `.json`），零 `.py`；
      `SKILL.md` frontmatter 的 `allowed-tools`／`argument-hint`／`version` 零 diff；
      未触碰 `pyproject.toml`／lockfile；新增行中出现的 `subprocess`
      与 `--overwrite-workspace` 均为对既有行为的描述性说明，非新增行为。
- [x] AC11（R8）：`docs/resource-manifest.json` 中被改 references 的 `sourceSha256` 已更新，
      en/zh 两份镜像与源一致，`docs/scripts/check_resource_sync.py` 通过。
      → `resource contract passed: all resources (271 manifest entries)`，exit 0；
      `tests/contracts/test_docs_bilingual_resources.py` 随 `just ci` 通过。
- [x] AC12（R8）：`just ci` 与 `just doc-build` 通过；
      新增 eval 用例可复跑；实跑证据与仅静态证据在交付说明中分别标注。
      → `just ci` exit 0（`1756 passed in 117.28s`，含 check-versions／lint／typecheck／test）；
      `just doc-build` exit 0。新增 eval 用例的**形状与内容契约**可复跑（进 `just ci`），
      但其断言在真实模型输出上未跑过——仓库内无执行器，已记为 missing evidence。
      三档标注见 [交付说明](../09-06-paper-audit-intake-delivery-verify/research/delivery-notes.md)。

## Out of Scope

不修改论文仓库部署副本 `thesis/.agents/skills/paper-audit/`（用户已选仅本仓库）。
不修改任何 `scripts/*.py` 的 CLI flag、默认值、schema、评分或输出结构。
不新增 mode、不新增 agent、不新增 lane、不新增检查码族。
不改 `allowed-tools`、不新增依赖、不改 `pyproject.toml` 或 lockfile。
不改其他五个 skill。不修改或编译真实论文。
不提交、不推送、不发布、不归档——均另需授权。
不宣称本轮改动在真实论文审稿上的效果已经改善。
