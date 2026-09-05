# 工程应用章与结果证据口径：现状差距研究

## 范围与结论

- 研究范围是七份论文项目写作规范与当前 `latex-thesis-zh` 的公开参考、路由、脚本、评测和仓库契约。
- 本文只提炼可复用的学术叙事与证据边界。章号、行业/装置名称、测点编号、项目 API、配置、时延、部署路径和现场数值均不得进入公开技能、示例或测试夹具。
- 当前最显著的缺口是：技能能识别“工程应用章”的放置方式，却没有指导如何把架构、服务、界面和运行结果写成“约束—设计目标—机制—证据”的学术论证；现有路由还把第三至第六章统一归入方法与实验，可能误路由系统实现章。
- 第二个独立小缺口是：结果分析已覆盖事实、协议、排名、轨迹、机制和证据等级，但没有区分图表展示通道、冻结聚合口径、重算范围与分层缺失率。
- 结论章和常规实验章的大部分可复用要求已经覆盖。原规范中要求删除诚实限定、把离线验证升级为工业实证或宣称绝对安全的内容，与当前证据契约冲突，必须拒绝吸收。
- 已核验当前工作树；归档任务的完成状态不等于当前实现。当前不存在拟议的通用 IR、工作流脚本或工程章检查器，不应据归档元数据假定其可用，也不应重新引入。

下文使用两个确定前缀：

- `SRC = D:/Documents/LYH/200-Learning/00博士毕业/毕业论文/thesis/.trellis/spec/writing`
- `TGT = D:/Documents/Code/Agents/academic-writing-skills/academic-writing-skills/latex-thesis-zh`
- `REPO = D:/Documents/Code/Agents/academic-writing-skills`

## 七份源文件覆盖与现状映射

### 1. `SRC/index.md`

- `index.md:3,7-9` 将这些文件限定为特定论文的中文工程写作规范；`index.md:70-73` 又要求本地论文只作结构样本，并保持引文、标签、公式、数据和证据边界。**状态：已遵循/边界依据。** 目标技能的通用性与证据约束见 `TGT/references/writing/thesis-writing-guide.md:152-163`、`TGT/references/writing/over-claim-guard.md:3-9,82-90`。
- `index.md:17,23,26-29` 给出结果、结论、实验章和工程平台章的规范索引。**状态：部分覆盖。** 当前资源表 `TGT/SKILL.md:148-154` 只有总写作、过程、方法、结果和结论指南，没有工程应用章指南。
- `index.md:74-83` 要求保持交叉引用、浮动体和编译完整。**状态：已覆盖。** 属于技能既有 LaTeX 审计边界，不构成本次新增脚本理由。

### 2. `SRC/result-analysis.md`

- `result-analysis.md:5-18,37-79` 要求锁定数据、协议、阶段、指标、来源和实验类型，并按真实次优、差值口径、组别基础、点值/边界解释。**状态：已覆盖。** 对应 `TGT/references/writing/results-analysis-guide-zh.md:18-35,67-131` 和 `TGT/references/modules/experiment.md:115-135`。
- `result-analysis.md:20-35,81-92,136-226` 建议按总体、子集、轨迹、分布、机制和部件证据组织，并明确表格、轨迹图、散点图、箱线图的角色。**状态：已覆盖。** 对应 `TGT/references/writing/results-analysis-guide-zh.md:37-65,133-190,248-304`。
- `result-analysis.md:266-289` 的证据等级和基线维度强调“证据类型决定可声称强度”。**状态：已覆盖。** 对应 `TGT/references/writing/results-analysis-guide-zh.md:192-230` 和 `TGT/references/writing/over-claim-guard.md:11-27,31-42`。
- `result-analysis.md:93-134,382-383` 区分展示通道、冻结图表/聚合、排除资产、是否重算，并要求在各采样层给出缺失率恒等式；只有所有方法在共同样本重算后才能比较排名。**状态：缺失。** 当前 `results-analysis-guide-zh.md:286-302` 的 17 项 R→RA 映射没有 `R-DISPLAY-SCOPE` 与 `R-MISSING-ID`；当前指南、`TGT/scripts/analyze_experiment.py`、相关契约和评测中也无冻结聚合/展示口径规则。
- `result-analysis.md:332-360` 的具体变量、模型和工业机理。**状态：私有，不迁移。** 仅可提炼“指标解释需说明业务/物理意义”和“机制强度不得超过证据”，现有对应为 `results-analysis-guide-zh.md:67-85,227-230`。
- `result-analysis.md:326-330` 鼓励消除防御性限定。**状态：冲突/拒绝。** `REPO/.trellis/spec/academic-writing-skills/defensive-ai-rhetoric-contract.md:32-44` 明确修辞清理不得提高确定性，缺证据机制应降级或标为待验证。

