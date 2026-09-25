# latex-defense-zh：博士学位论文答辩 Beamer 技能

## Goal

在 `academic-writing-skills/` 新增第 8 个公开技能 `latex-defense-zh`。输入为中文博士学位论文 LaTeX 仓库，
输出为按参考预答辩框架排布的 XeLaTeX Beamer 答辩稿（`.tex` + 主题文件 + 讲稿），并附质量门报告与预览总览图。
父任务持有来源事实、需求、任务图、跨子任务约束和集成验收；产品交付由四个子任务承担。
实施前置：`09-23-pws-catalog-register` 完成，`paper-writing-studio` 成为第 7 个 catalog 技能。

## Background / Confirmed Facts

- 产品基线：dev / cf62830，工作树在创建本任务树前干净。项目版本 6.0.0（`pyproject.toml`）。
- 参考框架：`ref/` 下 94 页博士预答辩 pptx（`.gitignore:85` 忽略 `ref/`）。页序、页型、讲稿规律和视觉测量见
  `research/framework-analysis.md`。
- 参考技能：`ref/claude-skill-academic-ppt`（MIT）与 `ref/thesis-defense-pptx-skill`（Apache-2.0）；
  keep/adapt/reject 映射与目录检索结果见 `research/reference-skills-analysis.md`。两者产物都是 .pptx。
- 目标论文仓库类型：ysuthesis 类、XeLaTeX、`\include` 章文件、`\bicaption`/`\subcaptionbox`、aux 图号、
  「对应论文第X章」成果标注；第 2 章为基础章。事实见 `research/thesis-repo-facts.md`。
- 本机工具：TeX Live 2025（XeTeX、latexmk、`beamer.cls`、`ctexbeamer.cls`）；字体 Microsoft YaHei 可用。
  运行依赖已有 Pillow、PyYAML、Jinja2（`pyproject.toml` dependencies）；PyMuPDF 不在依赖中，
  paper-audit 以懒加载方式使用（`academic-writing-skills/paper-audit/scripts/visual_check.py:22`）。
- 以下行号为 cf62830 基线；pws 登记后部分行号后移，测试名与文档中的技能数由 six/六 变 seven/七。
- 技能登记为硬编码列表：`tests/contracts/test_skill_versions.py:16`、`tests/contracts/test_skill_contracts.py:29`、
  `tests/contracts/test_skills_install.py:14`（测试名第 50 行含 six）、`tests/contracts/test_trigger_evals.py:55`、
  `scripts/skills_install.py:21`。docs 资源检查按目录遍历发现技能（`docs/scripts/check_resource_sync.py:55`）。
