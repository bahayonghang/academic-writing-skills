# Research: Cross-cutting audit (crosscut) — academic-writing-skills

- **Query**:横切面分析仓库（版本一致性 / CI 健康 / 测试架构 / 文档漂移 / CLAUDE.md 准确性 / 仓库卫生）
- **Scope**: internal
- **Date**: 2026-07-05
- **Repo root**: `D:\Documents\Code\Agents\academic-writing-skills`
- **Method**: 实跑 `just ci`；对比六个 SKILL.md frontmatter；哈希对比 deai_check.py 副本；核对 conftest sys.path；核对 docs 镜像 EN/zh；核对 git 跟踪状态。

---

## Findings

### XC-1 — `last_updated` 滞后于近期 deai 改动 (severity: low)

- **文件**:
  - `academic-writing-skills/latex-paper-en/SKILL.md:34` — `last_updated: "2026-06-20"`
  - `academic-writing-skills/latex-thesis-zh/SKILL.md` frontmatter — `last_updated: "2026-06-20"`
  - `academic-writing-skills/typst-paper/SKILL.md` frontmatter — `last_updated: "2026-06-20"`
- **证据**: commit `7311420`（2026-07-05 19:59，feat(skills): 加学术去 AI 味结构壳检查）修改了这三个 skill 的 `scripts/deai_check.py`（en +61 行、zh +102 行、typst +110 行）以及 references/evals，但没有 bump 对应 SKILL.md 的 `last_updated`，仍停留在 2026-06-20。
- **根因**: `tests/test_skill_versions.py` 只强校验 `version` 字段与 pyproject 对齐（CI step 1/4），`last_updated` 无任何测试或 hook 约束，靠人工维护，容易漏。
- **建议**: 把这三个 skill 的 `last_updated` 改为 `2026-07-05`；若希望长期防漏，可在 check-versions 里加一条“改了 skill 目录就必须动 last_updated”的软校验（可选，低优先）。

### XC-1b — frontmatter `category` 取值不统一 (severity: low)

- **文件**: `academic-writing-skills/bib-search-citation/SKILL.md` — `metadata.category: docs-writing-publishing`
- **证据**: 另外五个 skill 的 `category` 均为 `academic-writing`，唯 bib-search-citation 为 `docs-writing-publishing`。其余 frontmatter 字段结构（name / description / when_to_use / metadata.tags / version / last_updated / argument-hint / allowed-tools）六者一致，无缺失。
- **建议**: 若无平台分类上的特意区分，统一为 `academic-writing`；若是有意区分需在某处文档说明。判断性问题，非 bug。

### XC-2 — CI 健康：全绿，无 warning (severity: none / 未发现问题)

- **证据**: 实跑 `just ci`（check-versions → lint → typecheck → test）全部通过。测试 `843 passed in 57.93s`，pytest 无 warning 输出。ruff format/check、pyright 均无报错。
- 版本一致性由 `tests/test_skill_versions.py` 测试强制：六个 SKILL.md `version` 均为 `5.2.0`，等于 `pyproject.toml:3` 的 `version = "5.2.0"`。**版本维度干净且被测试锁定。**

### XC-3 — deai_check.py 共享逻辑无对齐锁 + 时态/over-claim 测试只覆盖 EN 副本 (severity: medium)

这是本次审计**最实的横切缺口**，与 test_parsers_alignment.py 保护 parsers.py 的动机完全一致，但 deai_check.py 没有等价保护。

- **文件**:
  - `academic-writing-skills/latex-paper-en/scripts/deai_check.py` (1097 行)
  - `academic-writing-skills/latex-thesis-zh/scripts/deai_check.py` (1210 行)
  - `academic-writing-skills/typst-paper/scripts/deai_check.py` (1217 行)
  - `tests/test_deai_tense.py:11`、`tests/test_deai_overclaim.py:10`
  - `tests/conftest.py:35-53`
