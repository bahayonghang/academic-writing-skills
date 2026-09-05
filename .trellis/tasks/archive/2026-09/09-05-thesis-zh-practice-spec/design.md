# 设计

## 边界与依据

源 spec 是实践材料，不能覆盖科学事实或学校模板要求。现有 SKILL/references/脚本/测试
决定当前能力；[迁移分析](research/spec-transfer-analysis.md) 是本轮采纳清单。
详见 [写作证据](research/writing-evidence.md)、[工程证据](research/engineering-evidence.md)
与 [先例调研](research/prior-art-research.md)。

采用 Qiaomu 泛化与证据分层方法，沿用项目原生包结构，不生产新技能，不宣称 Library-ready。
保留 agents/openai.yaml、trigger_eval.json 和 evals.json；不迁入 interface.yaml 或 Skill IR。
历史 08-25 任务虽已归档，其设计中的 visible_prose.py/thesis_workflow.py 当前不存在，
不作为依赖，不恢复该整套架构。

## 最小机制与所有权

- 第一子任务细化摘要、小结、综述、结果口径四处既有语义指南；语义判断保持 LLM/人工，不新增关键词规则。
- 第二子任务新增一份按需工程章指南，接入现有 logic；仅确有结果分析需求时再使用 RA。
- 第三子任务只修现有 caption 识别路径；版式问题用条件参考和编译/页面检查处理。
- 用户追加的 punctuation-prose 子任务细化既有表达指南，避免冒号分号代替真实句间逻辑；保留必要语法/源码用途。
- 运行约束及数据/证据来源由给定材料决定，不根据“写得更学术”补造机制或数据。

按 evidence-writing → engineering-chapter → punctuation-prose → caption-layout 串行实施。
四者共享 SKILL.md、routing-rules、eval JSON、docs usage、README 和 manifest；
当前子任务是唯一写者，完成自身同步后交接，不覆盖前序增量。
父 R 编号属于父任务；各子任务自行定义 R/AC，并说明父需求归属。

## 泛化决策

直接保留事实不变量：不造引用/数据、声明不超证据、源码保真、失败如实报告。
段数、数字数、序词、子题注、续图、长表间距均是有适用条件的指引。
固定章号、工艺、网络、指标结果、API/数据库及路径只留在源项目。
拒绝删除真实“离线/假设/适用范围”或把“缓解”升级为“消除”等无证据改写。
跨领域案例重新构造，不复制私有正文。

## 验收分层与回退

静态资源/语料检查证明形状与同步；checker 回归证明目标行为；模型输出需保存实际响应
及逐项审阅记录；视觉通过需要实际编译/渲染页。expected_output、关键字匹配或源码存在
不能替代输出质量和版式证据。
付费 provider、真实论文盲评、独立安装和跨平台验证未运行则写 missing evidence。
规划验证已完成且用户已批准实施；产品 AC 仅在获得相应实际证据后勾选。

不增加兼容层、不改变 CLI/schema；合法双语题注减少误报是预期变化。
只回退当前子任务确切 diff，禁止 reset/clean 整树。
