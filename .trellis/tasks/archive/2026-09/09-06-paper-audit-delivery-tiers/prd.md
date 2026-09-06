# 交付形态分级与不落盘审查路径

父任务：[09-06-paper-audit-intake-delivery](../09-06-paper-audit-intake-delivery/prd.md)
承担父需求 R3、R4、R5、R6、R7、R8。

## Goal

在 `SKILL.md` 与两份 references 中显式区分三级交付约束
（不得修改论文 / 不得写入仓库 / 完全不得落盘），
为最严格一级给出不依赖文件写入的审查路径，
并让已授权落盘时的目标目录明确、不静默覆盖。

## Background

`academic-writing-skills/paper-audit/SKILL.md:61` 只声明了一级边界：
"Don't rewrite the paper source"。没有关于写入仓库或写入磁盘的分级。

`SKILL.md:134-136` 把 deep-review Phase 1 写成
`prepare_review_workspace.py <paper> --output-dir ./review_results`，
`scripts/prepare_review_workspace.py:952` 的 `--output-dir` 默认值同为 `./review_results`。
文档没有说明禁止落盘时该怎么办。

落盘行为已于 2026-09-06 实跑确认，逐模式记录见
[write-behavior.md](research/write-behavior.md)：

| 模式 | 落盘产物 | T3 可用 |
| --- | --- | --- |
| `quick-audit` | 无 | 是 |
| `gate` | 无 | 是 |
| `re-audit` | 无 | 是 |
| `polish` | `.polish-state/`，写在**论文文件所在目录** | 否，且 T2 已排除 |
| `deep-review` | `./review_results`（静态证据，未实跑） | 否 |

实跑推翻了原先"polish 不建工作区"的静态推断。
polish 的写入点是 `scripts/audit.py:2509` 的 `paper_path.parent / ".polish-state"`——
写入论文目录意味着论文在仓库内时即违反 T2。

`references/workflow-detail.md:6-12` 的工作区覆盖确认是 codex 明确列为保留的项。
`references/output-layout.md` 是落盘产物的权威清单。

## Requirements

- R1（三级定义）：`SKILL.md` 显式定义三级并给出每级的允许动作与禁止动作。
  T1 不得修改论文源文件（沿用现有条款）。
  T2 在 T1 基础上不得写入仓库工作树。
  T3 在 T2 基础上不得写入任何位置。三级互不重叠、覆盖完整。
- R2（级别一次声明）：用户一句话即可选定级别，后续步骤不重新确认级别。
- R3（T3 可用路径）：列出 T3 下可运行的模式，清单由实跑确认后定稿；
  明写 deep-review 在 T3 下不可用，并给出降级选项与其能力差距。
- R4（证据缺失声明）：T3 下不可运行的脚本按名列出，并分两组——
  缺席会丢失审查证据的标 `missing evidence`；仅缺输出文件的渲染器标"未产出"。
  2026-09-06 修订：原文要求"统一标 missing evidence"，对抗核查证明该要求本身
  会误导读者以为审查证据缺失，实际只缺一个输出文件，故改为分组。
- R5（不冒充）：明确禁止用对话检查冒充完整脚本验证；
  区分手段沿用现有 `[Script]` / `[LLM]` provenance，不新造标记。
- R6（目录明确）：落盘前把 `--output-dir` 的实际目标路径念给用户；
  覆盖仍走 `workflow-detail.md:6` 现有确认，不新增覆盖入口。
- R7（不扩权）：不新增自动写入、自动执行、自动联网；
  `allowed-tools` 与 `argument-hint` 不放宽；不新增依赖。
- R8（同步）：`workflow-detail.md` 与 `output-layout.md` 的 sha256 更新进 manifest，
  各自 en/zh 镜像同步。`SKILL.md` 不在 manifest 中，但须复跑读取它的 contract 测试。

## Acceptance Criteria

- [x] AC1（R1）：`SKILL.md` 含三级边界段；逐级列出允许与禁止动作；
      任一动作只归属一级，不出现两级都允许或两级都禁止的重叠项。
- [x] AC2（R2）：文档说明级别由用户一句话选定，后续 Phase 不重复确认级别。
- [x] AC3（R3）：T3 可用模式清单中的每一项都有对应的实跑记录
      （只放论文文件的目录中，运行前后目录内容对比），未实跑的模式不进入清单，
      且文档明写 deep-review 一行未实测、来自读码。
- [x] AC4（R3）：deep-review 在 T3 下不可用被明写，并列出降级选项及其相对 deep-review 的能力差距。
- [x] AC5（R4，已修订）：不可运行的脚本按名列出并分两组。
      丢失证据组含 `prepare_review_workspace.py`、`build_claim_map.py`、
      `consolidate_review_findings.py`、`verify_quotes.py`，逐项标 `missing evidence`；
      渲染器组含 `render_deep_review_report.py`、`render_html_report.py`，
      标为"未产出"而非 `missing evidence`。
- [x] AC6（R4）：给定输入"审查这篇论文，但不要在磁盘上留下任何文件"，
      实际响应中不出现 `review_results` 的创建，且列出了缺失的脚本证据。
      验收依据是保存的实际响应。
- [x] AC7（R5）：文档含禁止对话检查冒充脚本验证的条款，并指明 `[Script]` / `[LLM]` 为区分手段。
- [x] AC8（R6）：`SKILL.md:134` 附近与 `output-layout.md` 均要求落盘前陈述目标目录路径；
      `workflow-detail.md:6-12` 覆盖确认段落保持存在且未被弱化。
- [x] AC9（R7）：`git diff` 显示 `SKILL.md` frontmatter 的 `allowed-tools` 与
      `argument-hint` 未变；无脚本改动；无依赖改动。
- [x] AC10（R8）：`uv run --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q` 通过；
      `uv run python docs/scripts/check_resource_sync.py` 通过。

## Out of Scope

不改 `MODE_GUIDE.md`（属 intake-gating 子任务）。不改 evals（属 verify 子任务）。
不改任何脚本、CLI flag、默认值或 schema——包括不改 `--output-dir` 的默认值。
不新增 mode、agent、lane。不改论文仓库部署副本。
