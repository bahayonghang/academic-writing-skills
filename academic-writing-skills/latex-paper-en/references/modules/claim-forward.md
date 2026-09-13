# Module: Claim-Forward Check

**Trigger**: claim-forward, self-weakening, defensive tone, under-claiming, "sounds apologetic", "leads with what we don't do", hedge stacking, weak closing paragraph

**Purpose**: Detect prose that postpones or weakens the paper's own claims (disclaimers before the claim, limitation sentences ahead of the claim, self-weakening collocations, stacked hedges, negative closing paragraphs) and propose minimal reorderings or substitutions. The module never removes a limitation, an unfavorable comparison, or a non-mainline result; it changes order and wording only.

## Commands

```bash
uv run python -B scripts/check_claim_forward.py main.tex
uv run python -B scripts/check_claim_forward.py main.tex --section introduction
uv run python -B scripts/check_claim_forward.py main.tex --section conclusion --json
```

`--section` accepts the same keys and aliases as the other modules (`introduction`, `contribution`, `results`, `discussion`, `conclusion`, ...). Without `--section` every detected section is scanned. Exit code is always 0; an unknown section prints an `ERROR` line listing the available keys.

## Raw Script Output

Five `[Script]` codes. Every block carries `Original`, `Candidate`, and `Meaning-Check: NEEDS-LLM`; the candidate is a proposal for the LLM layer, not replacement text.

| Code             | Fires when                                                                                                                                                                           | Severity / Priority                                                                  | Candidate shape                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `CF-DISCLAIM`    | A paragraph's first scope denial ("We do not claim ...", "This paper does not ...") comes before its first claim                                                                     | Minor / P2 in abstract, introduction, contributions, conclusion; Info / P3 elsewhere | Claim sentence moved first, disclaimer kept after it                                                           |
| `CF-SELFWEAK`    | A self-weakening collocation on the authors' own result (`regrettably`, `still lags far behind`, `falls short of`, `of limited effect`, `only marginally`, `we were unable to`, ...) | Minor / P2                                                                           | Collocation replaced by a `prefer` template with `{placeholders}` the LLM fills from the manuscript's evidence |
| `CF-CAVEAT-POS`  | A limitation sentence precedes the claim it qualifies inside one paragraph                                                                                                           | Info / P3                                                                            | Claim and limitation swapped; the limitation is kept                                                           |
| `CF-HEDGE-STACK` | Three or more hedges on one claim sentence (`may`, `possibly`, `to some extent`, `in some cases`, ...)                                                                               | Info / P3                                                                            | First hedge kept, the rest dropped; the note asks to check the over-claim ladder before strengthening          |
| `CF-CLOSE-NEG`   | The last paragraph of a conclusion/summary ends on a negative judgment with no direction marker after it (`future work`, `we plan`, `opens`, ...)                                    | Minor / P2                                                                           | Original sentence plus `[LLM: add the direction this limitation points to]`                                    |

Summary line: `% CLAIM-FORWARD: <n> finding(s) (CF-...=k, ...)`.

## Exemptions (built into the script)

- Sentences containing `\cite`/`\citep`/`\citet`, and the following sentence when its subject is prior work (`these methods`, `prior`, `existing`, `they`, ...). Describing prior work as falling short is legitimate comparison.
- Any `Limitations` heading (`\section*{Limitations}`, `\paragraph{Limitations}`): limitations belong there, so `CF-DISCLAIM`, `CF-CAVEAT-POS`, and `CF-CLOSE-NEG` are off inside it.
- Related Work: `CF-DISCLAIM` is off ("we do not survey ..." is a scope statement).
- Bare `only`, `limited`, `not` never fire; only the collocations in `references/writing/claim-forward-terms.yaml` do.
- Math, citations, labels, and captions are stripped by the parser before matching.

## Skill-Layer Response

1. Run the script on the requested section (default: `introduction`, `contribution`, `conclusion` first; they carry the highest cost).
2. For each finding, decide with [claim-forward.md](../writing/claim-forward.md): is the sentence a claim, a scope statement, a limitation, or process narration? Reorder or substitute only; never delete the caveat.
3. Before strengthening any wording, check the evidence rung in [over-claim-guard.md](../evidence/over-claim-guard.md) ("Upward calibration"). The ladder is the ceiling; claim-forward moves wording up to the rung the evidence already earns, never past it.
4. Emit the rewrite as an `[LLM]`-layer block with the four contract fields (`Changed`, `Protected`, `Meaning-Check`, `Risk-Flags`); the `[Script]` block itself stays `NEEDS-LLM`.
5. Also apply the `[LLM]`-only judgment `CF-LOSS-FRAME` (process chronology such as "We first tried X, which failed, then ...") from the writing guide; the script does not emit it.

## Boundaries with other modules

- `deai`: `not X but Y` contrast shells and "It is worth noting" throat-clearing stay in `deai`; they are not in this module's term table. Hedge counting here is independent of `deai_check.py`, which by contract carries no hedge regex.
- `abstract`: opening-structure diagnosis (five elements) belongs to `abstract`; this module only reports a disclaimer that precedes the abstract's first claim.
- `expression`: lexical tone polish; claim-forward output is not a lexical substitution list and is not run through `--goal`/`--strength`.
- `experiment` / paper-audit claim-evidence map: whether a claim has evidence is theirs; this module assumes the evidence exists and only fixes where the claim sits and how it is worded.

## Terms table

`references/writing/claim-forward-terms.yaml` (fields: `self_weakening`, `hedges`, `disclaim_openers`, `direction_markers`, `process_openers`). The script ships an identical built-in fallback and falls back per field when the YAML is missing or a field is malformed. EN collocation precision is UNVERIFIED (synthetic fixture only); tune the YAML rather than the code.
