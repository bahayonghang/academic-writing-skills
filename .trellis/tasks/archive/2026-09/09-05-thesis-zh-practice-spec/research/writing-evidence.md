# 写作规范证据矩阵：论文实践 spec → `latex-thesis-zh`

## 范围与结论

- 只读检查了论文项目指定的 9 份 writing spec 全文，并与当前
  `academic-writing-skills/latex-thesis-zh` 的公开参考、脚本、eval 和仓库级契约比对。
- 源根记为 `S = D:/Documents/LYH/200-Learning/00博士毕业/毕业论文/thesis/.trellis/spec/writing`；
  目标根记为 `T = academic-writing-skills/latex-thesis-zh`。
- 源 spec 对参考论文、学校规范和“最佳篇幅”的自述未在本轮独立复核；网络被明确禁用，故这些
  来源强度主张均为 `UNVERIFIED`。本轮能确认的是源文件内容与当前仓库实现。
- 建议只做 3 个 LLM/公开资源增量：摘要工作段因果链、本章小结章型化、综述宏观综合与微观归因。
  不新增脚本规则、配置层、检查码或运行时正则；method、RA、paragraph、subsection、process 能力不重做。

## 全文件覆盖与裁决

| 源文件（全文行数） | 当前覆盖证据 | 裁决 |
| --- | --- | --- |
| `S/abstract.md`（54） | `T/references/writing/abstract-structure.md:92-163`；`T/references/modules/abstract.md:18-33`；`T/scripts/analyze_abstract.py:796-868,988-1117` | **部分**：骨架、字数、中英对齐已覆盖；多组件工作段因果链缺失，值得补 LLM 规则 |
| `S/chapter-intro-two-paragraph.md`（90） | `T/references/writing/thesis-writing-guide.md:42-78`；`T/references/writing/process-chapter-guide-zh.md:211-230`；`T/scripts/analyze_logic.py:558-757` | **已覆盖**：两种引言形态、第 2 章免承上、依赖分级、篇幅均已实现；源“恰好两段”只作局部偏好 |
| `S/chapter-summary.md`（175） | `T/references/writing/thesis-writing-guide.md:80-109`；`T/evals/evals.json:495-518` | **部分/最高价值**：已有单段五角色与基础 eval；缺章型差异、模块主体衔接、验证范围与联合任务覆盖 |
| `S/literature-review.md`（344） | `T/references/modules/literature.md:9-65`；`T/references/writing/thesis-writing-guide.md:111-125`；`T/scripts/analyze_literature.py:47-64,184-270` | **部分**：A1-A3 和重写链已覆盖；缺“主题综合”与“单篇归因句”的层级接口 |
| `S/method-description.md`（334） | `T/references/writing/method-description-guide-zh.md:18-209`；`.trellis/spec/academic-writing-skills/method-narrative-contract.md:48-147` | **已覆盖+局部夹带**：前 253 行已实质落地；257-333 行是特定水泥章节/模型/符号，不迁移 |
| `S/paragraph-transition.md`（268） | `T/references/writing/paragraph-arc-zh.md:20-95`；`.trellis/spec/academic-writing-skills/paragraph-arc-contract.md:29-56`；`T/references/writing/subsection-context-zh.md:7-48` | **已覆盖+条件参考**：通用段落接口已落地；固定五段/P1-P5 与冒号逐项清扫属于本论文工作表 |
| `S/problem-statement-and-chapter-arrangement.md`（141） | `T/references/writing/introduction-guide-zh.md:13-27,70-104`；`T/references/writing/thesis-writing-guide.md:21-40` | **部分但非首批**：功能分区、科学问题与四方闭合已有；细化问题段/章安排句式可后续按需求吸收 |
| `S/process-and-framework-chapter.md`（71） | `T/references/writing/process-chapter-guide-zh.md:17-63,86-182,211-230` | **已覆盖+局部夹带**：章式、因果推导、框架图、绪论分工、第 2 章引言均已有；固定 2.3-2.6 与模型符号不迁移 |
| `S/anti-defensive-hedging.md`（86） | `T/references/writing/over-claim-guard.md:6-42,110-126`；`T/references/writing/results-analysis-guide-zh.md:18-33,192-230,248-282`；`.trellis/spec/academic-writing-skills/defensive-ai-rhetoric-contract.md:32-50` | **冲突/大部拒绝**：只保留“正面定义、删元话语”的风格方向，拒绝删证据边界或提高确定性 |

