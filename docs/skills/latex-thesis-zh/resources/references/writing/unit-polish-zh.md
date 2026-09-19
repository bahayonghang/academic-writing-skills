# Unit-Polishing Protocol for Chinese Degree Theses

## Scope and Mode

When the user explicitly requests polishing, rewriting, or sentence improvement, produce a complete revision of one natural paragraph or one depth-3 subsection. When the user only requests checking, reviewing, or identifying problems, return diagnosis without rewriting the body. See the [polish module](../modules/polish.md) for the entry point and parameters.

Route argument or logic problems to [logic](../modules/logic.md) first. Multiple rounds follow argument/logic, sentence structure, then vocabulary/typesetting. This protocol handles only the latter two layers; it neither reorders paragraphs nor adds or removes claims. Existing `--strength minimal` permits only wording, punctuation, and clear grammar fixes; splitting/merging sentences and reordering clauses belong to `moderate`. This workflow does not use the paragraph-reordering capability of `restructure`. Do not pass edit axes to the planning/verification script.

## Five-Step Workflow

1. Run `--plan` to locate one unit and its source line range. The list is a snapshot of the current text; regenerate it before each rewrite. Read only the current unit and designated read-only neighbors, not the entire thesis.
2. Run the following three pre-rewrite diagnoses on the structured entry file, replacing the section key and retaining only findings whose source file and line range fall within the current unit. Do not run them on a bare revision fragment and then claim there are no problems. Add `logic --paragraph-arc` when needed.

```bash
uv run python $SKILL_DIR/scripts/check_style_zh.py main.tex --section introduction
uv run python $SKILL_DIR/scripts/deai_check.py main.tex --section introduction
uv run python $SKILL_DIR/scripts/check_claim_forward.py main.tex --section introduction
```

3. Draft the revision according to the preservation list and admission criteria below. Keep the current subsection's existing heading command and heading text verbatim. Neighboring context supports understanding and is never copied into the revision.
4. Save the revision to a temporary file and run `--verify --unit <id> --revised <file>`; use `--original <file>` instead for a standalone original fragment. Fix Errors and rerun verification; explain every tier B candidate. State explicitly if verification failed or has not run; never mark it as passed.
5. Deliver the revision, change notes, four-field block, and verification summary in the order below. `PASS-SCRIPT` only means the differences covered by the script did not block the proposal; causality, scope, strength, and terminology semantics still require review.

Use `--terms` to supply an existing term file when verifying. Explicitly listed term spans are excluded from `UP-STRENGTH` counts, while their count changes still produce `UP-TERM`. Unconfigured terminology and ordinary usages can still trigger strength candidates. Read each candidate's reported context to distinguish technical names and general wording from actual claim words; do not mechanically strengthen or weaken the original based on counts.

## Must Preserve

- Proper names, theory names, and variable names; never substitute terminology merely to sound more sophisticated.
- Numbers, units, experimental parameters, citation numbers, and figure/table numbers.
- Causal and correlational relationships and claim strength, including significant, nonsignificant, and possible findings; neither strengthen nor weaken them without authorization.
- Research objects, time scope, method steps, and sample parameters; add no data, references, concepts, mechanisms, or conclusions and do not broaden applicability.
- Preserve `\cite{}`, `\ref{}`, `\label{}`, math environments, and template macros verbatim. Fabricate no bibliography or experimental results and do not change protected terminology. The script's math-whitespace normalization is not permission to edit mathematics.

## Admission Criteria and Editing Preferences

Edit only verified script findings, colloquial language, grammar errors, broken inter-sentence logic, and long sentences shaped by European-language syntax. Script candidates require contextual judgment first. Leave fluent sentences alone and do not impose uniform structures. When fixing a logic gap would require a new fact, flag it with `【待补证】` for the author rather than supplying an answer.

