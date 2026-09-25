# Example: Rewrite an Introduction for IEEE Transactions

User request:
Rewrite this introduction in the style of IEEE Transactions on Industrial Informatics. The research field is process control. Keep the citations.

Inputs:

- `input_text`: the synthetic introduction fragment below.
- `target`: `introduction`.
- `journal`: `IEEE Transactions on Industrial Informatics`.
- `domain`: `process_control`.

Profile selection and loading:

1. The request gives no explicit venue. The journal is in the IEEE allowlist, so the skill selects `ieee`, and `selection_source` is `journal allowlist`.
2. The domain `process_control` maps to `elsevier`. The journal mapping gives a different result. By precedence, the journal wins, and the conflict goes into `conflicts`.
3. Read only `profiles/ieee.json`. The profile has routing metadata only, and the package has no IEEE corpus snapshot. Thus `degraded` is `true`,
   the missing observation evidence goes into `missing_evidence`, and `rules_applied` and `evidence_rows` are empty.
4. `patterns_used` records only the mechanism that the profile file lists, `transactions-self-reference`: the text refers to itself as "this article".

Synthetic input:

```text
In recent years, many methods have been proposed for soft sensing [1]-[4]. However, they suffer from process drift. To address this issue, this paper proposes a DAGNN model.
```

Output example:

`text`:

```text
Many soft sensing methods have been proposed [1]-[4]. However, these methods are sensitive to process drift. To address this drift, this article proposes a DAGNN model.
```

`text_compact` (`render_result` takes the first 65% of the characters of the normalized text):

```text
Many soft sensing methods have been proposed [1]-[4]. However, these methods are sensitive to process drift.
```

`summary`:

```json
{
  "venue": "ieee",
  "profile_version": "materials-ieee-2026-09-11",
  "section": "introduction",
  "domain": null,
  "rules_applied": [],
  "patterns_used": ["transactions-self-reference"],
  "evidence_rows": [],
  "ai_tells_avoided": ["In recent years"],
  "untraceable_tokens": [],
  "degraded": true,
  "selection_source": "journal allowlist",
  "conflicts": ["domain=elsevier conflicts with journal=ieee"],
  "missing_evidence": ["corpus rows for profiles/ieee.json load_order"],
  "protected_tokens": ["[1]", "[4]", "DAGNN"]
}
```

Key points:

- `[1]`, `[4]`, and `DAGNN` stay unchanged, and the citation range `[1]-[4]` does not change.
- "suffer from" becomes "are sensitive to". The output adds no performance numbers or comparison claims.
- The skill reports the conflict and does not drop it silently. If the user wants an Elsevier-style rewrite, the user must give `venue=elsevier` explicitly.
