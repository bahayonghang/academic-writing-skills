# Example: Pre-emptive Rebuttal and Concession Shells

User request:
My advisor says chapters 4 and 5 of my thesis are defensive writing, full of "这并不意味着", "不能简单地认为", and "仍有提升空间". Remove the defensive wording and pre-emptive excuses, keep every real limitation, and calibrate the conclusions the evidence cannot support.

Recommended module sequence:
1. `claim-forward` (script check for the five `CF-*` codes)
2. `claim-forward` (LLM-only dispositions from `references/writing/claim-forward-zh.md`)

Commands:
```bash
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section results
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section discussion
```

The script may report nothing here. The four dispositions have no script code; the LLM applies them from the writing guide.

Expected output:
- One `[LLM]` block per finding, named by disposition heading: pre-emptive rebuttal shell, concession that dismisses a confound, over-strong claim with a vague concession, or empty modesty.
- A concession that points to a real difference or confound stays. The conclusion it was defending is bound to an existing analysis in the manuscript, pulled back to what the data support, or marked 【待补证】.
- No revised claim is stronger than the source; no control, stratification, significance result, number, or limitation is invented.
- Accurate and clear source text stays. Zero findings is a valid result.

Sample block (synthetic):
```latex
% 主张前置（合成）[Severity: Major] [Priority: P1]: [LLM] 让步后否定
% 原文：虽然随访登记人数由250增至320，按期完成随访的比例由84.0\%降至80.0\%，但这并不影响新提醒流程提高了随访依从性的判断。
% 修改后：随访登记人数由250增至320，按期完成随访的比例由84.0\%降至80.0\%。稿件未比较新增登记者与原有登记者的构成，现有数据不足以判断新提醒流程是否提高了随访依从性【待补证：按原有与新增登记者分别报告按期完成比例】。
% Changed:       主句收回到数据支持的范围；让步内容保留
% Protected:     250；320；84.0\%；80.0\%
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    understatement
```

`understatement` is set here because the user explicitly asked for calibration. Without that request, the rewrite block keeps the source strength and the over-claim is reported as a finding.

Boundary cases that stay unchanged:
- "受访者均来自同一城区，结果不说明各原因在其他城区的实际占比。" This is a real evidence boundary with its reason.
- "本文所称‘按期完成随访’……不包括仅发送短信提醒的情形。" This is a definitional negation.
- "虽然已有研究\cite{followup2020}报告了更高的随访完成率，但其统计口径只包含能够到院复诊的居民。" This is a concession about cited prior work.
- A conclusion-chapter transition that names a concrete limitation and is followed by the outlook, which satisfies `CC-OUTLOOK-TRANS`.

Several possible mechanisms followed by "现有数据无法验证" is defensive speculative explanation and goes to `deai`, not this module.
