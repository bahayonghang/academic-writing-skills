# C1 设计

## 规则所有权与修改边界
R1：结果证据的实质资格继续由 results-analysis-guide-zh 的证据阶梯拥有；
over-claim-guard 只负责匹配措辞，删除消融标签/未检索 hedge 的捷径。
将 philosophy/AXES 的数字例子改成显式给定输入与可支持结论的对照，不凭空补数字。
不复制新的因果规则到多个模块。

R2：philosophy 保留粗到细修改原则，其摘要/综述/实验建议回指已有专用指南。
abstract-structure 上部 five-model 长度表明确后备模型范围，移除无来源的通用 GB/T 字数结论；
不改 thesis 模型或模板数值。例子明确区分学校约束、写作建议与材料证据。
没有定量结果的理论/工程材料保留该状态，不补实验。

R3：扩展现有 logic-and-experiment 示例，给一段有缺口、一段论证已成立的合成材料。
人工复核“段主题→章目标”和“证据→段主题”，给保留/移位/收窄理由与源位置；
已成立且无显式过渡词的段落应保留。引用现有 P-ARC/S-CTX 的边界，不新增语义扫描器。
移位是提案；用户只要求检查时输出诊断/蓝图。

## 独占文件
C1 owner：academic_writing_editor；其他并行参与者不得写这些文件。
- academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md
- academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md
- academic-writing-skills/latex-thesis-zh/references/writing/abstract-structure.md
- academic-writing-skills/latex-thesis-zh/references/modules/logic.md
- academic-writing-skills/latex-thesis-zh/examples/logic-and-experiment.md
- 上述五文件对应的 docs/skills/latex-thesis-zh/resources/ 与 docs/zh/skills/latex-thesis-zh/resources/ 镜像
- academic-writing-skills/latex-thesis-zh/evals/evals.json
- academic-writing-skills/latex-thesis-zh/evals/trigger_eval.json（仅确有缺失的自然表达追加，不为数量扩充）
- academic-writing-skills/latex-thesis-zh/evals/fixtures/guidance_fidelity.tex（新增合成输入）
- tests/contracts/test_thesis_zh_guidance_fidelity.py（新增、仅覆盖本次实质冲突与 fixture 绑定）
- 本子任务 research/ 内的输出记录/复核
manifest 与跨任务集成 spec 由父任务最后串行更新，worker 不竞争写入。

## 场景与输出评估（R4）
1. 无新数据的“可能提升”：不补数字、不提高确定性。
2. 孤立 95%：可陈述准确率，不能推导改善或长程依赖因果。
3. 标为消融但训练预算不同：指出混杂，不证明机制。
4. 受控组件移除：只在证据范围内支持贡献。
5. 充分区分性证据：保留范围内强结论，不一律改成相关。
6. 没有文献检索的首次：移除或待核，不能靠“据我们所知”保留。
7. 已给学校要求的博士摘要及非 GPU/理论章：不套通用篇幅，不补实验/GPU。
8. 主题综述和逆向提纲：保留综合引用及合法无过渡词关系，只定位需要处置的段落。

先记录本任务修改前的相关公开指南快照/散列与8例 baseline，修改后在相同输入上再采样。
执行者使用本会话可用 native agent 能力；每次只提供输入、用户请求和选定版本的必要规则，
不传 expected_output/assertions/上一轮答案；采样 agent 不继承主线程上下文
（Codex 使用 fork_turns="none"，其他平台采用等价隔离）。原始回答原样保存为 research/output-before.md
和 research/output-after.md；由独立 reviewer 对照 rubric 写 research/output-review.md，
记录 agent/model（若可得）、日期、输入与规则散列、逐项结论及保真失败。
此为 local agent response review，不是 provider benchmark 或 human blind review；
缺少模型/用量元数据明确留空并说明，禁止伪造。
无 native 能力时可保留待评估状态，但不能宣布 AC5 通过。

每例逐项检查：数字、范围/确定性、术语实体、引用/标签/公式、授权范围。
关键断言任一失败即返回修复。contract tests 只锁资源/fixture 和禁止捷径，不代替响应核读。

## 验收映射与回滚
AC1→R1 的条件化示例＋场景1/2/5；AC2→R1 的权威指针＋场景3/4/6；
AC3→R2 的体裁规则＋场景7/8；AC4→R3 示例＋场景8；AC5→R4 采样/核读；
AC6→源/双语同步与父任务 manifest 门禁。
回滚只撤本任务 diff 和对应镜像/eval 追加，不回滚其他任务文件或原有用户改动。
