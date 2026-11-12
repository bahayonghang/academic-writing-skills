# 主张前置写作指南（Claim-Forward）

如何陈述贡献，让读者先遇到主张再遇到 caveat，且不删除任何一条限制或不利结果。配合 `claim-forward` 模块（`references/modules/claim-forward.md`）与 `references/evidence/over-claim-guard.md` 的"向上校准"节使用。

## 唯一规则

**先主张，再范围，限制只写一次。** 每个承载贡献的段落都以贡献开头。范围（主张覆盖什么）以肯定形式紧随其后。每条限制只在读者预期的位置写一次（设计约束写在方法章，证据边界写在讨论或 Limitations 节），不再作为 hedge 重复出现在每个主张前面。

## 本指南不允许的做法

以下改法被有意拒绝。它们与过度声明保护（"是校准，不是怯懦的文风"，绝不为显得果断而删 caveat）、claim-evidence 契约以及审稿人的 cherry-picking 检查冲突：

- 删除不利对比、失败设置或非主线结果。
- 把技术缺陷改写成"范围选择"（方法在长序列上失效却写成"我们不针对长序列"）。
- 挑选让论文"不可能输"的基线或指标。
- 把动词抬到证据未支撑的档位（见过度声明保护中的确定性阶梯）。

Claim-forward 改的是**顺序与措辞**。内容不动。

## 句子功能（改前先分类）

| 功能 | 判据 | 应处位置 |
| --- | --- | --- |
| 主张 | 陈述工作取得了什么，可带数字也可不带 | 段落第一句 |
| 证据 | 指向表、图、统计量或对比 | 紧跟主张之后 |
| 范围 | 说明主张覆盖什么，用肯定表述（"on indoor benchmarks"） | 主张句内或紧随其后 |
| 限制 | 说明主张不覆盖什么或在哪里失效 | 主张之后；每条一次；或写在 Limitations |
| 过渡 | 衔接下一段 | 最后一句 |
| 过程 | 叙述作者何时尝试了什么 | 通常从结果章删除；若读者需要复现则放方法章 |

## 五步改写

1. **定位主张。** 找到陈述贡献的那句。若没有，该段在做任何其他修改之前需要先有主张（不要编造；询问作者）。
2. **主张前移。** 把它放到段内任何免责、致歉或限制之前。
3. **范围转肯定。** "We do not handle outdoor scenes" 变成附在主张上的 "on three indoor benchmarks"。只有当肯定范围已承载同样信息时才删除否定句；否则它保留在主张之后。
4. **每条限制只放一处。** 若同一 caveat 出现在摘要、引言和结果中，保留在讨论证据处以及已有 Limitations 段的位置。要删的是其余副本，不是限制本身。
5. **最小改动并复核。** 重读：每个数字、对比、caveat 是否都还在？是否有动词已高于其证据档？若有，退回一档。

**补充：修复顺序。** 五步本身不变。同一段既有过强主张又有模糊让步时（见下文 "Over-strong claim with a vague concession"），固定按三步修复：(1) 证据前置：先写支撑主张的数字、表、图或材料；(2) 按 `over-claim-guard.md` 的确定性阶梯校准主张，降到证据支撑的那一档为止；(3) 把模糊让步换成一条说明原因的具体边界。只做第 (3) 步会删掉让步而留下过强主张，不要这样改。

## 优选与不推荐句式

| 不推荐 | 优选 | 原因 |
| --- | --- | --- |
| "We do not claim generality. Our method improves accuracy by 12%." | "Our method improves accuracy by 12% on three indoor benchmarks. We do not evaluate outdoor scenes." | 先主张；范围肯定；边界保留 |
| "Regrettably, our method still lags far behind the oracle." | "Our method trails the oracle by 4.1 points on the long-tail split." | 把差距写成测量值，而不是致歉 |
| "Although the evaluation is limited to one dataset, we show a 7% gain." | "We show a 7% gain on Dataset X. Evaluation on further datasets is future work." | 限制在主张之后，并给出方向 |
| "Our approach may potentially improve robustness to some extent in some cases." | "Our approach improves robustness under occlusion (Table 3)." 或证据弱时 "Our approach may improve robustness under occlusion." | 只留一个 hedge，由证据决定 |
| "It only reaches 91% and merely matches the baseline." | "It reaches 91%, matching the baseline at one third of the cost." | 带着权衡报告数字，而不是带着 `only`/`merely` |
| "We first tried a transformer, which failed, then a CNN, which also failed, and finally ..." | "We use a hybrid encoder (Section 3.2); Appendix B reports the alternatives we evaluated." | 过程编年移出结果章（`CF-LOSS-FRAME`） |
| 结论收尾："However, the method does not handle variable frame rates." | "... does not yet handle variable frame rates; extending the buffer to asynchronous input is the next step." | 以方向收尾，判定保留 |