See [paragraph arcs](paragraph-arc-zh.md) for diagnosis of one focus per paragraph and conclusion-first organization; do not alter factual relationships merely to meet a form. Prefer concrete verbs that match the actual research action, such as count, compare, identify, test, summarize, detect, or calculate. Split method prose according to the original process, retaining step order and parameters. Judge colon/semicolon logic using [Chinese academic style](academic-style-zh.md#punctuation-prose), without adding a sentence-length threshold.

Use [deai](../modules/deai.md) diagnosis to assess empty padding. Empty “综上所述” inside a paragraph may be removed, but preserve it at the opening of a chapter-end summary or conclusion chapter. Preserve “本章/本节将……” lead-ins and check their function against the [structure guide](structure-guide.md). Decide connective use by position and evidence, not a mechanical blacklist.

Keep “不仅……而且……” only when both clauses have evidence. Convert unsupported escalation or “不是……而是……” contrast into a statement supported by the original facts, without inventing another advantage. Chains of “的” and trailing metacommentary are judged by `[LLM]`; add no script category. Following [claim-forward](claim-forward-zh.md), relocate repeated disclaimers and generic limitations near the corresponding facts within the unit. Do not delete limitations, unfavorable comparisons, or secondary results, and do not directly apply that module's strengthening candidates here.

## Delivery Order

First provide the complete unit revision. Then provide “修改说明” (change notes) containing only three categories: empty expressions removed; sentence logic or structure adjusted; and locations needing evidence from the author, using the `【待补证】` marker from the [de-AI guide](../deai/guide.md). Write “none” for a category with no actual change. Do not explain unchanged content or repeat the body text.

Then provide the `[LLM]` four-field block, using the fields and closed risk set from the [routing contract](../modules/routing-rules.md):

```latex
% POLISH (source.tex:L10-L14) [Severity: Info] [Priority: P3] [LLM]: 单元润色提案
% Changed:       <实际改动，或 none>
% Protected:     <受保护内容，或 none>
% Meaning-Check: <PRESERVED | NEEDS-LLM>
% Risk-Flags:    <none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim>
```

Finally include the exact verification command, exit code, counts for each code, `BLOCK` or `PASS-SCRIPT`, and unresolved semantic issues. `[Script]` always uses `Meaning-Check: NEEDS-LLM` and emits no `Risk-Flags`; `[LLM]`'s `PRESERVED` remains a proposal for author review.

## Three Self-Checks

1. Deletion test: would deleting this sentence lose information, limitations, or evidence? If so, retain its content.
2. Neighbor comparison: did the rewrite introduce uniform sentence patterns or a style absent from the original neighbors? Preserve natural expression without extracting a reference-thesis fingerprint.
3. Strength comparison: using the [over-claim ladder](over-claim-guard.md), do causality, scope, terminology, and claim strength still match the original? Polishing does not justify either strengthening or weakening.

## Chapter and Full-Thesis Requests

List units with `--plan`; add `--section` for a chapter. Read, polish, verify, and deliver each unit in list order without producing a chapter replacement. Process subsections exceeding 1200 visible Han characters one internal natural-paragraph unit at a time. Read-only context never enters the revision. Without depth-3 headings, process natural paragraphs; do not substitute depth-2 units for subsections.

## Source Attribution

- S1: thesis-polish from graduate-thesis-polish-and-write-skill, Copyright (c) 2026 lmcgg, MIT. Adopted explicit per-pass scope, restrained editing, and the distinction between review and rewrite; adapted self-checking to the current neighboring paragraphs. Did not adopt its lead-in blacklist or reference-thesis fingerprint. This protocol adapts rules without copying implementation or source paragraphs.
- S2: [“Polishing Chinese Academic Paragraphs”](https://www.zhihu.com/question/582506176/answer/2083151703524877127), author: 大学生知识星球; source: Zhihu. Copyright belongs to the author; noncommercial republication requires attribution. Adopted factual/strength preservation, concrete research actions, and the three change-note categories. Adapted limitation handling to relocation without deletion and connective handling to position and evidence. These are paraphrased rules, not copied answer paragraphs.
