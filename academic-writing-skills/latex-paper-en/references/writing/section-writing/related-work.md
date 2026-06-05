# Related Work Section Writing

## Objective

Position the paper against the most relevant research lines so novelty is easy to verify and the gap feels earned, not asserted.

## Topic Design

Use 2-4 focused topic clusters:

1. mainstream methods for the task;
2. methods closest to the core idea;
3. auxiliary techniques or theory the method builds on;
4. evaluation settings or datasets when those define the gap.

## Paragraph Role Template

Each topic paragraph should contain:

1. **Topic scope**: what line of work is being discussed.
2. **Representative methods**: compact summary of shared paradigm.
3. **Comparison**: mechanism, assumption, strength, or trade-off.
4. **Limitation**: what remains unresolved for the target challenge.
5. **Bridge**: how the current paper differs without overclaiming.

## Rewrite Chain

Use this chain for rewrite blueprints:

```text
Consensus -> Disagreement -> Limitations -> Gap -> This paper
```

This chain should preserve existing citation anchors. Do not add new citations unless the user asks for literature research and provides or confirms sources.

## Safety Rules

- A citation key only proves the source is cited; it does not prove support for the exact gap claim.
- Do not hide the strongest baseline. If it is missing from the draft, flag the missing comparison instead of writing around it.
- Do not turn "few papers discuss X" into "no work has studied X" unless verified.
- Use bounded distinction language: `differs from`, `targets`, `focuses on`, `complements`, `addresses the setting of`.

## Claim-Evidence Map

For each gap or novelty claim:

```text
Claim: ...
Evidence: cited cluster / comparison dimension / missing
Status: supported/needs evidence/unsupported
Allowed wording: ...
```