- **证据 1（共享逻辑确实存在且已部分并行演化）**: 三个副本都含 `_load_thresholds`、`_apply_tier` 两个共享 helper。对 `_apply_tier` 函数体做 md5：EN 与 typst **字节完全相同**（`d49b0655...`），zh 因中文规则不同（`edc5c9c...`）。即 EN↔typst 之间存在事实共享代码，任何一处修 bug 落到 EN 会静默漏掉 typst——正是 `test_parsers_alignment.py` 当初要防的漂移，但 **deai_check.py 无任何 alignment 测试**（`grep deai_check tests/test_*alignment*.py` 为空）。
- **证据 2（时态/over-claim 测试只跑 EN 副本）**: `test_deai_tense.py` 与 `test_deai_overclaim.py` 都用 `importlib.import_module("deai_check")`。conftest 把 `SCRIPT_DIR_AUDIT`（无 deai_check）与 `SCRIPT_DIR_EN` prepend 到 sys.path，故 `import deai_check` 解析到 **EN 副本**。commit `3a8e3c2`（时态检测）和 `7311420`（结构壳检查）把逻辑镜像进了 zh/typst 副本，但这两个专项测试从不触达 zh/typst 的对应实现。zh/typst 各有 `test_latex_thesis_zh_coverage.py` / `test_typst_paper_coverage.py`，但对 deai_check 只做 smoke 级 `--analyze` 冒烟（见 test_typst_paper_coverage.py:123-150、test_latex_thesis_zh_coverage.py:96/137），并不验证时态门控、over-claim guard、结构壳这些新判据的实际行为。
- **影响**: 时态/over-claim/结构壳逻辑在 zh、typst 副本里若与 EN 漂移或有 bug，全套测试不会红。这是真实覆盖盲区，不是有意分歧（有意分歧指 parsers.py 那种被 ALIGNMENTS 文档化锁定的；这里既无锁也无独立覆盖）。
- **建议方向（二选一或并用）**:
  1. 参照 `tests/test_parsers_alignment.py` 的 `ALIGNMENTS` 模式，为 deai_check.py 新增对齐测试，把 EN/typst（及 zh 中确属共享的部分）中意图共享的 helper/常量 hash 锁定；EN↔typst 意图分歧处显式登记豁免。
  2. 把 `test_deai_tense.py` / `test_deai_overclaim.py` 参数化到三个副本（用 `spec_from_file_location` 分别加载 EN/zh/typst 的 deai_check，类似 zh coverage 的 `_load_zh`），让时态/over-claim/结构壳判据在每个副本都被独立验证。

### XC-3b — bare `import deai_check` 是 zh/typst 未来测试的静默陷阱 (severity: low, latent)

- **文件**: `tests/conftest.py:34-53`
- **证据**: conftest 注释已声明“只有 EN 依赖 bare import，ZH 用 _load_zh() 取优先级”。当前无 bug。但 `import deai_check`（以及 `parsers`、`tex_loader` 等同名脚本）永远解析到 EN/AUDIT 副本。将来若有人给 zh/typst 的 deai_check 写测试时习惯性用 bare import，会静默拿到 EN 副本、测错对象。
- **建议**: 现状无需动；若采纳 XC-3 建议 2，务必用 importlib 显式按路径加载，不要 bare import。

### XC-4 — 手工维护的 docs 镜像漏掉 tense-guide 与 paper-audit 新增引用 (severity: low)

- **文件 / 证据**:
  - EN 与 zh 镜像文件数**完全对齐**（各 137 个，且逐 skill 匹配：latex-paper-en 50/50、latex-thesis-zh 33/33、paper-audit 13/13、typst-paper 37/37、cover-letter 1/1、bib 2/2）。**locale 同步维度干净。**
  - de-AI 能力在顶层 `docs/index.md`、`docs/usage.md`、`docs/zh/index.md`、`docs/zh/usage.md` 及 `README.md` 均有描述。**能力级文档不缺。**
  - `over-claim-guard` 引用已镜像到三个写作 skill 的 docs（EN + zh 各有 `.../over-claim-guard.md` / `OVER_CLAIM_GUARD.md`，随 `7311420` 一起更新）。
  - **缺口 A**: `tense-guide`（`3a8e3c2` 于 06-20 给 en/zh/typst 加的 `TENSE_GUIDE.md` / `tense-guide.md` / `tense-guide-zh.md`）在 `docs/skills` 与 `docs/zh/skills` 下**一个都没有镜像**（`find docs -iname "*tense*"` 为空）。
  - **缺口 B**: paper-audit 于 06-20（`8cf4622`）新增的 `references/OVER_CLAIM_GUARD.md` 与 `references/REVIEWER_PSYCHOLOGY.md` **未进 paper-audit 的 docs 镜像**（`docs/skills/paper-audit/resources/` 仅 13 个精选文件，含 CHECKLIST，不含这两个）。注意 over-claim-guard 进了写作 skill 的镜像却没进 paper-audit 的镜像，处理不一致。
- **根因**: 未发现 docs 生成/同步脚本（仓库内只有 trellis linear_sync.py 与 ref/PaperSpine 的 sync，均无关），`docs/skills` 镜像是**人工维护**，故新增引用易漏。
- **建议**: 若镜像意在“精选子集”，则明确 tense-guide/REVIEWER_PSYCHOLOGY 属于有意不收录并统一 over-claim 的取舍；若意在“完整镜像”，补齐上述文件，并考虑加一个 skill→docs 的镜像生成脚本消除人工漂移。

### XC-5 — CLAUDE.md 关于 pyright 模式的描述错误 (severity: medium)

- **文件**: `CLAUDE.md:104` — `- Pyright with typeCheckingMode = "off" (lenient — focus is on runtime correctness).`
- **证据**: `pyproject.toml:78` 实际为 `typeCheckingMode = "basic"`（非 "off"），且 78-86 行把 `reportMissingImports=false`、`reportAttributeAccessIssue/ArgumentType/CallIssue/OperatorIssue/GeneralTypeIssues="warning"`。"basic" 语义与 "off" 不同：off 几乎不做类型检查，basic 会做且部分未被降级的规则仍以 error 级出现，可卡 `just typecheck`。与记忆条 [[pyright-basic-not-off]] 一致。
- **建议**: 把 CLAUDE.md 该行改为 `typeCheckingMode = "basic"`，并说明多数 report* 规则已降为 warning、但 basic 默认的其余规则仍以 error 生效。

