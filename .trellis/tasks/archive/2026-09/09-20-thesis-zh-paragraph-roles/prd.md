# latex-thesis-zh 正文各级段落职责与结构重复检查

任务目录：`.trellis/tasks/09-20-thesis-zh-paragraph-roles/`。单任务，两个 commit：文档层先行，脚本层其后。

## Goal

把用户总结的"各级段落分别承担什么任务"六行表（章引言 / 含子节的总节导语 / 具体方法小节首段 / 公式后段落 / 实验结果段 / 本章小结，各含"合适职责"与"不必反复做的事"）写入 `academic-writing-skills/latex-thesis-zh`：新增规则真相源指南、在五份既有指南追加交叉引用、接入路由与 docs 镜像，并为 `logic` 模块新增 opt-in `--paragraph-roles` 观察，使正文章诊断能按位置指出**结构重复与写作冗余**并定位到行号。

用户价值：盲审与导师批注中"这段前面已经说过了"类问题目前分散在 5 份指南中且缺少"不必反复做"的负面清单；六个位置没有合并视图；三个位置（总节导语、方法小节首段、公式后段落）既无规则也无检查。

## Background

需求来源：用户 2026-09-20 提供的表格截图（原文六行见 `research/sources-and-prior-art.md` §1）。用户只提供其总结的第 2 节，其他节未知，不推断。用户声明目的："主要是防止结构重复与写作冗余"，并要求结合 qiaomu-meta-skill 方法与网络检索。

外部来源、技能目录先例与 keep / adapt / reject / invent 处置见 `research/sources-and-prior-art.md` §2-§5。既有机制、代码锚点、编辑锚点与联动锁见 `research/existing-machinery.md`。技术设计见 `design.md`，执行顺序见 `implement.md`。

## Confirmed Facts

- 六行中章引言、实验结果段、本章小结已有规则源与检查码，缺"不必反复做"负面清单；总节导语、方法小节首段、公式后段落无规则、无检查（`research/existing-machinery.md` §1）。
- 仓库已判定并经 5 篇范文核实的口径（不得推翻）：章引言"编号引言节 / 章后导语"两形态均合规；"路线预告 / 节号目录"两态均合规；并列方法章可不承上；本章小结默认单段、可"首先……最后"串方法要点、启下句只作 Info；第 2 章引言是概述式（`research/existing-machinery.md` §5）。
- 检查器约定：新能力默认藏在新 flag 后，默认输出零变化（`tests/fixtures/paragraph_arc/baseline-before.txt` 逐字节锁）；`[Script]` 恒 `Meaning-Check: NEEDS-LLM`；启发式为 Info/P3 并标注 UNVERIFIED。
- 公开 `references/**` 每个文件都要有 `docs/resource-manifest.json` 行与 en/zh 镜像页；修改既有指南同样要更新散列与镜像。
- `evals/evals.json`（50 条，CRLF）与 `evals/trigger_eval.json`（56 条）只能 Bash python 追加，前缀哈希锁定。
- SkillsMP 三条查询无相关先例；skills.sh 候选中 `willoscar/research-units-pipeline-skills` 的 redundancy-pruner 与 chapter-lead-writer 可 adapt（`research/sources-and-prior-art.md` §4）。

## Requirements

### R1 新指南 `references/writing/paragraph-roles-zh.md`（规则真相源）

