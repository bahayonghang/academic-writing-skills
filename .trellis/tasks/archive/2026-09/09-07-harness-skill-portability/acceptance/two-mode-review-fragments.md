# Two-mode review fragments (documentation verification)

Status: documentation verification only. These fragments are not live
multi-agent proof. Five-tool live delegation stays UNVERIFIED.

Fixture: `tests/fixtures/paper_audit/sample_paper.tex` (same small paper
snippet for both modes).

Quoted evidence used below:

- Abstract: `We claim state-of-the-art long-context reasoning with strong improvements over prior work.`
- Results: `Our method improves accuracy by 12.4 over the baseline and outperforms prior work in the main setting.`
- Appendix: `Table A reports the same metric as 10.1 under a different aggregation rule.`

## Fragment A — `native delegated`

Use this shape only when the current tool actually spawned independent
children and each exclusive lane produced its own output.

```text
Execution mode: native delegated

Overall Assessment
The abstract SOTA claim outruns the reported comparison, and the headline
12.4 gain does not reconcile with Table A 10.1. Independent child outputs
from claims_vs_evidence and notation_and_numeric_consistency both flag the
numeric mismatch.

[CONSENSUS-ALL] headline metric vs appendix
- lanes: claims_vs_evidence, notation_and_numeric_consistency
- quote: `Our method improves accuracy by 12.4 over the baseline`
- explanation: Table A reports 10.1 under a different aggregation rule.
  Independent child outputs agree on the mismatch.

[LLM] via claims_vs_evidence
- quote: `We claim state-of-the-art long-context reasoning with strong improvements over prior work.`
- explanation: Results only report a 12.4 gain in the main setting. The
  SOTA wording is not supported.
```

## Fragment B — `sequential single-agent`

Use this shape when one agent ran the same review perspectives in this
session. This is not an independent panel.

```text
Execution mode: sequential single-agent

Overall Assessment
The abstract SOTA claim outruns the reported comparison, and the headline
12.4 gain does not reconcile with Table A 10.1. This session ran
claims_vs_evidence then notation_and_numeric_consistency in one agent.

[CONSENSUS-ALL] headline metric vs appendix
- perspectives: claims_vs_evidence, notation_and_numeric_consistency
- quote: `Our method improves accuracy by 12.4 over the baseline`
- explanation: Table A reports 10.1 under a different aggregation rule.
  CONSENSUS here is cross-perspective agreement in this session. It is
  not independent-reviewer consensus evidence.

[LLM] via claims_vs_evidence
- quote: `We claim state-of-the-art long-context reasoning with strong improvements over prior work.`
- explanation: Results only report a 12.4 gain in the main setting. The
  SOTA wording is not supported.
```

## Manual check

- Sequential sample does not say `independent panel`.
- Sequential `CONSENSUS` is labeled as cross-perspective only.
- Neither sample claims a live harness spawn or a real model call.
- JSON field names and score thresholds are unchanged.
