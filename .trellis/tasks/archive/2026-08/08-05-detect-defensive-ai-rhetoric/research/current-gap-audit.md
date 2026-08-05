# 防御性 AI 机制叙事现状审计

## 样本的可泛化行为

用户给出的样本不是普通的“语气太保守”。它包含一个复合修辞动作：

1. 从已观察到的 tail disparity 跳到多个高度具体的原因或机制；
2. 用 `one hypothesis`、`may`、`could`、`is consistent with` 降低表面确定性；
3. 没有为每个原因给出局部证据或区分这些原因的分析；
4. 最后用 `the present comparison does not verify these mechanisms` 整体撤回。

领域中立的定义是：**证据稀疏的多机制解释，通过 hedge 与末尾免责声明获得谨慎外观，但每项解释仍不可核查。** 这是一种 claim-evidence 结构问题，不是禁用某个短语。

## 当前已有能力

### Keep

- 三个写作 skill 都采用“先保护事实/主张/逻辑/边界，再处理 AI 结构壳”的工作流。
- 指南已把整篇结构问题标为 `[LLM]`，并有“无立场讨论”邻近类别。
- `deai_check.py` 对过度自信和未演示应用建议添加 hedge，这在各自适用范围内仍然正确。
- `paper-audit` 已有 claim strength、evidence anchor、missing evidence、allowed wording 与 forbidden wording，可承载修复结果，无需扩展 issue schema。
- over-claim guard 已有反向校准：证据足够时不应继续弱化措辞（`academic-writing-skills/paper-audit/references/OVER_CLAIM_GUARD.md:103`）。

### Gap

- 仓库内对 `does not verify these mechanisms`、`无法验证这些机制` 等目标语义没有写作/审计规则或 eval 命中；现有同词命中仅涉及引用验证或普通工具诊断。
- “适当 hedge”与“解释机制”分别正确，但没有要求每个机制绑定观察、消融、对照、引用或可区分测试。
- 指南没有明确 `may/could/可能` 只能校准 claim 强度，不能替代逐机制证据；脚本与 `[LLM]` 建议同时出现时存在过度套用风险。
- “无立场讨论”只要求作者选边，可能诱导模型把证据不足的问题误修成更肯定的主张。
- claims-vs-evidence lane 要求 missing caveat；它尚未说明 caveat 不能替代机制证据。
- output eval 只覆盖词面结构壳、overclaim、时态与一般证据映射，没有复合修辞的正反例。

## Qiaomu 泛化门槛

### 分类

- Core mechanism：逐机制 evidence anchor、推断等级与禁止升高确定性，属于跨领域事实/证据不变量。
- Optional adapter：EN、ZH、Typst 的自然语言示例和注释格式。
- Eval-only fixture：用户样本中的 JIT、tail disparity、PIFG-CDM 等领域细节。

### Keep / Adapt / Reject / Invent

- Keep：现有 claim-evidence-first、四桶保护、over-claim 反向校准与 `[LLM]` 标记。
- Adapt：把“无立场讨论”从“必须选一个观点”改为“只有证据足够才选择；否则明确机制未定”。
- Adapt：保留既有 script hedge 建议，但补上“hedge 不等于 evidence anchor”的边界。
- Reject：对 `may/could/可能/未验证` 做正则；一律删除 caveat；把推测改得更肯定。
- Invent：`观察 -> 候选解释 -> 逐项证据/区分测试 -> 推断等级 -> 最小修复` 的判断链，以及跨四个 surface 的正反例矩阵。

## Prior-Art Decision

本轮不运行外部 skill catalog discovery。原因是任务不创建 skill，也不进行 package 级重构；它是在已完成的仓库内 `academic-deai-humanization` 研究基础上补一个有明确失败样本的判断缺口。若实施阶段扩展为新的共享包、检测器或公共 skill，再按 qiaomu prior-art 流程重新研究；当前外部比较证据记为 not applicable，而不是已验证优势。

## 修复决策表

| 情形 | 结论 | 建议 |
| --- | --- | --- |
| 单一解释，有局部指标/消融/引用，措辞与证据相符 | 不标 AI 痕迹 | 保留，并保持作用范围 |
| 多个解释，每个都有证据锚点且说明如何区分 | 不按本规则标记 | 可因组织过载另提结构建议 |
| 多个具体解释无逐项证据，结尾统一声明未验证 | 标记防御性机制堆叠 | 压缩为一个最接近证据的解释；否则写“机制尚未确定” |
| 只写“观察到 X，但当前设计不能识别原因” | 不标 AI 痕迹 | 这是诚实且简洁的限制 |
| 受控干预或多组消融支持机制 | 不要求 hedge | 允许证据赚到的强措辞，并写出证据 |

## 风险

- 误把合理的 alternative hypotheses 当 AI 痕迹。缓解：要求“机制数量 + 无逐项证据 + 总括撤回”组合成立，并提供反例。
- 为了去 AI 味而过度声称。缓解：把 over-claim 反向校准与 zero-fabrication 写入同一修复契约。
- 三套指南语义漂移。缓解：用 contract test 锁核心语义，不要求中英文逐字镜像。
- 把风格问题错误升级为科学性 Major。缓解：严重度取决于它是否支撑中心结论，而不是是否“像 AI”。
