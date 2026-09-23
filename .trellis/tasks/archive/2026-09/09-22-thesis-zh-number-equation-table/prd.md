# C2：学院数字、公式、题注和表格源码体例

## Goal / Dependencies
承担父任务对应主题需求与通用约束；C1完成后执行并接手 check_style_zh；C3随后接手 check_references。
C5复用本子命令提示，不在本子修改任何既有 templates/*.md。

## Confirmed Facts
- academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py:105 现有数字单位正则不含百分号/摄氏度；
  UNIT_NO_SPACE 用于既有说明，不能只改该常量便声称行为修复。
- academic-writing-skills/latex-thesis-zh/references/formatting/formula-guide.md:3 已要求校规优先，
  第34行是 AMS 推导链；当前无学院源码专项规则。
- academic-writing-skills/latex-thesis-zh/scripts/check_tables.py:65 现有 check 不含本轮表身/题注规则。
- format路由有效但缺专项；学院原文要求空格/千分空，~ 与 \, 的具体源码选择是项目约定，
  不是学院逐字条文。来源与行号见父 research/planning-evidence.md。

## Requirements
- R1: 四脚本共用 CLI 拼写 --school yanshan-ee-2025|generic，缺省 generic。
  仅学院模式启用新增规则；不借研究生院 yanshan 模板静默启用。
- R2: 学院模式定位数字与普通单位含 %/℃ 的缺间隔候选、千分空缺失/错分组；
  平面角紧贴；年份/型号等不自动定性；正文数字、数学数值与单位、表格栏位明确分流。
- R3: 编号公式引导句、末标点、续行、上式/下式与式中/其中源码体例提供候选；
  独立定义/分段/约束豁免，复杂公式不判通过，视觉对齐留人工。
- R4: 表身同上/同左、明确同单位列、中文题注标点提供候选；只处理实际中文题注；
  空白/破折号语义、题注编号后视觉间距、英文大小写由指南人工核对。
- R5: 更新 formula/number/caption/table 指南和模块路由、学校边界、源码约定归因。
  保留旧模板文件；公开两语镜像、spec、evals按父契约同步。
- R6: 新规则正反例、学院/默认隔离、C1组合开关、style冻结哈希、既有报告字段与源位置均验证。

## Acceptance Criteria
- [ ] AC1 (R1,R6): 四入口缺省与generic旧输出一致；仅学院模式有新增候选；非法school非零；
  C1的--degree-wording可与school组合，互不吞掉或复制问题。
- [ ] AC2 (R2): 50\% / 25℃ 缺间隔有候选，50~\% / 25~℃ 与平面角无；
  1004.1/0.1746报分组，1\,004.1/0.174\,6不报；2026年、RTX4090、DOI、TikZ不报确定违规。
- [ ] AC3 (R3): 单条等式的重复关系符续行有候选，关系符留前行无；
  cases/独立成组定义/约束不误报；缺引导冒号/末中文标点/上下式/式中体例各有独立正反例。
- [ ] AC4 (R4): 表身同上、中文题注末标点、同列三行相同单位有候选；
  无标点中文题注、英文句点、\bicaption第二参数、正确量/单位表头无对应候选。
- [ ] AC5 (R5,R6): 指南区分学校与AMS约定，旧yanshan/THU/PKU/GEN模板不变；
  目标测试/父design门禁通过，新增numeric-equation-table-contract与实现一致。

## Out of Scope
不增加siunitx或配置文件，不改数值精度，不做PDF几何、字体、单位换算或表格事实解释；
不用闭集年份/型号表推断语义，不把学校要求外溢到其他模板。
旧编号映射：R2.1→R1；R2.2→R2；R2.3→R3；R2.4→R4；R2.5/R2.6→R5；R2.7→R6。
