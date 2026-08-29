# G2 controlled English sample review

Command:

```powershell
uv run python -B academic-writing-skills/latex-paper-en/scripts/analyze_logic.py `
  tests/fixtures/paragraph_arc_en/controlled-sample.tex `
  --section introduction --paragraph-arc
```

Observed on 2026-08-29:

- line 2 produced independent `P-ARC-LEAD` and `P-ARC-CLOSE` findings;
- line 4 produced `P-ARC-CLOSE` and the intended single-sentence `P-ARC-FLAT` finding;
- the original line 2 to line 4 interface produced `P-ARC-LINK` with four-decimal Jaccard `0.0000`;
- every block contained `[Script] P-ARC-*` and `Meaning-Check: NEEDS-LLM`;
- no replacement prose was emitted.

This review proves only that the runtime matches the committed controlled synthetic labels. No
5-10-paper target-venue corpus was available. Real-paper precision, recall, venue transfer, `N=2`,
`tau=0.0200`, the term patterns, and the borrowed organization factor remain **UNVERIFIED**.