### 3. `SRC/conclusion-chapter.md`

- `conclusion-chapter.md:10-20,56-58,78-82` 使用“问题—机制—证据—价值”写贡献，并将有证据的工程系统视为可独立贡献。**状态：已覆盖至部分覆盖。** `TGT/references/writing/conclusion-guide-zh.md:16-63` 已有扁平结构和贡献四元组；工程系统何时可成为贡献仍可在新工程章指南中明确。
- `conclusion-chapter.md:86-105,116-129` 要求展望具体、数字一致、不照抄摘要且通常不新增图表/引文。**状态：已覆盖。** 对应 `TGT/references/writing/conclusion-guide-zh.md:83-125,127-178` 与 `TGT/references/modules/conclusion.md:17-35`。
- 源文件的固定“四项贡献、两项展望”和特定章节对应关系。**状态：本地格式，不硬编码。** 当前通用指南 `conclusion-guide-zh.md:16-34` 保留 3–4 项贡献、2–3 项展望的弹性更合理。
- `conclusion-chapter.md:31-35,126` 要求删除诚实边界或把离线结果升级为工业实证。**状态：冲突/拒绝。** `conclusion-guide-zh.md:64-81` 要求区分适用范围与技术缺陷，不得隐藏不利结果；`over-claim-guard.md:82-90` 禁止无部署证据的现场声明。

### 4. `SRC/chapter5-experiment-and-summary.md`

- `chapter5-experiment-and-summary.md:8-17` 要求章首将方法链映射到分层验证目标，避免空泛设问。**状态：部分覆盖。** `TGT/references/writing/thesis-writing-guide.md:42-78` 已规范章首承接和路线预告，但没有工程验证层级的专门表达。
- `chapter5-experiment-and-summary.md:19-32` 要求参数、指标和质量边界有方法或物理依据。**状态：已覆盖。** 对应 `TGT/references/writing/method-chapter-guide-zh.md:113-131` 和 `results-analysis-guide-zh.md:67-85`。
- `chapter5-experiment-and-summary.md:34-64` 的“事实—误差位置—机制”和多目标权衡、范式级比较。**状态：已覆盖。** 对应 `results-analysis-guide-zh.md:133-190,208-246`；不得吸收其要求用强断言替代证据限定的措辞。
- `chapter5-experiment-and-summary.md:66-73` 要求章末总结核心比较并过渡到工程应用。**状态：部分覆盖。** `thesis-writing-guide.md:80-109` 和 `method-chapter-guide-zh.md:145-153` 已有问题、方法、证据、价值与下章桥接；新指南可补足“从离线方法证据到工程约束”的桥接。
- `chapter5-experiment-and-summary.md:99-110` 的零防御性陈述和具体工业机理。**状态：冲突或私有，不迁移。** 保留当前 `defensive-ai-rhetoric-contract.md:6-23,32-44` 的证据校准。

### 5. `SRC/chapter6-platform-and-architecture.md`

- `chapter6-platform-and-architecture.md:8-23,31-44` 把工程章定义为研究工件向可运行系统的转换，主链为运行约束→设计原则/目标→机制/接口→分级验证。**状态：缺失核心指南。** 当前 `TGT/references/writing/method-chapter-guide-zh.md:22-43` 只识别独立工程应用、系统级验证、嵌入式现场验证或无现场验证四种放置方式，未提供叙事链。
- `chapter6-platform-and-architecture.md:48-60,64-71` 要求将软件分层和技术栈清单提升为可观察系统属性，并解释技术选择如何满足可靠性/集成约束。**状态：缺失。** 当前公开参考没有工程架构写作规则。
- `chapter6-platform-and-architecture.md:75-85` 要求以数据语义、接口边界、版本/时间基准和可追溯性描述功能，而非界面/组件罗列。**状态：缺失。** 可作为新指南的机制类别，但不得复制项目接口名称。
- `chapter6-platform-and-architecture.md:89-123` 的章节编号、具体平台分层、接口和部署示例。**状态：私有，不迁移。** 只抽取上面的论证关系。

### 6. `SRC/chapter6-platform-app-and-summary.md`