- 技能数写死处：`AGENTS.md:13`、`CLAUDE.md:14`、`docs/index.md:7`。
- docs 资源契约按目录遍历：`tests/contracts/test_docs_bilingual_resources.py:35` 比对 `docs/resource-manifest.json`
  与全部技能的公开资源（`references/**/*.{md,yaml,yml}`、`templates/**/*.md`、`examples/**/*.md`、`agents/**/*.md`），
  并断言 manifest 技能集合等于六个技能名（pws 登记后为七个）；第 196 行要求 manifest 中每个技能在双语安装页有 `npx skills add` 命令。
  因此新增第一份公开资源的子任务必须同时登记 manifest、双语资源页与安装页命令，否则 `just test` 失败
  （规则见 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md`）。
- 仓库已有 catalog 外目录 `academic-writing-skills/paper-writing-studio`（在 cf62830 未登记于上列任一列表，AGENTS.md 未列出）。
  2026-09-23 用户要求先登记该技能（任务 `09-23-pws-catalog-register`），catalog 技能数由 6 变 7；
  本任务树在其后实施，技能计数口径为 catalog 技能数，由 7 变 8。
- 2026-09-23 用户确认：目录名 `latex-defense-zh`；完整第 7 个公开技能（pws 先登记后为第 8 个）；结构 + 视觉复刻燕山框架并另带 generic 主题，
  校徽从论文仓库读取不打包；默认汇报时长 40 分钟。

## Requirements

- R1 技能包：`academic-writing-skills/latex-defense-zh/` 含 SKILL.md（仓库默认十个必备节）、references、templates、
  examples（≥3）、evals（evals.json ≥5 条、trigger_eval.json ≥12 条）、agents（openai.yaml + 答辩提问 agent）、scripts。
  SKILL.md 与 references 给出答辩稿的模板、要点和规范。
- R2 框架保真：生成稿的页序与页型遵循框架：封面 → 总目录 → 绪论（背景、现状、现存问题与挑战、研究内容与章节安排）
  → 每章前目录（当前章高亮）→ 研究章（引言、问题描述、方法、实验、小结与「论文」框）→ 应用章 → 结论（主要创新点、
  未来研究展望）→ 致谢页。支持章角色 intro / foundation / research / application / conclusion，角色可在规划文件覆盖。
- R3 视觉：`yanshan` 主题按 `research/framework-analysis.md` §4 复刻颜色、版位、字号层级、页码、双线节标题、小节条、
  「论文」框；`generic` 主题使用相同页型宏，无校徽。两主题正文字号不低于 8 pt。
- R4 输入与提取：给定论文仓库目录，确定性提取元数据、章节树与章角色建议、图（文件、题注、aux 图号、子图）、表、
  带标签公式、算法、成果—章对应、结论章贡献与展望条目，输出 JSON 清单；只读，不改论文仓库任何已有文件。
- R5 规划：按分钟数（默认 40）和阶段（predefense | defense）生成规划文件骨架，每页含角色、版式、节标题、候选图表、
  预算秒数与源位置；LLM 按规则填写要点、结论句和讲稿；构建前输出标题与结论句串读供用户确认。
- R6 构建：由规划文件渲染 `defense.tex`、主题文件与 `notes.md` 到 `--out` 指定的输出目录（工作流在用户同意后建议
  `<论文仓库>/defense/`；目标文件已存在时需 `--force`）；图以相对 `\graphicspath` 引用原图，不复制；公式与表体逐字取自论文源；普通文本转义。
- R7 质量门：检查脚本输出 D-* 结果（编译、溢出、图允许清单、图号、数字来源、公式来源、占位符、目录、
  表体来源、问题—研究内容—创新点对应链、页型覆盖、密度、时长预算、讲稿、封面元数据、阶段字样、论文框、帧标记）；
  格式含 Severity、Priority 与 `[Script]` 标记；另提供 PDF 逐页 PNG 与总览图。
- R8 学术事实保护：不编造数字、图、文献、作者或成果；不生成新图或重绘数据图；创新点与展望取自论文结论章；
  不改动 `\cite`、`\ref`、`\label` 与数学内容。
- R9 catalog 集成：登记 R1 所列全部硬编码列表与版本锁（SKILL.md version 6.0.0）；公开资源进入双语 docs 与 manifest
  （新增资源的子任务在同一子任务内同步页面与 manifest）；
  VitePress 侧栏与首页（顶部导航只列技能索引与一个示例技能，保持不变）、README.md、README_CN.md、AGENTS.md、CLAUDE.md
  技能数与清单、docs/CHANGELOG.md 同步；
  新增 `.trellis/spec/academic-writing-skills/defense-deck-contract.md` 并登记索引。
- R10 公开内容卫生：公开文件不含参考 pptx 作者姓名、论文题目与内容，不含用户论文正文与结果；fixture 全部合成；
  不写本机绝对路径；校徽不进入技能包。

## Task Map

| 顺序 | 子任务 | 父需求 | 交付 |
| --- | --- | --- | --- |
| C1 | 09-23-defense-zh-framework-theme | R1(部分)、R2、R3、R9(部分)、R10 | 框架/页型/视觉/内容/时长/讲稿参考文档；yanshan 与 generic Beamer 主题、页型宏包；合成演示稿可编译；本技能 docs 资源登记（manifest、七份参考的双语页、安装页命令、资源契约测试技能集合） |
| C2 | 09-23-defense-zh-extract-build | R4、R5、R6、R8 | tex_loader 副本、extract_thesis.py、plan_deck.py、build_deck.py、Jinja2 帧模板、合成 fixture 与测试 |
| C3 | 09-23-defense-zh-quality-gate | R7、R8 | check_deck.py、render_preview.py、质量门参考文档与测试 |
| C4 | 09-23-defense-zh-catalog-docs | R1、R9、R10 | SKILL.md、examples、evals、agents、catalog 登记、双语 docs、README/AGENTS/CHANGELOG、spec 契约、真实论文端到端验收记录 |

串行 C1 → C2 → C3 → C4。C2 使用 C1 的宏 API 与模板目录；C3 读取 C2 的帧标记与清单格式；C4 的路由命令依赖 C2/C3 的 CLI。
文件所有权与接口真源见 design.md。

## Acceptance Criteria

- [ ] AC1 (R1): 技能目录结构满足 `tests/contracts/test_skill_contracts.py` 全部检查（必备节、examples、evals 形状、
  description 120–400 字符、命令卫生、路由命令参数出现在 `--help`）。
- [ ] AC2 (R2): 对合成 fixture 论文（含基础章、三研究章、应用章、结论章）执行 extract → plan → build，生成稿页序与
  框架一致：每章前目录且当前章高亮；每个研究章含 intro/problem/method/experiment/summary 五种角色；结论含创新点与展望；
  末页为致谢页。由测试断言帧标记序列。
- [ ] AC3 (R3): 两主题下合成演示稿与 fixture 生成稿 XeLaTeX 编译成功（有 xelatex 时运行，缺失时 skip 并在证据中注明）；
  yanshan 主题颜色常量与 §4 测量值一致（测试断言 .sty 中 hex 值）；无校徽路径时回退为文字标识且编译成功。
- [ ] AC4 (R4): fixture 清单 JSON 的章角色、图号（aux 优先、computed 回退）、子图、成果—章映射、结论条目与预期一致；
  提取前后论文目录文件哈希不变。
- [ ] AC5 (R5): 40/30/60 分钟三档规划的内容页数落在 `references/time-budget.md` 给出的区间；研究章不少于 6 页；
  `--outline` 输出按页序的节标题与结论句。
- [ ] AC6 (R6): 构建输出不覆盖已存在文件（无 `--force` 时退出码非 0）；公式与表体与论文源逐字一致；
  普通文本中的 `% & _ # $ { } ~ ^ \` 正确转义；`\graphicspath` 为相对路径。