- R1.1 六位置职责矩阵：位置 / 合适职责 / 不必反复做 / 既有 owner 指南 / 检查码（既有码、本任务 `PR-*` 码或"仅 `[LLM]`"）。六个位置名称与用户表格一致。
- R1.2 每个位置一组正反例（合成文本，不含私有语料），反例标出"重复了哪一层级的什么内容"。
- R1.3 跨层级去重判据（adapt W1、W2、redundancy-pruner）："一处完整、其余指代"；信息增量两问（是否提供前文没有的新信息；删掉是否断论证）；四类重复（同义复述 / 结论重述 / 材料复用 / 概念重复定义）；结构功能性重述（小结、结论回顾）压缩保留而非删除；过渡句须带本层级具体名词，不用"下面介绍……"目录式叙述。
- R1.4 与既有口径的协调节（见"已确认决策" D2-D5），逐条写明既有规则不变、本指南只追加什么。
- R1.5 `[LLM]` 复核清单：六位置各 2-3 个可回答问题；实验结果段指向 `results-analysis-guide-zh.md` 与 RA-*/B3，不新建判据。
- R1.6 检查映射与阈值表：位置 → 既有码 / `PR-*` / 仅 `[LLM]`；六个阈值常量标注"未标定 / UNVERIFIED"。
- R1.7 来源节：只引用 `research/sources-and-prior-art.md` §2 中带 URL 的条目；仓库已有出处交叉引用不复述。
- R1.8 文件名 kebab-case；被 `SKILL.md` Reference Map 与 `references/modules/logic.md` 链接（无孤儿）。

### R2 既有指南交叉引用与口径协调

- R2.1 `thesis-writing-guide.md`"正文章引言"弹性口径追加：不重述行业背景（与"不重复绪论综述"并列）；目录式与路线式二选一、不在同一引言内双写；节号目录不逐节展开每节内容。"两态均合规"原句不变。
- R2.2 `thesis-writing-guide.md`"正文章末小结"追加：不新增引用、公式、图表或推导（扩展既有"不新增未在原文出现的引用"，原句保留）；串方法要点合法，逐步骤复述训练/部署流程不合法；回指本章已有图表合法。
- R2.3 `structure-guide.md`"标题后导语规范"追加一条：含子节的总节导语只界定本节对象或给简短阅读地图，不重复整章问题与全方法链。
- R2.4 `method-chapter-guide-zh.md` §三追加"不重述行业背景 / 不双写目录与路线"；§六追加"不新增论证"；§十检查映射追加 `PR-*` 行；§九红线不改。
- R2.5 `method-description-guide-zh.md` §三追加"模块首段直接说明输入、作用或未解决接口，不再列全部研究挑战"；§五追加"公式后解释符号、关键机制、边界条件，不按公式顺序逐算子翻译成文字"。
- R2.6 `results-analysis-guide-zh.md` §二末尾追加一句指路：实验结果段的位置职责见新指南矩阵行；判据与码仍以本指南为准。既有保真锁句（`test_thesis_zh_guidance_fidelity.py`）全部保留。
- R2.7 每处追加均带 `(paragraph-roles-zh.md)` 相对链接。

### R3 路由与模块文档

- R3.1 `references/modules/routing-rules.md` 逐类判据新增一条：涉及"章引言又讲了一遍背景""每节开头都重复整章问题""小节首段又列一遍挑战""公式后把每步都翻成文字""小结又加了引用/公式""各级段落该写什么不该写什么 / 结构重复 / 写作冗余"时走 `logic --paragraph-roles` 并补读新指南；实验结果段流水账仍走 `experiment --results-analysis`。
- R3.2 `references/modules/logic.md` 新增 `## Paragraph Role Checks (--paragraph-roles)`：命令、六码表、豁免、`--method-narrative` 无 `--section` 时不运行的说明、指南与词表链接。
- R3.3 `SKILL.md`：Reference Map 新增一行；"路由规则"常见歧义速判追加"各级段落职责/结构重复走 `logic --paragraph-roles`（读 paragraph-roles-zh）"；`when_to_use` 追加触发词；`logic` 路由行 Use when 与命令追加 `--paragraph-roles`；`version` 不动，`last_updated` 改为实施日期；description 长度 120~400。
- R3.4 `evals/trigger_eval.json` 追加 ≥2 条正例（如"第三章引言又把行业背景讲了一遍""每个小节开头都在重复本章问题"）与 ≥1 条负例（英文论文 → `latex-paper-en`）。

### R4 docs 双语镜像

- R4.1 `docs/skills/latex-thesis-zh/index.md`"Writing References"与 `docs/zh/.../index.md`"写作参考"各加一行；两份 index 的 `logic` 路由行同步 `--paragraph-roles`。
- R4.2 新指南、词表 YAML 与所有被修改的 references（R2、R3.1、R3.2）的 en/zh 镜像页同步：zh 源 → zh 页原样、en 页译文、neutral YAML 两页与源相等；`docs/resource-manifest.json` 重生成散列。

