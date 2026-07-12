# latex-thesis-zh 摘要与结论章节优化

## Goal

基于五篇工科博士学位论文精读（`research/abstract-patterns.md`、`research/conclusion-patterns.md`）与网络最佳实践调研（`research/web-best-practices.md`），为 latex-thesis-zh 补齐**摘要与结论章的内容结构层能力**：学位论文摘要骨架诊断、中英摘要一致性、结论章写作指南与内容检查器。

## 背景与现状基线（勿重复建设）

| 层 | 已有能力 | 位置 |
|---|---|---|
| 格式硬规则 | 摘要字数（燕山博士 900~1200 可配置）、摘要禁引用、章节顺序、关键词数量/分隔符；结论字数（≤2000）、结论禁 `\cite`、结论模糊措辞 | `scripts/check_spec.py`（check_abstract_no_cite/len/order、check_conclusion_no_cite/len/hedge） |
| 摘要内容诊断 | **小论文式**五要素模型（Background/Objective/Methods/Results/Conclusion），默认 300 字上限，无学位论文骨架概念 | `scripts/analyze_abstract.py` + `references/writing/abstract-structure.md` |
| 三方闭合 | 摘要-创新点-结论错位（粗粒度）、绪论贡献在结论的回应 | `scripts/analyze_logic.py` |
| 写作指南 | thesis-writing-guide.md §摘要/创新点/总结 仅一小节；**无结论章专属指南**（绪论/方法章/过程章均已有专属 guide） | `references/writing/` |

**核心缺口**：① analyze_abstract 的五要素模型是会议论文口径，不认识博士摘要的"对象定位→痛点→总起句→编号工作段→收尾"骨架；② 中英摘要一致性完全无检查；③ 结论章无写作指南、无内容检查器（三段式、展望空话、结论抄摘要等均不查）。

## Requirements

### R1 摘要学位论文模式（analyze_abstract.py 增强）

新增学位论文骨架诊断（触发方式由 design 决定：flag 或模板自动判别），检查项对应 research 编号：

- 首句以研究对象为主语定位（abstract-patterns ★A1，5/5）
- 背景后有痛点/挑战段（★A2，5/5）
- 分点前有总起句且冒号收束（★A4，5/5）
- 主体为编号 (1)(2)… 工作段（★A5，5/5）；段落数=背景段+工作段+可选收尾段（D4）
- 工作段以问题导向短语开头（★B1，"针对…问题/鉴于…/为…"）
- 验证方式明确点名，非空泛"验证有效"（★C2：仿真/实际生产数据/实测/工业现场应用）
- 方法动词规范：提出/建立/设计/构建/研究/采用（★B4）
- 缩略语首现即定义中英全称（★E3）
- 数值指标若出现，用"约/以上/区间"稳健表述（C3，Info 级）
- 首个关键词≈研究对象/过程名（★D2，Info 级）
- 摘要不得写成目录式/背景铺陈（web A10，LLM lane）
- 博士摘要须体现创新点表述（web A3，校规硬性）

字数校验默认对齐 check_spec 的校规阈值（不再各自维护一套常量），--max-chars 仍可覆盖。

### R2 中英摘要一致性检查

- 英文 Abstract 与中文摘要逐要素/逐句对应，数值一致（abstract-patterns ★F1；web A9）
- 英摘方法句一般现在时+被动语态（★F2，联动既有 `tense-guide-zh.md`/deai 英文摘要区域门控，**不得让 deai trace 流入其他模块**）
- First/Second/Then/Finally 与"首先/其次/然后/最后"序词对齐（★F3）
- 脚本可判定部分走 [Script]，跨语种语义对应走 [LLM] lane

### R3 结论章写作指南（新建 references/writing/conclusion-guide-zh.md）

对齐既有 introduction-guide-zh.md / method-chapter-guide-zh.md 的体例，内容对应 conclusion-patterns 编号：

- 章结构：开篇承上式总述（复述问题+"首先…其次…最后"研究链，C-OPENING 5/5）→ 带导语"…如下："的 (1)(2)(3)[(4)] 贡献条（C-ENUM/C-LABEL 5/5，条数 3~4）→ 局限过渡句（C-OUTLOOK-TRANS 5/5）→ 展望 2~3 条（C-OUTLOOK-COUNT 5/5）
- 贡献条骨架："针对…问题，提出/建立/设计了…，实验/应用表明…"（C-SKELETON 5/5）
- 展望须为具体技术方向，反例=空话套话（C-OUTLOOK-SPEC 5/5；web C6 黑名单："广阔前景""值得进一步研究""有待深入"等）
- 篇幅：总结>展望（约 2:1~3:1，C-RATIO）；全章 2~4 页（C-LENGTH）
- 禁忌：不引新文献/新图表/新概念（C-NO-CITE/FIG/NEW-CONCEPT 均 5/5）、克制表述无 overclaim（C-NO-OVERCLAIM，联动既有 over-claim-guard.md）、不逐字复制摘要（C-NO-VERBATIM-ABS；web「结论≠摘要」HIT 校规）
- 分级说明：子节号 7.1/7.2（仅 1/5）、章编号风格（3/5）为 Info 级"与全文风格一致"提示，不设硬规则