- [ ] AC7 (R7): 每个 D-* 码至少一个正例与一个反例测试；输出行格式与 `--json` 字段稳定；
  preview 在 PyMuPDF 缺失时给出可执行提示且退出码为 3，存在时生成逐页 PNG 与总览图。
- [ ] AC8 (R8): 在规划中加入论文外数字、论文外图片、改写公式的三个反例，check_deck 分别报 D-NUM-SRC、D-FIG-ALLOW、D-EQ-SRC。
- [ ] AC9 (R9): `just ci`、`uv run python docs/scripts/check_resource_sync.py`（完整模式）与 `just doc-build` 通过；
  `just skills-install --list` 列出 8 个技能。
- [ ] AC10 (R10): 公开文件扫描不含参考 pptx 作者姓名、用户姓名与论文题目、本机绝对路径；技能包内无校徽图片。
- [ ] AC11（集成）: 用 Claude Code 对用户真实论文仓库完整执行一次技能流程，输出到用户指定目录或会话 scratchpad
  （不写入本仓库，未经用户同意不写入论文仓库）；编译成功，check_deck 无 Critical/Major；人工目视总览图；
  证据只记录页数、码计数与命令退出码。其他四个宿主运行状态记为 UNVERIFIED。

## Key Decisions / Out of Scope

- 2026-09-23 用户决定：名称 `latex-defense-zh`；完整 catalog；燕山视觉复刻 + generic；默认 40 分钟。
- 帧标题沿用框架的节号标题「k.x …」；academic-ppt 的行动标题改为每页结论句 `takeaway`，串读测试作用于结论句序列。
- 章角色由提取脚本建议、规划文件决定，不按章号写死。
- 不输出 .pptx；不生成或重绘任何图；不支持仅 PDF 输入；不支持 Typst 与英文答辩；不做动画叠层（`\pause`/overlay）；
  正式答辩的「预答辩/盲审意见修改说明」页本版不做，列入后续；不修改或编译用户论文源文件；不联网。
- 不新增 Python 依赖；PyMuPDF 仅懒加载。
- `paper-writing-studio` 的 catalog 登记由前置任务 `09-23-pws-catalog-register` 完成；本任务树不改该技能包。
- 进入实施需要用户对本版规划的明确授权；创建任务与规划评审不构成实施授权。
- 2026-09-23 用户授权：先登记 `paper-writing-studio`，再开始实施本任务树。
