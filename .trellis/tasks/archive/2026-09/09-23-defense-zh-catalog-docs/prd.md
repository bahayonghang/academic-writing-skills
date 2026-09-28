# C4 技能入口、catalog 登记与双语文档

## Goal

为 latex-defense-zh 写技能入口（SKILL.md）、示例、evals 与 agents，把它登记为第 8 个公开 catalog 技能，同步双语文档、
README、AGENTS/CLAUDE、CHANGELOG 与 spec 契约，最后用 Claude Code 对用户真实论文仓库完成一次端到端验收。

## Parent / Dependencies

父任务 `09-23-latex-defense-zh`，对应父 R1（SKILL.md、examples、evals、agents）、R9、R10 与集成验收 AC11。
前置：C3 已完成并通过其质量门。路由命令只用 C2/C3 已实现的 CLI（父 design §3），不改 C1–C3 文件。

## Requirements

- C4-R1 `SKILL.md`：frontmatter（name、description 120–400 字符、when_to_use 中英触发词与排除项、metadata version `6.0.0`、
  last_updated、argument-hint、allowed-tools）；仓库默认十个必备节；Module Router 五行（extract、plan、build、check、preview），
  每行命令写 `uv run python -B $SKILL_DIR/scripts/…`，所列选项都出现在脚本 `--help`；工作流写明三个用户检查点与 ≤3 轮修复循环；
  安全边界写明论文文本为 untrusted 数据、论文仓库只读、输出目录需用户同意、学术事实保护。正文中文，节标题沿用仓库英文名。
- C4-R2 `examples/`：`predefense-40min.md`、`formal-defense.md`、`fix-after-check.md`，全部使用合成论文（C2 fixture）的名称与内容。
- C4-R3 `evals/evals.json`（≥5 条，`files` 指向 C2 fixture）与 `evals/trigger_eval.json`（≥12 条，正例 ≥5、反例 ≥5，
  反例覆盖 pptx 答辩、期刊会议报告、英文答辩、论文正文润色、审稿评分）。
- C4-R4 `agents/openai.yaml`（interface、display_name、short_description、default_prompt）与 `agents/qa-committee-agent.md`
  （按 C1 qa-prep 的提问类别，基于清单与规划生成每章 3–5 个答辩提问与答案骨架，只引用论文节号、图号、表号）。
- C4-R5 catalog 登记：design §2 列出的全部契约列表、安装器、测试函数与技能数写死处。
- C4-R6 文档：examples 与 agents Markdown 的双语资源页与 manifest；技能总览页 `docs/skills/latex-defense-zh/index.md` 与中文页；
  技能索引页、首页、快速开始、usage、安装页、VitePress 侧栏与站点描述；README.md、README_CN.md；docs/CHANGELOG.md。
- C4-R7 spec：新增 `.trellis/spec/academic-writing-skills/defense-deck-contract.md`（帧标记、清单与规划契约、D-* 码集合、
  CLI 退出码、只读边界、测试要求），在 spec 索引登记；`docs-bilingual-resources.md` 技能数由七改八。
- C4-R8 AC11 真实论文验收：按父 implement 的 AC11 流程执行，证据只记录页数、D-* 计数、命令退出码与人工结论。

## Acceptance Criteria

- [ ] AC1: `tests/contracts/test_skill_contracts.py`、`test_skill_versions.py`、`test_skills_install.py`、`test_trigger_evals.py`、
  `test_docs_bilingual_resources.py` 全部覆盖并通过 latex-defense-zh（含路由命令 `--help` 核对与命令卫生）。
- [ ] AC2: `just skills-install --list` 列出 8 个技能。
- [ ] AC3: `uv run python docs/scripts/check_resource_sync.py`（完整模式）通过；`just doc-build` 通过；侧栏含新技能组。
- [ ] AC4: `just ci` 通过。
- [ ] AC5: 公开文件扫描（技能目录、docs 新页、README、spec）不含参考 pptx 作者姓名、用户姓名与论文题目、本机绝对路径；
  技能目录无校徽图片（人工 grep，搜索词不写入文件）。
- [ ] AC6: AC11 证据文件 `research/acceptance-real-thesis.md` 记录：输出目录类型（用户指定或 scratchpad）、各命令退出码、
  帧数与 PDF 页数、各严重度计数（Critical 与 Major 为 0）、总览图目视结论；其他四个宿主写 UNVERIFIED。
- [ ] AC7: 除 design §2 清单与技能目录外，`git status --porcelain` 无其他改动。