同步更新 abstract-structure.md（或新建学位论文摘要节）承载 R1 的骨架模型，thesis-writing-guide.md 相应小节改为指路。

### R4 结论章内容检查器

新增脚本检查（落点由 design 决定：新 analyze_conclusion.py 或并入 analyze_logic.py），检查项：

- 三段式齐全：总结/创新点表述/展望三要素（web C1 校规硬性·HIT；C5 创新点表述）
- 展望空话黑名单 + 未来向措辞存在性（C-OUTLOOK-SPEC/FUTURE-PHRASE；黑名单维护节律对齐既有 deai 词表约定）
- 结论与摘要逐字重复检测（文本相似度 [Script] + LLM 复核；C-NO-VERBATIM-ABS、web C4）
- 结论数值与摘要/正文一致性（C-QUANT-CONSIST；结论带数值不强制，出现即校验）
- 结论不引入新图表环境（C-NO-FIG，[Script]）；新概念检测走 [LLM] lane
- 展望前有局限/承接过渡句（C-OUTLOOK-TRANS）
- 总结:展望篇幅比异常提示（C-RATIO，Info 级）

**边界**：结论禁 `\cite`、结论字数、模糊措辞已由 check_spec 承担，检查器不得重复报告（可在报告中指路 spec-check）。

### R5 路由与模块文档

- SKILL.md 路由：新增/强化"结论、总结与展望、展望、结论章"触发词与模块串行顺序；`abstract` 模块描述更新
- 新建 `references/modules/conclusion.md`；更新 `references/modules/abstract.md`（学位论文模式命令与说明）
- blind-review.md 增加一行联动：摘要/结论规范问题命中盲审"规范性"维度（web X2，Info 级）

### R6 测试与质量

- 新增/更新 fixtures 与单测（对齐既有 tests/ 结构与 conftest 常量），覆盖 R1/R2/R4 的 [Script] 检查项正反例
- `just ci` 全绿（lint + pyright basic error 数 + 全部测试）

## Constraints

1. **规则分级**：仅 ≥4/5 的 ★ 规律可作默认告警；2~3/5 的规律（如摘要收尾数值段 A6/C1、"然而"转折 A3、结论重述数值 C-QUANT）只能做 Info/建议级。样本 3/5 出自燕山、领域偏过程工业，规则文案避免写成普适硬性断言。
2. **"本文"不是禁词**：五篇摘要全部使用"本文/本论文"；第一人称检查（web A6）只针对"我/我们/笔者"，不得把"本文"列入。
3. **校规数字一律可配置**，默认取仓库既有燕山常量（博士摘要 900~1200、结论 ≤2000）；不得改动 check_spec.py 既有燕山硬规则与有意设计（title_sub_max=title_max、THU/PKU 禁七等，见项目 memory）。
4. 红线：不修改 `\cite{}`/`\ref{}`/`\label{}`/数学环境；不虚构规范条款——web 调研中标"待核实"的条款（GB/T 7713.1-2025 新条款、A9 中英一致的校规原文）落地时只能以"最佳实践/建议"口径表述，不得写成国标硬性。
5. 输出契约：diff/suggestion 块 + severity/priority + `[Script]`/`[LLM]` 溯源标签，与既有模块一致。
6. 工程约定：SKILL.md version 不 bump（仅改 last_updated）；evals.json 如需改动走 Bash python 写入；SKILL.md 表格勿被格式化 hook 重排（ROUTER_ROW_RE 契约）。

## Acceptance Criteria

- [ ] analyze_abstract.py 支持学位论文骨架模式，R1 所列 ★ 检查项均有实现与正反例测试；字数阈值与 check_spec 校规对齐
- [ ] 中英摘要一致性检查可用（序词/数值/要素对应 [Script]，语义对应 [LLM] lane 文档化）
- [ ] conclusion-guide-zh.md 落地且体例对齐既有章节指南；abstract 侧指南含学位论文骨架模型
- [ ] 结论章内容检查器覆盖 R4 检查项，与 check_spec 无重复报告
- [ ] SKILL.md 路由触发词、modules/conclusion.md、modules/abstract.md 更新到位
- [ ] 每条新检查规则在代码注释或指南中可追溯到 research/ 三份文件的编号条目（如 ★A1、C-SKELETON、web C6）
- [ ] `just ci` 全绿

## Notes

- 复杂任务：`task.py start` 前需补 `design.md`（检查器落点：新脚本 vs 并入 analyze_logic；thesis 模式触发方式；相似度算法选型）与 `implement.md`。
- 研究材料：`research/abstract-patterns.md`（A/B/C/D/E/F 编号规律 + n/5）、`research/conclusion-patterns.md`（C-* 编号规律 + n/5）、`research/web-best-practices.md`（A*/C*/X* 规则候选 + 来源强度分级）。
- web 调研多数事实来自搜索摘要片段（二手转述），标"待核实"条款落地前须回原文核对；盲审权重口径仅作背景，不写入规则。
