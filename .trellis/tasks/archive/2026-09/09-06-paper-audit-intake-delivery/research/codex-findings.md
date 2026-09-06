# codex 建议取证

取证日期 2026-09-06。分支 dev，HEAD 8000ffe，工作树干净。

## 来源与副本一致性

codex 建议引用的三份文件位于论文仓库部署副本
`D:/Documents/LYH/200-Learning/00博士毕业/毕业论文/thesis/.agents/skills/paper-audit/`。

逐段比对结果：该副本的 `references/MODE_GUIDE.md` 与 `references/workflow-detail.md`
与本仓库 `academic-writing-skills/paper-audit/` 下同名文件内容一致。
改动落在本仓库源文件；部署副本由用户自行重装同步。

## 缺陷 1：意图门控无条件提问

`academic-writing-skills/paper-audit/references/MODE_GUIDE.md:30-56`

小节 `### Auto-Detection at Intake` 的前言写
"Surface these conditions to the user as a prompt"，为无条件表述。
四条 bullet 的动作分别是：

| 检测                                                                  | 现有动作                                      | 行    |
| --------------------------------------------------------------------- | --------------------------------------------- | ----- |
| 目录存在 `*audit_report*` / `*review_report*` / `*final_issues*.json` | ask whether the user wants `re-audit` mode    | 36-40 |
| 源文件含 `\added{` / `changes` / `Revision History` 等修订标记        | ask whether this is a revised submission      | 41-46 |
| mode 为 polish 且超 30 页或 25k 词                                    | ask whether `deep-review` is more appropriate | 47-49 |
| 存在审稿信形状文件                                                    | dispatch `revision_coach_agent.md` first      | 50-52 |

收尾句 `MODE_GUIDE.md:53-56`：
"Always present the detected signal in plain language … and let the user confirm or decline."

四条均不检查用户是否已在请求中显式指定模式。

## 缺陷 2：交付形态只有一级

`academic-writing-skills/paper-audit/SKILL.md:61`
只有 "Don't rewrite the paper source" 一条边界。
没有关于写入仓库工作树或写入磁盘的分级。

`academic-writing-skills/paper-audit/SKILL.md:134-136`
deep-review Phase 1 写成
`prepare_review_workspace.py <paper> --output-dir ./review_results`。

`academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:952`
`--output-dir` 的 `default="./review_results"`。

## 缺陷 3：无不落盘路径

文档未给出禁止落盘时的替代审查路径，也未说明此时哪些脚本检查不可运行。

## 落盘行为的静态证据（未实跑）

`academic-writing-skills/paper-audit/scripts/audit.py:2704`
`if canonical_mode == "deep-review":` 是唯一进入 `run_deep_review` 的分支。

`academic-writing-skills/paper-audit/scripts/audit.py:1961-1968`
`run_deep_review` 在 `review_dir is None` 时无条件调用 `prepare_workspace`。

据此推断 quick-audit / gate / polish / re-audit 不建立工作区。
**该推断未经实跑确认**——2026-09-06 的实跑尝试因权限未获批而未执行。
delivery-tiers 子任务的第一步必须实跑确认后才能定稿 T3 路径清单。

## 硬约束

| 约束                                                                                          | 位置                                                                                                                                 |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `MODE_GUIDE.md` 必须含 `Auto-Detection at Intake` 小节                                        | `tests/skills/paper_audit/test_paper_audit_synthesis.py:106-108`                                                                     |
| 该小节必须对审稿信 dispatch `revision_coach_agent`                                            | `tests/skills/paper_audit/test_paper_audit_synthesis.py:109-111`                                                                     |
| `MODE_GUIDE.md` 另被中文学位论文 lane 测试读取                                                | `tests/skills/paper_audit/test_zh_thesis_lane_wiring.py:27`                                                                          |
| `SKILL.md` 被 claim-evidence contract 测试读取                                                | `tests/contracts/test_claim_evidence_contract.py:79`                                                                                 |
| `MODE_GUIDE.md` / `workflow-detail.md` / `output-layout.md` 各有 `sourceSha256` 与 en/zh 镜像 | `docs/resource-manifest.json`；检查器 `docs/scripts/check_resource_sync.py`；测试 `tests/contracts/test_docs_bilingual_resources.py` |
| `SKILL.md` 不在 manifest 中                                                                   | 同上，按 skill 字段过滤后无 `SKILL.md` 条目                                                                                          |
| 改 `evals/evals.json` 须走 Bash python 写入                                                   | 全局 JSON 格式化 hook 会压平数组                                                                                                     |

## codex 明确要求保留的项

- `academic-writing-skills/paper-audit/references/workflow-detail.md:6-12`
  覆盖既有审查工作区前的明确确认。
- `academic-writing-skills/paper-audit/references/MODE_GUIDE.md:24-26`
  re-audit 对 `--previous-report` 的依赖（允许路径唯一可定时先自行查找）。
- `academic-writing-skills/paper-audit/SKILL.md:61`
  审稿与正文修改的授权边界。

## 现有 eval 结构

`academic-writing-skills/paper-audit/evals/trigger_eval.json`：
`{"skill_name", "queries": [{"query", "should_trigger", "category"}]}`。

`academic-writing-skills/paper-audit/evals/evals.json`：
`{"skill_name", "evals": [{"id", "prompt", "expected_output", "files", "assertions"}]}`，
assertion 类型见于现有条目的 `contains` 与 `regex`。
第 1 条已用 `\[(Script|LLM)\]` 正则验证 provenance。

## 双语手写页现状

`docs/skills/paper-audit/index.md` 与 `docs/zh/skills/paper-audit/index.md`
第 12、27、45、52、63、155 行把 review workspace 描述为 deep-review 的固有产物。
两页不在 `docs/resource-manifest.json` 托管范围内。
