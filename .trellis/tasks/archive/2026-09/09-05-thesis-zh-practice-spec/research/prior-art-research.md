# Prior-art 与 Qiaomu 取舍

## 检索过程

日期 2026-09-05；仅外发通用查询，无论文文本、路径或数据。
使用 qiaomu-meta-skill 2.8.1 的发现/泛化方法，本轮为现有技能优化规划，不是新包/发布。

查询意图：
1. thesis writing（中文学位论文写作结果）
2. academic writing evidence（证据机制）
3. thesis chapter revision（章节修订）

本机统一 runner 内部使用 npx，可直接调用的 Windows 命令为 npx.cmd；
拆为 `rtk proxy npx.cmd --yes skills find 'thesis writing'` 和 bundled
research_prior_art.py 的两项 SkillsMP 查询（--skip-skills-sh --timeout 12 --retries 0）。
Skills.sh CLI 返回成功；SkillsMP 两查询分别返回7与8项，去重为15家族。
双目录使用不同查询，未获得逐查询双目录 strict-complete 证明。
网页目录搜索页曾被浏览工具拒绝打开，CLI/API 后备成功，不能称目录全面失败。

Skills.sh 此次查询中本仓库 latex-thesis-zh 为约3.8K installs，
chinese-thesis-workbench 241，thesis-standardizer 174；
这些是当日显示值、不是评分/质量。SkillsMP 仓库 stars 与 installs 不合并。
投资 thesis、交易篮子、专利/PPT 等关键词撞车候选剔除；同一 K-Dense 仓库旧
claude-scientific-skills 路径和新 scientific-agent-skills 路径合并，不当独立证据。

## 已阅读候选与具体启发

| 候选 | 学到什么/采纳位置 | 刻意不采纳 | 信任及权限边界 |
| --- | --- | --- | --- |
| 本仓库 latex-thesis-zh | 现有 M/RA/P-ARC/S-CTX、源码保真、渐进加载；保持其 owner | 不以旧归档任务推断脚本存在 | 本轮源码/CLI可核；3.8K只为目录采用信号 |
| K-Dense scientific-writing | 从给定证据组织提纲再写正文、核对数值与声明；用于证据保真正反例 | 多注册表、全流程提交治理、额外发布步骤不迁入 | 当前根声明 MIT；可选CLI离线的说法仅为源声明，未执行安全审计 |
| K-Dense scientific-critical-thinking | 区分观察/解释、相关/因果、证据范围；用于工程章和结果边界 | 医学GRADE体系、评分和可选外部图像API不迁入 | 根声明MIT；可选图像外发依赖OPENROUTER_API_KEY，未调用 |
| chinese-thesis-workbench | 先厘清学校要求与项目事实、有限证据只支持有限写作；用于模板条件与工程事实 | DOCX四路径、workflow状态文件、强制ER图和附录交付不迁入 | 根/README已读，仓库显示MIT；Playwright等仅查说明、未安装 |

来源：
- [当前 scientific-writing 根](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md)
- [scientific-critical-thinking 根](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-critical-thinking/SKILL.md)
- [chinese-thesis-workbench 根](https://github.com/ZyhSechub/chinese-thesis-workbench-skill/blob/main/SKILL.md)
- [workbench 许可与仓库说明](https://github.com/zyhsechub/chinese-thesis-workbench-skill)
- [目标技能目录条目](https://skills.sh/bahayonghang/academic-writing-skills/latex-thesis-zh)

K-Dense 两个技能为同一仓库的互补机制，不按两个独立质量背书。
检索出现的旧版本“必须生成图片”等要求与当前根不同，以本轮打开的新路径为准，
不把旧缓存内容写成当前行为。

## Keep / adapt / reject / invent

- keep：现有模块、LaTeX token保护、启发式候选与语义复核分工、双语资源约定。
- adapt：源实践的章型差异、工程链条、展示/统计区分；转换为短指引与跨领域合成反例。
- reject：私有参数/数据、去限定增断言、固定数字/字数/章号、别的包的注册表/状态机和依赖。
- invent：把源实践—当前缺口—具体owner—验收例连接起来，题注用真实红/正对照证明修复目标。

## 证据等级与缺项

- design advantage：增量落在现有模块，保留真实限制，避免另建通用架构。
- validated advantage：本轮没有改善后的技能输出，不作此类声明；仅诊断了题注缺陷。
- hypothesis：章型和证据指引会提高实际输出质量，需未来合成响应与人工/模型评审验证。
- missing evidence：独立用户评分、严格全目录对比、候选安装/运行/安全审计、
  精确维护提交时间、K-Dense独立LICENSE文件复核（页面打开失败）、provider A/B、
  人工盲评、真实论文效果及跨平台验证。根声明MIT不替代完整许可审计。
