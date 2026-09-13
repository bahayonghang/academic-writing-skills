# Module: Claim-Forward Check

**Trigger**: claim-forward, self-weakening, "reads too modest / apologetic", "says what the thesis does not do first", hedge stacking, negative closing paragraph in the conclusion, "本文不试图", "遗憾的是".

**Purpose**: Detect prose that postpones or weakens the thesis's own claims (a disclaimer before the claim, a limitation sentence ahead of the claim, self-weakening collocations, stacked hedges on one claim, a conclusion whose last paragraph ends on a negative judgment with no direction) and propose minimal reorderings or collocation substitutions. The module never deletes a limitation, an unfavorable comparison, or a non-mainline result; it changes order and wording only.

## Commands

```bash
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section introduction
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section conclusion --json
```

`--section` accepts the same English keys and Chinese chapter titles as the other modules (`introduction` / `绪论`, `contribution`, `results`, `discussion`, `conclusion` / `结论与展望`, ...). Without `--section` every detected chapter is scanned. Multi-file projects are expanded through `tex_loader` (`\input` / `\include`). The exit code is always 0; an unknown section prints an `ERROR` line listing the available keys.

## Raw Script Output

Five `[Script]` codes. Every block carries `Original`, `Candidate`, and `Meaning-Check: NEEDS-LLM`; the candidate is a proposal for the `[LLM]` layer, not replacement text.

| Code             | Fires when                                                                                                                                                                             | Severity / Priority                                                                  | Candidate shape                                                                     |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| `CF-DISCLAIM`    | The paragraph's first negative disclaimer ("本文不试图 ...", "本文并不主张 ...") comes before its first claim                                                                            | Minor / P2 in abstract, introduction, contributions, conclusion; Info / P3 elsewhere | Claim sentence moved first, disclaimer kept after it                                |
| `CF-SELFWEAK`    | A self-weakening collocation on the authors' own result (`遗憾的是`, `仍明显落后于` ungated; `效果有限`, `存在严重不足`, `并不理想`, `仅能` / `仅仅` / `未能` and similar need an own-work subject in the sentence) | Minor / P2                                                                           | Collocation replaced by a `prefer` template whose `{占位}` the LLM fills from the manuscript's evidence |
| `CF-CAVEAT-POS`  | A limitation sentence **about the authors' own work** (subjects such as 本文 / 本章 / 所提 / 该方法) precedes the claim it qualifies inside one paragraph                              | Info / P3                                                                            | Claim and limitation swapped; the limitation is kept                                |
| `CF-HEDGE-STACK` | Three or more hedges on one claim sentence (`可能`, `或许`, `在一定程度上`, `似乎`, ...)                                                                                                | Info / P3                                                                            | First hedge kept, the rest dropped; the note asks to check the over-claim ladder before strengthening |
| `CF-CLOSE-NEG`   | The **last paragraph** of a conclusion / summary chapter ends on a negative judgment with no direction marker after it (`展望`, `未来工作`, `有待`, `下一步`, ...)                        | Minor / P2                                                                           | Original sentence plus `[LLM: add the direction this limitation points to]`         |

Summary line: `% CLAIM-FORWARD: <n> finding(s) (CF-...=k, ...)`.

## Exemptions (built into the script)

