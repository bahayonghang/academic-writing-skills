# Module: Section Writing

**Trigger**: section writing, rewrite introduction, draft abstract, method narrative, related-work rewrite, experiment narrative, conclusion polish, paragraph roles, claim-evidence self-review

**Purpose**: Plan or rewrite one existing English paper section while preserving LaTeX syntax and separating prose proposals from source diagnostics.

This is an LLM-driven workflow. Do not run a script unless the user also asks for a diagnostic module such as `logic`, `literature`, `experiment`, or `abstract`.

## When To Use

Use this module when the user asks to:

- draft, rewrite, or reviewer-polish Abstract, Introduction, Related Work, Method, Experiments, Discussion, or Conclusion;
- design paragraph roles or a compact section outline;
- turn diagnostic findings into a rewrite blueprint;
- check whether major claims are supported by visible evidence.

Keep existing diagnostic modules for source checks:

- `abstract`: five-element abstract diagnosis and word count.
- `logic`: coherence, funnel, motivation-thread, and cross-section closure checks.
- `literature`: Related Work enumeration, comparison, and gap diagnosis.
- `experiment`: result, discussion, baseline, ablation, significance, and conclusion checks.

## Progressive Loading

Read only the active section guide plus optional flow/self-review support:

| Target | Read |
| --- | --- |
| Abstract | `references/writing/section-writing/abstract.md` |
| Introduction | `references/writing/section-writing/introduction.md` |
| Related Work | `references/writing/section-writing/related-work.md` |
| Method | `references/writing/section-writing/method.md` |
| Experiments or Discussion | `references/writing/section-writing/experiments.md` |
| Conclusion | `references/writing/section-writing/conclusion.md` |
| Paragraph flow question | `references/writing/section-writing/flow.md` |
| Reviewer-facing claim check | `references/writing/section-writing/self-review.md` |

Use `references/writing/section-writing/index.md` only when choosing among these files.

## Workflow

1. Identify the target section and current user intent: diagnosis, rewrite blueprint, paragraph-level prose, or self-review.
2. Load only the relevant section guide. Add `flow.md` when the user asks about clarity/coherence, and `self-review.md` when claims or reviewer risk matter.
3. Build a compact outline before proposing prose.
4. Assign paragraph roles before rewriting: opening, challenge, prior-work limitation, method, technical advantage, evidence, limitation, implication, or closure.
5. Preserve LaTeX anchors verbatim by default: `\cite{}`, `\ref{}`, `\label{}`, math, custom macros, table/figure anchors, and venue commands.
6. Emit a claim-evidence map for major claims. If evidence is missing, mark it as missing instead of inventing a citation, metric, baseline, or result.

## Output Contract

For section-writing tasks, return:

1. **Section objective**: one sentence naming the target reader effect.
2. **Compact outline**: 3-7 bullets or a paragraph-role table.
3. **Rewrite blueprint or prose proposal**:
   - Use blueprint when the user asks for planning or when evidence is thin.
   - Use revised prose only when the user explicitly asks for wording.
4. **Claim-evidence map**:
   - `Claim: ... | Evidence: ... | Status: supported/needs evidence/unsupported`
5. **Self-review checklist**:
   - clarity, paragraph flow, terminology consistency, unsupported claims, missing experiments/evidence, and LaTeX preservation.

## Hard Boundaries

- Do not fabricate citations, metrics, baselines, ablations, p-values, datasets, or conclusions.
- Do not change citation keys, labels, refs, math, macros, or template commands unless explicitly asked.
- Do not make a weakly supported claim sound stronger than the visible evidence.
- Do not overwrite script findings with prose enthusiasm. Keep diagnosis and proposed prose separate.
