# 示例：反驳与让步壳

用户请求：
合作者说 main.tex 的 Results 与 Discussion 读起来像防御性写作："this does not mean that ..."、"admittedly ..."、"there is still room for improvement"。请删掉预设反驳，保留每一条真实限制，并校准数据不支持的结论。

推荐模块顺序：
1. `claim-forward`（脚本检查五个 `CF-*` 码）
2. `claim-forward`（按 `references/writing/claim-forward.md` 的仅 LLM 处置）

命令：
```bash
uv run python -B $SKILL_DIR/scripts/check_claim_forward.py main.tex --section results
uv run python -B $SKILL_DIR/scripts/check_claim_forward.py main.tex --section discussion
```

脚本在这里可能零发现。四类壳处置没有脚本码，由 LLM 按写作指南应用。

预期输出：
- 每条 finding 一个 `[LLM]` 块，以处置小节标题称呼：预设反驳壳、让步后否定、过强主张与模糊让步共现、空泛谦辞。
- 指向真实差异或混杂因素的让步保留。它所维护的结论绑定到稿件中的分析，或收回到数据支持的范围，或标 `needs evidence`。
- 改后主张都不强于原文。不补造对照、分层、显著性结果、数字或限制。
- 准确的句子保持原样。零发现是合法结果。

示例块（合成）：
```latex
% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Concession that dismisses a confound
% Original: Although monthly sample volume rose from 1,600 to 2,000 and the share of samples released on time fell from 90.0% to 86.0%, this does not affect the conclusion that the protocol improved on-time release.
% Revised: Monthly sample volume rose from 1,600 to 2,000, and the share of samples released on time fell from 90.0% to 86.0%. The manuscript does not compare the added samples with the original ones, so the current data cannot show whether the protocol improved on-time release (needs evidence: on-time share reported separately for original and added sample sources).
% Changed:       main clause pulled back to what the data support; concession content kept
% Protected:     1,600; 2,000; 90.0%; 86.0%
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    understatement
```

这里置 `understatement`，是因为用户要求了校准。没有这一要求时，改写块保持原强度，过度声称作为 finding 报告。

应保持不动的边界：
- "Because all 18 managers work in one regional network, the interviews do not measure how often each cause leads to a rejection elsewhere." 这是带原因的真实证据边界。
- "Turnaround time ... does not include transport time." 这是定义性否定。
- "Although earlier audits~\cite{audit2019} report lower rejection rates, they counted only samples rejected at the bench." 这是对带引用前人工作的让步。
- 写出具体限制、其后接下一步工作的收尾句。

多个具体机制后接 "the current data cannot verify this" 属于防御性推测解释，归 `deai`，不在这里处理。
