# 参考技能与先例检索（2026-09-23）

## 1. 用户指定的两个参考技能（只读，未执行其代码）

### 1.1 `ref/claude-skill-academic-ppt`（MIT，README 第 95–97 行）

产物为 python-pptx 生成的 .pptx；输入优先 LaTeX；三种场景模板（defense/conference/seminar）。

| 机制                                                   | 处置   | 在 latex-defense-zh 中的落点                                                                 |
| ------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------------- |
| 行动标题（结论句作标题）+ Ghost Deck 串读测试          | adapt  | 答辩框架要求节号标题「k.x …」，结论句放入每页 `takeaway` 行；串读测试对 takeaway 序列执行    |
| 每页讲稿五栏（说什么/要点/时长/过渡/可能提问）         | keep   | `references/SPEAKER_NOTES.md` + `notes.md` 输出 + `\note{}`                                  |
| Q&A 预测（方法/有效性/规模/对比/未来五类）             | adapt  | 增加博士答辩专属类：创新点界定、章间逻辑、成果对应、工程落地；`agents/qa_committee_agent.md` |
| 时间预算（按分钟分配各段页数）                         | adapt  | `references/TIME_BUDGET.md`；默认 40 分钟，按章角色分配                                      |
| 幻灯片数字与源文对照，标记潜在编造                     | keep   | `check_deck.py` 的 D-NUM-SRC                                                                 |
| 一页一意、正文 ≤6 条、数字带参照                       | keep   | `references/CONTENT_RULES.md`                                                                |
| 白底、单一无衬线字体、≤3 色、无装饰                    | reject | 与燕山框架视觉冲突；框架有深蓝题带、红色强调、校徽                                           |
| Gemini 生成概念图、Mermaid 兜底、Matplotlib 重绘数据图 | reject | 违反学术事实保护；答辩图只用论文已有图                                                       |
| python-pptx 装配                                       | reject | 用户要求 LaTeX/Beamer                                                                        |
| `\input` 递归三层解析                                  | reject | 使用仓库已有 `tex_loader.py`（行号映射、编码回退）                                           |

### 1.2 `ref/thesis-defense-pptx-skill`（Apache-2.0，NOTICE 署名 zouchenzhen）

产物为按学校 .pptx 模板克隆页面后替换内容的可编辑 .pptx；Windows + PowerPoint COM。

| 机制                                                                   | 处置   | 落点                                                           |
| ---------------------------------------------------------------------- | ------ | -------------------------------------------------------------- |
| 源素材清单：只允许使用论文 `\includegraphics` 引用过的图（allow-list） | keep   | `extract_thesis.py` 输出图清单；`check_deck.py` 的 D-FIG-ALLOW |
| 模板是视觉真源，保留封面、配色、导航、字号层级                         | adapt  | 由 pptx 测量值蒸馏出 Beamer 主题与 `references/VISUAL_SPEC.md` |
| 先缩短文字/拆页，再考虑缩小字号                                        | keep   | CONTENT_RULES 的溢出处置顺序                                   |
| 逐页导出 PNG + 总览图目视检查                                          | keep   | `render_preview.py`（PyMuPDF 懒加载 + Pillow 拼图）            |
| 旧模板词/占位符扫描                                                    | keep   | D-PLACEHOLDER                                                  |
| 文字溢出检查（COM BoundHeight）                                        | adapt  | 改为 XeLaTeX 日志 Overfull \vbox/\hbox 映射到帧                |
| 目录/导航与实际页序一致                                                | keep   | D-TOC                                                          |
| COM 克隆模板页、dump-before-replace、replace_partial_text              | reject | Beamer 由规划文件直接生成，无克隆替换环节                      |

两者都未覆盖：博士答辩「问题 k → 研究内容 k → 创新点 k」对应链、章角色（基础章/研究章/应用章）、
成果—章对应的「论文」框、预答辩与正式答辩的阶段差异。这些列为本技能的新增设计（invent）。

许可处置：只采纳机制，不复制源码或原文；在技能参考文档中注明两项目名称与许可证。

## 2. 目录检索（qiaomu-meta-skill 先例检索）

执行时间 2026-09-23。统一脚本 `research_prior_art.py` 在 Windows 上以 `npx` 无 `.cmd` 后缀调用失败（WinError 2），
改为分别调用两个目录。

skills.sh（`npx --yes skills find`；指标为安装量，表示采用度，不表示质量）：

| 查询                  | 候选                                                           | 安装量 | 相关性                                                                                                    |
| --------------------- | -------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------- |
| thesis defense slides | ykim22566-create/thesis-defense-pptx-skill@thesis-defense-pptx | 8      | 与 §1.2 同名同类（pptx 模板路线）                                                                         |
| thesis defense slides | vadym-khodak/researcher-skills@thesis-defense                  | 7      | 答辩准备：按学位类型生成提问与答案、复查演示；无生成稿件                                                  |
| beamer presentation   | zhouziyue233/great-econometrics@beamer-ppt                     | 8      | 名称含 beamer，产物为仿 Metropolis 风格的 pptx；规则：一页一意、正文 ≥20 pt、末页放结论不放「Questions?」 |
| beamer presentation   | wentorai/research-plugins@beamer-presentation-guide            | 4      | 未展开阅读                                                                                                |

SkillsMP（`search_skillsmp.py --sort stars`，需 `PYTHONIOENCODING=utf-8`；指标为仓库星数）：
两次查询返回的前 8 条均为高星仓库中的无关技能，记为无相关证据。

采纳：beamer-ppt 的「末页不以 Questions 结束」与框架致谢页一致（keep，已由框架覆盖）；
thesis-defense 的按学位类型分类提问（adapt 到 QA_PREP）。
缺失证据：未检索到以 LaTeX Beamer 生成中文博士答辩稿的现有技能；未做安装试用与质量对比。
