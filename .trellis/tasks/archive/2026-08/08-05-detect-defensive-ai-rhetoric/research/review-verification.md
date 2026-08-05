# Claude Code 审阅逐项核验

## Verification Summary

| 审阅结论 | 判定 | 仓库证据与处理 |
| --- | --- | --- |
| 三份脚本没有目标组合正则 | confirmed | 只有 over-confident `hedge` 与 application `hedge_application`；保持脚本不变。 |
| 脚本建议与新规则存在适用边界张力 | confirmed | EN `deai_check.py:900/:935`、ZH `:1038/:1074`、Typst `:1030/:1069`；design 新增显式边界。 |
| 公开 source 改动必须更新 manifest 散列 | confirmed | `validate_inventory` 比对 `sourceSha256`，`just test` 包含对应 contract。 |
| 计划涉及 18 个 source/36 个页面 | corrected | 原计划可确定 12 个；追踪实际 lane 入口后补 `SUBAGENT_TEMPLATES.md`，最终固定为 13 个 source/26 个页面。 |
| 双语 target 不同步会违反 spec | confirmed | `docs-bilingual-resources.md` 要求同语言忠实、另一语言完整翻译；`just ci` 不做 live full-target 校验，因此另加逐 skill/full checker 与 docs build。 |
| paper-audit 新 eval 必须绑定真实 fixture | confirmed | `test_paper_audit_evals_use_real_mode_specific_fixtures` 对每条 eval 断言 `files` 非空且存在。 |
| Typst/ZH 每条新 eval 也被既有测试强制绑定 | corrected | 既有测试只约束 fixture-bound eval 数量下限；本任务主动升级为四个 surface 的新 eval 全部绑定。 |
| ZH module deai 应用自然中文重写 | rejected | manifest 与正文都表明 `latex-thesis-zh/references/modules/deai.md` 是 en；计划改为逐文件遵守 sourceLocale。 |
| 三处 stance-less 修复必须同步修改 | confirmed | 当前均要求“明确表态”；已写入 runtime checklist 与 AC2。 |
| claims lane max 8 需要饱和排序 | confirmed | `REVIEW_LANE_GUIDE.md:20`、`SUBAGENT_TEMPLATES.md:90-92`；目标模式作为 unsupported extrapolation 子型，按中心性/严重度排序并合并重复位置。 |
| experiment/discussion 路径不明确 | confirmed | 已固定为 EN/ZH `references/modules/experiment.md` 与 Typst `references/modules/EXPERIMENT.md`。 |
| 跨 surface 并集反例不足以保护本地行为 | confirmed | 设计改为每个 surface 的组合 fixture 都覆盖一个正例和四个反例。 |
| PRD claims-agent 行号应从 7 开始 | confirmed | 已从 `:6` 修正为 `:7`。 |
| eval 只能追加，长期测试不应锁整数 ID | confirmed | 当前 max 为 EN 21、ZH 28、Typst 14、paper-audit 22；实施使用 current max + 1，测试用 fixture/prompt 语义锚点。 |
| 新 spec 必须采用 Contract/Convention + Tests Required/Validation | partially confirmed | 没有自动格式测试，但这是本 layer 的稳定写法；计划采纳，并保持 index 三列表。 |
| 新增脚本扫描断言与现有对齐/diff 检查重复 | confirmed | 删除新脚本扫描 contract，只保留现有 alignment test 与最终 scoped diff。 |
| 修改 evals.json 必须用 Bash/Python 文本写入 | confirmed by project spec | `.trellis/spec/academic-writing-skills/testing-and-tooling.md` 明文禁止 Edit/Write，且要求 paper-audit 采用文本级 splice 保持紧凑格式；该 spec 高于本地 Hook 是否可见。 |

## Additional Finding

外部报告遗漏了 `academic-writing-skills/paper-audit/references/SUBAGENT_TEMPLATES.md`。`SKILL.md:191`、`REVIEW_LANE_GUIDE.md:29` 与相关 contract tests 表明它是 deep-review lane 的实际任务模板；只更新独立 reviewer agent 不能保证 lane 行为同步，因此将它纳入第 13 个公开 source。

## Resolved Design Decisions

1. Lane saturation：不新增独立配额；按中心性、严重度、证据缺口排序，重复位置合并，局部风格让位。
2. Path ownership：13 个 runtime source 与 manifest locale 在 `design.md` 中写死；docs targets 从 manifest 派生。
3. False-positive coverage：每个 surface 本地覆盖全部四类反例，用单个组合 fixture 控制用例数量。
