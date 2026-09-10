# Qiaomu prior-art 与泛化裁决

研究日期：2026-09-10。交付是既有项目内的增量优化规划，采用 Production 的触发/输出/
证据检查思路；不在本轮制作新技能包，不声明 Library-ready/Governed-ready，不改原作者、
名称、Academic Use Only 许可，也不套入 qiaomu 命名/版权或发布流程。

## 检索与来源

意图查询：`thesis latex`、`scientific writing evidence`、
`Research-Paper-Writing-Skills reverse outline`。
已执行 skills.sh / SkillsMP 站点限定网页检索、打开两目录首页及 GitHub 原始仓库。
本轮有完整本地 ref 快照，未运行会通过 npx 获取 CLI 的统一 runner；
没有把脚本未运行描述成目录故障。未安装、执行候选技能脚本或 hooks。

原始目录入口：[skills.sh](https://skills.sh/)、[SkillsMP](https://skillsmp.com/)。
目录仅用于发现，采用依据来自以下具体源码。按仓库与 skill 路径去重，
语言页/host mirrors 不独立计数；本库自身的搜索命中不算外部对照。

| 候选与源码 | 本轮具体学习 | 采用位置 | 明确拒绝 | 来源/许可与限制 |
| --- | --- | --- | --- | --- |
| [research-paper-writing](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/main/research-paper-writing/SKILL.md)；本地 ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md | 逆向提纲检查段主题与章节目标、证据与段主题两条关系 | C1 扩充现有 logic-and-experiment 示例 | 固定 ML/CV/NLP 体裁、要求所有请求给整篇提纲、标签式强制句首 | 本地 LICENSE 为 MIT；原作者声明参考 Peng 的写作资料；源码可读，不证明写作效果 |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine) 的 paper-spine-rewrite；本地 ref/PaperSpine/dist/claude/skills/paper-spine-rewrite/SKILL.md | 修改前梳理原稿角色、可见证据与处置原因，按实际文章单元组织 | C1 的一个人工示例，缩减为必要输出 | 固定配置/产物树、强制 research/rewrite worker 流程、tier 与 launcher | 本地 LICENSE 为 MIT；只研究文档，不执行源码声明的脚本或委派 |
| [writing-anti-ai](https://github.com/Galaxy-Dawn/claude-scholar/blob/main/skills/writing-anti-ai/SKILL.md) | 学到去冗余须同时守住原意；也暴露“三项就拆、补个性/观点”的泛化风险 | 保留现有 deai-pattern-cluster 和 fidelity audit；本轮不新增 H-* | 按词/标点推断作者身份、注入观点、固定 quick score 与检测逃避承诺 | frontmatter/README 为 MIT；社区模式不是官方论文规范 |

本地快照的上游精确 commit 未复核；上游页面已打开，但不宣称本地与远端逐字一致。
三个候选的 skills.sh installs、SkillsMP repo stars、独立 user ratings、源码安全审计和
真实输出质量对比均为 missing evidence。未选定“最高人气”或“官方权威”候选；
不能由 stars、目录展示或仓库名补足这些身份。只有 license/源规则可读性证据。

## keep / adapt / reject / invent

- keep：已有 school/template authority、protected tokens、source fidelity、M-/RA-/P-ARC/S-CTX、
  双语资源门禁与分层证据。
- adapt：research-paper-writing 的逆向提纲和 PaperSpine 的原稿逻辑映射，压缩为既有
  example 中的一次人工复核。写作诊断默认只建议，不越过改写授权。
- reject：新 orchestrator、IR、状态机、词典、配置层、安装器、hooks、固定产物树，
  以及从单次论文案例推出跨学科硬阈值。
- invent：把本地新旧指南的冲突作为具体反例，联动 C1 的输出核读、C2 的语义边界探针、
  C3 的产物位置检查。它们是本任务设计，不是已验证的优越性。

## 泛化门槛

| 经验 | 无领域依赖的表述 | 归类 |
| --- | --- | --- |
| 不虚构 3.2%/不以 95% 推出提升 | 示例不得创造输入中没有的事实或比较 | 已有事实保护 core 的修复 |
| 消融不自动证明因果 | 主张资格来自实际设计与证据，不能仅看标签 | 已有证据阶梯 core 的一致性修复 |
| 不强制 GPU/固定摘要长度 | 通用建议服从目标体裁与来源规范 | 可选 specialist adapter；不改学校阈值 |
| 逆向提纲 | 需要时核对写作单元与目标和证据的关系 | example/人工操作，不新增默认扫描 |
| 深度学习与深度神经网络 | 共现与词频不证明概念等价 | 删除错误默认假设，保留显式用户组 |
| 缩写先用后定义、章间重引 | 校验必须使用真实顺序和归属 | 有确定结构证据的 script 修复 |
| outdir 与 PDF 查找一致 | 成功判据应读取本次命令实际产物位置 | 现有 IO 边界修复 |

## 设计优势与未验证效果

- **design advantage**：无需增加用户配置即可消除三个已定位的失败来源。
- **design advantage**：每个修改对应错误样例与合法反例，保持读写范围清楚。
- **validated advantage**：无；仅已验证当前缺陷可复现及已有测试基线通过。
- **hypothesis**：新指南能减少无依据增强和错误术语统一，需要 C1 实际响应核读后再评价。
- provider A/B、人工盲评、真实论文总体效果、五宿主与真实学校排版均 missing evidence。


## 实施后验证补充（2026-09-10）

规划阶段的采用/拒绝裁决保持不变。实施没有制作新技能包或扩张配置：
research-paper-writing的逆向提纲与PaperSpine的证据映射已落入原logic示例，
writing-anti-ai相关事实保护沿用既有规则。设计优势仍限于职责和文件范围的简化。

**validated advantage（有限场景）**：C2/C3原缺陷有失败回归与修复后完整CI证据；
八类新版实际响应通过独立保真核读，旧版场景8对合法综合引用的额外展开倾向未再出现。
旧版其余多数边界也已通过，不能宣称总体写作质量提升、对比因果效果或优于候选技能。
全量CI最终1908 passed/2平台skip、资源271项、docs构建及隔离真实TeX通过。

**hypothesis / missing evidence**：跨领域泛化、真实论文总体效果、provider benchmark、
人工盲评和五宿主运行仍未验证。完整结果见
[实施验收](../research/integration-validation.md)与独立响应/实施审查。
