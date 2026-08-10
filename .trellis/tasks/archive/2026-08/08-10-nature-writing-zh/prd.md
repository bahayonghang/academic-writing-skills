# latex-thesis-zh 整合 nature-writing 增量

## Goal

按父任务 `research/delta-matrix.md` 的 adapt 判定,将 nature-writing 增量整合进 latex-thesis-zh。实现前先读父任务 prd.md、source-basis.md、delta-matrix.md。差量小,预计轻中量级。

## 范围(delta-matrix 映射)

### D-ZH-1 英文摘要 nature 式 [LLM] 提示项 [P0] — N3

现状更正(初版 PRD 有误):`analyze_abstract.py --bilingual` 英文摘要区域已有 B-LEN/B-ORD/B-NUM/B-ENUM/B-SEM 五项,**均为中英一致性检查**;nature 式修辞诊断(Here-we 开头缺上下文 / 末句宽泛承诺 / 无落地感)不在其中。

实现:`_run_bilingual()` 新增**一条** [LLM] Info 提示项(暂名 B-NAT,design 阶段定 ID),沿用 B-SEM 既有模式——不做正则判定,只输出候选提示文案引导 LLM 复核三条诊断。文案措辞抄父级 N3 共享契约("可能"级候选,非判定)。同步 abstract-structure.md 检查项表。

约束:analyze_abstract.py(zh 副本)已于 2026-06 退出 en+typst 哈希组,可独立修改;不引入硬词表;不加 Nature profile 参数。

### D-ZH-2 结论章局限组织顺序 [P1, doc-only] — N17

conclusion-guide-zh.md 增补一节「局限的两类与陈述顺序」:

- 区分**范围局限**(受任务设定限制,设定内有竞争力)与**技术缺陷**(关键指标落后强基线 / 不可接受权衡)
- 定位为**组织顺序指导**:局限段优先围绕范围边界(数据范围/假设/部署场景)组织
- **红线:不得用于隐去实质不利结果**——基线落后、安全/有效性权衡必须如实陈述(与 over-claim-guard 交叉引用)
- 不新增 CC-* 检查项(CC-QUANT 系 NEEDS-LLM 既有取舍勿动;本节纯文档指导)

### D-ZH-3 结果章叙事顺序核对 [P2, 核对为主] — N19

概念区分(初版 PRD 未区分):nature 六层是**结果叙事顺序**;results-analysis-guide-zh.md §七的五级阶梯是**证据强度**分级。两者不可合并。

核对:结果章叙事顺序指导(总览→验证→主结果→对比→机制→泛化,及 claim-first 小节开头的中文对应)在现有指南中是否已有等价内容:

- 已覆盖 → 收尾报告落档"已覆盖不改"
- 缺失且适配学位论文结果章 → 补独立小节,显式说明与五级证据阶梯的概念区别并交叉引用,doc-only 不加脚本项

## 非增量(禁止重复实现)

- chinese-author-workflow 修复表后四类 → over-claim-guard.md 已覆盖(delta-matrix N16)
- 反向提纲/段落单信息 → logic-coherence.md;表格精度 → check_tables.py;中英摘要一致性 → B-* 五项
- CC-QUANT 恒 NEEDS-LLM、"本文"非禁词等历史判定勿重开(见 memory)

## Acceptance Criteria

- [ ] B-NAT(或最终 ID)提示项落地:[LLM] Info、flagged=False 恒提示或按 B-SEM 同模式;有测试断言其存在与文案关键词;abstract-structure.md 检查项表同步
- [ ] analyze_abstract.py 除新提示项外零逻辑改动;其余脚本零改动(git diff 验证)
- [ ] conclusion-guide-zh.md 新节含两类区分 + 组织顺序定位 + 不得隐去不利结果红线 + over-claim-guard 交叉引用
- [ ] D-ZH-3 核对结论落档:补文档或"已覆盖不改",二选一有据
- [ ] manifest 重建 + `--skill latex-thesis-zh` 单项与全量校验通过;双语页面就位
- [ ] 行为 eval(正反各≥1):含英文摘要的 fixture 跑 --bilingual 输出含新提示;无英文摘要时不输出。未执行 provider-backed 评估标 UNVERIFIED
- [ ] `just ci` 全绿 + `just doc-build` 成功
- [ ] SKILL.md 只改 last_updated;新增/修改参考带归属声明

## Constraints / 依赖

- **在 08-10-nature-writing-en 合入后开始**(manifest 串行,父任务架构决策 4)
- D-ZH-1 文案遵循父级 N3 共享契约
- Windows 重定向 JSON 输出须 PYTHONIOENCODING=utf-8(勿全局 export)
- 红线与全仓约束见父任务 prd.md
