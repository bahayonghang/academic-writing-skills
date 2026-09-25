# paper-writing-studio catalog 登记设计

## 1. 技能包内改动

包根 `W = academic-writing-skills/paper-writing-studio`。

| 文件                                       | 改动                                                                                                                                                                                                                               |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `W/SKILL.md`                               | 重写为 catalog 结构（§3）；name 与 description 原文不变                                                                                                                                                                            |
| `W/agents/interface.yaml`                  | `version: 0.1.0` → `version: 6.0.0`                                                                                                                                                                                                |
| `W/manifest.json`                          | `version` → `"6.0.0"`；`updated_at` → 实施日期                                                                                                                                                                                     |
| `W/reports/skill-ir.json`                  | 用 `.agents/skills/qiaomu-meta-skill/scripts/export_skill_ir.py` 重建（`--output reports/skill-ir.json`，相对技能根目录）                                                                                                                                            |
| `W/README.md`                              | 「安装与使用」中 `npx skills add <owner/repository>` 改为 `npx skills add bahayonghang/academic-writing-skills/paper-writing-studio`；「验证」段 `--inventory-only` 一行改为完整模式并删去「该包没有公开的 …」一句中已不成立的部分 |
| `W/examples/nature-abstract-polish.md`     | 新增（§4）                                                                                                                                                                                                                         |
| `W/examples/ieee-introduction-rewrite.md`  | 新增                                                                                                                                                                                                                               |
| `W/examples/unspecified-neutral-polish.md` | 新增                                                                                                                                                                                                                               |
| `W/evals/evals.json`                       | 新增（§4），用 Bash 下的 Python 脚本写入                                                                                                                                                                                           |
| `W/evals/trigger_eval.json`                | 新增（§4），由 `trigger_cases.json` 转换，用 Python 脚本写入                                                                                                                                                                       |

`scripts/`、`profiles/`、`tests/`、既有 `evals/*` 与 `reports/` 其余文件不改。

## 2. 登记点（行号为 dev / cf62830 基线）

