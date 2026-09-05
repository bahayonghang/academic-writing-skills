# 设计

## 现状与规则归属

academic-writing-skills/latex-thesis-zh/references/writing/academic-style-zh.md 第五节仅有字形/中英混用规则，没有过度冒号与分号的叙述约束。
references/deai/guide.md 已识别“冒号讲义腔”；references/deai/pattern-clusters.md 明确单个标点不能构成 finding。沿用这些边界，不新增语义检测器。

## 最小修改

下述相对路径均位于 academic-writing-skills/latex-thesis-zh/。
唯一规则 owner 为 references/writing/academic-style-zh.md，第五节补“正文中的冒号、分号与句间逻辑”。
识别被标点隐藏的命题关系，按原证据写成完整句；承接词只在关系成立时使用，不把未知关系写为因果。
正文默认避免标签式冒号和以分号串起整段，优先句号分句、实质主语承接与必要从句。
不是将全部冒号分号改为逗号，不设数量限额，不声称能据此识别作者是否使用 AI。
引出列表/定义、必要复杂并列、数学 $h=[h_A;h_B]$、URL、代码、引文、关键词及模板要求保持；
摘要“主要研究工作如下：”的合法引出不与新默认冲突。

references/modules/expression.md、references/deai/guide.md 和 SKILL.md 强调并链接唯一规则源；
必要时 routing-rules.md 增补触发语。不要复制第二份完整规则，不改 E-PUNCT 或 D1 行为。
同步修改资源的 EN/ZH 镜像、manifest、README/README_CN 和两语技能说明，保留先前累积增量。

## 实际评测

evals/evals.json 至少追加 3 例：标签+分号堆叠正文的有证据改写；仅有并列事实不可补因果；
合理引出/复杂并列并含公式、引用、URL/代码的保留反例。trigger_eval.json 追加中文大论文冒号分号过多正例。
主 Agent 委派只读采样并审阅，保存 research/output-responses.md 与 output-evidence.md。
最终独立 trellis-check 包括本追加任务，不把 JSON assertions 当实际响应证明。
