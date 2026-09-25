# C6：方法表达、防御性说明、结构桥接、引号与标题指南

## Goal / Dependencies
承担父任务对应主题需求与通用约束，C5后串行收口公开指南。五个主题，不限定恰好五个文件。
不消费C1 banned配置；比喻表达由上下文人工判断，本轮不新增脚本词表/CF或T码。

## Confirmed Facts
- tests/contracts/test_claim_forward_contract.py:21 固定CF五个脚本码；
  academic-writing-skills/latex-thesis-zh/scripts/check_claim_forward.py:643 确有YAML读取，
  但“能加载YAML”不等于获准新码或默认新行为。
- 父research/planning-evidence记录源方法8项、三类处置和桥接要求；
  UP-MATH已做改写前后数学保护，不能因此机械把不同自然语言段落当同义。
- 既有guidance-fidelity保护句不删除；按句义补边界，不重开历史规则。

## Requirements
- R1: 方法指南新增M-CODLANG/M-FIGTEXT/M-FORMDUPE/M-SEMICOLON/N-ISOLATE/
  M-DETAILINV/M-TERMREG/M-REDUNDANT八条文档判据、正反例、处置与脚本/LLM分工。
  拆句保持数学记号多重集，指路polish --verify，不改数学。
- R2: claim-forward指南补保留边界/否定转正面/弱点作trade-off三类；
  明确未验证弱点不得改写为设计优点；比喻词只作语境例，不内置禁词表。
- R3: paragraph-roles补删除预告后的指代桥接、禁止换词复述、禁止机械改首先/其次；
  合成正反例解释合法序词的叙述作用。
- R4: abstract-structure补中文成对弯引号、英文标点与引用语义保护；
  structure-guide及introduction-guide补标题/章节安排不堆公式符号的人工检查。
- R5: SKILL/reference map/routing补五主题触发，规范方法码表和公开说明一致；
  eval覆盖路由、输出与反例，镜像/manifest同步。
- R6: 全部为文档/LLM指导，不新增CF-METAPHOR/T-QUOTE，不改任何脚本/阈值；
  既有guidance-fidelity、CF固定码、父质量门禁通过。

## Acceptance Criteria
- [ ] AC1 (R1): 8条都有判据/正反例/处置/所有者；PR-EQ-NARR与M-FORMDUPE去重，
  N-ISOLATE与M-REPRO不把必要复现信息一概删除；拆句有保持数学的例子。
- [ ] AC2 (R2): 三类均有可保留与不可改例；未验证弱点不变成优点；比喻例不作为禁词正则。
- [ ] AC3 (R3): 删除预告后代词仍有先行词；合法序词不改；换词重复不能伪装为去重。
- [ ] AC4 (R4): 中文/英文摘要引号各有正反例；标题与章节安排两处各有例，
  不用“去公式符号”授权改正文数学或受保护名词。
- [ ] AC5 (R5,R6): 五主题路由与两语文档、spec一致；所有脚本字节不变；
  test_thesis_zh_guidance_fidelity和父design门禁通过，eval结构检查不冒充真实LLM效果。

## Out of Scope
不新加词表YAML/词频脚本、不修改analyze_abstract/check_claim_forward/analyze_logic；
不迁移论文专名、原句、专属章节流程。
旧编号映射：R6.1→R1；R6.2→R2；R6.3→R3；R6.4/R6.5→R4；R6.6→R5/R6。