## 自查（改写后运行四问）

1. 每个贡献段的第一句是否是主张？
2. 每条限制是否位于它所限定的主张之后，且只出现一次？
3. 每个 `regrettably` / `merely` / `only` / `unfortunately` / `falls short` 是否已替换为测量值或肯定范围？
4. 结尾段是否在最后一条限制之后补了方向，而不是新增自我否定？

若回答任一问题需要删除某个对比、结果或 caveat，撤销该修改。

## 脚本发出的码

| 码 | 层 | 处理 |
| --- | --- | --- |
| `CF-DISCLAIM` | `[Script]` | 第 2 步（主张前移） |
| `CF-CAVEAT-POS` | `[Script]` | 第 2 步与第 4 步 |
| `CF-SELFWEAK` | `[Script]` | 用测量值替换搭配；`{placeholders}` 只从稿件中填 |
| `CF-HEDGE-STACK` | `[Script]` | 只留一个 hedge；先核对过度声明阶梯 |
| `CF-CLOSE-NEG` | `[Script]` | 补方向；判定保留 |
| `CF-LOSS-FRAME` | 仅 `[LLM]` | 把过程编年移出结果 / 结论；备选方案保留在方法章或附录 |

## 与过度声明保护的关系

过度声明保护向下校正（证据弱于措辞）。Claim-forward 向上校正（措辞弱于证据）。两者在同一阶梯相遇：claim-forward 的改写只能把动词抬到证据已支撑的档位，保护条款的反向校准清单（"何时不进行对冲"）列出了强措辞成立的情形。拿不准时，动词不动，只改顺序。

## 来源归属

改编自两个 MIT 许可的 skill，并附上面注明的拒绝项：

- Kiterlin, *anti-defensive-writing* — https://github.com/Kiterlin/anti-defensive-writing（句子功能分类、五步改写、优选/不推荐句式、"限制只写一次"）。
- Adkid-Zephyr, *anti-defensive-writing-Skill* — https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill（主张先于限制的顺序、自我削弱词表、"结论不新增自我否定"、最小改动提示词、自查问题）。其关于选择性呈现的规则（只围绕优势组织、避开赢不了的对比、删除非主线结果）不予采纳；见"本指南不允许的做法"。

## 必要限制的三类仅 LLM 处置

这三类只由 LLM 判断。不新增观察码，不建词表；不得删除不利结果。强度上限仍是上文"与过度声明保护的关系"所述。未经验证的弱点不得写成设计优势。

### 保留真实证据边界

范围：删掉该句会让读者质疑方法的合法性或证据层级。
可保留："We report agreement with expert labels on the held-out clinic only; we do not treat this agreement as evidence of diagnostic benefit."
不可改：删掉该句，只留下 "Our classifier improves diagnosis."

### 否定转为正面陈述

范围：仅当原文已支持正面说法时适用。区分必须保留。
可保留："The survey measures self-reported study time. Logged study time is analysed separately in Section 5."
不可改：把 "We do not equate self-reported and logged study time" 改写为 "Self-reported study time accurately reflects actual effort."

### 弱点写成取舍

范围：仅当稿件已把该弱点写成真实设计选择时适用。
可保留："Recall on rare classes is lower than the baseline. Section 3.4 states that the loss weights frequent classes to bound annotation cost, and rare-class recall is not a design target."
不可改：把 "rare-class recall is lower" 改写为 "the model effectively avoids over-fitting to rare classes"。未经验证的弱点不得写成设计优势。高于基线的误报率不得删除，也不得改写为 "therefore more conservative"。

### 语境词只是例子，不是词表

"Gatekeeper"、"bulletproof"、"inherently safe" 与 "theoretical upper bound" 是语境例子，不是禁词正则。上下文若已写明校验、阻断或回退，就写那个可观察机制。不要据此编制禁词表。

### 建议块