## D1：摘要编号工作段的多组件因果链（核心机制）

**源→当前差异**

- `S/abstract.md:12-19` 要求“基础机制→剩余瓶颈→增强模块→质量控制”说明组件必要性；当前
  `T/references/writing/abstract-structure.md:100-110` 只给“针对问题→提出方法→实验表明”的单层骨架，
  `T/scripts/analyze_abstract.py:780-810` 也只观察问题开头与验证方式。该差异真实存在。
- `S/abstract.md:6-10` 的“正文一律无具体数值”不应硬化；当前
  `T/references/writing/abstract-structure.md:114-121` 明确数字可选，适合多校/多学科技能。
- `S/abstract.md:32-45` 的中英镜像、句间逻辑已由 B-ORD/B-NUM/B-ENUM/B-SEM 与现有骨架覆盖
  （`T/references/writing/abstract-structure.md:143-163`），无需新检查码。

**建议落点**

- 在 `T/references/writing/abstract-structure.md` 增加一小节：仅当一个编号工作含两个以上有依赖的
  组件时，按“当前约束→组件作用→剩余约束→下一组件→验证对象”组织；合法并行模块不得强编串行因果。
- 向 `T/evals/evals.json` 末尾追加一个无新 fixture 的 output eval；不修改 `analyze_abstract.py`。

**可观察 AC / 对抗样例**

1. AC：面对“构建由 A、B、C 组成的框架”，输出指出扁平并列，并给保持原事实的因果/接口蓝图。
2. AC：面对真实并行且无上游依赖的 A/B，允许按共同输入与融合点说明，不强行生成“B 修复 A”。
3. AC：原文没有组件消融或因果证据时，不把“用于/校准”升级为“带来/证明”，不新增数值、引用或模块。

## D2：章型化本章小结与证据收束（核心机制，优先级最高）

**源→当前差异**

- `S/chapter-summary.md:7-17` 区分框架章、方法章、系统章；`27-128` 给出问题、方法、模块贡献、
  验证、意义/衔接五角色及章型变体。当前 `T/references/writing/thesis-writing-guide.md:80-109`
  只有统一五角色，未说明同一角色在三类章如何落地。
- 源 `S/chapter-summary.md:65-89,150-156` 对方法章优先“模块/功能作主语”，只在系统部署的固有
  时间顺序中轻用序词；当前目标 `T/references/writing/thesis-writing-guide.md:84,94-98` 无条件示范
  “首先/其次/然后/最后”，容易把方法链写回清单体。
- 源 `S/chapter-summary.md:92-109,114-128` 要求验证陈述绑定数据源、范围、基线和证据等级；这与
  `T/references/writing/over-claim-guard.md:6-42` 一致。`S/chapter-summary.md:111-113` 的联合任务
  不漏副任务可抽象为“覆盖章内每个独立验证目标”，不保留水泥专属数值。
- `S/chapter-summary.md:100-101,130-133,165` 的“必须 2-4 数值/200-350 字/无数值必错”只作经验章
  条件参考；框架章、定性研究或证据尚缺时不得造数。目标现有 `T/references/writing/thesis-writing-guide.md:90-92`
  的“缺证据标不足”应保留。

**建议落点**

- 只细化 `T/references/writing/thesis-writing-guide.md` 的现有“正文章末小结”，不新增平行指南或脚本。
- 追加一个 output eval，覆盖方法章与系统章的序词边界、联合验证目标和证据限定；保留既有 id 22。

**可观察 AC / 对抗样例**

1. AC：方法章建议按模块主体/输入输出链衔接，系统章确有架构→部署→验证顺序时允许轻量序词。
2. AC：若章内有两个独立验证目标，小结必须逐一覆盖；没有现成量化值时标 `missing evidence`，不补数。
3. AC：保留“当前测试块/离线/观察性/单次运行”等原有限定；系统观察记录不得改写为单模型闭环收益。
4. AC：框架章不被要求伪造 RMSE，合法多段或列点在模板/导师明确要求时仍可作为例外。

## D3：文献综述的宏观综合—微观归因接口（条件参考）

**源→当前差异**

- 源 `S/literature-review.md:52-95` 提供“小节引入→主题技术块→小结”的层级；`97-121` 要求详细
  归因句交代作者、方法、对象、结果；`143-184` 要求研究间递进和局限接口。当前目标只给
  “共识→分歧→局限→空白→切入点”（`T/references/modules/literature.md:40-50`），尚未解释
  宏观主题综合与单篇证据归因如何共存。