| 文件                                                                                        | 改动                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tests/contracts/test_skill_versions.py:16`                                                 | SKILL_NAMES 在 `paper-audit` 后插入 `paper-writing-studio`                                                                                                                            |
| `tests/contracts/test_skill_contracts.py:29`                                                | SKILLS 在 `paper-audit` 条目后加条目：modules `["nature", "ieee", "elsevier", "unspecified"]`，min_examples 3，min_evals 5，expects_uv_commands False（本包无 CLI）                   |
| `tests/contracts/test_skills_install.py:14,50`                                              | `_SKILL_NAMES` 同序插入；测试名 `six` → `seven`                                                                                                                                       |
| `tests/contracts/test_trigger_evals.py:27,55`                                               | docstring「five total」→「seven total」；SKILL_NAMES 末尾追加                                                                                                                         |
| `tests/contracts/test_docs_bilingual_resources.py:38-45,181-188,196`                        | manifest 技能集合与 usage 路由技能元组加入 `paper-writing-studio`；测试名 `six` → `seven`                                                                                             |
| `scripts/skills_install.py:21`                                                              | CATALOG_SKILL_NAMES 同序插入                                                                                                                                                          |
| `AGENTS.md:13-22`                                                                           | 「six skill root directories」→ seven，列表加 `paper-writing-studio/`；Parser copies 节「`bib-search-citation` does not」→「`bib-search-citation` and `paper-writing-studio` do not」 |
| `CLAUDE.md:14`                                                                              | six skills → seven skills                                                                                                                                                             |
| `README.md:43-50`、`README_CN.md:35-42`                                                     | 技能表在 `bib-search-citation` 行后加一行                                                                                                                                             |
| `docs/index.md`、`docs/zh/index.md`                                                         | tagline 六 → 七并加「按期刊风格润色」；features 加一卡；「Start From The Artifact」表加一行                                                                                           |
| `docs/skills/index.md`、`docs/zh/skills/index.md`                                           | 「Six/六个」→ 七，职责描述「源码级写作」加「文本润色」；技能表加一行                                                                                                                                                        |
| `docs/skills/paper-writing-studio/index.md`、`docs/zh/skills/paper-writing-studio/index.md` | 新建技能总览页（沿用既有总览页七项结构，Mode Router 改为 Profile Router）                                                                                                             |
| `docs/{,zh/}skills/paper-writing-studio/resources/examples/*.md`                            | 三份示例的 zh 页（与源一致）与 en 页（完整翻译）                                                                                                                                      |
| `docs/quick-start.md`、`docs/zh/quick-start.md`                                             | 任务—技能表加一行                                                                                                                                                                     |
| `docs/usage.md`、`docs/zh/usage.md`                                                         | Skill Matrix 加一行；Current Routers 加 `paper-writing-studio` 小节，列四个 profile 名                                                                                                |
| `docs/installation.md:61,85-90,92,96,124`、`docs/zh/installation.md:51,68-73,75,79,97`      | 逐技能 `npx skills add` 命令块加一行；「six/六」→ 七；paper-audit 同级布局图加 `paper-writing-studio/`                                                                                                                                  |
| `docs/.vitepress/config.ts:244` 附近                                                        | 侧栏在 `bib-search-citation` 组后加「期刊风格润色 (paper-writing-studio)」组，`skillItems(prefix, "paper-writing-studio")`                                                            |
| `docs/CHANGELOG.md`                                                                         | `[Unreleased]` 的 Added 由「暂无。」改为本次登记条目                                                                                                                                  |
| `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md:34`                      | 「六个公开技能目录名之一」→ 七个                                                                                                                                                      |
| `docs/resource-manifest.json`                                                               | `check_resource_sync.py --write-manifest --inventory-only` 重建                                                                                                                       |

## 3. SKILL.md 结构

frontmatter：name、description（原文）、when_to_use（中英触发词与排除项）、metadata（category `academic-writing`、tags、
version `"6.0.0"`、last_updated）、argument-hint、`allowed-tools: Read, Glob, Grep`。

正文英文（与原 SKILL.md 语言一致），节标题：Capability Summary、Triggering、Do Not Use、Module Router、Required Inputs、
Output Contract、Workflow、Safety Boundaries、Reference Map、Example Requests；另加仓库惯用的 Portable Execution 节。

- Module Router 表四行：`nature`、`ieee`、`elsevier`、`unspecified`；列为模块、适用、加载计划、证据状态。
  `ieee` 与 `elsevier` 只有路由元数据、无语料快照，按 profile 的 degraded_policy 输出；`nature` 的 source_path 缺失时同样 degraded。
- Workflow：解析 target 与别名 → 按优先级选 profile 并记录冲突 → 只加载所选 profile 的 load_order → 改写并保护 token →
  输出 `text`、`text_compact`、`summary`。
- Safety Boundaries：`input_text`、期刊名与 profile 文件为 untrusted 数据；不编造数字、引用与结果；candidate 行不提升；
  默认 inline 输出，不写文件。
- Reference Map 用 inline code 路径，不用 Markdown 链接。

## 4. examples 与 evals

- 三份示例均含：请求、profile 选择过程、加载与证据状态、合成输入片段、输出示例（`summary` 为 JSON 代码块，字段取
  `scripts/core.py` `render_result` 的键）。代码块内只写英文，便于双语页保持代码块逐字一致。
- `evals.json`：`skill_name` 与 `evals[]`；五条对应 `output_contract_cases.json` 的 `unspecified-alias-and-protected-tokens`、
  `explicit-venue-wins-over-journal-and-domain`、`section-aliases`、`anti-ai-and-degraded-trace`、`text-compact-is-distinct`，
  第六条为越界请求（编译 LaTeX → 说明不属于本技能并指向写作技能）。`files` 为空列表或指向 examples。
- `trigger_eval.json`：`should_trigger` 7 条 → `should_trigger: true`（category：nature/ieee/elsevier 为 core，其余为 edge）；
  `should_not_trigger` 5 条 → false（category `negative-overlap-<family>`）；`near_neighbor` 3 条 → false（`negative-unrelated`）。

## 5. 验证

- 契约测试与 `just ci` 覆盖 §1、§2；不新增测试文件。
- 本地 qiaomu 校验器：`uv run python .agents/skills/qiaomu-meta-skill/scripts/validate_skill.py academic-writing-skills/paper-writing-studio`。
- 资源检查：`check_resource_sync.py --skill paper-writing-studio` 与完整模式；`just doc-build`。