### R5 脚本层 `analyze_logic.py --paragraph-roles`

- R5.1 新 flag 默认关闭；`analyze()` 末尾新增关键字参数 `paragraph_roles: bool = False`；可与 `--section`、`--first-chapter` 组合；不改任何既有码的语义与输出；`--method-narrative` 无 `--section` 的提前返回路径不变。
- R5.2 六个 `[Script]` 码，全部 Info/P3、`Meaning-Check: NEEDS-LLM`、不复制整句：`PR-INTRO-BG`（章引言重述行业背景，第 2 章跳过）、`PR-INTRO-TOC`（同一引言内节号目录与路线预告双写，或节号目录 ≥ 阈值条逐节展开；单独任一形态不报）、`PR-LEAD-DUP`（含子节的总节导语与本章章引言 token Jaccard ≥ 阈值）、`PR-SUB-CHAL`（depth-3 小节首段挑战词 + 列举序词并现）、`PR-EQ-NARR`（编号公式后首段算子翻译词 ≥ 阈值；"式中/其中"符号释义段不视为翻译）、`PR-SUM-NEW`（"本章小结"区间内出现 `\cite`、数学环境、图表/算法环境；`\ref` 回指不报）。触发条件、豁免与常量见 `design.md` §4.3。
- R5.3 实验结果段不新增码；小结"重列完整流程"不做脚本判定（仅 `[LLM]` 清单）。
- R5.4 词表 `references/writing/paragraph-roles-terms.yaml`，逐字段回退内置默认，内置默认与 YAML 及两份 docs 镜像相等。
- R5.5 阈值常量集中定义并在指南、spec、YAML 注释三处标注"未标定 / UNVERIFIED"；不在文档中宣称误报率。
- R5.6 章引言块定位从 `_check_chapter_intro` 抽为 helper 复用；抽取后默认输出逐字节不变。若基线锁红，回退为复制逻辑的私有 helper 并在 spec 记录两处同步义务。

### R6 脚本层测试、spec、evals

- R6.1 `tests/skills/latex_thesis_zh/test_paragraph_roles.py`（importlib 按路径加载）：六码各至少一条正例与一条反例；第 2 章豁免；两态单独合规；`--section` 作用域；YAML 逐字段回退与等价；默认输出基线逐字节不变（复用既有基线测试）；`evals/fixtures/thesis-project/main.tex` 加 flag 退出码 0；报告不含 fixture 整句。
- R6.2 `SMOKE_COMMANDS` 追加 `analyze_logic.py main.tex --paragraph-roles`；`test_latex_thesis_zh_module_router_commands_match_script_help` 绿。
- R6.3 新建 `.trellis/spec/academic-writing-skills/paragraph-roles-contract.md` 并在 `index.md` 加行：签名、常量、六码契约、豁免、私有标定边界、必需测试。
- R6.4 `evals/evals.json` 追加 id 51，fixture `evals/fixtures/paragraph-roles/main.tex`（合成：六类冗余各一处与合规对照）；前 47 条哈希不变；`git diff --stat` 为纯增量。

## Acceptance Criteria