- 不能把四要素句复制成逐作者模板：源自身 `S/literature-review.md:282-288` 也禁止机械人名流水账；
  当前 A1/A2/A3 的边界应保留（`T/scripts/analyze_literature.py:184-270`）。
- `S/literature-review.md:69-90,118-131,204-224` 的固定编号、3-4 技术块、同对象先写、必有逻辑图
  属流程工业/本论文组织惯例，作为条件选项；不得新增运行时硬门槛。

**建议落点**

- 在 `T/references/modules/literature.md` 补“主题簇层—单篇证据层—簇末综合层”三层合同，并扩充
  `T/examples/literature-review-rewrite.md:12-16` 的抽象正反例；追加一个 output eval，不改 A1-A3 正则。

**可观察 AC / 对抗样例**

1. AC：详细介绍单篇研究时能指出缺失的作者/方法/对象/结果角色，但不会要求每句机械齐全。
2. AC：连续三条完整四要素作者句仍判为流水账；按主题比较后选择性详述代表工作的段落可通过。
3. AC：作者名、研究结果或 citekey 无源证据时标 `missing evidence`，不得凭题名/BibTeX key 猜测。

## 其余源规则的边界与拒绝项

- **章引言**：源 `S/chapter-intro-two-paragraph.md:8-16,71-90` 的第 2 章免承上已在
  `T/references/writing/process-chapter-guide-zh.md:211-230` 和 `T/scripts/analyze_logic.py:573-580`
  实现。源“恰好两段、禁显式节号”与目标允许 1-2 段、两种路标形态
  （`T/references/writing/thesis-writing-guide.md:42-65`）冲突，只作论文局部 fixture。
- **绪论收束**：源 `S/problem-statement-and-chapter-arrangement.md:14-66,69-141` 的
  “现状→局限→后果→需求”和“问题→方法→产出→后续依赖”有价值，但目标已具六节漏斗、科学问题
  三要素与四方闭合（`T/references/writing/introduction-guide-zh.md:13-27,70-104`）；先不扩首批范围。
- **段落**：源 `S/paragraph-transition.md:31-103` 的固定五段只适配当前水泥论文；其通用首尾/相邻
  接口已由 P-ARC 与 S-CTX 覆盖。源 `184-203` 的全文禁序词还与章型差异冲突，不升为硬规则。
- **过程章**：源 `S/process-and-framework-chapter.md:8-70` 的可迁移骨架均已存在；具体 Y/U/S/G/K/R/Q、
  CV/MV、章号 3→6 和安全接口是局部事实，不能写入通用技能。
- **防御性表述**：源 `S/anti-defensive-hedging.md:12-14,23-27,40-58` 多处主张删去范围限定并改为
  “证明、全表最优、高保真、理论充分性”。当前契约明确修复不得靠删 caveat 或写得更肯定
  （`.trellis/spec/academic-writing-skills/defensive-ai-rhetoric-contract.md:32-50`），故拒绝。可迁移部分仅是
  “用正面对象定义替代元话语/法务腔”，且必须保留 observation、证据锚点和适用范围。
- **摘要缩略语**：源 `S/abstract.md:47-53` 的“一律不得出现英文缩写”与当前燕山官方快照
  `T/templates/yanshan.md:26-29,59,119-120,149` 的“非常用缩写不宜、非通用缩写首现注明英文原词”
  不一致，不得覆盖 `T-ABBR`。源英文摘要 500-650 词也无当前校规证据，保持 `UNVERIFIED`。

## 实施时的仓库门禁（供主计划引用）

- 公开 references/examples 变化必须同步 `docs/skills/...`、`docs/zh/skills/...` 和
  `docs/resource-manifest.json`，并跑单技能/全量 resource sync 与 docs build：
  `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md:5-7,30-50,79-87`。
- `evals/evals.json` 只追加、不重排；该文件为 CRLF canonical dump，实施时按
  `.trellis/spec/academic-writing-skills/testing-and-tooling.md:122-131,159-161` 的写入与 JSON 校验约定。
- 静态断言只能证明资源与用例存在；provider-backed 输出质量、真实论文查准率/召回率和导师可接受性
  均保持 `missing evidence / UNVERIFIED`。
