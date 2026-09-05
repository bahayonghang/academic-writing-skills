# `latex-thesis-zh` 中文正文标点合成输出采样（ID 43--45）

- 采样日期：2026-09-06
- 当前 Agent：`gpt-5.6-sol / max`
- 采样性质：这是当前 Agent 对合成输入生成的实际最终回答，不是外部 provider 或独立人类盲评，也不在本文件勾选验收条件或给出 `PASS` 判定。
- 输入提取：从 `academic-writing-skills/latex-thesis-zh/evals/evals.json` 仅投影 `id`、`prompt`、`files`；`expected_output` 与 `assertions` 未输出到当前 Agent 上下文。三条输入的 `files` 均为 `[]`，未读取真实论文、调用外部模型或执行产品脚本。
- 契约说明：下列 `[LLM]` 输出中的 `Meaning-Check: PRESERVED` 仅表示待作者核对的提案，不是已经验证的事实。

## 读取的规则来源

- `academic-writing-skills/latex-thesis-zh/SKILL.md`
- `academic-writing-skills/latex-thesis-zh/references/writing/academic-style-zh.md` §5.4
- `academic-writing-skills/latex-thesis-zh/references/modules/expression.md`
- `academic-writing-skills/latex-thesis-zh/references/deai/guide.md` 的 §5.4 渐进加载指针
- `academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md`
- `academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md` 的改写契约

## ID 43

### 输入

`files: []`

```text
请按中文学位论文语句级表达规则改写这段连续正文：‘结果：表\ref{tab:ablation}显示误差由0.28降至0.21；原因是：同一设置下唯一变化为移除校正模块，误差回升至0.27；局限：目前仅有离线数据。’保留\ref{tab:ablation}、0.28、0.21、0.27和离线范围。不要把冒号、分号简单换成逗号，也不要把组件移除对照升级成绝对因果证明。请给出[LLM]改写及Changed、Protected、Meaning-Check、Risk-Flags。
```

### 实际回答

`[LLM]` 建议改写：

```latex
表\ref{tab:ablation}显示，误差由0.28降至0.21。在同一设置下，唯一变化是移除校正模块，误差回升至0.27。该组件移除对照支持校正模块与误差改善相关，但这一结论目前仅限于离线数据。

% Changed:       删除“结果：”“原因是：”“局限：”三个标签壳；用完整句拆分事实、对照与适用范围；将绝对原因表述改为当前组件移除对照能够支持的关联表述
% Protected:     \ref{tab:ablation}、0.28、0.21、0.27、离线范围
% Meaning-Check: PRESERVED
% Risk-Flags:    none
```

## ID 44

### 输入

`files: []`

```text
请改写中文博士论文中的连续正文：‘数据：数据集A包含120个样本；数据集B包含118个样本；结果：模型C在A上的MAE为0.18，在B上的MAE为0.21；结论：因此A导致模型C更稳定。’材料只有这些并列事实，没有配对样本、重复实验或因果设计。保留A、B、120、118、MAE、0.18、0.21；允许删除无证据结论，禁止补造因果、递进或实验条件。请给出[LLM]改写及四个改写契约字段。
```

### 实际回答

`[LLM]` 建议改写：

```latex
数据集A包含120个样本，数据集B包含118个样本。模型C在A上的MAE为0.18，在B上的MAE为0.21。由于材料没有配对样本、重复实验或因果设计，现有结果只能分别描述模型C在两个数据集上的指标，不能据此认定A导致模型C更稳定。

% Changed:       删除“数据：”“结果：”“结论：”标签壳和分号清单；将并列事实改为完整句；删除无证据的因果结论并明确现有证据边界
% Protected:     A、B、120、118、MAE、0.18、0.21
% Meaning-Check: PRESERVED
% Risk-Flags:    none
```

## ID 45

### 输入

`files: []`

```text
请审阅以下中文学位论文片段中的冒号和分号，只局部改写真正的标签壳：‘主要研究工作如下：当输入完整时，系统执行联合估计；当输入缺失时，系统保留上一时刻状态。关键词：状态估计；缺失数据；鲁棒性。融合向量为$h=[h_A;h_B]$。配置示例为`mode: safe; retry: 2`，说明见https://example.org/a:b。文献\cite{std}给出定义：状态保持指沿用上一时刻值。结果：离线回放完成；局限：尚无现场验证。’保留全部公式、代码、URL、引用、摘要总起句、关键词格式和复杂条件并列，不要宣称冒号或分号普遍非法或足以证明AI作者身份。若改写最后一句，请给出四个改写契约字段。
```

### 实际回答

审阅结论：除最后一句外，前文这些标点各有明确作用，应当保留。“主要研究工作如下：”用于引出后文。两个条件分句内部已有逗号，使用分号分隔合理。“关键词：状态估计；缺失数据；鲁棒性。”属于关键词格式。公式、代码、URL、引用以及定义冒号均受保护。只有最后一句连续使用“结果：”“局限：”形成标签壳，适合局部改写。冒号或分号本身不能证明文本由 AI 生成。

`[LLM]` 局部改写后的完整片段：

```latex
主要研究工作如下：当输入完整时，系统执行联合估计；当输入缺失时，系统保留上一时刻状态。关键词：状态估计；缺失数据；鲁棒性。融合向量为$h=[h_A;h_B]$。配置示例为`mode: safe; retry: 2`，说明见https://example.org/a:b。文献\cite{std}给出定义：状态保持指沿用上一时刻值。离线回放完成，尚无现场验证。

% Changed:       仅删除最后一句中的“结果：”“局限：”标签壳，并将两个事实写成一个完整句；其余标点与内容不变
% Protected:     “主要研究工作如下：”；条件分句间的分号；“关键词：状态估计；缺失数据；鲁棒性。”；$h=[h_A;h_B]$；`mode: safe; retry: 2`；https://example.org/a:b；\cite{std}；定义冒号
% Meaning-Check: PRESERVED
% Risk-Flags:    none
```