### XC-6 — 构建产物 docs/.vitepress/dist 既被 gitignore 又被跟踪，且持续重复提交 (severity: medium)

- **文件**: `.gitignore:97`（`docs/.vitepress/dist/`，另 line 16 `dist/`）vs 实际 git 跟踪。
- **证据**: `git ls-files docs/.vitepress/dist` 返回 **26 个文件**——即构建产物被 .gitignore 声明忽略，却仍在版本库中被跟踪。commit `7311420` 一并改动了 10 个 `docs/.vitepress/dist/*.html`（404/index/installation/quick-start/usage 及 zh/ 对应页 + hashmap.json）。这些是 `npm run docs:build` 的产物；`.github/workflows/deploy.yml:44` 在 GH Pages 部署时会 `cd docs && npm run docs:build` **重新构建**，故仓库内的 dist 冗余，且每次文档改动都把编译后 HTML 塞进 diff，放大提交噪音、易产生陈旧产物。
- **建议**: `git rm -r --cached docs/.vitepress/dist`（保留 .gitignore 规则），让部署流水线负责构建；此后 dist 不再进版本库。

### XC-6b — docs/report 单文件疑似孤儿 (severity: low)

- **文件**: `docs/report/csw-vs-aws-analysis.md`（`git ls-files docs/report` 仅此 1 个）。
- **证据**: `docs/report/` 目录下只有这一个被跟踪文件，与其余 docs 内容结构（skills/ 镜像、顶层 md、zh/ locale）不相干，未见于 VitePress 导航布局。可能是历史遗留分析稿。
- **建议**: 确认是否仍需展示；若无引用可移除或归档，非 bug，判断性清理。

---

## 严重度汇总（按严重度排序）

| 编号 | 严重度 | 维度 | 一句话 | 关键证据位置 |
|---|---|---|---|---|
| XC-3 | medium | 测试架构 | deai_check.py 三副本有事实共享逻辑（_apply_tier EN==typst 字节相同）却无对齐锁；时态/over-claim/结构壳专项测试只跑 EN 副本 | tests/test_deai_tense.py:11, test_deai_overclaim.py:10, conftest.py:35-44, 三份 deai_check.py |
| XC-5 | medium | CLAUDE.md 准确性 | CLAUDE.md 写 pyright "off"，实际 pyproject 为 "basic" | CLAUDE.md:104 vs pyproject.toml:78 |
| XC-6 | medium | 仓库卫生 | dist 既 gitignore 又被跟踪(26 文件)，每次文档改动重复提交编译 HTML | .gitignore:97 vs git ls-files；commit 7311420 |
| XC-1 | low | 版本/元数据 | en/zh/typst 的 last_updated 停在 06-20，未随 07-05 deai_check.py 改动更新 | 三个 SKILL.md frontmatter；commit 7311420 |
| XC-1b | low | 版本/元数据 | bib-search category=docs-writing-publishing，与其余五者 academic-writing 不一致 | bib-search-citation/SKILL.md |
| XC-3b | low(latent) | 测试架构 | bare import deai_check 永远拿 EN 副本，是 zh/typst 未来测试的静默陷阱 | conftest.py:34-53 |
| XC-4 | low | 文档漂移 | 手工 docs 镜像漏掉 tense-guide(全无)及 paper-audit 的 OVER_CLAIM_GUARD/REVIEWER_PSYCHOLOGY | find docs -iname "*tense*" 空；docs/skills/paper-audit/resources/ |
| XC-6b | low | 仓库卫生 | docs/report 单文件疑似孤儿 | docs/report/csw-vs-aws-analysis.md |

## 干净（未发现问题）的维度

- **CI 健康 (XC-2)**: `just ci` 全绿，843 passed，无 warning。
- **版本一致性主体**: 六个 SKILL.md version 均 = pyproject 5.2.0，且被 test_skill_versions.py（CI step 1/4）强制锁定。
- **docs EN/zh locale 同步**: 137=137 文件、逐 skill 匹配，无 locale 漂移。
- **parsers.py 副本分歧**: 属 test_parsers_alignment.py ALIGNMENTS 哈希锁定的有意设计，非 bug（背景已知，本次复核确认 843 测试含 34 条 alignment 参数全绿）。

## Caveats / Not Found

- 未逐行审查各 skill 业务逻辑（按分工由其他代理负责）；本报告只覆盖跨技能与基础设施横切面。
- XC-4“镜像是精选子集还是完整镜像”属意图判断，需 owner 确认后才能定性为 drift 或有意取舍；本报告已列出客观缺失文件清单。
- XC-1b、XC-6b 为判断性清理项，非功能缺陷。
