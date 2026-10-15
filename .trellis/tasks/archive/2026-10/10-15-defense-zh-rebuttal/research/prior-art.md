# rebuttal 先例调研（2026-10-15）

## 1. 检索记录

- skills.sh：`npx skills find "rebuttal reviewer response"`。安装量（采集日 2026-10-15）：
  `mrilikecoding/dotfiles@rebuttal` 27、`onireimu/knows@knows-rebuttal-builder` 23、`chtc66/academic-skills@review-rebuttal` 11、
  `m1n-n9/paper-lifecycle@rebuttal-response` 8、`msimchowitz/writing-skills@rebuttal-writing` 6、`research-equality/re-paper-writing@rebuttal-writing` 6、
  `kalarislabs/research-agent-skills@rebuttal-and-response-to-reviewers` 4。
- SkillsMP（`search_skillsmp.py "rebuttal" --sort stars`）：`Imbad0202/academic-research-skills-codex`（仓库星 12576）、
  `HKUSTDial/Supervisor-Skills` rebuttal-guidance（仓库星 8934）、`Galaxy-Dawn/claude-scholar` review-response（仓库星 5749）。
  星数属于源仓库，不是该技能的评分。
- Web：`wanshuiyin/Auto-claude-code-research-in-sleep` 的 `skills/rebuttal/SKILL.md`（已读全文前半）、`TobiasLee/Rebuttal-Skill` README（已读）。
- `research_prior_art.py` 在 Windows 上因调用 `npx` 而非 `npx.cmd` 失败（FileNotFoundError）；改为直接运行两条目录命令。
- 缺失证据：未运行任何候选技能；除 ARIS 与 TobiasLee 外只读了目录描述或页面摘要。所有候选都面向期刊或会议投稿，没有面向中文学位论文评阅书的技能。

## 2. keep / adapt / reject / invent

| 来源                        | 机制                                                                          | 决定   | 落到本任务                                                                                                      |
| --------------------------- | ----------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------- |
| ARIS rebuttal               | Provenance / Commitment / Coverage 三道门                                     | adapt  | R-NUM-SRC（回复中的数字须出自论文）、R-COMMIT 与 R-CLAIM（「已修改」须有修改证据）、R-COVER（每条意见都有去向） |
| ARIS rebuttal               | 评审原文逐字归一到 `REVIEWS_RAW.md`；`REBUTTAL_STATE.md` 断点续做             | keep   | `workspace/reviews/R<n>.md` 与 `workspace/rebuttal_state.json`                                                  |
| ARIS rebuttal               | 跨模型压力测试、字符预算、OpenReview 线程模式                                 | reject | 评阅书回复无字数上限（表格「可插页」），无多轮线程                                                              |
| TobiasLee Rebuttal-Skill    | 原子化意见、严重度、P0–P3 优先级；可见占位符；不把计划写成已完成              | keep   | 台账 `severity`、`priority`；R-PLACEHOLDER；R-CLAIM                                                             |
| TobiasLee Rebuttal-Skill    | Direct Answer → Evidence → Revision                                           | adapt  | 「意见 / 回复 / 修改位置」三段，回复首句写处理动作                                                              |
| TobiasLee Rebuttal-Skill    | Stage 0 是否值得 rebuttal、补实验计划                                         | reject | 学位论文评阅意见须全部回复，不存在放弃选项                                                                      |
| Imbad0202 ARS               | R&R traceability matrix（意见 → 修改主张）；rebuttal-audit 只做建议           | adapt  | 台账 `locations` 与 `evidence`；`rebuttal_check.py` 只报告不改文件                                              |
| Galaxy-Dawn review-response | Major/Minor/Typo/Misunderstanding 分类；Accept/Defend/Clarify/Experiment 策略 | adapt  | `action` 枚举：revise / add / clarify / partial / future_work / decline                                         |
| Galaxy-Dawn review-response | 「提高录用率」类断言、ICLR 案例经验                                           | reject | 与学位论文评阅无关，无证据                                                                                      |
| chtc66 review-rebuttal      | 未做的实验写成计划或澄清，不写成已有结果                                      | keep   | R-CLAIM                                                                                                         |
| HKUSTDial rebuttal-guidance | 说服模型 P(Z\|X,Y)、历史 rebuttal 检索                                        | reject | 评阅书不是录用谈判，且需要联网与外部语料                                                                        |

本任务新增（invent）：

1. 纯文本等价 Markdown：responses 只用段落与普通文字行，原样复制与渲染后复制得到同一文本，便于粘贴到 Word。
2. aux 编号追踪：intake 把评阅书中的「图2-7」映射到 LaTeX 标签；build 用修改后 aux 取新编号与页码，编号变化时写「原图2-7（现图2-8）」。
3. git 基线证据：intake 记录论文仓库提交，check 只认「台账声明位置的文件自基线以来有改动」。
4. 同级目录布局与「预评审结果」行（总体评价 1/2）。

## 3. 领域规范来源

- 北京理工大学博士学位论文匿名评阅规定：评阅意见有 B 时须书面修改说明，导师签字，附评阅书存档。
  <https://soe.bit.edu.cn/docs//2024-05/d756666add2d441282769e7925b7b345.pdf>
- 中国科学院大学公管学院：修改情况须写具体修改内容，不能只写「已修改」。
  <https://sppm.ucas.edu.cn/index.php/zh-CN/jxpy/pygl/xwlw/503-2015-07-28-06-41-07/1315-2017-05-04-10-08-13>
- 南京邮电大学：每位专家一份修改与完善情况表，针对该专家意见。<https://pg.njupt.edu.cn/2011/0419/c981a20666/page.htm>
- 南京大学：只涉及格式的意见与涉及实质内容的意见填写范围不同。<https://grawww.nju.edu.cn/28/fe/c906a10494/page.htm>
- Flinders University：修改表须写明修改位置，含页码。<https://students.flinders.edu.au/my-course/hdr/examinations/thesis-amendments>
- MISQ 修改回复指南：不把整段正文贴入回复，写明修改位置。<https://misq.umn.edu/revision-response>
- Nottingham 答辩后修改回复实例：每位考官单独表格，逐条回复。<https://eprints.nottingham.ac.uk/66097/11/response%20to%20examinars_10279197_Kwon%20Jun%20Lee.pdf>
- 修改矩阵（意见原文 / 论文位置 / 类型 / 计划 / 状态）：<https://www.proof-reading-service.com/blogs/theses-dissertations/when-major-revisions-are-required-after-your-thesis-or-dissertation-exam>
- 中文回复写法汇总：<https://zhuanlan.zhihu.com/p/624112024>、<https://zhuanlan.zhihu.com/p/556931205>

归纳出的规则：先总体说明再逐条；不合并回复；每条写处理内容与修改位置（章节 + 图表号 + 页码，页码指修改稿）；
不采纳时给学术理由，不以时间或经费为理由；全部改完后重新核对页码。

## 4. Markdown 粘贴到 Word

- Typora 与 pandoc 都能导出 docx，中文字体需 `--reference-doc` 模板设置。<https://github.com/Achuan-2/pandoc_docx_template>
- 从渲染视图复制会带入主题字体与颜色；从源码复制会留下 `#`、`**`、`|` 等标记。<https://www.zhihu.com/question/473638695>
- 决定：用户要求 Markdown 且粘贴进既有 Word 表格，不需要独立 docx。采用纯文本等价 Markdown，两种复制方式结果一致；不引入 pandoc 依赖。