```latex
% CLAIM-FORWARD (synthetic) [Severity: Minor] [Priority: P2]: [LLM] Keep a real evidence boundary
% Problem: a limitation reads as self-weakening, but the boundary is the evidence level
% Original: We report agreement with expert labels on the held-out clinic only; we do not treat this agreement as evidence of diagnostic benefit.
% Revised: keep the sentence unchanged.
% Rationale: removing the boundary would turn label agreement into a diagnostic-benefit claim. LLM-only judgment.

% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Unverified weakness written as a design strength
% Problem: lower rare-class recall became a claimed benefit, and the unfavorable number was dropped
% Original: Rare-class recall is lower than the baseline. The false-alarm rate is higher than the baseline.
% Revised: keep both observations. Add "the loss weights frequent classes to bound annotation cost" only if the manuscript already states that design choice.
% Rationale: unverified weaknesses must not be written as design strengths; unfavorable results must not be deleted.
```

## 反驳与让步壳的四类仅 LLM 处置

这四类只由 LLM 按语境判断。不新增观察码，不建词表，也不写正则：下文的说法是语境例子，同样的词在别处可能是合理的。上面的三类处置保持不变。

四类中有两类与本指南其余内容方向相反。"Concession that dismisses a confound" 与 "Over-strong claim with a vague concession" 处理的是*强于*证据的措辞，属于过度声明保护的向下校准。凭"去掉对冲"的直觉删掉让步，会留下更强的主张。因此四类都遵守三条约束：

- 让步指向稿件中真实存在的差异或混杂因素时，绝不删除该让步。
- 改后主张不强于原文。四类都不授权抬高未经支撑的主张，也不授权删除限制、不利对比或非主线结果。
- 绝不补造对照、分层分析、显著性检验、限制或数字。稿件没有可写内容时，标 `needs evidence`。

### 预设反驳壳

范围：该句回应的异议既不来自稿件数据，也不来自所引文献，且回应本身没有带来证据、条件或范围。典型形态："This does not mean that ..."、"One should not simply conclude that ..."、"Admittedly, some may argue that ..."。壳中若带条件、范围或证据，它就是真实边界，按"保留真实证据边界"处理。
去向：存在真实混杂因素或备选解释时，把壳改写为一条说明原因的具体边界；不存在真实异议时，删去壳，保留主张且动词不变；属于定义性区分时保留（见"否定转为正面陈述"）。
可保留："In this paper, latency is the interval from request submission to the first returned result; queueing time is excluded."（定义性区分）
不可改：删壳的同时把 "reduces latency" 抬成 "substantially improves system performance"；把 "The interviews cannot tell us how often teachers actually use the tool" 当作壳删掉。该句是证据边界。

### 让步后否定

范围：让步从句指出稿件中真实存在的差异或混杂因素（分母变化、样本构成变化、测量口径变化），主句却不做分析就否定其影响。典型形态："Although X changed, this does not affect the conclusion that ..."。这是过度声称，不是自我削弱。
去向：绝不删除该让步。稿件已有分析（分层、调整、共同样本比较）时，把结论绑定到该分析并注明位置；没有分析时，把结论收回到数据支持的范围，或标 `needs evidence`。计数、比例与分母变化交给 `experiment` 模块与 `references/evidence/claim-evidence-contract.md`。
可保留："Enrolment rose from 200 to 250 and completions from 150 to 175, so the completion rate fell from 75.0% to 70.0%. All 50 new enrollees joined the part-time track; within each track the completion rate did not fall (Table 4)."（让步已由稿件中的分析回答）
不可改：删掉 "although enrolment changed" 而保留 "the redesign improved completion"；稿件未报告分层检验时补写 "stratified tests showed no significant difference"。

### 过强主张与模糊让步共现

范围：同一段既有高于其证据档的动词（"conclusively proves"、"the decisive factor"），又有模糊让步（"of course this may not hold everywhere, but overall it plays a key role to some extent"）。
去向：按五步改写之后的修复顺序处理：证据前置，按确定性阶梯校准主张，再把模糊让步换成一条说明原因的具体边界。整段报告为一条 finding。
可保留："Nine of the 14 interviewed nurses named missing handover templates as the main obstacle (Table 2). All interviewees work in one hospital, so the result reports what the nurses said, not the measured effect of each obstacle."（主张已校准，边界带原因）
不可改：只删模糊让步而保留 "conclusively proves"；把主张与让步报告为两条 finding。

