# Implement：执行清单

前置：用户在后续消息中明确批准最终规划摘要后，才运行 `python ./.trellis/scripts/task.py start`。两个阶段均执行（决策 D1）。分支：`dev`（与近期任务一致）。

## 阶段 A：文档层（R1-R4）

- [ ] A1 新建 `academic-writing-skills/latex-thesis-zh/references/writing/paragraph-roles-zh.md`（结构见 `design.md` §2；来源只用 `research/sources-and-prior-art.md` §2 带 URL 条目；正反例为合成文本）。
- [ ] A2 五份指南追加（锚点见 `design.md` §3、`research/existing-machinery.md` §3）：`thesis-writing-guide.md`（两处）、`structure-guide.md`、`method-chapter-guide-zh.md`（§三、§六、§十）、`method-description-guide-zh.md`（§三、§五）、`results-analysis-guide-zh.md`（§二）。只追加，不改既有句。
- [ ] A3 路由：`references/modules/routing-rules.md` 新条；`references/modules/logic.md` 新小节；`SKILL.md`（Reference Map、歧义速判、`when_to_use`、`last_updated`；`version` 不动）。
- [ ] A4 `evals/trigger_eval.json` 用 Bash python 追加 ≥2 正例 + ≥1 负例（CRLF、`json.dumps(indent=2, ensure_ascii=False)`；文件当前可 canonical round-trip）。
- [ ] A5 docs：两份 index 写作参考行；新指南 zh 镜像（原样）与 en 镜像（译文）；A2/A3 修改过的每个 references 文件同步 zh/en 镜像；`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh --write-manifest`，再不带 `--write-manifest` 复核。
- [ ] A6 验证（见"验证命令"A 组）。
- [ ] Gate A（复审）：AC-01~AC-05、AC-11、AC-12；四条口径协调与既有指南无矛盾；无孤儿文件；无私有语料。
- [ ] A7 commit：`docs(latex-thesis-zh): 新增正文各级段落职责与结构去重指南`（回滚点 1）。

## 阶段 B：脚本层（R5-R6）

- [ ] B1 `references/writing/paragraph-roles-terms.yaml` + `_load_paragraph_roles_terms`（复制 `_load_paragraph_arc_terms` 模式，L1186）；内置默认元组。
- [ ] B2 抽取 `_chapter_intro_block` helper（`analyze_logic.py` L600-660 内联逻辑），`_check_chapter_intro` 改为调用；立即跑 `tests/skills/latex_thesis_zh/test_paragraph_arc.py::test_default_output_is_byte_identical_to_pre_change_baseline` 与 `tests/skills/latex_thesis_zh -q`。红则按 `design.md` §6 回退为复制逻辑的私有 helper。
- [ ] B3 常量六个 + `_pr_finding` + `_check_paragraph_roles(content, lines, parser, sections, ranges, first_chapter)` 六码实现（契约见 `design.md` §4.3）。
- [ ] B4 `analyze()` 末尾参数 `paragraph_roles=False` 与分支（在 `subsection_context` 分支之后、兜底之前）；`main()` 新 flag 与传参。
- [ ] B5 `tests/skills/latex_thesis_zh/test_paragraph_roles.py`：loader 复制 `test_paragraph_arc.py` 的 `_load_zh_logic`；六码正反例；第 2 章豁免；两态单独合规；`--section`；YAML 逐字段回退与等价；thesis-project fixture 退出码 0；报告不含 fixture 整句。
- [ ] B6 `tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py::SMOKE_COMMANDS` 追加 `("analyze_logic.py", ["main.tex", "--paragraph-roles"], {0}, "缺少导语段落")`（默认输出仍在，token 稳定）；`SKILL.md` `logic` 行命令追加 `[--paragraph-roles]` 后跑 `tests/contracts/test_skill_contracts.py`。
- [ ] B7 spec：新建 `.trellis/spec/academic-writing-skills/paragraph-roles-contract.md`（Scope / Signatures & Constants / Contracts / Private Calibration Boundary / Tests Required，仿 `paragraph-arc-contract.md`）；`index.md` 加行。
- [ ] B8 `evals/fixtures/paragraph-roles/main.tex`（合成：第 2 章概述式引言 + 第 3 章含背景重述与双写目录的引言、复述章引言的 3.1 导语、列举挑战的 3.1.1 首段、逐算子翻译的公式后段、含 `\cite` 与 `equation` 的本章小结；另含一处阅读地图式合规导语与一处"式中"释义段作对照）；`evals/evals.json` 用 Bash python 追加 id 51（`contains` 六码、`not_contains` `Meaning-Check: PRESERVED`、`regex` 指向 `paragraph-roles-zh.md`）。
- [ ] B9 docs：`modules/logic.md` 新节镜像更新；terms YAML 两份镜像（与源相等）；`SKILL.md` `logic` 行同步到两份 index；manifest 重生成。
- [ ] B10 验证（见"验证命令"B 组）；`git diff --stat` 两 evals 文件为纯增量。
- [ ] Gate B（复审）：AC-06~AC-10、AC-11、AC-12；默认输出零变化；阈值在指南、spec、YAML 注释三处标 UNVERIFIED；不复制整句。
- [ ] B11 commit：`feat(latex-thesis-zh): logic 新增 --paragraph-roles 段落职责观察`（回滚点 2）。

## 验证命令

A 组（文档层）：

```bash
uv run pytest tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_skill_contracts.py tests/contracts/test_trigger_evals.py tests/contracts/test_docs_bilingual_resources.py -q
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
just ci
just doc-build
```

B 组（脚本层，在 A 组之上）：

```bash
uv run pytest tests/skills/latex_thesis_zh/test_paragraph_roles.py tests/skills/latex_thesis_zh/test_paragraph_arc.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/contracts/test_subsection_context_contract.py tests/contracts/test_paragraph_arc_audit_contract.py tests/contracts/test_parsers_alignment.py tests/contracts/test_deai_alignment.py -q
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex --paragraph-roles
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py academic-writing-skills/latex-thesis-zh/evals/fixtures/paragraph-roles/main.tex --paragraph-roles
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
just ci
just doc-build
git diff --stat -- academic-writing-skills/latex-thesis-zh/evals/
```

Windows 下把脚本输出重定向到文件时加 `PYTHONIOENCODING=utf-8`，但不给 pytest 命令加（`testing-and-tooling.md` L149）。

## 风险文件与回滚点

| 文件 | 风险 | 回滚 |
| --- | --- | --- |
| `scripts/analyze_logic.py`（B2 抽取） | 触碰默认路径，基线锁与章引言测试可能红 | 回退为复制逻辑的私有 helper |
| `SKILL.md` 路由表 | 全局格式化 hook 重排表格触发 `ROUTER_ROW_RE` | 改后立即跑 `test_skill_contracts.py` |
| `evals/*.json` | Edit/Write hook 压平数组 | 只用 Bash python；被重排则 `git checkout` 后重写 |
| `docs/resource-manifest.json` | 手改散列失配 | 只用 `--write-manifest` 生成 |
| `references/*.md` 保真锁句 | 误改既有句 | 只追加，不改；跑 guidance fidelity |

## `task.py start` 前的最后核对

- [x] `prd.md` 待决问题已由用户回答并写回（D1；该节已删除，R5/R6 转为无条件）。
- [x] `implement.jsonl` / `check.jsonl` 含真实条目（10 / 6 条），无 `_example`。
- [ ] 用户在后续消息中明确批准最终规划摘要。