- `chapter6-platform-app-and-summary.md:11-18,41-57` 要求把界面游览改写为运行任务和操作证据，并交代环境、协议和数据来源。**状态：缺失。** 现有指南没有“界面截图不等于可用性/现场证据”的明确规则。
- `chapter6-platform-app-and-summary.md:59-77` 区分受控变量、结果指标、执行/跟踪保真度和宏观效果，并解释动态时间尺度与权衡。**状态：部分覆盖。** 一般指标和权衡由 `results-analysis-guide-zh.md:67-85,208-246` 覆盖，工程运行证据层级未覆盖。
- `chapter6-platform-app-and-summary.md:79-86` 以“架构/服务机制—现场证据—论文贡献”收束。**状态：缺失至部分覆盖。** 通用章末结构在 `thesis-writing-guide.md:80-109`，工程章闭环需新指南补足。
- `chapter6-platform-app-and-summary.md:20-35,90-129` 的现场数据、功能名称、界面位置和性能数值。**状态：私有，不迁移。** 公开夹具必须合成且去标识。

### 7. `SRC/chapter6-service-mechanism.md`

- `chapter6-service-mechanism.md:11-26,50-91` 要求把服务层写成时间/数据对齐、工件生命周期、资源隔离、运行安全和审计机制，而非 CRUD、线程池或配置项说明。**状态：缺失。** 当前技能没有服务机制写作资源或路由。
- `chapter6-service-mechanism.md:92-107` 要求说明失败边界、降级/回退和可追溯性。**状态：可吸收但必须证据化。** 新指南应要求只写源码、设计文档、日志或试验可证实的机制；不得臆造状态机、公式或绝对安全保证。
- `chapter6-service-mechanism.md:111-159` 的具体服务名称、公式、门控、时序和参考实现。**状态：私有或过度规定，不迁移。** 不建立新规则引擎、配置、检查器或通用服务架构。

## 当前路由的实证差距

- `TGT/SKILL.md:3-8,34-42` 的触发和能力描述没有工程应用/系统实现章；`SKILL.md:83-85` 只将结果分析路由到实验模块、章首章末路由到逻辑模块。
- `TGT/references/modules/routing-rules.md:60` 把第三、四、五、六章统一描述为“方法章 + 实验章”，并路由到 `experiment --per-chapter`、逻辑检查和方法章指南。章号不是可靠的章型判定，独立工程应用章可能因此误用 E-* 方法实验检查。
- `TGT/references/modules/routing-rules.md:59,61` 的过程章和结果分析已有专门路由，应保持不变。
- `TGT/scripts/analyze_experiment.py` 当前只有 E-* 与 RA-* 家族，`TGT/scripts/analyze_conclusion.py` 只有 CC-* 家族；搜索当前 `analyze_logic.py`、公开参考和评测未发现工程章专用规则。这个事实支持“新增 LLM 写作指南与路由指针”，不支持新增脚本/标志。
- `TGT/evals/evals.json:495-525,593-674,700-787` 已覆盖章末总结、过程章、方法章、防御性修辞和结果分析，但没有工程应用章输出评测；`TGT/evals/trigger_eval.json:195-198` 有结果分析正例，没有工程章正例。

## 最小规划交付

### 交付 A：工程应用章写作指南、路由与评测

1. 新增 `TGT/references/writing/engineering-application-chapter-guide-zh.md`，作为 LLM 判断与写作指南，不新增检查器、CLI 标志、配置、状态机或通用架构。
2. 指南只包含可复用主链：章型与证据盘点；运行约束→设计目标/系统属性→机制/接口→证据；章首从方法产物过渡到部署问题；架构按约束解释；服务按数据语义、时间基准、工件生命周期、资源隔离、安全边界和审计描述；界面按操作者任务和决策作用描述；章末按机制、证据和论文贡献收束。
3. 指南给出证据梯度：离线/历史回放、影子或并行观察、受控试点、生产或闭环运行。名称可按论文事实调整，但不得从低等级推断高等级；应报告环境、时长/样本、比较对象、指标、覆盖/失败范围，并区分执行/跟踪保真度、系统可靠性、业务结果和人工可用性。
4. 修改 `TGT/SKILL.md` 的能力/资源入口；修改 `TGT/references/modules/routing-rules.md:60`，按“章型”而非章号区分方法实验章与工程应用章。工程章默认使用逻辑审阅+新指南；仅其定量结果小节复用现有 `--results-analysis`，不对整章运行 E-*。
5. 按 `REPO/.trellis/spec/academic-writing-skills/docs-bilingual-resources.md:30-51,79-87` 同步 manifest、英文/中文资源页和两侧资源索引。私有论文路径与事实不得出现在公开文档。
6. 在 `TGT/evals/evals.json` 增加去标识正例和证据边界反例；在 `TGT/evals/trigger_eval.json` 增加工程论文正例与纯软件文档近邻负例。无需建立静态规则测试去复述指南内容。

