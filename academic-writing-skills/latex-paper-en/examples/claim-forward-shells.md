# Example: Rebuttal and Concession Shells

User request:
My co-author says the Results and Discussion of main.tex read as defensive writing: "this does not mean that ...", "admittedly ...", "there is still room for improvement". Remove the pre-emptive rebuttals, keep every real limitation, and calibrate any conclusion the data do not support.

Recommended module sequence:
1. `claim-forward` (script pass for the five `CF-*` codes)
2. `claim-forward` (LLM-only dispositions from `references/writing/claim-forward.md`)

Commands:
```bash
uv run python -B $SKILL_DIR/scripts/check_claim_forward.py main.tex --section results
uv run python -B $SKILL_DIR/scripts/check_claim_forward.py main.tex --section discussion
```

The script may report nothing here. The four shell dispositions have no script code; the LLM applies them from the writing guide.

Expected output:
- One `[LLM]` block per finding, named by disposition heading: pre-emptive rebuttal shell, concession that dismisses a confound, over-strong claim with a vague concession, or empty modesty.
- A concession that points to a real difference or confound stays. The conclusion it was defending is bound to an analysis in the manuscript, pulled back to what the data support, or marked `needs evidence`.
- No revised claim is stronger than the source. No control, stratification, significance result, number, or limitation is invented.
- Accurate sentences stay as they are. Zero findings is a valid result.

Sample block (synthetic):
```latex
% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Concession that dismisses a confound
% Original: Although monthly sample volume rose from 1,600 to 2,000 and the share of samples released on time fell from 90.0% to 86.0%, this does not affect the conclusion that the protocol improved on-time release.
% Revised: Monthly sample volume rose from 1,600 to 2,000, and the share of samples released on time fell from 90.0% to 86.0%. The manuscript does not compare the added samples with the original ones, so the current data cannot show whether the protocol improved on-time release (needs evidence: on-time share reported separately for original and added sample sources).
% Changed:       main clause pulled back to what the data support; concession content kept
% Protected:     1,600; 2,000; 90.0%; 86.0%
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    understatement
```

The `understatement` flag is set because the user asked for calibration. Without that request, the block keeps the source strength and the over-claim is reported as a finding.

Boundary cases that stay unchanged:
- "Because all 18 managers work in one regional network, the interviews do not measure how often each cause leads to a rejection elsewhere." This is a real evidence boundary with its reason.
- "Turnaround time ... does not include transport time." This is a definitional negation.
- "Although earlier audits~\cite{audit2019} report lower rejection rates, they counted only samples rejected at the bench." This is a concession about cited prior work.
- A closing sentence that names the concrete limitation and is followed by the next step.

Several specific mechanisms followed by "the current data cannot verify this" is defensive speculative explanation and goes to `deai`, not here.
