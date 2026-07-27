# Module: Translation (Chinese -> English)

**Trigger**: translate, Chinese to English, bilingual polishing, terminology alignment

**Purpose**: Translate Chinese technical prose into academic English while keeping LaTeX commands and math segments intact.

## Commands

```bash
uv run python -B scripts/translate_academic.py "本文提出了一种基于Transformer的方法" --domain deep-learning
uv run python -B scripts/translate_academic.py input_zh.txt --domain industrial-control --output translation_report.md
```

## Raw Script Output

The script returns four sections:
- terminology confirmation table
- translation draft
- ambiguity notes that may need manual confirmation
- a `### Contract` block carrying the same four fields as the comment-stream modules

Protected fragments such as `\cite{...}`, `\ref{...}`, and `$...$` are masked before translation and restored verbatim in the draft; the count is reported under `Protected`.

```markdown
### Contract
- Changed: rule-based draft translation (2 glossary term(s) applied)
- Protected: 3 LaTeX/math span(s) masked and restored verbatim
- Meaning-Check: NEEDS-LLM
- Risk-Flags: not-assessed
- Envelope: goal=grammar strength=minimal
```

A rule-based draft is never a finished translation: `Meaning-Check` stays `NEEDS-LLM`, and raising claim strength while translating (e.g. rendering a hedged Chinese verb as `demonstrates`) is an over-claim — see [over-claim-guard.md](../evidence/over-claim-guard.md). Field definitions: [routing-rules.md](routing-rules.md).

## Skill-Layer Response

- Report the translated prose plus any ambiguity notes.
- Do not edit or normalize LaTeX fragments unless the user explicitly asks.
- If terminology is still ambiguous, surface the uncertainty instead of silently guessing.

Reference: [terminology.md](../writing/terminology.md), [translation-guide.md](../writing/translation-guide.md)
