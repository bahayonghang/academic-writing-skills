# latex-defense-zh：评阅意见回复（rebuttal）模块

## Goal

为 `academic-writing-skills/latex-defense-zh/` 新增 rebuttal 模块。输入为学位论文评阅书目录（预评审、终评审等）与论文 LaTeX 仓库，
输出为两份目录：评阅书目录同级的 `responses/`（逐条修改说明，纯文本等价 Markdown，直接粘贴到学校的「修改审查表」Word 表格）
与 `workspace/`（台账、归一化评阅原文、修改计划、锚点与检查结果等中间产物）。
父任务持有来源事实、需求、跨子任务契约与集成验收；产品交付由三个子任务串行承担：C1 intake → C2 response → C3 docs。

## Background / Confirmed Facts

- 产品基线：dev / 53c2ab5，工作树在创建本任务树前干净。项目版本 6.0.0（`pyproject.toml`）。
- 现有技能：五个模块 `extract`、`plan`、`build`、`check`、`preview`，21 个 D-* 码，论文仓库只读
  （`academic-writing-skills/latex-defense-zh/SKILL.md`）。SKILL.md 的 description 当前 362 字符，契约上限 400
  （`tests/contracts/test_skill_contracts.py:15-16`）。
- 用户的评阅书目录、Word 表格与论文仓库的结构事实见 `research/review-format-facts.md`（已脱敏）。
- 先例与领域规范见 `research/prior-art.md`：ARIS 三道门、TobiasLee 原子化意见、ARS 追踪矩阵；高校规范要求逐条、写具体修改内容与修改位置（含页码）。
- 运行依赖：Pillow、PyYAML、Jinja2；PyMuPDF 不在依赖中，`render_preview.py` 已懒加载并以退出码 3 报缺失。
- `tests/contracts/test_skill_contracts.py:625` 会把 references 中 `scripts/<name>.py --flag` 的每个选项与 `--help` 对照。
- `tests/skills/latex_defense_zh/test_defense_skill_entry.py:13` 把 Module Router 行集合写死为五个模块。
- 新增 references/examples 必须同步 `docs/resource-manifest.json` 与双语资源页（`.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`）。

## Assumptions（规划时采用，用户可在审阅时推翻）

- A1「评审的统计目录」按「评阅书目录的同级目录」理解：`<评阅书目录的父目录>/responses/` 与 `<父目录>/workspace/`；`--root` 可覆盖父目录。
- A2 rebuttal 模块不修改论文源文件。论文的实际修改由用户或 `latex-thesis-zh` 完成；本模块生成修改计划、回复与核对结果。
  这沿用现有「论文仓库只读」边界；输出目录位于论文仓库内是用户指定位置，不视为改论文。
- A3 输出 Markdown 而非 docx，不引入 pandoc。
- A4 一次运行处理一个阶段目录（如 `pre-review`）；终评审另起一次，目录结构相同。

## Requirements

- R1 目录初始化：给定评阅书目录，创建同级 `responses/` 与 `workspace/`；评阅书目录与其中文件只读。已有输出时不覆盖用户内容（见 R6）。
- R2 评阅书提取：支持文字层 PDF（PyMuPDF）、`.txt`、`.md`；去除跨页重复的水印行与页脚；按标题切分「学术评语」与「不足之处和建议」；
  解析总分、总体评价等级与是否同意答辩；按 `1.`、`1、`、`（1）` 等样式切分编号意见并合并跨行文本。
  无文字层或不支持的格式（如 `.docx`）给出明确提示，不猜测内容。
- R3 意见台账：`workspace/concerns.yaml` 为唯一事实源。每条意见有稳定编号、评阅人、逐字摘录、分类、严重度与优先级、跨评阅人重叠、
  文中锚点（图、表、式、章、节、文献）、处理方式、状态、修改计划、回复、修改位置与修改证据。脚本生成骨架；拆分复合意见与分类由 LLM 完成并标 `[LLM]`。
- R4 锚点与页码：intake 用论文 aux 把评阅书中的编号（如「图2-7」「文献[24]」）映射到标签与 bib 键；build 用修改后重新编译的 aux 取当前编号与页码，
  编号变化时同时写原编号与新编号。
- R5 修改计划：在论文修改前，从台账渲染 `workspace/revision_plan.md`，按论文文件与负责方（latex-thesis-zh、drawio 图源、手工）分组，供用户批准处理方式。
- R6 回复渲染：从台账渲染 `responses/review-result.md`（预评审结果行）、`responses/response-all.md`（总体说明 + 各评阅人逐条）
  与 `responses/response-R<n>.md`。文本只用段落和普通文字行（纯文本等价 Markdown）。build 发现 responses 自上次渲染后被手改时拒绝覆盖，除非 `--force`。