- Sentences containing `\cite` / `\upcite` / `\citep` / `\citet`, and the following sentence when its subject is prior work (`该类方法`, `上述方法`, `现有方法`, `传统方法`, `文献`, `他们`, ...). Describing prior work as falling short is legitimate comparison.
- Sections whose title contains `不足` / `局限` / `研究范围` / `范围界定`: limitations belong there, so `CF-DISCLAIM`, `CF-CAVEAT-POS`, and `CF-CLOSE-NEG` are off inside them; collocations with a `subject_gate` (`仅能` / `仅仅` / `未能`) do not fire there either.
- The `related` chapter (related work / research status) turns off `CF-DISCLAIM` ("本文不综述 ..." is a scope statement).
- Problem statements of the form “然而 … 难以 … 因此本文提出 …” are not self-limitations, so `CF-CAVEAT-POS` does not fire on them (in the 5-thesis baseline this form accounted for over 90% of positional hits; it is the normal motivation structure of a Chinese thesis paragraph).
- Bare `仅`, `尚未`, `不能`, `只` never fire (`仅为 0.018` and `不仅` are numeric and additive usage; `尚未解决` is the legitimate abstract pain-point wording of T-PAIN); only the collocations in `references/writing/claim-forward-terms-zh.yaml` do. Collocations with a `subject_gate` (`效果有限`, `存在严重不足`, `存在较大差距`, `并不理想`, `差强人意`, `略显不足`, `仅能`, `仅仅`, `未能`) fire only when the sentence carries an own-work subject (本文 / 本章 / 本研究 / 所提 / 本方法 / 提出的); only the `遗憾的是` / `令人遗憾` / `仍明显落后` family is ungated.
- `有望` is not counted as a hedge in conclusion / summary chapters (outlook context is legitimate).
- Math, citation commands, labels, and captions are stripped by the parser before matching.

## Skill-Layer Response

1. Run the script on the requested chapter (default: `introduction`, `contribution`, `conclusion` first; they carry the highest cost).
2. For each finding, decide with [claim-forward-zh.md](../writing/claim-forward-zh.md): is the sentence a claim, a scope statement, a limitation, or process narration? Reorder or substitute the collocation only; never delete the caveat.
3. Before strengthening any wording, check the "Upward calibration" section of [over-claim-guard.md](../writing/over-claim-guard.md). The ladder is the ceiling: claim-forward moves wording up to the rung the evidence already earns, never past it.
4. Emit the rewrite as an `[LLM]`-layer block with the four contract fields (`Changed`, `Protected`, `Meaning-Check`, `Risk-Flags`); the `[Script]` block itself stays `NEEDS-LLM`.
5. Also apply the `[LLM]`-only judgment `CF-LOSS-FRAME` from the writing guide (process chronology such as "起初尝试 X，失败后改用 ..."); the script does not emit it.

## Boundaries with other modules

- `deai`: `不是 X 而是 Y` contrast shells and the throat-clearing "值得注意的是 / 需要指出的是" stay in `deai` and are not in this module's term table. Hedge counting here is independent of `deai_check.py`, which by contract carries no hedge regex.
- `abstract`: abstract skeleton and pain-point words (T-PAIN / T-OPEN / T-VOICE) belong to `abstract`; in the abstract this module only reports a disclaimer that precedes the first claim, not pain-point statements.
- `conclusion`: `CC-OUTLOOK-TRANS` checks "a transition sentence before the outlook", `CF-CLOSE-NEG` checks "no direction after a negative judgment"; they do not conflict — negative judgment + transition + outlook passes both. The three-part conclusion structure, contribution verbs, and empty outlook wording stay with `conclusion`.
- `expression`: `E-ABSOLUTE` handles absolute wording (the opposite direction: over-claiming vs self-weakening) and the two term tables have no overlap; claim-forward output is not a lexical substitution list and is not run through `--goal` / `--strength`.
- `experiment` / paper-audit claim-evidence map: whether a claim has evidence is theirs; this module assumes the evidence exists and only fixes where the claim sits and how it is worded.

## Terms table

`references/writing/claim-forward-terms-zh.yaml` (fields: `self_weakening` (with the ZH-specific `subject_gate`), `hedges`, `disclaim_openers`, `direction_markers`, `process_openers`, `limitation_section_titles`). The script ships an identical built-in fallback and falls back per field when the YAML is missing or a field is malformed. The term baseline comes from 5 private doctoral theses (research only, not in tests) and collocation precision was tuned against it; tune the YAML rather than the code.
