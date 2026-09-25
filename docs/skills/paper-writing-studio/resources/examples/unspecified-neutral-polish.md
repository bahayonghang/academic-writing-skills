# Example: Neutral Polish Without a Venue

User request:
I plan to submit these results to Journal of Cleaner Production, and the domain is energy_systems. First, polish this paragraph from the experiments section.

Inputs:

- `input_text`: the synthetic results fragment below.
- `target`: `experiments` (an alias; the canonical section name is `results`).
- `journal`: `Journal of Cleaner Production`.
- `domain`: `energy_systems`.

Profile selection and loading:

1. The request gives no explicit venue. The journal is not in `IEEE_JOURNALS` or `ELSEVIER_JOURNALS`, and the skill does not guess a profile from the journal name.
2. `energy_systems` is not a domain key that maps to a profile.
3. The skill selects `unspecified`. `selection_source` is `neutral baseline`, and `missing_evidence` is `safe venue mapping`.
   The skill loads no profile file, `profile_version` is `unresolved`, and `degraded` is `false`.

Synthetic input:

```text
It can be clearly seen from Table 2 that our method obviously outperforms the baselines, and the RMSE is reduced from 0.312 to 0.214.
```

Output example:

`text`:

```text
Table 2 shows that our method outperforms the baselines; the RMSE decreases from 0.312 to 0.214.
```

`text_compact` (`render_result` takes the first 65% of the characters of the normalized text; the cut can fall inside a word):

```text
Table 2 shows that our method outperforms the baselines; the R
```

`summary`:

```json
{
  "venue": "unspecified",
  "profile_version": "unresolved",
  "section": "results",
  "domain": null,
  "rules_applied": [],
  "patterns_used": [],
  "evidence_rows": [],
  "ai_tells_avoided": ["clearly", "obviously"],
  "untraceable_tokens": [],
  "degraded": false,
  "selection_source": "neutral baseline",
  "conflicts": [],
  "missing_evidence": ["safe venue mapping"],
  "protected_tokens": ["2", "RMSE", "0.312", "0.214"]
}
```

Key points:

- `2`, `RMSE`, `0.312`, and `0.214` stay unchanged. The comparison claim stays within the scope of Table 2.
- The skill reports the missing venue evidence and does not guess the journal style.
- If the user wants an Elsevier-style rewrite, the user must give `venue=elsevier` explicitly. That profile has routing metadata only, so the output is marked `degraded`.
