# 模块：去AI编辑

**触发**：去AI、人性化、减少AI痕迹、自然书写、语气清理

**目的**：检测可见散文中可能的人工智能书写痕迹，同时保留 LaTeX 结构和技术声明。

## 命令

```bash
uv run python -B scripts/deai_check.py main.tex --section introduction
uv run python -B scripts/deai_check.py main.tex --analyze
uv run python -B scripts/deai_batch.py main.tex --all-sections
```

## 原始脚本输出

- `deai_check.py` 发出部分级分析、跟踪分数和可选的修复建议。
- `deai_batch.py`支持更广泛的跨部分批量检测。
- 这`tense`类别 （`[Script]`低）标记方法/实验/结果中的现在时报告动词，门控到这些部分；参见[时态指南.md](tense-guide.md).
- 这`overclaim`类别 （`[Script]`低）标记明确的因果/第一性/普遍性措辞；参见 [over-claim-guard.md](../evidence/over-claim-guard.md).

## 密度与预算语义

- 词项计数与分母共用同一可见正文适配器，排除注释、引用、标签、数学、图、表和算法。
- 英文 `term_thresholds` 在 C3 语料标定前仍使用 `threshold_unit: per_document`；
  未声明单位的自定义 YAML 也保留旧的绝对计数语义。
- `throat_clearing` 在全文收集段首命中，仅报告超出唯一全文预算的命中。

## 技能层响应

- 将脚本输出视为分析，而不是默认重写论文的权限。
- 返回 `% DE-AI ...` 风格的结果或简短的风险摘要，除非用户明确要求进行源代码编辑。
- 保存`\cite{}`, `\ref{}`, `\label{}`、自定义宏和数学环境。
- 在平滑散文的同时，切勿发明新的主张、指标、基线或参考文献。

## 主张证据第一的人性化

在降低 AI 语气之前，请保留学术负载：

- **事实/证据**：数字、数据集、实验、图形、表格、引文、方程和指标。
- **声明/立场**：论文的真实贡献、不确定性、设计选择和局限性。
- **逻辑**：段落角色、章节角色、主张证据图。
- **边界**：假设、范围、缺失的证据和不受支持的主张。

只有这样才能移除修辞支架，例如`not merely A, but B`, `essentially`, `the key is`, `The conclusion is:`，或模糊`this/things/factors`。在命名真实的基线、标准和证据时保持对比；否则直接声明声明。该模块不应承诺降低检测器分数或取代期刊或会议人工智能使用披露。

七类 evidence-aware H-* 模式簇及 `audit -> rewrite -> fidelity audit` 契约见
[pattern-clusters.md](../deai/pattern-clusters.md)。这些内容是 claim-local `[LLM]` 审阅提示，
不是 AI 作者身份判断或检测器分数规则。

将防御性推测解释作为 `[LLM]` finding 处理：当一个段落堆叠多个机制，随后又声明当前数据无法验证其中任何一项时，应把保留的每项机制映射到可见证据锚点或区分性检验。如果没有任何机制得到支持，直接说明机制尚未确定，并将可检验的备选解释移入未来工作。不得为了显得果断而删除限制语或强化推断。

脚本的 `hedge` / `hedge_application` 建议仍能正确校准过度自信措辞和未演示应用。`results suggest` 和 `may / could` 只能降低论断强度，不能替代逐机制证据。

## 披露义务（去AI编辑前必读）

该模块提高了可读性；它**不**消除披露义务。
如果法学硕士在论文的撰写中发挥了重要作用，那么目标地点可能会
要求您披露它（在专门的部分、清单、
致谢词或投稿信）。看
[ai-disclosure.md](../venues/ai-disclosure.md) 用于每个期刊或会议的策略矩阵。
不要将“减少人工智能痕迹”视为所需披露的替代品。

参考：[guide.md](../deai/guide.md)

## 分级模式 (`--tier`) 和 D1-D5 尺寸

`--tier {light|medium|heavy}` 是**选择加入**。如果没有它，默认输出与以前完全相同。当存在时，它：

- **尺度阈值** —`light`标记更少的项目（更宽松的上限），`heavy`标记更多（更严格的上限）；`medium`保持当前阈值；
- **启用 D1 句子长度检查** — 标记句子长度变异系数过低的部分（机器均匀节奏）；
- **用 AIGC 维度标记每个发现** D1-D5 并附上一行教学注释（为什么探测器标记该模式）。

```bash
uv run python -B scripts/deai_check.py main.tex --analyze --tier heavy
```

这五个维度是以可读性为导向的，**不**调整为逃避任何特定的检测器：D1 句子长度变化、D2 段落结构、D3 信息密度、D4 连接器频率、D5 术语上下文匹配。阈值（包括`sentence_length.cv_threshold`）仍然可以通过`references/deai/tone-thresholds.yaml`.
