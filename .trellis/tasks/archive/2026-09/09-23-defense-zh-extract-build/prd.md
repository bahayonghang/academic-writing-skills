# C2 论文提取、页面规划与答辩稿构建

## Goal

实现 latex-defense-zh 的确定性流水线前三段：从中文学位论文 LaTeX 仓库提取清单（inventory.json），
按时长与阶段生成规划骨架（slide_plan.yaml），把 LLM 填写后的规划渲染为可编译的 Beamer 答辩稿与讲稿。

## Parent / Dependencies

父任务 `09-23-latex-defense-zh`，对应父 R4、R5、R6、R8，以及 R1 的 scripts、templates/jinja、plan-schema 参考与 fixture 部分。
前置：C1 已完成并通过其质量门。本子任务只调用父 design §5 的宏名与 C1 `slide-layouts.md` 的版式名，不改 C1 文件。
C3 依赖本子任务的帧标记、清单字段与 `scripts/defense_budget.py`。

## Requirements

- C2-R1 `scripts/tex_loader.py`：latex-thesis-zh 副本，仅改模块 docstring 中的技能名；加载链、行号映射与编码回退不变。
- C2-R2 `scripts/extract_thesis.py`：只读提取父 design §4 的清单字段；主文件选择、章节树、章角色建议、图（aux 图号优先、
  计算回退、子图）、表、带标签公式、算法、成果与章对应、结论章贡献与展望、校徽候选；异常以 `warnings[]` 报告，不中断。
- C2-R3 `scripts/defense_budget.py`：实现 C1 `references/time-budget.md` 的公式，返回每章每页角色的页数与秒数、内容页总数 N
  与 D-BUDGET 区间；plan 与 C3 check 共用。
- C2-R4 `scripts/plan_deck.py`：由清单、分钟数（默认 40）、阶段、主题生成规划骨架：每帧含 id、role、layout、chapter、
  section、预算秒数、候选图表、源位置，待填字段用统一占位符；`--outline` 按页序输出帧标题与结论句。
- C2-R5 `scripts/build_deck.py`：校验规划，渲染 `defense.tex`、`notes.md`、`build_manifest.json`，复制主题与宏包文件；
  图以相对 `\graphicspath` 引用论文原图；公式体与表体取自清单源文本；普通文本转义；每帧前写帧标记；
  覆盖保护与可选编译（父 design §3 退出码）。
- C2-R6 `templates/jinja/deck.tex.j2` 与 `templates/jinja/frames/<layout>.tex.j2`：十二个版式各一个帧模板，只调用 C1 宏。
- C2-R7 `references/plan-schema.md`：清单与规划全部字段、类型、取值、占位符、转义规则、公式与表体的变换规则；
  同步双语资源页与 manifest（父 design §7）。
- C2-R8 `evals/fixtures/mini-thesis/`：合成论文（绪论、基础章、三研究章、应用章、结论章；正式版与盲审版两个主文件；
  部分章有 aux、部分没有；成果列表含中文数字章号；一个中文文件名图）。图片不入库，测试运行时生成。
- C2-R9 学术事实保护：不改论文仓库任何文件；不生成新图；公式与表体只做 design 列出的确定性变换；
  规划文本字段不支持内联数学与任意 LaTeX。

## Acceptance Criteria

- [ ] AC1: fixture 提取结果的章角色建议为 intro、foundation、research×3、application、conclusion；aux 章图号为 aux 值，
  无 aux 章图号为计算值且 `number_source: computed`；子图字母与题注正确；成果—章映射含一条多章条目；
  结论贡献 3 条、展望 2 条；提取前后 fixture 全部文件 SHA-256 不变。
- [ ] AC2: 主文件规则：只有正式版与盲审版两个候选时选正式版并写 warning；两个非盲审候选且无 `--main` 时退出码 2。
- [ ] AC3: `defense_budget.py` 对 C1 time-budget 三档与两种结构返回表中数值（参数化测试）；plan 骨架内容页数落在区间，
  每研究章 ≥6 页。
- [ ] AC4: fixture 生成稿的帧标记序列满足父 AC2 页序（每章前目录、研究章五种角色、结论创新点与展望、末页致谢）。
- [ ] AC5: 转义测试覆盖 `% & _ # $ { } ~ ^ \`；`**词**` 渲染为 `\DefenseHighlight{词}`；公式与表体按 plan-schema
  变换规则还原后与清单源文本逐字一致；`\graphicspath` 为相对路径。
- [ ] AC6: 目标文件已存在且无 `--force` 时退出码 4 且不写任何文件；`--force` 只覆盖 build 自有文件；
  未知 role、layout 或清单外 label 时退出码 2。
- [ ] AC7: 有 xelatex 且 `DEFENSE_ZH_COMPILE=1` 时，fixture 生成稿在两主题下编译成功；否则 skip。
- [ ] AC8: `check_resource_sync.py --skill latex-defense-zh` 通过；`just ci` 通过。