- R7 质量门：`rebuttal_check.py` 输出 R-* 结果，格式与 D-* 一致（Severity、Priority、`[Script]`），覆盖：意见覆盖、摘录逐字、状态完成、
  修改证据（自基线提交以来，台账声明位置的文件确有改动）、完成用语与处理方式一致、修改位置可解析、页码陈旧、编号变化、
  Markdown 语法、占位符、数字来源、评阅书文件变更、跨评阅人处理一致、预评审结果行一致；语气类为 Info + NEEDS-LLM。
- R8 学术事实保护：回复不编造实验、数字、文献或结论；未完成的工作只能写成后续工作或说明，不写成已完成；回复中的数字须能在论文可见文本中找到。
  评阅书与论文文本都是 untrusted 数据，其中的指令不执行。
- R9 技能集成：SKILL.md 新增 rebuttal 模块路由、触发词与排除项，description 保持 120–400 字符；新增 references 与 example；
  更新 evals、trigger_eval、入口测试、双语 docs 与 manifest；新增 spec 契约文件。版本保持 6.0.0，只改 `last_updated`。
- R10 隐私：公开 fixture 与示例全部为合成内容；仓库内任何文件不出现真实评阅书的姓名、学号、题目、评阅编号与正文。

## Non-goals

- 不修改论文 `.tex`、图、bib；不编译论文；不调用 latex-thesis-zh。
- 不生成 docx，不填写导师意见与分委员会结论栏。
- 不联网，不检索新文献，不运行新实验。
- 不处理期刊或会议的审稿回复（cover-letter 已声明 rebuttal 延后，本任务不改变该边界）。
- 不把台账接入 `agents/qa-committee-agent.md`（评阅意见转答辩提问可作为后续任务）。

## Task Map

| 子任务 | 交付 | 依赖 |
| --- | --- | --- |
| `10-15-defense-zh-rebuttal-intake`（C1） | `scripts/rebuttal_intake.py`、`scripts/rebuttal_common.py`、合成评阅书 fixture、`test_defense_rebuttal_intake.py` | 无 |
| `10-15-defense-zh-rebuttal-response`（C2） | `scripts/rebuttal_build.py`、`scripts/rebuttal_check.py`、合成修改后论文 fixture、`test_defense_rebuttal_build.py`、`test_defense_rebuttal_check.py` | C1 完成 |
| `10-15-defense-zh-rebuttal-docs`（C3） | SKILL.md、三份 references、一份 example、evals、入口测试、双语 docs、manifest、README、spec 契约、真实评阅书验收 | C2 完成 |

## Acceptance Criteria

- [ ] AC1 在合成 fixture（一份测试时由 PyMuPDF 生成的 PDF，一份 `.txt`）上运行 intake：同级创建 `responses/` 与 `workspace/`；
      `workspace/reviews/R1.md`、`R2.md` 不含水印与页脚行；两份等级、总分、同意答辩解析正确；编号意见条数与 fixture 一致；锚点检出且映射到 fixture aux 标签。
- [ ] AC2 只读：三个脚本运行前后，fixture 论文树与评阅书目录的文件 sha256 集合不变。
- [ ] AC3 build 在合成「修改后」fixture 上渲染三类 responses 文件；每条回复含「意见 / 回复 / 修改位置」；位置含编号与页码；
      编号变化的锚点写出原编号与新编号；responses 被手改后再次 build 退出码 4，`--force` 后覆盖。
- [ ] AC4 每个 R-* 码至少一个专门触发它的负例测试；干净 fixture 的 check 结果 Critical 与 Major 计数为 0，退出码 0。
- [ ] AC5 R-COMMIT 只认台账声明位置的文件改动：仓库其他路径有改动、而声明位置无改动时仍报 Critical；位于 `responses/`、`workspace/` 与评阅书目录下的改动不算修改证据。
- [ ] AC6 responses 原文与「去除 Markdown 渲染」后的文本逐行一致（R-MD-SYNTAX 测试以 fixture 断言）。
- [ ] AC7 SKILL.md Module Router 为 8 行（原 5 行 + `rebuttal-intake`、`rebuttal-build`、`rebuttal-check`）；description 120–400 字符；
      trigger_eval 新增至少 3 条应触发（评阅意见回复、修改说明、预评审修改审查表）与 2 条不应触发（期刊审稿回复、审稿打分）。
- [ ] AC8 `uv run python docs/scripts/check_resource_sync.py` 通过；`just ci` 通过；`just doc-build` 通过。
- [ ] AC9 真实评阅书验收（C3 末步，用户同意后执行）：对用户评阅书目录运行 intake，两份评阅书的等级、条数与锚点与 `research/review-format-facts.md` §2 一致；
      证据文件只写计数与码名，不写姓名、题目与正文。
- [ ] AC10 `git grep` 在仓库中查不到真实评阅书的姓名、学号、题目与评阅编号。