- [x] AC-01 `references/writing/paragraph-roles-zh.md` 存在、kebab-case，含六位置矩阵（六个位置字面与用户表格一致）、"不必反复做"列、owner/检查码列、正反例、跨层级去重判据、协调节、`[LLM]` 清单、阈值表（含 UNVERIFIED）、来源节（≥4 条带 URL 来源，含 W1/W5/W6/W10 各类）；被 `SKILL.md` 与 `modules/logic.md` 链接。
- [x] AC-02 五份既有指南各含 `(paragraph-roles-zh.md)` 链接；`thesis-writing-guide.md` 仍含"两态均合规"与"不新增未在原文出现的引用"；`method-chapter-guide-zh.md` §九第 6 条原句不变；`tests/contracts/test_thesis_zh_guidance_fidelity.py` 绿。
- [x] AC-03 `routing-rules.md` 新条存在；`SKILL.md` 歧义速判含"结构重复"指路，`logic` 行命令含 `--paragraph-roles`；`version` 仍 `6.0.0`；`last_updated` = 实施日期；description 长度 120~400；`tests/contracts/test_skill_contracts.py` 绿。
- [x] AC-04 两份 docs index 写作参考各含新指南链接、`logic` 行含 `--paragraph-roles`；`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh` 绿；`just doc-build` 绿；`tests/contracts/test_docs_bilingual_resources.py` 绿。
- [x] AC-05 `trigger_eval.json` 追加 ≥2 正例 + ≥1 负例，前 49 条哈希不变；`tests/contracts/test_trigger_evals.py` 绿。
- [x] AC-06 `analyze_logic.py evals/fixtures/thesis-project/main.tex --paragraph-roles` 退出码 0；不传 flag 时 `baseline-before.txt` 逐字节不变；`tests/skills/latex_thesis_zh/` 既有测试全绿。
- [x] AC-07 六码正反例测试全绿：第 2 章不报 `PR-INTRO-BG`；单独节号目录、单独路线预告均不报 `PR-INTRO-TOC`；阅读地图式导语不报 `PR-LEAD-DUP`；"式中"释义段不报 `PR-EQ-NARR`；小结 `\ref{tab:...}` 不报 `PR-SUM-NEW`。
- [x] AC-08 每条 finding 头含 `[Script] PR-`、`[Severity: Info] [Priority: P3]`，块含 `Meaning-Check: NEEDS-LLM`；报告不含任何 fixture 整句。
- [x] AC-09 YAML 六字段与内置默认相等，字段缺失/类型错/非法正则只回退该字段（测试断言）；两份 docs 镜像与源 YAML 相等。
- [x] AC-10 `SMOKE_COMMANDS` 新行、spec 文件与 index 行、`evals.json` id 51 存在；前 47 条哈希不变；`git diff --stat` 对两 evals 文件为纯增量。
- [x] AC-11 `just ci` 绿（check-versions / lint / typecheck / test 四步）。
- [x] AC-12 新增或修改的公开文件、fixture、测试不含私有语料或本机路径；`parsers.py`、`deai_check.py` 字节不变。

## Out of Scope

- 用户总结中第 2 节以外的任何内容。
- 绪论章与结论章的段落职责（各有专章指南）；实验结果段不新增检查码。
- `paper-audit`、`latex-paper-en`、`typst-paper` 的镜像或对齐。
- 既有码（章引言四项、S1、M-EQUATION、RA-*、P-ARC、S-CTX）的语义、阈值与输出格式。
- 私有语料标定与误报率声明；`version` bump；`justfile` / `pyproject.toml` / `uv.lock`。
- 自动改写：`logic` 仍是纯诊断模块，不新增改写契约。
- 父/子任务拆分（用户已选单任务）。

## 已确认决策

- D1 交付层级（用户 2026-09-20 回复"B"）：文档层 + opt-in `--paragraph-roles` 脚本层，单任务；文档层先单独 commit，脚本层失败不影响文档层。
- D2 章引言"详列每个小节顺序"：既有"节号目录 / 路线预告两态均合规"不变。追加：二选一、不在同一引言内双写；节号目录不逐节展开每节内容。脚本只报双写或 ≥ 阈值条逐节展开。
- D3 本章小结"再次列完整训练/部署流程"：既有"可'首先……最后'串方法要点"不变。追加：每个方法要点一个分句（章级粒度）合法，步骤级流水（数据加载→预处理→训练→部署逐步复述）不合法。仅 `[LLM]` 判定。
- D4 本章小结"新增论证"：既有"不新增结果、不新增引用"扩展为不新增引用、公式、图表、推导；回指本章已有图表（`\ref`）合法。
- D5 章引言"重新介绍整个行业背景"：与既有"禁重复绪论综述（清华§4.5）"并列为"背景与综述均不重述"；第 2 章概述式引言在脚本层豁免，指南仍建议不重述。

D2-D5 由仓库既有口径推出，已在 2026-09-20 规划摘要中呈现，用户未提出异议。
