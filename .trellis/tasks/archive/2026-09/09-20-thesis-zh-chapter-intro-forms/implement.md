# Implement：执行清单

前置：用户在后续消息中明确批准规划摘要（含 D1 交付层级）后，才运行 `python ./.trellis/scripts/task.py start`。分支：`dev`。两个阶段各一个 commit；阶段 B 失败不影响阶段 A。

## 阶段 A：文档层（R1-R4）

- [ ] A1 改写 `academic-writing-skills/latex-thesis-zh/references/writing/thesis-writing-guide.md`"正文章引言"节（结构见 `design.md` §3.1；六步表 §3.2；选型表 §3.3）。既有两段模板、弹性口径、正反例表、边界句原句保留；只改推荐语；正反例为合成文本；来源只引 `research/sources-and-prior-art.md` §2 带 URL 条目。
- [ ] A2 五处措辞协调（锚点见 `research/existing-machinery.md` §2）：`method-chapter-guide-zh.md`（§三首条、§三末尾、§三正反例表、§十映射表）、`structure-guide.md`、`process-chapter-guide-zh.md` §十、`paragraph-roles-zh.md` 指南分工、`modules/logic.md` Chapter Intro Specialization 措辞。只改含"两段"的句子，其余不动。
- [ ] A3 路由（只改措辞与触发词，不写 flag）：`modules/routing-rules.md` 章引言条改写 + 触发词；`SKILL.md`（`when_to_use` 触发词、歧义速判指路 thesis-writing-guide 段式选型、Reference Map L164 措辞、`last_updated`；`version` 不动；`logic` 行命令不动）。
- [ ] A4 `evals/trigger_eval.json` 用 Bash python 追加 ≥ 2 正例 + ≥ 1 负例（CRLF；`json.dumps(indent=2, ensure_ascii=False)` 后 `\n` → `\r\n`；先 round-trip 核对无 diff 再追加）。
- [ ] A5 docs：A1/A2/A3 改动的每个 references 文件同步 zh 页（原样）与 en 页（译文）；`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh --write-manifest`，再不带 `--write-manifest` 复核。
- [ ] A6 验证（"验证命令"A 组）。
- [ ] Gate A（复审）：AC-01~AC-05、AC-12；六文件"两段"措辞 0 处；无私有语料；`method-chapter-guide-zh.md` §九与阈值表原句不变。
- [ ] A7 commit：`docs(latex-thesis-zh): 章引言支持一段式与两段式并给出段式选型`（回滚点 1）。

注意：`SKILL.md` `logic` 行若先含 `--chapter-intro-style`，`test_latex_thesis_zh_module_router_commands_match_script_help` 会在阶段 B 落地前红。因此 flag 相关文档（`SKILL.md` `logic` 行命令、`modules/logic.md` 新节、`routing-rules.md` 的 flag 指路、docs `logic` 行、YAML 及镜像）全部放在阶段 B 的 B9；阶段 A 的 `logic.md` 只改 Chapter Intro Specialization 措辞。若用户复审后只要文档层（D1 回退），B9 中的 flag 文档一并取消，路由改为"读 thesis-writing-guide 段式选型 + 默认 `logic` 章引言检查"。

## 阶段 B：脚本层（R5-R7）

- [ ] B1 `CHAPTER_DEP_REF_RE` 替换为 `design.md` §4.1 正则（L277）；跑 `tests/skills/latex_thesis_zh -q` 确认存量绿。
- [ ] B2 四处建议文案改为 `design.md` §4.1 新文案（L683、L685、L758、L773 附近）；observe 行与理由行不动；跑存量章引言测试。
- [ ] B3 抽取 `_chapter_intro_span`（L559-619 区间逻辑），`_chapter_intro_block` 改为调用；立即跑 `test_paragraph_arc.py::test_default_output_is_byte_identical_to_pre_change_baseline`、`test_chapter_intro_forms.py`、`test_paragraph_roles.py`。红则按 `design.md` §6 回退。
- [ ] B4 `references/writing/chapter-intro-style-terms.yaml` + `_load_chapter_intro_style_terms`（复制 `_load_paragraph_roles_terms` 模式）+ 内置默认三元组 + `CI_ONE_PARA_MAX_HAN = 600`（注释 UNVERIFIED）。
- [ ] B5 `_ci_finding` + `_check_chapter_intro_style(content, lines, parser, sections, ranges, first_chapter)` 三码实现（`design.md` §4.3-§4.5）；`analyze()` 末尾参数 `chapter_intro_style=False` 与分支（`paragraph_roles` 分支之后、兜底之前）；`main()` 新 flag 与传参。
- [ ] B6 `evals/fixtures/chapter-intro-style/main.tex`（合成五章：第 2 章概述式一段编号引言；第 3 章一段式全要件 + "第 2、3 章"列举承上；第 4 章一段式缺收束/路线；第 5 章一段式约 700 字全要件；第 6 章两段式合规），章标题含"方法"以便 `--section method` 命中；`evals/evals.json` 用 Bash python 追加 id 52（`contains` 三码、`not_contains` `Meaning-Check: PRESERVED`、`regex` 指向 `thesis-writing-guide`）。
- [ ] B7 `tests/skills/latex_thesis_zh/test_chapter_intro_style.py`：loader 复制 `test_chapter_intro_forms.py` 的 `_load_zh`；R7.1 全部断言；含"第 3、4、5 章 / 第 3～5 章 / 第3-5章"承上不报缺承上、"第 2 章"仍命中、建议行不含"第一段 / 第二段 / 两段"。
- [ ] B8 `test_latex_thesis_zh_coverage.py::SMOKE_COMMANDS` 追加 `("analyze_logic.py", ["main.tex", "--chapter-intro-style"], {0}, "缺少导语段落")`；`test_polish_unit_zh.py::FROZEN_HASHES["analyze_logic.py"]` 更新为 LF 规范化 sha256。
- [ ] B9 文档收尾：`SKILL.md` `logic` 行命令加 `[--chapter-intro-style]`；`modules/logic.md` 新节；`modules/routing-rules.md` 章引言条加 flag；两份 docs index `logic` 行与写作参考 YAML 行；YAML 两份 neutral 镜像；被改 references 的 en/zh 镜像；manifest 重生成。改 `SKILL.md` 表格后立即跑 `tests/contracts/test_skill_contracts.py`。
- [ ] B10 spec：新建 `.trellis/spec/academic-writing-skills/chapter-intro-style-contract.md`（Scope / 术语分离 / Signatures & Constants / Contracts 三码 / 默认行为变化声明 / Private Calibration Boundary / Tests Required，仿 `paragraph-roles-contract.md`）；`index.md` 加行。
- [ ] B11 验证（"验证命令"B 组）；`git diff --stat` 两 evals 文件为纯增量；`git status` 全查（防子代理越权改 justfile / pyproject / version）。
- [ ] Gate B（复审）：AC-06~AC-12；默认输出零变化；阈值三处 UNVERIFIED；不复制整句；observe 行字面不变。
- [ ] B12 commit：`feat(latex-thesis-zh): logic 新增 --chapter-intro-style 段式观察并修正章引言承上误报`，正文含"默认行为变化：CHAPTER_DEP_REF_RE 识别章号列举（误报修复）；章引言建议文案改为段式中立（不改 observe 行）"（回滚点 2）。

