# C3：引用位置、重引页码、著录提示与综述递进

## Goal / Dependencies
承担父任务对应主题需求与通用约束；C2完成后接手check_references；C5依赖本子已验收CLI。
补静态候选与人工证据流程，不把格式要求转换成伪造元数据指令。

## Confirmed Facts
- academic-writing-skills/latex-thesis-zh/scripts/bib_scan.py:160 解析BibTeX，不负责正文引用；
  不把cite扫描加到这个共享副本。
- academic-writing-skills/latex-thesis-zh/scripts/verify_bib.py:315 已要求作者数据完整、交样式显示。
  正常完整姓名不能因不是“姓大写+缩写名”被判错。
- academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py:81 已有section定位；
  5/7是来源论文阈值，不能当通用已标定质量分。
- 来源图内无页码豁免是论文作者决定，不是学院普遍例外；详见父research/planning-evidence.md。

## Requirements
- R1: --author-cite在明确作者短语与同句滞后cite之间报位置候选，不给替换文本；
  一般事实句末引用和“由文献[n]可知”不报。
- R2: --repeat-cite按装配入口识别支持的cite语法并计重复key；重复且缺有效postnote报候选。
  不自动豁免图题/综述句，不建议具体页码；复杂宏或未识别语法说明覆盖不足。
- R3: verify_bib新增--college-details，仅与GB standard组合；缺出版地/页码给候选，
  作者显示给样式核验指引；保护完整姓名、机构、复姓和重音。默认GB运行不增加输出。
- R4: --progression-density复用section，进一步>5、针对>7给Info/P3候选并标UNVERIFIED；
  仅新模式启用，无新YAML；给六类改写方向和四种段落组织说明。
- R5: 新CLI与码表、引用来源边界、完整姓名/页码保真、学校接受未核实说明及合成eval同步公开资源/spec。
- R6: 位置/计数/字段/阈值正反例、输入错误、源映射、未启用旧路径和C2组合模式均有测试。

## Acceptance Criteria
- [ ] AC1 (R1): 明确作者+等后滞后标注命中，移到作者后消失；一般事实句、非作者主语不命中；
  不确定中文姓名仅候选或覆盖不足，不宣称识别出作者事实。
- [ ] AC2 (R2): 两次同键任一无postnote命中；两次均有页码/仅一次不命中；
  空postnote、双可选参数、多键共享postnote、注释、多文件/图题分别验证，无私有豁免。
- [ ] AC3 (R3): 缺address/location或pages的支持类型有候选，齐全无缺字段候选；
  Guozhi Li等完整姓名不报不合规；只报告样式需核读；不把文章号或PDF总页数建议为页码。
- [ ] AC4 (R4): 指定section内6个进一步/8个针对报，5/7不报；section外不计；
  找不到section不回退全文冒充通过，intro-citations与本模式冲突有明确参数错误。
- [ ] AC5 (R5,R6): 文档/合成例/CLI/help/路由一致；旧引用、默认和两GB模式输出保持；
  支持范围和未覆盖明确；父design全部质量门禁通过。

## Out of Scope
不修改bib_scan/online_bib_verify，不做在线查证、BibTeX姓名缩写化、自动补页码或挪动cite；
不把图1-1或特定论文key带入公开配置。
旧编号映射：R3.1→R1；R3.2→R2；R3.3→R3；R3.4→R4；R3.5→R5；R3.6→R6。
