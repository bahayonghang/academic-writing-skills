# C1 框架蒸馏与 Beamer 主题

## Goal

把参考预答辩框架蒸馏为 latex-defense-zh 的参考文档（模板、要点、规范），并实现 `yanshan` 与 `generic`
两个 Beamer 主题及共用页型宏包，用一份合成演示稿证明全部版式可编译。

## Parent / Dependencies

父任务 `09-23-latex-defense-zh`，对应父 R1（references 与 templates/beamer 部分）、R2、R3、R9（docs 资源登记部分）、R10。
无前置子任务；C2 依赖本子任务的宏 API（父 design §5）与版式名。

## Requirements

- C1-R1 `references/defense-framework.md`：全稿页序；五种章角色（intro、foundation、research、application、conclusion）
  的定义与识别提示；每种角色的页角色序列与默认页数；章前目录规则；阶段差异（predefense / defense 的封面字样、
  致谢页字样、defense 默认加成果页）；「问题 k → 研究内容 k → 创新点 k」对应链；「论文」框放置规则。
- C1-R2 `references/slide-layouts.md`：版式目录（至少 cover、toc、bullets、figure、figure-bullets、figure-grid、
  equations-figure、table、cards、paper-summary、outlook、thanks），每个版式给出规划字段、适用页角色、内容上限、调用的宏。
- C1-R3 `references/content-rules.md`：帧标题、小节条、结论句、要点条数与字数、正文字数、字号下限、图表编号沿用论文、
  图只用论文图、数字与单位和对照基准同出、公式逐字复制、强调词数量、溢出处置顺序、术语与缩写一致、学术事实保护、
  创新点与展望句式与取材、参考技能署名（名称与许可证）。
- C1-R4 `references/visual-spec.md`：两主题颜色、版位、字号层级表；pptx→Beamer 换算（系数 0.4724）；字体回退链；校徽尺寸与缺失回退。
- C1-R5 `references/time-budget.md`：40 分钟默认分配表；按分钟线性缩放规则与下限；30/40/60 分钟三档内容页区间。
- C1-R6 `references/speaker-notes.md` 与 `references/qa-prep.md`：讲稿五栏格式与字数；博士答辩提问类别与准备方法。
- C1-R7 Beamer：`templates/beamer/beamerthemeYanshanDefense.sty`、`beamerthemeGenericDefense.sty`、`defense-layouts.sty`
  实现父 design §5 的全部宏与颜色名；yanshan 复刻框架测量值；无校徽时显示文字标识。
- C1-R8 `templates/beamer/demo-deck.tex`：合成内容，覆盖 C1-R2 全部版式；通过 `\DefenseThemeName` 选择主题。
- C1-R9 公开内容卫生：不出现参考 pptx 作者、论文题目与内容；示例用中性合成题目。
- C1-R10 docs 资源登记：七份参考进入 `docs/resource-manifest.json`，并有双语资源页（zh 页与源一致，en 页完整翻译）；
  资源契约测试的技能集合与双语安装页命令包含 `latex-defense-zh`（父 design §7）。

## Acceptance Criteria

- [ ] AC1: 七份 references 存在，各含 C1-R1–R6 列出的主题小节；版式目录中的版式名与 `defense-layouts.sty` 宏一一对应。
- [ ] AC2: `test_defense_theme_assets.py` 断言 yanshan 主题六个颜色常量等于 visual-spec 表中 hex 值；两主题都加载同一宏包且不重定义版式宏。
- [ ] AC3: 设置 `DEFENSE_ZH_COMPILE=1` 且有 xelatex 时，演示稿在两主题下各编译成功；PDF 页数等于演示稿帧数；
  日志无 `Overfull \vbox`；generic 主题（无校徽）编译成功。
- [ ] AC4: 时长文档中 30/40/60 分钟区间与分配表自洽（各行页数之和落在区间内，研究章 ≥6 页）；由测试读取表格核对。
- [ ] AC5: `just lint`、`just typecheck` 通过；新增测试在默认 `just test` 下通过（编译用例 skip）。
- [ ] AC6: 技能目录内无校徽文件、无私有内容（人工 grep 记录，不把私有字符串写入测试）。
- [ ] AC7: `uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh` 与 `--inventory-only` 通过；
  `just ci` 通过（含 `tests/contracts/test_docs_bilingual_resources.py`）。
