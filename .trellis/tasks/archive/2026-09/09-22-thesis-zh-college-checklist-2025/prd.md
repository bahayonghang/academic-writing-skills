# C5：学院2025逐项清单与诚实的验收分流

## Goal / Dependencies
承担父任务对应主题需求与通用约束；C2/C3的CLI验收完成，且串行C4交付后才实施。
提供111项独立状态，不能把111个状态当成111项已合规。
用户2026-09-22确认PDF页底留白保留人工，不新增--pdf、PyMuPDF依赖或PDF checker。

## Confirmed Facts
- academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:729 按五列清单逐行执行；
  module只输出提示，不执行。不能靠模板一行module自动获得专项结果。
- academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:380 的对称10%缓冲、
  第589行的文献量缓冲、第604行的已知年份分母不能直接代表学院原文。
- 来源第10/47/66/92条同时含硕士和博士规则，含博士加严标记不等于整项博士专属。
  111项多为多子句；完整映射见 research/checklist-map.md。
- 旧yanshan模板是研究生院规范，不是学院2025清单；本轮保持其文件与运行输出。

## Requirements
- R1: 新模板templates/yanshan-ee-2025.md使用YSE-001..111，五列契约与来源信息齐全；
  每条保留所有规范子句，不复制材料的论文私有批注。
- R2: 检查方式依据整个条款选择；只在现有checker足以覆盖全条时script。
  复合语义项llm，版式/PDF项manual，可定位专项module并明确剩余人工子句。
  不新增复合检查引擎；不复制yanshan阈值制造新的PASS。
- R3: 新third_person通用检查器为第88项提供词位候选，范围包括摘要/正文/结论等，
  致谢豁免；我国/我校不能因裸“我”误报。候选不等于作者人称语义定论。
- R4: 学院模板MODULE提示显式带C2/C3 flags；旧MODULE提示保持。
  第87与111项固定MANUAL，不用脚本FAIL数量推导一审/二审结论。
- R5: 文档写清研究生院/学院选型、degree差异、静态覆盖边界及人工复核；
  SKILL/routing与资源镜像、manifest、eval/spec同步。
- R6: 两学位111行、来源子句和检查方式矩阵、无学校外溢、默认四模板与checker双向锁有验证。

## Acceptance Criteria
- [ ] AC1 (R1,R2,R6): doctor/master各输出111行且ID唯一、basis逐项可追溯；
  第10/47/66/92项硕士不SKIP；第90项博士专属；子句数量与来源映射无漏项。
- [ ] AC2 (R2,R4): 混合要求如1/3/10/12/86/89/92/93/109不因一个局部checker返回全项PASS；
  第87/111项MANUAL；规则来源无数字门限臆造。
- [ ] AC3 (R3): “我们/笔者/我认为”在适用文本有定位候选，致谢与“我国/我校”、代码/键无；
  无候选仍NEEDS-LLM说明静态范围，不将词表缺命中当第三人称证明。
- [ ] AC4 (R4,R5): 新MODULE提示含准确参数；旧四模板命令/字节输出不变；
  新flags在--help和合成CLI smoke可运行，MODULE没有被标记为已检查。
- [ ] AC5 (R5,R6): docs/spec/来源映射完整；test_spec_checklists双向锁、BANNED_NON_YS_METHODS隔离、
  两学位/固定年份测试及父design质量门禁通过。

## Out of Scope
不改旧yanshan模板；不调整旧checker阈值/缓冲；第10/92/93为人工语义验收和辅助测量，
不新增TEMPLATE_THRESHOLDS["yanshan-ee-2025"]，避免未声明的自动阈值回退。
不做PDF输入与几何、字体字号、Word模板、真实学校验收结论。
旧编号映射：R5.1→R1；R5.2/R5.4→R2；R5.3→R3/R4；R5.5→R5；R5.6→R6；R5.7→R5/R6。