### 空泛谦辞

范围：限制句既不指明对象，也不给条件或量值（"there remain certain limitations"、"there is still room for improvement"、"this work offers some reference value"），且不是已写出具体限制的收尾承接句。
去向：从稿件补出对象与条件或量值；稿件没有可写内容时标 `needs evidence`，不替作者编造限制；与已有限制重复时删去副本，保留讨论证据处或 Limitations 节中的那一份。
可保留：在展望之前写出具体限制的收尾承接句，例如 "Generalisation to multi-site deployments remains limited because all data come from one hospital; Section 6 outlines the multi-site study."
不可改：删掉唯一一处限制；写出稿件中没有的限制（例如 "the sample is small"）；把 "there is still room for improvement" 改写为 "the method is optimal"。

### 去重

- 清嗓子开头（"It is worth noting that"、"It should be emphasized that"）仍归 `deai`。同一句同时含开头语和预设反驳壳时，`deai` 只报开头语，壳由 claim-forward 处理。
- 脚本已在某主张句上报告 `CF-HEDGE-STACK`、且该句同时是让步壳时，合并为一条 finding：以壳的处置为主，hedge 计数作为佐证。
- 一个证据缺口对应一条 finding。过强主张与模糊让步共现只算一次；不要拆成一条过度声称 finding 和一条壳 finding。
- 多个具体机制后接整体撤回（"it may be A, or B; the current data cannot verify this"）仍属 `deai` 的防御性推测解释规则；不要在这里重复报告。

准确清楚的原文保持原样。零发现是合法结果；不为凑数量输出 finding，也不把稿件中未知的内容写成确定。

### 建议块

```latex
% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Over-strong claim with a vague concession
% Problem: an over-strong claim and a vague concession share one paragraph; deleting only the concession would keep "conclusively proves"
% Context: Table 2 already lists the 14 nurse interviews from one hospital and the obstacle each nurse named first.
% Original: The interviews conclusively prove that missing handover templates are the decisive obstacle. Of course, this may not hold in every ward, but overall the templates play a key role to some extent.
% Revised: Nine of the 14 interviewed nurses named missing handover templates as the main obstacle (Table 2). All interviewees work in one hospital, so the result reports what the nurses said, not the measured effect of each obstacle.
% Rationale: evidence first; "conclusively prove ... decisive" pulled back to the count in Table 2; the vague concession replaced by a boundary with its reason. The revised claim is no stronger than the source; numbers and table come from the manuscript.

% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Concession that dismisses a confound
% Problem: the concession admits a denominator change, and the main clause dismisses it without analysis
% Original: Although enrolment rose from 200 to 250 and the completion rate fell from 75.0% to 70.0%, this does not affect the conclusion that the redesign improved completion.
% Revised: Enrolment rose from 200 to 250 and the completion rate fell from 75.0% to 70.0%. The manuscript does not compare new and returning enrollees, so the current data cannot show whether the redesign improved completion (needs evidence: completion rates reported separately for new and returning enrollees).
% Rationale: the denominator change is a real confound, so the concession's content stays; with no analysis in the manuscript, the conclusion is pulled back to what the data support. No stratified result was invented. Denominator checks go to the experiment module.

% CLAIM-FORWARD (synthetic) [Severity: Minor] [Priority: P2]: [LLM] Pre-emptive rebuttal shell
% Problem: the sentence answers an objection nobody raised and adds no evidence, condition, or scope
% Original: Our method reduces mean latency from 420 ms to 310 ms. This does not mean that it suits every workload.
% Revised: Our method reduces mean latency from 420 ms to 310 ms.
% Rationale: shell deleted; claim and numbers unchanged. If the manuscript names the evaluated workloads, attach them as positive scope; if it names workloads it did not evaluate, keep that as a real boundary after the claim.

% CLAIM-FORWARD (synthetic) [Severity: Minor] [Priority: P2]: [LLM] Empty modesty
% Context: Section 5.3 already reports a higher mean error at night than in daytime.
% Original: Our method still has certain limitations and room for improvement.
% Revised: Our method has a higher mean error at night than in daytime (Section 5.3).
% Rationale: object and condition come from the result in Section 5.3. When the manuscript has nothing to write, keep the sentence and mark it `needs evidence`; do not invent a limitation and do not delete this one.
```
