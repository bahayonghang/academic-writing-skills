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
