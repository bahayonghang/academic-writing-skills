# Typst Method Section Adapter

> **Authoritative contract:** `latex-paper-en/references/writing/section-writing/method.md`.
> Load that file for method-interface, equation-closure, heading, evidence, and rewrite rules. This
> adapter contains only Typst syntax and command differences.

## Syntax Map

| Contract surface | Typst form | Boundary |
| --- | --- | --- |
| module subsection | `== Encoder` or `=== Alignment` | keep one technical unit per heading |
| run-in heading | `*Input contract.*` | navigation only; the following prose carries the interface |
| referenced block equation | `$ ... $ <eq:aligned>` | a label marks the block checked for a following `where` gloss |
| source comment | `// ...` | diagnostics use Typst comments and leave source tokens unchanged |

## Edge Table

Fill one row for every adjacent pair before rewriting transitions:

| Upstream module | Upstream output | Connection type | Intermediate transform | Downstream use |
| --- | --- | --- | --- | --- |
| `== Encoder` | `z_enc` | serial data | `project(z_enc)` | direct input to `== Decoder` |
| `== Candidate generator` | `candidates` | calibration/selection | threshold and budget filter | weighted supervision |

The Typst adapter is complete when the table covers every adjacent `==`/`===` pair and the authoritative
contract's producer-transform-consumer test passes for each row.

## Diagnostic

```bash
uv run python scripts/analyze_logic.py main.typ --section methods
```

The command reports `[Script]` candidates only. Review `M-HEADING`, `M-SEQWORD`, and `M-EQUATION`
against the authoritative contract, then fill the emitted `M-EDGETABLE` before editing.
