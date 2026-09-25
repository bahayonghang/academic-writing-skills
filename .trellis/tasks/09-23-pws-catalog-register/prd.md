# paper-writing-studio catalog 登记

## Goal

把已在仓库中的 `academic-writing-skills/paper-writing-studio` 登记为第 7 个公开 catalog 技能：技能包满足仓库技能契约测试，
进入安装器与全部硬编码技能列表，并同步双语文档、README、AGENTS、CLAUDE、CHANGELOG 与 spec 中的技能数。
不改变该技能的 venue 选择逻辑、profiles 与输出契约。

## Background / Confirmed Facts

- 产品基线：dev / cf62830。该技能由 `4c2a0b1`（2026-09-11）引入，`9731cba` 修正语料路径。归档任务
  `09-11-paper-writing-studio-*` 把 catalog 安装列为范围外。
- 包结构（20 个跟踪文件）：`SKILL.md`（frontmatter 含 `version: 0.1.0`，正文无仓库必备节）、`README.md`、
  `agents/interface.yaml`、`manifest.json`、`profiles/{nature,ieee,elsevier}.json`、`scripts/core.py`（内部模块，无 CLI）、
  `evals/{trigger_cases.json,output_cases.json,output_contract_cases.json,output_contract_eval.py}`、`reports/*`、`tests/*`。
- 包内测试 `paper-writing-studio/tests/` 已在 `just test` 的 testpaths（`pyproject.toml:88`）内运行。
- 未登记处：`tests/contracts/test_skill_versions.py:16`、`tests/contracts/test_skill_contracts.py:29`、
  `tests/contracts/test_skills_install.py:14`、`tests/contracts/test_trigger_evals.py:55`、`scripts/skills_install.py:21`、
  `tests/contracts/test_docs_bilingual_resources.py:38`（manifest 技能集合）与 `:181`（usage 路由技能元组）；
  `AGENTS.md:13` 写六个技能目录，`CLAUDE.md:14`、`docs/index.md:7` 等处写六个技能。
- 按契约测试的缺口：SKILL.md 缺十个必备节、模块名与 `untrusted` 字样；版本锁要求 SKILL.md frontmatter 版本为 6.0.0；
  缺 `examples/`（≥3 份 `.md`）、`evals/evals.json`、`evals/trigger_eval.json`（现有 `trigger_cases.json` 为 qiaomu 格式）。
- 新增 `examples/*.md` 属于公开资源，`tests/contracts/test_docs_bilingual_resources.py` 要求同步 manifest、双语资源页与
  安装页 `npx skills add` 命令。
- 本地 qiaomu 校验器（`.agents/` 被 `.gitignore:86` 忽略）当前对本包返回 ok；它要求 `manifest.json` 版本等于
  `reports/skill-ir.json` 的 `package.version`。
- `profiles/nature.json` 的 `source_path` 指向 `ref/nature-writing-studio/skill`；`ref/` 被 `.gitignore:85` 忽略。
  安装到论文项目后该路径不存在，技能按既有规则输出 degraded 与 missing evidence。本任务不改该行为。
- 2026-09-23 用户要求：先登记 paper-writing-studio，再实施 latex-defense-zh 任务树。

## Requirements

- P-R1 SKILL.md 改为 catalog 结构：保留 name 与 description；增加 when_to_use、metadata（category、tags、
  version `"6.0.0"`、last_updated）、argument-hint、allowed-tools；正文十个必备节。Module Router 以四个 profile
  `nature`、`ieee`、`elsevier`、`unspecified` 为模块；Safety Boundaries 写明输入文本为 untrusted 数据。
  原 SKILL.md 的事实（选择优先级、profile 隔离、输入、输出、排除项）全部保留。
- P-R2 版本一致：`agents/interface.yaml` 与 `manifest.json` 的 version 改为 6.0.0，`manifest.json` 的 updated_at 改为实施日期；
  用本地 qiaomu 导出脚本重建 `reports/skill-ir.json`，使本地校验器继续返回 ok。
- P-R3 `examples/`：三份中文示例（Nature 摘要润色、IEEE Transactions 引言改写、未指定 venue 的中性润色与冲突报告），
  示例文本为合成内容。
- P-R4 evals：`evals/evals.json`（≥5 条，对应 `output_contract_cases.json` 的 case 与一条越界请求）；
  `evals/trigger_eval.json`（由 `trigger_cases.json` 转换，15 条：7 正例、8 反例）。保留 qiaomu 格式的既有 evals 文件。
- P-R5 登记：design §2 所列列表、测试名、安装器、docs、README、AGENTS、CLAUDE、CHANGELOG、spec 技能数。
- P-R6 不改 `scripts/core.py`、`profiles/*.json`、包内 `tests/`、既有 evals 文件与 `reports/` 中除 `skill-ir.json` 外的文件。

## Acceptance Criteria

- [ ] AC1: `tests/contracts/test_skill_contracts.py`、`test_skill_versions.py`、`test_skills_install.py`、`test_trigger_evals.py`、
  `test_docs_bilingual_resources.py` 覆盖 paper-writing-studio 并通过。
- [ ] AC2: `just skills-install --list` 列出 7 个技能。
- [ ] AC3: `uv run python docs/scripts/check_resource_sync.py`（完整模式）通过；`just doc-build` 通过；侧栏含新技能组。
- [ ] AC4: `just ci` 通过。
- [ ] AC5: 本地 qiaomu 校验器对本包返回 ok（failures 为空）。
- [ ] AC6: `git status --porcelain` 只含 design §1、§2 所列文件与本任务目录。

## Out of Scope

- 不改 venue 选择、profiles、输出契约与包内测试；不补 nature 语料快照；不新增 CLI。
- 不改 `docs/CHANGELOG.md` 历史条目与 `harness-workflow-contract.md` 历史证据表。
- 不 commit、archive 或 push（未授权）。
