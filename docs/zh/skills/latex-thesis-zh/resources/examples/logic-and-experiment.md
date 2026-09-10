# 示例：主线逻辑与实验章节联查

用户请求：
请先检查这篇学位论文从绪论到结论的主线是不是闭合，再看看实验章节是不是更像项目汇报而不是论文讨论。

推荐模块顺序：
1. `logic`
2. `experiment`

命令：
```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex
uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex
```

说明：`analyze_logic.py` 全文档模式默认包含绪论漏斗、章节主线与 C3 绪论-结论闭合检查；
只关注单章时可加 `--section 绪论`（中文章节名与英文键均可）。

预期输出：
- 先指出绪论、贡献来源、结论之间是否错位。
- 再指出实验章节是否缺少比较、机制解释、限制讨论和未来工作。
- 两类问题分模块回报，不混成泛泛的“表达优化”。

## 用逆向提纲复核已有段落

以下为合成材料，演示人工核读，不是新增脚本输出格式。用户只要求检查时，给可定位的诊断
和处置蓝图，不改正文，也不自动移动段落。

章目标：第2章比较时序重建方法的输入假设，并推导本文问题。当前小节为 `2.1.2`。

```text
chapters/review.tex:18 [prev.tail]
下节比较上述方法对输入完整性的要求。

chapters/review.tex:24 [current]
现有时序重建方法对输入完整性的假设不同。固定采样方法要求等间隔观测，掩码建模方法显式接收缺失位置\cite{regular,masked,survey}。两类输入条件划定了本章比较的范围。

chapters/review.tex:29 [current]
方法B在数据集D上的准确率为95%，证明其在所有缺失条件下都能重建真实动态。

chapters/review.tex:33 [current]
本文界面提供深色配色和菜单折叠选项，见\ref{fig:ui}。

chapters/review.tex:38 [next.head]
本节据此分析不规则观测下的输入定义。
```

先从原段提取主题，核对“段主题→章目标”；再核对“证据→段主题”，最后决定是否需要处置：

| 源位置 | 段主题与章目标 | 可见证据及边界 | 处置与理由 |
| --- | --- | --- | --- |
| `chapters/review.tex:24` | 输入完整性假设直接服务本章比较目标 | 两类假设形成比较，综合引用保留；具体文献归因仍需核对原文 | 保留（Info/P3 [LLM]）：段内关系已成立，即使没有显式过渡词也不补“因此”；不将主题综合拆成逐篇罗列 |
| `chapters/review.tex:29` | 性能观察尚未解释输入假设差异 | 数据集D的95%仅支持当前观察，不能证明所有缺失条件或重建机制 | 收窄（Major/P1 [LLM]）：保留原数值和数据集范围，指出比较协议与机制证据缺口，不补结论 |
| `chapters/review.tex:33` | 界面偏好与本章输入假设目标没有已说明的联系 | 仅给出界面描述和图引用 | 移位提案（Minor/P2 [LLM]）：核实工程章是否需要后再考虑移动；本次不执行、不编造衔接关系 |

可按需结合[段落弧线](../references/writing/paragraph-arc-zh.md)的 `P-ARC` 观察和
[小节上下文](../references/writing/subsection-context-zh.md)的 `S-CTX` 窗口定位，形态提示
不能代替上面的语义核读。只有用户明确要求改写时才对 `current` 给出提案；`prev.tail`、
`next.head` 和 `parent_lead` 仅作证据。引用、标签、公式、术语、数字、确定性与范围都要保真，
不得因改写增添因果、实验或作者意图；移出 `current` 的操作需另有对应范围的授权。