### 交付 B：结果展示与聚合口径补遗

1. 只扩充 `TGT/references/writing/results-analysis-guide-zh.md` 和对应双语资源页/manifest：明确 `display_channels`、`excluded_assets`、`aggregate_channels`、`recalculated` 四项记录；删除图或通道不自动授权重算指标。
2. 增加分层缺失率口径：每层说明分母、分子、排除原因和共同样本；只有所有方法在同一有效集合重算，才比较排名或效果量。
3. 将指南内部 R→RA 清单由 17 项扩为 19 项，但保持 `results-analysis-checker-contract.md:53-55` 的固定运行时家族：本次不新增 RA 检查器规则。
4. 增加一个最小去标识输出评测，覆盖“隐藏异常图但保留冻结聚合”和“共同样本未重算不得声称排名变化”；不使用私有数据。

结论章与常规实验章不需独立子任务：可复用部分已由现有指南覆盖，工程过渡内容并入交付 A；冲突内容直接拒绝。

## 验收与评测用例

### 正向验收

- AC-A1：用户明确请求审阅中文学位论文的工程应用/系统实现章时，路由加载新指南，并按章型选择；仅因“第六章”不得自动运行 E-*。
- AC-A2：对“技术栈清单+界面游览”的输入，输出至少形成一条可追踪的“约束—设计目标—机制—证据”链，并把界面映射到操作任务或决策作用。
- AC-A3：输出准确区分离线回放、影子观察、试点和生产/闭环证据；缺少部署、硬件、现场时长或人工可用性证据时明确标为缺失，不臆造 API、指标、数值、时序或上线状态。
- AC-A4：保留真实失败边界、回退和审计机制，不以“去防御性”名义删除；机制解释的确定性不高于输入证据。
- AC-A5：工程章中的定量结果小节可复用结果分析指南，整章不新增或调用工程专用脚本；方法章、过程章、结论章的原路由不回归。
- AC-B1：当展示资产被排除而聚合冻结时，输出明确“显示范围改变、聚合未重算”，不得暗示指标或排名改变。
- AC-B2：存在通道/样本缺失时，输出分层分母、分子、原因和共同样本状态；未共同重算时拒绝跨方法排名声明。

### 负向/近邻评测

- “第三章一章一方法并含同章实验”仍走方法章指南与 `--per-chapter`，不加载工程章指南。
- “为生产软件写 API/部署 README”且没有学位论文语境，不应触发 `latex-thesis-zh`。
- 只有历史数据离线回放和界面截图时，不得改写为现场投用、闭环收益或已证实可用性。
- 输入含真实回退边界时，不得因追求积极语气删掉边界或改成绝对安全。
- 输入没有状态机、数学公式、服务接口或现场数值时，不得为了显得深入而生成这些事实。
- 删除异常曲线但没有重算日志时，不得声称均值、误差、显著性或排名已改善。

## 建议的去标识评测提示

- 正例：`这是一篇中文博士论文的独立工程应用章，目前主要是技术栈和界面操作说明。请按学术章节审阅架构、运行机制和验证叙事，保持所有 LaTeX 标签与已有证据边界。材料只证明历史回放和短期影子观察。`
  - 期望：触发技能和新指南；给出约束—目标—机制—证据链；区分两级证据；不声称试点/生产；不臆造接口、时延或工厂事实。
- 边界例：`结果图隐藏了两个异常通道，表格仍来自冻结聚合，没有共同样本重算。请把结论写得更有优势。`
  - 期望：指出展示与聚合口径不同；记录排除资产和未重算状态；拒绝排名/效果量升级；建议可执行的共同样本重算证据。
- 路由近邻：`请审阅中文论文第三章，该章是一种算法及其同章实验。`
  - 期望：方法章路由，不加载工程章指南。
- 触发负例：`请把这个后端服务的部署 README 和 REST API 文档写完整。`
  - 期望：不触发中文学位论文技能。

## 验证范围

- 结构与资源：JSON 可解析、eval ID 唯一、资源 manifest/源语言/hash/双语页面同步，运行既有资源同步契约测试。
- 行为：运行新增输出评测与 trigger eval；复跑方法章、过程章、结果分析、防御性修辞和结论章相邻用例。
- 仓库门禁：按风险运行相关 pytest 后再运行 `just ci` 与 `just doc-build`。
- 现场部署、硬件、真实服务、第三方模型、人工可用性和工业收益均为 `UNVERIFIED`；本次评测只能证明路由和文本证据边界，不能证明这些外部结果。
