# 外部依据与先行技能研究（qiaomu-meta 路径产物）

> 用途：参考文件写作时的引用来源与借鉴取舍依据。检索日期 2026-08-09。

## 1. 学理一手来源（新参考文件应引用）

- Gopen & Swan, "The Science of Scientific Writing", American Scientist 78(6), 1990.
  https://www.americanscientist.org/blog/the-long-view/the-science-of-scientific-writing
  要点：topic position 承接旧信息（向后链接）、stress position 放置新强调信息；
  "provide context before asking the reader to consider anything new"。
  对应用户 spec §8"段首承接当前约束或上游对象；段末给出输出、作用或下一步接口"。
- MIT EECS Communication Lab, Paper: Methods (EE)。最低必要论证；小标题建立逻辑流但不替代衔接。
  https://mitcommlab.mit.edu/eecs/commkit/journal-article-methods-ee/
- MIT MechE Comm Lab, Journal Article: Methods。"emphasis on how and why you applied a method
  rather than on how you performed the method"。
- IEEE Author Center, Structure Your Article（可复现性）；Nature Formatting Guide（简洁 + 全要素）；
  PLOS ONE Submission Guidelines（统计细节）。
- 方法章组织的一致外部口径（佐证 spec §2 总体顺序）：Southampton LibGuides（线性分层、
  决策影响后续决策）、USC LibGuides（general→specific、常见缺陷含 Irrelevant Detail /
  Unnecessary Explanation）、Monash / Federation（结构模板）。

## 2. 先行技能（prior-art，keep/adapt/reject/invent）

检索渠道：skills.sh 目录（`npx skills find`）+ SkillsMP（qiaomu-meta search_skillsmp.py）+ exa。
注：qiaomu-meta 自带 `research_prior_art.py` 在 Windows 下 subprocess 调 `npx` 失败
（WinError 2，npx.cmd 不可见），已用底层命令替代——该脚本缺陷已另行反馈。

| 候选 | 结论 |
| --- | --- |
| EvoScientist/EvoSkills `paper-writing/references/method-templates.md` | **adapt**：三要素（Motivation/Design/Advantages）与 Module Motivation Mapping 表（Module/What/Why needed/Advantage）。缺口＝无逐边接口、无 M-NONDIRECT、Advantages 无证据分级。本任务把逐模块表升级为逐边接口表 |
| EvoSkills `paper-planning/references/story-design.md` | 参考：pipeline 草图五步（novel 模块标注 + 单句动机）；challenge framing 反模式清单 |
| Yuan1z0825/nature-skills 标注范例（neural-body） | 参考：Motivation/Design-1/Design-2/Advantage 段落级标注示范 + 段落起手式 |
| jvgemert Storyline | 参考：house of whys、每个主张可被实验挑战 |
| zlab-princeton writing-guide | 参考：段落 5-8 行、一段一点、可一句话复述 |
| imbad0202/academic-research-skills@academic-paper（7.7K 安装） | **reject**：12-agent 全流程生成型，与本仓库"写后打磨/校验"定位不同轨 |
| affaan-m scholar-evaluation 等 | 评审型，与 paper-audit 已有能力重叠，不引入 |

计量口径：skills.sh 安装数≠质量评分；SkillsMP 星数属仓库非技能。本仓库自身已发布
（latex-paper-en 4.7K / paper-audit 2.5K / typst-paper 1.2K 安装），改动按 Production 级要求
带测试与文档证据。

## 3. 原创点（先行技能均无）

1. 六类连接类型判据表（串行数据/并行表征/监督目标/校准选择/反馈控制/剩余约束）。
2. M-NONDIRECT：无直接依赖须主动排除误读。
3. 报幕反模式的节门控脚本启发式（M-HEADING/M-SEQWORD/M-EQUATION）。
4. 四类主张（定义事实/机制作用/经验性能/因果归因）× claim-evidence 强度梯映射。

## 4. 证据缺口（missing evidence）

- 脚本启发式查准率：hypothesis，靠 fixture 与红线负例锁定，落地后由 C3 集成验收记录。
- trigger eval 未运行（实施完成后按需补例并跑）。
- WebSearch（内置）当日 429，检索由 exa 完成。