## 验证命令

A 组（文档层）：

```bash
uv run pytest tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_skill_contracts.py tests/contracts/test_trigger_evals.py tests/contracts/test_docs_bilingual_resources.py -q
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
grep -rn "两段式为推荐形态\|宜写成承上启下两段\|承上启下两段式从第 3 章" academic-writing-skills/latex-thesis-zh/references academic-writing-skills/latex-thesis-zh/SKILL.md
just ci
just doc-build
```

B 组（脚本层，在 A 组之上）：

```bash
uv run pytest tests/skills/latex_thesis_zh/test_chapter_intro_style.py tests/skills/latex_thesis_zh/test_chapter_intro_forms.py tests/skills/latex_thesis_zh/test_body_chapters.py tests/skills/latex_thesis_zh/test_paragraph_roles.py tests/skills/latex_thesis_zh/test_paragraph_arc.py tests/skills/latex_thesis_zh/test_polish_unit_zh.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/contracts/test_parsers_alignment.py tests/contracts/test_deai_alignment.py -q
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py academic-writing-skills/latex-thesis-zh/evals/fixtures/chapter-intro-style/main.tex --chapter-intro-style
uv run python -B academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex --chapter-intro-style
uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
just ci
just doc-build
git diff --stat -- academic-writing-skills/latex-thesis-zh/evals/
git status
```

Windows 下把脚本输出重定向到文件时加 `PYTHONIOENCODING=utf-8`，但不给 pytest 命令加（`testing-and-tooling.md`）。验证 finding 数量走 python API 数 `analyze()` 返回列表，不 grep 渲染报告。

## 风险文件与回滚点

| 文件 | 风险 | 回滚 |
| --- | --- | --- |
| `scripts/analyze_logic.py` B1/B2（默认路径） | 存量 observe 断言、基线锁 | 只改建议行；红则单独回退两处 |
| `scripts/analyze_logic.py` B3（helper 抽取） | 基线锁、`test_paragraph_roles.py` 复用 | 回退为内联 + 新检查复制区间逻辑 |
| `SKILL.md` 路由表 | 全局格式化 hook 重排表格触发 `ROUTER_ROW_RE`；flag 先于脚本落地触发 help 契约红 | flag 只在 B9 写入；改后立即跑 `test_skill_contracts.py` |
| `evals/*.json` | Edit/Write hook 压平数组 | 只用 Bash python；被重排则 `git checkout` 后重写 |
| `docs/resource-manifest.json` | 手改散列失配 | 只用 `--write-manifest` 生成 |
| `references/*.md` 既有句 | 误改弹性口径 / 红线 / 阈值表 | 只改含"两段"的句子；跑 guidance fidelity + `grep` 核对 |
| `test_polish_unit_zh.py::FROZEN_HASHES` | 漏更新导致无关测试红 | B8 固定步骤 |

## `task.py start` 前的最后核对

- [x] `prd.md` 需求、验收、Out of Scope、决策与假设已写；D1 标为假设待用户复审。
- [x] `design.md`、`implement.md` 已写；`research/` 三份文件 + 先例 JSON 已落盘。
- [x] `implement.jsonl` / `check.jsonl` 含真实条目，无 `_example`。
- [ ] 用户在后续消息中明确批准规划摘要（含 D1）。
